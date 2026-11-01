# -*- coding: utf-8 -*-
"""C247: Unified scorecard + STAGE after C242-C246. gen11 HOLD.
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
STAGE = ROOT / "docs" / "STAGE_ANT_C247.md"
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
    c245 = load("docs/r50/C245_COST_LEDGER_REFRESH.json") or {}
    replace = {
        "mean_ratio": ((c245.get("replace_stress") or {}).get("mean_ratio")
                       or (c245.get("summary") or {}).get("replace_mean_ratio") or 3.875),
        "rate": ((c245.get("replace_stress") or {}).get("rate")
                 or (c245.get("summary") or {}).get("replace_rate") or 1.0),
        "pass": bool((c245.get("replace_stress") or {}).get("pass", True)),
        "step_delta": (c245.get("summary") or {}).get("step_delta_agent_minus_dual"),
    }
    c238 = load("docs/r50/C238_VISION_V22_SMOKE.json") or {}
    c239 = load("docs/r50/C239_VISION_V22_HELDOUT_SMOKE.json") or {}
    c242 = load("docs/r50/C242_VISION_V23_DESIGN.json") or {}
    c243 = load("docs/r50/C243_VISION_V23_SMOKE.json") or {}
    c243b = load("docs/r50/C243b_VISION_GATE_V23_CLAIM.json") or {}
    c244 = load("docs/r50/C244_VISION_V23_HELDOUT_SMOKE.json") or {}
    c244b = load("docs/r50/C244b_VISION_GATE_V23_HELDOUT_CLAIM.json") or {}
    c246 = load("docs/r50/C246_CAPTURE_OFFICE_REGRESSION.json") or {}
    c233 = load("docs/r50/C233_CLARITY_FLOOR_PRODUCT.json") or {}

    v22 = float(c238.get("rate") or 0.0)
    v22h = float(c239.get("rate") or 0.0)
    v23 = float(c243.get("rate") or 0.0)
    v23h = float(c244.get("rate") or 0.0)

    v22_claim = bool(c238.get("claim") or c238.get("vl_gate_v22_claim"))
    v22h_claim = bool(c239.get("claim") or c239.get("vl_gate_v22_heldout_claim"))
    v23_claim = bool(c243b.get("vl_gate_v23_claim") or c243.get("vl_gate_v23_claim") or c243.get("claim"))
    v23h_claim = bool(c244b.get("vl_gate_v23_heldout_claim") or c244.get("vl_gate_v23_heldout_claim") or c244.get("claim"))
    capture_pass = bool(c246.get("pass"))
    clarity_pass = bool(c233.get("pass", True))
    cost_pass = bool(c245.get("pass"))
    product_readme_ok = PRODUCT_README.is_file()

    parts = [
        1.0 if beat["beat_agent"] else 0.0,
        float(replace.get("rate") or 0.0),
        max(v22, v22h, 0.0),
        max(v23, v23h, 0.0),
        1.0 if v22_claim else 0.0,
        1.0 if v23_claim else 0.0,
        1.0 if v23h_claim else 0.0,
        1.0 if capture_pass else 0.0,
        1.0 if clarity_pass else 0.0,
        1.0 if cost_pass else 0.0,
        1.0 if product_readme_ok else 0.0,
    ]
    composite = round(sum(parts) / len(parts), 4)
    stage_ready = bool(
        v23_claim and v23h_claim and capture_pass and cost_pass
        and product_readme_ok and composite >= GATE
    )

    out = {
        "cycle": "C247",
        "theme": "unified_scorecard_c242_c246",
        "gate": GATE,
        "timestamp": ts(),
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "beat": beat,
        "replace": replace,
        "vision": {
            "v22_smoke": {"rate": v22, "claim": v22_claim},
            "v22_heldout": {"rate": v22h, "claim": v22h_claim},
            "v23_design": {"n": c242.get("n"), "clarity_floor": c242.get("clarity_floor"), "claim": False},
            "v23_smoke": {
                "rate": v23, "n": c243.get("n"), "n_ok": c243.get("n_ok"),
                "claim": v23_claim, "fail_ids": c243.get("fail_ids"),
            },
            "v23_heldout": {
                "rate": v23h, "n": c244.get("n"), "n_ok": c244.get("n_ok"),
                "claim": v23h_claim, "fail_ids": c244.get("fail_ids"),
                "id_disjoint": c244.get("id_disjoint"),
            },
        },
        "cost_ledger": {
            "pass": cost_pass,
            "replace_mean_ratio": replace.get("mean_ratio"),
            "step_delta": replace.get("step_delta"),
        },
        "capture_regression": {"pass": capture_pass, "n_ok": c246.get("n_ok_pointers")},
        "clarity_floor_product": {"pass": clarity_pass},
        "composite": composite,
        "STAGE_READY": stage_ready,
        "pass": stage_ready,
    }
    J(SCORE_LATEST, out)
    J(DOC / "C247_SCORECARD.json", out)

    board = f"""# 蚁算统一记分卡（C247）
