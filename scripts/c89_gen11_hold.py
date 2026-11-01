# -*- coding: utf-8 -*-
"""C89: gen11 HOLD reaffirm — do NOT open seal unless measured fresh>=0.99."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = 0.6
FRESH_OPEN = 0.99


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def load(p):
    pp = ROOT / p
    return json.loads(pp.read_text(encoding="utf-8")) if pp.is_file() else {}


def main():
    prior = load("docs/r50/C81_gen11_hold.json")
    # Look for any measured fresh score without opening seal
    candidates = [
        "docs/r50/C68_gen11_strengthen.json",
        "docs/r50/C61_gen11_prep.json",
        "runs/heldout_gen11/fresh_score.json",
    ]
    measured_fresh = None
    measured_src = None
    for c in candidates:
        d = load(c)
        for key in ("fresh_rate", "fresh", "rate_fresh", "gen11_fresh"):
            if key in d and d[key] is not None:
                try:
                    measured_fresh = float(d[key])
                    measured_src = c
                    break
                except (TypeError, ValueError):
                    pass
        if measured_fresh is not None:
            break
        nested = d.get("fresh") or d.get("scores") or {}
        if isinstance(nested, dict) and nested.get("rate") is not None:
            measured_fresh = float(nested["rate"])
            measured_src = c
            break

    open_ok = measured_fresh is not None and measured_fresh >= FRESH_OPEN
    decision = "OPEN" if open_ok else "HOLD"
    payload = {
        "kind": "r50plus_c89_gen11_hold",
        "timestamp": ts(),
        "gate": GATE,
        "fresh_open_threshold": FRESH_OPEN,
        "measured_fresh": measured_fresh,
        "measured_src": measured_src,
        "decision": decision,
        "seal_opened": False,
        "prior_c81_decision": prior.get("decision"),
        "reason": (
            f"measured fresh {measured_fresh} >= {FRESH_OPEN}"
            if open_ok
            else f"no measured fresh>={FRESH_OPEN} (got {measured_fresh}); keep seal closed"
        ),
        "innovation": "Hard hold discipline; never open gen11 seal without fresh evidence",
        "gate2_3_untouched": True,
    }
    out = ROOT / "docs/r50/C89_gen11_hold.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "decision": decision,
        "seal_opened": False,
        "measured_fresh": measured_fresh,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
