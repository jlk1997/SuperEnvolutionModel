# -*- coding: utf-8 -*-
from __future__ import annotations
import json, re
from pathlib import Path
ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"
BAN = {755, 756, 770, 750, 830, 1830, 1560}

def lines_for_metric(name, kind_suf, metric, title, stamp, a, b, c, tag):
    if metric == "paid_total":
        expected, body = a + b, [f"a paid {a:.2f}", f"b paid {b:.2f}", f"c open {c:.2f}", f"TOTAL PAID TARGET {a+b:.2f}"]
    elif metric == "qty_sum":
        expected = float(a + b); body = [f"SKU1 qty {a} ok", f"SKU2 qty {c} hold", f"SKU3 qty {b} ok", f"qty_sum TARGET {a+b}"]
    elif metric == "refund_done":
        expected, body = a + b, [f"itemR1 {a:.2f} done", f"itemR2 {b:.2f} done", f"itemR3 {c:.2f} open", f"refund_done TARGET {a+b:.2f}"]
    elif metric == "tax_base_paid":
        expected, body = a + b, [f"base {a:.2f} paid", f"addon {b:.2f} paid", f"skip {c:.2f}", f"tax_base_paid TARGET {a+b:.2f}"]
    elif metric == "payroll_active":
        expected, body = a + b, [f"empA {a:.2f} active", f"empB {b:.2f} active", f"empC {c:.2f} leave", f"payroll_active TARGET {a+b:.2f}"]
    elif metric == "ship_ok":
        expected = float(a + b); body = [f"box1 {a} ok", f"box2 {b} ok", f"box3 {c} hold", f"ship_ok TARGET {a+b}"]
    elif metric == "sla_ok_hours":
        expected, body = a + b, [f"job1 {a:.2f} hours ok", f"job2 {b:.2f} hours ok", f"job3 {c:.2f} hours late", f"sla_ok_hours TARGET {a+b:.2f}"]
    elif metric == "exp_sum":
        expected, body = a + b, [f"e1 {a:.2f}", f"e2 {b:.2f}", f"e3 {c:.2f} void", f"exp_sum TARGET {a+b:.2f}"]
    elif metric == "po_open":
        expected, body = a + b, [f"line1 {a:.2f} open", f"line2 {b:.2f} open", f"line3 {c:.2f} closed", f"po_open TARGET {a+b:.2f}"]
    elif metric == "order_paid":
        expected, body = a + b, [f"skuA {a:.2f} paid", f"skuB {b:.2f} paid", f"skuC {c:.2f} due", f"order_paid TARGET {a+b:.2f}"]
    elif metric == "dup_mark":
        expected, body = 2.0, ["markA 1", "markB 1", "markC 0", "dup_mark TARGET 2"]
    elif metric == "zero_check":
        expected, body = 0.0, ["z1 0.00", "z2 0.00", "z3 0.00", "zero_check TARGET 0.00"]
    elif metric == "ledger_net":
        expected, body = a + b, [f"dr {a:.2f}", f"cr {b:.2f}", f"adj {c:.2f}", f"ledger_net TARGET {a+b:.2f}"]
    elif metric == "ui_ok":
        expected, body = 1.0, ["btnOK 1", "btnSkip 0", "btnBad 0", "ui_ok TARGET 1"]
    elif metric == "stack_count":
        expected = float(a + b); body = [f"p1 {a}", f"p2 {b}", f"p3 {c}", f"stack_count TARGET {a+b}"]
    elif metric == "fax_pages":
        expected = float(a + b); body = [f"pgA {a}", f"pgB {b}", f"pgC {c} drop", f"fax_pages TARGET {a+b}"]
    elif metric == "glare_ok":
        expected, body = 1.0, ["zone1 1 ok", "zone2 0", "zone3 0", "glare_ok TARGET 1"]
    elif metric == "tab_index":
        expected = float(a + b); body = [f"tabA {a}", f"tabB {b}", f"tabC {c}", f"tab_index TARGET {a+b}"]
    else:
        raise ValueError(metric)
    return expected, [f"{title} {tag}"] + body

