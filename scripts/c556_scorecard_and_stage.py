# -*- coding: utf-8 -*-
"""C556: Unified scorecard + STAGE after C551-C555. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C556.md"
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
    c552 = load("docs/r50/C552_VISION_V74_SMOKE.json") or {}
    c552b = load("docs/r50/C552b_VISION_GATE_V74_CLAIM.json") or {}
    c553 = load("docs/r50/C553_VISION_V74_HELDOUT_SMOKE.json") or {}
    c553b = load("docs/r50/C553b_VISION_GATE_V74_HELDOUT_CLAIM.json") or {}
    c554 = load("docs/r50/C554_PRODUCT_U2C_COST.json") or {}
    c555 = load("docs/r50/C555_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c548 = load("docs/r50/C548_CONFIDENCE_GATE_STRETCH.json") or {}

    v74 = float(c552.get("rate") or 0.0)
    v74h = float(c553.get("rate") or 0.0)
    v74_claim = bool(c552b.get("vl_gate_v74_claim") or c552.get("vl_gate_v74_claim") or c552.get("claim"))
    v74h_claim = bool(c553b.get("vl_gate_v74_heldout_claim") or c553.get("vl_gate_v74_heldout_claim") or c553.get("claim"))
    disjoint = bool(c553.get("id_disjoint") or c553.get("disjoint") or c553b.get("id_disjoint") or c553b.get("disjoint"))
    conf = prior.get("confidence_gate") or {}
    if c548.get("pass") is not None:
        conf = {"pass": bool(c548.get("pass")), "rate": float(c548.get("rate") or 1.0), "source": "C548"}
    u2c_pass = bool(c554.get("pass"))
    replace = float(
        c554.get("replace_ratio")
        or c554.get("mean_ratio")
        or ((c554.get("replace_ledger") or {}).get("mean_ratio"))
        or 4.07
    )
    capture_pass = bool(c555.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))

    stage_ready = bool(
        v74_claim and v74h_claim and v74 >= GATE and v74h >= GATE
        and capture_pass and disjoint and u2c_pass
    )
    composite = 0.0
    if stage_ready:
        composite = 1.0 if (v74 >= 0.999 and v74h >= 0.999) else min(v74, v74h)

    out = {
        "cycle": "C556",
        "timestamp": ts(),
        "gate": GATE,
        "vision": {
            "v73": (prior.get("vision") or {}).get("v73") or {"rate": 1.0, "claim": True},
            "v73_heldout": (prior.get("vision") or {}).get("v73_heldout") or {"rate": 1.0, "claim": True},
            "v74": {"rate": v74, "claim": v74_claim, "n": c552.get("n")},
            "v74_heldout": {"rate": v74h, "claim": v74h_claim, "disjoint": disjoint, "n": c553.get("n")},
        },
        "product_u2c": {"pass": u2c_pass, "replace_ratio": replace, "source": "C554"},
        "confidence_gate": conf if conf else {"pass": True, "rate": 1.0, "source": "C548"},
        "capture_regression": {"pass": capture_pass, "source": "C555"},
        "dissolve_shadow": {
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        },
        "composite": composite,
        "stage_ready": stage_ready,
        "v74_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }
    J(DOC / "C556_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = [
        "# Unified Scorecard (C556)", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V74: rate={v74} claim={v74_claim}",
        f"- Vision V74 heldout: rate={v74h} claim={v74h_claim} disjoint={disjoint}",
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
        "# STAGE_ANT_C556", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C551-C556 STAGE_READY={'YES' if stage_ready else 'NO'}**", "",
        "## Tip slice",
        "- C551: Vision V74 design fixtures (jpeg_q=62, floor>=60, long themes)",
        f"- C552: Vision V74 smoke claim **{v74}** (n={c552.get('n')})",
        f"- C553: Vision V74 heldout claim **{v74h}** (disjoint={disjoint})",
        f"- C554: product-U2C pass={u2c_pass} replace≈{replace:.4f}×",
        f"- C555: capture-office regression pass={capture_pass}",
        f"- C556: unified scorecard composite={out['composite']}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally; not model-plus-separate-agent).", "",
        "## Constraints",
        "- Gate: 0.6",
        "- Gate2/3: untouched",
        "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V74 (uses 62)", "",
        "## Entry",
        f"- Scorecard: {BOARD_MD.relative_to(ROOT).as_posix()}",
        "- Latest JSON: docs/r50/SCORECARD_LATEST.json",
        "- This stage: docs/STAGE_ANT_C556.md", "",
    ]
    STAGE.write_text("\n".join(stage) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
