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

# *mere ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T233 = [
    ["ashmere","recv","paid_total","ASHMERE GRAIN RECV","RECV","x"],
    ["cedarmere","wh","qty_sum","WH CEDARMERE BIN","RECV","x"],
    ["dawnmere","refund","refund_done","DAWNMERE PATCH REFUND","DONE","x"],
    ["elmmere","tax","tax_base_paid","ELMMERE TAX SLIP","TAX","x"],
    ["fernmere","pay","payroll_active","FERNMERE PAYROLL","PAY","x"],
    ["glenmere","ship","ship_ok","GLENMERE SHIP DOCK","SHIP","x"],
    ["hazemere","sla","sla_ok_hours","HAZEMERE SLA CARD","SLA","x"],
    ["inkmere","exp","exp_sum","INKMERE EXPENSE","EXP","x"],
    ["jademere","po","po_open","JADEMERE PO SHEET","PO","x"],
    ["knotmere","order","order_paid","KNOTMERE ORDER","ORD","x"],
    ["lakemere","dup","dup_mark","LAKEMERE DUP MARK","DUP","x"],
    ["mossmere","zero","zero_check","MOSSMERE AIR ZERO","ZERO","x"],
    ["nethermere","ledger","ledger_net","NETHERMERE LEDGER","LED","x"],
    ["oakmere","ui","ui_ok","OAKMERE UI SCAN","UI","x"],
    ["pinemere","stack","stack_count","PINEMERE STACK","STK","x"],
    ["quillmere","fax","fax_pages","QUILLMERE FAX","FAX","x"],
    ["reedmere","glare","glare_ok","REEDMERE GLARE","GLR","x"],
    ["stonemere","tab","tab_index","STONEMERE TAB INDEX","TAB","x"],
]
TR233 = [
    [1888.0, 1905.5, 1654.0],[840, 760, 820],[1811.0, 1840.25, 1634.0],[1944.0, 1961.0, 1724.0],
    [2006.0, 2030.0, 1694.0],[1752, 1768, 1652],[480.0, 520.0, 740.0],[1854.0, 1885.75, 1658.0],
    [840.0, 760.0, 820.0],[1921.0, 1909.0, 1655.0],[1,1,0],[0,0,0],
    [1987.0, 2008.5, 1680.0],[1,0,0],[1180, 1172, 1152],[1196, 1180, 748],[1,0,0],[1212, 1196, 1174],
]
HO233 = [
    [1714.0, 1726.75, 1575.0],[740, 780, 820],[1657.0, 1670.5, 1550.0],[1787.0, 1803.0, 1604.0],
    [1828.0, 1844.0, 1599.0],[1622, 1636, 1568],[360.0, 400.0, 730.0],[1698.0, 1719.75, 1575.0],
    [780.0, 740.0, 820.0],[1745.0, 1731.0, 1570.0],[1,1,0],[0,0,0],
    [1780.0, 1795.5, 1585.0],[1,0,0],[1168, 1163, 1156],[1182, 1176, 1164],[1,0,0],[1192, 1186, 1165],
]
check(TR233, "TR"); check(HO233, "HO")

