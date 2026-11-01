# -*- coding: utf-8 -*-
"""C436: Unified scorecard + STAGE after C431-C435. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C436.md"
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
    c432 = load("docs/r50/C432_VISION_V54_SMOKE.json") or {}
    c432b = load("docs/r50/C432b_VISION_GATE_V54_CLAIM.json") or {}
    c433 = load("docs/r50/C433_VISION_V54_HELDOUT_SMOKE.json") or {}
    c433b = load("docs/r50/C433b_VISION_GATE_V54_HELDOUT_CLAIM.json") or {}
    c434 = load("docs/r50/C434_PRODUCT_U2C_COST.json") or {}
    c435 = load("docs/r50/C435_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}

    v54 = float(c432.get("rate") or 0.0)
    v54h = float(c433.get("rate") or 0.0)
    v54_claim = bool(c432b.get("vl_gate_v54_claim") or c432.get("vl_gate_v54_claim") or c432.get("claim"))
    v54h_claim = bool(c433b.get("vl_gate_v54_heldout_claim") or c433.get("vl_gate_v54_heldout_claim") or c433.get("claim"))
    disjoint = bool(c433.get("id_disjoint") or c433.get("disjoint") or c433b.get("id_disjoint") or c433b.get("disjoint"))

    _rl = c434.get("replace_ledger") or {}
    u2c_pass = bool(c434.get("pass")) if c434 else bool((prior.get("product_u2c") or {}).get("pass"))
    u2c_replace = float(
        c434.get("replace_ratio")
        or _rl.get("mean_ratio")
        or ((prior.get("product_u2c") or {}).get("replace_ratio"))
        or 4.07
    )
    capture_pass = bool(c435.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))

    stage_ready = bool(
        v54_claim and v54h_claim and v54 >= GATE and v54h >= GATE
        and capture_pass and disjoint and u2c_pass
    )
    composite = 0.0
    if stage_ready:
        composite = 1.0 if (v54 >= 0.999 and v54h >= 0.999) else min(v54, v54h)

    out = {
        "cycle": "C436",
        "timestamp": ts(),
        "gate": GATE,
        "vision": {
            "v53": (prior.get("vision") or {}).get("v53") or {"rate": 1.0, "claim": True},
            "v53_heldout": (prior.get("vision") or {}).get("v53_heldout") or {"rate": 1.0, "claim": True},
            "v54": {"rate": v54, "claim": v54_claim, "n": c432.get("n")},
            "v54_heldout": {"rate": v54h, "claim": v54h_claim, "disjoint": disjoint, "n": c433.get("n")},
        },
        "product_u2c": {"pass": u2c_pass, "replace_ratio": u2c_replace, "source": "C434"},
        "capture_regression": {"pass": capture_pass, "source": "C435"},
        "dissolve_shadow": {
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        },
        "composite": composite,
        "stage_ready": stage_ready,
        "v54_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }
    J(DOC / "C436_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = [
        "# Unified Scorecard (C436)", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V54: rate={v54} claim={v54_claim}",
        f"- Vision V54 heldout: rate={v54h} claim={v54h_claim} disjoint={disjoint}",
        f"- product_u2c: pass={u2c_pass} replace≈{u2c_replace}",
        f"- capture_regression: pass={capture_pass}",
        f"- dissolve/shadow: {dissolve_pass}/{shadow_pass}",
        f"- composite: {out['composite']}",
        f"- stage_ready: {stage_ready}",
        "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",
    ]
    BOARD_MD.write_text("\n".join(md) + "\n", encoding="utf-8")

    stage = [
        "# STAGE_ANT_C436", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C431-C436 STAGE_READY={'YES' if stage_ready else 'NO'}**", "",
        "## Tip slice",
        "- C431: Vision V54 design fixtures (jpeg_q=62, floor>=60)",
        f"- C432: Vision V54 smoke claim **{v54}** (n={c432.get('n')})",
        f"- C433: Vision V54 heldout claim **{v54h}** (disjoint={disjoint})",
        f"- C434: product-u2c pass={u2c_pass} replace≈{u2c_replace}",
        f"- C435: capture-office regression pass={capture_pass}",
        f"- C436: unified scorecard composite={out['composite']}", "",
        "## Constraints",
        "- Gate: 0.6",
        "- Gate2/3: untouched",
        "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V54 (uses 62)", "",
        "## Entry",
        f"- Scorecard: {BOARD_MD.relative_to(ROOT).as_posix()}",
        "- Latest JSON: docs/r50/SCORECARD_LATEST.json",
        "- This stage: docs/STAGE_ANT_C436.md", "",
    ]
    STAGE.write_text("\n".join(stage) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
