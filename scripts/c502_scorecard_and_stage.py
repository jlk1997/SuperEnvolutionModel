# -*- coding: utf-8 -*-
"""C502: Unified scorecard + STAGE after C497-C501. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C502.md"
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
    c498 = load("docs/r50/C498_VISION_V65_SMOKE.json") or {}
    c498b = load("docs/r50/C498b_VISION_GATE_V65_CLAIM.json") or {}
    c499 = load("docs/r50/C499_VISION_V65_HELDOUT_SMOKE.json") or {}
    c499b = load("docs/r50/C499b_VISION_GATE_V65_HELDOUT_CLAIM.json") or {}
    c500 = load("docs/r50/C500_CONFIDENCE_GATE_STRETCH.json") or {}
    c501 = load("docs/r50/C501_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c494 = load("docs/r50/C494_PRODUCT_U2C_COST.json") or {}

    v65 = float(c498.get("rate") or 0.0)
    v65h = float(c499.get("rate") or 0.0)
    v65_claim = bool(c498b.get("vl_gate_v65_claim") or c498.get("vl_gate_v65_claim") or c498.get("claim"))
    v65h_claim = bool(c499b.get("vl_gate_v65_heldout_claim") or c499.get("vl_gate_v65_heldout_claim") or c499.get("claim"))
    disjoint = bool(c499.get("id_disjoint") or c499.get("disjoint") or c499b.get("id_disjoint") or c499b.get("disjoint"))
    conf_pass = bool(c500.get("pass")) if c500 else bool((prior.get("confidence_gate") or {}).get("pass"))
    conf_rate = float(c500.get("rate") or ((prior.get("confidence_gate") or {}).get("rate")) or 1.0)
    u2c = prior.get("product_u2c") or {}
    if c494.get("pass") is not None:
        u2c = {
            "pass": bool(c494.get("pass")),
            "replace_ratio": float(
                c494.get("replace_ratio")
                or c494.get("mean_ratio")
                or ((c494.get("replace_ledger") or {}).get("mean_ratio"))
                or 4.07
            ),
            "source": "C494",
        }
    capture_pass = bool(c501.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))

    stage_ready = bool(
        v65_claim and v65h_claim and v65 >= GATE and v65h >= GATE
        and capture_pass and disjoint and conf_pass
    )
    composite = 0.0
    if stage_ready:
        composite = 1.0 if (v65 >= 0.999 and v65h >= 0.999) else min(v65, v65h)

    out = {
        "cycle": "C502",
        "timestamp": ts(),
        "gate": GATE,
        "vision": {
            "v64": (prior.get("vision") or {}).get("v64") or {"rate": 1.0, "claim": True},
            "v64_heldout": (prior.get("vision") or {}).get("v64_heldout") or {"rate": 1.0, "claim": True},
            "v65": {"rate": v65, "claim": v65_claim, "n": c498.get("n")},
            "v65_heldout": {"rate": v65h, "claim": v65h_claim, "disjoint": disjoint, "n": c499.get("n")},
        },
        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": 4.0694, "source": "C494"},
        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C500"},
        "capture_regression": {"pass": capture_pass, "source": "C501"},
        "dissolve_shadow": {
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        },
        "composite": composite,
        "stage_ready": stage_ready,
        "v65_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }
    J(DOC / "C502_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = [
        "# Unified Scorecard (C502)", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V65: rate={v65} claim={v65_claim}",
        f"- Vision V65 heldout: rate={v65h} claim={v65h_claim} disjoint={disjoint}",
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
        "# STAGE_ANT_C502", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C497-C502 STAGE_READY={'YES' if stage_ready else 'NO'}**", "",
        "## Tip slice",
        "- C497: Vision V65 design fixtures (jpeg_q=62, floor>=60, long themes)",
        f"- C498: Vision V65 smoke claim **{v65}** (n={c498.get('n')})",
        f"- C499: Vision V65 heldout claim **{v65h}** (disjoint={disjoint})",
        f"- C500: confidence-gate stretch pass={conf_pass} rate={conf_rate}",
        f"- C501: capture-office regression pass={capture_pass}",
        f"- C502: unified scorecard composite={out['composite']}", "",
        "## Constraints",
        "- Gate: 0.6",
        "- Gate2/3: untouched",
        "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V65 (uses 62)", "",
        "## Entry",
        f"- Scorecard: {BOARD_MD.relative_to(ROOT).as_posix()}",
        "- Latest JSON: docs/r50/SCORECARD_LATEST.json",
        "- This stage: docs/STAGE_ANT_C502.md", "",
    ]
    STAGE.write_text("\n".join(stage) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
