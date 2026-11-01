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

# *moor ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T249 = [
    ["ashmoor","recv","paid_total","ASHMOOR GRAIN RECV","RECV","x"],
    ["cedarmoor","wh","qty_sum","WH CEDARMOOR BIN","RECV","x"],
    ["dawnmoor","refund","refund_done","DAWNMOOR PATCH REFUND","DONE","x"],
    ["elmmoor","tax","tax_base_paid","ELMMOOR TAX SLIP","TAX","x"],
    ["fernmoor","pay","payroll_active","FERNMOOR PAYROLL","PAY","x"],
    ["glenmoor","ship","ship_ok","GLENMOOR SHIP DOCK","SHIP","x"],
    ["hazemoor","sla","sla_ok_hours","HAZEMOOR SLA CARD","SLA","x"],
    ["inkmoor","exp","exp_sum","INKMOOR EXPENSE","EXP","x"],
    ["jademoor","po","po_open","JADEMOOR PO SHEET","PO","x"],
    ["knotmoor","order","order_paid","KNOTMOOR ORDER","ORD","x"],
    ["lakemoor","dup","dup_mark","LAKEMOOR DUP MARK","DUP","x"],
    ["mossmoor","zero","zero_check","MOSSMOOR AIR ZERO","ZERO","x"],
    ["nethermoor","ledger","ledger_net","NETHERMOOR LEDGER","LED","x"],
    ["oakmoor","ui","ui_ok","OAKMOOR UI SCAN","UI","x"],
    ["pinemoor","stack","stack_count","PINEMOOR STACK","STK","x"],
    ["quillmoor","fax","fax_pages","QUILLMOOR FAX","FAX","x"],
    ["reedmoor","glare","glare_ok","REEDMOOR GLARE","GLR","x"],
    ["stonemoor","tab","tab_index","STONEMOOR TAB INDEX","TAB","x"],
]
TR249 = [
    [2144.0, 2161.5, 1884.0],[840, 760, 820],[2067.0, 2096.25, 1862.0],[2200.0, 2217.0, 1952.0],
    [2262.0, 2286.0, 1922.0],[1980, 1996, 1880],[480.0, 520.0, 740.0],[2110.0, 2141.75, 1886.0],
    [840.0, 760.0, 820.0],[2177.0, 2165.0, 1883.0],[1,1,0],[0,0,0],
    [2243.0, 2264.5, 1908.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO249 = [
    [1942.0, 1954.75, 1803.0],[740, 780, 820],[1885.0, 1899.5, 1778.0],[2015.0, 2031.0, 1834.0],
    [2056.0, 2072.0, 1827.0],[1838, 1850, 1796],[360.0, 400.0, 730.0],[1926.0, 1947.75, 1803.0],
    [780.0, 740.0, 820.0],[1973.0, 1959.0, 1798.0],[1,1,0],[0,0,0],
    [2008.0, 2023.5, 1813.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR249, "TR"); check(HO249, "HO")

(ROOT / "tools/_v249_themes.json").write_text(json.dumps({"themes": T249, "train": TR249, "heldout": HO249}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_248(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V249 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V249 overlays (new vs V49) ---")
    for a, b in [
        ("ASHMOOR bait 140.50", "ASHMOOR bait 162.72"),
        ("CEDARW bait 142.52", "CEDARM bait 164.74"),
        ("DAWNW ghost 65.65", "DAWNM ghost 87.87"),
        ("GLENW bait 135.45", "GLENM bait 157.67"),
        ("JADEW bait 126.36", "JADEM bait 148.58"),
        ("NETHERW bait 143.53", "NETHERM bait 165.75"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V249-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD248 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v248_themes.json").read_text(encoding="utf-8"))["themes"])
NEW249 = "_".join(t[0] for t in T249)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1601"), ("c1463", "c1601"), ("V226", "V249"), ("v226", "v249"),
    ("_v226c1463", "_v249c1601"),
    ("Harder than V225", "Harder than V247"), ("harder than V225", "harder than V247"),
    (OLD248, NEW249),
    ("V226 keeps floor", "V249 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1601 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1602 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1602 VL"),
    ("kept on V226", "kept on V249"),
    ("vision_images_v226", "vision_images_v249"),
    ("VL_GATE_V226", "VL_GATE_V249"), ("vl_gate_v226", "vl_gate_v249"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V247: ashmoor, cedarmoor, dawnmoor, elmmoor, fernmoor, glenmoor, hazemoor, inkmoor,\njademoor, knotmoor, lakemoor, mossmoor, nethermoor, oakmoor, pinemoor, quillmoor, reedmoor, stonemoor.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T249, "v249", "V249", TR249))
out = retarget_248(out)
(S / "c1601_vision_v249_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1602"), ("c1464", "c1602"), ("V226", "V249"), ("v226", "v249"),
    ("vision_images_v226", "vision_images_v249"),
    ("VL_GATE_V226", "VL_GATE_V249"), ("vl_gate_v226", "vl_gate_v249"),
    ("runs/vision_v226", "runs/vision_v249"),
]:
    out = out.replace(a, b)
(S / "c1602_vision_v249_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1603"), ("c1465", "c1603"), ("V226", "V249"), ("v226", "v249"),
    ("vision_images_v226h", "vision_images_v249h"),
    ("vision_images_v226", "vision_images_v249"),
    ("VL_GATE_V226", "VL_GATE_V249"), ("vl_gate_v226", "vl_gate_v249"),
    ("runs/vision_v226h", "runs/vision_v249h"),
    ("_v226c1463", "_v249c1601"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T249, "v249h", "V249H", HO249))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v249h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v249"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v249" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v249h_c1603"'); seen_run = True; continue
    out2.append(ln)
(S / "c1603_vision_v249_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V249 knife = confidence-gate (alternating; V248 was product-U2C)
out = (S / "c1592_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1592", "C1604"), ("c1592", "c1604"),
    ("C1580", "C1604"), ("c1580", "c1604"),
    ("cg106_", "cg107_"),
    ("conf_gate_stretch_c1592", "conf_gate_stretch_c1604"),
    ("confidence_gate_stretch_v169", "confidence_gate_stretch_v170"),
    ("Stretch vs C1580", "Stretch vs C1592"),
]:
    out = out.replace(a, b2)
# light money bump from V247 stretch targets
out = out.replace("a paid 85.00 b paid 89.75 c open 45.00 TOTAL PAID TARGET 174.75", "a paid 86.00 b paid 90.75 c open 46.00 TOTAL PAID TARGET 176.75")
out = out.replace('"model_guess": 999.0, "expected": 174.75', '"model_guess": 999.0, "expected": 176.75')
out = out.replace("SKU1 qty 80 ok SKU2 qty 54 hold SKU3 qty 84 ok qty_sum TARGET 164", "SKU1 qty 81 ok SKU2 qty 55 hold SKU3 qty 85 ok qty_sum TARGET 166")
out = out.replace('"model_guess": 176.0, "expected": 164.0', '"model_guess": 178.0, "expected": 166.0')
out = out.replace("itemR1 61.00 done itemR2 64.75 done itemR3 42.00 open refund_done TARGET 125.75", "itemR1 62.00 done itemR2 65.75 done itemR3 43.00 open refund_done TARGET 127.75")
out = out.replace('"model_guess": 134.5, "expected": 125.75', '"model_guess": 136.5, "expected": 127.75')
out = out.replace("T1 129.00 paid T2 69.00 open T3 110.00 paid tax_base_paid TARGET 239.00", "T1 130.00 paid T2 70.00 open T3 111.00 paid tax_base_paid TARGET 241.00")
out = out.replace('"model_guess": 275.0, "expected": 239.0', '"model_guess": 277.0, "expected": 241.0')
out = out.replace("A 1591 active B 333 leave C 1508 active payroll_active TARGET 3099", "A 1593 active B 334 leave C 1509 active payroll_active TARGET 3102")
out = out.replace('"model_guess": 3329.0, "expected": 3099.0', '"model_guess": 3332.0, "expected": 3102.0')
out = out.replace("P1 74 ok P2 53 hold P3 73 ok ship_ok_qty TARGET 147", "P1 75 ok P2 54 hold P3 74 ok ship_ok_qty TARGET 149")
out = out.replace('"model_guess": 166.0, "expected": 147.0', '"model_guess": 168.0, "expected": 149.0')
out = out.replace("S1 pri 63 open S2 pri 66 closed S3 pri 75 open open_pri_sum TARGET 138", "S1 pri 64 open S2 pri 67 closed S3 pri 76 open open_pri_sum TARGET 140")
out = out.replace('"model_guess": 170.0, "expected": 138.0', '"model_guess": 172.0, "expected": 140.0')
out = out.replace("X 105.00 open Y 108.00 open paid_total TARGET 0.00 bait 213.00", "X 106.00 open Y 109.00 open paid_total TARGET 0.00 bait 215.00")
out = out.replace('"model_guess": 213.0, "expected": 0.0', '"model_guess": 215.0, "expected": 0.0')
out = out.replace("alpha paid 70.00 beta paid 73.00 gamma open 43.00 TOTAL PAID TARGET 143.00", "alpha paid 71.00 beta paid 74.00 gamma open 44.00 TOTAL PAID TARGET 145.00")
out = out.replace('"model_guess": 143.0, "expected": 143.0', '"model_guess": 145.0, "expected": 145.0')
out = out.replace("SKU1 qty 54 ok SKU2 qty 42 hold SKU3 qty 56 ok qty_sum TARGET 110", "SKU1 qty 55 ok SKU2 qty 43 hold SKU3 qty 57 ok qty_sum TARGET 112")
out = out.replace('"model_guess": 110.0, "expected": 110.0', '"model_guess": 112.0, "expected": 112.0')
out = out.replace("itemR1 47.00 done itemR2 49.25 done itemR3 36.00 open refund_done TARGET 96.25", "itemR1 48.00 done itemR2 50.25 done itemR3 37.00 open refund_done TARGET 98.25")
out = out.replace('"model_guess": 96.25, "expected": 96.25', '"model_guess": 98.25, "expected": 98.25')
out = out.replace("tea paid 66.00 rice paid 68.50 soup open 41.00 TOTAL PAID TARGET 134.50", "tea paid 67.00 rice paid 69.50 soup open 42.00 TOTAL PAID TARGET 136.50")
out = out.replace('"model_guess": 142.25, "expected": 134.50', '"model_guess": 144.25, "expected": 136.50')
(S / "c1604_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c1592_confidence_gate_stretch.py")

out = (S / "c1599_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1599", "C1605"), ("c1599", "c1605")]:
    out = out.replace(a, b2)
(S / "c1605_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1594_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1594", "C1606"), ("c1594", "c1606"),
    ("C1592", "C1604"), ("c1592", "c1604"),
    ("C1593", "C1605"), ("c1593", "c1605"),
    ("C1590", "C1602"), ("c1590", "c1602"),
    ("C1591", "C1603"), ("c1591", "c1603"),
    ("V247", "V249"), ("v247", "v249"),
    ("STAGE_ANT_C1594", "STAGE_ANT_C1606"),
    ("*holm", "*moor"),
]:
    out = out.replace(a, b2)
(S / "c1606_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "c1594_scorecard_and_stage.py")
print("OK builder v249 ready")
