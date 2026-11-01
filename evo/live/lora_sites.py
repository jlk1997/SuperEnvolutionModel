"""One training step per LoRA site, on a model that was built with the full preset."""

from __future__ import annotations

import torch

from evo.model import LORA_SITES, ensure_input_grads, set_trainable_sites


def site_step(evo, sites: list[str], text: str = "The office total for paid rows is 17.") -> dict:
    from evo.inner_loop import causal_loss

    snap = evo.snapshot("policy")
    try:
        ensure_input_grads(evo.model)
        evo.set_adapter("policy", inference=False)
        count = set_trainable_sites(evo.model, "policy", sites)
        params = [param for param in evo.model.parameters() if param.requires_grad]
        if not params:
            return {"params": 0, "loss": None}
        opt = torch.optim.AdamW(params, lr=5e-4)
        evo.model.train()
        evo.model.config.use_cache = False
        loss = causal_loss(evo, text, 64)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(params, 1.0)
        opt.step()
        value = float(loss.detach().item())
        evo.model.eval()
        with torch.no_grad():
            after = float(causal_loss(evo, text, 64).detach())
        del opt
        return {"params": count, "loss": value, "loss_after": after}
    finally:
        evo.restore("policy", snap)


def compare_sites(evo) -> dict:
    groups = {
        "attn": list(LORA_SITES["attn"]),
        "attn_delta": list(LORA_SITES["attn"]) + list(LORA_SITES["delta"]),
        "full": list(LORA_SITES["attn"]) + list(LORA_SITES["delta"]) + list(LORA_SITES["mlp"]),
        "day_delta": list(LORA_SITES["delta"]),
        "slot_mlp": list(LORA_SITES["mlp"]),
    }
    return {name: site_step(evo, sites) for name, sites in groups.items()}
