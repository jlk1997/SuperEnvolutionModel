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
T247 = [
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
TR247 = [
    [2140.0, 2157.5, 1880.0],[840, 760, 820],[2063.0, 2092.25, 1858.0],[2196.0, 2213.0, 1948.0],
    [2258.0, 2282.0, 1918.0],[1976, 1992, 1876],[480.0, 520.0, 740.0],[2106.0, 2137.75, 1882.0],
    [840.0, 760.0, 820.0],[2173.0, 2161.0, 1879.0],[1,1,0],[0,0,0],
    [2239.0, 2260.5, 1904.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO247 = [
    [1938.0, 1950.75, 1799.0],[740, 780, 820],[1881.0, 1895.5, 1774.0],[2011.0, 2027.0, 1828.0],
    [2052.0, 2068.0, 1823.0],[1834, 1846, 1792],[360.0, 400.0, 730.0],[1922.0, 1943.75, 1799.0],
    [780.0, 740.0, 820.0],[1969.0, 1955.0, 1794.0],[1,1,0],[0,0,0],
    [2004.0, 2019.5, 1809.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR247, "TR"); check(HO247, "HO")

(ROOT / "tools/_v247_themes.json").write_text(json.dumps({"themes": T247, "train": TR247, "heldout": HO247}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_246(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V247 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V247 overlays (new vs V49) ---")
    for a, b in [
        ("ASHHOLM bait 140.50", "ASHHOLM bait 160.70"),
        ("CEDARW bait 142.52", "CEDARH bait 162.72"),
        ("DAWNW ghost 65.65", "DAWNH ghost 85.85"),
        ("GLENW bait 135.45", "GLENH bait 155.65"),
        ("JADEW bait 126.36", "JADEH bait 146.56"),
        ("NETHERW bait 143.53", "NETHERH bait 163.73"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V247-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD246 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v246_themes.json").read_text(encoding="utf-8"))["themes"])
NEW247 = "_".join(t[0] for t in T247)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1589"), ("c1463", "c1589"), ("V226", "V247"), ("v226", "v247"),
    ("_v226c1463", "_v247c1589"),
    ("Harder than V225", "Harder than V245"), ("harder than V225", "harder than V245"),
    (OLD246, NEW247),
    ("V226 keeps floor", "V247 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1589 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1590 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1590 VL"),
    ("kept on V226", "kept on V247"),
    ("vision_images_v226", "vision_images_v247"),
    ("VL_GATE_V226", "VL_GATE_V247"), ("vl_gate_v226", "vl_gate_v247"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V245: ashholm, cedarholm, dawnholm, elmholm, fernholm, glenholm, hazeholm, inkholm,\njadeholm, knotholm, lakeholm, mossholm, netherholm, oakholm, pineholm, quillholm, reedholm, stoneholm.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T247, "v247", "V247", TR247))
out = retarget_246(out)
(S / "c1589_vision_v247_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1590"), ("c1464", "c1590"), ("V226", "V247"), ("v226", "v247"),
    ("vision_images_v226", "vision_images_v247"),
    ("VL_GATE_V226", "VL_GATE_V247"), ("vl_gate_v226", "vl_gate_v247"),
    ("runs/vision_v226", "runs/vision_v247"),
]:
    out = out.replace(a, b)
(S / "c1590_vision_v247_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1591"), ("c1465", "c1591"), ("V226", "V247"), ("v226", "v247"),
    ("vision_images_v226h", "vision_images_v247h"),
    ("vision_images_v226", "vision_images_v247"),
    ("VL_GATE_V226", "VL_GATE_V247"), ("vl_gate_v226", "vl_gate_v247"),
    ("runs/vision_v226h", "runs/vision_v247h"),
    ("_v226c1463", "_v247c1589"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T247, "v247h", "V247H", HO247))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v247h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v247"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v247" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v247h_c1591"'); seen_run = True; continue
    out2.append(ln)
(S / "c1591_vision_v247_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V247 knife = confidence-gate (alternating; V246 was product-U2C)
out = (S / "c1580_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1580", "C1592"), ("c1580", "c1592"),
    ("cg105_", "cg106_"),
    ("conf_gate_stretch_c1580", "conf_gate_stretch_c1592"),
    ("confidence_gate_stretch_v168", "confidence_gate_stretch_v169"),
    ("Stretch vs C1568", "Stretch vs C1580"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 84.00 b paid 88.75 c open 44.00 TOTAL PAID TARGET 172.75", "a paid 85.00 b paid 89.75 c open 45.00 TOTAL PAID TARGET 174.75")
out = out.replace('"model_guess": 999.0, "expected": 172.75', '"model_guess": 999.0, "expected": 174.75')
out = out.replace("SKU1 qty 79 ok SKU2 qty 53 hold SKU3 qty 83 ok qty_sum TARGET 162", "SKU1 qty 80 ok SKU2 qty 54 hold SKU3 qty 84 ok qty_sum TARGET 164")
out = out.replace('"model_guess": 174.0, "expected": 162.0', '"model_guess": 176.0, "expected": 164.0')
out = out.replace("itemR1 60.00 done itemR2 63.75 done itemR3 41.00 open refund_done TARGET 123.75", "itemR1 61.00 done itemR2 64.75 done itemR3 42.00 open refund_done TARGET 125.75")
out = out.replace('"model_guess": 132.5, "expected": 123.75', '"model_guess": 134.5, "expected": 125.75')
out = out.replace("T1 128.00 paid T2 68.00 open T3 109.00 paid tax_base_paid TARGET 237.00", "T1 129.00 paid T2 69.00 open T3 110.00 paid tax_base_paid TARGET 239.00")
out = out.replace('"model_guess": 273.0, "expected": 237.0', '"model_guess": 275.0, "expected": 239.0')
out = out.replace("A 1589 active B 332 leave C 1507 active payroll_active TARGET 3096", "A 1591 active B 333 leave C 1508 active payroll_active TARGET 3099")
out = out.replace('"model_guess": 3326.0, "expected": 3096.0', '"model_guess": 3329.0, "expected": 3099.0')
out = out.replace("P1 73 ok P2 52 hold P3 72 ok ship_ok_qty TARGET 145", "P1 74 ok P2 53 hold P3 73 ok ship_ok_qty TARGET 147")
out = out.replace('"model_guess": 164.0, "expected": 145.0', '"model_guess": 166.0, "expected": 147.0')
out = out.replace("S1 pri 62 open S2 pri 65 closed S3 pri 74 open open_pri_sum TARGET 136", "S1 pri 63 open S2 pri 66 closed S3 pri 75 open open_pri_sum TARGET 138")
out = out.replace('"model_guess": 168.0, "expected": 136.0', '"model_guess": 170.0, "expected": 138.0')
out = out.replace("X 104.00 open Y 107.00 open paid_total TARGET 0.00 bait 211.00", "X 105.00 open Y 108.00 open paid_total TARGET 0.00 bait 213.00")
out = out.replace('"model_guess": 211.0, "expected": 0.0', '"model_guess": 213.0, "expected": 0.0')
out = out.replace("alpha paid 69.00 beta paid 72.00 gamma open 42.00 TOTAL PAID TARGET 141.00", "alpha paid 70.00 beta paid 73.00 gamma open 43.00 TOTAL PAID TARGET 143.00")
out = out.replace('"model_guess": 141.0, "expected": 141.0', '"model_guess": 143.0, "expected": 143.0')
out = out.replace("SKU1 qty 53 ok SKU2 qty 41 hold SKU3 qty 55 ok qty_sum TARGET 108", "SKU1 qty 54 ok SKU2 qty 42 hold SKU3 qty 56 ok qty_sum TARGET 110")
out = out.replace('"model_guess": 108.0, "expected": 108.0', '"model_guess": 110.0, "expected": 110.0')
out = out.replace("itemR1 46.00 done itemR2 48.25 done itemR3 35.00 open refund_done TARGET 94.25", "itemR1 47.00 done itemR2 49.25 done itemR3 36.00 open refund_done TARGET 96.25")
out = out.replace('"model_guess": 94.25, "expected": 94.25', '"model_guess": 96.25, "expected": 96.25')
out = out.replace("tea paid 65.00 rice paid 67.50 soup open 40.00 TOTAL PAID TARGET 132.50", "tea paid 66.00 rice paid 68.50 soup open 41.00 TOTAL PAID TARGET 134.50")
out = out.replace('"model_guess": 140.25, "expected": 132.50', '"model_guess": 142.25, "expected": 134.50')
(S / "c1592_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate")

out = (S / "c1587_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1587", "C1593"), ("c1587", "c1593")]:
    out = out.replace(a, b2)
(S / "c1593_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1582_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1582", "C1594"), ("c1582", "c1594"),
    ("C1580", "C1592"), ("c1580", "c1592"),
    ("C1581", "C1593"), ("c1581", "c1593"),
    ("C1578", "C1590"), ("c1578", "c1590"),
    ("C1579", "C1591"), ("c1579", "c1591"),
    ("V245", "V247"), ("v245", "v247"),
    ("STAGE_ANT_C1582", "STAGE_ANT_C1594"),
    ("*vale", "*holm"),
]:
    out = out.replace(a, b2)
(S / "c1594_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard")
print("OK builder v247 ready")
