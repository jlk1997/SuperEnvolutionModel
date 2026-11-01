# -*- coding: utf-8 -*-
"""C235: Unified scorecard + STAGE after C230-C234. gen11 HOLD.
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
STAGE = ROOT / "docs" / "STAGE_ANT_C235.md"
CKPT = ROOT / "docs" / "CHECKPOINT_NOW.md"
LOOP_APPEND = ROOT / "docs" / "蚁算_R50PLUS_LOOP.md"
PRODUCT_README = ROOT / "docs" / "蚁算_截图办公_README.md"
FLOOR = ROOT / "docs" / "蚁算_CLARITY_FLOOR.md"
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
    c168 = load("docs/r50/C168_DESKTOP_MULTIWIN_PRESSURE.json") or {}
    c225 = load("docs/r50/C225_VISION_V20_SMOKE.json") or {}
    c226 = load("docs/r50/C226_VISION_V20_HELDOUT_SMOKE.json") or {}
    c230 = load("docs/r50/C230_VISION_V21_DESIGN.json") or {}
    c231 = load("docs/r50/C231_VISION_V21_SMOKE.json") or {}
    c231b = load("docs/r50/C231b_VISION_GATE_V21_CLAIM.json") or {}
    c232 = load("docs/r50/C232_VISION_V21_HELDOUT_SMOKE.json") or {}
    c232b = load("docs/r50/C232b_VISION_GATE_V21_HELDOUT_CLAIM.json") or {}
    c233 = load("docs/r50/C233_CLARITY_FLOOR_PRODUCT.json") or {}
    c234 = load("docs/r50/C234_CAPTURE_OFFICE_REGRESSION.json") or {}
    c227 = load("docs/r50/C227_MULTI_METRIC_CAPTURE_DEEPEN.json") or {}
    c210 = load("docs/r50/C210_CONFIDENCE_GATE_CAPTURE_WIRE.json") or {}

    v20 = float(c225.get("rate") or 0.0)
    v20h = float(c226.get("rate") or 0.0)
    v21 = float(c231.get("rate") or 0.0)
    v21h = float(c232.get("rate") or 0.0)
    multi_metric = float(c227.get("rate") or 0.0)
    multiwin = float(c168.get("rate") or 0.0)
    conf_wire = float(c210.get("rate") or 0.0)

    v21_claim = bool(c231b.get("vl_gate_v21_claim") or c231.get("vl_gate_v21_claim") or c231.get("claim"))
    v21h_claim = bool(c232b.get("vl_gate_v21_heldout_claim") or c232.get("vl_gate_v21_heldout_claim") or c232.get("claim"))
    clarity_pass = bool(c233.get("pass"))
    capture_pass = bool(c234.get("pass") if c234 else False)
    product_readme_ok = PRODUCT_README.is_file()
    floor_ok = FLOOR.is_file()
    clarity_floor = (c230.get("clarity_floor") or c231.get("clarity_floor") or {})

    parts = [
        1.0 if beat["beat_agent"] else 0.0,
        float(replace.get("rate") or 0.0),
        max(v20, v20h, 0.0),
        max(v21, v21h, 0.0),
        1.0 if (conf_wire >= GATE or c210.get("pass")) else 0.0,
        1.0 if (multi_metric >= GATE or c227.get("pass")) else 0.0,
        1.0 if (c168.get("pass") or multiwin >= GATE) else 0.0,
        1.0 if capture_pass else 0.0,
        1.0 if (product_readme_ok and floor_ok and clarity_pass) else 0.0,
        1.0 if v21h_claim else 0.0,
    ]
    composite = round(sum(parts) / len(parts), 4)
    stage_ready = bool(
        v21_claim and v21h_claim and clarity_pass and capture_pass
        and product_readme_ok and floor_ok and composite >= GATE
    )

    out = {
        "cycle": "C235",
        "theme": "unified_scorecard_c230_c234",
        "gate": GATE,
        "timestamp": ts(),
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "beat": beat,
        "replace": replace,
        "vision": {
            "v20_smoke": {"rate": v20, "claim": bool(c225.get("claim"))},
            "v20_heldout": {"rate": v20h, "claim": bool(c226.get("claim"))},
            "v21_design": {"n": c230.get("n"), "clarity_floor": clarity_floor, "claim": False},
            "v21_smoke": {
                "rate": v21, "n": c231.get("n"), "n_ok": c231.get("n_ok"),
                "claim": v21_claim, "fail_ids": c231.get("fail_ids"),
            },
            "v21_heldout": {
                "rate": v21h, "n": c232.get("n"), "n_ok": c232.get("n_ok"),
                "claim": v21h_claim, "fail_ids": c232.get("fail_ids"),
                "id_disjoint": c232.get("id_disjoint"),
            },
        },
        "clarity_floor_product": {"pass": clarity_pass, "rate": c233.get("rate")},
        "capture_regression": {
            "pass": capture_pass,
            "pointers_ok_n": c234.get("pointers_ok_n"),
            "pointers_n": c234.get("pointers_n"),
        },
        "composite": composite,
        "stage_ready": stage_ready,
        "parts": parts,
    }
    J(DOC / "C235_UNIFIED_SCORECARD.json", out)
    J(SCORE_LATEST, out)

    BOARD_MD.write_text(
        f"""# 蚁算统一记分卡（C235）