def build_specs(themes, prefix, tag, abcs):
    lines = ["SPECS = ["]
    for i, (t, abc) in enumerate(zip(themes, abcs), 1):
        name, kind_suf, metric, title, stamp, _bk = t
        a, b, c = abc
        expected, body = lines_for_metric(name, kind_suf, metric, title, stamp, a, b, c, tag)
        fid = f"{prefix}_{i:02d}"; kind = f"{name}_{kind_suf}"
        body_l = ",\n     ".join(repr(x) for x in body)
        lines.append(f'    ("{fid}", "{kind}", "{metric}", {repr(float(expected))},\n     [{body_l}],\n     {repr(name)}, "{stamp}"),')
    lines.append("]")
    return "\n".join(lines) + "\n"

def replace_specs(src, new_specs):
    return re.sub(r"SPECS = \[.*?\n\]\n", new_specs + "\n", src, count=1, flags=re.S)

def check(rows, label):
    for i, row in enumerate(rows):
        for v in row:
            if isinstance(v, (int, float)) and int(v) in BAN:
                raise SystemExit(f"banned {v} in {label}[{i}]={row}")

# *moor ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T227 = [
    ["ashmoor","recv","paid_total","ASHMOOR GRAIN RECV","RECV","x"],
    ["cedarmoor","wh","qty_sum","WH CEDARMOOR BIN","RECV","x"],
    ["dawnmoor","refund","refund_done","DAWNMOOR PATCH REFUND","DONE","x"],
    ["elmmoor","tax","tax_base_paid","ELMMOOR TAX SLIP","TAX","x"],
    ["fernmoor","pay","payroll_active","FERNMOOR PAYROLL","PAY","x"],
    ["glenmoor","ship","ship_ok","GLENMOOR SHIP DOCK","SHIP","x"],
    ["hazemoor","sla","sla_ok_hours","HAZEMOOR SLA CARD","SLA","x"],
    ["inkmoor","exp","exp_sum","INKMOOR EXPENSE","EXP","x"],
    ["jademoor","po","po_open","JADEMOOR PO SHEET","PO","x"],
    ["knotmoor","order","order_paid","KNOTMOOR ORDER","ORD","x"],
    ["lakemoor","dup","dup_mark","LAKEMOOR DUP MARK","DUP","x"],
    ["mossmoor","zero","zero_check","MOSSMOOR AIR ZERO","ZERO","x"],
    ["nethermoor","ledger","ledger_net","NETHERMOOR LEDGER","LED","x"],
    ["oakmoor","ui","ui_ok","OAKMOOR UI SCAN","UI","x"],
    ["pinemoor","stack","stack_count","PINEMOOR STACK","STK","x"],
    ["quillmoor","fax","fax_pages","QUILLMOOR FAX","FAX","x"],
    ["reedmoor","glare","glare_ok","REEDMOOR GLARE","GLR","x"],
    ["stonemoor","tab","tab_index","STONEMOOR TAB INDEX","TAB","x"],
]
TR227 = [
    [1780.0, 1797.5, 1558.0],[840, 760, 820],[1703.0, 1732.25, 1538.0],[1836.0, 1853.0, 1628.0],
    [1898.0, 1922.0, 1598.0],[1656, 1672, 1556],[480.0, 520.0, 740.0],[1746.0, 1777.75, 1562.0],
    [840.0, 760.0, 820.0],[1813.0, 1801.0, 1559.0],[1,1,0],[0,0,0],
    [1879.0, 1900.5, 1584.0],[1,0,0],[1156, 1148, 1128],[1172, 1156, 748],[1,0,0],[1188, 1172, 1150],
]
HO227 = [
    [1618.0, 1630.75, 1479.0],[740, 780, 820],[1561.0, 1574.5, 1454.0],[1691.0, 1707.0, 1508.0],
    [1732.0, 1748.0, 1503.0],[1526, 1540, 1472],[360.0, 400.0, 730.0],[1602.0, 1623.75, 1479.0],
    [780.0, 740.0, 820.0],[1649.0, 1635.0, 1474.0],[1,1,0],[0,0,0],
    [1684.0, 1699.5, 1489.0],[1,0,0],[1143, 1138, 1133],[1158, 1152, 1140],[1,0,0],[1168, 1162, 1141],
]
check(TR227, "TR"); check(HO227, "HO")

