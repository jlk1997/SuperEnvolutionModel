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
T275 = [
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
TR275 = [
    [2200.0, 2217.5, 1940.0],[840, 760, 820],[2123.0, 2152.25, 1918.0],[2256.0, 2273.0, 2008.0],
    [2318.0, 2342.0, 1978.0],[2036, 2052, 1936],[520.0, 560.0, 760.0],[2166.0, 2197.75, 1942.0],
    [840.0, 760.0, 820.0],[2233.0, 2221.0, 1939.0],[1,1,0],[0,0,0],
    [2299.0, 2320.5, 1964.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO275 = [
    [1998.0, 2010.75, 1859.0],[640, 660, 820],[1941.0, 1955.5, 1834.0],[2071.0, 2087.0, 1890.0],
    [2112.0, 2128.0, 1883.0],[1894, 1906, 1854],[400.0, 440.0, 740.0],[1982.0, 2003.75, 1859.0],
    [740.0, 780.0, 820.0],[2029.0, 2015.0, 1856.0],[1,1,0],[0,0,0],
    [2064.0, 2079.5, 1869.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR275, "TR"); check(HO275, "HO")

(ROOT / "tools/_v275_themes.json").write_text(json.dumps({"themes": T275, "train": TR275, "heldout": HO275}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_274(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V275 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V275 overlays (new vs V49) ---")
    for a, b in [
        ("ASHFORD bait 140.50", "ASHFORD bait 185.95"),
        ("CEDARW bait 142.52", "CEDARF bait 190.00"),
        ("DAWNW ghost 65.65", "DAWNF ghost 113.23"),
        ("GLENW bait 135.45", "GLENF bait 183.93"),
        ("JADEW bait 126.36", "JADEF bait 174.84"),
        ("NETHERW bait 143.53", "NETHERF bait 191.01"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V275-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD274 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v274_themes.json").read_text(encoding="utf-8"))["themes"])
NEW275 = "_".join(t[0] for t in T275)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1757"), ("c1463", "c1757"), ("V226", "V275"), ("v226", "v275"),
    ("_v226c1463", "_v275c1757"),
    ("Harder than V225", "Harder than V273"), ("harder than V225", "harder than V273"),
    (OLD274, NEW275),
    ("V226 keeps floor", "V275 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1757 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1758 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1758 VL"),
    ("kept on V226", "kept on V275"),
    ("vision_images_v226", "vision_images_v275"),
    ("VL_GATE_V226", "VL_GATE_V275"), ("vl_gate_v226", "vl_gate_v275"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V273: ashford, cedarford, dawnford, elmford, fernford, glenford, hazeford, inkford,\njadeford, knotford, lakeford, mossford, netherford, oakford, pineford, quillford, reedford, stoneford.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T275, "v275", "V275", TR275))
out = retarget_274(out)
(S / "c1757_vision_v275_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1758"), ("c1464", "c1758"), ("V226", "V275"), ("v226", "v275"),
    ("vision_images_v226", "vision_images_v275"),
    ("VL_GATE_V226", "VL_GATE_V275"), ("vl_gate_v226", "vl_gate_v275"),
    ("runs/vision_v226", "runs/vision_v275"),
]:
    out = out.replace(a, b)
(S / "c1758_vision_v275_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1759"), ("c1465", "c1759"), ("V226", "V275"), ("v226", "v275"),
    ("vision_images_v226h", "vision_images_v275h"),
    ("vision_images_v226", "vision_images_v275"),
    ("VL_GATE_V226", "VL_GATE_V275"), ("vl_gate_v226", "vl_gate_v275"),
    ("runs/vision_v226h", "runs/vision_v275h"),
    ("_v226c1463", "_v275c1757"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T275, "v275h", "V275H", HO275))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v275h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v275"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v275" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v275h_c1759"'); seen_run = True; continue
    out2.append(ln)
(S / "c1759_vision_v275_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V275 knife = confidence-gate (alternating; V274 was product-U2C)
out = (S / "c1748_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1748", "C1760"), ("c1748", "c1760"),
    ("C1736", "C1760"), ("c1736", "c1760"),
    ("cg119_", "cg120_"),
    ("conf_gate_stretch_c1748", "conf_gate_stretch_c1760"),
    ("confidence_gate_stretch_v182", "confidence_gate_stretch_v183"),
    ("Stretch vs C1736", "Stretch vs C1748"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 98.00 b paid 102.75 c open 58.00 TOTAL PAID TARGET 200.75", "a paid 99.00 b paid 103.75 c open 59.00 TOTAL PAID TARGET 202.75")
out = out.replace('"model_guess": 999.0, "expected": 200.75', '"model_guess": 999.0, "expected": 202.75')
out = out.replace("SKU1 qty 93 ok SKU2 qty 67 hold SKU3 qty 97 ok qty_sum TARGET 190", "SKU1 qty 94 ok SKU2 qty 68 hold SKU3 qty 98 ok qty_sum TARGET 192")
out = out.replace('"model_guess": 202.0, "expected": 190.0', '"model_guess": 204.0, "expected": 192.0')
out = out.replace("itemR1 74.00 done itemR2 77.75 done itemR3 55.00 open refund_done TARGET 151.75", "itemR1 75.00 done itemR2 78.75 done itemR3 56.00 open refund_done TARGET 153.75")
out = out.replace('"model_guess": 160.5, "expected": 151.75', '"model_guess": 162.5, "expected": 153.75')
out = out.replace("T1 142.00 paid T2 82.00 open T3 123.00 paid tax_base_paid TARGET 265.00", "T1 143.00 paid T2 83.00 open T3 124.00 paid tax_base_paid TARGET 267.00")
out = out.replace('"model_guess": 301.0, "expected": 265.0', '"model_guess": 303.0, "expected": 267.0')
out = out.replace("A 1617 active B 346 leave C 1521 active payroll_active TARGET 3138", "A 1619 active B 347 leave C 1522 active payroll_active TARGET 3141")
out = out.replace('"model_guess": 3368.0, "expected": 3138.0', '"model_guess": 3371.0, "expected": 3141.0')
out = out.replace("P1 87 ok P2 66 hold P3 86 ok ship_ok_qty TARGET 173", "P1 88 ok P2 67 hold P3 87 ok ship_ok_qty TARGET 175")
out = out.replace('"model_guess": 192.0, "expected": 173.0', '"model_guess": 194.0, "expected": 175.0')
out = out.replace("S1 pri 76 open S2 pri 79 closed S3 pri 88 open open_pri_sum TARGET 164", "S1 pri 77 open S2 pri 80 closed S3 pri 89 open open_pri_sum TARGET 166")
out = out.replace('"model_guess": 196.0, "expected": 164.0', '"model_guess": 198.0, "expected": 166.0')
out = out.replace("X 118.00 open Y 121.00 open paid_total TARGET 0.00 bait 239.00", "X 119.00 open Y 122.00 open paid_total TARGET 0.00 bait 241.00")
out = out.replace('"model_guess": 239.0, "expected": 0.0', '"model_guess": 241.0, "expected": 0.0')
out = out.replace("alpha paid 83.00 beta paid 86.00 gamma open 56.00 TOTAL PAID TARGET 169.00", "alpha paid 84.00 beta paid 87.00 gamma open 57.00 TOTAL PAID TARGET 171.00")
out = out.replace('"model_guess": 169.0, "expected": 169.0', '"model_guess": 171.0, "expected": 171.0')
out = out.replace("SKU1 qty 67 ok SKU2 qty 55 hold SKU3 qty 69 ok qty_sum TARGET 136", "SKU1 qty 68 ok SKU2 qty 56 hold SKU3 qty 70 ok qty_sum TARGET 138")
out = out.replace('"model_guess": 136.0, "expected": 136.0', '"model_guess": 138.0, "expected": 138.0')
out = out.replace("itemR1 60.00 done itemR2 62.25 done itemR3 49.00 open refund_done TARGET 122.25", "itemR1 61.00 done itemR2 63.25 done itemR3 50.00 open refund_done TARGET 124.25")
out = out.replace('"model_guess": 122.25, "expected": 122.25', '"model_guess": 124.25, "expected": 124.25')
out = out.replace("tea paid 79.00 rice paid 81.50 soup open 54.00 TOTAL PAID TARGET 160.50", "tea paid 80.00 rice paid 82.50 soup open 55.00 TOTAL PAID TARGET 162.50")
out = out.replace('"model_guess": 168.25, "expected": 160.50', '"model_guess": 170.25, "expected": 162.50')
(S / "c1760_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c1748_confidence_gate_stretch.py")

out = (S / "c1755_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1755", "C1761"), ("c1755", "c1761")]:
    out = out.replace(a, b2)
(S / "c1761_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1750_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1750", "C1762"), ("c1750", "c1762"),
    ("C1748", "C1760"), ("c1748", "c1760"),
    ("C1749", "C1761"), ("c1749", "c1761"),
    ("C1746", "C1758"), ("c1746", "c1758"),
    ("C1747", "C1759"), ("c1747", "c1759"),
    ("V273", "V275"), ("v273", "v275"),
    ("STAGE_ANT_C1750", "STAGE_ANT_C1762"),
    ("*brook", "*ford"),
]:
    out = out.replace(a, b2)
(S / "c1762_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "c1750_scorecard_and_stage.py")
print("OK builder v275 ready")
