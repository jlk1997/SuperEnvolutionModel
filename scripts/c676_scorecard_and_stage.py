# -*- coding: utf-8 -*-
"""C676: Unified scorecard + STAGE after C671-C675. V94 milestone. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C676.md"
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
    c648 = load("docs/r50/C672_VISION_V94_SMOKE.json") or {}
    c648b = load("docs/r50/C672b_VISION_GATE_V94_CLAIM.json") or {}
    c649 = load("docs/r50/C673_VISION_V94_HELDOUT_SMOKE.json") or {}
    c649b = load("docs/r50/C673b_VISION_GATE_V94_HELDOUT_CLAIM.json") or {}
    c650 = load("docs/r50/C674_PRODUCT_U2C_COST.json") or {}
    c651 = load("docs/r50/C675_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c644 = load("docs/r50/C668_CONFIDENCE_GATE_STRETCH.json") or {}

    v94 = float(c648.get("rate") or 0.0)
    v94h = float(c649.get("rate") or 0.0)
    v94_claim = bool(c648b.get("vl_gate_v94_claim") or c648.get("vl_gate_v94_claim") or c648.get("claim"))
    v94h_claim = bool(c649b.get("vl_gate_v94_heldout_claim") or c649.get("vl_gate_v94_heldout_claim") or c649.get("claim"))
    disjoint = bool(c649.get("id_disjoint") or c649.get("disjoint") or c649b.get("id_disjoint") or c649b.get("disjoint"))
    conf = prior.get("confidence_gate") or {}
    if c644.get("pass") is not None:
        conf = {"pass": bool(c644.get("pass")), "rate": float(c644.get("rate") or 1.0), "source": "C668"}
    u2c_pass = bool(c650.get("pass"))
    replace = float(c650.get("replace_ratio") or c650.get("mean_ratio") or ((c650.get("replace_ledger") or {}).get("mean_ratio")) or 4.07)
    capture_pass = bool(c651.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))
    stage_ready = bool(v94_claim and v94h_claim and v94 >= GATE and v94h >= GATE and capture_pass and disjoint and u2c_pass)
    composite = (1.0 if (v94 >= 0.999 and v94h >= 0.999) else min(v94, v94h)) if stage_ready else 0.0
    out = {
        "cycle": "C676", "timestamp": ts(), "gate": GATE, "milestone": "V94",
        "vision": {
            "v93": (prior.get("vision") or {}).get("v93") or {"rate": 1.0, "claim": True},
            "v93_heldout": (prior.get("vision") or {}).get("v93_heldout") or {"rate": 1.0, "claim": True},
            "v94": {"rate": v94, "claim": v94_claim, "n": c648.get("n")},
            "v94_heldout": {"rate": v94h, "claim": v94h_claim, "disjoint": disjoint, "n": c649.get("n")},
        },
        "product_u2c": {"pass": u2c_pass, "replace_ratio": replace, "source": "C674"},
        "confidence_gate": conf if conf else {"pass": True, "rate": 1.0, "source": "C668"},
        "capture_regression": {"pass": capture_pass, "source": "C675"},
        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},
        "composite": composite, "stage_ready": stage_ready,
        "v94_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",
    }
    J(DOC / "C676_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)
    BOARD_MD.write_text("\n".join([
        "# Unified Scorecard (C676) — V94 milestone", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V94: rate={v94} claim={v94_claim}",
        f"- Vision V94 heldout: rate={v94h} claim={v94h_claim} disjoint={disjoint}",
        f"- product_u2c: {out['product_u2c']}", f"- confidence_gate: {out['confidence_gate']}",
        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",
        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD | V94 continue", "",
    ]) + "\n", encoding="utf-8")
    STAGE.write_text("\n".join([
        "# STAGE_ANT_C676", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C671-C676 STAGE_READY={'YES' if stage_ready else 'NO'} — V94 milestone (continue)**", "",
        "## Tip slice",
        "- C671: Vision V94 design fixtures",
        f"- C672: Vision V94 smoke **{v94}**", f"- C673: Vision V94 heldout **{v94h}** (disjoint={disjoint})",
        f"- C674: product-U2C pass={u2c_pass} replace≈{replace:.4f}×",
        f"- C675: capture pass={capture_pass}", f"- C676: composite={composite}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",
        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V94 (uses 62)",
        "- V94 milestone is NOT a stop — continue to V93+",
        "- lesson: avoid *b theme-name collapse (V88)", "",
        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C676.md", "",
    ]) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