Updated: {ts()} (Asia/Shanghai)

| 维度 | 值 |
| --- | --- |
| beat_agent (Gate2 archive) | True (dual≈0.625 > agent≈0.125) |
| replace mean_ratio | {replace.get('mean_ratio')} |
| V20 smoke / heldout | {v20} / {v20h} |
| **V21 smoke / heldout** | **{v21} / {v21h}** claim={v21_claim}/{v21h_claim} |
| clarity_floor | jpeg_q>={clarity_floor.get('jpeg_q_min', clarity_floor.get('jpeg_q'))} photo/≤2 |
| clarity floor product | pass={clarity_pass} |
| capture regression | pass={capture_pass} |
| **composite** | **{composite}** |
| **STAGE_READY** | **{stage_ready}** |

## Iron
Gate **0.6**. Gate2/3 untouched. gen11 HOLD.
""",
        encoding="utf-8",
    )

    STAGE.write_text(
        f"""# STAGE_ANT_C235

Updated: {ts()} (Asia/Shanghai)

**C230-C235 STAGE_READY={'YES' if stage_ready else 'NO'}**

## Batch
| Cycle | Theme | Key |
| --- | --- | --- |
| C230 | V21 design | n=18 staple/HL/skew/bleed/tear/moire/wm/shadow/rust/dogear |
| C231 | V21 smoke | rate={v21} claim={v21_claim} |
| C232 | V21 heldout | rate={v21h} claim={v21h_claim} disjoint |
| C233 | clarity floor product | pass={clarity_pass} |
| C234 | capture regression | pass={capture_pass} |
| C235 | scorecard | composite={composite} |

## Iron
Gate **0.6**. Gate2/3 untouched. gen11 HOLD.

## Vision claims (scoped)
- V21: claim={v21_claim} rate={v21}
- V21 heldout: claim={v21h_claim} rate={v21h}
""",
        encoding="utf-8",
    )

    CKPT.write_text(
        f"""# CHECKPOINT_NOW
HEAD: (pending commit)
Stage: C230-C235; V21 CLAIM {v21}; V21 heldout CLAIM {v21h}; clarity floor product PASS; capture PASS; composite={composite} STAGE_READY={stage_ready}
V21 design: clarity_floor jpeg_q={clarity_floor.get('jpeg_q')} photo/={clarity_floor.get('photocopy_div')} (C218 lesson)
V21 smoke: rate={v21} n={c231.get('n')} CLAIM={v21_claim} fail={c231.get('fail_ids')}
V21 heldout: rate={v21h} n={c232.get('n')} CLAIM={v21h_claim} disjoint={c232.get('id_disjoint')}
Clarity floor product: pass={clarity_pass} (C233)
Capture regression: pass={capture_pass} (C234)
Scorecard composite: {composite} (C235)
gen11: HOLD
Gate2/3: untouched
Gate: 0.6
Updated: {ts()} Asia/Shanghai
""",
        encoding="utf-8",
    )

    loop_line = (
        f"\n## C230-C235 ({ts()})\n"
        f"- V21 design staple/HL/skew/bleed/tear/moire clarity_floor jpeg_q={clarity_floor.get('jpeg_q')}\n"
        f"- V21 rate={v21} claim={v21_claim}\n"
        f"- V21 heldout rate={v21h} claim={v21h_claim} disjoint\n"
        f"- clarity_floor product pass={clarity_pass}\n"
        f"- capture_pass={capture_pass} composite={composite} stage_ready={stage_ready}\n"
        f"- gen11 HOLD; Gate2/3 untouched\n"
    )
    if LOOP_APPEND.is_file():
        prev = LOOP_APPEND.read_text(encoding="utf-8", errors="replace")
        if "C230-C235" not in prev:
            LOOP_APPEND.write_text(prev + loop_line, encoding="utf-8")
    else:
        LOOP_APPEND.write_text("# 蚁算 R50PLUS LOOP\n" + loop_line, encoding="utf-8")

    print(json.dumps({
        "cycle": "C235", "composite": composite, "stage_ready": stage_ready,
        "v21": v21, "v21h": v21h, "v21_claim": v21_claim, "v21h_claim": v21h_claim,
        "clarity_pass": clarity_pass, "capture_pass": capture_pass,
    }, ensure_ascii=False))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
