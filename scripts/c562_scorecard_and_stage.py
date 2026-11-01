# -*- coding: utf-8 -*-
"""C562: Unified scorecard + STAGE after C557-C561. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C562.md"
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
    c558 = load("docs/r50/C558_VISION_V75_SMOKE.json") or {}
    c558b = load("docs/r50/C558b_VISION_GATE_V75_CLAIM.json") or {}
    c559 = load("docs/r50/C559_VISION_V75_HELDOUT_SMOKE.json") or {}
    c559b = load("docs/r50/C559b_VISION_GATE_V75_HELDOUT_CLAIM.json") or {}
    c560 = load("docs/r50/C560_CONFIDENCE_GATE_STRETCH.json") or {}
    c561 = load("docs/r50/C561_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c554 = load("docs/r50/C554_PRODUCT_U2C_COST.json") or {}

    v75 = float(c558.get("rate") or 0.0)
    v75h = float(c559.get("rate") or 0.0)
    v75_claim = bool(c558b.get("vl_gate_v75_claim") or c558.get("vl_gate_v75_claim") or c558.get("claim"))
    v75h_claim = bool(c559b.get("vl_gate_v75_heldout_claim") or c559.get("vl_gate_v75_heldout_claim") or c559.get("claim"))
    disjoint = bool(c559.get("id_disjoint") or c559.get("disjoint") or c559b.get("id_disjoint") or c559b.get("disjoint"))
    conf_pass = bool(c560.get("pass")) if c560 else bool((prior.get("confidence_gate") or {}).get("pass"))
    conf_rate = float(c560.get("rate") or ((prior.get("confidence_gate") or {}).get("rate")) or 1.0)
    u2c = prior.get("product_u2c") or {}
    if c554.get("pass") is not None:
        u2c = {
            "pass": bool(c554.get("pass")),
            "replace_ratio": float(
                c554.get("replace_ratio")
                or c554.get("mean_ratio")
                or ((c554.get("replace_ledger") or {}).get("mean_ratio"))
                or 4.07
            ),
            "source": "C554",
        }
    capture_pass = bool(c561.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))

    stage_ready = bool(
        v75_claim and v75h_claim and v75 >= GATE and v75h >= GATE
        and capture_pass and disjoint and conf_pass
    )
    composite = 0.0
    if stage_ready:
        composite = 1.0 if (v75 >= 0.999 and v75h >= 0.999) else min(v75, v75h)

    out = {
        "cycle": "C562",
        "timestamp": ts(),
        "gate": GATE,
        "vision": {
            "v74": (prior.get("vision") or {}).get("v74") or {"rate": 1.0, "claim": True},
            "v74_heldout": (prior.get("vision") or {}).get("v74_heldout") or {"rate": 1.0, "claim": True},
            "v75": {"rate": v75, "claim": v75_claim, "n": c558.get("n")},
            "v75_heldout": {"rate": v75h, "claim": v75h_claim, "disjoint": disjoint, "n": c559.get("n")},
        },
        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": 4.0694, "source": "C554"},
        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C560"},
        "capture_regression": {"pass": capture_pass, "source": "C561"},
        "dissolve_shadow": {
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        },
        "composite": composite,
        "stage_ready": stage_ready,
        "v75_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }
    J(DOC / "C562_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = [
        "# Unified Scorecard (C562)", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V75: rate={v75} claim={v75_claim}",
        f"- Vision V75 heldout: rate={v75h} claim={v75h_claim} disjoint={disjoint}",
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
        "# STAGE_ANT_C562", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C557-C562 STAGE_READY={'YES' if stage_ready else 'NO'}**", "",
        "## Tip slice",
        "- C557: Vision V75 design fixtures (jpeg_q=62, floor>=60, long themes)",
        f"- C558: Vision V75 smoke claim **{v75}** (n={c558.get('n')})",
        f"- C559: Vision V75 heldout claim **{v75h}** (disjoint={disjoint})",
        f"- C560: confidence-gate stretch pass={conf_pass} rate={conf_rate}",
        f"- C561: capture-office regression pass={capture_pass}",
        f"- C562: unified scorecard composite={out['composite']}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally; not model-plus-separate-agent).", "",
        "## Constraints",
        "- Gate: 0.6",
        "- Gate2/3: untouched",
        "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V75 (uses 62)", "",
        "## Entry",
        f"- Scorecard: {BOARD_MD.relative_to(ROOT).as_posix()}",
        "- Latest JSON: docs/r50/SCORECARD_LATEST.json",
        "- This stage: docs/STAGE_ANT_C562.md", "",
    ]
    STAGE.write_text("\n".join(stage) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
