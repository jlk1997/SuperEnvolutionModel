# -*- coding: utf-8 -*-
"""C130: gen11 HOLD + docs sync for C125-C129. No seal open."""
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


def load(name):
    p = DOC / name
    if not p.is_file():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def main():
    c125 = load("C125_VISION_V5_HELDOUT_FIXTURES.json") or {}
    c126 = load("C126_VISION_V5_HELDOUT_SMOKE.json") or {}
    c126b = load("C126b_VISION_GATE_V5_HELDOUT_CLAIM.json")
    c127 = load("C127_MONEY_TOOL_CAPTURE_E2E.json") or {}
    c128 = load("C128_REAL_SCREENSHOT_OFFICE.json") or {}
    c129 = load("C129_REPLACE_COST_REFRESH.json") or {}

    hold = {
        "cycle": "C130",
        "theme": "gen11_hold_docs_sync_c125_c129",
        "timestamp": ts(),
        "gate": GATE,
        "gen11": "HOLD",
        "seal_open": False,
        "gate2_3_untouched": True,
        "summary": {
            "C125_pass": c125.get("pass"),
            "C126_rate": c126.get("rate"),
            "C126_claim": c126.get("claim"),
            "C126_heldout_claim_file": bool(c126b),
            "C127_pass": c127.get("pass"),
            "C127_rate": c127.get("rate"),
            "C128_pass": c128.get("pass"),
            "C128_rate": c128.get("rate"),
            "C128_use_vl": c128.get("use_vl"),
            "C129_pass": c129.get("pass"),
            "C129_ratio": c129.get("step_ratio_agent_over_bare"),
        },
        "pass": True,
        "claim": False,
        "note": "gen11 remains HOLD. Sync only.",
    }
    J(DOC / "C130_GEN11_HOLD.json", hold)

    stage = f"""# STAGE_ANT_C130 — 蚁算 R50+ C125-C130

Updated: {ts()} (Asia/Shanghai)

## Status
- **V5 train claim**: untouched (prior True rate=1.0)
- **V5 heldout**: rate={c126.get('rate')} claim={c126.get('claim')} (only if >=0.6)
- **money_tool → capture E2E**: pass={c127.get('pass')} rate={c127.get('rate')}
- **real screenshot office**: pass={c128.get('pass')} rate={c128.get('rate')} use_vl={c128.get('use_vl')}
- **replace/cost refresh**: pass={c129.get('pass')} ratio={c129.get('step_ratio_agent_over_bare')}
- **gen11**: HOLD
- **Gate**: 0.6 — Gate2/3 untouched

## Evidence
- `docs/r50/C125_VISION_V5_HELDOUT_FIXTURES.json`
- `docs/r50/C126_VISION_V5_HELDOUT_SMOKE.json`
- `docs/r50/C126b_VISION_GATE_V5_HELDOUT_CLAIM.json` (only if claimed)
- `docs/r50/C127_MONEY_TOOL_CAPTURE_E2E.json`
- `docs/r50/C128_REAL_SCREENSHOT_OFFICE.json`
- `docs/r50/C129_REPLACE_COST_REFRESH.json`
- `docs/r50/C130_GEN11_HOLD.json`
- `docs/CHECKPOINT_NOW.md`

## Honesty
- No fake VL scores. Heldout claim only when rate>=0.6.
- U2C arithmetic still tool-backed (C120 ceiling).
- gen11 seal not opened.
"""
    (ROOT / "docs" / "STAGE_ANT_C130.md").write_text(stage, encoding="utf-8")

    ck = f"""# CHECKPOINT_NOW — {ts()} — 蚁算模型

**R50PLUS=YES** — C125-C130 landed

Gate **0.6**. Gate2/3 untouched. gen11 **HOLD**.

## C125-C130
- **C125** V5 heldout fixtures n={c125.get('n_fixtures')} pass={c125.get('pass')}
- **C126** V5 heldout smoke rate=**{c126.get('rate')}** claim=**{c126.get('claim')}**
- **C127** money_tool capture E2E pass=**{c127.get('pass')}** rate=**{c127.get('rate')}**
- **C128** real screenshot office pass=**{c128.get('pass')}** rate=**{c128.get('rate')}** use_vl={c128.get('use_vl')}
- **C129** replace/cost ratio=**{c129.get('step_ratio_agent_over_bare')}** pass={c129.get('pass')}
- **C130** gen11 HOLD

## Product defaults
- Vision dense-table: **bare**
- Money math: **tool-backed** (`evo/office/money_tool.py` wired into `ant_capture_office_lib`)
- U2C absorb gate: **not claimed**

## Untouched
- Gate2 / Gate3 text claims
- Vision V0-V5 train claims
- gen11 seal closed
"""
    (ROOT / "docs" / "CHECKPOINT_NOW.md").write_text(ck, encoding="utf-8")

    # append loop
    loop = ROOT / "docs" / "蚁算_R50PLUS_LOOP.md"
    if loop.is_file():
        prev = loop.read_text(encoding="utf-8")
    else:
        prev = "# 蚁算 R50PLUS LOOP\n\n"
    block = f"""
## C125-C130 @ {ts()}
- C125 heldout fixtures pass={c125.get('pass')} n={c125.get('n_fixtures')}
- C126 heldout rate={c126.get('rate')} claim={c126.get('claim')}
- C127 money_tool E2E pass={c127.get('pass')} rate={c127.get('rate')}
- C128 screenshot office pass={c128.get('pass')} rate={c128.get('rate')}
- C129 replace ratio={c129.get('step_ratio_agent_over_bare')}
- C130 gen11 HOLD
- Iron: Gate 0.6, Gate2/3 untouched
"""
    loop.write_text(prev.rstrip() + "\n" + block, encoding="utf-8")

    print(json.dumps({"cycle": "C130", "gen11": "HOLD", "summary": hold["summary"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
