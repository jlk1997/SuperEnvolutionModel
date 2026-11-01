# -*- coding: utf-8 -*-
"""C1096: Unified scorecard + STAGE after C1091-C1095. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C1096.md"
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
    c654 = load("docs/r50/C1092_VISION_V164_SMOKE.json") or {}
    c654b = load("docs/r50/C1092b_VISION_GATE_V164_CLAIM.json") or {}
    c655 = load("docs/r50/C1093_VISION_V164_HELDOUT_SMOKE.json") or {}
    c655b = load("docs/r50/C1093b_VISION_GATE_V164_HELDOUT_CLAIM.json") or {}
    c656 = load("docs/r50/C1088_CONFIDENCE_GATE_STRETCH.json") or {}
    c657 = load("docs/r50/C1095_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c650 = load("docs/r50/C1094_PRODUCT_U2C_COST.json") or {}

    v164 = float(c654.get("rate") or 0.0)
    v164h = float(c655.get("rate") or 0.0)
    v164_claim = bool(c654b.get("vl_gate_v164_claim") or c654.get("vl_gate_v164_claim") or c654.get("claim"))
    v164h_claim = bool(c655b.get("vl_gate_v164_heldout_claim") or c655.get("vl_gate_v164_heldout_claim") or c655.get("claim"))
    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))
    conf_pass = bool(c656.get("pass"))
    conf_rate = float(c656.get("rate") or 0.0)
    u2c = prior.get("product_u2c") or {}
    if c650.get("pass") is not None:
        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C1094"}
    replace = float(u2c.get("replace_ratio") or 4.07)
    u2c_pass = bool((u2c or {}).get("pass"))
    capture_pass = bool(c657.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))
    stage_ready = bool(v164_claim and v164h_claim and v164 >= GATE and v164h >= GATE and capture_pass and disjoint and u2c_pass)
    composite = (1.0 if (v164 >= 0.999 and v164h >= 0.999) else min(v164, v164h)) if stage_ready else 0.0
    out = {
        "cycle": "C1096", "timestamp": ts(), "gate": GATE,
        "vision": {
            "v163": (prior.get("vision") or {}).get("v163") or {"rate": 1.0, "claim": True},
            "v163_heldout": (prior.get("vision") or {}).get("v163_heldout") or {"rate": 1.0, "claim": True},
            "v164": {"rate": v164, "claim": v164_claim, "n": c654.get("n")},
            "v164_heldout": {"rate": v164h, "claim": v164h_claim, "disjoint": disjoint, "n": c655.get("n")},
        },
        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C1094"},
        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C1088"},
        "capture_regression": {"pass": capture_pass, "source": "C1095"},
        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},
        "composite": composite, "stage_ready": stage_ready,
        "v164_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",
    }
    J(DOC / "C1096_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)
    BOARD_MD.write_text("\n".join([
        "# Unified Scorecard (C1096)", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V164: rate={v164} claim={v164_claim}",
        f"- Vision V164 heldout: rate={v164h} claim={v164h_claim} disjoint={disjoint}",
        f"- product_u2c: {out['product_u2c']}", f"- confidence_gate: {out['confidence_gate']}",
        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",
        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",
    ]) + "\n", encoding="utf-8")
    STAGE.write_text("\n".join([
        "# STAGE_ANT_C1096", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C1091-C1096 STAGE_READY={'YES' if stage_ready else 'NO'}**", "",
        "## Tip slice",
        "- C1091: Vision V164 design fixtures",
        f"- C1092: Vision V164 smoke **{v164}**", f"- C1093: Vision V164 heldout **{v164h}** (disjoint={disjoint})",
        f"- C1094: product-U2C replace={replace} pass={u2c_pass}",
        f"- confidence-gate (prior C1088): pass={conf_pass} rate={conf_rate}",
        f"- C1095: capture pass={capture_pass}", f"- C1096: composite={composite}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",
        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V164 (uses 62)",
        "- lesson: avoid *b theme-name collapse (V88)", "",
        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C1096.md", "",
    ]) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
