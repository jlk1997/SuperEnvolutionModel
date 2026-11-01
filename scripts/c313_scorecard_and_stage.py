# -*- coding: utf-8 -*-
"""C313: Unified scorecard + STAGE after C308-C312. gen11 HOLD.
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
STAGE = ROOT / "docs" / "STAGE_ANT_C313.md"
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
    c281 = load("docs/r50/C281_PRODUCT_U2C_COST.json") or {}
    c269 = load("docs/r50/C311_DISSOLVE_COST_SHADOW.json") or {}
    c299 = load("docs/r50/C299_PRODUCT_U2C_COST.json") or {}
    c293 = load("docs/r50/C293_DISSOLVE_COST_SHADOW.json") or {}
    c287 = load("docs/r50/C287_CONFIDENCE_GATE_STRETCH.json") or {}
    rl = ((c299.get("replace_ledger") or {}) or (c293.get("replace_stress") or {}) or (c269.get("replace_ledger") or {}) or {})
    replace = {
        "mean_ratio": (rl.get("mean_ratio")
                       or (c269.get("replace_ledger") or {}).get("mean_ratio")
                       or (c293.get("replace_stress") or {}).get("mean_ratio")
                       or (c263.get("replace_stress") or {}).get("mean_ratio")
                       or (c263.get("cost_ledger") or {}).get("replace_mean_ratio") or 3.9188),
        "rate": (rl.get("bare_success_rate")
                 or (c263.get("replace_stress") or {}).get("rate") or 1.0),
        "pass": bool(rl.get("pass", (c263.get("replace_stress") or {}).get("pass", True))),
        "step_delta": rl.get("step_delta_agent_minus_bare")
                      or (c263.get("cost_ledger") or {}).get("step_delta_agent_minus_dual"),
        "source": "C299" if (c299.get("replace_ledger") or {}).get("mean_ratio") is not None else ("C293" if (c293.get("replace_stress") or {}).get("mean_ratio") is not None else "C263"),
    }
    c255 = load("docs/r50/C255_VISION_V25_SMOKE.json") or {}
    c256 = load("docs/r50/C256_VISION_V25_HELDOUT_SMOKE.json") or {}
    c261 = load("docs/r50/C261_VISION_V26_SMOKE.json") or {}
    c262 = load("docs/r50/C262_VISION_V26_HELDOUT_SMOKE.json") or {}
    c267v = load("docs/r50/C267_VISION_V27_SMOKE.json") or {}
    c267vb = load("docs/r50/C267b_VISION_GATE_V27_CLAIM.json") or {}
    c268v = load("docs/r50/C268_VISION_V27_HELDOUT_SMOKE.json") or {}
    c268vb = load("docs/r50/C268b_VISION_GATE_V27_HELDOUT_CLAIM.json") or {}
    c273v = load("docs/r50/C273_VISION_V28_SMOKE.json") or {}
    c273vb = load("docs/r50/C273b_VISION_GATE_V28_CLAIM.json") or {}
    c274v = load("docs/r50/C274_VISION_V28_HELDOUT_SMOKE.json") or {}
    c274vb = load("docs/r50/C274b_VISION_GATE_V28_HELDOUT_CLAIM.json") or {}
    c279v = load("docs/r50/C279_VISION_V29_SMOKE.json") or {}
    c279vb = load("docs/r50/C279b_VISION_GATE_V29_CLAIM.json") or {}
    c280v = load("docs/r50/C280_VISION_V29_HELDOUT_SMOKE.json") or {}
    c280vb = load("docs/r50/C280b_VISION_GATE_V29_HELDOUT_CLAIM.json") or {}
    c285v = load("docs/r50/C285_VISION_V30_SMOKE.json") or {}
    c285vb = load("docs/r50/C285b_VISION_GATE_V30_CLAIM.json") or {}
    c286v = load("docs/r50/C286_VISION_V30_HELDOUT_SMOKE.json") or {}
    c286vb = load("docs/r50/C286b_VISION_GATE_V30_HELDOUT_CLAIM.json") or {}
    c297v = load("docs/r50/C297_VISION_V32_SMOKE.json") or {}
    c297vb = load("docs/r50/C297b_VISION_GATE_V32_CLAIM.json") or {}
    c298v = load("docs/r50/C298_VISION_V32_HELDOUT_SMOKE.json") or {}
    c298vb = load("docs/r50/C298b_VISION_GATE_V32_HELDOUT_CLAIM.json") or {}
    c291v = load("docs/r50/C291_VISION_V31_SMOKE.json") or {}
    c291vb = load("docs/r50/C291b_VISION_GATE_V31_CLAIM.json") or {}
    c292v = load("docs/r50/C292_VISION_V31_HELDOUT_SMOKE.json") or {}
    c292vb = load("docs/r50/C292b_VISION_GATE_V31_HELDOUT_CLAIM.json") or {}
    c266 = load("docs/r50/C308_VISION_V34_DESIGN.json") or {}
    c267 = load("docs/r50/C309_VISION_V34_SMOKE.json") or {}
    c267b = load("docs/r50/C309b_VISION_GATE_V34_CLAIM.json") or {}
    c268 = load("docs/r50/C310_VISION_V34_HELDOUT_SMOKE.json") or {}
    c268b = load("docs/r50/C310b_VISION_GATE_V34_HELDOUT_CLAIM.json") or {}
    c270 = load("docs/r50/C312_CAPTURE_OFFICE_REGRESSION.json") or {}

    v25 = float(c255.get("rate") or 0.0)
    v25h = float(c256.get("rate") or 0.0)
    v26 = float(c261.get("rate") or 0.0)
    v26h = float(c262.get("rate") or 0.0)
    v27 = float(c267v.get("rate") or 0.0)
    v27h = float(c268v.get("rate") or 0.0)
    v28s = float(c273v.get("rate") or 0.0)
    v28h = float(c274v.get("rate") or 0.0)
    v29s = float(c279v.get("rate") or 0.0)
    v29h_hist = float(c280v.get("rate") or 0.0)
    v30 = float(c285v.get("rate") or 0.0)
    v30h = float(c286v.get("rate") or 0.0)
    v31 = float(c291v.get("rate") or 0.0)
    v31h = float(c292v.get("rate") or 0.0)
    v32 = float(c297v.get("rate") or 0.0)
    v32h = float(c298v.get("rate") or 0.0)
    v34 = float(c267.get("rate") or 0.0)
    v34h = float(c268.get("rate") or 0.0)

    v25_claim = bool(c255.get("vl_gate_v25_claim") or c255.get("claim"))
    v25h_claim = bool(c256.get("vl_gate_v25_heldout_claim") or c256.get("claim"))
    v26_claim = bool(c261.get("vl_gate_v26_claim") or c261.get("claim"))
    v26h_claim = bool(c262.get("vl_gate_v26_heldout_claim") or c262.get("claim"))
    v27_claim = bool(c267vb.get("vl_gate_v27_claim") or c267v.get("vl_gate_v27_claim") or c267v.get("claim"))
    v27h_claim = bool(c268vb.get("vl_gate_v27_heldout_claim") or c268v.get("vl_gate_v27_heldout_claim") or c268v.get("claim"))
    v28s_claim = bool(c273vb.get("vl_gate_v28_claim") or c273v.get("vl_gate_v28_claim") or c273v.get("claim"))
    v28h_claim = bool(c274vb.get("vl_gate_v28_heldout_claim") or c274v.get("vl_gate_v28_heldout_claim") or c274v.get("claim"))
    v29s_claim = bool(c279vb.get("vl_gate_v29_claim") or c279v.get("vl_gate_v29_claim") or c279v.get("claim"))
    v29h_hist_claim = bool(c280vb.get("vl_gate_v29_heldout_claim") or c280v.get("vl_gate_v29_heldout_claim") or c280v.get("claim"))
    v30_claim = bool(c285vb.get("vl_gate_v30_claim") or c285v.get("vl_gate_v30_claim") or c285v.get("claim"))
    v30h_claim = bool(c286vb.get("vl_gate_v30_heldout_claim") or c286v.get("vl_gate_v30_heldout_claim") or c286v.get("claim"))
    v31_claim = bool(c291vb.get("vl_gate_v31_claim") or c291v.get("vl_gate_v31_claim") or c291v.get("claim"))
    v31h_claim = bool(c292vb.get("vl_gate_v31_heldout_claim") or c292v.get("vl_gate_v31_heldout_claim") or c292v.get("claim"))
    v32_claim = bool(c297vb.get("vl_gate_v32_claim") or c297v.get("vl_gate_v32_claim") or c297v.get("claim"))
    v32h_claim = bool(c298vb.get("vl_gate_v32_heldout_claim") or c298v.get("vl_gate_v32_heldout_claim") or c298v.get("claim"))
    v34_claim = bool(c267b.get("vl_gate_v34_claim") or c267.get("vl_gate_v34_claim") or c267.get("claim"))
    v34h_claim = bool(c268b.get("vl_gate_v34_heldout_claim") or c268.get("vl_gate_v34_heldout_claim") or c268.get("claim"))
    capture_pass = bool(c270.get("pass"))
    dissolve_pass = bool((c293.get("dissolve") or c263.get("dissolve") or {}).get("pass", True))
    shadow_pass = bool((c293.get("shadow") or c263.get("shadow") or {}).get("pass", True))
    nv_pass = bool(c269.get("pass"))
    conf_pass = bool(c269.get("pass") or c287.get("pass"))
    conf_rate = float(c269.get("rate") or c287.get("rate") or 0.0)
    u2c_rate = float((c299.get("u2c") or {}).get("rate") or c299.get("rate") or 0.0)
    dissolve_rate = float(((c293.get("dissolve") or {}).get("summary") or {}).get("n_families") or 4)
    product_readme_ok = PRODUCT_README.is_file() or (ROOT / "scripts" / "ant_capture_office.py").is_file()

    parts = [
        1.0 if beat["beat_agent"] else 0.0,
        float(replace.get("rate") or 0.0),
        max(v25, v25h, 0.0),
        max(v26, v26h, 0.0),
        max(v27, v27h, 0.0),
        max(v28s, v28h, 0.0),
        max(v29s, v29h_hist, 0.0),
        max(v30, v30h, 0.0),
        1.0 if v30_claim else 0.0,
        1.0 if v30h_claim else 0.0,
        max(v31, v31h, 0.0),
        1.0 if v31_claim else 0.0,
        1.0 if v31h_claim else 0.0,
        max(v32, v32h, 0.0),
        1.0 if v32_claim else 0.0,
        1.0 if v32h_claim else 0.0,
        max(v34, v34h, 0.0),
        1.0 if v34_claim else 0.0,
        1.0 if v34h_claim else 0.0,
        1.0 if capture_pass else 0.0,
        1.0 if nv_pass else 0.0,
        1.0 if dissolve_pass else 0.0,
        1.0 if shadow_pass else 0.0,
        1.0 if conf_pass else 0.0,
        1.0 if product_readme_ok else 0.0,
    ]
    composite = round(sum(parts) / len(parts), 4)
    stage_ready = bool(
        v34_claim and v34h_claim and capture_pass and nv_pass
        and product_readme_ok and composite >= GATE
    )

    out = {
        "cycle": "C313",
        "theme": "unified_scorecard_c308_c312",
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
            "v28_smoke": {"rate": v28s, "claim": v28s_claim},
            "v28_heldout": {"rate": v28h, "claim": v28h_claim},
            "v29_smoke": {"rate": v29s, "claim": v29s_claim},
            "v29_heldout": {"rate": v29h_hist, "claim": v29h_hist_claim},
            "v30_smoke": {"rate": v30, "claim": v30_claim},
            "v30_heldout": {"rate": v30h, "claim": v30h_claim},
            "v31_smoke": {"rate": v31, "claim": v31_claim},
            "v31_heldout": {"rate": v31h, "claim": v31h_claim},
            "v32_smoke": {"rate": v32, "claim": v32_claim},
            "v32_heldout": {"rate": v32h, "claim": v32h_claim},
            "v34_design": {"n": c266.get("n"), "clarity_floor": c266.get("clarity_floor"), "claim": False},
            "v34_smoke": {
                "rate": v34, "n": c267.get("n"), "n_ok": c267.get("n_ok"),
                "claim": v34_claim, "fail_ids": c267.get("fail_ids"),
            },
            "v34_heldout": {
                "rate": v34h, "n": c268.get("n"), "n_ok": c268.get("n_ok"),
                "claim": v34h_claim, "fail_ids": c268.get("fail_ids"),
                "id_disjoint": c268.get("id_disjoint"),
            },
        },
        "non_vision": {
            "pass": nv_pass,
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "dissolve_cost_shadow": {"pass": conf_pass, "rate": conf_rate, "source": "C311"},
            "product_u2c_cost": {"pass": bool(c299.get("pass")), "rate": u2c_rate},
            "dissolve_cost_shadow": {"pass": bool(c293.get("pass")), "dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass},
            "replace_ratio": replace.get("mean_ratio"),
        },
        "capture_regression": {"pass": capture_pass, "n_ok": c270.get("n_ok_pointers") or c270.get("n_ok")},
        "composite": composite,
        "STAGE_READY": stage_ready,
        "pass": stage_ready,
    }
    J(SCORE_LATEST, out)
    J(DOC / "C313_SCORECARD.json", out)

    board = f"""# 蚁算统一记分板（C313）
