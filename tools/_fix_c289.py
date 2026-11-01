# -*- coding: utf-8 -*-
from pathlib import Path

p = Path("scripts/c289_scorecard_and_stage.py")
t = p.read_text(encoding="utf-8")

# Fix leftover v29/v29h variable refs that should be v30/v30h
t = t.replace('"rate": v29, "n": c267.get("n")', '"rate": v30, "n": c267.get("n")')
t = t.replace('"rate": v29h, "n": c268.get("n")', '"rate": v30h, "n": c268.get("n")')
t = t.replace(
    "Stage: C278-C289; V29 CLAIM {v29}; V30 heldout CLAIM {v29h}",
    "Stage: C284-C289; V30 CLAIM {v30}; V30 heldout CLAIM {v30h}",
)
t = t.replace("**C278-C289 STAGE_READY", "**C284-C289 STAGE_READY")
t = t.replace(
    'f"- V30 smoke={v29} claim={v30_claim}; heldout={v29h} claim={v30h_claim}\\n"',
    'f"- V30 smoke={v30} claim={v30_claim}; heldout={v30h} claim={v30h_claim}\\n"',
)
t = t.replace("| C287 | u2c-replace stretch |", "| C287 | confidence-gate stretch |")
t = t.replace(
    "n={c266.get('n')} rust/wet/hole/band/glare/...",
    "n={c266.get('n')} velvet/spiral/mimeo/ribbon/neon/...",
)

# Inject V29 history loads if missing
old = '    c274vb = load("docs/r50/C274b_VISION_GATE_V28_HELDOUT_CLAIM.json") or {}\n'
if old in t and "C279_VISION_V29_SMOKE" not in t:
    t = t.replace(
        old,
        old
        + '    c279v = load("docs/r50/C279_VISION_V29_SMOKE.json") or {}\n'
        + '    c279vb = load("docs/r50/C279b_VISION_GATE_V29_CLAIM.json") or {}\n'
        + '    c280v = load("docs/r50/C280_VISION_V29_HELDOUT_SMOKE.json") or {}\n'
        + '    c280vb = load("docs/r50/C280b_VISION_GATE_V29_HELDOUT_CLAIM.json") or {}\n',
    )

old = '    v28h = float(c274v.get("rate") or 0.0)\n'
if old in t and "v29s = float" not in t:
    t = t.replace(
        old,
        old
        + '    v29s = float(c279v.get("rate") or 0.0)\n'
        + '    v29h_hist = float(c280v.get("rate") or 0.0)\n',
    )

old = '    v28h_claim = bool(c274vb.get("vl_gate_v28_heldout_claim") or c274v.get("vl_gate_v28_heldout_claim") or c274v.get("claim"))\n'
if old in t and "v29s_claim" not in t:
    t = t.replace(
        old,
        old
        + '    v29s_claim = bool(c279vb.get("vl_gate_v29_claim") or c279v.get("vl_gate_v29_claim") or c279v.get("claim"))\n'
        + '    v29h_hist_claim = bool(c280vb.get("vl_gate_v29_heldout_claim") or c280v.get("vl_gate_v29_heldout_claim") or c280v.get("claim"))\n',
    )

if "max(v29s" not in t:
    t = t.replace(
        "        max(v28s, v28h, 0.0),\n        max(v30, v30h, 0.0),",
        "        max(v28s, v28h, 0.0),\n        max(v29s, v29h_hist, 0.0),\n        max(v30, v30h, 0.0),",
    )

if '"v29_smoke"' not in t:
    t = t.replace(
        '            "v30_design":',
        '            "v29_smoke": {"rate": v29s, "claim": v29s_claim},\n'
        '            "v29_heldout": {"rate": v29h_hist, "claim": v29h_hist_claim},\n'
        '            "v30_design":',
    )

if "| V29 smoke" not in t:
    t = t.replace(
        "| V30 smoke / heldout |",
        "| V29 smoke / heldout | **{v29s} / {v29h_hist}** claim={v29s_claim}/{v29h_hist_claim} |\n| V30 smoke / heldout |",
    )

if "- V29: claim=" not in t:
    t = t.replace(
        "- V30: claim=",
        "- V29: claim={v29s_claim} rate={v29s}\n- V29 heldout: claim={v29h_hist_claim} rate={v29h_hist}\n- V30: claim=",
    )

# Fix checkpoint theme text
t = t.replace(
    "V30 design: clarity_floor jpeg_q=60 photo/=2 themes=rust/wet/hole/band/glare/label/blot/clip/fax/tab/crease/overink/tape/shade/ring",
    "V30 design: clarity_floor jpeg_q=60 photo/=2 themes=velvet/spiral/mimeo/ribbon/neon/holo/lacquer/rivet/concertina/serrate/triptych/washi/inkjet/redink/bulldog/corner",
)
t = t.replace(
    "Non-vision C275: pass={conf_pass} rate={conf_rate} (u2c-replace stretch)",
    "Non-vision C287: pass={conf_pass} rate={conf_rate} (confidence-gate stretch)",
)
t = t.replace("Capture regression: pass={capture_pass} (C276)", "Capture regression: pass={capture_pass} (C288)")
t = t.replace(
    'f"- C275 u2c-replace stretch pass={conf_pass} rate={conf_rate}; replace≈{replace.get(\'mean_ratio\')}\\n"',
    'f"- C287 confidence-gate stretch pass={conf_pass} rate={conf_rate}; replace≈{replace.get(\'mean_ratio\')}\\n"',
)
# also fix garbled approx char variants
import re
t = re.sub(
    r'f"- C275 u2c-replace stretch pass=\{conf_pass\} rate=\{conf_rate\}; replace.*?\\n"',
    'f"- C287 confidence-gate stretch pass={conf_pass} rate={conf_rate}; replace≈{replace.get(\'mean_ratio\')}\\n"',
    t,
)

p.write_text(t, encoding="utf-8")
tt = p.read_text(encoding="utf-8")
compile(tt, "c289", "exec")
for name in [
    "c284_vision_v30_design_and_batch.py",
    "c285_vision_v30_smoke.py",
    "c286_vision_v30_heldout.py",
    "c287_confidence_gate_stretch.py",
    "c288_capture_office_regression.py",
]:
    compile(Path("scripts/"+name).read_text(encoding="utf-8"), name, "exec")
print("compile ok")
print("bad v29 rate", '"rate": v29,' in tt)
print("v29s", "v29s = float" in tt)
print("v30", "v30 = float" in tt)
print("STAGE C289", "STAGE_ANT_C289" in tt)
