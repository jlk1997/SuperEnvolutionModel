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

# *mere ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T244 = [
    ["ashmere","recv","paid_total","ASHMERE GRAIN RECV","RECV","x"],
    ["cedarmere","wh","qty_sum","WH CEDARMERE BIN","RECV","x"],
    ["dawnmere","refund","refund_done","DAWNMERE PATCH REFUND","DONE","x"],
    ["elmmere","tax","tax_base_paid","ELMMERE TAX SLIP","TAX","x"],
    ["fernmere","pay","payroll_active","FERNMERE PAYROLL","PAY","x"],
    ["glenmere","ship","ship_ok","GLENMERE SHIP DOCK","SHIP","x"],
    ["hazemere","sla","sla_ok_hours","HAZEMERE SLA CARD","SLA","x"],
    ["inkmere","exp","exp_sum","INKMERE EXPENSE","EXP","x"],
    ["jademere","po","po_open","JADEMERE PO SHEET","PO","x"],
    ["knotmere","order","order_paid","KNOTMERE ORDER","ORD","x"],
    ["lakemere","dup","dup_mark","LAKEMERE DUP MARK","DUP","x"],
    ["mossmere","zero","zero_check","MOSSMERE AIR ZERO","ZERO","x"],
    ["nethermere","ledger","ledger_net","NETHERMERE LEDGER","LED","x"],
    ["oakmere","ui","ui_ok","OAKMERE UI SCAN","UI","x"],
    ["pinemere","stack","stack_count","PINEMERE STACK","STK","x"],
    ["quillmere","fax","fax_pages","QUILLMERE FAX","FAX","x"],
    ["reedmere","glare","glare_ok","REEDMERE GLARE","GLR","x"],
    ["stonemere","tab","tab_index","STONEMERE TAB INDEX","TAB","x"],
]
TR244 = [
    [2086.0, 2103.5, 1832.0],[840, 760, 820],[2009.0, 2038.25, 1810.0],[2142.0, 2159.0, 1900.0],
    [2204.0, 2228.0, 1870.0],[1928, 1944, 1828],[480.0, 520.0, 740.0],[2052.0, 2083.75, 1834.0],
    [840.0, 760.0, 820.0],[2119.0, 2107.0, 1831.0],[1,1,0],[0,0,0],
    [2185.0, 2206.5, 1856.0],[1,0,0],[1180, 1172, 1152],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO244 = [
    [1890.0, 1902.75, 1751.0],[740, 780, 820],[1833.0, 1847.5, 1726.0],[1963.0, 1979.0, 1780.0],
    [2004.0, 2020.0, 1775.0],[1798, 1812, 1744],[360.0, 400.0, 730.0],[1874.0, 1895.75, 1751.0],
    [780.0, 740.0, 820.0],[1921.0, 1907.0, 1746.0],[1,1,0],[0,0,0],
    [1956.0, 1971.5, 1761.0],[1,0,0],[1172, 1167, 1160],[1186, 1180, 1168],[1,0,0],[1176, 1170, 1149],
]
check(TR244, "TR"); check(HO244, "HO")

(ROOT / "tools/_v244_themes.json").write_text(json.dumps({"themes": T244, "train": TR244, "heldout": HO244}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_243(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V244 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V244 overlays (new vs V49) ---")
    for a, b in [
        ("ASHMERE bait 140.50", "ASHMERE bait 157.67"),
        ("CEDARW bait 142.52", "CEDARM bait 159.69"),
        ("DAWNW ghost 65.65", "DAWNM ghost 82.82"),
        ("GLENW bait 135.45", "GLENM bait 152.62"),
        ("JADEW bait 126.36", "JADEM bait 143.53"),
        ("NETHERW bait 143.53", "NETHERM bait 160.70"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V244-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD243 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v243_themes.json").read_text(encoding="utf-8"))["themes"])
NEW244 = "_".join(t[0] for t in T244)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1571"), ("c1463", "c1571"), ("V226", "V244"), ("v226", "v244"),
    ("_v226c1463", "_v244c1571"),
    ("Harder than V225", "Harder than V242"), ("harder than V225", "harder than V242"),
    (OLD243, NEW244),
    ("V226 keeps floor", "V244 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1571 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1572 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1572 VL"),
    ("kept on V226", "kept on V244"),
    ("vision_images_v226", "vision_images_v244"),
    ("VL_GATE_V226", "VL_GATE_V244"), ("vl_gate_v226", "vl_gate_v244"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V242: ashmere, cedarmere, dawnmere, elmmere, fernmere, glenmere, hazemere, inkmere,\njademere, knotmere, lakemere, mossmere, nethermere, oakmere, pinemere, quillmere, reedmere, stonemere.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T244, "v244", "V244", TR244))
out = retarget_243(out)
(S / "c1571_vision_v244_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1572"), ("c1464", "c1572"), ("V226", "V244"), ("v226", "v244"),
    ("vision_images_v226", "vision_images_v244"),
    ("VL_GATE_V226", "VL_GATE_V244"), ("vl_gate_v226", "vl_gate_v244"),
    ("runs/vision_v226", "runs/vision_v244"),
]:
    out = out.replace(a, b)
(S / "c1572_vision_v244_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1573"), ("c1465", "c1573"), ("V226", "V244"), ("v226", "v244"),
    ("vision_images_v226h", "vision_images_v244h"),
    ("vision_images_v226", "vision_images_v244"),
    ("VL_GATE_V226", "VL_GATE_V244"), ("vl_gate_v226", "vl_gate_v244"),
    ("runs/vision_v226h", "runs/vision_v244h"),
    ("_v226c1463", "_v244c1571"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T244, "v244h", "V244H", HO244))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v244h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v244"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v244" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v244h_c1573"'); seen_run = True; continue
    out2.append(ln)
(S / "c1573_vision_v244_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V244 knife = product-U2C (alternating; V243 was conf-gate)
out = (S / "c1562_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1562", "C1574"), ("c1562", "c1574"),
    ("product_u2c_c1562", "product_u2c_c1574"),
    ("vs C1550", "vs C1562"),
]:
    out = out.replace(a, b2)
(S / "c1574_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c")

out = (S / "c1569_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1569", "C1575"), ("c1569", "c1575")]:
    out = out.replace(a, b2)
(S / "c1575_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1564_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1564", "C1576"), ("c1564", "c1576"),
    ("C1562", "C1574"), ("c1562", "c1574"),
    ("C1563", "C1575"), ("c1563", "c1575"),
    ("C1560", "C1572"), ("c1560", "c1572"),
    ("C1561", "C1573"), ("c1561", "c1573"),
    ("V242", "V244"), ("v242", "v244"),
    ("STAGE_ANT_C1564", "STAGE_ANT_C1576"),
    ("*ford", "*mere"),
]:
    out = out.replace(a, b2)
(S / "c1576_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard")
print("OK builder v244 ready")
