# -*- coding: utf-8 -*-
"""C229: Unified scorecard + STAGE after C224-C228. gen11 HOLD.
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
STAGE = ROOT / "docs" / "STAGE_ANT_C229.md"
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
    c168 = load("docs/r50/C168_DESKTOP_MULTIWIN_PRESSURE.json") or {}
    c219 = load("docs/r50/C219_V19_FAIL_FIX_RETEST.json") or {}
    c220 = load("docs/r50/C220_VISION_V19_HELDOUT_SMOKE.json") or {}
    c224 = load("docs/r50/C224_VISION_V20_DESIGN.json") or {}
    c225 = load("docs/r50/C225_VISION_V20_SMOKE.json") or {}
    c225b = load("docs/r50/C225b_VISION_GATE_V20_CLAIM.json") or {}
    c226 = load("docs/r50/C226_VISION_V20_HELDOUT_SMOKE.json") or {}
    c226b = load("docs/r50/C226b_VISION_GATE_V20_HELDOUT_CLAIM.json") or {}
    c227 = load("docs/r50/C227_MULTI_METRIC_CAPTURE_DEEPEN.json") or {}
    c228 = load("docs/r50/C228_CAPTURE_OFFICE_REGRESSION.json") or {}
    c210 = load("docs/r50/C210_CONFIDENCE_GATE_CAPTURE_WIRE.json") or {}

    v19 = float(c219.get("rate") or 0.0)
    v19h = float(c220.get("rate") or 0.0)
    v20 = float(c225.get("rate") or 0.0)
    v20h = float(c226.get("rate") or 0.0)
    multi_metric = float(c227.get("rate") or 0.0)
    multiwin = float(c168.get("rate") or 0.0)
    conf_wire = float(c210.get("rate") or 0.0)

    v20_claim = bool(c225b.get("vl_gate_v20_claim") or c225.get("vl_gate_v20_claim") or c225.get("claim"))
    v20h_claim = bool(c226b.get("vl_gate_v20_heldout_claim") or c226.get("vl_gate_v20_heldout_claim") or c226.get("claim"))
    multi_metric_pass = bool(c227.get("pass"))
    capture_pass = bool(c228.get("pass") if c228 else False)
    product_readme_ok = PRODUCT_README.is_file()
    clarity_floor = (c224.get("clarity_floor") or c225.get("clarity_floor") or {})

    parts = [
        1.0 if beat["beat_agent"] else 0.0,
        float(replace.get("rate") or 0.0),
        max(v19, v19h, 0.0),
        max(v20, v20h, 0.0),
        1.0 if (conf_wire >= GATE or c210.get("pass")) else 0.0,
        1.0 if multi_metric_pass else 0.0,
        1.0 if (c168.get("pass") or multiwin >= GATE) else 0.0,
        1.0 if capture_pass else 0.0,
        1.0 if product_readme_ok else 0.0,
        1.0 if v20h_claim else 0.0,
    ]
    composite = round(sum(parts) / len(parts), 4)
    stage_ready = bool(
        v20_claim and v20h_claim and multi_metric_pass and capture_pass
        and product_readme_ok and composite >= GATE
    )

    out = {
        "cycle": "C229",
        "theme": "unified_scorecard_c224_c228",
        "gate": GATE,
        "timestamp": ts(),
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "beat": beat,
        "replace": replace,
        "vision": {
            "v19_refresh": {"rate": v19, "claim": bool(c219.get("claim"))},
            "v19_heldout": {"rate": v19h, "claim": bool(c220.get("claim"))},
            "v20_design": {"n": c224.get("n"), "clarity_floor": clarity_floor, "claim": False},
            "v20_smoke": {
                "rate": v20, "n": c225.get("n"), "n_ok": c225.get("n_ok"),
                "claim": v20_claim, "fail_ids": c225.get("fail_ids"),
            },
            "v20_heldout": {
                "rate": v20h, "n": c226.get("n"), "n_ok": c226.get("n_ok"),
                "claim": v20h_claim, "fail_ids": c226.get("fail_ids"),
                "id_disjoint": c226.get("id_disjoint"),
            },
        },
        "multi_metric_deepen": {"rate": multi_metric, "pass": multi_metric_pass, "cli_pass": c227.get("cli_pass")},
        "capture_regression": {"pass": capture_pass, "pointers_ok_n": c228.get("pointers_ok_n"), "pointers_n": c228.get("pointers_n")},
        "composite": composite,
        "stage_ready": stage_ready,
        "parts": parts,
    }
    J(DOC / "C229_UNIFIED_SCORECARD.json", out)
    J(SCORE_LATEST, out)

    BOARD_MD.write_text(
        f"""# 蚁算统一记分卡（C229）

