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
T280 = [
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
TR280 = [
    [2215.0, 2232.5, 1955.0],[840, 760, 820],[2138.0, 2167.25, 1933.0],[2271.0, 2288.0, 2023.0],
    [2333.0, 2357.0, 1993.0],[2051, 2067, 1951],[490.0, 530.0, 760.0],[2181.0, 2212.75, 1957.0],
    [840.0, 760.0, 820.0],[2248.0, 2236.0, 1954.0],[1,1,0],[0,0,0],
    [2314.0, 2335.5, 1979.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO280 = [
    [2013.0, 2025.75, 1874.0],[640, 660, 820],[1956.0, 1970.5, 1849.0],[2086.0, 2102.0, 1905.0],
    [2127.0, 2143.0, 1898.0],[1909, 1921, 1869],[420.0, 460.0, 740.0],[1997.0, 2018.75, 1874.0],
    [740.0, 780.0, 820.0],[2044.0, 2030.0, 1871.0],[1,1,0],[0,0,0],
    [2079.0, 2094.5, 1884.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR280, "TR"); check(HO280, "HO")

(ROOT / "tools/_v280_themes.json").write_text(json.dumps({"themes": T280, "train": TR280, "heldout": HO280}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_279(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V280 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V280 overlays (new vs V49) ---")
    for a, b in [
        ("ASHHOLM bait 140.50", "ASHHOLM bait 185.95"),
        ("CEDARW bait 142.52", "CEDARH bait 195.05"),
        ("DAWNW ghost 65.65", "DAWNH ghost 118.28"),
        ("GLENW bait 135.45", "GLENH bait 188.98"),
        ("JADEW bait 126.36", "JADEH bait 179.89"),
        ("NETHERW bait 143.53", "NETHERH bait 196.06"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V280-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD279 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v279_themes.json").read_text(encoding="utf-8"))["themes"])
NEW280 = "_".join(t[0] for t in T280)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1787"), ("c1463", "c1787"), ("V226", "V280"), ("v226", "v280"),
    ("_v226c1463", "_v280c1787"),
    ("Harder than V225", "Harder than V278"), ("harder than V225", "harder than V278"),
    (OLD279, NEW280),
    ("V226 keeps floor", "V280 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1787 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1788 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1788 VL"),
    ("kept on V226", "kept on V280"),
    ("vision_images_v226", "vision_images_v280"),
    ("VL_GATE_V226", "VL_GATE_V280"), ("vl_gate_v226", "vl_gate_v280"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V278: ashholm, cedarholm, dawnholm, elmholm, fernholm, glenholm, hazeholm, inkholm,\njadeholm, knotholm, lakeholm, mossholm, netherholm, oakholm, pineholm, quillholm, reedholm, stoneholm.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T280, "v280", "V280", TR280))
out = retarget_279(out)
(S / "c1787_vision_v280_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1788"), ("c1464", "c1788"), ("V226", "V280"), ("v226", "v280"),
    ("vision_images_v226", "vision_images_v280"),
    ("VL_GATE_V226", "VL_GATE_V280"), ("vl_gate_v226", "vl_gate_v280"),
    ("runs/vision_v226", "runs/vision_v280"),
]:
    out = out.replace(a, b)
(S / "c1788_vision_v280_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1789"), ("c1465", "c1789"), ("V226", "V280"), ("v226", "v280"),
    ("vision_images_v226h", "vision_images_v280h"),
    ("vision_images_v226", "vision_images_v280"),
    ("VL_GATE_V226", "VL_GATE_V280"), ("vl_gate_v226", "vl_gate_v280"),
    ("runs/vision_v226h", "runs/vision_v280h"),
    ("_v226c1463", "_v280c1787"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T280, "v280h", "V280H", HO280))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v280h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v280"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v280" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v280h_c1789"'); seen_run = True; continue
    out2.append(ln)
(S / "c1789_vision_v280_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V280 knife = product-U2C (alternating; V279 was confidence-gate)
out = (S / "c1778_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1778", "C1790"), ("c1778", "c1790"),
    ("C1766", "C1790"), ("c1766", "c1790"),
    ("C1466", "C1790"), ("c1466", "c1790"),
]:
    out = out.replace(a, b2)
(S / "c1790_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from", "c1778_product_u2c_cost.py")

out = (S / "c1785_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1785", "C1791"), ("c1785", "c1791")]:
    out = out.replace(a, b2)
(S / "c1791_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1780_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1780", "C1792"), ("c1780", "c1792"),
    ("C1778", "C1790"), ("c1778", "c1790"),
    ("C1779", "C1791"), ("c1779", "c1791"),
    ("C1776", "C1788"), ("c1776", "c1788"),
    ("C1777", "C1789"), ("c1777", "c1789"),
    ("V278", "V280"), ("v278", "v280"),
    ("STAGE_ANT_C1780", "STAGE_ANT_C1792"),
    ("*vale", "*holm"),
]:
    out = out.replace(a, b2)
(S / "c1792_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "c1780_scorecard_and_stage.py")
print("OK builder v280 ready")
