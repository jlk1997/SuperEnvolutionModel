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

# *mere ; qty TR 840+760 HO 740+780; PO TR 840+760 HO 780+740; SLA TR 480+520 HO 360+400
T211 = [
    ["ashmere","recv","paid_total","ASHMERE GRAIN RECV","RECV","x"],
    ["cedarmere","wh","qty_sum","WH CEDARMERE BIN","RECV","x"],
    ["dawnmere","refund","refund_done","DAWNMERE PATCH REFUND","DONE","x"],
    ["elmmere","tax","tax_base_paid","ELMMERE TAX SLIP","TAX","x"],
    ["fernmere","pay","payroll_active","FERNMERE PAYROLL","PAY","x"],
    ["glenmere","ship","ship_ok","GLENMERE SHIP DOCK","SHIP","x"],
    ["hazemere","sla","sla_ok_hours","HAZEMERE SLA CARD","SLA","x"],
    ["inkmere","exp","exp_sum","INKMERE EXPENSE","EXP","x"],
    ["jademere","po","po_open","JADEMERE PO SHEET","PO","x"],
    ["knotmere","order","order_paid","KNOTMERE ORDER","ORD","x"],
    ["lakemere","dup","dup_mark","LAKEMERE DUP MARK","DUP","x"],
    ["mossmere","zero","zero_check","MOSSMERE AIR ZERO","ZERO","x"],
    ["nethermere","ledger","ledger_net","NETHERMERE LEDGER","LED","x"],
    ["oakmere","ui","ui_ok","OAKMERE UI SCAN","UI","x"],
    ["pinemere","stack","stack_count","PINEMERE STACK","STK","x"],
    ["quillmere","fax","fax_pages","QUILLMERE FAX","FAX","x"],
    ["reedmere","glare","glare_ok","REEDMERE GLARE","GLR","x"],
    ["stonemere","tab","tab_index","STONEMERE TAB INDEX","TAB","x"],
]
TR211 = [
    [1492.0, 1509.5, 1302.0],[840, 760, 820],[1415.0, 1444.25, 1282.0],[1548.0, 1565.0, 1372.0],
    [1610.0, 1634.0, 1342.0],[1368, 1384, 1300],[480.0, 520.0, 740.0],[1458.0, 1489.75, 1306.0],
    [840.0, 760.0, 820.0],[1525.0, 1513.0, 1303.0],[1,1,0],[0,0,0],
    [1591.0, 1612.5, 1328.0],[1,0,0],[1140, 1132, 1110],[1158, 1142, 748],[1,0,0],[1184, 1160, 1130],
]
HO211 = [
    [1362.0, 1374.75, 1255.0],[740, 780, 820],[1320.0, 1333.5, 1243.0],[1435.0, 1451.0, 1284.0],
    [1476.0, 1492.0, 1279.0],[1270, 1284, 1248],[360.0, 400.0, 730.0],[1346.0, 1367.75, 1255.0],
    [780.0, 740.0, 820.0],[1393.0, 1379.0, 1250.0],[1,1,0],[0,0,0],
    [1428.0, 1443.5, 1265.0],[1,0,0],[1117, 1112, 1107],[1132, 1126, 1114],[1,0,0],[1142, 1136, 1115],
]
check(TR211, "TR"); check(HO211, "HO")

