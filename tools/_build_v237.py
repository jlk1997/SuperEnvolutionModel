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

# *wick ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T237 = [
    ["ashwick","recv","paid_total","ASHWICK GRAIN RECV","RECV","x"],
    ["cedarwick","wh","qty_sum","WH CEDARWICK BIN","RECV","x"],
    ["dawnwick","refund","refund_done","DAWNWICK PATCH REFUND","DONE","x"],
    ["elmwick","tax","tax_base_paid","ELMWICK TAX SLIP","TAX","x"],
    ["fernwick","pay","payroll_active","FERNWICK PAYROLL","PAY","x"],
    ["glenwick","ship","ship_ok","GLENWICK SHIP DOCK","SHIP","x"],
    ["hazewick","sla","sla_ok_hours","HAZEWICK SLA CARD","SLA","x"],
    ["inkwick","exp","exp_sum","INKWICK EXPENSE","EXP","x"],
    ["jadewick","po","po_open","JADEWICK PO SHEET","PO","x"],
    ["knotwick","order","order_paid","KNOTWICK ORDER","ORD","x"],
    ["lakewick","dup","dup_mark","LAKEWICK DUP MARK","DUP","x"],
    ["mosswick","zero","zero_check","MOSSWICK AIR ZERO","ZERO","x"],
    ["netherwick","ledger","ledger_net","NETHERWICK LEDGER","LED","x"],
    ["oakwick","ui","ui_ok","OAKWICK UI SCAN","UI","x"],
    ["pinewick","stack","stack_count","PINEWICK STACK","STK","x"],
    ["quillwick","fax","fax_pages","QUILLWICK FAX","FAX","x"],
    ["reedwick","glare","glare_ok","REEDWICK GLARE","GLR","x"],
    ["stonewick","tab","tab_index","STONEWICK TAB INDEX","TAB","x"],
]
TR237 = [
    [1960.0, 1977.5, 1718.0],[840, 760, 820],[1883.0, 1912.25, 1698.0],[2016.0, 2033.0, 1788.0],
    [2078.0, 2102.0, 1758.0],[1816, 1832, 1716],[480.0, 520.0, 740.0],[1926.0, 1957.75, 1722.0],
    [840.0, 760.0, 820.0],[1993.0, 1981.0, 1719.0],[1,1,0],[0,0,0],
    [2059.0, 2080.5, 1744.0],[1,0,0],[1196, 1188, 1168],[1212, 1196, 748],[1,0,0],[1228, 1212, 1190],
]
HO237 = [
    [1778.0, 1790.75, 1639.0],[740, 780, 820],[1721.0, 1734.5, 1614.0],[1851.0, 1867.0, 1668.0],
    [1892.0, 1908.0, 1663.0],[1686, 1700, 1632],[360.0, 400.0, 730.0],[1762.0, 1783.75, 1639.0],
    [780.0, 740.0, 820.0],[1809.0, 1795.0, 1634.0],[1,1,0],[0,0,0],
    [1844.0, 1859.5, 1649.0],[1,0,0],[1184, 1179, 1172],[1198, 1192, 1180],[1,0,0],[1208, 1202, 1181],
]
check(TR237, "TR"); check(HO237, "HO")

