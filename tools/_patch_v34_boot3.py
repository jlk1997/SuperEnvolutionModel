# -*- coding: utf-8 -*-
"""Surgical renumber of xform_reg / xform_score / main in V34 boot."""
from pathlib import Path
import re

P = Path("tools/_boot_v34_c308.py")
t = P.read_text(encoding="utf-8")

# Truncate from xform_reg onward and append new code from a separately built list
head = t[: t.find("def xform_reg(text: str) -> str:")]

lines = []
W = lines.append

W('def xform_reg(text: str) -> str:')
W('    text = text.replace("C306", "C312")')
W('    text = text.replace("C302-C305", "C308-C311")')
W('    text = text.replace("c302_c305", "c308_c311")')
W('    text = text.replace("capture_regression_c306", "capture_regression_c312")')
W('    needle = \'("V33_heldout", DOC / "C304_VISION_V33_HELDOUT_SMOKE.json"),\'')
W('    insert = (')
W('        needle')
W("        + '\\n    (\"V34\", DOC / \"C309_VISION_V34_SMOKE.json\"),'")
W("        + '\\n    (\"V34_heldout\", DOC / \"C310_VISION_V34_HELDOUT_SMOKE.json\"),'")
W('    )')
W('    if needle in text and \'("V34"\' not in text:')
W('        text = text.replace(needle, insert)')
W('    text = text.replace(')
W('        \'("C305_confidence_gate_stretch", DOC / "C305_CONFIDENCE_GATE_STRETCH.json"),\',')
W('        \'("C305_confidence_gate_stretch", DOC / "C305_CONFIDENCE_GATE_STRETCH.json"),\\n\'')
W('        \'    ("C311_dissolve_cost_shadow", DOC / "C311_DISSOLVE_COST_SHADOW.json"),\',')
W('    )')
W('    text = text.replace(')
W('        \'required = ["V25", "V25_heldout", "V26", "V26_heldout", "V27", "V27_heldout", "V28", "V28_heldout", "V29", "V29_heldout", "V30", "V30_heldout", "V31", "V31_heldout", "V32", "V32_heldout", "V33", "V33_heldout", "C233_clarity_floor", "C305_confidence_gate_stretch"]\',')
W('        \'required = ["V25", "V25_heldout", "V26", "V26_heldout", "V27", "V27_heldout", "V28", "V28_heldout", "V29", "V29_heldout", "V30", "V30_heldout", "V31", "V31_heldout", "V32", "V32_heldout", "V33", "V33_heldout", "V34", "V34_heldout", "C233_clarity_floor", "C311_dissolve_cost_shadow"]\',')
W('    )')
W('    text = text.replace(\'DOC / "C306_CAPTURE_OFFICE_REGRESSION.json"\', \'DOC / "C312_CAPTURE_OFFICE_REGRESSION.json"\')')
W('    return text')
W('')
W('')
W('def xform_score(text: str) -> str:')
W('    text = text.replace("C307", "C313")')
W('    text = text.replace("c302_c306", "c308_c312")')
W('    text = text.replace("STAGE_ANT_C307.md", "STAGE_ANT_C313.md")')
W('    text = text.replace("C302-C306", "C308-C312")')
W('    text = text.replace("C302-C307", "C308-C313")')
W('    text = text.replace("unified_scorecard_c302_c306", "unified_scorecard_c308_c312")')
W('')
# hist_inject as chr(10)-joined to avoid triple quotes in this file's outer string... we're in a Set-Content file so OK to use '''
W("    hist_inject = (")
for row in [
    '    c303v = load("docs/r50/C303_VISION_V33_SMOKE.json") or {}',
    '    c303vb = load("docs/r50/C303b_VISION_GATE_V33_CLAIM.json") or {}',
    '    c304v = load("docs/r50/C304_VISION_V33_HELDOUT_SMOKE.json") or {}',
    '    c304vb = load("docs/r50/C304b_VISION_GATE_V33_HELDOUT_CLAIM.json") or {}',
    '    c297v = load("docs/r50/C297_VISION_V32_SMOKE.json") or {}',
    '    c297vb = load("docs/r50/C297b_VISION_GATE_V32_CLAIM.json") or {}',
    '    c298v = load("docs/r50/C298_VISION_V32_HELDOUT_SMOKE.json") or {}',
    '    c298vb = load("docs/r50/C298b_VISION_GATE_V32_HELDOUT_CLAIM.json") or {}',
    '    c291v = load("docs/r50/C291_VISION_V31_SMOKE.json") or {}',
    '    c291vb = load("docs/r50/C291b_VISION_GATE_V31_CLAIM.json") or {}',
    '    c292v = load("docs/r50/C292_VISION_V31_HELDOUT_SMOKE.json") or {}',
    '    c292vb = load("docs/r50/C292b_VISION_GATE_V31_HELDOUT_CLAIM.json") or {}',
    '    c266 = load("docs/r50/C308_VISION_V34_DESIGN.json") or {}',
    '    c267 = load("docs/r50/C309_VISION_V34_SMOKE.json") or {}',
    '    c267b = load("docs/r50/C309b_VISION_GATE_V34_CLAIM.json") or {}',
    '    c268 = load("docs/r50/C310_VISION_V34_HELDOUT_SMOKE.json") or {}',
    '    c268b = load("docs/r50/C310b_VISION_GATE_V34_HELDOUT_CLAIM.json") or {}',
    '    c270 = load("docs/r50/C312_CAPTURE_OFFICE_REGRESSION.json") or {}',
]:
    W(f"        {row!r} + '\\n'")
