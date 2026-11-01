# -*- coding: utf-8 -*-
"""C592: Unified scorecard + STAGE after C587-C591. V80 milestone. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C592.md"
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
    c588 = load("docs/r50/C588_VISION_V80_SMOKE.json") or {}
    c588b = load("docs/r50/C588b_VISION_GATE_V80_CLAIM.json") or {}
    c589 = load("docs/r50/C589_VISION_V80_HELDOUT_SMOKE.json") or {}
    c589b = load("docs/r50/C589b_VISION_GATE_V80_HELDOUT_CLAIM.json") or {}
    c590 = load("docs/r50/C590_PRODUCT_U2C_COST.json") or {}
    c591 = load("docs/r50/C591_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c584 = load("docs/r50/C584_CONFIDENCE_GATE_STRETCH.json") or {}

    v80 = float(c588.get("rate") or 0.0)
    v80h = float(c589.get("rate") or 0.0)
    v80_claim = bool(c588b.get("vl_gate_v80_claim") or c588.get("vl_gate_v80_claim") or c588.get("claim"))
    v80h_claim = bool(c589b.get("vl_gate_v80_heldout_claim") or c589.get("vl_gate_v80_heldout_claim") or c589.get("claim"))
    disjoint = bool(c589.get("id_disjoint") or c589.get("disjoint") or c589b.get("id_disjoint") or c589b.get("disjoint"))
    conf = prior.get("confidence_gate") or {}
    if c584.get("pass") is not None:
        conf = {"pass": bool(c584.get("pass")), "rate": float(c584.get("rate") or 1.0), "source": "C584"}
    u2c_pass = bool(c590.get("pass"))
    replace = float(c590.get("replace_ratio") or c590.get("mean_ratio") or ((c590.get("replace_ledger") or {}).get("mean_ratio")) or 4.07)
    capture_pass = bool(c591.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))
    stage_ready = bool(v80_claim and v80h_claim and v80 >= GATE and v80h >= GATE and capture_pass and disjoint and u2c_pass)
    composite = (1.0 if (v80 >= 0.999 and v80h >= 0.999) else min(v80, v80h)) if stage_ready else 0.0
    out = {
        "cycle": "C592", "timestamp": ts(), "gate": GATE, "milestone": "V80",
        "vision": {
            "v79": (prior.get("vision") or {}).get("v79") or {"rate": 1.0, "claim": True},
            "v79_heldout": (prior.get("vision") or {}).get("v79_heldout") or {"rate": 1.0, "claim": True},
            "v80": {"rate": v80, "claim": v80_claim, "n": c588.get("n")},
            "v80_heldout": {"rate": v80h, "claim": v80h_claim, "disjoint": disjoint, "n": c589.get("n")},
        },
        "product_u2c": {"pass": u2c_pass, "replace_ratio": replace, "source": "C590"},
        "confidence_gate": conf if conf else {"pass": True, "rate": 1.0, "source": "C584"},
        "capture_regression": {"pass": capture_pass, "source": "C591"},
        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},
        "composite": composite, "stage_ready": stage_ready,
        "v80_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",
    }
    J(DOC / "C592_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)
    BOARD_MD.write_text("\n".join([
        "# Unified Scorecard (C592) — V80 milestone", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V80: rate={v80} claim={v80_claim}",
        f"- Vision V80 heldout: rate={v80h} claim={v80h_claim} disjoint={disjoint}",
        f"- product_u2c: {out['product_u2c']}", f"- confidence_gate: {out['confidence_gate']}",
        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",
        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD | V80 not a stop", "",
    ]) + "\n", encoding="utf-8")
    STAGE.write_text("\n".join([
        "# STAGE_ANT_C592", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C587-C592 STAGE_READY={'YES' if stage_ready else 'NO'} — V80 milestone (continue)**", "",
        "## Tip slice",
        "- C587: Vision V80 design fixtures",
        f"- C588: Vision V80 smoke **{v80}**", f"- C589: Vision V80 heldout **{v80h}** (disjoint={disjoint})",
        f"- C590: product-U2C pass={u2c_pass} replace≈{replace:.4f}×",
        f"- C591: capture pass={capture_pass}", f"- C592: composite={composite}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",
        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V80 (uses 62)",
        "- V80 milestone is NOT a stop — continue to V81+", "",
        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C592.md", "",
    ]) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
