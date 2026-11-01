"""A weight write is a transaction: shadow copy, small update, canary, then switch or drop.

The live adapter keeps serving until the canary passes. `cand` is the shadow.
"""

from __future__ import annotations

from evo.live.canary import decide_commit, safety_violations
from evo.model import adapter_state, add_named_adapter, load_adapter_state


def run_shadow(evo, run, live: str, train, score, cfg: dict, meta: dict | None = None) -> dict:
    """Train `cand`, score it, and copy it onto `live` only when `decide_commit` agrees.

    `train(adapter) -> {steps, codes}`. `score(adapter) -> rate`.
    """
    snap = evo.snapshot(live)
    add_named_adapter(evo, "cand")
    load_adapter_state(evo.model, "cand", adapter_state(evo.model, live))
    keep = False
    before = 0.0
    after = 0.0
    trained = {}
    violations: list[str] = []
    try:
        before = float(score(live))
        trained = train("cand") or {}
        after = float(score("cand"))
        codes = list(trained.get("codes") or [])
        for code in codes:
            violations.extend(safety_violations(code))
        if int(trained.get("steps") or 0) == 0:
            evo.restore(live, snap)
            keep = False
        else:
            keep = decide_commit(before, after, float(cfg.get("gate_drop", 0.34)), violations)
        if keep:
            load_adapter_state(evo.model, live, adapter_state(evo.model, "cand"))
            if run is not None:
                run.commit_adapter(evo.model, live, {"kind": "shadow", "kept": True, **(meta or {})})
        else:
            evo.restore(live, snap)
    except Exception:
        evo.restore(live, snap)
        raise
    return {
        "kept": keep,
        "steps": int(trained.get("steps") or 0),
        "before": before,
        "after": after,
        "violations": violations,
    }


def drift_pairs(tool: dict) -> list[tuple[str, str]]:
    """Re-bind a tool whose behavior changed. The new return value is the target."""
    from evo.world.sleep import verified_drills

    return verified_drills(tool)
