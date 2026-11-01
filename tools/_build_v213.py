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

# *croft ; qty TR 840+760 HO 740+780; PO TR 840+760 HO 780+740; SLA TR 480+520 HO 360+400
T213 = [
    ["ashcroft","recv","paid_total","ASHCROFT GRAIN RECV","RECV","x"],
    ["cedarcroft","wh","qty_sum","WH CEDARCROFT BIN","RECV","x"],
    ["dawncroft","refund","refund_done","DAWNCROFT PATCH REFUND","DONE","x"],
    ["elmcroft","tax","tax_base_paid","ELMCROFT TAX SLIP","TAX","x"],
    ["ferncroft","pay","payroll_active","FERNCROFT PAYROLL","PAY","x"],
    ["glencroft","ship","ship_ok","GLENCROFT SHIP DOCK","SHIP","x"],
    ["hazecroft","sla","sla_ok_hours","HAZECROFT SLA CARD","SLA","x"],
    ["inkcroft","exp","exp_sum","INKCROFT EXPENSE","EXP","x"],
    ["jadecroft","po","po_open","JADECROFT PO SHEET","PO","x"],
    ["knotcroft","order","order_paid","KNOTCROFT ORDER","ORD","x"],
    ["lakecroft","dup","dup_mark","LAKECROFT DUP MARK","DUP","x"],
    ["mosscroft","zero","zero_check","MOSSCROFT AIR ZERO","ZERO","x"],
    ["nethercroft","ledger","ledger_net","NETHERCROFT LEDGER","LED","x"],
    ["oakcroft","ui","ui_ok","OAKCROFT UI SCAN","UI","x"],
    ["pinecroft","stack","stack_count","PINECROFT STACK","STK","x"],
    ["quillcroft","fax","fax_pages","QUILLCROFT FAX","FAX","x"],
    ["reedcroft","glare","glare_ok","REEDCROFT GLARE","GLR","x"],
    ["stonecroft","tab","tab_index","STONECROFT TAB INDEX","TAB","x"],
]
TR213 = [
    [1528.0, 1545.5, 1334.0],[840, 760, 820],[1451.0, 1480.25, 1314.0],[1584.0, 1601.0, 1404.0],
    [1646.0, 1670.0, 1374.0],[1404, 1420, 1332],[480.0, 520.0, 740.0],[1494.0, 1525.75, 1338.0],
    [840.0, 760.0, 820.0],[1561.0, 1549.0, 1335.0],[1,1,0],[0,0,0],
    [1627.0, 1648.5, 1360.0],[1,0,0],[1172, 1164, 1142],[1190, 1174, 748],[1,0,0],[1216, 1192, 1162],
]
HO213 = [
    [1394.0, 1406.75, 1283.0],[740, 780, 820],[1352.0, 1365.5, 1271.0],[1467.0, 1483.0, 1312.0],
    [1508.0, 1524.0, 1307.0],[1302, 1316, 1276],[360.0, 400.0, 730.0],[1378.0, 1399.75, 1283.0],
    [780.0, 740.0, 820.0],[1425.0, 1411.0, 1278.0],[1,1,0],[0,0,0],
    [1460.0, 1475.5, 1293.0],[1,0,0],[1145, 1140, 1135],[1160, 1154, 1142],[1,0,0],[1170, 1164, 1143],
]
check(TR213, "TR"); check(HO213, "HO")