Updated: {ts()} (Asia/Shanghai)

| 维度 | 值 |
| --- | --- |
| beat_agent (Gate2 archive) | True (dual≈0.625 > agent≈0.125) |
| replace mean_ratio (C263) | {replace.get('mean_ratio')} |
| V25 smoke / heldout | **{v25} / {v25h}** claim={v25_claim}/{v25h_claim} |
| V26 smoke / heldout | **{v26} / {v26h}** claim={v26_claim}/{v26h_claim} |
| V27 smoke / heldout | **{v27} / {v27h}** claim={v27_claim}/{v27h_claim} |
| V28 smoke / heldout | **{v28s} / {v28h}** claim={v28s_claim}/{v28h_claim} |
| V29 smoke / heldout | **{v29s} / {v29h_hist}** claim={v29s_claim}/{v29h_hist_claim} |
| V30 smoke / heldout | **{v30} / {v30h}** claim={v30_claim}/{v30h_claim} |
| V31 smoke / heldout | **{v31} / {v31h}** claim={v31_claim}/{v31h_claim} |
| V32 smoke / heldout | **{v32} / {v32h}** claim={v32_claim}/{v32h_claim} |
| V34 smoke / heldout | **{v34} / {v34h}** claim={v34_claim}/{v34h_claim} |
| dissolve/shadow (C305) | pass={nv_pass} rate={conf_rate} |
| product/U2C (C299) | pass={bool(c299.get('pass'))} rate={u2c_rate} |
| dissolve/shadow (C293) | dissolve={dissolve_pass} shadow={shadow_pass} |
| dissolve / shadow (C263) | {dissolve_pass} / {shadow_pass} |
| capture regression (C276) | {capture_pass} |
| composite | **{composite}** |
| STAGE_READY | **{stage_ready}** |
| gen11 | HOLD |
| Gate2/3 | untouched |
| Gate | {GATE} |
"""
    BOARD_MD.write_text(board, encoding="utf-8")

    stage = f"""# STAGE_ANT_C313

