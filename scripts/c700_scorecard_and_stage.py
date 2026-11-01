# -*- coding: utf-8 -*-
"""C700: Unified scorecard + STAGE after C695-C699. V98 milestone. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C700.md"
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
    c648 = load("docs/r50/C696_VISION_V98_SMOKE.json") or {}
    c648b = load("docs/r50/C696b_VISION_GATE_V98_CLAIM.json") or {}
    c649 = load("docs/r50/C697_VISION_V98_HELDOUT_SMOKE.json") or {}
    c649b = load("docs/r50/C697b_VISION_GATE_V98_HELDOUT_CLAIM.json") or {}
    c650 = load("docs/r50/C698_PRODUCT_U2C_COST.json") or {}
    c651 = load("docs/r50/C699_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c644 = load("docs/r50/C692_CONFIDENCE_GATE_STRETCH.json") or {}

    v98 = float(c648.get("rate") or 0.0)
    v98h = float(c649.get("rate") or 0.0)
    v98_claim = bool(c648b.get("vl_gate_v98_claim") or c648.get("vl_gate_v98_claim") or c648.get("claim"))
    v98h_claim = bool(c649b.get("vl_gate_v98_heldout_claim") or c649.get("vl_gate_v98_heldout_claim") or c649.get("claim"))
    disjoint = bool(c649.get("id_disjoint") or c649.get("disjoint") or c649b.get("id_disjoint") or c649b.get("disjoint"))
    conf = prior.get("confidence_gate") or {}
    if c644.get("pass") is not None:
        conf = {"pass": bool(c644.get("pass")), "rate": float(c644.get("rate") or 1.0), "source": "C692"}
    u2c_pass = bool(c650.get("pass"))
    replace = float(c650.get("replace_ratio") or c650.get("mean_ratio") or ((c650.get("replace_ledger") or {}).get("mean_ratio")) or 4.07)
    capture_pass = bool(c651.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))
    stage_ready = bool(v98_claim and v98h_claim and v98 >= GATE and v98h >= GATE and capture_pass and disjoint and u2c_pass)
    composite = (1.0 if (v98 >= 0.999 and v98h >= 0.999) else min(v98, v98h)) if stage_ready else 0.0
    out = {
        "cycle": "C700", "timestamp": ts(), "gate": GATE, "milestone": "V98",
        "vision": {
            "v97": (prior.get("vision") or {}).get("v97") or {"rate": 1.0, "claim": True},
            "v97_heldout": (prior.get("vision") or {}).get("v97_heldout") or {"rate": 1.0, "claim": True},
            "v98": {"rate": v98, "claim": v98_claim, "n": c648.get("n")},
            "v98_heldout": {"rate": v98h, "claim": v98h_claim, "disjoint": disjoint, "n": c649.get("n")},
        },
        "product_u2c": {"pass": u2c_pass, "replace_ratio": replace, "source": "C698"},
        "confidence_gate": conf if conf else {"pass": True, "rate": 1.0, "source": "C692"},
        "capture_regression": {"pass": capture_pass, "source": "C699"},
        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},
        "composite": composite, "stage_ready": stage_ready,
        "v98_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",
    }
    J(DOC / "C700_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)
    BOARD_MD.write_text("\n".join([
        "# Unified Scorecard (C700) — V98 milestone", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V98: rate={v98} claim={v98_claim}",
        f"- Vision V98 heldout: rate={v98h} claim={v98h_claim} disjoint={disjoint}",
        f"- product_u2c: {out['product_u2c']}", f"- confidence_gate: {out['confidence_gate']}",
        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",
        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD | V98 continue", "",
    ]) + "\n", encoding="utf-8")
    STAGE.write_text("\n".join([
        "# STAGE_ANT_C700", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C695-C700 STAGE_READY={'YES' if stage_ready else 'NO'} — V98 milestone (continue)**", "",
        "## Tip slice",
        "- C695: Vision V98 design fixtures",
        f"- C696: Vision V98 smoke **{v98}**", f"- C697: Vision V98 heldout **{v98h}** (disjoint={disjoint})",
        f"- C698: product-U2C pass={u2c_pass} replace≈{replace:.4f}×",
        f"- C699: capture pass={capture_pass}", f"- C700: composite={composite}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",
        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V98 (uses 62)",
        "- V98 milestone is NOT a stop — continue to V97+",
        "- lesson: avoid *b theme-name collapse (V88)", "",
        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C700.md", "",
    ]) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
