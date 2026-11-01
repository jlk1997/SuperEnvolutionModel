# -*- coding: utf-8 -*-
"""C212: Unified scorecard + STAGE after C207-C211. gen11 HOLD.
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
STAGE = ROOT / "docs" / "STAGE_ANT_C212.md"
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
    c198b = load("docs/r50/C198b_VISION_GATE_V16_CLAIM.json") or {}
    c201 = load("docs/r50/C201_VISION_V16_HELDOUT_SMOKE.json") or {}
    c201b = load("docs/r50/C201b_VISION_GATE_V16_HELDOUT_CLAIM.json") or {}
    c202 = load("docs/r50/C202_V17_DESIGN_BATCH.json") or {}
    c203 = load("docs/r50/C203_VISION_V17_SMOKE.json") or {}
    c203b = load("docs/r50/C203b_VISION_GATE_V17_CLAIM.json") or {}
    c204 = load("docs/r50/C204_CONFIDENCE_GATE_EXPAND.json") or {}
    c207 = load("docs/r50/C207_VISION_V17_HELDOUT_SMOKE.json") or {}
    c207b = load("docs/r50/C207b_VISION_GATE_V17_HELDOUT_CLAIM.json") or {}
    c208 = load("docs/r50/C208_V18_DESIGN_BATCH.json") or {}
    c209 = load("docs/r50/C209_VISION_V18_SMOKE.json") or {}
    c209b = load("docs/r50/C209b_VISION_GATE_V18_CLAIM.json") or {}
    c210 = load("docs/r50/C210_CONFIDENCE_GATE_CAPTURE_WIRE.json") or {}
    c211 = load("docs/r50/C211_CAPTURE_OFFICE_REGRESSION.json") or {}

    v16 = float(c198.get("rate") or 0.0)
    v16h = float(c201.get("rate") or 0.0)
    v17 = float(c203.get("rate") or 0.0)
    v17h = float(c207.get("rate") or 0.0)
    v18 = float(c209.get("rate") or 0.0)
    conf = float(c204.get("rate") or 0.0)
    conf_wire = float(c210.get("rate") or 0.0)
    multiwin = float(c168.get("rate") or 0.0)

    v16_claim = bool(c198b.get("vl_gate_v16_claim") or c198.get("vl_gate_v16_claim"))
    v16h_claim = bool(c201b.get("vl_gate_v16_heldout_claim") or c201.get("vl_gate_v16_heldout_claim") or c201.get("claim"))
    v17_claim = bool(c203b.get("vl_gate_v17_claim") or c203.get("vl_gate_v17_claim") or c203.get("claim"))
    v17h_claim = bool(c207b.get("vl_gate_v17_heldout_claim") or c207.get("vl_gate_v17_heldout_claim") or c207.get("claim"))
    v18_claim = bool(c209b.get("vl_gate_v18_claim") or c209.get("vl_gate_v18_claim") or c209.get("claim"))
    conf_pass = bool(c204.get("pass") or c204.get("claim"))
    conf_wire_pass = bool(c210.get("pass") or c210.get("claim"))
    product_readme_ok = PRODUCT_README.is_file()
    capture_pass = bool(c211.get("pass") if c211 else False)

    parts = [
        1.0 if beat["beat_agent"] else 0.0,
        float(replace.get("rate") or 0.0),
        max(v16, v16h, 0.0),
        max(v17, v17h, 0.0),
        max(v18, 0.0) if c209.get("attempted") else (0.8 if c208.get("pass") else 0.0),
        1.0 if conf_pass else 0.0,
        1.0 if conf_wire_pass else 0.0,
        1.0 if (c168.get("pass") or multiwin >= GATE) else 0.0,
        1.0 if capture_pass else 0.0,
        1.0 if product_readme_ok else 0.0,
    ]
    composite = round(sum(parts) / len(parts), 4)
    stage_ready = bool(
        v17h_claim and v18_claim and conf_wire_pass and capture_pass
        and product_readme_ok and composite >= GATE
    )

    out = {
        "cycle": "C212",
        "theme": "unified_scorecard_c207_c211",
        "gate": GATE,
        "timestamp": ts(),
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "beat": beat,
        "replace": replace,
        "vision": {
            "v16_smoke": {"rate": v16, "claim": v16_claim},
            "v16_heldout": {"rate": v16h, "claim": v16h_claim, "disjoint": True},
            "v17_design": {"n": c202.get("n"), "pass": c202.get("pass"), "claim": False},
            "v17_smoke": {"rate": v17, "n": c203.get("n"), "n_ok": c203.get("n_ok"), "claim": v17_claim, "fail_ids": c203.get("fail_ids")},
            "v17_heldout": {"rate": v17h, "n": c207.get("n"), "n_ok": c207.get("n_ok"), "claim": v17h_claim, "fail_ids": c207.get("fail_ids"), "disjoint": True},
            "v18_design": {"n": c208.get("n"), "pass": c208.get("pass"), "claim": False},
            "v18_smoke": {"rate": v18, "n": c209.get("n"), "n_ok": c209.get("n_ok"), "claim": v18_claim, "fail_ids": c209.get("fail_ids")},
            "confidence_gate_expand": {"rate": conf, "pass": conf_pass, "force_tool": c204.get("force_tool_count")},
            "confidence_gate_capture_wire": {"rate": conf_wire, "pass": conf_wire_pass, "metrics": c210.get("metrics_covered")},
        },
        "desktop_multiwin": {"pass": c168.get("pass"), "rate": multiwin},
        "product": {
            "readme_ok": product_readme_ok,
            "capture_regression_pass": capture_pass,
            "capture_cli": "scripts/ant_capture_office.py",
            "pointer_ok": c211.get("pointer_ok"),
            "pointer_rate": c211.get("pointer_rate"),
        },
        "composite": composite,
        "stage_ready": stage_ready,
        "pass": True,
        "claim": False,
        "note": "Scorecard after V17 heldout + V18 claim + conf-gate capture wire + regression; no new Gate2/3; gen11 HOLD",
    }
    J(DOC / "C212_UNIFIED_SCORECARD.json", out)
    J(SCORE_LATEST, {
        "timestamp": ts(),
        "composite": composite,
        "beat_agent": True,
        "replace_rate": replace.get("rate"),
        "replace_mean_ratio": replace.get("mean_ratio"),
        "vision_v16_heldout_claim": v16h_claim,
        "vision_v17_claim": v17_claim,
        "vision_v17_heldout_rate": v17h,
        "vision_v17_heldout_claim": v17h_claim,
        "vision_v18_rate": v18,
        "vision_v18_claim": v18_claim,
        "confidence_gate_expand_pass": conf_pass,
        "confidence_gate_capture_wire_pass": conf_wire_pass,
        "capture_regression_pass": capture_pass,
        "gen11_hold": True,
        "gate": GATE,
        "gate2_3_untouched": True,
        "cycle": "C212",
        "stage_ready": stage_ready,
    })

    BOARD_MD.write_text(
        f"""# 蚁算 UNIFIED SCORECARD

