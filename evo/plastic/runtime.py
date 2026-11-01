"""Which stack runs a population. The laptop uses transformers; a Linux GPU uses vLLM.

Rollouts are the expensive half. Updates stay on LoRA, one individual at a time.
vLLM is optional and is not imported unless the run asks for it.
"""

from __future__ import annotations

import os


def resolve_backend(name: str | None = None) -> str:
    choice = (name or os.environ.get("EVO_BACKEND") or "transformers").strip().lower()
    if choice not in {"transformers", "vllm"}:
        raise ValueError(f"unknown backend {choice}")
    if choice == "vllm":
        try:
            import vllm  # noqa: F401
        except ImportError as exc:
            raise RuntimeError(
                "vLLM is not installed. On a Linux GPU machine: pip install vllm, then set EVO_BACKEND=vllm."
            ) from exc
    return choice


def rollout_plan(pop: int, cfg: dict) -> dict:
    """What a generation needs from the rollout server. Training is not done inside vLLM."""
    from evo.plastic.signal import learning_signal

    signal = learning_signal(cfg)
    return {
        "backend": resolve_backend(cfg.get("backend")),
        "population": int(pop),
        "grpo_k": signal["grpo_k"],
        "temperature": signal["temperature"],
        "max_seq_len": int(cfg.get("max_seq_len", 1024)),
        "lora_rank": int(cfg.get("lora_rank", 8)),
        "note": "One frozen base, one LoRA per individual. Updates run outside the rollout server.",
    }
