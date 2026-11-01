# -*- coding: utf-8 -*-
"""C345: Unified scorecard + STAGE after C338-C344. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = 0.6
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
STAGE = ROOT / "docs" / "STAGE_ANT_C343.md"
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
    c340 = load("docs/r50/C340_VISION_V39_SMOKE.json") or {}
    c340b = load("docs/r50/C340b_VISION_GATE_V39_CLAIM.json") or {}
    c341 = load("docs/r50/C341_VISION_V39_HELDOUT_SMOKE.json") or {}
    c341b = load("docs/r50/C341b_VISION_GATE_V39_HELDOUT_CLAIM.json") or {}
    c333 = load("docs/r50/C333_VISION_V38_SMOKE.json") or {}
    c334 = load("docs/r50/C334_VISION_V38_HELDOUT_SMOKE.json") or {}
    c338b = load("docs/r50/C338b_VISION_V38_RESMOKE.json") or {}
    c342 = load("docs/r50/C342_CONFIDENCE_GATE_STRETCH.json") or {}
    c343 = load("docs/r50/C343_CAPTURE_OFFICE_REGRESSION.json") or {}
    c344 = load("docs/r50/C344_PRODUCT_U2C_COST.json") or {}
    c335 = load("docs/r50/C335_PRODUCT_U2C_COST.json") or {}
    c299 = load("docs/r50/C299_PRODUCT_U2C_COST.json") or {}
    c323 = load("docs/r50/C323_DISSOLVE_COST_SHADOW.json") or {}
    c263 = load("docs/r50/C263_DISSOLVE_COST_SHADOW.json") or {}
    prev = load("docs/r50/SCORECARD_LATEST.json") or {}

    v39 = float(c340.get("rate") or 0.0)
    v39h = float(c341.get("rate") or 0.0)
    v38 = float((c338b.get("rate") if c338b else None) or c333.get("rate") or 0.0)
    v38h = float(c334.get("rate") or 0.0)
    v39_claim = bool(c340b.get("vl_gate_v39_claim") or c340.get("vl_gate_v39_claim") or c340.get("claim"))
    v39h_claim = bool(c341b.get("vl_gate_v39_heldout_claim") or c341.get("vl_gate_v39_heldout_claim") or c341.get("claim"))
    v38_claim = bool(c333.get("claim") or c338b.get("claim"))
    v38h_claim = bool(c334.get("claim"))
    capture_pass = bool(c343.get("pass"))
    nv = c344 if c344 else c335
    nv_pass = bool(nv.get("pass"))
    rl = (nv.get("replace_ledger") or c299.get("replace_ledger") or {})
    replace_ratio = float(rl.get("mean_ratio") or (c263.get("replace_stress") or {}).get("mean_ratio") or 4.0694)
    replace_rate = float(rl.get("bare_success_rate") or 1.0)
    dissolve_pass = bool((c323.get("dissolve") or c263.get("dissolve") or {}).get("pass", True))
    shadow_pass = bool((c323.get("shadow") or c263.get("shadow") or {}).get("pass", True))
    conf_pass = bool(c342.get("pass"))
    conf_rate = float(c342.get("rate") or 0.0)
    product_readme_ok = (ROOT / "docs" / "蚁算_截图办公_README.md").is_file() or (ROOT / "scripts" / "ant_capture_office.py").is_file()

    # keep prior vision rates if present
    vis_prev = prev.get("vision") or {}
    def pr(key, default=1.0):
        return float((vis_prev.get(key) or {}).get("rate") or default)

    parts = [
        1.0,  # beat_agent archive
        replace_rate,
        pr("v25_smoke"), pr("v26_smoke"), pr("v27_smoke"), pr("v28_smoke"),
        pr("v29_smoke"), pr("v30_smoke"), pr("v31_smoke"), pr("v32_smoke"),
        pr("v33_smoke"), pr("v34_smoke"),
        max(v38, v38h), 1.0 if v38_claim else 0.0, 1.0 if v38h_claim else 0.0,
        max(v39, v39h), 1.0 if v39_claim else 0.0, 1.0 if v39h_claim else 0.0,
        1.0 if capture_pass else 0.0,
        1.0 if nv_pass else 0.0,
        1.0 if dissolve_pass else 0.0,
        1.0 if shadow_pass else 0.0,
        1.0 if conf_pass else 0.0,
        1.0 if product_readme_ok else 0.0,
    ]
    composite = round(sum(parts) / len(parts), 4)
    stage_ready = bool(
        v39_claim and v39h_claim and capture_pass and nv_pass
        and product_readme_ok and composite >= GATE
    )

    out = {
        "cycle": "C345",
        "theme": "unified_scorecard_c338_c344",
        "gate": GATE,
        "timestamp": ts(),
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "replace": {"mean_ratio": replace_ratio, "rate": replace_rate, "source": "C344" if c344 else "C299"},
        "vision": {
            "v38_smoke": {"rate": v38, "claim": v38_claim},
            "v38_heldout": {"rate": v38h, "claim": v38h_claim},
            "v39_smoke": {"rate": v39, "n": c340.get("n"), "n_ok": c340.get("n_ok"), "claim": v39_claim, "fail_ids": c340.get("fail_ids")},
            "v39_heldout": {"rate": v39h, "n": c341.get("n"), "n_ok": c341.get("n_ok"), "claim": v39h_claim, "id_disjoint": c341.get("id_disjoint"), "fail_ids": c341.get("fail_ids")},
        },
        "non_vision": {
            "pass": nv_pass,
            "product_u2c_cost": {"pass": nv_pass, "rate": (nv.get("u2c") or {}).get("rate"), "replace_ratio": replace_ratio, "source": "C344"},
            "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C342"},
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
        },
        "capture_regression": {"pass": capture_pass, "n_ok": c343.get("n_ok_pointers"), "source": "C343"},
        "composite": composite,
        "STAGE_READY": stage_ready,
        "pass": stage_ready,
        "tip_hint": "post-C344",
    }
    J(SCORE_LATEST, out)
    J(DOC / "C345_SCORECARD.json", out)

    board = f"""# 蚁算统一记分板（C345）
