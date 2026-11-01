"""Skill slots: a new LoRA per batch of tools, routed by the model's own hidden state.

Old slots stay frozen. When the 4-bit model can run two LoRA adapters at once, the
slot is added on top of policy. Otherwise the two updates are rank-concatenated,
because PeftModel.set_adapter accepts only one name.
"""

from __future__ import annotations

import torch
import torch.nn as nn

from evo.generate import render_user
from evo.model import activate, adapter_state, blend_adapters, load_adapter_state
from evo.world.sleep import _code_pair


class SkillSlot:
    def __init__(self, name: str, tool_names: list[str], day: int):
        self.name = name
        self.tool_names = list(tool_names)
        self.day = day
        self.prototypes: list[torch.Tensor] = []
        self.pairs: list[tuple[str, str]] = []
        self.frozen = False


class SkillLibrary:
    def __init__(self, cap: int = 8):
        self.cap = cap
        self.slots: list[SkillSlot] = []
        self.correct = 0
        self.asked = 0
        self._serial = 0

    def accuracy(self) -> float | None:
        if not self.asked:
            return None
        return self.correct / self.asked

    def snapshot(self, evo) -> list[dict]:
        rows = []
        for slot in self.slots:
            rows.append(
                {
                    "name": slot.name,
                    "tool_names": list(slot.tool_names),
                    "day": slot.day,
                    "prototypes": [vector.clone() for vector in slot.prototypes],
                    "pairs": list(slot.pairs),
                    "frozen": slot.frozen,
                    "state": adapter_state(evo.model, slot.name),
                }
            )
        return rows

    def restore(self, evo, rows: list[dict]) -> None:
        self.slots = []
        self._serial = 0
        paired = getattr(evo.model, "_paired", None)
        if isinstance(paired, dict):
            paired.clear()
        for row in rows:
            load_adapter_state(evo.model, row["name"], row["state"])
            slot = SkillSlot(row["name"], row["tool_names"], row["day"])
            slot.prototypes = [vector.clone() for vector in row["prototypes"]]
            slot.pairs = list(row["pairs"])
            slot.frozen = row["frozen"]
            self.slots.append(slot)
            self._serial = max(self._serial, _slot_index(row["name"]) + 1)
            self._pair(evo, slot.name, "policy")

    def most_similar(self, evo, tools: list[dict]) -> SkillSlot | None:
        if not self.slots or not tools:
            return None
        vectors = [prompt_vector(evo, _probe_prompt(tool)) for tool in tools[:2]]
        vectors = [vector for vector in vectors if vector is not None]
        if not vectors:
            return None
        best = None
        best_score = -1.0
        for slot in self.slots:
            if not slot.prototypes:
                continue
            score = max(_cosine(vector, proto) for vector in vectors for proto in slot.prototypes)
            if score > best_score:
                best_score = score
                best = slot
        return best

    def open_slot(self, evo, tools: list[dict], day: int, core: str = "policy") -> tuple[SkillSlot, SkillSlot | None]:
        """Copy the closest frozen slot, then leave the new slot ready to train.

        Returns the new slot and the oldest slot that should be distilled if the cap is full.
        """
        from evo.model import add_named_adapter

        evict = None
        if len(self.slots) >= self.cap:
            evict = self.slots.pop(0)
        donor = self.most_similar(evo, tools)
        name = f"slot_{self._serial:02d}"
        self._serial += 1
        if name in evo.model.peft_config:
            evo.model.delete_adapter(name)
        add_named_adapter(evo, name)
        if donor is not None:
            load_adapter_state(evo.model, name, adapter_state(evo.model, donor.name))
        self._pair(evo, name, core)
        slot = SkillSlot(name, [tool["name"] for tool in tools], day)
        slot.pairs = _slot_pairs(tools)
        self.slots.append(slot)
        return slot, evict

    def remember(self, evo, slot: SkillSlot, tools: list[dict]) -> None:
        slot.pairs = _slot_pairs(tools)
        slot.prototypes = []
        for tool in tools:
            for arg in (tool.get("bind_args") or tool.get("drill_args") or [])[:2]:
                vector = prompt_vector(evo, f"Print the result of {tool['nick']} applied to {arg}.")
                if vector is not None:
                    slot.prototypes.append(vector)
        slot.frozen = True

    def choose(self, evo, task: dict) -> SkillSlot | None:
        if not self.slots:
            return None
        vector = prompt_vector(evo, task.get("prompt") or "")
        if vector is None:
            return self.slots[-1]
        best = self.slots[-1]
        best_score = -1.0
        for slot in self.slots:
            if not slot.prototypes:
                continue
            score = max(_cosine(vector, proto) for proto in slot.prototypes)
            if score > best_score:
                best_score = score
                best = slot
        names = set(task.get("tools") or [])
        self.asked += 1
        if names and names.intersection(best.tool_names):
            self.correct += 1
        elif not names:
            self.asked -= 1
        return best

    def activate(self, evo, slot: SkillSlot | None, core: str = "policy") -> str:
        if slot is None:
            return core
        if getattr(evo, "joint", False):
            self._pair(evo, slot.name, core)
            return slot.name
        return blend_adapters(evo, core, slot.name, dest="blend")

    def _pair(self, evo, name: str, core: str) -> None:
        if not getattr(evo, "joint", False):
            return
        paired = getattr(evo.model, "_paired", None)
        if not isinstance(paired, dict):
            paired = {}
            evo.model._paired = paired
        paired[name] = [core, name]


def _slot_index(name: str) -> int:
    try:
        return int(name.split("_")[-1])
    except ValueError:
        return 0


def _probe_prompt(tool: dict) -> str:
    arg = (tool.get("drill_args") or [tool.get("exam_arg")])[0]
    return f"Print the result of {tool['nick']} applied to {arg}."


def _slot_pairs(tools: list[dict]) -> list[tuple[str, str]]:
    pairs = []
    for tool in tools:
        for arg in tool.get("bind_args") or tool.get("drill_args") or []:
            pairs.append(_code_pair(f"Print the result of {tool['nick']} applied to {arg}.", f"print({tool['name']}({arg}))"))
    return pairs


def _cosine(left: torch.Tensor, right: torch.Tensor) -> float:
    denom = float(left.norm() * right.norm())
    if denom == 0:
        return 0.0
    return float(torch.dot(left.flatten(), right.flatten()) / denom)


def prompt_vector(evo, prompt: str) -> torch.Tensor | None:
    """Mean hidden state at the middle layer, with adapters off so slots stay comparable."""
    layers = _decoder_layers(evo.model)
    if layers is None or not prompt.strip():
        return None
    layer = layers[len(layers) // 2]
    box: dict = {}

    def hook(_module, _inputs, output):
        tensor = output[0] if isinstance(output, tuple) else output
        box["vector"] = tensor.detach().float().mean(dim=(0, 1)).cpu()

    handle = layer.register_forward_hook(hook)
    try:
        text, add_special = render_user(evo.tok, prompt)
        encoded = evo.tok(
            text,
            return_tensors="pt",
            add_special_tokens=add_special,
            truncation=True,
            max_length=int(evo.cfg.get("max_seq_len", 384)),
        )
        encoded = {key: value.to(evo.device) for key, value in encoded.items()}
        evo.model.eval()
        with torch.no_grad(), activate(evo.model, None):
            evo.model(**encoded)
    finally:
        handle.remove()
    return box.get("vector")


def _decoder_layers(model) -> nn.ModuleList | None:
    best = None
    for module in model.modules():
        if isinstance(module, nn.ModuleList) and (best is None or len(module) > len(best)):
            best = module
    return best
