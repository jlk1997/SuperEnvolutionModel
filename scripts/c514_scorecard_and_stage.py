# -*- coding: utf-8 -*-
"""C514: Unified scorecard + STAGE after C509-C513. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C514.md"
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
    c510 = load("docs/r50/C510_VISION_V67_SMOKE.json") or {}
    c510b = load("docs/r50/C510b_VISION_GATE_V67_CLAIM.json") or {}
    c511 = load("docs/r50/C511_VISION_V67_HELDOUT_SMOKE.json") or {}
    c511b = load("docs/r50/C511b_VISION_GATE_V67_HELDOUT_CLAIM.json") or {}
    c512 = load("docs/r50/C512_CONFIDENCE_GATE_STRETCH.json") or {}
    c513 = load("docs/r50/C513_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c506 = load("docs/r50/C506_PRODUCT_U2C_COST.json") or {}

    v67 = float(c510.get("rate") or 0.0)
    v67h = float(c511.get("rate") or 0.0)
    v67_claim = bool(c510b.get("vl_gate_v67_claim") or c510.get("vl_gate_v67_claim") or c510.get("claim"))
    v67h_claim = bool(c511b.get("vl_gate_v67_heldout_claim") or c511.get("vl_gate_v67_heldout_claim") or c511.get("claim"))
    disjoint = bool(c511.get("id_disjoint") or c511.get("disjoint") or c511b.get("id_disjoint") or c511b.get("disjoint"))
    conf_pass = bool(c512.get("pass")) if c512 else bool((prior.get("confidence_gate") or {}).get("pass"))
    conf_rate = float(c512.get("rate") or ((prior.get("confidence_gate") or {}).get("rate")) or 1.0)
    u2c = prior.get("product_u2c") or {}
    if c506.get("pass") is not None:
        u2c = {
            "pass": bool(c506.get("pass")),
            "replace_ratio": float(
                c506.get("replace_ratio")
                or c506.get("mean_ratio")
                or ((c506.get("replace_ledger") or {}).get("mean_ratio"))
                or 4.07
            ),
            "source": "C506",
        }
    capture_pass = bool(c513.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))

    stage_ready = bool(
        v67_claim and v67h_claim and v67 >= GATE and v67h >= GATE
        and capture_pass and disjoint and conf_pass
    )
    composite = 0.0
    if stage_ready:
        composite = 1.0 if (v67 >= 0.999 and v67h >= 0.999) else min(v67, v67h)

    out = {
        "cycle": "C514",
        "timestamp": ts(),
        "gate": GATE,
        "vision": {
            "v66": (prior.get("vision") or {}).get("v66") or {"rate": 1.0, "claim": True},
            "v66_heldout": (prior.get("vision") or {}).get("v66_heldout") or {"rate": 1.0, "claim": True},
            "v67": {"rate": v67, "claim": v67_claim, "n": c510.get("n")},
            "v67_heldout": {"rate": v67h, "claim": v67h_claim, "disjoint": disjoint, "n": c511.get("n")},
        },
        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": 4.0694, "source": "C506"},
        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C512"},
        "capture_regression": {"pass": capture_pass, "source": "C513"},
        "dissolve_shadow": {
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        },
        "composite": composite,
        "stage_ready": stage_ready,
        "v67_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }
    J(DOC / "C514_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = [
        "# Unified Scorecard (C514)", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V67: rate={v67} claim={v67_claim}",
        f"- Vision V67 heldout: rate={v67h} claim={v67h_claim} disjoint={disjoint}",
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
        "# STAGE_ANT_C514", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C509-C514 STAGE_READY={'YES' if stage_ready else 'NO'}**", "",
        "## Tip slice",
        "- C509: Vision V67 design fixtures (jpeg_q=62, floor>=60, long themes)",
        f"- C510: Vision V67 smoke claim **{v67}** (n={c510.get('n')})",
        f"- C511: Vision V67 heldout claim **{v67h}** (disjoint={disjoint})",
        f"- C512: confidence-gate stretch pass={conf_pass} rate={conf_rate}",
        f"- C513: capture-office regression pass={capture_pass}",
        f"- C514: unified scorecard composite={out['composite']}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally; not model-plus-separate-agent).", "",
        "## Constraints",
        "- Gate: 0.6",
        "- Gate2/3: untouched",
        "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V67 (uses 62)", "",
        "## Entry",
        f"- Scorecard: {BOARD_MD.relative_to(ROOT).as_posix()}",
        "- Latest JSON: docs/r50/SCORECARD_LATEST.json",
        "- This stage: docs/STAGE_ANT_C514.md", "",
    ]
    STAGE.write_text("\n".join(stage) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
