"""New capacity when a rule will not fit, and sleep that folds it back.

A rule that cannot reach the target in `policy` without pushing an old rule
under the floor gets its own slot. The slot starts as a copy of `policy`, so it
already writes the answer format, and only the new rule trains it. Old rules
live elsewhere, so the slot has nothing to protect.

Questions go to the adapter of the nearest rule, by cosine of the base model's
middle-layer state (`evo.world.skills.prompt_vector`, adapters off).

Sleep trains `policy` on every rule's own lesson. The targets are the verified
completions, not slot samples. The merge is kept only if every rule still clears
the floor in `policy` alone; then the slots are deleted.
"""

from __future__ import annotations

import random

import torch


class Router:
    def __init__(self):
        self.centroids: dict[str, torch.Tensor] = {}
        self._cache: dict[str, torch.Tensor | None] = {}

    def vector(self, evo, prompt: str) -> torch.Tensor | None:
        from evo.world.skills import prompt_vector

        if prompt not in self._cache:
            self._cache[prompt] = prompt_vector(evo, prompt)
        return self._cache[prompt]

    def add(self, evo, skill_id: str, prompts: list[str]) -> None:
        vectors = [vector for vector in (self.vector(evo, prompt) for prompt in prompts[:6]) if vector is not None]
        if vectors:
            self.centroids[skill_id] = torch.stack(vectors).mean(dim=0)

    def route(self, evo, prompt: str) -> str | None:
        from evo.world.skills import _cosine

        if not self.centroids:
            return None
        vector = self.vector(evo, prompt)
        if vector is None:
            return None
        return max(self.centroids, key=lambda skill_id: _cosine(vector, self.centroids[skill_id]))


def _open_slot(body, skill) -> str:
    from evo.model import adapter_state, add_named_adapter, load_adapter_state

    name = f"slot_{body.serial:02d}"
    body.serial += 1
    add_named_adapter(body.evo, name)
    load_adapter_state(body.evo.model, name, adapter_state(body.evo.model, "policy"))
    body.slots.append(name)
    body.home[skill.id] = name
    return name


def _close_slot(body, skill, name: str) -> None:
    body.evo.model.set_adapter("policy")
    body.evo.model.delete_adapter(name)
    body.slots.remove(name)
    body.home[skill.id] = "policy"


def grow_first(body, skill, index: int, genes, cfg: dict) -> dict | None:
    """`always`: the new rule trains its own slot and nothing else. None if the slot learned nothing or none is free."""
    from evo.plastic.life import learn

    if len(body.slots) >= int(cfg.get("max_slots", 3)):
        return None
    name = _open_slot(body, skill)
    print(f"[grow] {skill.id} gets its own slot {name}", flush=True)
    grown = learn(body, skill, index, [], genes, cfg, adapter=name)
    if grown["best_select"] > grown["birth_select"]:
        grown["grew"] = name
        return grown
    _close_slot(body, skill, name)
    print(f"[grow] {name} learned nothing, removed", flush=True)
    return None


def maybe_grow(body, skill, index: int, result: dict, genes, cfg: dict) -> dict | None:
    """`need`: a slot after policy failed. Returns the slot's learning record, or None when no slot is kept."""
    from evo.plastic.life import learn

    if genes.grow == "never" or len(body.slots) >= int(cfg.get("max_slots", 3)):
        return None
    name = _open_slot(body, skill)
    print(f"[grow] {skill.id} did not fit in policy, opening {name}", flush=True)
    grown = learn(body, skill, index, [], genes, cfg, adapter=name, lesson=result["lesson"], seen_before=result["seen"])
    # A slot that clears policy's best by two questions in sixteen is kept even below the target.
    better = grown["best_select"] >= result["best_select"] + 2.0 / 16
    if grown["reached"] or better:
        grown["grew"] = name
        grown["policy_trace"] = result["trace"]
        grown["policy_best"] = result["best_select"]
        return grown
    _close_slot(body, skill, name)
    print(f"[grow] {name} did not beat policy either, removed", flush=True)
    return None


def maybe_sleep(body, learned: list[dict], genes, cfg: dict) -> dict | None:
    """Fold every slot into `policy`. Kept only when all rules clear the floor without the slots."""
    from evo.model import adapter_state, load_adapter_state
    from evo.plastic.curriculum import split_inputs
    from evo.plastic.fastscore import exact_rate
    from evo.plastic.life import Writer, scored

    if not body.slots:
        return None
    evo = body.evo
    split = split_inputs()
    # Same floor as the keeper: a merge may cost each rule at most one question in sixteen.
    routed = scored(body, learned, which="select")["rates"]
    floors = {skill_id: min(genes.keep, rate - 1.0 / 16) for skill_id, rate in routed.items()}
    before = adapter_state(evo.model, "policy")
    pairs = [pair for row in learned for pair in row["skill"].pairs(row["lesson"])]
    writer = Writer(evo, "policy", {"mlp": genes.mlp_lr, "attn": genes.attn_lr}, max_len=int(cfg.get("max_seq_len", 256)))
    rng = random.Random(int(cfg.get("seed", 0)) * 13 + len(learned))
    rates: dict[str, float] = {}
    for passes in range(1, int(genes.sleep_passes) + 1):
        rng.shuffle(pairs)
        for start in range(0, len(pairs), genes.batch):
            writer.step(pairs[start : start + genes.batch])
        rates = {row["skill"].id: exact_rate(evo, row["skill"].pairs(split["select"]), "policy")["rate"] for row in learned}
        print(f"[sleep] pass {passes} policy-only {rates} floors {floors}", flush=True)
        if all(rates[skill_id] >= floors[skill_id] for skill_id in rates):
            merged = list(body.slots)
            evo.model.set_adapter("policy")
            for name in merged:
                evo.model.delete_adapter(name)
            body.slots = []
            for skill_id in list(body.home):
                body.home[skill_id] = "policy"
            return {"accepted": True, "passes": passes, "rates": rates, "routed": routed, "merged": merged}
    load_adapter_state(evo.model, "policy", before)
    return {"accepted": False, "passes": int(genes.sleep_passes), "rates": rates, "routed": routed, "merged": []}
