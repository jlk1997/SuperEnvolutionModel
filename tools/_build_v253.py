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
T253 = [
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
TR253 = [
    [2152.0, 2169.5, 1892.0],[840, 760, 820],[2075.0, 2104.25, 1870.0],[2208.0, 2225.0, 1960.0],
    [2270.0, 2294.0, 1930.0],[1988, 2004, 1888],[480.0, 520.0, 740.0],[2118.0, 2149.75, 1894.0],
    [840.0, 760.0, 820.0],[2185.0, 2173.0, 1891.0],[1,1,0],[0,0,0],
    [2251.0, 2272.5, 1916.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO253 = [
    [1950.0, 1962.75, 1811.0],[740, 780, 820],[1893.0, 1907.5, 1786.0],[2023.0, 2039.0, 1842.0],
    [2064.0, 2080.0, 1835.0],[1846, 1858, 1804],[360.0, 400.0, 730.0],[1934.0, 1955.75, 1811.0],
    [780.0, 740.0, 820.0],[1981.0, 1967.0, 1806.0],[1,1,0],[0,0,0],
    [2016.0, 2031.5, 1821.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR253, "TR"); check(HO253, "HO")

(ROOT / "tools/_v253_themes.json").write_text(json.dumps({"themes": T253, "train": TR253, "heldout": HO253}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_252(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V253 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V253 overlays (new vs V49) ---")
    for a, b in [
        ("ASHFORD bait 140.50", "ASHFORD bait 166.76"),
        ("CEDARW bait 142.52", "CEDARF bait 168.78"),
        ("DAWNW ghost 65.65", "DAWNF ghost 91.91"),
        ("GLENW bait 135.45", "GLENF bait 161.71"),
        ("JADEW bait 126.36", "JADEF bait 152.62"),
        ("NETHERW bait 143.53", "NETHERF bait 169.79"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V253-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD252 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v252_themes.json").read_text(encoding="utf-8"))["themes"])
NEW253 = "_".join(t[0] for t in T253)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1625"), ("c1463", "c1625"), ("V226", "V253"), ("v226", "v253"),
    ("_v226c1463", "_v253c1625"),
    ("Harder than V225", "Harder than V251"), ("harder than V225", "harder than V251"),
    (OLD252, NEW253),
    ("V226 keeps floor", "V253 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1625 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1626 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1626 VL"),
    ("kept on V226", "kept on V253"),
    ("vision_images_v226", "vision_images_v253"),
    ("VL_GATE_V226", "VL_GATE_V253"), ("vl_gate_v226", "vl_gate_v253"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V251: ashford, cedarford, dawnford, elmford, fernford, glenford, hazeford, inkford,\njadeford, knotford, lakeford, mossford, netherford, oakford, pineford, quillford, reedford, stoneford.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T253, "v253", "V253", TR253))
out = retarget_252(out)
(S / "c1625_vision_v253_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1626"), ("c1464", "c1626"), ("V226", "V253"), ("v226", "v253"),
    ("vision_images_v226", "vision_images_v253"),
    ("VL_GATE_V226", "VL_GATE_V253"), ("vl_gate_v226", "vl_gate_v253"),
    ("runs/vision_v226", "runs/vision_v253"),
]:
    out = out.replace(a, b)
(S / "c1626_vision_v253_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1627"), ("c1465", "c1627"), ("V226", "V253"), ("v226", "v253"),
    ("vision_images_v226h", "vision_images_v253h"),
    ("vision_images_v226", "vision_images_v253"),
    ("VL_GATE_V226", "VL_GATE_V253"), ("vl_gate_v226", "vl_gate_v253"),
    ("runs/vision_v226h", "runs/vision_v253h"),
    ("_v226c1463", "_v253c1625"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T253, "v253h", "V253H", HO253))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v253h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v253"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v253" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v253h_c1627"'); seen_run = True; continue
    out2.append(ln)
(S / "c1627_vision_v253_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V253 knife = confidence-gate (alternating; V252 was product-U2C)
out = (S / "c1616_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1616", "C1628"), ("c1616", "c1628"),
    ("C1604", "C1628"), ("c1604", "c1628"),
    ("cg108_", "cg109_"),
    ("conf_gate_stretch_c1616", "conf_gate_stretch_c1628"),
    ("confidence_gate_stretch_v171", "confidence_gate_stretch_v172"),
    ("Stretch vs C1604", "Stretch vs C1616"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 87.00 b paid 91.75 c open 47.00 TOTAL PAID TARGET 178.75", "a paid 88.00 b paid 92.75 c open 48.00 TOTAL PAID TARGET 180.75")
out = out.replace('"model_guess": 999.0, "expected": 178.75', '"model_guess": 999.0, "expected": 180.75')
out = out.replace("SKU1 qty 82 ok SKU2 qty 56 hold SKU3 qty 86 ok qty_sum TARGET 168", "SKU1 qty 83 ok SKU2 qty 57 hold SKU3 qty 87 ok qty_sum TARGET 170")
out = out.replace('"model_guess": 180.0, "expected": 168.0', '"model_guess": 182.0, "expected": 170.0')
out = out.replace("itemR1 63.00 done itemR2 66.75 done itemR3 44.00 open refund_done TARGET 129.75", "itemR1 64.00 done itemR2 67.75 done itemR3 45.00 open refund_done TARGET 131.75")
out = out.replace('"model_guess": 138.5, "expected": 129.75', '"model_guess": 140.5, "expected": 131.75')
out = out.replace("T1 131.00 paid T2 71.00 open T3 112.00 paid tax_base_paid TARGET 243.00", "T1 132.00 paid T2 72.00 open T3 113.00 paid tax_base_paid TARGET 245.00")
out = out.replace('"model_guess": 279.0, "expected": 243.0', '"model_guess": 281.0, "expected": 245.0')
out = out.replace("A 1595 active B 335 leave C 1510 active payroll_active TARGET 3105", "A 1597 active B 336 leave C 1511 active payroll_active TARGET 3108")
out = out.replace('"model_guess": 3335.0, "expected": 3105.0', '"model_guess": 3338.0, "expected": 3108.0')
out = out.replace("P1 76 ok P2 55 hold P3 75 ok ship_ok_qty TARGET 151", "P1 77 ok P2 56 hold P3 76 ok ship_ok_qty TARGET 153")
out = out.replace('"model_guess": 170.0, "expected": 151.0', '"model_guess": 172.0, "expected": 153.0')
out = out.replace("S1 pri 65 open S2 pri 68 closed S3 pri 77 open open_pri_sum TARGET 142", "S1 pri 66 open S2 pri 69 closed S3 pri 78 open open_pri_sum TARGET 144")
out = out.replace('"model_guess": 174.0, "expected": 142.0', '"model_guess": 176.0, "expected": 144.0')
out = out.replace("X 107.00 open Y 110.00 open paid_total TARGET 0.00 bait 217.00", "X 108.00 open Y 111.00 open paid_total TARGET 0.00 bait 219.00")
out = out.replace('"model_guess": 217.0, "expected": 0.0', '"model_guess": 219.0, "expected": 0.0')
out = out.replace("alpha paid 72.00 beta paid 75.00 gamma open 45.00 TOTAL PAID TARGET 147.00", "alpha paid 73.00 beta paid 76.00 gamma open 46.00 TOTAL PAID TARGET 149.00")
out = out.replace('"model_guess": 147.0, "expected": 147.0', '"model_guess": 149.0, "expected": 149.0')
out = out.replace("SKU1 qty 56 ok SKU2 qty 44 hold SKU3 qty 58 ok qty_sum TARGET 114", "SKU1 qty 57 ok SKU2 qty 45 hold SKU3 qty 59 ok qty_sum TARGET 116")
out = out.replace('"model_guess": 114.0, "expected": 114.0', '"model_guess": 116.0, "expected": 116.0')
out = out.replace("itemR1 49.00 done itemR2 51.25 done itemR3 38.00 open refund_done TARGET 100.25", "itemR1 50.00 done itemR2 52.25 done itemR3 39.00 open refund_done TARGET 102.25")
out = out.replace('"model_guess": 100.25, "expected": 100.25', '"model_guess": 102.25, "expected": 102.25')
out = out.replace("tea paid 68.00 rice paid 70.50 soup open 43.00 TOTAL PAID TARGET 138.50", "tea paid 69.00 rice paid 71.50 soup open 44.00 TOTAL PAID TARGET 140.50")
out = out.replace('"model_guess": 146.25, "expected": 138.50', '"model_guess": 148.25, "expected": 140.50')
(S / "c1628_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c1616_confidence_gate_stretch.py")

out = (S / "c1623_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1623", "C1629"), ("c1623", "c1629")]:
    out = out.replace(a, b2)
(S / "c1629_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1618_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1618", "C1630"), ("c1618", "c1630"),
    ("C1616", "C1628"), ("c1616", "c1628"),
    ("C1617", "C1629"), ("c1617", "c1629"),
    ("C1614", "C1626"), ("c1614", "c1626"),
    ("C1615", "C1627"), ("c1615", "c1627"),
    ("V251", "V253"), ("v251", "v253"),
    ("STAGE_ANT_C1618", "STAGE_ANT_C1630"),
    ("*brook", "*ford"),
]:
    out = out.replace(a, b2)
(S / "c1630_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "c1618_scorecard_and_stage.py")
print("OK builder v253 ready")
