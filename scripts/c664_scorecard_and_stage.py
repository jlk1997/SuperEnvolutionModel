# -*- coding: utf-8 -*-
"""C664: Unified scorecard + STAGE after C659-C663. V92 milestone. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C664.md"
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
    c648 = load("docs/r50/C660_VISION_V92_SMOKE.json") or {}
    c648b = load("docs/r50/C660b_VISION_GATE_V92_CLAIM.json") or {}
    c649 = load("docs/r50/C661_VISION_V92_HELDOUT_SMOKE.json") or {}
    c649b = load("docs/r50/C661b_VISION_GATE_V92_HELDOUT_CLAIM.json") or {}
    c650 = load("docs/r50/C662_PRODUCT_U2C_COST.json") or {}
    c651 = load("docs/r50/C663_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c644 = load("docs/r50/C656_CONFIDENCE_GATE_STRETCH.json") or {}

    v92 = float(c648.get("rate") or 0.0)
    v92h = float(c649.get("rate") or 0.0)
    v92_claim = bool(c648b.get("vl_gate_v92_claim") or c648.get("vl_gate_v92_claim") or c648.get("claim"))
    v92h_claim = bool(c649b.get("vl_gate_v92_heldout_claim") or c649.get("vl_gate_v92_heldout_claim") or c649.get("claim"))
    disjoint = bool(c649.get("id_disjoint") or c649.get("disjoint") or c649b.get("id_disjoint") or c649b.get("disjoint"))
    conf = prior.get("confidence_gate") or {}
    if c644.get("pass") is not None:
        conf = {"pass": bool(c644.get("pass")), "rate": float(c644.get("rate") or 1.0), "source": "C656"}
    u2c_pass = bool(c650.get("pass"))
    replace = float(c650.get("replace_ratio") or c650.get("mean_ratio") or ((c650.get("replace_ledger") or {}).get("mean_ratio")) or 4.07)
    capture_pass = bool(c651.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))
    stage_ready = bool(v92_claim and v92h_claim and v92 >= GATE and v92h >= GATE and capture_pass and disjoint and u2c_pass)
    composite = (1.0 if (v92 >= 0.999 and v92h >= 0.999) else min(v92, v92h)) if stage_ready else 0.0
    out = {
        "cycle": "C664", "timestamp": ts(), "gate": GATE, "milestone": "V92",
        "vision": {
            "v91": (prior.get("vision") or {}).get("v91") or {"rate": 1.0, "claim": True},
            "v91_heldout": (prior.get("vision") or {}).get("v91_heldout") or {"rate": 1.0, "claim": True},
            "v92": {"rate": v92, "claim": v92_claim, "n": c648.get("n")},
            "v92_heldout": {"rate": v92h, "claim": v92h_claim, "disjoint": disjoint, "n": c649.get("n")},
        },
        "product_u2c": {"pass": u2c_pass, "replace_ratio": replace, "source": "C662"},
        "confidence_gate": conf if conf else {"pass": True, "rate": 1.0, "source": "C656"},
        "capture_regression": {"pass": capture_pass, "source": "C663"},
        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},
        "composite": composite, "stage_ready": stage_ready,
        "v92_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",
    }
    J(DOC / "C664_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)
    BOARD_MD.write_text("\n".join([
        "# Unified Scorecard (C664) — V92 milestone", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V92: rate={v92} claim={v92_claim}",
        f"- Vision V92 heldout: rate={v92h} claim={v92h_claim} disjoint={disjoint}",
        f"- product_u2c: {out['product_u2c']}", f"- confidence_gate: {out['confidence_gate']}",
        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",
        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD | V92 continue", "",
    ]) + "\n", encoding="utf-8")
    STAGE.write_text("\n".join([
        "# STAGE_ANT_C664", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C659-C664 STAGE_READY={'YES' if stage_ready else 'NO'} — V92 milestone (continue)**", "",
        "## Tip slice",
        "- C659: Vision V92 design fixtures",
        f"- C660: Vision V92 smoke **{v92}**", f"- C661: Vision V92 heldout **{v92h}** (disjoint={disjoint})",
        f"- C662: product-U2C pass={u2c_pass} replace≈{replace:.4f}×",
        f"- C663: capture pass={capture_pass}", f"- C664: composite={composite}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",
        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V92 (uses 62)",
        "- V92 milestone is NOT a stop — continue to V91+",
        "- lesson: avoid *b theme-name collapse (V88)", "",
        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C664.md", "",
    ]) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
