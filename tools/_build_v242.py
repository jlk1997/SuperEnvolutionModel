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
T242 = [
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
TR242 = [
    [2050.0, 2067.5, 1798.0],[840, 760, 820],[1973.0, 2002.25, 1778.0],[2106.0, 2123.0, 1868.0],
    [2168.0, 2192.0, 1838.0],[1896, 1912, 1796],[480.0, 520.0, 740.0],[2016.0, 2047.75, 1802.0],
    [840.0, 760.0, 820.0],[2083.0, 2071.0, 1799.0],[1,1,0],[0,0,0],
    [2149.0, 2170.5, 1824.0],[1,0,0],[1172, 1164, 1144],[1188, 1172, 748],[1,0,0],[1192, 1176, 1154],
]
HO242 = [
    [1858.0, 1870.75, 1719.0],[740, 780, 820],[1801.0, 1814.5, 1694.0],[1931.0, 1947.0, 1748.0],
    [1972.0, 1988.0, 1743.0],[1766, 1780, 1712],[360.0, 400.0, 730.0],[1842.0, 1863.75, 1719.0],
    [780.0, 740.0, 820.0],[1889.0, 1875.0, 1714.0],[1,1,0],[0,0,0],
    [1924.0, 1939.5, 1729.0],[1,0,0],[1164, 1159, 1152],[1178, 1172, 1160],[1,0,0],[1176, 1170, 1149],
]
check(TR242, "TR"); check(HO242, "HO")

(ROOT / "tools/_v242_themes.json").write_text(json.dumps({"themes": T242, "train": TR242, "heldout": HO242}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_241(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V242 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V242 overlays (new vs V49) ---")
    for a, b in [
        ("ASHFORD bait 140.50", "ASHFORD bait 155.65"),
        ("CEDARW bait 142.52", "CEDARF bait 157.67"),
        ("DAWNW ghost 65.65", "DAWNF ghost 80.80"),
        ("GLENW bait 135.45", "GLENF bait 150.60"),
        ("JADEW bait 126.36", "JADEF bait 141.51"),
        ("NETHERW bait 143.53", "NETHERF bait 158.68"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V242-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD241 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v241_themes.json").read_text(encoding="utf-8"))["themes"])
NEW242 = "_".join(t[0] for t in T242)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1559"), ("c1463", "c1559"), ("V226", "V242"), ("v226", "v242"),
    ("_v226c1463", "_v242c1559"),
    ("Harder than V225", "Harder than V240"), ("harder than V225", "harder than V240"),
    (OLD241, NEW242),
    ("V226 keeps floor", "V242 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1559 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1560 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1560 VL"),
    ("kept on V226", "kept on V242"),
    ("vision_images_v226", "vision_images_v242"),
    ("VL_GATE_V226", "VL_GATE_V242"), ("vl_gate_v226", "vl_gate_v242"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V240: ashford, cedarford, dawnford, elmford, fernford, glenford, hazeford, inkford,\njadeford, knotford, lakeford, mossford, netherford, oakford, pineford, quillford, reedford, stoneford.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T242, "v242", "V242", TR242))
out = retarget_241(out)
(S / "c1559_vision_v242_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1560"), ("c1464", "c1560"), ("V226", "V242"), ("v226", "v242"),
    ("vision_images_v226", "vision_images_v242"),
    ("VL_GATE_V226", "VL_GATE_V242"), ("vl_gate_v226", "vl_gate_v242"),
    ("runs/vision_v226", "runs/vision_v242"),
]:
    out = out.replace(a, b)
(S / "c1560_vision_v242_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1561"), ("c1465", "c1561"), ("V226", "V242"), ("v226", "v242"),
    ("vision_images_v226h", "vision_images_v242h"),
    ("vision_images_v226", "vision_images_v242"),
    ("VL_GATE_V226", "VL_GATE_V242"), ("vl_gate_v226", "vl_gate_v242"),
    ("runs/vision_v226h", "runs/vision_v242h"),
    ("_v226c1463", "_v242c1559"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T242, "v242h", "V242H", HO242))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v242h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v242"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v242" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v242h_c1561"'); seen_run = True; continue
    out2.append(ln)
(S / "c1561_vision_v242_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V242 knife = product-U2C (alternating; V241 was conf-gate)
out = (S / "c1550_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1550", "C1562"), ("c1550", "c1562"),
    ("product_u2c_c1550", "product_u2c_c1562"),
    ("vs C1538", "vs C1550"),
]:
    out = out.replace(a, b2)
(S / "c1562_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c")

out = (S / "c1557_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1557", "C1563"), ("c1557", "c1563")]:
    out = out.replace(a, b2)
(S / "c1563_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1552_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1552", "C1564"), ("c1552", "c1564"),
    ("C1550", "C1562"), ("c1550", "c1562"),
    ("C1551", "C1563"), ("c1551", "c1563"),
    ("C1548", "C1560"), ("c1548", "c1560"),
    ("C1549", "C1561"), ("c1549", "c1561"),
    ("V240", "V242"), ("v240", "v242"),
    ("STAGE_ANT_C1552", "STAGE_ANT_C1564"),
    ("*brook", "*ford"),
]:
    out = out.replace(a, b2)
(S / "c1564_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard")
print("OK builder v242 ready")
