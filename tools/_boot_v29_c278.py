# -*- coding: utf-8 -*-
"""Bootstrap C278-C283 Vision V29 suite from V28 scripts."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCR = ROOT / "scripts"

# New themes (distinct labels) + disjoint amounts vs V28/V28h
TRAIN_SPECS = '''SPECS = [
    ("v29_01", "chalk_recv", "paid_total", 97.5,
     ["CHALK DUST RECV V29", "a paid 47.00", "b paid 50.50", "c open 13.00", "TOTAL PAID TARGET 97.50"],
     "粉笔灰收款单", "RECV"),
    ("v29_02", "fan_wh", "qty_sum", 88.0,
     ["WH STAPLE FAN V29", "SKU1 qty 41 ok", "SKU2 qty 19 hold", "SKU3 qty 47 ok", "qty_sum TARGET 88"],
     "扇钉仓单", "RECV"),
    ("v29_03", "carbon_refund", "refund_done", 54.75,
     ["CARBON COPY REFUND V29", "itemR1 26.00 done", "itemR2 28.75 done", "itemR3 11.00 open", "refund_done TARGET 54.75"],
     "复写退款单", "DONE"),
    ("v29_04", "toner_tax", "tax_base_paid", 156.0,
     ["TAX TONER STREAK V29", "T1 88.00 paid", "T2 35.00 open", "T3 68.00 paid", "tax_base_paid TARGET 156.00"],
     "碳粉税基单", "RECV"),
    ("v29_05", "lamp_pay", "payroll_active", 2780.0,
     ["PAYROLL LAMP HOTSPOT V29", "A 1420 active", "B 280 leave", "C 1360 active", "payroll_active TARGET 2780"],
     "台灯眩光工资单", "OK"),
    ("v29_06", "foil_ship", "ship_ok_qty", 73.0,
     ["SHIP FOIL GLARE V29", "P1 37 ok", "P2 18 hold", "P3 36 ok", "ship_ok_qty TARGET 73"],
     "箔光运单", "SHIP"),
    ("v29_07", "wax_sla", "open_pri_sum", 69.0,
     ["SLA WAX SEAL BAIT V29", "S1 pri 29 open", "S2 pri 31 closed", "S3 pri 40 open", "open_pri_sum TARGET 69"],
     "蜡封印SLA", "OPEN"),
    ("v29_08", "magnet_exp", "paid_total", 131.25,
     ["EXPENSE MAGNET CLIP V29", "E1 63.00 paid", "E2 24.00 void", "E3 68.25 paid", "paid_total TARGET 131.25"],
     "磁夹报销单", "RECV"),
    ("v29_09", "accordion_po", "paid_total", 99.5,
     ["PO-ACCORDION FOLD V29", "itemA paid 48.00", "itemB paid 51.50", "itemC open 16.00", "TOTAL PAID TARGET 99.50"],
     "手风琴采购单", "RECV"),
    ("v29_10", "perforate_order", "paid_total", 84.0,
     ["ORDER PERFORATE EDGE V29", "A paid 41.00", "B paid 43.00", "C open 12.00", "TOTAL PAID TARGET 84.00"],
     "撕孔订单", "RECV"),
    ("v29_11", "xfold_dup", "paid_total", 118.5,
     ["INVOICE #V29-XFOLD", "lineA paid 39.50", "lineB paid 39.50", "lineC paid 39.50", "TOTAL PAID TARGET 118.50"],
     "交叉折页联单", "RECV"),
    ("v29_12", "ghost_zero", "paid_total", 0.0,
     ["OPEN ONLY V29", "X 61.00 open", "Y 64.00 open", "paid_total TARGET 0.00"],
     "复写鬼影未付", "HOLD"),
    ("v29_13", "highlighter_ledger", "paid_total", 66.5,
     ["LEDGER HIGHLIGHTER V29", "rA paid 32.00", "rB paid 34.50", "rC open 10.00", "TOTAL PAID TARGET 66.50"],
     "荧光笔台账", "RECV"),
    ("v29_14", "postit_ui", "paid_total", 77.25,
     ["UI POSTIT EDGE V29", "alpha paid 37.00", "beta paid 40.25", "gamma open 13.00", "TOTAL PAID TARGET 77.25"],
     "便利贴界面", "RECV"),
    ("v29_15", "thermal_stack", "paid_total", 113.0,
     ["THERMAL FADE STACK V29", "x paid 55.00 usd", "y paid 58.00 usd", "z open 19.00 usd", "TOTAL PAID TARGET 113.00"],
     "热敏褪色叠页", "RECV"),
    ("v29_16", "bluepen_fax", "paid_total", 64.5,
     ["CN-EN BLUEPEN FAX V29", "tea paid 31.00", "rice paid 33.50", "soup open 11.00", "TOTAL PAID TARGET 64.50"],
     "蓝笔传真混排", "RECV"),
    ("v29_17", "binder_glare", "paid_total", 89.75,
     ["BINDER CLIP GLARE V29", "w1 paid 43.00", "w2 paid 46.75", "w3 open 15.00", "TOTAL PAID TARGET 89.75"],
     "长尾夹眩光单", "RECV"),
    ("v29_18", "margin_tab", "paid_total", 48.0,
     ["LAMINATE MARGIN TAB V29", "p1 paid 23.00", "p2 paid 25.00", "p3 open 8.00", "TOTAL PAID TARGET 48.00"],
     "边距标签页", "RECV"),
]
'''

HELD_SPECS = '''SPECS = [
    ("v29h_01", "chalk_recv", "paid_total", 55.5,
     ["CHALK DUST RECV V29H", "a paid 27.00", "b paid 28.50", "c open 9.00", "TOTAL PAID TARGET 55.50"],
     "粉笔灰收款单H", "RECV"),
    ("v29h_02", "fan_wh", "qty_sum", 44.0,
     ["WH STAPLE FAN V29H", "SKU1 qty 21 ok", "SKU2 qty 10 hold", "SKU3 qty 23 ok", "qty_sum TARGET 44"],
     "扇钉仓单H", "RECV"),
    ("v29h_03", "carbon_refund", "refund_done", 31.75,
     ["CARBON COPY REFUND V29H", "itemR1 15.00 done", "itemR2 16.75 done", "itemR3 6.00 open", "refund_done TARGET 31.75"],
     "复写退款单H", "DONE"),
    ("v29h_04", "toner_tax", "tax_base_paid", 97.0,
     ["TAX TONER STREAK V29H", "T1 54.00 paid", "T2 22.00 open", "T3 43.00 paid", "tax_base_paid TARGET 97.00"],
     "碳粉税基单H", "RECV"),
    ("v29h_05", "lamp_pay", "payroll_active", 1890.0,
     ["PAYROLL LAMP HOTSPOT V29H", "A 970 active", "B 190 leave", "C 920 active", "payroll_active TARGET 1890"],
     "台灯眩光工资单H", "OK"),
    ("v29h_06", "foil_ship", "ship_ok_qty", 36.0,
     ["SHIP FOIL GLARE V29H", "P1 18 ok", "P2 9 hold", "P3 18 ok", "ship_ok_qty TARGET 36"],
     "箔光运单H", "SHIP"),
    ("v29h_07", "wax_sla", "open_pri_sum", 39.0,
     ["SLA WAX SEAL BAIT V29H", "S1 pri 16 open", "S2 pri 18 closed", "S3 pri 23 open", "open_pri_sum TARGET 39"],
     "蜡封印SLAH", "OPEN"),
    ("v29h_08", "magnet_exp", "paid_total", 74.25,
     ["EXPENSE MAGNET CLIP V29H", "E1 36.00 paid", "E2 14.00 void", "E3 38.25 paid", "paid_total TARGET 74.25"],
     "磁夹报销H", "RECV"),
    ("v29h_09", "accordion_po", "paid_total", 58.0,
     ["PO-ACCORDION FOLD V29H", "itemA paid 28.00", "itemB paid 30.00", "itemC open 10.00", "TOTAL PAID TARGET 58.00"],
     "手风琴采购H", "RECV"),
    ("v29h_10", "perforate_order", "paid_total", 49.5,
     ["ORDER PERFORATE EDGE V29H", "A paid 24.00", "B paid 25.50", "C open 8.00", "TOTAL PAID TARGET 49.50"],
     "撕孔订单H", "RECV"),
    ("v29h_11", "xfold_dup", "paid_total", 63.0,
     ["INVOICE #V29H-XFOLD", "lineA paid 21.00", "lineB paid 21.00", "lineC paid 21.00", "TOTAL PAID TARGET 63.00"],
     "交叉折页联单H", "RECV"),
    ("v29h_12", "ghost_zero", "paid_total", 0.0,
     ["OPEN ONLY V29H", "X 33.00 open", "Y 36.00 open", "paid_total TARGET 0.00"],
     "复写鬼影未付H", "HOLD"),
    ("v29h_13", "highlighter_ledger", "paid_total", 37.5,
     ["LEDGER HIGHLIGHTER V29H", "rA paid 18.00", "rB paid 19.50", "rC open 6.00", "TOTAL PAID TARGET 37.50"],
     "荧光笔台账H", "RECV"),
    ("v29h_14", "postit_ui", "paid_total", 42.75,
     ["UI POSTIT EDGE V29H", "alpha paid 20.00", "beta paid 22.75", "gamma open 7.00", "TOTAL PAID TARGET 42.75"],
     "便利贴界面H", "RECV"),
    ("v29h_15", "thermal_stack", "paid_total", 68.0,
     ["THERMAL FADE STACK V29H", "x paid 33.00 usd", "y paid 35.00 usd", "z open 11.00 usd", "TOTAL PAID TARGET 68.00"],
     "热敏褪色叠页H", "RECV"),
    ("v29h_16", "bluepen_fax", "paid_total", 35.25,
     ["CN-EN BLUEPEN FAX V29H", "tea paid 17.00", "rice paid 18.25", "soup open 6.00", "TOTAL PAID TARGET 35.25"],
     "蓝笔传真混排H", "RECV"),
    ("v29h_17", "binder_glare", "paid_total", 51.0,
     ["BINDER CLIP GLARE V29H", "w1 paid 25.00", "w2 paid 26.00", "w3 open 9.00", "TOTAL PAID TARGET 51.00"],
     "长尾夹眩光单H", "RECV"),
    ("v29h_18", "margin_tab", "paid_total", 29.5,
     ["LAMINATE MARGIN TAB V29H", "p1 paid 14.00", "p2 paid 15.50", "p3 open 5.00", "TOTAL PAID TARGET 29.50"],
     "边距标签页H", "RECV"),
]
'''


def replace_specs(text: str, new_specs: str) -> str:
    return re.sub(r"SPECS = \[.*?\]\n", new_specs + "\n", text, count=1, flags=re.S)


def xform_train(text: str) -> str:
    reps = [
        ("C272", "C278"), ("C273", "C279"), ("C274", "C280"),
        ("v28", "v29"), ("V28", "V29"), ("V28H", "V29H"), ("v28h", "v29h"),
        ("vision_images_v28", "vision_images_v29"),
        ("vision_v28_c272", "vision_v29_c278"),
        ("VL_GATE_V28_PROTOCOL", "VL_GATE_V29_PROTOCOL"),
        ("vl_gate_v28_claim", "vl_gate_v29_claim"),
        ("vision_gate_v28_claim", "vision_gate_v29_claim"),
        ("r50plus_v28_", "r50plus_v29_"),
        ("SCAN DESK V28", "SCAN DESK V29"),
        ("V28 C272", "V29 C278"),
        ("V28 keeps floor", "V29 keeps floor"),
        ("Vision V28", "Vision V29"),
        ("vision_v28", "vision_v29"),
    ]
    for a, b in reps:
        text = text.replace(a, b)
    text = replace_specs(text, TRAIN_SPECS)
    # docstring fix
    text = text.replace("harder than V25", "harder than V28")
    text = text.replace("NEW themes vs V25", "NEW themes vs V28")
    text = text.replace("No claim until C279 VL", "No claim until C279 VL")
    return text


def xform_smoke(text: str) -> str:
    reps = [
        ("C273", "C279"), ("C272", "C278"),
        ("v28", "v29"), ("V28", "V29"),
        ("vision_images_v28", "vision_images_v29"),
        ("vision_v28_c273", "vision_v29_c279"),
        ("vl_gate_v28_claim", "vl_gate_v29_claim"),
        ("vision_gate_v28_claim", "vision_gate_v29_claim"),
        ("r50plus_v28_", "r50plus_v29_"),
        ("vision_v28_smoke", "vision_v29_smoke"),
        ("C273_VISION_V28", "C279_VISION_V29"),
        ("C273b_VISION_GATE_V28", "C279b_VISION_GATE_V29"),
    ]
    for a, b in reps:
        text = text.replace(a, b)
    return text


def xform_heldout(text: str) -> str:
    reps = [
        ("C274", "C280"), ("C272", "C278"), ("C273", "C279"),
        ("v28h", "v29h"), ("V28H", "V29H"), ("v28", "v29"), ("V28", "V29"),
        ("vision_images_v28h", "vision_images_v29h"),
        ("vision_images_v28", "vision_images_v29"),
        ("vision_v28h_c274", "vision_v29h_c280"),
        ("VL_GATE_V28_HELDOUT_PROTOCOL", "VL_GATE_V29_HELDOUT_PROTOCOL"),
        ("vl_gate_v28_heldout_claim", "vl_gate_v29_heldout_claim"),
        ("vision_gate_v28_heldout_claim", "vision_gate_v29_heldout_claim"),
        ("r50plus_v28_heldout", "r50plus_v29_heldout"),
        ("vision_v28_heldout", "vision_v29_heldout"),
        ("C274_VISION_V28", "C280_VISION_V29"),
        ("C274b_VISION_GATE_V28", "C280b_VISION_GATE_V29"),
        ("SCAN DESK V28H", "SCAN DESK V29H"),
        ("V28H C274", "V29H C280"),
        ("heldout", "heldout"),  # noop keep
    ]
    for a, b in reps:
        text = text.replace(a, b)
    text = replace_specs(text, HELD_SPECS)
    return text


def xform_nv(text: str) -> str:
    reps = [
        ("C275", "C281"),
        ("u2c_replace_c275", "u2c_replace_c281"),
        ("vision_images_v27", "vision_images_v28"),  # stretch on prior train
        ("C275_U2C_REPLACE_STRETCH", "C281_PRODUCT_U2C_COST"),
        ("u2c_replace_stretch", "product_u2c_cost"),
        ("U2C crystal, capture multi-metric, replace ledger unit",
         "product polish + U2C crystal + replace/cost ledger"),
    ]
    for a, b in reps:
        text = text.replace(a, b)
    # also rename output json basename inside script if hardcoded
    text = text.replace("C275_U2C", "C281_PRODUCT_U2C_COST".replace("_PRODUCT_U2C_COST", "") )  # careful
    return text


def fix_nv(text: str) -> str:
    # rewrite carefully for C281
    text = text.replace("C275", "C281")
    text = text.replace("u2c_replace_c275", "product_u2c_c281")
    text = text.replace("vision_images_v27", "vision_images_v28")
    text = text.replace(
        'DOC / "C275_U2C_REPLACE_STRETCH.json"',
        'DOC / "C281_PRODUCT_U2C_COST.json"',
    )
    text = text.replace(
        "U2C crystal, capture multi-metric, replace ledger unit",
        "product polish + U2C on V28 + replace/cost ledger",
    )
    text = text.replace("u2c_replace_stretch", "product_u2c_cost")
    text = text.replace('theme": "u2c_replace_stretch"', 'theme": "product_u2c_cost"')
    return text


def xform_reg(text: str) -> str:
    text = text.replace("C276", "C282")
    text = text.replace("C272-C275", "C278-C281")
    text = text.replace("c260_c263", "c278_c281")
    text = text.replace("capture_regression_c276", "capture_regression_c282")
    # insert V29 pointers after V28_heldout if present
    needle = '("V28_heldout", DOC / "C274_VISION_V28_HELDOUT_SMOKE.json"),'
    insert = needle + '\n    ("V29", DOC / "C279_VISION_V29_SMOKE.json"),\n    ("V29_heldout", DOC / "C280_VISION_V29_HELDOUT_SMOKE.json"),'
    if needle in text and '("V29"' not in text:
        text = text.replace(needle, insert)
    # non-vision pointer
    text = text.replace(
        '("C275_u2c_replace_stretch", DOC / "C275_U2C_REPLACE_STRETCH.json"),',
        '("C275_u2c_replace_stretch", DOC / "C275_U2C_REPLACE_STRETCH.json"),\n'
        '    ("C281_product_u2c_cost", DOC / "C281_PRODUCT_U2C_COST.json"),',
    )
    # required list
    text = text.replace(
        'required = ["V25", "V25_heldout", "V26", "V26_heldout", "V27", "V27_heldout", "V28", "V28_heldout", "C233_clarity_floor", "C275_u2c_replace_stretch"]',
        'required = ["V25", "V25_heldout", "V26", "V26_heldout", "V27", "V27_heldout", "V28", "V28_heldout", "V29", "V29_heldout", "C233_clarity_floor", "C281_product_u2c_cost"]',
    )
    text = text.replace('DOC / "C276_CAPTURE_OFFICE_REGRESSION.json"', 'DOC / "C282_CAPTURE_OFFICE_REGRESSION.json"')
    return text


def xform_score(text: str) -> str:
    text = text.replace("C277", "C283")
    text = text.replace("c272_c276", "c278_c282")
    text = text.replace("STAGE_ANT_C277.md", "STAGE_ANT_C283.md")
    text = text.replace("C275_U2C_REPLACE_STRETCH.json", "C281_PRODUCT_U2C_COST.json")
    text = text.replace("C272_VISION_V28_DESIGN.json", "C278_VISION_V29_DESIGN.json")
    text = text.replace("C273_VISION_V28_SMOKE.json", "C279_VISION_V29_SMOKE.json")
    text = text.replace("C273b_VISION_GATE_V28_CLAIM.json", "C279b_VISION_GATE_V29_CLAIM.json")
    text = text.replace("C274_VISION_V28_HELDOUT_SMOKE.json", "C280_VISION_V29_HELDOUT_SMOKE.json")
    text = text.replace("C274b_VISION_GATE_V28_HELDOUT_CLAIM.json", "C280b_VISION_GATE_V29_HELDOUT_CLAIM.json")
    text = text.replace("C276_CAPTURE_OFFICE_REGRESSION.json", "C282_CAPTURE_OFFICE_REGRESSION.json")
    text = text.replace("vl_gate_v28_claim", "vl_gate_v29_claim")
    text = text.replace("vl_gate_v28_heldout_claim", "vl_gate_v29_heldout_claim")
    # keep v28 vars but add v29 — simpler: rename v28 block to v29 and also keep prior via v27 names already there
    # The scorecard uses c266/c267 as V28 — after replace they load V29 files into same var names.
    # Also update composite parts labels and stage_ready to use v29 claims.
    text = text.replace("v28_design", "v29_design")
    text = text.replace("v28_smoke", "v29_smoke")
    text = text.replace("v28_heldout", "v29_heldout")
    text = text.replace("v28_claim", "v29_claim")
    text = text.replace("v28h_claim", "v29h_claim")
    text = text.replace('"source": "C275"', '"source": "C281"')
    text = text.replace("u2c_replace_stretch", "product_u2c_cost")
    text = text.replace("u2c-replace stretch (C275)", "product-u2c-cost (C281)")
    text = text.replace("| C272 |", "| C278 |")
    text = text.replace("| C273 |", "| C279 |")
    text = text.replace("| C274 |", "| C280 |")
    text = text.replace("| C275 |", "| C281 |")
    text = text.replace("| C276 |", "| C282 |")
    text = text.replace("| C277 |", "| C283 |")
    text = text.replace("V28 design", "V29 design")
    text = text.replace("V28 smoke", "V29 smoke")
    text = text.replace("V28 heldout", "V29 heldout")
    text = text.replace("V28 smoke / heldout", "V29 smoke / heldout")
    text = text.replace("- V28:", "- V29:")
    text = text.replace("- V28 heldout:", "- V29 heldout:")
    # variable names v28 / v28h
    text = text.replace("v28 = float", "v29 = float")
    text = text.replace("v28h = float", "v29h = float")
    text = text.replace("max(v28, v28h", "max(v29, v29h")
    text = text.replace("1.0 if v29_claim", "1.0 if v29_claim")  # already
    text = text.replace("v29_claim and v29h_claim", "v29_claim and v29h_claim")
    # board table still may say V28 from partial — fix remaining
    text = text.replace("**{v28} / {v28h}**", "**{v29} / {v29h}**")
    text = text.replace("rate={v28}", "rate={v29}")
    text = text.replace("rate={v28h}", "rate={v29h}")
    text = text.replace("claim={v28_claim}", "claim={v29_claim}")
    text = text.replace("claim={v28h_claim}", "claim={v29h_claim}")
    text = text.replace("C272-C277", "C278-C283")
    text = text.replace("C272-C276", "C278-C282")
    return text


def main():
    mapping = [
        ("c272_vision_v28_design_and_batch.py", "c278_vision_v29_design_and_batch.py", xform_train),
        ("c273_vision_v28_smoke.py", "c279_vision_v29_smoke.py", xform_smoke),
        ("c274_vision_v28_heldout.py", "c280_vision_v29_heldout.py", xform_heldout),
        ("c275_u2c_replace_stretch.py", "c281_product_u2c_cost.py", fix_nv),
        ("c276_capture_office_regression.py", "c282_capture_office_regression.py", xform_reg),
        ("c277_scorecard_and_stage.py", "c283_scorecard_and_stage.py", xform_score),
    ]
    for src, dst, fn in mapping:
        t = (SCR / src).read_text(encoding="utf-8")
        out = fn(t)
        (SCR / dst).write_text(out, encoding="utf-8")
        print("wrote", dst, "bytes", len(out.encode("utf-8")))
    # sanity: no leftover v28 paths in design
    d = (SCR / "c278_vision_v29_design_and_batch.py").read_text(encoding="utf-8")
    assert "vision_images_v29" in d and "v29_01" in d
    assert "VISION_V28" not in d
    s = (SCR / "c283_scorecard_and_stage.py").read_text(encoding="utf-8")
    assert "STAGE_ANT_C283.md" in s
    assert "C279_VISION_V29_SMOKE" in s
    print("ok")


if __name__ == "__main__":
    main()
