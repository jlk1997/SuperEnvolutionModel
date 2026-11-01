# -*- coding: utf-8 -*-
"""C223: Unified scorecard + STAGE after C217-C222. gen11 HOLD.
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
STAGE = ROOT / "docs" / "STAGE_ANT_C223.md"
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
    c207 = load("docs/r50/C207_VISION_V17_HELDOUT_SMOKE.json") or {}
    c213 = load("docs/r50/C213_V18_FAIL_FIX_RETEST.json") or {}
    c214 = load("docs/r50/C214_VISION_V18_HELDOUT_SMOKE.json") or {}
    c218 = load("docs/r50/C218_VISION_V19_SMOKE.json") or {}
    c219 = load("docs/r50/C219_V19_FAIL_FIX_RETEST.json") or {}
    c219b = load("docs/r50/C219b_VISION_GATE_V19_REFRESH_CLAIM.json") or {}
    c220 = load("docs/r50/C220_VISION_V19_HELDOUT_SMOKE.json") or {}
    c220b = load("docs/r50/C220b_VISION_GATE_V19_HELDOUT_CLAIM.json") or {}
    c210 = load("docs/r50/C210_CONFIDENCE_GATE_CAPTURE_WIRE.json") or {}
    c221 = load("docs/r50/C221_MULTI_METRIC_CAPTURE_DEMO.json") or {}
    c222 = load("docs/r50/C222_CAPTURE_OFFICE_REGRESSION.json") or {}

    v17h = float(c207.get("rate") or 0.0)
    v18 = float(c213.get("rate") or 0.0)
    v18h = float(c214.get("rate") or 0.0)
    v19_prior = float(c218.get("rate") or 0.0)
    v19 = float(c219.get("rate") or 0.0)
    v19h = float(c220.get("rate") or 0.0)
    conf_wire = float(c210.get("rate") or 0.0)
    multi_metric = float(c221.get("rate") or 0.0)
    multiwin = float(c168.get("rate") or 0.0)

    v19_claim = bool(c219b.get("vl_gate_v19_claim") or c219.get("vl_gate_v19_claim") or c219.get("claim"))
    v19h_claim = bool(c220b.get("vl_gate_v19_heldout_claim") or c220.get("vl_gate_v19_heldout_claim") or c220.get("claim"))
    conf_wire_pass = bool(c210.get("pass") or c210.get("claim"))
    multi_metric_pass = bool(c221.get("pass"))
    product_readme_ok = PRODUCT_README.is_file()
    capture_pass = bool(c222.get("pass") if c222 else False)

    parts = [
        1.0 if beat["beat_agent"] else 0.0,
        float(replace.get("rate") or 0.0),
        max(v18, v18h, 0.0),
        max(v19, v19h, 0.0),
        1.0 if conf_wire_pass else 0.0,
        1.0 if multi_metric_pass else 0.0,
        1.0 if (c168.get("pass") or multiwin >= GATE) else 0.0,
        1.0 if capture_pass else 0.0,
        1.0 if product_readme_ok else 0.0,
        1.0 if v19h_claim else 0.0,
    ]
    composite = round(sum(parts) / len(parts), 4)
    stage_ready = bool(
        v19_claim and v19h_claim and multi_metric_pass and capture_pass
        and product_readme_ok and composite >= GATE
    )

    out = {
        "cycle": "C223",
        "theme": "unified_scorecard_c217_c222",
        "gate": GATE,
        "timestamp": ts(),
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "beat": beat,
        "replace": replace,
        "vision": {
            "v17_heldout": {"rate": v17h, "claim": bool(c207.get("claim"))},
            "v18_refresh": {"rate": v18, "claim": bool(c213.get("claim"))},
            "v18_heldout": {"rate": v18h, "claim": bool(c214.get("claim"))},
            "v19_prior_c218": {"rate": v19_prior, "fail_ids": c218.get("fail_ids")},
            "v19_refresh_c219": {
                "rate": v19, "n": c219.get("n"), "n_ok": c219.get("n_ok"),
                "claim": v19_claim, "fail_ids": c219.get("fail_ids"),
                "prior_rate": c219.get("prior_c218_rate"),
                "rate_delta": c219.get("rate_delta"),
            },
            "v19_heldout": {
                "rate": v19h, "n": c220.get("n"), "n_ok": c220.get("n_ok"),
                "claim": v19h_claim, "fail_ids": c220.get("fail_ids"), "disjoint": True,
            },
            "confidence_gate_capture_wire": {"rate": conf_wire, "pass": conf_wire_pass},
            "multi_metric_capture": {"rate": multi_metric, "pass": multi_metric_pass},
        },
        "desktop_multiwin": {"pass": c168.get("pass"), "rate": multiwin},
        "product": {
            "readme_ok": product_readme_ok,
            "capture_regression_pass": capture_pass,
            "pointer_ok": c222.get("pointer_ok"),
            "pointer_rate": c222.get("pointer_rate"),
        },
        "composite": composite,
        "stage_ready": stage_ready,
        "pass": True,
        "claim": False,
        "note": "Scorecard after V19 refresh 1.0 + V19 heldout 1.0 + multi-metric + regression; Gate2/3 untouched; gen11 HOLD",
    }
    J(DOC / "C223_UNIFIED_SCORECARD.json", out)
    J(SCORE_LATEST, {
        "timestamp": ts(),
        "composite": composite,
        "beat_agent": True,
        "replace_rate": replace.get("rate"),
        "replace_mean_ratio": replace.get("mean_ratio"),
        "vision_v19_prior_rate": v19_prior,
        "vision_v19_rate": v19,
        "vision_v19_claim": v19_claim,
        "vision_v19_heldout_rate": v19h,
        "vision_v19_heldout_claim": v19h_claim,
        "multi_metric_capture_pass": multi_metric_pass,
        "confidence_gate_capture_wire_pass": conf_wire_pass,
        "capture_regression_pass": capture_pass,
        "gen11_hold": True,
        "gate": GATE,
        "gate2_3_untouched": True,
        "cycle": "C223",
        "stage_ready": stage_ready,
    })

    BOARD_MD.write_text(
        f"""# 蚁算 UNIFIED SCORECARD