# fix last newline
lines[-1] = lines[-1].replace(" + '\\n'", "")
W("    )")
W("    # join")
W("    hist_inject = ''.join([")
# Actually redo hist_inject cleaner
# Remove the broken hist_inject lines we just added and do it properly
# Easier: rewrite file from scratch for tail only

tail_path = Path("tools/_v34_boot_tail_src.py")
# We'll rebuild entirely below
print("rebuild via list approach")

# Clear and rebuild from head
body = []
B = body.append

B('def xform_reg(text: str) -> str:')
B('    text = text.replace("C306", "C312")')
B('    text = text.replace("C302-C305", "C308-C311")')
B('    text = text.replace("c302_c305", "c308_c311")')
B('    text = text.replace("capture_regression_c306", "capture_regression_c312")')
B(r"""    needle = '("V33_heldout", DOC / "C304_VISION_V33_HELDOUT_SMOKE.json"),'""")
B('    insert = (')
B('        needle')
B(r"""        + '\n    ("V34", DOC / "C309_VISION_V34_SMOKE.json"),'""")
B(r"""        + '\n    ("V34_heldout", DOC / "C310_VISION_V34_HELDOUT_SMOKE.json"),'""")
B('    )')
B(r"""    if needle in text and '("V34"' not in text:""")
B('        text = text.replace(needle, insert)')
B('    text = text.replace(')
B(r"""        '("C305_confidence_gate_stretch", DOC / "C305_CONFIDENCE_GATE_STRETCH.json"),',""")
B(r"""        '("C305_confidence_gate_stretch", DOC / "C305_CONFIDENCE_GATE_STRETCH.json"),\n'""")
B(r"""        '    ("C311_dissolve_cost_shadow", DOC / "C311_DISSOLVE_COST_SHADOW.json"),',""")
B('    )')
B('    text = text.replace(')
B('        \'required = ["V25", "V25_heldout", "V26", "V26_heldout", "V27", "V27_heldout", "V28", "V28_heldout", "V29", "V29_heldout", "V30", "V30_heldout", "V31", "V31_heldout", "V32", "V32_heldout", "V33", "V33_heldout", "C233_clarity_floor", "C305_confidence_gate_stretch"]\',')
B('        \'required = ["V25", "V25_heldout", "V26", "V26_heldout", "V27", "V27_heldout", "V28", "V28_heldout", "V29", "V29_heldout", "V30", "V30_heldout", "V31", "V31_heldout", "V32", "V32_heldout", "V33", "V33_heldout", "V34", "V34_heldout", "C233_clarity_floor", "C311_dissolve_cost_shadow"]\',')
B('    )')
B(r"""    text = text.replace('DOC / "C306_CAPTURE_OFFICE_REGRESSION.json"', 'DOC / "C312_CAPTURE_OFFICE_REGRESSION.json"')""")
B('    return text')
B('')
B('')

