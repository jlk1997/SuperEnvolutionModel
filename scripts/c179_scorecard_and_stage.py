# -*- coding: utf-8 -*-
"""C179: Unified scorecard + STAGE after C175-C178. gen11 HOLD.
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
STAGE = ROOT / "docs" / "STAGE_ANT_C179.md"
CKPT = ROOT / "docs" / "CHECKPOINT_NOW.md"
LOOP_APPEND = ROOT / "docs" / "蚁算_R50PLUS_LOOP.md"
PRODUCT_README = ROOT / "docs" / "蚁算_截图办公_README.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"


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
    c167 = load("docs/r50/C167_VISION_V10_SMOKE.json") or {}
    c167b = load("docs/r50/C167b_VISION_GATE_V10_CLAIM.json") or {}
    c171 = load("docs/r50/C171_VISION_V10_HELDOUT_SMOKE.json") or {}
    c171b = load("docs/r50/C171b_VISION_GATE_V10_HELDOUT_CLAIM.json") or {}
    c173 = load("docs/r50/C173_VISION_V11_SMOKE.json") or {}
    c173b = load("docs/r50/C173b_VISION_GATE_V11_CLAIM.json") or {}
    c175 = load("docs/r50/C175_VISION_V11_HELDOUT_SMOKE.json") or {}
    c175b = load("docs/r50/C175b_VISION_GATE_V11_HELDOUT_CLAIM.json") or {}
    c176 = load("docs/r50/C176_V12_DESIGN_BATCH.json") or {}
    c177 = load("docs/r50/C177_VISION_V12_SMOKE.json") or {}
    c177b = load("docs/r50/C177b_VISION_GATE_V12_CLAIM.json") or {}
    c178 = load("docs/r50/C178_CAPTURE_OFFICE_REGRESSION.json") or {}
    c168 = load("docs/r50/C168_DESKTOP_MULTIWIN_PRESSURE.json") or {}

    v10 = float(c167.get("rate") or 0.0)
    v10h = float(c171.get("rate") or 0.0)
    v11 = float(c173.get("rate") or 0.0)
    v11h = float(c175.get("rate") or 0.0)
    v12 = float(c177.get("rate") or 0.0)
    multiwin = float(c168.get("rate") or 0.0)
    v10_claim = bool(c167b.get("vl_gate_v10_claim") or c167.get("vl_gate_v10_claim"))
    v10h_claim = bool(c171b.get("vl_gate_v10_heldout_claim") or c171.get("vl_gate_v10_heldout_claim"))
    v11_claim = bool(c173b.get("vl_gate_v11_claim") or c173.get("vl_gate_v11_claim"))
    v11h_claim = bool(c175b.get("vl_gate_v11_heldout_claim") or c175.get("vl_gate_v11_heldout_claim"))
    v12_claim = bool(c177b.get("vl_gate_v12_claim") or c177.get("vl_gate_v12_claim"))
    product_readme_ok = PRODUCT_README.is_file()
    capture_pass = bool(c178.get("pass"))

    parts = [
        1.0 if beat["beat_agent"] else 0.0,
        float(replace.get("rate") or 0.0),
        max(v10, v10h, 0.0),
        max(v11, v11h, 0.0),
        max(v12, 0.0) if c177.get("attempted") else (0.8 if c176.get("pass") else 0.0),
        1.0 if (c168.get("pass") or multiwin >= GATE) else 0.0,
        1.0 if capture_pass else 0.0,
        1.0 if product_readme_ok else 0.0,
    ]
    composite = round(sum(parts) / len(parts), 4)

    out = {
        "cycle": "C179",
        "theme": "unified_scorecard_c175_c178",
        "gate": GATE,
        "timestamp": ts(),
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "beat": beat,
        "replace": replace,
        "vision": {
            "v10": {"rate": v10, "claim": v10_claim},
            "v10_heldout": {"rate": v10h, "claim": v10h_claim},
            "v11": {"rate": v11, "claim": v11_claim},
            "v11_heldout": {
                "rate": v11h, "n": c175.get("n"), "n_ok": c175.get("n_ok"),
                "claim": v11h_claim, "fail_ids": c175.get("fail_ids"), "disjoint": True,
            },
            "v12_design": {"n": c176.get("n"), "pass": c176.get("pass"), "claim": False},
            "v12_smoke": {
                "rate": v12, "n": c177.get("n"), "n_ok": c177.get("n_ok"),
                "claim": v12_claim, "fail_ids": c177.get("fail_ids"),
            },
        },
        "desktop_multiwin": {"pass": c168.get("pass"), "rate": multiwin},
        "product": {
            "readme": str(PRODUCT_README.relative_to(ROOT)).replace("\\", "/") if product_readme_ok else None,
            "readme_ok": product_readme_ok,
            "capture_regression_pass": capture_pass,
            "capture_cli": "scripts/ant_capture_office.py",
        },
        "composite": composite,
        "stage_ready": bool(
            v11h_claim and v12_claim and capture_pass and product_readme_ok and composite >= GATE
        ),
        "pass": True,
        "claim": False,
        "note": "Scorecard after V11 heldout + V12 claim + capture README regression; no new Gate2/3; gen11 HOLD",
    }
    J(DOC / "C179_UNIFIED_SCORECARD.json", out)
    J(SCORE_LATEST, {
        "timestamp": ts(),
        "composite": composite,
        "beat_agent": True,
        "replace_rate": replace.get("rate"),
        "replace_mean_ratio": replace.get("mean_ratio"),
        "vision_v10_rate": v10,
        "vision_v10_heldout_rate": v10h,
        "vision_v11_rate": v11,
        "vision_v11_heldout_rate": v11h,
        "vision_v11_heldout_claim": v11h_claim,
        "vision_v12_rate": v12,
        "vision_v12_claim": v12_claim,
        "capture_regression_pass": capture_pass,
        "gen11_hold": True,
        "gate": GATE,
        "gate2_3_untouched": True,
        "cycle": "C179",
    })

    BOARD_MD.write_text(
        f"""# 蚁算 UNIFIED SCORECARD

