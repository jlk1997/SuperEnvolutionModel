# -*- coding: utf-8 -*-
"""Patch copied V37 boot into V38 boot, then emit scripts."""
from __future__ import annotations
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
boot = ROOT / "tools" / "_boot_v38_c332.py"
text = boot.read_text(encoding="utf-8")

# docstring / header
text = text.replace("C326-C331 Vision V37 from V36 + confidence NV", "C332-C337 Vision V38 from V37 + product U2C NV")
text = text.replace("Bootstrap C326-C331", "Bootstrap C332-C337")

KINDS_BLOCK = '''KINDS = [
    ("cedar_recv", "paid_total", "CEDAR GRAIN RECV V38", "柏木收款单", "RECV"),
    ("jasper_wh", "qty_sum", "WH JASPER TILE V38", "碧玉仓位单", "RECV"),
    ("gauze_refund", "refund_done", "GAUZE PATCH REFUND V38", "纱布补丁退款单", "DONE"),
    ("cyan_tax", "tax_base_paid", "CYAN TAX SLIP V38", "青空税基单", "TAX"),
    ("feldspar_pay", "payroll_active", "FELDSPAR PAYROLL V38", "长石薪资单", "PAY"),
    ("hinge_ship", "ship_ok", "HINGE SHIP DOCK V38", "铰链出库单", "SHIP"),
    ("citrine_sla", "sla_ok_hours", "CITRINE SLA CARD V38", "黄水晶SLA卡", "SLA"),
    ("basalt_exp", "exp_sum", "BASALT EXPENSE V38", "玄武岩费用单", "EXP"),
    ("pewter_po", "po_open", "PEWTER PO SHEET V38", "白镴采购单", "PO"),
    ("parchment_order", "order_paid", "PARCHMENT ORDER V38", "羊皮纸订单", "ORD"),
    ("herringbone_dup", "dup_mark", "HERRINGBONE DUP MARK V38", "鱼骨纹重复标", "DUP"),
    ("nil_zero", "zero_check", "NIL VOID ZERO V38", "空值零检单", "ZERO"),
    ("burlap_ledger", "ledger_net", "BURLAP LEDGER V38", "麻布账本", "LED"),
    ("lacquer_ui", "ui_ok", "LACQUER UI SCAN V38", "漆面界面扫描", "UI"),
    ("coir_stack", "stack_count", "COIR STACK V38", "棕丝堆叠单", "STK"),
    ("mulberry_fax", "fax_pages", "MULBERRY FAX V38", "桑档传真单", "FAX"),
    ("iridium_glare", "glare_ok", "IRIDIUM GLARE V38", "铱光眩光单", "GLR"),
    ("folio_tab", "tab_index", "FOLIO TAB INDEX V38", "简册页签索引", "TAB"),
]
'''

TRAIN_BLOCK = '''TRAIN_NUMS = [
    (127.5, [61.00, 66.50, 19.00]),
    (94.0, [36, 31, 44]),
    (71.25, [34.00, 37.25, 14.00]),
    (188.0, [91.00, 97.00, 41.00]),
    (256.0, [126.00, 130.00, 34.00]),
    (63.0, [29, 17, 21]),
    (81.5, [43.00, 38.50, 20.00]),
    (107.75, [51.00, 56.75, 24.00]),
    (121.0, [65.00, 56.00, 28.00]),
    (146.5, [78.00, 68.50, 21.00]),
    (2.0, [1, 1, 0]),
    (0.0, [0.00, 0.00, 0.00]),
    (221.25, [108.00, 113.25, 36.00]),
    (1.0, [1, 0, 0]),
    (11.0, [5, 4, 2]),
    (16.0, [8, 8, 3]),
    (1.0, [1, 0, 0]),
    (21.0, [12, 9, 2]),
]
'''

HELD_BLOCK = '''HELD_NUMS = [
    (74.75, [36.00, 38.75, 15.00]),
    (53.0, [23, 12, 30]),
    (42.5, [20.00, 22.50, 9.00]),
    (104.0, [51.00, 53.00, 24.00]),
    (138.0, [69.00, 69.00, 19.00]),
    (35.0, [17, 9, 13]),
    (45.25, [24.00, 21.25, 11.00]),
    (58.5, [28.00, 30.50, 13.00]),
    (66.0, [35.00, 31.00, 15.00]),
    (81.25, [43.00, 38.25, 12.00]),
    (2.0, [1, 1, 0]),
    (0.0, [0.00, 0.00, 0.00]),
    (123.75, [59.00, 64.75, 19.00]),
    (1.0, [1, 0, 0]),
    (6.0, [3, 2, 1]),
    (9.0, [5, 4, 2]),
    (1.0, [1, 0, 0]),
    (12.0, [7, 5, 1]),
]
'''

text = re.sub(r"KINDS = \[.*?\]\n", KINDS_BLOCK, text, count=1, flags=re.S)
text = re.sub(r"TRAIN_NUMS = \[.*?\]\n", TRAIN_BLOCK, text, count=1, flags=re.S)
text = re.sub(r"HELD_NUMS = \[.*?\]\n", HELD_BLOCK, text, count=1, flags=re.S)

# id prefixes inside build_lines / loops
text = text.replace('f"v37{tag}_{i+1:02d}"', 'f"v38{tag}_{i+1:02d}"')
text = text.replace('s["id"] = f"v37_{i+1:02d}"', 's["id"] = f"v38_{i+1:02d}"')
text = text.replace('s["id"] = f"v37h_{i+1:02d}"', 's["id"] = f"v38h_{i+1:02d}"')
text = text.replace('"_v37_specs.json"', '"_v38_specs.json"')

V38_OVERLAY = r'''
    # --- V38 overlays (new vs V37) ---
    for _ in range(100):
        bx = rng.randint(50, 540)
        by = rng.randint(350, 580)
        if in_text_band(by):
            continue
        d.line([(bx, by), (bx + rng.randint(5, 22), by + rng.randint(-4, 4))], fill=(90, 70, 40), width=1)
    for gi in range(5):
        d.ellipse([48 + gi * 24, 308, 66 + gi * 24, 326], outline=(40, 90, 50), width=2)
    d.text((48, 328), "CEDAR bait 38.38", fill=(80, 50, 20), font=f_tiny)
    for hi in range(4):
        d.polygon([(580 + hi * 34, 36), (606 + hi * 34, 36), (593 + hi * 34, 72)], fill=(20, 90, 140))
    d.text((580, 76), "CYAN bait 58.58", fill=(10, 40, 80), font=f_tiny)
    d.rectangle([250, 380, 410, 440], fill=(245, 250, 255))
    d.text((260, 400), "FELDSPAR ghost 88.88", fill=(40, 70, 90), font=f_pen)
    d.arc([410, 370, 500, 440], 20, 240, fill=(160, 120, 20), width=3)
    d.text((410, 445), "CITRINE bait 33.33", fill=(130, 90, 10), font=f_tiny)
    d.ellipse([60, 470, 130, 530], fill=(90, 95, 100), outline=(40, 45, 50), width=2)
    d.text((60, 535), "BASALT bait 24.24", fill=(50, 55, 60), font=f_tiny)
    for qi in range(4):
        d.rectangle([250 + qi * 42, 470, 282 + qi * 42, 502], outline=(80, 70, 50), width=2)
    d.rectangle([850, 110, 1000, 170], fill=(170, 175, 180), outline=(50, 55, 60), width=2)
    d.text((870, 128), "PEWTER", fill=(20, 25, 30), font=f_stamp)
    d.polygon([(40, 4), (420, 4), (405, 18), (50, 18)], fill=(210, 200, 180), outline=(90, 70, 50), width=1)
    d.text((70, 5), "IRIDIUM bait 68.68", fill=(30, 35, 45), font=f_tiny)
    for ti, ty in enumerate((90, 150, 210)):
        d.polygon([(1000, ty), (1024, ty + 12), (1000, ty + 24)], fill=(70, 100, 60 + ti * 20))
'''

text = re.sub(r"V37_OVERLAY = r'''.*?'''", "V38_OVERLAY = r'''" + V38_OVERLAY + "'''", text, count=1, flags=re.S)
text = text.replace("V37_OVERLAY", "V38_OVERLAY")
text = text.replace('"WALNUT bait"', '"CEDAR bait"')
text = text.replace("WALNUT bait", "CEDAR bait")

THEMES = "cedar/jasper/gauze/cyan/feldspar/hinge/citrine/basalt/pewter/parchment/herringbone/nil/burlap/lacquer/coir/mulberry/iridium/folio"
OLD_THEMES = "walnut/onyx/linen/indigo/quartz/latch/amber/shale/chrome/bond/tweed/void/hemp/enamel/raffia/plum/tungsten/binder"
text = re.sub(r'THEMES = ".*?"', f'THEMES = "{THEMES}"', text, count=1)
text = re.sub(r'OLD_THEMES = ".*?"', f'OLD_THEMES = "{OLD_THEMES}"', text, count=1)

# inject_overlay comment and regex for V36->V37 becomes V37->V38
text = text.replace("# --- V37 overlays (new vs V36) ---", "# --- V38 overlays (new vs V37) ---")
text = text.replace(r"# --- V36 overlays", r"# --- V37 overlays")
# After V37_OVERLAY rename, the inject still strips V36; make it strip V37
text = text.replace(
    r'\n    # --- V36 overlays.*?\n(?=    img\.save\(buf)',
    r'\n    # --- V37 overlays.*?\n(?=    img\.save\(buf)',
)
# If already changed to V37 strip in copied file:
text = text.replace(
    "re.sub(r\"\\n    # --- V36 overlays.*?\\n(?=    img\\.save\\(buf)\"",
    "re.sub(r\"\\n    # --- V37 overlays.*?\\n(?=    img\\.save\\(buf)\"",
)

# xform_train reps: rewrite block by replacing known strings
text = text.replace('("C320", "C326"), ("c320", "c326")', '("C326", "C332"), ("c326", "c332")')
text = text.replace('"vision_images_v36", "vision_images_v37"', '"vision_images_v37", "vision_images_v38"')
text = text.replace('"vision_v36", "vision_v37"', '"vision_v37", "vision_v38"')
text = text.replace('"VL_GATE_V36", "VL_GATE_V37"', '"VL_GATE_V37", "VL_GATE_V38"')
text = text.replace('"vl_gate_v36", "vl_gate_v37"', '"vl_gate_v37", "vl_gate_v38"')
text = text.replace('"vision_gate_v36", "vision_gate_v37"', '"vision_gate_v37", "vision_gate_v38"')
text = text.replace('"r50plus_v36", "r50plus_v37"', '"r50plus_v37", "r50plus_v38"')
text = text.replace('"SCAN DESK V36", "SCAN DESK V37"', '"SCAN DESK V37", "SCAN DESK V38"')
text = text.replace('"V36 C320", "V37 C326"), ("V36 C326", "V37 C326")', '"V37 C326", "V38 C332"), ("V37 C332", "V38 C332")')
text = text.replace('"V36 keeps floor", "V37 keeps floor"', '"V37 keeps floor", "V38 keeps floor"')
text = text.replace('"teak_recv", "walnut_recv"', '"walnut_recv", "cedar_recv"')
text = text.replace('"TEAK bait", "WALNUT bait"', '"WALNUT bait", "CEDAR bait"')
# after WALNUT->CEDAR global, the TEAK line may already be CEDAR
text = text.replace('"TEAK bait", "CEDAR bait"', '"WALNUT bait", "CEDAR bait"')
text = text.replace(r'v3[67]_01', r'v3[78]_01')

# smoke
text = text.replace('("C321", "C327"), ("c321", "c327")', '("C327", "C333"), ("c327", "c333")')
text = text.replace('"vision_v36_c321", "vision_v37_c327"', '"vision_v37_c327", "vision_v38_c333"')
text = text.replace('"C321_VISION_V36", "C327_VISION_V37"', '"C327_VISION_V37", "C333_VISION_V38"')
text = text.replace('"C321b_VISION_GATE_V36", "C327b_VISION_GATE_V37"', '"C327b_VISION_GATE_V37", "C333b_VISION_GATE_V38"')
text = text.replace('"VISION_V36_SMOKE", "VISION_V37_SMOKE"', '"VISION_V37_SMOKE", "VISION_V38_SMOKE"')
text = text.replace('"VISION_GATE_V36_CLAIM", "VISION_GATE_V37_CLAIM"', '"VISION_GATE_V37_CLAIM", "VISION_GATE_V38_CLAIM"')

# heldout
text = text.replace('("C322", "C328"), ("c322", "c328")', '("C328", "C334"), ("c328", "c334")')
text = text.replace('"vision_images_v36h", "vision_images_v37h"', '"vision_images_v37h", "vision_images_v38h"')
text = text.replace('"vision_v36h_c322", "vision_v37h_c328"', '"vision_v37h_c328", "vision_v38h_c334"')
text = text.replace('"VL_GATE_V36_HELDOUT", "VL_GATE_V37_HELDOUT"', '"VL_GATE_V37_HELDOUT", "VL_GATE_V38_HELDOUT"')
text = text.replace('"vl_gate_v36_heldout", "vl_gate_v37_heldout"', '"vl_gate_v37_heldout", "vl_gate_v38_heldout"')
text = text.replace('"vision_gate_v36_heldout", "vision_gate_v37_heldout"', '"vision_gate_v37_heldout", "vision_gate_v38_heldout"')
text = text.replace('"r50plus_v36_heldout", "r50plus_v37_heldout"', '"r50plus_v37_heldout", "r50plus_v38_heldout"')
text = text.replace('"vision_v36_heldout", "vision_v37_heldout"', '"vision_v37_heldout", "vision_v38_heldout"')
text = text.replace('"SCAN DESK V36H", "SCAN DESK V37H"', '"SCAN DESK V37H", "SCAN DESK V38H"')
text = text.replace('"V36H C322", "V37H C328"), ("V36H C328", "V37H C328")', '"V37H C328", "V38H C334"), ("V37H C334", "V38H C334")')
text = text.replace('"VISION_V36_HELDOUT", "VISION_V37_HELDOUT"', '"VISION_V37_HELDOUT", "VISION_V38_HELDOUT"')
text = text.replace('"VISION_GATE_V36_HELDOUT", "VISION_GATE_V37_HELDOUT"', '"VISION_GATE_V37_HELDOUT", "VISION_GATE_V38_HELDOUT"')
text = text.replace('"_v36hc322", "_v37hc328"', '"_v37hc328", "_v38hc334"')
text = text.replace("'\"version\": \"v36h\"', '\"version\": \"v37h\"'", "'\"version\": \"v37h\"', '\"version\": \"v38h\"'")
text = text.replace(r'v3[67]h_01', r'v3[78]h_01')

# NV: confidence -> product_u2c from c317
old_nv = '''def xform_nv(text):
    text = text.replace("C305", "C329").replace("c305", "c329")
    text = text.replace("confidence_gate_stretch_c305", "confidence_gate_stretch_c329")
    text = text.replace("C305_CONFIDENCE_GATE_STRETCH.json", "C329_CONFIDENCE_GATE_STRETCH.json")
    return text
'''
new_nv = '''def xform_nv(text):
    text = text.replace("C317", "C335").replace("c317", "c335")
    text = text.replace("product_u2c_cost_c317", "product_u2c_cost_c335")
    text = text.replace("C317_PRODUCT_U2C_COST.json", "C335_PRODUCT_U2C_COST.json")
    return text
'''
if old_nv in text:
    text = text.replace(old_nv, new_nv)
else:
    text = re.sub(r"def xform_nv\(text\):.*?return text\n", new_nv, text, count=1, flags=re.S)

# regression
text = text.replace('text = text.replace("C324", "C330").replace("c324", "c330")',
                    'text = text.replace("C330", "C336").replace("c330", "c336")')
text = text.replace('text = text.replace("C320-C323", "C326-C329")',
                    'text = text.replace("C326-C329", "C332-C335")')
text = text.replace('text = text.replace("c320_c323", "c326_c329")',
                    'text = text.replace("c326_c329", "c332_c335")')
text = text.replace('text = text.replace("capture_regression_c324", "capture_regression_c330")',
                    'text = text.replace("capture_regression_c330", "capture_regression_c336")')

# needles in xform_reg - rewrite carefully
text = text.replace(
    'needle = \'("V36_heldout", DOC / "C322_VISION_V36_HELDOUT_SMOKE.json"),\'',
    'needle = \'("V37_heldout", DOC / "C328_VISION_V37_HELDOUT_SMOKE.json"),\'',
)
text = text.replace('\'("V37"\' not in text', '\'("V38"\' not in text')
text = text.replace(
    '            + \'\\n    ("V37", DOC / "C327_VISION_V37_SMOKE.json"),\'\n'
    '            + \'\\n    ("V37_heldout", DOC / "C328_VISION_V37_HELDOUT_SMOKE.json"),\',',
    '            + \'\\n    ("V38", DOC / "C333_VISION_V38_SMOKE.json"),\'\n'
    '            + \'\\n    ("V38_heldout", DOC / "C334_VISION_V38_HELDOUT_SMOKE.json"),\',',
)
text = text.replace(
    'needle2 = \'("C323_dissolve_cost_shadow", DOC / "C323_DISSOLVE_COST_SHADOW.json"),\'',
    'needle2 = \'("C329_confidence_gate_stretch", DOC / "C329_CONFIDENCE_GATE_STRETCH.json"),\'',
)
text = text.replace('"C329_confidence" not in text', '"C335_product" not in text')
text = text.replace(
    '            + \'\\n    ("C329_confidence_gate_stretch", DOC / "C329_CONFIDENCE_GATE_STRETCH.json"),\',',
    '            + \'\\n    ("C335_product_u2c_cost", DOC / "C335_PRODUCT_U2C_COST.json"),\',',
)
text = text.replace(
    '\'"V36", "V36_heldout", "C233_clarity_floor", "C323_dissolve_cost_shadow"]\'',
    '\'"V37", "V37_heldout", "C233_clarity_floor", "C329_confidence_gate_stretch"]\'',
)
# After first pass the required_list replace target in boot may already mention V37:
text = text.replace(
    '\'"V36", "V36_heldout", "V37", "V37_heldout", "C233_clarity_floor", "C329_confidence_gate_stretch"]\'',
    '\'"V37", "V37_heldout", "V38", "V38_heldout", "C233_clarity_floor", "C335_product_u2c_cost"]\'',
)
text = text.replace(
    '\'"V37", "V37_heldout", "C233_clarity_floor", "C329_confidence_gate_stretch"]\'',
    '\'"V37", "V37_heldout", "V38", "V38_heldout", "C233_clarity_floor", "C335_product_u2c_cost"]\'',
)
text = text.replace(
    'text = text.replace(\'DOC / "C324_CAPTURE_OFFICE_REGRESSION.json"\', \'DOC / "C330_CAPTURE_OFFICE_REGRESSION.json"\')',
    'text = text.replace(\'DOC / "C330_CAPTURE_OFFICE_REGRESSION.json"\', \'DOC / "C336_CAPTURE_OFFICE_REGRESSION.json"\')',
)

# scorecard
text = text.replace('text = text.replace("C325", "C331").replace("c325", "c331")',
                    'text = text.replace("C331", "C337").replace("c331", "c337")')
text = text.replace('text = text.replace("c320_c324", "c326_c330")',
                    'text = text.replace("c326_c330", "c332_c336")')
text = text.replace('text = text.replace("STAGE_ANT_C325.md", "STAGE_ANT_C331.md")',
                    'text = text.replace("STAGE_ANT_C331.md", "STAGE_ANT_C337.md")')
text = text.replace('text = text.replace("C320-C324", "C326-C330")',
                    'text = text.replace("C326-C330", "C332-C336")')
text = text.replace('text = text.replace("C320-C325", "C326-C331")',
                    'text = text.replace("C326-C331", "C332-C337")')
text = text.replace('text = text.replace("unified_scorecard_c320_c324", "unified_scorecard_c326_c330")',
                    'text = text.replace("unified_scorecard_c326_c330", "unified_scorecard_c332_c336")')
text = text.replace('text = text.replace("unified_scorecard_c320_c325", "unified_scorecard_c326_c331")',
                    'text = text.replace("unified_scorecard_c326_c331", "unified_scorecard_c332_c337")')
text = text.replace('C320_VISION_V36_DESIGN", "C326_VISION_V37_DESIGN"',
                    'C326_VISION_V37_DESIGN", "C332_VISION_V38_DESIGN"')
text = text.replace('C321_VISION_V36_SMOKE", "C327_VISION_V37_SMOKE"',
                    'C327_VISION_V37_SMOKE", "C333_VISION_V38_SMOKE"')
text = text.replace('C321b_VISION_GATE_V36_CLAIM", "C327b_VISION_GATE_V37_CLAIM"',
                    'C327b_VISION_GATE_V37_CLAIM", "C333b_VISION_GATE_V38_CLAIM"')
text = text.replace('C322_VISION_V36_HELDOUT_SMOKE", "C328_VISION_V37_HELDOUT_SMOKE"',
                    'C328_VISION_V37_HELDOUT_SMOKE", "C334_VISION_V38_HELDOUT_SMOKE"')
text = text.replace('C322b_VISION_GATE_V36_HELDOUT_CLAIM", "C328b_VISION_GATE_V37_HELDOUT_CLAIM"',
                    'C328b_VISION_GATE_V37_HELDOUT_CLAIM", "C334b_VISION_GATE_V38_HELDOUT_CLAIM"')
text = text.replace('C324_CAPTURE_OFFICE_REGRESSION", "C330_CAPTURE_OFFICE_REGRESSION"',
                    'C330_CAPTURE_OFFICE_REGRESSION", "C336_CAPTURE_OFFICE_REGRESSION"')
text = text.replace('text = text.replace("vl_gate_v36", "vl_gate_v37")',
                    'text = text.replace("vl_gate_v37", "vl_gate_v38")')
text = text.replace('text = text.replace("v36_claim", "v37_claim").replace("v36h_claim", "v37h_claim")',
                    'text = text.replace("v37_claim", "v38_claim").replace("v37h_claim", "v38h_claim")')
text = text.replace('text = text.replace("v36 =", "v37 =").replace("v36h =", "v37h =")',
                    'text = text.replace("v37 =", "v38 =").replace("v37h =", "v38h =")')
text = text.replace('text = text.replace("max(v36, v36h", "max(v37, v37h")',
                    'text = text.replace("max(v37, v37h", "max(v38, v38h")')
text = text.replace('text = text.replace(\'"v36_design"\', \'"v37_design"\')',
                    'text = text.replace(\'"v37_design"\', \'"v38_design"\')')
text = text.replace('text = text.replace(\'"v36_smoke"\', \'"v37_smoke"\')',
                    'text = text.replace(\'"v37_smoke"\', \'"v38_smoke"\')')
text = text.replace('text = text.replace(\'"v36_heldout"\', \'"v37_heldout"\')',
                    'text = text.replace(\'"v37_heldout"\', \'"v38_heldout"\')')
text = text.replace('text = text.replace("teak/marble/canvas/cobalt/...", "walnut/onyx/linen/indigo/...")',
                    'text = text.replace("walnut/onyx/linen/indigo/...", "cedar/jasper/gauze/cyan/...")')
text = text.replace('text = text.replace("dissolve/cost/shadow", "confidence/gate/stretch")',
                    'text = text.replace("confidence/gate/stretch", "product/u2c/cost")')
text = text.replace('text = text.replace("dissolve/shadow", "confidence/stretch")',
                    'text = text.replace("confidence/stretch", "product/u2c")')
text = text.replace(
    'text = text.replace(\'c269 = load("docs/r50/C323_DISSOLVE_COST_SHADOW.json")\', \'c269 = load("docs/r50/C329_CONFIDENCE_GATE_STRETCH.json")\')',
    'text = text.replace(\'c269 = load("docs/r50/C329_CONFIDENCE_GATE_STRETCH.json")\', \'c269 = load("docs/r50/C335_PRODUCT_U2C_COST.json")\')',
)
text = text.replace(
    'text = text.replace(\'c311 = load("docs/r50/C323_DISSOLVE_COST_SHADOW.json")\', \'c311 = load("docs/r50/C329_CONFIDENCE_GATE_STRETCH.json")\')',
    'text = text.replace(\'c311 = load("docs/r50/C329_CONFIDENCE_GATE_STRETCH.json")\', \'c311 = load("docs/r50/C335_PRODUCT_U2C_COST.json")\')',
)
text = text.replace('text = text.replace(\'"source": "C323"\', \'"source": "C329"\')',
                    'text = text.replace(\'"source": "C329"\', \'"source": "C335"\')')
text = text.replace('text = text.replace(\'"dissolve_cost_shadow"\', \'"confidence_gate_stretch"\')',
                    'text = text.replace(\'"confidence_gate_stretch"\', \'"product_u2c_cost"\')')

# main mapping
old_map = '''    mapping = [
        ("c320_vision_v36_design_and_batch.py", "c326_vision_v37_design_and_batch.py", lambda t: xform_train(t, train_src)),
        ("c321_vision_v36_smoke.py", "c327_vision_v37_smoke.py", xform_smoke),
        ("c322_vision_v36_heldout.py", "c328_vision_v37_heldout.py", lambda t: xform_heldout(t, held_src)),
        ("c305_confidence_gate_stretch.py", "c329_confidence_gate_stretch.py", xform_nv),
        ("c324_capture_office_regression.py", "c330_capture_office_regression.py", xform_reg),
        ("c325_scorecard_and_stage.py", "c331_scorecard_and_stage.py", xform_score),
    ]'''
new_map = '''    mapping = [
        ("c326_vision_v37_design_and_batch.py", "c332_vision_v38_design_and_batch.py", lambda t: xform_train(t, train_src)),
        ("c327_vision_v37_smoke.py", "c333_vision_v38_smoke.py", xform_smoke),
        ("c328_vision_v37_heldout.py", "c334_vision_v38_heldout.py", lambda t: xform_heldout(t, held_src)),
        ("c317_product_u2c_cost.py", "c335_product_u2c_cost.py", xform_nv),
        ("c330_capture_office_regression.py", "c336_capture_office_regression.py", xform_reg),
        ("c331_scorecard_and_stage.py", "c337_scorecard_and_stage.py", xform_score),
    ]'''
if old_map in text:
    text = text.replace(old_map, new_map)
else:
    text = re.sub(r"    mapping = \[.*?\n    \]", new_map, text, count=1, flags=re.S)

text = text.replace('c326_vision_v37_design_and_batch.py', 'c332_vision_v38_design_and_batch.py')
text = text.replace('assert "vision_images_v37"', 'assert "vision_images_v38"')
text = text.replace('assert "v37_01"', 'assert "v38_01"')
text = text.replace('assert "WALNUT bait"', 'assert "CEDAR bait"')
text = text.replace('assert "walnut_recv"', 'assert "cedar_recv"')
# after global WALNUT->CEDAR the assert may already say CEDAR
text = text.replace('c331_scorecard_and_stage.py', 'c337_scorecard_and_stage.py')
text = text.replace('assert "STAGE_ANT_C331.md"', 'assert "STAGE_ANT_C337.md"')
text = text.replace('assert "C327_VISION_V37_SMOKE"', 'assert "C333_VISION_V38_SMOKE"')

boot.write_text(text, encoding="utf-8")
print("patched boot", boot.stat().st_size)
# sanity
assert "c332_vision_v38" in text
assert "CEDAR bait" in text or "cedar_recv" in text
assert "C335" in text
print("sanity ok")
