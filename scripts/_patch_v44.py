# -*- coding: utf-8 -*-
"""Patch C371-C376 copied from V43 into Vision V44."""
from pathlib import Path
import re

ROOT = Path(r"E:\envolution")

# --- Design SPECS (train) ---
SPECS_TRAIN = '''SPECS = [
    ("v44_01", "flint_recv", "paid_total", 188.75,
     ["FLINT GRAIN RECV V44",
     "a paid 92.00",
     "b paid 96.75",
     "c open 35.00",
     "TOTAL PAID TARGET 188.75"],
     "燧石收款单", "RECV"),
    ("v44_02", "velvet_wh", "qty_sum", 147.0,
     ["WH VELVET BIN V44",
     "SKU1 qty 61 ok",
     "SKU2 qty 48 hold",
     "SKU3 qty 65 ok",
     "qty_sum TARGET 147"],
     "天鹅绒仓位", "RECV"),
    ("v44_03", "bronze_refund", "refund_done", 119.25,
     ["BRONZE PATCH REFUND V44",
     "itemR1 57.00 done",
     "itemR2 62.25 done",
     "itemR3 26.00 open",
     "refund_done TARGET 119.25"],
     "青铜退款单", "DONE"),
    ("v44_04", "ivory_tax", "tax_base_paid", 274.5,
     ["IVORY TAX SLIP V44",
     "base 134.00 paid",
     "addon 140.50 paid",
     "skip 61.00",
     "tax_base_paid TARGET 274.50"],
     "象牙税基单", "TAX"),
    ("v44_05", "sapphire_pay", "payroll_active", 356.0,
     ["SAPPHIRE PAYROLL V44",
     "empA 174.00 active",
     "empB 182.00 active",
     "empC 55.00 leave",
     "payroll_active TARGET 356.00"],
     "蓝宝石工资", "PAY"),
    ("v44_06", "copper_ship", "ship_ok", 102.0,
     ["COPPER SHIP DOCK V44",
     "box1 48 ok",
     "box2 29 ok",
     "box3 34 hold",
     "ship_ok TARGET 102"],
     "紫铜出库单", "SHIP"),
    ("v44_07", "pewter_sla", "sla_ok_hours", 128.5,
     ["PEWTER SLA CARD V44",
     "job1 68.00 hours ok",
     "job2 60.50 hours ok",
     "job3 33.00 hours late",
     "sla_ok_hours TARGET 128.50"],
     "白镴SLA卡", "SLA"),
    ("v44_08", "willow_exp", "exp_sum", 164.25,
     ["WILLOW EXPENSE V44",
     "e1 78.00",
     "e2 86.25",
     "e3 37.00 void",
     "exp_sum TARGET 164.25"],
     "柳木费用单", "EXP"),
    ("v44_09", "mahogany_po", "po_open", 183.0,
     ["MAHOGANY PO SHEET V44",
     "line1 97.00 open",
     "line2 86.00 open",
     "line3 44.00 closed",
     "po_open TARGET 183.00"],
     "红木采购单", "PO"),
    ("v44_10", "silk_order", "order_paid", 221.75,
     ["SILK ORDER V44",
     "skuA 118.00 paid",
     "skuB 103.75 paid",
     "skuC 34.00 due",
     "order_paid TARGET 221.75"],
     "丝绸订单", "ORD"),
    ("v44_11", "basalt_dup", "dup_mark", 2.0,
     ["BASALT DUP MARK V44",
     "markA 1",
     "markB 1",
     "markC 0",
     "dup_mark TARGET 2"],
     "玄武重复标", "DUP"),
    ("v44_12", "ozone_zero", "zero_check", 0.0,
     ["OZONE AIR ZERO V44",
     "z1 0.00",
     "z2 0.00",
     "z3 0.00",
     "zero_check TARGET 0.00"],
     "臭氧零值校验", "ZERO"),
    ("v44_13", "teak_ledger", "ledger_net", 318.5,
     ["TEAK LEDGER V44",
     "dr 155.00",
     "cr 163.50",
     "adj 54.00",
     "ledger_net TARGET 318.50"],
     "柚木账本", "LED"),
    ("v44_14", "lacquer_ui", "ui_ok", 1.0,
     ["LACQUER UI SCAN V44",
     "btnOK 1",
     "btnSkip 0",
     "btnBad 0",
     "ui_ok TARGET 1"],
     "漆面界面扫描", "UI"),
    ("v44_15", "quartz_stack", "stack_count", 21.0,
     ["QUARTZ STACK V44",
     "p1 10",
     "p2 8",
     "p3 3",
     "stack_count TARGET 21"],
     "石英堆叠单", "STK"),
    ("v44_16", "parchment_fax", "fax_pages", 29.0,
     ["PARCHMENT FAX V44",
     "pgA 16",
     "pgB 13",
     "pgC 8 drop",
     "fax_pages TARGET 29"],
     "羊皮传真页", "FAX"),
    ("v44_17", "rivet_glare", "glare_ok", 1.0,
     ["RIVET GLARE V44",
     "zone1 1 ok",
     "zone2 0",
     "zone3 0",
     "glare_ok TARGET 1"],
     "铆钉眩光卡", "GLR"),
    ("v44_18", "canvas_tab", "tab_index", 41.0,
     ["CANVAS TAB INDEX V44",
     "tabA 23",
     "tabB 18",
     "tabC 7",
     "tab_index TARGET 41"],
     "帆布页签索引", "TAB"),
]
'''

