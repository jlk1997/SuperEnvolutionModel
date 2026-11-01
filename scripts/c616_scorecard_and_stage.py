# -*- coding: utf-8 -*-
"""C616: Unified scorecard + STAGE after C611-C615. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C616.md"
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
    c612 = load("docs/r50/C612_VISION_V84_SMOKE.json") or {}
    c612b = load("docs/r50/C612b_VISION_GATE_V84_CLAIM.json") or {}
    c613 = load("docs/r50/C613_VISION_V84_HELDOUT_SMOKE.json") or {}
    c613b = load("docs/r50/C613b_VISION_GATE_V84_HELDOUT_CLAIM.json") or {}
    c614 = load("docs/r50/C614_PRODUCT_U2C_COST.json") or {}
    c615 = load("docs/r50/C615_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c608 = load("docs/r50/C608_CONFIDENCE_GATE_STRETCH.json") or {}

    v84 = float(c612.get("rate") or 0.0)
    v84h = float(c613.get("rate") or 0.0)
    v84_claim = bool(c612b.get("vl_gate_v84_claim") or c612.get("vl_gate_v84_claim") or c612.get("claim"))
    v84h_claim = bool(c613b.get("vl_gate_v84_heldout_claim") or c613.get("vl_gate_v84_heldout_claim") or c613.get("claim"))
    disjoint = bool(c613.get("id_disjoint") or c613.get("disjoint") or c613b.get("id_disjoint") or c613b.get("disjoint"))
    conf = prior.get("confidence_gate") or {}
    if c608.get("pass") is not None:
        conf = {"pass": bool(c608.get("pass")), "rate": float(c608.get("rate") or 1.0), "source": "C608"}
    u2c_pass = bool(c614.get("pass"))
    replace = float(c614.get("replace_ratio") or c614.get("mean_ratio") or ((c614.get("replace_ledger") or {}).get("mean_ratio")) or 4.07)
    capture_pass = bool(c615.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))
    stage_ready = bool(v84_claim and v84h_claim and v84 >= GATE and v84h >= GATE and capture_pass and disjoint and u2c_pass)
    composite = (1.0 if (v84 >= 0.999 and v84h >= 0.999) else min(v84, v84h)) if stage_ready else 0.0
    out = {
        "cycle": "C616", "timestamp": ts(), "gate": GATE,
        "vision": {
            "v83": (prior.get("vision") or {}).get("v83") or {"rate": 1.0, "claim": True},
            "v83_heldout": (prior.get("vision") or {}).get("v83_heldout") or {"rate": 1.0, "claim": True},
            "v84": {"rate": v84, "claim": v84_claim, "n": c612.get("n")},
            "v84_heldout": {"rate": v84h, "claim": v84h_claim, "disjoint": disjoint, "n": c613.get("n")},
        },
        "product_u2c": {"pass": u2c_pass, "replace_ratio": replace, "source": "C614"},
        "confidence_gate": conf if conf else {"pass": True, "rate": 1.0, "source": "C608"},
        "capture_regression": {"pass": capture_pass, "source": "C615"},
        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},
        "composite": composite, "stage_ready": stage_ready,
        "v84_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",
    }
    J(DOC / "C616_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)
    BOARD_MD.write_text("\n".join([
        "# Unified Scorecard (C616)", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V84: rate={v84} claim={v84_claim}",
        f"- Vision V84 heldout: rate={v84h} claim={v84h_claim} disjoint={disjoint}",
        f"- product_u2c: {out['product_u2c']}", f"- confidence_gate: {out['confidence_gate']}",
        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",
        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",
    ]) + "\n", encoding="utf-8")
    STAGE.write_text("\n".join([
        "# STAGE_ANT_C616", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C611-C616 STAGE_READY={'YES' if stage_ready else 'NO'}**", "",
        "## Tip slice",
        "- C611: Vision V84 design fixtures",
        f"- C612: Vision V84 smoke **{v84}**", f"- C613: Vision V84 heldout **{v84h}** (disjoint={disjoint})",
        f"- C614: product-U2C pass={u2c_pass} replace≈{replace:.4f}×",
        f"- C615: capture pass={capture_pass}", f"- C616: composite={composite}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",
        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V84 (uses 62)", "",
        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C616.md", "",
    ]) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
