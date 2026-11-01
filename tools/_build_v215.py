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

# *moor ; qty TR 840+760 HO 740+780; PO TR 840+760 HO 780+740; SLA TR 480+520 HO 360+400
T215 = [
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
TR215 = [
    [1564.0, 1581.5, 1366.0],[840, 760, 820],[1487.0, 1516.25, 1346.0],[1620.0, 1637.0, 1436.0],
    [1682.0, 1706.0, 1406.0],[1440, 1456, 1364],[480.0, 520.0, 740.0],[1530.0, 1561.75, 1370.0],
    [840.0, 760.0, 820.0],[1597.0, 1585.0, 1367.0],[1,1,0],[0,0,0],
    [1663.0, 1684.5, 1392.0],[1,0,0],[1204, 1196, 1174],[1222, 1206, 748],[1,0,0],[1248, 1224, 1194],
]
HO215 = [
    [1426.0, 1438.75, 1311.0],[740, 780, 820],[1384.0, 1397.5, 1299.0],[1499.0, 1515.0, 1340.0],
    [1540.0, 1556.0, 1335.0],[1334, 1348, 1304],[360.0, 400.0, 730.0],[1410.0, 1431.75, 1311.0],
    [780.0, 740.0, 820.0],[1457.0, 1443.0, 1306.0],[1,1,0],[0,0,0],
    [1492.0, 1507.5, 1321.0],[1,0,0],[1173, 1168, 1163],[1188, 1182, 1170],[1,0,0],[1198, 1192, 1171],
]
check(TR215, "TR"); check(HO215, "HO")

(ROOT / "tools/_v215_themes.json").write_text(json.dumps({"themes": T215, "train": TR215, "heldout": HO215}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_215(src):
    src = src.replace("# --- V214 overlays (new vs V50) ---", "# --- V215 overlays (new vs V50) ---")
    src = src.replace("# --- V214 overlays (new vs V49) ---", "# --- V215 overlays (new vs V49) ---")
    for a, b in [
        ("ASHHURST bait 128.38", "ASHMOOR bait 129.39"),
        ("CEDARH bait 130.40", "CEDARM bait 131.41"),
        ("DAWNH ghost 53.53", "DAWNM ghost 54.54"),
        ("GLENH bait 123.33", "GLENM bait 124.34"),
        ("JADEH bait 114.24", "JADEM bait 115.25"),
        ("NETHERH bait 131.41", "NETHERM bait 132.42"),
        ("ash mist + stone ticks (V214-only)", "ash mist + stone ticks (V215-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD214 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v214_themes.json").read_text(encoding="utf-8"))["themes"])
NEW215 = "_".join(t[0] for t in T215)

out = (S / "c1391_vision_v214_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1391", "C1397"), ("c1391", "c1397"), ("V214", "V215"), ("v214", "v215"),
    ("_v214c1391", "_v215c1397"),
    ("Harder than V213", "Harder than V214"), ("harder than V213", "harder than V214"),
    (OLD214, NEW215),
    ("V214 keeps floor", "V215 keeps floor"),
    ("C1391 design+fixtures; no VL claim", "C1397 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1392 VL smoke", "fixtures only; claim deferred to C1398 VL smoke"),
    ("No claim until C1392 VL", "No claim until C1398 VL"),
    ("kept on V214", "kept on V215"),
    ("vision_images_v214", "vision_images_v215"),
    ("VL_GATE_V214", "VL_GATE_V215"), ("vl_gate_v214", "vl_gate_v215"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V213:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V214: ashmoor, cedarmoor, dawnmoor, elmmoor, fernmoor, glenmoor, hazemoor, inkmoor,\njademoor, knotmoor, lakemoor, mossmoor, nethermoor, oakmoor, pinemoor, quillmoor, reedmoor, stonemoor.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T215, "v215", "V215", TR215))
out = retarget_215(out)
(S / "c1397_vision_v215_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1392_vision_v214_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1392", "C1398"), ("c1392", "c1398"), ("V214", "V215"), ("v214", "v215"),
    ("vision_images_v214", "vision_images_v215"),
    ("VL_GATE_V214", "VL_GATE_V215"), ("vl_gate_v214", "vl_gate_v215"),
    ("runs/vision_v214", "runs/vision_v215"),
]:
    out = out.replace(a, b)
(S / "c1398_vision_v215_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1393_vision_v214_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1393", "C1399"), ("c1393", "c1399"), ("V214", "V215"), ("v214", "v215"),
    ("vision_images_v214h", "vision_images_v215h"),
    ("vision_images_v214", "vision_images_v215"),
    ("VL_GATE_V214", "VL_GATE_V215"), ("vl_gate_v214", "vl_gate_v215"),
    ("runs/vision_v214h", "runs/vision_v215h"),
    ("_v214c1391", "_v215c1397"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T215, "v215h", "V215H", HO215))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v215h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v215"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v215" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v215h_c1399"'); seen_run = True; continue
    out2.append(ln)
(S / "c1399_vision_v215_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1388_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1388", "C1400"), ("c1388", "c1400"),
    ("cg89_", "cg90_"),
    ("conf_gate_stretch_c1388", "conf_gate_stretch_c1400"),
    ("confidence_gate_stretch_v152", "confidence_gate_stretch_v153"),
    ("Stretch vs C1376", "Stretch vs C1388"),
]:
    out = out.replace(a, b)
