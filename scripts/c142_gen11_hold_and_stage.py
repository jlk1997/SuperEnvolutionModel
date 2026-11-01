# -*- coding: utf-8 -*-
"""C142: gen11 HOLD + stage docs for C137-C142. No seal open. Gate2/3 untouched."""
from __future__ import annotations
import json, sys
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
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def main():
    c137 = load("C137_VISION_V6_HELDOUT_FIXTURES.json") or {}
    c138 = load("C138_VISION_V6_HELDOUT_SMOKE.json") or {}
    c138b = load("C138b_VISION_GATE_V6_HELDOUT_CLAIM.json")
    c139 = load("C139_PRODUCT_DEMO_REGRESSION.json") or {}
    c140 = load("C140_CONFIDENCE_GATED_TOOL.json") or {}
    c141 = load("C141_UNIFIED_REPLACE_BOARD.json") or {}

    # gen11 HOLD: open only if fresh>=0.99 — not met / not attempted
    hold = {
        "cycle": "C142",
        "theme": "gen11_hold",
        "timestamp": ts(),
        "gen11": "HOLD",
        "seal_opened": False,
        "open_criteria": "fresh>=0.99 AND explicit operator unlock",
        "fresh_score": None,
        "reason": "continuous evolution focus on V6 heldout + product; heritability seal stays closed",
        "gate2_3_untouched": True,
        "gate": GATE,
        "pass": True,
        "claim": False,
    }
    J(DOC / "C142_GEN11_HOLD.json", hold)

    stage = {
        "stage": "ANT_C142",
        "cycles": "C137-C142",
        "timestamp": ts(),
        "gate": GATE,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "v6_heldout_fixtures": {"pass": c137.get("pass"), "n": c137.get("n_fixtures")},
        "v6_heldout_smoke": {
            "rate": c138.get("rate"),
            "claim": c138.get("claim") or c138.get("vl_gate_v6_heldout_claim"),
            "n": c138.get("n"),
            "n_ok": c138.get("n_ok"),
            "claim_file": bool(c138b),
        },
        "product_regression": {"pass": c139.get("pass"), "rate": c139.get("rate")},
        "confidence_gated_tool": {"pass": c140.get("pass"), "rate": c140.get("rate"), "innovation": True},
        "replace_board": {
            "pass": c141.get("pass"),
            "rate": c141.get("rate"),
            "mean_step_ratio": c141.get("mean_step_ratio"),
        },
        "STAGE_READY": bool(
            c137.get("pass")
            and c138.get("pass")
            and (c138.get("claim") or c138.get("vl_gate_v6_heldout_claim") or (c138.get("rate") or 0) >= GATE)
            and c139.get("pass")
            and c140.get("pass")
            and c141.get("pass")
        ),
    }
    J(DOC / "C142_STAGE_SUMMARY.json", stage)

    md = ROOT / "docs" / "STAGE_ANT_C142.md"
    md.write_text(
        f"""# STAGE_ANT_C142 — 蚁算 R50+ C137-C142

Updated: {ts()} (Asia/Shanghai)

## Status
- **V6 heldout fixtures**: pass={c137.get('pass')} n={c137.get('n_fixtures')}
- **V6 heldout smoke**: rate={c138.get('rate')} claim={c138.get('claim') or c138.get('vl_gate_v6_heldout_claim')} n={c138.get('n')}/{c138.get('n_ok')}
- **Product demo regression**: pass={c139.get('pass')} rate={c139.get('rate')}
- **Confidence-gated tool (innovation)**: pass={c140.get('pass')} rate={c140.get('rate')}
- **Unified replace board refresh**: pass={c141.get('pass')} mean_ratio={c141.get('mean_step_ratio')}
- **gen11**: HOLD (seal not opened)
- **Gate**: 0.6 — Gate2/3 untouched
- **STAGE_READY**: {stage['STAGE_READY']}

## Evidence
- `docs/r50/C137_VISION_V6_HELDOUT_FIXTURES.json`
- `docs/r50/C138_VISION_V6_HELDOUT_SMOKE.json`
- `docs/r50/C138b_VISION_GATE_V6_HELDOUT_CLAIM.json` (only if claimed)
- `docs/r50/C139_PRODUCT_DEMO_REGRESSION.json`
- `docs/r50/C140_CONFIDENCE_GATED_TOOL.json`
- `docs/r50/C141_UNIFIED_REPLACE_BOARD.json`
- `docs/r50/C142_GEN11_HOLD.json`
- `docs/蚁算_CONFIDENCE_GATED_TOOL.md`
- `docs/蚁算_UNIFIED_REPLACE_BOARD.md`

## Honesty
- No fake VL scores. V6 heldout claim only when rate>=0.6 with real VL.
- Confidence gate prefers tool on disagreement; no absorb claim.
- gen11 seal not opened.
- Prior V0–V6 train / Gate2 / Gate3 untouched.
""",
        encoding="utf-8",
    )

    # checkpoint + loop append
    ck = ROOT / "docs" / "CHECKPOINT_NOW.md"
    ck.write_text(
        f"""# CHECKPOINT_NOW — 蚁算

Updated: {ts()} (Asia/Shanghai)

## Latest
- HEAD to be filled by commit
- Cycles **C137–C142** complete (see `docs/STAGE_ANT_C142.md`)
- V6 heldout claim: {c138.get('claim') or c138.get('vl_gate_v6_heldout_claim')} rate={c138.get('rate')}
- Innovation: confidence-gated money_tool (`docs/蚁算_CONFIDENCE_GATED_TOOL.md`)
- Replace board mean_ratio={c141.get('mean_step_ratio')}
- gen11 **HOLD** · Gate **0.6** · Gate2/3 **untouched**

## Iron
- Do not reopen Gate2/3 claims
- Do not open gen11 seal without fresh>=0.99
- No synthetic VL pretending to be real
""",
        encoding="utf-8",
    )

    loop = ROOT / "docs" / "蚁算_R50PLUS_LOOP.md"
    line = (
        f"\n## C137-C142 @ {ts()}\n"
        f"- C137 heldout fixtures pass={c137.get('pass')} n={c137.get('n_fixtures')}\n"
        f"- C138 heldout rate={c138.get('rate')} claim={c138.get('claim') or c138.get('vl_gate_v6_heldout_claim')}\n"
        f"- C139 regression pass={c139.get('pass')} rate={c139.get('rate')}\n"
        f"- C140 confidence-gate pass={c140.get('pass')} rate={c140.get('rate')}\n"
        f"- C141 replace mean_ratio={c141.get('mean_step_ratio')} pass={c141.get('pass')}\n"
        f"- C142 gen11 HOLD\n"
        f"- Iron: Gate 0.6, Gate2/3 untouched\n"
    )
    if loop.is_file():
        body = loop.read_text(encoding="utf-8")
        if "## C137-C142 @" not in body:
            loop.write_text(body.rstrip() + line, encoding="utf-8")
    else:
        loop.write_text("# 蚁算 R50+ LOOP\n" + line, encoding="utf-8")

    print(json.dumps({
        "cycle": "C142", "STAGE_READY": stage["STAGE_READY"], "gen11": "HOLD",
        "v6h_claim": c138.get("claim") or c138.get("vl_gate_v6_heldout_claim"),
        "v6h_rate": c138.get("rate"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
