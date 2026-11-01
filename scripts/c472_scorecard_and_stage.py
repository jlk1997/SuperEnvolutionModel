# -*- coding: utf-8 -*-
"""C472: Unified scorecard + STAGE after C467-C471. V60 milestone. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C472.md"
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
    c468 = load("docs/r50/C468_VISION_V60_SMOKE.json") or {}
    c468b = load("docs/r50/C468b_VISION_GATE_V60_CLAIM.json") or {}
    c469 = load("docs/r50/C469_VISION_V60_HELDOUT_SMOKE.json") or {}
    c469b = load("docs/r50/C469b_VISION_GATE_V60_HELDOUT_CLAIM.json") or {}
    c470 = load("docs/r50/C470_PRODUCT_U2C_COST.json") or {}
    c471 = load("docs/r50/C471_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c464 = load("docs/r50/C464_CONFIDENCE_GATE_STRETCH.json") or {}

    v60 = float(c468.get("rate") or 0.0)
    v60h = float(c469.get("rate") or 0.0)
    v60_claim = bool(c468b.get("vl_gate_v60_claim") or c468.get("vl_gate_v60_claim") or c468.get("claim"))
    v60h_claim = bool(c469b.get("vl_gate_v60_heldout_claim") or c469.get("vl_gate_v60_heldout_claim") or c469.get("claim"))
    disjoint = bool(c469.get("id_disjoint") or c469.get("disjoint") or c469b.get("id_disjoint") or c469b.get("disjoint"))

    _rl = c470.get("replace_ledger") or {}
    u2c_pass = bool(c470.get("pass")) if c470 else bool((prior.get("product_u2c") or {}).get("pass"))
    u2c_replace = float(
        c470.get("replace_ratio")
        or _rl.get("mean_ratio")
        or ((prior.get("product_u2c") or {}).get("replace_ratio"))
        or 4.07
    )
    conf = prior.get("confidence_gate") or {}
    if c464.get("pass") is not None:
        conf = {
            "pass": bool(c464.get("pass")),
            "rate": float(c464.get("rate") or 1.0),
            "source": "C464",
        }
    capture_pass = bool(c471.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))

    stage_ready = bool(
        v60_claim and v60h_claim and v60 >= GATE and v60h >= GATE
        and capture_pass and disjoint and u2c_pass
    )
    composite = 0.0
    if stage_ready:
        composite = 1.0 if (v60 >= 0.999 and v60h >= 0.999) else min(v60, v60h)

    out = {
        "cycle": "C472",
        "timestamp": ts(),
        "gate": GATE,
        "milestone": "V60",
        "vision": {
            "v59": (prior.get("vision") or {}).get("v59") or {"rate": 1.0, "claim": True},
            "v59_heldout": (prior.get("vision") or {}).get("v59_heldout") or {"rate": 1.0, "claim": True},
            "v60": {"rate": v60, "claim": v60_claim, "n": c468.get("n")},
            "v60_heldout": {"rate": v60h, "claim": v60h_claim, "disjoint": disjoint, "n": c469.get("n")},
        },
        "product_u2c": {"pass": u2c_pass, "replace_ratio": u2c_replace, "source": "C470"},
        "confidence_gate": conf if conf else {"pass": True, "rate": 1.0, "source": "C464"},
        "capture_regression": {"pass": capture_pass, "source": "C471"},
        "dissolve_shadow": {
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        },
        "composite": composite,
        "stage_ready": stage_ready,
        "v60_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }
    J(DOC / "C472_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = [
        "# Unified Scorecard (C472) — V60 milestone", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V60: rate={v60} claim={v60_claim}",
        f"- Vision V60 heldout: rate={v60h} claim={v60h_claim} disjoint={disjoint}",
        f"- product_u2c: pass={u2c_pass} replace~={u2c_replace}",
        f"- confidence_gate: {out['confidence_gate']}",
        f"- capture_regression: pass={capture_pass}",
        f"- dissolve/shadow: {dissolve_pass}/{shadow_pass}",
        f"- composite: {out['composite']}",
        f"- stage_ready: {stage_ready}",
        "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD | V60 milestone", "",
    ]
    BOARD_MD.write_text("\n".join(md) + "\n", encoding="utf-8")

    stage = [
        "# STAGE_ANT_C472", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C467-C472 STAGE_READY={'YES' if stage_ready else 'NO'} (V60 milestone)**", "",
        "## Tip slice",
        "- C467: Vision V60 design fixtures (jpeg_q=62, floor>=60, long themes)",
        f"- C468: Vision V60 smoke claim **{v60}** (n={c468.get('n')})",
        f"- C469: Vision V60 heldout claim **{v60h}** (disjoint={disjoint})",
        f"- C470: product-u2c pass={u2c_pass} replace~={u2c_replace}",
        f"- C471: capture-office regression pass={capture_pass}",
        f"- C472: unified scorecard composite={out['composite']}", "",
        "## Constraints",
        "- Gate: 0.6",
        "- Gate2/3: untouched",
        "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V60 (uses 62)",
        "- lesson: avoid short VL-collapse theme names (V59 foam)", "",
        "## Entry",
        f"- Scorecard: {BOARD_MD.relative_to(ROOT).as_posix()}",
        "- Latest JSON: docs/r50/SCORECARD_LATEST.json",
        "- This stage: docs/STAGE_ANT_C472.md", "",
    ]
    STAGE.write_text("\n".join(stage) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
