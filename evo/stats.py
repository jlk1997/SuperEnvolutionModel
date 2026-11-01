"""Intervals and power for small exam papers. No model imports."""

from __future__ import annotations

import random


def paired_bootstrap(left: list[float], right: list[float], n_boot: int = 4000, seed: int = 0) -> dict:
    """Interval for the mean of left minus right, item by item.

    `excludes_zero` is the pre-registered claim that one side is ahead.
    An empty or unequal pair of lists returns an interval that does not exclude zero.
    """
    n = len(left)
    if n == 0 or n != len(right):
        return {"n": n, "mean": None, "low": None, "high": None, "excludes_zero": False}
    diffs = [float(left[i]) - float(right[i]) for i in range(n)]
    mean = sum(diffs) / n
    rng = random.Random(seed)
    draws = []
    for _ in range(n_boot):
        total = 0.0
        for _item in range(n):
            total += diffs[rng.randrange(n)]
        draws.append(total / n)
    draws.sort()
    low = draws[int(0.025 * (n_boot - 1))]
    high = draws[int(0.975 * (n_boot - 1))]
    return {"n": n, "mean": mean, "low": low, "high": high, "excludes_zero": low > 0 or high < 0}


def rate_interval(flags: list[bool], n_boot: int = 4000, seed: int = 0) -> dict:
    """Bootstrap interval for a single success rate."""
    if not flags:
        return {"n": 0, "rate": None, "low": None, "high": None}
    ones = [1.0 if flag else 0.0 for flag in flags]
    zeros = [0.0 for _ in ones]
    interval = paired_bootstrap(ones, zeros, n_boot=n_boot, seed=seed)
    return {"n": len(flags), "rate": interval["mean"], "low": interval["low"], "high": interval["high"]}


def power_paired(p_new: float, p_base: float, n: int, alpha_boots: int = 200, sims: int = 200, seed: int = 0) -> dict:
    """Share of simulated papers whose interval lies above zero.

    This is the check to run before a small exam. n=6 at a 0.3 gap is a weak paper.
    """
    rng = random.Random(seed)
    ahead = 0
    for _ in range(sims):
        left = [1.0 if rng.random() < p_new else 0.0 for _item in range(n)]
        right = [1.0 if rng.random() < p_base else 0.0 for _item in range(n)]
        interval = paired_bootstrap(left, right, n_boot=alpha_boots, seed=rng.randrange(10**6))
        if interval["low"] is not None and interval["low"] > 0:
            ahead += 1
    return {
        "p_new": p_new,
        "p_base": p_base,
        "n": n,
        "sims": sims,
        "power": ahead / sims if sims else 0.0,
    }


def breakeven_uses(train_cost: float, evolved_per_use: float, agent_per_use: float) -> float | None:
    """Uses until writing a skill into weights costs less than rereading the notes.

    None when the evolved answer is not cheaper per use, so the training never pays back.
    """
    gap = float(agent_per_use) - float(evolved_per_use)
    if gap <= 0:
        return None
    return float(train_cost) / gap
