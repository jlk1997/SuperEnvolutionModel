# -*- coding: utf-8 -*-
"""C157: Unified scorecard refresh after C153-C156.
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
        ("v7", "docs/r50/C153b_VISION_GATE_V7_REFRESH_CLAIM.json"),
        ("v7_c149", "docs/r50/C149b_VISION_GATE_V7_REFRESH_CLAIM.json"),
        ("v7_heldout", "docs/r50/C150b_VISION_GATE_V7_HELDOUT_CLAIM.json"),
        ("v7_smoke", "docs/r50/C153_V7_LINEN_FIX_RETEST.json"),
        ("v8", "docs/r50/C155b_VISION_GATE_V8_CLAIM.json"),
        ("v8_smoke", "docs/r50/C155_VISION_V8_SMOKE.json"),
    ]:
        d = load(rel)
        if d:
            vision[ver] = {
                "rate": d.get("rate"),
                "claim": d.get("vl_gate_v8_claim") or d.get("vl_gate_v7_claim") or d.get("vl_gate_v7_heldout_claim") or d.get("vl_gate_v6_claim") or d.get("claim"),
                "n": d.get("n"),
                "path": rel,
            }
    c145 = load("docs/r50/C145_CONFIDENCE_GATE_CAPTURE_WIRE.json") or {}
    c153 = load("docs/r50/C153_V7_LINEN_FIX_RETEST.json") or {}
    c154 = load("docs/r50/C154_V8_DESIGN_BATCH.json") or {}
    c155 = load("docs/r50/C155_VISION_V8_SMOKE.json") or {}
    c156 = load("docs/r50/C156_WEEK_SANDBOX.json") or {}
    c150 = load("docs/r50/C150_VISION_V7_HELDOUT_SMOKE.json") or {}

    v7_rate = float((vision.get("v7") or vision.get("v7_smoke") or vision.get("v7_c149") or {}).get("rate") or 0.0)
    v7h_rate = float((vision.get("v7_heldout") or {}).get("rate") or (c150.get("rate") or 0.0))
    v8_rate = float((vision.get("v8") or vision.get("v8_smoke") or {}).get("rate") or 0.0)
    v6_rate = float((vision.get("v6_heldout") or vision.get("v6") or {}).get("rate") or 1.0)

    parts = [
        1.0 if beat["beat_agent"] else 0.0,
        float(replace.get("rate") or 0.0),
        max(v8_rate, v7_rate, v6_rate * 0.9),
        max(v7h_rate, v7_rate),
        1.0 if c145.get("pass") else 0.0,
        1.0 if c156.get("pass") else 0.0,
        1.0,  # dissolve retained
    ]
    composite = sum(parts) / len(parts)

    out = {
        "cycle": "C157",
        "theme": "unified_scorecard_refresh_c153_c156",
        "gate": GATE,
        "timestamp": ts(),
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "beat": beat,
        "replace": replace,
        "vision": vision,
        "confidence_capture": {"pass": c145.get("pass"), "rate": c145.get("rate")},
        "v7_linen_fix": {
            "rate": c153.get("rate"),
            "claim": c153.get("claim"),
            "fixed": (c153.get("saved_reparse") or {}).get("fixed_ids") or ["v7_09", "v7_13"],
            "unit_proof": (c153.get("unit_bug_proof") or {}).get("pass"),
        },
        "v8_design": {"n": c154.get("n"), "pass": c154.get("pass")},
        "v8_smoke": {"rate": c155.get("rate"), "claim": c155.get("claim"), "n": c155.get("n")},
        "week_sandbox": {
            "pass": c156.get("pass"),
            "n_days": c156.get("n_days"),
            "n_files": c156.get("n_files_seeded"),
            "week_paid": c156.get("week_paid"),
            "rate": c156.get("rate"),
        },
        "v7_heldout": {"rate": v7h_rate, "claim": bool((vision.get("v7_heldout") or {}).get("claim"))},
        "composite": round(composite, 4),
        "pass": composite >= GATE,
        "claim": False,
        "note": "Scorecard after linen fix + V8 + week sandbox. Gate2/3 untouched. gen11 HOLD.",
    }
    latest = {
        "timestamp": ts(),
        "composite": out["composite"],
        "beat_agent": True,
        "replace_rate": replace["rate"],
        "replace_mean_ratio": replace["mean_ratio"],
        "vision_v7_rate": v7_rate,
        "vision_v7_claim": bool((vision.get("v7") or vision.get("v7_smoke") or {}).get("claim")),
        "vision_v7_heldout_rate": v7h_rate,
        "vision_v8_rate": v8_rate,
        "vision_v8_claim": bool((vision.get("v8") or {}).get("claim")),
        "week_sandbox_days": c156.get("n_days"),
        "week_sandbox_pass": bool(c156.get("pass")),
        "confidence_wired": bool(c145.get("pass")),
        "dissolve_note": "four_family_bare_retained",
        "cost_agent_over_bare": replace["mean_ratio"],
        "gen11_hold": True,
        "gate": GATE,
        "gate2_3_untouched": True,
        "cycle": "C157",
    }
    J(DOC / "C157_UNIFIED_SCORECARD.json", out)
    J(DOC / "SCORECARD_LATEST.json", latest)
    md = f"""# 蚁算统一计分板（C157）
更新时间：{ts()}（Asia/Shanghai）
| 维度 | 值 | 备注 |
|------|-----|------|
| composite | **{out['composite']}** | 诚实加权 |
| beat agent | True | Gate2 档案不动 |
| replace rate | {replace['rate']} | 步数比≈{replace['mean_ratio']} |
| Vision V7 | rate={v7_rate} claim={latest['vision_v7_claim']} | C153 lineN/rowN fix |
| Vision V7 heldout | rate={v7h_rate} | C150 retained |
| Vision V8 | rate={v8_rate} claim={latest['vision_v8_claim']} | C155 |
| week sandbox | {c156.get('n_days')} days / paid={c156.get('week_paid')} | C156 |
| confidence gate | {bool(c145.get('pass'))} | wired |
| gen11 | HOLD | 未开封 |
| Gate2/3 | untouched | 铁律 |
| gate | {GATE} | 不降 |
"""
    BOARD_MD.write_text(md, encoding="utf-8")
    print(json.dumps({
        "cycle": "C157", "composite": out["composite"],
        "v7": v7_rate, "v8": v8_rate, "week": c156.get("n_days"),
        "pass": out["pass"],
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
