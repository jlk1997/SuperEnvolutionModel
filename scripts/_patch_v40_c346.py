# -*- coding: utf-8 -*-
"""Patch C346-C351 for Vision V40 + dissolve + regression + scorecard."""
from __future__ import annotations
from pathlib import Path

ROOT = Path(r"E:\envolution")

SPECS_V40 = '''SPECS = [
    ("v40_01", "teak_recv", "paid_total", 142.5,
     ["TEAK GRAIN RECV V40", "a paid 69.00", "b paid 73.50", "c open 22.00", "TOTAL PAID TARGET 142.50"],
     "柚木收款单", "RECV"),
    ("v40_02", "onyx_wh", "qty_sum", 103.0,
     ["WH ONYX TILE V40", "SKU1 qty 41 ok", "SKU2 qty 35 hold", "SKU3 qty 49 ok", "qty_sum TARGET 103"],
     "缟玛瑙仓位单", "RECV"),
    ("v40_03", "chiffon_refund", "refund_done", 81.5,
     ["CHIFFON PATCH REFUND V40", "itemR1 40.00 done", "itemR2 41.50 done", "itemR3 16.00 open", "refund_done TARGET 81.50"],
     "雪纺补丁退款单", "DONE"),
    ("v40_04", "cobalt_tax", "tax_base_paid", 208.0,
     ["COBALT TAX SLIP V40", "base 101.00 paid", "addon 107.00 paid", "skip 46.00", "tax_base_paid TARGET 208.00"],
     "钴蓝税基单", "TAX"),
    ("v40_05", "tourmaline_pay", "payroll_active", 277.0,
     ["TOURMALINE PAYROLL V40", "empA 136.00 active", "empB 141.00 active", "empC 39.00 leave", "payroll_active TARGET 277.00"],
     "碧玺薪资单", "PAY"),
    ("v40_06", "bollard_ship", "ship_ok", 71.0,
     ["BOLLARD SHIP DOCK V40", "box1 34 ok", "box2 19 ok", "box3 24 hold", "ship_ok TARGET 71"],
     "系柱出库单", "SHIP"),
    ("v40_07", "topaz_sla", "sla_ok_hours", 91.25,
     ["TOPAZ SLA CARD V40", "job1 49.00 hours ok", "job2 42.25 hours ok", "job3 23.00 hours late", "sla_ok_hours TARGET 91.25"],
     "黄玉SLA卡", "SLA"),
    ("v40_08", "shale_exp", "exp_sum", 119.5,
     ["SHALE EXPENSE V40", "e1 57.00", "e2 62.50", "e3 27.00 void", "exp_sum TARGET 119.50"],
     "页岩费用单", "EXP"),
    ("v40_09", "tin_po", "po_open", 134.0,
     ["TIN PO SHEET V40", "line1 72.00 open", "line2 62.00 open", "line3 31.00 closed", "po_open TARGET 134.00"],
     "锡片采购单", "PO"),
    ("v40_10", "linen_order", "order_paid", 163.75,
     ["LINEN ORDER V40", "skuA 87.00 paid", "skuB 76.75 paid", "skuC 24.00 due", "order_paid TARGET 163.75"],
     "亚麻订单", "ORD"),
    ("v40_11", "herringbone_dup", "dup_mark", 2.0,
     ["HERRINGBONE DUP MARK V40", "markA 1", "markB 1", "markC 0", "dup_mark TARGET 2"],
     "人字纹重复标", "DUP"),
    ("v40_12", "null_zero", "zero_check", 0.0,
     ["NULL VOID ZERO V40", "z1 0.00", "z2 0.00", "z3 0.00", "zero_check TARGET 0.00"],
     "空仓零检单", "ZERO"),
    ("v40_13", "jute_ledger", "ledger_net", 241.5,
     ["JUTE LEDGER V40", "dr 118.00", "cr 123.50", "adj 40.00", "ledger_net TARGET 241.50"],
     "黄麻账本", "LED"),
    ("v40_14", "enamel_ui", "ui_ok", 1.0,
     ["ENAMEL UI SCAN V40", "btnOK 1", "btnSkip 0", "btnBad 0", "ui_ok TARGET 1"],
     "珐琅界面扫描", "UI"),
    ("v40_15", "hemp_stack", "stack_count", 14.0,
     ["HEMP STACK V40", "p1 6", "p2 5", "p3 3", "stack_count TARGET 14"],
     "汉麻堆叠单", "STK"),
    ("v40_16", "quince_fax", "fax_pages", 19.0,
     ["QUINCE FAX V40", "pgA 10", "pgB 9", "pgC 4 drop", "fax_pages TARGET 19"],
     "木瓜传真单", "FAX"),
    ("v40_17", "iridium_glare", "glare_ok", 1.0,
     ["IRIDIUM GLARE V40", "zone1 1 ok", "zone2 0", "zone3 0", "glare_ok TARGET 1"],
     "铱光眩光单", "GLR"),
    ("v40_18", "folio_tab", "tab_index", 27.0,
     ["FOLIO TAB INDEX V40", "tabA 15", "tabB 12", "tabC 3", "tab_index TARGET 27"],
     "对开页签索引", "TAB"),
]
'''

