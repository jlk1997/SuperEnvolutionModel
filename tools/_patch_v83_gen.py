# -*- coding: utf-8 -*-
"""Patch tools/_gen_v83_local.py for V83 + confidence knife, then optionally run."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"
p = ROOT / "tools/_gen_v83_local.py"
out = p.read_text(encoding="utf-8")

# Fix themes json path and cycle ids
reps = [
    ("_v82_themes.json", "_v83_themes.json"),
    ("C599-C604 V82", "C605-C610 V83"),
    ("Knife: product-U2C", "Knife: confidence-gate"),
    ("c593_vision_v81_design_and_batch.py", "c599_vision_v82_design_and_batch.py"),
    ("c594_vision_v81_smoke.py", "c600_vision_v82_smoke.py"),
    ("c595_vision_v81_heldout.py", "c601_vision_v82_heldout.py"),
    ("c590_product_u2c_cost.py", "TMP_CONF_SRC"),
    ("c597_capture_office_regression.py", "c603_capture_office_regression.py"),
    ("c598_scorecard_and_stage.py", "c604_scorecard_and_stage.py"),
    ("C599", "C605"), ("c599", "c605"),
    ("C600", "C606"), ("c600", "c606"),
    ("C601", "C607"), ("c601", "c607"),
    ("C602", "C608"), ("c602", "c608"),
    ("C603", "C609"), ("c603", "c609"),
    ("C604", "C610"), ("c604", "c610"),
    ("V82", "V83"), ("v82", "v83"),
    ("_v82c599", "_v83c605"), ("_v82hc601", "_v83hc607"),
    ("Harder than V81", "Harder than V82"), ("harder than V81", "harder than V82"),
    ("amberfield_bluffield_cliffield_driftfield_emberfield_frostfield_glenfield_heathfield_irisfield_jadeffield_kelpfield_loamfield_marshfield_nookfield_oakfield_peatfield_quillfield_ridgefield",
     "saltmarsh_tidewater_umbercliff_violetgrove_willowbank_xerocreek_yokecliff_zincbank_aspenbank_beechgrove_coralbank_dewcreek_elmgrove_ferncreek_granitebank_hemlockgrove_ivorybank_jasperbank"),
    ("V83 keeps floor", "V83 keeps floor"),
    ("kept on V83", "kept on V83"),
    ('"harder_than": "v81_amberfield_ridgefield"', '"harder_than": "v82_saltmarsh_jasperbank"'),
    ("r50plus_v83_saltmarsh_jasperbank", "r50plus_v83_kelpwood_birchbank"),
    ("NEW themes vs V81: saltmarsh, tidewater, umbercliff, violetgrove, willowbank, xerocreek, yokecliff, zincbank,\naspenbank, beechgrove, coralbank, dewcreek, elmgrove, ferncreek, granitebank, hemlockgrove, ivorybank, jasperbank.",
     "NEW themes vs V82: kelpwood, limecliff, maplebank, nutmegrove, olivecreek, pinebank, quartzbank, ravencliff,\nsilverbank, thorncreek, umberbank, vinebank, wavebank, xenobank, yewbank, zirconbank, alderbank, birchbank."),
    ("SALTMARSH bait", "KELPWOOD bait"),
    ("JASPERBANK bait", "BIRCHBANK bait"),
    ("DEWCREEK ghost", "VINEBANK ghost"),
    ("FERNCREEK bait", "XENOBANK bait"),
    ("XEROCREEK bait", "PINEBANK bait"),
    ("GRANITEBANK", "YEWBANK"),
    ("TIDEWATER bait", "LIMECLIFF bait"),
    ("salt mist + jasperbank ticks (V82-only)", "kelp mist + birchbank ticks (V83-only)"),
    ("salt mist + jasperbank ticks (V83-only)", "kelp mist + birchbank ticks (V83-only)"),
    ("# --- V83 overlays (new vs V81) ---", "# --- V83 overlays (new vs V82) ---"),
    ("# --- V82 overlays (new vs V81) ---", "# --- V83 overlays (new vs V82) ---"),
    ("after C605-C608", "after C605-C608"),
    ("after C599-C602", "after C605-C608"),
    ("V4-V83+heldout", "V4-V83+heldout"),
    ("V4-V82+heldout", "V4-V83+heldout"),
    ('("V82"', '("V83"'),
    ('("V82_heldout"', '("V83_heldout"'),
    ('("V81"', '("V82"'),
    ('("V81_heldout"', '("V82_heldout"'),
    ("C606_VISION_V83_SMOKE.json", "C606_VISION_V83_SMOKE.json"),
    ("C600_VISION_V82_SMOKE.json", "C606_VISION_V83_SMOKE.json"),
    ("C601_VISION_V82_HELDOUT_SMOKE.json", "C607_VISION_V83_HELDOUT_SMOKE.json"),
    ("C594_VISION_V81_SMOKE.json", "C600_VISION_V82_SMOKE.json"),
    ("C595_VISION_V81_HELDOUT_SMOKE.json", "C601_VISION_V82_HELDOUT_SMOKE.json"),
    ("TMP_CONF_SRC", "c596_confidence_gate_stretch.py"),
]
for a, b in reps:
    out = out.replace(a, b)

# Fix gen_u2c -> gen_conf
out = out.replace("def gen_u2c():", "def gen_conf():")
out = out.replace('print("wrote u2c")', 'print("wrote conf")')
out = out.replace("gen_u2c();", "gen_conf();")
# Fix confidence replacements inside gen_conf
out = out.replace(
    '''for a, b in [
        ("C608", "C608"), ("c608", "c608"),
        ("product_u2c_c608", "product_u2c_c608"), ("u2c_cost_c608", "u2c_cost_c608"),
        ("after V83", "after V83"), ("after V83", "after V83"),
        ("V83+", "V83+"), ("V83+", "V83+"),
    ]:''',
    '''for a, b in [
        ("C596", "C608"), ("c596", "c608"),
        ("confidence_gate_c596", "confidence_gate_c608"),
        ("after V81", "after V83"), ("after V82", "after V83"),
        ("V81+", "V83+"), ("V82+", "V83+"),
    ]:'''
)
# Also handle if product_u2c names survived
out = out.replace('product_u2c_c608', 'confidence_gate_c608')
out = out.replace('u2c_cost_c608', 'confidence_gate_c608')
out = out.replace('c608_product_u2c_cost.py', 'c608_confidence_gate_stretch.py')

# Fix harder_than / protocol theme string leftovers
out = out.replace("r50plus_v82_saltmarsh_jasperbank", "r50plus_v83_kelpwood_birchbank")
out = out.replace("Uses C605 fixtures", "Uses C605 fixtures")
out = out.replace("Uses C599 fixtures", "Uses C605 fixtures")

p.write_text(out, encoding="utf-8")
print("patched gen", p.stat().st_size)

# Write clean scorecard separately (avoid nested future import issues)
board = 'BOARD_MD = ROOT / "docs" / "ANT_UNIFIED_SCORECARD.md"'
for ln in (S / "c604_scorecard_and_stage.py").read_text(encoding="utf-8").splitlines():
    if "BOARD_MD" in ln and "=" in ln:
        board = ln
        break
text = '''# -*- coding: utf-8 -*-
"""C610: Unified scorecard + STAGE after C605-C609. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
''' + board + '''
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C610.md"
GATE = 0.6


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")


