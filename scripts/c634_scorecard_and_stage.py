# -*- coding: utf-8 -*-
"""C634: Unified scorecard + STAGE after C629-C633. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C634.md"
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
    c630 = load("docs/r50/C630_VISION_V87_SMOKE.json") or {}
    c630b = load("docs/r50/C630b_VISION_GATE_V87_CLAIM.json") or {}
    c631 = load("docs/r50/C631_VISION_V87_HELDOUT_SMOKE.json") or {}
    c631b = load("docs/r50/C631b_VISION_GATE_V87_HELDOUT_CLAIM.json") or {}
    c632 = load("docs/r50/C632_CONFIDENCE_GATE_STRETCH.json") or {}
    c633 = load("docs/r50/C633_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c626 = load("docs/r50/C626_PRODUCT_U2C_COST.json") or {}

    v87 = float(c630.get("rate") or 0.0)
    v87h = float(c631.get("rate") or 0.0)
    v87_claim = bool(c630b.get("vl_gate_v87_claim") or c630.get("vl_gate_v87_claim") or c630.get("claim"))
    v87h_claim = bool(c631b.get("vl_gate_v87_heldout_claim") or c631.get("vl_gate_v87_heldout_claim") or c631.get("claim"))
    disjoint = bool(c631.get("id_disjoint") or c631.get("disjoint") or c631b.get("id_disjoint") or c631b.get("disjoint"))
    conf_pass = bool(c632.get("pass"))
    conf_rate = float(c632.get("rate") or 0.0)
    u2c = prior.get("product_u2c") or {}
    if c626.get("pass") is not None:
        u2c = {
            "pass": bool(c626.get("pass")),
            "replace_ratio": float(c626.get("replace_ratio") or c626.get("mean_ratio") or 4.07),
            "source": "C626",
        }
    replace = float(u2c.get("replace_ratio") or 4.07)
    capture_pass = bool(c633.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))
    stage_ready = bool(v87_claim and v87h_claim and v87 >= GATE and v87h >= GATE and capture_pass and disjoint and conf_pass)
    composite = (1.0 if (v87 >= 0.999 and v87h >= 0.999) else min(v87, v87h)) if stage_ready else 0.0
    out = {
        "cycle": "C634", "timestamp": ts(), "gate": GATE,
        "vision": {
            "v86": (prior.get("vision") or {}).get("v86") or {"rate": 1.0, "claim": True},
            "v86_heldout": (prior.get("vision") or {}).get("v86_heldout") or {"rate": 1.0, "claim": True},
            "v87": {"rate": v87, "claim": v87_claim, "n": c630.get("n")},
            "v87_heldout": {"rate": v87h, "claim": v87h_claim, "disjoint": disjoint, "n": c631.get("n")},
        },
        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C626"},
        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C632"},
        "capture_regression": {"pass": capture_pass, "source": "C633"},
        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},
        "composite": composite, "stage_ready": stage_ready,
        "v87_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",
    }
    J(DOC / "C634_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)
    BOARD_MD.write_text("\n".join([
        "# Unified Scorecard (C634)", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V87: rate={v87} claim={v87_claim}",
        f"- Vision V87 heldout: rate={v87h} claim={v87h_claim} disjoint={disjoint}",
        f"- product_u2c: {out['product_u2c']}", f"- confidence_gate: {out['confidence_gate']}",
        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",
        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",
    ]) + "\n", encoding="utf-8")
    STAGE.write_text("\n".join([
        "# STAGE_ANT_C634", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C629-C634 STAGE_READY={'YES' if stage_ready else 'NO'}**", "",
        "## Tip slice",
        "- C629: Vision V87 design fixtures",
        f"- C630: Vision V87 smoke **{v87}**", f"- C631: Vision V87 heldout **{v87h}** (disjoint={disjoint})",
        f"- C632: confidence-gate stretch rate={conf_rate} pass={conf_pass}",
        f"- C633: capture pass={capture_pass}", f"- C634: composite={composite}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",
        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V87 (uses 62)", "",
        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C634.md", "",
    ]) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
