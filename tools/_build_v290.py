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

# *croft ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T290 = [
    ["ashcroft","recv","paid_total","ASHCROFT GRAIN RECV","RECV","x"],
    ["cedarcroft","wh","qty_sum","WH CEDARCROFT BIN","RECV","x"],
    ["dawncroft","refund","refund_done","DAWNCROFT PATCH REFUND","DONE","x"],
    ["elmcroft","tax","tax_base_paid","ELMCROFT TAX SLIP","TAX","x"],
    ["ferncroft","pay","payroll_active","FERNCROFT PAYROLL","PAY","x"],
    ["glencroft","ship","ship_ok","GLENCROFT SHIP DOCK","SHIP","x"],
    ["hazecroft","sla","sla_ok_hours","HAZECROFT SLA CARD","SLA","x"],
    ["inkcroft","exp","exp_sum","INKCROFT EXPENSE","EXP","x"],
    ["jadecroft","po","po_open","JADECROFT PO SHEET","PO","x"],
    ["knotcroft","order","order_paid","KNOTCROFT ORDER","ORD","x"],
    ["lakecroft","dup","dup_mark","LAKECROFT DUP MARK","DUP","x"],
    ["mosscroft","zero","zero_check","MOSSCROFT AIR ZERO","ZERO","x"],
    ["nethercroft","ledger","ledger_net","NETHERCROFT LEDGER","LED","x"],
    ["oakcroft","ui","ui_ok","OAKCROFT UI SCAN","UI","x"],
    ["pinecroft","stack","stack_count","PINECROFT STACK","STK","x"],
    ["quillcroft","fax","fax_pages","QUILLCROFT FAX","FAX","x"],
    ["reedcroft","glare","glare_ok","REEDCROFT GLARE","GLR","x"],
    ["stonecroft","tab","tab_index","STONECROFT TAB INDEX","TAB","x"],
]
TR290 = [
    [2244.0, 2261.5, 1984.0],[840, 760, 820],[2167.0, 2196.25, 1962.0],[2300.0, 2317.0, 2052.0],
    [2362.0, 2386.0, 2022.0],[2080, 2096, 1980],[490.0, 530.0, 760.0],[2210.0, 2241.75, 1986.0],
    [840.0, 760.0, 820.0],[2277.0, 2265.0, 1983.0],[1,1,0],[0,0,0],
    [2343.0, 2364.5, 2008.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO290 = [
    [2042.0, 2054.75, 1903.0],[640, 660, 820],[1985.0, 1999.5, 1878.0],[2115.0, 2131.0, 1934.0],
    [2156.0, 2172.0, 1927.0],[1938, 1950, 1898],[420.0, 460.0, 740.0],[2026.0, 2047.75, 1903.0],
    [740.0, 780.0, 820.0],[2073.0, 2059.0, 1900.0],[1,1,0],[0,0,0],
    [2108.0, 2123.5, 1913.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR290, "TR"); check(HO290, "HO")

(ROOT / "tools/_v290_themes.json").write_text(json.dumps({"themes": T290, "train": TR290, "heldout": HO290}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_289(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V290 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V290 overlays (new vs V49) ---")
    for a, b in [
        ("ASHCROFT bait 140.50", "ASHCROFT bait 185.95"),
        ("CEDARW bait 142.52", "CEDARC bait 205.15"),
        ("DAWNW ghost 65.65", "DAWNC ghost 128.38"),
        ("GLENW bait 135.45", "GLENC bait 198.08"),
        ("JADEW bait 126.36", "JADEC bait 189.99"),
        ("NETHERW bait 143.53", "NETHERC bait 206.16"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V290-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD289 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v289_themes.json").read_text(encoding="utf-8"))["themes"])
NEW290 = "_".join(t[0] for t in T290)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1847"), ("c1463", "c1847"), ("V226", "V290"), ("v226", "v290"),
    ("_v226c1463", "_v290c1847"),
    ("Harder than V225", "Harder than V288"), ("harder than V225", "harder than V288"),
    (OLD289, NEW290),
    ("V226 keeps floor", "V290 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1847 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1848 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1848 VL"),
    ("kept on V226", "kept on V290"),
    ("vision_images_v226", "vision_images_v290"),
    ("VL_GATE_V226", "VL_GATE_V290"), ("vl_gate_v226", "vl_gate_v290"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V288: ashcroft, cedarcroft, dawncroft, elmcroft, ferncroft, glencroft, hazecroft, inkcroft,\njadecroft, knotcroft, lakecroft, mosscroft, nethercroft, oakcroft, pinecroft, quillcroft, reedcroft, stonecroft.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T290, "v290", "V290", TR290))
out = retarget_289(out)
(S / "c1847_vision_v290_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1848"), ("c1464", "c1848"), ("V226", "V290"), ("v226", "v290"),
    ("vision_images_v226", "vision_images_v290"),
    ("VL_GATE_V226", "VL_GATE_V290"), ("vl_gate_v226", "vl_gate_v290"),
    ("runs/vision_v226", "runs/vision_v290"),
]:
    out = out.replace(a, b)
(S / "c1848_vision_v290_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1849"), ("c1465", "c1849"), ("V226", "V290"), ("v226", "v290"),
    ("vision_images_v226h", "vision_images_v290h"),
    ("vision_images_v226", "vision_images_v290"),
    ("VL_GATE_V226", "VL_GATE_V290"), ("vl_gate_v226", "vl_gate_v290"),
    ("runs/vision_v226h", "runs/vision_v290h"),
    ("_v226c1463", "_v290c1847"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T290, "v290h", "V290H", HO290))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v290h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v290"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v290" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v290h_c1849"'); seen_run = True; continue
    out2.append(ln)
(S / "c1849_vision_v290_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V290 knife = product-U2C (alternating; V289 was confidence-gate)
out = (S / "c1838_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1838", "C1850"), ("c1838", "c1850"),
    ("C1826", "C1850"), ("c1826", "c1850"),
    ("product_u2c_cost_c1838", "product_u2c_cost_c1850"),
    ("u2c_v188", "u2c_v189"),
]:
    out = out.replace(a, b2)
(S / "c1850_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from", "c1838_product_u2c_cost.py")

out = (S / "c1845_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1845", "C1851"), ("c1845", "c1851")]:
    out = out.replace(a, b2)
(S / "c1851_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1846_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1846", "C1852"), ("c1846", "c1852"),
    ("C1844", "C1850"), ("c1844", "c1850"),
    ("C1845", "C1851"), ("c1845", "c1851"),
    ("C1842", "C1848"), ("c1842", "c1848"),
    ("C1843", "C1849"), ("c1843", "c1849"),
    ("V289", "V290"), ("v289", "v290"),
    ("STAGE_ANT_C1846", "STAGE_ANT_C1852"),
    ("*vale", "*croft"),
    ("confidence-gate", "product-U2C"),
    ("confidence_gate", "product_u2c"),
]:
    out = out.replace(a, b2)
(S / "c1852_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "c1846_scorecard_and_stage.py")
print("OK builder v290 ready")
