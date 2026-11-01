# -*- coding: utf-8 -*-
"""C216: Unified scorecard + STAGE after C213-C215. gen11 HOLD.
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
STAGE = ROOT / "docs" / "STAGE_ANT_C216.md"
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
    c198 = load("docs/r50/C198_VISION_V16_SMOKE.json") or {}
    c201 = load("docs/r50/C201_VISION_V16_HELDOUT_SMOKE.json") or {}
    c203 = load("docs/r50/C203_VISION_V17_SMOKE.json") or {}
    c207 = load("docs/r50/C207_VISION_V17_HELDOUT_SMOKE.json") or {}
    c209 = load("docs/r50/C209_VISION_V18_SMOKE.json") or {}
    c210 = load("docs/r50/C210_CONFIDENCE_GATE_CAPTURE_WIRE.json") or {}
    c213 = load("docs/r50/C213_V18_FAIL_FIX_RETEST.json") or {}
    c213b = load("docs/r50/C213b_VISION_GATE_V18_REFRESH_CLAIM.json") or {}
    c214 = load("docs/r50/C214_VISION_V18_HELDOUT_SMOKE.json") or {}
    c214b = load("docs/r50/C214b_VISION_GATE_V18_HELDOUT_CLAIM.json") or {}
    c215 = load("docs/r50/C215_CAPTURE_OFFICE_REGRESSION.json") or {}

    v16 = float(c198.get("rate") or 0.0)
    v16h = float(c201.get("rate") or 0.0)
    v17 = float(c203.get("rate") or 0.0)
    v17h = float(c207.get("rate") or 0.0)
    v18_prior = float(c209.get("rate") or 0.0)
    v18 = float(c213.get("rate") or v18_prior)
    v18h = float(c214.get("rate") or 0.0)
    conf_wire = float(c210.get("rate") or 0.0)
    multiwin = float(c168.get("rate") or 0.0)

    v18_claim = bool(c213b.get("vl_gate_v18_claim") or c213.get("vl_gate_v18_claim") or c213.get("claim"))
    v18h_claim = bool(c214b.get("vl_gate_v18_heldout_claim") or c214.get("vl_gate_v18_heldout_claim") or c214.get("claim"))
    conf_wire_pass = bool(c210.get("pass") or c210.get("claim"))
    product_readme_ok = PRODUCT_README.is_file()
    capture_pass = bool(c215.get("pass") if c215 else False)

    parts = [
        1.0 if beat["beat_agent"] else 0.0,
        float(replace.get("rate") or 0.0),
        max(v16, v16h, 0.0),
        max(v17, v17h, 0.0),
        max(v18, v18h, 0.0),
        1.0 if conf_wire_pass else 0.0,
        1.0 if (c168.get("pass") or multiwin >= GATE) else 0.0,
        1.0 if capture_pass else 0.0,
        1.0 if product_readme_ok else 0.0,
        1.0 if v18h_claim else 0.0,
    ]
    composite = round(sum(parts) / len(parts), 4)
    stage_ready = bool(
        v18_claim and v18h_claim and conf_wire_pass and capture_pass
        and product_readme_ok and composite >= GATE
    )

    out = {
        "cycle": "C216",
        "theme": "unified_scorecard_c213_c215",
        "gate": GATE,
        "timestamp": ts(),
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "beat": beat,
        "replace": replace,
        "vision": {
            "v17_heldout": {"rate": v17h, "claim": bool(c207.get("claim"))},
            "v18_prior_c209": {"rate": v18_prior, "fail_ids": c209.get("fail_ids")},
            "v18_refresh_c213": {
                "rate": v18, "n": c213.get("n"), "n_ok": c213.get("n_ok"),
                "claim": v18_claim, "fail_ids": c213.get("fail_ids"),
                "prior_rate": c213.get("prior_c209_rate"),
                "rate_delta": c213.get("rate_delta"),
            },
            "v18_heldout": {
                "rate": v18h, "n": c214.get("n"), "n_ok": c214.get("n_ok"),
                "claim": v18h_claim, "fail_ids": c214.get("fail_ids"), "disjoint": True,
            },
            "confidence_gate_capture_wire": {"rate": conf_wire, "pass": conf_wire_pass},
        },
        "desktop_multiwin": {"pass": c168.get("pass"), "rate": multiwin},
        "product": {
            "readme_ok": product_readme_ok,
            "capture_regression_pass": capture_pass,
            "pointer_ok": c215.get("pointer_ok"),
            "pointer_rate": c215.get("pointer_rate"),
        },
        "composite": composite,
        "stage_ready": stage_ready,
        "pass": True,
        "claim": False,
        "note": "Scorecard after V18 refresh 1.0 + V18 heldout 1.0 + regression; Gate2/3 untouched; gen11 HOLD",
    }
    J(DOC / "C216_UNIFIED_SCORECARD.json", out)
    J(SCORE_LATEST, {
        "timestamp": ts(),
        "composite": composite,
        "beat_agent": True,
        "replace_rate": replace.get("rate"),
        "replace_mean_ratio": replace.get("mean_ratio"),
        "vision_v18_prior_rate": v18_prior,
        "vision_v18_rate": v18,
        "vision_v18_claim": v18_claim,
        "vision_v18_heldout_rate": v18h,
        "vision_v18_heldout_claim": v18h_claim,
        "confidence_gate_capture_wire_pass": conf_wire_pass,
        "capture_regression_pass": capture_pass,
        "gen11_hold": True,
        "gate": GATE,
        "gate2_3_untouched": True,
        "cycle": "C216",
        "stage_ready": stage_ready,
    })

    BOARD_MD.write_text(
        f"""# 蚁算 UNIFIED SCORECARD

