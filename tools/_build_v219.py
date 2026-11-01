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
T219 = [
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
TR219 = [
    [1636.0, 1653.5, 1430.0],[840, 760, 820],[1559.0, 1588.25, 1410.0],[1692.0, 1709.0, 1500.0],
    [1754.0, 1778.0, 1470.0],[1512, 1528, 1428],[480.0, 520.0, 740.0],[1602.0, 1633.75, 1434.0],
    [840.0, 760.0, 820.0],[1669.0, 1657.0, 1431.0],[1,1,0],[0,0,0],
    [1735.0, 1756.5, 1456.0],[1,0,0],[1188, 1180, 1160],[1286, 1270, 748],[1,0,0],[1312, 1288, 1258],
]
HO219 = [
    [1490.0, 1502.75, 1367.0],[740, 780, 820],[1448.0, 1461.5, 1355.0],[1563.0, 1579.0, 1396.0],
    [1604.0, 1620.0, 1391.0],[1398, 1412, 1360],[360.0, 400.0, 730.0],[1474.0, 1495.75, 1367.0],
    [780.0, 740.0, 820.0],[1521.0, 1507.0, 1362.0],[1,1,0],[0,0,0],
    [1556.0, 1571.5, 1377.0],[1,0,0],[1165, 1160, 1155],[1244, 1238, 1226],[1,0,0],[1254, 1248, 1227],
]
check(TR219, "TR"); check(HO219, "HO")

(ROOT / "tools/_v219_themes.json").write_text(json.dumps({"themes": T219, "train": TR219, "heldout": HO219}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_219(src):
    src = src.replace("# --- V218 overlays (new vs V50) ---", "# --- V219 overlays (new vs V50) ---")
    src = src.replace("# --- V218 overlays (new vs V49) ---", "# --- V219 overlays (new vs V49) ---")
    for a, b in [
        ("ASHDALE bait 132.42", "ASHVALE bait 133.43"),
        ("CEDARD bait 134.44", "CEDARV bait 135.45"),
        ("DAWND ghost 57.57", "DAWNV ghost 58.58"),
        ("GLEND bait 127.37", "GLENV bait 128.38"),
        ("JADED bait 118.28", "JADEV bait 119.29"),
        ("NETHERD bait 135.45", "NETHERV bait 136.46"),
        ("ash mist + stone ticks (V218-only)", "ash mist + stone ticks (V219-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD218 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v218_themes.json").read_text(encoding="utf-8"))["themes"])
NEW219 = "_".join(t[0] for t in T219)

out = (S / "c1415_vision_v218_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1415", "C1421"), ("c1415", "c1421"), ("V218", "V219"), ("v218", "v219"),
    ("_v218c1415", "_v219c1421"),
    ("Harder than V217", "Harder than V218"), ("harder than V217", "harder than V218"),
    (OLD218, NEW219),
    ("V218 keeps floor", "V219 keeps floor"),
    ("C1415 design+fixtures; no VL claim", "C1421 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1416 VL smoke", "fixtures only; claim deferred to C1422 VL smoke"),
    ("No claim until C1416 VL", "No claim until C1422 VL"),
    ("kept on V218", "kept on V219"),
    ("vision_images_v218", "vision_images_v219"),
    ("VL_GATE_V218", "VL_GATE_V219"), ("vl_gate_v218", "vl_gate_v219"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V217:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V218: ashvale, cedarvale, dawnvale, elmvale, fernvale, glenvale, hazevale, inkvale,\njadevale, knotvale, lakevale, mossvale, nethervale, oakvale, pinevale, quillvale, reedvale, stonevale.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T219, "v219", "V219", TR219))
out = retarget_219(out)
(S / "c1421_vision_v219_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1416_vision_v218_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1416", "C1422"), ("c1416", "c1422"), ("V218", "V219"), ("v218", "v219"),
    ("vision_images_v218", "vision_images_v219"),
    ("VL_GATE_V218", "VL_GATE_V219"), ("vl_gate_v218", "vl_gate_v219"),
    ("runs/vision_v218", "runs/vision_v219"),
]:
    out = out.replace(a, b)
(S / "c1422_vision_v219_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1417_vision_v218_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1417", "C1423"), ("c1417", "c1423"), ("V218", "V219"), ("v218", "v219"),
    ("vision_images_v218h", "vision_images_v219h"),
    ("vision_images_v218", "vision_images_v219"),
    ("VL_GATE_V218", "VL_GATE_V219"), ("vl_gate_v218", "vl_gate_v219"),
    ("runs/vision_v218h", "runs/vision_v219h"),
    ("_v218c1415", "_v219c1421"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T219, "v219h", "V219H", HO219))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v219h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v219"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v219" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v219h_c1423"'); seen_run = True; continue
    out2.append(ln)
(S / "c1423_vision_v219_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1412_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1412", "C1424"), ("c1412", "c1424"),
    ("cg91_", "cg92_"),
    ("conf_gate_stretch_c1412", "conf_gate_stretch_c1424"),
    ("confidence_gate_stretch_v154", "confidence_gate_stretch_v155"),
    ("Stretch vs C1400", "Stretch vs C1412"),
]:
    out = out.replace(a, b)
