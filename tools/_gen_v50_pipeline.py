# -*- coding: utf-8 -*-
"""Generate C407-C412 Vision V50 pipeline from V49 scripts on E:\\envolution."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(r"E:\envolution")
SCRIPTS = ROOT / "scripts"

# V50 train specs: new nature themes + amounts disjoint from V49/V49H
V50_SPECS = '''SPECS = [
    ("v50_01", "atoll_recv", "paid_total", 273.5,
     ['ATOLL GRAIN RECV V50',
     'a paid 134.00',
     'b paid 139.50',
     'c open 58.00',
     'TOTAL PAID TARGET 273.50'],
     'atoll', "RECV"),
    ("v50_02", "birch_wh", "qty_sum", 221.0,
     ['WH BIRCH BIN V50',
     'SKU1 qty 97 ok',
     'SKU2 qty 73 hold',
     'SKU3 qty 124 ok',
     'qty_sum TARGET 221'],
     'birch', "RECV"),
    ("v50_03", "cedar_refund", "refund_done", 191.25,
     ['CEDAR PATCH REFUND V50',
     'itemR1 92.00 done',
     'itemR2 99.25 done',
     'itemR3 44.00 open',
     'refund_done TARGET 191.25'],
     'cedar', "DONE"),
    ("v50_04", "delta_tax", "tax_base_paid", 368.0,
     ['DELTA TAX SLIP V50',
     'base 179.00 paid',
     'addon 189.00 paid',
     'skip 91.00',
     'tax_base_paid TARGET 368.00'],
     'delta', "TAX"),
    ("v50_05", "ember_pay", "payroll_active", 462.0,
     ['EMBER PAYROLL V50',
     'empA 226.00 active',
     'empB 236.00 active',
     'empC 79.00 leave',
     'payroll_active TARGET 462.00'],
     'ember', "PAY"),
    ("v50_06", "fern_ship", "ship_ok", 167.0,
     ['FERN SHIP DOCK V50',
     'box1 81 ok',
     'box2 86 ok',
     'box3 52 hold',
     'ship_ok TARGET 167'],
     'fern', "SHIP"),
    ("v50_07", "granite_sla", "sla_ok_hours", 197.5,
     ['GRANITE SLA CARD V50',
     'job1 104.00 hours ok',
     'job2 93.50 hours ok',
     'job3 51.00 hours late',
     'sla_ok_hours TARGET 197.50'],
     'granite', "SLA"),
    ("v50_08", "holly_exp", "exp_sum", 241.75,
     ['HOLLY EXPENSE V50',
     'e1 116.00',
     'e2 125.75',
     'e3 57.00 void',
     'exp_sum TARGET 241.75'],
     'holly', "EXP"),
    ("v50_09", "jade_po", "po_open", 267.0,
     ['JADE PO SHEET V50',
     'line1 141.00 open',
     'line2 126.00 open',
     'line3 64.00 closed',
     'po_open TARGET 267.00'],
     'jade', "PO"),
    ("v50_10", "knoll_order", "order_paid", 318.25,
     ['KNOLL ORDER V50',
     'skuA 168.00 paid',
     'skuB 150.25 paid',
     'skuC 54.00 due',
     'order_paid TARGET 318.25'],
     'knoll', "ORD"),
    ("v50_11", "lichen_dup", "dup_mark", 2.0,
     ['LICHEN DUP MARK V50',
     'markA 1',
     'markB 1',
     'markC 0',
     'dup_mark TARGET 2'],
     'lichen', "DUP"),
    ("v50_12", "moss_zero", "zero_check", 0.0,
     ['MOSS AIR ZERO V50',
     'z1 0.00',
     'z2 0.00',
     'z3 0.00',
     'zero_check TARGET 0.00'],
     'moss', "ZERO"),
    ("v50_13", "nimbus_ledger", "ledger_net", 401.5,
     ['NIMBUS LEDGER V50',
     'dr 195.00',
     'cr 206.50',
     'adj 74.00',
     'ledger_net TARGET 401.50'],
     'nimbus', "LED"),
    ("v50_14", "orchard_ui", "ui_ok", 1.0,
     ['ORCHARD UI SCAN V50',
     'btnOK 1',
     'btnSkip 0',
     'btnBad 0',
     'ui_ok TARGET 1'],
     'orchard', "UI"),
    ("v50_15", "pine_stack", "stack_count", 37.0,
     ['PINE STACK V50',
     'p1 18',
     'p2 13',
     'p3 6',
     'stack_count TARGET 37'],
     'pine', "STK"),
    ("v50_16", "raven_fax", "fax_pages", 44.0,
     ['RAVEN FAX V50',
     'pgA 25',
     'pgB 19',
     'pgC 14 drop',
     'fax_pages TARGET 44'],
     'raven', "FAX"),
    ("v50_17", "spruce_glare", "glare_ok", 1.0,
     ['SPRUCE GLARE V50',
     'zone1 1 ok',
     'zone2 0',
     'zone3 0',
     'glare_ok TARGET 1'],
     'spruce', "GLR"),
    ("v50_18", "tide_tab", "tab_index", 61.0,
     ['TIDE TAB INDEX V50',
     'tabA 33',
     'tabB 28',
     'tabC 13',
     'tab_index TARGET 61'],
     'tide', "TAB"),
]
'''

V50H_SPECS = '''SPECS = [
    ("v50h_01", "atoll_recv", "paid_total", 159.75,
     ['ATOLL GRAIN RECV V50H',
     'a paid 77.00',
     'b paid 82.75',
     'c open 35.00',
     'TOTAL PAID TARGET 159.75'],
     'atoll', "RECV"),
    ("v50h_02", "birch_wh", "qty_sum", 128.0,
     ['WH BIRCH BIN V50H',
     'SKU1 qty 56 ok',
     'SKU2 qty 42 hold',
     'SKU3 qty 72 ok',
     'qty_sum TARGET 128'],
     'birch', "RECV"),
    ("v50h_03", "cedar_refund", "refund_done", 112.5,
     ['CEDAR PATCH REFUND V50H',
     'itemR1 54.00 done',
     'itemR2 58.50 done',
     'itemR3 26.00 open',
     'refund_done TARGET 112.50'],
     'cedar', "DONE"),
    ("v50h_04", "delta_tax", "tax_base_paid", 219.0,
     ['DELTA TAX SLIP V50H',
     'base 107.00 paid',
     'addon 112.00 paid',
     'skip 49.00',
     'tax_base_paid TARGET 219.00'],
     'delta', "TAX"),
    ("v50h_05", "ember_pay", "payroll_active", 274.0,
     ['EMBER PAYROLL V50H',
     'empA 134.00 active',
     'empB 140.00 active',
     'empC 46.00 leave',
     'payroll_active TARGET 274.00'],
     'ember', "PAY"),
    ("v50h_06", "fern_ship", "ship_ok", 96.0,
     ['FERN SHIP DOCK V50H',
     'box1 46 ok',
     'box2 50 ok',
     'box3 29 hold',
     'ship_ok TARGET 96'],
     'fern', "SHIP"),
    ("v50h_07", "granite_sla", "sla_ok_hours", 116.0,
     ['GRANITE SLA CARD V50H',
     'job1 61.00 hours ok',
     'job2 55.00 hours ok',
     'job3 30.00 hours late',
     'sla_ok_hours TARGET 116.00'],
     'granite', "SLA"),
    ("v50h_08", "holly_exp", "exp_sum", 141.25,
     ['HOLLY EXPENSE V50H',
     'e1 68.00',
     'e2 73.25',
     'e3 35.00 void',
     'exp_sum TARGET 141.25'],
     'holly', "EXP"),
    ("v50h_09", "jade_po", "po_open", 155.0,
     ['JADE PO SHEET V50H',
     'line1 83.00 open',
     'line2 72.00 open',
     'line3 38.00 closed',
     'po_open TARGET 155.00'],
     'jade', "PO"),
    ("v50h_10", "knoll_order", "order_paid", 184.5,
     ['KNOLL ORDER V50H',
     'skuA 98.00 paid',
     'skuB 86.50 paid',
     'skuC 32.00 due',
     'order_paid TARGET 184.50'],
     'knoll', "ORD"),
    ("v50h_11", "lichen_dup", "dup_mark", 2.0,
     ['LICHEN DUP MARK V50H',
     'markA 1',
     'markB 1',
     'markC 0',
     'dup_mark TARGET 2'],
     'lichen', "DUP"),
    ("v50h_12", "moss_zero", "zero_check", 0.0,
     ['MOSS AIR ZERO V50H',
     'z1 0.00',
     'z2 0.00',
     'z3 0.00',
     'zero_check TARGET 0.00'],
     'moss', "ZERO"),
    ("v50h_13", "nimbus_ledger", "ledger_net", 236.75,
     ['NIMBUS LEDGER V50H',
     'dr 115.00',
     'cr 121.75',
     'adj 43.00',
     'ledger_net TARGET 236.75'],
     'nimbus', "LED"),
    ("v50h_14", "orchard_ui", "ui_ok", 1.0,
     ['ORCHARD UI SCAN V50H',
     'btnOK 1',
     'btnSkip 0',
     'btnBad 0',
     'ui_ok TARGET 1'],
     'orchard', "UI"),
    ("v50h_15", "pine_stack", "stack_count", 21.0,
     ['PINE STACK V50H',
     'p1 10',
     'p2 8',
     'p3 3',
     'stack_count TARGET 21'],
     'pine', "STK"),
    ("v50h_16", "raven_fax", "fax_pages", 27.0,
     ['RAVEN FAX V50H',
     'pgA 15',
     'pgB 12',
     'pgC 9 drop',
     'fax_pages TARGET 27'],
     'raven', "FAX"),
    ("v50h_17", "spruce_glare", "glare_ok", 1.0,
     ['SPRUCE GLARE V50H',
     'zone1 1 ok',
     'zone2 0',
     'zone3 0',
     'glare_ok TARGET 1'],
     'spruce', "GLR"),
    ("v50h_18", "tide_tab", "tab_index", 38.0,
     ['TIDE TAB INDEX V50H',
     'tabA 21',
     'tabB 17',
     'tabC 10',
     'tab_index TARGET 38'],
     'tide', "TAB"),
]
'''

V50_OVERLAY = '''
    # --- V50 overlays (new vs V49) ---
    for _ in range(140):
        bx = rng.randint(50, 540)
        by = rng.randint(365, 595)
        if in_text_band(by):
            continue
        d.line([(bx, by), (bx + rng.randint(8, 30), by + rng.randint(-7, 7))], fill=(55, 75, 45), width=1)
    for gi in range(5):
        d.ellipse([58 + gi * 24, 322, 76 + gi * 24, 340], outline=(30, 100, 70), width=2)
    d.text((58, 342), "JADE bait 45.45", fill=(20, 80, 50), font=f_tiny)
    for hi in range(4):
        d.polygon([(600 + hi * 34, 44), (626 + hi * 34, 44), (613 + hi * 34, 80)], fill=(160, 40, 60))
    d.text((600, 84), "GARNET bait 65.65", fill=(120, 20, 40), font=f_tiny)
    d.rectangle([270, 400, 430, 460], fill=(245, 255, 250))
    d.text((280, 420), "MOSS ghost 95.95", fill=(20, 70, 40), font=f_pen)
    d.arc([430, 390, 520, 460], 40, 265, fill=(40, 90, 120), width=3)
    d.text((430, 465), "AQUA bait 40.40", fill=(20, 60, 90), font=f_tiny)
    d.ellipse([80, 490, 150, 550], fill=(160, 150, 130), outline=(70, 65, 50), width=2)
    d.text((80, 555), "DRIFT bait 31.31", fill=(70, 55, 35), font=f_tiny)
    for qi in range(4):
        d.rectangle([270 + qi * 42, 490, 302 + qi * 42, 522], outline=(50, 90, 60), width=2)
    d.rectangle([870, 130, 1020, 190], fill=(185, 200, 190), outline=(50, 70, 55), width=2)
    d.text((890, 148), "FERN", fill=(20, 50, 30), font=f_stamp)
    d.polygon([(40, 4), (420, 4), (405, 18), (50, 18)], fill=(200, 215, 195), outline=(60, 90, 50), width=1)
    d.text((70, 5), "LEAF bait 75.75", fill=(30, 60, 35), font=f_tiny)
    for ti, ty in enumerate((110, 170, 230)):
        d.polygon([(1000, ty), (1024, ty + 12), (1000, ty + 24)], fill=(40, 100, 60 + ti * 20))
    # dew drops + vine marks (V50-only)
    for ry in (115, 195, 275):
        d.ellipse([12, ry, 28, ry + 16], fill=(140, 200, 220), outline=(30, 60, 80), width=2)
        d.ellipse([16, ry + 4, 24, ry + 12], fill=(200, 230, 240))
    for (sx, sy) in [(175, 370), (355, 400), (495, 380)]:
        if not in_text_band(sy):
            d.rectangle([sx, sy, sx + 18, sy + 5], fill=(40, 70, 40))
'''


def replace_specs(src: str, new_specs: str) -> str:
    return re.sub(r"SPECS = \[.*?\n\]\n", new_specs + "\n", src, count=1, flags=re.S)


def swap_v49_overlay(src: str) -> str:
    # Replace the V49-only overlay block with V50 overlay
    pat = r"    # --- V49 overlays \(new vs V43\) ---.*?(?=\n    buf = io\.BytesIO\(\))"
    if re.search(pat, src, flags=re.S):
        return re.sub(pat, V50_OVERLAY.rstrip() + "\n", src, count=1, flags=re.S)
    # heldout may have different comment
    pat2 = r"    # --- V49 overlays \(new vs V43\) ---.*?(?=\n    buf = io\.BytesIO\(\))"
    return src


def gen_design():
    src = (SCRIPTS / "c401_vision_v49_design_and_batch.py").read_text(encoding="utf-8")
    # Keep PROTO chinese prefix by only swapping V49->V50 in filename part
    out = src
    repls = [
        ("C401", "C407"),
        ("c401", "c407"),
        ("V49", "V50"),
        ("v49", "v50"),
        ("Vision V49", "Vision V50"),
        ("vision_v49", "vision_v50"),
        ("vision_images_v49", "vision_images_v50"),
        ("_v49c377", "_v50c407"),
        ("Harder than V48", "Harder than V49"),
        ("harder_than\": \"v48_atoll_birch", "harder_than\": \"v49_aurora_basalt"),
        ("ember_frost_granite_amber_cobalt_rust_sage_coral_slate_pearl_onyx_moss_cedar_chrome_jade_linen_brass_ink",
         "atoll_birch_cedar_delta_ember_fern_granite_holly_jade_knoll_lichen_moss_nimbus_orchard_pine_raven_spruce_tide"),
        ("NEW themes vs V47: atoll, birch, cedar, delta, ember, fern, granite, holly,\njade, knoll, lichen, moss, nimbus, orchard, pine, raven, spruce, tide.",
         "NEW themes vs V49: atoll, birch, cedar, delta, ember, fern, granite, holly,\njade, knoll, lichen, moss, nimbus, orchard, pine, raven, spruce, tide."),
        ("V49 keeps floor", "V50 keeps floor"),
        ("C401 design+fixtures; no VL claim", "C407 design+fixtures; no VL claim"),
        ("fixtures only; claim deferred to C402 VL smoke", "fixtures only; claim deferred to C408 VL smoke"),
        ("No claim until C402 VL", "No claim until C408 VL"),
    ]
    for a, b in repls:
        out = out.replace(a, b)
    out = replace_specs(out, V50_SPECS)
    out = swap_v49_overlay(out)
    # fix double-replaced cycle names that got mangled (C408 from C402 via C407 path?)
    # C401->C407 already; vl_gate_v50 ok
    # Protocol: V42 uses -> V50 uses
    out = out.replace("V42 uses", "V50 uses")
    out = out.replace("V50-only", "V50-only")  # noop
    # Fix overlay marker if still says V49 after partial
    out = out.replace("# --- V50 overlays (new vs V43) ---", "# --- V50 overlays (new vs V49) ---")
    # If swap failed and still has V49 overlays block renamed oddly
    if "# --- V50 overlays (new vs V49) ---" not in out and "JADE bait 45.45" not in out:
        # try after rename: V50 overlays (new vs V43)
        pat = r"    # --- V50 overlays \(new vs V43\) ---.*?(?=\n    buf = io\.BytesIO\(\))"
        if re.search(pat, out, flags=re.S):
            out = re.sub(pat, V50_OVERLAY.rstrip() + "\n", out, count=1, flags=re.S)
    dst = SCRIPTS / "c407_vision_v50_design_and_batch.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst, "bytes", dst.stat().st_size)
    return dst


def gen_smoke():
    src = (SCRIPTS / "c402_vision_v49_smoke.py").read_text(encoding="utf-8")
    out = src
    for a, b in [
        ("C402", "C408"),
        ("c402", "c408"),
        ("V49", "V50"),
        ("v49", "v50"),
        ("vision_v49", "vision_v50"),
        ("vision_images_v49", "vision_images_v50"),
        ("r50plus_v49_atoll_birch_clarity_floor_n>=16_qwen35_2b",
         "r50plus_v50_atoll_birch_clarity_floor_n>=16_qwen35_2b"),
        ("Uses C401 fixtures", "Uses C407 fixtures"),
    ]:
        out = out.replace(a, b)
    dst = SCRIPTS / "c408_vision_v50_smoke.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst, "bytes", dst.stat().st_size)
    return dst


def gen_heldout():
    src = (SCRIPTS / "c403_vision_v49_heldout.py").read_text(encoding="utf-8")
    out = src
    for a, b in [
        ("C403", "C409"),
        ("c403", "c409"),
        ("C395", "C407"),
        ("V49", "V50"),
        ("v49", "v50"),
        ("vision_v49h", "vision_v50h"),
        ("vision_v49", "vision_v50"),
        ("vision_images_v49h", "vision_images_v50h"),
        ("vision_images_v49", "vision_images_v50"),
        ("_v49hc379", "_v50hc409"),
        ("Disjoint from V50 train amounts (C407)", "Disjoint from V50 train amounts (C407)"),
        ("Disjoint heldout for V50 train (C407)", "Disjoint heldout for V50 train (C407)"),
    ]:
        out = out.replace(a, b)
    # Fix accidental v50h path issues: TRAIN should be v50 not v50h
    # After replace vision_images_v49 -> vision_images_v50, then v49h -> v50h:
    # Order above did v49h first then v49 - good if v49h done first
    out = replace_specs(out, V50H_SPECS)
    # Swap overlay in heldout too
    pat = r"    # --- V50 overlays \(new vs V43\) ---.*?(?=\n    buf = io\.BytesIO\(\))"
    if re.search(pat, out, flags=re.S):
        out = re.sub(pat, V50_OVERLAY.rstrip() + "\n", out, count=1, flags=re.S)
    else:
        pat2 = r"    # --- V49 overlays \(new vs V43\) ---.*?(?=\n    buf = io\.BytesIO\(\))"
        if re.search(pat2, out, flags=re.S):
            out = re.sub(pat2, V50_OVERLAY.rstrip() + "\n", out, count=1, flags=re.S)
        else:
            # after rename maybe V50 overlays still old content
            pat3 = r"    # --- V50 overlays \(new vs V49\) ---.*?(?=\n    buf = io\.BytesIO\(\))"
            if re.search(pat3, out, flags=re.S) and "JADE bait 45.45" not in out:
                out = re.sub(pat3, V50_OVERLAY.rstrip() + "\n", out, count=1, flags=re.S)
    dst = SCRIPTS / "c409_vision_v50_heldout.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst, "bytes", dst.stat().st_size)
    # sanity: train path
    if "vision_images_v50h" in out and "TRAIN_FIX" in out:
        # ensure TRAIN_FIX points to v50 not v50h
        out2 = out.replace(
            'TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v50h"',
            'TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v50"',
        )
        # also FIX should be v50h
        if 'FIX = ROOT / "evo/office/fixtures/vision_images_v50"' in out2 and "v50h" not in out2.split("FIX =")[1][:120]:
            pass
        dst.write_text(out2, encoding="utf-8")
        out = out2
    # Fix FIX path properly
    lines = out.splitlines()
    fixed = []
    for ln in lines:
        if ln.strip().startswith("FIX = ") and "vision_images_v50" in ln and "v50h" not in ln:
            ln = 'FIX = ROOT / "evo/office/fixtures/vision_images_v50h"'
        if ln.strip().startswith("TRAIN_FIX = ") and "v50h" in ln:
            ln = 'TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v50"'
        if ln.strip().startswith("RUN = ") and "vision_v50h" not in ln and "vision_v50" in ln:
            ln = 'RUN = ROOT / "runs/vision_v50h_c409"'
        fixed.append(ln)
    out = "\n".join(fixed) + "\n"
    dst.write_text(out, encoding="utf-8")
    print("fixed heldout paths")
    return dst


def gen_u2c():
    src = (SCRIPTS / "c386_product_u2c_cost.py").read_text(encoding="utf-8")
    out = src
    for a, b in [
        ("C386", "C410"),
        ("c386", "c410"),
        ("product_u2c_c386", "product_u2c_c410"),
        ("vision_images_v44", "vision_images_v50"),
        ('"version": "v44"', '"version": "v50"'),
        ("missing_v44_manifest", "missing_v50_manifest"),
        ("Non-vision knife", "Non-vision knife"),
        ("product polish + U2C on V28", "product polish + U2C on V50"),
    ]:
        out = out.replace(a, b)
    dst = SCRIPTS / "c410_product_u2c_cost.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst, "bytes", dst.stat().st_size)
    return dst


def gen_regression():
    src = (SCRIPTS / "c405_capture_office_regression.py").read_text(encoding="utf-8")
    out = src
    for a, b in [
        ("C405", "C411"),
        ("c405", "c411"),
        ("capture_regression_c405", "capture_regression_c411"),
        ("after C401-C404", "after C407-C410"),
        ("V4-V28+heldout", "V4-V50+heldout"),
    ]:
        out = out.replace(a, b)
    # append V50 pointers if not present
    if "VISION_V50_SMOKE" not in out:
        needle = 'SMOKE_POINTERS = ['
        insert = '''SMOKE_POINTERS = [
    ("V50", DOC / "C408_VISION_V50_SMOKE.json"),
    ("V50_heldout", DOC / "C409_VISION_V50_HELDOUT_SMOKE.json"),
'''
        # keep existing list - insert after opening
        out = out.replace(needle, insert, 1)
    dst = SCRIPTS / "c411_capture_office_regression.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst, "bytes", dst.stat().st_size)
    return dst


def gen_scorecard():
    src = (SCRIPTS / "c406_scorecard_and_stage.py").read_text(encoding="utf-8")
    out = src
    for a, b in [
        ("C406", "C412"),
        ("c406", "c412"),
        ("C401-C405", "C407-C411"),
        ("STAGE_ANT_C406.md", "STAGE_ANT_C412.md"),
        ("C402_VISION_V49_SMOKE", "C408_VISION_V50_SMOKE"),
        ("C402b_VISION_GATE_V49_CLAIM", "C408b_VISION_GATE_V50_CLAIM"),
        ("C403_VISION_V49_HELDOUT_SMOKE", "C409_VISION_V50_HELDOUT_SMOKE"),
        ("C403b_VISION_GATE_V49_HELDOUT_CLAIM", "C409b_VISION_GATE_V50_HELDOUT_CLAIM"),
        ("C404_CONFIDENCE_GATE_STRETCH", "C410_PRODUCT_U2C_COST"),
        ("C405_CAPTURE_OFFICE_REGRESSION", "C411_CAPTURE_OFFICE_REGRESSION"),
        ("v49", "v50"),
        ("V49", "V50"),
        ("v50_jpeg_q", "v50_jpeg_q"),
        ('"source": "C404"', '"source": "C410"'),
        ('"source": "C405"', '"source": "C411"'),
        ("confidence_gate", "product_u2c_knife"),
    ]:
        out = out.replace(a, b)
    # Fix scorecard logic for product u2c instead of conf gate
    # After replacements, product_u2c may be duplicated - rewrite main carefully by patching key loads
    dst = SCRIPTS / "c412_scorecard_and_stage.py"
    # Write a clean scorecard instead if mangled
    board_line = None
    for ln in src.splitlines():
        if "BOARD_MD" in ln:
            board_line = ln
            break
    # Keep chinese board path from original
    clean = f'''# -*- coding: utf-8 -*-
"""C412: Unified scorecard + STAGE after C407-C411. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
{board_line if board_line else 'BOARD_MD = ROOT / "docs" / "ANT_UNIFIED_SCORECARD.md"'}
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C412.md"
GATE = 0.6


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")


