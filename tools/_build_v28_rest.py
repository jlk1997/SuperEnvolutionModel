# -*- coding: utf-8 -*-
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SCR = ROOT / "scripts"

# C275 U2C/replace knife from c257
src = (SCR / "c257_innovation_u2c_capture_replace.py").read_text(encoding="utf-8")
out = src.replace("C257", "C275").replace("c257", "c275")
out = out.replace("innovation_c257", "u2c_replace_c275")
out = out.replace("innovation_u2c_capture_replace", "u2c_replace_stretch")
out = out.replace("vision_images_v25", "vision_images_v27")
out = out.replace("Optional innovation knife", "Non-vision knife")
out = out.replace("innovation knife; no VL claim here", "U2C on V27 fixtures + replace ledger; no VL claim")
# bump numbers slightly in inline cases if any V25 refs remain
(SCR / "c275_u2c_replace_stretch.py").write_text(out, encoding="utf-8")
print("wrote c275", len(out))

# C276 regression from c270
src = (SCR / "c270_capture_office_regression.py").read_text(encoding="utf-8")
out = src.replace("C270", "C276").replace("c270", "c276")
out = out.replace("C266-C269", "C272-C275")
out = out.replace("V4-V27", "V4-V28")
out = out.replace("V27+", "V28+")
# ensure V28 appears in required list if pattern exists
out = out.replace('"V27", "V27_heldout"', '"V27", "V27_heldout", "V28", "V28_heldout"')
out = out.replace("'V27', 'V27_heldout'", "'V27', 'V27_heldout', 'V28', 'V28_heldout'")
# C269 -> C275 for non-vision ref if present
out = out.replace("C269_conf_gate_stretch", "C275_u2c_replace_stretch")
out = out.replace("C269", "C275")
# careful: may have doubled
(SCR / "c276_capture_office_regression.py").write_text(out, encoding="utf-8")
print("wrote c276", len(out))

# C277 scorecard from c271
src = (SCR / "c271_scorecard_and_stage.py").read_text(encoding="utf-8")
out = src.replace("C271", "C277").replace("c271", "c277")
out = out.replace("C266-C270", "C272-C276")
out = out.replace("C266-C271", "C272-C277")
out = out.replace("C266", "C272").replace("C267", "C273").replace("C268", "C274")
out = out.replace("C269", "C275").replace("C270", "C276")
out = out.replace("V27", "V28").replace("v27", "v28")
# restore V25/V26 retained claims that got mangled
out = out.replace("V28 train/heldout retained", "V27 train/heldout retained")
# Fix vision load paths - need V25-V28
# Read and surgically fix the load/vision section
# After blind replace, C255 may have become wrong — check
out = out.replace("C255_VISION_V28", "C255_VISION_V25")
out = out.replace("C256_VISION_V28", "C256_VISION_V25")
out = out.replace("C261_VISION_V28", "C261_VISION_V26")
out = out.replace("C262_VISION_V28", "C262_VISION_V26")
# v25/v26 keys in vision dict
out = out.replace('"V28":', '"V28_TMP":')  # temp
# Actually look at structure after write
(SCR / "c277_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("wrote c277 raw", len(out))

# Patch c277 vision section properly
text = (SCR / "c277_scorecard_and_stage.py").read_text(encoding="utf-8")
# Ensure loads include V25-V28
if "C255_VISION_V25" not in text:
    text = text.replace(
        'c255 = load("docs/r50/C255_VISION_V28_SMOKE.json")',
        'c255 = load("docs/r50/C255_VISION_V25_SMOKE.json")',
    )
# Add V27 loads if missing after replace
if "C267_VISION_V27" not in text and "C273_VISION_V28" in text:
    # insert V27 loads before V28
    needle = 'c272 = load("docs/r50/C272_VISION_V28_DESIGN.json")'
    if needle in text:
        insert = (
            'c266 = load("docs/r50/C266_VISION_V27_DESIGN.json") or {}\n'
            '    c267 = load("docs/r50/C267_VISION_V27_SMOKE.json") or {}\n'
            '    c267b = load("docs/r50/C267b_VISION_GATE_V27_CLAIM.json") or {}\n'
            '    c268 = load("docs/r50/C268_VISION_V27_HELDOUT_SMOKE.json") or {}\n'
            '    c268b = load("docs/r50/C268b_VISION_GATE_V27_HELDOUT_CLAIM.json") or {}\n'
            '    ' + needle
        )
        text = text.replace(needle, insert, 1)

# Fix STAGE doc name
text = text.replace("STAGE_ANT_C271", "STAGE_ANT_C277")
text = text.replace("STAGE_ANT_C277.md", "STAGE_ANT_C277.md")

# Non-vision: c275 u2c instead of conf-gate
text = text.replace("confidence-gate stretch", "u2c-replace stretch")
text = text.replace("conf-gate stretch", "u2c-replace stretch")
text = text.replace("conf_gate", "u2c_replace")

(SCR / "c277_scorecard_and_stage.py").write_text(text, encoding="utf-8")
print("patched c277")

# Quick syntax check
import py_compile
for p in [
    "scripts/c272_vision_v28_design_and_batch.py",
    "scripts/c273_vision_v28_smoke.py",
    "scripts/c274_vision_v28_heldout.py",
    "scripts/c275_u2c_replace_stretch.py",
    "scripts/c276_capture_office_regression.py",
    "scripts/c277_scorecard_and_stage.py",
]:
    try:
        py_compile.compile(p, doraise=True)
        print("syntax ok", p)
    except Exception as e:
        print("SYNTAX FAIL", p, e)