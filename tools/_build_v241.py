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

# *dale ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T241 = [
    ["ashdale","recv","paid_total","ASHDALE GRAIN RECV","RECV","x"],
    ["cedardale","wh","qty_sum","WH CEDARDALE BIN","RECV","x"],
    ["dawndale","refund","refund_done","DAWNDALE PATCH REFUND","DONE","x"],
    ["elmdale","tax","tax_base_paid","ELMDALE TAX SLIP","TAX","x"],
    ["ferndale","pay","payroll_active","FERNDALE PAYROLL","PAY","x"],
    ["glendale","ship","ship_ok","GLENDALE SHIP DOCK","SHIP","x"],
    ["hazedale","sla","sla_ok_hours","HAZEDALE SLA CARD","SLA","x"],
    ["inkdale","exp","exp_sum","INKDALE EXPENSE","EXP","x"],
    ["jadedale","po","po_open","JADEDALE PO SHEET","PO","x"],
    ["knotdale","order","order_paid","KNOTDALE ORDER","ORD","x"],
    ["lakedale","dup","dup_mark","LAKEDALE DUP MARK","DUP","x"],
    ["mossdale","zero","zero_check","MOSSDALE AIR ZERO","ZERO","x"],
    ["netherdale","ledger","ledger_net","NETHERDALE LEDGER","LED","x"],
    ["oakdale","ui","ui_ok","OAKDALE UI SCAN","UI","x"],
    ["pinedale","stack","stack_count","PINEDALE STACK","STK","x"],
    ["quilldale","fax","fax_pages","QUILLDALE FAX","FAX","x"],
    ["reeddale","glare","glare_ok","REEDDALE GLARE","GLR","x"],
    ["stonedale","tab","tab_index","STONEDALE TAB INDEX","TAB","x"],
]
TR241 = [
    [2032.0, 2049.5, 1782.0],[840, 760, 820],[1955.0, 1984.25, 1762.0],[2088.0, 2105.0, 1852.0],
    [2150.0, 2174.0, 1822.0],[1880, 1896, 1780],[480.0, 520.0, 740.0],[1998.0, 2029.75, 1786.0],
    [840.0, 760.0, 820.0],[2065.0, 2053.0, 1783.0],[1,1,0],[0,0,0],
    [2131.0, 2152.5, 1808.0],[1,0,0],[1168, 1160, 1140],[1184, 1168, 748],[1,0,0],[1192, 1176, 1154],
]
HO241 = [
    [1842.0, 1854.75, 1703.0],[740, 780, 820],[1785.0, 1798.5, 1678.0],[1915.0, 1931.0, 1732.0],
    [1956.0, 1972.0, 1727.0],[1750, 1764, 1696],[360.0, 400.0, 730.0],[1826.0, 1847.75, 1703.0],
    [780.0, 740.0, 820.0],[1873.0, 1859.0, 1698.0],[1,1,0],[0,0,0],
    [1908.0, 1923.5, 1713.0],[1,0,0],[1160, 1155, 1148],[1174, 1168, 1156],[1,0,0],[1176, 1170, 1149],
]
check(TR241, "TR"); check(HO241, "HO")

