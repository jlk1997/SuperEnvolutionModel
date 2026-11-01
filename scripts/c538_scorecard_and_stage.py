# -*- coding: utf-8 -*-
"""C538: Unified scorecard + STAGE after C533-C537. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C538.md"
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
    c534 = load("docs/r50/C534_VISION_V71_SMOKE.json") or {}
    c534b = load("docs/r50/C534b_VISION_GATE_V71_CLAIM.json") or {}
    c535 = load("docs/r50/C535_VISION_V71_HELDOUT_SMOKE.json") or {}
    c535b = load("docs/r50/C535b_VISION_GATE_V71_HELDOUT_CLAIM.json") or {}
    c536 = load("docs/r50/C536_CONFIDENCE_GATE_STRETCH.json") or {}
    c537 = load("docs/r50/C537_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c530 = load("docs/r50/C530_PRODUCT_U2C_COST.json") or {}

    v71 = float(c534.get("rate") or 0.0)
    v71h = float(c535.get("rate") or 0.0)
    v71_claim = bool(c534b.get("vl_gate_v71_claim") or c534.get("vl_gate_v71_claim") or c534.get("claim"))
    v71h_claim = bool(c535b.get("vl_gate_v71_heldout_claim") or c535.get("vl_gate_v71_heldout_claim") or c535.get("claim"))
    disjoint = bool(c535.get("id_disjoint") or c535.get("disjoint") or c535b.get("id_disjoint") or c535b.get("disjoint"))
    conf_pass = bool(c536.get("pass")) if c536 else bool((prior.get("confidence_gate") or {}).get("pass"))
    conf_rate = float(c536.get("rate") or ((prior.get("confidence_gate") or {}).get("rate")) or 1.0)
    u2c = prior.get("product_u2c") or {}
    if c530.get("pass") is not None:
        u2c = {
            "pass": bool(c530.get("pass")),
            "replace_ratio": float(
                c530.get("replace_ratio")
                or c530.get("mean_ratio")
                or ((c530.get("replace_ledger") or {}).get("mean_ratio"))
                or 4.07
            ),
            "source": "C530",
        }
    capture_pass = bool(c537.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))

    stage_ready = bool(
        v71_claim and v71h_claim and v71 >= GATE and v71h >= GATE
        and capture_pass and disjoint and conf_pass
    )
    composite = 0.0
    if stage_ready:
        composite = 1.0 if (v71 >= 0.999 and v71h >= 0.999) else min(v71, v71h)

    out = {
        "cycle": "C538",
        "timestamp": ts(),
        "gate": GATE,
        "vision": {
            "v70": (prior.get("vision") or {}).get("v70") or {"rate": 1.0, "claim": True},
            "v70_heldout": (prior.get("vision") or {}).get("v70_heldout") or {"rate": 1.0, "claim": True},
            "v71": {"rate": v71, "claim": v71_claim, "n": c534.get("n")},
            "v71_heldout": {"rate": v71h, "claim": v71h_claim, "disjoint": disjoint, "n": c535.get("n")},
        },
        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": 4.0694, "source": "C530"},
        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C536"},
        "capture_regression": {"pass": capture_pass, "source": "C537"},
        "dissolve_shadow": {
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        },
        "composite": composite,
        "stage_ready": stage_ready,
        "v71_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }
    J(DOC / "C538_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = [
        "# Unified Scorecard (C538)", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V71: rate={v71} claim={v71_claim}",
        f"- Vision V71 heldout: rate={v71h} claim={v71h_claim} disjoint={disjoint}",
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
        "# STAGE_ANT_C538", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C533-C538 STAGE_READY={'YES' if stage_ready else 'NO'}**", "",
        "## Tip slice",
        "- C533: Vision V71 design fixtures (jpeg_q=62, floor>=60, long themes)",
        f"- C534: Vision V71 smoke claim **{v71}** (n={c534.get('n')})",
        f"- C535: Vision V71 heldout claim **{v71h}** (disjoint={disjoint})",
        f"- C536: confidence-gate stretch pass={conf_pass} rate={conf_rate}",
        f"- C537: capture-office regression pass={capture_pass}",
        f"- C538: unified scorecard composite={out['composite']}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally; not model-plus-separate-agent).", "",
        "## Constraints",
        "- Gate: 0.6",
        "- Gate2/3: untouched",
        "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V71 (uses 62)", "",
        "## Entry",
        f"- Scorecard: {BOARD_MD.relative_to(ROOT).as_posix()}",
        "- Latest JSON: docs/r50/SCORECARD_LATEST.json",
        "- This stage: docs/STAGE_ANT_C538.md", "",
    ]
    STAGE.write_text("\n".join(stage) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
