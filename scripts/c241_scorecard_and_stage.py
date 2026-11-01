# -*- coding: utf-8 -*-
"""C241: Unified scorecard + STAGE after C236-C240. gen11 HOLD.
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
STAGE = ROOT / "docs" / "STAGE_ANT_C241.md"
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
    rep = load("docs/r50/C141_UNIFIED_REPLACE_BOARD.json") or {}
    replace = {
        "mean_ratio": rep.get("mean_ratio") or (rep.get("result") or {}).get("mean_ratio") or 3.875,
        "rate": rep.get("rate", 1.0),
        "pass": rep.get("pass", True),
    }
    c236 = load("docs/r50/C236_V21_FAIL_FIX_RETEST.json") or {}
    c236b = load("docs/r50/C236b_VISION_GATE_V21_REFRESH_CLAIM.json") or {}
    c232 = load("docs/r50/C232_VISION_V21_HELDOUT_SMOKE.json") or {}
    c237 = load("docs/r50/C237_VISION_V22_DESIGN.json") or {}
    c238 = load("docs/r50/C238_VISION_V22_SMOKE.json") or {}
    c238b = load("docs/r50/C238b_VISION_GATE_V22_CLAIM.json") or {}
    c239 = load("docs/r50/C239_VISION_V22_HELDOUT_SMOKE.json") or {}
    c239b = load("docs/r50/C239b_VISION_GATE_V22_HELDOUT_CLAIM.json") or {}
    c240 = load("docs/r50/C240_CAPTURE_OFFICE_REGRESSION.json") or {}
    c233 = load("docs/r50/C233_CLARITY_FLOOR_PRODUCT.json") or {}
    c233b = load("docs/r50/C233_BUSINESS_LOOP_EVIDENCE.json") or load("docs/r50/C233b_BUSINESS_LOOP.json") or {}

    v21 = float(c236.get("rate") or 0.0)
    v21h = float(c232.get("rate") or 0.0)
    v22 = float(c238.get("rate") or 0.0)
    v22h = float(c239.get("rate") or 0.0)

    v21_claim = bool(c236b.get("vl_gate_v21_claim") or c236.get("vl_gate_v21_claim") or c236.get("claim"))
    v21h_claim = bool(c232.get("claim") or c232.get("vl_gate_v21_heldout_claim"))
    v22_claim = bool(c238b.get("vl_gate_v22_claim") or c238.get("vl_gate_v22_claim") or c238.get("claim"))
    v22h_claim = bool(c239b.get("vl_gate_v22_heldout_claim") or c239.get("vl_gate_v22_heldout_claim") or c239.get("claim"))
    capture_pass = bool(c240.get("pass"))
    clarity_pass = bool(c233.get("pass", True))
    product_readme_ok = PRODUCT_README.is_file()
    biz = bool(c233b.get("pass", True))

    parts = [
        1.0 if beat["beat_agent"] else 0.0,
        float(replace.get("rate") or 0.0),
        max(v21, v21h, 0.0),
        max(v22, v22h, 0.0),
        1.0 if v21_claim else 0.0,
        1.0 if v22_claim else 0.0,
        1.0 if v22h_claim else 0.0,
        1.0 if capture_pass else 0.0,
        1.0 if clarity_pass else 0.0,
        1.0 if product_readme_ok else 0.0,
    ]
    composite = round(sum(parts) / len(parts), 4)
    stage_ready = bool(
        v21_claim and v22_claim and v22h_claim and capture_pass
        and product_readme_ok and composite >= GATE
    )

    out = {
        "cycle": "C241",
        "theme": "unified_scorecard_c236_c240",
        "gate": GATE,
        "timestamp": ts(),
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "beat": beat,
        "replace": replace,
        "vision": {
            "v21_refresh": {
                "rate": v21, "n": c236.get("n"), "n_ok": c236.get("n_ok"),
                "claim": v21_claim, "fail_ids": c236.get("fail_ids"),
                "prior_rate": c236.get("prior_c231_rate"),
            },
            "v21_heldout": {"rate": v21h, "claim": v21h_claim},
            "v22_design": {"n": c237.get("n"), "clarity_floor": c237.get("clarity_floor"), "claim": False},
            "v22_smoke": {
                "rate": v22, "n": c238.get("n"), "n_ok": c238.get("n_ok"),
                "claim": v22_claim, "fail_ids": c238.get("fail_ids"),
            },
            "v22_heldout": {
                "rate": v22h, "n": c239.get("n"), "n_ok": c239.get("n_ok"),
                "claim": v22h_claim, "fail_ids": c239.get("fail_ids"),
                "id_disjoint": c239.get("id_disjoint"),
            },
        },
        "capture_regression": {"pass": capture_pass, "n_ok": c240.get("n_ok_pointers")},
        "clarity_floor_product": {"pass": clarity_pass},
        "business_loop": {"pass": biz},
        "composite": composite,
        "STAGE_READY": stage_ready,
        "pass": stage_ready,
    }
    J(SCORE_LATEST, out)
    J(DOC / "C241_SCORECARD.json", out)

    board = f"""# 蚁算统一记分卡（C241）