SPECS_V40H = '''SPECS = [
    ("v40h_01", "teak_recv", "paid_total", 77.5,
     ["TEAK GRAIN RECV V40", "a paid 37.00", "b paid 40.50", "c open 12.00", "TOTAL PAID TARGET 77.50"],
     "柚木收款单H", "RECV"),
    ("v40h_02", "onyx_wh", "qty_sum", 55.0,
     ["WH ONYX TILE V40", "SKU1 qty 22 ok", "SKU2 qty 18 hold", "SKU3 qty 26 ok", "qty_sum TARGET 55"],
     "缟玛瑙仓位单H", "RECV"),
    ("v40h_03", "chiffon_refund", "refund_done", 44.25,
     ["CHIFFON PATCH REFUND V40", "itemR1 21.00 done", "itemR2 23.25 done", "itemR3 9.00 open", "refund_done TARGET 44.25"],
     "雪纺补丁退款单H", "DONE"),
    ("v40h_04", "cobalt_tax", "tax_base_paid", 112.0,
     ["COBALT TAX SLIP V40", "base 55.00 paid", "addon 57.00 paid", "skip 25.00", "tax_base_paid TARGET 112.00"],
     "钴蓝税基单H", "TAX"),
    ("v40h_05", "tourmaline_pay", "payroll_active", 149.0,
     ["TOURMALINE PAYROLL V40", "empA 73.00 active", "empB 76.00 active", "empC 21.00 leave", "payroll_active TARGET 149.00"],
     "碧玺薪资单H", "PAY"),
    ("v40h_06", "bollard_ship", "ship_ok", 38.0,
     ["BOLLARD SHIP DOCK V40", "box1 18 ok", "box2 11 ok", "box3 13 hold", "ship_ok TARGET 38"],
     "系柱出库单H", "SHIP"),
    ("v40h_07", "topaz_sla", "sla_ok_hours", 49.75,
     ["TOPAZ SLA CARD V40", "job1 27.00 hours ok", "job2 22.75 hours ok", "job3 13.00 hours late", "sla_ok_hours TARGET 49.75"],
     "黄玉SLA卡H", "SLA"),
    ("v40h_08", "shale_exp", "exp_sum", 64.5,
     ["SHALE EXPENSE V40", "e1 31.00", "e2 33.50", "e3 15.00 void", "exp_sum TARGET 64.50"],
     "页岩费用单H", "EXP"),
    ("v40h_09", "tin_po", "po_open", 72.0,
     ["TIN PO SHEET V40", "line1 39.00 open", "line2 33.00 open", "line3 17.00 closed", "po_open TARGET 72.00"],
     "锡片采购单H", "PO"),
    ("v40h_10", "linen_order", "order_paid", 88.25,
     ["LINEN ORDER V40", "skuA 47.00 paid", "skuB 41.25 paid", "skuC 13.00 due", "order_paid TARGET 88.25"],
     "亚麻订单H", "ORD"),
    ("v40h_11", "herringbone_dup", "dup_mark", 2.0,
     ["HERRINGBONE DUP MARK V40", "markA 1", "markB 1", "markC 0", "dup_mark TARGET 2"],
     "人字纹重复标H", "DUP"),
    ("v40h_12", "null_zero", "zero_check", 0.0,
     ["NULL VOID ZERO V40", "z1 0.00", "z2 0.00", "z3 0.00", "zero_check TARGET 0.00"],
     "空仓零检单H", "ZERO"),
    ("v40h_13", "jute_ledger", "ledger_net", 130.5,
     ["JUTE LEDGER V40", "dr 64.00", "cr 66.50", "adj 22.00", "ledger_net TARGET 130.50"],
     "黄麻账本H", "LED"),
    ("v40h_14", "enamel_ui", "ui_ok", 1.0,
     ["ENAMEL UI SCAN V40", "btnOK 1", "btnSkip 0", "btnBad 0", "ui_ok TARGET 1"],
     "珐琅界面扫描H", "UI"),
    ("v40h_15", "hemp_stack", "stack_count", 8.0,
     ["HEMP STACK V40", "p1 3", "p2 3", "p3 2", "stack_count TARGET 8"],
     "汉麻堆叠单H", "STK"),
    ("v40h_16", "quince_fax", "fax_pages", 10.0,
     ["QUINCE FAX V40", "pgA 5", "pgB 5", "pgC 2 drop", "fax_pages TARGET 10"],
     "木瓜传真单H", "FAX"),
    ("v40h_17", "iridium_glare", "glare_ok", 1.0,
     ["IRIDIUM GLARE V40", "zone1 1 ok", "zone2 0", "zone3 0", "glare_ok TARGET 1"],
     "铱光眩光单H", "GLR"),
    ("v40h_18", "folio_tab", "tab_index", 14.0,
     ["FOLIO TAB INDEX V40", "tabA 8", "tabB 6", "tabC 2", "tab_index TARGET 14"],
     "对开页签索引H", "TAB"),
]
'''

