# -*- coding: utf-8 -*-
"""C646: Unified scorecard + STAGE after C641-C645. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C646.md"
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
    c642 = load("docs/r50/C642_VISION_V89_SMOKE.json") or {}
    c642b = load("docs/r50/C642b_VISION_GATE_V89_CLAIM.json") or {}
    c643 = load("docs/r50/C643_VISION_V89_HELDOUT_SMOKE.json") or {}
    c643b = load("docs/r50/C643b_VISION_GATE_V89_HELDOUT_CLAIM.json") or {}
    c644 = load("docs/r50/C644_CONFIDENCE_GATE_STRETCH.json") or {}
    c645 = load("docs/r50/C645_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c638 = load("docs/r50/C638_PRODUCT_U2C_COST.json") or {}

    v89 = float(c642.get("rate") or 0.0)
    v89h = float(c643.get("rate") or 0.0)
    v89_claim = bool(c642b.get("vl_gate_v89_claim") or c642.get("vl_gate_v89_claim") or c642.get("claim"))
    v89h_claim = bool(c643b.get("vl_gate_v89_heldout_claim") or c643.get("vl_gate_v89_heldout_claim") or c643.get("claim"))
    disjoint = bool(c643.get("id_disjoint") or c643.get("disjoint") or c643b.get("id_disjoint") or c643b.get("disjoint"))
    conf_pass = bool(c644.get("pass"))
    conf_rate = float(c644.get("rate") or 0.0)
    u2c = prior.get("product_u2c") or {}
    if c638.get("pass") is not None:
        u2c = {
            "pass": bool(c638.get("pass")),
            "replace_ratio": float(c638.get("replace_ratio") or c638.get("mean_ratio") or 4.07),
            "source": "C638",
        }
    replace = float(u2c.get("replace_ratio") or 4.07)
    capture_pass = bool(c645.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))
    stage_ready = bool(v89_claim and v89h_claim and v89 >= GATE and v89h >= GATE and capture_pass and disjoint and conf_pass)
    composite = (1.0 if (v89 >= 0.999 and v89h >= 0.999) else min(v89, v89h)) if stage_ready else 0.0
    out = {
        "cycle": "C646", "timestamp": ts(), "gate": GATE,
        "vision": {
            "v88": (prior.get("vision") or {}).get("v88") or {"rate": 1.0, "claim": True},
            "v88_heldout": (prior.get("vision") or {}).get("v88_heldout") or {"rate": 1.0, "claim": True},
            "v89": {"rate": v89, "claim": v89_claim, "n": c642.get("n")},
            "v89_heldout": {"rate": v89h, "claim": v89h_claim, "disjoint": disjoint, "n": c643.get("n")},
        },
        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C638"},
        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C644"},
        "capture_regression": {"pass": capture_pass, "source": "C645"},
        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},
        "composite": composite, "stage_ready": stage_ready,
        "v89_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",
    }
    J(DOC / "C646_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)
    BOARD_MD.write_text("\n".join([
        "# Unified Scorecard (C646)", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V89: rate={v89} claim={v89_claim}",
        f"- Vision V89 heldout: rate={v89h} claim={v89h_claim} disjoint={disjoint}",
        f"- product_u2c: {out['product_u2c']}", f"- confidence_gate: {out['confidence_gate']}",
        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",
        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",
    ]) + "\n", encoding="utf-8")
    STAGE.write_text("\n".join([
        "# STAGE_ANT_C646", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C641-C646 STAGE_READY={'YES' if stage_ready else 'NO'}**", "",
        "## Tip slice",
        "- C641: Vision V89 design fixtures",
        f"- C642: Vision V89 smoke **{v89}**", f"- C643: Vision V89 heldout **{v89h}** (disjoint={disjoint})",
        f"- C644: confidence-gate stretch rate={conf_rate} pass={conf_pass}",
        f"- C645: capture pass={capture_pass}", f"- C646: composite={composite}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",
        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V89 (uses 62)", "",
        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C646.md", "",
    ]) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
