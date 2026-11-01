"""The learning signal the plasticity line is willing to train on.

The office census sampled twice at temperature 0, so the group advantage was
usually zero and nothing moved. Here a batch is at least 8 draws, and a
non-positive temperature is rejected.
"""

from __future__ import annotations


MIN_GROUP = 8
DEFAULT_TEMPERATURE = 0.7


def learning_signal(cfg: dict | None) -> dict:
    cfg = cfg or {}
    group = max(MIN_GROUP, int(cfg.get("grpo_k", MIN_GROUP)))
    temperature = float(cfg.get("temperature", DEFAULT_TEMPERATURE))
    if temperature <= 0:
        temperature = DEFAULT_TEMPERATURE
    return {"grpo_k": group, "temperature": temperature}


def keep_successes(prompt: str, samples: list[str], correct) -> dict:
    """Prefer the model's own correct draws. Otherwise take the verifier's target.

    The fallback is labeled. A run must not report it as an on-policy sample.
    """
    good = [text for text in samples if text and correct(text)]
    if good:
        return {"pairs": [(prompt, text) for text in good], "source": "on_policy", "kept": len(good)}
    return {"pairs": [], "source": "none", "kept": 0}


def with_verifier(prompt: str, samples: list[str], correct, target: str) -> dict:
    chosen = keep_successes(prompt, samples, correct)
    if chosen["pairs"] or not str(target).strip():
        return chosen
    return {"pairs": [(prompt, target)], "source": "verifier", "kept": 0}
