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
T277 = [
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
TR277 = [
    [2206.0, 2223.5, 1946.0],[840, 760, 820],[2129.0, 2158.25, 1924.0],[2262.0, 2279.0, 2014.0],
    [2324.0, 2348.0, 1984.0],[2042, 2058, 1942],[540.0, 580.0, 760.0],[2172.0, 2203.75, 1948.0],
    [840.0, 760.0, 820.0],[2239.0, 2227.0, 1945.0],[1,1,0],[0,0,0],
    [2305.0, 2326.5, 1970.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO277 = [
    [2004.0, 2016.75, 1865.0],[640, 660, 820],[1947.0, 1961.5, 1840.0],[2077.0, 2093.0, 1896.0],
    [2118.0, 2134.0, 1889.0],[1900, 1912, 1860],[420.0, 460.0, 740.0],[1988.0, 2009.75, 1865.0],
    [740.0, 780.0, 820.0],[2035.0, 2021.0, 1862.0],[1,1,0],[0,0,0],
    [2070.0, 2085.5, 1875.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR277, "TR"); check(HO277, "HO")

(ROOT / "tools/_v277_themes.json").write_text(json.dumps({"themes": T277, "train": TR277, "heldout": HO277}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_276(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V277 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V277 overlays (new vs V49) ---")
    for a, b in [
        ("ASHMERE bait 140.50", "ASHMERE bait 185.95"),
        ("CEDARW bait 142.52", "CEDARM bait 192.02"),
        ("DAWNW ghost 65.65", "DAWNM ghost 115.25"),
        ("GLENW bait 135.45", "GLENM bait 185.95"),
        ("JADEW bait 126.36", "JADEM bait 176.86"),
        ("NETHERW bait 143.53", "NETHERM bait 193.03"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V277-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD276 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v276_themes.json").read_text(encoding="utf-8"))["themes"])
NEW277 = "_".join(t[0] for t in T277)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1769"), ("c1463", "c1769"), ("V226", "V277"), ("v226", "v277"),
    ("_v226c1463", "_v277c1769"),
    ("Harder than V225", "Harder than V275"), ("harder than V225", "harder than V275"),
    (OLD276, NEW277),
    ("V226 keeps floor", "V277 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1769 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1770 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1770 VL"),
    ("kept on V226", "kept on V277"),
    ("vision_images_v226", "vision_images_v277"),
    ("VL_GATE_V226", "VL_GATE_V277"), ("vl_gate_v226", "vl_gate_v277"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V275: ashmere, cedarmere, dawnmere, elmmere, fernmere, glenmere, hazemere, inkmere,\njademere, knotmere, lakemere, mossmere, nethermere, oakmere, pinemere, quillmere, reedmere, stonemere.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T277, "v277", "V277", TR277))
out = retarget_276(out)
(S / "c1769_vision_v277_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1770"), ("c1464", "c1770"), ("V226", "V277"), ("v226", "v277"),
    ("vision_images_v226", "vision_images_v277"),
    ("VL_GATE_V226", "VL_GATE_V277"), ("vl_gate_v226", "vl_gate_v277"),
    ("runs/vision_v226", "runs/vision_v277"),
]:
    out = out.replace(a, b)
(S / "c1770_vision_v277_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1771"), ("c1465", "c1771"), ("V226", "V277"), ("v226", "v277"),
    ("vision_images_v226h", "vision_images_v277h"),
    ("vision_images_v226", "vision_images_v277"),
    ("VL_GATE_V226", "VL_GATE_V277"), ("vl_gate_v226", "vl_gate_v277"),
    ("runs/vision_v226h", "runs/vision_v277h"),
    ("_v226c1463", "_v277c1769"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T277, "v277h", "V277H", HO277))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v277h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v277"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v277" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v277h_c1771"'); seen_run = True; continue
    out2.append(ln)
(S / "c1771_vision_v277_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V277 knife = confidence-gate (alternating; V276 was product-U2C)
out = (S / "c1760_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1760", "C1772"), ("c1760", "c1772"),
    ("C1748", "C1772"), ("c1748", "c1772"),
    ("cg120_", "cg121_"),
    ("conf_gate_stretch_c1760", "conf_gate_stretch_c1772"),
    ("confidence_gate_stretch_v183", "confidence_gate_stretch_v184"),
    ("Stretch vs C1748", "Stretch vs C1760"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 99.00 b paid 103.75 c open 59.00 TOTAL PAID TARGET 202.75", "a paid 100.00 b paid 104.75 c open 60.00 TOTAL PAID TARGET 204.75")
out = out.replace('"model_guess": 999.0, "expected": 202.75', '"model_guess": 999.0, "expected": 204.75')
out = out.replace("SKU1 qty 94 ok SKU2 qty 68 hold SKU3 qty 98 ok qty_sum TARGET 192", "SKU1 qty 95 ok SKU2 qty 69 hold SKU3 qty 99 ok qty_sum TARGET 194")
out = out.replace('"model_guess": 204.0, "expected": 192.0', '"model_guess": 206.0, "expected": 194.0')
out = out.replace("itemR1 75.00 done itemR2 78.75 done itemR3 56.00 open refund_done TARGET 153.75", "itemR1 76.00 done itemR2 79.75 done itemR3 57.00 open refund_done TARGET 155.75")
out = out.replace('"model_guess": 162.5, "expected": 153.75', '"model_guess": 164.5, "expected": 155.75')
out = out.replace("T1 143.00 paid T2 83.00 open T3 124.00 paid tax_base_paid TARGET 267.00", "T1 144.00 paid T2 84.00 open T3 125.00 paid tax_base_paid TARGET 269.00")
out = out.replace('"model_guess": 303.0, "expected": 267.0', '"model_guess": 305.0, "expected": 269.0')
out = out.replace("A 1619 active B 347 leave C 1522 active payroll_active TARGET 3141", "A 1621 active B 348 leave C 1523 active payroll_active TARGET 3144")
out = out.replace('"model_guess": 3371.0, "expected": 3141.0', '"model_guess": 3374.0, "expected": 3144.0')
out = out.replace("P1 88 ok P2 67 hold P3 87 ok ship_ok_qty TARGET 175", "P1 89 ok P2 68 hold P3 88 ok ship_ok_qty TARGET 177")
out = out.replace('"model_guess": 194.0, "expected": 175.0', '"model_guess": 196.0, "expected": 177.0')
out = out.replace("S1 pri 77 open S2 pri 80 closed S3 pri 89 open open_pri_sum TARGET 166", "S1 pri 78 open S2 pri 81 closed S3 pri 90 open open_pri_sum TARGET 168")
out = out.replace('"model_guess": 198.0, "expected": 166.0', '"model_guess": 200.0, "expected": 168.0')
out = out.replace("X 119.00 open Y 122.00 open paid_total TARGET 0.00 bait 241.00", "X 120.00 open Y 123.00 open paid_total TARGET 0.00 bait 243.00")
out = out.replace('"model_guess": 241.0, "expected": 0.0', '"model_guess": 243.0, "expected": 0.0')
out = out.replace("alpha paid 84.00 beta paid 87.00 gamma open 57.00 TOTAL PAID TARGET 171.00", "alpha paid 85.00 beta paid 88.00 gamma open 58.00 TOTAL PAID TARGET 173.00")
out = out.replace('"model_guess": 171.0, "expected": 171.0', '"model_guess": 173.0, "expected": 173.0')
out = out.replace("SKU1 qty 68 ok SKU2 qty 56 hold SKU3 qty 70 ok qty_sum TARGET 138", "SKU1 qty 69 ok SKU2 qty 57 hold SKU3 qty 71 ok qty_sum TARGET 140")
out = out.replace('"model_guess": 138.0, "expected": 138.0', '"model_guess": 140.0, "expected": 140.0')
out = out.replace("itemR1 61.00 done itemR2 63.25 done itemR3 50.00 open refund_done TARGET 124.25", "itemR1 62.00 done itemR2 64.25 done itemR3 51.00 open refund_done TARGET 126.25")
out = out.replace('"model_guess": 124.25, "expected": 124.25', '"model_guess": 126.25, "expected": 126.25')
out = out.replace("tea paid 80.00 rice paid 82.50 soup open 55.00 TOTAL PAID TARGET 162.50", "tea paid 81.00 rice paid 83.50 soup open 56.00 TOTAL PAID TARGET 164.50")
out = out.replace('"model_guess": 170.25, "expected": 162.50', '"model_guess": 172.25, "expected": 164.50')
(S / "c1772_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c1760_confidence_gate_stretch.py")

out = (S / "c1767_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1767", "C1773"), ("c1767", "c1773")]:
    out = out.replace(a, b2)
(S / "c1773_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1762_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1762", "C1774"), ("c1762", "c1774"),
    ("C1760", "C1772"), ("c1760", "c1772"),
    ("C1761", "C1773"), ("c1761", "c1773"),
    ("C1758", "C1770"), ("c1758", "c1770"),
    ("C1759", "C1771"), ("c1759", "c1771"),
    ("V275", "V277"), ("v275", "v277"),
    ("STAGE_ANT_C1762", "STAGE_ANT_C1774"),
    ("*ford", "*mere"),
]:
    out = out.replace(a, b2)
(S / "c1774_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "c1762_scorecard_and_stage.py")
print("OK builder v277 ready")
