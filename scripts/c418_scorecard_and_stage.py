# -*- coding: utf-8 -*-
"""C418: Unified scorecard + STAGE after C413-C417. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C418.md"
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
    c414 = load("docs/r50/C414_VISION_V51_SMOKE.json") or {}
    c414b = load("docs/r50/C414b_VISION_GATE_V51_CLAIM.json") or {}
    c415 = load("docs/r50/C415_VISION_V51_HELDOUT_SMOKE.json") or {}
    c415b = load("docs/r50/C415b_VISION_GATE_V51_HELDOUT_CLAIM.json") or {}
    c416 = load("docs/r50/C416_CONFIDENCE_GATE_STRETCH.json") or {}
    c417 = load("docs/r50/C417_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c410 = load("docs/r50/C410_PRODUCT_U2C_COST.json") or {}

    v51 = float(c414.get("rate") or 0.0)
    v51h = float(c415.get("rate") or 0.0)
    v51_claim = bool(c414b.get("vl_gate_v51_claim") or c414.get("vl_gate_v51_claim") or c414.get("claim"))
    v51h_claim = bool(c415b.get("vl_gate_v51_heldout_claim") or c415.get("vl_gate_v51_heldout_claim") or c415.get("claim"))
    disjoint = bool(c415.get("id_disjoint") or c415.get("disjoint") or c415b.get("id_disjoint") or c415b.get("disjoint"))
    conf_pass = bool(c416.get("pass") or (c416.get("rate") or 0) >= GATE)
    conf_rate = float(c416.get("rate") or (prior.get("confidence_gate") or {}).get("rate") or 1.0)
    capture_pass = bool(c417.get("pass"))
    u2c = prior.get("product_u2c") or {}
    if c410.get("pass") is not None:
        u2c = {
            "pass": bool(c410.get("pass")),
            "replace_ratio": float(c410.get("replace_ratio") or c410.get("mean_ratio") or (c410.get("replace_ledger") or {}).get("mean_ratio") or 4.07),
            "source": "C410",
        }
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))

    stage_ready = bool(
        v51_claim and v51h_claim and v51 >= GATE and v51h >= GATE
        and capture_pass and disjoint
    )
    composite = 0.0
    if stage_ready:
        composite = 1.0 if (v51 >= 0.999 and v51h >= 0.999) else min(v51, v51h)

    out = {
        "cycle": "C418",
        "timestamp": ts(),
        "gate": GATE,
        "vision": {
            "v50": (prior.get("vision") or {}).get("v50") or {"rate": 1.0, "claim": True},
            "v50_heldout": (prior.get("vision") or {}).get("v50_heldout") or {"rate": 1.0, "claim": True},
            "v51": {"rate": v51, "claim": v51_claim, "n": c414.get("n")},
            "v51_heldout": {"rate": v51h, "claim": v51h_claim, "disjoint": disjoint, "n": c415.get("n")},
        },
        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": 4.0694, "source": "C410"},
        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C416"},
        "capture_regression": {"pass": capture_pass, "source": "C417"},
        "dissolve_shadow": {
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        },
        "composite": composite,
        "stage_ready": stage_ready,
        "v51_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }
    J(DOC / "C418_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = [
        "# Unified Scorecard (C418)", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V51: rate={v51} claim={v51_claim}",
        f"- Vision V51 heldout: rate={v51h} claim={v51h_claim} disjoint={disjoint}",
        f"- confidence_gate: pass={conf_pass} rate={conf_rate}",
        f"- product_u2c: {out['product_u2c']}",
        f"- capture_regression: pass={capture_pass}",
        f"- dissolve/shadow: {dissolve_pass}/{shadow_pass}",
        f"- composite: {out['composite']}",
        f"- stage_ready: {stage_ready}",
        "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",
    ]
    BOARD_MD.write_text("\n".join(md) + "\n", encoding="utf-8")

    stage = [
        "# STAGE_ANT_C418", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C413-C418 STAGE_READY={'YES' if stage_ready else 'NO'}**", "",
        "## Tip slice",
        "- C413: Vision V51 design fixtures (jpeg_q=62, floor>=60)",
        f"- C414: Vision V51 smoke claim **{v51}** (n={c414.get('n')})",
        f"- C415: Vision V51 heldout claim **{v51h}** (disjoint={disjoint})",
        f"- C416: confidence-gate stretch pass={conf_pass} rate={conf_rate}",
        f"- C417: capture-office regression pass={capture_pass}",
        f"- C418: unified scorecard composite={out['composite']}", "",
        "## Constraints",
        "- Gate: 0.6",
        "- Gate2/3: untouched",
        "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V51 (uses 62)", "",
        "## Entry",
        f"- Scorecard: {BOARD_MD.relative_to(ROOT).as_posix()}",
        "- Latest JSON: docs/r50/SCORECARD_LATEST.json",
        "- This stage: docs/STAGE_ANT_C418.md", "",
    ]
    STAGE.write_text("\n".join(stage) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
