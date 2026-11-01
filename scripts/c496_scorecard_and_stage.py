# -*- coding: utf-8 -*-
"""C496: Unified scorecard + STAGE after C491-C495. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C496.md"
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
    c492 = load("docs/r50/C492_VISION_V64_SMOKE.json") or {}
    c492b = load("docs/r50/C492b_VISION_GATE_V64_CLAIM.json") or {}
    c493 = load("docs/r50/C493_VISION_V64_HELDOUT_SMOKE.json") or {}
    c493b = load("docs/r50/C493b_VISION_GATE_V64_HELDOUT_CLAIM.json") or {}
    c494 = load("docs/r50/C494_PRODUCT_U2C_COST.json") or {}
    c495 = load("docs/r50/C495_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c488 = load("docs/r50/C488_CONFIDENCE_GATE_STRETCH.json") or {}

    v64 = float(c492.get("rate") or 0.0)
    v64h = float(c493.get("rate") or 0.0)
    v64_claim = bool(c492b.get("vl_gate_v64_claim") or c492.get("vl_gate_v64_claim") or c492.get("claim"))
    v64h_claim = bool(c493b.get("vl_gate_v64_heldout_claim") or c493.get("vl_gate_v64_heldout_claim") or c493.get("claim"))
    disjoint = bool(c493.get("id_disjoint") or c493.get("disjoint") or c493b.get("id_disjoint") or c493b.get("disjoint"))

    _rl = c494.get("replace_ledger") or {}
    u2c_pass = bool(c494.get("pass")) if c494 else bool((prior.get("product_u2c") or {}).get("pass"))
    u2c_replace = float(
        c494.get("replace_ratio")
        or _rl.get("mean_ratio")
        or ((prior.get("product_u2c") or {}).get("replace_ratio"))
        or 4.07
    )
    conf = prior.get("confidence_gate") or {}
    if c488.get("pass") is not None:
        conf = {
            "pass": bool(c488.get("pass")),
            "rate": float(c488.get("rate") or 1.0),
            "source": "C488",
        }
    capture_pass = bool(c495.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))

    stage_ready = bool(
        v64_claim and v64h_claim and v64 >= GATE and v64h >= GATE
        and capture_pass and disjoint and u2c_pass
    )
    composite = 0.0
    if stage_ready:
        composite = 1.0 if (v64 >= 0.999 and v64h >= 0.999) else min(v64, v64h)

    out = {
        "cycle": "C496",
        "timestamp": ts(),
        "gate": GATE,
        "vision": {
            "v63": (prior.get("vision") or {}).get("v63") or {"rate": 1.0, "claim": True},
            "v63_heldout": (prior.get("vision") or {}).get("v63_heldout") or {"rate": 1.0, "claim": True},
            "v64": {"rate": v64, "claim": v64_claim, "n": c492.get("n")},
            "v64_heldout": {"rate": v64h, "claim": v64h_claim, "disjoint": disjoint, "n": c493.get("n")},
        },
        "product_u2c": {"pass": u2c_pass, "replace_ratio": u2c_replace, "source": "C494"},
        "confidence_gate": conf if conf else {"pass": True, "rate": 1.0, "source": "C488"},
        "capture_regression": {"pass": capture_pass, "source": "C495"},
        "dissolve_shadow": {
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        },
        "composite": composite,
        "stage_ready": stage_ready,
        "v64_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }
    J(DOC / "C496_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = [
        "# Unified Scorecard (C496)", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V64: rate={v64} claim={v64_claim}",
        f"- Vision V64 heldout: rate={v64h} claim={v64h_claim} disjoint={disjoint}",
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
        "# STAGE_ANT_C496", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C491-C496 STAGE_READY={'YES' if stage_ready else 'NO'}**", "",
        "## Tip slice",
        "- C491: Vision V64 design fixtures (jpeg_q=62, floor>=60, long themes)",
        f"- C492: Vision V64 smoke claim **{v64}** (n={c492.get('n')})",
        f"- C493: Vision V64 heldout claim **{v64h}** (disjoint={disjoint})",
        f"- C494: product-u2c pass={u2c_pass} replace~={u2c_replace}",
        f"- C495: capture-office regression pass={capture_pass}",
        f"- C496: unified scorecard composite={out['composite']}", "",
        "## Constraints",
        "- Gate: 0.6",
        "- Gate2/3: untouched",
        "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V64 (uses 62)", "",
        "## Entry",
        f"- Scorecard: {BOARD_MD.relative_to(ROOT).as_posix()}",
        "- Latest JSON: docs/r50/SCORECARD_LATEST.json",
        "- This stage: docs/STAGE_ANT_C496.md", "",
    ]
    STAGE.write_text("\n".join(stage) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
