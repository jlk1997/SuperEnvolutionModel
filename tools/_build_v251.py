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

# *brook ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T251 = [
    ["ashbrook","recv","paid_total","ASHBROOK GRAIN RECV","RECV","x"],
    ["cedarbrook","wh","qty_sum","WH CEDARBROOK BIN","RECV","x"],
    ["dawnbrook","refund","refund_done","DAWNBROOK PATCH REFUND","DONE","x"],
    ["elmbrook","tax","tax_base_paid","ELMBROOK TAX SLIP","TAX","x"],
    ["fernbrook","pay","payroll_active","FERNBROOK PAYROLL","PAY","x"],
    ["glenbrook","ship","ship_ok","GLENBROOK SHIP DOCK","SHIP","x"],
    ["hazebrook","sla","sla_ok_hours","HAZEBROOK SLA CARD","SLA","x"],
    ["inkbrook","exp","exp_sum","INKBROOK EXPENSE","EXP","x"],
    ["jadebrook","po","po_open","JADEBROOK PO SHEET","PO","x"],
    ["knotbrook","order","order_paid","KNOTBROOK ORDER","ORD","x"],
    ["lakebrook","dup","dup_mark","LAKEBROOK DUP MARK","DUP","x"],
    ["mossbrook","zero","zero_check","MOSSBROOK AIR ZERO","ZERO","x"],
    ["netherbrook","ledger","ledger_net","NETHERBROOK LEDGER","LED","x"],
    ["oakbrook","ui","ui_ok","OAKBROOK UI SCAN","UI","x"],
    ["pinebrook","stack","stack_count","PINEBROOK STACK","STK","x"],
    ["quillbrook","fax","fax_pages","QUILLBROOK FAX","FAX","x"],
    ["reedbrook","glare","glare_ok","REEDBROOK GLARE","GLR","x"],
    ["stonebrook","tab","tab_index","STONEBROOK TAB INDEX","TAB","x"],
]
TR251 = [
    [2148.0, 2165.5, 1888.0],[840, 760, 820],[2071.0, 2100.25, 1866.0],[2204.0, 2221.0, 1956.0],
    [2266.0, 2290.0, 1926.0],[1984, 2000, 1884],[480.0, 520.0, 740.0],[2114.0, 2145.75, 1890.0],
    [840.0, 760.0, 820.0],[2181.0, 2169.0, 1887.0],[1,1,0],[0,0,0],
    [2247.0, 2268.5, 1912.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO251 = [
    [1946.0, 1958.75, 1807.0],[740, 780, 820],[1889.0, 1903.5, 1782.0],[2019.0, 2035.0, 1838.0],
    [2060.0, 2076.0, 1831.0],[1842, 1854, 1800],[360.0, 400.0, 730.0],[1930.0, 1951.75, 1807.0],
    [780.0, 740.0, 820.0],[1977.0, 1963.0, 1802.0],[1,1,0],[0,0,0],
    [2012.0, 2027.5, 1817.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR251, "TR"); check(HO251, "HO")

(ROOT / "tools/_v251_themes.json").write_text(json.dumps({"themes": T251, "train": TR251, "heldout": HO251}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_250(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V251 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V251 overlays (new vs V49) ---")
    for a, b in [
        ("ASHBROOK bait 140.50", "ASHBROOK bait 164.74"),
        ("CEDARW bait 142.52", "CEDARB bait 166.76"),
        ("DAWNW ghost 65.65", "DAWNB ghost 89.89"),
        ("GLENW bait 135.45", "GLENB bait 159.69"),
        ("JADEW bait 126.36", "JADEB bait 150.60"),
        ("NETHERW bait 143.53", "NETHERB bait 167.77"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V251-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD250 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v250_themes.json").read_text(encoding="utf-8"))["themes"])
NEW251 = "_".join(t[0] for t in T251)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1613"), ("c1463", "c1613"), ("V226", "V251"), ("v226", "v251"),
    ("_v226c1463", "_v251c1613"),
    ("Harder than V225", "Harder than V249"), ("harder than V225", "harder than V249"),
    (OLD250, NEW251),
    ("V226 keeps floor", "V251 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1613 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1614 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1614 VL"),
    ("kept on V226", "kept on V251"),
    ("vision_images_v226", "vision_images_v251"),
    ("VL_GATE_V226", "VL_GATE_V251"), ("vl_gate_v226", "vl_gate_v251"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V249: ashbrook, cedarbrook, dawnbrook, elmbrook, fernbrook, glenbrook, hazebrook, inkbrook,\njadebrook, knotbrook, lakebrook, mossbrook, netherbrook, oakbrook, pinebrook, quillbrook, reedbrook, stonebrook.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T251, "v251", "V251", TR251))
out = retarget_250(out)
(S / "c1613_vision_v251_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1614"), ("c1464", "c1614"), ("V226", "V251"), ("v226", "v251"),
    ("vision_images_v226", "vision_images_v251"),
    ("VL_GATE_V226", "VL_GATE_V251"), ("vl_gate_v226", "vl_gate_v251"),
    ("runs/vision_v226", "runs/vision_v251"),
]:
    out = out.replace(a, b)
(S / "c1614_vision_v251_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1615"), ("c1465", "c1615"), ("V226", "V251"), ("v226", "v251"),
    ("vision_images_v226h", "vision_images_v251h"),
    ("vision_images_v226", "vision_images_v251"),
    ("VL_GATE_V226", "VL_GATE_V251"), ("vl_gate_v226", "vl_gate_v251"),
    ("runs/vision_v226h", "runs/vision_v251h"),
    ("_v226c1463", "_v251c1613"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T251, "v251h", "V251H", HO251))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v251h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v251"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v251" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v251h_c1615"'); seen_run = True; continue
    out2.append(ln)
(S / "c1615_vision_v251_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V251 knife = confidence-gate (alternating; V250 was product-U2C)
out = (S / "c1604_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1604", "C1616"), ("c1604", "c1616"),
    ("C1592", "C1616"), ("c1592", "c1616"),
    ("cg107_", "cg108_"),
    ("conf_gate_stretch_c1604", "conf_gate_stretch_c1616"),
    ("confidence_gate_stretch_v170", "confidence_gate_stretch_v171"),
    ("Stretch vs C1592", "Stretch vs C1604"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 86.00 b paid 90.75 c open 46.00 TOTAL PAID TARGET 176.75", "a paid 87.00 b paid 91.75 c open 47.00 TOTAL PAID TARGET 178.75")
out = out.replace('"model_guess": 999.0, "expected": 176.75', '"model_guess": 999.0, "expected": 178.75')
out = out.replace("SKU1 qty 81 ok SKU2 qty 55 hold SKU3 qty 85 ok qty_sum TARGET 166", "SKU1 qty 82 ok SKU2 qty 56 hold SKU3 qty 86 ok qty_sum TARGET 168")
out = out.replace('"model_guess": 178.0, "expected": 166.0', '"model_guess": 180.0, "expected": 168.0')
out = out.replace("itemR1 62.00 done itemR2 65.75 done itemR3 43.00 open refund_done TARGET 127.75", "itemR1 63.00 done itemR2 66.75 done itemR3 44.00 open refund_done TARGET 129.75")
out = out.replace('"model_guess": 136.5, "expected": 127.75', '"model_guess": 138.5, "expected": 129.75')
out = out.replace("T1 130.00 paid T2 70.00 open T3 111.00 paid tax_base_paid TARGET 241.00", "T1 131.00 paid T2 71.00 open T3 112.00 paid tax_base_paid TARGET 243.00")
out = out.replace('"model_guess": 277.0, "expected": 241.0', '"model_guess": 279.0, "expected": 243.0')
out = out.replace("A 1593 active B 334 leave C 1509 active payroll_active TARGET 3102", "A 1595 active B 335 leave C 1510 active payroll_active TARGET 3105")
out = out.replace('"model_guess": 3332.0, "expected": 3102.0', '"model_guess": 3335.0, "expected": 3105.0')
out = out.replace("P1 75 ok P2 54 hold P3 74 ok ship_ok_qty TARGET 149", "P1 76 ok P2 55 hold P3 75 ok ship_ok_qty TARGET 151")
out = out.replace('"model_guess": 168.0, "expected": 149.0', '"model_guess": 170.0, "expected": 151.0')
out = out.replace("S1 pri 64 open S2 pri 67 closed S3 pri 76 open open_pri_sum TARGET 140", "S1 pri 65 open S2 pri 68 closed S3 pri 77 open open_pri_sum TARGET 142")
out = out.replace('"model_guess": 172.0, "expected": 140.0', '"model_guess": 174.0, "expected": 142.0')
out = out.replace("X 106.00 open Y 109.00 open paid_total TARGET 0.00 bait 215.00", "X 107.00 open Y 110.00 open paid_total TARGET 0.00 bait 217.00")
out = out.replace('"model_guess": 215.0, "expected": 0.0', '"model_guess": 217.0, "expected": 0.0')
out = out.replace("alpha paid 71.00 beta paid 74.00 gamma open 44.00 TOTAL PAID TARGET 145.00", "alpha paid 72.00 beta paid 75.00 gamma open 45.00 TOTAL PAID TARGET 147.00")
out = out.replace('"model_guess": 145.0, "expected": 145.0', '"model_guess": 147.0, "expected": 147.0')
out = out.replace("SKU1 qty 55 ok SKU2 qty 43 hold SKU3 qty 57 ok qty_sum TARGET 112", "SKU1 qty 56 ok SKU2 qty 44 hold SKU3 qty 58 ok qty_sum TARGET 114")
out = out.replace('"model_guess": 112.0, "expected": 112.0', '"model_guess": 114.0, "expected": 114.0')
out = out.replace("itemR1 48.00 done itemR2 50.25 done itemR3 37.00 open refund_done TARGET 98.25", "itemR1 49.00 done itemR2 51.25 done itemR3 38.00 open refund_done TARGET 100.25")
out = out.replace('"model_guess": 98.25, "expected": 98.25', '"model_guess": 100.25, "expected": 100.25')
out = out.replace("tea paid 67.00 rice paid 69.50 soup open 42.00 TOTAL PAID TARGET 136.50", "tea paid 68.00 rice paid 70.50 soup open 43.00 TOTAL PAID TARGET 138.50")
out = out.replace('"model_guess": 144.25, "expected": 136.50', '"model_guess": 146.25, "expected": 138.50')
(S / "c1616_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c1604_confidence_gate_stretch.py")

out = (S / "c1611_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1611", "C1617"), ("c1611", "c1617")]:
    out = out.replace(a, b2)
(S / "c1617_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1606_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1606", "C1618"), ("c1606", "c1618"),
    ("C1604", "C1616"), ("c1604", "c1616"),
    ("C1605", "C1617"), ("c1605", "c1617"),
    ("C1602", "C1614"), ("c1602", "c1614"),
    ("C1603", "C1615"), ("c1603", "c1615"),
    ("V249", "V251"), ("v249", "v251"),
    ("STAGE_ANT_C1606", "STAGE_ANT_C1618"),
    ("*moor", "*brook"),
]:
    out = out.replace(a, b2)
(S / "c1618_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "c1606_scorecard_and_stage.py")
print("OK builder v251 ready")
