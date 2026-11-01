"""4-bit base model with policy, memory, and scratch LoRA adapters."""

from __future__ import annotations

import gc
import os
from contextlib import contextmanager

import torch
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig


ADAPTERS = ("policy", "memory", "scratch")

LORA_SITES = {
    "attn": ["q_proj", "k_proj", "v_proj", "o_proj"],
    "delta": ["in_proj_qkv", "in_proj_z", "out_proj"],
    "mlp": ["gate_proj", "up_proj", "down_proj"],
}


def lora_targets(cfg: dict) -> list[str]:
    """Where a LoRA is allowed to write. `full` covers attention, DeltaNet, and the MLP."""
    preset = cfg.get("lora_preset")
    if preset == "attn":
        return list(LORA_SITES["attn"])
    if preset == "attn_delta":
        return list(LORA_SITES["attn"]) + list(LORA_SITES["delta"])
    if preset == "full":
        return list(LORA_SITES["attn"]) + list(LORA_SITES["delta"]) + list(LORA_SITES["mlp"])
    if preset == "day_delta":
        return list(LORA_SITES["delta"])
    if preset == "mlp":
        return list(LORA_SITES["mlp"])
    if preset == "attn_mlp":
        return list(LORA_SITES["attn"]) + list(LORA_SITES["mlp"])
    return list(cfg.get("target_modules") or LORA_SITES["attn"])


def set_trainable_sites(model, adapter: str, sites: list[str]) -> int:
    """Train one adapter, and only on the named projections. The other LoRA rows stay zero."""
    count = 0
    for name, param in model.named_parameters():
        trainable = adapter_in_name(name, adapter) and any(f".{site}." in name for site in sites)
        param.requires_grad = trainable
        if trainable:
            count += param.numel()
    return count


def _is_4bit(model) -> bool:
    return any(module.__class__.__name__ == "Linear4bit" for module in model.modules())


def _move_lora_to_cuda(model) -> None:
    for name, param in model.named_parameters():
        if "lora_" in name and param.device.type != "cuda":
            param.data = param.data.to("cuda")


def ensure_input_grads(model) -> None:
    """4-bit checkpointing only backprops when an embedding output requires grad.

    Clearing forward hooks removes the hook that prepare_model_for_kbit_training installed.
    """
    enable = getattr(model, "enable_input_require_grads", None)
    if enable is not None:
        enable()


def adapter_in_name(name: str, adapter: str) -> bool:
    return f".{adapter}." in name and "lora_" in name


def set_only_trainable(model, adapter: str) -> int:
    count = 0
    for name, param in model.named_parameters():
        trainable = adapter_in_name(name, adapter)
        param.requires_grad = trainable
        if trainable:
            count += param.numel()
    if count == 0:
        sample = [name for name, _ in model.named_parameters() if "lora_" in name][:5]
        raise RuntimeError(f"No LoRA parameters for adapter {adapter}. Sample names: {sample}")
    return count


def adapter_state(model, adapter: str) -> dict[str, torch.Tensor]:
    state = {}
    for name, param in model.named_parameters():
        if adapter_in_name(name, adapter):
            state[name] = param.detach().cpu().clone()
    if not state:
        raise RuntimeError(f"Adapter {adapter} has no parameters to snapshot")
    return state


def load_adapter_state(model, adapter: str, state: dict[str, torch.Tensor]) -> None:
    named = dict(model.named_parameters())
    missing = []
    with torch.no_grad():
        for name, tensor in state.items():
            target_name = _retarget(name, adapter)
            param = named.get(target_name)
            if param is None:
                missing.append(target_name)
                continue
            param.data.copy_(tensor.to(device=param.device, dtype=param.dtype))
    if missing:
        raise RuntimeError(f"Missing parameters while loading {adapter}: {missing[:3]}")


def _retarget(name: str, adapter: str) -> str:
    parts = name.split(".")
    known = set(ADAPTERS) | {"blend", "cross", "mate", "cand"}
    for index, part in enumerate(parts):
        if part in known or part.startswith("slot_"):
            parts[index] = adapter
            return ".".join(parts)
    return name


def use_adapters(model, names: list[str], inference: bool) -> None:
    """Activate every name for the forward pass.

    PeftModel.set_adapter accepts one string. The base tuner adds the LoRA updates.
    """
    model.base_model.set_adapter(list(names), inference_mode=inference)


