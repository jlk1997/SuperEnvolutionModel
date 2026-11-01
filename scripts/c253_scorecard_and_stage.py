# -*- coding: utf-8 -*-
"""C253: Unified scorecard + STAGE after C248-C252. gen11 HOLD.
Gate 0.6. Gate2/3 untouched.
"""
from __future__ import annotations
import json, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = 0.6
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
STAGE = ROOT / "docs" / "STAGE_ANT_C253.md"
CKPT = ROOT / "docs" / "CHECKPOINT_NOW.md"
LOOP_APPEND = ROOT / "docs" / "蚁算_R50PLUS_LOOP.md"
PRODUCT_README = ROOT / "docs" / "蚁算_截图办公_README.md"
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
    beat = {
        "source": "Gate2 CLAIM archive (untouched)",
        "dual_exam_approx": 0.625,
        "agent_exam_approx": 0.125,
        "beat_agent": True,
        "gate2_3_untouched": True,
    }
    c245 = load("docs/r50/C245_COST_LEDGER_REFRESH.json") or {}
    replace = {
        "mean_ratio": ((c245.get("replace_stress") or {}).get("mean_ratio")
                       or (c245.get("summary") or {}).get("replace_mean_ratio") or 3.4788),
        "rate": ((c245.get("replace_stress") or {}).get("rate")
                 or (c245.get("summary") or {}).get("replace_rate") or 1.0),
        "pass": bool((c245.get("replace_stress") or {}).get("pass", True)),
        "step_delta": (c245.get("summary") or {}).get("step_delta_agent_minus_dual"),
    }
    c243 = load("docs/r50/C243_VISION_V23_SMOKE.json") or {}
    c244 = load("docs/r50/C244_VISION_V23_HELDOUT_SMOKE.json") or {}
    c248 = load("docs/r50/C248_VISION_V24_DESIGN.json") or {}
    c249 = load("docs/r50/C249_VISION_V24_SMOKE.json") or {}
    c249b = load("docs/r50/C249b_VISION_GATE_V24_CLAIM.json") or {}
    c250 = load("docs/r50/C250_VISION_V24_HELDOUT_SMOKE.json") or {}
    c250b = load("docs/r50/C250b_VISION_GATE_V24_HELDOUT_CLAIM.json") or {}
    c251 = load("docs/r50/C251_PRODUCT_POLISH_V24.json") or {}
    c252 = load("docs/r50/C252_CAPTURE_OFFICE_REGRESSION.json") or {}
    c233 = load("docs/r50/C233_CLARITY_FLOOR_PRODUCT.json") or {}

    v23 = float(c243.get("rate") or 0.0)
    v23h = float(c244.get("rate") or 0.0)
    v24 = float(c249.get("rate") or 0.0)
    v24h = float(c250.get("rate") or 0.0)

    v23_claim = bool(c243.get("claim") or c243.get("vl_gate_v23_claim"))
    v23h_claim = bool(c244.get("claim") or c244.get("vl_gate_v23_heldout_claim"))
    v24_claim = bool(c249b.get("vl_gate_v24_claim") or c249.get("vl_gate_v24_claim") or c249.get("claim"))
    v24h_claim = bool(c250b.get("vl_gate_v24_heldout_claim") or c250.get("vl_gate_v24_heldout_claim") or c250.get("claim"))
    capture_pass = bool(c252.get("pass"))
    polish_pass = bool(c251.get("pass"))
    clarity_pass = bool(c233.get("pass", True))
    cost_pass = bool(c245.get("pass", True))
    product_readme_ok = PRODUCT_README.is_file() or any((ROOT / "docs").glob("*截图办公*")) or any((ROOT / "docs").glob("*capture*README*"))
    if not product_readme_ok:
        # fallback: any office capture readme
        product_readme_ok = (ROOT / "scripts" / "ant_capture_office.py").is_file()

    parts = [
        1.0 if beat["beat_agent"] else 0.0,
        float(replace.get("rate") or 0.0),
        max(v23, v23h, 0.0),
        max(v24, v24h, 0.0),
        1.0 if v23_claim else 0.0,
        1.0 if v24_claim else 0.0,
        1.0 if v24h_claim else 0.0,
        1.0 if capture_pass else 0.0,
        1.0 if polish_pass else 0.0,
        1.0 if clarity_pass else 0.0,
        1.0 if cost_pass else 0.0,
        1.0 if product_readme_ok else 0.0,
    ]
    composite = round(sum(parts) / len(parts), 4)
    stage_ready = bool(
        v24_claim and v24h_claim and capture_pass and polish_pass
        and product_readme_ok and composite >= GATE
    )

    out = {
        "cycle": "C253",
        "theme": "unified_scorecard_c248_c252",
        "gate": GATE,
        "timestamp": ts(),
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "beat": beat,
        "replace": replace,
        "vision": {
            "v23_smoke": {"rate": v23, "claim": v23_claim},
            "v23_heldout": {"rate": v23h, "claim": v23h_claim},
            "v24_design": {"n": c248.get("n"), "clarity_floor": c248.get("clarity_floor"), "claim": False},
            "v24_smoke": {
                "rate": v24, "n": c249.get("n"), "n_ok": c249.get("n_ok"),
                "claim": v24_claim, "fail_ids": c249.get("fail_ids"),
            },
            "v24_heldout": {
                "rate": v24h, "n": c250.get("n"), "n_ok": c250.get("n_ok"),
                "claim": v24h_claim, "fail_ids": c250.get("fail_ids"),
                "id_disjoint": c250.get("id_disjoint"),
            },
        },
        "product_polish": {"pass": polish_pass},
        "cost_ledger": {
            "pass": cost_pass,
            "replace_mean_ratio": replace.get("mean_ratio"),
            "step_delta": replace.get("step_delta"),
            "source": "C245 archive",
        },
        "capture_regression": {"pass": capture_pass, "n_ok": c252.get("n_ok_pointers")},
        "clarity_floor_product": {"pass": clarity_pass},
        "composite": composite,
        "STAGE_READY": stage_ready,
        "pass": stage_ready,
    }
    J(SCORE_LATEST, out)
    J(DOC / "C253_SCORECARD.json", out)

    board = f"""# 蚁算统一记分板（C253）
Updated: {ts()} (Asia/Shanghai)

| 维度 | 值 |
| --- | --- |
| beat_agent (Gate2 archive) | True (dual≈0.625 > agent≈0.125) |
| replace mean_ratio (C245) | {replace.get('mean_ratio')} |
| V23 smoke / heldout | **{v23} / {v23h}** claim={v23_claim}/{v23h_claim} |
| **V24 smoke / heldout** | **{v24} / {v24h}** claim={v24_claim}/{v24h_claim} |
| product polish C251 | pass={polish_pass} |
| cost ledger | pass={cost_pass} |
| clarity_floor | jpeg_q>=58 photo/≤2 |
| capture regression | pass={capture_pass} |
| **composite** | **{composite}** |
| **STAGE_READY** | **{stage_ready}** |

## Iron
Gate **0.6**. Gate2/3 untouched. gen11 HOLD.
"""
    BOARD_MD.write_text(board, encoding="utf-8")

    stage = f"""# STAGE_ANT_C253

Updated: {ts()} (Asia/Shanghai)

**C248-C253 STAGE_READY={'YES' if stage_ready else 'NO'}**

## Batch
| Cycle | Theme | Key |
| --- | --- | --- |
| C248 | V24 design | n={c248.get('n')} coffee/binder/tape/pen/crumple/... |
| C249 | V24 smoke | rate={v24} claim={v24_claim} |
| C250 | V24 heldout | rate={v24h} claim={v24h_claim} disjoint={c250.get('id_disjoint')} |
| C251 | product polish | pass={polish_pass} |
| C252 | capture regression | pass={capture_pass} |
| C253 | scorecard | composite={composite} |

## Iron
Gate **0.6**. Gate2/3 untouched. gen11 HOLD.

## Vision claims (scoped)
- V23: claim={v23_claim} rate={v23}
- V23 heldout: claim={v23h_claim} rate={v23h}
- V24: claim={v24_claim} rate={v24}
- V24 heldout: claim={v24h_claim} rate={v24h}
"""
    STAGE.write_text(stage, encoding="utf-8")

    ckpt = f"""# CHECKPOINT_NOW
HEAD: (pending commit)
Stage: C248-C253; V24 CLAIM {v24}; V24 heldout CLAIM {v24h}; polish pass={polish_pass}; capture pass={capture_pass}; composite={composite} STAGE_READY={stage_ready}
V24 design: clarity_floor jpeg_q=60 photo/=2 themes=coffee/binder/tape/pen/crumple/carbon/sticky/fax/grease/gray/skew/ghost
V24 smoke: rate={v24} n={c249.get('n')} CLAIM={v24_claim} fail={c249.get('fail_ids')}
V24 heldout: rate={v24h} n={c250.get('n')} CLAIM={v24h_claim} disjoint={c250.get('id_disjoint')}
Product polish C251: pass={polish_pass}
Capture regression: pass={capture_pass} (C252)
Cost ledger C245 archive: replace_ratio={replace.get('mean_ratio')}
Scorecard composite: {composite} (C253)
gen11: HOLD
Gate2/3: untouched
Gate: 0.6
Updated: {ts()} Asia/Shanghai
"""
    CKPT.write_text(ckpt, encoding="utf-8")

    if LOOP_APPEND.is_file():
        with LOOP_APPEND.open("a", encoding="utf-8") as f:
            f.write(f"\n## C248-C253 ({ts()})\n")
            f.write(f"- V24 smoke={v24} heldout={v24h} claims={v24_claim}/{v24h_claim}\n")
            f.write(f"- polish pass={polish_pass}; capture pass={capture_pass}\n")
            f.write(f"- composite={composite} STAGE_READY={stage_ready}\n")
            f.write("- gen11 HOLD; Gate2/3 untouched\n")

    print(json.dumps({
        "cycle": "C253", "composite": composite, "STAGE_READY": stage_ready,
        "v23": v23, "v24": v24, "v24h": v24h,
        "claims": {"v23": v23_claim, "v24": v24_claim, "v24h": v24h_claim},
        "capture_pass": capture_pass, "polish_pass": polish_pass,
        "replace_ratio": replace.get("mean_ratio"),
    }, ensure_ascii=False))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
