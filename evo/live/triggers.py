"""When a verified experience is allowed to touch weights."""

from __future__ import annotations


DEFAULT_GENE = {
    "cooldown": 1,
    "fail_streak": 2,
    "buffer_min": 1,
    "successes_needed": 1,
}


def decide(state: dict, gene: dict | None = None) -> str | None:
    """`promote` writes a verified success. `teacher` asks the scaffold after a losing streak.

    None while the step budget is spent or the cooldown has not elapsed.
    """
    rules = dict(DEFAULT_GENE)
    if gene:
        rules.update(gene)
    if int(state.get("opt_steps", 0)) >= int(state.get("max_opt_steps", 0)):
        return None
    if int(state.get("tick", 0)) - int(state.get("last_commit_tick", -10**9)) < int(rules["cooldown"]):
        return None
    if int(state.get("consecutive_failures", 0)) >= int(rules["fail_streak"]):
        return "teacher"
    successes = int(state.get("recent_successes", 0))
    if int(state.get("buffer_size", 0)) >= int(rules["buffer_min"]) and successes >= int(rules["successes_needed"]):
        return "promote"
    return None
