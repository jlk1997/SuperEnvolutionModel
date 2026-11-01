# -*- coding: utf-8 -*-
"""Patch copied V40 scripts into V41 / C352-C357."""
from __future__ import annotations
from pathlib import Path

ROOT = Path(r"E:\envolution")

# --- C352 design: rewrite SPECS + renames + V41 overlay ---
SPECS_BLOCK = '''SPECS = [
    ("v41_01", "basalt_recv", "paid_total", 156.25,
     ["BASALT GRAIN RECV V41", "a paid 74.00", "b paid 82.25", "c open 28.00", "TOTAL PAID TARGET 156.25"],
     "玄武岩收款单", "RECV"),
    ("v41_02", "velvet_wh", "qty_sum", 118.0,
     ["WH VELVET BIN V41", "SKU1 qty 47 ok", "SKU2 qty 39 hold", "SKU3 qty 52 ok", "qty_sum TARGET 118"],
     "丝绒仓位单", "RECV"),
    ("v41_03", "bronze_refund", "refund_done", 93.5,
     ["BRONZE PATCH REFUND V41", "itemR1 46.00 done", "itemR2 47.50 done", "itemR3 19.00 open", "refund_done TARGET 93.50"],
     "青铜补丁退款单", "DONE"),
    ("v41_04", "silk_tax", "tax_base_paid", 231.0,
     ["SILK TAX SLIP V41", "base 112.00 paid", "addon 119.00 paid", "skip 51.00", "tax_base_paid TARGET 231.00"],
     "真丝税基单", "TAX"),
    ("v41_05", "graphite_pay", "payroll_active", 301.0,
     ["GRAPHITE PAYROLL V41", "empA 148.00 active", "empB 153.00 active", "empC 44.00 leave", "payroll_active TARGET 301.00"],
     "石墨薪资单", "PAY"),
    ("v41_06", "flint_ship", "ship_ok", 79.0,
     ["FLINT SHIP DOCK V41", "box1 38 ok", "box2 22 ok", "box3 27 hold", "ship_ok TARGET 79"],
     "燧石出库单", "SHIP"),
    ("v41_07", "pewter_sla", "sla_ok_hours", 102.5,
     ["PEWTER SLA CARD V41", "job1 55.00 hours ok", "job2 47.50 hours ok", "job3 26.00 hours late", "sla_ok_hours TARGET 102.50"],
     "锡镴SLA卡", "SLA"),
    ("v41_08", "gauze_exp", "exp_sum", 133.75,
     ["GAUZE EXPENSE V41", "e1 64.00", "e2 69.75", "e3 30.00 void", "exp_sum TARGET 133.75"],
     "纱布费用单", "EXP"),
    ("v41_09", "walnut_po", "po_open", 149.0,
     ["WALNUT PO SHEET V41", "line1 80.00 open", "line2 69.00 open", "line3 35.00 closed", "po_open TARGET 149.00"],
     "胡桃采购单", "PO"),
    ("v41_10", "mica_order", "order_paid", 181.5,
     ["MICA ORDER V41", "skuA 96.00 paid", "skuB 85.50 paid", "skuC 27.00 due", "order_paid TARGET 181.50"],
     "云母订单", "ORD"),
    ("v41_11", "slate_dup", "dup_mark", 2.0,
     ["SLATE DUP MARK V41", "markA 1", "markB 1", "markC 0", "dup_mark TARGET 2"],
     "板岩重复标", "DUP"),
    ("v41_12", "air_zero", "zero_check", 0.0,
     ["AIR VOID ZERO V41", "z1 0.00", "z2 0.00", "z3 0.00", "zero_check TARGET 0.00"],
     "空仓零检单", "ZERO"),
    ("v41_13", "bamboo_ledger", "ledger_net", 268.25,
     ["BAMBOO LEDGER V41", "dr 131.00", "cr 137.25", "adj 44.00", "ledger_net TARGET 268.25"],
     "竹简账本", "LED"),
    ("v41_14", "lacquer_ui", "ui_ok", 1.0,
     ["LACQUER UI SCAN V41", "btnOK 1", "btnSkip 0", "btnBad 0", "ui_ok TARGET 1"],
     "大漆界面扫描", "UI"),
    ("v41_15", "quartz_stack", "stack_count", 16.0,
     ["QUARTZ STACK V41", "p1 7", "p2 6", "p3 3", "stack_count TARGET 16"],
     "石英堆叠单", "STK"),
    ("v41_16", "parchment_fax", "fax_pages", 22.0,
     ["PARCHMENT FAX V41", "pgA 12", "pgB 10", "pgC 5 drop", "fax_pages TARGET 22"],
     "羊皮纸传真单", "FAX"),
    ("v41_17", "rivet_glare", "glare_ok", 1.0,
     ["RIVET GLARE V41", "zone1 1 ok", "zone2 0", "zone3 0", "glare_ok TARGET 1"],
     "铆钉眩光单", "GLR"),
    ("v41_18", "canvas_tab", "tab_index", 31.0,
     ["CANVAS TAB INDEX V41", "tabA 17", "tabB 14", "tabC 4", "tab_index TARGET 31"],
     "帆布页签索引", "TAB"),
]
'''

