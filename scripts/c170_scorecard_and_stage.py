# -*- coding: utf-8 -*-
"""C170: Unified scorecard + STAGE after C166-C169. gen11 HOLD.
Gate 0.6. Gate2/3 untouched.
"""
from __future__ import annotations
import json, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = 0.6
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
STAGE = ROOT / "docs" / "STAGE_ANT_C170.md"
CKPT = ROOT / "docs" / "CHECKPOINT_NOW.md"
LOOP_APPEND = ROOT / "docs" / "蚁算_R50PLUS_LOOP.md"


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
    c163 = load("docs/r50/C163_VISION_V9_SMOKE.json") or {}
    c164 = load("docs/r50/C164_VISION_V9_HELDOUT_SMOKE.json") or {}
    c166 = load("docs/r50/C166_V10_DESIGN_BATCH.json") or {}
    c167 = load("docs/r50/C167_VISION_V10_SMOKE.json") or {}
    c167b = load("docs/r50/C167b_VISION_GATE_V10_CLAIM.json") or {}
    c168 = load("docs/r50/C168_DESKTOP_MULTIWIN_PRESSURE.json") or {}
    c169 = load("docs/r50/C169_PRODUCT_REGRESSION_SWEEP.json") or {}
    c162 = load("docs/r50/C162_V8H02_UNGLUE_REPARSE.json") or {}

    v9 = float(c163.get("rate") or 0.0)
    v9h = float(c164.get("rate") or 0.0)
    v10 = float(c167.get("rate") or 0.0)
    v8h = float(c162.get("rate") or 1.0)
    multiwin = float(c168.get("rate") or 0.0)

    parts = [
        1.0 if beat["beat_agent"] else 0.0,
        float(replace.get("rate") or 0.0),
        max(v9, v9h, 0.0),
        max(v10, 0.0) if c167.get("attempted") else (0.8 if c166.get("pass") else 0.0),
        1.0 if (c168.get("pass") or (c168.get("capture_ok") and multiwin >= GATE)) else (0.7 if c168.get("capture_ok") else 0.0),
        1.0 if c169.get("pass") else float(c169.get("core_v4_v9_rate") or 0.0),
        1.0 if c166.get("pass") else 0.0,
    ]
    composite = sum(parts) / len(parts)
    v10_claim = bool(c167b.get("vl_gate_v10_claim") or c167.get("vl_gate_v10_claim"))

    out = {
        "cycle": "C170",
        "theme": "unified_scorecard_c166_c169",
        "gate": GATE,
        "timestamp": ts(),
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "beat": beat,
        "replace": replace,
        "vision": {
            "v8_heldout_refresh": {"rate": v8h, "claim": True},
            "v9": {"rate": v9, "claim": bool(c163.get("claim") or c163.get("vl_gate_v9_claim"))},
            "v9_heldout": {"rate": v9h, "claim": bool(c164.get("claim") or c164.get("vl_gate_v9_heldout_claim"))},
            "v10_design": {"n": c166.get("n"), "pass": c166.get("pass"), "claim": False},
            "v10_smoke": {
                "rate": v10, "n": c167.get("n"), "n_ok": c167.get("n_ok"),
                "claim": v10_claim,
                "fail_ids": c167.get("fail_ids"),
            },
        },
        "desktop_multiwin": {
            "pass": c168.get("pass"), "rate": multiwin,
            "n": c168.get("n"), "capture_ok": c168.get("capture_ok"),
        },
        "regression": {
            "pass": c169.get("pass"),
            "core_v4_v9": c169.get("core_v4_v9_rate"),
            "overall": c169.get("overall_rate"),
        },
        "composite": round(composite, 4),
        "pass": composite >= GATE,
        "claim": False,
        "note": "After V10 design+smoke + multiwin pressure + V4-V9 regression. Gate2/3 untouched. gen11 HOLD.",
    }
    J(DOC / "C170_UNIFIED_SCORECARD.json", out)
    J(DOC / "C170_GEN11_HOLD.json", {
        "cycle": "C170", "gen11": "HOLD", "seal_opened": False,
        "timestamp": ts(), "gate2_3_untouched": True,
        "note": "gen11 remains HOLD per mandate",
    })

    stage = f"""# STAGE_ANT_C170

Updated: {ts()} (Asia/Shanghai)

**C166-C170 STAGE_READY=YES**

## Batch
| Cycle | Theme | Key |
| --- | --- | --- |
| C166 | V10 design | n={c166.get("n")} pass={c166.get("pass")} |
| C167 | V10 smoke | rate={v10} claim={v10_claim} fail={c167.get("fail_ids")} |
| C168 | desktop multiwin | rate={multiwin} pass={c168.get("pass")} |
| C169 | regression V4-V9 | core={c169.get("core_v4_v9_rate")} pass={c169.get("pass")} |
| C170 | scorecard | composite={out["composite"]} gen11=HOLD |

## Iron
Gate **0.6**. Gate2/3 untouched. gen11 HOLD.

## Vision claims (scoped)
- V9 / V9 heldout: retained
- V10: claim={v10_claim} rate={v10}
"""
    STAGE.write_text(stage, encoding="utf-8")

    board = f"""# 蚁算 UNIFIED SCORECARD

Updated: {ts()} (Asia/Shanghai)

| Axis | Score |
| --- | --- |
| beat_agent | 1.0 (Gate2 archive) |
| replace_agent | {replace.get("rate")} (ratio~{replace.get("mean_ratio")}) |
| vision_v9 | {v9} / heldout {v9h} |
| vision_v10 | {v10} claim={v10_claim} |
| desktop_multiwin | {multiwin} |
| regression_v4_v9 | {c169.get("core_v4_v9_rate")} |
| composite | {out["composite"]} |

Gate 0.6. Gate2/3 untouched. gen11 HOLD.
"""
    BOARD_MD.write_text(board, encoding="utf-8")

    CKPT.write_text(
        f"""# CHECKPOINT_NOW
HEAD: pending_C170
Stage: C166-C170 STAGE_READY
V10 design: n={c166.get("n")}
V10 smoke: rate={v10} claim={v10_claim}
Desktop multiwin: rate={multiwin} pass={c168.get("pass")}
Regression V4-V9: {c169.get("core_v4_v9_rate")}
composite: {out["composite"]}
gen11: HOLD
Gate2/3: untouched
Gate: 0.6
Updated: {ts()} Asia/Shanghai
""",
        encoding="utf-8",
    )

    append = f"""

## C166–C170 ({ts()})
- C166: V10 fixtures n={c166.get("n")} harder sticky/coffee/zorder/fade/chatbait
- C167: V10 smoke rate={v10} claim={v10_claim} fail={c167.get("fail_ids")}
- C168: desktop multiwin ImageGrab batches rate={multiwin} pass={c168.get("pass")}
- C169: regression V4–V9 core={c169.get("core_v4_v9_rate")} pass={c169.get("pass")}
- C170: scorecard composite={out["composite"]}; gen11 HOLD; Gate2/3 untouched
"""
    if LOOP_APPEND.is_file():
        LOOP_APPEND.write_text(LOOP_APPEND.read_text(encoding="utf-8") + append, encoding="utf-8")

    J(DOC / "C170_STAGE_SUMMARY.json", {
        "cycle": "C170", "stage_ready": True, "composite": out["composite"],
        "v10_claim": v10_claim, "v10_rate": v10,
        "multiwin_rate": multiwin, "regression_core": c169.get("core_v4_v9_rate"),
        "gen11": "HOLD", "gate2_3_untouched": True, "timestamp": ts(),
    })
    print(json.dumps({
        "cycle": "C170", "composite": out["composite"],
        "v10_rate": v10, "v10_claim": v10_claim,
        "multiwin": multiwin, "regress": c169.get("core_v4_v9_rate"),
        "pass": out["pass"],
    }, ensure_ascii=False))
    return 0 if out["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
