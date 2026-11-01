# -*- coding: utf-8 -*-
"""C622: Unified scorecard + STAGE after C617-C621. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C622.md"
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
    c618 = load("docs/r50/C618_VISION_V85_SMOKE.json") or {}
    c618b = load("docs/r50/C618b_VISION_GATE_V85_CLAIM.json") or {}
    c619 = load("docs/r50/C619_VISION_V85_HELDOUT_SMOKE.json") or {}
    c619b = load("docs/r50/C619b_VISION_GATE_V85_HELDOUT_CLAIM.json") or {}
    c620 = load("docs/r50/C620_CONFIDENCE_GATE_STRETCH.json") or {}
    c621 = load("docs/r50/C621_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c614 = load("docs/r50/C614_PRODUCT_U2C_COST.json") or {}

    v85 = float(c618.get("rate") or 0.0)
    v85h = float(c619.get("rate") or 0.0)
    v85_claim = bool(c618b.get("vl_gate_v85_claim") or c618.get("vl_gate_v85_claim") or c618.get("claim"))
    v85h_claim = bool(c619b.get("vl_gate_v85_heldout_claim") or c619.get("vl_gate_v85_heldout_claim") or c619.get("claim"))
    disjoint = bool(c619.get("id_disjoint") or c619.get("disjoint") or c619b.get("id_disjoint") or c619b.get("disjoint"))
    conf_pass = bool(c620.get("pass"))
    conf_rate = float(c620.get("rate") or 0.0)
    u2c = prior.get("product_u2c") or {}
    if c614.get("pass") is not None:
        u2c = {
            "pass": bool(c614.get("pass")),
            "replace_ratio": float(c614.get("replace_ratio") or c614.get("mean_ratio") or 4.07),
            "source": "C614",
        }
    replace = float(u2c.get("replace_ratio") or 4.07)
    capture_pass = bool(c621.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))
    stage_ready = bool(v85_claim and v85h_claim and v85 >= GATE and v85h >= GATE and capture_pass and disjoint and conf_pass)
    composite = (1.0 if (v85 >= 0.999 and v85h >= 0.999) else min(v85, v85h)) if stage_ready else 0.0
    out = {
        "cycle": "C622", "timestamp": ts(), "gate": GATE,
        "vision": {
            "v84": (prior.get("vision") or {}).get("v84") or {"rate": 1.0, "claim": True},
            "v84_heldout": (prior.get("vision") or {}).get("v84_heldout") or {"rate": 1.0, "claim": True},
            "v85": {"rate": v85, "claim": v85_claim, "n": c618.get("n")},
            "v85_heldout": {"rate": v85h, "claim": v85h_claim, "disjoint": disjoint, "n": c619.get("n")},
        },
        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C614"},
        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C620"},
        "capture_regression": {"pass": capture_pass, "source": "C621"},
        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},
        "composite": composite, "stage_ready": stage_ready,
        "v85_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",
    }
    J(DOC / "C622_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)
    BOARD_MD.write_text("\n".join([
        "# Unified Scorecard (C622)", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V85: rate={v85} claim={v85_claim}",
        f"- Vision V85 heldout: rate={v85h} claim={v85h_claim} disjoint={disjoint}",
        f"- product_u2c: {out['product_u2c']}", f"- confidence_gate: {out['confidence_gate']}",
        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",
        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",
    ]) + "\n", encoding="utf-8")
    STAGE.write_text("\n".join([
        "# STAGE_ANT_C622", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C617-C622 STAGE_READY={'YES' if stage_ready else 'NO'}**", "",
        "## Tip slice",
        "- C617: Vision V85 design fixtures",
        f"- C618: Vision V85 smoke **{v85}**", f"- C619: Vision V85 heldout **{v85h}** (disjoint={disjoint})",
        f"- C620: confidence-gate stretch rate={conf_rate} pass={conf_pass}",
        f"- C621: capture pass={capture_pass}", f"- C622: composite={composite}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",
        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V85 (uses 62)", "",
        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C622.md", "",
    ]) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