V41_OVERLAY = r'''
    # --- V41 overlays (new vs V40) ---
    for _ in range(120):
        bx = rng.randint(50, 540)
        by = rng.randint(355, 585)
        if in_text_band(by):
            continue
        d.line([(bx, by), (bx + rng.randint(6, 26), by + rng.randint(-5, 5))], fill=(60, 80, 50), width=1)
    for gi in range(5):
        d.ellipse([54 + gi * 24, 316, 72 + gi * 24, 334], outline=(40, 90, 40), width=2)
    d.text((54, 336), "BASALT bait 41.41", fill=(40, 70, 40), font=f_tiny)
    for hi in range(4):
        d.polygon([(590 + hi * 34, 40), (616 + hi * 34, 40), (603 + hi * 34, 76)], fill=(120, 40, 20))
    d.text((590, 80), "BRONZE bait 61.61", fill=(90, 30, 10), font=f_tiny)
    d.rectangle([260, 390, 420, 450], fill=(250, 248, 255))
    d.text((270, 410), "VELVET ghost 91.91", fill=(60, 20, 80), font=f_pen)
    d.arc([420, 380, 510, 450], 25, 255, fill=(40, 40, 120), width=3)
    d.text((420, 455), "GRAPHITE bait 36.36", fill=(30, 30, 80), font=f_tiny)
    d.ellipse([70, 480, 140, 540], fill=(150, 140, 120), outline=(70, 60, 50), width=2)
    d.text((70, 545), "WALNUT bait 27.27", fill=(70, 50, 30), font=f_tiny)
    for qi in range(4):
        d.rectangle([260 + qi * 42, 480, 292 + qi * 42, 512], outline=(80, 90, 50), width=2)
    d.rectangle([860, 120, 1010, 180], fill=(190, 185, 170), outline=(60, 55, 45), width=2)
    d.text((880, 138), "FLINT", fill=(30, 30, 25), font=f_stamp)
    d.polygon([(40, 4), (420, 4), (405, 18), (50, 18)], fill=(210, 200, 175), outline=(100, 80, 50), width=1)
    d.text((70, 5), "RIVET bait 71.71", fill=(50, 40, 30), font=f_tiny)
    for ti, ty in enumerate((100, 160, 220)):
        d.polygon([(1000, ty), (1024, ty + 12), (1000, ty + 24)], fill=(50, 90, 50 + ti * 20))
    # binder ring holes + stapler scatter (V41-only)
    for hy in (100, 180, 260):
        d.ellipse([8, hy, 28, hy + 20], fill=(210, 206, 196), outline=(30, 30, 30), width=2)
    for (sx, sy) in [(160, 360), (340, 390), (480, 370)]:
        if not in_text_band(sy):
            d.rectangle([sx, sy, sx + 14, sy + 6], fill=(40, 40, 50))
'''

