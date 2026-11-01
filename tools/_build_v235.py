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

# *croft ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T235 = [
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
TR235 = [
    [1924.0, 1941.5, 1686.0],[840, 760, 820],[1847.0, 1876.25, 1666.0],[1980.0, 1997.0, 1756.0],
    [2042.0, 2066.0, 1726.0],[1784, 1800, 1684],[480.0, 520.0, 740.0],[1890.0, 1921.75, 1690.0],
    [840.0, 760.0, 820.0],[1957.0, 1945.0, 1687.0],[1,1,0],[0,0,0],
    [2023.0, 2044.5, 1712.0],[1,0,0],[1188, 1180, 1160],[1204, 1188, 748],[1,0,0],[1220, 1204, 1182],
]
HO235 = [
    [1746.0, 1758.75, 1607.0],[740, 780, 820],[1689.0, 1702.5, 1582.0],[1819.0, 1835.0, 1636.0],
    [1860.0, 1876.0, 1631.0],[1654, 1668, 1600],[360.0, 400.0, 730.0],[1730.0, 1751.75, 1607.0],
    [780.0, 740.0, 820.0],[1777.0, 1763.0, 1602.0],[1,1,0],[0,0,0],
    [1812.0, 1827.5, 1617.0],[1,0,0],[1176, 1171, 1164],[1190, 1184, 1172],[1,0,0],[1200, 1194, 1173],
]
check(TR235, "TR"); check(HO235, "HO")

