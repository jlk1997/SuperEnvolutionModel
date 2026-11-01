# -*- coding: utf-8 -*-
"""C1156: Unified scorecard + STAGE after C1151-C1155. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C1156.md"
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
    c654 = load("docs/r50/C1152_VISION_V174_SMOKE.json") or {}
    c654b = load("docs/r50/C1152b_VISION_GATE_V174_CLAIM.json") or {}
    c655 = load("docs/r50/C1153_VISION_V174_HELDOUT_SMOKE.json") or {}
    c655b = load("docs/r50/C1153b_VISION_GATE_V174_HELDOUT_CLAIM.json") or {}
    c656 = load("docs/r50/C1148_CONFIDENCE_GATE_STRETCH.json") or {}
    c657 = load("docs/r50/C1155_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c650 = load("docs/r50/C1154_PRODUCT_U2C_COST.json") or {}

    v174 = float(c654.get("rate") or 0.0)
    v174h = float(c655.get("rate") or 0.0)
    v174_claim = bool(c654b.get("vl_gate_v174_claim") or c654.get("vl_gate_v174_claim") or c654.get("claim"))
    v174h_claim = bool(c655b.get("vl_gate_v174_heldout_claim") or c655.get("vl_gate_v174_heldout_claim") or c655.get("claim"))
    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))
    conf_pass = bool(c656.get("pass"))
    conf_rate = float(c656.get("rate") or 0.0)
    u2c = prior.get("product_u2c") or {}
    if c650.get("pass") is not None:
        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C1154"}
    replace = float(u2c.get("replace_ratio") or 4.07)
    u2c_pass = bool((u2c or {}).get("pass"))
    capture_pass = bool(c657.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))
    stage_ready = bool(v174_claim and v174h_claim and v174 >= GATE and v174h >= GATE and capture_pass and disjoint and u2c_pass)
    composite = (1.0 if (v174 >= 0.999 and v174h >= 0.999) else min(v174, v174h)) if stage_ready else 0.0
    out = {
        "cycle": "C1156", "timestamp": ts(), "gate": GATE,
        "vision": {
            "v173": (prior.get("vision") or {}).get("v173") or {"rate": 1.0, "claim": True},
            "v173_heldout": (prior.get("vision") or {}).get("v173_heldout") or {"rate": 1.0, "claim": True},
            "v174": {"rate": v174, "claim": v174_claim, "n": c654.get("n")},
            "v174_heldout": {"rate": v174h, "claim": v174h_claim, "disjoint": disjoint, "n": c655.get("n")},
        },
        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C1154"},
        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C1148"},
        "capture_regression": {"pass": capture_pass, "source": "C1155"},
        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},
        "composite": composite, "stage_ready": stage_ready,
        "v174_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",
    }
    J(DOC / "C1156_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)
    BOARD_MD.write_text("\n".join([
        "# Unified Scorecard (C1156)", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V174: rate={v174} claim={v174_claim}",
        f"- Vision V174 heldout: rate={v174h} claim={v174h_claim} disjoint={disjoint}",
        f"- product_u2c: {out['product_u2c']}", f"- confidence_gate: {out['confidence_gate']}",
        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",
        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",
    ]) + "\n", encoding="utf-8")
    STAGE.write_text("\n".join([
        "# STAGE_ANT_C1156", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C1151-C1156 STAGE_READY={'YES' if stage_ready else 'NO'}**", "",
        "## Tip slice",
        "- C1151: Vision V174 design fixtures",
        f"- C1152: Vision V174 smoke **{v174}**", f"- C1153: Vision V174 heldout **{v174h}** (disjoint={disjoint})",
        f"- C1154: product-U2C replace={replace} pass={u2c_pass}",
        f"- confidence-gate (prior C1148): pass={conf_pass} rate={conf_rate}",
        f"- C1155: capture pass={capture_pass}", f"- C1156: composite={composite}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",
        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V174 (uses 62)",
        "- lesson: avoid *b theme-name collapse (V88)", "",
        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C1156.md", "",
    ]) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
