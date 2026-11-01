# -*- coding: utf-8 -*-
"""Patch copied c313 scorecard from c307 for V34 + dissolve C311."""
from pathlib import Path
import re

P = Path("scripts/c313_scorecard_and_stage.py")
t = P.read_text(encoding="utf-8")

# Basic renames
reps = [
    ("C307", "C313"),
    ("c302_c306", "c308_c312"),
    ("STAGE_ANT_C307.md", "STAGE_ANT_C313.md"),
    ("C302-C306", "C308-C312"),
    ("C302-C307", "C308-C313"),
    ("unified_scorecard_c302_c306", "unified_scorecard_c308_c312"),
    ("C306_CAPTURE_OFFICE_REGRESSION.json", "C312_CAPTURE_OFFICE_REGRESSION.json"),
]
for a, b in reps:
    t = t.replace(a, b)

# Insert V33 historical loads before current (which still point at V33 files) then retarget current to V34
old_cur = '''    c266 = load("docs/r50/C302_VISION_V33_DESIGN.json") or {}
    c267 = load("docs/r50/C303_VISION_V33_SMOKE.json") or {}
    c267b = load("docs/r50/C303b_VISION_GATE_V33_CLAIM.json") or {}
    c268 = load("docs/r50/C304_VISION_V33_HELDOUT_SMOKE.json") or {}
    c268b = load("docs/r50/C304b_VISION_GATE_V33_HELDOUT_CLAIM.json") or {}
    c270 = load("docs/r50/C312_CAPTURE_OFFICE_REGRESSION.json") or {}'''

new_cur = '''    c303v = load("docs/r50/C303_VISION_V33_SMOKE.json") or {}
    c303vb = load("docs/r50/C303b_VISION_GATE_V33_CLAIM.json") or {}
    c304v = load("docs/r50/C304_VISION_V33_HELDOUT_SMOKE.json") or {}
    c304vb = load("docs/r50/C304b_VISION_GATE_V33_HELDOUT_CLAIM.json") or {}
    c266 = load("docs/r50/C308_VISION_V34_DESIGN.json") or {}
    c267 = load("docs/r50/C309_VISION_V34_SMOKE.json") or {}
    c267b = load("docs/r50/C309b_VISION_GATE_V34_CLAIM.json") or {}
    c268 = load("docs/r50/C310_VISION_V34_HELDOUT_SMOKE.json") or {}
    c268b = load("docs/r50/C310b_VISION_GATE_V34_HELDOUT_CLAIM.json") or {}
    c270 = load("docs/r50/C312_CAPTURE_OFFICE_REGRESSION.json") or {}'''

if old_cur not in t:
    raise SystemExit("current load block missing")
t = t.replace(old_cur, new_cur)

# NV loads: primary dissolve C311
t = t.replace(
    'c269 = load("docs/r50/C305_CONFIDENCE_GATE_STRETCH.json") or {}\n'
    '    c299 = load("docs/r50/C299_PRODUCT_U2C_COST.json") or {}\n'
    '    c293 = load("docs/r50/C293_DISSOLVE_COST_SHADOW.json") or {}\n'
    '    c287 = load("docs/r50/C287_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c269 = load("docs/r50/C311_DISSOLVE_COST_SHADOW.json") or {}\n'
    '    c305 = load("docs/r50/C305_CONFIDENCE_GATE_STRETCH.json") or {}\n'
    '    c299 = load("docs/r50/C299_PRODUCT_U2C_COST.json") or {}\n'
    '    c293 = load("docs/r50/C293_DISSOLVE_COST_SHADOW.json") or {}\n'
    '    c287 = load("docs/r50/C287_CONFIDENCE_GATE_STRETCH.json") or {}',
)

# rates: keep v33 from hist, add v34 from current
t = t.replace(
    '''    v32 = float(c297v.get("rate") or 0.0)
    v32h = float(c298v.get("rate") or 0.0)
    v33 = float(c267.get("rate") or 0.0)
    v33h = float(c268.get("rate") or 0.0)''',
    '''    v32 = float(c297v.get("rate") or 0.0)
    v32h = float(c298v.get("rate") or 0.0)
    v33 = float(c303v.get("rate") or 0.0)
    v33h = float(c304v.get("rate") or 0.0)
    v34 = float(c267.get("rate") or 0.0)
    v34h = float(c268.get("rate") or 0.0)''',
)

