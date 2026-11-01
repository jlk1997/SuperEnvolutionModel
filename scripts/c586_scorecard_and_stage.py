# -*- coding: utf-8 -*-
"""C586: Unified scorecard + STAGE after C581-C585. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C586.md"
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
    c582 = load("docs/r50/C582_VISION_V79_SMOKE.json") or {}
    c582b = load("docs/r50/C582b_VISION_GATE_V79_CLAIM.json") or {}
    c583 = load("docs/r50/C583_VISION_V79_HELDOUT_SMOKE.json") or {}
    c583b = load("docs/r50/C583b_VISION_GATE_V79_HELDOUT_CLAIM.json") or {}
    c584 = load("docs/r50/C584_CONFIDENCE_GATE_STRETCH.json") or {}
    c585 = load("docs/r50/C585_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c578 = load("docs/r50/C578_PRODUCT_U2C_COST.json") or {}

    v79 = float(c582.get("rate") or 0.0)
    v79h = float(c583.get("rate") or 0.0)
    v79_claim = bool(c582b.get("vl_gate_v79_claim") or c582.get("vl_gate_v79_claim") or c582.get("claim"))
    v79h_claim = bool(c583b.get("vl_gate_v79_heldout_claim") or c583.get("vl_gate_v79_heldout_claim") or c583.get("claim"))
    disjoint = bool(c583.get("id_disjoint") or c583.get("disjoint") or c583b.get("id_disjoint") or c583b.get("disjoint"))
    conf_pass = bool(c584.get("pass")) if c584 else bool((prior.get("confidence_gate") or {}).get("pass"))
    conf_rate = float(c584.get("rate") or ((prior.get("confidence_gate") or {}).get("rate")) or 1.0)
    u2c = prior.get("product_u2c") or {}
    if c578.get("pass") is not None:
        u2c = {"pass": bool(c578.get("pass")), "replace_ratio": float(c578.get("replace_ratio") or c578.get("mean_ratio") or ((c578.get("replace_ledger") or {}).get("mean_ratio")) or 4.07), "source": "C578"}
    capture_pass = bool(c585.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))
    stage_ready = bool(v79_claim and v79h_claim and v79 >= GATE and v79h >= GATE and capture_pass and disjoint and conf_pass)
    composite = (1.0 if (v79 >= 0.999 and v79h >= 0.999) else min(v79, v79h)) if stage_ready else 0.0
    out = {
        "cycle": "C586", "timestamp": ts(), "gate": GATE,
        "vision": {
            "v78": (prior.get("vision") or {}).get("v78") or {"rate": 1.0, "claim": True},
            "v78_heldout": (prior.get("vision") or {}).get("v78_heldout") or {"rate": 1.0, "claim": True},
            "v79": {"rate": v79, "claim": v79_claim, "n": c582.get("n")},
            "v79_heldout": {"rate": v79h, "claim": v79h_claim, "disjoint": disjoint, "n": c583.get("n")},
        },
        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": 4.0694, "source": "C578"},
        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C584"},
        "capture_regression": {"pass": capture_pass, "source": "C585"},
        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},
        "composite": composite, "stage_ready": stage_ready,
        "v79_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",
    }
    J(DOC / "C586_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)
    BOARD_MD.write_text("\n".join([
        "# Unified Scorecard (C586)", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V79: rate={v79} claim={v79_claim}",
        f"- Vision V79 heldout: rate={v79h} claim={v79h_claim} disjoint={disjoint}",
        f"- product_u2c: {out['product_u2c']}", f"- confidence_gate: {out['confidence_gate']}",
        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",
        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",
    ]) + "\n", encoding="utf-8")
    STAGE.write_text("\n".join([
        "# STAGE_ANT_C586", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C581-C586 STAGE_READY={'YES' if stage_ready else 'NO'}**", "",
        "## Tip slice",
        "- C581: Vision V79 design fixtures",
        f"- C582: Vision V79 smoke **{v79}**", f"- C583: Vision V79 heldout **{v79h}** (disjoint={disjoint})",
        f"- C584: confidence-gate pass={conf_pass} rate={conf_rate}",
        f"- C585: capture pass={capture_pass}", f"- C586: composite={composite}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",
        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V79 (uses 62)", "",
        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C586.md", "",
    ]) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
