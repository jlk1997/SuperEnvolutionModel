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

# *moor ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T238 = [
    ["ashmoor","recv","paid_total","ASHMOOR GRAIN RECV","RECV","x"],
    ["cedarmoor","wh","qty_sum","WH CEDARMOOR BIN","RECV","x"],
    ["dawnmoor","refund","refund_done","DAWNMOOR PATCH REFUND","DONE","x"],
    ["elmmoor","tax","tax_base_paid","ELMMOOR TAX SLIP","TAX","x"],
    ["fernmoor","pay","payroll_active","FERNMOOR PAYROLL","PAY","x"],
    ["glenmoor","ship","ship_ok","GLENMOOR SHIP DOCK","SHIP","x"],
    ["hazemoor","sla","sla_ok_hours","HAZEMOOR SLA CARD","SLA","x"],
    ["inkmoor","exp","exp_sum","INKMOOR EXPENSE","EXP","x"],
    ["jademoor","po","po_open","JADEMOOR PO SHEET","PO","x"],
    ["knotmoor","order","order_paid","KNOTMOOR ORDER","ORD","x"],
    ["lakemoor","dup","dup_mark","LAKEMOOR DUP MARK","DUP","x"],
    ["mossmoor","zero","zero_check","MOSSMOOR AIR ZERO","ZERO","x"],
    ["nethermoor","ledger","ledger_net","NETHERMOOR LEDGER","LED","x"],
    ["oakmoor","ui","ui_ok","OAKMOOR UI SCAN","UI","x"],
    ["pinemoor","stack","stack_count","PINEMOOR STACK","STK","x"],
    ["quillmoor","fax","fax_pages","QUILLMOOR FAX","FAX","x"],
    ["reedmoor","glare","glare_ok","REEDMOOR GLARE","GLR","x"],
    ["stonemoor","tab","tab_index","STONEMOOR TAB INDEX","TAB","x"],
]
TR238 = [
    [1978.0, 1995.5, 1734.0],[840, 760, 820],[1901.0, 1930.25, 1714.0],[2034.0, 2051.0, 1804.0],
    [2096.0, 2120.0, 1774.0],[1832, 1848, 1732],[480.0, 520.0, 740.0],[1944.0, 1975.75, 1738.0],
    [840.0, 760.0, 820.0],[2011.0, 1999.0, 1735.0],[1,1,0],[0,0,0],
    [2077.0, 2098.5, 1760.0],[1,0,0],[1156, 1148, 1128],[1172, 1156, 748],[1,0,0],[1188, 1172, 1150],
]
HO238 = [
    [1794.0, 1806.75, 1655.0],[740, 780, 820],[1737.0, 1750.5, 1630.0],[1867.0, 1883.0, 1684.0],
    [1908.0, 1924.0, 1679.0],[1702, 1716, 1648],[360.0, 400.0, 730.0],[1778.0, 1799.75, 1655.0],
    [780.0, 740.0, 820.0],[1825.0, 1811.0, 1650.0],[1,1,0],[0,0,0],
    [1860.0, 1875.5, 1665.0],[1,0,0],[1148, 1143, 1136],[1162, 1156, 1144],[1,0,0],[1172, 1166, 1145],
]
check(TR238, "TR"); check(HO238, "HO")

(ROOT / "tools/_v238_themes.json").write_text(json.dumps({"themes": T238, "train": TR238, "heldout": HO238}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_237(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V238 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V238 overlays (new vs V49) ---")
    for a, b in [
        ("ASHMOOR bait 140.50", "ASHMOOR bait 151.61"),
        ("CEDARW bait 142.52", "CEDARM bait 153.63"),
        ("DAWNW ghost 65.65", "DAWNM ghost 76.76"),
        ("GLENW bait 135.45", "GLENM bait 146.56"),
        ("JADEW bait 126.36", "JADEM bait 137.47"),
        ("NETHERW bait 143.53", "NETHERM bait 154.64"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V238-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD237 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v237_themes.json").read_text(encoding="utf-8"))["themes"])
NEW238 = "_".join(t[0] for t in T238)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1535"), ("c1463", "c1535"), ("V226", "V238"), ("v226", "v238"),
    ("_v226c1463", "_v238c1535"),
    ("Harder than V225", "Harder than V236"), ("harder than V225", "harder than V236"),
    (OLD237, NEW238),
    ("V226 keeps floor", "V238 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1535 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1536 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1536 VL"),
    ("kept on V226", "kept on V238"),
    ("vision_images_v226", "vision_images_v238"),
    ("VL_GATE_V226", "VL_GATE_V238"), ("vl_gate_v226", "vl_gate_v238"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V236: ashmoor, cedarmoor, dawnmoor, elmmoor, fernmoor, glenmoor, hazemoor, inkmoor,\njademoor, knotmoor, lakemoor, mossmoor, nethermoor, oakmoor, pinemoor, quillmoor, reedmoor, stonemoor.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T238, "v238", "V238", TR238))
out = retarget_237(out)
(S / "c1535_vision_v238_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1536"), ("c1464", "c1536"), ("V226", "V238"), ("v226", "v238"),
    ("vision_images_v226", "vision_images_v238"),
    ("VL_GATE_V226", "VL_GATE_V238"), ("vl_gate_v226", "vl_gate_v238"),
    ("runs/vision_v226", "runs/vision_v238"),
]:
    out = out.replace(a, b)
(S / "c1536_vision_v238_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1537"), ("c1465", "c1537"), ("V226", "V238"), ("v226", "v238"),
    ("vision_images_v226h", "vision_images_v238h"),
    ("vision_images_v226", "vision_images_v238"),
    ("VL_GATE_V226", "VL_GATE_V238"), ("vl_gate_v226", "vl_gate_v238"),
    ("runs/vision_v226h", "runs/vision_v238h"),
    ("_v226c1463", "_v238c1535"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T238, "v238h", "V238H", HO238))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v238h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v238"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v238" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v238h_c1537"'); seen_run = True; continue
    out2.append(ln)
(S / "c1537_vision_v238_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V238 knife = product-U2C (alternating; V237 was conf-gate)
out = (S / "c1526_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1526", "C1538"), ("c1526", "c1538"),
    ("product_u2c_c1526", "product_u2c_c1538"),
    ("vs C1514", "vs C1526"),
]:
    out = out.replace(a, b2)
(S / "c1538_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c")

out = (S / "c1533_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1533", "C1539"), ("c1533", "c1539")]:
    out = out.replace(a, b2)
(S / "c1539_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1528_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1528", "C1540"), ("c1528", "c1540"),
    ("C1526", "C1538"), ("c1526", "c1538"),
    ("C1527", "C1539"), ("c1527", "c1539"),
    ("C1524", "C1536"), ("c1524", "c1536"),
    ("C1525", "C1537"), ("c1525", "c1537"),
    ("V236", "V238"), ("v236", "v238"),
    ("STAGE_ANT_C1528", "STAGE_ANT_C1540"),
    ("*holm", "*moor"),
]:
    out = out.replace(a, b2)
(S / "c1540_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard")
print("OK builder v238 ready")
