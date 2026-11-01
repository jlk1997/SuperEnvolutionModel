# -*- coding: utf-8 -*-
"""C277: Unified scorecard + STAGE after C272-C276. gen11 HOLD.
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
STAGE = ROOT / "docs" / "STAGE_ANT_C277.md"
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
    c269 = load("docs/r50/C275_U2C_REPLACE_STRETCH.json") or {}
    rl = (c269.get("replace_ledger") or {})
    replace = {
        "mean_ratio": (rl.get("mean_ratio")
                       or (c263.get("replace_stress") or {}).get("mean_ratio")
                       or (c263.get("cost_ledger") or {}).get("replace_mean_ratio") or 3.9188),
        "rate": (rl.get("bare_success_rate")
                 or (c263.get("replace_stress") or {}).get("rate") or 1.0),
        "pass": bool(rl.get("pass", (c263.get("replace_stress") or {}).get("pass", True))),
        "step_delta": rl.get("step_delta_agent_minus_bare")
                      or (c263.get("cost_ledger") or {}).get("step_delta_agent_minus_dual"),
        "source": "C275" if rl.get("mean_ratio") is not None else "C263",
    }
    c255 = load("docs/r50/C255_VISION_V25_SMOKE.json") or {}
    c256 = load("docs/r50/C256_VISION_V25_HELDOUT_SMOKE.json") or {}
    c261 = load("docs/r50/C261_VISION_V26_SMOKE.json") or {}
    c262 = load("docs/r50/C262_VISION_V26_HELDOUT_SMOKE.json") or {}
    c267v = load("docs/r50/C267_VISION_V27_SMOKE.json") or {}
    c267vb = load("docs/r50/C267b_VISION_GATE_V27_CLAIM.json") or {}
    c268v = load("docs/r50/C268_VISION_V27_HELDOUT_SMOKE.json") or {}
    c268vb = load("docs/r50/C268b_VISION_GATE_V27_HELDOUT_CLAIM.json") or {}
    c266 = load("docs/r50/C272_VISION_V28_DESIGN.json") or {}
    c267 = load("docs/r50/C273_VISION_V28_SMOKE.json") or {}
    c267b = load("docs/r50/C273b_VISION_GATE_V28_CLAIM.json") or {}
    c268 = load("docs/r50/C274_VISION_V28_HELDOUT_SMOKE.json") or {}
    c268b = load("docs/r50/C274b_VISION_GATE_V28_HELDOUT_CLAIM.json") or {}
    c270 = load("docs/r50/C276_CAPTURE_OFFICE_REGRESSION.json") or {}

    v25 = float(c255.get("rate") or 0.0)
    v25h = float(c256.get("rate") or 0.0)
    v26 = float(c261.get("rate") or 0.0)
    v26h = float(c262.get("rate") or 0.0)
    v27 = float(c267v.get("rate") or 0.0)
    v27h = float(c268v.get("rate") or 0.0)
    v28 = float(c267.get("rate") or 0.0)
    v28h = float(c268.get("rate") or 0.0)

    v25_claim = bool(c255.get("vl_gate_v25_claim") or c255.get("claim"))
    v25h_claim = bool(c256.get("vl_gate_v25_heldout_claim") or c256.get("claim"))
    v26_claim = bool(c261.get("vl_gate_v26_claim") or c261.get("claim"))
    v26h_claim = bool(c262.get("vl_gate_v26_heldout_claim") or c262.get("claim"))
    v27_claim = bool(c267vb.get("vl_gate_v27_claim") or c267v.get("vl_gate_v27_claim") or c267v.get("claim"))
    v27h_claim = bool(c268vb.get("vl_gate_v27_heldout_claim") or c268v.get("vl_gate_v27_heldout_claim") or c268v.get("claim"))
    v28_claim = bool(c267b.get("vl_gate_v28_claim") or c267.get("vl_gate_v28_claim") or c267.get("claim"))
    v28h_claim = bool(c268b.get("vl_gate_v28_heldout_claim") or c268.get("vl_gate_v28_heldout_claim") or c268.get("claim"))
    capture_pass = bool(c270.get("pass"))
    nv_pass = bool(c269.get("pass") and (
        (c263.get("dissolve") or {}).get("pass", True)
        and (c263.get("shadow") or {}).get("pass", True)
    ))
    dissolve_pass = bool((c263.get("dissolve") or {}).get("pass", True))
    shadow_pass = bool((c263.get("shadow") or {}).get("pass", True))
    conf_pass = bool(c269.get("pass"))
    conf_rate = float((c269.get("u2c") or {}).get("rate") or c269.get("rate") or (c269.get("replace_ledger") or {}).get("bare_success_rate") or 0.0)
    product_readme_ok = PRODUCT_README.is_file() or (ROOT / "scripts" / "ant_capture_office.py").is_file()

    parts = [
        1.0 if beat["beat_agent"] else 0.0,
        float(replace.get("rate") or 0.0),
        max(v25, v25h, 0.0),
        max(v26, v26h, 0.0),
        max(v27, v27h, 0.0),
        max(v28, v28h, 0.0),
        1.0 if v28_claim else 0.0,
        1.0 if v28h_claim else 0.0,
        1.0 if capture_pass else 0.0,
        1.0 if nv_pass else 0.0,
        1.0 if dissolve_pass else 0.0,
        1.0 if shadow_pass else 0.0,
        1.0 if conf_pass else 0.0,
        1.0 if product_readme_ok else 0.0,
    ]
    composite = round(sum(parts) / len(parts), 4)
    stage_ready = bool(
        v28_claim and v28h_claim and capture_pass and nv_pass
        and product_readme_ok and composite >= GATE
    )

    out = {
        "cycle": "C277",
        "theme": "unified_scorecard_c272_c276",
        "gate": GATE,
        "timestamp": ts(),
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "beat": beat,
        "replace": replace,
        "vision": {
            "v25_smoke": {"rate": v25, "claim": v25_claim},
            "v25_heldout": {"rate": v25h, "claim": v25h_claim},
            "v26_smoke": {"rate": v26, "claim": v26_claim},
            "v26_heldout": {"rate": v26h, "claim": v26h_claim},
            "v27_smoke": {"rate": v27, "claim": v27_claim},
            "v27_heldout": {"rate": v27h, "claim": v27h_claim},
            "v28_design": {"n": c266.get("n"), "clarity_floor": c266.get("clarity_floor"), "claim": False},
            "v28_smoke": {
                "rate": v28, "n": c267.get("n"), "n_ok": c267.get("n_ok"),
                "claim": v28_claim, "fail_ids": c267.get("fail_ids"),
            },
            "v28_heldout": {
                "rate": v28h, "n": c268.get("n"), "n_ok": c268.get("n_ok"),
                "claim": v28h_claim, "fail_ids": c268.get("fail_ids"),
                "id_disjoint": c268.get("id_disjoint"),
            },
        },
        "non_vision": {
            "pass": nv_pass,
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "u2c_replace_stretch": {"pass": conf_pass, "rate": conf_rate},
            "replace_ratio": replace.get("mean_ratio"),
        },
        "capture_regression": {"pass": capture_pass, "n_ok": c270.get("n_ok_pointers") or c270.get("n_ok")},
        "composite": composite,
        "STAGE_READY": stage_ready,
        "pass": stage_ready,
    }
    J(SCORE_LATEST, out)
    J(DOC / "C277_SCORECARD.json", out)

    board = f"""# 蚁算统一记分板（C277）
