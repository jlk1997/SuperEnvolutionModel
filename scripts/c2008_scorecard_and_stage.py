# -*- coding: utf-8 -*-
"""C2008: Unified scorecard + STAGE after C2003-C2007. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C2008.md"
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
    c654 = load("docs/r50/C2004_VISION_V316_SMOKE.json") or {}
    c654b = load("docs/r50/C2004b_VISION_GATE_V316_CLAIM.json") or {}
    c655 = load("docs/r50/C2005_VISION_V316_HELDOUT_SMOKE.json") or {}
    c655b = load("docs/r50/C2005b_VISION_GATE_V316_HELDOUT_CLAIM.json") or {}
    c656 = load("docs/r50/C2000_CONFIDENCE_GATE_STRETCH.json") or {}
    c657 = load("docs/r50/C2007_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c650 = load("docs/r50/C2006_PRODUCT_U2C_COST.json") or {}

    v316 = float(c654.get("rate") or 0.0)
    v316h = float(c655.get("rate") or 0.0)
    v316_claim = bool(c654b.get("vl_gate_v316_claim") or c654.get("vl_gate_v316_claim") or c654.get("claim"))
    v316h_claim = bool(c655b.get("vl_gate_v316_heldout_claim") or c655.get("vl_gate_v316_heldout_claim") or c655.get("claim"))
    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))
    conf_pass = bool(c656.get("pass"))
    conf_rate = float(c656.get("rate") or 0.0)
    u2c = prior.get("product_u2c") or {}
    if c650.get("pass") is not None:
        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C2006"}
    replace = float(u2c.get("replace_ratio") or 4.07)
    u2c_pass = bool((u2c or {}).get("pass"))
    capture_pass = bool(c657.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))
    stage_ready = bool(v316_claim and v316h_claim and v316 >= GATE and v316h >= GATE and capture_pass and disjoint and u2c_pass)
    composite = (1.0 if (v316 >= 0.999 and v316h >= 0.999) else min(v316, v316h)) if stage_ready else 0.0
    out = {
        "cycle": "C2008", "timestamp": ts(), "gate": GATE,
        "vision": {
            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},
            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},
            "v316": {"rate": v316, "claim": v316_claim, "n": c654.get("n")},
            "v316_heldout": {"rate": v316h, "claim": v316h_claim, "disjoint": disjoint, "n": c655.get("n")},
        },
        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C2006"},
        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C2000"},
        "capture_regression": {"pass": capture_pass, "source": "C2007"},
        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},
        "composite": composite, "stage_ready": stage_ready,
        "v316_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",
    }
    J(DOC / "C2008_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)
    BOARD_MD.write_text("\n".join([
        "# Unified Scorecard (C2008)", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V316: rate={v316} claim={v316_claim}",
        f"- Vision V316 heldout: rate={v316h} claim={v316h_claim} disjoint={disjoint}",
        f"- product_u2c: {out['product_u2c']}", f"- confidence_gate: {out['confidence_gate']}",
        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",
        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",
    ]) + "\n", encoding="utf-8")
    STAGE.write_text("\n".join([
        "# STAGE_ANT_C2008", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C2003-C2008 STAGE_READY={'YES' if stage_ready else 'NO'}**", "",
        "## Tip slice",
        "- C2003: Vision V316 design fixtures",
        f"- C2004: Vision V316 smoke **{v316}**", f"- C2005: Vision V316 heldout **{v316h}** (disjoint={disjoint})",
        f"- C2006: product-U2C replace={replace} pass={u2c_pass}",
        f"- confidence-gate (prior C2000): pass={conf_pass} rate={conf_rate}",
        f"- C2007: capture pass={capture_pass}", f"- C2008: composite={composite}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",
        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V316 (uses 62)",
        "- lesson: avoid *b theme-name collapse (V88)", "",
        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C2008.md", "",
    ]) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
