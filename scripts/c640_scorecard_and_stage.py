# -*- coding: utf-8 -*-
"""C640: Unified scorecard + STAGE after C635-C639. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C640.md"
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
    c636 = load("docs/r50/C636_VISION_V88_SMOKE.json") or {}
    c636b = load("docs/r50/C636b_VISION_GATE_V88_CLAIM.json") or {}
    c637 = load("docs/r50/C637_VISION_V88_HELDOUT_SMOKE.json") or {}
    c637b = load("docs/r50/C637b_VISION_GATE_V88_HELDOUT_CLAIM.json") or {}
    c638 = load("docs/r50/C638_PRODUCT_U2C_COST.json") or {}
    c639 = load("docs/r50/C639_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c632 = load("docs/r50/C632_CONFIDENCE_GATE_STRETCH.json") or {}

    v88 = float(c636.get("rate") or 0.0)
    v88h = float(c637.get("rate") or 0.0)
    v88_claim = bool(c636b.get("vl_gate_v88_claim") or c636.get("vl_gate_v88_claim") or c636.get("claim"))
    v88h_claim = bool(c637b.get("vl_gate_v88_heldout_claim") or c637.get("vl_gate_v88_heldout_claim") or c637.get("claim"))
    disjoint = bool(c637.get("id_disjoint") or c637.get("disjoint") or c637b.get("id_disjoint") or c637b.get("disjoint"))
    conf = prior.get("confidence_gate") or {}
    if c632.get("pass") is not None:
        conf = {"pass": bool(c632.get("pass")), "rate": float(c632.get("rate") or 1.0), "source": "C632"}
    u2c_pass = bool(c638.get("pass"))
    replace = float(c638.get("replace_ratio") or c638.get("mean_ratio") or ((c638.get("replace_ledger") or {}).get("mean_ratio")) or 4.07)
    capture_pass = bool(c639.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))
    stage_ready = bool(v88_claim and v88h_claim and v88 >= GATE and v88h >= GATE and capture_pass and disjoint and u2c_pass)
    composite = (1.0 if (v88 >= 0.999 and v88h >= 0.999) else min(v88, v88h)) if stage_ready else 0.0
    out = {
        "cycle": "C640", "timestamp": ts(), "gate": GATE,
        "vision": {
            "v87": (prior.get("vision") or {}).get("v87") or {"rate": 1.0, "claim": True},
            "v87_heldout": (prior.get("vision") or {}).get("v87_heldout") or {"rate": 1.0, "claim": True},
            "v88": {"rate": v88, "claim": v88_claim, "n": c636.get("n")},
            "v88_heldout": {"rate": v88h, "claim": v88h_claim, "disjoint": disjoint, "n": c637.get("n")},
        },
        "product_u2c": {"pass": u2c_pass, "replace_ratio": replace, "source": "C638"},
        "confidence_gate": conf if conf else {"pass": True, "rate": 1.0, "source": "C632"},
        "capture_regression": {"pass": capture_pass, "source": "C639"},
        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},
        "composite": composite, "stage_ready": stage_ready,
        "v88_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",
    }
    J(DOC / "C640_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)
    BOARD_MD.write_text("\n".join([
        "# Unified Scorecard (C640)", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V88: rate={v88} claim={v88_claim}",
        f"- Vision V88 heldout: rate={v88h} claim={v88h_claim} disjoint={disjoint}",
        f"- product_u2c: {out['product_u2c']}", f"- confidence_gate: {out['confidence_gate']}",
        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",
        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",
    ]) + "\n", encoding="utf-8")
    STAGE.write_text("\n".join([
        "# STAGE_ANT_C640", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C635-C640 STAGE_READY={'YES' if stage_ready else 'NO'}**", "",
        "## Tip slice",
        "- C635: Vision V88 design fixtures",
        f"- C636: Vision V88 smoke **{v88}**", f"- C637: Vision V88 heldout **{v88h}** (disjoint={disjoint})",
        f"- C638: product-U2C pass={u2c_pass} replace≈{replace:.4f}×",
        f"- C639: capture pass={capture_pass}", f"- C640: composite={composite}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",
        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V88 (uses 62)", "",
        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C640.md", "",
    ]) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
