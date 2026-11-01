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
T246 = [
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
TR246 = [
    [2122.0, 2139.5, 1864.0],[840, 760, 820],[2045.0, 2074.25, 1842.0],[2178.0, 2195.0, 1932.0],
    [2240.0, 2264.0, 1902.0],[1960, 1976, 1860],[480.0, 520.0, 740.0],[2088.0, 2119.75, 1866.0],
    [840.0, 760.0, 820.0],[2155.0, 2143.0, 1863.0],[1,1,0],[0,0,0],
    [2221.0, 2242.5, 1888.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO246 = [
    [1922.0, 1934.75, 1783.0],[740, 780, 820],[1865.0, 1879.5, 1758.0],[1995.0, 2011.0, 1812.0],
    [2036.0, 2052.0, 1807.0],[1832, 1844, 1776],[360.0, 400.0, 730.0],[1906.0, 1927.75, 1783.0],
    [780.0, 740.0, 820.0],[1953.0, 1939.0, 1778.0],[1,1,0],[0,0,0],
    [1988.0, 2003.5, 1793.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR246, "TR"); check(HO246, "HO")

(ROOT / "tools/_v246_themes.json").write_text(json.dumps({"themes": T246, "train": TR246, "heldout": HO246}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_245(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V246 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V246 overlays (new vs V49) ---")
    for a, b in [
        ("ASHCROFT bait 140.50", "ASHCROFT bait 159.69"),
        ("CEDARW bait 142.52", "CEDARC bait 161.71"),
        ("DAWNW ghost 65.65", "DAWNC ghost 84.84"),
        ("GLENW bait 135.45", "GLENC bait 154.64"),
        ("JADEW bait 126.36", "JADEC bait 145.55"),
        ("NETHERW bait 143.53", "NETHERC bait 162.72"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V246-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD245 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v245_themes.json").read_text(encoding="utf-8"))["themes"])
NEW246 = "_".join(t[0] for t in T246)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1583"), ("c1463", "c1583"), ("V226", "V246"), ("v226", "v246"),
    ("_v226c1463", "_v246c1583"),
    ("Harder than V225", "Harder than V244"), ("harder than V225", "harder than V244"),
    (OLD245, NEW246),
    ("V226 keeps floor", "V246 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1583 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1584 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1584 VL"),
    ("kept on V226", "kept on V246"),
    ("vision_images_v226", "vision_images_v246"),
    ("VL_GATE_V226", "VL_GATE_V246"), ("vl_gate_v226", "vl_gate_v246"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V244: ashcroft, cedarcroft, dawncroft, elmcroft, ferncroft, glencroft, hazecroft, inkcroft,\njadecroft, knotcroft, lakecroft, mosscroft, nethercroft, oakcroft, pinecroft, quillcroft, reedcroft, stonecroft.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T246, "v246", "V246", TR246))
out = retarget_245(out)
(S / "c1583_vision_v246_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1584"), ("c1464", "c1584"), ("V226", "V246"), ("v226", "v246"),
    ("vision_images_v226", "vision_images_v246"),
    ("VL_GATE_V226", "VL_GATE_V246"), ("vl_gate_v226", "vl_gate_v246"),
    ("runs/vision_v226", "runs/vision_v246"),
]:
    out = out.replace(a, b)
(S / "c1584_vision_v246_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1585"), ("c1465", "c1585"), ("V226", "V246"), ("v226", "v246"),
    ("vision_images_v226h", "vision_images_v246h"),
    ("vision_images_v226", "vision_images_v246"),
    ("VL_GATE_V226", "VL_GATE_V246"), ("vl_gate_v226", "vl_gate_v246"),
    ("runs/vision_v226h", "runs/vision_v246h"),
    ("_v226c1463", "_v246c1583"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T246, "v246h", "V246H", HO246))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v246h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v246"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v246" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v246h_c1585"'); seen_run = True; continue
    out2.append(ln)
(S / "c1585_vision_v246_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V246 knife = product-U2C (alternating; V245 was conf-gate)
out = (S / "c1574_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1574", "C1586"), ("c1574", "c1586"),
    ("product_u2c_c1574", "product_u2c_c1586"),
    ("vs C1562", "vs C1574"),
]:
    out = out.replace(a, b2)
(S / "c1586_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c")

out = (S / "c1581_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1581", "C1587"), ("c1581", "c1587")]:
    out = out.replace(a, b2)
(S / "c1587_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1576_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1576", "C1588"), ("c1576", "c1588"),
    ("C1574", "C1586"), ("c1574", "c1586"),
    ("C1575", "C1587"), ("c1575", "c1587"),
    ("C1572", "C1584"), ("c1572", "c1584"),
    ("C1573", "C1585"), ("c1573", "c1585"),
    ("V244", "V246"), ("v244", "v246"),
    ("STAGE_ANT_C1576", "STAGE_ANT_C1588"),
    ("*mere", "*croft"),
]:
    out = out.replace(a, b2)
(S / "c1588_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard")
print("OK builder v246 ready")
