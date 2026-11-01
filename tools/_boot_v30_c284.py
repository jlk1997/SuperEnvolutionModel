# -*- coding: utf-8 -*-
"""Bootstrap C284-C289 Vision V30 suite from V29 scripts."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCR = ROOT / "scripts"

TRAIN_SPECS = '''SPECS = [
    ("v30_01", "velvet_recv", "paid_total", 103.5,
     ["VELVET DUST RECV V30", "a paid 51.00", "b paid 52.50", "c open 14.00", "TOTAL PAID TARGET 103.50"],
     "丝绒灰收款单", "RECV"),
    ("v30_02", "spiral_wh", "qty_sum", 91.0,
     ["WH SPIRAL BIND V30", "SKU1 qty 43 ok", "SKU2 qty 20 hold", "SKU3 qty 48 ok", "qty_sum TARGET 91"],
     "螺旋装订仓单", "RECV"),
    ("v30_03", "mimeo_refund", "refund_done", 57.25,
     ["MIMEO COPY REFUND V30", "itemR1 27.00 done", "itemR2 30.25 done", "itemR3 12.00 open", "refund_done TARGET 57.25"],
     "油印退款单", "DONE"),
    ("v30_04", "ribbon_tax", "tax_base_paid", 163.0,
     ["TAX RIBBON STREAK V30", "T1 92.00 paid", "T2 37.00 open", "T3 71.00 paid", "tax_base_paid TARGET 163.00"],
     "色带税基单", "RECV"),
    ("v30_05", "neon_pay", "payroll_active", 2920.0,
     ["PAYROLL NEON HOTSPOT V30", "A 1490 active", "B 290 leave", "C 1430 active", "payroll_active TARGET 2920"],
     "霓虹热点工资单", "OK"),
    ("v30_06", "hologram_ship", "ship_ok_qty", 76.0,
     ["SHIP HOLOGRAM GLARE V30", "P1 38 ok", "P2 19 hold", "P3 38 ok", "ship_ok_qty TARGET 76"],
     "全息发货单", "SHIP"),
    ("v30_07", "lacquer_sla", "open_pri_sum", 72.0,
     ["SLA LACQUER SEAL BAIT V30", "S1 pri 30 open", "S2 pri 32 closed", "S3 pri 42 open", "open_pri_sum TARGET 72"],
     "漆印SLA", "OPEN"),
    ("v30_08", "rivet_exp", "paid_total", 137.25,
     ["EXPENSE RIVET CLIP V30", "E1 66.00 paid", "E2 25.00 void", "E3 71.25 paid", "paid_total TARGET 137.25"],
     "铆钉报销单", "RECV"),
    ("v30_09", "concertina_po", "paid_total", 105.5,
     ["PO-CONCERTINA FOLD V30", "itemA paid 51.00", "itemB paid 54.50", "itemC open 17.00", "TOTAL PAID TARGET 105.50"],
     "手风琴折采购单", "RECV"),
    ("v30_10", "serrate_order", "paid_total", 87.0,
     ["ORDER SERRATE EDGE V30", "A paid 42.00", "B paid 45.00", "C open 13.00", "TOTAL PAID TARGET 87.00"],
     "锯齿边订单", "RECV"),
    ("v30_11", "triptych_dup", "paid_total", 124.5,
     ["INVOICE #V30-TRIPTYCH", "lineA paid 41.50", "lineB paid 41.50", "lineC paid 41.50", "TOTAL PAID TARGET 124.50"],
     "三联页重复发票", "RECV"),
    ("v30_12", "void_zero", "paid_total", 0.0,
     ["OPEN ONLY V30", "X 64.00 open", "Y 67.00 open", "paid_total TARGET 0.00"],
     "油印阴影未付", "HOLD"),
    ("v30_13", "marker_ledger", "paid_total", 69.5,
     ["LEDGER MARKER STREAK V30", "rA paid 33.00", "rB paid 36.50", "rC open 11.00", "TOTAL PAID TARGET 69.50"],
     "马克笔台账", "RECV"),
    ("v30_14", "washi_ui", "paid_total", 81.25,
     ["UI WASHI EDGE V30", "alpha paid 39.00", "beta paid 42.25", "gamma open 14.00", "TOTAL PAID TARGET 81.25"],
     "和纸边界面单", "RECV"),
    ("v30_15", "inkjet_stack", "paid_total", 119.0,
     ["INKJET FADE STACK V30", "x paid 58.00 usd", "y paid 61.00 usd", "z open 20.00 usd", "TOTAL PAID TARGET 119.00"],
     "喷墨褪色叠页", "RECV"),
    ("v30_16", "redink_fax", "paid_total", 67.5,
     ["CN-EN REDINK FAX V30", "tea paid 32.00", "rice paid 35.50", "soup open 12.00", "TOTAL PAID TARGET 67.50"],
     "红墨传真双语", "RECV"),
    ("v30_17", "bulldog_glare", "paid_total", 93.75,
     ["BULLDOG CLIP GLARE V30", "w1 paid 45.00", "w2 paid 48.75", "w3 open 16.00", "TOTAL PAID TARGET 93.75"],
     "长尾夹眩光单", "RECV"),
    ("v30_18", "corner_tab", "paid_total", 51.0,
     ["LAMINATE CORNER TAB V30", "p1 paid 24.00", "p2 paid 27.00", "p3 open 9.00", "TOTAL PAID TARGET 51.00"],
     "角签覆膜页", "RECV"),
]
'''

HELD_SPECS = '''SPECS = [
    ("v30h_01", "velvet_recv", "paid_total", 58.5,
     ["VELVET DUST RECV V30H", "a paid 28.00", "b paid 30.50", "c open 10.00", "TOTAL PAID TARGET 58.50"],
     "丝绒灰收款单H", "RECV"),
    ("v30h_02", "spiral_wh", "qty_sum", 47.0,
     ["WH SPIRAL BIND V30H", "SKU1 qty 22 ok", "SKU2 qty 11 hold", "SKU3 qty 25 ok", "qty_sum TARGET 47"],
     "螺旋装订仓单H", "RECV"),
    ("v30h_03", "mimeo_refund", "refund_done", 33.75,
     ["MIMEO COPY REFUND V30H", "itemR1 16.00 done", "itemR2 17.75 done", "itemR3 7.00 open", "refund_done TARGET 33.75"],
     "油印退款单H", "DONE"),
    ("v30h_04", "ribbon_tax", "tax_base_paid", 101.0,
     ["TAX RIBBON STREAK V30H", "T1 56.00 paid", "T2 23.00 open", "T3 45.00 paid", "tax_base_paid TARGET 101.00"],
     "色带税基单H", "RECV"),
    ("v30h_05", "neon_pay", "payroll_active", 1980.0,
     ["PAYROLL NEON HOTSPOT V30H", "A 1010 active", "B 200 leave", "C 970 active", "payroll_active TARGET 1980"],
     "霓虹热点工资单H", "OK"),
    ("v30h_06", "hologram_ship", "ship_ok_qty", 39.0,
     ["SHIP HOLOGRAM GLARE V30H", "P1 19 ok", "P2 10 hold", "P3 20 ok", "ship_ok_qty TARGET 39"],
     "全息发货单H", "SHIP"),
    ("v30h_07", "lacquer_sla", "open_pri_sum", 41.0,
     ["SLA LACQUER SEAL BAIT V30H", "S1 pri 17 open", "S2 pri 19 closed", "S3 pri 24 open", "open_pri_sum TARGET 41"],
     "漆印SLAH", "OPEN"),
    ("v30h_08", "rivet_exp", "paid_total", 77.25,
     ["EXPENSE RIVET CLIP V30H", "E1 37.00 paid", "E2 15.00 void", "E3 40.25 paid", "paid_total TARGET 77.25"],
     "铆钉报销H", "RECV"),
    ("v30h_09", "concertina_po", "paid_total", 61.0,
     ["PO-CONCERTINA FOLD V30H", "itemA paid 29.00", "itemB paid 32.00", "itemC open 11.00", "TOTAL PAID TARGET 61.00"],
     "手风琴折采购H", "RECV"),
    ("v30h_10", "serrate_order", "paid_total", 52.5,
     ["ORDER SERRATE EDGE V30H", "A paid 25.00", "B paid 27.50", "C open 9.00", "TOTAL PAID TARGET 52.50"],
     "锯齿边订单H", "RECV"),
    ("v30h_11", "triptych_dup", "paid_total", 66.0,
     ["INVOICE #V30H-TRIPTYCH", "lineA paid 22.00", "lineB paid 22.00", "lineC paid 22.00", "TOTAL PAID TARGET 66.00"],
     "三联页重复发票H", "RECV"),
    ("v30h_12", "void_zero", "paid_total", 0.0,
     ["OPEN ONLY V30H", "X 35.00 open", "Y 38.00 open", "paid_total TARGET 0.00"],
     "油印阴影未付H", "HOLD"),
    ("v30h_13", "marker_ledger", "paid_total", 40.5,
     ["LEDGER MARKER STREAK V30H", "rA paid 19.00", "rB paid 21.50", "rC open 7.00", "TOTAL PAID TARGET 40.50"],
     "马克笔台账H", "RECV"),
    ("v30h_14", "washi_ui", "paid_total", 45.75,
     ["UI WASHI EDGE V30H", "alpha paid 22.00", "beta paid 23.75", "gamma open 8.00", "TOTAL PAID TARGET 45.75"],
     "和纸边界面单H", "RECV"),
    ("v30h_15", "inkjet_stack", "paid_total", 71.0,
     ["INKJET FADE STACK V30H", "x paid 34.00 usd", "y paid 37.00 usd", "z open 12.00 usd", "TOTAL PAID TARGET 71.00"],
     "喷墨褪色叠页H", "RECV"),
    ("v30h_16", "redink_fax", "paid_total", 38.25,
     ["CN-EN REDINK FAX V30H", "tea paid 18.00", "rice paid 20.25", "soup open 7.00", "TOTAL PAID TARGET 38.25"],
     "红墨传真双语H", "RECV"),
    ("v30h_17", "bulldog_glare", "paid_total", 54.0,
     ["BULLDOG CLIP GLARE V30H", "w1 paid 26.00", "w2 paid 28.00", "w3 open 10.00", "TOTAL PAID TARGET 54.00"],
     "长尾夹眩光单H", "RECV"),
    ("v30h_18", "corner_tab", "paid_total", 31.5,
     ["LAMINATE CORNER TAB V30H", "p1 paid 15.00", "p2 paid 16.50", "p3 open 6.00", "TOTAL PAID TARGET 31.50"],
     "角签覆膜页H", "RECV"),
]
'''

V30_OVERLAY = r'''
    # --- V30 overlays (new vs V29) ---
    # velvet dust speckles (below text band)
    for _ in range(90):
        vx = rng.randint(60, 520)
        vy = rng.randint(300, 560)
        if in_text_band(vy):
            continue
        d.ellipse([vx, vy, vx + 3, vy + 2], fill=(190, 180, 170))
    # spiral bind holes right of card
    for hy in range(80, 560, 28):
        d.ellipse([548, hy, 562, hy + 12], fill=(210, 206, 196), outline=(50, 50, 50), width=1)
    # mimeo purple ghost text
    d.text((80, 360), "MIMEO GHOST bait 88.88", fill=(180, 140, 200), font=f_pen)
    # ribbon ink streak
    d.line([(55, 310), (540, 330)], fill=(40, 20, 80), width=4)
    d.line([(55, 314), (540, 334)], fill=(90, 60, 140), width=2)
    # neon hotspot wash (upper-right outside text)
    d.rectangle([420, 30, 555, 95], fill=(180, 255, 220))
    d.text((430, 50), "NEON wash", fill=(20, 80, 60), font=f_tiny)
    # hologram foil stripe
    for hx in range(70, 500, 12):
        col = (200, 220, 255) if (hx // 12) % 2 == 0 else (255, 220, 200)
        d.rectangle([hx, 275, hx + 8, 295], fill=col)
    # lacquer seal blob
    d.ellipse([470, 480, 540, 540], fill=(160, 30, 40))
    d.text((480, 500), "LACQ", fill=(255, 220, 220), font=f_stamp)
    # rivet dots top bar
    for rx in range(80, 480, 40):
        d.ellipse([rx, 22, rx + 10, 32], fill=(70, 70, 80), outline=(20, 20, 20), width=1)
    # concertina fold zig below text
    for t in range(0, 10):
        x0 = 80 + t * 44
        d.line([(x0, 340), (x0 + 22, 360), (x0 + 44, 340)], fill=(90, 90, 100), width=2)
    # serrated bottom edge marks
    for sx in range(50, 540, 16):
        d.polygon([(sx, 595), (sx + 8, 610), (sx + 16, 595)], fill=bg)
    # washi tape strip
    d.rectangle([100, 18, 320, 40], fill=(255, 220, 200), outline=(200, 150, 120), width=1)
    d.text((110, 22), "WASHI bait 55.55", fill=(120, 60, 40), font=f_tiny)
    # red ink fax header
    d.text((760, 20), "REDINK FAX bait 99.99 FROM:V30", fill=(160, 20, 20), font=f_fax)
    # bulldog clip silhouette
    d.polygon([(250, 6), (300, 6), (310, 40), (240, 40)], fill=(50, 60, 70))
    d.rectangle([255, 40, 295, 55], fill=(70, 80, 90))
    # corner tab laminate
    d.polygon([(520, 70), (560, 70), (560, 120), (530, 110)], fill=(255, 200, 80), outline=(160, 100, 20), width=1)
    d.text((525, 85), "CORNER", fill=(80, 40, 0), font=f_tiny)
'''


def replace_specs(text: str, new_specs: str) -> str:
    return re.sub(r"SPECS = \[.*?\]\n", new_specs + "\n", text, count=1, flags=re.S)


def xform_train(text: str) -> str:
    reps = [
        ("C278", "C284"), ("C279", "C285"), ("C280", "C286"),
        ("v29", "v30"), ("V29", "V30"), ("V29H", "V30H"), ("v29h", "v30h"),
        ("vision_images_v29", "vision_images_v30"),
        ("vision_v29_c278", "vision_v30_c284"),
        ("VL_GATE_V29_PROTOCOL", "VL_GATE_V30_PROTOCOL"),
        ("vl_gate_v29_claim", "vl_gate_v30_claim"),
        ("vision_gate_v29_claim", "vision_gate_v30_claim"),
        ("r50plus_v29_", "r50plus_v30_"),
        ("SCAN DESK V29", "SCAN DESK V30"),
        ("V29 C278", "V30 C284"),
        ("V29 keeps floor", "V30 keeps floor"),
        ("Vision V29", "Vision V30"),
        ("vision_v29", "vision_v30"),
        ("_v29c272", "_v30c284"),
        ("harder than V28", "harder than V29"),
        ("NEW themes vs V28", "NEW themes vs V29"),
        ("No claim until C279 VL", "No claim until C285 VL"),
        ("Rust|Wet|Hole|Band|Glare|Label|Blot|Clip|Fax|Tab|Crease|Overink|Tape|Shade|Ring",
         "Velvet|Spiral|Mimeo|Ribbon|Neon|Holo|Lacquer|Rivet|Concertina|Serrate|Triptych|Washi|Inkjet|Redink|Bulldog|Corner"),
        ("rust_wet_hole_band_glare_label_blot_clip_fax_tab_crease_overink_tape_shade_ring",
         "velvet_spiral_mimeo_ribbon_neon_holo_lacquer_rivet_concertina_serrate_triptych_washi_inkjet_redink_bulldog_corner"),
    ]
    for a, b in reps:
        text = text.replace(a, b)
    text = replace_specs(text, TRAIN_SPECS)
    # inject V30 overlays before fingerprint block if present
    needle = "    # fingerprint ovals (outside text band preferred)"
    if needle in text and "V30 overlays" not in text:
        text = text.replace(needle, V30_OVERLAY + "\n" + needle)
    return text


def xform_smoke(text: str) -> str:
    reps = [
        ("C279", "C285"), ("C278", "C284"),
        ("v29", "v30"), ("V29", "V30"),
        ("vision_images_v29", "vision_images_v30"),
        ("vision_v29_c279", "vision_v30_c285"),
        ("vl_gate_v29_claim", "vl_gate_v30_claim"),
        ("vision_gate_v29_claim", "vision_gate_v30_claim"),
        ("r50plus_v29_", "r50plus_v30_"),
        ("vision_v29_smoke", "vision_v30_smoke"),
        ("C279_VISION_V29", "C285_VISION_V30"),
        ("C279b_VISION_GATE_V29", "C285b_VISION_GATE_V30"),
    ]
    for a, b in reps:
        text = text.replace(a, b)
    return text


def xform_heldout(text: str) -> str:
    reps = [
        ("C280", "C286"), ("C278", "C284"), ("C279", "C285"),
        ("v29h", "v30h"), ("V29H", "V30H"), ("v29", "v30"), ("V29", "V30"),
        ("vision_images_v29h", "vision_images_v30h"),
        ("vision_images_v29", "vision_images_v30"),
        ("vision_v29h_c280", "vision_v30h_c286"),
        ("VL_GATE_V29_HELDOUT_PROTOCOL", "VL_GATE_V30_HELDOUT_PROTOCOL"),
        ("vl_gate_v29_heldout_claim", "vl_gate_v30_heldout_claim"),
        ("vision_gate_v29_heldout_claim", "vision_gate_v30_heldout_claim"),
        ("r50plus_v29_heldout", "r50plus_v30_heldout"),
        ("vision_v29_heldout", "vision_v30_heldout"),
        ("C280_VISION_V29", "C286_VISION_V30"),
        ("C280b_VISION_GATE_V29", "C286b_VISION_GATE_V30"),
        ("SCAN DESK V29H", "SCAN DESK V30H"),
        ("V29H C280", "V30H C286"),
    ]
    for a, b in reps:
        text = text.replace(a, b)
    text = replace_specs(text, HELD_SPECS)
    return text


def xform_nv(text: str) -> str:
    # from c269 confidence gate stretch -> c287
    text = text.replace("C269", "C287")
    text = text.replace("conf_gate_stretch_c269", "conf_gate_stretch_c287")
    text = text.replace("confidence_gate_stretch_v27", "confidence_gate_stretch_v30")
    text = text.replace("cg27_", "cg30_")
    # fresh amounts distinct from C269
    swaps = [
        ("49.00", "52.00"), ("53.25", "56.25"), ("14.00", "15.00"), ("102.25", "108.25"),
        ("45", "47"), ("21", "22"), ("49", "51"), ("94", "98"), ("115.0", "120.0"),
        ("29.00", "31.00"), ("32.50", "34.50"), ("12.00", "13.00"), ("61.50", "65.50"), ("73.5", "78.5"),
        ("96.00", "99.00"), ("38.00", "40.00"), ("77.00", "80.00"), ("173.00", "179.00"), ("211.0", "219.0"),
        ("1490", "1520"), ("280", "295"), ("1420", "1450"), ("2910", "2970"), ("3190.0", "3260.0"),
        ("42", "44"), ("22", "23"), ("41", "43"), ("83", "87"), ("105.0", "110.0"),
        ("31", "33"), ("34", "36"), ("43", "45"), ("74", "78"), ("108.0", "114.0"),
        ("71.00", "75.00"), ("74.00", "78.00"), ("145.0", "153.0"),
        ("38.00", "40.00"), ("41.00", "43.00"), ("13.00", "14.00"), ("79.00", "83.00"),
        ("22", "24"), ("11", "12"), ("25", "26"), ("47", "50"),
        ("16.00", "17.00"), ("18.50", "19.50"), ("6.00", "7.00"), ("34.50", "36.50"),
        ("34.00", "36.00"), ("36.25", "38.25"), ("11.00", "12.00"), ("70.25", "74.25"), ("81.25", "86.25"),
    ]
    # careful: do limited unique replacements on CASES only — rewrite CASES block entirely
    return text


CONF_CASES = '''CASES = [
    {"id": "cg30_paid_force", "metric": "paid_total",
     "text": "a paid 52.00 b paid 56.25 c open 15.00 TOTAL PAID TARGET 108.25 bait 999.00",
     "model_guess": 999.0, "expected": 108.25, "want_decision": "force_tool"},
    {"id": "cg30_qty_force", "metric": "qty_sum",
     "text": "SKU1 qty 47 ok SKU2 qty 22 hold SKU3 qty 51 ok qty_sum TARGET 98",
     "model_guess": 120.0, "expected": 98.0, "want_decision": "force_tool"},
    {"id": "cg30_refund_force", "metric": "refund_done",
     "text": "itemR1 31.00 done itemR2 34.50 done itemR3 13.00 open refund_done TARGET 65.50",
     "model_guess": 78.5, "expected": 65.5, "want_decision": "force_tool"},
    {"id": "cg30_tax_force", "metric": "tax_base_paid",
     "text": "T1 99.00 paid T2 40.00 open T3 80.00 paid tax_base_paid TARGET 179.00",
     "model_guess": 219.0, "expected": 179.0, "want_decision": "force_tool"},
    {"id": "cg30_payroll_force", "metric": "payroll_active",
     "text": "A 1520 active B 295 leave C 1450 active payroll_active TARGET 2970",
     "model_guess": 3260.0, "expected": 2970.0, "want_decision": "force_tool"},
    {"id": "cg30_ship_force", "metric": "ship_ok_qty",
     "text": "P1 44 ok P2 23 hold P3 43 ok ship_ok_qty TARGET 87",
     "model_guess": 110.0, "expected": 87.0, "want_decision": "force_tool"},
    {"id": "cg30_sla_force", "metric": "open_pri_sum",
     "text": "S1 pri 33 open S2 pri 36 closed S3 pri 45 open open_pri_sum TARGET 78",
     "model_guess": 114.0, "expected": 78.0, "want_decision": "force_tool"},
    {"id": "cg30_zero_force", "metric": "paid_total",
     "text": "X 75.00 open Y 78.00 open paid_total TARGET 0.00 bait 153.00",
     "model_guess": 153.0, "expected": 0.0, "want_decision": "force_tool"},
    {"id": "cg30_paid_trust", "metric": "paid_total",
     "text": "alpha paid 40.00 beta paid 43.00 gamma open 14.00 TOTAL PAID TARGET 83.00",
     "model_guess": 83.0, "expected": 83.0, "want_decision": "trust_model"},
    {"id": "cg30_qty_trust", "metric": "qty_sum",
     "text": "SKU1 qty 24 ok SKU2 qty 12 hold SKU3 qty 26 ok qty_sum TARGET 50",
     "model_guess": 50.0, "expected": 50.0, "want_decision": "trust_model"},
    {"id": "cg30_refund_trust", "metric": "refund_done",
     "text": "itemR1 17.00 done itemR2 19.50 done itemR3 7.00 open refund_done TARGET 36.50",
     "model_guess": 36.5, "expected": 36.5, "want_decision": "trust_model"},
    {"id": "cg30_paid_path", "metric": "paid_total",
     "text": "tea paid 36.00 rice paid 38.25 soup open 12.00 TOTAL PAID TARGET 74.25",
     "model_guess": 86.25, "expected": 74.25, "want_decision": "force_tool", "also_parse_paid": True},
]
'''


def fix_nv(text: str) -> str:
    text = text.replace("C269", "C287")
    text = text.replace("conf_gate_stretch_c269", "conf_gate_stretch_c287")
    text = text.replace("confidence_gate_stretch_v27", "confidence_gate_stretch_v30")
    text = text.replace("C269_CONFIDENCE_GATE_STRETCH.json", "C287_CONFIDENCE_GATE_STRETCH.json")
    text = re.sub(r"CASES = \[.*?\]\n", CONF_CASES + "\n", text, count=1, flags=re.S)
    return text


def xform_reg(text: str) -> str:
    text = text.replace("C282", "C288")
    text = text.replace("C278-C281", "C284-C287")
    text = text.replace("c278_c281", "c284_c287")
    text = text.replace("capture_regression_c282", "capture_regression_c288")
    needle = '("V29_heldout", DOC / "C280_VISION_V29_HELDOUT_SMOKE.json"),'
    insert = (
        needle
        + '\n    ("V30", DOC / "C285_VISION_V30_SMOKE.json"),'
        + '\n    ("V30_heldout", DOC / "C286_VISION_V30_HELDOUT_SMOKE.json"),'
    )
    if needle in text and '("V30"' not in text:
        text = text.replace(needle, insert)
    text = text.replace(
        '("C281_product_u2c_cost", DOC / "C281_PRODUCT_U2C_COST.json"),',
        '("C281_product_u2c_cost", DOC / "C281_PRODUCT_U2C_COST.json"),\n'
        '    ("C287_confidence_gate_stretch", DOC / "C287_CONFIDENCE_GATE_STRETCH.json"),',
    )
    text = text.replace(
        'required = ["V25", "V25_heldout", "V26", "V26_heldout", "V27", "V27_heldout", "V28", "V28_heldout", "V29", "V29_heldout", "C233_clarity_floor", "C281_product_u2c_cost"]',
        'required = ["V25", "V25_heldout", "V26", "V26_heldout", "V27", "V27_heldout", "V28", "V28_heldout", "V29", "V29_heldout", "V30", "V30_heldout", "C233_clarity_floor", "C287_confidence_gate_stretch"]',
    )
    text = text.replace('DOC / "C282_CAPTURE_OFFICE_REGRESSION.json"', 'DOC / "C288_CAPTURE_OFFICE_REGRESSION.json"')
    return text


def xform_score(text: str) -> str:
    text = text.replace("C283", "C289")
    text = text.replace("c278_c282", "c284_c288")
    text = text.replace("STAGE_ANT_C283.md", "STAGE_ANT_C289.md")
    text = text.replace("C281_PRODUCT_U2C_COST.json", "C287_CONFIDENCE_GATE_STRETCH.json")
    text = text.replace("C278_VISION_V29_DESIGN.json", "C284_VISION_V30_DESIGN.json")
    text = text.replace("C279_VISION_V29_SMOKE.json", "C285_VISION_V30_SMOKE.json")
    text = text.replace("C279b_VISION_GATE_V29_CLAIM.json", "C285b_VISION_GATE_V30_CLAIM.json")
    text = text.replace("C280_VISION_V29_HELDOUT_SMOKE.json", "C286_VISION_V30_HELDOUT_SMOKE.json")
    text = text.replace("C280b_VISION_GATE_V29_HELDOUT_CLAIM.json", "C286b_VISION_GATE_V30_HELDOUT_CLAIM.json")
    text = text.replace("C282_CAPTURE_OFFICE_REGRESSION.json", "C288_CAPTURE_OFFICE_REGRESSION.json")
    text = text.replace("vl_gate_v29_claim", "vl_gate_v30_claim")
    text = text.replace("vl_gate_v29_heldout_claim", "vl_gate_v30_heldout_claim")
    text = text.replace("v29_design", "v30_design")
    text = text.replace("v29_smoke", "v30_smoke")
    text = text.replace("v29_heldout", "v30_heldout")
    # careful with claims - do after smoke renames
    text = text.replace("v29_claim", "v30_claim")
    text = text.replace("v29h_claim", "v30h_claim")
    text = text.replace('"source": "C281"', '"source": "C287"')
    text = text.replace("product_u2c_cost", "confidence_gate_stretch")
    text = text.replace("product-u2c-cost (C281)", "confidence-gate stretch (C287)")
    text = text.replace("| C278 |", "| C284 |")
    text = text.replace("| C279 |", "| C285 |")
    text = text.replace("| C280 |", "| C286 |")
    text = text.replace("| C281 |", "| C287 |")
    text = text.replace("| C282 |", "| C288 |")
    text = text.replace("| C283 |", "| C289 |")
    text = text.replace("V29 design", "V30 design")
    text = text.replace("V29 smoke", "V30 smoke")
    text = text.replace("V29 heldout", "V30 heldout")
    text = text.replace("V29 smoke / heldout", "V30 smoke / heldout")
    text = text.replace("- V29:", "- V30:")
    text = text.replace("- V29 heldout:", "- V30 heldout:")
    text = text.replace("v29 = float", "v30 = float")
    text = text.replace("v29h = float", "v30h = float")
    text = text.replace("max(v29, v29h", "max(v30, v30h")
    text = text.replace("**{v29} / {v29h}**", "**{v30} / {v30h}**")
    text = text.replace("rate={v29}", "rate={v30}")
    text = text.replace("rate={v29h}", "rate={v30h}")
    text = text.replace("claim={v29_claim}", "claim={v30_claim}")
    text = text.replace("claim={v29h_claim}", "claim={v30h_claim}")
    text = text.replace("C278-C283", "C284-C289")
    text = text.replace("C278-C282", "C284-C288")
    text = text.replace("C272-C283", "C284-C289")
    # keep prior V29 rates in scorecard — inject loads
    return text


def main():
    mapping = [
        ("c278_vision_v29_design_and_batch.py", "c284_vision_v30_design_and_batch.py", xform_train),
        ("c279_vision_v29_smoke.py", "c285_vision_v30_smoke.py", xform_smoke),
        ("c280_vision_v29_heldout.py", "c286_vision_v30_heldout.py", xform_heldout),
        ("c269_confidence_gate_stretch.py", "c287_confidence_gate_stretch.py", fix_nv),
        ("c282_capture_office_regression.py", "c288_capture_office_regression.py", xform_reg),
        ("c283_scorecard_and_stage.py", "c289_scorecard_and_stage.py", xform_score),
    ]
    for src, dst, fn in mapping:
        t = (SCR / src).read_text(encoding="utf-8")
        out = fn(t)
        (SCR / dst).write_text(out, encoding="utf-8")
        print("wrote", dst, "bytes", len(out.encode("utf-8")))
    d = (SCR / "c284_vision_v30_design_and_batch.py").read_text(encoding="utf-8")
    assert "vision_images_v30" in d and "v30_01" in d
    assert "VISION_V29" not in d
    assert "V30 overlays" in d
    s = (SCR / "c289_scorecard_and_stage.py").read_text(encoding="utf-8")
    assert "STAGE_ANT_C289.md" in s
    assert "C285_VISION_V30_SMOKE" in s
    nv = (SCR / "c287_confidence_gate_stretch.py").read_text(encoding="utf-8")
    assert "cg30_paid_force" in nv and "108.25" in nv
    print("ok")


if __name__ == "__main__":
    main()
