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

# *vale ; qty TR 840+760 HO 740+780; PO TR 840+760 HO 780+740; SLA TR 480+520 HO 360+400
T197 = [
    ["ashvale","recv","paid_total","ASHVALE GRAIN RECV","RECV","x"],
    ["cedarvale","wh","qty_sum","WH CEDARVALE BIN","RECV","x"],
    ["dawnvale","refund","refund_done","DAWNVALE PATCH REFUND","DONE","x"],
    ["elmvale","tax","tax_base_paid","ELMVALE TAX SLIP","TAX","x"],
    ["fernvale","pay","payroll_active","FERNVALE PAYROLL","PAY","x"],
    ["glenvale","ship","ship_ok","GLENVALE SHIP DOCK","SHIP","x"],
    ["hazevale","sla","sla_ok_hours","HAZEVALE SLA CARD","SLA","x"],
    ["inkvale","exp","exp_sum","INKVALE EXPENSE","EXP","x"],
    ["jadevale","po","po_open","JADEVALE PO SHEET","PO","x"],
    ["knotvale","order","order_paid","KNOTVALE ORDER","ORD","x"],
    ["lakevale","dup","dup_mark","LAKEVALE DUP MARK","DUP","x"],
    ["mossvale","zero","zero_check","MOSSVALE AIR ZERO","ZERO","x"],
    ["nethervale","ledger","ledger_net","NETHERVALE LEDGER","LED","x"],
    ["oakvale","ui","ui_ok","OAKVALE UI SCAN","UI","x"],
    ["pinevale","stack","stack_count","PINEVALE STACK","STK","x"],
    ["quillvale","fax","fax_pages","QUILLVALE FAX","FAX","x"],
    ["reedvale","glare","glare_ok","REEDVALE GLARE","GLR","x"],
    ["stonevale","tab","tab_index","STONEVALE TAB INDEX","TAB","x"],
]
TR197 = [
    [1366.0, 1383.5, 1176.0],[840, 760, 820],[1289.0, 1318.25, 1156.0],[1422.0, 1439.0, 1246.0],
    [1484.0, 1508.0, 1216.0],[1242, 1258, 1174],[480.0, 520.0, 720.0],[1332.0, 1363.75, 1180.0],
    [840.0, 760.0, 820.0],[1399.0, 1387.0, 1177.0],[1,1,0],[0,0,0],
    [1465.0, 1486.5, 1202.0],[1,0,0],[1014, 1006, 984],[1032, 1016, 748],[1,0,0],[1058, 1034, 1004],
]
HO197 = [
    [1236.0, 1248.75, 1129.0],[740, 780, 820],[1194.0, 1207.5, 1117.0],[1309.0, 1325.0, 1158.0],
    [1350.0, 1366.0, 1153.0],[1144, 1158, 1122],[360.0, 400.0, 710.0],[1220.0, 1241.75, 1129.0],
    [780.0, 740.0, 820.0],[1267.0, 1253.0, 1124.0],[1,1,0],[0,0,0],
    [1302.0, 1317.5, 1139.0],[1,0,0],[991, 986, 981],[1006, 1000, 988],[1,0,0],[1016, 1010, 989],
]
check(TR197, "TR"); check(HO197, "HO")