p = ROOT / "scripts/c352_vision_v41_design_and_batch.py"
t = p.read_text(encoding="utf-8")
# replace SPECS block
import re
t2, n = re.subn(r"SPECS = \[.*?\]\n", SPECS_BLOCK + "\n", t, count=1, flags=re.S)
assert n == 1, n
repls = [
    ("Vision V40", "Vision V41"),
    ("Harder than V39", "Harder than V40"),
    ("v40c346", "v41c352"),
    ("vision_images_v40", "vision_images_v41"),
    ("蚁算_VL_GATE_V40_PROTOCOL.md", "蚁算_VL_GATE_V41_PROTOCOL.md"),
    ("runs/vision_v40_c346", "runs/vision_v41_c352"),
    ("SCAN DESK V40", "SCAN DESK V41"),
    ("V40 C346 clarity", "V41 C352 clarity"),
    ("Teak|Onyx|Chiffon|Cobalt|Tourmaline|Bollard|Topaz|Shale|Tin|Linen|Herringbone|Null|Jute|Enamel|Hemp|Quince|Iridium|Folio",
     "Basalt|Velvet|Bronze|Silk|Graphite|Flint|Pewter|Gauze|Walnut|Mica|Slate|Air|Bamboo|Lacquer|Quartz|Parchment|Rivet|Canvas"),
    ('"version": "v40"', '"version": "v41"'),
    ("teak_onyx_chiffon_cobalt_tourmaline_bollard_topaz_shale_tin_linen_herringbone_null_jute_enamel_hemp_quince_iridium_folio",
     "basalt_velvet_bronze_silk_graphite_flint_pewter_gauze_walnut_mica_slate_air_bamboo_lacquer_quartz_parchment_rivet_canvas"),
    ("v39_spruce_carnelian_voile", "v40_teak_onyx_chiffon"),
    ("V40 keeps floor", "V41 keeps floor"),
    ("C346", "C352"),
    ("vision_v40_design_and_batch", "vision_v41_design_and_batch"),
    ("vl_gate_v40_claim", "vl_gate_v41_claim"),
    ("C346_VISION_V40_DESIGN.json", "C352_VISION_V41_DESIGN.json"),
    ("Ant VL Gate V40 Protocol", "Ant VL Gate V41 Protocol"),
    ("Harder than V39:", "Harder than V40:"),
    ("(V40 uses", "(V41 uses"),
    ("# --- V40 overlays (new vs V39) ---", "# --- V40 overlays kept; V41 overlays follow ---"),
]
for a, b in repls:
    t2 = t2.replace(a, b)
# insert V41 overlay before buf = io.BytesIO
marker = '    buf = io.BytesIO()'
assert marker in t2
t2 = t2.replace(marker, V41_OVERLAY + "\n" + marker, 1)
# fix docstring themes line
t2 = t2.replace(
    "NEW themes vs V32: parchment, cork, canvas, rivet, holo, zip, filament, honey,\nmarble, copper, acetate, perf, waxseal, magnet, crepe, satin, spiral.",
    "NEW themes vs V40: basalt, velvet, bronze, silk, graphite, flint, pewter, gauze,\nwalnut, mica, slate, air, bamboo, lacquer, quartz, parchment, rivet, canvas.",
)
p.write_text(t2, encoding="utf-8")
print("c352 ok", len(t2))

# --- C353 smoke ---
p = ROOT / "scripts/c353_vision_v41_smoke.py"
t = p.read_text(encoding="utf-8")
for a, b in [
    ("V40", "V41"), ("v40", "v41"), ("C347", "C353"), ("c347", "c353"),
    ("C346", "C352"),
]:
    t = t.replace(a, b)
p.write_text(t, encoding="utf-8")
print("c353 ok")