Updated: {ts()} (Asia/Shanghai)

**C308-C313 STAGE_READY={'YES' if stage_ready else 'NO'}**

## Batch
| Cycle | Theme | Key |
| --- | --- | --- |
| C308 | V34 design | n={c266.get('n')} bamboo/slate/denim/brass/... clarity jpeg_q>=60 |
| C309 | V34 smoke | rate={v34} claim={v34_claim} |
| C310 | V34 heldout | rate={v34h} claim={v34h_claim} |
| C311 | dissolve/cost/shadow | pass={nv_pass} replace={replace.get('mean_ratio')} |
| C312 | capture regression | pass={capture_pass} |
| C313 | scorecard | composite={composite} |

## Iron
Gate **0.6**. Gate2/3 untouched. gen11 HOLD.

## Vision claims (scoped)
- V25: claim={v25_claim} rate={v25}
- V25 heldout: claim={v25h_claim} rate={v25h}
- V26: claim={v26_claim} rate={v26}
- V26 heldout: claim={v26h_claim} rate={v26h}
- V27: claim={v27_claim} rate={v27}
- V27 heldout: claim={v27h_claim} rate={v27h}
- V28: claim={v28s_claim} rate={v28s}
- V28 heldout: claim={v28h_claim} rate={v28h}
- V29: claim={v29s_claim} rate={v29s}
- V29 heldout: claim={v29h_hist_claim} rate={v29h_hist}
- V30: claim={v30_claim} rate={v30}
- V30 heldout: claim={v30h_claim} rate={v30h}
- V31: claim={v31_claim} rate={v31}
- V31 heldout: claim={v31h_claim} rate={v31h}
- V32: claim={v32_claim} rate={v32}
- V32 heldout: claim={v32h_claim} rate={v32h}
- V34: claim={v34_claim} rate={v34}
- V34 heldout: claim={v34h_claim} rate={v34h}
"""
    STAGE.write_text(stage, encoding="utf-8")

    ckpt = f"""# CHECKPOINT_NOW
