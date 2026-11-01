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

# *ford ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T231 = [
    ["ashford","recv","paid_total","ASHFORD GRAIN RECV","RECV","x"],
    ["cedarford","wh","qty_sum","WH CEDARFORD BIN","RECV","x"],
    ["dawnford","refund","refund_done","DAWNFORD PATCH REFUND","DONE","x"],
    ["elmford","tax","tax_base_paid","ELMFORD TAX SLIP","TAX","x"],
    ["fernford","pay","payroll_active","FERNFORD PAYROLL","PAY","x"],
    ["glenford","ship","ship_ok","GLENFORD SHIP DOCK","SHIP","x"],
    ["hazeford","sla","sla_ok_hours","HAZEFORD SLA CARD","SLA","x"],
    ["inkford","exp","exp_sum","INKFORD EXPENSE","EXP","x"],
    ["jadeford","po","po_open","JADEFORD PO SHEET","PO","x"],
    ["knotford","order","order_paid","KNOTFORD ORDER","ORD","x"],
    ["lakeford","dup","dup_mark","LAKEFORD DUP MARK","DUP","x"],
    ["mossford","zero","zero_check","MOSSFORD AIR ZERO","ZERO","x"],
    ["netherford","ledger","ledger_net","NETHERFORD LEDGER","LED","x"],
    ["oakford","ui","ui_ok","OAKFORD UI SCAN","UI","x"],
    ["pineford","stack","stack_count","PINEFORD STACK","STK","x"],
    ["quillford","fax","fax_pages","QUILLFORD FAX","FAX","x"],
    ["reedford","glare","glare_ok","REEDFORD GLARE","GLR","x"],
    ["stoneford","tab","tab_index","STONEFORD TAB INDEX","TAB","x"],
]
TR231 = [
    [1852.0, 1869.5, 1622.0],[840, 760, 820],[1775.0, 1804.25, 1602.0],[1908.0, 1925.0, 1692.0],
    [1970.0, 1994.0, 1662.0],[1720, 1736, 1620],[480.0, 520.0, 740.0],[1818.0, 1849.75, 1626.0],
    [840.0, 760.0, 820.0],[1885.0, 1873.0, 1623.0],[1,1,0],[0,0,0],
    [1951.0, 1972.5, 1648.0],[1,0,0],[1172, 1164, 1144],[1188, 1172, 748],[1,0,0],[1204, 1188, 1166],
]
HO231 = [
    [1682.0, 1694.75, 1543.0],[740, 780, 820],[1625.0, 1638.5, 1518.0],[1755.0, 1771.0, 1572.0],
    [1796.0, 1812.0, 1567.0],[1590, 1604, 1536],[360.0, 400.0, 730.0],[1666.0, 1687.75, 1543.0],
    [780.0, 740.0, 820.0],[1713.0, 1699.0, 1538.0],[1,1,0],[0,0,0],
    [1748.0, 1763.5, 1553.0],[1,0,0],[1160, 1155, 1148],[1174, 1168, 1156],[1,0,0],[1184, 1178, 1157],
]
check(TR231, "TR"); check(HO231, "HO")

