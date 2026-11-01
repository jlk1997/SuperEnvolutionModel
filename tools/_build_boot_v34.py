# -*- coding: utf-8 -*-
"""Build tools/_boot_v34_c308.py from _boot_v33_c302.py then emit C308-C313 scripts."""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
SCR = ROOT / "scripts"

V34_OVERLAY = r'''
    # --- V34 overlays (new vs V33) ---
    # bamboo grain vertical strokes
    for _ in range(90):
        bx = rng.randint(70, 520)
        by = rng.randint(320, 560)
        if in_text_band(by):
            continue
        d.line([(bx, by), (bx, by + rng.randint(8, 22))], fill=(150, 170, 120), width=1)
    # slate tile hatch
    for lx in range(70, 240, 12):
        d.line([(lx, 300), (lx + 20, 330)], fill=(90, 95, 105), width=1)
    for ly in range(300, 340, 10):
        d.line([(70, ly), (200, ly)], fill=(100, 105, 115), width=1)
    # denim stitch Xs
    for di in range(8):
        x0 = 250 + di * 28
        d.line([(x0, 350), (x0 + 10, 360)], fill=(40, 60, 120), width=1)
        d.line([(x0 + 10, 350), (x0, 360)], fill=(40, 60, 120), width=1)
    d.text((250, 366), "DENIM bait 27.27", fill=(30, 40, 90), font=f_tiny)
    # brass fastener circles
    for by in (100, 190, 280, 370):
        d.ellipse([30, by, 54, by + 22], fill=(180, 140, 50), outline=(90, 60, 20), width=2)
        d.ellipse([38, by + 7, 46, by + 15], fill=(230, 200, 100))
    # prism rainbow wedges
    for hi, col in enumerate([(255, 60, 60), (255, 180, 40), (60, 220, 80), (60, 120, 255)]):
        d.polygon([(610 + hi * 35, 40), (640 + hi * 35, 40), (625 + hi * 35, 72)], fill=col)
    d.text((610, 76), "PRISM bait 61.61", fill=(80, 40, 120), font=f_tiny)
    # latch hook
    d.arc([400, 340, 460, 400], 200, 340, fill=(70, 70, 80), width=3)
    d.rectangle([455, 360, 480, 375], fill=(90, 90, 100))
    d.text((400, 405), "LATCH bait 19.19", fill=(40, 40, 50), font=f_tiny)
    # amber resin blob
    d.ellipse([70, 430, 130, 480], fill=(220, 150, 40), outline=(160, 90, 20), width=2)
    d.text((70, 485), "AMBER bait 15.15", fill=(120, 70, 10), font=f_tiny)
    # quarry stone blocks
    for qi in range(4):
        d.rectangle([250 + qi * 40, 430, 285 + qi * 40, 465], outline=(110, 100, 90), width=2)
    # tin plate band
    d.rectangle([850, 100, 980, 155], fill=(170, 175, 180), outline=(80, 85, 90), width=2)
    d.text((870, 118), "TIN", fill=(40, 40, 50), font=f_stamp)
    # mylar sheen rect
    d.rectangle([420, 340, 560, 415], fill=(235, 245, 255))
    d.text((430, 365), "MYLAR ghost 88.88", fill=(90, 120, 150), font=f_pen)
    # felt pad soft rect
    d.rectangle([100, 500, 230, 545], fill=(140, 100, 80), outline=(80, 50, 40), width=2)
    d.text((120, 512), "FELT", fill=(240, 220, 200), font=f_stamp)
    # stitch dashed edge
    for px in range(70, 520, 8):
        d.line([(px, 285), (px + 4, 285)], fill=(60, 60, 70), width=1)
    # enamel pin circle
    d.ellipse([880, 470, 980, 555], fill=(40, 90, 160), outline=(20, 40, 80), width=3)
    d.text((900, 500), "ENML", fill=(230, 240, 255), font=f_stamp)
    # cord bind loops
    for cy in range(470, 560, 14):
        d.arc([250, cy, 310, cy + 20], 0, 180, fill=(90, 60, 40), width=2)
    # rice paper fiber wash
    for _ in range(70):
        px = rng.randint(320, 520)
        py = rng.randint(470, 560)
        d.point((px, py), fill=(210, 200, 180))
    # chrome glare band
    d.polygon([(60, 12), (420, 12), (405, 26), (70, 26)], fill=(200, 210, 230), outline=(90, 100, 120), width=1)
    d.text((80, 13), "CHROME bait 48.48", fill=(50, 60, 90), font=f_tiny)
    # index tab flags right
    for ti, ty in enumerate((90, 150, 210, 270)):
        d.polygon([(990, ty), (1020, ty + 12), (990, ty + 24)], fill=(200, 80, 80 + ti * 20))
'''

