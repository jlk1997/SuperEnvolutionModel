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
T248 = [
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
TR248 = [
    [2142.0, 2159.5, 1882.0],[840, 760, 820],[2065.0, 2094.25, 1860.0],[2198.0, 2215.0, 1950.0],
    [2260.0, 2284.0, 1920.0],[1978, 1994, 1878],[480.0, 520.0, 740.0],[2108.0, 2139.75, 1884.0],
    [840.0, 760.0, 820.0],[2175.0, 2163.0, 1881.0],[1,1,0],[0,0,0],
    [2241.0, 2262.5, 1906.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO248 = [
    [1940.0, 1952.75, 1801.0],[740, 780, 820],[1883.0, 1897.5, 1776.0],[2013.0, 2029.0, 1832.0],
    [2054.0, 2070.0, 1825.0],[1836, 1848, 1794],[360.0, 400.0, 730.0],[1924.0, 1945.75, 1801.0],
    [780.0, 740.0, 820.0],[1971.0, 1957.0, 1796.0],[1,1,0],[0,0,0],
    [2006.0, 2021.5, 1811.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR248, "TR"); check(HO248, "HO")

(ROOT / "tools/_v248_themes.json").write_text(json.dumps({"themes": T248, "train": TR248, "heldout": HO248}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_247(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V248 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V248 overlays (new vs V49) ---")
    for a, b in [
        ("ASHWICK bait 140.50", "ASHWICK bait 161.71"),
        ("CEDARW bait 142.52", "CEDARW bait 163.73"),
        ("DAWNW ghost 65.65", "DAWNW ghost 86.86"),
        ("GLENW bait 135.45", "GLENW bait 156.66"),
        ("JADEW bait 126.36", "JADEW bait 147.57"),
        ("NETHERW bait 143.53", "NETHERW bait 164.74"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V248-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD247 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v247_themes.json").read_text(encoding="utf-8"))["themes"])
NEW248 = "_".join(t[0] for t in T248)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1595"), ("c1463", "c1595"), ("V226", "V248"), ("v226", "v248"),
    ("_v226c1463", "_v248c1595"),
    ("Harder than V225", "Harder than V246"), ("harder than V225", "harder than V246"),
    (OLD247, NEW248),
    ("V226 keeps floor", "V248 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1595 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1596 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1596 VL"),
    ("kept on V226", "kept on V248"),
    ("vision_images_v226", "vision_images_v248"),
    ("VL_GATE_V226", "VL_GATE_V248"), ("vl_gate_v226", "vl_gate_v248"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V246: ashwick, cedarwick, dawnwick, elmwick, fernwick, glenwick, hazewick, inkwick,\njadewick, knotwick, lakewick, mosswick, netherwick, oakwick, pinewick, quillwick, reedwick, stonewick.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T248, "v248", "V248", TR248))
out = retarget_247(out)
(S / "c1595_vision_v248_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1596"), ("c1464", "c1596"), ("V226", "V248"), ("v226", "v248"),
    ("vision_images_v226", "vision_images_v248"),
    ("VL_GATE_V226", "VL_GATE_V248"), ("vl_gate_v226", "vl_gate_v248"),
    ("runs/vision_v226", "runs/vision_v248"),
]:
    out = out.replace(a, b)
(S / "c1596_vision_v248_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1597"), ("c1465", "c1597"), ("V226", "V248"), ("v226", "v248"),
    ("vision_images_v226h", "vision_images_v248h"),
    ("vision_images_v226", "vision_images_v248"),
    ("VL_GATE_V226", "VL_GATE_V248"), ("vl_gate_v226", "vl_gate_v248"),
    ("runs/vision_v226h", "runs/vision_v248h"),
    ("_v226c1463", "_v248c1595"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T248, "v248h", "V248H", HO248))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v248h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v248"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v248" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v248h_c1597"'); seen_run = True; continue
    out2.append(ln)
(S / "c1597_vision_v248_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V248 knife = product-U2C (alternating; V247 was confidence-gate)
out = (S / "c1586_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1586", "C1598"), ("c1586", "c1598"),
    ("C1574", "C1598"), ("c1574", "c1598"),
    ("C1466", "C1598"), ("c1466", "c1598"),
]:
    out = out.replace(a, b2)
(S / "c1598_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from", "c1586_product_u2c_cost.py")

out = (S / "c1593_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1593", "C1599"), ("c1593", "c1599")]:
    out = out.replace(a, b2)
(S / "c1599_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1588_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1588", "C1600"), ("c1588", "c1600"),
    ("C1586", "C1598"), ("c1586", "c1598"),
    ("C1587", "C1599"), ("c1587", "c1599"),
    ("C1584", "C1596"), ("c1584", "c1596"),
    ("C1585", "C1597"), ("c1585", "c1597"),
    ("C1594", "C1600"), ("c1594", "c1600"),
    ("C1592", "C1598"), ("c1592", "c1598"),
    ("C1593", "C1599"), ("c1593", "c1599"),
    ("C1590", "C1596"), ("c1590", "c1596"),
    ("C1591", "C1597"), ("c1591", "c1597"),
    ("V246", "V248"), ("v246", "v248"),
    ("V247", "V248"), ("v247", "v248"),
    ("STAGE_ANT_C1588", "STAGE_ANT_C1600"),
    ("STAGE_ANT_C1594", "STAGE_ANT_C1600"),
    ("*croft", "*wick"),
    ("*holm", "*wick"),
]:
    out = out.replace(a, b2)
(S / "c1600_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "c1588_scorecard_and_stage.py")
print("OK builder v248 ready")