out = out.replace("a paid 70.00 b paid 74.75 c open 30.00 TOTAL PAID TARGET 144.75", "a paid 71.00 b paid 75.75 c open 31.00 TOTAL PAID TARGET 146.75")
out = out.replace('"model_guess": 999.0, "expected": 144.75', '"model_guess": 999.0, "expected": 146.75')
out = out.replace("SKU1 qty 65 ok SKU2 qty 39 hold SKU3 qty 69 ok qty_sum TARGET 134", "SKU1 qty 66 ok SKU2 qty 40 hold SKU3 qty 70 ok qty_sum TARGET 136")
out = out.replace('"model_guess": 146.0, "expected": 134.0', '"model_guess": 148.0, "expected": 136.0')
out = out.replace("itemR1 46.00 done itemR2 49.75 done itemR3 27.00 open refund_done TARGET 95.75", "itemR1 47.00 done itemR2 50.75 done itemR3 28.00 open refund_done TARGET 97.75")
out = out.replace('"model_guess": 104.5, "expected": 95.75', '"model_guess": 106.5, "expected": 97.75')
out = out.replace("T1 114.00 paid T2 54.00 open T3 95.00 paid tax_base_paid TARGET 209.00", "T1 115.00 paid T2 55.00 open T3 96.00 paid tax_base_paid TARGET 211.00")
out = out.replace('"model_guess": 245.0, "expected": 209.0', '"model_guess": 247.0, "expected": 211.0')
out = out.replace("A 1564 active B 318 leave C 1493 active payroll_active TARGET 3057", "A 1565 active B 319 leave C 1494 active payroll_active TARGET 3059")
out = out.replace('"model_guess": 3287.0, "expected": 3057.0', '"model_guess": 3289.0, "expected": 3059.0')
out = out.replace("P1 59 ok P2 38 hold P3 58 ok ship_ok_qty TARGET 117", "P1 60 ok P2 39 hold P3 59 ok ship_ok_qty TARGET 119")
out = out.replace('"model_guess": 136.0, "expected": 117.0', '"model_guess": 138.0, "expected": 119.0')
out = out.replace("S1 pri 48 open S2 pri 51 closed S3 pri 60 open open_pri_sum TARGET 108", "S1 pri 49 open S2 pri 52 closed S3 pri 61 open open_pri_sum TARGET 110")
out = out.replace('"model_guess": 140.0, "expected": 108.0', '"model_guess": 142.0, "expected": 110.0')
out = out.replace("X 90.00 open Y 93.00 open paid_total TARGET 0.00 bait 183.00", "X 91.00 open Y 94.00 open paid_total TARGET 0.00 bait 185.00")
out = out.replace('"model_guess": 183.0, "expected": 0.0', '"model_guess": 185.0, "expected": 0.0')
out = out.replace("alpha paid 55.00 beta paid 58.00 gamma open 28.00 TOTAL PAID TARGET 113.00", "alpha paid 56.00 beta paid 59.00 gamma open 29.00 TOTAL PAID TARGET 115.00")
out = out.replace('"model_guess": 113.0, "expected": 113.0', '"model_guess": 115.0, "expected": 115.0')
out = out.replace("SKU1 qty 39 ok SKU2 qty 27 hold SKU3 qty 41 ok qty_sum TARGET 80", "SKU1 qty 40 ok SKU2 qty 28 hold SKU3 qty 42 ok qty_sum TARGET 82")
out = out.replace('"model_guess": 80.0, "expected": 80.0', '"model_guess": 82.0, "expected": 82.0')
out = out.replace("itemR1 32.00 done itemR2 34.25 done itemR3 21.00 open refund_done TARGET 66.25", "itemR1 33.00 done itemR2 35.25 done itemR3 22.00 open refund_done TARGET 68.25")
out = out.replace('"model_guess": 66.25, "expected": 66.25', '"model_guess": 68.25, "expected": 68.25')
out = out.replace("tea paid 51.00 rice paid 53.50 soup open 26.00 TOTAL PAID TARGET 104.50", "tea paid 52.00 rice paid 54.50 soup open 27.00 TOTAL PAID TARGET 106.50")
out = out.replace('"model_guess": 112.25, "expected": 104.50', '"model_guess": 114.25, "expected": 106.50')
(S / "c1424_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("conf")

out = (S / "c1419_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1419", "C1425"), ("c1419", "c1425"),
    ("capture_regression_c1419", "capture_regression_c1425"),
    ("after C1415-C1418", "after C1421-C1424"),
    ("V4-V218+heldout", "V4-V219+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V218", DOC / "C1416_VISION_V218_SMOKE.json"),'
if needle in out and "VISION_V219_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V219", DOC / "C1422_VISION_V219_SMOKE.json"),\n    ("V219_heldout", DOC / "C1423_VISION_V219_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1425_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1414_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1414", "C1426"), ("c1414", "c1426"),
    ("C1410", "C1422"), ("C1411", "C1423"), ("C1413", "C1425"),
    ("C1409", "C1421"), ("C1412", "C1424"),
    ("V217", "V219"), ("v217", "v219"),
    ("V216", "V218"), ("v216", "v218"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c650 = load("docs/r50/C1406_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1418_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace('"source": "C1406"', '"source": "C1418"')
out = out.replace("prior C1406", "prior C1418")
out = out.replace("C1409-C1414", "C1421-C1426")
out = out.replace("C1409-C1413", "C1421-C1425")
(S / "c1426_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T219 if t[0].endswith("b")])
print("qty", TR219[1], HO219[1], "po", TR219[8], HO219[8], "sla", TR219[6], HO219[6], "fax", TR219[15], HO219[15])
print("done")
