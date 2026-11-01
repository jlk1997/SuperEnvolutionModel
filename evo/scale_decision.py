"""After the local runs: should a 7B rental be the next step?"""

from __future__ import annotations

import json
from pathlib import Path


def _exam_rates(summary: dict, actor: str) -> list[float]:
    rows = summary.get("days") or []
    rates = []
    for row in rows:
        cell = (row.get("exam") or {}).get(actor) or {}
        if "rate" in cell:
            rates.append(float(cell["rate"]))
    return rates


def _mean(values: list[float]) -> float | None:
    if not values:
        return None
    return sum(values) / len(values)


def decide_scale(smoke: dict | None, live: dict | None) -> dict:
    """Compare the evolved-minus-agent gap at 0.5B and 1.5B.

    Renting a larger card is justified only when a local advantage exists and
    did not shrink when the model grew from 0.5B to 1.5B.
    """
    gap_small = None
    gap_large = None
    if smoke is not None:
        small_e = _mean(_exam_rates(smoke, "evolved"))
        small_a = _mean(_exam_rates(smoke, "agent"))
        if small_e is not None and small_a is not None:
            gap_small = small_e - small_a
    if live is not None:
        large_e = _mean(_exam_rates(live, "evolved"))
        large_a = _mean(_exam_rates(live, "agent"))
        if large_e is not None and large_a is not None:
            gap_large = large_e - large_a
    shrunk = False
    if gap_small is not None and gap_large is not None:
        shrunk = gap_small > 0.05 and gap_large < gap_small - 0.05
    has_advantage = gap_large is not None and gap_large >= -0.05
    rising = False
    if live is not None:
        rates = _exam_rates(live, "evolved")
        rising = len(rates) >= 2 and rates[-1] > rates[0]
    recommend = bool(has_advantage and not shrunk and rising)
    if gap_large is None:
        reason = "No 1.5B live run yet, so a 7B rental is not decided."
    elif not has_advantage:
        reason = "On this machine the evolved model did not match the agent, so a larger rental is not justified."
    elif shrunk:
        reason = "The evolved-versus-agent gap shrank from 0.5B to 1.5B, so a 7B run may lose the local advantage."
    elif not rising:
        reason = "The 1.5B exam rate did not rise across days, so the mechanism is not ready to scale."
    else:
        reason = "The local advantage held from 0.5B to 1.5B and the exam rate rose. A 7B rental is the optional next measurement."
    return {
        "gap_0_5b": gap_small,
        "gap_1_5b": gap_large,
        "advantage_shrunk": shrunk,
        "evolved_rate_rose": rising,
        "recommend_rent_7b": recommend,
        "reason": reason,
    }


def write_decision(path: Path, smoke: dict | None, live: dict | None) -> dict:
    payload = decide_scale(smoke, live)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload
