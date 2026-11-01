# -*- coding: utf-8 -*-
from __future__ import annotations
import json, re
from pathlib import Path

ROOT = Path(r"E:\envolution")
SCR = ROOT / "scripts"
SPEC = ROOT / "tools" / "_v34_specs.json"

OVERLAY = """
    # --- V34 overlays (new vs V33) ---
    for _ in range(90):
        bx = rng.randint(70, 520); by = rng.randint(320, 560)
        if in_text_band(by):
            continue
        d.line([(bx, by), (bx, by + rng.randint(8, 22))], fill=(150, 170, 120), width=1)
    for lx in range(70, 240, 12):
        d.line([(lx, 300), (lx + 20, 330)], fill=(90, 95, 105), width=1)
    for di in range(8):
        x0 = 250 + di * 28
        d.line([(x0, 350), (x0 + 10, 360)], fill=(40, 60, 120), width=1)
        d.line([(x0 + 10, 350), (x0, 360)], fill=(40, 60, 120), width=1)
    d.text((250, 366), "DENIM bait 27.27", fill=(30, 40, 90), font=f_tiny)
    for by in (100, 190, 280, 370):
        d.ellipse([30, by, 54, by + 22], fill=(180, 140, 50), outline=(90, 60, 20), width=2)
    for hi, col in enumerate([(255, 60, 60), (255, 180, 40), (60, 220, 80), (60, 120, 255)]):
        d.polygon([(610 + hi * 35, 40), (640 + hi * 35, 40), (625 + hi * 35, 72)], fill=col)
    d.text((610, 76), "PRISM bait 61.61", fill=(80, 40, 120), font=f_tiny)
    d.arc([400, 340, 460, 400], 200, 340, fill=(70, 70, 80), width=3)
    d.ellipse([70, 430, 130, 480], fill=(220, 150, 40), outline=(160, 90, 20), width=2)
    d.rectangle([850, 100, 980, 155], fill=(170, 175, 180), outline=(80, 85, 90), width=2)
    d.text((870, 118), "TIN", fill=(40, 40, 50), font=f_stamp)
    d.rectangle([420, 340, 560, 415], fill=(235, 245, 255))
    d.text((430, 365), "MYLAR ghost 88.88", fill=(90, 120, 150), font=f_pen)
    d.rectangle([100, 500, 230, 545], fill=(140, 100, 80), outline=(80, 50, 40), width=2)
    d.text((120, 512), "FELT", fill=(240, 220, 200), font=f_stamp)
    d.ellipse([880, 470, 980, 555], fill=(40, 90, 160), outline=(20, 40, 80), width=3)
    d.text((900, 500), "ENML", fill=(230, 240, 255), font=f_stamp)
    d.polygon([(60, 12), (420, 12), (405, 26), (70, 26)], fill=(200, 210, 230), outline=(90, 100, 120), width=1)
    d.text((80, 13), "CHROME bait 48.48", fill=(50, 60, 90), font=f_tiny)
    for ti, ty in enumerate((90, 150, 210, 270)):
        d.polygon([(990, ty), (1020, ty + 12), (990, ty + 24)], fill=(200, 80, 80 + ti * 20))
"""

THEMES_SHORT = "bamboo/slate/denim/brass/prism/latch/amber/quarry/tin/mylar/felt/void/stitch/enamel/cord/rice/chrome/index"

def specs_to_py(rows):
    lines = ["SPECS = ["]
    for r in rows:
        lines.append(
            f'    ("{r["id"]}", "{r["kind"]}", "{r["metric"]}", {r["expected"]},\n'
            f'     {json.dumps(r["lines"], ensure_ascii=False)},\n'
            f'     {json.dumps(r["cn"], ensure_ascii=False)}, "{r["stamp"]}"),'
        )
    lines.append("]")
    return "\n".join(lines) + "\n"

def replace_specs(text, new_specs):
    return re.sub(r"SPECS = \[.*?\]\n", new_specs, text, count=1, flags=re.S)

def inject_overlay(text):
    # remove any prior V34 overlay injection
    text = re.sub(r"\n    # --- V34 overlays \(new vs V33\) ---.*?\n(?=    buf = io\.BytesIO\(\))", "\n", text, count=1, flags=re.S)
    needle = "    buf = io.BytesIO()"
    if "DENIM bait" not in text and needle in text:
        text = text.replace(needle, OVERLAY + "\n" + needle, 1)
    return text

def main():
    specs = json.loads(SPEC.read_text(encoding="utf-8"))
    train_specs = specs_to_py(specs["train"])
    held_specs = specs_to_py(specs["held"])

    t = (SCR / "c302_vision_v33_design_and_batch.py").read_text(encoding="utf-8")
    for a,b in [
        ("C302","C308"),("c302","c308"),
        ("vision_images_v33","vision_images_v34"),
        ("vision_v33","vision_v34"),
        ("VL_GATE_V33","VL_GATE_V34"),("vl_gate_v33","vl_gate_v34"),
        ("vision_gate_v33","vision_gate_v34"),("r50plus_v33","r50plus_v34"),
        ("SCAN DESK V33","SCAN DESK V34"),
        ("V33 C302","V34 C308"),("V33 C308","V34 C308"),
    ]:
        t = t.replace(a,b)
    t = replace_specs(t, train_specs)
    t = inject_overlay(t)
    assert "buf = io.BytesIO()" in t
    assert "GaussianBlur" in t
    assert "v34_01" in t and "bamboo_recv" in t and "DENIM bait" in t
    (SCR / "c308_vision_v34_design_and_batch.py").write_text(t, encoding="utf-8")
    print("design OK")

    t = (SCR / "c303_vision_v33_smoke.py").read_text(encoding="utf-8")
    for a,b in [("C303","C309"),("c303","c309"),("vision_images_v33","vision_images_v34"),("vision_v33_c303","vision_v34_c309"),("vision_v33","vision_v34"),("VL_GATE_V33","VL_GATE_V34"),("vl_gate_v33","vl_gate_v34"),("r50plus_v33","r50plus_v34")]:
        t = t.replace(a,b)
    (SCR / "c309_vision_v34_smoke.py").write_text(t, encoding="utf-8")
    print("smoke OK")

    t = (SCR / "c304_vision_v33_heldout.py").read_text(encoding="utf-8")
    for a,b in [("C304","C310"),("c304","c310"),("vision_images_v33h","vision_images_v34h"),("vision_images_v33","vision_images_v34"),("vision_v33h_c304","vision_v34h_c310"),("VL_GATE_V33_HELDOUT","VL_GATE_V34_HELDOUT"),("vl_gate_v33_heldout","vl_gate_v34_heldout"),("vision_gate_v33_heldout","vision_gate_v34_heldout"),("r50plus_v33_heldout","r50plus_v34_heldout"),("vision_v33_heldout","vision_v34_heldout"),("SCAN DESK V33H","SCAN DESK V34H"),("V33H C304","V34H C310"),("V33H C310","V34H C310")]:
        t = t.replace(a,b)
    t = replace_specs(t, held_specs)
    assert "v34h_01" in t
    (SCR / "c310_vision_v34_heldout.py").write_text(t, encoding="utf-8")
    print("heldout OK")

    t = (SCR / "c293_dissolve_cost_shadow.py").read_text(encoding="utf-8")
    t = t.replace("C293","C311").replace("dissolve_cost_shadow_c293","dissolve_cost_shadow_c311").replace("C293_DISSOLVE_COST_SHADOW.json","C311_DISSOLVE_COST_SHADOW.json").replace("c293","c311")
    (SCR / "c311_dissolve_cost_shadow.py").write_text(t, encoding="utf-8")
    print("nv OK")

    t = (SCR / "c306_capture_office_regression.py").read_text(encoding="utf-8")
    t = t.replace("C306","C312").replace("C302-C305","C308-C311").replace("c302_c305","c308_c311").replace("capture_regression_c306","capture_regression_c312")
    needle = '("V33_heldout", DOC / "C304_VISION_V33_HELDOUT_SMOKE.json"),'
    if needle in t and '("V34"' not in t:
        t = t.replace(needle, needle + '\n    ("V34", DOC / "C309_VISION_V34_SMOKE.json"),\n    ("V34_heldout", DOC / "C310_VISION_V34_HELDOUT_SMOKE.json"),')
    n2 = '("C305_confidence_gate_stretch", DOC / "C305_CONFIDENCE_GATE_STRETCH.json"),'
    if n2 in t and "C311_dissolve" not in t:
        t = t.replace(n2, n2 + '\n    ("C311_dissolve_cost_shadow", DOC / "C311_DISSOLVE_COST_SHADOW.json"),')
    t = t.replace('"V33", "V33_heldout", "C233_clarity_floor", "C305_confidence_gate_stretch"]',
                  '"V33", "V33_heldout", "V34", "V34_heldout", "C233_clarity_floor", "C311_dissolve_cost_shadow"]')
    t = t.replace('DOC / "C306_CAPTURE_OFFICE_REGRESSION.json"', 'DOC / "C312_CAPTURE_OFFICE_REGRESSION.json"')
    (SCR / "c312_capture_office_regression.py").write_text(t, encoding="utf-8")
    print("reg OK")

    t = (SCR / "c307_scorecard_and_stage.py").read_text(encoding="utf-8")
    for a,b in [("C307","C313"),("c302_c306","c308_c312"),("STAGE_ANT_C307.md","STAGE_ANT_C313.md"),("C302-C306","C308-C312"),("C302-C307","C308-C313"),("unified_scorecard_c302_c306","unified_scorecard_c308_c312"),("C302_VISION_V33_DESIGN","C308_VISION_V34_DESIGN"),("C303_VISION_V33_SMOKE","C309_VISION_V34_SMOKE"),("C303b_VISION_GATE_V33_CLAIM","C309b_VISION_GATE_V34_CLAIM"),("C304_VISION_V33_HELDOUT_SMOKE","C310_VISION_V34_HELDOUT_SMOKE"),("C304b_VISION_GATE_V33_HELDOUT_CLAIM","C310b_VISION_GATE_V34_HELDOUT_CLAIM"),("C306_CAPTURE_OFFICE_REGRESSION","C312_CAPTURE_OFFICE_REGRESSION"),("C305_CONFIDENCE_GATE_STRETCH","C311_DISSOLVE_COST_SHADOW")]:
        t = t.replace(a,b)
    t = t.replace('"confidence_gate_stretch"', '"dissolve_cost_shadow"')
    t = t.replace('"source": "C305"', '"source": "C311"')
    t = t.replace("V33", "V34").replace("v33", "v34")
    t = t.replace("parchment/cork/canvas/rivet/holo/zip/filament/honey/marble/copper/acetate/perf/waxseal/magnet/crepe/satin/spiral", THEMES_SHORT)
    t = t.replace("parchment/cork/canvas/rivet/...", "bamboo/slate/denim/brass/...")
    t = t.replace("confidence-gate", "dissolve/shadow")
    (SCR / "c313_scorecard_and_stage.py").write_text(t, encoding="utf-8")
    print("score OK")
    print("BOOT_OK")

if __name__ == "__main__":
    main()