(ROOT / "tools/_v235_themes.json").write_text(json.dumps({"themes": T235, "train": TR235, "heldout": HO235}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_234(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V235 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V235 overlays (new vs V49) ---")
    for a, b in [
        ("ASHWICK bait 140.50", "ASHCROFT bait 148.58"),
        ("CEDARW bait 142.52", "CEDARC bait 150.60"),
        ("DAWNW ghost 65.65", "DAWNC ghost 73.73"),
        ("GLENW bait 135.45", "GLENC bait 143.53"),
        ("JADEW bait 126.36", "JADEC bait 134.44"),
        ("NETHERW bait 143.53", "NETHERC bait 151.61"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V235-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD234 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v234_themes.json").read_text(encoding="utf-8"))["themes"])
NEW235 = "_".join(t[0] for t in T235)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1517"), ("c1463", "c1517"), ("V226", "V235"), ("v226", "v235"),
    ("_v226c1463", "_v235c1517"),
    ("Harder than V225", "Harder than V233"), ("harder than V225", "harder than V233"),
    (OLD234, NEW235),
    ("V226 keeps floor", "V235 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1517 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1518 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1518 VL"),
    ("kept on V226", "kept on V235"),
    ("vision_images_v226", "vision_images_v235"),
    ("VL_GATE_V226", "VL_GATE_V235"), ("vl_gate_v226", "vl_gate_v235"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V233: ashcroft, cedarcroft, dawncroft, elmcroft, ferncroft, glencroft, hazecroft, inkcroft,\njadecroft, knotcroft, lakecroft, mosscroft, nethercroft, oakcroft, pinecroft, quillcroft, reedcroft, stonecroft.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T235, "v235", "V235", TR235))
out = retarget_234(out)
(S / "c1517_vision_v235_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1518"), ("c1464", "c1518"), ("V226", "V235"), ("v226", "v235"),
    ("vision_images_v226", "vision_images_v235"),
    ("VL_GATE_V226", "VL_GATE_V235"), ("vl_gate_v226", "vl_gate_v235"),
    ("runs/vision_v226", "runs/vision_v235"),
]:
    out = out.replace(a, b)
(S / "c1518_vision_v235_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1519"), ("c1465", "c1519"), ("V226", "V235"), ("v226", "v235"),
    ("vision_images_v226h", "vision_images_v235h"),
    ("vision_images_v226", "vision_images_v235"),
    ("VL_GATE_V226", "VL_GATE_V235"), ("vl_gate_v226", "vl_gate_v235"),
    ("runs/vision_v226h", "runs/vision_v235h"),
    ("_v226c1463", "_v235c1517"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T235, "v235h", "V235H", HO235))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v235h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v235"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v235" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v235h_c1519"'); seen_run = True; continue
    out2.append(ln)
(S / "c1519_vision_v235_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V235 knife = confidence-gate (alternating; V234 was product-U2C)
out = (S / "c1508_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1508", "C1520"), ("c1508", "c1520"),
    ("cg99_", "cg100_"),
    ("conf_gate_stretch_c1508", "conf_gate_stretch_c1520"),
    ("confidence_gate_stretch_v162", "confidence_gate_stretch_v163"),
    ("Stretch vs C1496", "Stretch vs C1508"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 78.00 b paid 82.75 c open 38.00 TOTAL PAID TARGET 160.75", "a paid 79.00 b paid 83.75 c open 39.00 TOTAL PAID TARGET 162.75")
out = out.replace('"model_guess": 999.0, "expected": 160.75', '"model_guess": 999.0, "expected": 162.75')
out = out.replace("SKU1 qty 73 ok SKU2 qty 47 hold SKU3 qty 77 ok qty_sum TARGET 150", "SKU1 qty 74 ok SKU2 qty 48 hold SKU3 qty 78 ok qty_sum TARGET 152")
out = out.replace('"model_guess": 162.0, "expected": 150.0', '"model_guess": 164.0, "expected": 152.0')
out = out.replace("itemR1 54.00 done itemR2 57.75 done itemR3 35.00 open refund_done TARGET 111.75", "itemR1 55.00 done itemR2 58.75 done itemR3 36.00 open refund_done TARGET 113.75")
out = out.replace('"model_guess": 120.5, "expected": 111.75', '"model_guess": 122.5, "expected": 113.75')
out = out.replace("T1 122.00 paid T2 62.00 open T3 103.00 paid tax_base_paid TARGET 225.00", "T1 123.00 paid T2 63.00 open T3 104.00 paid tax_base_paid TARGET 227.00")
out = out.replace('"model_guess": 261.0, "expected": 225.0', '"model_guess": 263.0, "expected": 227.0')
out = out.replace("A 1577 active B 326 leave C 1501 active payroll_active TARGET 3078", "A 1579 active B 327 leave C 1502 active payroll_active TARGET 3081")
out = out.replace('"model_guess": 3308.0, "expected": 3078.0', '"model_guess": 3311.0, "expected": 3081.0')
out = out.replace("P1 67 ok P2 46 hold P3 66 ok ship_ok_qty TARGET 133", "P1 68 ok P2 47 hold P3 67 ok ship_ok_qty TARGET 135")
out = out.replace('"model_guess": 152.0, "expected": 133.0', '"model_guess": 154.0, "expected": 135.0')
out = out.replace("S1 pri 56 open S2 pri 59 closed S3 pri 68 open open_pri_sum TARGET 124", "S1 pri 57 open S2 pri 60 closed S3 pri 69 open open_pri_sum TARGET 126")
out = out.replace('"model_guess": 156.0, "expected": 124.0', '"model_guess": 158.0, "expected": 126.0')
out = out.replace("X 98.00 open Y 101.00 open paid_total TARGET 0.00 bait 199.00", "X 99.00 open Y 102.00 open paid_total TARGET 0.00 bait 201.00")
out = out.replace('"model_guess": 199.0, "expected": 0.0', '"model_guess": 201.0, "expected": 0.0')
out = out.replace("alpha paid 63.00 beta paid 66.00 gamma open 36.00 TOTAL PAID TARGET 129.00", "alpha paid 64.00 beta paid 67.00 gamma open 37.00 TOTAL PAID TARGET 131.00")
out = out.replace('"model_guess": 129.0, "expected": 129.0', '"model_guess": 131.0, "expected": 131.0')
out = out.replace("SKU1 qty 47 ok SKU2 qty 35 hold SKU3 qty 49 ok qty_sum TARGET 96", "SKU1 qty 48 ok SKU2 qty 36 hold SKU3 qty 50 ok qty_sum TARGET 98")
out = out.replace('"model_guess": 96.0, "expected": 96.0', '"model_guess": 98.0, "expected": 98.0')
out = out.replace("itemR1 40.00 done itemR2 42.25 done itemR3 29.00 open refund_done TARGET 82.25", "itemR1 41.00 done itemR2 43.25 done itemR3 30.00 open refund_done TARGET 84.25")
out = out.replace('"model_guess": 82.25, "expected": 82.25', '"model_guess": 84.25, "expected": 84.25')
out = out.replace("tea paid 59.00 rice paid 61.50 soup open 34.00 TOTAL PAID TARGET 120.50", "tea paid 60.00 rice paid 62.50 soup open 35.00 TOTAL PAID TARGET 122.50")
out = out.replace('"model_guess": 128.25, "expected": 120.50', '"model_guess": 130.25, "expected": 122.50')
(S / "c1520_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate")

out = (S / "c1515_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1515", "C1521"), ("c1515", "c1521")]:
    out = out.replace(a, b2)
(S / "c1521_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1510_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1510", "C1522"), ("c1510", "c1522"),
    ("C1508", "C1520"), ("c1508", "c1520"),
    ("C1509", "C1521"), ("c1509", "c1521"),
    ("C1506", "C1518"), ("c1506", "c1518"),
    ("C1507", "C1519"), ("c1507", "c1519"),
    ("V233", "V235"), ("v233", "v235"),
    ("STAGE_ANT_C1510", "STAGE_ANT_C1522"),
    ("*mere", "*croft"),
]:
    out = out.replace(a, b2)
(S / "c1522_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard")
print("OK builder v235 ready")
