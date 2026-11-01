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

# *brook ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T284 = [
    ["ashbrook","recv","paid_total","ASHBROOK GRAIN RECV","RECV","x"],
    ["cedarbrook","wh","qty_sum","WH CEDARBROOK BIN","RECV","x"],
    ["dawnbrook","refund","refund_done","DAWNBROOK PATCH REFUND","DONE","x"],
    ["elmbrook","tax","tax_base_paid","ELMBROOK TAX SLIP","TAX","x"],
    ["fernbrook","pay","payroll_active","FERNBROOK PAYROLL","PAY","x"],
    ["glenbrook","ship","ship_ok","GLENBROOK SHIP DOCK","SHIP","x"],
    ["hazebrook","sla","sla_ok_hours","HAZEBROOK SLA CARD","SLA","x"],
    ["inkbrook","exp","exp_sum","INKBROOK EXPENSE","EXP","x"],
    ["jadebrook","po","po_open","JADEBROOK PO SHEET","PO","x"],
    ["knotbrook","order","order_paid","KNOTBROOK ORDER","ORD","x"],
    ["lakebrook","dup","dup_mark","LAKEBROOK DUP MARK","DUP","x"],
    ["mossbrook","zero","zero_check","MOSSBROOK AIR ZERO","ZERO","x"],
    ["netherbrook","ledger","ledger_net","NETHERBROOK LEDGER","LED","x"],
    ["oakbrook","ui","ui_ok","OAKBROOK UI SCAN","UI","x"],
    ["pinebrook","stack","stack_count","PINEBROOK STACK","STK","x"],
    ["quillbrook","fax","fax_pages","QUILLBROOK FAX","FAX","x"],
    ["reedbrook","glare","glare_ok","REEDBROOK GLARE","GLR","x"],
    ["stonebrook","tab","tab_index","STONEBROOK TAB INDEX","TAB","x"],
]
TR284 = [
    [2227.0, 2244.5, 1967.0],[840, 760, 820],[2150.0, 2179.25, 1945.0],[2283.0, 2300.0, 2035.0],
    [2345.0, 2369.0, 2005.0],[2063, 2079, 1963],[490.0, 530.0, 760.0],[2193.0, 2224.75, 1969.0],
    [840.0, 760.0, 820.0],[2260.0, 2248.0, 1966.0],[1,1,0],[0,0,0],
    [2326.0, 2347.5, 1991.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO284 = [
    [2025.0, 2037.75, 1886.0],[640, 660, 820],[1968.0, 1982.5, 1861.0],[2098.0, 2114.0, 1917.0],
    [2139.0, 2155.0, 1910.0],[1921, 1933, 1881],[420.0, 460.0, 740.0],[2009.0, 2030.75, 1886.0],
    [740.0, 780.0, 820.0],[2056.0, 2042.0, 1883.0],[1,1,0],[0,0,0],
    [2091.0, 2106.5, 1896.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR284, "TR"); check(HO284, "HO")

(ROOT / "tools/_v284_themes.json").write_text(json.dumps({"themes": T284, "train": TR284, "heldout": HO284}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_283(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V284 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V284 overlays (new vs V49) ---")
    for a, b in [
        ("ASHBROOK bait 140.50", "ASHBROOK bait 185.95"),
        ("CEDARW bait 142.52", "CEDARB bait 199.09"),
        ("DAWNW ghost 65.65", "DAWNB ghost 122.32"),
        ("GLENW bait 135.45", "GLENB bait 192.02"),
        ("JADEW bait 126.36", "JADEB bait 183.93"),
        ("NETHERW bait 143.53", "NETHERB bait 200.10"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V284-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD283 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v283_themes.json").read_text(encoding="utf-8"))["themes"])
NEW284 = "_".join(t[0] for t in T284)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1811"), ("c1463", "c1811"), ("V226", "V284"), ("v226", "v284"),
    ("_v226c1463", "_v284c1811"),
    ("Harder than V225", "Harder than V282"), ("harder than V225", "harder than V282"),
    (OLD283, NEW284),
    ("V226 keeps floor", "V284 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1811 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1812 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1812 VL"),
    ("kept on V226", "kept on V284"),
    ("vision_images_v226", "vision_images_v284"),
    ("VL_GATE_V226", "VL_GATE_V284"), ("vl_gate_v226", "vl_gate_v284"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V282: ashbrook, cedarbrook, dawnbrook, elmbrook, fernbrook, glenbrook, hazebrook, inkbrook,\njadebrook, knotbrook, lakebrook, mossbrook, netherbrook, oakbrook, pinebrook, quillbrook, reedbrook, stonebrook.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T284, "v284", "V284", TR284))
out = retarget_283(out)
(S / "c1811_vision_v284_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1812"), ("c1464", "c1812"), ("V226", "V284"), ("v226", "v284"),
    ("vision_images_v226", "vision_images_v284"),
    ("VL_GATE_V226", "VL_GATE_V284"), ("vl_gate_v226", "vl_gate_v284"),
    ("runs/vision_v226", "runs/vision_v284"),
]:
    out = out.replace(a, b)
(S / "c1812_vision_v284_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1813"), ("c1465", "c1813"), ("V226", "V284"), ("v226", "v284"),
    ("vision_images_v226h", "vision_images_v284h"),
    ("vision_images_v226", "vision_images_v284"),
    ("VL_GATE_V226", "VL_GATE_V284"), ("vl_gate_v226", "vl_gate_v284"),
    ("runs/vision_v226h", "runs/vision_v284h"),
    ("_v226c1463", "_v284c1811"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T284, "v284h", "V284H", HO284))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v284h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v284"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v284" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v284h_c1813"'); seen_run = True; continue
    out2.append(ln)
(S / "c1813_vision_v284_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V284 knife = product-U2C (alternating; V283 was confidence-gate)
out = (S / "c1802_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1802", "C1814"), ("c1802", "c1814"),
    ("C1790", "C1814"), ("c1790", "c1814"),
    ("C1466", "C1814"), ("c1466", "c1814"),
]:
    out = out.replace(a, b2)
(S / "c1814_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from", "c1802_product_u2c_cost.py")

out = (S / "c1809_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1809", "C1815"), ("c1809", "c1815")]:
    out = out.replace(a, b2)
(S / "c1815_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1804_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1804", "C1816"), ("c1804", "c1816"),
    ("C1802", "C1814"), ("c1802", "c1814"),
    ("C1803", "C1815"), ("c1803", "c1815"),
    ("C1800", "C1812"), ("c1800", "c1812"),
    ("C1801", "C1813"), ("c1801", "c1813"),
    ("V282", "V284"), ("v282", "v284"),
    ("STAGE_ANT_C1804", "STAGE_ANT_C1816"),
    ("*moor", "*brook"),
]:
    out = out.replace(a, b2)
(S / "c1816_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "c1804_scorecard_and_stage.py")
print("OK builder v284 ready")
