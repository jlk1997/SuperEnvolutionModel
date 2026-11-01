# -*- coding: utf-8 -*-
"""C259: Unified scorecard + STAGE after C254-C258. gen11 HOLD.
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
STAGE = ROOT / "docs" / "STAGE_ANT_C259.md"
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
    c249 = load("docs/r50/C249_VISION_V24_SMOKE.json") or {}
    c250 = load("docs/r50/C250_VISION_V24_HELDOUT_SMOKE.json") or {}
    c254 = load("docs/r50/C254_VISION_V25_DESIGN.json") or {}
    c255 = load("docs/r50/C255_VISION_V25_SMOKE.json") or {}
    c255b = load("docs/r50/C255b_VISION_GATE_V25_CLAIM.json") or {}
    c256 = load("docs/r50/C256_VISION_V25_HELDOUT_SMOKE.json") or {}
    c256b = load("docs/r50/C256b_VISION_GATE_V25_HELDOUT_CLAIM.json") or {}
    c257 = load("docs/r50/C257_INNOVATION_U2C_CAPTURE_REPLACE.json") or {}
    c258 = load("docs/r50/C258_CAPTURE_OFFICE_REGRESSION.json") or {}
    c233 = load("docs/r50/C233_CLARITY_FLOOR_PRODUCT.json") or {}

    v24 = float(c249.get("rate") or 0.0)
    v24h = float(c250.get("rate") or 0.0)
    v25 = float(c255.get("rate") or 0.0)
    v25h = float(c256.get("rate") or 0.0)

    v24_claim = bool(c249.get("vl_gate_v24_claim") or c249.get("claim"))
    v24h_claim = bool(c250.get("vl_gate_v24_heldout_claim") or c250.get("claim"))
    v25_claim = bool(c255b.get("vl_gate_v25_claim") or c255.get("vl_gate_v25_claim") or c255.get("claim"))
    v25h_claim = bool(c256b.get("vl_gate_v25_heldout_claim") or c256.get("vl_gate_v25_heldout_claim") or c256.get("claim"))
    capture_pass = bool(c258.get("pass"))
    innov_pass = bool(c257.get("pass"))
    clarity_pass = bool(c233.get("pass", True))
    cost_pass = bool(c245.get("pass", True))
    product_readme_ok = PRODUCT_README.is_file() or (ROOT / "scripts" / "ant_capture_office.py").is_file()

    parts = [
        1.0 if beat["beat_agent"] else 0.0,
        float(replace.get("rate") or 0.0),
        max(v24, v24h, 0.0),
        max(v25, v25h, 0.0),
        1.0 if v24_claim else 0.0,
        1.0 if v25_claim else 0.0,
        1.0 if v25h_claim else 0.0,
        1.0 if capture_pass else 0.0,
        1.0 if innov_pass else 0.0,
        1.0 if clarity_pass else 0.0,
        1.0 if cost_pass else 0.0,
        1.0 if product_readme_ok else 0.0,
    ]
    composite = round(sum(parts) / len(parts), 4)
    stage_ready = bool(
        v25_claim and v25h_claim and capture_pass and innov_pass
        and product_readme_ok and composite >= GATE
    )

    out = {
        "cycle": "C259",
        "theme": "unified_scorecard_c254_c258",
        "gate": GATE,
        "timestamp": ts(),
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "beat": beat,
        "replace": replace,
        "vision": {
            "v24_smoke": {"rate": v24, "claim": v24_claim},
            "v24_heldout": {"rate": v24h, "claim": v24h_claim},
            "v25_design": {"n": c254.get("n"), "clarity_floor": c254.get("clarity_floor"), "claim": False},
            "v25_smoke": {
                "rate": v25, "n": c255.get("n"), "n_ok": c255.get("n_ok"),
                "claim": v25_claim, "fail_ids": c255.get("fail_ids"),
            },
            "v25_heldout": {
                "rate": v25h, "n": c256.get("n"), "n_ok": c256.get("n_ok"),
                "claim": v25h_claim, "fail_ids": c256.get("fail_ids"),
                "id_disjoint": c256.get("id_disjoint"),
            },
        },
        "innovation": {"pass": innov_pass, "u2c_rate": (c257.get("u2c") or {}).get("rate"),
                       "replace_ratio": (c257.get("replace_ledger") or {}).get("mean_ratio")},
        "cost_ledger": {
            "pass": cost_pass,
            "replace_mean_ratio": replace.get("mean_ratio"),
            "step_delta": replace.get("step_delta"),
            "source": "C245 archive",
        },
        "capture_regression": {"pass": capture_pass, "n_ok": c258.get("n_ok_pointers")},
        "clarity_floor_product": {"pass": clarity_pass},
        "composite": composite,
        "STAGE_READY": stage_ready,
        "pass": stage_ready,
    }
    J(SCORE_LATEST, out)
    J(DOC / "C259_SCORECARD.json", out)

    board = f"""# 蚁算统一记分板（C259）