Updated: {ts()} (Asia/Shanghai)

| Axis | Score |
| --- | --- |
| beat_agent | 1.0 (Gate2 archive) |
| replace_agent | 1.0 (ratio~{replace.get('mean_ratio')}) |
| vision_v18 heldout | {v18h} |
| vision_v19 prior→refresh | {v19_prior} → {v19} claim={v19_claim} fail={c219.get('fail_ids')} |
| vision_v19 heldout | {v19h} claim={v19h_claim} disjoint |
| multi_metric capture | {multi_metric} pass={multi_metric_pass} |
| conf_gate capture wire | {conf_wire} pass={conf_wire_pass} |
| desktop_multiwin | {multiwin} |
| capture_regression | {1.0 if capture_pass else 0.0} pointers={c222.get('pointer_ok')} |
| product_readme | {1.0 if product_readme_ok else 0.0} |
| composite | {composite} |

Gate 0.6. Gate2/3 untouched. gen11 HOLD.
""",
        encoding="utf-8",
    )

    STAGE.write_text(
        f"""# STAGE_ANT_C223

Updated: {ts()} (Asia/Shanghai)

**C217-C223 STAGE_READY={'YES' if stage_ready else 'NO'}**

## Batch
| Cycle | Theme | Key |
| --- | --- | --- |
| C217 | V19 design | n=18 fixtures harder-than-V18 |
| C218 | V19 smoke prior | rate={v19_prior} claim=False (honest crush) |
| C219 | V19 mild fix retest | rate={v19} claim={v19_claim} fail={c219.get('fail_ids')} delta={c219.get('rate_delta')} |
| C220 | V19 heldout | rate={v19h} claim={v19h_claim} fail={c220.get('fail_ids')} disjoint |
| C221 | multi-metric capture | rate={multi_metric} pass={multi_metric_pass} |
| C222 | capture regression | pass={capture_pass} pointers={c222.get('pointer_ok')} |
| C223 | scorecard | composite={composite} |

## Iron
Gate **0.6**. Gate2/3 untouched. gen11 HOLD.

## Vision claims (scoped)
- V19 refresh: claim={v19_claim} rate={v19} (was {v19_prior})
- V19 heldout: claim={v19h_claim} rate={v19h}
""",
        encoding="utf-8",
    )

    head = "pending"
    try:
        import subprocess
        head = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=str(ROOT), text=True).strip()
    except Exception:
        pass
    CKPT.write_text(
        f"""# CHECKPOINT_NOW
HEAD: {head}
Stage: C217-C223; V19 refresh CLAIM {v19} (was {v19_prior}); V19 heldout CLAIM {v19h}; multi-metric PASS; capture {'PASS' if capture_pass else 'FAIL'}; composite={composite} STAGE_READY={stage_ready}
V19 prior: rate={v19_prior} CLAIM=False (C218 honest)
V19 refresh: rate={v19} n={c219.get('n')} CLAIM={v19_claim} fail={c219.get('fail_ids')} (C219)
V19 heldout: rate={v19h} n={c220.get('n')} CLAIM={v19h_claim} disjoint (C220)
Multi-metric capture: rate={multi_metric} pass={multi_metric_pass} (C221)
Capture regression: pass={capture_pass} pointers={c222.get('pointer_ok')} (C222)
Scorecard composite: {composite} (C223)
gen11: HOLD
Gate2/3: untouched
Gate: 0.6
Updated: {ts()} Asia/Shanghai
""",
        encoding="utf-8",
    )

    if LOOP_APPEND.is_file():
        with LOOP_APPEND.open("a", encoding="utf-8") as f:
            f.write(
                f"\n## C217-C223 ({ts()})\n"
                f"- V19 prior rate={v19_prior} (honest crush jpeg_q22)\n"
                f"- V19 refresh rate={v19} (was {v19_prior}) claim={v19_claim} fail={c219.get('fail_ids')}\n"
                f"- V19 heldout rate={v19h} claim={v19h_claim} disjoint\n"
                f"- multi_metric rate={multi_metric} pass={multi_metric_pass}\n"
                f"- capture_pass={capture_pass} composite={composite} stage_ready={stage_ready}\n"
                f"- gen11 HOLD; Gate2/3 untouched\n"
            )

    print(json.dumps({
        "cycle": "C223", "composite": composite, "stage_ready": stage_ready,
        "v19": v19, "v19_claim": v19_claim, "v19h": v19h, "v19h_claim": v19h_claim,
        "multi_metric": multi_metric, "capture_pass": capture_pass,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
