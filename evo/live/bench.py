"""Generation and one training step, plus a projection of a 10-day office comparison."""

from __future__ import annotations

import time

from evo.util import repo_path


def project_hours(seconds_per_episode: float, episodes: int) -> float:
    return seconds_per_episode * episodes / 3600.0


def run_bench(model: str | None = None, episodes: int = 7 * 3 * 40) -> dict:
    """Time one short generation and one train step. `episodes` is the 10-day projection."""
    import torch

    from evo.generate import generate
    from evo.inner_loop import causal_loss
    from evo.model import build_model, ensure_input_grads, release

    from evo.registry import PRIMARY, resolve

    path = model or str(resolve(PRIMARY))
    if not __import__("pathlib").Path(path).is_dir():
        path = str(resolve(PRIMARY))
    cfg = {
        "model_name": path,
        "lora_rank": 8,
        "lora_alpha": 16,
        "lora_dropout": 0.0,
        "lora_preset": "full",
        "max_seq_len": 256,
    }
    evo = build_model(cfg)
    try:
        started = time.perf_counter()
        reply = generate(evo, "Reply with the single digit 4.", 16, 0.0, "policy")
        gen_seconds = time.perf_counter() - started
        ensure_input_grads(evo.model)
        evo.trainable("policy")
        params = [param for param in evo.model.parameters() if param.requires_grad]
        opt = torch.optim.AdamW(params, lr=5e-4)
        evo.model.train()
        started = time.perf_counter()
        loss = causal_loss(evo, "The office total for paid rows is 17. " * 40, int(cfg["max_seq_len"]))
        loss.backward()
        opt.step()
        train_seconds = time.perf_counter() - started
        del opt
        episode_seconds = gen_seconds * 4 + train_seconds
        hours = project_hours(episode_seconds, episodes)
        from evo.live.lora_sites import compare_sites

        sites = compare_sites(evo)
        return {
            "model": path,
            "reply": reply,
            "gen_seconds": gen_seconds,
            "train_seconds": train_seconds,
            "train_loss": float(loss.detach().item()),
            "projected_hours": hours,
            "episodes": episodes,
            "over_48h": hours > 48,
            "vram_mb": evo.vram_mb(),
            "sites": sites,
        }
    finally:
        release(evo)