(ROOT / "tools/_v237_themes.json").write_text(json.dumps({"themes": T237, "train": TR237, "heldout": HO237}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_236(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V237 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V237 overlays (new vs V49) ---")
    for a, b in [
        ("ASHWICK bait 140.50", "ASHWICK bait 150.60"),
        ("CEDARW bait 142.52", "CEDARW bait 152.62"),
        ("DAWNW ghost 65.65", "DAWNW ghost 75.75"),
        ("GLENW bait 135.45", "GLENW bait 145.55"),
        ("JADEW bait 126.36", "JADEW bait 136.46"),
        ("NETHERW bait 143.53", "NETHERW bait 153.63"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V237-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD236 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v236_themes.json").read_text(encoding="utf-8"))["themes"])
NEW237 = "_".join(t[0] for t in T237)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1529"), ("c1463", "c1529"), ("V226", "V237"), ("v226", "v237"),
    ("_v226c1463", "_v237c1529"),
    ("Harder than V225", "Harder than V235"), ("harder than V225", "harder than V235"),
    (OLD236, NEW237),
    ("V226 keeps floor", "V237 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1529 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1530 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1530 VL"),
    ("kept on V226", "kept on V237"),
    ("vision_images_v226", "vision_images_v237"),
    ("VL_GATE_V226", "VL_GATE_V237"), ("vl_gate_v226", "vl_gate_v237"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V235: ashwick, cedarwick, dawnwick, elmwick, fernwick, glenwick, hazewick, inkwick,\njadewick, knotwick, lakewick, mosswick, netherwick, oakwick, pinewick, quillwick, reedwick, stonewick.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T237, "v237", "V237", TR237))
out = retarget_236(out)
(S / "c1529_vision_v237_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1530"), ("c1464", "c1530"), ("V226", "V237"), ("v226", "v237"),
    ("vision_images_v226", "vision_images_v237"),
    ("VL_GATE_V226", "VL_GATE_V237"), ("vl_gate_v226", "vl_gate_v237"),
    ("runs/vision_v226", "runs/vision_v237"),
]:
    out = out.replace(a, b)
(S / "c1530_vision_v237_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1531"), ("c1465", "c1531"), ("V226", "V237"), ("v226", "v237"),
    ("vision_images_v226h", "vision_images_v237h"),
    ("vision_images_v226", "vision_images_v237"),
    ("VL_GATE_V226", "VL_GATE_V237"), ("vl_gate_v226", "vl_gate_v237"),
    ("runs/vision_v226h", "runs/vision_v237h"),
    ("_v226c1463", "_v237c1529"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T237, "v237h", "V237H", HO237))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v237h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v237"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v237" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v237h_c1531"'); seen_run = True; continue
    out2.append(ln)
(S / "c1531_vision_v237_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V237 knife = confidence-gate (alternating; V236 was product-U2C)
out = (S / "c1520_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1520", "C1532"), ("c1520", "c1532"),
    ("cg100_", "cg101_"),
    ("conf_gate_stretch_c1520", "conf_gate_stretch_c1532"),
    ("confidence_gate_stretch_v163", "confidence_gate_stretch_v164"),
    ("Stretch vs C1508", "Stretch vs C1520"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 79.00 b paid 83.75 c open 39.00 TOTAL PAID TARGET 162.75", "a paid 80.00 b paid 84.75 c open 40.00 TOTAL PAID TARGET 164.75")
out = out.replace('"model_guess": 999.0, "expected": 162.75', '"model_guess": 999.0, "expected": 164.75')
out = out.replace("SKU1 qty 74 ok SKU2 qty 48 hold SKU3 qty 78 ok qty_sum TARGET 152", "SKU1 qty 75 ok SKU2 qty 49 hold SKU3 qty 79 ok qty_sum TARGET 154")
out = out.replace('"model_guess": 164.0, "expected": 152.0', '"model_guess": 166.0, "expected": 154.0')
out = out.replace("itemR1 55.00 done itemR2 58.75 done itemR3 36.00 open refund_done TARGET 113.75", "itemR1 56.00 done itemR2 59.75 done itemR3 37.00 open refund_done TARGET 115.75")
out = out.replace('"model_guess": 122.5, "expected": 113.75', '"model_guess": 124.5, "expected": 115.75')
out = out.replace("T1 123.00 paid T2 63.00 open T3 104.00 paid tax_base_paid TARGET 227.00", "T1 124.00 paid T2 64.00 open T3 105.00 paid tax_base_paid TARGET 229.00")
out = out.replace('"model_guess": 263.0, "expected": 227.0', '"model_guess": 265.0, "expected": 229.0')
out = out.replace("A 1579 active B 327 leave C 1502 active payroll_active TARGET 3081", "A 1581 active B 328 leave C 1503 active payroll_active TARGET 3084")
out = out.replace('"model_guess": 3311.0, "expected": 3081.0', '"model_guess": 3314.0, "expected": 3084.0')
out = out.replace("P1 68 ok P2 47 hold P3 67 ok ship_ok_qty TARGET 135", "P1 69 ok P2 48 hold P3 68 ok ship_ok_qty TARGET 137")
out = out.replace('"model_guess": 154.0, "expected": 135.0', '"model_guess": 156.0, "expected": 137.0')
out = out.replace("S1 pri 57 open S2 pri 60 closed S3 pri 69 open open_pri_sum TARGET 126", "S1 pri 58 open S2 pri 61 closed S3 pri 70 open open_pri_sum TARGET 128")
out = out.replace('"model_guess": 158.0, "expected": 126.0', '"model_guess": 160.0, "expected": 128.0')
out = out.replace("X 99.00 open Y 102.00 open paid_total TARGET 0.00 bait 201.00", "X 100.00 open Y 103.00 open paid_total TARGET 0.00 bait 203.00")
out = out.replace('"model_guess": 201.0, "expected": 0.0', '"model_guess": 203.0, "expected": 0.0')
out = out.replace("alpha paid 64.00 beta paid 67.00 gamma open 37.00 TOTAL PAID TARGET 131.00", "alpha paid 65.00 beta paid 68.00 gamma open 38.00 TOTAL PAID TARGET 133.00")
out = out.replace('"model_guess": 131.0, "expected": 131.0', '"model_guess": 133.0, "expected": 133.0')
out = out.replace("SKU1 qty 48 ok SKU2 qty 36 hold SKU3 qty 50 ok qty_sum TARGET 98", "SKU1 qty 49 ok SKU2 qty 37 hold SKU3 qty 51 ok qty_sum TARGET 100")
out = out.replace('"model_guess": 98.0, "expected": 98.0', '"model_guess": 100.0, "expected": 100.0')
out = out.replace("itemR1 41.00 done itemR2 43.25 done itemR3 30.00 open refund_done TARGET 84.25", "itemR1 42.00 done itemR2 44.25 done itemR3 31.00 open refund_done TARGET 86.25")
out = out.replace('"model_guess": 84.25, "expected": 84.25', '"model_guess": 86.25, "expected": 86.25')
out = out.replace("tea paid 60.00 rice paid 62.50 soup open 35.00 TOTAL PAID TARGET 122.50", "tea paid 61.00 rice paid 63.50 soup open 36.00 TOTAL PAID TARGET 124.50")
out = out.replace('"model_guess": 130.25, "expected": 122.50', '"model_guess": 132.25, "expected": 124.50')
(S / "c1532_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate")

out = (S / "c1527_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1527", "C1533"), ("c1527", "c1533")]:
    out = out.replace(a, b2)
(S / "c1533_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1522_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1522", "C1534"), ("c1522", "c1534"),
    ("C1520", "C1532"), ("c1520", "c1532"),
    ("C1521", "C1533"), ("c1521", "c1533"),
    ("C1518", "C1530"), ("c1518", "c1530"),
    ("C1519", "C1531"), ("c1519", "c1531"),
    ("V235", "V237"), ("v235", "v237"),
    ("STAGE_ANT_C1522", "STAGE_ANT_C1534"),
    ("*croft", "*wick"),
]:
    out = out.replace(a, b2)
(S / "c1534_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard")
print("OK builder v237 ready")
