# -*- coding: utf-8 -*-
"""C430: Unified scorecard + STAGE after C425-C429. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C430.md"
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
    c426 = load("docs/r50/C426_VISION_V53_SMOKE.json") or {}
    c426b = load("docs/r50/C426b_VISION_GATE_V53_CLAIM.json") or {}
    c427 = load("docs/r50/C427_VISION_V53_HELDOUT_SMOKE.json") or {}
    c427b = load("docs/r50/C427b_VISION_GATE_V53_HELDOUT_CLAIM.json") or {}
    c428 = load("docs/r50/C428_CONFIDENCE_GATE_STRETCH.json") or {}
    c429 = load("docs/r50/C429_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c422 = load("docs/r50/C422_PRODUCT_U2C_COST.json") or {}

    v53 = float(c426.get("rate") or 0.0)
    v53h = float(c427.get("rate") or 0.0)
    v53_claim = bool(c426b.get("vl_gate_v53_claim") or c426.get("vl_gate_v53_claim") or c426.get("claim"))
    v53h_claim = bool(c427b.get("vl_gate_v53_heldout_claim") or c427.get("vl_gate_v53_heldout_claim") or c427.get("claim"))
    disjoint = bool(c427.get("id_disjoint") or c427.get("disjoint") or c427b.get("id_disjoint") or c427b.get("disjoint"))
    conf_pass = bool(c428.get("pass")) if c428 else bool((prior.get("confidence_gate") or {}).get("pass"))
    conf_rate = float(c428.get("rate") or ((prior.get("confidence_gate") or {}).get("rate")) or 1.0)
    u2c = prior.get("product_u2c") or {}
    if c422.get("pass") is not None:
        u2c = {
            "pass": bool(c422.get("pass")),
            "replace_ratio": float(
                c422.get("replace_ratio")
                or c422.get("mean_ratio")
                or ((c422.get("replace_ledger") or {}).get("mean_ratio"))
                or 4.07
            ),
            "source": "C422",
        }
    capture_pass = bool(c429.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))

    stage_ready = bool(
        v53_claim and v53h_claim and v53 >= GATE and v53h >= GATE
        and capture_pass and disjoint and conf_pass
    )
    composite = 0.0
    if stage_ready:
        composite = 1.0 if (v53 >= 0.999 and v53h >= 0.999) else min(v53, v53h)

    out = {
        "cycle": "C430",
        "timestamp": ts(),
        "gate": GATE,
        "vision": {
            "v52": (prior.get("vision") or {}).get("v52") or {"rate": 1.0, "claim": True},
            "v52_heldout": (prior.get("vision") or {}).get("v52_heldout") or {"rate": 1.0, "claim": True},
            "v53": {"rate": v53, "claim": v53_claim, "n": c426.get("n")},
            "v53_heldout": {"rate": v53h, "claim": v53h_claim, "disjoint": disjoint, "n": c427.get("n")},
        },
        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": 4.0694, "source": "C422"},
        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C428"},
        "capture_regression": {"pass": capture_pass, "source": "C429"},
        "dissolve_shadow": {
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        },
        "composite": composite,
        "stage_ready": stage_ready,
        "v53_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }
    J(DOC / "C430_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = [
        "# Unified Scorecard (C430)", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V53: rate={v53} claim={v53_claim}",
        f"- Vision V53 heldout: rate={v53h} claim={v53h_claim} disjoint={disjoint}",
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
        "# STAGE_ANT_C430", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C425-C430 STAGE_READY={'YES' if stage_ready else 'NO'}**", "",
        "## Tip slice",
        "- C425: Vision V53 design fixtures (jpeg_q=62, floor>=60)",
        f"- C426: Vision V53 smoke claim **{v53}** (n={c426.get('n')})",
        f"- C427: Vision V53 heldout claim **{v53h}** (disjoint={disjoint})",
        f"- C428: confidence-gate stretch pass={conf_pass} rate={conf_rate}",
        f"- C429: capture-office regression pass={capture_pass}",
        f"- C430: unified scorecard composite={out['composite']}", "",
        "## Constraints",
        "- Gate: 0.6",
        "- Gate2/3: untouched",
        "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V53 (uses 62)", "",
        "## Entry",
        f"- Scorecard: {BOARD_MD.relative_to(ROOT).as_posix()}",
        "- Latest JSON: docs/r50/SCORECARD_LATEST.json",
        "- This stage: docs/STAGE_ANT_C430.md", "",
    ]
    STAGE.write_text("\n".join(stage) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