(ROOT / "tools/_v211_themes.json").write_text(json.dumps({"themes": T211, "train": TR211, "heldout": HO211}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_211(src):
    src = src.replace("# --- V210 overlays (new vs V50) ---", "# --- V211 overlays (new vs V50) ---")
    src = src.replace("# --- V210 overlays (new vs V49) ---", "# --- V211 overlays (new vs V49) ---")
    for a, b in [
        ("ASHHOLM bait 124.34", "ASHMERE bait 125.35"),
        ("CEDARH bait 126.36", "CEDARM bait 127.37"),
        ("DAWNH ghost 49.49", "DAWNM ghost 50.50"),
        ("GLENH bait 119.29", "GLENM bait 120.30"),
        ("JADEH bait 110.20", "JADEM bait 111.21"),
        ("NETHERH bait 127.37", "NETHERM bait 128.38"),
        ("ash mist + stone ticks (V210-only)", "ash mist + stone ticks (V211-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD210 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v210_themes.json").read_text(encoding="utf-8"))["themes"])
NEW211 = "_".join(t[0] for t in T211)

out = (S / "c1367_vision_v210_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1367", "C1373"), ("c1367", "c1373"), ("V210", "V211"), ("v210", "v211"),
    ("_v210c1367", "_v211c1373"),
    ("Harder than V209", "Harder than V210"), ("harder than V209", "harder than V210"),
    (OLD210, NEW211),
    ("V210 keeps floor", "V211 keeps floor"),
    ("C1367 design+fixtures; no VL claim", "C1373 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1368 VL smoke", "fixtures only; claim deferred to C1374 VL smoke"),
    ("No claim until C1368 VL", "No claim until C1374 VL"),
    ("kept on V210", "kept on V211"),
    ("vision_images_v210", "vision_images_v211"),
    ("VL_GATE_V210", "VL_GATE_V211"), ("vl_gate_v210", "vl_gate_v211"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V209:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V210: ashmere, cedarmere, dawnmere, elmmere, fernmere, glenmere, hazemere, inkmere,\njademere, knotmere, lakemere, mossmere, nethermere, oakmere, pinemere, quillmere, reedmere, stonemere.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T211, "v211", "V211", TR211))
out = retarget_211(out)
(S / "c1373_vision_v211_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1368_vision_v210_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1368", "C1374"), ("c1368", "c1374"), ("V210", "V211"), ("v210", "v211"),
    ("vision_images_v210", "vision_images_v211"),
    ("VL_GATE_V210", "VL_GATE_V211"), ("vl_gate_v210", "vl_gate_v211"),
    ("runs/vision_v210", "runs/vision_v211"),
]:
    out = out.replace(a, b)
(S / "c1374_vision_v211_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1369_vision_v210_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1369", "C1375"), ("c1369", "c1375"), ("V210", "V211"), ("v210", "v211"),
    ("vision_images_v210h", "vision_images_v211h"),
    ("vision_images_v210", "vision_images_v211"),
    ("VL_GATE_V210", "VL_GATE_V211"), ("vl_gate_v210", "vl_gate_v211"),
    ("runs/vision_v210h", "runs/vision_v211h"),
    ("_v210c1367", "_v211c1373"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T211, "v211h", "V211H", HO211))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v211h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v211"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v211" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v211h_c1375"'); seen_run = True; continue
    out2.append(ln)
(S / "c1375_vision_v211_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1364_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1364", "C1376"), ("c1364", "c1376"),
    ("cg87_", "cg88_"),
    ("conf_gate_stretch_c1364", "conf_gate_stretch_c1376"),
    ("confidence_gate_stretch_v150", "confidence_gate_stretch_v151"),
    ("Stretch vs C1352", "Stretch vs C1364"),
]:
    out = out.replace(a, b)