# --- C354 heldout ---
HELDOUT_SPECS = '''SPECS = [
    ("v41h_01", "basalt_recv", "paid_total", 84.75,
     ["BASALT GRAIN RECV V41", "a paid 40.00", "b paid 44.75", "c open 15.00", "TOTAL PAID TARGET 84.75"],
     "玄武岩收款单H", "RECV"),
    ("v41h_02", "velvet_wh", "qty_sum", 63.0,
     ["WH VELVET BIN V41", "SKU1 qty 25 ok", "SKU2 qty 21 hold", "SKU3 qty 28 ok", "qty_sum TARGET 63"],
     "丝绒仓位单H", "RECV"),
    ("v41h_03", "bronze_refund", "refund_done", 50.5,
     ["BRONZE PATCH REFUND V41", "itemR1 25.00 done", "itemR2 25.50 done", "itemR3 10.00 open", "refund_done TARGET 50.50"],
     "青铜补丁退款单H", "DONE"),
    ("v41h_04", "silk_tax", "tax_base_paid", 124.0,
     ["SILK TAX SLIP V41", "base 60.00 paid", "addon 64.00 paid", "skip 28.00", "tax_base_paid TARGET 124.00"],
     "真丝税基单H", "TAX"),
    ("v41h_05", "graphite_pay", "payroll_active", 162.0,
     ["GRAPHITE PAYROLL V41", "empA 79.00 active", "empB 83.00 active", "empC 24.00 leave", "payroll_active TARGET 162.00"],
     "石墨薪资单H", "PAY"),
    ("v41h_06", "flint_ship", "ship_ok", 42.0,
     ["FLINT SHIP DOCK V41", "box1 20 ok", "box2 12 ok", "box3 15 hold", "ship_ok TARGET 42"],
     "燧石出库单H", "SHIP"),
    ("v41h_07", "pewter_sla", "sla_ok_hours", 55.25,
     ["PEWTER SLA CARD V41", "job1 30.00 hours ok", "job2 25.25 hours ok", "job3 14.00 hours late", "sla_ok_hours TARGET 55.25"],
     "锡镴SLA卡H", "SLA"),
    ("v41h_08", "gauze_exp", "exp_sum", 72.25,
     ["GAUZE EXPENSE V41", "e1 35.00", "e2 37.25", "e3 16.00 void", "exp_sum TARGET 72.25"],
     "纱布费用单H", "EXP"),
    ("v41h_09", "walnut_po", "po_open", 80.0,
     ["WALNUT PO SHEET V41", "line1 43.00 open", "line2 37.00 open", "line3 19.00 closed", "po_open TARGET 80.00"],
     "胡桃采购单H", "PO"),
    ("v41h_10", "mica_order", "order_paid", 97.75,
     ["MICA ORDER V41", "skuA 52.00 paid", "skuB 45.75 paid", "skuC 15.00 due", "order_paid TARGET 97.75"],
     "云母订单H", "ORD"),
    ("v41h_11", "slate_dup", "dup_mark", 2.0,
     ["SLATE DUP MARK V41", "markA 1", "markB 1", "markC 0", "dup_mark TARGET 2"],
     "板岩重复标H", "DUP"),
    ("v41h_12", "air_zero", "zero_check", 0.0,
     ["AIR VOID ZERO V41", "z1 0.00", "z2 0.00", "z3 0.00", "zero_check TARGET 0.00"],
     "空仓零检单H", "ZERO"),
    ("v41h_13", "bamboo_ledger", "ledger_net", 144.5,
     ["BAMBOO LEDGER V41", "dr 71.00", "cr 73.50", "adj 24.00", "ledger_net TARGET 144.50"],
     "竹简账本H", "LED"),
    ("v41h_14", "lacquer_ui", "ui_ok", 1.0,
     ["LACQUER UI SCAN V41", "btnOK 1", "btnSkip 0", "btnBad 0", "ui_ok TARGET 1"],
     "大漆界面扫描H", "UI"),
    ("v41h_15", "quartz_stack", "stack_count", 9.0,
     ["QUARTZ STACK V41", "p1 4", "p2 3", "p3 2", "stack_count TARGET 9"],
     "石英堆叠单H", "STK"),
    ("v41h_16", "parchment_fax", "fax_pages", 12.0,
     ["PARCHMENT FAX V41", "pgA 6", "pgB 6", "pgC 3 drop", "fax_pages TARGET 12"],
     "羊皮纸传真单H", "FAX"),
    ("v41h_17", "rivet_glare", "glare_ok", 1.0,
     ["RIVET GLARE V41", "zone1 1 ok", "zone2 0", "zone3 0", "glare_ok TARGET 1"],
     "铆钉眩光单H", "GLR"),
    ("v41h_18", "canvas_tab", "tab_index", 17.0,
     ["CANVAS TAB INDEX V41", "tabA 9", "tabB 8", "tabC 2", "tab_index TARGET 17"],
     "帆布页签索引H", "TAB"),
]
'''
p = ROOT / "scripts/c354_vision_v41_heldout.py"
t = p.read_text(encoding="utf-8")
t2, n = re.subn(r"SPECS = \[.*?\]\n", HELDOUT_SPECS + "\n", t, count=1, flags=re.S)
assert n == 1, n
for a, b in [
    ("Vision V40", "Vision V41"),
    ("V33 train", "V41 train"),
    ("vision_images_v40h", "vision_images_v41h"),
    ("vision_images_v40", "vision_images_v41"),
    ("蚁算_VL_GATE_V40_HELDOUT_PROTOCOL.md", "蚁算_VL_GATE_V41_HELDOUT_PROTOCOL.md"),
    ("runs/vision_v40h_c348", "runs/vision_v41h_c354"),
    ("v40c346", "v41c352"),
    ("v40h", "v41h"),  # careful - may double
]:
    pass
