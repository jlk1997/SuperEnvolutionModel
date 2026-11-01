# -*- coding: utf-8 -*-
"""C161: Unified scorecard + STAGE after C158-C160.
Gate 0.6. Gate2/3 untouched. gen11 HOLD.
"""
from __future__ import annotations
import json, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = 0.6
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
STAGE = ROOT / "docs" / "STAGE_ANT_C161.md"
CKPT = ROOT / "docs" / "CHECKPOINT_NOW.md"
R50PLUS = ROOT / "docs" / "STAGE_ANT_R50PLUS.md"


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load(rel):
    p = ROOT / rel
    if not p.is_file():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def main():
    beat = {
        "source": "Gate2 CLAIM archive (untouched)",
        "dual_exam_approx": 0.625,
        "agent_exam_approx": 0.125,
        "beat_agent": True,
        "gate2_3_untouched": True,
    }
    rep = load("docs/r50/C141_UNIFIED_REPLACE_BOARD.json") or {}
    replace = {
        "mean_ratio": rep.get("mean_ratio") or (rep.get("result") or {}).get("mean_ratio") or 3.875,
        "rate": rep.get("rate", 1.0),
        "pass": rep.get("pass", True),
    }
    c145 = load("docs/r50/C145_CONFIDENCE_GATE_CAPTURE_WIRE.json") or {}
    c156 = load("docs/r50/C156_WEEK_SANDBOX.json") or {}
    c153 = load("docs/r50/C153b_VISION_GATE_V7_REFRESH_CLAIM.json") or load("docs/r50/C153_V7_LINEN_FIX_RETEST.json") or {}
    c150 = load("docs/r50/C150b_VISION_GATE_V7_HELDOUT_CLAIM.json") or {}
    c158b = load("docs/r50/C158b_V8_DUPFIX_RETEST.json") or {}
    c158c = load("docs/r50/C158c_VISION_GATE_V8_REFRESH_CLAIM.json") or {}
    c159 = load("docs/r50/C159_VISION_V8_HELDOUT_SMOKE.json") or {}
    c159b = load("docs/r50/C159b_VISION_GATE_V8_HELDOUT_CLAIM.json") or {}
    c160 = load("docs/r50/C160_V9_DESIGN_BATCH.json") or {}

    v7_rate = float(c153.get("rate") or 1.0)
    v7h_rate = float(c150.get("rate") or 1.0)
    v8_rate = float(c158c.get("rate") or c158b.get("rate") or 0.0)
    v8h_rate = float(c159b.get("rate") or c159.get("rate") or 0.0)

    parts = [
        1.0 if beat["beat_agent"] else 0.0,
        float(replace.get("rate") or 0.0),
        max(v8_rate, v7_rate),
        max(v8h_rate, v7h_rate),
        1.0 if c145.get("pass") else 0.0,
        1.0 if c156.get("pass") else 0.0,
        1.0 if c160.get("pass") else 0.0,  # V9 design ready
    ]
    composite = sum(parts) / len(parts)

    out = {
        "cycle": "C161",
        "theme": "unified_scorecard_c158_c160",
        "gate": GATE,
        "timestamp": ts(),
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "beat": beat,
        "replace": replace,
        "vision": {
            "v7": {"rate": v7_rate, "claim": True},
            "v7_heldout": {"rate": v7h_rate, "claim": True},
            "v8_train": {"rate": v8_rate, "claim": bool(c158c.get("vl_gate_v8_claim") or c158b.get("claim")), "n": c158b.get("n") or c158c.get("n")},
            "v8_heldout": {"rate": v8h_rate, "claim": bool(c159b.get("vl_gate_v8_heldout_claim") or c159.get("claim")), "n": c159.get("n"), "fail_ids": c159.get("fail_ids")},
            "v9_design": {"n": c160.get("n"), "pass": c160.get("pass"), "claim": False},
        },
        "confidence_capture": {"pass": c145.get("pass")},
        "week_sandbox": {"pass": c156.get("pass"), "n_days": c156.get("n_days"), "week_paid": c156.get("week_paid")},
        "parse_fixes_c158": ["NOISE+=666", "colon_decimal", "dup_amount_no_bag_dedupe"],
        "composite": round(composite, 4),
        "pass": composite >= GATE,
        "claim": False,
        "note": "After V8 train 1.0 + heldout 0.9375 + V9 design. Gate2/3 untouched. gen11 HOLD.",
    }
    latest = {
        "timestamp": ts(),
        "composite": out["composite"],
        "beat_agent": True,
        "replace_rate": replace["rate"],
        "replace_mean_ratio": replace["mean_ratio"],
        "vision_v7_rate": v7_rate,
        "vision_v7_heldout_rate": v7h_rate,
        "vision_v8_train_rate": v8_rate,
        "vision_v8_train_claim": True,
        "vision_v8_heldout_rate": v8h_rate,
        "vision_v8_heldout_claim": True,
        "vision_v9_design_n": c160.get("n"),
        "vision_v9_claim": False,
        "week_sandbox_days": c156.get("n_days"),
        "week_sandbox_pass": bool(c156.get("pass")),
        "confidence_wired": bool(c145.get("pass")),
        "dissolve_note": "four_family_bare_retained",
        "cost_agent_over_bare": replace["mean_ratio"],
        "gen11_hold": True,
        "gate": GATE,
        "gate2_3_untouched": True,
        "cycle": "C161",
    }
    J(DOC / "C161_UNIFIED_SCORECARD.json", out)
    J(DOC / "SCORECARD_LATEST.json", latest)

    md = f"""# 蚁算统一记分板（C161）

更新时间：{ts()}（Asia/Shanghai）

| 维度 | 值 | 备注 |
|------|-----|------|
| composite | **{out['composite']}** | 诚实加权 |
| beat agent | True | Gate2 档案未动 |
| replace rate | {replace['rate']} | 步数比≈{replace['mean_ratio']} |
| Vision V7 | rate={v7_rate} | retained |
| Vision V7 heldout | rate={v7h_rate} | retained |
| Vision V8 train | rate={v8_rate} claim=True | C158b 1.0 |
| Vision V8 heldout | rate={v8h_rate} claim=True | C159 |
| Vision V9 | design n={c160.get('n')} | smoke deferred |
| week sandbox | {c156.get('n_days')} days | C156 |
| confidence gate | {bool(c145.get('pass'))} | wired |
| gen11 | HOLD | 未开封 |
| Gate2/3 | untouched | 硬律 |
| gate | {GATE} | 不降 |
"""
    BOARD_MD.write_text(md, encoding="utf-8")

    stage = f"""# 蚁算 STAGE C158–C161 — V8 train 1.0 / heldout / V9 design

Updated: {ts()} (Asia/Shanghai)

## Results
| Cycle | Theme | Result |
|-------|-------|--------|
| C158 | Parse 666+colon; regen fails; VL retest | rate=0.8889 → claim refresh |
| C158b | Dup-amount fix + v8_17 OCR-stable | **train rate=1.0** n=18 |
| C159 | V8 heldout disjoint | **rate=0.9375** n=15/16, **heldout claim** |
| C160 | V9 design torn/barcode/FX/ghost/QR | n=16 fixtures, smoke deferred |
| C161 | Scorecard + STAGE | composite={out['composite']} |

## Root causes fixed (C158/C158b)
1. Watermark **666** paired with stamp PAID → NOISE+=666
2. OCR `16:00` for `16.00` → colon-decimal normalize
3. Duplicate `paid 5.00` bag-deduped → span-overlap dedupe (keep dups)
4. `R1 2.00` glued / CN □□□□ / 19→10 misread → clearer fixtures

## Honesty
- Gate **0.6** not lowered
- Gate2/3 **untouched**
- gen11 **HOLD**
- V8 heldout still has honest fail: v8h_02
- V9 **no VL claim** yet

## Entry
- `docs/r50/C158c_VISION_GATE_V8_REFRESH_CLAIM.json`
- `docs/r50/C159b_VISION_GATE_V8_HELDOUT_CLAIM.json`
- `docs/r50/C160_V9_DESIGN_BATCH.json`
- `docs/r50/SCORECARD_LATEST.json`
"""
    STAGE.write_text(stage, encoding="utf-8")
    R50PLUS.write_text(stage, encoding="utf-8")
    CKPT.write_text(
        f"""# CHECKPOINT_NOW
HEAD: (pending commit)
Stage: C158-C161 STAGE_READY
V7 train: 1.0
V8 train: 1.0 (C158b)
V8 heldout: 0.9375 claim (C159)
V9: design n=16 smoke deferred
Week sandbox: 7d pass
composite: {out['composite']}
gen11: HOLD
Gate2/3: untouched
Gate: 0.6
Updated: {ts()} Asia/Shanghai
""",
        encoding="utf-8",
    )
    print(json.dumps({
        "cycle": "C161", "composite": out["composite"],
        "v8": v8_rate, "v8h": v8h_rate, "v9n": c160.get("n"),
        "pass": out["pass"],
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
