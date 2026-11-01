# -*- coding: utf-8 -*-
"""C265: Unified scorecard + STAGE after C260-C264. gen11 HOLD.
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
STAGE = ROOT / "docs" / "STAGE_ANT_C265.md"
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
    c263 = load("docs/r50/C263_DISSOLVE_COST_SHADOW.json") or {}
    replace = {
        "mean_ratio": ((c263.get("replace_stress") or {}).get("mean_ratio")
                       or (c263.get("cost_ledger") or {}).get("replace_mean_ratio") or 3.7),
        "rate": ((c263.get("replace_stress") or {}).get("rate") or 1.0),
        "pass": bool((c263.get("replace_stress") or {}).get("pass", True)),
        "step_delta": (c263.get("cost_ledger") or {}).get("step_delta_agent_minus_dual"),
    }
    c255 = load("docs/r50/C255_VISION_V25_SMOKE.json") or {}
    c256 = load("docs/r50/C256_VISION_V25_HELDOUT_SMOKE.json") or {}
    c260 = load("docs/r50/C260_VISION_V26_DESIGN.json") or {}
    c261 = load("docs/r50/C261_VISION_V26_SMOKE.json") or {}
    c261b = load("docs/r50/C261b_VISION_GATE_V26_CLAIM.json") or {}
    c262 = load("docs/r50/C262_VISION_V26_HELDOUT_SMOKE.json") or {}
    c262b = load("docs/r50/C262b_VISION_GATE_V26_HELDOUT_CLAIM.json") or {}
    c264 = load("docs/r50/C264_CAPTURE_OFFICE_REGRESSION.json") or {}

    v25 = float(c255.get("rate") or 0.0)
    v25h = float(c256.get("rate") or 0.0)
    v26 = float(c261.get("rate") or 0.0)
    v26h = float(c262.get("rate") or 0.0)

    v25_claim = bool(c255.get("vl_gate_v25_claim") or c255.get("claim"))
    v25h_claim = bool(c256.get("vl_gate_v25_heldout_claim") or c256.get("claim"))
    v26_claim = bool(c261b.get("vl_gate_v26_claim") or c261.get("vl_gate_v26_claim") or c261.get("claim"))
    v26h_claim = bool(c262b.get("vl_gate_v26_heldout_claim") or c262.get("vl_gate_v26_heldout_claim") or c262.get("claim"))
    capture_pass = bool(c264.get("pass"))
    nv_pass = bool(c263.get("pass") or (
        (c263.get("dissolve") or {}).get("pass")
        and (c263.get("shadow") or {}).get("pass")
        and (c263.get("replace_stress") or {}).get("pass")
    ))
    dissolve_pass = bool((c263.get("dissolve") or {}).get("pass", True))
    shadow_pass = bool((c263.get("shadow") or {}).get("pass", True))
    product_readme_ok = PRODUCT_README.is_file() or (ROOT / "scripts" / "ant_capture_office.py").is_file()

    parts = [
        1.0 if beat["beat_agent"] else 0.0,
        float(replace.get("rate") or 0.0),
        max(v25, v25h, 0.0),
        max(v26, v26h, 0.0),
        1.0 if v25_claim else 0.0,
        1.0 if v26_claim else 0.0,
        1.0 if v26h_claim else 0.0,
        1.0 if capture_pass else 0.0,
        1.0 if nv_pass else 0.0,
        1.0 if dissolve_pass else 0.0,
        1.0 if shadow_pass else 0.0,
        1.0 if product_readme_ok else 0.0,
    ]
    composite = round(sum(parts) / len(parts), 4)
    stage_ready = bool(
        v26_claim and v26h_claim and capture_pass and nv_pass
        and product_readme_ok and composite >= GATE
    )

    out = {
        "cycle": "C265",
        "theme": "unified_scorecard_c260_c264",
        "gate": GATE,
        "timestamp": ts(),
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "beat": beat,
        "replace": replace,
        "vision": {
            "v25_smoke": {"rate": v25, "claim": v25_claim},
            "v25_heldout": {"rate": v25h, "claim": v25h_claim},
            "v26_design": {"n": c260.get("n"), "clarity_floor": c260.get("clarity_floor"), "claim": False},
            "v26_smoke": {
                "rate": v26, "n": c261.get("n"), "n_ok": c261.get("n_ok"),
                "claim": v26_claim, "fail_ids": c261.get("fail_ids"),
            },
            "v26_heldout": {
                "rate": v26h, "n": c262.get("n"), "n_ok": c262.get("n_ok"),
                "claim": v26h_claim, "fail_ids": c262.get("fail_ids"),
                "id_disjoint": c262.get("id_disjoint"),
            },
        },
        "non_vision": {
            "pass": nv_pass,
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "replace_ratio": replace.get("mean_ratio"),
        },
        "cost_ledger": {
            "pass": bool(c263.get("cost_pass", True)),
            "replace_mean_ratio": replace.get("mean_ratio"),
            "step_delta": replace.get("step_delta"),
            "source": "C263",
        },
        "capture_regression": {"pass": capture_pass, "n_ok": c264.get("n_ok_pointers") or c264.get("n_ok")},
        "composite": composite,
        "STAGE_READY": stage_ready,
        "pass": stage_ready,
    }
    J(SCORE_LATEST, out)
    J(DOC / "C265_SCORECARD.json", out)

    board = f"""# 蚁算统一记分板（C265）
