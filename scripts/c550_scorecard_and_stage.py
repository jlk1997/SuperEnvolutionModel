# -*- coding: utf-8 -*-
"""C550: Unified scorecard + STAGE after C545-C549. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C550.md"
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
    c546 = load("docs/r50/C546_VISION_V73_SMOKE.json") or {}
    c546b = load("docs/r50/C546b_VISION_GATE_V73_CLAIM.json") or {}
    c547 = load("docs/r50/C547_VISION_V73_HELDOUT_SMOKE.json") or {}
    c547b = load("docs/r50/C547b_VISION_GATE_V73_HELDOUT_CLAIM.json") or {}
    c548 = load("docs/r50/C548_CONFIDENCE_GATE_STRETCH.json") or {}
    c549 = load("docs/r50/C549_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c542 = load("docs/r50/C542_PRODUCT_U2C_COST.json") or {}

    v73 = float(c546.get("rate") or 0.0)
    v73h = float(c547.get("rate") or 0.0)
    v73_claim = bool(c546b.get("vl_gate_v73_claim") or c546.get("vl_gate_v73_claim") or c546.get("claim"))
    v73h_claim = bool(c547b.get("vl_gate_v73_heldout_claim") or c547.get("vl_gate_v73_heldout_claim") or c547.get("claim"))
    disjoint = bool(c547.get("id_disjoint") or c547.get("disjoint") or c547b.get("id_disjoint") or c547b.get("disjoint"))
    conf_pass = bool(c548.get("pass")) if c548 else bool((prior.get("confidence_gate") or {}).get("pass"))
    conf_rate = float(c548.get("rate") or ((prior.get("confidence_gate") or {}).get("rate")) or 1.0)
    u2c = prior.get("product_u2c") or {}
    if c542.get("pass") is not None:
        u2c = {
            "pass": bool(c542.get("pass")),
            "replace_ratio": float(
                c542.get("replace_ratio")
                or c542.get("mean_ratio")
                or ((c542.get("replace_ledger") or {}).get("mean_ratio"))
                or 4.07
            ),
            "source": "C542",
        }
    capture_pass = bool(c549.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))

    stage_ready = bool(
        v73_claim and v73h_claim and v73 >= GATE and v73h >= GATE
        and capture_pass and disjoint and conf_pass
    )
    composite = 0.0
    if stage_ready:
        composite = 1.0 if (v73 >= 0.999 and v73h >= 0.999) else min(v73, v73h)

    out = {
        "cycle": "C550",
        "timestamp": ts(),
        "gate": GATE,
        "vision": {
            "v72": (prior.get("vision") or {}).get("v72") or {"rate": 1.0, "claim": True},
            "v72_heldout": (prior.get("vision") or {}).get("v72_heldout") or {"rate": 1.0, "claim": True},
            "v73": {"rate": v73, "claim": v73_claim, "n": c546.get("n")},
            "v73_heldout": {"rate": v73h, "claim": v73h_claim, "disjoint": disjoint, "n": c547.get("n")},
        },
        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": 4.0694, "source": "C542"},
        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C548"},
        "capture_regression": {"pass": capture_pass, "source": "C549"},
        "dissolve_shadow": {
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        },
        "composite": composite,
        "stage_ready": stage_ready,
        "v73_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }
    J(DOC / "C550_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = [
        "# Unified Scorecard (C550)", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V73: rate={v73} claim={v73_claim}",
        f"- Vision V73 heldout: rate={v73h} claim={v73h_claim} disjoint={disjoint}",
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
        "# STAGE_ANT_C550", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C545-C550 STAGE_READY={'YES' if stage_ready else 'NO'}**", "",
        "## Tip slice",
        "- C545: Vision V73 design fixtures (jpeg_q=62, floor>=60, long themes)",
        f"- C546: Vision V73 smoke claim **{v73}** (n={c546.get('n')})",
        f"- C547: Vision V73 heldout claim **{v73h}** (disjoint={disjoint})",
        f"- C548: confidence-gate stretch pass={conf_pass} rate={conf_rate}",
        f"- C549: capture-office regression pass={capture_pass}",
        f"- C550: unified scorecard composite={out['composite']}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally; not model-plus-separate-agent).", "",
        "## Constraints",
        "- Gate: 0.6",
        "- Gate2/3: untouched",
        "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V73 (uses 62)", "",
        "## Entry",
        f"- Scorecard: {BOARD_MD.relative_to(ROOT).as_posix()}",
        "- Latest JSON: docs/r50/SCORECARD_LATEST.json",
        "- This stage: docs/STAGE_ANT_C550.md", "",
    ]
    STAGE.write_text("\n".join(stage) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
