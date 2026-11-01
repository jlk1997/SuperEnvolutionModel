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

# *wick ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T259 = [
    ["ashwick","recv","paid_total","ASHWICK GRAIN RECV","RECV","x"],
    ["cedarwick","wh","qty_sum","WH CEDARWICK BIN","RECV","x"],
    ["dawnwick","refund","refund_done","DAWNWICK PATCH REFUND","DONE","x"],
    ["elmwick","tax","tax_base_paid","ELMWICK TAX SLIP","TAX","x"],
    ["fernwick","pay","payroll_active","FERNWICK PAYROLL","PAY","x"],
    ["glenwick","ship","ship_ok","GLENWICK SHIP DOCK","SHIP","x"],
    ["hazewick","sla","sla_ok_hours","HAZEWICK SLA CARD","SLA","x"],
    ["inkwick","exp","exp_sum","INKWICK EXPENSE","EXP","x"],
    ["jadewick","po","po_open","JADEWICK PO SHEET","PO","x"],
    ["knotwick","order","order_paid","KNOTWICK ORDER","ORD","x"],
    ["lakewick","dup","dup_mark","LAKEWICK DUP MARK","DUP","x"],
    ["mosswick","zero","zero_check","MOSSWICK AIR ZERO","ZERO","x"],
    ["netherwick","ledger","ledger_net","NETHERWICK LEDGER","LED","x"],
    ["oakwick","ui","ui_ok","OAKWICK UI SCAN","UI","x"],
    ["pinewick","stack","stack_count","PINEWICK STACK","STK","x"],
    ["quillwick","fax","fax_pages","QUILLWICK FAX","FAX","x"],
    ["reedwick","glare","glare_ok","REEDWICK GLARE","GLR","x"],
    ["stonewick","tab","tab_index","STONEWICK TAB INDEX","TAB","x"],
]
TR259 = [
    [2164.0, 2181.5, 1904.0],[840, 760, 820],[2087.0, 2116.25, 1882.0],[2220.0, 2237.0, 1972.0],
    [2282.0, 2306.0, 1942.0],[2000, 2016, 1900],[480.0, 520.0, 740.0],[2130.0, 2161.75, 1906.0],
    [840.0, 760.0, 820.0],[2197.0, 2185.0, 1903.0],[1,1,0],[0,0,0],
    [2263.0, 2284.5, 1928.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO259 = [
    [1962.0, 1974.75, 1823.0],[740, 780, 820],[1905.0, 1919.5, 1798.0],[2035.0, 2051.0, 1854.0],
    [2076.0, 2092.0, 1847.0],[1858, 1870, 1816],[360.0, 400.0, 730.0],[1946.0, 1967.75, 1823.0],
    [780.0, 740.0, 820.0],[1993.0, 1979.0, 1818.0],[1,1,0],[0,0,0],
    [2028.0, 2043.5, 1833.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR259, "TR"); check(HO259, "HO")

(ROOT / "tools/_v259_themes.json").write_text(json.dumps({"themes": T259, "train": TR259, "heldout": HO259}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_258(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V259 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V259 overlays (new vs V49) ---")
    for a, b in [
        ("ASHWICK bait 140.50", "ASHWICK bait 172.82"),
        ("CEDARW bait 142.52", "CEDARW bait 174.84"),
        ("DAWNW ghost 65.65", "DAWNW ghost 97.97"),
        ("GLENW bait 135.45", "GLENW bait 167.77"),
        ("JADEW bait 126.36", "JADEW bait 158.68"),
        ("NETHERW bait 143.53", "NETHERW bait 175.85"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V259-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD258 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v258_themes.json").read_text(encoding="utf-8"))["themes"])
NEW259 = "_".join(t[0] for t in T259)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1661"), ("c1463", "c1661"), ("V226", "V259"), ("v226", "v259"),
    ("_v226c1463", "_v259c1661"),
    ("Harder than V225", "Harder than V257"), ("harder than V225", "harder than V257"),
    (OLD258, NEW259),
    ("V226 keeps floor", "V259 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1661 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1662 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1662 VL"),
    ("kept on V226", "kept on V259"),
    ("vision_images_v226", "vision_images_v259"),
    ("VL_GATE_V226", "VL_GATE_V259"), ("vl_gate_v226", "vl_gate_v259"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V257: ashwick, cedarwick, dawnwick, elmwick, fernwick, glenwick, hazewick, inkwick,\njadewick, knotwick, lakewick, mosswick, netherwick, oakwick, pinewick, quillwick, reedwick, stonewick.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T259, "v259", "V259", TR259))
out = retarget_258(out)
(S / "c1661_vision_v259_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1662"), ("c1464", "c1662"), ("V226", "V259"), ("v226", "v259"),
    ("vision_images_v226", "vision_images_v259"),
    ("VL_GATE_V226", "VL_GATE_V259"), ("vl_gate_v226", "vl_gate_v259"),
    ("runs/vision_v226", "runs/vision_v259"),
]:
    out = out.replace(a, b)
(S / "c1662_vision_v259_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1663"), ("c1465", "c1663"), ("V226", "V259"), ("v226", "v259"),
    ("vision_images_v226h", "vision_images_v259h"),
    ("vision_images_v226", "vision_images_v259"),
    ("VL_GATE_V226", "VL_GATE_V259"), ("vl_gate_v226", "vl_gate_v259"),
    ("runs/vision_v226h", "runs/vision_v259h"),
    ("_v226c1463", "_v259c1661"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T259, "v259h", "V259H", HO259))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v259h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v259"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v259" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v259h_c1663"'); seen_run = True; continue
    out2.append(ln)
(S / "c1663_vision_v259_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V259 knife = confidence-gate (alternating; V258 was product-U2C)
out = (S / "c1652_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1652", "C1664"), ("c1652", "c1664"),
    ("C1640", "C1664"), ("c1640", "c1664"),
    ("cg111_", "cg112_"),
    ("conf_gate_stretch_c1652", "conf_gate_stretch_c1664"),
    ("confidence_gate_stretch_v174", "confidence_gate_stretch_v175"),
    ("Stretch vs C1640", "Stretch vs C1652"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 90.00 b paid 94.75 c open 50.00 TOTAL PAID TARGET 184.75", "a paid 91.00 b paid 95.75 c open 51.00 TOTAL PAID TARGET 186.75")
out = out.replace('"model_guess": 999.0, "expected": 184.75', '"model_guess": 999.0, "expected": 186.75')
out = out.replace("SKU1 qty 85 ok SKU2 qty 59 hold SKU3 qty 89 ok qty_sum TARGET 174", "SKU1 qty 86 ok SKU2 qty 60 hold SKU3 qty 90 ok qty_sum TARGET 176")
out = out.replace('"model_guess": 186.0, "expected": 174.0', '"model_guess": 188.0, "expected": 176.0')
out = out.replace("itemR1 66.00 done itemR2 69.75 done itemR3 47.00 open refund_done TARGET 135.75", "itemR1 67.00 done itemR2 70.75 done itemR3 48.00 open refund_done TARGET 137.75")
out = out.replace('"model_guess": 144.5, "expected": 135.75', '"model_guess": 146.5, "expected": 137.75')
out = out.replace("T1 134.00 paid T2 74.00 open T3 115.00 paid tax_base_paid TARGET 249.00", "T1 135.00 paid T2 75.00 open T3 116.00 paid tax_base_paid TARGET 251.00")
out = out.replace('"model_guess": 285.0, "expected": 249.0', '"model_guess": 287.0, "expected": 251.0')
out = out.replace("A 1601 active B 338 leave C 1513 active payroll_active TARGET 3114", "A 1603 active B 339 leave C 1514 active payroll_active TARGET 3117")
out = out.replace('"model_guess": 3344.0, "expected": 3114.0', '"model_guess": 3347.0, "expected": 3117.0')
out = out.replace("P1 79 ok P2 58 hold P3 78 ok ship_ok_qty TARGET 157", "P1 80 ok P2 59 hold P3 79 ok ship_ok_qty TARGET 159")
out = out.replace('"model_guess": 176.0, "expected": 157.0', '"model_guess": 178.0, "expected": 159.0')
out = out.replace("S1 pri 68 open S2 pri 71 closed S3 pri 80 open open_pri_sum TARGET 148", "S1 pri 69 open S2 pri 72 closed S3 pri 81 open open_pri_sum TARGET 150")
out = out.replace('"model_guess": 180.0, "expected": 148.0', '"model_guess": 182.0, "expected": 150.0')
out = out.replace("X 110.00 open Y 113.00 open paid_total TARGET 0.00 bait 223.00", "X 111.00 open Y 114.00 open paid_total TARGET 0.00 bait 225.00")
out = out.replace('"model_guess": 223.0, "expected": 0.0', '"model_guess": 225.0, "expected": 0.0')
out = out.replace("alpha paid 75.00 beta paid 78.00 gamma open 48.00 TOTAL PAID TARGET 153.00", "alpha paid 76.00 beta paid 79.00 gamma open 49.00 TOTAL PAID TARGET 155.00")
out = out.replace('"model_guess": 153.0, "expected": 153.0', '"model_guess": 155.0, "expected": 155.0')
out = out.replace("SKU1 qty 59 ok SKU2 qty 47 hold SKU3 qty 61 ok qty_sum TARGET 120", "SKU1 qty 60 ok SKU2 qty 48 hold SKU3 qty 62 ok qty_sum TARGET 122")
out = out.replace('"model_guess": 120.0, "expected": 120.0', '"model_guess": 122.0, "expected": 122.0')
out = out.replace("itemR1 52.00 done itemR2 54.25 done itemR3 41.00 open refund_done TARGET 106.25", "itemR1 53.00 done itemR2 55.25 done itemR3 42.00 open refund_done TARGET 108.25")
out = out.replace('"model_guess": 106.25, "expected": 106.25', '"model_guess": 108.25, "expected": 108.25')
out = out.replace("tea paid 71.00 rice paid 73.50 soup open 46.00 TOTAL PAID TARGET 144.50", "tea paid 72.00 rice paid 74.50 soup open 47.00 TOTAL PAID TARGET 146.50")
out = out.replace('"model_guess": 152.25, "expected": 144.50', '"model_guess": 154.25, "expected": 146.50')
(S / "c1664_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c1652_confidence_gate_stretch.py")

out = (S / "c1659_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1659", "C1665"), ("c1659", "c1665")]:
    out = out.replace(a, b2)
(S / "c1665_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1654_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1654", "C1666"), ("c1654", "c1666"),
    ("C1652", "C1664"), ("c1652", "c1664"),
    ("C1653", "C1665"), ("c1653", "c1665"),
    ("C1650", "C1662"), ("c1650", "c1662"),
    ("C1651", "C1663"), ("c1651", "c1663"),
    ("V257", "V259"), ("v257", "v259"),
    ("STAGE_ANT_C1654", "STAGE_ANT_C1666"),
    ("*croft", "*wick"),
]:
    out = out.replace(a, b2)
(S / "c1666_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "c1654_scorecard_and_stage.py")
print("OK builder v259 ready")
