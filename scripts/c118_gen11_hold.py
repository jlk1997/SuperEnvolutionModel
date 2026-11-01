# -*- coding: utf-8 -*-
"""C118: gen11 remains HOLD — do not open seal."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/r50"
GATE = 0.6


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    # Check prior registration if any
    prior = None
    for name in ("C111_GEN11_HOLD.json", "C105_GEN11_HOLD.json", "C95_GEN11_HOLD.json"):
        p = DOC / name
        if p.is_file():
            prior = json.loads(p.read_text(encoding="utf-8"))
            break
    out = {
        "cycle": "C118",
        "theme": "gen11_hold",
        "gate": GATE,
        "timestamp": ts(),
        "gate2_3_untouched": True,
        "decision": "HOLD",
        "seal": False,
        "open": False,
        "reason": "fresh_score_threshold_not_met_or_policy_hold; user directive gen11 HOLD",
        "fresh_required_hint": 0.99,
        "prior": {k: prior.get(k) for k in ("cycle", "decision", "seal", "timestamp") if prior and k in prior} if prior else None,
        "pass": True,
        "claim": False,
        "note": "gen11 sealed package NOT opened. Gate2/3 untouched.",
    }
    J(DOC / "C118_GEN11_HOLD.json", out)
    print(json.dumps({"cycle": "C118", "decision": "HOLD", "seal": False, "pass": True}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