(ROOT / "tools/_v213_themes.json").write_text(json.dumps({"themes": T213, "train": TR213, "heldout": HO213}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_213(src):
    src = src.replace("# --- V212 overlays (new vs V50) ---", "# --- V213 overlays (new vs V50) ---")
    src = src.replace("# --- V212 overlays (new vs V49) ---", "# --- V213 overlays (new vs V49) ---")
    for a, b in [
        ("ASHWICK bait 126.36", "ASHCROFT bait 127.37"),
        ("CEDARW bait 128.38", "CEDARC bait 129.39"),
        ("DAWNW ghost 51.51", "DAWNC ghost 52.52"),
        ("GLENW bait 121.31", "GLENC bait 122.32"),
        ("JADEW bait 112.22", "JADEC bait 113.23"),
        ("NETHERW bait 129.39", "NETHERC bait 130.40"),
        ("ash mist + stone ticks (V212-only)", "ash mist + stone ticks (V213-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD212 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v212_themes.json").read_text(encoding="utf-8"))["themes"])
NEW213 = "_".join(t[0] for t in T213)

out = (S / "c1379_vision_v212_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1379", "C1385"), ("c1379", "c1385"), ("V212", "V213"), ("v212", "v213"),
    ("_v212c1379", "_v213c1385"),
    ("Harder than V211", "Harder than V212"), ("harder than V211", "harder than V212"),
    (OLD212, NEW213),
    ("V212 keeps floor", "V213 keeps floor"),
    ("C1379 design+fixtures; no VL claim", "C1385 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1380 VL smoke", "fixtures only; claim deferred to C1386 VL smoke"),
    ("No claim until C1380 VL", "No claim until C1386 VL"),
    ("kept on V212", "kept on V213"),
    ("vision_images_v212", "vision_images_v213"),
    ("VL_GATE_V212", "VL_GATE_V213"), ("vl_gate_v212", "vl_gate_v213"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V211:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V212: ashcroft, cedarcroft, dawncroft, elmcroft, ferncroft, glencroft, hazecroft, inkcroft,\njadecroft, knotcroft, lakecroft, mosscroft, nethercroft, oakcroft, pinecroft, quillcroft, reedcroft, stonecroft.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T213, "v213", "V213", TR213))
out = retarget_213(out)
(S / "c1385_vision_v213_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1380_vision_v212_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1380", "C1386"), ("c1380", "c1386"), ("V212", "V213"), ("v212", "v213"),
    ("vision_images_v212", "vision_images_v213"),
    ("VL_GATE_V212", "VL_GATE_V213"), ("vl_gate_v212", "vl_gate_v213"),
    ("runs/vision_v212", "runs/vision_v213"),
]:
    out = out.replace(a, b)
(S / "c1386_vision_v213_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1381_vision_v212_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1381", "C1387"), ("c1381", "c1387"), ("V212", "V213"), ("v212", "v213"),
    ("vision_images_v212h", "vision_images_v213h"),
    ("vision_images_v212", "vision_images_v213"),
    ("VL_GATE_V212", "VL_GATE_V213"), ("vl_gate_v212", "vl_gate_v213"),
    ("runs/vision_v212h", "runs/vision_v213h"),
    ("_v212c1379", "_v213c1385"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T213, "v213h", "V213H", HO213))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v213h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v213"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v213" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v213h_c1387"'); seen_run = True; continue
    out2.append(ln)
(S / "c1387_vision_v213_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1376_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1376", "C1388"), ("c1376", "c1388"),
    ("cg88_", "cg89_"),
    ("conf_gate_stretch_c1376", "conf_gate_stretch_c1388"),
    ("confidence_gate_stretch_v151", "confidence_gate_stretch_v152"),
    ("Stretch vs C1364", "Stretch vs C1376"),
]:
    out = out.replace(a, b)
