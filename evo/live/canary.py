"""Held-out items and a hard safety scan. Neither one trains the model."""

from __future__ import annotations

import random


FORBIDDEN = (
    "os.system",
    "subprocess",
    "shutil.rmtree",
    "os.remove",
    "socket",
    "urllib",
    "requests.",
    "__import__",
)


def safety_violations(code: str) -> list[str]:
    """Calls a learned program is not allowed to grow. The body enforces the same list."""
    text = code or ""
    found = [token for token in FORBIDDEN if token in text]
    if "../" in text or "..\\" in text:
        found.append("path-escape")
    return found


def anchors_hold(codes: list[str]) -> bool:
    return not any(safety_violations(code) for code in codes)


def pick_canaries(tasks: list[dict], k: int, rng: random.Random) -> list[dict]:
    """Spread a small exam across tools. Practice items are not canaries."""
    groups: dict[str, list[dict]] = {}
    for task in tasks:
        if task.get("split") != "exam":
            continue
        key = (task.get("tools") or ["?"])[0]
        groups.setdefault(str(key), []).append(task)
    if k <= 0 or not groups:
        return []
    keys = sorted(groups)
    chosen = []
    while len(chosen) < k:
        progressed = False
        for key in keys:
            bucket = groups[key]
            if not bucket or len(chosen) >= k:
                continue
            chosen.append(bucket.pop(rng.randrange(len(bucket))))
            progressed = True
        if not progressed:
            break
    return chosen


def decide_commit(before_rate: float, after_rate: float, max_drop: float, violations: list[str]) -> bool:
    """A shadow update lands only when the canary holds and the code stays inside the safety list."""
    if violations:
        return False
    return (float(before_rate) - float(after_rate)) <= float(max_drop)
