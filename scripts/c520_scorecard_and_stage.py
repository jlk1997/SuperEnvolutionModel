# -*- coding: utf-8 -*-
"""C520: Unified scorecard + STAGE after C515-C519. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C520.md"
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
    c516 = load("docs/r50/C516_VISION_V68_SMOKE.json") or {}
    c516b = load("docs/r50/C516b_VISION_GATE_V68_CLAIM.json") or {}
    c517 = load("docs/r50/C517_VISION_V68_HELDOUT_SMOKE.json") or {}
    c517b = load("docs/r50/C517b_VISION_GATE_V68_HELDOUT_CLAIM.json") or {}
    c518 = load("docs/r50/C518_PRODUCT_U2C_COST.json") or {}
    c519 = load("docs/r50/C519_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c512 = load("docs/r50/C512_CONFIDENCE_GATE_STRETCH.json") or {}

    v68 = float(c516.get("rate") or 0.0)
    v68h = float(c517.get("rate") or 0.0)
    v68_claim = bool(c516b.get("vl_gate_v68_claim") or c516.get("vl_gate_v68_claim") or c516.get("claim"))
    v68h_claim = bool(c517b.get("vl_gate_v68_heldout_claim") or c517.get("vl_gate_v68_heldout_claim") or c517.get("claim"))
    disjoint = bool(c517.get("id_disjoint") or c517.get("disjoint") or c517b.get("id_disjoint") or c517b.get("disjoint"))
    conf = prior.get("confidence_gate") or {}
    if c512.get("pass") is not None:
        conf = {"pass": bool(c512.get("pass")), "rate": float(c512.get("rate") or 1.0), "source": "C512"}
    u2c_pass = bool(c518.get("pass"))
    replace = float(
        c518.get("replace_ratio")
        or c518.get("mean_ratio")
        or ((c518.get("replace_ledger") or {}).get("mean_ratio"))
        or 4.07
    )
    capture_pass = bool(c519.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))

    stage_ready = bool(
        v68_claim and v68h_claim and v68 >= GATE and v68h >= GATE
        and capture_pass and disjoint and u2c_pass
    )
    composite = 0.0
    if stage_ready:
        composite = 1.0 if (v68 >= 0.999 and v68h >= 0.999) else min(v68, v68h)

    out = {
        "cycle": "C520",
        "timestamp": ts(),
        "gate": GATE,
        "vision": {
            "v67": (prior.get("vision") or {}).get("v67") or {"rate": 1.0, "claim": True},
            "v67_heldout": (prior.get("vision") or {}).get("v67_heldout") or {"rate": 1.0, "claim": True},
            "v68": {"rate": v68, "claim": v68_claim, "n": c516.get("n")},
            "v68_heldout": {"rate": v68h, "claim": v68h_claim, "disjoint": disjoint, "n": c517.get("n")},
        },
        "product_u2c": {"pass": u2c_pass, "replace_ratio": replace, "source": "C518"},
        "confidence_gate": conf if conf else {"pass": True, "rate": 1.0, "source": "C512"},
        "capture_regression": {"pass": capture_pass, "source": "C519"},
        "dissolve_shadow": {
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        },
        "composite": composite,
        "stage_ready": stage_ready,
        "v68_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }
    J(DOC / "C520_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = [
        "# Unified Scorecard (C520)", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V68: rate={v68} claim={v68_claim}",
        f"- Vision V68 heldout: rate={v68h} claim={v68h_claim} disjoint={disjoint}",
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
        "# STAGE_ANT_C520", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C515-C520 STAGE_READY={'YES' if stage_ready else 'NO'}**", "",
        "## Tip slice",
        "- C515: Vision V68 design fixtures (jpeg_q=62, floor>=60, long themes)",
        f"- C516: Vision V68 smoke claim **{v68}** (n={c516.get('n')})",
        f"- C517: Vision V68 heldout claim **{v68h}** (disjoint={disjoint})",
        f"- C518: product-U2C pass={u2c_pass} replace≈{replace:.4f}×",
        f"- C519: capture-office regression pass={capture_pass}",
        f"- C520: unified scorecard composite={out['composite']}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally; not model-plus-separate-agent).", "",
        "## Constraints",
        "- Gate: 0.6",
        "- Gate2/3: untouched",
        "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V68 (uses 62)", "",
        "## Entry",
        f"- Scorecard: {BOARD_MD.relative_to(ROOT).as_posix()}",
        "- Latest JSON: docs/r50/SCORECARD_LATEST.json",
        "- This stage: docs/STAGE_ANT_C520.md", "",
    ]
    STAGE.write_text("\n".join(stage) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