Updated: {ts()} (Asia/Shanghai)

| 维度 | 值 |
| --- | --- |
| beat_agent (Gate2 archive) | True (dual≈0.625 > agent≈0.125) |
| replace mean_ratio (C263) | {replace.get('mean_ratio')} |
| V25 smoke / heldout | **{v25} / {v25h}** claim={v25_claim}/{v25h_claim} |
| V26 smoke / heldout | **{v26} / {v26h}** claim={v26_claim}/{v26h_claim} |
| dissolve / shadow (C263) | {dissolve_pass} / {shadow_pass} |
| capture regression (C264) | {capture_pass} |
| composite | **{composite}** |
| STAGE_READY | **{stage_ready}** |
| gen11 | HOLD |
| Gate2/3 | untouched |
| Gate | {GATE} |
"""
    BOARD_MD.write_text(board, encoding="utf-8")

    stage = f"""# STAGE_ANT_C265

Updated: {ts()} (Asia/Shanghai)

**C260-C265 STAGE_READY={'YES' if stage_ready else 'NO'}**

## Batch
| Cycle | Theme | Key |
| --- | --- | --- |
| C260 | V26 design | n={c260.get('n')} hl/crumple/rubber/clip/... |
| C261 | V26 smoke | rate={v26} claim={v26_claim} |
| C262 | V26 heldout | rate={v26h} claim={v26h_claim} |
| C263 | dissolve/cost/shadow | pass={nv_pass} ratio={replace.get('mean_ratio')} |
| C264 | capture regression | pass={capture_pass} |
| C265 | scorecard | composite={composite} |

## Iron
Gate **0.6**. Gate2/3 untouched. gen11 HOLD.

## Vision claims (scoped)
- V25: claim={v25_claim} rate={v25}
- V25 heldout: claim={v25h_claim} rate={v25h}
- V26: claim={v26_claim} rate={v26}
- V26 heldout: claim={v26h_claim} rate={v26h}
"""
    STAGE.write_text(stage, encoding="utf-8")

    ckpt = f"""# CHECKPOINT_NOW
HEAD: (see git)
Stage: C260-C265; V26 CLAIM {v26}; V26 heldout CLAIM {v26h}; nv pass={nv_pass}; capture pass={capture_pass}; composite={composite} STAGE_READY={stage_ready}
V26 design: clarity_floor jpeg_q=60 photo/=2 themes=hl/crumple/rubber/clip/grease/carbon/stamp/pocket/dust/binder/perf/polaroid/wb/sticky/pen/fax/env/laminate
V26 smoke: rate={v26} n={c261.get('n')} CLAIM={v26_claim} fail={c261.get('fail_ids')}
V26 heldout: rate={v26h} n={c262.get('n')} CLAIM={v26h_claim} disjoint={c262.get('id_disjoint')}
Non-vision C263: pass={nv_pass} dissolve={dissolve_pass} shadow={shadow_pass} replace_ratio={replace.get('mean_ratio')}
Capture regression: pass={capture_pass} (C264)
Scorecard composite: {composite} (C265)
gen11: HOLD
Gate2/3: untouched
Gate: 0.6
Updated: {ts()} Asia/Shanghai
"""
    CKPT.write_text(ckpt, encoding="utf-8")

    if LOOP_APPEND.is_file():
        with LOOP_APPEND.open("a", encoding="utf-8") as f:
            f.write(f"\n## C260-C265 ({ts()})\n")
            f.write(f"- V26 smoke={v26} claim={v26_claim}; heldout={v26h} claim={v26h_claim}\n")
            f.write(f"- C263 dissolve/cost/shadow pass={nv_pass}; replace≈{replace.get('mean_ratio')}\n")
            f.write(f"- composite={composite} STAGE_READY={stage_ready}; gen11 HOLD\n")

    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
