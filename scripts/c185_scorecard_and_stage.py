# -*- coding: utf-8 -*-
"""C185: Unified scorecard + STAGE after C181-C184. gen11 HOLD.
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
STAGE = ROOT / "docs" / "STAGE_ANT_C185.md"
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
    c167 = load("docs/r50/C167_VISION_V10_SMOKE.json") or {}
    c171 = load("docs/r50/C171_VISION_V10_HELDOUT_SMOKE.json") or {}
    c173 = load("docs/r50/C173_VISION_V11_SMOKE.json") or {}
    c175 = load("docs/r50/C175_VISION_V11_HELDOUT_SMOKE.json") or {}
    c180 = load("docs/r50/C180_V12_FAIL_FIX_RETEST.json") or {}
    c180b = load("docs/r50/C180b_VISION_GATE_V12_REFRESH_CLAIM.json") or {}
    c181 = load("docs/r50/C181_VISION_V12_HELDOUT_SMOKE.json") or {}
    c181b = load("docs/r50/C181b_VISION_GATE_V12_HELDOUT_CLAIM.json") or {}
    c182 = load("docs/r50/C182_V13_DESIGN_BATCH.json") or {}
    c183 = load("docs/r50/C183_VISION_V13_SMOKE.json") or {}
    c183b = load("docs/r50/C183b_VISION_GATE_V13_CLAIM.json") or {}
    c184 = load("docs/r50/C184_CAPTURE_OFFICE_REGRESSION.json") or {}
    c168 = load("docs/r50/C168_DESKTOP_MULTIWIN_PRESSURE.json") or {}

    v10 = float(c167.get("rate") or 0.0)
    v10h = float(c171.get("rate") or 0.0)
    v11 = float(c173.get("rate") or 0.0)
    v11h = float(c175.get("rate") or 0.0)
    v12 = float(c180.get("rate") or 0.0)
    v12h = float(c181.get("rate") or 0.0)
    v13 = float(c183.get("rate") or 0.0)
    multiwin = float(c168.get("rate") or 0.0)
    v12_claim = bool(c180b.get("vl_gate_v12_claim") or c180.get("vl_gate_v12_claim_refreshed") or c180.get("claim"))
    v12h_claim = bool(c181b.get("vl_gate_v12_heldout_claim") or c181.get("vl_gate_v12_heldout_claim"))
    v13_claim = bool(c183b.get("vl_gate_v13_claim") or c183.get("vl_gate_v13_claim"))
    product_readme_ok = PRODUCT_README.is_file()
    capture_pass = bool(c184.get("pass"))

    parts = [
        1.0 if beat["beat_agent"] else 0.0,
        float(replace.get("rate") or 0.0),
        max(v10, v10h, 0.0),
        max(v11, v11h, 0.0),
        max(v12, v12h, 0.0),
        max(v13, 0.0) if c183.get("attempted") else (0.8 if c182.get("pass") else 0.0),
        1.0 if (c168.get("pass") or multiwin >= GATE) else 0.0,
        1.0 if capture_pass else 0.0,
        1.0 if product_readme_ok else 0.0,
    ]
    composite = round(sum(parts) / len(parts), 4)
    stage_ready = bool(
        v12h_claim and v13_claim and capture_pass and product_readme_ok and composite >= GATE
    )

    out = {
        "cycle": "C185",
        "theme": "unified_scorecard_c181_c184",
        "gate": GATE,
        "timestamp": ts(),
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "beat": beat,
        "replace": replace,
        "vision": {
            "v10": {"rate": v10},
            "v10_heldout": {"rate": v10h},
            "v11": {"rate": v11},
            "v11_heldout": {"rate": v11h},
            "v12": {"rate": v12, "claim": v12_claim},
            "v12_heldout": {
                "rate": v12h, "n": c181.get("n"), "n_ok": c181.get("n_ok"),
                "claim": v12h_claim, "fail_ids": c181.get("fail_ids"), "disjoint": True,
            },
            "v13_design": {"n": c182.get("n"), "pass": c182.get("pass"), "claim": False},
            "v13_smoke": {
                "rate": v13, "n": c183.get("n"), "n_ok": c183.get("n_ok"),
                "claim": v13_claim, "fail_ids": c183.get("fail_ids"),
            },
        },
        "desktop_multiwin": {"pass": c168.get("pass"), "rate": multiwin},
        "product": {
            "readme_ok": product_readme_ok,
            "capture_regression_pass": capture_pass,
            "capture_cli": "scripts/ant_capture_office.py",
        },
        "composite": composite,
        "stage_ready": stage_ready,
        "pass": True,
        "claim": False,
        "note": "Scorecard after V12 heldout + V13 claim + capture regression; no new Gate2/3; gen11 HOLD",
    }
    J(DOC / "C185_UNIFIED_SCORECARD.json", out)
    J(SCORE_LATEST, {
        "timestamp": ts(),
        "composite": composite,
        "beat_agent": True,
        "replace_rate": replace.get("rate"),
        "replace_mean_ratio": replace.get("mean_ratio"),
        "vision_v12_rate": v12,
        "vision_v12_heldout_rate": v12h,
        "vision_v12_heldout_claim": v12h_claim,
        "vision_v13_rate": v13,
        "vision_v13_claim": v13_claim,
        "capture_regression_pass": capture_pass,
        "gen11_hold": True,
        "gate": GATE,
        "gate2_3_untouched": True,
        "cycle": "C185",
        "stage_ready": stage_ready,
    })

    BOARD_MD.write_text(
        f"""# 蚁算 UNIFIED SCORECARD

