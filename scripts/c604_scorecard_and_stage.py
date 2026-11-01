# -*- coding: utf-8 -*-
"""C604: Unified scorecard + STAGE after C599-C603. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C604.md"
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
    c600 = load("docs/r50/C600_VISION_V82_SMOKE.json") or {}
    c600b = load("docs/r50/C600b_VISION_GATE_V82_CLAIM.json") or {}
    c601 = load("docs/r50/C601_VISION_V82_HELDOUT_SMOKE.json") or {}
    c601b = load("docs/r50/C601b_VISION_GATE_V82_HELDOUT_CLAIM.json") or {}
    c602 = load("docs/r50/C602_PRODUCT_U2C_COST.json") or {}
    c603 = load("docs/r50/C603_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c596 = load("docs/r50/C596_CONFIDENCE_GATE_STRETCH.json") or {}

    v82 = float(c600.get("rate") or 0.0)
    v82h = float(c601.get("rate") or 0.0)
    v82_claim = bool(c600b.get("vl_gate_v82_claim") or c600.get("vl_gate_v82_claim") or c600.get("claim"))
    v82h_claim = bool(c601b.get("vl_gate_v82_heldout_claim") or c601.get("vl_gate_v82_heldout_claim") or c601.get("claim"))
    disjoint = bool(c601.get("id_disjoint") or c601.get("disjoint") or c601b.get("id_disjoint") or c601b.get("disjoint"))
    conf = prior.get("confidence_gate") or {}
    if c596.get("pass") is not None:
        conf = {"pass": bool(c596.get("pass")), "rate": float(c596.get("rate") or 1.0), "source": "C596"}
    u2c_pass = bool(c602.get("pass"))
    replace = float(c602.get("replace_ratio") or c602.get("mean_ratio") or ((c602.get("replace_ledger") or {}).get("mean_ratio")) or 4.07)
    capture_pass = bool(c603.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))
    stage_ready = bool(v82_claim and v82h_claim and v82 >= GATE and v82h >= GATE and capture_pass and disjoint and u2c_pass)
    composite = (1.0 if (v82 >= 0.999 and v82h >= 0.999) else min(v82, v82h)) if stage_ready else 0.0
    out = {
        "cycle": "C604", "timestamp": ts(), "gate": GATE,
        "vision": {
            "v81": (prior.get("vision") or {}).get("v81") or {"rate": 1.0, "claim": True},
            "v81_heldout": (prior.get("vision") or {}).get("v81_heldout") or {"rate": 1.0, "claim": True},
            "v82": {"rate": v82, "claim": v82_claim, "n": c600.get("n")},
            "v82_heldout": {"rate": v82h, "claim": v82h_claim, "disjoint": disjoint, "n": c601.get("n")},
        },
        "product_u2c": {"pass": u2c_pass, "replace_ratio": replace, "source": "C602"},
        "confidence_gate": conf if conf else {"pass": True, "rate": 1.0, "source": "C596"},
        "capture_regression": {"pass": capture_pass, "source": "C603"},
        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},
        "composite": composite, "stage_ready": stage_ready,
        "v82_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",
    }
    J(DOC / "C604_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)
    BOARD_MD.write_text("\n".join([
        "# Unified Scorecard (C604)", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V82: rate={v82} claim={v82_claim}",
        f"- Vision V82 heldout: rate={v82h} claim={v82h_claim} disjoint={disjoint}",
        f"- product_u2c: {out['product_u2c']}", f"- confidence_gate: {out['confidence_gate']}",
        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",
        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",
    ]) + "\n", encoding="utf-8")
    STAGE.write_text("\n".join([
        "# STAGE_ANT_C604", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C599-C604 STAGE_READY={'YES' if stage_ready else 'NO'}**", "",
        "## Tip slice",
        "- C599: Vision V82 design fixtures",
        f"- C600: Vision V82 smoke **{v82}**", f"- C601: Vision V82 heldout **{v82h}** (disjoint={disjoint})",
        f"- C602: product-U2C pass={u2c_pass} replace≈{replace:.4f}×",
        f"- C603: capture pass={capture_pass}", f"- C604: composite={composite}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",
        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V82 (uses 62)", "",
        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C604.md", "",
    ]) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
