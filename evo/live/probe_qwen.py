"""Can the primary (and optional 2B) checkpoint take a 4-bit LoRA step, and does its delta state carry?"""

from __future__ import annotations

import json
import math
import traceback
from pathlib import Path

from evo.util import repo_path


def run_probe(models: list[str] | None = None) -> dict:
    from evo.registry import OPTIONAL_2B, PRIMARY, resolve

    names = models or [
        str(resolve(PRIMARY)),
        str(resolve(OPTIONAL_2B)),
    ]
    rows = [_one(name) for name in names]
    payload = {"models": rows}
    dest = repo_path("runs") / "qwen35_probe.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2), flush=True)
    return payload


def _one(name: str) -> dict:
    path = Path(name)
    row = {"model": str(path), "loaded": False, "lora_ok": False, "state_replay": False}
    if not path.is_dir() or not (path / "config.json").is_file():
        row["reason"] = "weights are not on disk"
        return row
    evo = None
    try:
        import torch

        from evo.inner_loop import adapt_scratch
        from evo.model import activate, build_model, release

        cfg = {
            "model_name": str(path),
            "lora_rank": 8,
            "lora_alpha": 16,
            "lora_dropout": 0.0,
            "target_modules": ["q_proj", "k_proj", "v_proj", "o_proj"],
            "max_seq_len": 128,
        }
        evo = build_model(cfg)
        row["loaded"] = True
        row["vram_mb"] = evo.vram_mb()
        row["base_class"] = type(evo.model.get_base_model()).__name__
        from evo.generate import generate
        from evo.inner_loop import causal_loss

        row["base_loss"] = float(causal_loss(evo, "The capital of France is Paris.", 64).detach())
        row["reply"] = generate(evo, "What is 2+2? Reply with one digit.", 16, 0.0, None)
        classes = sorted({type(module).__name__ for module in evo.model.modules()})
        row["delta_classes"] = [label for label in classes if "delta" in label.lower() or "gated" in label.lower()]
        row["state_replay"] = _replay_state(evo, activate, torch)
        evo.reset_scratch()
        loss, params = adapt_scratch(evo, "A fabricated probe token stays at 7.", steps=1, lr=5e-4, max_len=64)
        row["lora_loss"] = loss
        row["lora_params"] = params
        row["lora_ok"] = math.isfinite(loss)
    except Exception as exc:
        row["error"] = f"{type(exc).__name__}: {exc}"
        row["trace"] = traceback.format_exc()[-800:]
    finally:
        if evo is not None:
            from evo.model import release

            release(evo)
    return row


def _replay_state(evo, activate, torch) -> bool:
    """True when a second forward accepts the cache from the first."""
    evo.model.eval()
    text = evo.tok("alpha beta", return_tensors="pt")
    text = {key: value.to(evo.device) for key, value in text.items()}
    with torch.no_grad(), activate(evo.model, "policy"):
        first = evo.model(**text, use_cache=True)
    cache = getattr(first, "past_key_values", None)
    if cache is None:
        return False
    more = evo.tok(" gamma", return_tensors="pt", add_special_tokens=False)
    more = {key: value.to(evo.device) for key, value in more.items()}
    with torch.no_grad(), activate(evo.model, "policy"):
        evo.model(**more, past_key_values=cache, use_cache=True)
    return True