(ROOT / "tools/_v227_themes.json").write_text(json.dumps({"themes": T227, "train": TR227, "heldout": HO227}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_227(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V227 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V227 overlays (new vs V49) ---")
    for a, b in [
        ("ASHWICK bait 140.50", "ASHMOOR bait 141.51"),
        ("CEDARW bait 142.52", "CEDARM bait 143.53"),
        ("DAWNW ghost 65.65", "DAWNM ghost 66.66"),
        ("GLENW bait 135.45", "GLENM bait 136.46"),
        ("JADEW bait 126.36", "JADEM bait 127.37"),
        ("NETHERW bait 143.53", "NETHERM bait 144.54"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V227-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD226 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v226_themes.json").read_text(encoding="utf-8"))["themes"])
NEW227 = "_".join(t[0] for t in T227)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1469"), ("c1463", "c1469"), ("V226", "V227"), ("v226", "v227"),
    ("_v226c1463", "_v227c1469"),
    ("Harder than V225", "Harder than V226"), ("harder than V225", "harder than V226"),
    (OLD226, NEW227),
    ("V226 keeps floor", "V227 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1469 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1470 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1470 VL"),
    ("kept on V226", "kept on V227"),
    ("vision_images_v226", "vision_images_v227"),
    ("VL_GATE_V226", "VL_GATE_V227"), ("vl_gate_v226", "vl_gate_v227"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V226: ashmoor, cedarmoor, dawnmoor, elmmoor, fernmoor, glenmoor, hazemoor, inkmoor,\njademoor, knotmoor, lakemoor, mossmoor, nethermoor, oakmoor, pinemoor, quillmoor, reedmoor, stonemoor.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T227, "v227", "V227", TR227))
out = retarget_227(out)
(S / "c1469_vision_v227_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1470"), ("c1464", "c1470"), ("V226", "V227"), ("v226", "v227"),
    ("vision_images_v226", "vision_images_v227"),
    ("VL_GATE_V226", "VL_GATE_V227"), ("vl_gate_v226", "vl_gate_v227"),
    ("runs/vision_v226", "runs/vision_v227"),
]:
    out = out.replace(a, b)
(S / "c1470_vision_v227_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1471"), ("c1465", "c1471"), ("V226", "V227"), ("v226", "v227"),
    ("vision_images_v226h", "vision_images_v227h"),
    ("vision_images_v226", "vision_images_v227"),
    ("VL_GATE_V226", "VL_GATE_V227"), ("vl_gate_v226", "vl_gate_v227"),
    ("runs/vision_v226h", "runs/vision_v227h"),
    ("_v226c1463", "_v227c1469"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T227, "v227h", "V227H", HO227))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v227h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v227"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v227" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v227h_c1471"'); seen_run = True; continue
    out2.append(ln)
(S / "c1471_vision_v227_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1460_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1460", "C1472"), ("c1460", "c1472"),
    ("cg95_", "cg96_"),
    ("conf_gate_stretch_c1460", "conf_gate_stretch_c1472"),
    ("confidence_gate_stretch_v158", "confidence_gate_stretch_v159"),
    ("Stretch vs C1448", "Stretch vs C1460"),
]:
    out = out.replace(a, b)
out = out.replace("a paid 74.00 b paid 78.75 c open 34.00 TOTAL PAID TARGET 152.75", "a paid 75.00 b paid 79.75 c open 35.00 TOTAL PAID TARGET 154.75")
out = out.replace('"model_guess": 999.0, "expected": 152.75', '"model_guess": 999.0, "expected": 154.75')
out = out.replace("SKU1 qty 69 ok SKU2 qty 43 hold SKU3 qty 73 ok qty_sum TARGET 142", "SKU1 qty 70 ok SKU2 qty 44 hold SKU3 qty 74 ok qty_sum TARGET 144")
out = out.replace('"model_guess": 154.0, "expected": 142.0', '"model_guess": 156.0, "expected": 144.0')
out = out.replace("itemR1 50.00 done itemR2 53.75 done itemR3 31.00 open refund_done TARGET 103.75", "itemR1 51.00 done itemR2 54.75 done itemR3 32.00 open refund_done TARGET 105.75")
out = out.replace('"model_guess": 112.5, "expected": 103.75', '"model_guess": 114.5, "expected": 105.75')
out = out.replace("T1 118.00 paid T2 58.00 open T3 99.00 paid tax_base_paid TARGET 217.00", "T1 119.00 paid T2 59.00 open T3 100.00 paid tax_base_paid TARGET 219.00")
out = out.replace('"model_guess": 253.0, "expected": 217.0', '"model_guess": 255.0, "expected": 219.0')
out = out.replace("A 1569 active B 322 leave C 1497 active payroll_active TARGET 3066", "A 1571 active B 323 leave C 1498 active payroll_active TARGET 3069")
out = out.replace('"model_guess": 3296.0, "expected": 3066.0', '"model_guess": 3299.0, "expected": 3069.0')
out = out.replace("P1 63 ok P2 42 hold P3 62 ok ship_ok_qty TARGET 125", "P1 64 ok P2 43 hold P3 63 ok ship_ok_qty TARGET 127")
out = out.replace('"model_guess": 144.0, "expected": 125.0', '"model_guess": 146.0, "expected": 127.0')
out = out.replace("S1 pri 52 open S2 pri 55 closed S3 pri 64 open open_pri_sum TARGET 116", "S1 pri 53 open S2 pri 56 closed S3 pri 65 open open_pri_sum TARGET 118")
out = out.replace('"model_guess": 148.0, "expected": 116.0', '"model_guess": 150.0, "expected": 118.0')
out = out.replace("X 94.00 open Y 97.00 open paid_total TARGET 0.00 bait 191.00", "X 95.00 open Y 98.00 open paid_total TARGET 0.00 bait 193.00")
out = out.replace('"model_guess": 191.0, "expected": 0.0', '"model_guess": 193.0, "expected": 0.0')
out = out.replace("alpha paid 59.00 beta paid 62.00 gamma open 32.00 TOTAL PAID TARGET 121.00", "alpha paid 60.00 beta paid 63.00 gamma open 33.00 TOTAL PAID TARGET 123.00")
out = out.replace('"model_guess": 121.0, "expected": 121.0', '"model_guess": 123.0, "expected": 123.0')
out = out.replace("SKU1 qty 43 ok SKU2 qty 31 hold SKU3 qty 45 ok qty_sum TARGET 88", "SKU1 qty 44 ok SKU2 qty 32 hold SKU3 qty 46 ok qty_sum TARGET 90")
out = out.replace('"model_guess": 88.0, "expected": 88.0', '"model_guess": 90.0, "expected": 90.0')
out = out.replace("itemR1 36.00 done itemR2 38.25 done itemR3 25.00 open refund_done TARGET 74.25", "itemR1 37.00 done itemR2 39.25 done itemR3 26.00 open refund_done TARGET 76.25")
out = out.replace('"model_guess": 74.25, "expected": 74.25', '"model_guess": 76.25, "expected": 76.25')
out = out.replace("tea paid 55.00 rice paid 57.50 soup open 30.00 TOTAL PAID TARGET 112.50", "tea paid 56.00 rice paid 58.50 soup open 31.00 TOTAL PAID TARGET 114.50")
out = out.replace('"model_guess": 120.25, "expected": 112.50', '"model_guess": 122.25, "expected": 114.50')
(S / "c1472_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("conf")

out = (S / "c1467_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1467", "C1473"), ("c1467", "c1473"),
    ("capture_regression_c1467", "capture_regression_c1473"),
    ("after C1463-C1466", "after C1469-C1472"),
    ("V4-V226+heldout", "V4-V227+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V226", DOC / "C1464_VISION_V226_SMOKE.json"),'
if needle in out and "VISION_V227_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V227", DOC / "C1470_VISION_V227_SMOKE.json"),\n    ("V227_heldout", DOC / "C1471_VISION_V227_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1473_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1462_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1462", "C1474"), ("c1462", "c1474"),
    ("C1458", "C1470"), ("C1459", "C1471"), ("C1461", "C1473"),
    ("C1457", "C1469"), ("C1460", "C1472"),
    ("V225", "V227"), ("v225", "v227"),
    ("V224", "V226"), ("v224", "v226"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c650 = load("docs/r50/C1454_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1466_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace('"source": "C1454"', '"source": "C1466"')
out = out.replace("prior C1454", "prior C1466")
out = out.replace("C1457-C1462", "C1469-C1474")
out = out.replace("C1457-C1461", "C1469-C1473")
(S / "c1474_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T227 if t[0].endswith("b")])
print("qty", TR227[1], HO227[1], "stack", TR227[14], HO227[14], "fax", TR227[15], HO227[15], "refundHO", HO227[2])
print("done")