(ROOT / "tools/_v241_themes.json").write_text(json.dumps({"themes": T241, "train": TR241, "heldout": HO241}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_240(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V241 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V241 overlays (new vs V49) ---")
    for a, b in [
        ("ASHDALE bait 140.50", "ASHDALE bait 154.64"),
        ("CEDARW bait 142.52", "CEDARD bait 156.66"),
        ("DAWNW ghost 65.65", "DAWND ghost 79.79"),
        ("GLENW bait 135.45", "GLEND bait 149.59"),
        ("JADEW bait 126.36", "JADED bait 140.50"),
        ("NETHERW bait 143.53", "NETHERD bait 157.67"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V241-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD240 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v240_themes.json").read_text(encoding="utf-8"))["themes"])
NEW241 = "_".join(t[0] for t in T241)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1553"), ("c1463", "c1553"), ("V226", "V241"), ("v226", "v241"),
    ("_v226c1463", "_v241c1553"),
    ("Harder than V225", "Harder than V239"), ("harder than V225", "harder than V239"),
    (OLD240, NEW241),
    ("V226 keeps floor", "V241 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1553 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1554 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1554 VL"),
    ("kept on V226", "kept on V241"),
    ("vision_images_v226", "vision_images_v241"),
    ("VL_GATE_V226", "VL_GATE_V241"), ("vl_gate_v226", "vl_gate_v241"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V239: ashdale, cedardale, dawndale, elmdale, ferndale, glendale, hazedale, inkdale,\njadedale, knotdale, lakedale, mossdale, netherdale, oakdale, pinedale, quilldale, reeddale, stonedale.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T241, "v241", "V241", TR241))
out = retarget_240(out)
(S / "c1553_vision_v241_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1554"), ("c1464", "c1554"), ("V226", "V241"), ("v226", "v241"),
    ("vision_images_v226", "vision_images_v241"),
    ("VL_GATE_V226", "VL_GATE_V241"), ("vl_gate_v226", "vl_gate_v241"),
    ("runs/vision_v226", "runs/vision_v241"),
]:
    out = out.replace(a, b)
(S / "c1554_vision_v241_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1555"), ("c1465", "c1555"), ("V226", "V241"), ("v226", "v241"),
    ("vision_images_v226h", "vision_images_v241h"),
    ("vision_images_v226", "vision_images_v241"),
    ("VL_GATE_V226", "VL_GATE_V241"), ("vl_gate_v226", "vl_gate_v241"),
    ("runs/vision_v226h", "runs/vision_v241h"),
    ("_v226c1463", "_v241c1553"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T241, "v241h", "V241H", HO241))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v241h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v241"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v241" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v241h_c1555"'); seen_run = True; continue
    out2.append(ln)
(S / "c1555_vision_v241_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V241 knife = confidence-gate (alternating; V240 was product-U2C)
out = (S / "c1544_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1544", "C1556"), ("c1544", "c1556"),
    ("cg102_", "cg103_"),
    ("conf_gate_stretch_c1544", "conf_gate_stretch_c1556"),
    ("confidence_gate_stretch_v165", "confidence_gate_stretch_v166"),
    ("Stretch vs C1532", "Stretch vs C1544"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 81.00 b paid 85.75 c open 41.00 TOTAL PAID TARGET 166.75", "a paid 82.00 b paid 86.75 c open 42.00 TOTAL PAID TARGET 168.75")
out = out.replace('"model_guess": 999.0, "expected": 166.75', '"model_guess": 999.0, "expected": 168.75')
out = out.replace("SKU1 qty 76 ok SKU2 qty 50 hold SKU3 qty 80 ok qty_sum TARGET 156", "SKU1 qty 77 ok SKU2 qty 51 hold SKU3 qty 81 ok qty_sum TARGET 158")
out = out.replace('"model_guess": 168.0, "expected": 156.0', '"model_guess": 170.0, "expected": 158.0')
out = out.replace("itemR1 57.00 done itemR2 60.75 done itemR3 38.00 open refund_done TARGET 117.75", "itemR1 58.00 done itemR2 61.75 done itemR3 39.00 open refund_done TARGET 119.75")
out = out.replace('"model_guess": 126.5, "expected": 117.75', '"model_guess": 128.5, "expected": 119.75')
out = out.replace("T1 125.00 paid T2 65.00 open T3 106.00 paid tax_base_paid TARGET 231.00", "T1 126.00 paid T2 66.00 open T3 107.00 paid tax_base_paid TARGET 233.00")
out = out.replace('"model_guess": 267.0, "expected": 231.0', '"model_guess": 269.0, "expected": 233.0')
out = out.replace("A 1583 active B 329 leave C 1504 active payroll_active TARGET 3087", "A 1585 active B 330 leave C 1505 active payroll_active TARGET 3090")
out = out.replace('"model_guess": 3317.0, "expected": 3087.0', '"model_guess": 3320.0, "expected": 3090.0')
out = out.replace("P1 70 ok P2 49 hold P3 69 ok ship_ok_qty TARGET 139", "P1 71 ok P2 50 hold P3 70 ok ship_ok_qty TARGET 141")
out = out.replace('"model_guess": 158.0, "expected": 139.0', '"model_guess": 160.0, "expected": 141.0')
out = out.replace("S1 pri 59 open S2 pri 62 closed S3 pri 71 open open_pri_sum TARGET 130", "S1 pri 60 open S2 pri 63 closed S3 pri 72 open open_pri_sum TARGET 132")
out = out.replace('"model_guess": 162.0, "expected": 130.0', '"model_guess": 164.0, "expected": 132.0')
out = out.replace("X 101.00 open Y 104.00 open paid_total TARGET 0.00 bait 205.00", "X 102.00 open Y 105.00 open paid_total TARGET 0.00 bait 207.00")
out = out.replace('"model_guess": 205.0, "expected": 0.0', '"model_guess": 207.0, "expected": 0.0')
out = out.replace("alpha paid 66.00 beta paid 69.00 gamma open 39.00 TOTAL PAID TARGET 135.00", "alpha paid 67.00 beta paid 70.00 gamma open 40.00 TOTAL PAID TARGET 137.00")
out = out.replace('"model_guess": 135.0, "expected": 135.0', '"model_guess": 137.0, "expected": 137.0')
out = out.replace("SKU1 qty 50 ok SKU2 qty 38 hold SKU3 qty 52 ok qty_sum TARGET 102", "SKU1 qty 51 ok SKU2 qty 39 hold SKU3 qty 53 ok qty_sum TARGET 104")
out = out.replace('"model_guess": 102.0, "expected": 102.0', '"model_guess": 104.0, "expected": 104.0')
out = out.replace("itemR1 43.00 done itemR2 45.25 done itemR3 32.00 open refund_done TARGET 88.25", "itemR1 44.00 done itemR2 46.25 done itemR3 33.00 open refund_done TARGET 90.25")
out = out.replace('"model_guess": 88.25, "expected": 88.25', '"model_guess": 90.25, "expected": 90.25')
out = out.replace("tea paid 62.00 rice paid 64.50 soup open 37.00 TOTAL PAID TARGET 126.50", "tea paid 63.00 rice paid 65.50 soup open 38.00 TOTAL PAID TARGET 128.50")
out = out.replace('"model_guess": 134.25, "expected": 126.50', '"model_guess": 136.25, "expected": 128.50')
(S / "c1556_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate")

out = (S / "c1551_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1551", "C1557"), ("c1551", "c1557")]:
    out = out.replace(a, b2)
(S / "c1557_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1546_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1546", "C1558"), ("c1546", "c1558"),
    ("C1544", "C1556"), ("c1544", "c1556"),
    ("C1545", "C1557"), ("c1545", "c1557"),
    ("C1542", "C1554"), ("c1542", "c1554"),
    ("C1543", "C1555"), ("c1543", "c1555"),
    ("V239", "V241"), ("v239", "v241"),
    ("STAGE_ANT_C1546", "STAGE_ANT_C1558"),
    ("*fen", "*dale"),
]:
    out = out.replace(a, b2)
(S / "c1558_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard")
print("OK builder v241 ready")