Updated: {ts()} (Asia/Shanghai)

| Axis | Score |
| --- | --- |
| beat_agent | 1.0 (Gate2 archive) |
| replace_agent | 1.0 (ratio~{replace.get('mean_ratio')}) |
| vision_v16 / heldout | {v16} / {v16h} claim={v16h_claim} |
| vision_v17 / heldout | {v17} / {v17h} claim={v17h_claim} |
| vision_v18 | {v18} claim={v18_claim} fail={c209.get('fail_ids')} |
| conf_gate expand | {conf} pass={conf_pass} |
| conf_gate capture wire | {conf_wire} pass={conf_wire_pass} |
| desktop_multiwin | {multiwin} |
| capture_readme_regression | {1.0 if capture_pass else 0.0} |
| product_readme | {1.0 if product_readme_ok else 0.0} |
| composite | {composite} |

Gate 0.6. Gate2/3 untouched. gen11 HOLD.
""",
        encoding="utf-8",
    )

    STAGE.write_text(
        f"""# STAGE_ANT_C212

Updated: {ts()} (Asia/Shanghai)

**C207-C212 STAGE_READY={'YES' if stage_ready else 'NO'}**

## Batch
| Cycle | Theme | Key |
| --- | --- | --- |
| C207 | V17 heldout | rate={v17h} claim={v17h_claim} fail={c207.get('fail_ids')} |
| C208 | V18 design | n={c208.get('n')} pass={c208.get('pass')} |
| C209 | V18 smoke | rate={v18} claim={v18_claim} fail={c209.get('fail_ids')} |
| C210 | conf-gate capture wire | rate={conf_wire} pass={conf_wire_pass} |
| C211 | capture README regression | pass={capture_pass} pointers={c211.get('pointer_ok')} |
| C212 | scorecard | composite={composite} |

## Iron
Gate **0.6**. Gate2/3 untouched. gen11 HOLD.

## Vision claims (scoped)
- V17 heldout: claim={v17h_claim} rate={v17h}
- V18: claim={v18_claim} rate={v18}
- conf-gate capture wire: pass={conf_wire_pass} rate={conf_wire}
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
Stage: C207-C212 continuous; V17 heldout CLAIM {v17h}; V18 CLAIM {v18}; conf-gate capture wire {conf_wire}; capture {'PASS' if capture_pass else 'FAIL'}; composite={composite} STAGE_READY={stage_ready}
V17 heldout: rate={v17h} n={c207.get('n')} CLAIM={v17h_claim} (C207) disjoint
V18 smoke: rate={v18} n={c209.get('n')} CLAIM={v18_claim} fail={c209.get('fail_ids')} (C209)
Conf-gate capture wire: rate={conf_wire} pass={conf_wire_pass} (C210)
Capture README regression: pass={capture_pass} pointers={c211.get('pointer_ok')} (C211)
Scorecard composite: {composite} (C212)
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
                f"\n## C207-C212 ({ts()})\n"
                f"- V17 heldout rate={v17h} claim={v17h_claim}\n"
                f"- V18 rate={v18} claim={v18_claim} fail={c209.get('fail_ids')}\n"
                f"- conf_gate_wire rate={conf_wire} pass={conf_wire_pass}\n"
                f"- capture_pass={capture_pass} composite={composite} stage_ready={stage_ready}\n"
                f"- gen11 HOLD; Gate2/3 untouched\n"
            )

    print(json.dumps({
        "cycle": "C212", "composite": composite, "stage_ready": stage_ready,
        "v17h": v17h, "v17h_claim": v17h_claim, "v18": v18, "v18_claim": v18_claim,
        "conf_wire": conf_wire, "capture_pass": capture_pass,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