SPECS_HELDOUT = '''SPECS = [
    ("v44h_01", "flint_recv", "paid_total", 104.5,
     ["FLINT GRAIN RECV V44H",
     "a paid 50.00",
     "b paid 54.50",
     "c open 19.00",
     "TOTAL PAID TARGET 104.50"],
     "燧石收款单", "RECV"),
    ("v44h_02", "velvet_wh", "qty_sum", 82.0,
     ["WH VELVET BIN V44H",
     "SKU1 qty 34 ok",
     "SKU2 qty 22 hold",
     "SKU3 qty 39 ok",
     "qty_sum TARGET 82"],
     "天鹅绒仓位", "RECV"),
    ("v44h_03", "bronze_refund", "refund_done", 66.75,
     ["BRONZE PATCH REFUND V44H",
     "itemR1 32.00 done",
     "itemR2 34.75 done",
     "itemR3 14.00 open",
     "refund_done TARGET 66.75"],
     "青铜退款单", "DONE"),
    ("v44h_04", "ivory_tax", "tax_base_paid", 152.0,
     ["IVORY TAX SLIP V44H",
     "base 74.00 paid",
     "addon 78.00 paid",
     "skip 34.00",
     "tax_base_paid TARGET 152.00"],
     "象牙税基单", "TAX"),
    ("v44h_05", "sapphire_pay", "payroll_active", 191.0,
     ["SAPPHIRE PAYROLL V44H",
     "empA 94.00 active",
     "empB 97.00 active",
     "empC 30.00 leave",
     "payroll_active TARGET 191.00"],
     "蓝宝石工资", "PAY"),
    ("v44h_06", "copper_ship", "ship_ok", 56.0,
     ["COPPER SHIP DOCK V44H",
     "box1 27 ok",
     "box2 15 ok",
     "box3 19 hold",
     "ship_ok TARGET 56"],
     "紫铜出库单", "SHIP"),
    ("v44h_07", "pewter_sla", "sla_ok_hours", 71.25,
     ["PEWTER SLA CARD V44H",
     "job1 38.00 hours ok",
     "job2 33.25 hours ok",
     "job3 18.00 hours late",
     "sla_ok_hours TARGET 71.25"],
     "白镴SLA卡", "SLA"),
    ("v44h_08", "willow_exp", "exp_sum", 90.5,
     ["WILLOW EXPENSE V44H",
     "e1 43.00",
     "e2 47.50",
     "e3 21.00 void",
     "exp_sum TARGET 90.50"],
     "柳木费用单", "EXP"),
    ("v44h_09", "mahogany_po", "po_open", 101.0,
     ["MAHOGANY PO SHEET V44H",
     "line1 54.00 open",
     "line2 47.00 open",
     "line3 24.00 closed",
     "po_open TARGET 101.00"],
     "红木采购单", "PO"),
    ("v44h_10", "silk_order", "order_paid", 121.25,
     ["SILK ORDER V44H",
     "skuA 65.00 paid",
     "skuB 56.25 paid",
     "skuC 18.00 due",
     "order_paid TARGET 121.25"],
     "丝绸订单", "ORD"),
    ("v44h_11", "basalt_dup", "dup_mark", 2.0,
     ["BASALT DUP MARK V44H",
     "markA 1",
     "markB 1",
     "markC 0",
     "dup_mark TARGET 2"],
     "玄武重复标", "DUP"),
    ("v44h_12", "ozone_zero", "zero_check", 0.0,
     ["OZONE AIR ZERO V44H",
     "z1 0.00",
     "z2 0.00",
     "z3 0.00",
     "zero_check TARGET 0.00"],
     "臭氧零值校验", "ZERO"),
    ("v44h_13", "teak_ledger", "ledger_net", 172.75,
     ["TEAK LEDGER V44H",
     "dr 84.00",
     "cr 88.75",
     "adj 28.00",
     "ledger_net TARGET 172.75"],
     "柚木账本", "LED"),
    ("v44h_14", "lacquer_ui", "ui_ok", 1.0,
     ["LACQUER UI SCAN V44H",
     "btnOK 1",
     "btnSkip 0",
     "btnBad 0",
     "ui_ok TARGET 1"],
     "漆面界面扫描", "UI"),
    ("v44h_15", "quartz_stack", "stack_count", 12.0,
     ["QUARTZ STACK V44H",
     "p1 5",
     "p2 4",
     "p3 3",
     "stack_count TARGET 12"],
     "石英堆叠单", "STK"),
    ("v44h_16", "parchment_fax", "fax_pages", 15.0,
     ["PARCHMENT FAX V44H",
     "pgA 8",
     "pgB 7",
     "pgC 4 drop",
     "fax_pages TARGET 15"],
     "羊皮传真页", "FAX"),
    ("v44h_17", "rivet_glare", "glare_ok", 1.0,
     ["RIVET GLARE V44H",
     "zone1 1 ok",
     "zone2 0",
     "zone3 0",
     "glare_ok TARGET 1"],
     "铆钉眩光卡", "GLR"),
    ("v44h_18", "canvas_tab", "tab_index", 22.0,
     ["CANVAS TAB INDEX V44H",
     "tabA 12",
     "tabB 10",
     "tabC 4",
     "tab_index TARGET 22"],
     "帆布页签索引", "TAB"),
]
'''