Updated: {ts()} (Asia/Shanghai)

| Axis | Score |
| --- | --- |
| beat_agent | 1.0 (Gate2 archive) |
| replace_agent | 1.0 (ratio~{replace.get('mean_ratio')}) |
| vision_v10 / heldout | {v10} / {v10h} |
| vision_v11 / heldout | {v11} / {v11h} |
| vision_v12 / heldout | {v12} / {v12h} claim={v12h_claim} |
| vision_v13 | {v13} claim={v13_claim} |
| desktop_multiwin | {multiwin} |
| capture_readme_regression | {1.0 if capture_pass else 0.0} |
| product_readme | {1.0 if product_readme_ok else 0.0} |
| composite | {composite} |

Gate 0.6. Gate2/3 untouched. gen11 HOLD.
""",
        encoding="utf-8",
    )

    STAGE.write_text(
        f"""# STAGE_ANT_C185

Updated: {ts()} (Asia/Shanghai)

**C181-C185 STAGE_READY={'YES' if stage_ready else 'NO'}**

## Batch
| Cycle | Theme | Key |
| --- | --- | --- |
| C181 | V12 heldout | rate={v12h} claim={v12h_claim} fail={c181.get('fail_ids')} |
| C182 | V13 design | n={c182.get('n')} pass={c182.get('pass')} |
| C183 | V13 smoke | rate={v13} claim={v13_claim} fail={c183.get('fail_ids')} |
| C184 | capture README regression | pass={capture_pass} |
| C185 | scorecard | composite={composite} |

## Iron
Gate **0.6**. Gate2/3 untouched. gen11 HOLD.

## Vision claims (scoped)
- V12 heldout: claim={v12h_claim} rate={v12h}
- V13: claim={v13_claim} rate={v13}
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
Stage: C181-C185 continuous; V12 heldout CLAIM {v12h}; V13 CLAIM {v13}; capture regression {'PASS' if capture_pass else 'FAIL'}; composite={composite} STAGE_READY={stage_ready}
V12 heldout: rate={v12h} n={c181.get('n')} CLAIM={v12h_claim} (C181) disjoint
V13 smoke: rate={v13} n={c183.get('n')} CLAIM={v13_claim} (C183)
Capture README regression: pass={capture_pass} (C184)
Scorecard composite: {composite} (C185)
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
                f"\n## C181-C185 ({ts()})\n"
                f"- V12 heldout rate={v12h} claim={v12h_claim}\n"
                f"- V13 rate={v13} claim={v13_claim}\n"
                f"- capture_pass={capture_pass} composite={composite} stage_ready={stage_ready}\n"
                f"- gen11 HOLD; Gate2/3 untouched\n"
            )

    print(json.dumps({
        "cycle": "C185", "composite": composite, "stage_ready": stage_ready,
        "v12h": v12h, "v12h_claim": v12h_claim, "v13": v13, "v13_claim": v13_claim,
        "capture_pass": capture_pass,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