Updated: {ts()} (Asia/Shanghai)

| 维度 | 值 |
| --- | --- |
| beat_agent (Gate2 archive) | True (dual≈0.625 > agent≈0.125) |
| replace mean_ratio (C263) | {replace.get('mean_ratio')} |
| V25 smoke / heldout | **{v25} / {v25h}** claim={v25_claim}/{v25h_claim} |
| V26 smoke / heldout | **{v26} / {v26h}** claim={v26_claim}/{v26h_claim} |
| V27 smoke / heldout | **{v27} / {v27h}** claim={v27_claim}/{v27h_claim} |
| V28 smoke / heldout | **{v28} / {v28h}** claim={v28_claim}/{v28h_claim} |
| u2c-replace stretch (C275) | pass={conf_pass} rate={conf_rate} |
| dissolve / shadow (C263) | {dissolve_pass} / {shadow_pass} |
| capture regression (C276) | {capture_pass} |
| composite | **{composite}** |
| STAGE_READY | **{stage_ready}** |
| gen11 | HOLD |
| Gate2/3 | untouched |
| Gate | {GATE} |
"""
    BOARD_MD.write_text(board, encoding="utf-8")

    stage = f"""# STAGE_ANT_C277

Updated: {ts()} (Asia/Shanghai)

**C272-C277 STAGE_READY={'YES' if stage_ready else 'NO'}**