out = out.replace("a paid 68.00 b paid 72.75 c open 28.00 TOTAL PAID TARGET 140.75", "a paid 69.00 b paid 73.75 c open 29.00 TOTAL PAID TARGET 142.75")
out = out.replace('"model_guess": 999.0, "expected": 140.75', '"model_guess": 999.0, "expected": 142.75')
out = out.replace("SKU1 qty 63 ok SKU2 qty 37 hold SKU3 qty 67 ok qty_sum TARGET 130", "SKU1 qty 64 ok SKU2 qty 38 hold SKU3 qty 68 ok qty_sum TARGET 132")
out = out.replace('"model_guess": 142.0, "expected": 130.0', '"model_guess": 144.0, "expected": 132.0')
out = out.replace("itemR1 44.00 done itemR2 47.75 done itemR3 25.00 open refund_done TARGET 91.75", "itemR1 45.00 done itemR2 48.75 done itemR3 26.00 open refund_done TARGET 93.75")
out = out.replace('"model_guess": 100.5, "expected": 91.75', '"model_guess": 102.5, "expected": 93.75')
out = out.replace("T1 112.00 paid T2 52.00 open T3 93.00 paid tax_base_paid TARGET 205.00", "T1 113.00 paid T2 53.00 open T3 94.00 paid tax_base_paid TARGET 207.00")
out = out.replace('"model_guess": 241.0, "expected": 205.0', '"model_guess": 243.0, "expected": 207.0')
out = out.replace("A 1562 active B 316 leave C 1491 active payroll_active TARGET 3053", "A 1563 active B 317 leave C 1492 active payroll_active TARGET 3055")
out = out.replace('"model_guess": 3283.0, "expected": 3053.0', '"model_guess": 3285.0, "expected": 3055.0')
out = out.replace("P1 57 ok P2 36 hold P3 56 ok ship_ok_qty TARGET 113", "P1 58 ok P2 37 hold P3 57 ok ship_ok_qty TARGET 115")
out = out.replace('"model_guess": 132.0, "expected": 113.0', '"model_guess": 134.0, "expected": 115.0')
out = out.replace("S1 pri 46 open S2 pri 49 closed S3 pri 58 open open_pri_sum TARGET 104", "S1 pri 47 open S2 pri 50 closed S3 pri 59 open open_pri_sum TARGET 106")
out = out.replace('"model_guess": 136.0, "expected": 104.0', '"model_guess": 138.0, "expected": 106.0')
out = out.replace("X 88.00 open Y 91.00 open paid_total TARGET 0.00 bait 179.00", "X 89.00 open Y 92.00 open paid_total TARGET 0.00 bait 181.00")
out = out.replace('"model_guess": 179.0, "expected": 0.0', '"model_guess": 181.0, "expected": 0.0')
out = out.replace("alpha paid 53.00 beta paid 56.00 gamma open 26.00 TOTAL PAID TARGET 109.00", "alpha paid 54.00 beta paid 57.00 gamma open 27.00 TOTAL PAID TARGET 111.00")
out = out.replace('"model_guess": 109.0, "expected": 109.0', '"model_guess": 111.0, "expected": 111.0')
out = out.replace("SKU1 qty 37 ok SKU2 qty 25 hold SKU3 qty 39 ok qty_sum TARGET 76", "SKU1 qty 38 ok SKU2 qty 26 hold SKU3 qty 40 ok qty_sum TARGET 78")
out = out.replace('"model_guess": 76.0, "expected": 76.0', '"model_guess": 78.0, "expected": 78.0')
out = out.replace("itemR1 30.00 done itemR2 32.25 done itemR3 19.00 open refund_done TARGET 62.25", "itemR1 31.00 done itemR2 33.25 done itemR3 20.00 open refund_done TARGET 64.25")
out = out.replace('"model_guess": 62.25, "expected": 62.25', '"model_guess": 64.25, "expected": 64.25')
out = out.replace("tea paid 49.00 rice paid 51.50 soup open 24.00 TOTAL PAID TARGET 100.50", "tea paid 50.00 rice paid 52.50 soup open 25.00 TOTAL PAID TARGET 102.50")
out = out.replace('"model_guess": 108.25, "expected": 100.50', '"model_guess": 110.25, "expected": 102.50')
(S / "c1400_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("conf")

out = (S / "c1395_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1395", "C1401"), ("c1395", "c1401"),
    ("capture_regression_c1395", "capture_regression_c1401"),
    ("after C1391-C1394", "after C1397-C1400"),
    ("V4-V214+heldout", "V4-V215+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V214", DOC / "C1392_VISION_V214_SMOKE.json"),'
if needle in out and "VISION_V215_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V215", DOC / "C1398_VISION_V215_SMOKE.json"),\n    ("V215_heldout", DOC / "C1399_VISION_V215_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1401_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1390_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1390", "C1402"), ("c1390", "c1402"),
    ("C1386", "C1398"), ("C1387", "C1399"), ("C1389", "C1401"),
    ("C1385", "C1397"), ("C1388", "C1400"),
    ("V213", "V215"), ("v213", "v215"),
    ("V212", "V214"), ("v212", "v214"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c650 = load("docs/r50/C1382_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1394_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace('"source": "C1382"', '"source": "C1394"')
out = out.replace("prior C1382", "prior C1394")
out = out.replace("C1385-C1390", "C1397-C1402")
out = out.replace("C1385-C1389", "C1397-C1401")
(S / "c1402_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T215 if t[0].endswith("b")])
print("qty", TR215[1], HO215[1], "po", TR215[8], HO215[8], "sla", TR215[6], HO215[6], "fax", TR215[15], HO215[15])
print("done")
