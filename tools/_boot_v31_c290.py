# -*- coding: utf-8 -*-
"""Bootstrap C290-C295 Vision V31 suite from V30 scripts + dissolve/shadow NV."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCR = ROOT / "scripts"

TRAIN_SPECS = '''SPECS = [
    ("v31_01", "graphite_recv", "paid_total", 109.5,
     ["GRAPHITE SMUDGE RECV V31", "a paid 54.00", "b paid 55.50", "c open 15.00", "TOTAL PAID TARGET 109.50"],
     "石墨擦痕收款单", "RECV"),
    ("v31_02", "emboss_wh", "qty_sum", 97.0,
     ["WH EMBOSS SEAL V31", "SKU1 qty 46 ok", "SKU2 qty 21 hold", "SKU3 qty 51 ok", "qty_sum TARGET 97"],
     "浮雕印章仓单", "RECV"),
    ("v31_03", "carbon_refund", "refund_done", 61.75,
     ["CARBON COPY REFUND V31", "itemR1 29.00 done", "itemR2 32.75 done", "itemR3 13.00 open", "refund_done TARGET 61.75"],
     "复写纸退款单", "DONE"),
    ("v31_04", "binder_tax", "tax_base_paid", 171.0,
     ["TAX BINDER RING V31", "T1 96.00 paid", "T2 39.00 open", "T3 75.00 paid", "tax_base_paid TARGET 171.00"],
     "活页环税基单", "RECV"),
    ("v31_05", "postage_pay", "payroll_active", 3080.0,
     ["PAYROLL POSTAGE METER V31", "A 1570 active", "B 310 leave", "C 1510 active", "payroll_active TARGET 3080"],
     "邮资计费工资单", "OK"),
    ("v31_06", "foil_ship", "ship_ok_qty", 82.0,
     ["SHIP FOIL STAMP V31", "P1 41 ok", "P2 20 hold", "P3 41 ok", "ship_ok_qty TARGET 82"],
     "烫金发运单", "SHIP"),
    ("v31_07", "mesh_sla", "open_pri_sum", 78.0,
     ["SLA MESH SCREEN BAIT V31", "S1 pri 33 open", "S2 pri 35 closed", "S3 pri 45 open", "open_pri_sum TARGET 78"],
     "网纹SLA", "OPEN"),
    ("v31_08", "wax_exp", "paid_total", 145.25,
     ["EXPENSE WAX SEAL V31", "E1 70.00 paid", "E2 26.00 void", "E3 75.25 paid", "paid_total TARGET 145.25"],
     "火漆报销单", "RECV"),
    ("v31_09", "punch_po", "paid_total", 111.5,
     ["PO-PUNCH HOLE V31", "itemA paid 54.00", "itemB paid 57.50", "itemC open 18.00", "TOTAL PAID TARGET 111.50"],
     "打孔采购单", "RECV"),
    ("v31_10", "accordion_order", "paid_total", 93.0,
     ["ORDER ACCORDION FILE V31", "A paid 45.00", "B paid 48.00", "C open 14.00", "TOTAL PAID TARGET 93.00"],
     "风琴夹订单", "RECV"),
    ("v31_11", "stencil_dup", "paid_total", 132.0,
     ["INVOICE #V31-STENCIL", "lineA paid 44.00", "lineB paid 44.00", "lineC paid 44.00", "TOTAL PAID TARGET 132.00"],
     "镂空模板重复发票", "RECV"),
    ("v31_12", "void_zero", "paid_total", 0.0,
     ["OPEN ONLY V31", "X 68.00 open", "Y 71.00 open", "paid_total TARGET 0.00"],
     "复写阴影未付", "HOLD"),
    ("v31_13", "mottled_ledger", "paid_total", 74.5,
     ["LEDGER MOTTLED GRAIN V31", "rA paid 36.00", "rB paid 38.50", "rC open 12.00", "TOTAL PAID TARGET 74.50"],
     "斑纹台账", "RECV"),
    ("v31_14", "toner_ui", "paid_total", 87.25,
     ["UI TONER BAND V31", "alpha paid 42.00", "beta paid 45.25", "gamma open 15.00", "TOTAL PAID TARGET 87.25"],
     "碳粉带界单据", "RECV"),
    ("v31_15", "blueprint_stack", "paid_total", 127.0,
     ["BLUEPRINT GRID STACK V31", "x paid 62.00 usd", "y paid 65.00 usd", "z open 21.00 usd", "TOTAL PAID TARGET 127.00"],
     "蓝图网格叠页", "RECV"),
    ("v31_16", "clasp_fax", "paid_total", 72.5,
     ["CN-EN CLASP ENVELOPE FAX V31", "tea paid 35.00", "rice paid 37.50", "soup open 13.00", "TOTAL PAID TARGET 72.50"],
     "扣钉信封传真双语", "RECV"),
    ("v31_17", "edgeband_glare", "paid_total", 99.75,
     ["EDGEBAND GLARE V31", "w1 paid 48.00", "w2 paid 51.75", "w3 open 17.00", "TOTAL PAID TARGET 99.75"],
     "封边眩光单", "RECV"),
    ("v31_18", "grommet_tab", "paid_total", 55.0,
     ["GROMMET CORNER TAB V31", "p1 paid 26.00", "p2 paid 29.00", "p3 open 10.00", "TOTAL PAID TARGET 55.00"],
     "鸡眼角签页", "RECV"),
]
'''

HELD_SPECS = '''SPECS = [
    ("v31h_01", "graphite_recv", "paid_total", 62.5,
     ["GRAPHITE SMUDGE RECV V31H", "a paid 30.00", "b paid 32.50", "c open 11.00", "TOTAL PAID TARGET 62.50"],
     "石墨擦痕收款单H", "RECV"),
    ("v31h_02", "emboss_wh", "qty_sum", 51.0,
     ["WH EMBOSS SEAL V31H", "SKU1 qty 24 ok", "SKU2 qty 12 hold", "SKU3 qty 27 ok", "qty_sum TARGET 51"],
     "浮雕印章仓单H", "RECV"),
    ("v31h_03", "carbon_refund", "refund_done", 36.25,
     ["CARBON COPY REFUND V31H", "itemR1 17.00 done", "itemR2 19.25 done", "itemR3 8.00 open", "refund_done TARGET 36.25"],
     "复写纸退款单H", "DONE"),
    ("v31h_04", "binder_tax", "tax_base_paid", 107.0,
     ["TAX BINDER RING V31H", "T1 59.00 paid", "T2 24.00 open", "T3 48.00 paid", "tax_base_paid TARGET 107.00"],
     "活页环税基单H", "RECV"),
    ("v31h_05", "postage_pay", "payroll_active", 2120.0,
     ["PAYROLL POSTAGE METER V31H", "A 1080 active", "B 220 leave", "C 1040 active", "payroll_active TARGET 2120"],
     "邮资计费工资单H", "OK"),
    ("v31h_06", "foil_ship", "ship_ok_qty", 43.0,
     ["SHIP FOIL STAMP V31H", "P1 21 ok", "P2 11 hold", "P3 22 ok", "ship_ok_qty TARGET 43"],
     "烫金发运单H", "SHIP"),
    ("v31h_07", "mesh_sla", "open_pri_sum", 45.0,
     ["SLA MESH SCREEN BAIT V31H", "S1 pri 19 open", "S2 pri 21 closed", "S3 pri 26 open", "open_pri_sum TARGET 45"],
     "网纹SLAH", "OPEN"),
    ("v31h_08", "wax_exp", "paid_total", 81.25,
     ["EXPENSE WAX SEAL V31H", "E1 39.00 paid", "E2 16.00 void", "E3 42.25 paid", "paid_total TARGET 81.25"],
     "火漆报销单H", "RECV"),
    ("v31h_09", "punch_po", "paid_total", 65.0,
     ["PO-PUNCH HOLE V31H", "itemA paid 31.00", "itemB paid 34.00", "itemC open 12.00", "TOTAL PAID TARGET 65.00"],
     "打孔采购单H", "RECV"),
    ("v31h_10", "accordion_order", "paid_total", 56.5,
     ["ORDER ACCORDION FILE V31H", "A paid 27.00", "B paid 29.50", "C open 10.00", "TOTAL PAID TARGET 56.50"],
     "风琴夹订单H", "RECV"),
    ("v31h_11", "stencil_dup", "paid_total", 72.0,
     ["INVOICE #V31H-STENCIL", "lineA paid 24.00", "lineB paid 24.00", "lineC paid 24.00", "TOTAL PAID TARGET 72.00"],
     "镂空模板重复发票H", "RECV"),
    ("v31h_12", "void_zero", "paid_total", 0.0,
     ["OPEN ONLY V31H", "X 37.00 open", "Y 40.00 open", "paid_total TARGET 0.00"],
     "复写阴影未付H", "HOLD"),
    ("v31h_13", "mottled_ledger", "paid_total", 43.5,
     ["LEDGER MOTTLED GRAIN V31H", "rA paid 21.00", "rB paid 22.50", "rC open 8.00", "TOTAL PAID TARGET 43.50"],
     "斑纹台账H", "RECV"),
    ("v31h_14", "toner_ui", "paid_total", 49.75,
     ["UI TONER BAND V31H", "alpha paid 24.00", "beta paid 25.75", "gamma open 9.00", "TOTAL PAID TARGET 49.75"],
     "碳粉带界单据H", "RECV"),
    ("v31h_15", "blueprint_stack", "paid_total", 77.0,
     ["BLUEPRINT GRID STACK V31H", "x paid 37.00 usd", "y paid 40.00 usd", "z open 13.00 usd", "TOTAL PAID TARGET 77.00"],
     "蓝图网格叠页H", "RECV"),
    ("v31h_16", "clasp_fax", "paid_total", 41.25,
     ["CN-EN CLASP ENVELOPE FAX V31H", "tea paid 20.00", "rice paid 21.25", "soup open 8.00", "TOTAL PAID TARGET 41.25"],
     "扣钉信封传真双语H", "RECV"),
    ("v31h_17", "edgeband_glare", "paid_total", 58.0,
     ["EDGEBAND GLARE V31H", "w1 paid 28.00", "w2 paid 30.00", "w3 open 11.00", "TOTAL PAID TARGET 58.00"],
     "封边眩光单H", "RECV"),
    ("v31h_18", "grommet_tab", "paid_total", 33.5,
     ["GROMMET CORNER TAB V31H", "p1 paid 16.00", "p2 paid 17.50", "p3 open 7.00", "TOTAL PAID TARGET 33.50"],
     "鸡眼角签页H", "RECV"),
]
'''

V31_OVERLAY = r'''
    # --- V31 overlays (new vs V30) ---
    # graphite pencil smudge arcs (below text band)
    for _ in range(70):
        gx = rng.randint(70, 510)
        gy = rng.randint(310, 560)
        if in_text_band(gy):
            continue
        d.ellipse([gx, gy, gx + 5, gy + 2], fill=(90, 90, 95))
    # emboss seal ring bottom-right of card
    d.ellipse([430, 470, 520, 550], outline=(120, 100, 80), width=3)
    d.ellipse([445, 485, 505, 535], outline=(140, 120, 100), width=2)
    d.text((455, 500), "EMBOSS", fill=(130, 110, 90), font=f_tiny)
    # carbon-copy blue ghost
    d.text((90, 370), "CARBON GHOST bait 77.77", fill=(80, 100, 160), font=f_pen)
    # binder ring holes left of card
    for hy in range(90, 520, 36):
        d.ellipse([8, hy, 28, hy + 16], fill=(210, 206, 196), outline=(40, 40, 40), width=1)
        d.ellipse([12, hy + 4, 24, hy + 12], fill=(180, 176, 166))
    # postage meter bar
    d.rectangle([760, 20, 1060, 70], fill=(240, 240, 255), outline=(0, 0, 80), width=2)
    d.text((770, 30), "POSTAGE METER bait 66.66", fill=(0, 0, 80), font=f_fax)
    d.text((770, 50), "METER #V31-FAKE", fill=(0, 0, 80), font=f_fax)
    # foil stamp glitter strip
    for fx in range(80, 500, 10):
        col = (220, 190, 60) if (fx // 10) % 2 == 0 else (255, 230, 120)
        d.rectangle([fx, 285, fx + 7, 302], fill=col)
    # mesh screen hatch below text
    for mx in range(70, 520, 14):
        d.line([(mx, 330), (mx + 40, 370)], fill=(160, 160, 170), width=1)
    # wax seal blob
    d.ellipse([470, 500, 545, 560], fill=(140, 20, 40))
    d.text((485, 520), "WAX", fill=(255, 220, 220), font=f_stamp)
    # punch holes bottom row
    for px in range(90, 500, 40):
        d.ellipse([px, 580, px + 12, 592], fill=(210, 206, 196), outline=(30, 30, 30), width=1)
    # accordion fold zig
    for t in range(0, 9):
        x0 = 90 + t * 48
        d.line([(x0, 350), (x0 + 24, 375), (x0 + 48, 350)], fill=(80, 80, 90), width=2)
    # stencil cutout rectangles (bait numbers outside text)
    d.rectangle([100, 400, 180, 430], outline=(40, 40, 40), width=2)
    d.text((110, 408), "88.88", fill=(40, 40, 40), font=f_tiny)
    # mottled grain dots
    for _ in range(120):
        mx = rng.randint(60, 530)
        my = rng.randint(450, 570)
        d.point((mx, my), fill=(150, 140, 130))
    # toner band vertical
    d.rectangle([540, 60, 555, 280], fill=(50, 50, 55))
    # blueprint grid light
    for bx in range(70, 520, 20):
        d.line([(bx, 250), (bx, 290)], fill=(180, 200, 230), width=1)
    for by in range(250, 295, 10):
        d.line([(70, by), (520, by)], fill=(180, 200, 230), width=1)
    # clasp envelope triangle
    d.polygon([(250, 8), (310, 8), (280, 45)], fill=(60, 70, 90))
    d.rectangle([265, 40, 295, 55], fill=(80, 90, 110))
    # edgeband stripe top
    d.rectangle([60, 14, 400, 26], fill=(200, 160, 80), outline=(120, 80, 20), width=1)
    d.text((70, 15), "EDGEBAND bait 44.44", fill=(80, 40, 0), font=f_tiny)
    # grommet corner
    d.ellipse([520, 70, 548, 98], fill=(70, 70, 80), outline=(20, 20, 20), width=2)
    d.ellipse([528, 78, 540, 90], fill=(210, 206, 196))
'''


def replace_specs(text: str, new_specs: str) -> str:
    return re.sub(r"SPECS = \[.*?\]\n", new_specs + "\n", text, count=1, flags=re.S)


def xform_train(text: str) -> str:
    reps = [
        ("C284", "C290"), ("C285", "C291"), ("C286", "C292"),
        ("v30", "v31"), ("V30", "V31"), ("V30H", "V31H"), ("v30h", "v31h"),
        ("vision_images_v30", "vision_images_v31"),
        ("vision_v30_c284", "vision_v31_c290"),
        ("VL_GATE_V30_PROTOCOL", "VL_GATE_V31_PROTOCOL"),
        ("vl_gate_v30_claim", "vl_gate_v31_claim"),
        ("vision_gate_v30_claim", "vision_gate_v31_claim"),
        ("r50plus_v30_", "r50plus_v31_"),
        ("SCAN DESK V30", "SCAN DESK V31"),
        ("V30 C284", "V31 C290"),
        ("V30 keeps floor", "V31 keeps floor"),
        ("Vision V30", "Vision V31"),
        ("vision_v30", "vision_v31"),
        ("_v30c284", "_v31c290"),
        ("harder than V29", "harder than V30"),
        ("NEW themes vs V29", "NEW themes vs V30"),
        ("No claim until C285 VL", "No claim until C291 VL"),
        ("Velvet|Spiral|Mimeo|Ribbon|Neon|Holo|Lacquer|Rivet|Concertina|Serrate|Triptych|Washi|Inkjet|Redink|Bulldog|Corner",
         "Graphite|Emboss|Carbon|Binder|Postage|Foil|Mesh|Wax|Punch|Accordion|Stencil|Mottled|Toner|Blueprint|Clasp|Edgeband|Grommet"),
        ("velvet_spiral_mimeo_ribbon_neon_holo_lacquer_rivet_concertina_serrate_triptych_washi_inkjet_redink_bulldog_corner",
         "graphite_emboss_carbon_binder_postage_foil_mesh_wax_punch_accordion_stencil_mottled_toner_blueprint_clasp_edgeband_grommet"),
    ]
    for a, b in reps:
        text = text.replace(a, b)
    text = replace_specs(text, TRAIN_SPECS)
    needle = "    # fingerprint ovals (outside text band preferred)"
    if needle in text and "V31 overlays" not in text:
        text = text.replace(needle, V31_OVERLAY + "\n" + needle)
    elif "V30 overlays" in text and "V31 overlays" not in text:
        # inject after last V30 overlay block marker area — append before soft_affine if present
        soft = "    # soft_affine"
        if soft in text:
            text = text.replace(soft, V31_OVERLAY + "\n" + soft, 1)
        else:
            # fallback: before img.save
            text = text.replace("    img.save(buf", V31_OVERLAY + "\n    img.save(buf", 1)
    # docstring themes cleanup
    text = re.sub(
        r'NEW themes vs V31:.*?\nCLARITY FLOOR:',
        "NEW themes vs V30: graphite, emboss, carbon, binder, postage, foil, mesh, wax,\n"
        "punch, accordion, stencil, mottled, toner, blueprint, clasp, edgeband, grommet.\n"
        "CLARITY FLOOR:",
        text,
        count=1,
        flags=re.S,
    )
    return text


def xform_smoke(text: str) -> str:
    reps = [
        ("C285", "C291"), ("C284", "C290"),
        ("v30", "v31"), ("V30", "V31"),
        ("vision_images_v30", "vision_images_v31"),
        ("vision_v30_c285", "vision_v31_c291"),
        ("vl_gate_v30_claim", "vl_gate_v31_claim"),
        ("vision_gate_v30_claim", "vision_gate_v31_claim"),
        ("r50plus_v30_", "r50plus_v31_"),
        ("vision_v30_smoke", "vision_v31_smoke"),
        ("C285_VISION_V30", "C291_VISION_V31"),
        ("C285b_VISION_GATE_V30", "C291b_VISION_GATE_V31"),
    ]
    for a, b in reps:
        text = text.replace(a, b)
    return text


def xform_heldout(text: str) -> str:
    reps = [
        ("C286", "C292"), ("C284", "C290"), ("C285", "C291"),
        ("v30h", "v31h"), ("V30H", "V31H"), ("v30", "v31"), ("V30", "V31"),
        ("vision_images_v30h", "vision_images_v31h"),
        ("vision_images_v30", "vision_images_v31"),
        ("vision_v30h_c286", "vision_v31h_c292"),
        ("VL_GATE_V30_HELDOUT_PROTOCOL", "VL_GATE_V31_HELDOUT_PROTOCOL"),
        ("vl_gate_v30_heldout_claim", "vl_gate_v31_heldout_claim"),
        ("vision_gate_v30_heldout_claim", "vision_gate_v31_heldout_claim"),
        ("r50plus_v30_heldout", "r50plus_v31_heldout"),
        ("vision_v30_heldout", "vision_v31_heldout"),
        ("C286_VISION_V30", "C292_VISION_V31"),
        ("C286b_VISION_GATE_V30", "C292b_VISION_GATE_V31"),
        ("SCAN DESK V30H", "SCAN DESK V31H"),
        ("V30H C286", "V31H C292"),
    ]
    for a, b in reps:
        text = text.replace(a, b)
    text = replace_specs(text, HELD_SPECS)
    return text


def xform_nv(text: str) -> str:
    # C263 dissolve_cost_shadow -> C293
    text = text.replace("C263", "C293")
    text = text.replace("dissolve_cost_shadow_c263", "dissolve_cost_shadow_c293")
    text = text.replace("DISSOLVE_DASHBOARD_C263", "DISSOLVE_DASHBOARD_C293")
    text = text.replace("C263_DISSOLVE_COST_SHADOW.json", "C293_DISSOLVE_COST_SHADOW.json")
    # tweak replace_stress scenarios slightly for freshness
    text = text.replace('"bare_steps": 4, "agent_steps": 15', '"bare_steps": 4, "agent_steps": 16')
    text = text.replace('"bare_steps": 3, "agent_steps": 12', '"bare_steps": 3, "agent_steps": 13', 1)
    text = text.replace('"bare_steps": 5, "agent_steps": 18', '"bare_steps": 5, "agent_steps": 19')
    text = text.replace('"bare_steps": 2, "agent_steps": 9', '"bare_steps": 2, "agent_steps": 10')
    text = text.replace('"bare_steps": 3, "agent_steps": 13', '"bare_steps": 3, "agent_steps": 14', 1)
    text = text.replace('"bare_steps": 3, "agent_steps": 11', '"bare_steps": 3, "agent_steps": 12')
    return text


def xform_reg(text: str) -> str:
    text = text.replace("C288", "C294")
    text = text.replace("C284-C287", "C290-C293")
    text = text.replace("c284_c287", "c290_c293")
    text = text.replace("capture_regression_c288", "capture_regression_c294")
    needle = '("V30_heldout", DOC / "C286_VISION_V30_HELDOUT_SMOKE.json"),'
    insert = (
        needle
        + '\n    ("V31", DOC / "C291_VISION_V31_SMOKE.json"),'
        + '\n    ("V31_heldout", DOC / "C292_VISION_V31_HELDOUT_SMOKE.json"),'
    )
    if needle in text and '("V31"' not in text:
        text = text.replace(needle, insert)
    # add dissolve C293 pointer
    text = text.replace(
        '("C287_confidence_gate_stretch", DOC / "C287_CONFIDENCE_GATE_STRETCH.json"),',
        '("C287_confidence_gate_stretch", DOC / "C287_CONFIDENCE_GATE_STRETCH.json"),\n'
        '    ("C293_dissolve_cost_shadow", DOC / "C293_DISSOLVE_COST_SHADOW.json"),',
    )
    # required list
    text = text.replace(
        'required = ["V25", "V25_heldout", "V26", "V26_heldout", "V27", "V27_heldout", "V28", "V28_heldout", "V29", "V29_heldout", "V30", "V30_heldout", "C233_clarity_floor", "C287_confidence_gate_stretch"]',
        'required = ["V25", "V25_heldout", "V26", "V26_heldout", "V27", "V27_heldout", "V28", "V28_heldout", "V29", "V29_heldout", "V30", "V30_heldout", "V31", "V31_heldout", "C233_clarity_floor", "C293_dissolve_cost_shadow"]',
    )
    text = text.replace('DOC / "C288_CAPTURE_OFFICE_REGRESSION.json"', 'DOC / "C294_CAPTURE_OFFICE_REGRESSION.json"')
    return text


def xform_score(text: str) -> str:
    # Keep V30 historical; promote V31 as current; NV = dissolve C293
    text = text.replace("C289", "C295")
    text = text.replace("c284_c288", "c290_c294")
    text = text.replace("STAGE_ANT_C289.md", "STAGE_ANT_C295.md")
    text = text.replace("C284-C288", "C290-C294")
    text = text.replace("C284-C289", "C290-C295")
    text = text.replace("C272-C289", "C290-C295")

    # Inject V30 historical loads before current V30 loads, then rename current -> V31
    hist_inject = '''    c285v = load("docs/r50/C285_VISION_V30_SMOKE.json") or {}
    c285vb = load("docs/r50/C285b_VISION_GATE_V30_CLAIM.json") or {}
    c286v = load("docs/r50/C286_VISION_V30_HELDOUT_SMOKE.json") or {}
    c286vb = load("docs/r50/C286b_VISION_GATE_V30_HELDOUT_CLAIM.json") or {}
    c266 = load("docs/r50/C290_VISION_V31_DESIGN.json") or {}
    c267 = load("docs/r50/C291_VISION_V31_SMOKE.json") or {}
    c267b = load("docs/r50/C291b_VISION_GATE_V31_CLAIM.json") or {}
    c268 = load("docs/r50/C292_VISION_V31_HELDOUT_SMOKE.json") or {}
    c268b = load("docs/r50/C292b_VISION_GATE_V31_HELDOUT_CLAIM.json") or {}
    c270 = load("docs/r50/C294_CAPTURE_OFFICE_REGRESSION.json") or {}'''

    old_block = '''    c266 = load("docs/r50/C284_VISION_V30_DESIGN.json") or {}
    c267 = load("docs/r50/C285_VISION_V30_SMOKE.json") or {}
    c267b = load("docs/r50/C285b_VISION_GATE_V30_CLAIM.json") or {}
    c268 = load("docs/r50/C286_VISION_V30_HELDOUT_SMOKE.json") or {}
    c268b = load("docs/r50/C286b_VISION_GATE_V30_HELDOUT_CLAIM.json") or {}
    c270 = load("docs/r50/C288_CAPTURE_OFFICE_REGRESSION.json") or {}'''
    if old_block in text:
        text = text.replace(old_block, hist_inject)

    # NV: use C293 dissolve as primary non-vision; keep C287 as secondary
    text = text.replace(
        'c269 = load("docs/r50/C287_CONFIDENCE_GATE_STRETCH.json") or {}',
        'c269 = load("docs/r50/C293_DISSOLVE_COST_SHADOW.json") or {}\n'
        '    c287 = load("docs/r50/C287_CONFIDENCE_GATE_STRETCH.json") or {}',
    )
    # nv_pass: dissolve+shadow from C293
    text = text.replace(
        '''    nv_pass = bool(c269.get("pass") and (
        (c263.get("dissolve") or {}).get("pass", True)
        and (c263.get("shadow") or {}).get("pass", True)
    ))
    dissolve_pass = bool((c263.get("dissolve") or {}).get("pass", True))
    shadow_pass = bool((c263.get("shadow") or {}).get("pass", True))
    conf_pass = bool(c269.get("pass"))
    conf_rate = float((c269.get("u2c") or {}).get("rate") or c269.get("rate") or (c269.get("replace_ledger") or {}).get("bare_success_rate") or 0.0)''',
        '''    dissolve_pass = bool((c269.get("dissolve") or c263.get("dissolve") or {}).get("pass", True))
    shadow_pass = bool((c269.get("shadow") or c263.get("shadow") or {}).get("pass", True))
    nv_pass = bool(c269.get("pass") and dissolve_pass and shadow_pass)
    conf_pass = bool(c287.get("pass"))
    conf_rate = float(c287.get("rate") or 0.0)
    dissolve_rate = float(((c269.get("dissolve") or {}).get("summary") or {}).get("n_families") or 4)'''
    )

    # rates: keep v30 from hist, v31 from current c267
    text = text.replace(
        '''    v30 = float(c267.get("rate") or 0.0)
    v30h = float(c268.get("rate") or 0.0)''',
        '''    v30 = float(c285v.get("rate") or 0.0)
    v30h = float(c286v.get("rate") or 0.0)
    v31 = float(c267.get("rate") or 0.0)
    v31h = float(c268.get("rate") or 0.0)'''
    )
    text = text.replace(
        '''    v30_claim = bool(c267b.get("vl_gate_v30_claim") or c267.get("vl_gate_v30_claim") or c267.get("claim"))
    v30h_claim = bool(c268b.get("vl_gate_v30_heldout_claim") or c268.get("vl_gate_v30_heldout_claim") or c268.get("claim"))''',
        '''    v30_claim = bool(c285vb.get("vl_gate_v30_claim") or c285v.get("vl_gate_v30_claim") or c285v.get("claim"))
    v30h_claim = bool(c286vb.get("vl_gate_v30_heldout_claim") or c286v.get("vl_gate_v30_heldout_claim") or c286v.get("claim"))
    v31_claim = bool(c267b.get("vl_gate_v31_claim") or c267.get("vl_gate_v31_claim") or c267.get("claim"))
    v31h_claim = bool(c268b.get("vl_gate_v31_heldout_claim") or c268.get("vl_gate_v31_heldout_claim") or c268.get("claim"))'''
    )

    # composite: add v31
    text = text.replace(
        '''        max(v30, v30h, 0.0),
        1.0 if v30_claim else 0.0,
        1.0 if v30h_claim else 0.0,''',
        '''        max(v30, v30h, 0.0),
        1.0 if v30_claim else 0.0,
        1.0 if v30h_claim else 0.0,
        max(v31, v31h, 0.0),
        1.0 if v31_claim else 0.0,
        1.0 if v31h_claim else 0.0,'''
    )
    text = text.replace(
        "v30_claim and v30h_claim and capture_pass and nv_pass",
        "v31_claim and v31h_claim and capture_pass and nv_pass",
    )

    # vision dict: keep v30, add v31
    text = text.replace(
        '''            "v30_design": {"n": c266.get("n"), "clarity_floor": c266.get("clarity_floor"), "claim": False},
            "v30_smoke": {
                "rate": v30, "n": c267.get("n"), "n_ok": c267.get("n_ok"),
                "claim": v30_claim, "fail_ids": c267.get("fail_ids"),
            },
            "v30_heldout": {
                "rate": v30h, "n": c268.get("n"), "n_ok": c268.get("n_ok"),
                "claim": v30h_claim, "fail_ids": c268.get("fail_ids"),
                "id_disjoint": c268.get("id_disjoint"),
            },''',
        '''            "v30_smoke": {"rate": v30, "claim": v30_claim},
            "v30_heldout": {"rate": v30h, "claim": v30h_claim},
            "v31_design": {"n": c266.get("n"), "clarity_floor": c266.get("clarity_floor"), "claim": False},
            "v31_smoke": {
                "rate": v31, "n": c267.get("n"), "n_ok": c267.get("n_ok"),
                "claim": v31_claim, "fail_ids": c267.get("fail_ids"),
            },
            "v31_heldout": {
                "rate": v31h, "n": c268.get("n"), "n_ok": c268.get("n_ok"),
                "claim": v31h_claim, "fail_ids": c268.get("fail_ids"),
                "id_disjoint": c268.get("id_disjoint"),
            },'''
    )
    text = text.replace(
        '''            "confidence_gate_stretch": {"pass": conf_pass, "rate": conf_rate},
            "replace_ratio": replace.get("mean_ratio"),''',
        '''            "dissolve_cost_shadow": {"pass": nv_pass, "dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass},
            "confidence_gate_stretch": {"pass": conf_pass, "rate": conf_rate},
            "replace_ratio": replace.get("mean_ratio"),'''
    )

    # board / stage / ckpt text
    text = text.replace(
        "| V30 smoke / heldout | **{v30} / {v30h}** claim={v30_claim}/{v30h_claim} |\n| confidence-gate stretch (C287) | pass={conf_pass} rate={conf_rate} |",
        "| V30 smoke / heldout | **{v30} / {v30h}** claim={v30_claim}/{v30h_claim} |\n"
        "| V31 smoke / heldout | **{v31} / {v31h}** claim={v31_claim}/{v31h_claim} |\n"
        "| dissolve/shadow (C293) | pass={nv_pass} dissolve={dissolve_pass} shadow={shadow_pass} |\n"
        "| confidence-gate stretch (C287) | pass={conf_pass} rate={conf_rate} |",
    )
    text = text.replace(
        '''| C284 | V30 design | n={c266.get('n')} velvet/spiral/mimeo/ribbon/neon/... |
| C285 | V30 smoke | rate={v30} claim={v30_claim} |
| C286 | V30 heldout | rate={v30h} claim={v30h_claim} |
| C287 | confidence-gate stretch | pass={conf_pass} rate={conf_rate} |
| C288 | capture regression | pass={capture_pass} |
| C289 | scorecard | composite={composite} |''',
        '''| C290 | V31 design | n={c266.get('n')} graphite/emboss/carbon/binder/... |
| C291 | V31 smoke | rate={v31} claim={v31_claim} |
| C292 | V31 heldout | rate={v31h} claim={v31h_claim} |
| C293 | dissolve/shadow refresh | pass={nv_pass} |
| C294 | capture regression | pass={capture_pass} |
| C295 | scorecard | composite={composite} |'''
    )
    text = text.replace(
        "- V30: claim={v30_claim} rate={v30}\n- V30 heldout: claim={v30h_claim} rate={v30h}",
        "- V30: claim={v30_claim} rate={v30}\n- V30 heldout: claim={v30h_claim} rate={v30h}\n"
        "- V31: claim={v31_claim} rate={v31}\n- V31 heldout: claim={v31h_claim} rate={v31h}",
    )
    text = text.replace(
        '''Stage: C290-C295; V30 CLAIM {v30}; V30 heldout CLAIM {v30h}; nv pass={nv_pass}; capture pass={capture_pass}; composite={composite} STAGE_READY={stage_ready}
V30 design: clarity_floor jpeg_q=60 photo/=2 themes=velvet/spiral/mimeo/ribbon/neon/holo/lacquer/rivet/concertina/serrate/triptych/washi/inkjet/redink/bulldog/corner
V30 smoke: rate={v30} n={c267.get('n')} CLAIM={v30_claim} fail={c267.get('fail_ids')}
V30 heldout: rate={v30h} n={c268.get('n')} CLAIM={v30h_claim} disjoint={c268.get('id_disjoint')}
Non-vision C287: pass={conf_pass} rate={conf_rate} (confidence-gate stretch); dissolve/shadow from C263={dissolve_pass}/{shadow_pass}; replace_ratio={replace.get('mean_ratio')}
Capture regression: pass={capture_pass} (C288)
Scorecard composite: {composite} (C289)''',
        '''Stage: C290-C295; V31 CLAIM {v31}; V31 heldout CLAIM {v31h}; nv pass={nv_pass}; capture pass={capture_pass}; composite={composite} STAGE_READY={stage_ready}
V31 design: clarity_floor jpeg_q=60 photo/=2 themes=graphite/emboss/carbon/binder/postage/foil/mesh/wax/punch/accordion/stencil/mottled/toner/blueprint/clasp/edgeband/grommet
V31 smoke: rate={v31} n={c267.get('n')} CLAIM={v31_claim} fail={c267.get('fail_ids')}
V31 heldout: rate={v31h} n={c268.get('n')} CLAIM={v31h_claim} disjoint={c268.get('id_disjoint')}
Non-vision C293: pass={nv_pass} (dissolve/shadow refresh); conf-gate C287={conf_pass}/{conf_rate}; replace_ratio={replace.get('mean_ratio')}
Capture regression: pass={capture_pass} (C294)
Scorecard composite: {composite} (C295)'''
    )
    # fix leftover C290-C295 that may not have matched if Stage line still said C284
    text = text.replace(
        "Stage: C284-C289; V30 CLAIM {v30}; V30 heldout CLAIM {v30h}",
        "Stage: C290-C295; V31 CLAIM {v31}; V31 heldout CLAIM {v31h}",
    )
    text = text.replace(
        "V30 design: clarity_floor jpeg_q=60 photo/=2 themes=velvet/spiral/mimeo/ribbon/neon/holo/lacquer/rivet/concertina/serrate/triptych/washi/inkjet/redink/bulldog/corner",
        "V31 design: clarity_floor jpeg_q=60 photo/=2 themes=graphite/emboss/carbon/binder/postage/foil/mesh/wax/punch/accordion/stencil/mottled/toner/blueprint/clasp/edgeband/grommet",
    )
    text = text.replace(
        "V30 smoke: rate={v30} n={c267.get('n')} CLAIM={v30_claim} fail={c267.get('fail_ids')}",
        "V31 smoke: rate={v31} n={c267.get('n')} CLAIM={v31_claim} fail={c267.get('fail_ids')}",
    )
    text = text.replace(
        "V30 heldout: rate={v30h} n={c268.get('n')} CLAIM={v30h_claim} disjoint={c268.get('id_disjoint')}",
        "V31 heldout: rate={v31h} n={c268.get('n')} CLAIM={v31h_claim} disjoint={c268.get('id_disjoint')}",
    )
    text = text.replace(
        "Non-vision C287: pass={conf_pass} rate={conf_rate} (confidence-gate stretch); dissolve/shadow from C263={dissolve_pass}/{shadow_pass}; replace_ratio={replace.get('mean_ratio')}",
        "Non-vision C293: pass={nv_pass} (dissolve/shadow refresh); conf-gate C287={conf_pass}/{conf_rate}; replace_ratio={replace.get('mean_ratio')}",
    )
    text = text.replace("Capture regression: pass={capture_pass} (C288)", "Capture regression: pass={capture_pass} (C294)")
    text = text.replace("Scorecard composite: {composite} (C289)", "Scorecard composite: {composite} (C295)")
    text = text.replace(
        'f.write(f"- V30 smoke={v30} claim={v30_claim}; heldout={v30h} claim={v30h_claim}\\n")',
        'f.write(f"- V31 smoke={v31} claim={v31_claim}; heldout={v31h} claim={v31h_claim}\\n")',
    )
    text = text.replace(
        'f.write(f"- C287 confidence-gate stretch pass={conf_pass} rate={conf_rate}; replace',
        'f.write(f"- C293 dissolve/shadow pass={nv_pass}; conf-gate={conf_pass}/{conf_rate}; replace',
    )
    text = text.replace('"theme": "unified_scorecard_c290_c294"', '"theme": "unified_scorecard_c290_c294"')
    text = text.replace("unified_scorecard_c284_c288", "unified_scorecard_c290_c294")
    # replace source preference: C293 replace_stress if present
    text = text.replace(
        'rl = (c281.get("replace_ledger") or c269.get("replace_ledger") or {})',
        'rl = (c281.get("replace_ledger") or (c269.get("replace_stress") or {}) or c269.get("replace_ledger") or {})',
    )
    text = text.replace(
        '"source": "C281" if (c281.get("replace_ledger") or {}).get("mean_ratio") is not None else ("C287" if rl.get("mean_ratio") is not None else "C263")',
        '"source": "C281" if (c281.get("replace_ledger") or {}).get("mean_ratio") is not None else ("C293" if rl.get("mean_ratio") is not None else "C263")',
    )
    return text


def main():
    mapping = [
        ("c284_vision_v30_design_and_batch.py", "c290_vision_v31_design_and_batch.py", xform_train),
        ("c285_vision_v30_smoke.py", "c291_vision_v31_smoke.py", xform_smoke),
        ("c286_vision_v30_heldout.py", "c292_vision_v31_heldout.py", xform_heldout),
        ("c263_dissolve_cost_shadow.py", "c293_dissolve_cost_shadow.py", xform_nv),
        ("c288_capture_office_regression.py", "c294_capture_office_regression.py", xform_reg),
        ("c289_scorecard_and_stage.py", "c295_scorecard_and_stage.py", xform_score),
    ]
    for src, dst, fn in mapping:
        t = (SCR / src).read_text(encoding="utf-8")
        out = fn(t)
        (SCR / dst).write_text(out, encoding="utf-8")
        print("wrote", dst, "bytes", len(out.encode("utf-8")))
    d = (SCR / "c290_vision_v31_design_and_batch.py").read_text(encoding="utf-8")
    assert "vision_images_v31" in d and "v31_01" in d
    assert "VISION_V30" not in d or "vs V30" in d
    assert "V31 overlays" in d
    assert "graphite_recv" in d
    s = (SCR / "c295_scorecard_and_stage.py").read_text(encoding="utf-8")
    assert "STAGE_ANT_C295.md" in s
    assert "C291_VISION_V31_SMOKE" in s
    assert "c285v" in s and "v31_claim" in s
    nv = (SCR / "c293_dissolve_cost_shadow.py").read_text(encoding="utf-8")
    assert "C293" in nv and "dissolve_cost_shadow_c293" in nv
    print("ok")


if __name__ == "__main__":
    main()
