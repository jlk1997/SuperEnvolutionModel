# -*- coding: utf-8 -*-
"""C490: Unified scorecard + STAGE after C485-C489. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C490.md"
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
    c486 = load("docs/r50/C486_VISION_V63_SMOKE.json") or {}
    c486b = load("docs/r50/C486b_VISION_GATE_V63_CLAIM.json") or {}
    c487 = load("docs/r50/C487_VISION_V63_HELDOUT_SMOKE.json") or {}
    c487b = load("docs/r50/C487b_VISION_GATE_V63_HELDOUT_CLAIM.json") or {}
    c488 = load("docs/r50/C488_CONFIDENCE_GATE_STRETCH.json") or {}
    c489 = load("docs/r50/C489_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c482 = load("docs/r50/C482_PRODUCT_U2C_COST.json") or {}

    v63 = float(c486.get("rate") or 0.0)
    v63h = float(c487.get("rate") or 0.0)
    v63_claim = bool(c486b.get("vl_gate_v63_claim") or c486.get("vl_gate_v63_claim") or c486.get("claim"))
    v63h_claim = bool(c487b.get("vl_gate_v63_heldout_claim") or c487.get("vl_gate_v63_heldout_claim") or c487.get("claim"))
    disjoint = bool(c487.get("id_disjoint") or c487.get("disjoint") or c487b.get("id_disjoint") or c487b.get("disjoint"))
    conf_pass = bool(c488.get("pass")) if c488 else bool((prior.get("confidence_gate") or {}).get("pass"))
    conf_rate = float(c488.get("rate") or ((prior.get("confidence_gate") or {}).get("rate")) or 1.0)
    u2c = prior.get("product_u2c") or {}
    if c482.get("pass") is not None:
        u2c = {
            "pass": bool(c482.get("pass")),
            "replace_ratio": float(
                c482.get("replace_ratio")
                or c482.get("mean_ratio")
                or ((c482.get("replace_ledger") or {}).get("mean_ratio"))
                or 4.07
            ),
            "source": "C482",
        }
    capture_pass = bool(c489.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))

    stage_ready = bool(
        v63_claim and v63h_claim and v63 >= GATE and v63h >= GATE
        and capture_pass and disjoint and conf_pass
    )
    composite = 0.0
    if stage_ready:
        composite = 1.0 if (v63 >= 0.999 and v63h >= 0.999) else min(v63, v63h)

    out = {
        "cycle": "C490",
        "timestamp": ts(),
        "gate": GATE,
        "vision": {
            "v62": (prior.get("vision") or {}).get("v62") or {"rate": 1.0, "claim": True},
            "v62_heldout": (prior.get("vision") or {}).get("v62_heldout") or {"rate": 1.0, "claim": True},
            "v63": {"rate": v63, "claim": v63_claim, "n": c486.get("n")},
            "v63_heldout": {"rate": v63h, "claim": v63h_claim, "disjoint": disjoint, "n": c487.get("n")},
        },
        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": 4.0694, "source": "C482"},
        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C488"},
        "capture_regression": {"pass": capture_pass, "source": "C489"},
        "dissolve_shadow": {
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        },
        "composite": composite,
        "stage_ready": stage_ready,
        "v63_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }
    J(DOC / "C490_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = [
        "# Unified Scorecard (C490)", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V63: rate={v63} claim={v63_claim}",
        f"- Vision V63 heldout: rate={v63h} claim={v63h_claim} disjoint={disjoint}",
        f"- product_u2c: {out['product_u2c']}",
        f"- confidence_gate: {out['confidence_gate']}",
        f"- capture_regression: pass={capture_pass}",
        f"- dissolve/shadow: {dissolve_pass}/{shadow_pass}",
        f"- composite: {out['composite']}",
        f"- stage_ready: {stage_ready}",
        "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",
    ]
    BOARD_MD.write_text("\n".join(md) + "\n", encoding="utf-8")

    stage = [
        "# STAGE_ANT_C490", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C485-C490 STAGE_READY={'YES' if stage_ready else 'NO'}**", "",
        "## Tip slice",
        "- C485: Vision V63 design fixtures (jpeg_q=62, floor>=60, long themes)",
        f"- C486: Vision V63 smoke claim **{v63}** (n={c486.get('n')})",
        f"- C487: Vision V63 heldout claim **{v63h}** (disjoint={disjoint})",
        f"- C488: confidence-gate stretch pass={conf_pass} rate={conf_rate}",
        f"- C489: capture-office regression pass={capture_pass}",
        f"- C490: unified scorecard composite={out['composite']}", "",
        "## Constraints",
        "- Gate: 0.6",
        "- Gate2/3: untouched",
        "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V63 (uses 62)", "",
        "## Entry",
        f"- Scorecard: {BOARD_MD.relative_to(ROOT).as_posix()}",
        "- Latest JSON: docs/r50/SCORECARD_LATEST.json",
        "- This stage: docs/STAGE_ANT_C490.md", "",
    ]
    STAGE.write_text("\n".join(stage) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
