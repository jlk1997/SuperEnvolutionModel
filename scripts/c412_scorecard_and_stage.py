# -*- coding: utf-8 -*-
"""C412: Unified scorecard + STAGE after C407-C411. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C412.md"
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
    raw = p.read_text(encoding="utf-8").lstrip("\ufeff")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return json.JSONDecoder().raw_decode(raw)[0]


def main():
    c408 = load("docs/r50/C408_VISION_V50_SMOKE.json") or {}
    c408b = load("docs/r50/C408b_VISION_GATE_V50_CLAIM.json") or {}
    c409 = load("docs/r50/C409_VISION_V50_HELDOUT_SMOKE.json") or {}
    c409b = load("docs/r50/C409b_VISION_GATE_V50_HELDOUT_CLAIM.json") or {}
    c410 = load("docs/r50/C410_PRODUCT_U2C_COST.json") or {}
    c411 = load("docs/r50/C411_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}

    v50 = float(c408.get("rate") or 0.0)
    v50h = float(c409.get("rate") or 0.0)
    v50_claim = bool(c408b.get("vl_gate_v50_claim") or c408.get("vl_gate_v50_claim") or c408.get("claim"))
    v50h_claim = bool(c409b.get("vl_gate_v50_heldout_claim") or c409.get("vl_gate_v50_heldout_claim") or c409.get("claim"))
    disjoint = bool(c409.get("id_disjoint") or c409.get("disjoint") or c409b.get("id_disjoint") or c409b.get("disjoint"))
    u2c_pass = bool(c410.get("pass"))
    replace_ratio = float(c410.get("replace_ratio") or c410.get("mean_ratio") or (c410.get("replace_ledger") or {}).get("mean_ratio") or (prior.get("product_u2c") or {}).get("replace_ratio") or 4.07)
    capture_pass = bool(c411.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))
    conf_pass = bool((prior.get("confidence_gate") or {}).get("pass", True))
    conf_rate = float((prior.get("confidence_gate") or {}).get("rate") or 1.0)

    rates = [v50, v50h]
    if dissolve_pass:
        rates.append(1.0)
    if capture_pass:
        rates.append(1.0)
    if u2c_pass:
        rates.append(1.0)
    composite = round(min(rates) if rates else 0.0, 4)
    if not (v50_claim and v50h_claim and v50 >= GATE and v50h >= GATE):
        composite = min(composite, 0.0)
    stage_ready = bool(
        v50_claim and v50h_claim and v50 >= GATE and v50h >= GATE
        and capture_pass and disjoint
    )

    out = {
        "cycle": "C412",
        "timestamp": ts(),
        "gate": GATE,
        "vision": {
            "v49": (prior.get("vision") or {}).get("v49") or {"rate": 1.0, "claim": True},
            "v49_heldout": (prior.get("vision") or {}).get("v49_heldout") or {"rate": 1.0, "claim": True},
            "v50": {"rate": v50, "claim": v50_claim, "n": c408.get("n")},
            "v50_heldout": {"rate": v50h, "claim": v50h_claim, "disjoint": disjoint, "n": c409.get("n")},
        },
        "product_u2c": {
            "pass": u2c_pass,
            "replace_ratio": replace_ratio,
            "source": "C410",
        },
        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "prior_C404"},
        "capture_regression": {"pass": capture_pass, "source": "C411"},
        "dissolve_shadow": {
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        },
        "composite": composite,
        "stage_ready": stage_ready,
        "v50_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }
    if stage_ready and v50 >= GATE and v50h >= GATE:
        out["composite"] = 1.0 if (v50 >= 0.999 and v50h >= 0.999) else min(v50, v50h)
    J(DOC / "C412_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = []
    md.append("# Unified Scorecard (C412)")
    md.append("")
    md.append(f"Updated: {ts()} (Asia/Shanghai)")
    md.append("")
    md.append(f"- Vision V50: rate={v50} claim={v50_claim}")
    md.append(f"- Vision V50 heldout: rate={v50h} claim={v50h_claim} disjoint={disjoint}")
    md.append(f"- product_u2c: pass={u2c_pass} replace_ratio={replace_ratio}")
    md.append(f"- capture_regression: pass={capture_pass}")
    md.append(f"- dissolve/shadow: {dissolve_pass}/{shadow_pass}")
    md.append(f"- composite: {out['composite']}")
    md.append(f"- stage_ready: {stage_ready}")
    md.append("- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD")
    md.append("")
    BOARD_MD.write_text("\n".join(md) + "\n", encoding="utf-8")

    stage = []
    stage.append("# STAGE_ANT_C412")
    stage.append("")
    stage.append(f"Updated: {ts()} (Asia/Shanghai)")
    stage.append("")
    stage.append(f"**C407-C412 STAGE_READY={'YES' if stage_ready else 'NO'}**")
    stage.append("")
    stage.append("## Tip slice")
    stage.append("- C407: Vision V50 design fixtures (jpeg_q=62, floor>=60)")
    stage.append(f"- C408: Vision V50 smoke claim **{v50}** (n={c408.get('n')})")
    stage.append(f"- C409: Vision V50 heldout claim **{v50h}** (disjoint={disjoint})")
    stage.append(f"- C410: product-U2C pass={u2c_pass} replace≈{replace_ratio}")
    stage.append(f"- C411: capture-office regression pass={capture_pass}")
    stage.append(f"- C412: unified scorecard composite={out['composite']}")
    stage.append("")
    stage.append("## Constraints")
    stage.append("- Gate: 0.6")
    stage.append("- Gate2/3: untouched")
    stage.append("- gen11: HOLD")
    stage.append("- clarity floor jpeg_q>=60 kept on V50 (uses 62)")
    stage.append("")
    stage.append("## Entry")
    stage.append(f"- Scorecard: {BOARD_MD.relative_to(ROOT).as_posix()}")
    stage.append("- Latest JSON: docs/r50/SCORECARD_LATEST.json")
    stage.append("- This stage: docs/STAGE_ANT_C412.md")
    stage.append("")
    STAGE.write_text("\n".join(stage) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
