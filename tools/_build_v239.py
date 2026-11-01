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

# *fen ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T239 = [
    ["ashfen","recv","paid_total","ASHFEN GRAIN RECV","RECV","x"],
    ["cedarfen","wh","qty_sum","WH CEDARFEN BIN","RECV","x"],
    ["dawnfen","refund","refund_done","DAWNFEN PATCH REFUND","DONE","x"],
    ["elmfen","tax","tax_base_paid","ELMFEN TAX SLIP","TAX","x"],
    ["fernfen","pay","payroll_active","FERNFEN PAYROLL","PAY","x"],
    ["glenfen","ship","ship_ok","GLENFEN SHIP DOCK","SHIP","x"],
    ["hazefen","sla","sla_ok_hours","HAZEFEN SLA CARD","SLA","x"],
    ["inkfen","exp","exp_sum","INKFEN EXPENSE","EXP","x"],
    ["jadefen","po","po_open","JADEFEN PO SHEET","PO","x"],
    ["knotfen","order","order_paid","KNOTFEN ORDER","ORD","x"],
    ["lakefen","dup","dup_mark","LAKEFEN DUP MARK","DUP","x"],
    ["mossfen","zero","zero_check","MOSSFEN AIR ZERO","ZERO","x"],
    ["netherfen","ledger","ledger_net","NETHERFEN LEDGER","LED","x"],
    ["oakfen","ui","ui_ok","OAKFEN UI SCAN","UI","x"],
    ["pinefen","stack","stack_count","PINEFEN STACK","STK","x"],
    ["quillfen","fax","fax_pages","QUILLFEN FAX","FAX","x"],
    ["reedfen","glare","glare_ok","REEDFEN GLARE","GLR","x"],
    ["stonefen","tab","tab_index","STONEFEN TAB INDEX","TAB","x"],
]
TR239 = [
    [1996.0, 2013.5, 1750.0],[840, 760, 820],[1919.0, 1948.25, 1730.0],[2052.0, 2069.0, 1820.0],
    [2114.0, 2138.0, 1790.0],[1848, 1864, 1748],[480.0, 520.0, 740.0],[1962.0, 1993.75, 1754.0],
    [840.0, 760.0, 820.0],[2029.0, 2017.0, 1751.0],[1,1,0],[0,0,0],
    [2095.0, 2116.5, 1776.0],[1,0,0],[1160, 1152, 1132],[1176, 1160, 748],[1,0,0],[1192, 1176, 1154],
]
HO239 = [
    [1810.0, 1822.75, 1671.0],[740, 780, 820],[1753.0, 1766.5, 1646.0],[1883.0, 1899.0, 1700.0],
    [1924.0, 1940.0, 1695.0],[1718, 1732, 1664],[360.0, 400.0, 730.0],[1794.0, 1815.75, 1671.0],
    [780.0, 740.0, 820.0],[1841.0, 1827.0, 1666.0],[1,1,0],[0,0,0],
    [1876.0, 1891.5, 1681.0],[1,0,0],[1152, 1147, 1140],[1166, 1160, 1148],[1,0,0],[1176, 1170, 1149],
]
check(TR239, "TR"); check(HO239, "HO")