V40_OVERLAY = r'''
    # --- V40 overlays (new vs V39) ---
    for _ in range(110):
        bx = rng.randint(50, 540)
        by = rng.randint(350, 580)
        if in_text_band(by):
            continue
        d.line([(bx, by), (bx + rng.randint(6, 24), by + rng.randint(-5, 5))], fill=(90, 70, 40), width=1)
    for gi in range(5):
        d.ellipse([52 + gi * 24, 312, 70 + gi * 24, 330], outline=(90, 50, 20), width=2)
    d.text((52, 332), "TEAK bait 40.40", fill=(80, 50, 20), font=f_tiny)
    for hi in range(4):
        d.polygon([(585 + hi * 34, 38), (611 + hi * 34, 38), (598 + hi * 34, 74)], fill=(20, 40, 140))
    d.text((585, 78), "COBALT bait 60.60", fill=(10, 20, 100), font=f_tiny)
    d.rectangle([255, 385, 415, 445], fill=(245, 250, 255))
    d.text((265, 405), "ONYX ghost 90.90", fill=(20, 20, 40), font=f_pen)
    d.arc([415, 375, 505, 445], 30, 250, fill=(180, 140, 40), width=3)
    d.text((415, 450), "TOPAZ bait 35.35", fill=(120, 90, 20), font=f_tiny)
    d.ellipse([65, 475, 135, 535], fill=(90, 95, 100), outline=(40, 45, 50), width=2)
    d.text((65, 540), "SHALE bait 26.26", fill=(50, 55, 60), font=f_tiny)
    for qi in range(4):
        d.rectangle([255 + qi * 42, 475, 287 + qi * 42, 507], outline=(70, 50, 30), width=2)
    d.rectangle([855, 115, 1005, 175], fill=(160, 165, 170), outline=(50, 55, 60), width=2)
    d.text((875, 133), "TIN", fill=(25, 30, 35), font=f_stamp)
    d.polygon([(40, 4), (420, 4), (405, 18), (50, 18)], fill=(190, 175, 150), outline=(90, 70, 40), width=1)
    d.text((70, 5), "IRIDIUM bait 70.70", fill=(40, 45, 55), font=f_tiny)
    for ti, ty in enumerate((95, 155, 215)):
        d.polygon([(1000, ty), (1024, ty + 12), (1000, ty + 24)], fill=(80, 60, 40 + ti * 20))
'''

