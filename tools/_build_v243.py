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

# *hurst ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T243 = [
    ["ashhurst","recv","paid_total","ASHHURST GRAIN RECV","RECV","x"],
    ["cedarhurst","wh","qty_sum","WH CEDARHURST BIN","RECV","x"],
    ["dawnhurst","refund","refund_done","DAWNHURST PATCH REFUND","DONE","x"],
    ["elmhurst","tax","tax_base_paid","ELMHURST TAX SLIP","TAX","x"],
    ["fernhurst","pay","payroll_active","FERNHURST PAYROLL","PAY","x"],
    ["glenhurst","ship","ship_ok","GLENHURST SHIP DOCK","SHIP","x"],
    ["hazehurst","sla","sla_ok_hours","HAZEHURST SLA CARD","SLA","x"],
    ["inkhurst","exp","exp_sum","INKHURST EXPENSE","EXP","x"],
    ["jadehurst","po","po_open","JADEHURST PO SHEET","PO","x"],
    ["knothurst","order","order_paid","KNOTHURST ORDER","ORD","x"],
    ["lakehurst","dup","dup_mark","LAKEHURST DUP MARK","DUP","x"],
    ["mosshurst","zero","zero_check","MOSSHURST AIR ZERO","ZERO","x"],
    ["netherhurst","ledger","ledger_net","NETHERHURST LEDGER","LED","x"],
    ["oakhurst","ui","ui_ok","OAKHURST UI SCAN","UI","x"],
    ["pinehurst","stack","stack_count","PINEHURST STACK","STK","x"],
    ["quillhurst","fax","fax_pages","QUILLHURST FAX","FAX","x"],
    ["reedhurst","glare","glare_ok","REEDHURST GLARE","GLR","x"],
    ["stonehurst","tab","tab_index","STONEHURST TAB INDEX","TAB","x"],
]
TR243 = [
    [2068.0, 2085.5, 1814.0],[840, 760, 820],[1991.0, 2020.25, 1794.0],[2124.0, 2141.0, 1884.0],
    [2186.0, 2210.0, 1854.0],[1912, 1928, 1812],[480.0, 520.0, 740.0],[2034.0, 2065.75, 1818.0],
    [840.0, 760.0, 820.0],[2101.0, 2089.0, 1815.0],[1,1,0],[0,0,0],
    [2167.0, 2188.5, 1840.0],[1,0,0],[1176, 1168, 1148],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO243 = [
    [1874.0, 1886.75, 1735.0],[740, 780, 820],[1817.0, 1831.5, 1710.0],[1947.0, 1963.0, 1764.0],
    [1988.0, 2004.0, 1759.0],[1782, 1796, 1728],[360.0, 400.0, 730.0],[1858.0, 1879.75, 1735.0],
    [780.0, 740.0, 820.0],[1905.0, 1891.0, 1730.0],[1,1,0],[0,0,0],
    [1940.0, 1955.5, 1745.0],[1,0,0],[1168, 1163, 1156],[1182, 1176, 1164],[1,0,0],[1176, 1170, 1149],
]
check(TR243, "TR"); check(HO243, "HO")

(ROOT / "tools/_v243_themes.json").write_text(json.dumps({"themes": T243, "train": TR243, "heldout": HO243}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_242(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V243 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V243 overlays (new vs V49) ---")
    for a, b in [
        ("ASHHURST bait 140.50", "ASHHURST bait 156.66"),
        ("CEDARW bait 142.52", "CEDARH bait 158.68"),
        ("DAWNW ghost 65.65", "DAWNH ghost 81.81"),
        ("GLENW bait 135.45", "GLENH bait 151.61"),
        ("JADEW bait 126.36", "JADEH bait 142.52"),
        ("NETHERW bait 143.53", "NETHERH bait 159.69"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V243-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD242 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v242_themes.json").read_text(encoding="utf-8"))["themes"])
NEW243 = "_".join(t[0] for t in T243)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1565"), ("c1463", "c1565"), ("V226", "V243"), ("v226", "v243"),
    ("_v226c1463", "_v243c1565"),
    ("Harder than V225", "Harder than V241"), ("harder than V225", "harder than V241"),
    (OLD242, NEW243),
    ("V226 keeps floor", "V243 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1565 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1566 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1566 VL"),
    ("kept on V226", "kept on V243"),
    ("vision_images_v226", "vision_images_v243"),
    ("VL_GATE_V226", "VL_GATE_V243"), ("vl_gate_v226", "vl_gate_v243"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V241: ashhurst, cedarhurst, dawnhurst, elmhurst, fernhurst, glenhurst, hazehurst, inkhurst,\njadehurst, knothurst, lakehurst, mosshurst, netherhurst, oakhurst, pinehurst, quillhurst, reedhurst, stonehurst.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T243, "v243", "V243", TR243))
out = retarget_242(out)
(S / "c1565_vision_v243_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1566"), ("c1464", "c1566"), ("V226", "V243"), ("v226", "v243"),
    ("vision_images_v226", "vision_images_v243"),
    ("VL_GATE_V226", "VL_GATE_V243"), ("vl_gate_v226", "vl_gate_v243"),
    ("runs/vision_v226", "runs/vision_v243"),
]:
    out = out.replace(a, b)
(S / "c1566_vision_v243_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1567"), ("c1465", "c1567"), ("V226", "V243"), ("v226", "v243"),
    ("vision_images_v226h", "vision_images_v243h"),
    ("vision_images_v226", "vision_images_v243"),
    ("VL_GATE_V226", "VL_GATE_V243"), ("vl_gate_v226", "vl_gate_v243"),
    ("runs/vision_v226h", "runs/vision_v243h"),
    ("_v226c1463", "_v243c1565"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T243, "v243h", "V243H", HO243))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v243h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v243"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v243" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v243h_c1567"'); seen_run = True; continue
    out2.append(ln)
(S / "c1567_vision_v243_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V243 knife = confidence-gate (alternating; V242 was product-U2C)
out = (S / "c1556_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1556", "C1568"), ("c1556", "c1568"),
    ("cg103_", "cg104_"),
    ("conf_gate_stretch_c1556", "conf_gate_stretch_c1568"),
    ("confidence_gate_stretch_v166", "confidence_gate_stretch_v167"),
    ("Stretch vs C1544", "Stretch vs C1556"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 82.00 b paid 86.75 c open 42.00 TOTAL PAID TARGET 168.75", "a paid 83.00 b paid 87.75 c open 43.00 TOTAL PAID TARGET 170.75")
out = out.replace('"model_guess": 999.0, "expected": 168.75', '"model_guess": 999.0, "expected": 170.75')
out = out.replace("SKU1 qty 77 ok SKU2 qty 51 hold SKU3 qty 81 ok qty_sum TARGET 158", "SKU1 qty 78 ok SKU2 qty 52 hold SKU3 qty 82 ok qty_sum TARGET 160")
out = out.replace('"model_guess": 170.0, "expected": 158.0', '"model_guess": 172.0, "expected": 160.0')
out = out.replace("itemR1 58.00 done itemR2 61.75 done itemR3 39.00 open refund_done TARGET 119.75", "itemR1 59.00 done itemR2 62.75 done itemR3 40.00 open refund_done TARGET 121.75")
out = out.replace('"model_guess": 128.5, "expected": 119.75', '"model_guess": 130.5, "expected": 121.75')
out = out.replace("T1 126.00 paid T2 66.00 open T3 107.00 paid tax_base_paid TARGET 233.00", "T1 127.00 paid T2 67.00 open T3 108.00 paid tax_base_paid TARGET 235.00")
out = out.replace('"model_guess": 269.0, "expected": 233.0', '"model_guess": 271.0, "expected": 235.0')
out = out.replace("A 1585 active B 330 leave C 1505 active payroll_active TARGET 3090", "A 1587 active B 331 leave C 1506 active payroll_active TARGET 3093")
out = out.replace('"model_guess": 3320.0, "expected": 3090.0', '"model_guess": 3323.0, "expected": 3093.0')
out = out.replace("P1 71 ok P2 50 hold P3 70 ok ship_ok_qty TARGET 141", "P1 72 ok P2 51 hold P3 71 ok ship_ok_qty TARGET 143")
out = out.replace('"model_guess": 160.0, "expected": 141.0', '"model_guess": 162.0, "expected": 143.0')
out = out.replace("S1 pri 60 open S2 pri 63 closed S3 pri 72 open open_pri_sum TARGET 132", "S1 pri 61 open S2 pri 64 closed S3 pri 73 open open_pri_sum TARGET 134")
out = out.replace('"model_guess": 164.0, "expected": 132.0', '"model_guess": 166.0, "expected": 134.0')
out = out.replace("X 102.00 open Y 105.00 open paid_total TARGET 0.00 bait 207.00", "X 103.00 open Y 106.00 open paid_total TARGET 0.00 bait 209.00")
out = out.replace('"model_guess": 207.0, "expected": 0.0', '"model_guess": 209.0, "expected": 0.0')
out = out.replace("alpha paid 67.00 beta paid 70.00 gamma open 40.00 TOTAL PAID TARGET 137.00", "alpha paid 68.00 beta paid 71.00 gamma open 41.00 TOTAL PAID TARGET 139.00")
out = out.replace('"model_guess": 137.0, "expected": 137.0', '"model_guess": 139.0, "expected": 139.0')
out = out.replace("SKU1 qty 51 ok SKU2 qty 39 hold SKU3 qty 53 ok qty_sum TARGET 104", "SKU1 qty 52 ok SKU2 qty 40 hold SKU3 qty 54 ok qty_sum TARGET 106")
out = out.replace('"model_guess": 104.0, "expected": 104.0', '"model_guess": 106.0, "expected": 106.0')
out = out.replace("itemR1 44.00 done itemR2 46.25 done itemR3 33.00 open refund_done TARGET 90.25", "itemR1 45.00 done itemR2 47.25 done itemR3 34.00 open refund_done TARGET 92.25")
out = out.replace('"model_guess": 90.25, "expected": 90.25', '"model_guess": 92.25, "expected": 92.25')
out = out.replace("tea paid 63.00 rice paid 65.50 soup open 38.00 TOTAL PAID TARGET 128.50", "tea paid 64.00 rice paid 66.50 soup open 39.00 TOTAL PAID TARGET 130.50")
out = out.replace('"model_guess": 136.25, "expected": 128.50', '"model_guess": 138.25, "expected": 130.50')
(S / "c1568_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate")

out = (S / "c1563_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1563", "C1569"), ("c1563", "c1569")]:
    out = out.replace(a, b2)
(S / "c1569_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1558_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1558", "C1570"), ("c1558", "c1570"),
    ("C1556", "C1568"), ("c1556", "c1568"),
    ("C1557", "C1569"), ("c1557", "c1569"),
    ("C1554", "C1566"), ("c1554", "c1566"),
    ("C1555", "C1567"), ("c1555", "c1567"),
    ("V241", "V243"), ("v241", "v243"),
    ("STAGE_ANT_C1558", "STAGE_ANT_C1570"),
    ("*dale", "*hurst"),
]:
    out = out.replace(a, b2)
(S / "c1570_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard")
print("OK builder v243 ready")
