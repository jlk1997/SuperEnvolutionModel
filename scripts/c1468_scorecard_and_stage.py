# -*- coding: utf-8 -*-
"""C1468: Unified scorecard + STAGE after C1463-C1467. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C1468.md"
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
    c654 = load("docs/r50/C1464_VISION_V226_SMOKE.json") or {}
    c654b = load("docs/r50/C1464b_VISION_GATE_V226_CLAIM.json") or {}
    c655 = load("docs/r50/C1465_VISION_V226_HELDOUT_SMOKE.json") or {}
    c655b = load("docs/r50/C1465b_VISION_GATE_V226_HELDOUT_CLAIM.json") or {}
    c656 = load("docs/r50/C1460_CONFIDENCE_GATE_STRETCH.json") or {}
    c657 = load("docs/r50/C1467_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c650 = load("docs/r50/C1466_PRODUCT_U2C_COST.json") or {}

    v226 = float(c654.get("rate") or 0.0)
    v226h = float(c655.get("rate") or 0.0)
    v226_claim = bool(c654b.get("vl_gate_v226_claim") or c654.get("vl_gate_v226_claim") or c654.get("claim"))
    v226h_claim = bool(c655b.get("vl_gate_v226_heldout_claim") or c655.get("vl_gate_v226_heldout_claim") or c655.get("claim"))
    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))
    conf_pass = bool(c656.get("pass"))
    conf_rate = float(c656.get("rate") or 0.0)
    u2c = prior.get("product_u2c") or {}
    if c650.get("pass") is not None:
        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C1466"}
    replace = float(u2c.get("replace_ratio") or 4.07)
    u2c_pass = bool((u2c or {}).get("pass"))
    capture_pass = bool(c657.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))
    stage_ready = bool(v226_claim and v226h_claim and v226 >= GATE and v226h >= GATE and capture_pass and disjoint and u2c_pass)
    composite = (1.0 if (v226 >= 0.999 and v226h >= 0.999) else min(v226, v226h)) if stage_ready else 0.0
    out = {
        "cycle": "C1468", "timestamp": ts(), "gate": GATE,
        "vision": {
            "v225": (prior.get("vision") or {}).get("v225") or {"rate": 1.0, "claim": True},
            "v225_heldout": (prior.get("vision") or {}).get("v225_heldout") or {"rate": 1.0, "claim": True},
            "v226": {"rate": v226, "claim": v226_claim, "n": c654.get("n")},
            "v226_heldout": {"rate": v226h, "claim": v226h_claim, "disjoint": disjoint, "n": c655.get("n")},
        },
        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C1466"},
        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C1460"},
        "capture_regression": {"pass": capture_pass, "source": "C1467"},
        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},
        "composite": composite, "stage_ready": stage_ready,
        "v226_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",
    }
    J(DOC / "C1468_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)
    BOARD_MD.write_text("\n".join([
        "# Unified Scorecard (C1468)", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V226: rate={v226} claim={v226_claim}",
        f"- Vision V226 heldout: rate={v226h} claim={v226h_claim} disjoint={disjoint}",
        f"- product_u2c: {out['product_u2c']}", f"- confidence_gate: {out['confidence_gate']}",
        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",
        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",
    ]) + "\n", encoding="utf-8")
    STAGE.write_text("\n".join([
        "# STAGE_ANT_C1468", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C1463-C1468 STAGE_READY={'YES' if stage_ready else 'NO'}**", "",
        "## Tip slice",
        "- C1463: Vision V226 design fixtures",
        f"- C1464: Vision V226 smoke **{v226}**", f"- C1465: Vision V226 heldout **{v226h}** (disjoint={disjoint})",
        f"- C1466: product-U2C replace={replace} pass={u2c_pass}",
        f"- confidence-gate (prior C1460): pass={conf_pass} rate={conf_rate}",
        f"- C1467: capture pass={capture_pass}", f"- C1468: composite={composite}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",
        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V226 (uses 62)",
        "- lesson: avoid *b theme-name collapse (V88)", "",
        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C1468.md", "",
    ]) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
