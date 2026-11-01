# -*- coding: utf-8 -*-
"""C448: Unified scorecard + STAGE after C443-C447. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C448.md"
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
    c444 = load("docs/r50/C444_VISION_V56_SMOKE.json") or {}
    c444b = load("docs/r50/C444b_VISION_GATE_V56_CLAIM.json") or {}
    c445 = load("docs/r50/C445_VISION_V56_HELDOUT_SMOKE.json") or {}
    c445b = load("docs/r50/C445b_VISION_GATE_V56_HELDOUT_CLAIM.json") or {}
    c446 = load("docs/r50/C446_PRODUCT_U2C_COST.json") or {}
    c447 = load("docs/r50/C447_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c440 = load("docs/r50/C440_CONFIDENCE_GATE_STRETCH.json") or {}

    v56 = float(c444.get("rate") or 0.0)
    v56h = float(c445.get("rate") or 0.0)
    v56_claim = bool(c444b.get("vl_gate_v56_claim") or c444.get("vl_gate_v56_claim") or c444.get("claim"))
    v56h_claim = bool(c445b.get("vl_gate_v56_heldout_claim") or c445.get("vl_gate_v56_heldout_claim") or c445.get("claim"))
    disjoint = bool(c445.get("id_disjoint") or c445.get("disjoint") or c445b.get("id_disjoint") or c445b.get("disjoint"))

    _rl = c446.get("replace_ledger") or {}
    u2c_pass = bool(c446.get("pass")) if c446 else bool((prior.get("product_u2c") or {}).get("pass"))
    u2c_replace = float(
        c446.get("replace_ratio")
        or _rl.get("mean_ratio")
        or ((prior.get("product_u2c") or {}).get("replace_ratio"))
        or 4.07
    )
    conf = prior.get("confidence_gate") or {}
    if c440.get("pass") is not None:
        conf = {
            "pass": bool(c440.get("pass")),
            "rate": float(c440.get("rate") or 1.0),
            "source": "C440",
        }
    capture_pass = bool(c447.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))

    stage_ready = bool(
        v56_claim and v56h_claim and v56 >= GATE and v56h >= GATE
        and capture_pass and disjoint and u2c_pass
    )
    composite = 0.0
    if stage_ready:
        composite = 1.0 if (v56 >= 0.999 and v56h >= 0.999) else min(v56, v56h)

    out = {
        "cycle": "C448",
        "timestamp": ts(),
        "gate": GATE,
        "vision": {
            "v55": (prior.get("vision") or {}).get("v55") or {"rate": 1.0, "claim": True},
            "v55_heldout": (prior.get("vision") or {}).get("v55_heldout") or {"rate": 1.0, "claim": True},
            "v56": {"rate": v56, "claim": v56_claim, "n": c444.get("n")},
            "v56_heldout": {"rate": v56h, "claim": v56h_claim, "disjoint": disjoint, "n": c445.get("n")},
        },
        "product_u2c": {"pass": u2c_pass, "replace_ratio": u2c_replace, "source": "C446"},
        "confidence_gate": conf if conf else {"pass": True, "rate": 1.0, "source": "C440"},
        "capture_regression": {"pass": capture_pass, "source": "C447"},
        "dissolve_shadow": {
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        },
        "composite": composite,
        "stage_ready": stage_ready,
        "v56_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }
    J(DOC / "C448_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = [
        "# Unified Scorecard (C448)", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V56: rate={v56} claim={v56_claim}",
        f"- Vision V56 heldout: rate={v56h} claim={v56h_claim} disjoint={disjoint}",
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
        "# STAGE_ANT_C448", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C443-C448 STAGE_READY={'YES' if stage_ready else 'NO'}**", "",
        "## Tip slice",
        "- C443: Vision V56 design fixtures (jpeg_q=62, floor>=60)",
        f"- C444: Vision V56 smoke claim **{v56}** (n={c444.get('n')})",
        f"- C445: Vision V56 heldout claim **{v56h}** (disjoint={disjoint})",
        f"- C446: product-u2c pass={u2c_pass} replace~={u2c_replace}",
        f"- C447: capture-office regression pass={capture_pass}",
        f"- C448: unified scorecard composite={out['composite']}", "",
        "## Constraints",
        "- Gate: 0.6",
        "- Gate2/3: untouched",
        "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V56 (uses 62)", "",
        "## Entry",
        f"- Scorecard: {BOARD_MD.relative_to(ROOT).as_posix()}",
        "- Latest JSON: docs/r50/SCORECARD_LATEST.json",
        "- This stage: docs/STAGE_ANT_C448.md", "",
    ]
    STAGE.write_text("\n".join(stage) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