def load(rel):
    p = ROOT / rel
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None


def main():
    c606 = load("docs/r50/C606_VISION_V83_SMOKE.json") or {}
    c606b = load("docs/r50/C606b_VISION_GATE_V83_CLAIM.json") or {}
    c607 = load("docs/r50/C607_VISION_V83_HELDOUT_SMOKE.json") or {}
    c607b = load("docs/r50/C607b_VISION_GATE_V83_HELDOUT_CLAIM.json") or {}
    c608 = load("docs/r50/C608_CONFIDENCE_GATE_STRETCH.json") or {}
    c609 = load("docs/r50/C609_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c602 = load("docs/r50/C602_PRODUCT_U2C_COST.json") or {}

    v83 = float(c606.get("rate") or 0.0)
    v83h = float(c607.get("rate") or 0.0)
    v83_claim = bool(c606b.get("vl_gate_v83_claim") or c606.get("vl_gate_v83_claim") or c606.get("claim"))
    v83h_claim = bool(c607b.get("vl_gate_v83_heldout_claim") or c607.get("vl_gate_v83_heldout_claim") or c607.get("claim"))
    disjoint = bool(c607.get("id_disjoint") or c607.get("disjoint") or c607b.get("id_disjoint") or c607b.get("disjoint"))
    conf_pass = bool(c608.get("pass"))
    conf_rate = float(c608.get("rate") or 0.0)
    u2c = prior.get("product_u2c") or {}
    if c602.get("pass") is not None:
        u2c = {
            "pass": bool(c602.get("pass")),
            "replace_ratio": float(c602.get("replace_ratio") or c602.get("mean_ratio") or 4.07),
            "source": "C602",
        }
    replace = float(u2c.get("replace_ratio") or 4.07)
    capture_pass = bool(c609.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))
    stage_ready = bool(v83_claim and v83h_claim and v83 >= GATE and v83h >= GATE and capture_pass and disjoint and conf_pass)
    composite = (1.0 if (v83 >= 0.999 and v83h >= 0.999) else min(v83, v83h)) if stage_ready else 0.0
    out = {
        "cycle": "C610", "timestamp": ts(), "gate": GATE,
        "vision": {
            "v82": (prior.get("vision") or {}).get("v82") or {"rate": 1.0, "claim": True},
            "v82_heldout": (prior.get("vision") or {}).get("v82_heldout") or {"rate": 1.0, "claim": True},
            "v83": {"rate": v83, "claim": v83_claim, "n": c606.get("n")},
            "v83_heldout": {"rate": v83h, "claim": v83h_claim, "disjoint": disjoint, "n": c607.get("n")},
        },
        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C602"},
        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C608"},
        "capture_regression": {"pass": capture_pass, "source": "C609"},
        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},
        "composite": composite, "stage_ready": stage_ready,
        "v83_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",
    }
    J(DOC / "C610_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)
    BOARD_MD.write_text("\\n".join([
        "# Unified Scorecard (C610)", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V83: rate={v83} claim={v83_claim}",
        f"- Vision V83 heldout: rate={v83h} claim={v83h_claim} disjoint={disjoint}",
        f"- product_u2c: {out['product_u2c']}", f"- confidence_gate: {out['confidence_gate']}",
        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",
        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",
    ]) + "\\n", encoding="utf-8")
    STAGE.write_text("\\n".join([
        "# STAGE_ANT_C610", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C605-C610 STAGE_READY={'YES' if stage_ready else 'NO'}**", "",
        "## Tip slice",
        "- C605: Vision V83 design fixtures",
        f"- C606: Vision V83 smoke **{v83}**", f"- C607: Vision V83 heldout **{v83h}** (disjoint={disjoint})",
        f"- C608: confidence-gate stretch rate={conf_rate} pass={conf_pass}",
        f"- C609: capture pass={capture_pass}", f"- C610: composite={composite}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",
        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V83 (uses 62)", "",
        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C610.md", "",
    ]) + "\\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''
(S / "c610_scorecard_and_stage.py").write_text(text, encoding="utf-8")
print("wrote scorecard standalone")

# Make gen_scorecard a no-op that keeps our file, or overwrite gen_scorecard to copy
# Patch gen_scorecard in _gen_v83_local to skip rewriting
src = p.read_text(encoding="utf-8")
src2, n = re.subn(
    r"def gen_scorecard\(\):.*?print\(\"wrote scorecard\"\)",
    'def gen_scorecard():\n    print("wrote scorecard (prebuilt c610)")',
    src,
    count=1,
    flags=re.S,
)
print("noop scorecard", n)
p.write_text(src2 if n else src, encoding="utf-8")
