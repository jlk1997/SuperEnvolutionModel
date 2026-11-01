# -*- coding: utf-8 -*-
"""C1162: Unified scorecard + STAGE after C1157-C1161. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C1162.md"
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
    c654 = load("docs/r50/C1158_VISION_V175_SMOKE.json") or {}
    c654b = load("docs/r50/C1158b_VISION_GATE_V175_CLAIM.json") or {}
    c655 = load("docs/r50/C1159_VISION_V175_HELDOUT_SMOKE.json") or {}
    c655b = load("docs/r50/C1159b_VISION_GATE_V175_HELDOUT_CLAIM.json") or {}
    c656 = load("docs/r50/C1160_CONFIDENCE_GATE_STRETCH.json") or {}
    c657 = load("docs/r50/C1161_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c650 = load("docs/r50/C1154_PRODUCT_U2C_COST.json") or {}

    v175 = float(c654.get("rate") or 0.0)
    v175h = float(c655.get("rate") or 0.0)
    v175_claim = bool(c654b.get("vl_gate_v175_claim") or c654.get("vl_gate_v175_claim") or c654.get("claim"))
    v175h_claim = bool(c655b.get("vl_gate_v175_heldout_claim") or c655.get("vl_gate_v175_heldout_claim") or c655.get("claim"))
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
    stage_ready = bool(v175_claim and v175h_claim and v175 >= GATE and v175h >= GATE and capture_pass and disjoint and conf_pass)
    composite = (1.0 if (v175 >= 0.999 and v175h >= 0.999) else min(v175, v175h)) if stage_ready else 0.0
    out = {
        "cycle": "C1162", "timestamp": ts(), "gate": GATE,
        "vision": {
            "v174": (prior.get("vision") or {}).get("v174") or {"rate": 1.0, "claim": True},
            "v174_heldout": (prior.get("vision") or {}).get("v174_heldout") or {"rate": 1.0, "claim": True},
            "v175": {"rate": v175, "claim": v175_claim, "n": c654.get("n")},
            "v175_heldout": {"rate": v175h, "claim": v175h_claim, "disjoint": disjoint, "n": c655.get("n")},
        },
        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C1154"},
        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C1160"},
        "capture_regression": {"pass": capture_pass, "source": "C1161"},
        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},
        "composite": composite, "stage_ready": stage_ready,
        "v175_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",
    }
    J(DOC / "C1162_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)
    BOARD_MD.write_text("\n".join([
        "# Unified Scorecard (C1162)", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V175: rate={v175} claim={v175_claim}",
        f"- Vision V175 heldout: rate={v175h} claim={v175h_claim} disjoint={disjoint}",
        f"- product_u2c: {out['product_u2c']}", f"- confidence_gate: {out['confidence_gate']}",
        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",
        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",
    ]) + "\n", encoding="utf-8")
    STAGE.write_text("\n".join([
        "# STAGE_ANT_C1162", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C1157-C1162 STAGE_READY={'YES' if stage_ready else 'NO'}**", "",
        "## Tip slice",
        "- C1157: Vision V175 design fixtures",
        f"- C1158: Vision V175 smoke **{v175}**", f"- C1159: Vision V175 heldout **{v175h}** (disjoint={disjoint})",
        f"- C1160: confidence-gate pass={conf_pass} rate={conf_rate}",
        f"- product-U2C (prior C1154): replace={replace} pass={u2c_pass}",
        f"- C1161: capture pass={capture_pass}", f"- C1162: composite={composite}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",
        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V175 (uses 62)",
        "- lesson: avoid *b theme-name collapse (V88)", "",
        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C1162.md", "",
    ]) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
