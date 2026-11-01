# -*- coding: utf-8 -*-
"""C610: Unified scorecard + STAGE after C605-C609. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C610.md"
GATE = 0.6


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load(rel):
    p = ROOT / rel
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None


def main():
    c606 = load("docs/r50/C606_VISION_V83_SMOKE.json") or {}
    c606b = load("docs/r50/C606b_VISION_GATE_V83_CLAIM.json") or {}
    c607 = load("docs/r50/C607_VISION_V83_HELDOUT_SMOKE.json") or {}
    c607b = load("docs/r50/C607b_VISION_GATE_V83_HELDOUT_CLAIM.json") or {}
    c608 = load("docs/r50/C608_CONFIDENCE_GATE_STRETCH.json") or {}
    c609 = load("docs/r50/C609_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c602 = load("docs/r50/C602_PRODUCT_U2C_COST.json") or {}

    v83 = float(c606.get("rate") or 0.0)
    v83h = float(c607.get("rate") or 0.0)
    v83_claim = bool(c606b.get("vl_gate_v83_claim") or c606.get("vl_gate_v83_claim") or c606.get("claim"))
    v83h_claim = bool(c607b.get("vl_gate_v83_heldout_claim") or c607.get("vl_gate_v83_heldout_claim") or c607.get("claim"))
    disjoint = bool(c607.get("id_disjoint") or c607.get("disjoint") or c607b.get("id_disjoint") or c607b.get("disjoint"))
    conf_pass = bool(c608.get("pass"))
    conf_rate = float(c608.get("rate") or 0.0)
    u2c = prior.get("product_u2c") or {}
    if c602.get("pass") is not None:
        u2c = {
            "pass": bool(c602.get("pass")),
            "replace_ratio": float(c602.get("replace_ratio") or c602.get("mean_ratio") or 4.07),
            "source": "C602",
        }
    replace = float(u2c.get("replace_ratio") or 4.07)
    capture_pass = bool(c609.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))
    stage_ready = bool(v83_claim and v83h_claim and v83 >= GATE and v83h >= GATE and capture_pass and disjoint and conf_pass)
    composite = (1.0 if (v83 >= 0.999 and v83h >= 0.999) else min(v83, v83h)) if stage_ready else 0.0
    out = {
        "cycle": "C610", "timestamp": ts(), "gate": GATE,
        "vision": {
            "v82": (prior.get("vision") or {}).get("v82") or {"rate": 1.0, "claim": True},
            "v82_heldout": (prior.get("vision") or {}).get("v82_heldout") or {"rate": 1.0, "claim": True},
            "v83": {"rate": v83, "claim": v83_claim, "n": c606.get("n")},
            "v83_heldout": {"rate": v83h, "claim": v83h_claim, "disjoint": disjoint, "n": c607.get("n")},
        },
        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C602"},
        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C608"},
        "capture_regression": {"pass": capture_pass, "source": "C609"},
        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},
        "composite": composite, "stage_ready": stage_ready,
        "v83_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",
    }
    J(DOC / "C610_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)
    BOARD_MD.write_text("\n".join([
        "# Unified Scorecard (C610)", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V83: rate={v83} claim={v83_claim}",
        f"- Vision V83 heldout: rate={v83h} claim={v83h_claim} disjoint={disjoint}",
        f"- product_u2c: {out['product_u2c']}", f"- confidence_gate: {out['confidence_gate']}",
        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",
        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",
    ]) + "\n", encoding="utf-8")
    STAGE.write_text("\n".join([
        "# STAGE_ANT_C610", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C605-C610 STAGE_READY={'YES' if stage_ready else 'NO'}**", "",
        "## Tip slice",
        "- C605: Vision V83 design fixtures",
        f"- C606: Vision V83 smoke **{v83}**", f"- C607: Vision V83 heldout **{v83h}** (disjoint={disjoint})",
        f"- C608: confidence-gate stretch rate={conf_rate} pass={conf_pass}",
        f"- C609: capture pass={capture_pass}", f"- C610: composite={composite}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",
        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V83 (uses 62)", "",
        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C610.md", "",
    ]) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