V44_OVERLAY = '''
    # --- V44 overlays (new vs V43) ---
    for _ in range(130):
        bx = rng.randint(50, 540)
        by = rng.randint(360, 590)
        if in_text_band(by):
            continue
        d.line([(bx, by), (bx + rng.randint(7, 28), by + rng.randint(-6, 6))], fill=(70, 55, 35), width=1)
    for gi in range(5):
        d.ellipse([56 + gi * 24, 320, 74 + gi * 24, 338], outline=(110, 70, 30), width=2)
    d.text((56, 340), "FLINT bait 44.44", fill=(70, 45, 20), font=f_tiny)
    for hi in range(4):
        d.polygon([(595 + hi * 34, 42), (621 + hi * 34, 42), (608 + hi * 34, 78)], fill=(20, 50, 140))
    d.text((595, 82), "SAPPHIRE bait 64.64", fill=(10, 30, 100), font=f_tiny)
    d.rectangle([265, 395, 425, 455], fill=(255, 250, 245))
    d.text((275, 415), "VELVET ghost 94.94", fill=(80, 40, 60), font=f_pen)
    d.arc([425, 385, 515, 455], 35, 260, fill=(140, 90, 40), width=3)
    d.text((425, 460), "BRONZE bait 39.39", fill=(100, 60, 20), font=f_tiny)
    d.ellipse([75, 485, 145, 545], fill=(170, 160, 140), outline=(80, 70, 55), width=2)
    d.text((75, 550), "TEAK bait 30.30", fill=(80, 55, 30), font=f_tiny)
    for qi in range(4):
        d.rectangle([265 + qi * 42, 485, 297 + qi * 42, 517], outline=(90, 70, 40), width=2)
    d.rectangle([865, 125, 1015, 185], fill=(200, 190, 170), outline=(70, 60, 45), width=2)
    d.text((885, 143), "COPPER", fill=(40, 25, 15), font=f_stamp)
    d.polygon([(40, 4), (420, 4), (405, 18), (50, 18)], fill=(220, 205, 180), outline=(110, 85, 50), width=1)
    d.text((70, 5), "CANVAS bait 74.74", fill=(55, 40, 25), font=f_tiny)
    for ti, ty in enumerate((105, 165, 225)):
        d.polygon([(1000, ty), (1024, ty + 12), (1000, ty + 24)], fill=(90, 70, 40 + ti * 20))
    # rivet row + canvas weave marks (V44-only)
    for ry in (110, 190, 270):
        d.ellipse([10, ry, 26, ry + 16], fill=(90, 90, 95), outline=(30, 30, 30), width=2)
        d.ellipse([14, ry + 4, 22, ry + 12], fill=(180, 180, 185))
    for (sx, sy) in [(170, 365), (350, 395), (490, 375)]:
        if not in_text_band(sy):
            d.rectangle([sx, sy, sx + 16, sy + 5], fill=(50, 40, 30))
'''

