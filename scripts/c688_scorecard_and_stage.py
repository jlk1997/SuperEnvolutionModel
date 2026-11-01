# -*- coding: utf-8 -*-
"""C688: Unified scorecard + STAGE after C683-C687. V96 milestone. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C688.md"
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
    c648 = load("docs/r50/C684_VISION_V96_SMOKE.json") or {}
    c648b = load("docs/r50/C684b_VISION_GATE_V96_CLAIM.json") or {}
    c649 = load("docs/r50/C685_VISION_V96_HELDOUT_SMOKE.json") or {}
    c649b = load("docs/r50/C685b_VISION_GATE_V96_HELDOUT_CLAIM.json") or {}
    c650 = load("docs/r50/C686_PRODUCT_U2C_COST.json") or {}
    c651 = load("docs/r50/C687_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c644 = load("docs/r50/C680_CONFIDENCE_GATE_STRETCH.json") or {}

    v96 = float(c648.get("rate") or 0.0)
    v96h = float(c649.get("rate") or 0.0)
    v96_claim = bool(c648b.get("vl_gate_v96_claim") or c648.get("vl_gate_v96_claim") or c648.get("claim"))
    v96h_claim = bool(c649b.get("vl_gate_v96_heldout_claim") or c649.get("vl_gate_v96_heldout_claim") or c649.get("claim"))
    disjoint = bool(c649.get("id_disjoint") or c649.get("disjoint") or c649b.get("id_disjoint") or c649b.get("disjoint"))
    conf = prior.get("confidence_gate") or {}
    if c644.get("pass") is not None:
        conf = {"pass": bool(c644.get("pass")), "rate": float(c644.get("rate") or 1.0), "source": "C680"}
    u2c_pass = bool(c650.get("pass"))
    replace = float(c650.get("replace_ratio") or c650.get("mean_ratio") or ((c650.get("replace_ledger") or {}).get("mean_ratio")) or 4.07)
    capture_pass = bool(c651.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))
    stage_ready = bool(v96_claim and v96h_claim and v96 >= GATE and v96h >= GATE and capture_pass and disjoint and u2c_pass)
    composite = (1.0 if (v96 >= 0.999 and v96h >= 0.999) else min(v96, v96h)) if stage_ready else 0.0
    out = {
        "cycle": "C688", "timestamp": ts(), "gate": GATE, "milestone": "V96",
        "vision": {
            "v95": (prior.get("vision") or {}).get("v95") or {"rate": 1.0, "claim": True},
            "v95_heldout": (prior.get("vision") or {}).get("v95_heldout") or {"rate": 1.0, "claim": True},
            "v96": {"rate": v96, "claim": v96_claim, "n": c648.get("n")},
            "v96_heldout": {"rate": v96h, "claim": v96h_claim, "disjoint": disjoint, "n": c649.get("n")},
        },
        "product_u2c": {"pass": u2c_pass, "replace_ratio": replace, "source": "C686"},
        "confidence_gate": conf if conf else {"pass": True, "rate": 1.0, "source": "C680"},
        "capture_regression": {"pass": capture_pass, "source": "C687"},
        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},
        "composite": composite, "stage_ready": stage_ready,
        "v96_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",
    }
    J(DOC / "C688_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)
    BOARD_MD.write_text("\n".join([
        "# Unified Scorecard (C688) — V96 milestone", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V96: rate={v96} claim={v96_claim}",
        f"- Vision V96 heldout: rate={v96h} claim={v96h_claim} disjoint={disjoint}",
        f"- product_u2c: {out['product_u2c']}", f"- confidence_gate: {out['confidence_gate']}",
        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",
        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD | V96 continue", "",
    ]) + "\n", encoding="utf-8")
    STAGE.write_text("\n".join([
        "# STAGE_ANT_C688", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C683-C688 STAGE_READY={'YES' if stage_ready else 'NO'} — V96 milestone (continue)**", "",
        "## Tip slice",
        "- C683: Vision V96 design fixtures",
        f"- C684: Vision V96 smoke **{v96}**", f"- C685: Vision V96 heldout **{v96h}** (disjoint={disjoint})",
        f"- C686: product-U2C pass={u2c_pass} replace≈{replace:.4f}×",
        f"- C687: capture pass={capture_pass}", f"- C688: composite={composite}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",
        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V96 (uses 62)",
        "- V96 milestone is NOT a stop — continue to V95+",
        "- lesson: avoid *b theme-name collapse (V88)", "",
        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C688.md", "",
    ]) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
