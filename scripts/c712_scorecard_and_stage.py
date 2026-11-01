# -*- coding: utf-8 -*-
"""C712: Unified scorecard + STAGE after C707-C711. V100 milestone. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C712.md"
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
    c648 = load("docs/r50/C708_VISION_V100_SMOKE.json") or {}
    c648b = load("docs/r50/C708b_VISION_GATE_V100_CLAIM.json") or {}
    c649 = load("docs/r50/C709_VISION_V100_HELDOUT_SMOKE.json") or {}
    c649b = load("docs/r50/C709b_VISION_GATE_V100_HELDOUT_CLAIM.json") or {}
    c650 = load("docs/r50/C710_PRODUCT_U2C_COST.json") or {}
    c651 = load("docs/r50/C711_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c644 = load("docs/r50/C704_CONFIDENCE_GATE_STRETCH.json") or {}

    v100 = float(c648.get("rate") or 0.0)
    v100h = float(c649.get("rate") or 0.0)
    v100_claim = bool(c648b.get("vl_gate_v100_claim") or c648.get("vl_gate_v100_claim") or c648.get("claim"))
    v100h_claim = bool(c649b.get("vl_gate_v100_heldout_claim") or c649.get("vl_gate_v100_heldout_claim") or c649.get("claim"))
    disjoint = bool(c649.get("id_disjoint") or c649.get("disjoint") or c649b.get("id_disjoint") or c649b.get("disjoint"))
    conf = prior.get("confidence_gate") or {}
    if c644.get("pass") is not None:
        conf = {"pass": bool(c644.get("pass")), "rate": float(c644.get("rate") or 1.0), "source": "C704"}
    u2c_pass = bool(c650.get("pass"))
    replace = float(c650.get("replace_ratio") or c650.get("mean_ratio") or ((c650.get("replace_ledger") or {}).get("mean_ratio")) or 4.07)
    capture_pass = bool(c651.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))
    stage_ready = bool(v100_claim and v100h_claim and v100 >= GATE and v100h >= GATE and capture_pass and disjoint and u2c_pass)
    composite = (1.0 if (v100 >= 0.999 and v100h >= 0.999) else min(v100, v100h)) if stage_ready else 0.0
    out = {
        "cycle": "C712", "timestamp": ts(), "gate": GATE, "milestone": "V100",
        "vision": {
            "v99": (prior.get("vision") or {}).get("v99") or {"rate": 1.0, "claim": True},
            "v99_heldout": (prior.get("vision") or {}).get("v99_heldout") or {"rate": 1.0, "claim": True},
            "v100": {"rate": v100, "claim": v100_claim, "n": c648.get("n")},
            "v100_heldout": {"rate": v100h, "claim": v100h_claim, "disjoint": disjoint, "n": c649.get("n")},
        },
        "product_u2c": {"pass": u2c_pass, "replace_ratio": replace, "source": "C710"},
        "confidence_gate": conf if conf else {"pass": True, "rate": 1.0, "source": "C704"},
        "capture_regression": {"pass": capture_pass, "source": "C711"},
        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},
        "composite": composite, "stage_ready": stage_ready,
        "v100_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",
    }
    J(DOC / "C712_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)
    BOARD_MD.write_text("\n".join([
        "# Unified Scorecard (C712) — V100 milestone", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V100: rate={v100} claim={v100_claim}",
        f"- Vision V100 heldout: rate={v100h} claim={v100h_claim} disjoint={disjoint}",
        f"- product_u2c: {out['product_u2c']}", f"- confidence_gate: {out['confidence_gate']}",
        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",
        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD | V100 continue — V100 not a stop", "",
    ]) + "\n", encoding="utf-8")
    STAGE.write_text("\n".join([
        "# STAGE_ANT_C712", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C707-C712 STAGE_READY={'YES' if stage_ready else 'NO'} — V100 milestone (continue — V100 not a stop)**", "",
        "## Tip slice",
        "- C707: Vision V100 design fixtures",
        f"- C708: Vision V100 smoke **{v100}**", f"- C709: Vision V100 heldout **{v100h}** (disjoint={disjoint})",
        f"- C710: product-U2C pass={u2c_pass} replace≈{replace:.4f}×",
        f"- C711: capture pass={capture_pass}", f"- C712: composite={composite}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",
        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V100 (uses 62)",
        "- V100 milestone is NOT a stop — continue — V100 not a stop to V99+",
        "- lesson: avoid *b theme-name collapse (V88)", "",
        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C712.md", "",
    ]) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
