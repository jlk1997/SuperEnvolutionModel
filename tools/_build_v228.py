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

# *fen ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T228 = [
    ["ashfen","recv","paid_total","ASHFEN GRAIN RECV","RECV","x"],
    ["cedarfen","wh","qty_sum","WH CEDARFEN BIN","RECV","x"],
    ["dawnfen","refund","refund_done","DAWNFEN PATCH REFUND","DONE","x"],
    ["elmfen","tax","tax_base_paid","ELMFEN TAX SLIP","TAX","x"],
    ["fernfen","pay","payroll_active","FERNFEN PAYROLL","PAY","x"],
    ["glenfen","ship","ship_ok","GLENFEN SHIP DOCK","SHIP","x"],
    ["hazefen","sla","sla_ok_hours","HAZEFEN SLA CARD","SLA","x"],
    ["inkfen","exp","exp_sum","INKFEN EXPENSE","EXP","x"],
    ["jadefen","po","po_open","JADEFEN PO SHEET","PO","x"],
    ["knotfen","order","order_paid","KNOTFEN ORDER","ORD","x"],
    ["lakefen","dup","dup_mark","LAKEFEN DUP MARK","DUP","x"],
    ["mossfen","zero","zero_check","MOSSFEN AIR ZERO","ZERO","x"],
    ["netherfen","ledger","ledger_net","NETHERFEN LEDGER","LED","x"],
    ["oakfen","ui","ui_ok","OAKFEN UI SCAN","UI","x"],
    ["pinefen","stack","stack_count","PINEFEN STACK","STK","x"],
    ["quillfen","fax","fax_pages","QUILLFEN FAX","FAX","x"],
    ["reedfen","glare","glare_ok","REEDFEN GLARE","GLR","x"],
    ["stonefen","tab","tab_index","STONEFEN TAB INDEX","TAB","x"],
]
TR228 = [
    [1798.0, 1815.5, 1574.0],[840, 760, 820],[1721.0, 1750.25, 1554.0],[1854.0, 1871.0, 1644.0],
    [1916.0, 1940.0, 1614.0],[1672, 1688, 1572],[480.0, 520.0, 740.0],[1764.0, 1795.75, 1578.0],
    [840.0, 760.0, 820.0],[1831.0, 1819.0, 1575.0],[1,1,0],[0,0,0],
    [1897.0, 1918.5, 1600.0],[1,0,0],[1160, 1152, 1132],[1176, 1160, 752],[1,0,0],[1192, 1176, 1154],
]
HO228 = [
    [1634.0, 1646.75, 1495.0],[740, 780, 820],[1577.0, 1590.5, 1470.0],[1707.0, 1723.0, 1524.0],
    [1748.0, 1764.0, 1519.0],[1542, 1556, 1488],[360.0, 400.0, 730.0],[1618.0, 1639.75, 1495.0],
    [780.0, 740.0, 820.0],[1665.0, 1651.0, 1490.0],[1,1,0],[0,0,0],
    [1700.0, 1715.5, 1505.0],[1,0,0],[1148, 1143, 1136],[1162, 1156, 1144],[1,0,0],[1172, 1166, 1145],
]
check(TR228, "TR"); check(HO228, "HO")

(ROOT / "tools/_v228_themes.json").write_text(json.dumps({"themes": T228, "train": TR228, "heldout": HO228}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_227(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V228 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V228 overlays (new vs V49) ---")
    for a, b in [
        ("ASHWICK bait 140.50", "ASHFEN bait 141.51"),
        ("CEDARW bait 142.52", "CEDARM bait 143.53"),
        ("DAWNW ghost 65.65", "DAWNM ghost 66.66"),
        ("GLENW bait 135.45", "GLENM bait 136.46"),
        ("JADEW bait 126.36", "JADEM bait 127.37"),
        ("NETHERW bait 143.53", "NETHERM bait 144.54"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V228-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD226 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v226_themes.json").read_text(encoding="utf-8"))["themes"])
NEW228 = "_".join(t[0] for t in T228)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1475"), ("c1463", "c1475"), ("V226", "V228"), ("v226", "v228"),
    ("_v226c1463", "_v228c1475"),
    ("Harder than V225", "Harder than V226"), ("harder than V225", "harder than V226"),
    (OLD226, NEW228),
    ("V226 keeps floor", "V228 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1475 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1476 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1476 VL"),
    ("kept on V226", "kept on V228"),
    ("vision_images_v226", "vision_images_v228"),
    ("VL_GATE_V226", "VL_GATE_V228"), ("vl_gate_v226", "vl_gate_v228"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V226: ashfen, cedarfen, dawnfen, elmfen, fernfen, glenfen, hazefen, inkfen,\njadefen, knotfen, lakefen, mossfen, netherfen, oakfen, pinefen, quillfen, reedfen, stonefen.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T228, "v228", "V228", TR228))
out = retarget_227(out)
(S / "c1475_vision_v228_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1476"), ("c1464", "c1476"), ("V226", "V228"), ("v226", "v228"),
    ("vision_images_v226", "vision_images_v228"),
    ("VL_GATE_V226", "VL_GATE_V228"), ("vl_gate_v226", "vl_gate_v228"),
    ("runs/vision_v226", "runs/vision_v228"),
]:
    out = out.replace(a, b)
(S / "c1476_vision_v228_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1477"), ("c1465", "c1477"), ("V226", "V228"), ("v226", "v228"),
    ("vision_images_v226h", "vision_images_v228h"),
    ("vision_images_v226", "vision_images_v228"),
    ("VL_GATE_V226", "VL_GATE_V228"), ("vl_gate_v226", "vl_gate_v228"),
    ("runs/vision_v226h", "runs/vision_v228h"),
    ("_v226c1463", "_v228c1475"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T228, "v228h", "V228H", HO228))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v228h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v228"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v228" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v228h_c1477"'); seen_run = True; continue
    out2.append(ln)
(S / "c1477_vision_v228_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V228 knife = product-U2C (alternating; V227 was conf-gate)
out = (S / "c1466_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1466", "C1478"), ("c1466", "c1478"),
    ("product_u2c_c1466", "product_u2c_c1478"),
    ("vs C1454", "vs C1466"),
]:
    out = out.replace(a, b2)
(S / "c1478_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c")

out = (S / "c1467_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1467", "C1479"), ("c1467", "c1479"),
]:
    out = out.replace(a, b2)
(S / "c1479_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1468_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1468", "C1480"), ("c1468", "c1480"),
    ("C1466", "C1478"), ("c1466", "c1478"),
    ("C1467", "C1479"), ("c1467", "c1479"),
    ("C1464", "C1476"), ("c1464", "c1476"),
    ("C1465", "C1477"), ("c1465", "c1477"),
    ("V226", "V228"), ("v226", "v228"),
    ("STAGE_ANT_C1468", "STAGE_ANT_C1480"),
    ("*wick", "*fen"),
]:
    out = out.replace(a, b2)
(S / "c1480_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard")
print("OK builder v228 ready")
