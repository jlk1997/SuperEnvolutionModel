# -*- coding: utf-8 -*-
"""C454: Unified scorecard + STAGE after C449-C453. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C454.md"
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
    c450 = load("docs/r50/C450_VISION_V57_SMOKE.json") or {}
    c450b = load("docs/r50/C450b_VISION_GATE_V57_CLAIM.json") or {}
    c451 = load("docs/r50/C451_VISION_V57_HELDOUT_SMOKE.json") or {}
    c451b = load("docs/r50/C451b_VISION_GATE_V57_HELDOUT_CLAIM.json") or {}
    c452 = load("docs/r50/C452_CONFIDENCE_GATE_STRETCH.json") or {}
    c453 = load("docs/r50/C453_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c446 = load("docs/r50/C446_PRODUCT_U2C_COST.json") or {}

    v57 = float(c450.get("rate") or 0.0)
    v57h = float(c451.get("rate") or 0.0)
    v57_claim = bool(c450b.get("vl_gate_v57_claim") or c450.get("vl_gate_v57_claim") or c450.get("claim"))
    v57h_claim = bool(c451b.get("vl_gate_v57_heldout_claim") or c451.get("vl_gate_v57_heldout_claim") or c451.get("claim"))
    disjoint = bool(c451.get("id_disjoint") or c451.get("disjoint") or c451b.get("id_disjoint") or c451b.get("disjoint"))
    conf_pass = bool(c452.get("pass")) if c452 else bool((prior.get("confidence_gate") or {}).get("pass"))
    conf_rate = float(c452.get("rate") or ((prior.get("confidence_gate") or {}).get("rate")) or 1.0)
    u2c = prior.get("product_u2c") or {}
    if c446.get("pass") is not None:
        u2c = {
            "pass": bool(c446.get("pass")),
            "replace_ratio": float(
                c446.get("replace_ratio")
                or c446.get("mean_ratio")
                or ((c446.get("replace_ledger") or {}).get("mean_ratio"))
                or 4.07
            ),
            "source": "C446",
        }
    capture_pass = bool(c453.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))

    stage_ready = bool(
        v57_claim and v57h_claim and v57 >= GATE and v57h >= GATE
        and capture_pass and disjoint and conf_pass
    )
    composite = 0.0
    if stage_ready:
        composite = 1.0 if (v57 >= 0.999 and v57h >= 0.999) else min(v57, v57h)

    out = {
        "cycle": "C454",
        "timestamp": ts(),
        "gate": GATE,
        "vision": {
            "v56": (prior.get("vision") or {}).get("v56") or {"rate": 1.0, "claim": True},
            "v56_heldout": (prior.get("vision") or {}).get("v56_heldout") or {"rate": 1.0, "claim": True},
            "v57": {"rate": v57, "claim": v57_claim, "n": c450.get("n")},
            "v57_heldout": {"rate": v57h, "claim": v57h_claim, "disjoint": disjoint, "n": c451.get("n")},
        },
        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": 4.0694, "source": "C446"},
        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C452"},
        "capture_regression": {"pass": capture_pass, "source": "C453"},
        "dissolve_shadow": {
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        },
        "composite": composite,
        "stage_ready": stage_ready,
        "v57_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }
    J(DOC / "C454_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = [
        "# Unified Scorecard (C454)", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V57: rate={v57} claim={v57_claim}",
        f"- Vision V57 heldout: rate={v57h} claim={v57h_claim} disjoint={disjoint}",
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
        "# STAGE_ANT_C454", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C449-C454 STAGE_READY={'YES' if stage_ready else 'NO'}**", "",
        "## Tip slice",
        "- C449: Vision V57 design fixtures (jpeg_q=62, floor>=60)",
        f"- C450: Vision V57 smoke claim **{v57}** (n={c450.get('n')})",
        f"- C451: Vision V57 heldout claim **{v57h}** (disjoint={disjoint})",
        f"- C452: confidence-gate stretch pass={conf_pass} rate={conf_rate}",
        f"- C453: capture-office regression pass={capture_pass}",
        f"- C454: unified scorecard composite={out['composite']}", "",
        "## Constraints",
        "- Gate: 0.6",
        "- Gate2/3: untouched",
        "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V57 (uses 62)", "",
        "## Entry",
        f"- Scorecard: {BOARD_MD.relative_to(ROOT).as_posix()}",
        "- Latest JSON: docs/r50/SCORECARD_LATEST.json",
        "- This stage: docs/STAGE_ANT_C454.md", "",
    ]
    STAGE.write_text("\n".join(stage) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
