# -*- coding: utf-8 -*-
"""C136: gen11 HOLD (unless fresh>=0.99 — we do NOT open) + STAGE sync C131-C135.
Gate 0.6. Gate2/3 untouched.
"""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/r50"
GATE = 0.6
FRESH_OPEN_THRESHOLD = 0.99  # gen11 only if fresh>=this; we keep HOLD


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load(name):
    p = DOC / name
    if not p.is_file():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def main():
    c131 = load("C131_V6_DESIGN_BATCH.json") or {}
    c132 = load("C132_VISION_V6_SMOKE.json") or {}
    c132b = load("C132b_VISION_GATE_V6_CLAIM.json")
    c133 = load("C133_CAPTURE_PRODUCT_DEMO.json") or {}
    c134 = load("C134_UNIFIED_REPLACE_BOARD.json") or {}
    c135 = load("C135_U2C_SANDBOX_MONEY_TOOL.json") or {}

    # gen11: require explicit fresh score >= 0.99 to open — we do not have that here
    fresh_score = None  # no gen11 fresh eval this cycle
    gen11_status = "HOLD"
    seal_open = False
    if fresh_score is not None and fresh_score >= FRESH_OPEN_THRESHOLD:
        gen11_status = "OPEN_ELIGIBLE"
        # still do not auto-open seal in this cycle without explicit runner
        seal_open = False

    hold = {
        "cycle": "C136",
        "theme": "gen11_hold_stage_sync_c131_c135",
        "timestamp": ts(),
        "gate": GATE,
        "gen11": gen11_status,
        "seal_open": seal_open,
        "fresh_score": fresh_score,
        "open_threshold": FRESH_OPEN_THRESHOLD,
        "gate2_3_untouched": True,
        "summary": {
            "C131_pass": c131.get("pass"),
            "C131_n_fixtures": c131.get("n_fixtures"),
            "C132_rate": c132.get("rate"),
            "C132_claim": c132.get("claim"),
            "C132_v6_claim_file": bool(c132b),
            "C133_pass": c133.get("pass"),
            "C133_oneshot_ok": c133.get("oneshot_ok"),
            "C134_pass": c134.get("pass"),
            "C134_rate": c134.get("rate"),
            "C134_mean_ratio": (c134.get("board") or {}).get("mean_step_ratio"),
            "C135_pass": c135.get("pass"),
            "C135_rate": c135.get("rate"),
            "C135_absorb_claim": c135.get("absorb_claim"),
        },
        "pass": True,
        "claim": False,
        "note": "gen11 remains HOLD (no fresh>=0.99). Sync only.",
    }
    J(DOC / "C136_GEN11_HOLD.json", hold)

    stage = f"""# STAGE_ANT_C136 — 蚁算 R50+ C131-C136

Updated: {ts()} (Asia/Shanghai)

## Status
- **V6 design**: pass={c131.get('pass')} n={c131.get('n_fixtures')}
- **V6 smoke**: rate={c132.get('rate')} claim={c132.get('claim')} (only if >=0.6)
- **Capture product demo**: pass={c133.get('pass')} oneshot_ok={c133.get('oneshot_ok')}
- **Unified replace board**: pass={c134.get('pass')} rate={c134.get('rate')} mean_ratio={(c134.get('board') or {}).get('mean_step_ratio')}
- **U2C sandbox money_tool**: pass={c135.get('pass')} rate={c135.get('rate')} absorb_claim={c135.get('absorb_claim')}
- **gen11**: {gen11_status} (open only if fresh>={FRESH_OPEN_THRESHOLD}; not met)
- **Gate**: 0.6 — Gate2/3 untouched

## Evidence
- `docs/r50/C131_V6_DESIGN_BATCH.json`
- `docs/r50/C132_VISION_V6_SMOKE.json`
- `docs/r50/C132b_VISION_GATE_V6_CLAIM.json` (only if claimed)
- `docs/r50/C133_CAPTURE_PRODUCT_DEMO.json`
- `docs/r50/C133_CAPTURE_ONESHOT_EVIDENCE.json`
- `docs/r50/C134_UNIFIED_REPLACE_BOARD.json`
- `docs/r50/C135_U2C_SANDBOX_MONEY_TOOL.json`
- `docs/r50/C136_GEN11_HOLD.json`
- `docs/蚁算_CAPTURE_OFFICE_DEMO.md`
- `docs/蚁算_UNIFIED_REPLACE_BOARD.md`
- `docs/CHECKPOINT_NOW.md`

## Honesty
- No fake VL scores. V6 claim only when rate>=0.6 with real VL.
- U2C arithmetic tool-backed; absorb_claim=false.
- gen11 seal not opened.
- Prior V0–V5 / Gate2 / Gate3 untouched.
"""
    (ROOT / "docs" / "STAGE_ANT_C136.md").write_text(stage, encoding="utf-8")

    # also alias STAGE_ANT_C131plus for discoverability
    (ROOT / "docs" / "STAGE_ANT_C131.md").write_text(stage, encoding="utf-8")

    ck = f"""# CHECKPOINT_NOW — {ts()} — 蚁算模型

**R50PLUS=YES** — C131-C136 landed

Gate **0.6**. Gate2/3 untouched. gen11 **{gen11_status}**.

## C131-C136
- **C131** V6 fixtures n={c131.get('n_fixtures')} pass={c131.get('pass')}
- **C132** V6 smoke rate=**{c132.get('rate')}** claim=**{c132.get('claim')}**
- **C133** capture product demo oneshot_ok=**{c133.get('oneshot_ok')}**
- **C134** unified replace rate=**{c134.get('rate')}** mean_ratio=**{(c134.get('board') or {}).get('mean_step_ratio')}**
- **C135** U2C money_tool rate=**{c135.get('rate')}** absorb_claim=**{c135.get('absorb_claim')}**
- **C136** gen11 {gen11_status}

## Product defaults
- Vision dense-table: **bare**
- Money math: **tool-backed**
- Capture CLI: `python scripts/ant_capture_office.py`
- U2C absorb gate: **not claimed**

## Untouched
- Gate2 / Gate3 text claims
- Vision V0-V5 claims
- gen11 seal closed
"""
    (ROOT / "docs" / "CHECKPOINT_NOW.md").write_text(ck, encoding="utf-8")

    loop = ROOT / "docs" / "蚁算_R50PLUS_LOOP.md"
    if loop.is_file():
        prev = loop.read_text(encoding="utf-8")
    else:
        prev = "# 蚁算 R50PLUS LOOP\n\n"
    block = f"""
## C131-C136 @ {ts()}
- C131 V6 design n={c131.get('n_fixtures')} pass={c131.get('pass')}
- C132 V6 smoke rate={c132.get('rate')} claim={c132.get('claim')}
- C133 capture demo oneshot={c133.get('oneshot_ok')}
- C134 unified replace rate={c134.get('rate')} mean_ratio={(c134.get('board') or {}).get('mean_step_ratio')}
- C135 U2C money_tool rate={c135.get('rate')} absorb_claim={c135.get('absorb_claim')}
- C136 gen11 {gen11_status}
- Iron: Gate 0.6, Gate2/3 untouched
"""
    loop.write_text(prev.rstrip() + "\n" + block, encoding="utf-8")

    # STAGE_ANT_R50PLUS bump
    plus = ROOT / "docs" / "STAGE_ANT_R50PLUS.md"
    plus_body = f"""# STAGE_ANT_R50PLUS

Updated: {ts()} (Asia/Shanghai)

Latest band: **C131-C136**
- V6: rate={c132.get('rate')} claim={c132.get('claim')}
- Capture demo: {c133.get('oneshot_ok')}
- Unified replace mean_ratio: {(c134.get('board') or {}).get('mean_step_ratio')}
- U2C money_tool rate: {c135.get('rate')}
- gen11: {gen11_status}

See `docs/STAGE_ANT_C136.md` and `docs/CHECKPOINT_NOW.md`.
"""
    plus.write_text(plus_body, encoding="utf-8")

    print(json.dumps({"cycle": "C136", "gen11": gen11_status, "summary": hold["summary"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