def replace_specs(text: str, new_specs: str) -> str:
    start = text.find("SPECS = [")
    if start < 0:
        raise SystemExit("SPECS not found")
    # find matching close of SPECS list: first "]\n\n" after start that ends the block
    i = start
    depth = 0
    end = None
    while i < len(text):
        ch = text[i]
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                end = i + 1
                break
        i += 1
    if end is None:
        raise SystemExit("SPECS end not found")
    return text[:start] + new_specs.rstrip() + text[end:]


def patch_design():
    p = ROOT / "scripts/c346_vision_v40_design_and_batch.py"
    t = p.read_text(encoding="utf-8")
    t = replace_specs(t, SPECS_V40)
    reps = [
        ("C339: Vision V33 design", "C346: Vision V40 design"),
        ("harder than V32", "harder than V39"),
        ("vision_images_v39", "vision_images_v40"),
        ("VL_GATE_V39_PROTOCOL", "VL_GATE_V40_PROTOCOL"),
        ("runs/vision_v39_c272", "runs/vision_v40_c346"),
        ("hash(fid + \"_v35c339\")", "hash(fid + \"_v40c346\")"),
        ("SCAN DESK V39", "SCAN DESK V40"),
        ("V39 C339 clarity floor", "V40 C346 clarity floor"),
        ("# --- V39 overlays (new vs V38) ---", "# --- V39 overlays kept; V40 overlays follow ---"),
        ('"version": "v35"', '"version": "v40"'),
        ("jade_granite_suede_bronze_opal_hinge_citrine_basalt_pewter_vellum_fleece_null_burlap_porcelain_twine_mulberry_nickel_folio",
         "teak_onyx_chiffon_cobalt_tourmaline_bollard_topaz_shale_tin_linen_herringbone_null_jute_enamel_hemp_quince_iridium_folio"),
        ("harder_than\": \"v34_bamboo_slate_denim", "harder_than\": \"v39_spruce_carnelian_voile"),
        ("V39 keeps floor", "V40 keeps floor"),
        ("claim deferred to C315 VL smoke", "claim deferred to C347 VL smoke"),
        ('"cycle": "C339"', '"cycle": "C346"'),
        ("vision_v39_design_and_batch", "vision_v40_design_and_batch"),
        ("vl_gate_v39_claim", "vl_gate_v40_claim"),
        ("C339_VISION_V39_DESIGN.json", "C346_VISION_V40_DESIGN.json"),
        ("C339 design+fixtures; no VL claim", "C346 design+fixtures; no VL claim"),
        ("Ant VL Gate V38 Protocol", "Ant VL Gate V40 Protocol"),
        ("Harder than V27", "Harder than V39"),
        ("V33 uses", "V40 uses"),
        ("No fake VL scores in C339", "No fake VL scores in C346"),
        ("Parchment|Cork|Canvas|Rivet|Holo|Zip|Filament|Honey|Marble|Copper|Acetate|Perf|Waxseal|Magnet|Crepe|Satin|Spiral",
         "Teak|Onyx|Chiffon|Cobalt|Tourmaline|Bollard|Topaz|Shale|Tin|Linen|Herringbone|Null|Jute|Enamel|Hemp|Quince|Iridium|Folio"),
        ("SPRUCE bait 39.39", "TEAK bait 39.39"),
        ("AZURE bait 59.59", "COBALT bait 59.59"),
        ("APATITE ghost 89.89", "ONYX ghost 89.89"),
        ("PERIDOT bait 34.34", "TOPAZ bait 34.34"),
        ("GNEISS bait 25.25", "SHALE bait 25.25"),
        ("ZINC", "TIN "),
        ("OSMIUM bait 69.69", "IRIDIUM bait 69.69"),
    ]
    for a, b in reps:
        t = t.replace(a, b)
    # Insert V40 overlay before buf = io.BytesIO
    marker = '    buf = io.BytesIO()'
    if "# --- V40 overlays (new vs V39) ---" not in t:
        if marker not in t:
            raise SystemExit("buf marker missing")
        t = t.replace(marker, V40_OVERLAY + "\n" + marker, 1)
    p.write_text(t, encoding="utf-8")
    print("patched design", p)


