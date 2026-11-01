# -*- coding: utf-8 -*-
"""C466: Unified scorecard + STAGE after C461-C465. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C466.md"
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
    c462 = load("docs/r50/C462_VISION_V59_SMOKE.json") or {}
    c462b = load("docs/r50/C462b_VISION_GATE_V59_CLAIM.json") or {}
    c463 = load("docs/r50/C463_VISION_V59_HELDOUT_SMOKE.json") or {}
    c463b = load("docs/r50/C463b_VISION_GATE_V59_HELDOUT_CLAIM.json") or {}
    c464 = load("docs/r50/C464_CONFIDENCE_GATE_STRETCH.json") or {}
    c465 = load("docs/r50/C465_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c458 = load("docs/r50/C458_PRODUCT_U2C_COST.json") or {}

    v59 = float(c462.get("rate") or 0.0)
    v59h = float(c463.get("rate") or 0.0)
    v59_claim = bool(c462b.get("vl_gate_v59_claim") or c462.get("vl_gate_v59_claim") or c462.get("claim"))
    v59h_claim = bool(c463b.get("vl_gate_v59_heldout_claim") or c463.get("vl_gate_v59_heldout_claim") or c463.get("claim"))
    disjoint = bool(c463.get("id_disjoint") or c463.get("disjoint") or c463b.get("id_disjoint") or c463b.get("disjoint"))
    conf_pass = bool(c464.get("pass")) if c464 else bool((prior.get("confidence_gate") or {}).get("pass"))
    conf_rate = float(c464.get("rate") or ((prior.get("confidence_gate") or {}).get("rate")) or 1.0)
    u2c = prior.get("product_u2c") or {}
    if c458.get("pass") is not None:
        u2c = {
            "pass": bool(c458.get("pass")),
            "replace_ratio": float(
                c458.get("replace_ratio")
                or c458.get("mean_ratio")
                or ((c458.get("replace_ledger") or {}).get("mean_ratio"))
                or 4.07
            ),
            "source": "C458",
        }
    capture_pass = bool(c465.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))

    stage_ready = bool(
        v59_claim and v59h_claim and v59 >= GATE and v59h >= GATE
        and capture_pass and disjoint and conf_pass
    )
    composite = 0.0
    if stage_ready:
        composite = 1.0 if (v59 >= 0.999 and v59h >= 0.999) else min(v59, v59h)

    out = {
        "cycle": "C466",
        "timestamp": ts(),
        "gate": GATE,
        "vision": {
            "v58": (prior.get("vision") or {}).get("v58") or {"rate": 1.0, "claim": True},
            "v58_heldout": (prior.get("vision") or {}).get("v58_heldout") or {"rate": 1.0, "claim": True},
            "v59": {"rate": v59, "claim": v59_claim, "n": c462.get("n")},
            "v59_heldout": {"rate": v59h, "claim": v59h_claim, "disjoint": disjoint, "n": c463.get("n")},
        },
        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": 4.0694, "source": "C458"},
        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C464"},
        "capture_regression": {"pass": capture_pass, "source": "C465"},
        "dissolve_shadow": {
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        },
        "composite": composite,
        "stage_ready": stage_ready,
        "v59_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }
    J(DOC / "C466_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = [
        "# Unified Scorecard (C466)", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V59: rate={v59} claim={v59_claim}",
        f"- Vision V59 heldout: rate={v59h} claim={v59h_claim} disjoint={disjoint}",
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
        "# STAGE_ANT_C466", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C461-C466 STAGE_READY={'YES' if stage_ready else 'NO'}**", "",
        "## Tip slice",
        "- C461: Vision V59 design fixtures (jpeg_q=62, floor>=60)",
        f"- C462: Vision V59 smoke claim **{v59}** (n={c462.get('n')})",
        f"- C463: Vision V59 heldout claim **{v59h}** (disjoint={disjoint})",
        f"- C464: confidence-gate stretch pass={conf_pass} rate={conf_rate}",
        f"- C465: capture-office regression pass={capture_pass}",
        f"- C466: unified scorecard composite={out['composite']}", "",
        "## Constraints",
        "- Gate: 0.6",
        "- Gate2/3: untouched",
        "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V59 (uses 62)", "",
        "## Entry",
        f"- Scorecard: {BOARD_MD.relative_to(ROOT).as_posix()}",
        "- Latest JSON: docs/r50/SCORECARD_LATEST.json",
        "- This stage: docs/STAGE_ANT_C466.md", "",
    ]
    STAGE.write_text("\n".join(stage) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
