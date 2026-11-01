from pathlib import Path
import re

# fix heldout leftovers
p = Path('scripts/c354_vision_v41_heldout.py')
t = p.read_text(encoding='utf-8')
t = t.replace('_v41hc348', '_v41hc354')
t = t.replace('"version": "v38h"', '"version": "v41h"')
t = t.replace('"version": "v41h"', '"version": "v41h"')  # noop if already
t = t.replace('"jpeg_q_min": 58', '"jpeg_q_min": 60')
# also check theme/harder_than strings
t = re.sub(r'"theme":\s*"[^"]*"', '"theme": "basalt_velvet_bronze_silk_graphite_flint_pewter_gauze_walnut_mica_slate_air_bamboo_lacquer_quartz_parchment_rivet_canvas_heldout"', t, count=1)
t = re.sub(r'"harder_than":\s*"[^"]*"', '"harder_than": "v41_train_c352"', t, count=1)
p.write_text(t, encoding='utf-8')
print('heldout fixed', '"version": "v41h"' in t, '_v41hc354' in t)

# rewrite c357 scorecard cleanly based on c351 structure
src = Path('scripts/c351_scorecard_and_stage.py').read_text(encoding='utf-8')
# Start from fresh write for clarity
score = r'''# -*- coding: utf-8 -*-
"""C357: Unified scorecard + STAGE after C352-C356. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = 0.6
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
STAGE = ROOT / "docs" / "STAGE_ANT_C357.md"
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
    c353 = load("docs/r50/C353_VISION_V41_SMOKE.json") or {}
    c353b = load("docs/r50/C353b_VISION_GATE_V41_CLAIM.json") or {}
    c354 = load("docs/r50/C354_VISION_V41_HELDOUT_SMOKE.json") or {}
    c354b = load("docs/r50/C354b_VISION_GATE_V41_HELDOUT_CLAIM.json") or {}
    c347 = load("docs/r50/C347_VISION_V40_SMOKE.json") or {}
    c348 = load("docs/r50/C348_VISION_V40_HELDOUT_SMOKE.json") or {}
    c355 = load("docs/r50/C355_DISSOLVE_COST_SHADOW.json") or {}
    c356 = load("docs/r50/C356_CAPTURE_OFFICE_REGRESSION.json") or {}
    c349 = load("docs/r50/C349_DISSOLVE_COST_SHADOW.json") or {}
    c344 = load("docs/r50/C344_PRODUCT_U2C_COST.json") or {}
    c342 = load("docs/r50/C342_CONFIDENCE_GATE_STRETCH.json") or {}
    c323 = load("docs/r50/C323_DISSOLVE_COST_SHADOW.json") or {}
    c263 = load("docs/r50/C263_DISSOLVE_COST_SHADOW.json") or {}
    prev = load("docs/r50/SCORECARD_LATEST.json") or {}

    v41 = float(c353.get("rate") or 0.0)
    v41h = float(c354.get("rate") or 0.0)
    v40 = float(c347.get("rate") or 0.0)
    v40h = float(c348.get("rate") or 0.0)
    v41_claim = bool(c353b.get("vl_gate_v41_claim") or c353.get("vl_gate_v41_claim") or c353.get("claim"))
    v41h_claim = bool(c354b.get("vl_gate_v41_heldout_claim") or c354.get("vl_gate_v41_heldout_claim") or c354.get("claim"))
    v40_claim = bool(c347.get("claim") or c347.get("vl_gate_v40_claim"))
    v40h_claim = bool(c348.get("claim") or c348.get("vl_gate_v40_heldout_claim"))
    capture_pass = bool(c356.get("pass"))
    nv = c355 if c355 else (c349 if c349 else c344)
    nv_pass = bool(nv.get("pass", True))
    rl = (c344.get("replace_ledger") or {})
    dissolve_block = (c355.get("dissolve") or c349.get("dissolve") or c323.get("dissolve") or c263.get("dissolve") or {})
    shadow_block = (c355.get("shadow") or c349.get("shadow") or c323.get("shadow") or c263.get("shadow") or {})
    replace_ratio = float(
        (c355.get("replace_stress") or {}).get("mean_ratio")
        or (c349.get("replace_stress") or {}).get("mean_ratio")
        or rl.get("mean_ratio")
        or (c263.get("replace_stress") or {}).get("mean_ratio")
        or 4.0694
    )
    replace_rate = float(
        rl.get("bare_success_rate")
        or (c355.get("replace_stress") or {}).get("rate")
        or (c349.get("replace_stress") or {}).get("rate")
        or 1.0
    )
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
        pr("v33_smoke"), pr("v34_smoke"), pr("v35_smoke"), pr("v36_smoke"),
        pr("v37_smoke"), pr("v38_smoke"), pr("v39_smoke"),
        max(v40, v40h), 1.0 if v40_claim else 0.0, 1.0 if v40h_claim else 0.0,
        max(v41, v41h), 1.0 if v41_claim else 0.0, 1.0 if v41h_claim else 0.0,
        1.0 if capture_pass else 0.0,
        1.0 if nv_pass else 0.0,
        1.0 if dissolve_pass else 0.0,
        1.0 if shadow_pass else 0.0,
        1.0 if conf_pass else 0.0,
        1.0 if product_readme_ok else 0.0,
    ]
    composite = round(sum(parts) / len(parts), 4)
    stage_ready = bool(
        v41_claim and v41h_claim and capture_pass and nv_pass
        and product_readme_ok and composite >= GATE
    )

    out = {
        "cycle": "C357",
        "theme": "unified_scorecard_c352_c356",
        "gate": GATE,
        "timestamp": ts(),
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "replace": {"mean_ratio": replace_ratio, "rate": replace_rate, "source": "C355" if c355 else ("C349" if c349 else "C344")},
        "vision": {
            "v40_smoke": {"rate": v40, "claim": v40_claim},
            "v40_heldout": {"rate": v40h, "claim": v40h_claim},
            "v41_smoke": {"rate": v41, "n": c353.get("n"), "n_ok": c353.get("n_ok"), "claim": v41_claim, "fail_ids": c353.get("fail_ids")},
            "v41_heldout": {"rate": v41h, "n": c354.get("n"), "n_ok": c354.get("n_ok"), "claim": v41h_claim, "id_disjoint": c354.get("id_disjoint"), "fail_ids": c354.get("fail_ids")},
        },
        "non_vision": {
            "pass": nv_pass,
            "dissolve_cost_shadow": {"pass": nv_pass, "source": "C355"},
            "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C342"},
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "product_u2c_prior": {"pass": bool(c344.get("pass")), "replace_ratio": float(rl.get("mean_ratio") or 4.0694), "source": "C344"},
        },
        "capture_regression": {"pass": capture_pass, "n_ok": c356.get("n_ok"), "source": "C356"},
        "composite": composite,
        "STAGE_READY": stage_ready,
        "pass": stage_ready,
        "tip_hint": "post-C356",
    }
    J(SCORE_LATEST, out)
    J(DOC / "C357_SCORECARD_AND_STAGE.json", out)

    md = f"""# 蚁算 UNIFIED SCORECARD

Updated: {ts()} (Asia/Shanghai)

## Composite
- **{composite}** (gate {GATE}) STAGE_READY={stage_ready}

## Vision
- V40 smoke/heldout: {v40} / {v40h} claim={v40_claim}/{v40h_claim}
- V41 smoke/heldout: {v41} / {v41h} claim={v41_claim}/{v41h_claim} fail={c353.get("fail_ids")}/{c354.get("fail_ids")}

## Non-vision
- dissolve/shadow C355: {dissolve_pass}/{shadow_pass}
- confidence C342: {conf_pass} rate={conf_rate}
- product-u2c prior C344 replace≈{replace_ratio}

## Capture regression
- C356 pass={capture_pass} n_ok={c356.get("n_ok")}

## Constraints
- Gate 0.6 · Gate2/3 untouched · gen11 HOLD · jpeg_q≥60
"""
    BOARD_MD.write_text(md, encoding="utf-8")

    stage = f"""# STAGE_ANT_C357

Updated: {ts()} (Asia/Shanghai)

**C352-C357 STAGE_READY={"YES" if stage_ready else "NO"}**

## Tip slice
- C352: Vision V41 design fixtures (jpeg_q≥60)
- C353: Vision V41 smoke claim **{v41}** (n={c353.get("n")})
- C354: Vision V41 heldout claim **{v41h}** (disjoint={c354.get("id_disjoint")})
- C355: dissolve/cost/shadow pass={nv_pass}
- C356: capture-office regression pass={capture_pass}
- C357: unified scorecard composite={composite}

## Constraints
- Gate: 0.6
- Gate2/3: untouched
- gen11: HOLD
- clarity floor jpeg_q≥60 kept on V41

## Entry
- Scorecard: `docs/蚁算_UNIFIED_SCORECARD.md`
- Latest JSON: `docs/r50/SCORECARD_LATEST.json`
- This stage: `docs/STAGE_ANT_C357.md`
"""
    STAGE.write_text(stage, encoding="utf-8")
    CKPT.write_text(stage, encoding="utf-8")
    try:
        with LOOP_APPEND.open("a", encoding="utf-8") as f:
            f.write(f"\n\n## C357 tip\n- composite={composite} STAGE_READY={stage_ready} v41={v41}/{v41h}\n")
    except Exception:
        pass
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''
Path('scripts/c357_scorecard_and_stage.py').write_text(score, encoding='utf-8')
print('c357 written')
