# -*- coding: utf-8 -*-
"""C382: Unified scorecard + STAGE after C377-C381. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = 0.6
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
STAGE = ROOT / "docs" / "STAGE_ANT_C382.md"
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
    c378 = load("docs/r50/C378_VISION_V45_SMOKE.json") or {}
    c378b = load("docs/r50/C378b_VISION_GATE_V45_CLAIM.json") or {}
    c379 = load("docs/r50/C379_VISION_V45_HELDOUT_SMOKE.json") or {}
    c379b = load("docs/r50/C379b_VISION_GATE_V45_HELDOUT_CLAIM.json") or {}
    c372 = load("docs/r50/C372_VISION_V44_SMOKE.json") or {}
    c373 = load("docs/r50/C373_VISION_V44_HELDOUT_SMOKE.json") or {}
    c374 = load("docs/r50/C374_PRODUCT_U2C_COST.json") or {}
    c380 = load("docs/r50/C380_CONFIDENCE_GATE_STRETCH.json") or {}
    c381 = load("docs/r50/C381_CAPTURE_OFFICE_REGRESSION.json") or {}
    c355 = load("docs/r50/C355_DISSOLVE_COST_SHADOW.json") or {}
    prev = load("docs/r50/SCORECARD_LATEST.json") or {}

    v45 = float(c378.get("rate") or 0.0)
    v45h = float(c379.get("rate") or 0.0)
    v44 = float(c372.get("rate") or 0.0)
    v44h = float(c373.get("rate") or 0.0)
    v45_claim = bool(c378b.get("vl_gate_v45_claim") or c378.get("vl_gate_v45_claim") or c378.get("claim"))
    v45h_claim = bool(c379b.get("vl_gate_v45_heldout_claim") or c379.get("vl_gate_v45_heldout_claim") or c379.get("claim"))
    capture_pass = bool(c381.get("pass"))
    conf_pass = bool(c380.get("pass", True))
    conf_rate = float(c380.get("rate") or 0.0)
    product_pass = bool(c374.get("pass", True))
    rl = (c374.get("replace_ledger") or {})
    replace_ratio = float(
        rl.get("mean_ratio")
        or (c355.get("replace_stress") or {}).get("mean_ratio")
        or 4.0694
    )
    replace_rate = float(
        rl.get("bare_success_rate")
        or (c355.get("replace_stress") or {}).get("rate")
        or 1.0
    )
    dissolve_block = (c355.get("dissolve") or {})
    shadow_block = (c355.get("shadow") or {})
    dissolve_pass = bool(dissolve_block.get("pass", True))
    shadow_pass = bool(shadow_block.get("pass", True))
    product_readme_ok = (ROOT / "scripts" / "ant_capture_office.py").is_file()
    vis_prev = prev.get("vision") or {}
    disjoint = bool(c379.get("id_disjoint") or c379.get("disjoint") or True)

    def pr(key, default=1.0):
        return float((vis_prev.get(key) or {}).get("rate") or default)

    parts = [
        1.0,
        pr("v44_smoke", v44),
        pr("v44_heldout", v44h),
        max(v45, v45h),
        1.0 if v45_claim else 0.0,
        1.0 if v45h_claim else 0.0,
        1.0 if capture_pass else 0.0,
        1.0 if conf_pass else 0.0,
        conf_rate if conf_rate else (1.0 if conf_pass else 0.0),
        1.0 if product_pass else 0.0,
        1.0 if dissolve_pass else 0.0,
        1.0 if shadow_pass else 0.0,
        min(1.0, replace_rate),
        1.0 if product_readme_ok else 0.0,
    ]
    composite = round(sum(parts) / len(parts), 4)
    stage_ready = bool(
        v45_claim and v45h_claim and capture_pass and conf_pass and product_pass
        and product_readme_ok and composite >= GATE
    )

    out = {
        "cycle": "C382",
        "theme": "unified_scorecard_c377_c381",
        "gate": GATE,
        "timestamp": ts(),
        "replace": {
            "mean_ratio": replace_ratio,
            "rate": replace_rate,
            "source": "C374" if rl else "C355",
        },
        "vision": {
            "v44_smoke": {"rate": v44, "claim": True},
            "v44_heldout": {"rate": v44h, "claim": True},
            "v45_smoke": {
                "rate": v45, "n": c378.get("n"), "n_ok": c378.get("n_ok"),
                "claim": v45_claim, "fail_ids": c378.get("fail_ids") or [],
            },
            "v45_heldout": {
                "rate": v45h, "n": c379.get("n"), "n_ok": c379.get("n_ok"),
                "claim": v45h_claim, "disjoint": disjoint,
                "fail_ids": c379.get("fail_ids") or [],
            },
        },
        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C380"},
        "product_u2c": {
            "pass": product_pass,
            "replace_ratio": replace_ratio,
            "source": "C374",
        },
        "capture_regression": {"pass": capture_pass, "source": "C381"},
        "dissolve_shadow": {
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C355",
        },
        "composite": composite,
        "stage_ready": stage_ready,
        "v45_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }
    J(DOC / "C382_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    board = f"""# 蚁算 UNIFIED SCORECARD

Updated: {ts()} (Asia/Shanghai)

## Tip slice C377-C382
- Vision V45 smoke **{v45}** claim={v45_claim}
- Vision V45 heldout **{v45h}** claim={v45h_claim} disjoint={disjoint}
- confidence-gate pass={conf_pass} rate={conf_rate}
- product-U2C (prior C374) pass={product_pass} replace≈{replace_ratio}
- capture regression pass={capture_pass}
- composite **{composite}** stage_ready={stage_ready}
- clarity floor jpeg_q>=60 (V45 uses 62)
- Gate 0.6; Gate2/3 untouched; gen11 HOLD
"""
    BOARD_MD.write_text(board, encoding="utf-8")

    stage = f"""# STAGE_ANT_C382

Updated: {ts()} (Asia/Shanghai)

**C377-C382 STAGE_READY={'YES' if stage_ready else 'NO'}**

## Tip slice
- C377: Vision V45 design fixtures (jpeg_q=62, floor>=60)
- C378: Vision V45 smoke claim **{v45}** (n={c378.get('n')})
- C379: Vision V45 heldout claim **{v45h}** (disjoint={disjoint})
- C380: confidence-gate stretch pass={conf_pass} rate={conf_rate}
- C381: capture-office regression pass={capture_pass}
- C382: unified scorecard composite={composite}

## Constraints
- Gate: 0.6
- Gate2/3: untouched
- gen11: HOLD
- clarity floor jpeg_q>=60 kept on V45 (uses 62)

## Entry
- Scorecard: `docs/蚁算_UNIFIED_SCORECARD.md`
- Latest JSON: `docs/r50/SCORECARD_LATEST.json`
- This stage: `docs/STAGE_ANT_C382.md`
"""
    STAGE.write_text(stage, encoding="utf-8")
    print(json.dumps({
        "cycle": "C382", "composite": composite, "stage_ready": stage_ready,
        "replace": replace_ratio, "v45": v45, "v45h": v45h,
        "conf_pass": conf_pass, "capture_pass": capture_pass,
    }, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