def replace_specs(text, new_specs):
    return re.sub(r"SPECS = \[.*?\]\n", new_specs + "\n", text, count=1, flags=re.S)

def bulk(text, pairs):
    for a, b in pairs:
        text = text.replace(a, b)
    return text

# Design
p = ROOT / "scripts/c371_vision_v44_design_and_batch.py"
t = p.read_text(encoding="utf-8")
t = replace_specs(t, SPECS_TRAIN)
t = bulk(t, [
    ("C365", "C371"),
    ("Vision V42 design", "Vision V44 design"),
    ("Vision V43 design", "Vision V44 design"),
    ("vs V43:", "vs V44:"),
    ("vision_images_v43", "vision_images_v44"),
    ("VL_GATE_V43_PROTOCOL", "VL_GATE_V44_PROTOCOL"),
    ("vision_v43_c365", "vision_v44_c371"),
    ("_v43c365", "_v44c371"),
    ("V43 keeps floor", "V44 keeps floor"),
    ('"version": "v43"', '"version": "v44"'),
    ("vision_v43_design_and_batch", "vision_v44_design_and_batch"),
    ("vl_gate_v43_claim", "vl_gate_v44_claim"),
    ("C365_VISION_V43_DESIGN", "C371_VISION_V44_DESIGN"),
    ("fixtures only; claim deferred to C347 VL smoke", "fixtures only; claim deferred to C372 VL smoke"),
    ("C365 design+fixtures; no VL claim", "C371 design+fixtures; no VL claim"),
    ("Ant VL Gate V42 Protocol", "Ant VL Gate V44 Protocol"),
    ("Harder than V40:", "Harder than V43:"),
    ("obsidian_denim_coral_indigo_jade_amber_nickel_moss_pine_opal_granite_void_cedar_enamel_resin_sage_terra_hazel",
     "flint_velvet_bronze_ivory_sapphire_copper_pewter_willow_mahogany_silk_basalt_ozone_teak_lacquer_quartz_parchment_rivet_canvas"),
    ("harder_than\": \"v41_basalt_velvet", "harder_than\": \"v43_marble_linen"),
    ("# --- V42 overlays (new vs V40) ---", "# --- V43 overlays (kept) ---"),
])
# Append V44 overlays before buf = io.BytesIO
if "# --- V44 overlays (new vs V43) ---" not in t:
    needle = "    buf = io.BytesIO()"
    if needle not in t:
        raise SystemExit("buf marker missing in design")
    t = t.replace(needle, V44_OVERLAY + "\n" + needle, 1)
