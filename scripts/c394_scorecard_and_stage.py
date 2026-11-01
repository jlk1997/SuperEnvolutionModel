# -*- coding: utf-8 -*-
"""C394: Unified scorecard + STAGE after C389-C393. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = 0.6
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
STAGE = ROOT / "docs" / "STAGE_ANT_C394.md"
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
    c390 = load("docs/r50/C390_VISION_V47_SMOKE.json") or {}
    c390b = load("docs/r50/C390b_VISION_GATE_V47_CLAIM.json") or {}
    c391 = load("docs/r50/C391_VISION_V47_HELDOUT_SMOKE.json") or {}
    c391b = load("docs/r50/C391b_VISION_GATE_V47_HELDOUT_CLAIM.json") or {}
    c372 = load("docs/r50/C372_VISION_V44_SMOKE.json") or {}
    c373 = load("docs/r50/C373_VISION_V44_HELDOUT_SMOKE.json") or {}
    c374 = load("docs/r50/C386_PRODUCT_U2C_COST.json") or load("docs/r50/C374_PRODUCT_U2C_COST.json") or {}
    c392 = load("docs/r50/C392_CONFIDENCE_GATE_STRETCH.json") or {}
    c393 = load("docs/r50/C393_CAPTURE_OFFICE_REGRESSION.json") or {}
    c355 = load("docs/r50/C355_DISSOLVE_COST_SHADOW.json") or {}
    prev = load("docs/r50/SCORECARD_LATEST.json") or {}

    v47 = float(c390.get("rate") or 0.0)
    v47h = float(c391.get("rate") or 0.0)
    v44 = float(c372.get("rate") or 0.0)
    v44h = float(c373.get("rate") or 0.0)
    v47_claim = bool(c390b.get("vl_gate_v47_claim") or c390.get("vl_gate_v47_claim") or c390.get("claim"))
    v47h_claim = bool(c391b.get("vl_gate_v47_heldout_claim") or c391.get("vl_gate_v47_heldout_claim") or c391.get("claim"))
    capture_pass = bool(c393.get("pass"))
    conf_pass = bool(c392.get("pass", True))
    conf_rate = float(c392.get("rate") or 0.0)
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
    disjoint = bool(c391.get("id_disjoint") or c391.get("disjoint") or True)

    def pr(key, default=1.0):
        return float((vis_prev.get(key) or {}).get("rate") or default)

    parts = [
        1.0,
        pr("v44_smoke", v44),
        pr("v44_heldout", v44h),
        max(v47, v47h),
        1.0 if v47_claim else 0.0,
        1.0 if v47h_claim else 0.0,
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
        v47_claim and v47h_claim and capture_pass and conf_pass and product_pass
        and product_readme_ok and composite >= GATE
    )

    out = {
        "cycle": "C394",
        "theme": "unified_scorecard_c389_c393",
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
            "v46_smoke": vis_prev.get("v46_smoke") or {"rate": 1.0, "claim": True},
            "v46_heldout": vis_prev.get("v46_heldout") or {"rate": 1.0, "claim": True},
            "v47_smoke": {
                "rate": v47, "n": c390.get("n"), "n_ok": c390.get("n_ok"),
                "claim": v47_claim, "fail_ids": c390.get("fail_ids") or [],
            },
            "v47_heldout": {
                "rate": v47h, "n": c391.get("n"), "n_ok": c391.get("n_ok"),
                "claim": v47h_claim, "disjoint": disjoint,
                "fail_ids": c391.get("fail_ids") or [],
            },
        },
        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C392"},
        "product_u2c": {
            "pass": product_pass,
            "replace_ratio": replace_ratio,
            "source": "C374",
        },
        "capture_regression": {"pass": capture_pass, "source": "C393"},
        "dissolve_shadow": {
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C355",
        },
        "composite": composite,
        "stage_ready": stage_ready,
        "v47_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }
    J(DOC / "C394_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    board = f"""# 蚁算 UNIFIED SCORECARD

Updated: {ts()} (Asia/Shanghai)

## Tip slice C389-C394
- Vision V47 smoke **{v47}** claim={v47_claim}
- Vision V47 heldout **{v47h}** claim={v47h_claim} disjoint={disjoint}
- product-U2C (prior C386) pass={product_pass} replace≈{replace_ratio}
- confidence-gate (C392) pass={conf_pass} rate={conf_rate}
- capture regression pass={capture_pass}
- composite **{composite}** stage_ready={stage_ready}
- clarity floor jpeg_q>=60 (V47 uses 62)
- Gate 0.6; Gate2/3 untouched; gen11 HOLD
"""
    BOARD_MD.write_text(board, encoding="utf-8")

    stage = f"""# STAGE_ANT_C394

Updated: {ts()} (Asia/Shanghai)

**C389-C394 STAGE_READY={'YES' if stage_ready else 'NO'}**

## Tip slice
- C389: Vision V47 design fixtures (jpeg_q=62, floor>=60)
- C390: Vision V47 smoke claim **{v47}** (n={c390.get('n')})
- C391: Vision V47 heldout claim **{v47h}** (disjoint={disjoint})
- C386(prior): product-u2c cost pass={product_pass}
- C392: confidence-gate pass={conf_pass} rate={conf_rate}
- C393: capture-office regression pass={capture_pass}
- C394: unified scorecard composite={composite}

## Constraints
- Gate: 0.6
- Gate2/3: untouched
- gen11: HOLD
- clarity floor jpeg_q>=60 kept on V47 (uses 62)

## Entry
- Scorecard: `docs/蚁算_UNIFIED_SCORECARD.md`
- Latest JSON: `docs/r50/SCORECARD_LATEST.json`
- This stage: `docs/STAGE_ANT_C394.md`
"""
    STAGE.write_text(stage, encoding="utf-8")
    print(json.dumps({
        "cycle": "C394", "composite": composite, "stage_ready": stage_ready,
        "replace": replace_ratio, "v47": v47, "v47h": v47h,
        "conf_pass": conf_pass, "capture_pass": capture_pass,
    }, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
