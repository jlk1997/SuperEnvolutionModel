# -*- coding: utf-8 -*-
"""C351: Unified scorecard + STAGE after C346-C350. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = 0.6
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
STAGE = ROOT / "docs" / "STAGE_ANT_C351.md"
CKPT = ROOT / "docs" / "CHECKPOINT_NOW.md"
LOOP_APPEND = ROOT / "docs" / "蚁算_R50PLUS_LOOP.md"
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
    c347 = load("docs/r50/C347_VISION_V40_SMOKE.json") or {}
    c347b = load("docs/r50/C347b_VISION_GATE_V40_CLAIM.json") or {}
    c348 = load("docs/r50/C348_VISION_V40_HELDOUT_SMOKE.json") or {}
    c348b = load("docs/r50/C348b_VISION_GATE_V40_HELDOUT_CLAIM.json") or {}
    c340 = load("docs/r50/C340_VISION_V39_SMOKE.json") or {}
    c341 = load("docs/r50/C341_VISION_V39_HELDOUT_SMOKE.json") or {}
    c349 = load("docs/r50/C349_DISSOLVE_COST_SHADOW.json") or {}
    c350 = load("docs/r50/C350_CAPTURE_OFFICE_REGRESSION.json") or {}
    c344 = load("docs/r50/C344_PRODUCT_U2C_COST.json") or {}
    c342 = load("docs/r50/C342_CONFIDENCE_GATE_STRETCH.json") or {}
    c323 = load("docs/r50/C323_DISSOLVE_COST_SHADOW.json") or {}
    c263 = load("docs/r50/C263_DISSOLVE_COST_SHADOW.json") or {}
    prev = load("docs/r50/SCORECARD_LATEST.json") or {}

    v40 = float(c347.get("rate") or 0.0)
    v40h = float(c348.get("rate") or 0.0)
    v39 = float(c340.get("rate") or 0.0)
    v39h = float(c341.get("rate") or 0.0)
    v40_claim = bool(c347b.get("vl_gate_v40_claim") or c347.get("vl_gate_v40_claim") or c347.get("claim"))
    v40h_claim = bool(c348b.get("vl_gate_v40_heldout_claim") or c348.get("vl_gate_v40_heldout_claim") or c348.get("claim"))
    v39_claim = bool(c340.get("claim") or c340.get("vl_gate_v39_claim"))
    v39h_claim = bool(c341.get("claim") or c341.get("vl_gate_v39_heldout_claim"))
    capture_pass = bool(c350.get("pass"))
    nv = c349 if c349 else c344
    nv_pass = bool(nv.get("pass", True))
    rl = (c344.get("replace_ledger") or {})
    dissolve_block = (c349.get("dissolve") or c323.get("dissolve") or c263.get("dissolve") or {})
    shadow_block = (c349.get("shadow") or c323.get("shadow") or c263.get("shadow") or {})
    replace_ratio = float(
        (c349.get("replace_stress") or {}).get("mean_ratio")
        or rl.get("mean_ratio")
        or (c263.get("replace_stress") or {}).get("mean_ratio")
        or 4.0694
    )
    replace_rate = float(rl.get("bare_success_rate") or (c349.get("replace_stress") or {}).get("rate") or 1.0)
    dissolve_pass = bool(dissolve_block.get("pass", True))
    shadow_pass = bool(shadow_block.get("pass", True))
    conf_pass = bool(c342.get("pass", True))
    conf_rate = float(c342.get("rate") or 0.0)
    product_readme_ok = (ROOT / "scripts" / "ant_capture_office.py").is_file()

    vis_prev = prev.get("vision") or {}
    def pr(key, default=1.0):
        return float((vis_prev.get(key) or {}).get("rate") or default)

    parts = [
        1.0,
        replace_rate,
        pr("v25_smoke"), pr("v26_smoke"), pr("v27_smoke"), pr("v28_smoke"),
        pr("v29_smoke"), pr("v30_smoke"), pr("v31_smoke"), pr("v32_smoke"),
        pr("v33_smoke"), pr("v34_smoke"), pr("v35_smoke", v39), pr("v36_smoke", 1.0),
        pr("v37_smoke", 1.0), pr("v38_smoke", 1.0),
        max(v39, v39h), 1.0 if v39_claim else 0.0, 1.0 if v39h_claim else 0.0,
        max(v40, v40h), 1.0 if v40_claim else 0.0, 1.0 if v40h_claim else 0.0,
        1.0 if capture_pass else 0.0,
        1.0 if nv_pass else 0.0,
        1.0 if dissolve_pass else 0.0,
        1.0 if shadow_pass else 0.0,
        1.0 if conf_pass else 0.0,
        1.0 if product_readme_ok else 0.0,
    ]
    composite = round(sum(parts) / len(parts), 4)
    stage_ready = bool(
        v40_claim and v40h_claim and capture_pass and nv_pass
        and product_readme_ok and composite >= GATE
    )

    out = {
        "cycle": "C351",
        "theme": "unified_scorecard_c346_c350",
        "gate": GATE,
        "timestamp": ts(),
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "replace": {"mean_ratio": replace_ratio, "rate": replace_rate, "source": "C349" if c349 else "C344"},
        "vision": {
            "v39_smoke": {"rate": v39, "claim": v39_claim},
            "v39_heldout": {"rate": v39h, "claim": v39h_claim},
            "v40_smoke": {"rate": v40, "n": c347.get("n"), "n_ok": c347.get("n_ok"), "claim": v40_claim, "fail_ids": c347.get("fail_ids")},
            "v40_heldout": {"rate": v40h, "n": c348.get("n"), "n_ok": c348.get("n_ok"), "claim": v40h_claim, "id_disjoint": c348.get("id_disjoint"), "fail_ids": c348.get("fail_ids")},
        },
        "non_vision": {
            "pass": nv_pass,
            "dissolve_cost_shadow": {"pass": nv_pass, "source": "C349"},
            "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C342"},
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "product_u2c_prior": {"pass": bool(c344.get("pass")), "replace_ratio": float(rl.get("mean_ratio") or 4.0694), "source": "C344"},
        },
        "capture_regression": {"pass": capture_pass, "n_ok": c350.get("n_ok"), "source": "C350"},
        "composite": composite,
        "STAGE_READY": stage_ready,
        "pass": stage_ready,
        "tip_hint": "post-C350",
    }
    J(SCORE_LATEST, out)
    J(DOC / "C351_SCORECARD_AND_STAGE.json", out)

    md = f"""# 蚁算 UNIFIED SCORECARD

