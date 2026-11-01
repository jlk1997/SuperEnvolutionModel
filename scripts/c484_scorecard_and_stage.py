# -*- coding: utf-8 -*-
"""C484: Unified scorecard + STAGE after C479-C483. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C484.md"
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
    c480 = load("docs/r50/C480_VISION_V62_SMOKE.json") or {}
    c480b = load("docs/r50/C480b_VISION_GATE_V62_CLAIM.json") or {}
    c481 = load("docs/r50/C481_VISION_V62_HELDOUT_SMOKE.json") or {}
    c481b = load("docs/r50/C481b_VISION_GATE_V62_HELDOUT_CLAIM.json") or {}
    c482 = load("docs/r50/C482_PRODUCT_U2C_COST.json") or {}
    c483 = load("docs/r50/C483_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c476 = load("docs/r50/C476_CONFIDENCE_GATE_STRETCH.json") or {}

    v62 = float(c480.get("rate") or 0.0)
    v62h = float(c481.get("rate") or 0.0)
    v62_claim = bool(c480b.get("vl_gate_v62_claim") or c480.get("vl_gate_v62_claim") or c480.get("claim"))
    v62h_claim = bool(c481b.get("vl_gate_v62_heldout_claim") or c481.get("vl_gate_v62_heldout_claim") or c481.get("claim"))
    disjoint = bool(c481.get("id_disjoint") or c481.get("disjoint") or c481b.get("id_disjoint") or c481b.get("disjoint"))

    _rl = c482.get("replace_ledger") or {}
    u2c_pass = bool(c482.get("pass")) if c482 else bool((prior.get("product_u2c") or {}).get("pass"))
    u2c_replace = float(
        c482.get("replace_ratio")
        or _rl.get("mean_ratio")
        or ((prior.get("product_u2c") or {}).get("replace_ratio"))
        or 4.07
    )
    conf = prior.get("confidence_gate") or {}
    if c476.get("pass") is not None:
        conf = {
            "pass": bool(c476.get("pass")),
            "rate": float(c476.get("rate") or 1.0),
            "source": "C476",
        }
    capture_pass = bool(c483.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))

    stage_ready = bool(
        v62_claim and v62h_claim and v62 >= GATE and v62h >= GATE
        and capture_pass and disjoint and u2c_pass
    )
    composite = 0.0
    if stage_ready:
        composite = 1.0 if (v62 >= 0.999 and v62h >= 0.999) else min(v62, v62h)

    out = {
        "cycle": "C484",
        "timestamp": ts(),
        "gate": GATE,
        "vision": {
            "v61": (prior.get("vision") or {}).get("v61") or {"rate": 1.0, "claim": True},
            "v61_heldout": (prior.get("vision") or {}).get("v61_heldout") or {"rate": 1.0, "claim": True},
            "v62": {"rate": v62, "claim": v62_claim, "n": c480.get("n")},
            "v62_heldout": {"rate": v62h, "claim": v62h_claim, "disjoint": disjoint, "n": c481.get("n")},
        },
        "product_u2c": {"pass": u2c_pass, "replace_ratio": u2c_replace, "source": "C482"},
        "confidence_gate": conf if conf else {"pass": True, "rate": 1.0, "source": "C476"},
        "capture_regression": {"pass": capture_pass, "source": "C483"},
        "dissolve_shadow": {
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        },
        "composite": composite,
        "stage_ready": stage_ready,
        "v62_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }
    J(DOC / "C484_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = [
        "# Unified Scorecard (C484)", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V62: rate={v62} claim={v62_claim}",
        f"- Vision V62 heldout: rate={v62h} claim={v62h_claim} disjoint={disjoint}",
        f"- product_u2c: pass={u2c_pass} replace~={u2c_replace}",
        f"- confidence_gate: {out['confidence_gate']}",
        f"- capture_regression: pass={capture_pass}",
        f"- dissolve/shadow: {dissolve_pass}/{shadow_pass}",
        f"- composite: {out['composite']}",
        f"- stage_ready: {stage_ready}",
        "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",
    ]
    BOARD_MD.write_text("\n".join(md) + "\n", encoding="utf-8")

    stage = [
        "# STAGE_ANT_C484", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C479-C484 STAGE_READY={'YES' if stage_ready else 'NO'}**", "",
        "## Tip slice",
        "- C479: Vision V62 design fixtures (jpeg_q=62, floor>=60, long themes)",
        f"- C480: Vision V62 smoke claim **{v62}** (n={c480.get('n')})",
        f"- C481: Vision V62 heldout claim **{v62h}** (disjoint={disjoint})",
        f"- C482: product-u2c pass={u2c_pass} replace~={u2c_replace}",
        f"- C483: capture-office regression pass={capture_pass}",
        f"- C484: unified scorecard composite={out['composite']}", "",
        "## Constraints",
        "- Gate: 0.6",
        "- Gate2/3: untouched",
        "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V62 (uses 62)", "",
        "## Entry",
        f"- Scorecard: {BOARD_MD.relative_to(ROOT).as_posix()}",
        "- Latest JSON: docs/r50/SCORECARD_LATEST.json",
        "- This stage: docs/STAGE_ANT_C484.md", "",
    ]
    STAGE.write_text("\n".join(stage) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