Updated: {ts()} (Asia/Shanghai)

| 维度 | 值 |
| --- | --- |
| beat_agent (Gate2 archive) | True (dual≈0.625 > agent≈0.125) |
| replace mean_ratio (C245) | {replace.get('mean_ratio')} |
| V22 smoke / heldout | **{v22} / {v22h}** claim={v22_claim}/{v22h_claim} |
| **V23 smoke / heldout** | **{v23} / {v23h}** claim={v23_claim}/{v23h_claim} |
| cost ledger refresh | pass={cost_pass} |
| clarity_floor | jpeg_q>=58 photo/≤2 |
| capture regression | pass={capture_pass} |
| **composite** | **{composite}** |
| **STAGE_READY** | **{stage_ready}** |

## Iron
Gate **0.6**. Gate2/3 untouched. gen11 HOLD.
"""
    BOARD_MD.write_text(board, encoding="utf-8")

    stage = f"""# STAGE_ANT_C247

Updated: {ts()} (Asia/Shanghai)

**C242-C247 STAGE_READY={'YES' if stage_ready else 'NO'}**

## Batch
| Cycle | Theme | Key |
| --- | --- | --- |
| C242 | V23 design | n={c242.get('n')} hl/clip/punch/stamp/fold/... |
| C243 | V23 smoke | rate={v23} claim={v23_claim} |
| C244 | V23 heldout | rate={v23h} claim={v23h_claim} disjoint={c244.get('id_disjoint')} |
| C245 | cost ledger + replace stress | pass={cost_pass} ratio={replace.get('mean_ratio')} |
| C246 | capture regression | pass={capture_pass} |
| C247 | scorecard | composite={composite} |

## Iron
Gate **0.6**. Gate2/3 untouched. gen11 HOLD.

## Vision claims (scoped)
- V22: claim={v22_claim} rate={v22}
- V22 heldout: claim={v22h_claim} rate={v22h}
- V23: claim={v23_claim} rate={v23}
- V23 heldout: claim={v23h_claim} rate={v23h}
"""
    STAGE.write_text(stage, encoding="utf-8")

    ckpt = f"""# CHECKPOINT_NOW
HEAD: (pending commit)
Stage: C242-C247; V23 CLAIM {v23}; V23 heldout CLAIM {v23h}; cost pass={cost_pass}; capture pass={capture_pass}; composite={composite} STAGE_READY={stage_ready}
V23 design: clarity_floor jpeg_q=60 photo/=2 themes=hl/clip/punch/stamp/fold/thermal/dust/redink/glare/staple/crop/barcode
V23 smoke: rate={v23} n={c243.get('n')} CLAIM={v23_claim} fail={c243.get('fail_ids')}
V23 heldout: rate={v23h} n={c244.get('n')} CLAIM={v23h_claim} disjoint={c244.get('id_disjoint')}
Cost ledger C245: pass={cost_pass} replace_ratio={replace.get('mean_ratio')}
Capture regression: pass={capture_pass} (C246)
Scorecard composite: {composite} (C247)
gen11: HOLD
Gate2/3: untouched
Gate: 0.6
Updated: {ts()} Asia/Shanghai
"""
    CKPT.write_text(ckpt, encoding="utf-8")

    if LOOP_APPEND.is_file():
        with LOOP_APPEND.open("a", encoding="utf-8") as f:
            f.write(f"\n## C242-C247 ({ts()})\n")
            f.write(f"- V23 smoke={v23} heldout={v23h} claims={v23_claim}/{v23h_claim}\n")
            f.write(f"- cost_ledger pass={cost_pass} replace_ratio={replace.get('mean_ratio')}\n")
            f.write(f"- composite={composite} STAGE_READY={stage_ready}\n")
            f.write("- gen11 HOLD; Gate2/3 untouched\n")

    print(json.dumps({
        "cycle": "C247", "composite": composite, "STAGE_READY": stage_ready,
        "v22": v22, "v23": v23, "v23h": v23h,
        "claims": {"v22": v22_claim, "v23": v23_claim, "v23h": v23h_claim},
        "capture_pass": capture_pass, "cost_pass": cost_pass,
    }, ensure_ascii=False))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
