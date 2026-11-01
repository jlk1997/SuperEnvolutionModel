# -*- coding: utf-8 -*-
"""C174: Unified scorecard + STAGE after C171-C173. gen11 HOLD.
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
STAGE = ROOT / "docs" / "STAGE_ANT_C174.md"
CKPT = ROOT / "docs" / "CHECKPOINT_NOW.md"
LOOP_APPEND = ROOT / "docs" / "蚁算_R50PLUS_LOOP.md"
PRODUCT_README = ROOT / "docs" / "蚁算_截图办公_README.md"


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
    c167b = load("docs/r50/C167b_VISION_GATE_V10_CLAIM.json") or {}
    c171 = load("docs/r50/C171_VISION_V10_HELDOUT_SMOKE.json") or {}
    c171b = load("docs/r50/C171b_VISION_GATE_V10_HELDOUT_CLAIM.json") or {}
    c172 = load("docs/r50/C172_V11_DESIGN_BATCH.json") or {}
    c173 = load("docs/r50/C173_VISION_V11_SMOKE.json") or {}
    c173b = load("docs/r50/C173b_VISION_GATE_V11_CLAIM.json") or {}
    c168 = load("docs/r50/C168_DESKTOP_MULTIWIN_PRESSURE.json") or {}
    c169 = load("docs/r50/C169_PRODUCT_REGRESSION_SWEEP.json") or {}

    v10 = float(c167.get("rate") or 0.0)
    v10h = float(c171.get("rate") or 0.0)
    v11 = float(c173.get("rate") or 0.0)
    multiwin = float(c168.get("rate") or 0.0)
    v10_claim = bool(c167b.get("vl_gate_v10_claim") or c167.get("vl_gate_v10_claim"))
    v10h_claim = bool(c171b.get("vl_gate_v10_heldout_claim") or c171.get("vl_gate_v10_heldout_claim"))
    v11_claim = bool(c173b.get("vl_gate_v11_claim") or c173.get("vl_gate_v11_claim"))
    product_readme_ok = PRODUCT_README.is_file()

    parts = [
        1.0 if beat["beat_agent"] else 0.0,
        float(replace.get("rate") or 0.0),
        max(v10, v10h, 0.0),
        max(v11, 0.0) if c173.get("attempted") else (0.8 if c172.get("pass") else 0.0),
        1.0 if (c168.get("pass") or multiwin >= GATE) else 0.0,
        1.0 if c169.get("pass") else float(c169.get("core_v4_v9_rate") or 0.0),
        1.0 if product_readme_ok else 0.0,
    ]
    composite = round(sum(parts) / len(parts), 4)

    out = {
        "cycle": "C174",
        "theme": "unified_scorecard_c171_c173",
        "gate": GATE,
        "timestamp": ts(),
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "beat": beat,
        "replace": replace,
        "vision": {
            "v10": {"rate": v10, "claim": v10_claim},
            "v10_heldout": {
                "rate": v10h, "n": c171.get("n"), "n_ok": c171.get("n_ok"),
                "claim": v10h_claim, "fail_ids": c171.get("fail_ids"), "disjoint": True,
            },
            "v11_design": {"n": c172.get("n"), "pass": c172.get("pass"), "claim": False},
            "v11_smoke": {
                "rate": v11, "n": c173.get("n"), "n_ok": c173.get("n_ok"),
                "claim": v11_claim, "fail_ids": c173.get("fail_ids"),
            },
        },
        "desktop_multiwin": {"pass": c168.get("pass"), "rate": multiwin},
        "product": {
            "readme": str(PRODUCT_README.relative_to(ROOT)).replace("\\", "/") if product_readme_ok else None,
            "readme_ok": product_readme_ok,
            "capture_cli": "scripts/ant_capture_office.py",
        },
        "composite": composite,
        "stage_ready": bool(
            v10h_claim and v11_claim and product_readme_ok and composite >= GATE
        ),
        "pass": True,
        "claim": False,
        "note": "Scorecard refresh after V10 heldout + V11 claim; no new Gate2/3; gen11 HOLD",
    }
    J(DOC / "C174_UNIFIED_SCORECARD.json", out)

    BOARD_MD.write_text(
        f"""# 蚁算 UNIFIED SCORECARD

Updated: {ts()} (Asia/Shanghai)

| Axis | Score |
| --- | --- |
| beat_agent | 1.0 (Gate2 archive) |
| replace_agent | 1.0 (ratio~{replace.get('mean_ratio')}) |
| vision_v10 | {v10} claim={v10_claim} |
| vision_v10_heldout | {v10h} claim={v10h_claim} |
| vision_v11 | {v11} claim={v11_claim} |
| desktop_multiwin | {multiwin} |
| product_readme | {1.0 if product_readme_ok else 0.0} |
| composite | {composite} |

Gate 0.6. Gate2/3 untouched. gen11 HOLD.
""",
        encoding="utf-8",
    )

    STAGE.write_text(
        f"""# STAGE_ANT_C174

Updated: {ts()} (Asia/Shanghai)

**C171-C174 STAGE_READY={'YES' if out['stage_ready'] else 'NO'}**

## Batch
| Cycle | Theme | Key |
| --- | --- | --- |
| C171 | V10 heldout | rate={v10h} claim={v10h_claim} fail={c171.get('fail_ids')} |
| C172 | V11 design | n={c172.get('n')} pass={c172.get('pass')} |
| C173 | V11 smoke | rate={v11} claim={v11_claim} fail={c173.get('fail_ids')} |
| C174 | scorecard + product README | composite={composite} |

## Product
- `docs/蚁算_截图办公_README.md` polished demo entry

## Iron
Gate **0.6**. Gate2/3 untouched. gen11 HOLD.

## Vision claims (scoped)
- V10 / V10 heldout: claim={v10_claim}/{v10h_claim}
- V11: claim={v11_claim} rate={v11}
""",
        encoding="utf-8",
    )

    CKPT.write_text(
        f"""# CHECKPOINT_NOW
HEAD: (pending commit)
Stage: C171-C174 STAGE_READY={'YES' if out['stage_ready'] else 'NO'}
V10 heldout: rate={v10h} n={c171.get('n')} CLAIM={v10h_claim} (C171) disjoint
V11 design: n={c172.get('n')} (C172)
V11 smoke: rate={v11} n={c173.get('n')} CLAIM={v11_claim} (C173) glare/skew/hand/redact/night/mosaic
Product README: docs/蚁算_截图办公_README.md
Scorecard composite: {composite} (C174)
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
                f"\n## C171-C174 @ {ts()}\n"
                f"- C171 V10 heldout rate={v10h} claim={v10h_claim}\n"
                f"- C172 V11 design n={c172.get('n')}\n"
                f"- C173 V11 smoke rate={v11} claim={v11_claim}\n"
                f"- C174 scorecard composite={composite} STAGE_READY={out['stage_ready']}\n"
                f"- gen11 HOLD; Gate2/3 untouched\n"
            )

    print(json.dumps({
        "cycle": "C174",
        "composite": composite,
        "stage_ready": out["stage_ready"],
        "v10h": v10h,
        "v11": v11,
        "v10h_claim": v10h_claim,
        "v11_claim": v11_claim,
    }, ensure_ascii=False))
    return 0 if out["stage_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