(ROOT / "tools/_v233_themes.json").write_text(json.dumps({"themes": T233, "train": TR233, "heldout": HO233}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_232(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V233 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V233 overlays (new vs V49) ---")
    for a, b in [
        ("ASHWICK bait 140.50", "ASHMERE bait 146.56"),
        ("CEDARW bait 142.52", "CEDARM bait 148.58"),
        ("DAWNW ghost 65.65", "DAWNM ghost 71.71"),
        ("GLENW bait 135.45", "GLENM bait 141.51"),
        ("JADEW bait 126.36", "JADEM bait 132.42"),
        ("NETHERW bait 143.53", "NETHERM bait 149.59"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V233-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD232 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v232_themes.json").read_text(encoding="utf-8"))["themes"])
NEW233 = "_".join(t[0] for t in T233)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1505"), ("c1463", "c1505"), ("V226", "V233"), ("v226", "v233"),
    ("_v226c1463", "_v233c1505"),
    ("Harder than V225", "Harder than V231"), ("harder than V225", "harder than V231"),
    (OLD232, NEW233),
    ("V226 keeps floor", "V233 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1505 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1506 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1506 VL"),
    ("kept on V226", "kept on V233"),
    ("vision_images_v226", "vision_images_v233"),
    ("VL_GATE_V226", "VL_GATE_V233"), ("vl_gate_v226", "vl_gate_v233"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V231: ashmere, cedarmere, dawnmere, elmmere, fernmere, glenmere, hazemere, inkmere,\njademere, knotmere, lakemere, mossmere, nethermere, oakmere, pinemere, quillmere, reedmere, stonemere.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T233, "v233", "V233", TR233))
out = retarget_232(out)
(S / "c1505_vision_v233_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1506"), ("c1464", "c1506"), ("V226", "V233"), ("v226", "v233"),
    ("vision_images_v226", "vision_images_v233"),
    ("VL_GATE_V226", "VL_GATE_V233"), ("vl_gate_v226", "vl_gate_v233"),
    ("runs/vision_v226", "runs/vision_v233"),
]:
    out = out.replace(a, b)
(S / "c1506_vision_v233_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1507"), ("c1465", "c1507"), ("V226", "V233"), ("v226", "v233"),
    ("vision_images_v226h", "vision_images_v233h"),
    ("vision_images_v226", "vision_images_v233"),
    ("VL_GATE_V226", "VL_GATE_V233"), ("vl_gate_v226", "vl_gate_v233"),
    ("runs/vision_v226h", "runs/vision_v233h"),
    ("_v226c1463", "_v233c1505"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T233, "v233h", "V233H", HO233))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v233h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v233"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v233" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v233h_c1507"'); seen_run = True; continue
    out2.append(ln)
(S / "c1507_vision_v233_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V233 knife = confidence-gate (alternating; V232 was product-U2C)
out = (S / "c1496_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1496", "C1508"), ("c1496", "c1508"),
    ("cg98_", "cg99_"),
    ("conf_gate_stretch_c1496", "conf_gate_stretch_c1508"),
    ("confidence_gate_stretch_v161", "confidence_gate_stretch_v162"),
    ("Stretch vs C1484", "Stretch vs C1496"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 77.00 b paid 81.75 c open 37.00 TOTAL PAID TARGET 158.75", "a paid 78.00 b paid 82.75 c open 38.00 TOTAL PAID TARGET 160.75")
out = out.replace('"model_guess": 999.0, "expected": 158.75', '"model_guess": 999.0, "expected": 160.75')
out = out.replace("SKU1 qty 72 ok SKU2 qty 46 hold SKU3 qty 76 ok qty_sum TARGET 148", "SKU1 qty 73 ok SKU2 qty 47 hold SKU3 qty 77 ok qty_sum TARGET 150")
out = out.replace('"model_guess": 160.0, "expected": 148.0', '"model_guess": 162.0, "expected": 150.0')
out = out.replace("itemR1 53.00 done itemR2 56.75 done itemR3 34.00 open refund_done TARGET 109.75", "itemR1 54.00 done itemR2 57.75 done itemR3 35.00 open refund_done TARGET 111.75")
out = out.replace('"model_guess": 118.5, "expected": 109.75', '"model_guess": 120.5, "expected": 111.75')
out = out.replace("T1 121.00 paid T2 61.00 open T3 102.00 paid tax_base_paid TARGET 223.00", "T1 122.00 paid T2 62.00 open T3 103.00 paid tax_base_paid TARGET 225.00")
out = out.replace('"model_guess": 259.0, "expected": 223.0', '"model_guess": 261.0, "expected": 225.0')
out = out.replace("A 1575 active B 325 leave C 1500 active payroll_active TARGET 3075", "A 1577 active B 326 leave C 1501 active payroll_active TARGET 3078")
out = out.replace('"model_guess": 3305.0, "expected": 3075.0', '"model_guess": 3308.0, "expected": 3078.0')
out = out.replace("P1 66 ok P2 45 hold P3 65 ok ship_ok_qty TARGET 131", "P1 67 ok P2 46 hold P3 66 ok ship_ok_qty TARGET 133")
out = out.replace('"model_guess": 150.0, "expected": 131.0', '"model_guess": 152.0, "expected": 133.0')
out = out.replace("S1 pri 55 open S2 pri 58 closed S3 pri 67 open open_pri_sum TARGET 122", "S1 pri 56 open S2 pri 59 closed S3 pri 68 open open_pri_sum TARGET 124")
out = out.replace('"model_guess": 154.0, "expected": 122.0', '"model_guess": 156.0, "expected": 124.0')
out = out.replace("X 97.00 open Y 100.00 open paid_total TARGET 0.00 bait 197.00", "X 98.00 open Y 101.00 open paid_total TARGET 0.00 bait 199.00")
out = out.replace('"model_guess": 197.0, "expected": 0.0', '"model_guess": 199.0, "expected": 0.0')
out = out.replace("alpha paid 62.00 beta paid 65.00 gamma open 35.00 TOTAL PAID TARGET 127.00", "alpha paid 63.00 beta paid 66.00 gamma open 36.00 TOTAL PAID TARGET 129.00")
out = out.replace('"model_guess": 127.0, "expected": 127.0', '"model_guess": 129.0, "expected": 129.0')
out = out.replace("SKU1 qty 46 ok SKU2 qty 34 hold SKU3 qty 48 ok qty_sum TARGET 94", "SKU1 qty 47 ok SKU2 qty 35 hold SKU3 qty 49 ok qty_sum TARGET 96")
out = out.replace('"model_guess": 94.0, "expected": 94.0', '"model_guess": 96.0, "expected": 96.0')
out = out.replace("itemR1 39.00 done itemR2 41.25 done itemR3 28.00 open refund_done TARGET 80.25", "itemR1 40.00 done itemR2 42.25 done itemR3 29.00 open refund_done TARGET 82.25")
out = out.replace('"model_guess": 80.25, "expected": 80.25', '"model_guess": 82.25, "expected": 82.25')
out = out.replace("tea paid 58.00 rice paid 60.50 soup open 33.00 TOTAL PAID TARGET 118.50", "tea paid 59.00 rice paid 61.50 soup open 34.00 TOTAL PAID TARGET 120.50")
out = out.replace('"model_guess": 126.25, "expected": 118.50', '"model_guess": 128.25, "expected": 120.50')
(S / "c1508_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate")

out = (S / "c1503_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1503", "C1509"), ("c1503", "c1509")]:
    out = out.replace(a, b2)
(S / "c1509_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1498_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1498", "C1510"), ("c1498", "c1510"),
    ("C1496", "C1508"), ("c1496", "c1508"),
    ("C1497", "C1509"), ("c1497", "c1509"),
    ("C1494", "C1506"), ("c1494", "c1506"),
    ("C1495", "C1507"), ("c1495", "c1507"),
    ("V231", "V233"), ("v231", "v233"),
    ("STAGE_ANT_C1498", "STAGE_ANT_C1510"),
    ("*ford", "*mere"),
]:
    out = out.replace(a, b2)
(S / "c1510_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard")
print("OK builder v233 ready")
