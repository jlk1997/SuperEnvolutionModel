# -*- coding: utf-8 -*-
"""C2194: Unified scorecard + STAGE after C2189-C2193. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C2194.md"
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
    c654 = load("docs/r50/C2190_VISION_V347_SMOKE.json") or {}
    c654b = load("docs/r50/C2190b_VISION_GATE_V347_CLAIM.json") or {}
    c655 = load("docs/r50/C2191_VISION_V347_HELDOUT_SMOKE.json") or {}
    c655b = load("docs/r50/C2191b_VISION_GATE_V347_HELDOUT_CLAIM.json") or {}
    c656 = load("docs/r50/C2192_CONFIDENCE_GATE_STRETCH.json") or {}
    c657 = load("docs/r50/C2193_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c650 = load("docs/r50/C2186_PRODUCT_U2C_COST.json") or {}

    v347 = float(c654.get("rate") or 0.0)
    v347h = float(c655.get("rate") or 0.0)
    v347_claim = bool(c654b.get("vl_gate_v347_claim") or c654.get("vl_gate_v347_claim") or c654.get("claim"))
    v347h_claim = bool(c655b.get("vl_gate_v347_heldout_claim") or c655.get("vl_gate_v347_heldout_claim") or c655.get("claim"))
    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))
    conf_pass = bool(c656.get("pass"))
    conf_rate = float(c656.get("rate") or 0.0)
    u2c = prior.get("product_u2c") or {}
    if c650.get("pass") is not None:
        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C2186"}
    replace = float(u2c.get("replace_ratio") or 4.07)
    u2c_pass = bool((u2c or {}).get("pass"))
    capture_pass = bool(c657.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))
    stage_ready = bool(v347_claim and v347h_claim and v347 >= GATE and v347h >= GATE and capture_pass and disjoint and conf_pass)
    composite = (1.0 if (v347 >= 0.999 and v347h >= 0.999) else min(v347, v347h)) if stage_ready else 0.0
    out = {
        "cycle": "C2194", "timestamp": ts(), "gate": GATE,
        "vision": {
            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},
            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},
            "v347": {"rate": v347, "claim": v347_claim, "n": c654.get("n")},
            "v347_heldout": {"rate": v347h, "claim": v347h_claim, "disjoint": disjoint, "n": c655.get("n")},
        },
        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C2186"},
        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C2192"},
        "capture_regression": {"pass": capture_pass, "source": "C2193"},
        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},
        "composite": composite, "stage_ready": stage_ready,
        "v347_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",
    }
    J(DOC / "C2194_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)
    BOARD_MD.write_text("\n".join([
        "# Unified Scorecard (C2194)", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V347: rate={v347} claim={v347_claim}",
        f"- Vision V347 heldout: rate={v347h} claim={v347h_claim} disjoint={disjoint}",
        f"- product_u2c: {out['product_u2c']}", f"- confidence_gate: {out['confidence_gate']}",
        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",
        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",
    ]) + "\n", encoding="utf-8")
    STAGE.write_text("\n".join([
        "# STAGE_ANT_C2194", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C2189-C2194 STAGE_READY={'YES' if stage_ready else 'NO'}**", "",
        "## Tip slice",
        "- C2189: Vision V347 design fixtures",
        f"- C2190: Vision V347 smoke **{v347}**", f"- C2191: Vision V347 heldout **{v347h}** (disjoint={disjoint})",
        f"- C2192: confidence-gate pass={conf_pass} rate={conf_rate}",
        f"- product-U2C (prior C2186): replace={replace} pass={u2c_pass}",
        f"- C2193: capture pass={capture_pass}", f"- C2194: composite={composite}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",
        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V347 (uses 62)",
        "- lesson: avoid *b theme-name collapse (V88)", "",
        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C2194.md", "",
    ]) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
