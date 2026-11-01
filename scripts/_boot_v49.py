# -*- coding: utf-8 -*-
"""Compact C401-C406 bootstrap for V49."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1] if Path(__file__).name.startswith("c") else Path(".").resolve()
# when run as scripts/_boot_v49.py, parents[1] is repo
HERE = Path(__file__).resolve().parent
if (HERE / "c395_vision_v48_design_and_batch.py").is_file():
    S = HERE
    ROOT = HERE.parent
else:
    S = ROOT / "scripts"

V49_OVERLAY = """
    # --- V49 overlays (new vs V48) ---
    for _ in range(140):
        bx = rng.randint(50, 540)
        by = rng.randint(365, 595)
        if in_text_band(by):
            continue
        d.line([(bx, by), (bx + rng.randint(8, 30), by + rng.randint(-7, 7))], fill=(55, 45, 30), width=1)
    for gi in range(5):
        d.ellipse([58 + gi * 24, 324, 76 + gi * 24, 342], outline=(130, 80, 40), width=2)
    d.text((58, 344), "WAX bait 45.45", fill=(90, 50, 20), font=f_tiny)
    for hi in range(4):
        d.polygon([(600 + hi * 34, 44), (626 + hi * 34, 44), (613 + hi * 34, 80)], fill=(30, 70, 40))
    d.text((600, 84), "KELP bait 65.65", fill=(20, 50, 20), font=f_tiny)
    d.rectangle([270, 400, 430, 460], fill=(255, 248, 240))
    d.text((280, 420), "PARCHMENT ghost 95.95", fill=(90, 50, 30), font=f_pen)
    d.arc([430, 390, 520, 460], 40, 265, fill=(160, 100, 50), width=3)
    d.text((430, 465), "AMBER bait 40.40", fill=(120, 70, 20), font=f_tiny)
    d.ellipse([80, 490, 150, 550], fill=(180, 170, 150), outline=(90, 80, 60), width=2)
    d.text((80, 555), "DUNE bait 31.31", fill=(90, 70, 40), font=f_tiny)
    for qi in range(4):
        d.rectangle([270 + qi * 42, 490, 302 + qi * 42, 522], outline=(100, 80, 50), width=2)
    d.rectangle([870, 130, 1020, 190], fill=(210, 200, 175), outline=(80, 70, 50), width=2)
    d.text((890, 148), "BRASS", fill=(50, 35, 15), font=f_stamp)
    d.polygon([(40, 4), (420, 4), (405, 18), (50, 18)], fill=(230, 215, 185), outline=(120, 95, 55), width=1)
    d.text((70, 5), "GUMSTRIP bait 75.75", fill=(60, 45, 25), font=f_tiny)
    for ti, ty in enumerate((110, 170, 230)):
        d.polygon([(1000, ty), (1024, ty + 12), (1000, ty + 24)], fill=(100, 80, 45 + ti * 20))
    d.ellipse([980, 480, 1060, 560], fill=(150, 30, 30), outline=(80, 10, 10), width=2)
    d.text((992, 508), "SEAL", fill=(240, 220, 180), font=f_sm)
    for py in range(80, 560, 18):
        d.ellipse([548, py, 556, py + 6], fill=(210, 206, 196), outline=(40, 40, 40), width=1)
    for si in range(8):
        d.arc([20, 100 + si * 50, 55, 140 + si * 50], 200, 340, fill=(90, 70, 40), width=2)