(ROOT / "tools/_v197_themes.json").write_text(json.dumps({"themes": T197, "train": TR197, "heldout": HO197}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_197(src):
    src = src.replace("# --- V196 overlays (new vs V50) ---", "# --- V197 overlays (new vs V50) ---")
    src = src.replace("# --- V196 overlays (new vs V49) ---", "# --- V197 overlays (new vs V49) ---")
    for a, b in [
        ("ASHDALE bait 110.20", "ASHVALE bait 111.21"),
        ("CEDARD bait 112.22", "CEDARV bait 113.23"),
        ("DAWND ghost 35.35", "DAWNV ghost 36.36"),
        ("GLEND bait 105.15", "GLENV bait 106.16"),
        ("JADED bait 96.96", "JADEV bait 97.97"),
        ("NETHERD bait 113.23", "NETHERV bait 114.24"),
        ("ash mist + stone ticks (V196-only)", "ash mist + stone ticks (V197-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD196 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v196_themes.json").read_text(encoding="utf-8"))["themes"])
NEW197 = "_".join(t[0] for t in T197)

out = (S / "c1283_vision_v196_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1283", "C1289"), ("c1283", "c1289"), ("V196", "V197"), ("v196", "v197"),
    ("_v196c1283", "_v197c1289"),
    ("Harder than V195", "Harder than V196"), ("harder than V195", "harder than V196"),
    (OLD196, NEW197),
    ("V196 keeps floor", "V197 keeps floor"),
    ("C1283 design+fixtures; no VL claim", "C1289 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1284 VL smoke", "fixtures only; claim deferred to C1290 VL smoke"),
    ("No claim until C1284 VL", "No claim until C1290 VL"),
    ("kept on V196", "kept on V197"),
    ("vision_images_v196", "vision_images_v197"),
    ("VL_GATE_V196", "VL_GATE_V197"), ("vl_gate_v196", "vl_gate_v197"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V195:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V196: ashvale, cedarvale, dawnvale, elmvale, fernvale, glenvale, hazevale, inkvale,\njadevale, knotvale, lakevale, mossvale, nethervale, oakvale, pinevale, quillvale, reedvale, stonevale.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T197, "v197", "V197", TR197))
out = retarget_197(out)
(S / "c1289_vision_v197_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1284_vision_v196_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1284", "C1290"), ("c1284", "c1290"), ("V196", "V197"), ("v196", "v197"),
    ("vision_images_v196", "vision_images_v197"),
    ("VL_GATE_V196", "VL_GATE_V197"), ("vl_gate_v196", "vl_gate_v197"),
    ("runs/vision_v196", "runs/vision_v197"),
]:
    out = out.replace(a, b)
(S / "c1290_vision_v197_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1285_vision_v196_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1285", "C1291"), ("c1285", "c1291"), ("V196", "V197"), ("v196", "v197"),
    ("vision_images_v196h", "vision_images_v197h"),
    ("vision_images_v196", "vision_images_v197"),
    ("VL_GATE_V196", "VL_GATE_V197"), ("vl_gate_v196", "vl_gate_v197"),
    ("runs/vision_v196h", "runs/vision_v197h"),
    ("_v196c1283", "_v197c1289"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T197, "v197h", "V197H", HO197))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v197h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v197"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v197" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v197h_c1291"'); seen_run = True; continue
    out2.append(ln)
(S / "c1291_vision_v197_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1280_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1280", "C1292"), ("c1280", "c1292"),
    ("cg80_", "cg81_"),
    ("conf_gate_stretch_c1280", "conf_gate_stretch_c1292"),
    ("confidence_gate_stretch_v143", "confidence_gate_stretch_v144"),
    ("Stretch vs C1268", "Stretch vs C1280"),
]:
    out = out.replace(a, b)
