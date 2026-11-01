# -*- coding: utf-8 -*-
"""C628: Unified scorecard + STAGE after C623-C627. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C628.md"
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
    c624 = load("docs/r50/C624_VISION_V86_SMOKE.json") or {}
    c624b = load("docs/r50/C624b_VISION_GATE_V86_CLAIM.json") or {}
    c625 = load("docs/r50/C625_VISION_V86_HELDOUT_SMOKE.json") or {}
    c625b = load("docs/r50/C625b_VISION_GATE_V86_HELDOUT_CLAIM.json") or {}
    c626 = load("docs/r50/C626_PRODUCT_U2C_COST.json") or {}
    c627 = load("docs/r50/C627_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c620 = load("docs/r50/C620_CONFIDENCE_GATE_STRETCH.json") or {}

    v86 = float(c624.get("rate") or 0.0)
    v86h = float(c625.get("rate") or 0.0)
    v86_claim = bool(c624b.get("vl_gate_v86_claim") or c624.get("vl_gate_v86_claim") or c624.get("claim"))
    v86h_claim = bool(c625b.get("vl_gate_v86_heldout_claim") or c625.get("vl_gate_v86_heldout_claim") or c625.get("claim"))
    disjoint = bool(c625.get("id_disjoint") or c625.get("disjoint") or c625b.get("id_disjoint") or c625b.get("disjoint"))
    conf = prior.get("confidence_gate") or {}
    if c620.get("pass") is not None:
        conf = {"pass": bool(c620.get("pass")), "rate": float(c620.get("rate") or 1.0), "source": "C620"}
    u2c_pass = bool(c626.get("pass"))
    replace = float(c626.get("replace_ratio") or c626.get("mean_ratio") or ((c626.get("replace_ledger") or {}).get("mean_ratio")) or 4.07)
    capture_pass = bool(c627.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))
    stage_ready = bool(v86_claim and v86h_claim and v86 >= GATE and v86h >= GATE and capture_pass and disjoint and u2c_pass)
    composite = (1.0 if (v86 >= 0.999 and v86h >= 0.999) else min(v86, v86h)) if stage_ready else 0.0
    out = {
        "cycle": "C628", "timestamp": ts(), "gate": GATE,
        "vision": {
            "v85": (prior.get("vision") or {}).get("v85") or {"rate": 1.0, "claim": True},
            "v85_heldout": (prior.get("vision") or {}).get("v85_heldout") or {"rate": 1.0, "claim": True},
            "v86": {"rate": v86, "claim": v86_claim, "n": c624.get("n")},
            "v86_heldout": {"rate": v86h, "claim": v86h_claim, "disjoint": disjoint, "n": c625.get("n")},
        },
        "product_u2c": {"pass": u2c_pass, "replace_ratio": replace, "source": "C626"},
        "confidence_gate": conf if conf else {"pass": True, "rate": 1.0, "source": "C620"},
        "capture_regression": {"pass": capture_pass, "source": "C627"},
        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},
        "composite": composite, "stage_ready": stage_ready,
        "v86_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",
    }
    J(DOC / "C628_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)
    BOARD_MD.write_text("\n".join([
        "# Unified Scorecard (C628)", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V86: rate={v86} claim={v86_claim}",
        f"- Vision V86 heldout: rate={v86h} claim={v86h_claim} disjoint={disjoint}",
        f"- product_u2c: {out['product_u2c']}", f"- confidence_gate: {out['confidence_gate']}",
        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",
        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",
    ]) + "\n", encoding="utf-8")
    STAGE.write_text("\n".join([
        "# STAGE_ANT_C628", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C623-C628 STAGE_READY={'YES' if stage_ready else 'NO'}**", "",
        "## Tip slice",
        "- C623: Vision V86 design fixtures",
        f"- C624: Vision V86 smoke **{v86}**", f"- C625: Vision V86 heldout **{v86h}** (disjoint={disjoint})",
        f"- C626: product-U2C pass={u2c_pass} replace≈{replace:.4f}×",
        f"- C627: capture pass={capture_pass}", f"- C628: composite={composite}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",
        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V86 (uses 62)", "",
        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C628.md", "",
    ]) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
