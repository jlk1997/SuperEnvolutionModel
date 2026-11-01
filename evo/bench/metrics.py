"""Lifetime metrics. Curves are success or competence in [0, 1].

`AR_k` is samples-to-competence on the first new family divided by the same
number on a later family. A learner that does not transfer sits near 1.
"""

from __future__ import annotations

import math

from evo.stats import paired_bootstrap, power_paired


AR_CAP = 50.0


def learning_curve_area(curve: list[float]) -> float:
    if not curve:
        return 0.0
    return float(sum(curve) / len(curve))


def samples_to_competence(curve: list[float], criterion: float = 0.6, cap: int | None = None) -> int:
    for index, value in enumerate(curve):
        if float(value) >= criterion:
            return index
    return int(cap if cap is not None else len(curve))


def acceleration_ratio(n_first: float, n_later: float, cap: float = AR_CAP) -> float:
    later = float(n_later)
    first = float(n_first)
    if later <= 0:
        return cap if first > 0 else 1.0
    return min(cap, first / later)


def evolution_index(counts: list[float]) -> float:
    """Negative slope of log samples-to-competence across successive families."""
    if len(counts) < 2:
        return 0.0
    ys = [math.log(max(float(value), 0.5)) for value in counts]
    xs = list(range(len(ys)))
    x_mean = sum(xs) / len(xs)
    y_mean = sum(ys) / len(ys)
    numer = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, ys))
    denom = sum((x - x_mean) ** 2 for x in xs)
    if denom == 0:
        return 0.0
    return float(-(numer / denom))


def forgetting(before: float, after: float) -> float:
    return max(0.0, float(before) - float(after))


def heritability(ar_source: float, ar_transferred: float, floor: float = 1.0) -> float:
    """Share of the source acceleration that is still there on the new base.

    Values above 1 mean the new base amplified the same genome. Values below 0
    mean the transferred genome is worse than a non-learning floor.
    """
    gained = float(ar_source) - float(floor)
    if gained <= 1e-6:
        return 0.0
    return (float(ar_transferred) - float(floor)) / gained


def compare_curves(left: list[float], right: list[float], seed: int = 0) -> dict:
    """Paired interval for left minus right, one point per family or episode."""
    return paired_bootstrap(left, right, seed=seed)


def power_for_acceleration(n: int, p_later: float = 0.75, p_first: float = 0.45, sims: int = 200, seed: int = 0) -> dict:
    """Power of 'later families beat the first family' at this paper size."""
    return power_paired(p_later, p_first, n, sims=sims, seed=seed)


def families_for_power(target: float = 0.8, p_later: float = 0.75, p_first: float = 0.45, seed: int = 0) -> dict:
    """Smallest registered family count whose power clears `target`."""
    chosen = None
    rows = []
    for n in (8, 12, 16, 24, 30, 40, 60, 80):
        row = power_for_acceleration(n, p_later=p_later, p_first=p_first, sims=80, seed=seed)
        rows.append(row)
        if chosen is None and row["power"] >= target:
            chosen = n
    return {"n": chosen or 80, "target": target, "checks": rows}