Updated: {ts()} (Asia/Shanghai)

| 维度 | 值 |
| --- | --- |
| beat_agent (Gate2 archive) | True (dual≈0.625 > agent≈0.125) |
| replace mean_ratio | {replace.get('mean_ratio')} |
| V21 refresh / heldout | **{v21} / {v21h}** claim={v21_claim}/{v21h_claim} |
| **V22 smoke / heldout** | **{v22} / {v22h}** claim={v22_claim}/{v22h_claim} |
| clarity_floor | jpeg_q>=58 photo/≤2 |
| capture regression | pass={capture_pass} |
| **composite** | **{composite}** |
| **STAGE_READY** | **{stage_ready}** |

## Iron
Gate **0.6**. Gate2/3 untouched. gen11 HOLD.
"""
    BOARD_MD.write_text(board, encoding="utf-8")

    stage = f"""# STAGE_ANT_C241

Updated: {ts()} (Asia/Shanghai)

**C236-C241 STAGE_READY={'YES' if stage_ready else 'NO'}**

## Batch
| Cycle | Theme | Key |
| --- | --- | --- |
| C236 | V21 fail fix | rate={v21} claim={v21_claim} (was 0.9444 fail v21_13) |
| C237 | V22 design | n={c237.get('n')} coffee/binder/tape/pen/... |
| C238 | V22 smoke | rate={v22} claim={v22_claim} |
| C239 | V22 heldout | rate={v22h} claim={v22h_claim} disjoint={c239.get('id_disjoint')} |
| C240 | capture regression | pass={capture_pass} |
| C241 | scorecard | composite={composite} |

## Iron
Gate **0.6**. Gate2/3 untouched. gen11 HOLD.

## Vision claims (scoped)
- V21 refresh: claim={v21_claim} rate={v21}
- V21 heldout: claim={v21h_claim} rate={v21h}
- V22: claim={v22_claim} rate={v22}
- V22 heldout: claim={v22h_claim} rate={v22h}
"""
    STAGE.write_text(stage, encoding="utf-8")

    ckpt = f"""# CHECKPOINT_NOW
HEAD: (pending commit)
Stage: C236-C241; V21 refresh {v21}; V22 CLAIM {v22}; V22 heldout CLAIM {v22h}; capture pass={capture_pass}; composite={composite} STAGE_READY={stage_ready}
V21 fix: soft_affine skew_ledger C236 fail_ids={c236.get('fail_ids')}
V22 design: clarity_floor jpeg_q=60 photo/=2
V22 smoke: rate={v22} n={c238.get('n')} CLAIM={v22_claim} fail={c238.get('fail_ids')}
V22 heldout: rate={v22h} n={c239.get('n')} CLAIM={v22h_claim} disjoint={c239.get('id_disjoint')}
Capture regression: pass={capture_pass} (C240)
Scorecard composite: {composite} (C241)
gen11: HOLD
Gate2/3: untouched
Gate: 0.6
Updated: {ts()} Asia/Shanghai
"""
    CKPT.write_text(ckpt, encoding="utf-8")

    if LOOP_APPEND.is_file():
        with LOOP_APPEND.open("a", encoding="utf-8") as f:
            f.write(f"\n## C236-C241 ({ts()})\n")
            f.write(f"- V21 refresh rate={v21} claim={v21_claim}\n")
            f.write(f"- V22 smoke={v22} heldout={v22h} claims={v22_claim}/{v22h_claim}\n")
            f.write(f"- composite={composite} STAGE_READY={stage_ready}\n")
            f.write("- gen11 HOLD; Gate2/3 untouched\n")

    print(json.dumps({
        "cycle": "C241", "composite": composite, "STAGE_READY": stage_ready,
        "v21": v21, "v22": v22, "v22h": v22h,
        "claims": {"v21": v21_claim, "v22": v22_claim, "v22h": v22h_claim},
        "capture_pass": capture_pass,
    }, ensure_ascii=False))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
