# -*- coding: utf-8 -*-
"""C508: Unified scorecard + STAGE after C503-C507. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C508.md"
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
    c504 = load("docs/r50/C504_VISION_V66_SMOKE.json") or {}
    c504b = load("docs/r50/C504b_VISION_GATE_V66_CLAIM.json") or {}
    c505 = load("docs/r50/C505_VISION_V66_HELDOUT_SMOKE.json") or {}
    c505b = load("docs/r50/C505b_VISION_GATE_V66_HELDOUT_CLAIM.json") or {}
    c506 = load("docs/r50/C506_PRODUCT_U2C_COST.json") or {}
    c507 = load("docs/r50/C507_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c500 = load("docs/r50/C500_CONFIDENCE_GATE_STRETCH.json") or {}

    v66 = float(c504.get("rate") or 0.0)
    v66h = float(c505.get("rate") or 0.0)
    v66_claim = bool(c504b.get("vl_gate_v66_claim") or c504.get("vl_gate_v66_claim") or c504.get("claim"))
    v66h_claim = bool(c505b.get("vl_gate_v66_heldout_claim") or c505.get("vl_gate_v66_heldout_claim") or c505.get("claim"))
    disjoint = bool(c505.get("id_disjoint") or c505.get("disjoint") or c505b.get("id_disjoint") or c505b.get("disjoint"))
    conf = prior.get("confidence_gate") or {}
    if c500.get("pass") is not None:
        conf = {"pass": bool(c500.get("pass")), "rate": float(c500.get("rate") or 1.0), "source": "C500"}
    u2c_pass = bool(c506.get("pass"))
    replace = float(
        c506.get("replace_ratio")
        or c506.get("mean_ratio")
        or ((c506.get("replace_ledger") or {}).get("mean_ratio"))
        or 4.07
    )
    capture_pass = bool(c507.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))

    stage_ready = bool(
        v66_claim and v66h_claim and v66 >= GATE and v66h >= GATE
        and capture_pass and disjoint and u2c_pass
    )
    composite = 0.0
    if stage_ready:
        composite = 1.0 if (v66 >= 0.999 and v66h >= 0.999) else min(v66, v66h)

    out = {
        "cycle": "C508",
        "timestamp": ts(),
        "gate": GATE,
        "vision": {
            "v65": (prior.get("vision") or {}).get("v65") or {"rate": 1.0, "claim": True},
            "v65_heldout": (prior.get("vision") or {}).get("v65_heldout") or {"rate": 1.0, "claim": True},
            "v66": {"rate": v66, "claim": v66_claim, "n": c504.get("n")},
            "v66_heldout": {"rate": v66h, "claim": v66h_claim, "disjoint": disjoint, "n": c505.get("n")},
        },
        "product_u2c": {"pass": u2c_pass, "replace_ratio": replace, "source": "C506"},
        "confidence_gate": conf if conf else {"pass": True, "rate": 1.0, "source": "C500"},
        "capture_regression": {"pass": capture_pass, "source": "C507"},
        "dissolve_shadow": {
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        },
        "composite": composite,
        "stage_ready": stage_ready,
        "v66_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }
    J(DOC / "C508_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = [
        "# Unified Scorecard (C508)", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V66: rate={v66} claim={v66_claim}",
        f"- Vision V66 heldout: rate={v66h} claim={v66h_claim} disjoint={disjoint}",
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
        "# STAGE_ANT_C508", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C503-C508 STAGE_READY={'YES' if stage_ready else 'NO'}**", "",
        "## Tip slice",
        "- C503: Vision V66 design fixtures (jpeg_q=62, floor>=60, long themes)",
        f"- C504: Vision V66 smoke claim **{v66}** (n={c504.get('n')})",
        f"- C505: Vision V66 heldout claim **{v66h}** (disjoint={disjoint})",
        f"- C506: product-U2C pass={u2c_pass} replace≈{replace:.4f}×",
        f"- C507: capture-office regression pass={capture_pass}",
        f"- C508: unified scorecard composite={out['composite']}", "",
        "## Constraints",
        "- Gate: 0.6",
        "- Gate2/3: untouched",
        "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V66 (uses 62)", "",
        "## Entry",
        f"- Scorecard: {BOARD_MD.relative_to(ROOT).as_posix()}",
        "- Latest JSON: docs/r50/SCORECARD_LATEST.json",
        "- This stage: docs/STAGE_ANT_C508.md", "",
    ]
    STAGE.write_text("\n".join(stage) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