"""

# kind, metric, stamp, lines_builder data
TRAIN = [
    ("aurora_recv", "paid_total", "RECV", 256.25, ["AURORA GRAIN RECV V49", "a paid 124.00", "b paid 132.25", "c open 55.00", "TOTAL PAID TARGET 256.25"]),
    ("basalt_wh", "qty_sum", "RECV", 208.0, ["WH BASALT BIN V49", "SKU1 qty 91 ok", "SKU2 qty 68 hold", "SKU3 qty 117 ok", "qty_sum TARGET 208"]),
    ("canyon_refund", "refund_done", "DONE", 178.5, ["CANYON PATCH REFUND V49", "itemR1 86.00 done", "itemR2 92.50 done", "itemR3 41.00 open", "refund_done TARGET 178.50"]),
    ("dune_tax", "tax_base_paid", "TAX", 351.0, ["DUNE TAX SLIP V49", "base 171.00 paid", "addon 180.00 paid", "skip 86.00", "tax_base_paid TARGET 351.00"]),
    ("estuary_pay", "payroll_active", "PAY", 441.0, ["ESTUARY PAYROLL V49", "empA 215.00 active", "empB 226.00 active", "empC 74.00 leave", "payroll_active TARGET 441.00"]),
    ("fjord_ship", "ship_ok", "SHIP", 156.0, ["FJORD SHIP DOCK V49", "box1 75 ok", "box2 81 ok", "box3 49 hold", "ship_ok TARGET 156"]),
    ("glacier_sla", "sla_ok_hours", "SLA", 184.75, ["GLACIER SLA CARD V49", "job1 98.00 hours ok", "job2 86.75 hours ok", "job3 47.00 hours late", "sla_ok_hours TARGET 184.75"]),
    ("harbor_exp", "exp_sum", "EXP", 227.25, ["HARBOR EXPENSE V49", "e1 109.00", "e2 118.25", "e3 54.00 void", "exp_sum TARGET 227.25"]),
    ("islet_po", "po_open", "PO", 252.0, ["ISLET PO SHEET V49", "line1 133.00 open", "line2 119.00 open", "line3 61.00 closed", "po_open TARGET 252.00"]),
    ("jasper_order", "order_paid", "ORD", 301.5, ["JASPER ORDER V49", "skuA 159.00 paid", "skuB 142.50 paid", "skuC 51.00 due", "order_paid TARGET 301.50"]),
    ("kelp_dup", "dup_mark", "DUP", 2.0, ["KELP DUP MARK V49", "markA 1", "markB 1", "markC 0", "dup_mark TARGET 2"]),
    ("lagoon_zero", "zero_check", "ZERO", 0.0, ["LAGOON AIR ZERO V49", "z1 0.00", "z2 0.00", "z3 0.00", "zero_check TARGET 0.00"]),
    ("meadow_ledger", "ledger_net", "LED", 382.75, ["MEADOW LEDGER V49", "dr 186.00", "cr 196.75", "adj 71.00", "ledger_net TARGET 382.75"]),
    ("nectar_ui", "ui_ok", "UI", 1.0, ["NECTAR UI SCAN V49", "btnOK 1", "btnSkip 0", "btnBad 0", "ui_ok TARGET 1"]),
    ("oasis_stack", "stack_count", "STK", 34.0, ["OASIS STACK V49", "p1 16", "p2 12", "p3 6", "stack_count TARGET 34"]),
    ("prairie_fax", "fax_pages", "FAX", 41.0, ["PRAIRIE FAX V49", "pgA 23", "pgB 18", "pgC 13 drop", "fax_pages TARGET 41"]),
    ("quarry_glare", "glare_ok", "GLR", 1.0, ["QUARRY GLARE V49", "zone1 1 ok", "zone2 0", "zone3 0", "glare_ok TARGET 1"]),
    ("ridge_tab", "tab_index", "TAB", 57.0, ["RIDGE TAB INDEX V49", "tabA 31", "tabB 26", "tabC 12", "tab_index TARGET 57"]),
]
# Fix jasper typo 311 -> 301.5 already in TARGET line; amount field 301.5 ok
TRAIN[9] = ("jasper_order", "order_paid", "ORD", 301.5, ["JASPER ORDER V49", "skuA 159.00 paid", "skuB 142.50 paid", "skuC 51.00 due", "order_paid TARGET 301.50"])

HELDOUT = [
    ("aurora_recv", "paid_total", "RECV", 148.5, ["AURORA GRAIN RECV V49H", "a paid 71.00", "b paid 77.50", "c open 32.00", "TOTAL PAID TARGET 148.50"]),
    ("basalt_wh", "qty_sum", "RECV", 119.0, ["WH BASALT BIN V49H", "SKU1 qty 52 ok", "SKU2 qty 39 hold", "SKU3 qty 67 ok", "qty_sum TARGET 119"]),
    ("canyon_refund", "refund_done", "DONE", 103.75, ["CANYON PATCH REFUND V49H", "itemR1 49.50 done", "itemR2 54.25 done", "itemR3 24.00 open", "refund_done TARGET 103.75"]),
    ("dune_tax", "tax_base_paid", "TAX", 206.0, ["DUNE TAX SLIP V49H", "base 100.00 paid", "addon 106.00 paid", "skip 47.00", "tax_base_paid TARGET 206.00"]),
    ("estuary_pay", "payroll_active", "PAY", 259.0, ["ESTUARY PAYROLL V49H", "empA 126.00 active", "empB 133.00 active", "empC 43.00 leave", "payroll_active TARGET 259.00"]),
    ("fjord_ship", "ship_ok", "SHIP", 89.0, ["FJORD SHIP DOCK V49H", "box1 42 ok", "box2 47 ok", "box3 27 hold", "ship_ok TARGET 89"]),
    ("glacier_sla", "sla_ok_hours", "SLA", 107.25, ["GLACIER SLA CARD V49H", "job1 57.00 hours ok", "job2 50.25 hours ok", "job3 28.00 hours late", "sla_ok_hours TARGET 107.25"]),
    ("harbor_exp", "exp_sum", "EXP", 132.5, ["HARBOR EXPENSE V49H", "e1 63.00", "e2 69.50", "e3 33.00 void", "exp_sum TARGET 132.50"]),
    ("islet_po", "po_open", "PO", 146.0, ["ISLET PO SHEET V49H", "line1 78.00 open", "line2 68.00 open", "line3 36.00 closed", "po_open TARGET 146.00"]),
    ("jasper_order", "order_paid", "ORD", 173.0, ["JASPER ORDER V49H", "skuA 92.00 paid", "skuB 81.00 paid", "skuC 30.00 due", "order_paid TARGET 173.00"]),
    ("kelp_dup", "dup_mark", "DUP", 2.0, ["KELP DUP MARK V49H", "markA 1", "markB 1", "markC 0", "dup_mark TARGET 2"]),
    ("lagoon_zero", "zero_check", "ZERO", 0.0, ["LAGOON AIR ZERO V49H", "z1 0.00", "z2 0.00", "z3 0.00", "zero_check TARGET 0.00"]),
    ("meadow_ledger", "ledger_net", "LED", 221.5, ["MEADOW LEDGER V49H", "dr 108.00", "cr 113.50", "adj 41.00", "ledger_net TARGET 221.50"]),
    ("nectar_ui", "ui_ok", "UI", 1.0, ["NECTAR UI SCAN V49H", "btnOK 1", "btnSkip 0", "btnBad 0", "ui_ok TARGET 1"]),
    ("oasis_stack", "stack_count", "STK", 19.0, ["OASIS STACK V49H", "p1 9", "p2 7", "p3 3", "stack_count TARGET 19"]),
    ("prairie_fax", "fax_pages", "FAX", 24.0, ["PRAIRIE FAX V49H", "pgA 13", "pgB 11", "pgC 8 drop", "fax_pages TARGET 24"]),
    ("quarry_glare", "glare_ok", "GLR", 1.0, ["QUARRY GLARE V49H", "zone1 1 ok", "zone2 0", "zone3 0", "glare_ok TARGET 1"]),
    ("ridge_tab", "tab_index", "TAB", 35.0, ["RIDGE TAB INDEX V49H", "tabA 19", "tabB 16", "tabC 9", "tab_index TARGET 35"]),
]

CN = {
    "aurora_recv": "aurora", "basalt_wh": "basalt", "canyon_refund": "canyon", "dune_tax": "dune",
    "estuary_pay": "estuary", "fjord_ship": "fjord", "glacier_sla": "glacier", "harbor_exp": "harbor",
    "islet_po": "islet", "jasper_order": "jasper", "kelp_dup": "kelp", "lagoon_zero": "lagoon",
    "meadow_ledger": "meadow", "nectar_ui": "nectar", "oasis_stack": "oasis", "prairie_fax": "prairie",
    "quarry_glare": "quarry", "ridge_tab": "ridge",
}


def fmt_specs(rows, prefix):
    parts = ["SPECS = ["]
    for i, (kind, metric, stamp, expected, lines) in enumerate(rows, 1):
        fid = f"{prefix}_{i:02d}"
        lines_s = ",\n     ".join(repr(x) for x in lines)
        parts.append(
            f'    ("{fid}", "{kind}", "{metric}", {expected},\n'
            f'     [{lines_s}],\n'
            f'     {repr(CN[kind])}, "{stamp}"),'
        )
    parts.append("]")
    return "\n".join(parts)


def replace_specs(text, new_specs):
    start = text.find("SPECS = [")
    end = text.find("]\n\n\ndef ts()", start)
    if end < 0:
        end = text.find("]\n\ndef ts()", start)
    if start < 0 or end < 0:
        raise SystemExit(f"specs not found start={start} end={end}")
    return text[:start] + new_specs + text[end + 1 :]


def insert_overlay(text):
    marker = "    buf = io.BytesIO()"
    idx = text.find(marker)
    if idx < 0:
        raise SystemExit("buf marker missing")
    if "V49 overlays" in text:
        return text
    return text[:idx] + V49_OVERLAY + "\n" + text[idx:]


def main():
    # C401
    t = (S / "c395_vision_v48_design_and_batch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C395", "C401"), ("c395", "c401"), ("V48", "V49"), ("v48", "v49"),
        ("vision_images_v48", "vision_images_v49"), ("VL_GATE_V48", "VL_GATE_V49"),
        ("vl_gate_v48", "vl_gate_v49"), ("_v48c377", "_v49c401"),
        ("Harder than V43", "Harder than V48"),
        ('harder_than": "v44_flint_velvet"', 'harder_than": "v48_atoll_birch"'),
        ("V48 keeps floor", "V49 keeps floor"),
        ("No claim until C303 VL", "No claim until C402 VL"),
        ("claim deferred to C396", "claim deferred to C402"),
        ("No fake VL scores in C395", "No fake VL scores in C401"),
        ("C395 design+fixtures; no VL claim", "C401 design+fixtures; no VL claim"),
    ]:
        t = t.replace(a, b)
    t = replace_specs(t, fmt_specs(TRAIN, "v49"))
    t = insert_overlay(t)
    t = t.replace('"coffee_ring_center",', '"coffee_ring_center",\n            "wax_seal", "ledger_perforation", "string_binding",')
    (S / "c401_vision_v49_design_and_batch.py").write_text(t, encoding="utf-8")
    print("wrote c401", len(t))

    # C402
    t = (S / "c396_vision_v48_smoke.py").read_text(encoding="utf-8")
    for a, b in [
        ("C396", "C402"), ("c396", "c402"), ("V48", "V49"), ("v48", "v49"),
        ("vision_images_v48", "vision_images_v49"), ("vl_gate_v48", "vl_gate_v49"),
        ("r50plus_v48_atoll_birch", "r50plus_v49_aurora_basalt"),
        ("Uses C395 fixtures", "Uses C401 fixtures"),
    ]:
        t = t.replace(a, b)
    (S / "c402_vision_v49_smoke.py").write_text(t, encoding="utf-8")
    print("wrote c402", len(t))

    # C403
    t = (S / "c397_vision_v48_heldout.py").read_text(encoding="utf-8")
    for a, b in [
        ("C397", "C403"), ("c397", "c403"), ("V48", "V49"), ("v48", "v49"),
        ("vision_images_v48h", "vision_images_v49h"),
        ("vision_images_v48", "vision_images_v49"),
        ("VL_GATE_V48_HELDOUT", "VL_GATE_V49_HELDOUT"),
        ("vl_gate_v48_heldout", "vl_gate_v49_heldout"),
        ("_v48hc379", "_v49hc403"), ("V48H C397", "V49H C403"),
        ("V48 train (C395)", "V49 train (C401)"),
        ("Different ids/amounts from V48 train (C395)", "Different ids/amounts from V49 train (C401)"),
        ("r50plus_v48_heldout_flint_velvet", "r50plus_v49_heldout_aurora_basalt"),
        ('version": "v43h"', 'version": "v49h"'),
        ("Ant VL Gate V42 Heldout", "Ant VL Gate V49 Heldout"),
    ]:
        t = t.replace(a, b)
    t = replace_specs(t, fmt_specs(HELDOUT, "v49h"))
    t = insert_overlay(t)
    (S / "c403_vision_v49_heldout.py").write_text(t, encoding="utf-8")
    print("wrote c403", len(t))

    # C404
    t = (S / "c392_confidence_gate_stretch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C392", "C404"), ("c392", "c404"),
        ("confidence_gate_stretch_v45", "confidence_gate_stretch_v49"),
        ("cg43_", "cg49_"), ("V27 amounts", "V49 amounts"),
    ]:
        t = t.replace(a, b)
    t = t.replace("TOTAL PAID TARGET 112.50", "TOTAL PAID TARGET 118.75")
    t = t.replace('"expected": 112.50', '"expected": 118.75', 1)
    t = t.replace("a paid 54.00 b paid 58.50 c open 16.00", "a paid 57.00 b paid 61.75 c open 17.00")
    t = t.replace("qty_sum TARGET 102", "qty_sum TARGET 108")
    t = t.replace('"expected": 102.0, "want_decision": "force_tool"', '"expected": 108.0, "want_decision": "force_tool"', 1)
    t = t.replace("SKU1 qty 49 ok SKU2 qty 24 hold SKU3 qty 53 ok", "SKU1 qty 52 ok SKU2 qty 26 hold SKU3 qty 56 ok")
    (S / "c404_confidence_gate_stretch.py").write_text(t, encoding="utf-8")
    print("wrote c404", len(t))

    # C405
    t = (S / "c399_capture_office_regression.py").read_text(encoding="utf-8")
    t = t.replace("C399", "C405").replace("c399", "c405")
    t = t.replace("after C395-C398", "after C401-C404")
    if "V49" not in t:
        insert = (
            '    ("V48", DOC / "C396_VISION_V48_SMOKE.json"),\n'
            '    ("V48_heldout", DOC / "C397_VISION_V48_HELDOUT_SMOKE.json"),\n'
            '    ("V49", DOC / "C402_VISION_V49_SMOKE.json"),\n'
            '    ("V49_heldout", DOC / "C403_VISION_V49_HELDOUT_SMOKE.json"),\n'
            '    ("C404_conf_gate", DOC / "C404_CONFIDENCE_GATE_STRETCH.json"),\n'
        )
        needle = '("V27_heldout", DOC / "C268_VISION_V27_HELDOUT_SMOKE.json"),'
        if needle in t:
            t = t.replace(needle, needle + "\n" + insert, 1)
    (S / "c405_capture_office_regression.py").write_text(t, encoding="utf-8")
    print("wrote c405", len(t))

    # C406 from prior template with replacements
    t = (S / "c400_scorecard_and_stage.py").read_text(encoding="utf-8")
    t = t.replace("C400", "C406").replace("c400", "c406")
    t = t.replace("C395-C399", "C401-C405").replace("C395-C400", "C401-C406")
    t = t.replace("C396_VISION_V48", "C402_VISION_V49").replace("C396b_VISION_GATE_V48", "C402b_VISION_GATE_V49")
    t = t.replace("C397_VISION_V48", "C403_VISION_V49").replace("C397b_VISION_GATE_V48", "C403b_VISION_GATE_V49")
    t = t.replace("vl_gate_v48", "vl_gate_v49").replace("V48", "V49").replace("v48", "v49")
    # undo over-replace of STAGE path already C406; fix dissolve to C398 prior and conf to C404
    t = t.replace("C398_DISSOLVE", "C398_DISSOLVE")  # keep
    # After V48->V49, C398 may have become C399? Check: C398 has no V48. Good.
    # confidence was c392 - need C404
    t = t.replace('load("docs/r50/C392_CONFIDENCE_GATE_STRETCH.json")', 'load("docs/r50/C404_CONFIDENCE_GATE_STRETCH.json")')
    t = t.replace('c392 = load', 'c404 = load').replace('c392.get', 'c404.get')
    t = t.replace('"source": "C392"', '"source": "C404"')
    t = t.replace("C399_CAPTURE", "C405_CAPTURE").replace("source\": \"C399\"", "source\": \"C405\"")
    t = t.replace("prior C392", "C404").replace("(prior C392)", "(C404)")
    t = t.replace("C395: Vision V49", "C401: Vision V49")
    t = t.replace("C396: Vision V49", "C402: Vision V49")
    t = t.replace("C397: Vision V49", "C403: Vision V49")
    # fix v47 leftovers: after replace v48->v49, vision keys for prior should keep v48 from prior json
    # Rebuild scorecard cleanly instead
    body = (Path(__file__).resolve().parent / "_unused")
    (S / "c406_scorecard_and_stage.py").write_text(t, encoding="utf-8")
    print("wrote c406 draft", len(t))
    print("ROOT", ROOT, "S", S)
    print("DONE_BOOT")


if __name__ == "__main__":
    main()