# Fix docstring themes
t = re.sub(
    r'NEW themes vs V44:.*?\nCLARITY',
    "NEW themes vs V43: flint, velvet, bronze, ivory, sapphire, copper, pewter, willow,\n"
    "mahogany, silk, basalt, ozone, teak, lacquer, quartz, parchment, rivet, canvas.\nCLARITY",
    t, count=1, flags=re.S,
)
p.write_text(t, encoding="utf-8")
print("design ok", p.stat().st_size)

# Smoke
p = ROOT / "scripts/c372_vision_v44_smoke.py"
t = p.read_text(encoding="utf-8")
t = bulk(t, [
    ("C366", "C372"),
    ("Vision V42 real", "Vision V44 real"),
    ("Vision V43 real", "Vision V44 real"),
    ("Uses C359 fixtures", "Uses C371 fixtures"),
    ("vision_images_v43", "vision_images_v44"),
    ("vision_v43_c366", "vision_v44_c372"),
    ("vision_v43_smoke", "vision_v44_smoke"),
    ("vl_gate_v43_claim", "vl_gate_v44_claim"),
    ("C366_VISION_V43_SMOKE", "C372_VISION_V44_SMOKE"),
    ("C366b_VISION_GATE_V43_CLAIM", "C372b_VISION_GATE_V44_CLAIM"),
    ("vision_gate_v43_claim", "vision_gate_v44_claim"),
    ("r50plus_v43_teak_onyx_clarity_floor_n>=16_qwen35_2b", "r50plus_v44_flint_velvet_clarity_floor_n>=16_qwen35_2b"),
])
p.write_text(t, encoding="utf-8")
print("smoke ok")

# Heldout
p = ROOT / "scripts/c373_vision_v44_heldout.py"
t = p.read_text(encoding="utf-8")
t = replace_specs(t, SPECS_HELDOUT)
t = bulk(t, [
    ("C367", "C373"),
    ("Vision V42 heldout", "Vision V44 heldout"),
    ("Vision V43 heldout", "Vision V44 heldout"),
    ("from V42 train", "from V44 train"),
    ("(C365/C353)", "(C371)"),
    ("vision_images_v43h", "vision_images_v44h"),
    ("vision_v43h_c367", "vision_v44h_c373"),
    ("VL_GATE_V42_HELDOUT_PROTOCOL", "VL_GATE_V44_HELDOUT_PROTOCOL"),
    ("VL_GATE_V43_HELDOUT_PROTOCOL", "VL_GATE_V44_HELDOUT_PROTOCOL"),
    ("vision_images_v43", "vision_images_v44"),
    ("_v43c367", "_v44c373"),
    ("_v43hc367", "_v44hc373"),
    ("V43H", "V44H"),
    ("v43h_", "v44h_"),
    ("vision_v43_heldout", "vision_v44_heldout"),
    ("vl_gate_v43_heldout_claim", "vl_gate_v44_heldout_claim"),
    ("C367_VISION_V43_HELDOUT_SMOKE", "C373_VISION_V44_HELDOUT_SMOKE"),
    ("C367b_VISION_GATE_V43_HELDOUT_CLAIM", "C373b_VISION_GATE_V44_HELDOUT_CLAIM"),
    ("vision_gate_v43_heldout_claim", "vision_gate_v44_heldout_claim"),
    ("r50plus_v43_heldout_teak_onyx_n>=16_qwen35_2b_clarity_floor", "r50plus_v44_heldout_flint_velvet_n>=16_qwen35_2b_clarity_floor"),
    ("Disjoint from V33 train", "Disjoint from V44 train"),
])
# Fix hash seed if present
t = t.replace("_v43c365", "_v44c371").replace("hash(fid + \"_v43", "hash(fid + \"_v44")
if "# --- V44 overlays (new vs V43) ---" not in t and "buf = io.BytesIO()" in t:
    t = t.replace("    buf = io.BytesIO()", V44_OVERLAY + "\n    buf = io.BytesIO()", 1)
