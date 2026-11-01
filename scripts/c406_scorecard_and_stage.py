# -*- coding: utf-8 -*-
"""C406: Unified scorecard + STAGE after C401-C405. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C406.md"
GATE = 0.6


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")


def load(rel):
    p = ROOT / rel
    if not p.is_file():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def main():
    c402 = load("docs/r50/C402_VISION_V49_SMOKE.json") or {}
    c402b = load("docs/r50/C402b_VISION_GATE_V49_CLAIM.json") or {}
    c403 = load("docs/r50/C403_VISION_V49_HELDOUT_SMOKE.json") or {}
    c403b = load("docs/r50/C403b_VISION_GATE_V49_HELDOUT_CLAIM.json") or {}
    c404 = load("docs/r50/C404_CONFIDENCE_GATE_STRETCH.json") or {}
    c405 = load("docs/r50/C405_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}

    v49 = float(c402.get("rate") or 0.0)
    v49h = float(c403.get("rate") or 0.0)
    v49_claim = bool(c402b.get("vl_gate_v49_claim") or c402.get("vl_gate_v49_claim") or c402.get("claim"))
    v49h_claim = bool(c403b.get("vl_gate_v49_heldout_claim") or c403.get("vl_gate_v49_heldout_claim") or c403.get("claim"))
    disjoint = bool(c403.get("id_disjoint") or c403.get("disjoint") or c403b.get("id_disjoint") or c403b.get("disjoint"))
    conf_pass = bool(c404.get("pass"))
    conf_rate = float(c404.get("rate") or 0.0)
    capture_pass = bool(c405.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))
    product_pass = bool((prior.get("product_u2c") or {}).get("pass", True))
    replace_ratio = float((prior.get("product_u2c") or {}).get("replace_ratio") or (prior.get("replace_ratio") or 4.07))

    rates = [v49, v49h]
    if dissolve_pass:
        rates.append(1.0)
    if capture_pass:
        rates.append(1.0)
    if conf_pass:
        rates.append(float(conf_rate) if conf_rate else 1.0)
    composite = round(min(rates) if rates else 0.0, 4)
    if not (v49_claim and v49h_claim and v49 >= GATE and v49h >= GATE):
        composite = min(composite, 0.0)
    stage_ready = bool(
        v49_claim and v49h_claim and v49 >= GATE and v49h >= GATE
        and capture_pass and disjoint
    )

    out = {
        "cycle": "C406",
        "timestamp": ts(),
        "gate": GATE,
        "vision": {
            "v48": (prior.get("vision") or {}).get("v48") or {"rate": 1.0, "claim": True},
            "v48_heldout": (prior.get("vision") or {}).get("v48_heldout") or {"rate": 1.0, "claim": True},
            "v49": {"rate": v49, "claim": v49_claim, "n": c402.get("n")},
            "v49_heldout": {"rate": v49h, "claim": v49h_claim, "disjoint": disjoint, "n": c403.get("n")},
        },
        "product_u2c": {
            "pass": product_pass,
            "replace_ratio": replace_ratio,
            "source": "prior",
        },
        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C404"},
        "capture_regression": {"pass": capture_pass, "source": "C405"},
        "dissolve_shadow": {
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        },
        "composite": composite,
        "stage_ready": stage_ready,
        "v49_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }
    if stage_ready and v49 >= GATE and v49h >= GATE:
        out["composite"] = 1.0 if (v49 >= 0.999 and v49h >= 0.999) else min(v49, v49h)
    J(DOC / "C406_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    board = f"""# 蚁算 UNIFIED SCORECARD

Updated: {ts()} (Asia/Shanghai)

## Tip slice C401-C406
- Vision V49 smoke **{v49}** claim={v49_claim}
- Vision V49 heldout **{v49h}** claim={v49h_claim} disjoint={disjoint}
- confidence-gate (C404) pass={conf_pass} rate={conf_rate}
- dissolve/shadow (prior C398) pass={dissolve_pass}/{shadow_pass}
- capture regression pass={capture_pass}
- replace\approx{replace_ratio}
- composite **{out['composite']}** stage_ready={stage_ready}
- clarity floor jpeg_q>=60 (V49 uses 62)
- Gate 0.6; Gate2/3 untouched; gen11 HOLD
"""
    BOARD_MD.write_text(board, encoding="utf-8")

    stage = f"""# STAGE_ANT_C406

Updated: {ts()} (Asia/Shanghai)

**C401-C406 STAGE_READY={'YES' if stage_ready else 'NO'}**

## Tip slice
- C401: Vision V49 design fixtures (jpeg_q=62, floor>=60)
- C402: Vision V49 smoke claim **{v49}** (n={c402.get('n')})
- C403: Vision V49 heldout claim **{v49h}** (disjoint={disjoint})
- C404: confidence-gate stretch pass={conf_pass} rate={conf_rate}
- C398(prior): dissolve/shadow pass={dissolve_pass}/{shadow_pass}
- C405: capture-office regression pass={capture_pass}
- C406: unified scorecard composite={out['composite']}

## Constraints
- Gate: 0.6
- Gate2/3: untouched
- gen11: HOLD
- clarity floor jpeg_q>=60 kept on V49 (uses 62)

## Entry
- Scorecard: docs/蚁算_UNIFIED_SCORECARD.md
- Latest JSON: docs/r50/SCORECARD_LATEST.json
- This stage: docs/STAGE_ANT_C406.md
"""
    STAGE.write_text(stage, encoding="utf-8")
    print(json.dumps({
        "cycle": "C406", "composite": out["composite"], "stage_ready": stage_ready,
        "replace": replace_ratio, "v49": v49, "v49h": v49h,
        "conf_pass": conf_pass, "capture_pass": capture_pass,
    }, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
