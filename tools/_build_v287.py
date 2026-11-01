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
T287 = [
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
TR287 = [
    [2236.0, 2253.5, 1976.0],[840, 760, 820],[2159.0, 2188.25, 1954.0],[2292.0, 2309.0, 2044.0],
    [2354.0, 2378.0, 2014.0],[2072, 2088, 1972],[490.0, 530.0, 760.0],[2202.0, 2233.75, 1978.0],
    [840.0, 760.0, 820.0],[2269.0, 2257.0, 1975.0],[1,1,0],[0,0,0],
    [2335.0, 2356.5, 2000.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO287 = [
    [2034.0, 2046.75, 1895.0],[640, 660, 820],[1977.0, 1991.5, 1870.0],[2107.0, 2123.0, 1926.0],
    [2148.0, 2164.0, 1919.0],[1930, 1942, 1890],[420.0, 460.0, 740.0],[2018.0, 2039.75, 1895.0],
    [740.0, 780.0, 820.0],[2065.0, 2051.0, 1892.0],[1,1,0],[0,0,0],
    [2100.0, 2115.5, 1905.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR287, "TR"); check(HO287, "HO")

(ROOT / "tools/_v287_themes.json").write_text(json.dumps({"themes": T287, "train": TR287, "heldout": HO287}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_286(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V287 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V287 overlays (new vs V49) ---")
    for a, b in [
        ("ASHHURST bait 140.50", "ASHHURST bait 185.95"),
        ("CEDARW bait 142.52", "CEDARH bait 202.12"),
        ("DAWNW ghost 65.65", "DAWNH ghost 125.35"),
        ("GLENW bait 135.45", "GLENH bait 195.05"),
        ("JADEW bait 126.36", "JADEH bait 186.96"),
        ("NETHERW bait 143.53", "NETHERH bait 203.13"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V287-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD286 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v286_themes.json").read_text(encoding="utf-8"))["themes"])
NEW287 = "_".join(t[0] for t in T287)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1829"), ("c1463", "c1829"), ("V226", "V287"), ("v226", "v287"),
    ("_v226c1463", "_v287c1829"),
    ("Harder than V225", "Harder than V285"), ("harder than V225", "harder than V285"),
    (OLD286, NEW287),
    ("V226 keeps floor", "V287 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1829 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1830 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1830 VL"),
    ("kept on V226", "kept on V287"),
    ("vision_images_v226", "vision_images_v287"),
    ("VL_GATE_V226", "VL_GATE_V287"), ("vl_gate_v226", "vl_gate_v287"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V285: ashhurst, cedarhurst, dawnhurst, elmhurst, fernhurst, glenhurst, hazehurst, inkhurst,\njadehurst, knothurst, lakehurst, mosshurst, netherhurst, oakhurst, pinehurst, quillhurst, reedhurst, stonehurst.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T287, "v287", "V287", TR287))
out = retarget_286(out)
(S / "c1829_vision_v287_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1830"), ("c1464", "c1830"), ("V226", "V287"), ("v226", "v287"),
    ("vision_images_v226", "vision_images_v287"),
    ("VL_GATE_V226", "VL_GATE_V287"), ("vl_gate_v226", "vl_gate_v287"),
    ("runs/vision_v226", "runs/vision_v287"),
]:
    out = out.replace(a, b)
(S / "c1830_vision_v287_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1831"), ("c1465", "c1831"), ("V226", "V287"), ("v226", "v287"),
    ("vision_images_v226h", "vision_images_v287h"),
    ("vision_images_v226", "vision_images_v287"),
    ("VL_GATE_V226", "VL_GATE_V287"), ("vl_gate_v226", "vl_gate_v287"),
    ("runs/vision_v226h", "runs/vision_v287h"),
    ("_v226c1463", "_v287c1829"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T287, "v287h", "V287H", HO287))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v287h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v287"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v287" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v287h_c1831"'); seen_run = True; continue
    out2.append(ln)
(S / "c1831_vision_v287_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V287 knife = confidence-gate (alternating; V286 was product-U2C)
out = (S / "c1820_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1820", "C1832"), ("c1820", "c1832"),
    ("C1808", "C1832"), ("c1808", "c1832"),
    ("cg125_", "cg126_"),
    ("conf_gate_stretch_c1820", "conf_gate_stretch_c1832"),
    ("confidence_gate_stretch_v188", "confidence_gate_stretch_v189"),
    ("Stretch vs C1808", "Stretch vs C1820"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 104.00 b paid 108.75 c open 64.00 TOTAL PAID TARGET 212.75", "a paid 105.00 b paid 109.75 c open 65.00 TOTAL PAID TARGET 214.75")
out = out.replace('"model_guess": 999.0, "expected": 212.75', '"model_guess": 999.0, "expected": 214.75')
out = out.replace("SKU1 qty 99 ok SKU2 qty 73 hold SKU3 qty 103 ok qty_sum TARGET 202", "SKU1 qty 100 ok SKU2 qty 74 hold SKU3 qty 104 ok qty_sum TARGET 204")
out = out.replace('"model_guess": 214.0, "expected": 202.0', '"model_guess": 216.0, "expected": 204.0')
out = out.replace("itemR1 80.00 done itemR2 83.75 done itemR3 61.00 open refund_done TARGET 163.75", "itemR1 81.00 done itemR2 84.75 done itemR3 62.00 open refund_done TARGET 165.75")
out = out.replace('"model_guess": 172.5, "expected": 163.75', '"model_guess": 174.5, "expected": 165.75')
out = out.replace("T1 148.00 paid T2 88.00 open T3 129.00 paid tax_base_paid TARGET 277.00", "T1 149.00 paid T2 89.00 open T3 130.00 paid tax_base_paid TARGET 279.00")
out = out.replace('"model_guess": 313.0, "expected": 277.0', '"model_guess": 315.0, "expected": 279.0')
out = out.replace("A 1629 active B 352 leave C 1527 active payroll_active TARGET 3156", "A 1631 active B 353 leave C 1528 active payroll_active TARGET 3159")
out = out.replace('"model_guess": 3386.0, "expected": 3156.0', '"model_guess": 3389.0, "expected": 3159.0')
out = out.replace("P1 93 ok P2 72 hold P3 92 ok ship_ok_qty TARGET 185", "P1 94 ok P2 73 hold P3 93 ok ship_ok_qty TARGET 187")
out = out.replace('"model_guess": 204.0, "expected": 185.0', '"model_guess": 206.0, "expected": 187.0')
out = out.replace("S1 pri 82 open S2 pri 85 closed S3 pri 94 open open_pri_sum TARGET 176", "S1 pri 83 open S2 pri 86 closed S3 pri 95 open open_pri_sum TARGET 178")
out = out.replace('"model_guess": 208.0, "expected": 176.0', '"model_guess": 210.0, "expected": 178.0')
out = out.replace("X 124.00 open Y 127.00 open paid_total TARGET 0.00 bait 251.00", "X 125.00 open Y 128.00 open paid_total TARGET 0.00 bait 253.00")
out = out.replace('"model_guess": 251.0, "expected": 0.0', '"model_guess": 253.0, "expected": 0.0')
out = out.replace("alpha paid 89.00 beta paid 92.00 gamma open 62.00 TOTAL PAID TARGET 181.00", "alpha paid 90.00 beta paid 93.00 gamma open 63.00 TOTAL PAID TARGET 183.00")
out = out.replace('"model_guess": 181.0, "expected": 181.0', '"model_guess": 183.0, "expected": 183.0')
out = out.replace("SKU1 qty 73 ok SKU2 qty 61 hold SKU3 qty 75 ok qty_sum TARGET 148", "SKU1 qty 74 ok SKU2 qty 62 hold SKU3 qty 76 ok qty_sum TARGET 150")
out = out.replace('"model_guess": 148.0, "expected": 148.0', '"model_guess": 150.0, "expected": 150.0')
out = out.replace("itemR1 66.00 done itemR2 68.25 done itemR3 55.00 open refund_done TARGET 134.25", "itemR1 67.00 done itemR2 69.25 done itemR3 56.00 open refund_done TARGET 136.25")
out = out.replace('"model_guess": 134.25, "expected": 134.25', '"model_guess": 136.25, "expected": 136.25')
out = out.replace("tea paid 85.00 rice paid 87.50 soup open 60.00 TOTAL PAID TARGET 172.50", "tea paid 86.00 rice paid 88.50 soup open 61.00 TOTAL PAID TARGET 174.50")
out = out.replace('"model_guess": 180.25, "expected": 172.50', '"model_guess": 182.25, "expected": 174.50')
(S / "c1832_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c1820_confidence_gate_stretch.py")

out = (S / "c1827_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1827", "C1833"), ("c1827", "c1833")]:
    out = out.replace(a, b2)
(S / "c1833_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1822_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1822", "C1834"), ("c1822", "c1834"),
    ("C1820", "C1832"), ("c1820", "c1832"),
    ("C1821", "C1833"), ("c1821", "c1833"),
    ("C1818", "C1830"), ("c1818", "c1830"),
    ("C1819", "C1831"), ("c1819", "c1831"),
    ("V285", "V287"), ("v285", "v287"),
    ("STAGE_ANT_C1822", "STAGE_ANT_C1834"),
    ("*dale", "*hurst"),
]:
    out = out.replace(a, b2)
(S / "c1834_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "c1822_scorecard_and_stage.py")
print("OK builder v287 ready")
