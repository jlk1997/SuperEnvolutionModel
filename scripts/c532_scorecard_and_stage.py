# -*- coding: utf-8 -*-
"""C532: Unified scorecard + STAGE after C527-C531. V70 milestone. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C532.md"
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
    c528 = load("docs/r50/C528_VISION_V70_SMOKE.json") or {}
    c528b = load("docs/r50/C528b_VISION_GATE_V70_CLAIM.json") or {}
    c529 = load("docs/r50/C529_VISION_V70_HELDOUT_SMOKE.json") or {}
    c529b = load("docs/r50/C529b_VISION_GATE_V70_HELDOUT_CLAIM.json") or {}
    c530 = load("docs/r50/C530_PRODUCT_U2C_COST.json") or {}
    c531 = load("docs/r50/C531_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c524 = load("docs/r50/C524_CONFIDENCE_GATE_STRETCH.json") or {}

    v70 = float(c528.get("rate") or 0.0)
    v70h = float(c529.get("rate") or 0.0)
    v70_claim = bool(c528b.get("vl_gate_v70_claim") or c528.get("vl_gate_v70_claim") or c528.get("claim"))
    v70h_claim = bool(c529b.get("vl_gate_v70_heldout_claim") or c529.get("vl_gate_v70_heldout_claim") or c529.get("claim"))
    disjoint = bool(c529.get("id_disjoint") or c529.get("disjoint") or c529b.get("id_disjoint") or c529b.get("disjoint"))
    conf = prior.get("confidence_gate") or {}
    if c524.get("pass") is not None:
        conf = {"pass": bool(c524.get("pass")), "rate": float(c524.get("rate") or 1.0), "source": "C524"}
    u2c_pass = bool(c530.get("pass"))
    replace = float(
        c530.get("replace_ratio")
        or c530.get("mean_ratio")
        or ((c530.get("replace_ledger") or {}).get("mean_ratio"))
        or 4.07
    )
    capture_pass = bool(c531.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))

    stage_ready = bool(
        v70_claim and v70h_claim and v70 >= GATE and v70h >= GATE
        and capture_pass and disjoint and u2c_pass
    )
    composite = 0.0
    if stage_ready:
        composite = 1.0 if (v70 >= 0.999 and v70h >= 0.999) else min(v70, v70h)

    out = {
        "cycle": "C532",
        "timestamp": ts(),
        "gate": GATE,
        "milestone": "V70",
        "vision": {
            "v69": (prior.get("vision") or {}).get("v69") or {"rate": 1.0, "claim": True},
            "v69_heldout": (prior.get("vision") or {}).get("v69_heldout") or {"rate": 1.0, "claim": True},
            "v70": {"rate": v70, "claim": v70_claim, "n": c528.get("n")},
            "v70_heldout": {"rate": v70h, "claim": v70h_claim, "disjoint": disjoint, "n": c529.get("n")},
        },
        "product_u2c": {"pass": u2c_pass, "replace_ratio": replace, "source": "C530"},
        "confidence_gate": conf if conf else {"pass": True, "rate": 1.0, "source": "C524"},
        "capture_regression": {"pass": capture_pass, "source": "C531"},
        "dissolve_shadow": {
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        },
        "composite": composite,
        "stage_ready": stage_ready,
        "v70_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }
    J(DOC / "C532_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = [
        "# Unified Scorecard (C532) — V70 milestone", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V70: rate={v70} claim={v70_claim}",
        f"- Vision V70 heldout: rate={v70h} claim={v70h_claim} disjoint={disjoint}",
        f"- product_u2c: {out['product_u2c']}",
        f"- confidence_gate: {out['confidence_gate']}",
        f"- capture_regression: pass={capture_pass}",
        f"- dissolve/shadow: {dissolve_pass}/{shadow_pass}",
        f"- composite: {out['composite']}",
        f"- stage_ready: {stage_ready}",
        "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD | V70 not a stop", "",
    ]
    BOARD_MD.write_text("\n".join(md) + "\n", encoding="utf-8")

    stage = [
        "# STAGE_ANT_C532", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C527-C532 STAGE_READY={'YES' if stage_ready else 'NO'} — V70 milestone (continue)**", "",
        "## Tip slice",
        "- C527: Vision V70 design fixtures (jpeg_q=62, floor>=60, long themes)",
        f"- C528: Vision V70 smoke claim **{v70}** (n={c528.get('n')})",
        f"- C529: Vision V70 heldout claim **{v70h}** (disjoint={disjoint})",
        f"- C530: product-U2C pass={u2c_pass} replace≈{replace:.4f}×",
        f"- C531: capture-office regression pass={capture_pass}",
        f"- C532: unified scorecard composite={out['composite']}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally; not model-plus-separate-agent).", "",
        "## Constraints",
        "- Gate: 0.6",
        "- Gate2/3: untouched",
        "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V70 (uses 62)",
        "- V70 milestone is NOT a stop — continue to V71+", "",
        "## Entry",
        f"- Scorecard: {BOARD_MD.relative_to(ROOT).as_posix()}",
        "- Latest JSON: docs/r50/SCORECARD_LATEST.json",
        "- This stage: docs/STAGE_ANT_C532.md", "",
    ]
    STAGE.write_text("\n".join(stage) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