t = t.replace(
    '''    v32_claim = bool(c297vb.get("vl_gate_v32_claim") or c297v.get("vl_gate_v32_claim") or c297v.get("claim"))
    v32h_claim = bool(c298vb.get("vl_gate_v32_heldout_claim") or c298v.get("vl_gate_v32_heldout_claim") or c298v.get("claim"))
    v33_claim = bool(c267b.get("vl_gate_v33_claim") or c267.get("vl_gate_v33_claim") or c267.get("claim"))
    v33h_claim = bool(c268b.get("vl_gate_v33_heldout_claim") or c268.get("vl_gate_v33_heldout_claim") or c268.get("claim"))''',
    '''    v32_claim = bool(c297vb.get("vl_gate_v32_claim") or c297v.get("vl_gate_v32_claim") or c297v.get("claim"))
    v32h_claim = bool(c298vb.get("vl_gate_v32_heldout_claim") or c298v.get("vl_gate_v32_heldout_claim") or c298v.get("claim"))
    v33_claim = bool(c303vb.get("vl_gate_v33_claim") or c303v.get("vl_gate_v33_claim") or c303v.get("claim"))
    v33h_claim = bool(c304vb.get("vl_gate_v33_heldout_claim") or c304v.get("vl_gate_v33_heldout_claim") or c304v.get("claim"))
    v34_claim = bool(c267b.get("vl_gate_v34_claim") or c267.get("vl_gate_v34_claim") or c267.get("claim"))
    v34h_claim = bool(c268b.get("vl_gate_v34_heldout_claim") or c268.get("vl_gate_v34_heldout_claim") or c268.get("claim"))''',
)

t = t.replace(
    '''    dissolve_pass = bool((c293.get("dissolve") or c263.get("dissolve") or {}).get("pass", True))
    shadow_pass = bool((c293.get("shadow") or c263.get("shadow") or {}).get("pass", True))
    nv_pass = bool(c269.get("pass"))
    conf_pass = bool(c269.get("pass") or c287.get("pass"))
    conf_rate = float(c269.get("rate") or c287.get("rate") or 0.0)
    u2c_rate = float((c299.get("u2c") or {}).get("rate") or c299.get("rate") or 0.0)
    dissolve_rate = float(((c293.get("dissolve") or {}).get("summary") or {}).get("n_families") or 4)''',
    '''    dissolve_pass = bool((c269.get("dissolve") or c293.get("dissolve") or {}).get("pass", True))
    shadow_pass = bool((c269.get("shadow") or c293.get("shadow") or {}).get("pass", True))
    nv_pass = bool(c269.get("pass") and dissolve_pass and shadow_pass)
    conf_pass = bool(c305.get("pass") or c287.get("pass"))
    conf_rate = float(c305.get("rate") or c287.get("rate") or 0.0)
    u2c_rate = float((c299.get("u2c") or {}).get("rate") or c299.get("rate") or 0.0)
    dissolve_rate = float(((c269.get("dissolve") or {}).get("summary") or {}).get("n_families") or 4)''',
)

t = t.replace(
    'rl = ((c299.get("replace_ledger") or {}) or (c293.get("replace_stress") or {}) or (c269.get("replace_ledger") or {}) or {})',
    'rl = ((c269.get("replace_stress") or {}) or (c299.get("replace_ledger") or {}) or (c293.get("replace_stress") or {}) or {})',
)
t = t.replace(
    '"source": "C299" if (c299.get("replace_ledger") or {}).get("mean_ratio") is not None else ("C293" if (c293.get("replace_stress") or {}).get("mean_ratio") is not None else "C263")',
    '"source": "C311" if (c269.get("replace_stress") or {}).get("mean_ratio") is not None else ("C299" if (c299.get("replace_ledger") or {}).get("mean_ratio") is not None else "C293")',
)

t = t.replace(
    '''        max(v33, v33h, 0.0),
        1.0 if v33_claim else 0.0,
        1.0 if v33h_claim else 0.0,''',
    '''        max(v33, v33h, 0.0),
        1.0 if v33_claim else 0.0,
        1.0 if v33h_claim else 0.0,
        max(v34, v34h, 0.0),
        1.0 if v34_claim else 0.0,
        1.0 if v34h_claim else 0.0,''',
)
t = t.replace(
    "v33_claim and v33h_claim and capture_pass and nv_pass",
    "v34_claim and v34h_claim and capture_pass and nv_pass",
)