def joint_adapters(model, left: str, right: str) -> bool:
    """True when both adapters are active together. Restores `left` afterwards."""
    try:
        use_adapters(model, [left, right], inference=True)
    except (TypeError, ValueError, AttributeError, RuntimeError):
        return False
    found = False
    for module in model.modules():
        active = getattr(module, "active_adapters", None)
        if not active:
            continue
        names = list(active)
        if left in names and right in names:
            found = True
            break
    model.set_adapter(left)
    return found


def stack_lora(left_a, left_b, right_a, right_b):
    """Rank-concat two LoRA updates. The product equals the sum of the two updates.

    A is (rank, in). B is (out, rank).
    """
    import torch

    rank = left_a.shape[0]
    extra = 0 if right_a is None else right_a.shape[0]
    dest_a = torch.zeros(rank + extra, left_a.shape[1], dtype=left_a.dtype, device=left_a.device)
    dest_b = torch.zeros(left_b.shape[0], rank + extra, dtype=left_b.dtype, device=left_b.device)
    dest_a[:rank].copy_(left_a)
    dest_b[:, :rank].copy_(left_b)
    if right_a is not None and right_b is not None:
        dest_a[rank:].copy_(right_a)
        dest_b[:, rank:].copy_(right_b)
    return dest_a, dest_b


def add_named_adapter(evo, name: str, rank: int | None = None) -> None:
    if name in evo.model.peft_config:
        return
    from peft import LoraConfig

    width = int(rank or evo.cfg["lora_rank"])
    base = max(1, int(evo.cfg["lora_rank"]))
    alpha = float(evo.cfg["lora_alpha"]) * width / base
    lora = LoraConfig(
        r=width,
        lora_alpha=int(round(alpha)),
        lora_dropout=evo.cfg["lora_dropout"],
        target_modules=list(evo.cfg["target_modules"]),
        bias="none",
        task_type="CAUSAL_LM",
    )
    evo.model.add_adapter(name, lora)
    _move_lora_to_cuda(evo.model)


def _module_key(name: str, adapter: str) -> str:
    text = name.replace(f".{adapter}.", ".")
    for label in ("lora_A", "lora_B", "lora_embedding_A", "lora_embedding_B"):
        text = text.replace(f".{label}.", ".")
    return text


def blend_adapters(evo, left: str, right: str | None, dest: str = "blend") -> str:
    """Write left and right into one wider adapter. This PEFT build activates one adapter at a time."""
    width = int(evo.cfg["lora_rank"]) * (2 if right else 1)
    add_named_adapter(evo, dest, rank=width)
    named = dict(evo.model.named_parameters())

    def grouped(adapter: str) -> dict[str, dict[str, object]]:
        groups: dict[str, dict[str, object]] = {}
        for name, param in named.items():
            if not adapter_in_name(name, adapter):
                continue
            kind = "A" if "lora_A" in name or "lora_embedding_A" in name else "B"
            groups.setdefault(_module_key(name, adapter), {})[kind] = param
        return groups

    left_groups = grouped(left)
    right_groups = grouped(right) if right else {}
    dest_groups = grouped(dest)
    for key, dest_pair in dest_groups.items():
        pair = left_groups.get(key)
        other = right_groups.get(key)
        if not pair or "A" not in pair or "B" not in pair or "A" not in dest_pair or "B" not in dest_pair:
            continue
        right_a = None if not other else other["A"].data
        right_b = None if not other else other["B"].data
        stacked_a, stacked_b = stack_lora(pair["A"].data, pair["B"].data, right_a, right_b)
        with torch.no_grad():
            dest_pair["A"].zero_()
            dest_pair["B"].zero_()
            dest_pair["A"][: stacked_a.shape[0]].copy_(stacked_a)
            dest_pair["B"][:, : stacked_b.shape[1]].copy_(stacked_b)
    return dest


class EvoModel:
    """One frozen 4-bit base, three LoRA adapters.

    policy: persistent self-edit / self-play behavior, trained by ReST-EM.
    memory: persistent knowledge. Identity until a gated update is copied in.
    scratch: disposable copy used to try an update without touching memory.
    """

    def __init__(self, model, tok, cfg: dict):
        self.model = model
        self.tok = tok
        self.cfg = cfg
        self.identity_memory = adapter_state(model, "memory")
        self.is_4bit = _is_4bit(model)
        self.joint = False
        self.model._paired = {}

    @property
    def device(self) -> torch.device:
        return next(self.model.parameters()).device

    def set_adapter(self, name: str, inference: bool = False) -> None:
        names = getattr(self.model, "_paired", {}).get(name)
        if names and len(names) > 1:
            use_adapters(self.model, names, inference=inference)
            return
        self.model.set_adapter(name)

    def reset_scratch(self) -> None:
        load_adapter_state(self.model, "scratch", self.identity_memory)

    def copy_memory_to_scratch(self) -> None:
        load_adapter_state(self.model, "scratch", adapter_state(self.model, "memory"))

    def copy_scratch_to_memory(self) -> None:
        load_adapter_state(self.model, "memory", adapter_state(self.model, "scratch"))

    def snapshot(self, adapter: str) -> dict[str, torch.Tensor]:
        return adapter_state(self.model, adapter)

    def restore(self, adapter: str, state: dict[str, torch.Tensor]) -> None:
        load_adapter_state(self.model, adapter, state)

    def trainable(self, adapter: str) -> int:
        return set_only_trainable(self.model, adapter)

    def vram_mb(self) -> float:
        if not torch.cuda.is_available():
            return 0.0
        return torch.cuda.max_memory_allocated() / (1024 * 1024)


