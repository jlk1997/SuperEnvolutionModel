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
T262 = [
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
TR262 = [
    [2170.0, 2187.5, 1910.0],[840, 760, 820],[2093.0, 2122.25, 1888.0],[2226.0, 2243.0, 1978.0],
    [2288.0, 2312.0, 1948.0],[2006, 2022, 1906],[480.0, 520.0, 740.0],[2136.0, 2167.75, 1912.0],
    [840.0, 760.0, 820.0],[2203.0, 2191.0, 1909.0],[1,1,0],[0,0,0],
    [2269.0, 2290.5, 1934.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO262 = [
    [1968.0, 1980.75, 1829.0],[740, 780, 820],[1911.0, 1925.5, 1804.0],[2041.0, 2057.0, 1860.0],
    [2082.0, 2098.0, 1853.0],[1864, 1876, 1822],[360.0, 400.0, 730.0],[1952.0, 1973.75, 1829.0],
    [780.0, 740.0, 820.0],[1999.0, 1985.0, 1824.0],[1,1,0],[0,0,0],
    [2034.0, 2049.5, 1839.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR262, "TR"); check(HO262, "HO")

(ROOT / "tools/_v262_themes.json").write_text(json.dumps({"themes": T262, "train": TR262, "heldout": HO262}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_261(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V262 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V262 overlays (new vs V49) ---")
    for a, b in [
        ("ASHBROOK bait 140.50", "ASHBROOK bait 175.85"),
        ("CEDARW bait 142.52", "CEDARB bait 177.87"),
        ("DAWNW ghost 65.65", "DAWNB ghost 100.10"),
        ("GLENW bait 135.45", "GLENB bait 170.80"),
        ("JADEW bait 126.36", "JADEB bait 161.71"),
        ("NETHERW bait 143.53", "NETHERB bait 178.88"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V262-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD261 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v261_themes.json").read_text(encoding="utf-8"))["themes"])
NEW262 = "_".join(t[0] for t in T262)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1679"), ("c1463", "c1679"), ("V226", "V262"), ("v226", "v262"),
    ("_v226c1463", "_v262c1679"),
    ("Harder than V225", "Harder than V260"), ("harder than V225", "harder than V260"),
    (OLD261, NEW262),
    ("V226 keeps floor", "V262 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1679 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1680 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1680 VL"),
    ("kept on V226", "kept on V262"),
    ("vision_images_v226", "vision_images_v262"),
    ("VL_GATE_V226", "VL_GATE_V262"), ("vl_gate_v226", "vl_gate_v262"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V260: ashbrook, cedarbrook, dawnbrook, elmbrook, fernbrook, glenbrook, hazebrook, inkbrook,\njadebrook, knotbrook, lakebrook, mossbrook, netherbrook, oakbrook, pinebrook, quillbrook, reedbrook, stonebrook.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T262, "v262", "V262", TR262))
out = retarget_261(out)
(S / "c1679_vision_v262_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1680"), ("c1464", "c1680"), ("V226", "V262"), ("v226", "v262"),
    ("vision_images_v226", "vision_images_v262"),
    ("VL_GATE_V226", "VL_GATE_V262"), ("vl_gate_v226", "vl_gate_v262"),
    ("runs/vision_v226", "runs/vision_v262"),
]:
    out = out.replace(a, b)
(S / "c1680_vision_v262_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1681"), ("c1465", "c1681"), ("V226", "V262"), ("v226", "v262"),
    ("vision_images_v226h", "vision_images_v262h"),
    ("vision_images_v226", "vision_images_v262"),
    ("VL_GATE_V226", "VL_GATE_V262"), ("vl_gate_v226", "vl_gate_v262"),
    ("runs/vision_v226h", "runs/vision_v262h"),
    ("_v226c1463", "_v262c1679"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T262, "v262h", "V262H", HO262))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v262h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v262"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v262" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v262h_c1681"'); seen_run = True; continue
    out2.append(ln)
(S / "c1681_vision_v262_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V262 knife = product-U2C (alternating; V261 was confidence-gate)
out = (S / "c1670_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1670", "C1682"), ("c1670", "c1682"),
    ("C1658", "C1682"), ("c1658", "c1682"),
    ("C1466", "C1682"), ("c1466", "c1682"),
]:
    out = out.replace(a, b2)
(S / "c1682_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from", "c1670_product_u2c_cost.py")

out = (S / "c1677_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1677", "C1683"), ("c1677", "c1683")]:
    out = out.replace(a, b2)
(S / "c1683_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1672_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1672", "C1684"), ("c1672", "c1684"),
    ("C1670", "C1682"), ("c1670", "c1682"),
    ("C1671", "C1683"), ("c1671", "c1683"),
    ("C1668", "C1680"), ("c1668", "c1680"),
    ("C1669", "C1681"), ("c1669", "c1681"),
    ("V260", "V262"), ("v260", "v262"),
    ("STAGE_ANT_C1672", "STAGE_ANT_C1684"),
    ("*moor", "*brook"),
]:
    out = out.replace(a, b2)
(S / "c1684_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "c1672_scorecard_and_stage.py")
print("OK builder v262 ready")
