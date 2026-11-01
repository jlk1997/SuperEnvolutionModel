# -*- coding: utf-8 -*-
"""Clone V139 knife/capture/scorecard -> V141 C956-C958 (confidence-gate knife)."""
from pathlib import Path
import re
ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"

# --- C956 from C944 ---
src = (S / "c944_confidence_gate_stretch.py").read_text(encoding="utf-8")
dst = src
for a, b in [
    ("C944", "C956"),
    ("c944", "c956"),
    ("confidence_gate_stretch_v49", "confidence_gate_stretch_v141"),
    ("conf_gate_stretch_c944", "conf_gate_stretch_c956"),
]:
    dst = dst.replace(a, b)
(S / "c956_confidence_gate_stretch.py").write_text(dst, encoding="utf-8")
print("wrote c956", len(dst))

# --- C957 from C945: add V141 smoke/heldout refs at top of CHECKS, bump cycle ---
src = (S / "c945_capture_office_regression.py").read_text(encoding="utf-8")
dst = src
dst = dst.replace("C945", "C957").replace("c945", "c957")
dst = dst.replace("capture_regression_c945", "capture_regression_c957")
dst = dst.replace("C941-C944", "C953-C956")
dst = dst.replace("V4-V139+heldout", "V4-V141+heldout")
# Insert V141 checks right after the docstring block's CHECKS start - find V139 lines and prepend V141
needle = '    ("V139", DOC / "C942_VISION_V139_SMOKE.json"),\n    ("V139_heldout", DOC / "C943_VISION_V139_HELDOUT_SMOKE.json"),'
insert = (
    '    ("V141", DOC / "C954_VISION_V141_SMOKE.json"),\n'
    '    ("V141_heldout", DOC / "C955_VISION_V141_HELDOUT_SMOKE.json"),\n'
    '    ("V140", DOC / "C948_VISION_V140_SMOKE.json"),\n'
    '    ("V140_heldout", DOC / "C949_VISION_V140_HELDOUT_SMOKE.json"),\n'
    + needle
)
if needle in dst:
    dst = dst.replace(needle, insert, 1)
    print("inserted V141/V140 into CHECKS")
else:
    print("WARN: V139 needle not found")
# also add C956 conf gate to known list if C944 present
dst = dst.replace(
    '("C944_conf_gate"',
    '("C956_conf_gate", DOC / "C956_CONFIDENCE_GATE_STRETCH.json"),\n    ("C944_conf_gate"',
)
# required list: append V141
dst = dst.replace(
    '"V40", "V40_heldout"]',
    '"V40", "V40_heldout", "V141", "V141_heldout"]',
)
(S / "c957_capture_office_regression.py").write_text(dst, encoding="utf-8")
print("wrote c957", len(dst))

# --- C958 from C952 (more recent scorecard pattern) adapted for confidence knife ---
src = (S / "c952_scorecard_and_stage.py").read_text(encoding="utf-8")
dst = src
dst = dst.replace("C952", "C958").replace("c952", "c958")
dst = dst.replace("C947-C951", "C953-C957")
dst = dst.replace("C947-C952", "C953-C958")
dst = dst.replace("STAGE_ANT_C952", "STAGE_ANT_C958")  # may already be C958 from replace
# Fix double-replace if STAGE became C958 already via C952->C958
dst = dst.replace("STAGE_ANT_C958.md", "STAGE_ANT_C958.md")
# Vision file refs: V140 -> V141, C948->C954, C949->C955, C950-> keep u2c prior, C951->C957, C944->C956
# Careful ordered replaces
dst = dst.replace("C948_VISION_V140_SMOKE", "C954_VISION_V141_SMOKE")
dst = dst.replace("C948b_VISION_GATE_V140_CLAIM", "C954b_VISION_GATE_V141_CLAIM")
dst = dst.replace("C949_VISION_V140_HELDOUT_SMOKE", "C955_VISION_V141_HELDOUT_SMOKE")
dst = dst.replace("C949b_VISION_GATE_V140_HELDOUT_CLAIM", "C955b_VISION_GATE_V141_HELDOUT_CLAIM")
dst = dst.replace("C944_CONFIDENCE_GATE_STRETCH", "C956_CONFIDENCE_GATE_STRETCH")
dst = dst.replace("C951_CAPTURE_OFFICE_REGRESSION", "C957_CAPTURE_OFFICE_REGRESSION")
dst = dst.replace("C950_PRODUCT_U2C_COST", "C950_PRODUCT_U2C_COST")  # keep prior u2c
dst = dst.replace("vl_gate_v140_heldout_claim", "vl_gate_v141_heldout_claim")
dst = dst.replace("vl_gate_v140_claim", "vl_gate_v141_claim")
dst = dst.replace("v140h", "v141h")
dst = dst.replace("v140_claim", "v141_claim")
dst = dst.replace("v140h_claim", "v141h_claim")
# variable names v140 = -> v141 =  (after v140h already done)
dst = dst.replace("v140 = float", "v141 = float")
dst = dst.replace('"v140":', '"v141":')
dst = dst.replace('"v140_heldout":', '"v141_heldout":')
dst = dst.replace("Vision V140", "Vision V141")
dst = dst.replace("v140_jpeg_q", "v141_jpeg_q")
dst = dst.replace("clarity floor jpeg_q>=60 kept on V140", "clarity floor jpeg_q>=60 kept on V141")
dst = dst.replace("uses 62)", "uses 62)")
# prior vision carry-forward: was v139 from prior; now carry v140
dst = dst.replace(
    '"v139": (prior.get("vision") or {}).get("v139")',
    '"v140": (prior.get("vision") or {}).get("v140")',
)
dst = dst.replace(
    '"v139_heldout": (prior.get("vision") or {}).get("v139_heldout")',
    '"v140_heldout": (prior.get("vision") or {}).get("v140_heldout")',
)
# confidence source C944 -> C956 (already via file rename); product still C950
dst = dst.replace('"source": "C944"', '"source": "C956"')
dst = dst.replace('"source": "C951"', '"source": "C957"')
# STAGE bullets
dst = dst.replace("C947: Vision V140 design", "C953: Vision V141 design")
dst = dst.replace("C948: Vision V141 smoke", "C954: Vision V141 smoke")  # after V140->V141 already
dst = dst.replace("C949: Vision V141 heldout", "C955: Vision V141 heldout")
dst = dst.replace("C950: product-U2C", "C956: confidence-gate")
# Fix the product-U2C line that now says confidence-gate incorrectly for replace=
# Read the STAGE section carefully after write
dst = dst.replace("C951: capture", "C957: capture")
dst = dst.replace("C952: composite", "C958: composite")
# Fix STAGE knife line: originally C950 product-U2C replace=... — we replaced C950: product-U2C with C956: confidence-gate
# Need STAGE to show both confidence and prior replace
# Fix scorecard knife: stage_ready should use conf_pass instead of/in addition to u2c
# Looking at C952: stage_ready = v140_claim and v140h_claim and rates and capture and disjoint and u2c_pass
# For V141 confidence knife cycle, use conf_pass (like C946 did)
dst = dst.replace("and u2c_pass)", "and conf_pass)")
(S / "c958_scorecard_and_stage.py").write_text(dst, encoding="utf-8")
print("wrote c958", len(dst))
print("done")