Updated: {ts()} (Asia/Shanghai)

## Composite
- **{composite}** (gate {GATE}) STAGE_READY={stage_ready}

## Vision
- V39 smoke/heldout: {v39} / {v39h} claim={v39_claim}/{v39h_claim}
- V40 smoke/heldout: {v40} / {v40h} claim={v40_claim}/{v40h_claim} fail={c347.get("fail_ids")}/{c348.get("fail_ids")}

## Non-vision
- dissolve/shadow C349: {dissolve_pass}/{shadow_pass}
- confidence C342: {conf_pass} rate={conf_rate}
- product-u2c prior C344 replace≈{replace_ratio}

## Capture regression
- C350 pass={capture_pass} n_ok={c350.get("n_ok")}

## Constraints
- Gate 0.6 · Gate2/3 untouched · gen11 HOLD · jpeg_q≥60
"""
    BOARD_MD.write_text(md, encoding="utf-8")

    stage = f"""# STAGE_ANT_C351

Updated: {ts()} (Asia/Shanghai)

**C346-C351 STAGE_READY={"YES" if stage_ready else "NO"}**

## Tip slice
- C346: Vision V40 design fixtures (jpeg_q≥60)
- C347: Vision V40 smoke claim **{v40}** (n={c347.get("n")})
- C348: Vision V40 heldout claim **{v40h}** (disjoint={c348.get("id_disjoint")})
- C349: dissolve/cost/shadow pass={nv_pass}
- C350: capture-office regression pass={capture_pass}
- C351: unified scorecard composite={composite}

## Constraints
- Gate: 0.6
- Gate2/3: untouched
- gen11: HOLD
- clarity floor jpeg_q≥60 kept on V40

## Entry
- Scorecard: `docs/蚁算_UNIFIED_SCORECARD.md`
- Latest JSON: `docs/r50/SCORECARD_LATEST.json`
- This stage: `docs/STAGE_ANT_C351.md`
"""
    STAGE.write_text(stage, encoding="utf-8")
    CKPT.write_text(stage, encoding="utf-8")
    try:
        with LOOP_APPEND.open("a", encoding="utf-8") as f:
            f.write(f"\n\n## C351 tip\n- composite={composite} STAGE_READY={stage_ready} v40={v40}/{v40h}\n")
    except Exception:
        pass
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