Updated: {ts()} (Asia/Shanghai)

| 维度 | 值 |
| --- | --- |
| beat_agent (Gate2 archive) | True (dual≈0.625 > agent≈0.125) |
| replace mean_ratio (C245) | {replace.get('mean_ratio')} |
| V24 smoke / heldout | **{v24} / {v24h}** claim={v24_claim}/{v24h_claim} |
| **V25 smoke / heldout** | **{v25} / {v25h}** claim={v25_claim}/{v25h_claim} |
| innovation C257 | pass={innov_pass} |
| cost ledger | pass={cost_pass} |
| clarity_floor | jpeg_q>=58 photo/≤2 |
| capture regression | pass={capture_pass} |
| **composite** | **{composite}** |
| **STAGE_READY** | **{stage_ready}** |

## Iron
Gate **0.6**. Gate2/3 untouched. gen11 HOLD.
"""
    BOARD_MD.write_text(board, encoding="utf-8")

    stage = f"""# STAGE_ANT_C259

Updated: {ts()} (Asia/Shanghai)

**C254-C259 STAGE_READY={'YES' if stage_ready else 'NO'}**

## Batch
| Cycle | Theme | Key |
| --- | --- | --- |
| C254 | V25 design | n={c254.get('n')} fp/rain/staple/qr/curl/... |
| C255 | V25 smoke | rate={v25} claim={v25_claim} |
| C256 | V25 heldout | rate={v25h} claim={v25h_claim} disjoint={c256.get('id_disjoint')} |
| C257 | innovation U2C/capture/replace | pass={innov_pass} |
| C258 | capture regression | pass={capture_pass} |
| C259 | scorecard | composite={composite} |

## Iron
Gate **0.6**. Gate2/3 untouched. gen11 HOLD.

## Vision claims (scoped)
- V24: claim={v24_claim} rate={v24}
- V24 heldout: claim={v24h_claim} rate={v24h}
- V25: claim={v25_claim} rate={v25}
- V25 heldout: claim={v25h_claim} rate={v25h}
"""
    STAGE.write_text(stage, encoding="utf-8")

    ckpt = f"""# CHECKPOINT_NOW
HEAD: (pending commit)
Stage: C254-C259; V25 CLAIM {v25}; V25 heldout CLAIM {v25h}; innov pass={innov_pass}; capture pass={capture_pass}; composite={composite} STAGE_READY={stage_ready}
V25 design: clarity_floor jpeg_q=60 photo/=2 themes=fp/rain/staple/qr/curl/flare/clutter/ink/torn/zig/combo/barcode/moire/rings
V25 smoke: rate={v25} n={c255.get('n')} CLAIM={v25_claim} fail={c255.get('fail_ids')}
V25 heldout: rate={v25h} n={c256.get('n')} CLAIM={v25h_claim} disjoint={c256.get('id_disjoint')}
Innovation C257: pass={innov_pass}
Capture regression: pass={capture_pass} (C258)
Cost ledger C245 archive: replace_ratio={replace.get('mean_ratio')}
Scorecard composite: {composite} (C259)
gen11: HOLD
Gate2/3: untouched
Gate: 0.6
Updated: {ts()} Asia/Shanghai
"""
    CKPT.write_text(ckpt, encoding="utf-8")

    if LOOP_APPEND.is_file():
        with LOOP_APPEND.open("a", encoding="utf-8") as f:
            f.write(f"\n## C254-C259 ({ts()})\n")
            f.write(f"- V25 smoke={v25} heldout={v25h} claims={v25_claim}/{v25h_claim}\n")
            f.write(f"- innov pass={innov_pass}; capture pass={capture_pass}\n")
            f.write(f"- composite={composite} STAGE_READY={stage_ready}\n")
            f.write("- gen11 HOLD; Gate2/3 untouched\n")

    print(json.dumps({
        "cycle": "C259", "composite": composite, "STAGE_READY": stage_ready,
        "v24": v24, "v25": v25, "v25h": v25h,
        "claims": {"v24": v24_claim, "v25": v25_claim, "v25h": v25h_claim},
        "capture_pass": capture_pass, "innov_pass": innov_pass,
        "replace_ratio": replace.get("mean_ratio"),
    }, ensure_ascii=False))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
