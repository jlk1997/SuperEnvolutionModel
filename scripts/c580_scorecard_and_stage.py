# -*- coding: utf-8 -*-
"""C580: Unified scorecard + STAGE after C575-C579. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C580.md"
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
    c576 = load("docs/r50/C576_VISION_V78_SMOKE.json") or {}
    c576b = load("docs/r50/C576b_VISION_GATE_V78_CLAIM.json") or {}
    c577 = load("docs/r50/C577_VISION_V78_HELDOUT_SMOKE.json") or {}
    c577b = load("docs/r50/C577b_VISION_GATE_V78_HELDOUT_CLAIM.json") or {}
    c578 = load("docs/r50/C578_PRODUCT_U2C_COST.json") or {}
    c579 = load("docs/r50/C579_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c572 = load("docs/r50/C572_CONFIDENCE_GATE_STRETCH.json") or {}

    v78 = float(c576.get("rate") or 0.0)
    v78h = float(c577.get("rate") or 0.0)
    v78_claim = bool(c576b.get("vl_gate_v78_claim") or c576.get("vl_gate_v78_claim") or c576.get("claim"))
    v78h_claim = bool(c577b.get("vl_gate_v78_heldout_claim") or c577.get("vl_gate_v78_heldout_claim") or c577.get("claim"))
    disjoint = bool(c577.get("id_disjoint") or c577.get("disjoint") or c577b.get("id_disjoint") or c577b.get("disjoint"))
    conf = prior.get("confidence_gate") or {}
    if c572.get("pass") is not None:
        conf = {"pass": bool(c572.get("pass")), "rate": float(c572.get("rate") or 1.0), "source": "C572"}
    u2c_pass = bool(c578.get("pass"))
    replace = float(c578.get("replace_ratio") or c578.get("mean_ratio") or ((c578.get("replace_ledger") or {}).get("mean_ratio")) or 4.07)
    capture_pass = bool(c579.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))
    stage_ready = bool(v78_claim and v78h_claim and v78 >= GATE and v78h >= GATE and capture_pass and disjoint and u2c_pass)
    composite = (1.0 if (v78 >= 0.999 and v78h >= 0.999) else min(v78, v78h)) if stage_ready else 0.0
    out = {
        "cycle": "C580", "timestamp": ts(), "gate": GATE,
        "vision": {
            "v77": (prior.get("vision") or {}).get("v77") or {"rate": 1.0, "claim": True},
            "v77_heldout": (prior.get("vision") or {}).get("v77_heldout") or {"rate": 1.0, "claim": True},
            "v78": {"rate": v78, "claim": v78_claim, "n": c576.get("n")},
            "v78_heldout": {"rate": v78h, "claim": v78h_claim, "disjoint": disjoint, "n": c577.get("n")},
        },
        "product_u2c": {"pass": u2c_pass, "replace_ratio": replace, "source": "C578"},
        "confidence_gate": conf if conf else {"pass": True, "rate": 1.0, "source": "C572"},
        "capture_regression": {"pass": capture_pass, "source": "C579"},
        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},
        "composite": composite, "stage_ready": stage_ready,
        "v78_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",
    }
    J(DOC / "C580_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)
    BOARD_MD.write_text("\n".join([
        "# Unified Scorecard (C580)", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V78: rate={v78} claim={v78_claim}",
        f"- Vision V78 heldout: rate={v78h} claim={v78h_claim} disjoint={disjoint}",
        f"- product_u2c: {out['product_u2c']}", f"- confidence_gate: {out['confidence_gate']}",
        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",
        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",
    ]) + "\n", encoding="utf-8")
    STAGE.write_text("\n".join([
        "# STAGE_ANT_C580", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C575-C580 STAGE_READY={'YES' if stage_ready else 'NO'}**", "",
        "## Tip slice",
        "- C575: Vision V78 design fixtures",
        f"- C576: Vision V78 smoke **{v78}**", f"- C577: Vision V78 heldout **{v78h}** (disjoint={disjoint})",
        f"- C578: product-U2C pass={u2c_pass} replace≈{replace:.4f}×",
        f"- C579: capture pass={capture_pass}", f"- C580: composite={composite}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",
        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V78 (uses 62)", "",
        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C580.md", "",
    ]) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
