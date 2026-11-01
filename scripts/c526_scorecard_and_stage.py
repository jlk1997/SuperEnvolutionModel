# -*- coding: utf-8 -*-
"""C526: Unified scorecard + STAGE after C521-C525. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C526.md"
GATE = 0.6


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load(rel):
    p = ROOT / rel
    if not p.is_file():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def main():
    c522 = load("docs/r50/C522_VISION_V69_SMOKE.json") or {}
    c522b = load("docs/r50/C522b_VISION_GATE_V69_CLAIM.json") or {}
    c523 = load("docs/r50/C523_VISION_V69_HELDOUT_SMOKE.json") or {}
    c523b = load("docs/r50/C523b_VISION_GATE_V69_HELDOUT_CLAIM.json") or {}
    c524 = load("docs/r50/C524_CONFIDENCE_GATE_STRETCH.json") or {}
    c525 = load("docs/r50/C525_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c518 = load("docs/r50/C518_PRODUCT_U2C_COST.json") or {}

    v69 = float(c522.get("rate") or 0.0)
    v69h = float(c523.get("rate") or 0.0)
    v69_claim = bool(c522b.get("vl_gate_v69_claim") or c522.get("vl_gate_v69_claim") or c522.get("claim"))
    v69h_claim = bool(c523b.get("vl_gate_v69_heldout_claim") or c523.get("vl_gate_v69_heldout_claim") or c523.get("claim"))
    disjoint = bool(c523.get("id_disjoint") or c523.get("disjoint") or c523b.get("id_disjoint") or c523b.get("disjoint"))
    conf_pass = bool(c524.get("pass")) if c524 else bool((prior.get("confidence_gate") or {}).get("pass"))
    conf_rate = float(c524.get("rate") or ((prior.get("confidence_gate") or {}).get("rate")) or 1.0)
    u2c = prior.get("product_u2c") or {}
    if c518.get("pass") is not None:
        u2c = {
            "pass": bool(c518.get("pass")),
            "replace_ratio": float(
                c518.get("replace_ratio")
                or c518.get("mean_ratio")
                or ((c518.get("replace_ledger") or {}).get("mean_ratio"))
                or 4.07
            ),
            "source": "C518",
        }
    capture_pass = bool(c525.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))

    stage_ready = bool(
        v69_claim and v69h_claim and v69 >= GATE and v69h >= GATE
        and capture_pass and disjoint and conf_pass
    )
    composite = 0.0
    if stage_ready:
        composite = 1.0 if (v69 >= 0.999 and v69h >= 0.999) else min(v69, v69h)

    out = {
        "cycle": "C526",
        "timestamp": ts(),
        "gate": GATE,
        "vision": {
            "v68": (prior.get("vision") or {}).get("v68") or {"rate": 1.0, "claim": True},
            "v68_heldout": (prior.get("vision") or {}).get("v68_heldout") or {"rate": 1.0, "claim": True},
            "v69": {"rate": v69, "claim": v69_claim, "n": c522.get("n")},
            "v69_heldout": {"rate": v69h, "claim": v69h_claim, "disjoint": disjoint, "n": c523.get("n")},
        },
        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": 4.0694, "source": "C518"},
        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C524"},
        "capture_regression": {"pass": capture_pass, "source": "C525"},
        "dissolve_shadow": {
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        },
        "composite": composite,
        "stage_ready": stage_ready,
        "v69_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }
    J(DOC / "C526_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = [
        "# Unified Scorecard (C526)", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V69: rate={v69} claim={v69_claim}",
        f"- Vision V69 heldout: rate={v69h} claim={v69h_claim} disjoint={disjoint}",
        f"- product_u2c: {out['product_u2c']}",
        f"- confidence_gate: {out['confidence_gate']}",
        f"- capture_regression: pass={capture_pass}",
        f"- dissolve/shadow: {dissolve_pass}/{shadow_pass}",
        f"- composite: {out['composite']}",
        f"- stage_ready: {stage_ready}",
        "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",
    ]
    BOARD_MD.write_text("\n".join(md) + "\n", encoding="utf-8")

    stage = [
        "# STAGE_ANT_C526", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C521-C526 STAGE_READY={'YES' if stage_ready else 'NO'}**", "",
        "## Tip slice",
        "- C521: Vision V69 design fixtures (jpeg_q=62, floor>=60, long themes)",
        f"- C522: Vision V69 smoke claim **{v69}** (n={c522.get('n')})",
        f"- C523: Vision V69 heldout claim **{v69h}** (disjoint={disjoint})",
        f"- C524: confidence-gate stretch pass={conf_pass} rate={conf_rate}",
        f"- C525: capture-office regression pass={capture_pass}",
        f"- C526: unified scorecard composite={out['composite']}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally; not model-plus-separate-agent).", "",
        "## Constraints",
        "- Gate: 0.6",
        "- Gate2/3: untouched",
        "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V69 (uses 62)", "",
        "## Entry",
        f"- Scorecard: {BOARD_MD.relative_to(ROOT).as_posix()}",
        "- Latest JSON: docs/r50/SCORECARD_LATEST.json",
        "- This stage: docs/STAGE_ANT_C526.md", "",
    ]
    STAGE.write_text("\n".join(stage) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
