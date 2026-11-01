"""Pure retention math used by the phase-1 gate and reward."""

from __future__ import annotations


def retention_reward(
    new_before: float,
    new_after: float,
    old_before: float,
    old_after: float,
    lam: float,
) -> float:
    """Gain on the new passage minus a penalty for lost accuracy on old ones."""
    gain = new_after - new_before
    forgotten = max(0.0, old_before - old_after)
    return gain - lam * forgotten


def peak_drop(
    peaks: dict[str, float],
    after: dict[str, float],
    min_peak: float = 0.0,
) -> tuple[str, float] | None:
    """Largest drop below a historical peak. Peaks under `min_peak` do not count."""
    worst_key = None
    worst = -1.0
    for key, peak in peaks.items():
        if peak < min_peak:
            continue
        current = after.get(key)
        if current is None:
            continue
        drop = peak - current
        if drop > worst:
            worst_key = key
            worst = drop
    if worst_key is None:
        return None
    return worst_key, worst


def peak_accept(
    peaks: dict[str, float],
    after: dict[str, float],
    max_drop: float,
    min_peak: float = 0.0,
) -> bool:
    """Reject when a tracked skill falls more than `max_drop` below its own best."""
    found = peak_drop(peaks, after, min_peak)
    if found is None:
        return True
    return found[1] <= max_drop


def positive_gain(accept_peak: bool, gain: float, reward: float, min_gain: float) -> bool:
    """A peak-safe update still has to raise the new passage and not lose old ones."""
    return bool(accept_peak) and gain > min_gain and reward >= 0.0


def gate_accept(
    old_before: float,
    old_after: float,
    kl: float | None,
    max_drop: float,
    max_kl: float | None,
) -> bool:
    """Reject an update that drops old F1 or moves too far in KL."""
    if old_before - old_after > max_drop:
        return False
    if kl is not None and max_kl is not None and kl > max_kl:
        return False
    return True
