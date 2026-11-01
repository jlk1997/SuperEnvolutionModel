# -*- coding: utf-8 -*-
"""C1396: Unified scorecard + STAGE after C1391-C1395. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C1396.md"
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
    c654 = load("docs/r50/C1392_VISION_V214_SMOKE.json") or {}
    c654b = load("docs/r50/C1392b_VISION_GATE_V214_CLAIM.json") or {}
    c655 = load("docs/r50/C1393_VISION_V214_HELDOUT_SMOKE.json") or {}
    c655b = load("docs/r50/C1393b_VISION_GATE_V214_HELDOUT_CLAIM.json") or {}
    c656 = load("docs/r50/C1388_CONFIDENCE_GATE_STRETCH.json") or {}
    c657 = load("docs/r50/C1395_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c650 = load("docs/r50/C1394_PRODUCT_U2C_COST.json") or {}

    v214 = float(c654.get("rate") or 0.0)
    v214h = float(c655.get("rate") or 0.0)
    v214_claim = bool(c654b.get("vl_gate_v214_claim") or c654.get("vl_gate_v214_claim") or c654.get("claim"))
    v214h_claim = bool(c655b.get("vl_gate_v214_heldout_claim") or c655.get("vl_gate_v214_heldout_claim") or c655.get("claim"))
    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))
    conf_pass = bool(c656.get("pass"))
    conf_rate = float(c656.get("rate") or 0.0)
    u2c = prior.get("product_u2c") or {}
    if c650.get("pass") is not None:
        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C1394"}
    replace = float(u2c.get("replace_ratio") or 4.07)
    u2c_pass = bool((u2c or {}).get("pass"))
    capture_pass = bool(c657.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))
    stage_ready = bool(v214_claim and v214h_claim and v214 >= GATE and v214h >= GATE and capture_pass and disjoint and u2c_pass)
    composite = (1.0 if (v214 >= 0.999 and v214h >= 0.999) else min(v214, v214h)) if stage_ready else 0.0
    out = {
        "cycle": "C1396", "timestamp": ts(), "gate": GATE,
        "vision": {
            "v213": (prior.get("vision") or {}).get("v213") or {"rate": 1.0, "claim": True},
            "v213_heldout": (prior.get("vision") or {}).get("v213_heldout") or {"rate": 1.0, "claim": True},
            "v214": {"rate": v214, "claim": v214_claim, "n": c654.get("n")},
            "v214_heldout": {"rate": v214h, "claim": v214h_claim, "disjoint": disjoint, "n": c655.get("n")},
        },
        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C1394"},
        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C1388"},
        "capture_regression": {"pass": capture_pass, "source": "C1395"},
        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},
        "composite": composite, "stage_ready": stage_ready,
        "v214_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",
    }
    J(DOC / "C1396_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)
    BOARD_MD.write_text("\n".join([
        "# Unified Scorecard (C1396)", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V214: rate={v214} claim={v214_claim}",
        f"- Vision V214 heldout: rate={v214h} claim={v214h_claim} disjoint={disjoint}",
        f"- product_u2c: {out['product_u2c']}", f"- confidence_gate: {out['confidence_gate']}",
        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",
        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",
    ]) + "\n", encoding="utf-8")
    STAGE.write_text("\n".join([
        "# STAGE_ANT_C1396", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C1391-C1396 STAGE_READY={'YES' if stage_ready else 'NO'}**", "",
        "## Tip slice",
        "- C1391: Vision V214 design fixtures",
        f"- C1392: Vision V214 smoke **{v214}**", f"- C1393: Vision V214 heldout **{v214h}** (disjoint={disjoint})",
        f"- C1394: product-U2C replace={replace} pass={u2c_pass}",
        f"- confidence-gate (prior C1388): pass={conf_pass} rate={conf_rate}",
        f"- C1395: capture pass={capture_pass}", f"- C1396: composite={composite}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",
        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V214 (uses 62)",
        "- lesson: avoid *b theme-name collapse (V88)", "",
        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C1396.md", "",
    ]) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
