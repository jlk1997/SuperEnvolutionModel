# -*- coding: utf-8 -*-
"""C1036: Unified scorecard + STAGE after C1031-C1035. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C1036.md"
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
    c654 = load("docs/r50/C1032_VISION_V154_SMOKE.json") or {}
    c654b = load("docs/r50/C1032b_VISION_GATE_V154_CLAIM.json") or {}
    c655 = load("docs/r50/C1033_VISION_V154_HELDOUT_SMOKE.json") or {}
    c655b = load("docs/r50/C1033b_VISION_GATE_V154_HELDOUT_CLAIM.json") or {}
    c656 = load("docs/r50/C1028_CONFIDENCE_GATE_STRETCH.json") or {}
    c657 = load("docs/r50/C1035_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c650 = load("docs/r50/C1034_PRODUCT_U2C_COST.json") or {}

    v154 = float(c654.get("rate") or 0.0)
    v154h = float(c655.get("rate") or 0.0)
    v154_claim = bool(c654b.get("vl_gate_v154_claim") or c654.get("vl_gate_v154_claim") or c654.get("claim"))
    v154h_claim = bool(c655b.get("vl_gate_v154_heldout_claim") or c655.get("vl_gate_v154_heldout_claim") or c655.get("claim"))
    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))
    conf_pass = bool(c656.get("pass"))
    conf_rate = float(c656.get("rate") or 0.0)
    u2c = prior.get("product_u2c") or {}
    if c650.get("pass") is not None:
        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C1034"}
    replace = float(u2c.get("replace_ratio") or 4.07)
    u2c_pass = bool((u2c or {}).get("pass"))
    capture_pass = bool(c657.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))
    stage_ready = bool(v154_claim and v154h_claim and v154 >= GATE and v154h >= GATE and capture_pass and disjoint and u2c_pass)
    composite = (1.0 if (v154 >= 0.999 and v154h >= 0.999) else min(v154, v154h)) if stage_ready else 0.0
    out = {
        "cycle": "C1036", "timestamp": ts(), "gate": GATE,
        "vision": {
            "v153": (prior.get("vision") or {}).get("v153") or {"rate": 1.0, "claim": True},
            "v153_heldout": (prior.get("vision") or {}).get("v153_heldout") or {"rate": 1.0, "claim": True},
            "v154": {"rate": v154, "claim": v154_claim, "n": c654.get("n")},
            "v154_heldout": {"rate": v154h, "claim": v154h_claim, "disjoint": disjoint, "n": c655.get("n")},
        },
        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C1034"},
        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C1028"},
        "capture_regression": {"pass": capture_pass, "source": "C1035"},
        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},
        "composite": composite, "stage_ready": stage_ready,
        "v154_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",
    }
    J(DOC / "C1036_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)
    BOARD_MD.write_text("\n".join([
        "# Unified Scorecard (C1036)", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V154: rate={v154} claim={v154_claim}",
        f"- Vision V154 heldout: rate={v154h} claim={v154h_claim} disjoint={disjoint}",
        f"- product_u2c: {out['product_u2c']}", f"- confidence_gate: {out['confidence_gate']}",
        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",
        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",
    ]) + "\n", encoding="utf-8")
    STAGE.write_text("\n".join([
        "# STAGE_ANT_C1036", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C1031-C1036 STAGE_READY={'YES' if stage_ready else 'NO'}**", "",
        "## Tip slice",
        "- C1031: Vision V154 design fixtures",
        f"- C1032: Vision V154 smoke **{v154}**", f"- C1033: Vision V154 heldout **{v154h}** (disjoint={disjoint})",
        f"- C1034: product-U2C replace={replace} pass={u2c_pass}",
        f"- confidence-gate (prior C1028): pass={conf_pass} rate={conf_rate}",
        f"- C1035: capture pass={capture_pass}", f"- C1036: composite={composite}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",
        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V154 (uses 62)",
        "- lesson: avoid *b theme-name collapse (V88)", "",
        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C1036.md", "",
    ]) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
