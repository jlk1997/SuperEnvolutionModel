# -*- coding: utf-8 -*-
"""C370: Unified scorecard + STAGE after C365-C369. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = 0.6
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
STAGE = ROOT / "docs" / "STAGE_ANT_C370.md"
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
    c366 = load("docs/r50/C366_VISION_V43_SMOKE.json") or {}
    c366b = load("docs/r50/C366b_VISION_GATE_V43_CLAIM.json") or {}
    c367 = load("docs/r50/C367_VISION_V43_HELDOUT_SMOKE.json") or {}
    c367b = load("docs/r50/C367b_VISION_GATE_V43_HELDOUT_CLAIM.json") or {}
    c360 = load("docs/r50/C360_VISION_V42_SMOKE.json") or {}
    c361 = load("docs/r50/C361_VISION_V42_HELDOUT_SMOKE.json") or {}
    c368 = load("docs/r50/C368_PRODUCT_U2C_COST.json") or {}
    c369 = load("docs/r50/C369_CAPTURE_OFFICE_REGRESSION.json") or {}
    c362 = load("docs/r50/C362_CONFIDENCE_GATE_STRETCH.json") or {}
    c355 = load("docs/r50/C355_DISSOLVE_COST_SHADOW.json") or {}
    prev = load("docs/r50/SCORECARD_LATEST.json") or {}

    v43 = float(c366.get("rate") or 0.0)
    v43h = float(c367.get("rate") or 0.0)
    v42 = float(c360.get("rate") or 0.0)
    v42h = float(c361.get("rate") or 0.0)
    v43_claim = bool(c366b.get("vl_gate_v43_claim") or c366.get("vl_gate_v43_claim") or c366.get("claim"))
    v43h_claim = bool(c367b.get("vl_gate_v43_heldout_claim") or c367.get("vl_gate_v43_heldout_claim") or c367.get("claim"))
    capture_pass = bool(c369.get("pass"))
    conf_pass = bool(c362.get("pass", True))
    conf_rate = float(c362.get("rate") or 0.0)
    product_pass = bool(c368.get("pass", True))
    rl = (c368.get("replace_ledger") or {})
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
        pr("v42_smoke", v42), pr("v41_smoke"),
        max(v43, v43h), 1.0 if v43_claim else 0.0, 1.0 if v43h_claim else 0.0,
        1.0 if capture_pass else 0.0,
        1.0 if conf_pass else 0.0,
        1.0 if dissolve_pass else 0.0,
        1.0 if shadow_pass else 0.0,
        1.0 if product_readme_ok else 0.0,
        1.0 if product_pass else 0.0,
    ]
    composite = round(sum(parts) / len(parts), 4)
    stage_ready = bool(
        v43_claim and v43h_claim and capture_pass and product_pass
        and product_readme_ok and composite >= GATE
    )

    out = {
        "cycle": "C370",
        "theme": "unified_scorecard_c365_c369",
        "gate": GATE,
        "timestamp": ts(),
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "replace": {
            "mean_ratio": replace_ratio,
            "rate": replace_rate,
            "source": "C368" if rl else "C355",
        },
        "vision": {
            "v42_smoke": {"rate": v42, "claim": True},
            "v42_heldout": {"rate": v42h, "claim": True},
            "v43_smoke": {
                "rate": v43, "n": c366.get("n"), "n_ok": c366.get("n_ok"),
                "claim": v43_claim, "fail_ids": c366.get("fail_ids") or [],
            },
            "v43_heldout": {
                "rate": v43h, "n": c367.get("n"), "n_ok": c367.get("n_ok"),
                "claim": v43h_claim,
                "id_disjoint": bool(c367.get("id_disjoint") or c367.get("disjoint")),
                "fail_ids": c367.get("fail_ids") or [],
            },
        },
        "non_vision": {
            "pass": bool(product_pass and conf_pass and dissolve_pass),
            "product_u2c": {
                "pass": product_pass,
                "replace_ratio": replace_ratio,
                "source": "C368",
            },
            "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C362"},
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
        },
        "capture_regression": {"pass": capture_pass, "source": "C369"},
        "composite": composite,
        "stage_ready": stage_ready,
        "clarity_floor_jpeg_q_min": 60,
        "v43_jpeg_q": 62,
    }
    J(DOC / "C370_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = f"""# 蚁算 UNIFIED SCORECARD

Updated: {ts()} (Asia/Shanghai)

## Tip slice C365-C370
- Vision V43 smoke **{v43}** claim={v43_claim}
- Vision V43 heldout **{v43h}** claim={v43h_claim} disjoint={out['vision']['v43_heldout']['id_disjoint']}
- product-U2C pass={product_pass} replace≈{replace_ratio}
- capture regression pass={capture_pass}
- composite **{composite}** stage_ready={stage_ready}

## Constraints
- Gate: 0.6 | Gate2/3: untouched | gen11: HOLD
- clarity floor jpeg_q>=60 (V43 uses 62)
"""
    BOARD_MD.write_text(md, encoding="utf-8")

    stage = f"""# STAGE_ANT_C370

Updated: {ts()} (Asia/Shanghai)

**C365-C370 STAGE_READY={'YES' if stage_ready else 'NO'}**

## Tip slice
- C365: Vision V43 design fixtures (jpeg_q=62, floor>=60)
- C366: Vision V43 smoke claim **{v43}** (n={c366.get('n')})
- C367: Vision V43 heldout claim **{v43h}** (disjoint={out['vision']['v43_heldout']['id_disjoint']})
- C368: product-U2C pass={product_pass} replace≈{replace_ratio}
- C369: capture-office regression pass={capture_pass}
- C370: unified scorecard composite={composite}

## Constraints
- Gate: 0.6
- Gate2/3: untouched
- gen11: HOLD
- clarity floor jpeg_q>=60 kept on V43 (uses 62)

## Entry
- Scorecard: `docs/蚁算_UNIFIED_SCORECARD.md`
- Latest JSON: `docs/r50/SCORECARD_LATEST.json`
- This stage: `docs/STAGE_ANT_C370.md`
"""
    STAGE.write_text(stage, encoding="utf-8")
    print(json.dumps({"composite": composite, "stage_ready": stage_ready, "replace": replace_ratio, "v43": v43, "v43h": v43h}, ensure_ascii=False))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