p.write_text(t, encoding="utf-8")
print("heldout ok", p.stat().st_size)

# U2C
p = ROOT / "scripts/c374_product_u2c_cost.py"
t = p.read_text(encoding="utf-8")
t = bulk(t, [
    ("C368", "C374"),
    ("vision_images_v43", "vision_images_v44"),
    ("product_u2c_c368", "product_u2c_c374"),
    ("missing_v43_manifest", "missing_v44_manifest"),
    ('"version": "v43"', '"version": "v44"'),
    ("C368_PRODUCT_U2C_COST", "C374_PRODUCT_U2C_COST"),
])
p.write_text(t, encoding="utf-8")
print("u2c ok")

# Regression
p = ROOT / "scripts/c375_capture_office_regression.py"
t = p.read_text(encoding="utf-8")
t = bulk(t, [
    ("C369", "C375"),
    ("capture_office_c369", "capture_office_c375"),
    ("C369_CAPTURE_OFFICE_REGRESSION", "C375_CAPTURE_OFFICE_REGRESSION"),
    ("vision_images_v43", "vision_images_v44"),
])
p.write_text(t, encoding="utf-8")
print("reg ok")

# Scorecard
p = ROOT / "scripts/c376_scorecard_and_stage.py"
t = p.read_text(encoding="utf-8")
t = bulk(t, [
    ("C370", "C376"),
    ("after C365-C369", "after C371-C375"),
    ("STAGE_ANT_C370.md", "STAGE_ANT_C376.md"),
    ("C366_VISION_V43_SMOKE", "C372_VISION_V44_SMOKE"),
    ("C366b_VISION_GATE_V43_CLAIM", "C372b_VISION_GATE_V44_CLAIM"),
    ("C367_VISION_V43_HELDOUT_SMOKE", "C373_VISION_V44_HELDOUT_SMOKE"),
    ("C367b_VISION_GATE_V43_HELDOUT_CLAIM", "C373b_VISION_GATE_V44_HELDOUT_CLAIM"),
    ("C360_VISION_V42_SMOKE", "C366_VISION_V43_SMOKE"),
    ("C361_VISION_V42_HELDOUT_SMOKE", "C367_VISION_V43_HELDOUT_SMOKE"),
    ("C368_PRODUCT_U2C_COST", "C374_PRODUCT_U2C_COST"),
    ("C369_CAPTURE_OFFICE_REGRESSION", "C375_CAPTURE_OFFICE_REGRESSION"),
    ("C370_SCORECARD_AND_STAGE", "C376_SCORECARD_AND_STAGE"),
    ("vl_gate_v43_claim", "vl_gate_v44_claim"),
    ("vl_gate_v43_heldout_claim", "vl_gate_v44_heldout_claim"),
])
# Rename v43/v42 local vars carefully - do after path renames
t = t.replace("v43 = float(c366", "v44 = float(c372")
t = t.replace("v43h = float(c367", "v44h = float(c373")
t = t.replace("v42 = float(c360", "v43 = float(c366")
t = t.replace("v42h = float(c361", "v43h = float(c367")
# Fix load var names
t = t.replace("c366 = load", "c372 = load")
t = t.replace("c366b = load", "c372b = load")
t = t.replace("c367 = load", "c373 = load")
t = t.replace("c367b = load", "c373b = load")
t = t.replace("c360 = load", "c366 = load")
t = t.replace("c361 = load", "c367 = load")
t = t.replace("c368 = load", "c374 = load")
t = t.replace("c369 = load", "c375 = load")
# Fix remaining references that used old names
for old, new in [
    ("c366b.get", "c372b.get"), ("c366.get", "c372.get"),
    ("c367b.get", "c373b.get"), ("c367.get", "c373.get"),
    ("c368.get", "c374.get"), ("c369.get", "c375.get"),
    ("v43_claim", "v44_claim"), ("v43h_claim", "v44h_claim"),
]:
    t = t.replace(old, new)
# Fix rate variable uses in parts - read file and check later
p.write_text(t, encoding="utf-8")
print("scorecard ok")
print("ALL PATCHED")