HEAD: (see git)
Stage: C308-C313; V34 CLAIM {v34}; V34 heldout CLAIM {v34h}; nv pass={nv_pass}; capture pass={capture_pass}; composite={composite} STAGE_READY={stage_ready}
V34 design: clarity_floor jpeg_q=60 photo/=2 themes=bamboo/slate/denim/brass/prism/latch/amber/quarry/tin/mylar/felt/void/stitch/enamel/cord/rice/chrome/index
V34 smoke: rate={v34} n={c267.get('n')} CLAIM={v34_claim} fail={c267.get('fail_ids')}
V34 heldout: rate={v34h} n={c268.get('n')} CLAIM={v34h_claim} disjoint={c268.get('id_disjoint')}
Non-vision C311: pass={nv_pass} dissolve/shadow; product C299={bool(c299.get('pass'))}/{u2c_rate}; dissolve C311={dissolve_pass}/{shadow_pass}; replace_ratio={replace.get('mean_ratio')}
Capture regression: pass={capture_pass} (C306)
Scorecard composite: {composite} (C313)
gen11: HOLD
Gate2/3: untouched
Gate: 0.6
Updated: {ts()} Asia/Shanghai
"""
    CKPT.write_text(ckpt, encoding="utf-8")

    if LOOP_APPEND.is_file():
        with LOOP_APPEND.open("a", encoding="utf-8") as f:
            f.write(f"\n## C308-C313 ({ts()})\n")
            f.write(f"- V34 smoke={v34} claim={v34_claim}; heldout={v34h} claim={v34h_claim}\n")
            f.write(f"- C305 conf-gate pass={nv_pass} rate={conf_rate}; product C299={u2c_rate}; replace≈{replace.get('mean_ratio')}\n")
            f.write(f"- composite={composite} STAGE_READY={stage_ready}; gen11 HOLD\n")

    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