@contextmanager
def activate(model, adapter: str | None):
    """Select one adapter, or disable them all when adapter is None.

    Callers that need a specific adapter afterwards set it again. Restoring the
    previous name is unreliable across PEFT versions (string vs list).
    """
    if adapter is None:
        with model.disable_adapter():
            yield
        return
    names = None
    if isinstance(adapter, str):
        names = getattr(model, "_paired", {}).get(adapter)
    elif isinstance(adapter, (list, tuple)):
        names = list(adapter)
    if names and len(names) > 1:
        use_adapters(model, names, inference=True)
        yield
        return
    model.set_adapter(adapter if isinstance(adapter, str) else names[0])
    yield


def _from_pretrained(loader, name: str, **kwargs):
    try:
        return loader(name, **kwargs)
    except Exception as first:
        if os.environ.get("HF_ENDPOINT"):
            raise
        os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
        print(f"[model] retry via hf-mirror after {type(first).__name__}", flush=True)
        return loader(name, **kwargs)


def _load_base(name: str, load_kwargs: dict):
    """Qwen3.5 checkpoints are conditional-generation weights. Take that class, text only."""
    from transformers import AutoConfig

    try:
        config = AutoConfig.from_pretrained(name)
    except Exception:
        config = None
    model_type = getattr(config, "model_type", "")
    if model_type == "qwen3_5":
        from transformers import Qwen3_5ForConditionalGeneration

        try:
            return _from_pretrained(Qwen3_5ForConditionalGeneration.from_pretrained, name, dtype=torch.bfloat16, **load_kwargs)
        except TypeError:
            return _from_pretrained(
                Qwen3_5ForConditionalGeneration.from_pretrained, name, torch_dtype=torch.bfloat16, **load_kwargs
            )
    try:
        return _from_pretrained(AutoModelForCausalLM.from_pretrained, name, dtype=torch.bfloat16, **load_kwargs)
    except TypeError:
        return _from_pretrained(AutoModelForCausalLM.from_pretrained, name, torch_dtype=torch.bfloat16, **load_kwargs)


def build_model(cfg: dict) -> EvoModel:
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA GPU is required to load the 4-bit model")
    torch.backends.cuda.matmul.allow_tf32 = True
    name = cfg["model_name"]
    tok = _from_pretrained(AutoTokenizer.from_pretrained, name)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    tok.padding_side = "left"

    quant = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=torch.bfloat16,
    )
    load_kwargs = dict(quantization_config=quant, device_map={"": 0}, low_cpu_mem_usage=True)
    base = _load_base(name, load_kwargs)
    base = prepare_model_for_kbit_training(base, use_gradient_checkpointing=True)
    cfg["target_modules"] = lora_targets(cfg)
    lora = LoraConfig(
        r=cfg["lora_rank"],
        lora_alpha=cfg["lora_alpha"],
        lora_dropout=cfg["lora_dropout"],
        target_modules=list(cfg["target_modules"]),
        bias="none",
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(base, lora, adapter_name="policy")
    model.add_adapter("memory", lora)
    model.add_adapter("scratch", lora)
    _move_lora_to_cuda(model)
    model.config.use_cache = False
    evo = EvoModel(model, tok, cfg)
    if not evo.is_4bit:
        raise RuntimeError("Model did not load in 4-bit. Check bitsandbytes and CUDA.")
    for adapter in ADAPTERS:
        evo.trainable(adapter)
    evo.trainable("scratch")
    print(
        f"[model] name={name} 4bit=True rank={cfg['lora_rank']} "
        f"vram_mb={evo.vram_mb():.0f}",
        flush=True,
    )
    return evo


def release(evo: EvoModel | None) -> None:
    if evo is not None:
        del evo
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