# vision dict: retarget v33 keys to hist, add v34
t = t.replace(
    '''            "v33_design": {"n": c266.get("n"), "clarity_floor": c266.get("clarity_floor"), "claim": False},
            "v33_smoke": {"rate": v33, "n": c267.get("n"), "n_ok": c267.get("n_ok"), "claim": v33_claim, "fail_ids": c267.get("fail_ids")},
            "v33_heldout": {"rate": v33h, "n": c268.get("n"), "n_ok": c268.get("n_ok"), "claim": v33h_claim, "fail_ids": c268.get("fail_ids"), "id_disjoint": c268.get("id_disjoint")},''',
    '''            "v33_design": {"n": (load("docs/r50/C302_VISION_V33_DESIGN.json") or {}).get("n"), "clarity_floor": (load("docs/r50/C302_VISION_V33_DESIGN.json") or {}).get("clarity_floor"), "claim": False},
            "v33_smoke": {"rate": v33, "n": c303v.get("n"), "n_ok": c303v.get("n_ok"), "claim": v33_claim, "fail_ids": c303v.get("fail_ids")},
            "v33_heldout": {"rate": v33h, "n": c304v.get("n"), "n_ok": c304v.get("n_ok"), "claim": v33h_claim, "fail_ids": c304v.get("fail_ids"), "id_disjoint": c304v.get("id_disjoint")},
            "v34_design": {"n": c266.get("n"), "clarity_floor": c266.get("clarity_floor"), "claim": False},
            "v34_smoke": {"rate": v34, "n": c267.get("n"), "n_ok": c267.get("n_ok"), "claim": v34_claim, "fail_ids": c267.get("fail_ids")},
            "v34_heldout": {"rate": v34h, "n": c268.get("n"), "n_ok": c268.get("n_ok"), "claim": v34h_claim, "fail_ids": c268.get("fail_ids"), "id_disjoint": c268.get("id_disjoint")},''',
)

t = t.replace(
    '''            "confidence_gate_stretch": {"pass": conf_pass, "rate": conf_rate, "source": "C305"},
            "product_u2c_cost": {"pass": bool(c299.get("pass")), "rate": u2c_rate},
            "dissolve_cost_shadow": {"pass": bool(c293.get("pass")), "dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass},''',
    '''            "dissolve_cost_shadow": {"pass": nv_pass, "dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C311"},
            "confidence_gate_stretch": {"pass": conf_pass, "rate": conf_rate, "source": "C305"},
            "product_u2c_cost": {"pass": bool(c299.get("pass")), "rate": u2c_rate},''',
)

# STAGE / CHECKPOINT prose
t = t.replace(
    "| V33 smoke / heldout | **{v33} / {v33h}** claim={v33_claim}/{v33h_claim} |\n"
    "| confidence-gate (C305) | pass={nv_pass} rate={conf_rate} |\n"
    "| product/U2C (C299) | pass={bool(c299.get('pass'))} rate={u2c_rate} |\n"
    "| dissolve/shadow (C293) | dissolve={dissolve_pass} shadow={shadow_pass} |",
    "| V33 smoke / heldout | **{v33} / {v33h}** claim={v33_claim}/{v33h_claim} |\n"
    "| V34 smoke / heldout | **{v34} / {v34h}** claim={v34_claim}/{v34h_claim} |\n"
    "| dissolve/shadow (C311) | pass={nv_pass} dissolve={dissolve_pass} shadow={shadow_pass} |\n"
    "| confidence-gate (C305) | pass={conf_pass} rate={conf_rate} |\n"
    "| product/U2C (C299) | pass={bool(c299.get('pass'))} rate={u2c_rate} |",
)
t = t.replace(
    '''| C302 | V33 design | n={c266.get('n')} parchment/cork/canvas/rivet/... |
| C303 | V33 smoke | rate={v33} claim={v33_claim} |
| C304 | V33 heldout | rate={v33h} claim={v33h_claim} |
| C305 | confidence-gate | pass={nv_pass} rate={conf_rate} |
| C306 | capture regression | pass={capture_pass} |
| C307 | scorecard | composite={composite} |''',
    '''| C308 | V34 design | n={c266.get('n')} bamboo/slate/denim/brass/... |
| C309 | V34 smoke | rate={v34} claim={v34_claim} |
| C310 | V34 heldout | rate={v34h} claim={v34h_claim} |
| C311 | dissolve/shadow | pass={nv_pass} |
| C312 | capture regression | pass={capture_pass} |
| C313 | scorecard | composite={composite} |''',
)
# After C307->C313 blind replace, the table above may already say C313 for scorecard line in old string - handle both
t = t.replace(
    '''| C302 | V33 design | n={c266.get('n')} parchment/cork/canvas/rivet/... |
| C303 | V33 smoke | rate={v33} claim={v33_claim} |
| C304 | V33 heldout | rate={v33h} claim={v33h_claim} |
| C305 | confidence-gate | pass={nv_pass} rate={conf_rate} |
| C306 | capture regression | pass={capture_pass} |
| C313 | scorecard | composite={composite} |''',
    '''| C308 | V34 design | n={c266.get('n')} bamboo/slate/denim/brass/... |
| C309 | V34 smoke | rate={v34} claim={v34_claim} |
| C310 | V34 heldout | rate={v34h} claim={v34h_claim} |
| C311 | dissolve/shadow | pass={nv_pass} |
| C312 | capture regression | pass={capture_pass} |
| C313 | scorecard | composite={composite} |''',
)

