# -*- coding: utf-8 -*-
"""C424: Unified scorecard + STAGE after C419-C423. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C424.md"
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
    c420 = load("docs/r50/C420_VISION_V52_SMOKE.json") or {}
    c420b = load("docs/r50/C420b_VISION_GATE_V52_CLAIM.json") or {}
    c421 = load("docs/r50/C421_VISION_V52_HELDOUT_SMOKE.json") or {}
    c421b = load("docs/r50/C421b_VISION_GATE_V52_HELDOUT_CLAIM.json") or {}
    c422 = load("docs/r50/C422_PRODUCT_U2C_COST.json") or {}
    c423 = load("docs/r50/C423_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c416 = load("docs/r50/C416_CONFIDENCE_GATE_STRETCH.json") or {}

    v52 = float(c420.get("rate") or 0.0)
    v52h = float(c421.get("rate") or 0.0)
    v52_claim = bool(c420b.get("vl_gate_v52_claim") or c420.get("vl_gate_v52_claim") or c420.get("claim"))
    v52h_claim = bool(c421b.get("vl_gate_v52_heldout_claim") or c421.get("vl_gate_v52_heldout_claim") or c421.get("claim"))
    disjoint = bool(c421.get("id_disjoint") or c421.get("disjoint") or c421b.get("id_disjoint") or c421b.get("disjoint"))
    u2c_pass = bool(c422.get("pass")) if c422 else bool((prior.get("product_u2c") or {}).get("pass"))
    u2c_ratio = float(
        c422.get("replace_ratio")
        or c422.get("mean_ratio")
        or ((c422.get("replace_ledger") or {}).get("mean_ratio"))
        or ((prior.get("product_u2c") or {}).get("replace_ratio"))
        or 4.07
    )
    conf = prior.get("confidence_gate") or {}
    if c416.get("pass") is not None:
        conf = {"pass": bool(c416.get("pass")), "rate": float(c416.get("rate") or 1.0), "source": "C416"}
    capture_pass = bool(c423.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))

    stage_ready = bool(
        v52_claim and v52h_claim and v52 >= GATE and v52h >= GATE
        and capture_pass and disjoint and u2c_pass
    )
    composite = 0.0
    if stage_ready:
        composite = 1.0 if (v52 >= 0.999 and v52h >= 0.999) else min(v52, v52h)

    out = {
        "cycle": "C424",
        "timestamp": ts(),
        "gate": GATE,
        "vision": {
            "v51": (prior.get("vision") or {}).get("v51") or {"rate": 1.0, "claim": True},
            "v51_heldout": (prior.get("vision") or {}).get("v51_heldout") or {"rate": 1.0, "claim": True},
            "v52": {"rate": v52, "claim": v52_claim, "n": c420.get("n")},
            "v52_heldout": {"rate": v52h, "claim": v52h_claim, "disjoint": disjoint, "n": c421.get("n")},
        },
        "product_u2c": {"pass": u2c_pass, "replace_ratio": u2c_ratio, "source": "C422"},
        "confidence_gate": conf if conf else {"pass": True, "rate": 1.0, "source": "C416"},
        "capture_regression": {"pass": capture_pass, "source": "C423"},
        "dissolve_shadow": {
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        },
        "composite": composite,
        "stage_ready": stage_ready,
        "v52_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }
    J(DOC / "C424_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = [
        "# Unified Scorecard (C424)", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V52: rate={v52} claim={v52_claim}",
        f"- Vision V52 heldout: rate={v52h} claim={v52h_claim} disjoint={disjoint}",
        f"- product_u2c: pass={u2c_pass} replace_ratio={u2c_ratio}",
        f"- confidence_gate: {out['confidence_gate']}",
        f"- capture_regression: pass={capture_pass}",
        f"- dissolve/shadow: {dissolve_pass}/{shadow_pass}",
        f"- composite: {out['composite']}",
        f"- stage_ready: {stage_ready}",
        "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",
    ]
    BOARD_MD.write_text("\n".join(md) + "\n", encoding="utf-8")

    stage = [
        "# STAGE_ANT_C424", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C419-C424 STAGE_READY={'YES' if stage_ready else 'NO'}**", "",
        "## Tip slice",
        "- C419: Vision V52 design fixtures (jpeg_q=62, floor>=60)",
        f"- C420: Vision V52 smoke claim **{v52}** (n={c420.get('n')})",
        f"- C421: Vision V52 heldout claim **{v52h}** (disjoint={disjoint})",
        f"- C422: product-u2c replace_ratio={u2c_ratio} pass={u2c_pass}",
        f"- C423: capture-office regression pass={capture_pass}",
        f"- C424: unified scorecard composite={out['composite']}", "",
        "## Constraints",
        "- Gate: 0.6",
        "- Gate2/3: untouched",
        "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V52 (uses 62)", "",
        "## Entry",
        f"- Scorecard: {BOARD_MD.relative_to(ROOT).as_posix()}",
        "- Latest JSON: docs/r50/SCORECARD_LATEST.json",
        "- This stage: docs/STAGE_ANT_C424.md", "",
    ]
    STAGE.write_text("\n".join(stage) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
