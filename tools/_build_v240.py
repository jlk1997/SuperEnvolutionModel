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
T240 = [
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
TR240 = [
    [2014.0, 2031.5, 1766.0],[840, 760, 820],[1937.0, 1966.25, 1746.0],[2070.0, 2087.0, 1836.0],
    [2132.0, 2156.0, 1806.0],[1864, 1880, 1764],[480.0, 520.0, 740.0],[1980.0, 2011.75, 1770.0],
    [840.0, 760.0, 820.0],[2047.0, 2035.0, 1767.0],[1,1,0],[0,0,0],
    [2113.0, 2134.5, 1792.0],[1,0,0],[1164, 1156, 1136],[1180, 1164, 748],[1,0,0],[1196, 1180, 1158],
]
HO240 = [
    [1826.0, 1838.75, 1687.0],[740, 780, 820],[1769.0, 1782.5, 1662.0],[1899.0, 1915.0, 1716.0],
    [1940.0, 1956.0, 1711.0],[1734, 1748, 1680],[360.0, 400.0, 730.0],[1810.0, 1831.75, 1687.0],
    [780.0, 740.0, 820.0],[1857.0, 1843.0, 1682.0],[1,1,0],[0,0,0],
    [1892.0, 1907.5, 1697.0],[1,0,0],[1156, 1151, 1144],[1170, 1164, 1152],[1,0,0],[1180, 1174, 1153],
]
check(TR240, "TR"); check(HO240, "HO")

(ROOT / "tools/_v240_themes.json").write_text(json.dumps({"themes": T240, "train": TR240, "heldout": HO240}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_239(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V240 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V240 overlays (new vs V49) ---")
    for a, b in [
        ("ASHBROOK bait 140.50", "ASHBROOK bait 153.63"),
        ("CEDARW bait 142.52", "CEDARB bait 155.65"),
        ("DAWNW ghost 65.65", "DAWNB ghost 78.78"),
        ("GLENW bait 135.45", "GLENB bait 148.58"),
        ("JADEW bait 126.36", "JADEB bait 139.49"),
        ("NETHERW bait 143.53", "NETHERB bait 156.66"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V240-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD239 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v239_themes.json").read_text(encoding="utf-8"))["themes"])
NEW240 = "_".join(t[0] for t in T240)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1547"), ("c1463", "c1547"), ("V226", "V240"), ("v226", "v240"),
    ("_v226c1463", "_v240c1547"),
    ("Harder than V225", "Harder than V238"), ("harder than V225", "harder than V238"),
    (OLD239, NEW240),
    ("V226 keeps floor", "V240 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1547 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1548 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1548 VL"),
    ("kept on V226", "kept on V240"),
    ("vision_images_v226", "vision_images_v240"),
    ("VL_GATE_V226", "VL_GATE_V240"), ("vl_gate_v226", "vl_gate_v240"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V238: ashbrook, cedarbrook, dawnbrook, elmbrook, fernbrook, glenbrook, hazebrook, inkbrook,\njadebrook, knotbrook, lakebrook, mossbrook, netherbrook, oakbrook, pinebrook, quillbrook, reedbrook, stonebrook.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T240, "v240", "V240", TR240))
out = retarget_239(out)
(S / "c1547_vision_v240_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1548"), ("c1464", "c1548"), ("V226", "V240"), ("v226", "v240"),
    ("vision_images_v226", "vision_images_v240"),
    ("VL_GATE_V226", "VL_GATE_V240"), ("vl_gate_v226", "vl_gate_v240"),
    ("runs/vision_v226", "runs/vision_v240"),
]:
    out = out.replace(a, b)
(S / "c1548_vision_v240_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1549"), ("c1465", "c1549"), ("V226", "V240"), ("v226", "v240"),
    ("vision_images_v226h", "vision_images_v240h"),
    ("vision_images_v226", "vision_images_v240"),
    ("VL_GATE_V226", "VL_GATE_V240"), ("vl_gate_v226", "vl_gate_v240"),
    ("runs/vision_v226h", "runs/vision_v240h"),
    ("_v226c1463", "_v240c1547"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T240, "v240h", "V240H", HO240))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v240h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v240"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v240" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v240h_c1549"'); seen_run = True; continue
    out2.append(ln)
(S / "c1549_vision_v240_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V240 knife = product-U2C (alternating; V239 was conf-gate)
out = (S / "c1538_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1538", "C1550"), ("c1538", "c1550"),
    ("product_u2c_c1538", "product_u2c_c1550"),
    ("vs C1526", "vs C1538"),
]:
    out = out.replace(a, b2)
(S / "c1550_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c")

out = (S / "c1545_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1545", "C1551"), ("c1545", "c1551")]:
    out = out.replace(a, b2)
(S / "c1551_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1540_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1540", "C1552"), ("c1540", "c1552"),
    ("C1538", "C1550"), ("c1538", "c1550"),
    ("C1539", "C1551"), ("c1539", "c1551"),
    ("C1536", "C1548"), ("c1536", "c1548"),
    ("C1537", "C1549"), ("c1537", "c1549"),
    ("V238", "V240"), ("v238", "v240"),
    ("STAGE_ANT_C1540", "STAGE_ANT_C1552"),
    ("*moor", "*brook"),
]:
    out = out.replace(a, b2)
(S / "c1552_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard")
print("OK builder v240 ready")
