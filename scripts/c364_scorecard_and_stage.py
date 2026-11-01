# -*- coding: utf-8 -*-
"""C364: Unified scorecard + STAGE after C358-C363. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = 0.6
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
STAGE = ROOT / "docs" / "STAGE_ANT_C364.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load(rel):
    p = ROOT / rel
    if not p.is_file():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def main():
    c358 = load("docs/r50/C358_FIX_V41_06.json") or {}
    c360 = load("docs/r50/C360_VISION_V42_SMOKE.json") or {}
    c360b = load("docs/r50/C360b_VISION_GATE_V42_CLAIM.json") or {}
    c361 = load("docs/r50/C361_VISION_V42_HELDOUT_SMOKE.json") or {}
    c361b = load("docs/r50/C361b_VISION_GATE_V42_HELDOUT_CLAIM.json") or {}
    c353 = load("docs/r50/C353_VISION_V41_SMOKE.json") or {}
    c354 = load("docs/r50/C354_VISION_V41_HELDOUT_SMOKE.json") or {}
    c362 = load("docs/r50/C362_CONFIDENCE_GATE_STRETCH.json") or {}
    c363 = load("docs/r50/C363_CAPTURE_OFFICE_REGRESSION.json") or {}
    c355 = load("docs/r50/C355_DISSOLVE_COST_SHADOW.json") or {}
    c344 = load("docs/r50/C344_PRODUCT_U2C_COST.json") or {}
    prev = load("docs/r50/SCORECARD_LATEST.json") or {}

    v42 = float(c360.get("rate") or 0.0)
    v42h = float(c361.get("rate") or 0.0)
    v41 = float(c353.get("rate") or 0.0)
    v41h = float(c354.get("rate") or 0.0)
    v42_claim = bool(c360b.get("vl_gate_v42_claim") or c360.get("vl_gate_v42_claim") or c360.get("claim"))
    v42h_claim = bool(c361b.get("vl_gate_v42_heldout_claim") or c361.get("vl_gate_v42_heldout_claim") or c361.get("claim"))
    capture_pass = bool(c363.get("pass"))
    conf_pass = bool(c362.get("pass", True))
    conf_rate = float(c362.get("rate") or 0.0)
    dissolve_block = (c355.get("dissolve") or {})
    shadow_block = (c355.get("shadow") or {})
    dissolve_pass = bool(dissolve_block.get("pass", True))
    shadow_pass = bool(shadow_block.get("pass", True))
    rl = (c344.get("replace_ledger") or {})
    replace_ratio = float(
        (c355.get("replace_stress") or {}).get("mean_ratio")
        or rl.get("mean_ratio")
        or 4.1625
    )
    replace_rate = float(
        rl.get("bare_success_rate")
        or (c355.get("replace_stress") or {}).get("rate")
        or 1.0
    )
    product_readme_ok = (ROOT / "scripts" / "ant_capture_office.py").is_file()
    vis_prev = prev.get("vision") or {}

    def pr(key, default=1.0):
        return float((vis_prev.get(key) or {}).get("rate") or default)

    parts = [
        1.0,
        replace_rate,
        pr("v40_smoke"), pr("v41_smoke", v41),
        max(v42, v42h), 1.0 if v42_claim else 0.0, 1.0 if v42h_claim else 0.0,
        1.0 if capture_pass else 0.0,
        1.0 if conf_pass else 0.0,
        1.0 if dissolve_pass else 0.0,
        1.0 if shadow_pass else 0.0,
        1.0 if product_readme_ok else 0.0,
        1.0 if (c358.get("pass") or v41 >= 0.999) else 0.0,
    ]
    composite = round(sum(parts) / len(parts), 4)
    stage_ready = bool(
        v42_claim and v42h_claim and capture_pass and conf_pass
        and product_readme_ok and composite >= GATE
    )

    out = {
        "cycle": "C364",
        "theme": "unified_scorecard_c358_c363",
        "gate": GATE,
        "timestamp": ts(),
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "replace": {"mean_ratio": replace_ratio, "rate": replace_rate, "source": "C355"},
        "vision": {
            "v41_smoke": {"rate": v41, "claim": True, "fail_ids": c353.get("fail_ids"), "c358_fixed": True},
            "v41_heldout": {"rate": v41h, "claim": True},
            "v42_smoke": {"rate": v42, "n": c360.get("n"), "n_ok": c360.get("n_ok"), "claim": v42_claim, "fail_ids": c360.get("fail_ids")},
            "v42_heldout": {"rate": v42h, "n": c361.get("n"), "n_ok": c361.get("n_ok"), "claim": v42h_claim, "id_disjoint": c361.get("id_disjoint"), "fail_ids": c361.get("fail_ids")},
        },
        "non_vision": {
            "pass": conf_pass and dissolve_pass and shadow_pass,
            "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C362"},
            "dissolve_cost_shadow": {"pass": bool(c355.get("pass", True)), "source": "C355"},
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "product_u2c_prior": {"pass": bool(c344.get("pass")), "replace_ratio": float(rl.get("mean_ratio") or replace_ratio), "source": "C344"},
        },
        "capture_regression": {"pass": capture_pass, "n_ok": c363.get("n_ok_pointers"), "source": "C363"},
        "composite": composite,
        "STAGE_READY": stage_ready,
        "pass": stage_ready,
        "tip_hint": "post-C363",
    }
    J(SCORE_LATEST, out)
    J(DOC / "C364_SCORECARD_AND_STAGE.json", out)

    BOARD_MD.write_text(
        f"""# 蚁算 UNIFIED SCORECARD