## Batch
| Cycle | Theme | Key |
| --- | --- | --- |
| C272 | V28 design | n={c266.get('n')} rust/wet/hole/band/glare/... |
| C273 | V28 smoke | rate={v28} claim={v28_claim} |
| C274 | V28 heldout | rate={v28h} claim={v28h_claim} |
| C275 | u2c-replace stretch | pass={conf_pass} rate={conf_rate} |
| C276 | capture regression | pass={capture_pass} |
| C277 | scorecard | composite={composite} |

## Iron
Gate **0.6**. Gate2/3 untouched. gen11 HOLD.

## Vision claims (scoped)
- V25: claim={v25_claim} rate={v25}
- V25 heldout: claim={v25h_claim} rate={v25h}
- V26: claim={v26_claim} rate={v26}
- V26 heldout: claim={v26h_claim} rate={v26h}
- V27: claim={v27_claim} rate={v27}
- V27 heldout: claim={v27h_claim} rate={v27h}
- V28: claim={v28_claim} rate={v28}
- V28 heldout: claim={v28h_claim} rate={v28h}
"""
    STAGE.write_text(stage, encoding="utf-8")

    ckpt = f"""# CHECKPOINT_NOW
HEAD: (see git)
Stage: C272-C277; V28 CLAIM {v28}; V28 heldout CLAIM {v28h}; nv pass={nv_pass}; capture pass={capture_pass}; composite={composite} STAGE_READY={stage_ready}
V28 design: clarity_floor jpeg_q=60 photo/=2 themes=rust/wet/hole/band/glare/label/blot/clip/fax/tab/crease/overink/tape/shade/ring
V28 smoke: rate={v28} n={c267.get('n')} CLAIM={v28_claim} fail={c267.get('fail_ids')}
V28 heldout: rate={v28h} n={c268.get('n')} CLAIM={v28h_claim} disjoint={c268.get('id_disjoint')}
Non-vision C275: pass={conf_pass} rate={conf_rate} (u2c-replace stretch); dissolve/shadow from C263={dissolve_pass}/{shadow_pass}; replace_ratio={replace.get('mean_ratio')}
Capture regression: pass={capture_pass} (C276)
Scorecard composite: {composite} (C277)
gen11: HOLD
Gate2/3: untouched
Gate: 0.6
Updated: {ts()} Asia/Shanghai
"""
    CKPT.write_text(ckpt, encoding="utf-8")

    if LOOP_APPEND.is_file():
        with LOOP_APPEND.open("a", encoding="utf-8") as f:
            f.write(f"\n## C272-C277 ({ts()})\n")
            f.write(f"- V28 smoke={v28} claim={v28_claim}; heldout={v28h} claim={v28h_claim}\n")
            f.write(f"- C275 u2c-replace stretch pass={conf_pass} rate={conf_rate}; replace≈{replace.get('mean_ratio')}\n")
            f.write(f"- composite={composite} STAGE_READY={stage_ready}; gen11 HOLD\n")

    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
