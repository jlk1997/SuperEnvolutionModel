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

# *dale ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T252 = [
    ["ashdale","recv","paid_total","ASHDALE GRAIN RECV","RECV","x"],
    ["cedardale","wh","qty_sum","WH CEDARDALE BIN","RECV","x"],
    ["dawndale","refund","refund_done","DAWNDALE PATCH REFUND","DONE","x"],
    ["elmdale","tax","tax_base_paid","ELMDALE TAX SLIP","TAX","x"],
    ["ferndale","pay","payroll_active","FERNDALE PAYROLL","PAY","x"],
    ["glendale","ship","ship_ok","GLENDALE SHIP DOCK","SHIP","x"],
    ["hazedale","sla","sla_ok_hours","HAZEDALE SLA CARD","SLA","x"],
    ["inkdale","exp","exp_sum","INKDALE EXPENSE","EXP","x"],
    ["jadedale","po","po_open","JADEDALE PO SHEET","PO","x"],
    ["knotdale","order","order_paid","KNOTDALE ORDER","ORD","x"],
    ["lakedale","dup","dup_mark","LAKEDALE DUP MARK","DUP","x"],
    ["mossdale","zero","zero_check","MOSSDALE AIR ZERO","ZERO","x"],
    ["netherdale","ledger","ledger_net","NETHERDALE LEDGER","LED","x"],
    ["oakdale","ui","ui_ok","OAKDALE UI SCAN","UI","x"],
    ["pinedale","stack","stack_count","PINEDALE STACK","STK","x"],
    ["quilldale","fax","fax_pages","QUILLDALE FAX","FAX","x"],
    ["reeddale","glare","glare_ok","REEDDALE GLARE","GLR","x"],
    ["stonedale","tab","tab_index","STONEDALE TAB INDEX","TAB","x"],
]
TR252 = [
    [2150.0, 2167.5, 1890.0],[840, 760, 820],[2073.0, 2102.25, 1868.0],[2206.0, 2223.0, 1958.0],
    [2268.0, 2292.0, 1928.0],[1986, 2002, 1886],[480.0, 520.0, 740.0],[2116.0, 2147.75, 1892.0],
    [840.0, 760.0, 820.0],[2183.0, 2171.0, 1889.0],[1,1,0],[0,0,0],
    [2249.0, 2270.5, 1914.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO252 = [
    [1948.0, 1960.75, 1809.0],[740, 780, 820],[1891.0, 1905.5, 1784.0],[2021.0, 2037.0, 1840.0],
    [2062.0, 2078.0, 1833.0],[1844, 1856, 1802],[360.0, 400.0, 730.0],[1932.0, 1953.75, 1809.0],
    [780.0, 740.0, 820.0],[1979.0, 1965.0, 1804.0],[1,1,0],[0,0,0],
    [2014.0, 2029.5, 1819.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR252, "TR"); check(HO252, "HO")

(ROOT / "tools/_v252_themes.json").write_text(json.dumps({"themes": T252, "train": TR252, "heldout": HO252}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_251(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V252 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V252 overlays (new vs V49) ---")
    for a, b in [
        ("ASHDALE bait 140.50", "ASHDALE bait 165.75"),
        ("CEDARW bait 142.52", "CEDARD bait 167.77"),
        ("DAWNW ghost 65.65", "DAWND ghost 90.90"),
        ("GLENW bait 135.45", "GLEND bait 160.70"),
        ("JADEW bait 126.36", "JADED bait 151.61"),
        ("NETHERW bait 143.53", "NETHERD bait 168.78"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V252-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD251 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v251_themes.json").read_text(encoding="utf-8"))["themes"])
NEW252 = "_".join(t[0] for t in T252)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1619"), ("c1463", "c1619"), ("V226", "V252"), ("v226", "v252"),
    ("_v226c1463", "_v252c1619"),
    ("Harder than V225", "Harder than V250"), ("harder than V225", "harder than V250"),
    (OLD251, NEW252),
    ("V226 keeps floor", "V252 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1619 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1620 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1620 VL"),
    ("kept on V226", "kept on V252"),
    ("vision_images_v226", "vision_images_v252"),
    ("VL_GATE_V226", "VL_GATE_V252"), ("vl_gate_v226", "vl_gate_v252"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V250: ashdale, cedardale, dawndale, elmdale, ferndale, glendale, hazedale, inkdale,\njadedale, knotdale, lakedale, mossdale, netherdale, oakdale, pinedale, quilldale, reeddale, stonedale.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T252, "v252", "V252", TR252))
out = retarget_251(out)
(S / "c1619_vision_v252_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1620"), ("c1464", "c1620"), ("V226", "V252"), ("v226", "v252"),
    ("vision_images_v226", "vision_images_v252"),
    ("VL_GATE_V226", "VL_GATE_V252"), ("vl_gate_v226", "vl_gate_v252"),
    ("runs/vision_v226", "runs/vision_v252"),
]:
    out = out.replace(a, b)
(S / "c1620_vision_v252_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1621"), ("c1465", "c1621"), ("V226", "V252"), ("v226", "v252"),
    ("vision_images_v226h", "vision_images_v252h"),
    ("vision_images_v226", "vision_images_v252"),
    ("VL_GATE_V226", "VL_GATE_V252"), ("vl_gate_v226", "vl_gate_v252"),
    ("runs/vision_v226h", "runs/vision_v252h"),
    ("_v226c1463", "_v252c1619"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T252, "v252h", "V252H", HO252))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v252h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v252"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v252" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v252h_c1621"'); seen_run = True; continue
    out2.append(ln)
(S / "c1621_vision_v252_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V252 knife = product-U2C (alternating; V251 was confidence-gate)
out = (S / "c1610_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1610", "C1622"), ("c1610", "c1622"),
    ("C1598", "C1622"), ("c1598", "c1622"),
    ("C1466", "C1622"), ("c1466", "c1622"),
]:
    out = out.replace(a, b2)
(S / "c1622_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from", "c1610_product_u2c_cost.py")

out = (S / "c1617_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1617", "C1623"), ("c1617", "c1623")]:
    out = out.replace(a, b2)
(S / "c1623_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1612_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1612", "C1624"), ("c1612", "c1624"),
    ("C1610", "C1622"), ("c1610", "c1622"),
    ("C1611", "C1623"), ("c1611", "c1623"),
    ("C1608", "C1620"), ("c1608", "c1620"),
    ("C1609", "C1621"), ("c1609", "c1621"),
    ("V250", "V252"), ("v250", "v252"),
    ("STAGE_ANT_C1612", "STAGE_ANT_C1624"),
    ("*fen", "*dale"),
]:
    out = out.replace(a, b2)
(S / "c1624_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "c1612_scorecard_and_stage.py")
print("OK builder v252 ready")