# do careful replacements
t2 = t2.replace("Vision V40 heldout", "Vision V41 heldout")
t2 = t2.replace("Different ids/amounts from V33 train (C302/C303)", "Different ids/amounts from V41 train (C352/C353)")
t2 = t2.replace("vision_images_v40h", "vision_images_v41h")
t2 = t2.replace("TRAIN_FIX = ROOT / \"evo/office/fixtures/vision_images_v40\"",
                "TRAIN_FIX = ROOT / \"evo/office/fixtures/vision_images_v41\"")
t2 = t2.replace("蚁算_VL_GATE_V40_HELDOUT_PROTOCOL.md", "蚁算_VL_GATE_V41_HELDOUT_PROTOCOL.md")
t2 = t2.replace("runs/vision_v40h_c348", "runs/vision_v41h_c354")
t2 = t2.replace("C348", "C354")
t2 = t2.replace("C346", "C352")
t2 = t2.replace("C347", "C353")
t2 = t2.replace("v40", "v41")
t2 = t2.replace("V40", "V41")
# fix any double v41h from v40h -> if we had already v41h from SPECS it's fine
# But replacing v40 globally after SPECS may have broken v41h if SPECS had v40h originally - we replaced SPECS first with v41h, then v40->v41 shouldn't touch v41h
p.write_text(t2, encoding="utf-8")
print("c354 ok", "v41h_01" in t2, "v40" in t2.lower())

# --- C355 dissolve ---
p = ROOT / "scripts/c355_dissolve_cost_shadow.py"
t = p.read_text(encoding="utf-8")
t = t.replace("C349", "C355").replace("c349", "c355")
p.write_text(t, encoding="utf-8")
print("c355 ok")

# --- C356 regression ---
p = ROOT / "scripts/c356_capture_office_regression.py"
t = p.read_text(encoding="utf-8")
t = t.replace("C350", "C356").replace("c350", "c356")
p.write_text(t, encoding="utf-8")
print("c356 ok")

print("patch design done")
