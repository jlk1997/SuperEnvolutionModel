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

# *holm ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T291 = [
    ["ashholm","recv","paid_total","ASHHOLM GRAIN RECV","RECV","x"],
    ["cedarholm","wh","qty_sum","WH CEDARHOLM BIN","RECV","x"],
    ["dawnholm","refund","refund_done","DAWNHOLM PATCH REFUND","DONE","x"],
    ["elmholm","tax","tax_base_paid","ELMHOLM TAX SLIP","TAX","x"],
    ["fernholm","pay","payroll_active","FERNHOLM PAYROLL","PAY","x"],
    ["glenholm","ship","ship_ok","GLENHOLM SHIP DOCK","SHIP","x"],
    ["hazeholm","sla","sla_ok_hours","HAZEHOLM SLA CARD","SLA","x"],
    ["inkholm","exp","exp_sum","INKHOLM EXPENSE","EXP","x"],
    ["jadeholm","po","po_open","JADEHOLM PO SHEET","PO","x"],
    ["knotholm","order","order_paid","KNOTHOLM ORDER","ORD","x"],
    ["lakeholm","dup","dup_mark","LAKEHOLM DUP MARK","DUP","x"],
    ["mossholm","zero","zero_check","MOSSHOLM AIR ZERO","ZERO","x"],
    ["netherholm","ledger","ledger_net","NETHERHOLM LEDGER","LED","x"],
    ["oakholm","ui","ui_ok","OAKHOLM UI SCAN","UI","x"],
    ["pineholm","stack","stack_count","PINEHOLM STACK","STK","x"],
    ["quillholm","fax","fax_pages","QUILLHOLM FAX","FAX","x"],
    ["reedholm","glare","glare_ok","REEDHOLM GLARE","GLR","x"],
    ["stoneholm","tab","tab_index","STONEHOLM TAB INDEX","TAB","x"],
]
TR291 = [
    [2246.0, 2263.5, 1986.0],[840, 760, 820],[2169.0, 2198.25, 1964.0],[2302.0, 2319.0, 2054.0],
    [2364.0, 2388.0, 2024.0],[2082, 2098, 1982],[490.0, 530.0, 760.0],[2212.0, 2243.75, 1988.0],
    [840.0, 760.0, 820.0],[2279.0, 2267.0, 1985.0],[1,1,0],[0,0,0],
    [2345.0, 2366.5, 2010.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO291 = [
    [2044.0, 2056.75, 1905.0],[640, 660, 820],[1987.0, 2001.5, 1880.0],[2117.0, 2133.0, 1936.0],
    [2158.0, 2174.0, 1929.0],[1940, 1952, 1900],[420.0, 460.0, 740.0],[2028.0, 2049.75, 1905.0],
    [740.0, 780.0, 820.0],[2075.0, 2061.0, 1902.0],[1,1,0],[0,0,0],
    [2110.0, 2125.5, 1915.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR291, "TR"); check(HO291, "HO")

(ROOT / "tools/_v291_themes.json").write_text(json.dumps({"themes": T291, "train": TR291, "heldout": HO291}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_290(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V291 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V291 overlays (new vs V49) ---")
    for a, b in [
        ("ASHHOLM bait 140.50", "ASHHOLM bait 185.95"),
        ("CEDARW bait 142.52", "CEDARH bait 206.16"),
        ("DAWNW ghost 65.65", "DAWNH ghost 129.39"),
        ("GLENW bait 135.45", "GLENH bait 199.09"),
        ("JADEW bait 126.36", "JADEH bait 190.00"),
        ("NETHERW bait 143.53", "NETHERH bait 207.17"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V291-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD290 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v290_themes.json").read_text(encoding="utf-8"))["themes"])
NEW291 = "_".join(t[0] for t in T291)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1853"), ("c1463", "c1853"), ("V226", "V291"), ("v226", "v291"),
    ("_v226c1463", "_v291c1853"),
    ("Harder than V225", "Harder than V289"), ("harder than V225", "harder than V289"),
    (OLD290, NEW291),
    ("V226 keeps floor", "V291 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1853 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1854 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1854 VL"),
    ("kept on V226", "kept on V291"),
    ("vision_images_v226", "vision_images_v291"),
    ("VL_GATE_V226", "VL_GATE_V291"), ("vl_gate_v226", "vl_gate_v291"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V289: ashholm, cedarholm, dawnholm, elmholm, fernholm, glenholm, hazeholm, inkholm,\njadeholm, knotholm, lakeholm, mossholm, netherholm, oakholm, pineholm, quillholm, reedholm, stoneholm.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T291, "v291", "V291", TR291))
out = retarget_290(out)
(S / "c1853_vision_v291_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1854"), ("c1464", "c1854"), ("V226", "V291"), ("v226", "v291"),
    ("vision_images_v226", "vision_images_v291"),
    ("VL_GATE_V226", "VL_GATE_V291"), ("vl_gate_v226", "vl_gate_v291"),
    ("runs/vision_v226", "runs/vision_v291"),
]:
    out = out.replace(a, b)
(S / "c1854_vision_v291_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1855"), ("c1465", "c1855"), ("V226", "V291"), ("v226", "v291"),
    ("vision_images_v226h", "vision_images_v291h"),
    ("vision_images_v226", "vision_images_v291"),
    ("VL_GATE_V226", "VL_GATE_V291"), ("vl_gate_v226", "vl_gate_v291"),
    ("runs/vision_v226h", "runs/vision_v291h"),
    ("_v226c1463", "_v291c1853"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T291, "v291h", "V291H", HO291))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v291h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v291"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v291" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v291h_c1855"'); seen_run = True; continue
    out2.append(ln)
(S / "c1855_vision_v291_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V291 knife = confidence-gate (alternating; V290 was product-U2C)
out = (S / "c1844_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1844", "C1856"), ("c1844", "c1856"),
    ("C1832", "C1856"), ("c1832", "c1856"),
    ("cg127_", "cg128_"),
    ("conf_gate_stretch_c1844", "conf_gate_stretch_c1856"),
    ("confidence_gate_stretch_v190", "confidence_gate_stretch_v191"),
    ("Stretch vs C1832", "Stretch vs C1844"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 106.00 b paid 110.75 c open 66.00 TOTAL PAID TARGET 216.75", "a paid 107.00 b paid 111.75 c open 67.00 TOTAL PAID TARGET 218.75")
out = out.replace('"model_guess": 999.0, "expected": 216.75', '"model_guess": 999.0, "expected": 218.75')
out = out.replace("SKU1 qty 101 ok SKU2 qty 75 hold SKU3 qty 105 ok qty_sum TARGET 206", "SKU1 qty 102 ok SKU2 qty 76 hold SKU3 qty 106 ok qty_sum TARGET 208")
out = out.replace('"model_guess": 218.0, "expected": 206.0', '"model_guess": 220.0, "expected": 208.0')
out = out.replace("itemR1 82.00 done itemR2 85.75 done itemR3 63.00 open refund_done TARGET 167.75", "itemR1 83.00 done itemR2 86.75 done itemR3 64.00 open refund_done TARGET 169.75")
out = out.replace('"model_guess": 176.5, "expected": 167.75', '"model_guess": 178.5, "expected": 169.75')
out = out.replace("T1 150.00 paid T2 90.00 open T3 131.00 paid tax_base_paid TARGET 281.00", "T1 151.00 paid T2 91.00 open T3 132.00 paid tax_base_paid TARGET 283.00")
out = out.replace('"model_guess": 317.0, "expected": 281.0', '"model_guess": 319.0, "expected": 283.0')
out = out.replace("A 1633 active B 354 leave C 1529 active payroll_active TARGET 3162", "A 1635 active B 355 leave C 1530 active payroll_active TARGET 3165")
out = out.replace('"model_guess": 3392.0, "expected": 3162.0', '"model_guess": 3395.0, "expected": 3165.0')
out = out.replace("P1 95 ok P2 74 hold P3 94 ok ship_ok_qty TARGET 189", "P1 96 ok P2 75 hold P3 95 ok ship_ok_qty TARGET 191")
out = out.replace('"model_guess": 208.0, "expected": 189.0', '"model_guess": 210.0, "expected": 191.0')
out = out.replace("S1 pri 84 open S2 pri 87 closed S3 pri 96 open open_pri_sum TARGET 180", "S1 pri 85 open S2 pri 88 closed S3 pri 97 open open_pri_sum TARGET 182")
out = out.replace('"model_guess": 212.0, "expected": 180.0', '"model_guess": 214.0, "expected": 182.0')
out = out.replace("X 126.00 open Y 129.00 open paid_total TARGET 0.00 bait 255.00", "X 127.00 open Y 130.00 open paid_total TARGET 0.00 bait 257.00")
out = out.replace('"model_guess": 255.0, "expected": 0.0', '"model_guess": 257.0, "expected": 0.0')
out = out.replace("alpha paid 91.00 beta paid 94.00 gamma open 64.00 TOTAL PAID TARGET 185.00", "alpha paid 92.00 beta paid 95.00 gamma open 65.00 TOTAL PAID TARGET 187.00")
out = out.replace('"model_guess": 185.0, "expected": 185.0', '"model_guess": 187.0, "expected": 187.0')
out = out.replace("SKU1 qty 75 ok SKU2 qty 63 hold SKU3 qty 77 ok qty_sum TARGET 152", "SKU1 qty 76 ok SKU2 qty 64 hold SKU3 qty 78 ok qty_sum TARGET 154")
out = out.replace('"model_guess": 152.0, "expected": 152.0', '"model_guess": 154.0, "expected": 154.0')
out = out.replace("itemR1 68.00 done itemR2 70.25 done itemR3 57.00 open refund_done TARGET 138.25", "itemR1 69.00 done itemR2 71.25 done itemR3 58.00 open refund_done TARGET 140.25")
out = out.replace('"model_guess": 138.25, "expected": 138.25', '"model_guess": 140.25, "expected": 140.25')
out = out.replace("tea paid 87.00 rice paid 89.50 soup open 62.00 TOTAL PAID TARGET 176.50", "tea paid 88.00 rice paid 90.50 soup open 63.00 TOTAL PAID TARGET 178.50")
out = out.replace('"model_guess": 184.25, "expected": 176.50', '"model_guess": 186.25, "expected": 178.50')
(S / "c1856_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c1844_confidence_gate_stretch.py")

out = (S / "c1851_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1851", "C1857"), ("c1851", "c1857")]:
    out = out.replace(a, b2)
(S / "c1857_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1846_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1846", "C1858"), ("c1846", "c1858"),
    ("C1844", "C1856"), ("c1844", "c1856"),
    ("C1845", "C1857"), ("c1845", "c1857"),
    ("C1842", "C1854"), ("c1842", "c1854"),
    ("C1843", "C1855"), ("c1843", "c1855"),
    ("V289", "V291"), ("v289", "v291"),
    ("STAGE_ANT_C1846", "STAGE_ANT_C1858"),
    ("*vale", "*holm"),
]:
    out = out.replace(a, b2)
(S / "c1858_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "c1846_scorecard_and_stage.py")
print("OK builder v291 ready")