def build_boot():
    src = (TOOLS / "_boot_v33_c302.py").read_text(encoding="utf-8")
    # Replace overlay block
    start = src.find("V33_OVERLAY = r'''")
    end = src.find("'''", start + 20) + 3
    assert start > 0 and end > start
    new_overlay = "V34_OVERLAY = r'''" + V34_OVERLAY + "'''"
    out = src[:start] + new_overlay + src[end:]
    reps = [
        ("Bootstrap C302-C307 Vision V33 suite from V32 scripts + confidence-gate NV.",
         "Bootstrap C308-C313 Vision V34 suite from V33 scripts + dissolve/shadow NV."),
        ("_v33_specs.json", "_v34_specs.json"),
        ("V33_OVERLAY", "V34_OVERLAY"),
        ("parchment/cork/canvas/rivet/holo/zip/filament/honey/marble/copper/acetate/perf/waxseal/magnet/crepe/satin/spiral",
         "bamboo/slate/denim/brass/prism/latch/amber/quarry/tin/mylar/felt/void/stitch/enamel/cord/rice/chrome/index"),
        ("c296_vision_v32_design_and_batch.py", "c302_vision_v33_design_and_batch.py"),
        ("c302_vision_v33_design_and_batch.py", "c308_vision_v34_design_and_batch.py"),
        ("c297_vision_v32_smoke.py", "c303_vision_v33_smoke.py"),
        ("c303_vision_v33_smoke.py", "c309_vision_v34_smoke.py"),
        ("c298_vision_v32_heldout.py", "c304_vision_v33_heldout.py"),
        ("c304_vision_v33_heldout.py", "c310_vision_v34_heldout.py"),
        ("c287_confidence_gate_stretch.py", "c293_dissolve_cost_shadow.py"),
        ("c305_confidence_gate_stretch.py", "c311_dissolve_cost_shadow.py"),
        ("c300_capture_office_regression.py", "c306_capture_office_regression.py"),
        ("c306_capture_office_regression.py", "c312_capture_office_regression.py"),
        ("c301_scorecard_and_stage.py", "c307_scorecard_and_stage.py"),
        ("c307_scorecard_and_stage.py", "c313_scorecard_and_stage.py"),
    ]
    # careful ordered replace - do structural ones via dedicated function rewrite instead
    # Simpler approach: string-replace V33->V34 and cycle numbers after overlay swap,
    # then fix mapping + xform functions manually in second pass.
    out = out.replace("V33", "V34")
    out = out.replace("v33", "v34")
    out = out.replace("V32", "V33")  # historical refs in scorecard may break - fix below
    # Undo over-eager V32->V33 inside comments about V32 history? We'll fix mapping block.
    out = out.replace("_v34_specs.json", "_v34_specs.json")  # keep
    # Fix docstring
    out = out.replace(
        "Bootstrap C302-C307 Vision V34 suite from V33 scripts + confidence-gate NV.",
        "Bootstrap C308-C313 Vision V34 suite from V33 scripts + dissolve/shadow NV.",
    )
    # Fix SPEC already ok if was _v33 -> _v34
    out = out.replace('SPEC_PATH = ROOT / "tools" / "_v33_specs.json"',
                      'SPEC_PATH = ROOT / "tools" / "_v34_specs.json"')
    # Cycle number bumps in xforms: C302->C308 etc done partially by...? not yet
    # Replace cycle ids systematically
    for a, b in [
        ("C307", "C313"), ("C306", "C312"), ("C305", "C311"), ("C304", "C310"),
        ("C303", "C309"), ("C302", "C308"),
        ("c307", "c313"), ("c306", "c312"), ("c305", "c311"), ("c304", "c310"),
        ("c303", "c309"), ("c302", "c308"),
        ("C301", "C307"), ("C300", "C306"), ("C299", "C305"), ("C298", "C304"),
        ("C297", "C303"), ("C296", "C302"),
        ("c301", "c307"), ("c300", "c306"), ("c299", "c305"), ("c298", "c304"),
        ("c297", "c303"), ("c296", "c302"),
        ("cg33_", "cg34_"), ("cg30_", "cg34_"),
    ]:
        out = out.replace(a, b)

    # The above double-bumped some things that were already C302 in source mapped to C308 then
    # from C296->C302. Source boot maps C296->C302. After replace C296->C302 and C302->C308,
    # sources become C308 and dests become wrong. Need clean rewrite of main() mapping.

    # Rebuild main mapping and critical xform_nv from scratch by cutting from '# def main' 
    marker = "def main():"
    mi = out.find(marker)
    assert mi > 0
    head = out[:mi]

    # Fix xform_nv to dissolve instead of confidence-gate
    # Find def xform_nv in head and replace function body
    nvi = head.find("def xform_nv")
    nve = head.find("\ndef xform_reg", nvi)
    assert nvi > 0 and nve > nvi
    new_nv = '''def xform_nv(text: str) -> str:
    """Dissolve/cost/shadow from C293 -> C311 with fresh sandbox tag."""
    text = text.replace("C293", "C311")
    text = text.replace("dissolve_cost_shadow_c293", "dissolve_cost_shadow_c311")
    text = text.replace("C293_DISSOLVE_COST_SHADOW.json", "C311_DISSOLVE_COST_SHADOW.json")
    text = text.replace("c293", "c311")
    return text


'''
    head = head[:nvi] + new_nv + head[nve+1:]  # nve points at \ndef xform_reg; keep from def xform_reg

    # Fix THEMES_SHORT if mangled
    head = re_sub_themes(head)

    # Fix assert kraft leftovers etc at end via new main
    main = '''def main():
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
        ("c307_scorecard_and_stage.py", "c313_scorecard_and_stage.py", xform_score),
    ]
    for src, dst, fn in mapping:
        t = (SCR / src).read_text(encoding="utf-8")
        out = fn(t)
        (SCR / dst).write_text(out, encoding="utf-8")
        print("wrote", dst, "bytes", len(out.encode("utf-8")))
    d = (SCR / "c308_vision_v34_design_and_batch.py").read_text(encoding="utf-8")
    assert "vision_images_v34" in d and "v34_01" in d
    assert "V34 overlays" in d
    assert "bamboo_recv" in d
    assert "JPEG_Q = 60" in d
    assert "parchment_recv" not in d
    s = (SCR / "c313_scorecard_and_stage.py").read_text(encoding="utf-8")
    assert "STAGE_ANT_C313.md" in s
    assert "C309_VISION_V34_SMOKE" in s
    assert "v34_claim" in s
    assert "C311_DISSOLVE_COST_SHADOW" in s
    nv = (SCR / "c311_dissolve_cost_shadow.py").read_text(encoding="utf-8")
    assert "C311" in nv and "dissolve_cost_shadow_c311" in nv
    print("ok")


if __name__ == "__main__":
    main()
'''
    # Fix xform_score / xform_reg / xform_train references that may be broken from double-bump
    head = cleanup_xforms(head)
    final = head + main
    # Ensure import json still there
    assert "import json" in final
    dest = TOOLS / "_boot_v34_c308.py"
    dest.write_text(final, encoding="utf-8")
    print("wrote", dest, "bytes", dest.stat().st_size)


