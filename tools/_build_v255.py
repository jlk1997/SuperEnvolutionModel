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
T255 = [
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
TR255 = [
    [2156.0, 2173.5, 1896.0],[840, 760, 820],[2079.0, 2108.25, 1874.0],[2212.0, 2229.0, 1964.0],
    [2274.0, 2298.0, 1934.0],[1992, 2008, 1892],[480.0, 520.0, 740.0],[2122.0, 2153.75, 1898.0],
    [840.0, 760.0, 820.0],[2189.0, 2177.0, 1895.0],[1,1,0],[0,0,0],
    [2255.0, 2276.5, 1920.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO255 = [
    [1954.0, 1966.75, 1815.0],[740, 780, 820],[1897.0, 1911.5, 1790.0],[2027.0, 2043.0, 1846.0],
    [2068.0, 2084.0, 1839.0],[1850, 1862, 1808],[360.0, 400.0, 730.0],[1938.0, 1959.75, 1815.0],
    [780.0, 740.0, 820.0],[1985.0, 1971.0, 1810.0],[1,1,0],[0,0,0],
    [2020.0, 2035.5, 1825.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR255, "TR"); check(HO255, "HO")

(ROOT / "tools/_v255_themes.json").write_text(json.dumps({"themes": T255, "train": TR255, "heldout": HO255}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_254(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V255 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V255 overlays (new vs V49) ---")
    for a, b in [
        ("ASHMERE bait 140.50", "ASHMERE bait 168.78"),
        ("CEDARW bait 142.52", "CEDARM bait 170.80"),
        ("DAWNW ghost 65.65", "DAWNM ghost 93.93"),
        ("GLENW bait 135.45", "GLENM bait 163.73"),
        ("JADEW bait 126.36", "JADEM bait 154.64"),
        ("NETHERW bait 143.53", "NETHERM bait 171.81"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V255-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD254 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v254_themes.json").read_text(encoding="utf-8"))["themes"])
NEW255 = "_".join(t[0] for t in T255)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1637"), ("c1463", "c1637"), ("V226", "V255"), ("v226", "v255"),
    ("_v226c1463", "_v255c1637"),
    ("Harder than V225", "Harder than V253"), ("harder than V225", "harder than V253"),
    (OLD254, NEW255),
    ("V226 keeps floor", "V255 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1637 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1638 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1638 VL"),
    ("kept on V226", "kept on V255"),
    ("vision_images_v226", "vision_images_v255"),
    ("VL_GATE_V226", "VL_GATE_V255"), ("vl_gate_v226", "vl_gate_v255"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V253: ashmere, cedarmere, dawnmere, elmmere, fernmere, glenmere, hazemere, inkmere,\njademere, knotmere, lakemere, mossmere, nethermere, oakmere, pinemere, quillmere, reedmere, stonemere.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T255, "v255", "V255", TR255))
out = retarget_254(out)
(S / "c1637_vision_v255_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1638"), ("c1464", "c1638"), ("V226", "V255"), ("v226", "v255"),
    ("vision_images_v226", "vision_images_v255"),
    ("VL_GATE_V226", "VL_GATE_V255"), ("vl_gate_v226", "vl_gate_v255"),
    ("runs/vision_v226", "runs/vision_v255"),
]:
    out = out.replace(a, b)
(S / "c1638_vision_v255_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1639"), ("c1465", "c1639"), ("V226", "V255"), ("v226", "v255"),
    ("vision_images_v226h", "vision_images_v255h"),
    ("vision_images_v226", "vision_images_v255"),
    ("VL_GATE_V226", "VL_GATE_V255"), ("vl_gate_v226", "vl_gate_v255"),
    ("runs/vision_v226h", "runs/vision_v255h"),
    ("_v226c1463", "_v255c1637"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T255, "v255h", "V255H", HO255))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v255h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v255"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v255" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v255h_c1639"'); seen_run = True; continue
    out2.append(ln)
(S / "c1639_vision_v255_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V255 knife = confidence-gate (alternating; V254 was product-U2C)
out = (S / "c1628_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1628", "C1640"), ("c1628", "c1640"),
    ("C1616", "C1640"), ("c1616", "c1640"),
    ("cg109_", "cg110_"),
    ("conf_gate_stretch_c1628", "conf_gate_stretch_c1640"),
    ("confidence_gate_stretch_v172", "confidence_gate_stretch_v173"),
    ("Stretch vs C1616", "Stretch vs C1628"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 88.00 b paid 92.75 c open 48.00 TOTAL PAID TARGET 180.75", "a paid 89.00 b paid 93.75 c open 49.00 TOTAL PAID TARGET 182.75")
out = out.replace('"model_guess": 999.0, "expected": 180.75', '"model_guess": 999.0, "expected": 182.75')
out = out.replace("SKU1 qty 83 ok SKU2 qty 57 hold SKU3 qty 87 ok qty_sum TARGET 170", "SKU1 qty 84 ok SKU2 qty 58 hold SKU3 qty 88 ok qty_sum TARGET 172")
out = out.replace('"model_guess": 182.0, "expected": 170.0', '"model_guess": 184.0, "expected": 172.0')
out = out.replace("itemR1 64.00 done itemR2 67.75 done itemR3 45.00 open refund_done TARGET 131.75", "itemR1 65.00 done itemR2 68.75 done itemR3 46.00 open refund_done TARGET 133.75")
out = out.replace('"model_guess": 140.5, "expected": 131.75', '"model_guess": 142.5, "expected": 133.75')
out = out.replace("T1 132.00 paid T2 72.00 open T3 113.00 paid tax_base_paid TARGET 245.00", "T1 133.00 paid T2 73.00 open T3 114.00 paid tax_base_paid TARGET 247.00")
out = out.replace('"model_guess": 281.0, "expected": 245.0', '"model_guess": 283.0, "expected": 247.0')
out = out.replace("A 1597 active B 336 leave C 1511 active payroll_active TARGET 3108", "A 1599 active B 337 leave C 1512 active payroll_active TARGET 3111")
out = out.replace('"model_guess": 3338.0, "expected": 3108.0', '"model_guess": 3341.0, "expected": 3111.0')
out = out.replace("P1 77 ok P2 56 hold P3 76 ok ship_ok_qty TARGET 153", "P1 78 ok P2 57 hold P3 77 ok ship_ok_qty TARGET 155")
out = out.replace('"model_guess": 172.0, "expected": 153.0', '"model_guess": 174.0, "expected": 155.0')
out = out.replace("S1 pri 66 open S2 pri 69 closed S3 pri 78 open open_pri_sum TARGET 144", "S1 pri 67 open S2 pri 70 closed S3 pri 79 open open_pri_sum TARGET 146")
out = out.replace('"model_guess": 176.0, "expected": 144.0', '"model_guess": 178.0, "expected": 146.0')
out = out.replace("X 108.00 open Y 111.00 open paid_total TARGET 0.00 bait 219.00", "X 109.00 open Y 112.00 open paid_total TARGET 0.00 bait 221.00")
out = out.replace('"model_guess": 219.0, "expected": 0.0', '"model_guess": 221.0, "expected": 0.0')
out = out.replace("alpha paid 73.00 beta paid 76.00 gamma open 46.00 TOTAL PAID TARGET 149.00", "alpha paid 74.00 beta paid 77.00 gamma open 47.00 TOTAL PAID TARGET 151.00")
out = out.replace('"model_guess": 149.0, "expected": 149.0', '"model_guess": 151.0, "expected": 151.0')
out = out.replace("SKU1 qty 57 ok SKU2 qty 45 hold SKU3 qty 59 ok qty_sum TARGET 116", "SKU1 qty 58 ok SKU2 qty 46 hold SKU3 qty 60 ok qty_sum TARGET 118")
out = out.replace('"model_guess": 116.0, "expected": 116.0', '"model_guess": 118.0, "expected": 118.0')
out = out.replace("itemR1 50.00 done itemR2 52.25 done itemR3 39.00 open refund_done TARGET 102.25", "itemR1 51.00 done itemR2 53.25 done itemR3 40.00 open refund_done TARGET 104.25")
out = out.replace('"model_guess": 102.25, "expected": 102.25', '"model_guess": 104.25, "expected": 104.25')
out = out.replace("tea paid 69.00 rice paid 71.50 soup open 44.00 TOTAL PAID TARGET 140.50", "tea paid 70.00 rice paid 72.50 soup open 45.00 TOTAL PAID TARGET 142.50")
out = out.replace('"model_guess": 148.25, "expected": 140.50', '"model_guess": 150.25, "expected": 142.50')
(S / "c1640_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c1628_confidence_gate_stretch.py")

out = (S / "c1635_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1635", "C1641"), ("c1635", "c1641")]:
    out = out.replace(a, b2)
(S / "c1641_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1630_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1630", "C1642"), ("c1630", "c1642"),
    ("C1628", "C1640"), ("c1628", "c1640"),
    ("C1629", "C1641"), ("c1629", "c1641"),
    ("C1626", "C1638"), ("c1626", "c1638"),
    ("C1627", "C1639"), ("c1627", "c1639"),
    ("V253", "V255"), ("v253", "v255"),
    ("STAGE_ANT_C1630", "STAGE_ANT_C1642"),
    ("*ford", "*mere"),
]:
    out = out.replace(a, b2)
(S / "c1642_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "c1630_scorecard_and_stage.py")
print("OK builder v255 ready")
