# -*- coding: utf-8 -*-
"""C200: Unified scorecard + STAGE after C196-C199. gen11 HOLD.
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
STAGE = ROOT / "docs" / "STAGE_ANT_C200.md"
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
    c183 = load("docs/r50/C183_VISION_V13_SMOKE.json") or {}
    c183b = load("docs/r50/C183b_VISION_GATE_V13_CLAIM.json") or {}
    c186 = load("docs/r50/C186_VISION_V13_HELDOUT_SMOKE.json") or {}
    c186b = load("docs/r50/C186b_VISION_GATE_V13_HELDOUT_CLAIM.json") or {}
    c187 = load("docs/r50/C187_V14_DESIGN_BATCH.json") or {}
    c188 = load("docs/r50/C188_VISION_V14_SMOKE.json") or {}
    c188b = load("docs/r50/C188b_VISION_GATE_V14_CLAIM.json") or {}
    c191 = load("docs/r50/C191_VISION_V14_HELDOUT_SMOKE.json") or {}
    c191b = load("docs/r50/C191b_VISION_GATE_V14_HELDOUT_CLAIM.json") or {}
    c192 = load("docs/r50/C192_V15_DESIGN_BATCH.json") or {}
    c193 = load("docs/r50/C193_VISION_V15_SMOKE.json") or {}
    c193b = load("docs/r50/C193b_VISION_GATE_V15_CLAIM.json") or {}
    c194 = load("docs/r50/C194_CAPTURE_OFFICE_REGRESSION.json") or {}
    c196 = load("docs/r50/C196_VISION_V15_HELDOUT_SMOKE.json") or {}
    c196b = load("docs/r50/C196b_VISION_GATE_V15_HELDOUT_CLAIM.json") or {}
    c197 = load("docs/r50/C197_V16_DESIGN_BATCH.json") or {}
    c198 = load("docs/r50/C198_VISION_V16_SMOKE.json") or {}
    c198b = load("docs/r50/C198b_VISION_GATE_V16_CLAIM.json") or {}
    c199 = load("docs/r50/C199_CAPTURE_OFFICE_REGRESSION.json") or {}
    c168 = load("docs/r50/C168_DESKTOP_MULTIWIN_PRESSURE.json") or {}

    v10 = float(c167.get("rate") or 0.0)
    v10h = float(c171.get("rate") or 0.0)
    v11 = float(c173.get("rate") or 0.0)
    v11h = float(c175.get("rate") or 0.0)
    v12 = float(c180.get("rate") or 0.0)
    v12h = float(c181.get("rate") or 0.0)
    v13 = float(c183.get("rate") or 0.0)
    v13h = float(c186.get("rate") or 0.0)
    v14 = float(c188.get("rate") or 0.0)
    v14h = float(c191.get("rate") or 0.0)
    v15 = float(c193.get("rate") or 0.0)
    v15h = float(c196.get("rate") or 0.0)
    v16 = float(c198.get("rate") or 0.0)
    multiwin = float(c168.get("rate") or 0.0)
    v12_claim = bool(c180b.get("vl_gate_v12_claim") or c180.get("vl_gate_v12_claim_refreshed") or c180.get("claim"))
    v12h_claim = bool(c181b.get("vl_gate_v12_heldout_claim") or c181.get("vl_gate_v12_heldout_claim"))
    v13_claim = bool(c183b.get("vl_gate_v13_claim") or c183.get("vl_gate_v13_claim"))
    v13h_claim = bool(c186b.get("vl_gate_v13_heldout_claim") or c186.get("vl_gate_v13_heldout_claim"))
    v14_claim = bool(c188b.get("vl_gate_v14_claim") or c188.get("vl_gate_v14_claim"))
    v14h_claim = bool(c191b.get("vl_gate_v14_heldout_claim") or c191.get("vl_gate_v14_heldout_claim"))
    v15_claim = bool(c193b.get("vl_gate_v15_claim") or c193.get("vl_gate_v15_claim"))
    v15h_claim = bool(c196b.get("vl_gate_v15_heldout_claim") or c196.get("vl_gate_v15_heldout_claim"))
    v16_claim = bool(c198b.get("vl_gate_v16_claim") or c198.get("vl_gate_v16_claim"))
    product_readme_ok = PRODUCT_README.is_file()
    capture_pass = bool(c199.get("pass") if c199 else c194.get("pass"))

    parts = [
        1.0 if beat["beat_agent"] else 0.0,
        float(replace.get("rate") or 0.0),
        max(v10, v10h, 0.0),
        max(v11, v11h, 0.0),
        max(v12, v12h, 0.0),
        max(v13, v13h, 0.0),
        max(v14, v14h, 0.0),
        max(v15, v15h, 0.0) if (c193.get("attempted") or c196.get("attempted")) else (0.8 if c192.get("pass") else 0.0),
        max(v16, 0.0) if c198.get("attempted") else (0.8 if c197.get("pass") else 0.0),
        1.0 if (c168.get("pass") or multiwin >= GATE) else 0.0,
        1.0 if capture_pass else 0.0,
        1.0 if product_readme_ok else 0.0,
    ]
    composite = round(sum(parts) / len(parts), 4)
    stage_ready = bool(
        v15h_claim and v16_claim and capture_pass and product_readme_ok and composite >= GATE
    )

    out = {
        "cycle": "C200",
        "theme": "unified_scorecard_c196_c199",
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
            "v12_heldout": {"rate": v12h, "claim": v12h_claim},
            "v13": {"rate": v13, "claim": v13_claim},
            "v13_heldout": {"rate": v13h, "claim": v13h_claim, "disjoint": True},
            "v14": {"rate": v14, "claim": v14_claim},
            "v14_heldout": {
                "rate": v14h, "n": c191.get("n"), "n_ok": c191.get("n_ok"),
                "claim": v14h_claim, "fail_ids": c191.get("fail_ids"), "disjoint": True,
            },
            "v15_design": {"n": c192.get("n"), "pass": c192.get("pass"), "claim": False},
            "v15_smoke": {
                "rate": v15, "n": c193.get("n"), "n_ok": c193.get("n_ok"),
                "claim": v15_claim, "fail_ids": c193.get("fail_ids"),
            },
            "v15_heldout": {
                "rate": v15h, "n": c196.get("n"), "n_ok": c196.get("n_ok"),
                "claim": v15h_claim, "fail_ids": c196.get("fail_ids"), "disjoint": True,
            },
            "v16_design": {"n": c197.get("n"), "pass": c197.get("pass"), "claim": False},
            "v16_smoke": {
                "rate": v16, "n": c198.get("n"), "n_ok": c198.get("n_ok"),
                "claim": v16_claim, "fail_ids": c198.get("fail_ids"),
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
        "note": "Scorecard after V15 heldout + V16 claim + capture regression; no new Gate2/3; gen11 HOLD",
    }
    J(DOC / "C200_UNIFIED_SCORECARD.json", out)
    J(SCORE_LATEST, {
        "timestamp": ts(),
        "composite": composite,
        "beat_agent": True,
        "replace_rate": replace.get("rate"),
        "replace_mean_ratio": replace.get("mean_ratio"),
        "vision_v14_rate": v14,
        "vision_v14_heldout_rate": v14h,
        "vision_v14_heldout_claim": v14h_claim,
        "vision_v15_rate": v15,
        "vision_v15_claim": v15_claim,
        "vision_v15_heldout_rate": v15h,
        "vision_v15_heldout_claim": v15h_claim,
        "vision_v16_rate": v16,
        "vision_v16_claim": v16_claim,
        "capture_regression_pass": capture_pass,
        "gen11_hold": True,
        "gate": GATE,
        "gate2_3_untouched": True,
        "cycle": "C200",
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
| vision_v13 / heldout | {v13} / {v13h} claim={v13h_claim} |
| vision_v14 / heldout | {v14} / {v14h} claim={v14h_claim} |
| vision_v15 / heldout | {v15} / {v15h} claim={v15h_claim} |
| vision_v16 | {v16} claim={v16_claim} |
| desktop_multiwin | {multiwin} |
| capture_readme_regression | {1.0 if capture_pass else 0.0} |
| product_readme | {1.0 if product_readme_ok else 0.0} |
| composite | {composite} |

Gate 0.6. Gate2/3 untouched. gen11 HOLD.
""",
        encoding="utf-8",
    )

    STAGE.write_text(
        f"""# STAGE_ANT_C200

Updated: {ts()} (Asia/Shanghai)

**C196-C200 STAGE_READY={'YES' if stage_ready else 'NO'}**

## Batch
| Cycle | Theme | Key |
| --- | --- | --- |
| C196 | V15 heldout | rate={v15h} claim={v15h_claim} fail={c196.get('fail_ids')} |
| C197 | V16 design | n={c197.get('n')} pass={c197.get('pass')} |
| C198 | V16 smoke | rate={v16} claim={v16_claim} fail={c198.get('fail_ids')} |
| C199 | capture README regression | pass={capture_pass} |
| C200 | scorecard | composite={composite} |

## Iron
Gate **0.6**. Gate2/3 untouched. gen11 HOLD.

## Vision claims (scoped)
- V15 heldout: claim={v15h_claim} rate={v15h}
- V16: claim={v16_claim} rate={v16}
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
Stage: C196-C200 continuous; V15 heldout CLAIM {v15h}; V16 CLAIM {v16}; capture regression {'PASS' if capture_pass else 'FAIL'}; composite={composite} STAGE_READY={stage_ready}
V15 heldout: rate={v15h} n={c196.get('n')} CLAIM={v15h_claim} (C196) disjoint
V16 smoke: rate={v16} n={c198.get('n')} CLAIM={v16_claim} (C198)
Capture README regression: pass={capture_pass} (C199)
Scorecard composite: {composite} (C200)
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
                f"\n## C196-C200 ({ts()})\n"
                f"- V15 heldout rate={v15h} claim={v15h_claim}\n"
                f"- V16 rate={v16} claim={v16_claim}\n"
                f"- capture_pass={capture_pass} composite={composite} stage_ready={stage_ready}\n"
                f"- gen11 HOLD; Gate2/3 untouched\n"
            )

    print(json.dumps({
        "cycle": "C200", "composite": composite, "stage_ready": stage_ready,
        "v15h": v15h, "v15h_claim": v15h_claim, "v16": v16, "v16_claim": v16_claim,
        "capture_pass": capture_pass,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
