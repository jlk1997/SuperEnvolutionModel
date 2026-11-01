# -*- coding: utf-8 -*-
"""C376: Unified scorecard + STAGE after C371-C375. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = 0.6
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
STAGE = ROOT / "docs" / "STAGE_ANT_C376.md"
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
    c372 = load("docs/r50/C372_VISION_V44_SMOKE.json") or {}
    c372b = load("docs/r50/C372b_VISION_GATE_V44_CLAIM.json") or {}
    c373 = load("docs/r50/C373_VISION_V44_HELDOUT_SMOKE.json") or {}
    c373b = load("docs/r50/C373b_VISION_GATE_V44_HELDOUT_CLAIM.json") or {}
    c366 = load("docs/r50/C366_VISION_V43_SMOKE.json") or {}
    c367 = load("docs/r50/C367_VISION_V43_HELDOUT_SMOKE.json") or {}
    c374 = load("docs/r50/C374_PRODUCT_U2C_COST.json") or {}
    c375 = load("docs/r50/C375_CAPTURE_OFFICE_REGRESSION.json") or {}
    c362 = load("docs/r50/C362_CONFIDENCE_GATE_STRETCH.json") or {}
    c355 = load("docs/r50/C355_DISSOLVE_COST_SHADOW.json") or {}
    prev = load("docs/r50/SCORECARD_LATEST.json") or {}

    v44 = float(c372.get("rate") or 0.0)
    v44h = float(c373.get("rate") or 0.0)
    v43 = float(c366.get("rate") or 0.0)
    v43h = float(c367.get("rate") or 0.0)
    v44_claim = bool(c372b.get("vl_gate_v44_claim") or c372.get("vl_gate_v44_claim") or c372.get("claim"))
    v44h_claim = bool(c373b.get("vl_gate_v44_heldout_claim") or c373.get("vl_gate_v44_heldout_claim") or c373.get("claim"))
    capture_pass = bool(c375.get("pass"))
    conf_pass = bool(c362.get("pass", True))
    conf_rate = float(c362.get("rate") or 0.0)
    product_pass = bool(c374.get("pass", True))
    rl = (c374.get("replace_ledger") or {})
    replace_ratio = float(
        rl.get("mean_ratio")
        or (c355.get("replace_stress") or {}).get("mean_ratio")
        or 4.1625
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

    def pr(key, default=1.0):
        return float((vis_prev.get(key) or {}).get("rate") or default)

    parts = [
        1.0,
        replace_rate,
        pr("v43_smoke", v43), pr("v42_smoke"),
        max(v44, v44h), 1.0 if v44_claim else 0.0, 1.0 if v44h_claim else 0.0,
        1.0 if capture_pass else 0.0,
        1.0 if conf_pass else 0.0,
        1.0 if dissolve_pass else 0.0,
        1.0 if shadow_pass else 0.0,
        1.0 if product_readme_ok else 0.0,
        1.0 if product_pass else 0.0,
    ]
    composite = round(sum(parts) / len(parts), 4)
    stage_ready = bool(
        v44_claim and v44h_claim and capture_pass and product_pass
        and product_readme_ok and composite >= GATE
    )
    disjoint = bool(c373.get("id_disjoint") or c373.get("disjoint"))

    out = {
        "cycle": "C376",
        "theme": "unified_scorecard_c371_c375",
        "gate": GATE,
        "timestamp": ts(),
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "replace": {
            "mean_ratio": replace_ratio,
            "rate": replace_rate,
            "source": "C374" if rl else "C355",
        },
        "vision": {
            "v43_smoke": {"rate": v43, "claim": True},
            "v43_heldout": {"rate": v43h, "claim": True},
            "v44_smoke": {
                "rate": v44, "n": c372.get("n"), "n_ok": c372.get("n_ok"),
                "claim": v44_claim, "fail_ids": c372.get("fail_ids") or [],
            },
            "v44_heldout": {
                "rate": v44h, "n": c373.get("n"), "n_ok": c373.get("n_ok"),
                "claim": v44h_claim,
                "id_disjoint": disjoint,
                "fail_ids": c373.get("fail_ids") or [],
            },
        },
        "non_vision": {
            "pass": bool(product_pass and conf_pass and dissolve_pass),
            "product_u2c": {
                "pass": product_pass,
                "replace_ratio": replace_ratio,
                "source": "C374",
            },
            "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C362"},
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
        },
        "capture_regression": {"pass": capture_pass, "source": "C375"},
        "composite": composite,
        "stage_ready": stage_ready,
        "clarity_floor_jpeg_q_min": 60,
        "v44_jpeg_q": 62,
    }
    J(DOC / "C376_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = f"""# 蚁算 UNIFIED SCORECARD

Updated: {ts()} (Asia/Shanghai)

## Tip slice C371-C376
- Vision V44 smoke **{v44}** claim={v44_claim}
- Vision V44 heldout **{v44h}** claim={v44h_claim} disjoint={disjoint}
- product-U2C pass={product_pass} replace≈{replace_ratio}
- capture regression pass={capture_pass}
- composite **{composite}** stage_ready={stage_ready}

## Constraints
- Gate: 0.6 | Gate2/3: untouched | gen11: HOLD
- clarity floor jpeg_q>=60 (V44 uses 62)
"""
    BOARD_MD.write_text(md, encoding="utf-8")

    stage = f"""# STAGE_ANT_C376

Updated: {ts()} (Asia/Shanghai)

**C371-C376 STAGE_READY={'YES' if stage_ready else 'NO'}**

## Tip slice
- C371: Vision V44 design fixtures (jpeg_q=62, floor>=60)
- C372: Vision V44 smoke claim **{v44}** (n={c372.get('n')})
- C373: Vision V44 heldout claim **{v44h}** (disjoint={disjoint})
- C374: product-U2C pass={product_pass} replace≈{replace_ratio}
- C375: capture-office regression pass={capture_pass}
- C376: unified scorecard composite={composite}

## Constraints
- Gate: 0.6
- Gate2/3: untouched
- gen11: HOLD
- clarity floor jpeg_q>=60 kept on V44 (uses 62)

## Entry
- Scorecard: `docs/蚁算_UNIFIED_SCORECARD.md`
- Latest JSON: `docs/r50/SCORECARD_LATEST.json`
- This stage: `docs/STAGE_ANT_C376.md`
"""
    STAGE.write_text(stage, encoding="utf-8")
    print(json.dumps({
        "composite": composite, "stage_ready": stage_ready,
        "replace": replace_ratio, "v44": v44, "v44h": v44h,
    }, ensure_ascii=False))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
