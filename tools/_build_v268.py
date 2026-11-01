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
T268 = [
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
TR268 = [
    [2182.0, 2199.5, 1922.0],[840, 760, 820],[2105.0, 2134.25, 1900.0],[2238.0, 2255.0, 1990.0],
    [2300.0, 2324.0, 1960.0],[2018, 2034, 1918],[480.0, 520.0, 740.0],[2148.0, 2179.75, 1924.0],
    [840.0, 760.0, 820.0],[2215.0, 2203.0, 1921.0],[1,1,0],[0,0,0],
    [2281.0, 2302.5, 1946.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO268 = [
    [1980.0, 1992.75, 1841.0],[740, 780, 820],[1923.0, 1937.5, 1816.0],[2053.0, 2069.0, 1872.0],
    [2094.0, 2110.0, 1865.0],[1876, 1888, 1836],[360.0, 400.0, 730.0],[1964.0, 1985.75, 1841.0],
    [780.0, 740.0, 820.0],[2011.0, 1997.0, 1838.0],[1,1,0],[0,0,0],
    [2046.0, 2061.5, 1851.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR268, "TR"); check(HO268, "HO")

(ROOT / "tools/_v268_themes.json").write_text(json.dumps({"themes": T268, "train": TR268, "heldout": HO268}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_267(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V268 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V268 overlays (new vs V49) ---")
    for a, b in [
        ("ASHCROFT bait 140.50", "ASHCROFT bait 181.91"),
        ("CEDARW bait 142.52", "CEDARC bait 183.93"),
        ("DAWNW ghost 65.65", "DAWNC ghost 106.16"),
        ("GLENW bait 135.45", "GLENC bait 176.86"),
        ("JADEW bait 126.36", "JADEC bait 167.77"),
        ("NETHERW bait 143.53", "NETHERC bait 184.94"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V268-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD267 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v267_themes.json").read_text(encoding="utf-8"))["themes"])
NEW268 = "_".join(t[0] for t in T268)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1715"), ("c1463", "c1715"), ("V226", "V268"), ("v226", "v268"),
    ("_v226c1463", "_v268c1715"),
    ("Harder than V225", "Harder than V266"), ("harder than V225", "harder than V266"),
    (OLD267, NEW268),
    ("V226 keeps floor", "V268 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1715 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1716 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1716 VL"),
    ("kept on V226", "kept on V268"),
    ("vision_images_v226", "vision_images_v268"),
    ("VL_GATE_V226", "VL_GATE_V268"), ("vl_gate_v226", "vl_gate_v268"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V266: ashcroft, cedarcroft, dawncroft, elmcroft, ferncroft, glencroft, hazecroft, inkcroft,\njadecroft, knotcroft, lakecroft, mosscroft, nethercroft, oakcroft, pinecroft, quillcroft, reedcroft, stonecroft.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T268, "v268", "V268", TR268))
out = retarget_267(out)
(S / "c1715_vision_v268_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1716"), ("c1464", "c1716"), ("V226", "V268"), ("v226", "v268"),
    ("vision_images_v226", "vision_images_v268"),
    ("VL_GATE_V226", "VL_GATE_V268"), ("vl_gate_v226", "vl_gate_v268"),
    ("runs/vision_v226", "runs/vision_v268"),
]:
    out = out.replace(a, b)
(S / "c1716_vision_v268_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1717"), ("c1465", "c1717"), ("V226", "V268"), ("v226", "v268"),
    ("vision_images_v226h", "vision_images_v268h"),
    ("vision_images_v226", "vision_images_v268"),
    ("VL_GATE_V226", "VL_GATE_V268"), ("vl_gate_v226", "vl_gate_v268"),
    ("runs/vision_v226h", "runs/vision_v268h"),
    ("_v226c1463", "_v268c1715"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T268, "v268h", "V268H", HO268))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v268h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v268"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v268" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v268h_c1717"'); seen_run = True; continue
    out2.append(ln)
(S / "c1717_vision_v268_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V268 knife = product-U2C (alternating; V267 was confidence-gate)
out = (S / "c1706_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1706", "C1718"), ("c1706", "c1718"),
    ("C1694", "C1718"), ("c1694", "c1718"),
    ("C1466", "C1718"), ("c1466", "c1718"),
]:
    out = out.replace(a, b2)
(S / "c1718_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from", "c1706_product_u2c_cost.py")

out = (S / "c1713_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1713", "C1719"), ("c1713", "c1719")]:
    out = out.replace(a, b2)
(S / "c1719_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1708_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1708", "C1720"), ("c1708", "c1720"),
    ("C1706", "C1718"), ("c1706", "c1718"),
    ("C1707", "C1719"), ("c1707", "c1719"),
    ("C1704", "C1716"), ("c1704", "c1716"),
    ("C1705", "C1717"), ("c1705", "c1717"),
    ("V266", "V268"), ("v266", "v268"),
    ("STAGE_ANT_C1708", "STAGE_ANT_C1720"),
    ("*mere", "*croft"),
]:
    out = out.replace(a, b2)
(S / "c1720_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "c1708_scorecard_and_stage.py")
print("OK builder v268 ready")
