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
T278 = [
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
TR278 = [
    [2209.0, 2226.5, 1949.0],[840, 760, 820],[2132.0, 2161.25, 1927.0],[2265.0, 2282.0, 2017.0],
    [2327.0, 2351.0, 1987.0],[2045, 2061, 1945],[490.0, 530.0, 760.0],[2175.0, 2206.75, 1951.0],
    [840.0, 760.0, 820.0],[2242.0, 2230.0, 1948.0],[1,1,0],[0,0,0],
    [2308.0, 2329.5, 1973.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO278 = [
    [2007.0, 2019.75, 1868.0],[640, 660, 820],[1950.0, 1964.5, 1843.0],[2080.0, 2096.0, 1899.0],
    [2121.0, 2137.0, 1892.0],[1903, 1915, 1863],[430.0, 470.0, 740.0],[1991.0, 2012.75, 1868.0],
    [740.0, 780.0, 820.0],[2038.0, 2024.0, 1865.0],[1,1,0],[0,0,0],
    [2073.0, 2088.5, 1878.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR278, "TR"); check(HO278, "HO")

(ROOT / "tools/_v278_themes.json").write_text(json.dumps({"themes": T278, "train": TR278, "heldout": HO278}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_277(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V278 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V278 overlays (new vs V49) ---")
    for a, b in [
        ("ASHVALE bait 140.50", "ASHVALE bait 185.95"),
        ("CEDARW bait 142.52", "CEDARV bait 193.03"),
        ("DAWNW ghost 65.65", "DAWNV ghost 116.26"),
        ("GLENW bait 135.45", "GLENV bait 186.96"),
        ("JADEW bait 126.36", "JADEV bait 177.87"),
        ("NETHERW bait 143.53", "NETHERV bait 194.04"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V278-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD277 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v277_themes.json").read_text(encoding="utf-8"))["themes"])
NEW278 = "_".join(t[0] for t in T278)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1775"), ("c1463", "c1775"), ("V226", "V278"), ("v226", "v278"),
    ("_v226c1463", "_v278c1775"),
    ("Harder than V225", "Harder than V276"), ("harder than V225", "harder than V276"),
    (OLD277, NEW278),
    ("V226 keeps floor", "V278 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1775 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1776 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1776 VL"),
    ("kept on V226", "kept on V278"),
    ("vision_images_v226", "vision_images_v278"),
    ("VL_GATE_V226", "VL_GATE_V278"), ("vl_gate_v226", "vl_gate_v278"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V276: ashvale, cedarvale, dawnvale, elmvale, fernvale, glenvale, hazevale, inkvale,\njadevale, knotvale, lakevale, mossvale, nethervale, oakvale, pinevale, quillvale, reedvale, stonevale.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T278, "v278", "V278", TR278))
out = retarget_277(out)
(S / "c1775_vision_v278_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1776"), ("c1464", "c1776"), ("V226", "V278"), ("v226", "v278"),
    ("vision_images_v226", "vision_images_v278"),
    ("VL_GATE_V226", "VL_GATE_V278"), ("vl_gate_v226", "vl_gate_v278"),
    ("runs/vision_v226", "runs/vision_v278"),
]:
    out = out.replace(a, b)
(S / "c1776_vision_v278_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1777"), ("c1465", "c1777"), ("V226", "V278"), ("v226", "v278"),
    ("vision_images_v226h", "vision_images_v278h"),
    ("vision_images_v226", "vision_images_v278"),
    ("VL_GATE_V226", "VL_GATE_V278"), ("vl_gate_v226", "vl_gate_v278"),
    ("runs/vision_v226h", "runs/vision_v278h"),
    ("_v226c1463", "_v278c1775"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T278, "v278h", "V278H", HO278))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v278h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v278"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v278" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v278h_c1777"'); seen_run = True; continue
    out2.append(ln)
(S / "c1777_vision_v278_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V278 knife = product-U2C (alternating; V277 was confidence-gate; theme wrap *mere→*vale)
out = (S / "c1766_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1766", "C1778"), ("c1766", "c1778"),
    ("C1754", "C1778"), ("c1754", "c1778"),
    ("C1466", "C1778"), ("c1466", "c1778"),
]:
    out = out.replace(a, b2)
(S / "c1778_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from", "c1766_product_u2c_cost.py")

out = (S / "c1773_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1773", "C1779"), ("c1773", "c1779")]:
    out = out.replace(a, b2)
(S / "c1779_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1768_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1768", "C1780"), ("c1768", "c1780"),
    ("C1766", "C1778"), ("c1766", "c1778"),
    ("C1767", "C1779"), ("c1767", "c1779"),
    ("C1764", "C1776"), ("c1764", "c1776"),
    ("C1765", "C1777"), ("c1765", "c1777"),
    ("V276", "V278"), ("v276", "v278"),
    ("STAGE_ANT_C1768", "STAGE_ANT_C1780"),
    ("*hurst", "*vale"),
]:
    out = out.replace(a, b2)
(S / "c1780_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "c1768_scorecard_and_stage.py")
print("OK builder v278 ready")
