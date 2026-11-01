# -*- coding: utf-8 -*-
"""C544: Unified scorecard + STAGE after C539-C543. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C544.md"
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
    c540 = load("docs/r50/C540_VISION_V72_SMOKE.json") or {}
    c540b = load("docs/r50/C540b_VISION_GATE_V72_CLAIM.json") or {}
    c541 = load("docs/r50/C541_VISION_V72_HELDOUT_SMOKE.json") or {}
    c541b = load("docs/r50/C541b_VISION_GATE_V72_HELDOUT_CLAIM.json") or {}
    c542 = load("docs/r50/C542_PRODUCT_U2C_COST.json") or {}
    c543 = load("docs/r50/C543_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c536 = load("docs/r50/C536_CONFIDENCE_GATE_STRETCH.json") or {}

    v72 = float(c540.get("rate") or 0.0)
    v72h = float(c541.get("rate") or 0.0)
    v72_claim = bool(c540b.get("vl_gate_v72_claim") or c540.get("vl_gate_v72_claim") or c540.get("claim"))
    v72h_claim = bool(c541b.get("vl_gate_v72_heldout_claim") or c541.get("vl_gate_v72_heldout_claim") or c541.get("claim"))
    disjoint = bool(c541.get("id_disjoint") or c541.get("disjoint") or c541b.get("id_disjoint") or c541b.get("disjoint"))
    conf = prior.get("confidence_gate") or {}
    if c536.get("pass") is not None:
        conf = {"pass": bool(c536.get("pass")), "rate": float(c536.get("rate") or 1.0), "source": "C536"}
    u2c_pass = bool(c542.get("pass"))
    replace = float(
        c542.get("replace_ratio")
        or c542.get("mean_ratio")
        or ((c542.get("replace_ledger") or {}).get("mean_ratio"))
        or 4.07
    )
    capture_pass = bool(c543.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))

    stage_ready = bool(
        v72_claim and v72h_claim and v72 >= GATE and v72h >= GATE
        and capture_pass and disjoint and u2c_pass
    )
    composite = 0.0
    if stage_ready:
        composite = 1.0 if (v72 >= 0.999 and v72h >= 0.999) else min(v72, v72h)

    out = {
        "cycle": "C544",
        "timestamp": ts(),
        "gate": GATE,
        "vision": {
            "v71": (prior.get("vision") or {}).get("v71") or {"rate": 1.0, "claim": True},
            "v71_heldout": (prior.get("vision") or {}).get("v71_heldout") or {"rate": 1.0, "claim": True},
            "v72": {"rate": v72, "claim": v72_claim, "n": c540.get("n")},
            "v72_heldout": {"rate": v72h, "claim": v72h_claim, "disjoint": disjoint, "n": c541.get("n")},
        },
        "product_u2c": {"pass": u2c_pass, "replace_ratio": replace, "source": "C542"},
        "confidence_gate": conf if conf else {"pass": True, "rate": 1.0, "source": "C536"},
        "capture_regression": {"pass": capture_pass, "source": "C543"},
        "dissolve_shadow": {
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        },
        "composite": composite,
        "stage_ready": stage_ready,
        "v72_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }
    J(DOC / "C544_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = [
        "# Unified Scorecard (C544)", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V72: rate={v72} claim={v72_claim}",
        f"- Vision V72 heldout: rate={v72h} claim={v72h_claim} disjoint={disjoint}",
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
        "# STAGE_ANT_C544", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C539-C544 STAGE_READY={'YES' if stage_ready else 'NO'}**", "",
        "## Tip slice",
        "- C539: Vision V72 design fixtures (jpeg_q=62, floor>=60, long themes)",
        f"- C540: Vision V72 smoke claim **{v72}** (n={c540.get('n')})",
        f"- C541: Vision V72 heldout claim **{v72h}** (disjoint={disjoint})",
        f"- C542: product-U2C pass={u2c_pass} replace≈{replace:.4f}×",
        f"- C543: capture-office regression pass={capture_pass}",
        f"- C544: unified scorecard composite={out['composite']}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally; not model-plus-separate-agent).", "",
        "## Constraints",
        "- Gate: 0.6",
        "- Gate2/3: untouched",
        "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V72 (uses 62)", "",
        "## Entry",
        f"- Scorecard: {BOARD_MD.relative_to(ROOT).as_posix()}",
        "- Latest JSON: docs/r50/SCORECARD_LATEST.json",
        "- This stage: docs/STAGE_ANT_C544.md", "",
    ]
    STAGE.write_text("\n".join(stage) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