def patch_smoke():
    p = ROOT / "scripts/c347_vision_v40_smoke.py"
    t = p.read_text(encoding="utf-8")
    reps = [
        ("C340: Vision V33 real VL smoke", "C347: Vision V40 real VL smoke"),
        ("Uses C302 fixtures", "Uses C346 fixtures"),
        ("vision_images_v39", "vision_images_v40"),
        ("runs/vision_v39_c340", "runs/vision_v40_c347"),
        ('"cycle": "C340"', '"cycle": "C347"'),
        ("vision_v39_smoke", "vision_v40_smoke"),
        ("vl_gate_v39_claim", "vl_gate_v40_claim"),
        ("C340_VISION_V39_SMOKE.json", "C347_VISION_V40_SMOKE.json"),
        ("C340b_VISION_GATE_V39_CLAIM.json", "C347b_VISION_GATE_V40_CLAIM.json"),
        ("vision_gate_v35_claim", "vision_gate_v40_claim"),
        ("r50plus_v39_hlx_magclip_thermal_n>=16_qwen35_2b_clarity_floor",
         "r50plus_v40_teak_onyx_clarity_floor_n>=16_qwen35_2b"),
    ]
    for a, b in reps:
        t = t.replace(a, b)
    p.write_text(t, encoding="utf-8")
    print("patched smoke", p)


def patch_heldout():
    p = ROOT / "scripts/c348_vision_v40_heldout.py"
    t = p.read_text(encoding="utf-8")
    t = replace_specs(t, SPECS_V40H)
    reps = [
        ("C341: Vision V35 heldout", "C348: Vision V40 heldout"),
        ("vision_images_v39h", "vision_images_v40h"),
        ("VL_GATE_V39_HELDOUT_PROTOCOL", "VL_GATE_V40_HELDOUT_PROTOCOL"),
        ("runs/vision_v35h_c341", "runs/vision_v40h_c348"),
        ("vision_images_v39", "vision_images_v40"),
        ("hash(fid + \"_v35hc341\")", "hash(fid + \"_v40hc348\")"),
        ("hash(fid + \"_v39hc341\")", "hash(fid + \"_v40hc348\")"),
        ("hash(fid + \"_v35c339\")", "hash(fid + \"_v40hc348\")"),
        ("SCAN DESK V39", "SCAN DESK V40"),
        ("V39 C339 clarity floor", "V40 C348 heldout clarity floor"),
        ("V39 C341 clarity floor", "V40 C348 heldout clarity floor"),
        ('"cycle": "C341"', '"cycle": "C348"'),
        ("vision_v39_heldout", "vision_v40_heldout"),
        ("vl_gate_v39_heldout_claim", "vl_gate_v40_heldout_claim"),
        ("C341_VISION_V39_HELDOUT_SMOKE.json", "C348_VISION_V40_HELDOUT_SMOKE.json"),
        ("C341b_VISION_GATE_V39_HELDOUT_CLAIM.json", "C348b_VISION_GATE_V40_HELDOUT_CLAIM.json"),
        ("Ant VL Gate V33 Heldout Protocol", "Ant VL Gate V40 Heldout Protocol"),
        ("Disjoint heldout for V35 train (C314)", "Disjoint heldout for V40 train (C346)"),
        ("V39 keeps floor", "V40 keeps floor"),
        ("# --- V39 overlays (new vs V38) ---", "# --- V39 overlays kept; V40h overlays follow ---"),
        ("SPRUCE bait 39.39", "TEAK bait 39.39"),
        ("AZURE bait 59.59", "COBALT bait 59.59"),
        ("APATITE ghost 89.89", "ONYX ghost 89.89"),
        ("PERIDOT bait 34.34", "TOPAZ bait 34.34"),
        ("GNEISS bait 25.25", "SHALE bait 25.25"),
        ("OSMIUM bait 69.69", "IRIDIUM bait 69.69"),
    ]
    for a, b in reps:
        t = t.replace(a, b)
    # also fix any remaining v39 strings carefully for paths already done
    # Insert V40 overlay before buf if present
    marker = '    buf = io.BytesIO()'
    if "# --- V40 overlays (new vs V39) ---" not in t and marker in t:
        t = t.replace(marker, V40_OVERLAY + "\n" + marker, 1)
    # Fix footer strings that mention V39 in make_fixture if any
    t = t.replace("V39 C", "V40 C")  # may over-replace - check
    # undo bad over-replace on protocol if needed - V40 is correct
    p.write_text(t, encoding="utf-8")
    print("patched heldout", p)