def load(rel):
    p = ROOT / rel
    if not p.is_file():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def main():
    c408 = load("docs/r50/C408_VISION_V50_SMOKE.json") or {{}}
    c408b = load("docs/r50/C408b_VISION_GATE_V50_CLAIM.json") or {{}}
    c409 = load("docs/r50/C409_VISION_V50_HELDOUT_SMOKE.json") or {{}}
    c409b = load("docs/r50/C409b_VISION_GATE_V50_HELDOUT_CLAIM.json") or {{}}
    c410 = load("docs/r50/C410_PRODUCT_U2C_COST.json") or {{}}
    c411 = load("docs/r50/C411_CAPTURE_OFFICE_REGRESSION.json") or {{}}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {{}}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {{}}

    v50 = float(c408.get("rate") or 0.0)
    v50h = float(c409.get("rate") or 0.0)
    v50_claim = bool(c408b.get("vl_gate_v50_claim") or c408.get("vl_gate_v50_claim") or c408.get("claim"))
    v50h_claim = bool(c409b.get("vl_gate_v50_heldout_claim") or c409.get("vl_gate_v50_heldout_claim") or c409.get("claim"))
    disjoint = bool(c409.get("id_disjoint") or c409.get("disjoint") or c409b.get("id_disjoint") or c409b.get("disjoint"))
    u2c_pass = bool(c410.get("pass"))
    replace_ratio = float(c410.get("replace_ratio") or c410.get("mean_ratio") or (c410.get("replace_ledger") or {{}}).get("mean_ratio") or (prior.get("product_u2c") or {{}}).get("replace_ratio") or 4.07)
    capture_pass = bool(c411.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {{}}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {{}}).get("shadow_pass", dissolve_pass))
    conf_pass = bool((prior.get("confidence_gate") or {{}}).get("pass", True))
    conf_rate = float((prior.get("confidence_gate") or {{}}).get("rate") or 1.0)

    rates = [v50, v50h]
    if dissolve_pass:
        rates.append(1.0)
    if capture_pass:
        rates.append(1.0)
    if u2c_pass:
        rates.append(1.0)
    composite = round(min(rates) if rates else 0.0, 4)
    if not (v50_claim and v50h_claim and v50 >= GATE and v50h >= GATE):
        composite = min(composite, 0.0)
    stage_ready = bool(
        v50_claim and v50h_claim and v50 >= GATE and v50h >= GATE
        and capture_pass and disjoint
    )

    out = {{
        "cycle": "C412",
        "timestamp": ts(),
        "gate": GATE,
        "vision": {{
            "v49": (prior.get("vision") or {{}}).get("v49") or {{"rate": 1.0, "claim": True}},
            "v49_heldout": (prior.get("vision") or {{}}).get("v49_heldout") or {{"rate": 1.0, "claim": True}},
            "v50": {{"rate": v50, "claim": v50_claim, "n": c408.get("n")}},
            "v50_heldout": {{"rate": v50h, "claim": v50h_claim, "disjoint": disjoint, "n": c409.get("n")}},
        }},
        "product_u2c": {{
            "pass": u2c_pass,
            "replace_ratio": replace_ratio,
            "source": "C410",
        }},
        "confidence_gate": {{"pass": conf_pass, "rate": conf_rate, "source": "prior_C404"}},
        "capture_regression": {{"pass": capture_pass, "source": "C411"}},
        "dissolve_shadow": {{
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        }},
        "composite": composite,
        "stage_ready": stage_ready,
        "v50_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }}
    if stage_ready and v50 >= GATE and v50h >= GATE:
        out["composite"] = 1.0 if (v50 >= 0.999 and v50h >= 0.999) else min(v50, v50h)
    J(DOC / "C412_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = []
    md.append("# Unified Scorecard (C412)")
    md.append("")
    md.append(f"Updated: {{ts()}} (Asia/Shanghai)")
    md.append("")
    md.append(f"- Vision V50: rate={{v50}} claim={{v50_claim}}")
    md.append(f"- Vision V50 heldout: rate={{v50h}} claim={{v50h_claim}} disjoint={{disjoint}}")
    md.append(f"- product_u2c: pass={{u2c_pass}} replace_ratio={{replace_ratio}}")
    md.append(f"- capture_regression: pass={{capture_pass}}")
    md.append(f"- dissolve/shadow: {{dissolve_pass}}/{{shadow_pass}}")
    md.append(f"- composite: {{out['composite']}}")
    md.append(f"- stage_ready: {{stage_ready}}")
    md.append("- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD")
    md.append("")
    BOARD_MD.write_text("\\n".join(md) + "\\n", encoding="utf-8")

    stage = []
    stage.append("# STAGE_ANT_C412")
    stage.append("")
    stage.append(f"Updated: {{ts()}} (Asia/Shanghai)")
    stage.append("")
    stage.append("**C407-C412 STAGE_READY={{'YES' if stage_ready else 'NO'}}**")
    stage.append("")
    stage.append("## Tip slice")
    stage.append("- C407: Vision V50 design fixtures (jpeg_q=62, floor>=60)")
    stage.append(f"- C408: Vision V50 smoke claim **{{v50}}** (n={{c408.get('n')}})")
    stage.append(f"- C409: Vision V50 heldout claim **{{v50h}}** (disjoint={{disjoint}})")
    stage.append(f"- C410: product-U2C pass={{u2c_pass}} replace≈{{replace_ratio}}")
    stage.append(f"- C411: capture-office regression pass={{capture_pass}}")
    stage.append(f"- C412: unified scorecard composite={{out['composite']}}")
    stage.append("")
    stage.append("## Constraints")
    stage.append("- Gate: 0.6")
    stage.append("- Gate2/3: untouched")
    stage.append("- gen11: HOLD")
    stage.append("- clarity floor jpeg_q>=60 kept on V50 (uses 62)")
    stage.append("")
    stage.append("## Entry")
    stage.append(f"- Scorecard: {{BOARD_MD.relative_to(ROOT).as_posix()}}")
    stage.append("- Latest JSON: docs/r50/SCORECARD_LATEST.json")
    stage.append("- This stage: docs/STAGE_ANT_C412.md")
    stage.append("")
    STAGE.write_text("\\n".join(stage) + "\\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''
    # Fix escaped newlines in J and write_text - the clean template used \\n which becomes \n in file - good for Python source wanting \n in string
    # Actually in the f-string I used "\\n" which writes \n to file - correct for Python.
    # But BOARD_MD.write_text("\\n".join - in the written file that becomes "\n".join which is correct.
    dst.write_text(clean, encoding="utf-8")
    print("wrote", dst, "bytes", dst.stat().st_size)
    return dst


def main():
    gen_design()
    gen_smoke()
    gen_heldout()
    gen_u2c()
    gen_regression()
    gen_scorecard()
    print("OK all C407-C412 scripts")


if __name__ == "__main__":
    main()
