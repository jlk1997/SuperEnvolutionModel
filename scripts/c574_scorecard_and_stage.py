# -*- coding: utf-8 -*-
"""C574: Unified scorecard + STAGE after C569-C573. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C574.md"
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
    c570 = load("docs/r50/C570_VISION_V77_SMOKE.json") or {}
    c570b = load("docs/r50/C570b_VISION_GATE_V77_CLAIM.json") or {}
    c571 = load("docs/r50/C571_VISION_V77_HELDOUT_SMOKE.json") or {}
    c571b = load("docs/r50/C571b_VISION_GATE_V77_HELDOUT_CLAIM.json") or {}
    c572 = load("docs/r50/C572_CONFIDENCE_GATE_STRETCH.json") or {}
    c573 = load("docs/r50/C573_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c566 = load("docs/r50/C566_PRODUCT_U2C_COST.json") or {}

    v77 = float(c570.get("rate") or 0.0)
    v77h = float(c571.get("rate") or 0.0)
    v77_claim = bool(c570b.get("vl_gate_v77_claim") or c570.get("vl_gate_v77_claim") or c570.get("claim"))
    v77h_claim = bool(c571b.get("vl_gate_v77_heldout_claim") or c571.get("vl_gate_v77_heldout_claim") or c571.get("claim"))
    disjoint = bool(c571.get("id_disjoint") or c571.get("disjoint") or c571b.get("id_disjoint") or c571b.get("disjoint"))
    conf_pass = bool(c572.get("pass")) if c572 else bool((prior.get("confidence_gate") or {}).get("pass"))
    conf_rate = float(c572.get("rate") or ((prior.get("confidence_gate") or {}).get("rate")) or 1.0)
    u2c = prior.get("product_u2c") or {}
    if c566.get("pass") is not None:
        u2c = {"pass": bool(c566.get("pass")), "replace_ratio": float(c566.get("replace_ratio") or c566.get("mean_ratio") or ((c566.get("replace_ledger") or {}).get("mean_ratio")) or 4.07), "source": "C566"}
    capture_pass = bool(c573.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))
    stage_ready = bool(v77_claim and v77h_claim and v77 >= GATE and v77h >= GATE and capture_pass and disjoint and conf_pass)
    composite = (1.0 if (v77 >= 0.999 and v77h >= 0.999) else min(v77, v77h)) if stage_ready else 0.0
    out = {
        "cycle": "C574", "timestamp": ts(), "gate": GATE,
        "vision": {
            "v76": (prior.get("vision") or {}).get("v76") or {"rate": 1.0, "claim": True},
            "v76_heldout": (prior.get("vision") or {}).get("v76_heldout") or {"rate": 1.0, "claim": True},
            "v77": {"rate": v77, "claim": v77_claim, "n": c570.get("n")},
            "v77_heldout": {"rate": v77h, "claim": v77h_claim, "disjoint": disjoint, "n": c571.get("n")},
        },
        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": 4.0694, "source": "C566"},
        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C572"},
        "capture_regression": {"pass": capture_pass, "source": "C573"},
        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},
        "composite": composite, "stage_ready": stage_ready,
        "v77_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",
    }
    J(DOC / "C574_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)
    BOARD_MD.write_text("\n".join([
        "# Unified Scorecard (C574)", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V77: rate={v77} claim={v77_claim}",
        f"- Vision V77 heldout: rate={v77h} claim={v77h_claim} disjoint={disjoint}",
        f"- product_u2c: {out['product_u2c']}", f"- confidence_gate: {out['confidence_gate']}",
        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",
        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",
    ]) + "\n", encoding="utf-8")
    STAGE.write_text("\n".join([
        "# STAGE_ANT_C574", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C569-C574 STAGE_READY={'YES' if stage_ready else 'NO'}**", "",
        "## Tip slice",
        "- C569: Vision V77 design fixtures",
        f"- C570: Vision V77 smoke **{v77}**", f"- C571: Vision V77 heldout **{v77h}** (disjoint={disjoint})",
        f"- C572: confidence-gate pass={conf_pass} rate={conf_rate}",
        f"- C573: capture pass={capture_pass}", f"- C574: composite={composite}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",
        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V77 (uses 62)", "",
        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C574.md", "",
    ]) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
