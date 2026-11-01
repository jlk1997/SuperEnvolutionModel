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

# *holm ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T236 = [
    ["ashholm","recv","paid_total","ASHHOLM GRAIN RECV","RECV","x"],
    ["cedarholm","wh","qty_sum","WH CEDARHOLM BIN","RECV","x"],
    ["dawnholm","refund","refund_done","DAWNHOLM PATCH REFUND","DONE","x"],
    ["elmholm","tax","tax_base_paid","ELMHOLM TAX SLIP","TAX","x"],
    ["fernholm","pay","payroll_active","FERNHOLM PAYROLL","PAY","x"],
    ["glenholm","ship","ship_ok","GLENHOLM SHIP DOCK","SHIP","x"],
    ["hazeholm","sla","sla_ok_hours","HAZEHOLM SLA CARD","SLA","x"],
    ["inkholm","exp","exp_sum","INKHOLM EXPENSE","EXP","x"],
    ["jadeholm","po","po_open","JADEHOLM PO SHEET","PO","x"],
    ["knotholm","order","order_paid","KNOTHOLM ORDER","ORD","x"],
    ["lakeholm","dup","dup_mark","LAKEHOLM DUP MARK","DUP","x"],
    ["mossholm","zero","zero_check","MOSSHOLM AIR ZERO","ZERO","x"],
    ["netherholm","ledger","ledger_net","NETHERHOLM LEDGER","LED","x"],
    ["oakholm","ui","ui_ok","OAKHOLM UI SCAN","UI","x"],
    ["pineholm","stack","stack_count","PINEHOLM STACK","STK","x"],
    ["quillholm","fax","fax_pages","QUILLHOLM FAX","FAX","x"],
    ["reedholm","glare","glare_ok","REEDHOLM GLARE","GLR","x"],
    ["stoneholm","tab","tab_index","STONEHOLM TAB INDEX","TAB","x"],
]
TR236 = [
    [1942.0, 1959.5, 1702.0],[840, 760, 820],[1865.0, 1894.25, 1682.0],[1998.0, 2015.0, 1772.0],
    [2060.0, 2084.0, 1742.0],[1800, 1816, 1700],[480.0, 520.0, 740.0],[1908.0, 1939.75, 1706.0],
    [840.0, 760.0, 820.0],[1975.0, 1963.0, 1703.0],[1,1,0],[0,0,0],
    [2041.0, 2062.5, 1728.0],[1,0,0],[1192, 1184, 1164],[1208, 1192, 748],[1,0,0],[1224, 1208, 1186],
]
HO236 = [
    [1762.0, 1774.75, 1623.0],[740, 780, 820],[1705.0, 1718.5, 1598.0],[1835.0, 1851.0, 1652.0],
    [1876.0, 1892.0, 1647.0],[1670, 1684, 1616],[360.0, 400.0, 730.0],[1746.0, 1767.75, 1623.0],
    [780.0, 740.0, 820.0],[1793.0, 1779.0, 1618.0],[1,1,0],[0,0,0],
    [1828.0, 1843.5, 1633.0],[1,0,0],[1180, 1175, 1168],[1194, 1188, 1176],[1,0,0],[1204, 1198, 1177],
]
check(TR236, "TR"); check(HO236, "HO")

(ROOT / "tools/_v236_themes.json").write_text(json.dumps({"themes": T236, "train": TR236, "heldout": HO236}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_235(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V236 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V236 overlays (new vs V49) ---")
    for a, b in [
        ("ASHWICK bait 140.50", "ASHHOLM bait 149.59"),
        ("CEDARW bait 142.52", "CEDARH bait 151.61"),
        ("DAWNW ghost 65.65", "DAWNH ghost 74.74"),
        ("GLENW bait 135.45", "GLENH bait 144.54"),
        ("JADEW bait 126.36", "JADEH bait 135.45"),
        ("NETHERW bait 143.53", "NETHERH bait 152.62"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V236-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD235 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v235_themes.json").read_text(encoding="utf-8"))["themes"])
NEW236 = "_".join(t[0] for t in T236)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1523"), ("c1463", "c1523"), ("V226", "V236"), ("v226", "v236"),
    ("_v226c1463", "_v236c1523"),
    ("Harder than V225", "Harder than V234"), ("harder than V225", "harder than V234"),
    (OLD235, NEW236),
    ("V226 keeps floor", "V236 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1523 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1524 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1524 VL"),
    ("kept on V226", "kept on V236"),
    ("vision_images_v226", "vision_images_v236"),
    ("VL_GATE_V226", "VL_GATE_V236"), ("vl_gate_v226", "vl_gate_v236"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V234: ashholm, cedarholm, dawnholm, elmholm, fernholm, glenholm, hazeholm, inkholm,\njadeholm, knotholm, lakeholm, mossholm, netherholm, oakholm, pineholm, quillholm, reedholm, stoneholm.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T236, "v236", "V236", TR236))
out = retarget_235(out)
(S / "c1523_vision_v236_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1524"), ("c1464", "c1524"), ("V226", "V236"), ("v226", "v236"),
    ("vision_images_v226", "vision_images_v236"),
    ("VL_GATE_V226", "VL_GATE_V236"), ("vl_gate_v226", "vl_gate_v236"),
    ("runs/vision_v226", "runs/vision_v236"),
]:
    out = out.replace(a, b)
(S / "c1524_vision_v236_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1525"), ("c1465", "c1525"), ("V226", "V236"), ("v226", "v236"),
    ("vision_images_v226h", "vision_images_v236h"),
    ("vision_images_v226", "vision_images_v236"),
    ("VL_GATE_V226", "VL_GATE_V236"), ("vl_gate_v226", "vl_gate_v236"),
    ("runs/vision_v226h", "runs/vision_v236h"),
    ("_v226c1463", "_v236c1523"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T236, "v236h", "V236H", HO236))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v236h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v236"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v236" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v236h_c1525"'); seen_run = True; continue
    out2.append(ln)
(S / "c1525_vision_v236_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V236 knife = product-U2C (alternating; V235 was conf-gate)
out = (S / "c1514_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1514", "C1526"), ("c1514", "c1526"),
    ("product_u2c_c1514", "product_u2c_c1526"),
    ("vs C1502", "vs C1514"),
]:
    out = out.replace(a, b2)
(S / "c1526_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c")

out = (S / "c1521_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1521", "C1527"), ("c1521", "c1527")]:
    out = out.replace(a, b2)
(S / "c1527_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1516_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1516", "C1528"), ("c1516", "c1528"),
    ("C1514", "C1526"), ("c1514", "c1526"),
    ("C1515", "C1527"), ("c1515", "c1527"),
    ("C1512", "C1524"), ("c1512", "c1524"),
    ("C1513", "C1525"), ("c1513", "c1525"),
    ("V234", "V236"), ("v234", "v236"),
    ("STAGE_ANT_C1516", "STAGE_ANT_C1528"),
    ("*vale", "*holm"),
]:
    out = out.replace(a, b2)
(S / "c1528_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard")
print("OK builder v236 ready")
