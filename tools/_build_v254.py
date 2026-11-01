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

# *hurst ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T254 = [
    ["ashhurst","recv","paid_total","ASHHURST GRAIN RECV","RECV","x"],
    ["cedarhurst","wh","qty_sum","WH CEDARHURST BIN","RECV","x"],
    ["dawnhurst","refund","refund_done","DAWNHURST PATCH REFUND","DONE","x"],
    ["elmhurst","tax","tax_base_paid","ELMHURST TAX SLIP","TAX","x"],
    ["fernhurst","pay","payroll_active","FERNHURST PAYROLL","PAY","x"],
    ["glenhurst","ship","ship_ok","GLENHURST SHIP DOCK","SHIP","x"],
    ["hazehurst","sla","sla_ok_hours","HAZEHURST SLA CARD","SLA","x"],
    ["inkhurst","exp","exp_sum","INKHURST EXPENSE","EXP","x"],
    ["jadehurst","po","po_open","JADEHURST PO SHEET","PO","x"],
    ["knothurst","order","order_paid","KNOTHURST ORDER","ORD","x"],
    ["lakehurst","dup","dup_mark","LAKEHURST DUP MARK","DUP","x"],
    ["mosshurst","zero","zero_check","MOSSHURST AIR ZERO","ZERO","x"],
    ["netherhurst","ledger","ledger_net","NETHERHURST LEDGER","LED","x"],
    ["oakhurst","ui","ui_ok","OAKHURST UI SCAN","UI","x"],
    ["pinehurst","stack","stack_count","PINEHURST STACK","STK","x"],
    ["quillhurst","fax","fax_pages","QUILLHURST FAX","FAX","x"],
    ["reedhurst","glare","glare_ok","REEDHURST GLARE","GLR","x"],
    ["stonehurst","tab","tab_index","STONEHURST TAB INDEX","TAB","x"],
]
TR254 = [
    [2154.0, 2171.5, 1894.0],[840, 760, 820],[2077.0, 2106.25, 1872.0],[2210.0, 2227.0, 1962.0],
    [2272.0, 2296.0, 1932.0],[1990, 2006, 1890],[480.0, 520.0, 740.0],[2120.0, 2151.75, 1896.0],
    [840.0, 760.0, 820.0],[2187.0, 2175.0, 1893.0],[1,1,0],[0,0,0],
    [2253.0, 2274.5, 1918.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO254 = [
    [1952.0, 1964.75, 1813.0],[740, 780, 820],[1895.0, 1909.5, 1788.0],[2025.0, 2041.0, 1844.0],
    [2066.0, 2082.0, 1837.0],[1848, 1860, 1806],[360.0, 400.0, 730.0],[1936.0, 1957.75, 1813.0],
    [780.0, 740.0, 820.0],[1983.0, 1969.0, 1808.0],[1,1,0],[0,0,0],
    [2018.0, 2033.5, 1823.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR254, "TR"); check(HO254, "HO")

(ROOT / "tools/_v254_themes.json").write_text(json.dumps({"themes": T254, "train": TR254, "heldout": HO254}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_253(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V254 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V254 overlays (new vs V49) ---")
    for a, b in [
        ("ASHHURST bait 140.50", "ASHHURST bait 167.77"),
        ("CEDARW bait 142.52", "CEDARH bait 169.79"),
        ("DAWNW ghost 65.65", "DAWNH ghost 92.92"),
        ("GLENW bait 135.45", "GLENH bait 162.72"),
        ("JADEW bait 126.36", "JADEH bait 153.63"),
        ("NETHERW bait 143.53", "NETHERH bait 170.80"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V254-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD253 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v253_themes.json").read_text(encoding="utf-8"))["themes"])
NEW254 = "_".join(t[0] for t in T254)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1631"), ("c1463", "c1631"), ("V226", "V254"), ("v226", "v254"),
    ("_v226c1463", "_v254c1631"),
    ("Harder than V225", "Harder than V252"), ("harder than V225", "harder than V252"),
    (OLD253, NEW254),
    ("V226 keeps floor", "V254 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1631 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1632 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1632 VL"),
    ("kept on V226", "kept on V254"),
    ("vision_images_v226", "vision_images_v254"),
    ("VL_GATE_V226", "VL_GATE_V254"), ("vl_gate_v226", "vl_gate_v254"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V252: ashhurst, cedarhurst, dawnhurst, elmhurst, fernhurst, glenhurst, hazehurst, inkhurst,\njadehurst, knothurst, lakehurst, mosshurst, netherhurst, oakhurst, pinehurst, quillhurst, reedhurst, stonehurst.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T254, "v254", "V254", TR254))
out = retarget_253(out)
(S / "c1631_vision_v254_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1632"), ("c1464", "c1632"), ("V226", "V254"), ("v226", "v254"),
    ("vision_images_v226", "vision_images_v254"),
    ("VL_GATE_V226", "VL_GATE_V254"), ("vl_gate_v226", "vl_gate_v254"),
    ("runs/vision_v226", "runs/vision_v254"),
]:
    out = out.replace(a, b)
(S / "c1632_vision_v254_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1633"), ("c1465", "c1633"), ("V226", "V254"), ("v226", "v254"),
    ("vision_images_v226h", "vision_images_v254h"),
    ("vision_images_v226", "vision_images_v254"),
    ("VL_GATE_V226", "VL_GATE_V254"), ("vl_gate_v226", "vl_gate_v254"),
    ("runs/vision_v226h", "runs/vision_v254h"),
    ("_v226c1463", "_v254c1631"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T254, "v254h", "V254H", HO254))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v254h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v254"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v254" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v254h_c1633"'); seen_run = True; continue
    out2.append(ln)
(S / "c1633_vision_v254_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V254 knife = product-U2C (alternating; V253 was confidence-gate)
out = (S / "c1622_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1622", "C1634"), ("c1622", "c1634"),
    ("C1610", "C1634"), ("c1610", "c1634"),
    ("C1466", "C1634"), ("c1466", "c1634"),
]:
    out = out.replace(a, b2)
(S / "c1634_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from", "c1622_product_u2c_cost.py")

out = (S / "c1629_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1629", "C1635"), ("c1629", "c1635")]:
    out = out.replace(a, b2)
(S / "c1635_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1624_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1624", "C1636"), ("c1624", "c1636"),
    ("C1622", "C1634"), ("c1622", "c1634"),
    ("C1623", "C1635"), ("c1623", "c1635"),
    ("C1620", "C1632"), ("c1620", "c1632"),
    ("C1621", "C1633"), ("c1621", "c1633"),
    ("V252", "V254"), ("v252", "v254"),
    ("STAGE_ANT_C1624", "STAGE_ANT_C1636"),
    ("*dale", "*hurst"),
]:
    out = out.replace(a, b2)
(S / "c1636_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "c1624_scorecard_and_stage.py")
print("OK builder v254 ready")