t = t.replace(
    "- V33: claim={v33_claim} rate={v33}\n- V33 heldout: claim={v33h_claim} rate={v33h}",
    "- V33: claim={v33_claim} rate={v33}\n- V33 heldout: claim={v33h_claim} rate={v33h}\n"
    "- V34: claim={v34_claim} rate={v34}\n- V34 heldout: claim={v34h_claim} rate={v34h}",
)
t = t.replace(
    "Stage: C308-C313; V34 CLAIM {v33}; V34 heldout CLAIM {v33h}",  # if partial
    "Stage: C308-C313; V34 CLAIM {v34}; V34 heldout CLAIM {v34h}",
)
t = t.replace(
    "Stage: C302-C307; V33 CLAIM {v33}; V33 heldout CLAIM {v33h}",
    "Stage: C308-C313; V34 CLAIM {v34}; V34 heldout CLAIM {v34h}",
)
# After C302-C307 -> C308-C313 blind? We only replaced C302-C307 with C308-C313 earlier
t = t.replace(
    "Stage: C308-C313; V33 CLAIM {v33}; V33 heldout CLAIM {v33h}",
    "Stage: C308-C313; V34 CLAIM {v34}; V34 heldout CLAIM {v34h}",
)

t = t.replace(
    "V33 design: clarity_floor jpeg_q=60 photo/=2 themes=parchment/cork/canvas/rivet/holo/zip/filament/honey/marble/copper/acetate/perf/waxseal/magnet/crepe/satin/spiral",
    "V34 design: clarity_floor jpeg_q=60 photo/=2 themes=bamboo/slate/denim/brass/prism/latch/amber/quarry/tin/mylar/felt/stitch/enamel/cord/rice/chrome/index",
)
t = t.replace(
    "V33 smoke: rate={v33} n={c267.get('n')} CLAIM={v33_claim} fail={c267.get('fail_ids')}",
    "V34 smoke: rate={v34} n={c267.get('n')} CLAIM={v34_claim} fail={c267.get('fail_ids')}",
)
t = t.replace(
    "V33 heldout: rate={v33h} n={c268.get('n')} CLAIM={v33h_claim} disjoint={c268.get('id_disjoint')}",
    "V34 heldout: rate={v34h} n={c268.get('n')} CLAIM={v34h_claim} disjoint={c268.get('id_disjoint')}",
)
t = t.replace(
    "Non-vision C305: pass={nv_pass} rate={conf_rate} (confidence-gate); product C299={bool(c299.get('pass'))}/{u2c_rate}; dissolve C293={dissolve_pass}/{shadow_pass}; replace_ratio={replace.get('mean_ratio')}",
    "Non-vision C311: pass={nv_pass} (dissolve/shadow); conf-gate C305={conf_pass}/{conf_rate}; product C299={bool(c299.get('pass'))}/{u2c_rate}; replace_ratio={replace.get('mean_ratio')}",
)
t = t.replace("Capture regression: pass={capture_pass} (C306)", "Capture regression: pass={capture_pass} (C312)")
t = t.replace("Scorecard composite: {composite} (C313)", "Scorecard composite: {composite} (C313)")  # already
t = t.replace("Scorecard composite: {composite} (C307)", "Scorecard composite: {composite} (C313)")

t = t.replace(
    'f.write(f"- V33 smoke={v33} claim={v33_claim}; heldout={v33h} claim={v33h_claim}\\n")',
    'f.write(f"- V34 smoke={v34} claim={v34_claim}; heldout={v34h} claim={v34h_claim}\\n")',
)
t = t.replace(
    'f.write(f"- C305 conf-gate pass={nv_pass} rate={conf_rate}; product C299={u2c_rate}; replace',
    'f.write(f"- C311 dissolve/shadow pass={nv_pass}; conf-gate={conf_pass}/{conf_rate}; replace',
)

# sanity
assert "STAGE_ANT_C313.md" in t
assert "v34_claim" in t
assert "C311_DISSOLVE" in t or "C311_DISSOLVE_COST_SHADOW" in t
assert "C309_VISION_V34_SMOKE" in t
compile(t, str(P), "exec")
P.write_text(t, encoding="utf-8")
print("c313 score fixed")
