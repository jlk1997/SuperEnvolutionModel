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

# *vale ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T234 = [
    ["ashvale","recv","paid_total","ASHVALE GRAIN RECV","RECV","x"],
    ["cedarvale","wh","qty_sum","WH CEDARVALE BIN","RECV","x"],
    ["dawnvale","refund","refund_done","DAWNVALE PATCH REFUND","DONE","x"],
    ["elmvale","tax","tax_base_paid","ELMVALE TAX SLIP","TAX","x"],
    ["fernvale","pay","payroll_active","FERNVALE PAYROLL","PAY","x"],
    ["glenvale","ship","ship_ok","GLENVALE SHIP DOCK","SHIP","x"],
    ["hazevale","sla","sla_ok_hours","HAZEVALE SLA CARD","SLA","x"],
    ["inkvale","exp","exp_sum","INKVALE EXPENSE","EXP","x"],
    ["jadevale","po","po_open","JADEVALE PO SHEET","PO","x"],
    ["knotvale","order","order_paid","KNOTVALE ORDER","ORD","x"],
    ["lakevale","dup","dup_mark","LAKEVALE DUP MARK","DUP","x"],
    ["mossvale","zero","zero_check","MOSSVALE AIR ZERO","ZERO","x"],
    ["nethervale","ledger","ledger_net","NETHERVALE LEDGER","LED","x"],
    ["oakvale","ui","ui_ok","OAKVALE UI SCAN","UI","x"],
    ["pinevale","stack","stack_count","PINEVALE STACK","STK","x"],
    ["quillvale","fax","fax_pages","QUILLVALE FAX","FAX","x"],
    ["reedvale","glare","glare_ok","REEDVALE GLARE","GLR","x"],
    ["stonevale","tab","tab_index","STONEVALE TAB INDEX","TAB","x"],
]
TR234 = [
    [1906.0, 1923.5, 1670.0],[840, 760, 820],[1829.0, 1858.25, 1650.0],[1962.0, 1979.0, 1740.0],
    [2024.0, 2048.0, 1710.0],[1768, 1784, 1668],[480.0, 520.0, 740.0],[1872.0, 1903.75, 1674.0],
    [840.0, 760.0, 820.0],[1939.0, 1927.0, 1671.0],[1,1,0],[0,0,0],
    [2005.0, 2026.5, 1696.0],[1,0,0],[1184, 1176, 1156],[1200, 1184, 748],[1,0,0],[1216, 1200, 1178],
]
HO234 = [
    [1730.0, 1742.75, 1591.0],[740, 780, 820],[1673.0, 1686.5, 1566.0],[1803.0, 1819.0, 1620.0],
    [1844.0, 1860.0, 1615.0],[1638, 1652, 1584],[360.0, 400.0, 730.0],[1714.0, 1735.75, 1591.0],
    [780.0, 740.0, 820.0],[1761.0, 1747.0, 1586.0],[1,1,0],[0,0,0],
    [1796.0, 1811.5, 1601.0],[1,0,0],[1172, 1167, 1160],[1186, 1180, 1168],[1,0,0],[1196, 1190, 1169],
]
check(TR234, "TR"); check(HO234, "HO")

(ROOT / "tools/_v234_themes.json").write_text(json.dumps({"themes": T234, "train": TR234, "heldout": HO234}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_233(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V234 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V234 overlays (new vs V49) ---")
    for a, b in [
        ("ASHWICK bait 140.50", "ASHVALE bait 147.57"),
        ("CEDARW bait 142.52", "CEDARV bait 149.59"),
        ("DAWNW ghost 65.65", "DAWNV ghost 72.72"),
        ("GLENW bait 135.45", "GLENV bait 142.52"),
        ("JADEW bait 126.36", "JADEV bait 133.43"),
        ("NETHERW bait 143.53", "NETHERV bait 150.60"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V234-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD233 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v233_themes.json").read_text(encoding="utf-8"))["themes"])
NEW234 = "_".join(t[0] for t in T234)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1511"), ("c1463", "c1511"), ("V226", "V234"), ("v226", "v234"),
    ("_v226c1463", "_v234c1511"),
    ("Harder than V225", "Harder than V232"), ("harder than V225", "harder than V232"),
    (OLD233, NEW234),
    ("V226 keeps floor", "V234 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1511 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1512 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1512 VL"),
    ("kept on V226", "kept on V234"),
    ("vision_images_v226", "vision_images_v234"),
    ("VL_GATE_V226", "VL_GATE_V234"), ("vl_gate_v226", "vl_gate_v234"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V232: ashvale, cedarvale, dawnvale, elmvale, fernvale, glenvale, hazevale, inkvale,\njadevale, knotvale, lakevale, mossvale, nethervale, oakvale, pinevale, quillvale, reedvale, stonevale.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T234, "v234", "V234", TR234))
out = retarget_233(out)
(S / "c1511_vision_v234_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1512"), ("c1464", "c1512"), ("V226", "V234"), ("v226", "v234"),
    ("vision_images_v226", "vision_images_v234"),
    ("VL_GATE_V226", "VL_GATE_V234"), ("vl_gate_v226", "vl_gate_v234"),
    ("runs/vision_v226", "runs/vision_v234"),
]:
    out = out.replace(a, b)
(S / "c1512_vision_v234_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1513"), ("c1465", "c1513"), ("V226", "V234"), ("v226", "v234"),
    ("vision_images_v226h", "vision_images_v234h"),
    ("vision_images_v226", "vision_images_v234"),
    ("VL_GATE_V226", "VL_GATE_V234"), ("vl_gate_v226", "vl_gate_v234"),
    ("runs/vision_v226h", "runs/vision_v234h"),
    ("_v226c1463", "_v234c1511"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T234, "v234h", "V234H", HO234))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v234h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v234"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v234" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v234h_c1513"'); seen_run = True; continue
    out2.append(ln)
(S / "c1513_vision_v234_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V234 knife = product-U2C (alternating; V233 was conf-gate)
out = (S / "c1502_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1502", "C1514"), ("c1502", "c1514"),
    ("product_u2c_c1502", "product_u2c_c1514"),
    ("vs C1490", "vs C1502"),
]:
    out = out.replace(a, b2)
(S / "c1514_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c")

out = (S / "c1509_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1509", "C1515"), ("c1509", "c1515")]:
    out = out.replace(a, b2)
(S / "c1515_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1504_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1504", "C1516"), ("c1504", "c1516"),
    ("C1502", "C1514"), ("c1502", "c1514"),
    ("C1503", "C1515"), ("c1503", "c1515"),
    ("C1500", "C1512"), ("c1500", "c1512"),
    ("C1501", "C1513"), ("c1501", "c1513"),
    ("V232", "V234"), ("v232", "v234"),
    ("STAGE_ANT_C1504", "STAGE_ANT_C1516"),
    ("*hurst", "*vale"),
]:
    out = out.replace(a, b2)
(S / "c1516_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard")
print("OK builder v234 ready")