def re_sub_themes(head: str) -> str:
    import re
    head = re.sub(
        r'THEMES_SHORT = "[^"]*"',
        'THEMES_SHORT = "bamboo/slate/denim/brass/prism/latch/amber/quarry/tin/mylar/felt/void/stitch/enamel/cord/rice/chrome/index"',
        head,
        count=1,
    )
    return head


def cleanup_xforms(head: str) -> str:
    """Rewrite xform_reg and xform_score to sensible C308-C313 forms from current (possibly mangled) text."""
    # Replace entire xform_reg
    i = head.find("def xform_reg")
    j = head.find("\ndef xform_score", i)
    assert i > 0 and j > i
    xform_reg = '''def xform_reg(text: str) -> str:
    text = text.replace("C306", "C312")
    text = text.replace("C302-C305", "C308-C311")
    text = text.replace("c302_c305", "c308_c311")
    text = text.replace("capture_regression_c306", "capture_regression_c312")
    needle = '("V34_heldout", DOC / "C310_VISION_V34_HELDOUT_SMOKE.json"),'
    # after V33->V34 bump in source file, V33 heldout line becomes V34; insert new V34 after previous V33
    # Source c306 already lists through V33. After prior replaces it may list V34. Ensure V34 present.
    if '("V34"' not in text and '("V33"' in text:
        needle33 = '("V33_heldout", DOC / "C304_VISION_V33_HELDOUT_SMOKE.json"),'
        if needle33 in text:
            text = text.replace(
                needle33,
                needle33
                + '\\n    ("V34", DOC / "C309_VISION_V34_SMOKE.json"),'
                + '\\n    ("V34_heldout", DOC / "C310_VISION_V34_HELDOUT_SMOKE.json"),',
            )
    text = text.replace(
        '("C311_confidence_gate_stretch", DOC / "C311_CONFIDENCE_GATE_STRETCH.json"),',
        '("C311_dissolve_cost_shadow", DOC / "C311_DISSOLVE_COST_SHADOW.json"),',
    )
    text = text.replace(
        '("C305_confidence_gate_stretch", DOC / "C305_CONFIDENCE_GATE_STRETCH.json"),',
        '("C305_confidence_gate_stretch", DOC / "C305_CONFIDENCE_GATE_STRETCH.json"),\\n'
        '    ("C311_dissolve_cost_shadow", DOC / "C311_DISSOLVE_COST_SHADOW.json"),',
    )
    # required list: ensure V34
    if '"V34"' not in text:
        text = text.replace(
            '"V33", "V33_heldout"',
            '"V33", "V33_heldout", "V34", "V34_heldout"',
        )
    text = text.replace('DOC / "C306_CAPTURE_OFFICE_REGRESSION.json"', 'DOC / "C312_CAPTURE_OFFICE_REGRESSION.json"')
    text = text.replace('DOC / "C312_CAPTURE_OFFICE_REGRESSION.json"', 'DOC / "C312_CAPTURE_OFFICE_REGRESSION.json"')
    return text


'''
    # Fix escapes - I used \\n in the string incorrectly for the function source
    xform_reg = xform_reg.replace("\\n", "\n")
    head = head[:i] + xform_reg + head[j+1:]

    # Rewrite xform_score more carefully by loading and doing targeted fixes on the already-bumped text
    i = head.find("def xform_score")
    j = head.find("\ndef main", i)
    if j < 0:
        j = len(head)
    # Keep a simplified xform_score that does mechanical renames from C307 scorecard template
    xform_score = '''def xform_score(text: str) -> str:
    text = text.replace("C307", "C313")
    text = text.replace("c302_c306", "c308_c312")
    text = text.replace("STAGE_ANT_C307.md", "STAGE_ANT_C313.md")
    text = text.replace("STAGE_ANT_C313.md", "STAGE_ANT_C313.md")
    text = text.replace("C302-C306", "C308-C312")
    text = text.replace("C302-C307", "C308-C313")
    text = text.replace("C308-C313", "C308-C313")
    text = text.replace("unified_scorecard_c302_c306", "unified_scorecard_c308_c312")
    text = text.replace("unified_scorecard_c308_c312", "unified_scorecard_c308_c312")

    # Inject V34 loads; keep V33 history
    old = '''    c266 = load("docs/r50/C308_VISION_V34_DESIGN.json") or {}
    c267 = load("docs/r50/C309_VISION_V34_SMOKE.json") or {}
    c267b = load("docs/r50/C309b_VISION_GATE_V34_CLAIM.json") or {}
    c268 = load("docs/r50/C310_VISION_V34_HELDOUT_SMOKE.json") or {}
    c268b = load("docs/r50/C310b_VISION_GATE_V34_HELDOUT_CLAIM.json") or {}
    c270 = load("docs/r50/C312_CAPTURE_OFFICE_REGRESSION.json") or {}'''
    # If still pointing at V33 design under c266 after bumps from C302->C308:
    alt_old = '''    c266 = load("docs/r50/C302_VISION_V33_DESIGN.json") or {}
    c267 = load("docs/r50/C303_VISION_V33_SMOKE.json") or {}
    c267b = load("docs/r50/C303b_VISION_GATE_V33_CLAIM.json") or {}
    c268 = load("docs/r50/C304_VISION_V33_HELDOUT_SMOKE.json") or {}
    c268b = load("docs/r50/C304b_VISION_GATE_V33_HELDOUT_CLAIM.json") or {}
    c270 = load("docs/r50/C306_CAPTURE_OFFICE_REGRESSION.json") or {}'''
    hist = '''    c303v = load("docs/r50/C303_VISION_V33_SMOKE.json") or {}
    c303vb = load("docs/r50/C303b_VISION_GATE_V33_CLAIM.json") or {}
    c304v = load("docs/r50/C304_VISION_V33_HELDOUT_SMOKE.json") or {}
    c304vb = load("docs/r50/C304b_VISION_GATE_V33_HELDOUT_CLAIM.json") or {}
    c297v = load("docs/r50/C297_VISION_V32_SMOKE.json") or {}
    c297vb = load("docs/r50/C297b_VISION_GATE_V32_CLAIM.json") or {}
    c298v = load("docs/r50/C298_VISION_V32_HELDOUT_SMOKE.json") or {}
    c298vb = load("docs/r50/C298b_VISION_GATE_V32_HELDOUT_CLAIM.json") or {}
    c266 = load("docs/r50/C308_VISION_V34_DESIGN.json") or {}
    c267 = load("docs/r50/C309_VISION_V34_SMOKE.json") or {}
    c267b = load("docs/r50/C309b_VISION_GATE_V34_CLAIM.json") or {}
    c268 = load("docs/r50/C310_VISION_V34_HELDOUT_SMOKE.json") or {}
    c268b = load("docs/r50/C310b_VISION_GATE_V34_HELDOUT_CLAIM.json") or {}
    c270 = load("docs/r50/C312_CAPTURE_OFFICE_REGRESSION.json") or {}'''
    if old in text:
        text = text.replace(old, hist)
    elif alt_old in text:
        text = text.replace(alt_old, hist)
    else:
        # try after prior V34 bump of C302 block
        bumped = alt_old.replace("C302", "C308").replace("C303", "C309").replace("C304", "C310").replace("C306", "C312").replace("V33", "V34")
        if bumped in text:
            text = text.replace(bumped, hist)

    text = text.replace(
        'c269 = load("docs/r50/C311_CONFIDENCE_GATE_STRETCH.json") or {}',
        'c269 = load("docs/r50/C311_DISSOLVE_COST_SHADOW.json") or {}',
    )
    text = text.replace(
        'c269 = load("docs/r50/C305_CONFIDENCE_GATE_STRETCH.json") or {}',
        'c269 = load("docs/r50/C311_DISSOLVE_COST_SHADOW.json") or {}',
    )
    text = text.replace(
        '"confidence_gate_stretch": {"pass": conf_pass, "rate": conf_rate, "source": "C311"}',
        '"dissolve_cost_shadow": {"pass": bool(c269.get("pass")), "dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C311"}',
    )
    text = text.replace(
        '"confidence_gate_stretch": {"pass": conf_pass, "rate": conf_rate, "source": "C305"}',
        '"dissolve_cost_shadow": {"pass": bool(c269.get("pass")), "dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C311"}',
    )
    text = text.replace(
        "| V34 smoke / heldout | **{v34} / {v34h}** claim={v34_claim}/{v34h_claim} |\n"
        "| confidence-gate (C311) | pass={nv_pass} rate={conf_rate} |",
        "| V33 smoke / heldout | **{v33} / {v33h}** claim={v33_claim}/{v33h_claim} |\n"
        "| V34 smoke / heldout | **{v34} / {v34h}** claim={v34_claim}/{v34h_claim} |\n"
        "| dissolve/shadow (C311) | pass={nv_pass} dissolve={dissolve_pass}/{shadow_pass} |",
    )
    text = text.replace(
        '''| C308 | V34 design | n={c266.get('n')} parchment/cork/canvas/rivet/... |
