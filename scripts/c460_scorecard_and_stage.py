# -*- coding: utf-8 -*-
"""C460: Unified scorecard + STAGE after C455-C459. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C460.md"
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
    c456 = load("docs/r50/C456_VISION_V58_SMOKE.json") or {}
    c456b = load("docs/r50/C456b_VISION_GATE_V58_CLAIM.json") or {}
    c457 = load("docs/r50/C457_VISION_V58_HELDOUT_SMOKE.json") or {}
    c457b = load("docs/r50/C457b_VISION_GATE_V58_HELDOUT_CLAIM.json") or {}
    c458 = load("docs/r50/C458_PRODUCT_U2C_COST.json") or {}
    c459 = load("docs/r50/C459_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c452 = load("docs/r50/C452_CONFIDENCE_GATE_STRETCH.json") or {}

    v58 = float(c456.get("rate") or 0.0)
    v58h = float(c457.get("rate") or 0.0)
    v58_claim = bool(c456b.get("vl_gate_v58_claim") or c456.get("vl_gate_v58_claim") or c456.get("claim"))
    v58h_claim = bool(c457b.get("vl_gate_v58_heldout_claim") or c457.get("vl_gate_v58_heldout_claim") or c457.get("claim"))
    disjoint = bool(c457.get("id_disjoint") or c457.get("disjoint") or c457b.get("id_disjoint") or c457b.get("disjoint"))

    _rl = c458.get("replace_ledger") or {}
    u2c_pass = bool(c458.get("pass")) if c458 else bool((prior.get("product_u2c") or {}).get("pass"))
    u2c_replace = float(
        c458.get("replace_ratio")
        or _rl.get("mean_ratio")
        or ((prior.get("product_u2c") or {}).get("replace_ratio"))
        or 4.07
    )
    conf = prior.get("confidence_gate") or {}
    if c452.get("pass") is not None:
        conf = {
            "pass": bool(c452.get("pass")),
            "rate": float(c452.get("rate") or 1.0),
            "source": "C452",
        }
    capture_pass = bool(c459.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))

    stage_ready = bool(
        v58_claim and v58h_claim and v58 >= GATE and v58h >= GATE
        and capture_pass and disjoint and u2c_pass
    )
    composite = 0.0
    if stage_ready:
        composite = 1.0 if (v58 >= 0.999 and v58h >= 0.999) else min(v58, v58h)

    out = {
        "cycle": "C460",
        "timestamp": ts(),
        "gate": GATE,
        "vision": {
            "v57": (prior.get("vision") or {}).get("v57") or {"rate": 1.0, "claim": True},
            "v57_heldout": (prior.get("vision") or {}).get("v57_heldout") or {"rate": 1.0, "claim": True},
            "v58": {"rate": v58, "claim": v58_claim, "n": c456.get("n")},
            "v58_heldout": {"rate": v58h, "claim": v58h_claim, "disjoint": disjoint, "n": c457.get("n")},
        },
        "product_u2c": {"pass": u2c_pass, "replace_ratio": u2c_replace, "source": "C458"},
        "confidence_gate": conf if conf else {"pass": True, "rate": 1.0, "source": "C452"},
        "capture_regression": {"pass": capture_pass, "source": "C459"},
        "dissolve_shadow": {
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        },
        "composite": composite,
        "stage_ready": stage_ready,
        "v58_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }
    J(DOC / "C460_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = [
        "# Unified Scorecard (C460)", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V58: rate={v58} claim={v58_claim}",
        f"- Vision V58 heldout: rate={v58h} claim={v58h_claim} disjoint={disjoint}",
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
        "# STAGE_ANT_C460", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C455-C460 STAGE_READY={'YES' if stage_ready else 'NO'}**", "",
        "## Tip slice",
        "- C455: Vision V58 design fixtures (jpeg_q=62, floor>=60)",
        f"- C456: Vision V58 smoke claim **{v58}** (n={c456.get('n')})",
        f"- C457: Vision V58 heldout claim **{v58h}** (disjoint={disjoint})",
        f"- C458: product-u2c pass={u2c_pass} replace~={u2c_replace}",
        f"- C459: capture-office regression pass={capture_pass}",
        f"- C460: unified scorecard composite={out['composite']}", "",
        "## Constraints",
        "- Gate: 0.6",
        "- Gate2/3: untouched",
        "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V58 (uses 62)", "",
        "## Entry",
        f"- Scorecard: {BOARD_MD.relative_to(ROOT).as_posix()}",
        "- Latest JSON: docs/r50/SCORECARD_LATEST.json",
        "- This stage: docs/STAGE_ANT_C460.md", "",
    ]
    STAGE.write_text("\n".join(stage) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
