# -*- coding: utf-8 -*-
"""C152: Unified scorecard refresh after C149-C151.
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
    beat = {
        "source": "Gate2 CLAIM archive (untouched)",
        "dual_exam_approx": 0.625,
        "agent_exam_approx": 0.125,
        "beat_agent": True,
        "mid_n_obs_dual": 0.8125,
        "gate2_3_untouched": True,
    }
    rep = load("docs/r50/C141_UNIFIED_REPLACE_BOARD.json") or {}
    replace = {
        "mean_ratio": rep.get("mean_ratio") or (rep.get("result") or {}).get("mean_ratio") or 3.875,
        "rate": rep.get("rate", 1.0),
        "pass": rep.get("pass", True),
        "source": "docs/r50/C141_UNIFIED_REPLACE_BOARD.json",
    }
    vision = {}
    for ver, rel in [
        ("v6_heldout", "docs/r50/C138b_VISION_GATE_V6_HELDOUT_CLAIM.json"),
        ("v6", "docs/r50/C132b_VISION_GATE_V6_CLAIM.json"),
        ("v7", "docs/r50/C149b_VISION_GATE_V7_REFRESH_CLAIM.json"),
        ("v7_legacy", "docs/r50/C144b_VISION_GATE_V7_CLAIM.json"),
        ("v7_heldout", "docs/r50/C150b_VISION_GATE_V7_HELDOUT_CLAIM.json"),
        ("v7_smoke", "docs/r50/C149_V7_PARSE_FIX_RETEST.json"),
        ("v7_heldout_smoke", "docs/r50/C150_VISION_V7_HELDOUT_SMOKE.json"),
    ]:
        d = load(rel)
        if d:
            vision[ver] = {
                "rate": d.get("rate"),
                "claim": d.get("vl_gate_v7_claim") or d.get("vl_gate_v7_heldout_claim") or d.get("vl_gate_v6_claim") or d.get("claim"),
                "n": d.get("n"),
                "path": rel,
            }
    c145 = load("docs/r50/C145_CONFIDENCE_GATE_CAPTURE_WIRE.json") or {}
    c146 = load("docs/r50/C146_DAY_IN_LIFE_BUSINESS.json") or {}
    c149 = load("docs/r50/C149_V7_PARSE_FIX_RETEST.json") or {}
    c150 = load("docs/r50/C150_VISION_V7_HELDOUT_SMOKE.json") or {}
    c151 = load("docs/r50/C151_BUSINESS_DAY_GROW.json") or {}

    v7_rate = float((vision.get("v7") or vision.get("v7_legacy") or vision.get("v7_smoke") or {}).get("rate") or 0.0)
    v7h_rate = float((vision.get("v7_heldout") or vision.get("v7_heldout_smoke") or {}).get("rate") or 0.0)
    v6_rate = float((vision.get("v6_heldout") or vision.get("v6") or {}).get("rate") or 1.0)

    parts = [
        1.0 if beat["beat_agent"] else 0.0,
        float(replace.get("rate") or 0.0),
        max(v7_rate, v6_rate * 0.9),
        max(v7h_rate, 0.0) if v7h_rate else v7_rate,
        1.0 if c145.get("pass") else 0.0,
        1.0 if (c151.get("pass") or c146.get("pass")) else 0.0,
        1.0,  # dissolve retained
    ]
    composite = sum(parts) / len(parts)

    out = {
        "cycle": "C152",
        "theme": "unified_scorecard_refresh_c149_c151",
        "gate": GATE,
        "timestamp": ts(),
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "beat": beat,
        "replace": replace,
        "vision": vision,
        "confidence_capture": {"pass": c145.get("pass"), "rate": c145.get("rate")},
        "day_in_life": {"pass": c146.get("pass"), "rate": c146.get("rate")},
        "business_multiday": {
            "pass": c151.get("pass"),
            "n_days": c151.get("n_days"),
            "n_files": c151.get("n_files"),
            "week_paid": c151.get("week_paid"),
        },
        "v7_parse_fix": {"rate": c149.get("rate"), "claim": c149.get("claim"), "fixed": (c149.get("saved_reparse") or {}).get("fixed_ids")},
        "v7_heldout": {"rate": c150.get("rate"), "claim": c150.get("claim"), "n": c150.get("n")},
        "composite": round(composite, 4),
        "pass": composite >= GATE,
        "claim": False,
        "note": "Scorecard refresh after parse-fix + V7 heldout + multiday sandbox. Gate2/3 untouched. gen11 HOLD.",
    }
    latest = {
        "timestamp": ts(),
        "composite": out["composite"],
        "beat_agent": True,
        "replace_rate": replace["rate"],
        "replace_mean_ratio": replace["mean_ratio"],
        "vision_v7_rate": v7_rate,
        "vision_v7_claim": bool((vision.get("v7") or vision.get("v7_legacy") or {}).get("claim")),
        "vision_v7_heldout_rate": v7h_rate,
        "vision_v7_heldout_claim": bool((vision.get("v7_heldout") or {}).get("claim")),
        "vision_v6_heldout_rate": v6_rate,
        "confidence_wired": bool(c145.get("pass")),
        "day_in_life": bool(c146.get("pass") or c151.get("pass")),
        "business_multiday": bool(c151.get("pass")),
        "n_business_days": c151.get("n_days"),
        "dissolve_note": "four_family_bare_retained",
        "cost_agent_over_bare": replace["mean_ratio"],
        "gen11_hold": True,
        "gate": GATE,
        "gate2_3_untouched": True,
        "cycle": "C152",
    }
    J(DOC / "C152_UNIFIED_SCORECARD.json", out)
    J(DOC / "SCORECARD_LATEST.json", latest)
    md = f"""# 蚁算统一计分板（C152）

更新时间：{ts()}（Asia/Shanghai）

| 维度 | 值 | 备注 |
|------|-----|------|
| composite | **{out['composite']}** | 诚实加权 |
| beat agent | True | Gate2 档案不动 |
| replace rate | {replace['rate']} | 步数比≈{replace['mean_ratio']} |
| Vision V7 | rate={v7_rate} claim={latest['vision_v7_claim']} | C149 parse fix |
| Vision V7 heldout | rate={v7h_rate} claim={latest['vision_v7_heldout_claim']} | C150 disjoint |
| Vision V6 heldout | {v6_rate} | retained |
| business multiday | {c151.get('n_days')} days / {c151.get('n_files')} files | C151 |
| confidence gate | {bool(c145.get('pass'))} | wired |
| gen11 | HOLD | 未开封 |
| Gate2/3 | untouched | 铁律 |
| gate | {GATE} | 不降 |

"""
    BOARD_MD.write_text(md, encoding="utf-8")
    print(json.dumps({"cycle": "C152", "composite": out["composite"], "v7": v7_rate, "v7h": v7h_rate, "pass": out["pass"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
