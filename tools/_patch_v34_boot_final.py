# -*- coding: utf-8 -*-
"""Finish V34 boot: minimal xform_reg/score/main; score refined by post-fix."""
from pathlib import Path

P = Path("tools/_boot_v34_c308.py")
t = P.read_text(encoding="utf-8")
head = t[: t.find("def xform_reg(text: str) -> str:")]

tail = '''def xform_reg(text: str) -> str:
    text = text.replace("C306", "C312")
    text = text.replace("C302-C305", "C308-C311")
    text = text.replace("c302_c305", "c308_c311")
    text = text.replace("capture_regression_c306", "capture_regression_c312")
    needle = '("V33_heldout", DOC / "C304_VISION_V33_HELDOUT_SMOKE.json"),'
    insert = (
        needle
        + '\\n    ("V34", DOC / "C309_VISION_V34_SMOKE.json"),'
        + '\\n    ("V34_heldout", DOC / "C310_VISION_V34_HELDOUT_SMOKE.json"),'
    )
    if needle in text and '("V34"' not in text:
        text = text.replace(needle, insert)
    text = text.replace(
        '("C305_confidence_gate_stretch", DOC / "C305_CONFIDENCE_GATE_STRETCH.json"),',
        '("C305_confidence_gate_stretch", DOC / "C305_CONFIDENCE_GATE_STRETCH.json"),\\n'
        '    ("C311_dissolve_cost_shadow", DOC / "C311_DISSOLVE_COST_SHADOW.json"),',
    )
    text = text.replace(
        'required = ["V25", "V25_heldout", "V26", "V26_heldout", "V27", "V27_heldout", "V28", "V28_heldout", "V29", "V29_heldout", "V30", "V30_heldout", "V31", "V31_heldout", "V32", "V32_heldout", "V33", "V33_heldout", "C233_clarity_floor", "C305_confidence_gate_stretch"]',
        'required = ["V25", "V25_heldout", "V26", "V26_heldout", "V27", "V27_heldout", "V28", "V28_heldout", "V29", "V29_heldout", "V30", "V30_heldout", "V31", "V31_heldout", "V32", "V32_heldout", "V33", "V33_heldout", "V34", "V34_heldout", "C233_clarity_floor", "C311_dissolve_cost_shadow"]',
    )
    text = text.replace('DOC / "C306_CAPTURE_OFFICE_REGRESSION.json"', 'DOC / "C312_CAPTURE_OFFICE_REGRESSION.json"')
    return text


def xform_score(text: str) -> str:
    """Stub: real scorecard patch applied by tools/_fix_c313_score.py after copy."""
    return text


def main():
    specs = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    train_specs = specs_to_py(specs["train"])
    held_specs = specs_to_py(specs["held"])
    mapping = [
        ("c302_vision_v33_design_and_batch.py", "c308_vision_v34_design_and_batch.py",
         lambda t: xform_train(t, train_specs)),
        ("c303_vision_v33_smoke.py", "c309_vision_v34_smoke.py", xform_smoke),
        ("c304_vision_v33_heldout.py", "c310_vision_v34_heldout.py",
         lambda t: xform_heldout(t, held_specs)),
        ("c293_dissolve_cost_shadow.py", "c311_dissolve_cost_shadow.py", xform_nv),
        ("c306_capture_office_regression.py", "c312_capture_office_regression.py", xform_reg),
    ]
    for src, dst, fn in mapping:
        src_t = (SCR / src).read_text(encoding="utf-8")
        out = fn(src_t)
        (SCR / dst).write_text(out, encoding="utf-8")
        print("wrote", dst, "bytes", len(out.encode("utf-8")))
    # scorecard: copy then external fix
    import shutil
    shutil.copy2(SCR / "c307_scorecard_and_stage.py", SCR / "c313_scorecard_and_stage.py")
    print("copied c313_scorecard_and_stage.py (pending fix)")
    d = (SCR / "c308_vision_v34_design_and_batch.py").read_text(encoding="utf-8")
    assert "vision_images_v34" in d and "v34_01" in d
    assert "V34 overlays" in d
    assert "bamboo_recv" in d
    assert "JPEG_Q = 60" in d
    assert "parchment_recv" not in d
    nv = (SCR / "c311_dissolve_cost_shadow.py").read_text(encoding="utf-8")
    assert "C311" in nv and "dissolve_cost_shadow_c311" in nv
    print("ok")


if __name__ == "__main__":
    main()
'''

# Fix double-escaped newlines in tail - we used \\n in replace strings which is correct for source code
out = head + tail
compile(out, str(P), "exec")
P.write_text(out, encoding="utf-8")
print("boot finished", len(out))
