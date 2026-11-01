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
T256 = [
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
TR256 = [
    [2158.0, 2175.5, 1898.0],[840, 760, 820],[2081.0, 2110.25, 1876.0],[2214.0, 2231.0, 1966.0],
    [2276.0, 2300.0, 1936.0],[1994, 2010, 1894],[480.0, 520.0, 740.0],[2124.0, 2155.75, 1900.0],
    [840.0, 760.0, 820.0],[2191.0, 2179.0, 1897.0],[1,1,0],[0,0,0],
    [2257.0, 2278.5, 1922.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO256 = [
    [1956.0, 1968.75, 1817.0],[740, 780, 820],[1899.0, 1913.5, 1792.0],[2029.0, 2045.0, 1848.0],
    [2070.0, 2086.0, 1841.0],[1852, 1864, 1810],[360.0, 400.0, 730.0],[1940.0, 1961.75, 1817.0],
    [780.0, 740.0, 820.0],[1987.0, 1973.0, 1812.0],[1,1,0],[0,0,0],
    [2022.0, 2037.5, 1827.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR256, "TR"); check(HO256, "HO")

(ROOT / "tools/_v256_themes.json").write_text(json.dumps({"themes": T256, "train": TR256, "heldout": HO256}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_255(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V256 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V256 overlays (new vs V49) ---")
    for a, b in [
        ("ASHVALE bait 140.50", "ASHVALE bait 169.79"),
        ("CEDARW bait 142.52", "CEDARV bait 171.81"),
        ("DAWNW ghost 65.65", "DAWNV ghost 94.94"),
        ("GLENW bait 135.45", "GLENV bait 164.74"),
        ("JADEW bait 126.36", "JADEV bait 155.65"),
        ("NETHERW bait 143.53", "NETHERV bait 172.82"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V256-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD255 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v255_themes.json").read_text(encoding="utf-8"))["themes"])
NEW256 = "_".join(t[0] for t in T256)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1643"), ("c1463", "c1643"), ("V226", "V256"), ("v226", "v256"),
    ("_v226c1463", "_v256c1643"),
    ("Harder than V225", "Harder than V254"), ("harder than V225", "harder than V254"),
    (OLD255, NEW256),
    ("V226 keeps floor", "V256 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1643 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1644 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1644 VL"),
    ("kept on V226", "kept on V256"),
    ("vision_images_v226", "vision_images_v256"),
    ("VL_GATE_V226", "VL_GATE_V256"), ("vl_gate_v226", "vl_gate_v256"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V254: ashvale, cedarvale, dawnvale, elmvale, fernvale, glenvale, hazevale, inkvale,\njadevale, knotvale, lakevale, mossvale, nethervale, oakvale, pinevale, quillvale, reedvale, stonevale.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T256, "v256", "V256", TR256))
out = retarget_255(out)
(S / "c1643_vision_v256_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1644"), ("c1464", "c1644"), ("V226", "V256"), ("v226", "v256"),
    ("vision_images_v226", "vision_images_v256"),
    ("VL_GATE_V226", "VL_GATE_V256"), ("vl_gate_v226", "vl_gate_v256"),
    ("runs/vision_v226", "runs/vision_v256"),
]:
    out = out.replace(a, b)
(S / "c1644_vision_v256_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1645"), ("c1465", "c1645"), ("V226", "V256"), ("v226", "v256"),
    ("vision_images_v226h", "vision_images_v256h"),
    ("vision_images_v226", "vision_images_v256"),
    ("VL_GATE_V226", "VL_GATE_V256"), ("vl_gate_v226", "vl_gate_v256"),
    ("runs/vision_v226h", "runs/vision_v256h"),
    ("_v226c1463", "_v256c1643"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T256, "v256h", "V256H", HO256))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v256h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v256"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v256" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v256h_c1645"'); seen_run = True; continue
    out2.append(ln)
(S / "c1645_vision_v256_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V256 knife = product-U2C (alternating; V255 was confidence-gate); theme wrap *vale
out = (S / "c1634_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1634", "C1646"), ("c1634", "c1646"),
    ("C1622", "C1646"), ("c1622", "c1646"),
    ("C1466", "C1646"), ("c1466", "c1646"),
]:
    out = out.replace(a, b2)
(S / "c1646_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from", "c1634_product_u2c_cost.py")

out = (S / "c1641_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1641", "C1647"), ("c1641", "c1647")]:
    out = out.replace(a, b2)
(S / "c1647_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1636_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1636", "C1648"), ("c1636", "c1648"),
    ("C1634", "C1646"), ("c1634", "c1646"),
    ("C1635", "C1647"), ("c1635", "c1647"),
    ("C1632", "C1644"), ("c1632", "c1644"),
    ("C1633", "C1645"), ("c1633", "c1645"),
    ("V254", "V256"), ("v254", "v256"),
    ("STAGE_ANT_C1636", "STAGE_ANT_C1648"),
    ("*hurst", "*vale"),
]:
    out = out.replace(a, b2)
(S / "c1648_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "c1636_scorecard_and_stage.py")
print("OK builder v256 ready")