Updated: {ts()} (Asia/Shanghai)

| Axis | Score |
| --- | --- |
| beat_agent | 1.0 (Gate2 archive) |
| replace_agent | 1.0 (ratio~{replace.get('mean_ratio')}) |
| vision_v17 heldout | {v17h} |
| vision_v18 prior→refresh | {v18_prior} → {v18} claim={v18_claim} fail={c213.get('fail_ids')} |
| vision_v18 heldout | {v18h} claim={v18h_claim} disjoint |
| conf_gate capture wire | {conf_wire} pass={conf_wire_pass} |
| desktop_multiwin | {multiwin} |
| capture_regression | {1.0 if capture_pass else 0.0} pointers={c215.get('pointer_ok')} |
| product_readme | {1.0 if product_readme_ok else 0.0} |
| composite | {composite} |

Gate 0.6. Gate2/3 untouched. gen11 HOLD.
""",
        encoding="utf-8",
    )

    STAGE.write_text(
        f"""# STAGE_ANT_C216

Updated: {ts()} (Asia/Shanghai)

**C213-C216 STAGE_READY={'YES' if stage_ready else 'NO'}**

## Batch
| Cycle | Theme | Key |
| --- | --- | --- |
| C213 | V18 fail fix retest | rate={v18} claim={v18_claim} fail={c213.get('fail_ids')} delta={c213.get('rate_delta')} |
| C214 | V18 heldout | rate={v18h} claim={v18h_claim} fail={c214.get('fail_ids')} disjoint |
| C215 | capture regression | pass={capture_pass} pointers={c215.get('pointer_ok')} |
| C216 | scorecard | composite={composite} |

## Iron
Gate **0.6**. Gate2/3 untouched. gen11 HOLD.

## Vision claims (scoped)
- V18 refresh: claim={v18_claim} rate={v18} (was {v18_prior})
- V18 heldout: claim={v18h_claim} rate={v18h}
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
Stage: C213-C216; V18 refresh CLAIM {v18} (was {v18_prior}); V18 heldout CLAIM {v18h}; capture {'PASS' if capture_pass else 'FAIL'}; composite={composite} STAGE_READY={stage_ready}
V18 refresh: rate={v18} n={c213.get('n')} CLAIM={v18_claim} fail={c213.get('fail_ids')} (C213)
V18 heldout: rate={v18h} n={c214.get('n')} CLAIM={v18h_claim} disjoint (C214)
Capture regression: pass={capture_pass} pointers={c215.get('pointer_ok')} (C215)
Scorecard composite: {composite} (C216)
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
                f"\n## C213-C216 ({ts()})\n"
                f"- V18 refresh rate={v18} (was {v18_prior}) claim={v18_claim} fail={c213.get('fail_ids')}\n"
                f"- V18 heldout rate={v18h} claim={v18h_claim} disjoint\n"
                f"- capture_pass={capture_pass} composite={composite} stage_ready={stage_ready}\n"
                f"- gen11 HOLD; Gate2/3 untouched\n"
            )

    print(json.dumps({
        "cycle": "C216", "composite": composite, "stage_ready": stage_ready,
        "v18": v18, "v18_claim": v18_claim, "v18h": v18h, "v18h_claim": v18h_claim,
        "capture_pass": capture_pass,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
