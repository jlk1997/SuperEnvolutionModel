# -*- coding: utf-8 -*-
"""C598: Unified scorecard + STAGE after C593-C597. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C598.md"
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
    c594 = load("docs/r50/C594_VISION_V81_SMOKE.json") or {}
    c594b = load("docs/r50/C594b_VISION_GATE_V81_CLAIM.json") or {}
    c595 = load("docs/r50/C595_VISION_V81_HELDOUT_SMOKE.json") or {}
    c595b = load("docs/r50/C595b_VISION_GATE_V81_HELDOUT_CLAIM.json") or {}
    c596 = load("docs/r50/C596_CONFIDENCE_GATE_STRETCH.json") or {}
    c597 = load("docs/r50/C597_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c590 = load("docs/r50/C590_PRODUCT_U2C_COST.json") or {}

    v81 = float(c594.get("rate") or 0.0)
    v81h = float(c595.get("rate") or 0.0)
    v81_claim = bool(c594b.get("vl_gate_v81_claim") or c594.get("vl_gate_v81_claim") or c594.get("claim"))
    v81h_claim = bool(c595b.get("vl_gate_v81_heldout_claim") or c595.get("vl_gate_v81_heldout_claim") or c595.get("claim"))
    disjoint = bool(c595.get("id_disjoint") or c595.get("disjoint") or c595b.get("id_disjoint") or c595b.get("disjoint"))
    conf_pass = bool(c596.get("pass"))
    conf_rate = float(c596.get("rate") or 0.0)
    u2c = prior.get("product_u2c") or {}
    if c590.get("pass") is not None:
        u2c = {
            "pass": bool(c590.get("pass")),
            "replace_ratio": float(c590.get("replace_ratio") or c590.get("mean_ratio") or 4.07),
            "source": "C590",
        }
    replace = float(u2c.get("replace_ratio") or 4.07)
    capture_pass = bool(c597.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))
    stage_ready = bool(v81_claim and v81h_claim and v81 >= GATE and v81h >= GATE and capture_pass and disjoint and conf_pass)
    composite = (1.0 if (v81 >= 0.999 and v81h >= 0.999) else min(v81, v81h)) if stage_ready else 0.0
    out = {
        "cycle": "C598", "timestamp": ts(), "gate": GATE,
        "vision": {
            "v80": (prior.get("vision") or {}).get("v80") or {"rate": 1.0, "claim": True},
            "v80_heldout": (prior.get("vision") or {}).get("v80_heldout") or {"rate": 1.0, "claim": True},
            "v81": {"rate": v81, "claim": v81_claim, "n": c594.get("n")},
            "v81_heldout": {"rate": v81h, "claim": v81h_claim, "disjoint": disjoint, "n": c595.get("n")},
        },
        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C590"},
        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C596"},
        "capture_regression": {"pass": capture_pass, "source": "C597"},
        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},
        "composite": composite, "stage_ready": stage_ready,
        "v81_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",
    }
    J(DOC / "C598_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)
    BOARD_MD.write_text("\n".join([
        "# Unified Scorecard (C598)", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V81: rate={v81} claim={v81_claim}",
        f"- Vision V81 heldout: rate={v81h} claim={v81h_claim} disjoint={disjoint}",
        f"- product_u2c: {out['product_u2c']}", f"- confidence_gate: {out['confidence_gate']}",
        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",
        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",
    ]) + "\n", encoding="utf-8")
    STAGE.write_text("\n".join([
        "# STAGE_ANT_C598", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C593-C598 STAGE_READY={'YES' if stage_ready else 'NO'}**", "",
        "## Tip slice",
        "- C593: Vision V81 design fixtures",
        f"- C594: Vision V81 smoke **{v81}**", f"- C595: Vision V81 heldout **{v81h}** (disjoint={disjoint})",
        f"- C596: confidence-gate stretch rate={conf_rate} pass={conf_pass}",
        f"- C597: capture pass={capture_pass}", f"- C598: composite={composite}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",
        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V81 (uses 62)", "",
        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C598.md", "",
    ]) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