# For xform_score - do lighter touch: copy from existing score and apply replaces in the GENERATED scorecard script via post-pass
# Instead of complex xform_score, write a simpler version that does sequential replaces on C307 scorecard

B('def xform_score(text: str) -> str:')
B('    """Promote C307 scorecard -> C313 with V34 current + dissolve NV."""')
repls = [
    ("C307", "C313"),
    ("c302_c306", "c308_c312"),
    ("STAGE_ANT_C307.md", "STAGE_ANT_C313.md"),
    ("C302-C306", "C308-C312"),
    ("C302-C307", "C308-C313"),
    ("unified_scorecard_c302_c306", "unified_scorecard_c308_c312"),
    ("C302_VISION_V33_DESIGN.json", "C308_VISION_V34_DESIGN.json"),
    ("C303_VISION_V33_SMOKE.json", "C309_VISION_V34_SMOKE.json"),
    ("C303b_VISION_GATE_V33_CLAIM.json", "C309b_VISION_GATE_V34_CLAIM.json"),
    ("C304_VISION_V33_HELDOUT_SMOKE.json", "C310_VISION_V34_HELDOUT_SMOKE.json"),
    ("C304b_VISION_GATE_V33_HELDOUT_CLAIM.json", "C310b_VISION_GATE_V34_HELDOUT_CLAIM.json"),
    ("C306_CAPTURE_OFFICE_REGRESSION.json", "C312_CAPTURE_OFFICE_REGRESSION.json"),
    ("vl_gate_v33_claim", "vl_gate_v34_claim"),
    ("vl_gate_v33_heldout_claim", "vl_gate_v34_heldout_claim"),
    ("v33_claim", "v34_claim"),
    ("v33h_claim", "v34h_claim"),
    # careful: v33 = float must become v34 after we inject hist
]
B('    reps = [')
for a, b in repls:
    B(f'        ({a!r}, {b!r}),')
B('    ]')
B('    for a, b in reps:')
B('        text = text.replace(a, b)')
# Fix over-replacement: v33 rate vars that should stay for historical
# After blind replace, C303 became C309 for historical loads too - need to re-inject V33 hist
B('')
B('    # Re-inject V33 historical loads (blind replace turned them into V34)')
B('    # Restore V32 hist block then add V33 hist before V34 current')
B('    # Load block already points at V34 files for c266..c270; prepend V33/V32 hist.')
B('    needle = \'    c297v = load("docs/r50/C297_VISION_V32_SMOKE.json") or {}\'')
B('    hist = (')
B(r"""        '    c303v = load("docs/r50/C303_VISION_V33_SMOKE.json") or {}\n'""")
B(r"""        '    c303vb = load("docs/r50/C303b_VISION_GATE_V33_CLAIM.json") or {}\n'""")
B(r"""        '    c304v = load("docs/r50/C304_VISION_V33_HELDOUT_SMOKE.json") or {}\n'""")
B(r"""        '    c304vb = load("docs/r50/C304b_VISION_GATE_V33_HELDOUT_CLAIM.json") or {}\n'""")
B('    )')
B('    if needle in text and "c303v" not in text:')
B('        text = text.replace(needle, hist + needle)')
B('')
B('    # rate vars: after replace v33->v34, restore v33 from c303v and keep v34 from c267')
B('    text = text.replace(')
B('        """    v32 = float(c297v.get(\\"rate\\") or 0.0)\\n')
B('    v32h = float(c298v.get(\\"rate\\") or 0.0)\\n')
B('    v34 = float(c267.get(\\"rate\\") or 0.0)\\n')
B('    v34h = float(c268.get(\\"rate\\") or 0.0)""",')
B('        """    v32 = float(c297v.get(\\"rate\\") or 0.0)\\n')
B('    v32h = float(c298v.get(\\"rate\\") or 0.0)\\n')
B('    v33 = float(c303v.get(\\"rate\\") or 0.0)\\n')
B('    v33h = float(c304v.get(\\"rate\\") or 0.0)\\n')
B('    v34 = float(c267.get(\\"rate\\") or 0.0)\\n')
B('    v34h = float(c268.get(\\"rate\\") or 0.0)""",')
B('    )')
# This is getting too fragile. Different strategy:
print("switching strategy")
raise SystemExit(0)