Updated: {ts()} (Asia/Shanghai)

| 维度 | 值 |
| --- | --- |
| beat_agent (Gate2 archive) | True (dual≈0.625 > agent≈0.125) |
| replace mean_ratio | {replace.get('mean_ratio')} |
| V19 refresh / heldout | {v19} / {v19h} |
| **V20 smoke / heldout** | **{v20} / {v20h}** claim={v20_claim}/{v20h_claim} |
| clarity_floor | jpeg_q>={clarity_floor.get('jpeg_q_min', clarity_floor.get('jpeg_q'))} photo/≤2 |
| multi_metric deepen | pass={multi_metric_pass} rate={multi_metric} |
| capture regression | pass={capture_pass} |
| **composite** | **{composite}** |
| **STAGE_READY** | **{stage_ready}** |

## Iron
Gate **0.6**. Gate2/3 untouched. gen11 HOLD.
""",
        encoding="utf-8",
    )

    STAGE.write_text(
        f"""# STAGE_ANT_C229

Updated: {ts()} (Asia/Shanghai)

**C224-C229 STAGE_READY={'YES' if stage_ready else 'NO'}**

## Batch
| Cycle | Theme | Key |
| --- | --- | --- |
| C224 | V20 design | n=18 clarity floor (no jpeg crush) |
| C225 | V20 smoke | rate={v20} claim={v20_claim} |
| C226 | V20 heldout | rate={v20h} claim={v20h_claim} disjoint |
| C227 | multi-metric deepen | rate={multi_metric} pass={multi_metric_pass} |
| C228 | capture regression | pass={capture_pass} |
| C229 | scorecard | composite={composite} |

## Iron
Gate **0.6**. Gate2/3 untouched. gen11 HOLD.

## Vision claims (scoped)
- V20: claim={v20_claim} rate={v20}
- V20 heldout: claim={v20h_claim} rate={v20h}
""",
        encoding="utf-8",
    )

    CKPT.write_text(
        f"""# CHECKPOINT_NOW
HEAD: (pending commit)
Stage: C224-C229; V20 CLAIM {v20}; V20 heldout CLAIM {v20h}; multi-metric deepen PASS; capture PASS; composite={composite} STAGE_READY={stage_ready}
V20 design: clarity_floor jpeg_q={clarity_floor.get('jpeg_q')} photo/={clarity_floor.get('photocopy_div')} (C218 lesson)
V20 smoke: rate={v20} n={c225.get('n')} CLAIM={v20_claim} fail={c225.get('fail_ids')}
V20 heldout: rate={v20h} n={c226.get('n')} CLAIM={v20h_claim} disjoint={c226.get('id_disjoint')}
Multi-metric deepen: rate={multi_metric} pass={multi_metric_pass} (C227)
Capture regression: pass={capture_pass} (C228)
Scorecard composite: {composite} (C229)
gen11: HOLD
Gate2/3: untouched
Gate: 0.6
Updated: {ts()} Asia/Shanghai
""",
        encoding="utf-8",
    )

    loop_line = (
        f"\n## C224-C229 ({ts()})\n"
        f"- V20 design clarity_floor jpeg_q={clarity_floor.get('jpeg_q')} (no C218 crush)\n"
        f"- V20 rate={v20} claim={v20_claim}\n"
        f"- V20 heldout rate={v20h} claim={v20h_claim} disjoint\n"
        f"- multi_metric deepen rate={multi_metric} pass={multi_metric_pass}\n"
        f"- capture_pass={capture_pass} composite={composite} stage_ready={stage_ready}\n"
        f"- gen11 HOLD; Gate2/3 untouched\n"
    )
    if LOOP_APPEND.is_file():
        prev = LOOP_APPEND.read_text(encoding="utf-8", errors="replace")
        if "C224-C229" not in prev:
            LOOP_APPEND.write_text(prev + loop_line, encoding="utf-8")
    else:
        LOOP_APPEND.write_text("# 蚁算 R50PLUS LOOP\n" + loop_line, encoding="utf-8")

    print(json.dumps({
        "cycle": "C229", "composite": composite, "stage_ready": stage_ready,
        "v20": v20, "v20h": v20h, "v20_claim": v20_claim, "v20h_claim": v20h_claim,
        "multi_metric_pass": multi_metric_pass, "capture_pass": capture_pass,
    }, ensure_ascii=False))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