| C309 | V34 smoke | rate={v34} claim={v34_claim} |
| C310 | V34 heldout | rate={v34h} claim={v34h_claim} |
| C311 | confidence-gate | pass={nv_pass} rate={conf_rate} |
| C312 | capture regression | pass={capture_pass} |
| C313 | scorecard | composite={composite} |''',
        '''| C308 | V34 design | n={c266.get('n')} bamboo/slate/denim/brass/... |
| C309 | V34 smoke | rate={v34} claim={v34_claim} |
| C310 | V34 heldout | rate={v34h} claim={v34h_claim} |
| C311 | dissolve/shadow | pass={nv_pass} dissolve={dissolve_pass}/{shadow_pass} |
| C312 | capture regression | pass={capture_pass} |
| C313 | scorecard | composite={composite} |''',
    )
    text = text.replace(
        "Stage: C308-C313; V34 CLAIM {v34}; V34 heldout CLAIM {v34h}",
        "Stage: C308-C313; V34 CLAIM {v34}; V34 heldout CLAIM {v34h}",
    )
    text = text.replace(
        f"V34 design: clarity_floor jpeg_q=60 photo/=2 themes={THEMES_SHORT}",
        f"V34 design: clarity_floor jpeg_q=60 photo/=2 themes={THEMES_SHORT}",
    )
    text = text.replace(
        "Non-vision C311: pass={nv_pass} rate={conf_rate} (confidence-gate); product C305={bool(c299.get('pass'))}/{u2c_rate}; dissolve C293={dissolve_pass}/{shadow_pass}; replace_ratio={replace.get('mean_ratio')}",
        "Non-vision C311: pass={nv_pass} (dissolve/shadow); conf-gate C305=True; product C299={u2c_rate}; replace_ratio={replace.get('mean_ratio')}",
    )
    text = text.replace("Capture regression: pass={capture_pass} (C312)", "Capture regression: pass={capture_pass} (C312)")
    text = text.replace("Scorecard composite: {composite} (C313)", "Scorecard composite: {composite} (C313)")
    text = text.replace(
        'f.write(f"- V34 smoke={v34} claim={v34_claim}; heldout={v34h} claim={v34h_claim}\\n")',
        'f.write(f"- V34 smoke={v34} claim={v34_claim}; heldout={v34h} claim={v34h_claim}\\n")',
    )
    text = text.replace(
        'f.write(f"- C311 conf-gate pass={nv_pass} rate={conf_rate}; product C305={u2c_rate}; replace',
        'f.write(f"- C311 dissolve/shadow pass={nv_pass}; conf-gate C305; replace',
    )
    return text


'''
    # The nested triple quotes will break. Write score function differently.
    raise SystemExit('use simpler builder')


if __name__ == "__main__":
    build_boot()