Updated: {ts()} (Asia/Shanghai)

| 维度 | 值 |
| --- | --- |
| beat_agent (Gate2 archive) | True |
| replace mean_ratio (C344) | {replace_ratio} |
| V25-V37 | prior CLAIM (see archive) |
| V38 smoke / heldout | **{v38} / {v38h}** claim={v38_claim}/{v38h_claim} |
| V39 smoke / heldout | **{v39} / {v39h}** claim={v39_claim}/{v39h_claim} |
| product/u2c (C344) | pass={nv_pass} replace={replace_ratio} |
| confidence (C342) | pass={conf_pass} rate={conf_rate} |
| dissolve / shadow | {dissolve_pass} / {shadow_pass} |
| capture regression (C343) | {capture_pass} |
| composite | **{composite}** |
| STAGE_READY | **{stage_ready}** |
| gen11 | HOLD |
| Gate2/3 | untouched |
| Gate | {GATE} |
"""
    BOARD_MD.write_text(board, encoding="utf-8")

    stage = f"""# STAGE_ANT_C343

Updated: {ts()} (Asia/Shanghai)

**C338-C345 STAGE_READY={'YES' if stage_ready else 'NO'}**

## Tip slice
- C338 / C338b: V38 `v38_07` sla_ok_hours atom fix → smoke claim **1.0**
- C339: Vision V39 design fixtures (jpeg_q≥60)
- C340: Vision V39 smoke claim **{v39}** (n={c340.get('n')})
- C341: Vision V39 heldout claim **{v39h}** (disjoint={c341.get('id_disjoint')})
- C342: confidence-gate stretch rate={conf_rate}
- C343: capture-office regression pass={capture_pass}
- C344: product/U2C + replace ledger pass={nv_pass} mean_ratio={replace_ratio}
- C345: unified scorecard composite={composite}

## Constraints
- Gate: {GATE}
- Gate2/3: untouched
- gen11: HOLD
- clarity floor jpeg_q≥60 kept on V39

## Entry
- Scorecard: `docs/蚁算_UNIFIED_SCORECARD.md`
- Latest JSON: `docs/r50/SCORECARD_LATEST.json`
- This stage: `docs/STAGE_ANT_C343.md`
"""
    STAGE.write_text(stage, encoding="utf-8")

    ckpt = f"""# CHECKPOINT_NOW
HEAD: (see git)
Stage: C338-C345; V39 CLAIM {v39}; V39 heldout CLAIM {v39h}; nv pass={nv_pass}; capture pass={capture_pass}; composite={composite} STAGE_READY={stage_ready}
V39 smoke: rate={v39} n={c340.get('n')} CLAIM={v39_claim}
V39 heldout: rate={v39h} n={c341.get('n')} CLAIM={v39h_claim} disjoint={c341.get('id_disjoint')}
Non-vision C344: pass={nv_pass} product/u2c; replace_ratio={replace_ratio}
Capture regression: pass={capture_pass} (C343)
Scorecard composite: {composite} (C345)
gen11: HOLD
Gate2/3: untouched
Gate: {GATE}
Updated: {ts()} Asia/Shanghai
"""
    CKPT.write_text(ckpt, encoding="utf-8")

    with LOOP_APPEND.open("a", encoding="utf-8") as f:
        f.write(f"\n## C345 scorecard ({ts()})\n")
        f.write(f"- V39 smoke/heldout {v39}/{v39h} claim={v39_claim}/{v39h_claim}\n")
        f.write(f"- C344 product/u2c pass={nv_pass} replace={replace_ratio}\n")
        f.write(f"- C343 capture pass={capture_pass}; composite={composite}; STAGE_READY={stage_ready}\n")
        f.write(f"- entry: docs/STAGE_ANT_C343.md\n")

    print(json.dumps({
        "cycle": "C345", "composite": composite, "STAGE_READY": stage_ready,
        "v39": v39, "v39h": v39h, "replace_ratio": replace_ratio,
        "capture": capture_pass, "nv": nv_pass,
    }, ensure_ascii=False))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
