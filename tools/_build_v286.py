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
T286 = [
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
TR286 = [
    [2233.0, 2250.5, 1973.0],[840, 760, 820],[2156.0, 2185.25, 1951.0],[2289.0, 2306.0, 2041.0],
    [2351.0, 2375.0, 2011.0],[2069, 2085, 1969],[490.0, 530.0, 760.0],[2199.0, 2230.75, 1975.0],
    [840.0, 760.0, 820.0],[2266.0, 2254.0, 1972.0],[1,1,0],[0,0,0],
    [2332.0, 2353.5, 1997.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO286 = [
    [2031.0, 2043.75, 1892.0],[640, 660, 820],[1974.0, 1988.5, 1867.0],[2104.0, 2120.0, 1923.0],
    [2145.0, 2161.0, 1916.0],[1927, 1939, 1887],[420.0, 460.0, 740.0],[2015.0, 2036.75, 1892.0],
    [740.0, 780.0, 820.0],[2062.0, 2048.0, 1889.0],[1,1,0],[0,0,0],
    [2097.0, 2112.5, 1902.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR286, "TR"); check(HO286, "HO")

(ROOT / "tools/_v286_themes.json").write_text(json.dumps({"themes": T286, "train": TR286, "heldout": HO286}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_285(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V286 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V286 overlays (new vs V49) ---")
    for a, b in [
        ("ASHFORD bait 140.50", "ASHFORD bait 185.95"),
        ("CEDARW bait 142.52", "CEDARF bait 201.11"),
        ("DAWNW ghost 65.65", "DAWNF ghost 124.34"),
        ("GLENW bait 135.45", "GLENF bait 194.04"),
        ("JADEW bait 126.36", "JADEF bait 185.95"),
        ("NETHERW bait 143.53", "NETHERF bait 202.12"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V286-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD285 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v285_themes.json").read_text(encoding="utf-8"))["themes"])
NEW286 = "_".join(t[0] for t in T286)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1823"), ("c1463", "c1823"), ("V226", "V286"), ("v226", "v286"),
    ("_v226c1463", "_v286c1823"),
    ("Harder than V225", "Harder than V284"), ("harder than V225", "harder than V284"),
    (OLD285, NEW286),
    ("V226 keeps floor", "V286 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1823 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1824 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1824 VL"),
    ("kept on V226", "kept on V286"),
    ("vision_images_v226", "vision_images_v286"),
    ("VL_GATE_V226", "VL_GATE_V286"), ("vl_gate_v226", "vl_gate_v286"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V284: ashford, cedarford, dawnford, elmford, fernford, glenford, hazeford, inkford,\njadeford, knotford, lakeford, mossford, netherford, oakford, pineford, quillford, reedford, stoneford.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T286, "v286", "V286", TR286))
out = retarget_285(out)
(S / "c1823_vision_v286_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1824"), ("c1464", "c1824"), ("V226", "V286"), ("v226", "v286"),
    ("vision_images_v226", "vision_images_v286"),
    ("VL_GATE_V226", "VL_GATE_V286"), ("vl_gate_v226", "vl_gate_v286"),
    ("runs/vision_v226", "runs/vision_v286"),
]:
    out = out.replace(a, b)
(S / "c1824_vision_v286_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1825"), ("c1465", "c1825"), ("V226", "V286"), ("v226", "v286"),
    ("vision_images_v226h", "vision_images_v286h"),
    ("vision_images_v226", "vision_images_v286"),
    ("VL_GATE_V226", "VL_GATE_V286"), ("vl_gate_v226", "vl_gate_v286"),
    ("runs/vision_v226h", "runs/vision_v286h"),
    ("_v226c1463", "_v286c1823"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T286, "v286h", "V286H", HO286))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v286h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v286"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v286" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v286h_c1825"'); seen_run = True; continue
    out2.append(ln)
(S / "c1825_vision_v286_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V286 knife = product-U2C (alternating; V285 was confidence-gate)
out = (S / "c1814_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1814", "C1826"), ("c1814", "c1826"),
    ("C1802", "C1826"), ("c1802", "c1826"),
    ("C1466", "C1826"), ("c1466", "c1826"),
]:
    out = out.replace(a, b2)
(S / "c1826_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from", "c1814_product_u2c_cost.py")

out = (S / "c1821_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1821", "C1827"), ("c1821", "c1827")]:
    out = out.replace(a, b2)
(S / "c1827_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1816_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1816", "C1828"), ("c1816", "c1828"),
    ("C1814", "C1826"), ("c1814", "c1826"),
    ("C1815", "C1827"), ("c1815", "c1827"),
    ("C1812", "C1824"), ("c1812", "c1824"),
    ("C1813", "C1825"), ("c1813", "c1825"),
    ("V284", "V286"), ("v284", "v286"),
    ("STAGE_ANT_C1816", "STAGE_ANT_C1828"),
    ("*brook", "*ford"),
]:
    out = out.replace(a, b2)
(S / "c1828_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "c1816_scorecard_and_stage.py")
print("OK builder v286 ready")
