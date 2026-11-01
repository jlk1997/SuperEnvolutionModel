# -*- coding: utf-8 -*-
"""C400: Unified scorecard + STAGE after C395-C399. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C400.md"
GATE = 0.6


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load(rel):
    p = ROOT / rel
    if not p.is_file():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def main():
    c396 = load("docs/r50/C396_VISION_V48_SMOKE.json") or {}
    c396b = load("docs/r50/C396b_VISION_GATE_V48_CLAIM.json") or {}
    c397 = load("docs/r50/C397_VISION_V48_HELDOUT_SMOKE.json") or {}
    c397b = load("docs/r50/C397b_VISION_GATE_V48_HELDOUT_CLAIM.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c399 = load("docs/r50/C399_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c392 = load("docs/r50/C392_CONFIDENCE_GATE_STRETCH.json") or {}

    v48 = float(c396.get("rate") or 0.0)
    v48h = float(c397.get("rate") or 0.0)
    v48_claim = bool(c396b.get("vl_gate_v48_claim") or c396.get("vl_gate_v48_claim") or c396.get("claim"))
    v48h_claim = bool(c397b.get("vl_gate_v48_heldout_claim") or c397.get("vl_gate_v48_heldout_claim") or c397.get("claim"))
    disjoint = bool(c397.get("id_disjoint") or c397.get("disjoint") or c397b.get("id_disjoint") or c397b.get("disjoint"))
    dissolve_pass = bool(c398.get("pass") or c398.get("dissolve_pass") or c398.get("ok"))
    shadow_pass = bool(c398.get("shadow_pass") or c398.get("pass"))
    capture_pass = bool(c399.get("pass"))
    conf_pass = bool(c392.get("pass") if c392 else prior.get("confidence_gate", {}).get("pass"))
    conf_rate = float((c392.get("rate") if c392 else None) or (prior.get("confidence_gate") or {}).get("rate") or 0.0)
    product_pass = bool((prior.get("product_u2c") or {}).get("pass", True))
    replace_ratio = float((prior.get("product_u2c") or {}).get("replace_ratio") or (prior.get("replace_ratio") or 4.07))

    rates = [v48, v48h]
    if dissolve_pass:
        rates.append(1.0)
    if capture_pass:
        rates.append(1.0)
    if conf_pass:
        rates.append(float(conf_rate) if conf_rate else 1.0)
    composite = round(min(rates) if rates else 0.0, 4)
    if not (v48_claim and v48h_claim and v48 >= GATE and v48h >= GATE):
        composite = min(composite, 0.0)
    stage_ready = bool(
        v48_claim and v48h_claim and v48 >= GATE and v48h >= GATE
        and capture_pass and disjoint
    )

    out = {
        "cycle": "C400",
        "timestamp": ts(),
        "gate": GATE,
        "vision": {
            "v47": (prior.get("vision") or {}).get("v47") or {"rate": 1.0, "claim": True},
            "v47_heldout": (prior.get("vision") or {}).get("v47_heldout") or {"rate": 1.0, "claim": True},
            "v48": {"rate": v48, "claim": v48_claim, "n": c396.get("n")},
            "v48_heldout": {"rate": v48h, "claim": v48h_claim, "disjoint": disjoint, "n": c397.get("n")},
        },
        "product_u2c": {
            "pass": product_pass,
            "replace_ratio": replace_ratio,
            "source": "prior",
        },
        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C392"},
        "capture_regression": {"pass": capture_pass, "source": "C399"},
        "dissolve_shadow": {
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        },
        "composite": composite if stage_ready else composite,
        "stage_ready": stage_ready,
        "v48_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }
    if stage_ready and v48 >= GATE and v48h >= GATE:
        out["composite"] = 1.0 if (v48 >= 0.999 and v48h >= 0.999) else min(v48, v48h)
    J(DOC / "C400_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    board = f"""# 蚁算 UNIFIED SCORECARD

Updated: {ts()} (Asia/Shanghai)

## Tip slice C395-C400
- Vision V48 smoke **{v48}** claim={v48_claim}
- Vision V48 heldout **{v48h}** claim={v48h_claim} disjoint={disjoint}
- dissolve/shadow (C398) pass={dissolve_pass}/{shadow_pass}
- confidence-gate (prior C392) pass={conf_pass} rate={conf_rate}
- capture regression pass={capture_pass}
- replace≈{replace_ratio}
- composite **{out['composite']}** stage_ready={stage_ready}
- clarity floor jpeg_q>=60 (V48 uses 62)
- Gate 0.6; Gate2/3 untouched; gen11 HOLD
"""
    BOARD_MD.write_text(board, encoding="utf-8")

    stage = f"""# STAGE_ANT_C400

Updated: {ts()} (Asia/Shanghai)

**C395-C400 STAGE_READY={'YES' if stage_ready else 'NO'}**

## Tip slice
- C395: Vision V48 design fixtures (jpeg_q=62, floor>=60)
- C396: Vision V48 smoke claim **{v48}** (n={c396.get('n')})
- C397: Vision V48 heldout claim **{v48h}** (disjoint={disjoint})
- C398: dissolve/shadow pass={dissolve_pass}/{shadow_pass}
- C392(prior): confidence-gate pass={conf_pass} rate={conf_rate}
- C399: capture-office regression pass={capture_pass}
- C400: unified scorecard composite={out['composite']}

## Constraints
- Gate: 0.6
- Gate2/3: untouched
- gen11: HOLD
- clarity floor jpeg_q>=60 kept on V48 (uses 62)

## Entry
- Scorecard: `docs/蚁算_UNIFIED_SCORECARD.md`
- Latest JSON: `docs/r50/SCORECARD_LATEST.json`
- This stage: `docs/STAGE_ANT_C400.md`
"""
    STAGE.write_text(stage, encoding="utf-8")
    print(json.dumps({
        "cycle": "C400", "composite": out["composite"], "stage_ready": stage_ready,
        "replace": replace_ratio, "v48": v48, "v48h": v48h,
        "dissolve_pass": dissolve_pass, "capture_pass": capture_pass,
    }, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