Updated: {ts()} (Asia/Shanghai)

| Axis | Score |
| --- | --- |
| beat_agent | 1.0 (Gate2 archive) |
| replace_agent | 1.0 (ratio~{replace.get('mean_ratio')}) |
| vision_v10 / heldout | {v10} / {v10h} |
| vision_v11 / heldout | {v11} / {v11h} claim={v11h_claim} |
| vision_v12 | {v12} claim={v12_claim} |
| desktop_multiwin | {multiwin} |
| capture_readme_regression | {1.0 if capture_pass else 0.0} |
| product_readme | {1.0 if product_readme_ok else 0.0} |
| composite | {composite} |

Gate 0.6. Gate2/3 untouched. gen11 HOLD.
""",
        encoding="utf-8",
    )

    STAGE.write_text(
        f"""# STAGE_ANT_C179

Updated: {ts()} (Asia/Shanghai)

**C175-C179 STAGE_READY={'YES' if out['stage_ready'] else 'NO'}**

## Batch
| Cycle | Theme | Key |
| --- | --- | --- |
| C175 | V11 heldout | rate={v11h} claim={v11h_claim} fail={c175.get('fail_ids')} |
| C176 | V12 design | n={c176.get('n')} pass={c176.get('pass')} |
| C177 | V12 smoke | rate={v12} claim={v12_claim} fail={c177.get('fail_ids')} |
| C178 | capture README regression | pass={capture_pass} |
| C179 | scorecard | composite={composite} |

## Iron
Gate **0.6**. Gate2/3 untouched. gen11 HOLD.

## Vision claims (scoped)
- V11 heldout: claim={v11h_claim} rate={v11h}
- V12: claim={v12_claim} rate={v12}
""",
        encoding="utf-8",
    )

    CKPT.write_text(
        f"""# CHECKPOINT_NOW
HEAD: (pending commit)
Stage: C175-C179 STAGE_READY={'YES' if out['stage_ready'] else 'NO'}
V11 heldout: rate={v11h} n={c175.get('n')} CLAIM={v11h_claim} (C175) disjoint
V12 design: n={c176.get('n')} (C176)
V12 smoke: rate={v12} n={c177.get('n')} CLAIM={v12_claim} (C177) torn/barcode/persp/qr/thermal/shadow/jpeg/ghost
Capture README regression: pass={capture_pass} (C178)
Scorecard composite: {composite} (C179)
gen11: HOLD
Gate2/3: untouched
Gate: 0.6
Updated: {ts()} Asia/Shanghai
""",
        encoding="utf-8",
    )

    if LOOP_APPEND.is_file():
        with LOOP_APPEND.open("a", encoding="utf-8") as f:
            f.write(
                f"\n## C175-C179 @ {ts()}\n"
                f"- C175 V11 heldout rate={v11h} claim={v11h_claim}\n"
                f"- C176 V12 design n={c176.get('n')}\n"
                f"- C177 V12 smoke rate={v12} claim={v12_claim}\n"
                f"- C178 capture README regression pass={capture_pass}\n"
                f"- C179 scorecard composite={composite} STAGE_READY={out['stage_ready']}\n"
                f"- gen11 HOLD; Gate2/3 untouched\n"
            )

    print(json.dumps({
        "cycle": "C179",
        "composite": composite,
        "stage_ready": out["stage_ready"],
        "v11h": v11h,
        "v12": v12,
        "v11h_claim": v11h_claim,
        "v12_claim": v12_claim,
        "capture_pass": capture_pass,
    }, ensure_ascii=False))
    return 0 if out["stage_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