out = out.replace("a paid 66.00 b paid 70.75 c open 26.00 TOTAL PAID TARGET 136.75", "a paid 67.00 b paid 71.75 c open 27.00 TOTAL PAID TARGET 138.75")
out = out.replace('"model_guess": 999.0, "expected": 136.75', '"model_guess": 999.0, "expected": 138.75')
out = out.replace("SKU1 qty 61 ok SKU2 qty 35 hold SKU3 qty 65 ok qty_sum TARGET 126", "SKU1 qty 62 ok SKU2 qty 36 hold SKU3 qty 66 ok qty_sum TARGET 128")
out = out.replace('"model_guess": 138.0, "expected": 126.0', '"model_guess": 140.0, "expected": 128.0')
out = out.replace("itemR1 42.00 done itemR2 45.75 done itemR3 23.00 open refund_done TARGET 87.75", "itemR1 43.00 done itemR2 46.75 done itemR3 24.00 open refund_done TARGET 89.75")
out = out.replace('"model_guess": 96.5, "expected": 87.75', '"model_guess": 98.5, "expected": 89.75')
out = out.replace("T1 110.00 paid T2 50.00 open T3 91.00 paid tax_base_paid TARGET 201.00", "T1 111.00 paid T2 51.00 open T3 92.00 paid tax_base_paid TARGET 203.00")
out = out.replace('"model_guess": 237.0, "expected": 201.0', '"model_guess": 239.0, "expected": 203.0')
out = out.replace("A 1559 active B 314 leave C 1489 active payroll_active TARGET 3048", "A 1561 active B 315 leave C 1490 active payroll_active TARGET 3051")
out = out.replace('"model_guess": 3278.0, "expected": 3048.0', '"model_guess": 3281.0, "expected": 3051.0')
out = out.replace("P1 55 ok P2 34 hold P3 54 ok ship_ok_qty TARGET 109", "P1 56 ok P2 35 hold P3 55 ok ship_ok_qty TARGET 111")
out = out.replace('"model_guess": 128.0, "expected": 109.0', '"model_guess": 130.0, "expected": 111.0')
out = out.replace("S1 pri 44 open S2 pri 47 closed S3 pri 56 open open_pri_sum TARGET 100", "S1 pri 45 open S2 pri 48 closed S3 pri 57 open open_pri_sum TARGET 102")
out = out.replace('"model_guess": 132.0, "expected": 100.0', '"model_guess": 134.0, "expected": 102.0')
out = out.replace("X 86.00 open Y 89.00 open paid_total TARGET 0.00 bait 175.00", "X 87.00 open Y 90.00 open paid_total TARGET 0.00 bait 177.00")
out = out.replace('"model_guess": 175.0, "expected": 0.0', '"model_guess": 177.0, "expected": 0.0')
out = out.replace("alpha paid 51.00 beta paid 54.00 gamma open 24.00 TOTAL PAID TARGET 105.00", "alpha paid 52.00 beta paid 55.00 gamma open 25.00 TOTAL PAID TARGET 107.00")
out = out.replace('"model_guess": 105.0, "expected": 105.0', '"model_guess": 107.0, "expected": 107.0')
out = out.replace("SKU1 qty 35 ok SKU2 qty 23 hold SKU3 qty 37 ok qty_sum TARGET 72", "SKU1 qty 36 ok SKU2 qty 24 hold SKU3 qty 38 ok qty_sum TARGET 74")
out = out.replace('"model_guess": 72.0, "expected": 72.0', '"model_guess": 74.0, "expected": 74.0')
out = out.replace("itemR1 28.00 done itemR2 30.25 done itemR3 17.00 open refund_done TARGET 58.25", "itemR1 29.00 done itemR2 31.25 done itemR3 18.00 open refund_done TARGET 60.25")
out = out.replace('"model_guess": 58.25, "expected": 58.25', '"model_guess": 60.25, "expected": 60.25')
out = out.replace("tea paid 47.00 rice paid 49.50 soup open 22.00 TOTAL PAID TARGET 96.50", "tea paid 48.00 rice paid 50.50 soup open 23.00 TOTAL PAID TARGET 98.50")
out = out.replace('"model_guess": 104.25, "expected": 96.50', '"model_guess": 106.25, "expected": 98.50')
(S / "c1376_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("conf")

out = (S / "c1371_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1371", "C1377"), ("c1371", "c1377"),
    ("capture_regression_c1371", "capture_regression_c1377"),
    ("after C1367-C1370", "after C1373-C1376"),
    ("V4-V210+heldout", "V4-V211+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V210", DOC / "C1368_VISION_V210_SMOKE.json"),'
if needle in out and "VISION_V211_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V211", DOC / "C1374_VISION_V211_SMOKE.json"),\n    ("V211_heldout", DOC / "C1375_VISION_V211_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1377_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1366_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1366", "C1378"), ("c1366", "c1378"),
    ("C1362", "C1374"), ("C1363", "C1375"), ("C1365", "C1377"),
    ("C1361", "C1373"), ("C1364", "C1376"),
    ("V209", "V211"), ("v209", "v211"),
    ("V208", "V210"), ("v208", "v210"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c650 = load("docs/r50/C1358_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1370_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace('"source": "C1358"', '"source": "C1370"')
out = out.replace("prior C1358", "prior C1370")
out = out.replace("C1361-C1366", "C1373-C1378")
out = out.replace("C1361-C1365", "C1373-C1377")
(S / "c1378_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T211 if t[0].endswith("b")])
print("qty", TR211[1], HO211[1], "po", TR211[8], HO211[8], "sla", TR211[6], HO211[6], "fax", TR211[15], HO211[15])
print("done")