(ROOT / "tools/_v239_themes.json").write_text(json.dumps({"themes": T239, "train": TR239, "heldout": HO239}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_238(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V239 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V239 overlays (new vs V49) ---")
    for a, b in [
        ("ASHFEN bait 140.50", "ASHFEN bait 152.62"),
        ("CEDARW bait 142.52", "CEDARF bait 154.64"),
        ("DAWNW ghost 65.65", "DAWNF ghost 77.77"),
        ("GLENW bait 135.45", "GLENF bait 147.57"),
        ("JADEW bait 126.36", "JADEF bait 138.48"),
        ("NETHERW bait 143.53", "NETHERF bait 155.65"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V239-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD238 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v238_themes.json").read_text(encoding="utf-8"))["themes"])
NEW239 = "_".join(t[0] for t in T239)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1541"), ("c1463", "c1541"), ("V226", "V239"), ("v226", "v239"),
    ("_v226c1463", "_v239c1541"),
    ("Harder than V225", "Harder than V237"), ("harder than V225", "harder than V237"),
    (OLD238, NEW239),
    ("V226 keeps floor", "V239 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1541 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1542 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1542 VL"),
    ("kept on V226", "kept on V239"),
    ("vision_images_v226", "vision_images_v239"),
    ("VL_GATE_V226", "VL_GATE_V239"), ("vl_gate_v226", "vl_gate_v239"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V237: ashfen, cedarfen, dawnfen, elmfen, fernfen, glenfen, hazefen, inkfen,\njadefen, knotfen, lakefen, mossfen, netherfen, oakfen, pinefen, quillfen, reedfen, stonefen.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T239, "v239", "V239", TR239))
out = retarget_238(out)
(S / "c1541_vision_v239_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1542"), ("c1464", "c1542"), ("V226", "V239"), ("v226", "v239"),
    ("vision_images_v226", "vision_images_v239"),
    ("VL_GATE_V226", "VL_GATE_V239"), ("vl_gate_v226", "vl_gate_v239"),
    ("runs/vision_v226", "runs/vision_v239"),
]:
    out = out.replace(a, b)
(S / "c1542_vision_v239_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1543"), ("c1465", "c1543"), ("V226", "V239"), ("v226", "v239"),
    ("vision_images_v226h", "vision_images_v239h"),
    ("vision_images_v226", "vision_images_v239"),
    ("VL_GATE_V226", "VL_GATE_V239"), ("vl_gate_v226", "vl_gate_v239"),
    ("runs/vision_v226h", "runs/vision_v239h"),
    ("_v226c1463", "_v239c1541"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T239, "v239h", "V239H", HO239))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v239h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v239"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v239" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v239h_c1543"'); seen_run = True; continue
    out2.append(ln)
(S / "c1543_vision_v239_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V239 knife = confidence-gate (alternating; V238 was product-U2C)
out = (S / "c1532_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1532", "C1544"), ("c1532", "c1544"),
    ("cg101_", "cg102_"),
    ("conf_gate_stretch_c1532", "conf_gate_stretch_c1544"),
    ("confidence_gate_stretch_v164", "confidence_gate_stretch_v165"),
    ("Stretch vs C1520", "Stretch vs C1532"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 80.00 b paid 84.75 c open 40.00 TOTAL PAID TARGET 164.75", "a paid 81.00 b paid 85.75 c open 41.00 TOTAL PAID TARGET 166.75")
out = out.replace('"model_guess": 999.0, "expected": 164.75', '"model_guess": 999.0, "expected": 166.75')
out = out.replace("SKU1 qty 75 ok SKU2 qty 49 hold SKU3 qty 79 ok qty_sum TARGET 154", "SKU1 qty 76 ok SKU2 qty 50 hold SKU3 qty 80 ok qty_sum TARGET 156")
out = out.replace('"model_guess": 166.0, "expected": 154.0', '"model_guess": 168.0, "expected": 156.0')
out = out.replace("itemR1 56.00 done itemR2 59.75 done itemR3 37.00 open refund_done TARGET 115.75", "itemR1 57.00 done itemR2 60.75 done itemR3 38.00 open refund_done TARGET 117.75")
out = out.replace('"model_guess": 124.5, "expected": 115.75', '"model_guess": 126.5, "expected": 117.75')
out = out.replace("T1 124.00 paid T2 64.00 open T3 105.00 paid tax_base_paid TARGET 229.00", "T1 125.00 paid T2 65.00 open T3 106.00 paid tax_base_paid TARGET 231.00")
out = out.replace('"model_guess": 265.0, "expected": 229.0', '"model_guess": 267.0, "expected": 231.0')
out = out.replace("A 1581 active B 328 leave C 1503 active payroll_active TARGET 3084", "A 1583 active B 329 leave C 1504 active payroll_active TARGET 3087")
out = out.replace('"model_guess": 3314.0, "expected": 3084.0', '"model_guess": 3317.0, "expected": 3087.0')
out = out.replace("P1 69 ok P2 48 hold P3 68 ok ship_ok_qty TARGET 137", "P1 70 ok P2 49 hold P3 69 ok ship_ok_qty TARGET 139")
out = out.replace('"model_guess": 156.0, "expected": 137.0', '"model_guess": 158.0, "expected": 139.0')
out = out.replace("S1 pri 58 open S2 pri 61 closed S3 pri 70 open open_pri_sum TARGET 128", "S1 pri 59 open S2 pri 62 closed S3 pri 71 open open_pri_sum TARGET 130")
out = out.replace('"model_guess": 160.0, "expected": 128.0', '"model_guess": 162.0, "expected": 130.0')
out = out.replace("X 100.00 open Y 103.00 open paid_total TARGET 0.00 bait 203.00", "X 101.00 open Y 104.00 open paid_total TARGET 0.00 bait 205.00")
out = out.replace('"model_guess": 203.0, "expected": 0.0', '"model_guess": 205.0, "expected": 0.0')
out = out.replace("alpha paid 65.00 beta paid 68.00 gamma open 38.00 TOTAL PAID TARGET 133.00", "alpha paid 66.00 beta paid 69.00 gamma open 39.00 TOTAL PAID TARGET 135.00")
out = out.replace('"model_guess": 133.0, "expected": 133.0', '"model_guess": 135.0, "expected": 135.0')
out = out.replace("SKU1 qty 49 ok SKU2 qty 37 hold SKU3 qty 51 ok qty_sum TARGET 100", "SKU1 qty 50 ok SKU2 qty 38 hold SKU3 qty 52 ok qty_sum TARGET 102")
out = out.replace('"model_guess": 100.0, "expected": 100.0', '"model_guess": 102.0, "expected": 102.0')
out = out.replace("itemR1 42.00 done itemR2 44.25 done itemR3 31.00 open refund_done TARGET 86.25", "itemR1 43.00 done itemR2 45.25 done itemR3 32.00 open refund_done TARGET 88.25")
out = out.replace('"model_guess": 86.25, "expected": 86.25', '"model_guess": 88.25, "expected": 88.25')
out = out.replace("tea paid 61.00 rice paid 63.50 soup open 36.00 TOTAL PAID TARGET 124.50", "tea paid 62.00 rice paid 64.50 soup open 37.00 TOTAL PAID TARGET 126.50")
out = out.replace('"model_guess": 132.25, "expected": 124.50', '"model_guess": 134.25, "expected": 126.50')
(S / "c1544_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate")

out = (S / "c1539_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1539", "C1545"), ("c1539", "c1545")]:
    out = out.replace(a, b2)
(S / "c1545_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1534_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1534", "C1546"), ("c1534", "c1546"),
    ("C1532", "C1544"), ("c1532", "c1544"),
    ("C1533", "C1545"), ("c1533", "c1545"),
    ("C1530", "C1542"), ("c1530", "c1542"),
    ("C1531", "C1543"), ("c1531", "c1543"),
    ("V237", "V239"), ("v237", "v239"),
    ("STAGE_ANT_C1534", "STAGE_ANT_C1546"),
    ("*wick", "*fen"),
]:
    out = out.replace(a, b2)
(S / "c1546_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard")
print("OK builder v239 ready")
