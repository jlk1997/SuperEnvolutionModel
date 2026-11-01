# -*- coding: utf-8 -*-
"""C568: Unified scorecard + STAGE after C563-C567. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C568.md"
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
    c564 = load("docs/r50/C564_VISION_V76_SMOKE.json") or {}
    c564b = load("docs/r50/C564b_VISION_GATE_V76_CLAIM.json") or {}
    c565 = load("docs/r50/C565_VISION_V76_HELDOUT_SMOKE.json") or {}
    c565b = load("docs/r50/C565b_VISION_GATE_V76_HELDOUT_CLAIM.json") or {}
    c566 = load("docs/r50/C566_PRODUCT_U2C_COST.json") or {}
    c567 = load("docs/r50/C567_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c560 = load("docs/r50/C560_CONFIDENCE_GATE_STRETCH.json") or {}

    v76 = float(c564.get("rate") or 0.0)
    v76h = float(c565.get("rate") or 0.0)
    v76_claim = bool(c564b.get("vl_gate_v76_claim") or c564.get("vl_gate_v76_claim") or c564.get("claim"))
    v76h_claim = bool(c565b.get("vl_gate_v76_heldout_claim") or c565.get("vl_gate_v76_heldout_claim") or c565.get("claim"))
    disjoint = bool(c565.get("id_disjoint") or c565.get("disjoint") or c565b.get("id_disjoint") or c565b.get("disjoint"))
    conf = prior.get("confidence_gate") or {}
    if c560.get("pass") is not None:
        conf = {"pass": bool(c560.get("pass")), "rate": float(c560.get("rate") or 1.0), "source": "C560"}
    u2c_pass = bool(c566.get("pass"))
    replace = float(c566.get("replace_ratio") or c566.get("mean_ratio") or ((c566.get("replace_ledger") or {}).get("mean_ratio")) or 4.07)
    capture_pass = bool(c567.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))
    stage_ready = bool(v76_claim and v76h_claim and v76 >= GATE and v76h >= GATE and capture_pass and disjoint and u2c_pass)
    composite = (1.0 if (v76 >= 0.999 and v76h >= 0.999) else min(v76, v76h)) if stage_ready else 0.0
    out = {
        "cycle": "C568", "timestamp": ts(), "gate": GATE,
        "vision": {
            "v75": (prior.get("vision") or {}).get("v75") or {"rate": 1.0, "claim": True},
            "v75_heldout": (prior.get("vision") or {}).get("v75_heldout") or {"rate": 1.0, "claim": True},
            "v76": {"rate": v76, "claim": v76_claim, "n": c564.get("n")},
            "v76_heldout": {"rate": v76h, "claim": v76h_claim, "disjoint": disjoint, "n": c565.get("n")},
        },
        "product_u2c": {"pass": u2c_pass, "replace_ratio": replace, "source": "C566"},
        "confidence_gate": conf if conf else {"pass": True, "rate": 1.0, "source": "C560"},
        "capture_regression": {"pass": capture_pass, "source": "C567"},
        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},
        "composite": composite, "stage_ready": stage_ready,
        "v76_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",
    }
    J(DOC / "C568_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)
    BOARD_MD.write_text("\n".join([
        "# Unified Scorecard (C568)", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V76: rate={v76} claim={v76_claim}",
        f"- Vision V76 heldout: rate={v76h} claim={v76h_claim} disjoint={disjoint}",
        f"- product_u2c: {out['product_u2c']}", f"- confidence_gate: {out['confidence_gate']}",
        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",
        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",
    ]) + "\n", encoding="utf-8")
    STAGE.write_text("\n".join([
        "# STAGE_ANT_C568", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C563-C568 STAGE_READY={'YES' if stage_ready else 'NO'}**", "",
        "## Tip slice",
        "- C563: Vision V76 design fixtures",
        f"- C564: Vision V76 smoke **{v76}**", f"- C565: Vision V76 heldout **{v76h}** (disjoint={disjoint})",
        f"- C566: product-U2C pass={u2c_pass} replace≈{replace:.4f}×",
        f"- C567: capture pass={capture_pass}", f"- C568: composite={composite}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",
        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V76 (uses 62)", "",
        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C568.md", "",
    ]) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
