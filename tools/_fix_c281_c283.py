# -*- coding: utf-8 -*-
from pathlib import Path

p = Path("scripts/c281_product_u2c_cost.py")
t = p.read_text(encoding="utf-8")
t = t.replace("C281_U2C_REPLACE_STRETCH.json", "C281_PRODUCT_U2C_COST.json")
p.write_text(t, encoding="utf-8")
assert "C281_PRODUCT_U2C_COST.json" in p.read_text(encoding="utf-8")
print("c281 ok")

p = Path("scripts/c283_scorecard_and_stage.py")
t = p.read_text(encoding="utf-8")

t = t.replace('"rate": v28, "n": c267.get("n")', '"rate": v29, "n": c267.get("n")')
t = t.replace('"rate": v28h, "n": c268.get("n")', '"rate": v29h, "n": c268.get("n")')
t = t.replace(
    "Stage: C272-C283; V28 CLAIM {v28}; V29 heldout CLAIM {v28h}",
    "Stage: C278-C283; V29 CLAIM {v29}; V29 heldout CLAIM {v29h}",
)
t = t.replace("**C272-C283 STAGE_READY", "**C278-C283 STAGE_READY")
t = t.replace(
    'f"- V29 smoke={v28} claim={v29_claim}; heldout={v28h} claim={v29h_claim}\\n"',
    'f"- V29 smoke={v29} claim={v29_claim}; heldout={v29h} claim={v29h_claim}\\n"',
)

old = '    c268vb = load("docs/r50/C268b_VISION_GATE_V27_HELDOUT_CLAIM.json") or {}\n'
if old in t and "C273_VISION_V28_SMOKE" not in t:
    t = t.replace(
        old,
        old
        + '    c273v = load("docs/r50/C273_VISION_V28_SMOKE.json") or {}\n'
        + '    c273vb = load("docs/r50/C273b_VISION_GATE_V28_CLAIM.json") or {}\n'
        + '    c274v = load("docs/r50/C274_VISION_V28_HELDOUT_SMOKE.json") or {}\n'
        + '    c274vb = load("docs/r50/C274b_VISION_GATE_V28_HELDOUT_CLAIM.json") or {}\n',
    )
    print("injected v28 loads")

old = '    v27h = float(c268v.get("rate") or 0.0)\n'
if old in t and "v28s = float" not in t:
    t = t.replace(
        old,
        old
        + '    v28s = float(c273v.get("rate") or 0.0)\n'
        + '    v28h = float(c274v.get("rate") or 0.0)\n',
    )
    print("injected v28 rates")

old = '    v27h_claim = bool(c268vb.get("vl_gate_v27_heldout_claim") or c268v.get("vl_gate_v27_heldout_claim") or c268v.get("claim"))\n'
if old in t and "v28s_claim" not in t:
    t = t.replace(
        old,
        old
        + '    v28s_claim = bool(c273vb.get("vl_gate_v28_claim") or c273v.get("vl_gate_v28_claim") or c273v.get("claim"))\n'
        + '    v28h_claim = bool(c274vb.get("vl_gate_v28_heldout_claim") or c274v.get("vl_gate_v28_heldout_claim") or c274v.get("claim"))\n',
    )
    print("injected v28 claims")

if "max(v28s" not in t:
    t = t.replace(
        "        max(v29, v29h, 0.0),",
        "        max(v28s, v28h, 0.0),\n        max(v29, v29h, 0.0),",
    )

if '"v28_smoke"' not in t:
    t = t.replace(
        '            "v29_design":',
        '            "v28_smoke": {"rate": v28s, "claim": v28s_claim},\n'
        '            "v28_heldout": {"rate": v28h, "claim": v28h_claim},\n'
        '            "v29_design":',
    )

if "| V28 smoke" not in t:
    t = t.replace(
        "| V29 smoke / heldout |",
        "| V28 smoke / heldout | **{v28s} / {v28h}** claim={v28s_claim}/{v28h_claim} |\n| V29 smoke / heldout |",
    )

if "- V28: claim=" not in t:
    t = t.replace(
        "- V29: claim=",
        "- V28: claim={v28s_claim} rate={v28s}\n- V28 heldout: claim={v28h_claim} rate={v28h}\n- V29: claim=",
    )

p.write_text(t, encoding="utf-8")
tt = p.read_text(encoding="utf-8")
print("bad rate v28", '"rate": v28,' in tt)
print("v28s", "v28s = float" in tt)
print("product", "C281_PRODUCT_U2C_COST" in Path("scripts/c281_product_u2c_cost.py").read_text(encoding="utf-8"))
# compile check
compile(tt, "c283", "exec")
compile(Path("scripts/c278_vision_v29_design_and_batch.py").read_text(encoding="utf-8"), "c278", "exec")
compile(Path("scripts/c279_vision_v29_smoke.py").read_text(encoding="utf-8"), "c279", "exec")
compile(Path("scripts/c280_vision_v29_heldout.py").read_text(encoding="utf-8"), "c280", "exec")
compile(Path("scripts/c281_product_u2c_cost.py").read_text(encoding="utf-8"), "c281", "exec")
compile(Path("scripts/c282_capture_office_regression.py").read_text(encoding="utf-8"), "c282", "exec")
print("compile ok")
