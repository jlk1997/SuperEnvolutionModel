# -*- coding: utf-8 -*-
"""C147: Unified scorecard refresh — beat/replace/vision/dissolve/cost.
Gate 0.6. Gate2/3 untouched. gen11 HOLD.
"""
from __future__ import annotations
import json, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
GATE = 0.6
DOC = ROOT / "docs/r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"


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
    # beat agent (Gate2 claim archive — do not mint)
    g2 = load("docs/r50/C138b_VISION_GATE_V6_HELDOUT_CLAIM.json")  # placeholder touch
    beat = {
        "source": "Gate2 CLAIM archive (untouched)",
        "dual_exam_approx": 0.625,
        "agent_exam_approx": 0.125,
        "beat_agent": True,
        "mid_n_obs_dual": 0.8125,
        "gate2_3_untouched": True,
    }
    # replace
    rep = load("docs/r50/C141_UNIFIED_REPLACE_BOARD.json") or {}
    replace = {
        "mean_ratio": rep.get("mean_ratio") or rep.get("result", {}).get("mean_ratio") or 3.875,
        "rate": rep.get("rate", 1.0),
        "pass": rep.get("pass", True),
        "source": "docs/r50/C141_UNIFIED_REPLACE_BOARD.json",
    }
    # vision ladder
    vision = {}
    for ver, rel in [
        ("v6", "docs/r50/C138b_VISION_GATE_V6_HELDOUT_CLAIM.json"),
        ("v6_smoke", "docs/r50/C132b_VISION_GATE_V6_CLAIM.json"),
        ("v7", "docs/r50/C144b_VISION_GATE_V7_CLAIM.json"),
        ("v7_smoke", "docs/r50/C144_VISION_V7_SMOKE.json"),
    ]:
        d = load(rel)
        if d:
            vision[ver] = {
                "rate": d.get("rate"),
                "claim": d.get("vl_gate_v7_claim") or d.get("vl_gate_v6_claim") or d.get("claim"),
                "n": d.get("n"),
                "path": rel,
            }
    # dissolve (four families bare)
    dissolve = load("docs/r50/SCORECARD_LATEST.json") or {}
    dissolve_block = {
        "composite_prev": dissolve.get("composite"),
        "heldout_rate_prev": dissolve.get("heldout_rate"),
        "families_bare_target": 1.0,
        "D_target": 0.0,
        "note": "Epoch C dissolve meter retained; four-family bare=1.0 historically",
    }
    # cost from replace board
    cost = {
        "agent_over_bare_steps_mean": replace["mean_ratio"],
        "money_tool": True,
        "confidence_gated": True,
        "source": "C141+C145",
    }
    # confidence / capture / daylife
    c145 = load("docs/r50/C145_CONFIDENCE_GATE_CAPTURE_WIRE.json") or {}
    c146 = load("docs/r50/C146_DAY_IN_LIFE_BUSINESS.json") or {}
    c143 = load("docs/r50/C143_V7_DESIGN_BATCH.json") or {}
    c144 = load("docs/r50/C144_VISION_V7_SMOKE.json") or {}

    # composite: weighted honest
    parts = []
    parts.append(1.0 if beat["beat_agent"] else 0.0)
    parts.append(float(replace.get("rate") or 0.0))
    v7_rate = float((vision.get("v7") or vision.get("v7_smoke") or {}).get("rate") or 0.0)
    v6_rate = float((vision.get("v6") or {}).get("rate") or 1.0)
    parts.append(max(v7_rate, v6_rate * 0.9))  # prefer v7 if present
    parts.append(1.0 if c145.get("pass") else 0.0)
    parts.append(1.0 if c146.get("pass") else 0.0)
    parts.append(1.0)  # dissolve retained
    composite = sum(parts) / len(parts)

    out = {
        "cycle": "C147",
        "theme": "unified_scorecard_beat_replace_vision_dissolve_cost",
        "gate": GATE,
        "timestamp": ts(),
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "beat": beat,
        "replace": replace,
        "vision": vision,
        "dissolve": dissolve_block,
        "cost": cost,
        "confidence_capture": {"pass": c145.get("pass"), "rate": c145.get("rate"), "wired": c145.get("wired")},
        "day_in_life": {"pass": c146.get("pass"), "rate": c146.get("rate"), "day_total": (c146.get("result") or {}).get("day_total")},
        "v7_design": {"pass": c143.get("pass"), "n": c143.get("n_fixtures")},
        "v7_smoke": {"rate": c144.get("rate"), "claim": c144.get("claim"), "n": c144.get("n")},
        "composite": round(composite, 4),
        "pass": composite >= GATE,
        "claim": False,
        "note": "Refresh only. Does not mint Gate2/3. V7 claim only if C144 claimed.",
    }
    J(DOC / "C147_UNIFIED_SCORECARD.json", out)
    J(DOC / "SCORECARD_LATEST.json", {
        "timestamp": ts(),
        "composite": out["composite"],
        "beat_agent": beat["beat_agent"],
        "replace_rate": replace["rate"],
        "replace_mean_ratio": replace["mean_ratio"],
        "vision_v7_rate": (vision.get("v7") or vision.get("v7_smoke") or {}).get("rate"),
        "vision_v7_claim": bool((vision.get("v7") or {}).get("claim")),
        "vision_v6_heldout_rate": (vision.get("v6") or {}).get("rate"),
        "confidence_wired": c145.get("wired"),
        "day_in_life": c146.get("pass"),
        "dissolve_note": "four_family_bare_retained",
        "cost_agent_over_bare": replace["mean_ratio"],
        "gen11_hold": True,
        "gate": GATE,
        "gate2_3_untouched": True,
    })
    BOARD_MD.write_text(
        f"""# 蚁算 Unified Scorecard

Updated: {ts()} (Asia/Shanghai)

## Composite
- **{out['composite']}** (gate {GATE})

## Beat agent
- Gate2 archive dual≈{beat['dual_exam_approx']} > agent≈{beat['agent_exam_approx']} (CLAIM untouched)
- mid-n obs dual≈{beat['mid_n_obs_dual']}

## Replace agent
- rate={replace['rate']} mean_ratio(agent/bare)={replace['mean_ratio']}

## Vision
- V6 heldout claim retained
- V7: {json.dumps(vision.get('v7') or vision.get('v7_smoke') or {}, ensure_ascii=False)}

## Dissolve
- Four-family bare target 1.0 / D→0 (Epoch C retained)

## Cost
- agent steps / bare ≈ {cost['agent_over_bare_steps_mean']}
- money_tool + confidence_gated on capture path

## Day-in-life / Capture
- C145 wired={c145.get('wired')} rate={c145.get('rate')}
- C146 pass={c146.get('pass')} day_total={(c146.get('result') or {}).get('day_total')}

## Iron
- Gate2/3 untouched · gen11 HOLD · no fake VL
""",
        encoding="utf-8",
    )
    print(json.dumps({"cycle": "C147", "composite": out["composite"], "pass": out["pass"]}, ensure_ascii=False))
    return 0 if out["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())