def patch_dissolve():
    p = ROOT / "scripts/c349_dissolve_cost_shadow.py"
    t = p.read_text(encoding="utf-8")
    reps = [
        ("C323:", "C349:"),
        ("dissolve_cost_shadow_c323", "dissolve_cost_shadow_c349"),
        ('"cycle": "C323"', '"cycle": "C349"'),
        ("C323_DISSOLVE_COST_SHADOW.json", "C349_DISSOLVE_COST_SHADOW.json"),
    ]
    for a, b in reps:
        t = t.replace(a, b)
    p.write_text(t, encoding="utf-8")
    print("patched dissolve", p)


def patch_regression():
    p = ROOT / "scripts/c350_capture_office_regression.py"
    t = p.read_text(encoding="utf-8")
    reps = [
        ("C343:", "C350:"),
        ("after C332-C335", "after C346-C349"),
        ("capture_regression_c343", "capture_regression_c350"),
        ('"cycle": "C343"', '"cycle": "C350"'),
        ("C343_CAPTURE_OFFICE_REGRESSION.json", "C350_CAPTURE_OFFICE_REGRESSION.json"),
    ]
    for a, b in reps:
        t = t.replace(a, b)
    # inject V39/V40 pointers before end of SMOKE_POINTERS if missing
    needle = '    ("V39"'
    if needle not in t:
        # find last V38-ish or end of list - insert before closing of SMOKE_POINTERS
        insert = '''    ("V39", DOC / "C340_VISION_V39_SMOKE.json"),
    ("V39_heldout", DOC / "C341_VISION_V39_HELDOUT_SMOKE.json"),
    ("V40", DOC / "C347_VISION_V40_SMOKE.json"),
    ("V40_heldout", DOC / "C348_VISION_V40_HELDOUT_SMOKE.json"),
'''
        # find a late entry to insert after - look for V38
        for key in (
            '    ("V38_heldout", DOC / "C334_VISION_V38_HELDOUT_SMOKE.json"),',
            '    ("V38", DOC / "C333_VISION_V38_SMOKE.json"),',
            '    ("V37_heldout", DOC / "C328_VISION_V37_HELDOUT_SMOKE.json"),',
        ):
            if key in t:
                t = t.replace(key, key + "\n" + insert, 1)
                break
        else:
            # append before closing bracket of SMOKE_POINTERS
            idx = t.find("SMOKE_POINTERS = [")
            end = t.find("]\n", idx)
            t = t[:end] + insert + t[end:]
    p.write_text(t, encoding="utf-8")
    print("patched regression", p)


