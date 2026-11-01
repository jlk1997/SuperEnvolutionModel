# -*- coding: utf-8 -*-
"""C81: gen11 HOLD refresh — open only if measured fresh>=0.99 (not available)."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NEAR = 0.99


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load(p):
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None


def main():
    seal = ROOT / "runs/heldout_seal_gen11.json"
    fresh = None  # seal closed → unmeasured
    decision = "HOLD"
    go = False
    reason = (
        f"gen11 seal closed; fresh unmeasured. Policy: open only if fresh>={NEAR}. "
        "Other boards at 1.0 do not authorize burn."
    )
    if seal.is_file():
        # should not happen under HOLD
        decision = "REVIEW"
        reason = "seal file present unexpectedly — review before any claim"
    signals = [
        {"src": "gen11_fresh", "metric": "fresh_rate", "value": fresh, "near_ceiling": False},
        {"src": "c74", "metric": "replace_rate", "value": (load(ROOT / "docs/r50/C74_replace_dual_strengthen.json") or {}).get("replace_rate"), "near_ceiling": True},
        {"src": "c80", "metric": "replace_rate", "value": (load(ROOT / "docs/r50/C80_dual_cost_refresh.json") or {}).get("replace_rate"), "near_ceiling": True},
        {"src": "c73c", "metric": "v3_rate", "value": (load(ROOT / "docs/r50/C73c_vision_gate_v3_claim.json") or {}).get("rate"), "near_ceiling": True},
    ]
    payload = {
        "kind": "r50plus_c81_gen11_hold",
        "timestamp": ts(),
        "near_ceiling_threshold": NEAR,
        "fresh_measured": False,
        "fresh_rate": fresh,
        "fresh_ge_099": False,
        "seal_opened": False,
        "seal_file_absent": not seal.is_file(),
        "decision": decision,
        "go_open_seal": go,
        "reason": reason,
        "signals": signals,
        "gate2_3_untouched": True,
        "innovation": "Reaffirm burn discipline: boards≠fresh",
    }
    J(ROOT / "docs/r50/C81_gen11_hold.json", payload)
    print(json.dumps({"decision": decision, "go_open_seal": go, "fresh": fresh}, ensure_ascii=False))


if __name__ == "__main__":
    main()