out = out.replace("a paid 67.00 b paid 71.75 c open 27.00 TOTAL PAID TARGET 138.75", "a paid 68.00 b paid 72.75 c open 28.00 TOTAL PAID TARGET 140.75")
out = out.replace('"model_guess": 999.0, "expected": 138.75', '"model_guess": 999.0, "expected": 140.75')
out = out.replace("SKU1 qty 62 ok SKU2 qty 36 hold SKU3 qty 66 ok qty_sum TARGET 128", "SKU1 qty 63 ok SKU2 qty 37 hold SKU3 qty 67 ok qty_sum TARGET 130")
out = out.replace('"model_guess": 140.0, "expected": 128.0', '"model_guess": 142.0, "expected": 130.0')
out = out.replace("itemR1 43.00 done itemR2 46.75 done itemR3 24.00 open refund_done TARGET 89.75", "itemR1 44.00 done itemR2 47.75 done itemR3 25.00 open refund_done TARGET 91.75")
out = out.replace('"model_guess": 98.5, "expected": 89.75', '"model_guess": 100.5, "expected": 91.75')
out = out.replace("T1 111.00 paid T2 51.00 open T3 92.00 paid tax_base_paid TARGET 203.00", "T1 112.00 paid T2 52.00 open T3 93.00 paid tax_base_paid TARGET 205.00")
out = out.replace('"model_guess": 239.0, "expected": 203.0', '"model_guess": 241.0, "expected": 205.0')
out = out.replace("A 1561 active B 315 leave C 1490 active payroll_active TARGET 3051", "A 1562 active B 316 leave C 1491 active payroll_active TARGET 3053")
out = out.replace('"model_guess": 3281.0, "expected": 3051.0', '"model_guess": 3283.0, "expected": 3053.0')
out = out.replace("P1 56 ok P2 35 hold P3 55 ok ship_ok_qty TARGET 111", "P1 57 ok P2 36 hold P3 56 ok ship_ok_qty TARGET 113")
out = out.replace('"model_guess": 130.0, "expected": 111.0', '"model_guess": 132.0, "expected": 113.0')
out = out.replace("S1 pri 45 open S2 pri 48 closed S3 pri 57 open open_pri_sum TARGET 102", "S1 pri 46 open S2 pri 49 closed S3 pri 58 open open_pri_sum TARGET 104")
out = out.replace('"model_guess": 134.0, "expected": 102.0', '"model_guess": 136.0, "expected": 104.0')
out = out.replace("X 87.00 open Y 90.00 open paid_total TARGET 0.00 bait 177.00", "X 88.00 open Y 91.00 open paid_total TARGET 0.00 bait 179.00")
out = out.replace('"model_guess": 177.0, "expected": 0.0', '"model_guess": 179.0, "expected": 0.0')
out = out.replace("alpha paid 52.00 beta paid 55.00 gamma open 25.00 TOTAL PAID TARGET 107.00", "alpha paid 53.00 beta paid 56.00 gamma open 26.00 TOTAL PAID TARGET 109.00")
out = out.replace('"model_guess": 107.0, "expected": 107.0', '"model_guess": 109.0, "expected": 109.0')
out = out.replace("SKU1 qty 36 ok SKU2 qty 24 hold SKU3 qty 38 ok qty_sum TARGET 74", "SKU1 qty 37 ok SKU2 qty 25 hold SKU3 qty 39 ok qty_sum TARGET 76")
out = out.replace('"model_guess": 74.0, "expected": 74.0', '"model_guess": 76.0, "expected": 76.0')
out = out.replace("itemR1 29.00 done itemR2 31.25 done itemR3 18.00 open refund_done TARGET 60.25", "itemR1 30.00 done itemR2 32.25 done itemR3 19.00 open refund_done TARGET 62.25")
out = out.replace('"model_guess": 60.25, "expected": 60.25', '"model_guess": 62.25, "expected": 62.25')
out = out.replace("tea paid 48.00 rice paid 50.50 soup open 23.00 TOTAL PAID TARGET 98.50", "tea paid 49.00 rice paid 51.50 soup open 24.00 TOTAL PAID TARGET 100.50")
out = out.replace('"model_guess": 106.25, "expected": 98.50', '"model_guess": 108.25, "expected": 100.50')
(S / "c1388_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("conf")

out = (S / "c1383_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1383", "C1389"), ("c1383", "c1389"),
    ("capture_regression_c1383", "capture_regression_c1389"),
    ("after C1379-C1382", "after C1385-C1388"),
    ("V4-V212+heldout", "V4-V213+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V212", DOC / "C1380_VISION_V212_SMOKE.json"),'
if needle in out and "VISION_V213_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V213", DOC / "C1386_VISION_V213_SMOKE.json"),\n    ("V213_heldout", DOC / "C1387_VISION_V213_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1389_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1378_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1378", "C1390"), ("c1378", "c1390"),
    ("C1374", "C1386"), ("C1375", "C1387"), ("C1377", "C1389"),
    ("C1373", "C1385"), ("C1376", "C1388"),
    ("V211", "V213"), ("v211", "v213"),
    ("V210", "V212"), ("v210", "v212"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c650 = load("docs/r50/C1370_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1382_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace('"source": "C1370"', '"source": "C1382"')
out = out.replace("prior C1370", "prior C1382")
out = out.replace("C1373-C1378", "C1385-C1390")
out = out.replace("C1373-C1377", "C1385-C1389")
(S / "c1390_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T213 if t[0].endswith("b")])
print("qty", TR213[1], HO213[1], "po", TR213[8], HO213[8], "sla", TR213[6], HO213[6], "fax", TR213[15], HO213[15])
print("done")