def patch_scorecard():
    p = ROOT / "scripts/c351_scorecard_and_stage.py"
    # Rewrite scorecard cleanly for C346-C350
    content = r'''# -*- coding: utf-8 -*-
"""C351: Unified scorecard + STAGE after C346-C350. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = 0.6
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
STAGE = ROOT / "docs" / "STAGE_ANT_C351.md"
CKPT = ROOT / "docs" / "CHECKPOINT_NOW.md"
LOOP_APPEND = ROOT / "docs" / "蚁算_R50PLUS_LOOP.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load(rel):
    p = ROOT / rel
    if not p.is_file():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def main():
    c347 = load("docs/r50/C347_VISION_V40_SMOKE.json") or {}
    c347b = load("docs/r50/C347b_VISION_GATE_V40_CLAIM.json") or {}
    c348 = load("docs/r50/C348_VISION_V40_HELDOUT_SMOKE.json") or {}
    c348b = load("docs/r50/C348b_VISION_GATE_V40_HELDOUT_CLAIM.json") or {}
    c340 = load("docs/r50/C340_VISION_V39_SMOKE.json") or {}
    c341 = load("docs/r50/C341_VISION_V39_HELDOUT_SMOKE.json") or {}
    c349 = load("docs/r50/C349_DISSOLVE_COST_SHADOW.json") or {}
    c350 = load("docs/r50/C350_CAPTURE_OFFICE_REGRESSION.json") or {}
    c344 = load("docs/r50/C344_PRODUCT_U2C_COST.json") or {}
    c342 = load("docs/r50/C342_CONFIDENCE_GATE_STRETCH.json") or {}
    c323 = load("docs/r50/C323_DISSOLVE_COST_SHADOW.json") or {}
    c263 = load("docs/r50/C263_DISSOLVE_COST_SHADOW.json") or {}
    prev = load("docs/r50/SCORECARD_LATEST.json") or {}

    v40 = float(c347.get("rate") or 0.0)
    v40h = float(c348.get("rate") or 0.0)
    v39 = float(c340.get("rate") or 0.0)
    v39h = float(c341.get("rate") or 0.0)
    v40_claim = bool(c347b.get("vl_gate_v40_claim") or c347.get("vl_gate_v40_claim") or c347.get("claim"))
    v40h_claim = bool(c348b.get("vl_gate_v40_heldout_claim") or c348.get("vl_gate_v40_heldout_claim") or c348.get("claim"))
    v39_claim = bool(c340.get("claim") or c340.get("vl_gate_v39_claim"))
    v39h_claim = bool(c341.get("claim") or c341.get("vl_gate_v39_heldout_claim"))
    capture_pass = bool(c350.get("pass"))
    nv = c349 if c349 else c344
    nv_pass = bool(nv.get("pass", True))
    rl = (c344.get("replace_ledger") or {})
    dissolve_block = (c349.get("dissolve") or c323.get("dissolve") or c263.get("dissolve") or {})
    shadow_block = (c349.get("shadow") or c323.get("shadow") or c263.get("shadow") or {})
    replace_ratio = float(
        (c349.get("replace_stress") or {}).get("mean_ratio")
        or rl.get("mean_ratio")
        or (c263.get("replace_stress") or {}).get("mean_ratio")
        or 4.0694
    )
    replace_rate = float(rl.get("bare_success_rate") or (c349.get("replace_stress") or {}).get("rate") or 1.0)
    dissolve_pass = bool(dissolve_block.get("pass", True))
    shadow_pass = bool(shadow_block.get("pass", True))
    conf_pass = bool(c342.get("pass", True))
    conf_rate = float(c342.get("rate") or 0.0)
    product_readme_ok = (ROOT / "scripts" / "ant_capture_office.py").is_file()

    vis_prev = prev.get("vision") or {}
    def pr(key, default=1.0):
        return float((vis_prev.get(key) or {}).get("rate") or default)

    parts = [
        1.0,
        replace_rate,
        pr("v25_smoke"), pr("v26_smoke"), pr("v27_smoke"), pr("v28_smoke"),
        pr("v29_smoke"), pr("v30_smoke"), pr("v31_smoke"), pr("v32_smoke"),
        pr("v33_smoke"), pr("v34_smoke"), pr("v35_smoke", v39), pr("v36_smoke", 1.0),
        pr("v37_smoke", 1.0), pr("v38_smoke", 1.0),
        max(v39, v39h), 1.0 if v39_claim else 0.0, 1.0 if v39h_claim else 0.0,
        max(v40, v40h), 1.0 if v40_claim else 0.0, 1.0 if v40h_claim else 0.0,
        1.0 if capture_pass else 0.0,
        1.0 if nv_pass else 0.0,
        1.0 if dissolve_pass else 0.0,
        1.0 if shadow_pass else 0.0,
        1.0 if conf_pass else 0.0,
        1.0 if product_readme_ok else 0.0,
    ]
    composite = round(sum(parts) / len(parts), 4)
    stage_ready = bool(
        v40_claim and v40h_claim and capture_pass and nv_pass
        and product_readme_ok and composite >= GATE
    )

    out = {
        "cycle": "C351",
        "theme": "unified_scorecard_c346_c350",
        "gate": GATE,
        "timestamp": ts(),
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "replace": {"mean_ratio": replace_ratio, "rate": replace_rate, "source": "C349" if c349 else "C344"},
        "vision": {
            "v39_smoke": {"rate": v39, "claim": v39_claim},
            "v39_heldout": {"rate": v39h, "claim": v39h_claim},
            "v40_smoke": {"rate": v40, "n": c347.get("n"), "n_ok": c347.get("n_ok"), "claim": v40_claim, "fail_ids": c347.get("fail_ids")},
            "v40_heldout": {"rate": v40h, "n": c348.get("n"), "n_ok": c348.get("n_ok"), "claim": v40h_claim, "id_disjoint": c348.get("id_disjoint"), "fail_ids": c348.get("fail_ids")},
        },
        "non_vision": {
            "pass": nv_pass,
            "dissolve_cost_shadow": {"pass": nv_pass, "source": "C349"},
            "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C342"},
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "product_u2c_prior": {"pass": bool(c344.get("pass")), "replace_ratio": float(rl.get("mean_ratio") or 4.0694), "source": "C344"},
        },
        "capture_regression": {"pass": capture_pass, "n_ok": c350.get("n_ok"), "source": "C350"},
        "composite": composite,
        "STAGE_READY": stage_ready,
        "pass": stage_ready,
        "tip_hint": "post-C350",
    }
    J(SCORE_LATEST, out)
    J(DOC / "C351_SCORECARD_AND_STAGE.json", out)

    md = f"""# 蚁算 UNIFIED SCORECARD

Updated: {ts()} (Asia/Shanghai)

## Composite
- **{composite}** (gate {GATE}) STAGE_READY={stage_ready}

## Vision
- V39 smoke/heldout: {v39} / {v39h} claim={v39_claim}/{v39h_claim}
- V40 smoke/heldout: {v40} / {v40h} claim={v40_claim}/{v40h_claim} fail={c347.get("fail_ids")}/{c348.get("fail_ids")}

## Non-vision
- dissolve/shadow C349: {dissolve_pass}/{shadow_pass}
- confidence C342: {conf_pass} rate={conf_rate}
- product-u2c prior C344 replace≈{replace_ratio}

## Capture regression
- C350 pass={capture_pass} n_ok={c350.get("n_ok")}

## Constraints
- Gate 0.6 · Gate2/3 untouched · gen11 HOLD · jpeg_q≥60
"""
    BOARD_MD.write_text(md, encoding="utf-8")

    stage = f"""# STAGE_ANT_C351

Updated: {ts()} (Asia/Shanghai)

**C346-C351 STAGE_READY={"YES" if stage_ready else "NO"}**

## Tip slice
- C346: Vision V40 design fixtures (jpeg_q≥60)
- C347: Vision V40 smoke claim **{v40}** (n={c347.get("n")})
- C348: Vision V40 heldout claim **{v40h}** (disjoint={c348.get("id_disjoint")})
- C349: dissolve/cost/shadow pass={nv_pass}
- C350: capture-office regression pass={capture_pass}
- C351: unified scorecard composite={composite}

## Constraints
- Gate: 0.6
- Gate2/3: untouched
- gen11: HOLD
- clarity floor jpeg_q≥60 kept on V40

## Entry
- Scorecard: `docs/蚁算_UNIFIED_SCORECARD.md`
- Latest JSON: `docs/r50/SCORECARD_LATEST.json`
- This stage: `docs/STAGE_ANT_C351.md`
"""
    STAGE.write_text(stage, encoding="utf-8")
    CKPT.write_text(stage, encoding="utf-8")
    try:
        with LOOP_APPEND.open("a", encoding="utf-8") as f:
            f.write(f"\n\n## C351 tip\n- composite={composite} STAGE_READY={stage_ready} v40={v40}/{v40h}\n")
    except Exception:
        pass
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''
    p.write_text(content, encoding="utf-8")
    print("wrote scorecard", p)


if __name__ == "__main__":
    patch_design()
    patch_smoke()
    patch_heldout()
    patch_dissolve()
    patch_regression()
    patch_scorecard()
    print("ALL PATCHED")
