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

# *vale ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T245 = [
    ["ashvale","recv","paid_total","ASHVALE GRAIN RECV","RECV","x"],
    ["cedarvale","wh","qty_sum","WH CEDARVALE BIN","RECV","x"],
    ["dawnvale","refund","refund_done","DAWNVALE PATCH REFUND","DONE","x"],
    ["elmvale","tax","tax_base_paid","ELMVALE TAX SLIP","TAX","x"],
    ["fernvale","pay","payroll_active","FERNVALE PAYROLL","PAY","x"],
    ["glenvale","ship","ship_ok","GLENVALE SHIP DOCK","SHIP","x"],
    ["hazevale","sla","sla_ok_hours","HAZEVALE SLA CARD","SLA","x"],
    ["inkvale","exp","exp_sum","INKVALE EXPENSE","EXP","x"],
    ["jadevale","po","po_open","JADEVALE PO SHEET","PO","x"],
    ["knotvale","order","order_paid","KNOTVALE ORDER","ORD","x"],
    ["lakevale","dup","dup_mark","LAKEVALE DUP MARK","DUP","x"],
    ["mossvale","zero","zero_check","MOSSVALE AIR ZERO","ZERO","x"],
    ["nethervale","ledger","ledger_net","NETHERVALE LEDGER","LED","x"],
    ["oakvale","ui","ui_ok","OAKVALE UI SCAN","UI","x"],
    ["pinevale","stack","stack_count","PINEVALE STACK","STK","x"],
    ["quillvale","fax","fax_pages","QUILLVALE FAX","FAX","x"],
    ["reedvale","glare","glare_ok","REEDVALE GLARE","GLR","x"],
    ["stonevale","tab","tab_index","STONEVALE TAB INDEX","TAB","x"],
]
TR245 = [
    [2104.0, 2121.5, 1848.0],[840, 760, 820],[2027.0, 2056.25, 1826.0],[2160.0, 2177.0, 1916.0],
    [2222.0, 2246.0, 1886.0],[1944, 1960, 1844],[480.0, 520.0, 740.0],[2070.0, 2101.75, 1850.0],
    [840.0, 760.0, 820.0],[2137.0, 2125.0, 1847.0],[1,1,0],[0,0,0],
    [2203.0, 2224.5, 1872.0],[1,0,0],[1184, 1176, 1156],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO245 = [
    [1906.0, 1918.75, 1767.0],[740, 780, 820],[1849.0, 1863.5, 1742.0],[1979.0, 1995.0, 1796.0],
    [2020.0, 2036.0, 1791.0],[1814, 1828, 1760],[360.0, 400.0, 730.0],[1890.0, 1911.75, 1767.0],
    [780.0, 740.0, 820.0],[1937.0, 1923.0, 1762.0],[1,1,0],[0,0,0],
    [1972.0, 1987.5, 1777.0],[1,0,0],[1176, 1171, 1164],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR245, "TR"); check(HO245, "HO")

(ROOT / "tools/_v245_themes.json").write_text(json.dumps({"themes": T245, "train": TR245, "heldout": HO245}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_244(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V245 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V245 overlays (new vs V49) ---")
    for a, b in [
        ("ASHVALE bait 140.50", "ASHVALE bait 158.68"),
        ("CEDARW bait 142.52", "CEDARV bait 160.70"),
        ("DAWNW ghost 65.65", "DAWNV ghost 83.83"),
        ("GLENW bait 135.45", "GLENV bait 153.63"),
        ("JADEW bait 126.36", "JADEV bait 144.54"),
        ("NETHERW bait 143.53", "NETHERV bait 161.71"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V245-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD244 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v244_themes.json").read_text(encoding="utf-8"))["themes"])
NEW245 = "_".join(t[0] for t in T245)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1577"), ("c1463", "c1577"), ("V226", "V245"), ("v226", "v245"),
    ("_v226c1463", "_v245c1577"),
    ("Harder than V225", "Harder than V243"), ("harder than V225", "harder than V243"),
    (OLD244, NEW245),
    ("V226 keeps floor", "V245 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1577 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1578 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1578 VL"),
    ("kept on V226", "kept on V245"),
    ("vision_images_v226", "vision_images_v245"),
    ("VL_GATE_V226", "VL_GATE_V245"), ("vl_gate_v226", "vl_gate_v245"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V243: ashvale, cedarvale, dawnvale, elmvale, fernvale, glenvale, hazevale, inkvale,\njadevale, knotvale, lakevale, mossvale, nethervale, oakvale, pinevale, quillvale, reedvale, stonevale.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T245, "v245", "V245", TR245))
out = retarget_244(out)
(S / "c1577_vision_v245_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1578"), ("c1464", "c1578"), ("V226", "V245"), ("v226", "v245"),
    ("vision_images_v226", "vision_images_v245"),
    ("VL_GATE_V226", "VL_GATE_V245"), ("vl_gate_v226", "vl_gate_v245"),
    ("runs/vision_v226", "runs/vision_v245"),
]:
    out = out.replace(a, b)
(S / "c1578_vision_v245_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1579"), ("c1465", "c1579"), ("V226", "V245"), ("v226", "v245"),
    ("vision_images_v226h", "vision_images_v245h"),
    ("vision_images_v226", "vision_images_v245"),
    ("VL_GATE_V226", "VL_GATE_V245"), ("vl_gate_v226", "vl_gate_v245"),
    ("runs/vision_v226h", "runs/vision_v245h"),
    ("_v226c1463", "_v245c1577"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T245, "v245h", "V245H", HO245))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v245h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v245"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v245" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v245h_c1579"'); seen_run = True; continue
    out2.append(ln)
(S / "c1579_vision_v245_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V245 knife = confidence-gate (alternating; V244 was product-U2C)
out = (S / "c1568_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1568", "C1580"), ("c1568", "c1580"),
    ("cg104_", "cg105_"),
    ("conf_gate_stretch_c1568", "conf_gate_stretch_c1580"),
    ("confidence_gate_stretch_v167", "confidence_gate_stretch_v168"),
    ("Stretch vs C1556", "Stretch vs C1568"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 83.00 b paid 87.75 c open 43.00 TOTAL PAID TARGET 170.75", "a paid 84.00 b paid 88.75 c open 44.00 TOTAL PAID TARGET 172.75")
out = out.replace('"model_guess": 999.0, "expected": 170.75', '"model_guess": 999.0, "expected": 172.75')
out = out.replace("SKU1 qty 78 ok SKU2 qty 52 hold SKU3 qty 82 ok qty_sum TARGET 160", "SKU1 qty 79 ok SKU2 qty 53 hold SKU3 qty 83 ok qty_sum TARGET 162")
out = out.replace('"model_guess": 172.0, "expected": 160.0', '"model_guess": 174.0, "expected": 162.0')
out = out.replace("itemR1 59.00 done itemR2 62.75 done itemR3 40.00 open refund_done TARGET 121.75", "itemR1 60.00 done itemR2 63.75 done itemR3 41.00 open refund_done TARGET 123.75")
out = out.replace('"model_guess": 130.5, "expected": 121.75', '"model_guess": 132.5, "expected": 123.75')
out = out.replace("T1 127.00 paid T2 67.00 open T3 108.00 paid tax_base_paid TARGET 235.00", "T1 128.00 paid T2 68.00 open T3 109.00 paid tax_base_paid TARGET 237.00")
out = out.replace('"model_guess": 271.0, "expected": 235.0', '"model_guess": 273.0, "expected": 237.0')
out = out.replace("A 1587 active B 331 leave C 1506 active payroll_active TARGET 3093", "A 1589 active B 332 leave C 1507 active payroll_active TARGET 3096")
out = out.replace('"model_guess": 3323.0, "expected": 3093.0', '"model_guess": 3326.0, "expected": 3096.0')
out = out.replace("P1 72 ok P2 51 hold P3 71 ok ship_ok_qty TARGET 143", "P1 73 ok P2 52 hold P3 72 ok ship_ok_qty TARGET 145")
out = out.replace('"model_guess": 162.0, "expected": 143.0', '"model_guess": 164.0, "expected": 145.0')
out = out.replace("S1 pri 61 open S2 pri 64 closed S3 pri 73 open open_pri_sum TARGET 134", "S1 pri 62 open S2 pri 65 closed S3 pri 74 open open_pri_sum TARGET 136")
out = out.replace('"model_guess": 166.0, "expected": 134.0', '"model_guess": 168.0, "expected": 136.0')
out = out.replace("X 103.00 open Y 106.00 open paid_total TARGET 0.00 bait 209.00", "X 104.00 open Y 107.00 open paid_total TARGET 0.00 bait 211.00")
out = out.replace('"model_guess": 209.0, "expected": 0.0', '"model_guess": 211.0, "expected": 0.0')
out = out.replace("alpha paid 68.00 beta paid 71.00 gamma open 41.00 TOTAL PAID TARGET 139.00", "alpha paid 69.00 beta paid 72.00 gamma open 42.00 TOTAL PAID TARGET 141.00")
out = out.replace('"model_guess": 139.0, "expected": 139.0', '"model_guess": 141.0, "expected": 141.0')
out = out.replace("SKU1 qty 52 ok SKU2 qty 40 hold SKU3 qty 54 ok qty_sum TARGET 106", "SKU1 qty 53 ok SKU2 qty 41 hold SKU3 qty 55 ok qty_sum TARGET 108")
out = out.replace('"model_guess": 106.0, "expected": 106.0', '"model_guess": 108.0, "expected": 108.0')
out = out.replace("itemR1 45.00 done itemR2 47.25 done itemR3 34.00 open refund_done TARGET 92.25", "itemR1 46.00 done itemR2 48.25 done itemR3 35.00 open refund_done TARGET 94.25")
out = out.replace('"model_guess": 92.25, "expected": 92.25', '"model_guess": 94.25, "expected": 94.25')
out = out.replace("tea paid 64.00 rice paid 66.50 soup open 39.00 TOTAL PAID TARGET 130.50", "tea paid 65.00 rice paid 67.50 soup open 40.00 TOTAL PAID TARGET 132.50")
out = out.replace('"model_guess": 138.25, "expected": 130.50', '"model_guess": 140.25, "expected": 132.50')
(S / "c1580_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate")

out = (S / "c1575_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1575", "C1581"), ("c1575", "c1581")]:
    out = out.replace(a, b2)
(S / "c1581_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1570_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1570", "C1582"), ("c1570", "c1582"),
    ("C1568", "C1580"), ("c1568", "c1580"),
    ("C1569", "C1581"), ("c1569", "c1581"),
    ("C1566", "C1578"), ("c1566", "c1578"),
    ("C1567", "C1579"), ("c1567", "c1579"),
    ("V243", "V245"), ("v243", "v245"),
    ("STAGE_ANT_C1570", "STAGE_ANT_C1582"),
    ("*hurst", "*vale"),
]:
    out = out.replace(a, b2)
(S / "c1582_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard")
print("OK builder v245 ready")
