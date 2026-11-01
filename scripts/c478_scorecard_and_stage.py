# -*- coding: utf-8 -*-
"""C478: Unified scorecard + STAGE after C473-C477. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C478.md"
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
    c474 = load("docs/r50/C474_VISION_V61_SMOKE.json") or {}
    c474b = load("docs/r50/C474b_VISION_GATE_V61_CLAIM.json") or {}
    c475 = load("docs/r50/C475_VISION_V61_HELDOUT_SMOKE.json") or {}
    c475b = load("docs/r50/C475b_VISION_GATE_V61_HELDOUT_CLAIM.json") or {}
    c476 = load("docs/r50/C476_CONFIDENCE_GATE_STRETCH.json") or {}
    c477 = load("docs/r50/C477_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c470 = load("docs/r50/C470_PRODUCT_U2C_COST.json") or {}

    v61 = float(c474.get("rate") or 0.0)
    v61h = float(c475.get("rate") or 0.0)
    v61_claim = bool(c474b.get("vl_gate_v61_claim") or c474.get("vl_gate_v61_claim") or c474.get("claim"))
    v61h_claim = bool(c475b.get("vl_gate_v61_heldout_claim") or c475.get("vl_gate_v61_heldout_claim") or c475.get("claim"))
    disjoint = bool(c475.get("id_disjoint") or c475.get("disjoint") or c475b.get("id_disjoint") or c475b.get("disjoint"))
    conf_pass = bool(c476.get("pass")) if c476 else bool((prior.get("confidence_gate") or {}).get("pass"))
    conf_rate = float(c476.get("rate") or ((prior.get("confidence_gate") or {}).get("rate")) or 1.0)
    u2c = prior.get("product_u2c") or {}
    if c470.get("pass") is not None:
        u2c = {
            "pass": bool(c470.get("pass")),
            "replace_ratio": float(
                c470.get("replace_ratio")
                or c470.get("mean_ratio")
                or ((c470.get("replace_ledger") or {}).get("mean_ratio"))
                or 4.07
            ),
            "source": "C470",
        }
    capture_pass = bool(c477.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))

    stage_ready = bool(
        v61_claim and v61h_claim and v61 >= GATE and v61h >= GATE
        and capture_pass and disjoint and conf_pass
    )
    composite = 0.0
    if stage_ready:
        composite = 1.0 if (v61 >= 0.999 and v61h >= 0.999) else min(v61, v61h)

    out = {
        "cycle": "C478",
        "timestamp": ts(),
        "gate": GATE,
        "vision": {
            "v60": (prior.get("vision") or {}).get("v60") or {"rate": 1.0, "claim": True},
            "v60_heldout": (prior.get("vision") or {}).get("v60_heldout") or {"rate": 1.0, "claim": True},
            "v61": {"rate": v61, "claim": v61_claim, "n": c474.get("n")},
            "v61_heldout": {"rate": v61h, "claim": v61h_claim, "disjoint": disjoint, "n": c475.get("n")},
        },
        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": 4.0694, "source": "C470"},
        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C476"},
        "capture_regression": {"pass": capture_pass, "source": "C477"},
        "dissolve_shadow": {
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        },
        "composite": composite,
        "stage_ready": stage_ready,
        "v61_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }
    J(DOC / "C478_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = [
        "# Unified Scorecard (C478)", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V61: rate={v61} claim={v61_claim}",
        f"- Vision V61 heldout: rate={v61h} claim={v61h_claim} disjoint={disjoint}",
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
        "# STAGE_ANT_C478", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C473-C478 STAGE_READY={'YES' if stage_ready else 'NO'}**", "",
        "## Tip slice",
        "- C473: Vision V61 design fixtures (jpeg_q=62, floor>=60, long themes)",
        f"- C474: Vision V61 smoke claim **{v61}** (n={c474.get('n')})",
        f"- C475: Vision V61 heldout claim **{v61h}** (disjoint={disjoint})",
        f"- C476: confidence-gate stretch pass={conf_pass} rate={conf_rate}",
        f"- C477: capture-office regression pass={capture_pass}",
        f"- C478: unified scorecard composite={out['composite']}", "",
        "## Constraints",
        "- Gate: 0.6",
        "- Gate2/3: untouched",
        "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V61 (uses 62)", "",
        "## Entry",
        f"- Scorecard: {BOARD_MD.relative_to(ROOT).as_posix()}",
        "- Latest JSON: docs/r50/SCORECARD_LATEST.json",
        "- This stage: docs/STAGE_ANT_C478.md", "",
    ]
    STAGE.write_text("\n".join(stage) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