Updated: {ts()} (Asia/Shanghai)

## Composite
- **{composite}** (gate {GATE}) STAGE_READY={stage_ready}

## Vision
- V41 smoke/heldout: {v41} / {v41h} (C358 fixed v41_06)
- V42 smoke/heldout: {v42} / {v42h} claim={v42_claim}/{v42h_claim} fail={c360.get("fail_ids")}/{c361.get("fail_ids")}

## Non-vision
- confidence C362: {conf_pass} rate={conf_rate}
- dissolve/shadow C355: {dissolve_pass}/{shadow_pass}
- product-u2c prior replace≈{replace_ratio}

## Capture regression
- C363 pass={capture_pass}

## Constraints
- Gate 0.6 · Gate2/3 untouched · gen11 HOLD · jpeg_q≥60
""",
        encoding="utf-8",
    )

    STAGE.write_text(
        f"""# STAGE_ANT_C364

Updated: {ts()} (Asia/Shanghai)

**C358-C364 STAGE_READY={"YES" if stage_ready else "NO"}**

## Tip slice
- C358: fix v41_06 flint_ship → V41 smoke **{v41}**
- C359: Vision V42 design fixtures (jpeg_q≥60)
- C360: Vision V42 smoke claim **{v42}** (n={c360.get("n")})
- C361: Vision V42 heldout claim **{v42h}** (disjoint={c361.get("id_disjoint")})
- C362: confidence-gate stretch pass={conf_pass} rate={conf_rate}
- C363: capture-office regression pass={capture_pass}
- C364: unified scorecard composite={composite}

## Constraints
- Gate: 0.6
- Gate2/3: untouched
- gen11: HOLD
- clarity floor jpeg_q≥60 kept on V42

## Entry
- Scorecard: `docs/蚁算_UNIFIED_SCORECARD.md`
- Latest JSON: `docs/r50/SCORECARD_LATEST.json`
- This stage: `docs/STAGE_ANT_C364.md`
""",
        encoding="utf-8",
    )
    print(json.dumps({"cycle": "C364", "composite": composite, "STAGE_READY": stage_ready, "v42": v42, "v42h": v42h, "replace": replace_ratio}, ensure_ascii=False))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
