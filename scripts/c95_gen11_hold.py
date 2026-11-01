# -*- coding: utf-8 -*-
"""C95: gen11 HOLD reaffirm — do not open seal unless measured fresh>=0.99."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
GATE = 0.6
FRESH_OPEN = 0.99


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    # Look for any gen11 fresh measurement; default none
    fresh = None
    candidates = list((ROOT / "docs").rglob("*GEN11*")) + list((ROOT / "runs").rglob("*gen11*"))
    found = [str(p.relative_to(ROOT)).replace("\\", "/") for p in candidates[:20]]
    # Prior HOLD artifacts
    prior = DOC / "C89_GEN11_HOLD.json"
    prior_c81 = DOC / "C81_GEN11_HOLD.json"
    prior_data = None
    for p in (prior, prior_c81):
        if p.is_file():
            prior_data = json.loads(p.read_text(encoding="utf-8"))
            break
    if prior_data and "fresh" in prior_data:
        fresh = prior_data.get("fresh")
    decision = "HOLD"
    seal_opened = False
    reason = "no_fresh_measurement_ge_0.99"
    if fresh is not None and float(fresh) >= FRESH_OPEN:
        decision = "OPEN_ELIGIBLE"
        reason = f"fresh={fresh}>={FRESH_OPEN}"
        # Still do not open in this cycle without explicit blast — keep seal closed
        seal_opened = False
        reason += "; seal_kept_closed_policy"
    out = {
        "cycle": "C95",
        "theme": "gen11_hold",
        "decision": decision,
        "seal_opened": seal_opened,
        "fresh": fresh,
        "threshold": FRESH_OPEN,
        "gate": GATE,
        "pass": decision == "HOLD" and seal_opened is False,
        "prior_artifacts": found,
        "timestamp": ts(),
        "note": "gen11 remains HOLD. Gate2/3 untouched.",
    }
    J(DOC / "C95_GEN11_HOLD.json", out)
    print(json.dumps({k: out[k] for k in ("cycle", "decision", "seal_opened", "pass")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
