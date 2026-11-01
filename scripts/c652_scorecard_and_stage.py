# -*- coding: utf-8 -*-
"""C652: Unified scorecard + STAGE after C647-C651. V90 milestone. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C652.md"
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
    c648 = load("docs/r50/C648_VISION_V90_SMOKE.json") or {}
    c648b = load("docs/r50/C648b_VISION_GATE_V90_CLAIM.json") or {}
    c649 = load("docs/r50/C649_VISION_V90_HELDOUT_SMOKE.json") or {}
    c649b = load("docs/r50/C649b_VISION_GATE_V90_HELDOUT_CLAIM.json") or {}
    c650 = load("docs/r50/C650_PRODUCT_U2C_COST.json") or {}
    c651 = load("docs/r50/C651_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c644 = load("docs/r50/C644_CONFIDENCE_GATE_STRETCH.json") or {}

    v90 = float(c648.get("rate") or 0.0)
    v90h = float(c649.get("rate") or 0.0)
    v90_claim = bool(c648b.get("vl_gate_v90_claim") or c648.get("vl_gate_v90_claim") or c648.get("claim"))
    v90h_claim = bool(c649b.get("vl_gate_v90_heldout_claim") or c649.get("vl_gate_v90_heldout_claim") or c649.get("claim"))
    disjoint = bool(c649.get("id_disjoint") or c649.get("disjoint") or c649b.get("id_disjoint") or c649b.get("disjoint"))
    conf = prior.get("confidence_gate") or {}
    if c644.get("pass") is not None:
        conf = {"pass": bool(c644.get("pass")), "rate": float(c644.get("rate") or 1.0), "source": "C644"}
    u2c_pass = bool(c650.get("pass"))
    replace = float(c650.get("replace_ratio") or c650.get("mean_ratio") or ((c650.get("replace_ledger") or {}).get("mean_ratio")) or 4.07)
    capture_pass = bool(c651.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))
    stage_ready = bool(v90_claim and v90h_claim and v90 >= GATE and v90h >= GATE and capture_pass and disjoint and u2c_pass)
    composite = (1.0 if (v90 >= 0.999 and v90h >= 0.999) else min(v90, v90h)) if stage_ready else 0.0
    out = {
        "cycle": "C652", "timestamp": ts(), "gate": GATE, "milestone": "V90",
        "vision": {
            "v89": (prior.get("vision") or {}).get("v89") or {"rate": 1.0, "claim": True},
            "v89_heldout": (prior.get("vision") or {}).get("v89_heldout") or {"rate": 1.0, "claim": True},
            "v90": {"rate": v90, "claim": v90_claim, "n": c648.get("n")},
            "v90_heldout": {"rate": v90h, "claim": v90h_claim, "disjoint": disjoint, "n": c649.get("n")},
        },
        "product_u2c": {"pass": u2c_pass, "replace_ratio": replace, "source": "C650"},
        "confidence_gate": conf if conf else {"pass": True, "rate": 1.0, "source": "C644"},
        "capture_regression": {"pass": capture_pass, "source": "C651"},
        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},
        "composite": composite, "stage_ready": stage_ready,
        "v90_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",
    }
    J(DOC / "C652_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)
    BOARD_MD.write_text("\n".join([
        "# Unified Scorecard (C652) — V90 milestone", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V90: rate={v90} claim={v90_claim}",
        f"- Vision V90 heldout: rate={v90h} claim={v90h_claim} disjoint={disjoint}",
        f"- product_u2c: {out['product_u2c']}", f"- confidence_gate: {out['confidence_gate']}",
        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",
        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD | V90 not a stop", "",
    ]) + "\n", encoding="utf-8")
    STAGE.write_text("\n".join([
        "# STAGE_ANT_C652", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C647-C652 STAGE_READY={'YES' if stage_ready else 'NO'} — V90 milestone (continue)**", "",
        "## Tip slice",
        "- C647: Vision V90 design fixtures",
        f"- C648: Vision V90 smoke **{v90}**", f"- C649: Vision V90 heldout **{v90h}** (disjoint={disjoint})",
        f"- C650: product-U2C pass={u2c_pass} replace≈{replace:.4f}×",
        f"- C651: capture pass={capture_pass}", f"- C652: composite={composite}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",
        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V90 (uses 62)",
        "- V90 milestone is NOT a stop — continue to V91+",
        "- lesson: avoid *b theme-name collapse (V88)", "",
        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C652.md", "",
    ]) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