out = out.replace("a paid 59.00 b paid 63.75 c open 19.00 TOTAL PAID TARGET 122.75", "a paid 60.00 b paid 64.75 c open 20.00 TOTAL PAID TARGET 124.75")
out = out.replace('"model_guess": 999.0, "expected": 122.75', '"model_guess": 999.0, "expected": 124.75')
out = out.replace("SKU1 qty 54 ok SKU2 qty 28 hold SKU3 qty 58 ok qty_sum TARGET 112", "SKU1 qty 55 ok SKU2 qty 29 hold SKU3 qty 59 ok qty_sum TARGET 114")
out = out.replace('"model_guess": 124.0, "expected": 112.0', '"model_guess": 126.0, "expected": 114.0')
out = out.replace("itemR1 35.00 done itemR2 38.75 done itemR3 16.00 open refund_done TARGET 73.75", "itemR1 36.00 done itemR2 39.75 done itemR3 17.00 open refund_done TARGET 75.75")
out = out.replace('"model_guess": 82.5, "expected": 73.75', '"model_guess": 84.5, "expected": 75.75')
out = out.replace("T1 103.00 paid T2 43.00 open T3 84.00 paid tax_base_paid TARGET 187.00", "T1 104.00 paid T2 44.00 open T3 85.00 paid tax_base_paid TARGET 189.00")
out = out.replace('"model_guess": 223.0, "expected": 187.0', '"model_guess": 225.0, "expected": 189.0')
out = out.replace("A 1552 active B 307 leave C 1482 active payroll_active TARGET 3034", "A 1553 active B 308 leave C 1483 active payroll_active TARGET 3036")
out = out.replace('"model_guess": 3264.0, "expected": 3034.0', '"model_guess": 3266.0, "expected": 3036.0')
out = out.replace("P1 48 ok P2 27 hold P3 47 ok ship_ok_qty TARGET 95", "P1 49 ok P2 28 hold P3 48 ok ship_ok_qty TARGET 97")
out = out.replace('"model_guess": 114.0, "expected": 95.0', '"model_guess": 116.0, "expected": 97.0')
out = out.replace("S1 pri 37 open S2 pri 40 closed S3 pri 49 open open_pri_sum TARGET 86", "S1 pri 38 open S2 pri 41 closed S3 pri 50 open open_pri_sum TARGET 88")
out = out.replace('"model_guess": 118.0, "expected": 86.0', '"model_guess": 120.0, "expected": 88.0')
out = out.replace("X 79.00 open Y 82.00 open paid_total TARGET 0.00 bait 161.00", "X 80.00 open Y 83.00 open paid_total TARGET 0.00 bait 163.00")
out = out.replace('"model_guess": 161.0, "expected": 0.0', '"model_guess": 163.0, "expected": 0.0')
out = out.replace("alpha paid 44.00 beta paid 47.00 gamma open 17.00 TOTAL PAID TARGET 91.00", "alpha paid 45.00 beta paid 48.00 gamma open 18.00 TOTAL PAID TARGET 93.00")
out = out.replace('"model_guess": 91.0, "expected": 91.0', '"model_guess": 93.0, "expected": 93.0')
out = out.replace("SKU1 qty 28 ok SKU2 qty 16 hold SKU3 qty 30 ok qty_sum TARGET 58", "SKU1 qty 29 ok SKU2 qty 17 hold SKU3 qty 31 ok qty_sum TARGET 60")
out = out.replace('"model_guess": 58.0, "expected": 58.0', '"model_guess": 60.0, "expected": 60.0')
out = out.replace("itemR1 21.00 done itemR2 23.25 done itemR3 10.00 open refund_done TARGET 44.25", "itemR1 22.00 done itemR2 24.25 done itemR3 11.00 open refund_done TARGET 46.25")
out = out.replace('"model_guess": 44.25, "expected": 44.25', '"model_guess": 46.25, "expected": 46.25')
out = out.replace("tea paid 40.00 rice paid 42.50 soup open 15.00 TOTAL PAID TARGET 82.50", "tea paid 41.00 rice paid 43.50 soup open 16.00 TOTAL PAID TARGET 84.50")
out = out.replace('"model_guess": 90.25, "expected": 82.50', '"model_guess": 92.25, "expected": 84.50')
(S / "c1292_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("conf")

out = (S / "c1287_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1287", "C1293"), ("c1287", "c1293"),
    ("capture_regression_c1287", "capture_regression_c1293"),
    ("after C1283-C1286", "after C1289-C1292"),
    ("V4-V196+heldout", "V4-V197+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V196", DOC / "C1284_VISION_V196_SMOKE.json"),'
if needle in out and "VISION_V197_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V197", DOC / "C1290_VISION_V197_SMOKE.json"),\n    ("V197_heldout", DOC / "C1291_VISION_V197_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1293_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1282_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1282", "C1294"), ("c1282", "c1294"),
    ("C1278", "C1290"), ("C1279", "C1291"), ("C1281", "C1293"),
    ("C1277", "C1289"), ("C1280", "C1292"),
    ("V195", "V197"), ("v195", "v197"),
    ("V194", "V196"), ("v194", "v196"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c650 = load("docs/r50/C1274_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1286_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace('"source": "C1274"', '"source": "C1286"')
out = out.replace("prior C1274", "prior C1286")
out = out.replace("C1277-C1282", "C1289-C1294")
out = out.replace("C1277-C1281", "C1289-C1293")
(S / "c1294_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T197 if t[0].endswith("b")])
print("qty", TR197[1], HO197[1], "po", TR197[8], HO197[8], "sla", TR197[6], HO197[6], "fax", TR197[15], HO197[15])
print("done")