(ROOT / "tools/_v231_themes.json").write_text(json.dumps({"themes": T231, "train": TR231, "heldout": HO231}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_230(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V231 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V231 overlays (new vs V49) ---")
    for a, b in [
        ("ASHWICK bait 140.50", "ASHFORD bait 144.54"),
        ("CEDARW bait 142.52", "CEDARF bait 146.56"),
        ("DAWNW ghost 65.65", "DAWNF ghost 69.69"),
        ("GLENW bait 135.45", "GLENF bait 139.49"),
        ("JADEW bait 126.36", "JADEF bait 130.40"),
        ("NETHERW bait 143.53", "NETHERF bait 147.57"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V231-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD230 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v230_themes.json").read_text(encoding="utf-8"))["themes"])
NEW231 = "_".join(t[0] for t in T231)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1493"), ("c1463", "c1493"), ("V226", "V231"), ("v226", "v231"),
    ("_v226c1463", "_v231c1493"),
    ("Harder than V225", "Harder than V229"), ("harder than V225", "harder than V229"),
    (OLD230, NEW231),
    ("V226 keeps floor", "V231 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1493 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1494 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1494 VL"),
    ("kept on V226", "kept on V231"),
    ("vision_images_v226", "vision_images_v231"),
    ("VL_GATE_V226", "VL_GATE_V231"), ("vl_gate_v226", "vl_gate_v231"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V229: ashford, cedarford, dawnford, elmford, fernford, glenford, hazeford, inkford,\njadeford, knotford, lakeford, mossford, netherford, oakford, pineford, quillford, reedford, stoneford.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T231, "v231", "V231", TR231))
out = retarget_230(out)
(S / "c1493_vision_v231_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1494"), ("c1464", "c1494"), ("V226", "V231"), ("v226", "v231"),
    ("vision_images_v226", "vision_images_v231"),
    ("VL_GATE_V226", "VL_GATE_V231"), ("vl_gate_v226", "vl_gate_v231"),
    ("runs/vision_v226", "runs/vision_v231"),
]:
    out = out.replace(a, b)
(S / "c1494_vision_v231_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1495"), ("c1465", "c1495"), ("V226", "V231"), ("v226", "v231"),
    ("vision_images_v226h", "vision_images_v231h"),
    ("vision_images_v226", "vision_images_v231"),
    ("VL_GATE_V226", "VL_GATE_V231"), ("vl_gate_v226", "vl_gate_v231"),
    ("runs/vision_v226h", "runs/vision_v231h"),
    ("_v226c1463", "_v231c1493"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T231, "v231h", "V231H", HO231))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v231h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v231"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v231" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v231h_c1495"'); seen_run = True; continue
    out2.append(ln)
(S / "c1495_vision_v231_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V231 knife = confidence-gate (alternating; V230 was product-U2C)
out = (S / "c1484_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1484", "C1496"), ("c1484", "c1496"),
    ("cg97_", "cg98_"),
    ("conf_gate_stretch_c1484", "conf_gate_stretch_c1496"),
    ("confidence_gate_stretch_v160", "confidence_gate_stretch_v161"),
    ("Stretch vs C1472", "Stretch vs C1484"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 76.00 b paid 80.75 c open 36.00 TOTAL PAID TARGET 156.75", "a paid 77.00 b paid 81.75 c open 37.00 TOTAL PAID TARGET 158.75")
out = out.replace('"model_guess": 999.0, "expected": 156.75', '"model_guess": 999.0, "expected": 158.75')
out = out.replace("SKU1 qty 71 ok SKU2 qty 45 hold SKU3 qty 75 ok qty_sum TARGET 146", "SKU1 qty 72 ok SKU2 qty 46 hold SKU3 qty 76 ok qty_sum TARGET 148")
out = out.replace('"model_guess": 158.0, "expected": 146.0', '"model_guess": 160.0, "expected": 148.0')
out = out.replace("itemR1 52.00 done itemR2 55.75 done itemR3 33.00 open refund_done TARGET 107.75", "itemR1 53.00 done itemR2 56.75 done itemR3 34.00 open refund_done TARGET 109.75")
out = out.replace('"model_guess": 116.5, "expected": 107.75', '"model_guess": 118.5, "expected": 109.75')
out = out.replace("T1 120.00 paid T2 60.00 open T3 101.00 paid tax_base_paid TARGET 221.00", "T1 121.00 paid T2 61.00 open T3 102.00 paid tax_base_paid TARGET 223.00")
out = out.replace('"model_guess": 257.0, "expected": 221.0', '"model_guess": 259.0, "expected": 223.0')
out = out.replace("A 1573 active B 324 leave C 1499 active payroll_active TARGET 3072", "A 1575 active B 325 leave C 1500 active payroll_active TARGET 3075")
out = out.replace('"model_guess": 3302.0, "expected": 3072.0', '"model_guess": 3305.0, "expected": 3075.0')
out = out.replace("P1 65 ok P2 44 hold P3 64 ok ship_ok_qty TARGET 129", "P1 66 ok P2 45 hold P3 65 ok ship_ok_qty TARGET 131")
out = out.replace('"model_guess": 148.0, "expected": 129.0', '"model_guess": 150.0, "expected": 131.0')
out = out.replace("S1 pri 54 open S2 pri 57 closed S3 pri 66 open open_pri_sum TARGET 120", "S1 pri 55 open S2 pri 58 closed S3 pri 67 open open_pri_sum TARGET 122")
out = out.replace('"model_guess": 152.0, "expected": 120.0', '"model_guess": 154.0, "expected": 122.0')
out = out.replace("X 96.00 open Y 99.00 open paid_total TARGET 0.00 bait 195.00", "X 97.00 open Y 100.00 open paid_total TARGET 0.00 bait 197.00")
out = out.replace('"model_guess": 195.0, "expected": 0.0', '"model_guess": 197.0, "expected": 0.0')
out = out.replace("alpha paid 61.00 beta paid 64.00 gamma open 34.00 TOTAL PAID TARGET 125.00", "alpha paid 62.00 beta paid 65.00 gamma open 35.00 TOTAL PAID TARGET 127.00")
out = out.replace('"model_guess": 125.0, "expected": 125.0', '"model_guess": 127.0, "expected": 127.0')
out = out.replace("SKU1 qty 45 ok SKU2 qty 33 hold SKU3 qty 47 ok qty_sum TARGET 92", "SKU1 qty 46 ok SKU2 qty 34 hold SKU3 qty 48 ok qty_sum TARGET 94")
out = out.replace('"model_guess": 92.0, "expected": 92.0', '"model_guess": 94.0, "expected": 94.0')
out = out.replace("itemR1 38.00 done itemR2 40.25 done itemR3 27.00 open refund_done TARGET 78.25", "itemR1 39.00 done itemR2 41.25 done itemR3 28.00 open refund_done TARGET 80.25")
out = out.replace('"model_guess": 78.25, "expected": 78.25', '"model_guess": 80.25, "expected": 80.25')
out = out.replace("tea paid 57.00 rice paid 59.50 soup open 32.00 TOTAL PAID TARGET 116.50", "tea paid 58.00 rice paid 60.50 soup open 33.00 TOTAL PAID TARGET 118.50")
out = out.replace('"model_guess": 124.25, "expected": 116.50', '"model_guess": 126.25, "expected": 118.50')
(S / "c1496_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate")

out = (S / "c1491_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1491", "C1497"), ("c1491", "c1497")]:
    out = out.replace(a, b2)
(S / "c1497_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1486_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1486", "C1498"), ("c1486", "c1498"),
    ("C1484", "C1496"), ("c1484", "c1496"),
    ("C1485", "C1497"), ("c1485", "c1497"),
    ("C1482", "C1494"), ("c1482", "c1494"),
    ("C1483", "C1495"), ("c1483", "c1495"),
    ("V229", "V231"), ("v229", "v231"),
    ("STAGE_ANT_C1486", "STAGE_ANT_C1498"),
    ("*brook", "*ford"),
]:
    out = out.replace(a, b2)
(S / "c1498_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard")
print("OK builder v231 ready")
