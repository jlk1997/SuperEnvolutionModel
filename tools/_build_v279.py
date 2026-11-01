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
T279 = [
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
TR279 = [
    [2212.0, 2229.5, 1952.0],[840, 760, 820],[2135.0, 2164.25, 1930.0],[2268.0, 2285.0, 2020.0],
    [2330.0, 2354.0, 1990.0],[2048, 2064, 1948],[490.0, 530.0, 760.0],[2178.0, 2209.75, 1954.0],
    [840.0, 760.0, 820.0],[2245.0, 2233.0, 1951.0],[1,1,0],[0,0,0],
    [2311.0, 2332.5, 1976.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO279 = [
    [2010.0, 2022.75, 1871.0],[640, 660, 820],[1953.0, 1967.5, 1846.0],[2083.0, 2099.0, 1902.0],
    [2124.0, 2140.0, 1895.0],[1906, 1918, 1866],[420.0, 460.0, 740.0],[1994.0, 2015.75, 1871.0],
    [740.0, 780.0, 820.0],[2041.0, 2027.0, 1868.0],[1,1,0],[0,0,0],
    [2076.0, 2091.5, 1881.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR279, "TR"); check(HO279, "HO")

(ROOT / "tools/_v279_themes.json").write_text(json.dumps({"themes": T279, "train": TR279, "heldout": HO279}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_278(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V279 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V279 overlays (new vs V49) ---")
    for a, b in [
        ("ASHCROFT bait 140.50", "ASHCROFT bait 185.95"),
        ("CEDARW bait 142.52", "CEDARC bait 194.04"),
        ("DAWNW ghost 65.65", "DAWNC ghost 117.27"),
        ("GLENW bait 135.45", "GLENC bait 187.97"),
        ("JADEW bait 126.36", "JADEC bait 178.88"),
        ("NETHERW bait 143.53", "NETHERC bait 195.05"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V279-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD278 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v278_themes.json").read_text(encoding="utf-8"))["themes"])
NEW279 = "_".join(t[0] for t in T279)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1781"), ("c1463", "c1781"), ("V226", "V279"), ("v226", "v279"),
    ("_v226c1463", "_v279c1781"),
    ("Harder than V225", "Harder than V277"), ("harder than V225", "harder than V277"),
    (OLD278, NEW279),
    ("V226 keeps floor", "V279 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1781 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1782 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1782 VL"),
    ("kept on V226", "kept on V279"),
    ("vision_images_v226", "vision_images_v279"),
    ("VL_GATE_V226", "VL_GATE_V279"), ("vl_gate_v226", "vl_gate_v279"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V277: ashcroft, cedarcroft, dawncroft, elmcroft, ferncroft, glencroft, hazecroft, inkcroft,\njadecroft, knotcroft, lakecroft, mosscroft, nethercroft, oakcroft, pinecroft, quillcroft, reedcroft, stonecroft.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T279, "v279", "V279", TR279))
out = retarget_278(out)
(S / "c1781_vision_v279_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1782"), ("c1464", "c1782"), ("V226", "V279"), ("v226", "v279"),
    ("vision_images_v226", "vision_images_v279"),
    ("VL_GATE_V226", "VL_GATE_V279"), ("vl_gate_v226", "vl_gate_v279"),
    ("runs/vision_v226", "runs/vision_v279"),
]:
    out = out.replace(a, b)
(S / "c1782_vision_v279_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1783"), ("c1465", "c1783"), ("V226", "V279"), ("v226", "v279"),
    ("vision_images_v226h", "vision_images_v279h"),
    ("vision_images_v226", "vision_images_v279"),
    ("VL_GATE_V226", "VL_GATE_V279"), ("vl_gate_v226", "vl_gate_v279"),
    ("runs/vision_v226h", "runs/vision_v279h"),
    ("_v226c1463", "_v279c1781"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T279, "v279h", "V279H", HO279))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v279h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v279"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v279" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v279h_c1783"'); seen_run = True; continue
    out2.append(ln)
(S / "c1783_vision_v279_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V279 knife = confidence-gate (alternating; V278 was product-U2C)
out = (S / "c1772_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1772", "C1784"), ("c1772", "c1784"),
    ("C1760", "C1784"), ("c1760", "c1784"),
    ("cg121_", "cg122_"),
    ("conf_gate_stretch_c1772", "conf_gate_stretch_c1784"),
    ("confidence_gate_stretch_v184", "confidence_gate_stretch_v185"),
    ("Stretch vs C1760", "Stretch vs C1772"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 100.00 b paid 104.75 c open 60.00 TOTAL PAID TARGET 204.75", "a paid 101.00 b paid 105.75 c open 61.00 TOTAL PAID TARGET 206.75")
out = out.replace('"model_guess": 999.0, "expected": 204.75', '"model_guess": 999.0, "expected": 206.75')
out = out.replace("SKU1 qty 95 ok SKU2 qty 69 hold SKU3 qty 99 ok qty_sum TARGET 194", "SKU1 qty 96 ok SKU2 qty 70 hold SKU3 qty 100 ok qty_sum TARGET 196")
out = out.replace('"model_guess": 206.0, "expected": 194.0', '"model_guess": 208.0, "expected": 196.0')
out = out.replace("itemR1 76.00 done itemR2 79.75 done itemR3 57.00 open refund_done TARGET 155.75", "itemR1 77.00 done itemR2 80.75 done itemR3 58.00 open refund_done TARGET 157.75")
out = out.replace('"model_guess": 164.5, "expected": 155.75', '"model_guess": 166.5, "expected": 157.75')
out = out.replace("T1 144.00 paid T2 84.00 open T3 125.00 paid tax_base_paid TARGET 269.00", "T1 145.00 paid T2 85.00 open T3 126.00 paid tax_base_paid TARGET 271.00")
out = out.replace('"model_guess": 305.0, "expected": 269.0', '"model_guess": 307.0, "expected": 271.0')
out = out.replace("A 1621 active B 348 leave C 1523 active payroll_active TARGET 3144", "A 1623 active B 349 leave C 1524 active payroll_active TARGET 3147")
out = out.replace('"model_guess": 3374.0, "expected": 3144.0', '"model_guess": 3377.0, "expected": 3147.0')
out = out.replace("P1 89 ok P2 68 hold P3 88 ok ship_ok_qty TARGET 177", "P1 90 ok P2 69 hold P3 89 ok ship_ok_qty TARGET 179")
out = out.replace('"model_guess": 196.0, "expected": 177.0', '"model_guess": 198.0, "expected": 179.0')
out = out.replace("S1 pri 78 open S2 pri 81 closed S3 pri 90 open open_pri_sum TARGET 168", "S1 pri 79 open S2 pri 82 closed S3 pri 91 open open_pri_sum TARGET 170")
out = out.replace('"model_guess": 200.0, "expected": 168.0', '"model_guess": 202.0, "expected": 170.0')
out = out.replace("X 120.00 open Y 123.00 open paid_total TARGET 0.00 bait 243.00", "X 121.00 open Y 124.00 open paid_total TARGET 0.00 bait 245.00")
out = out.replace('"model_guess": 243.0, "expected": 0.0', '"model_guess": 245.0, "expected": 0.0')
out = out.replace("alpha paid 85.00 beta paid 88.00 gamma open 58.00 TOTAL PAID TARGET 173.00", "alpha paid 86.00 beta paid 89.00 gamma open 59.00 TOTAL PAID TARGET 175.00")
out = out.replace('"model_guess": 173.0, "expected": 173.0', '"model_guess": 175.0, "expected": 175.0')
out = out.replace("SKU1 qty 69 ok SKU2 qty 57 hold SKU3 qty 71 ok qty_sum TARGET 140", "SKU1 qty 70 ok SKU2 qty 58 hold SKU3 qty 72 ok qty_sum TARGET 142")
out = out.replace('"model_guess": 140.0, "expected": 140.0', '"model_guess": 142.0, "expected": 142.0')
out = out.replace("itemR1 62.00 done itemR2 64.25 done itemR3 51.00 open refund_done TARGET 126.25", "itemR1 63.00 done itemR2 65.25 done itemR3 52.00 open refund_done TARGET 128.25")
out = out.replace('"model_guess": 126.25, "expected": 126.25', '"model_guess": 128.25, "expected": 128.25')
out = out.replace("tea paid 81.00 rice paid 83.50 soup open 56.00 TOTAL PAID TARGET 164.50", "tea paid 82.00 rice paid 84.50 soup open 57.00 TOTAL PAID TARGET 166.50")
out = out.replace('"model_guess": 172.25, "expected": 164.50', '"model_guess": 174.25, "expected": 166.50')
(S / "c1784_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c1772_confidence_gate_stretch.py")

out = (S / "c1779_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1779", "C1785"), ("c1779", "c1785")]:
    out = out.replace(a, b2)
(S / "c1785_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1774_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1774", "C1786"), ("c1774", "c1786"),
    ("C1772", "C1784"), ("c1772", "c1784"),
    ("C1773", "C1785"), ("c1773", "c1785"),
    ("C1770", "C1782"), ("c1770", "c1782"),
    ("C1771", "C1783"), ("c1771", "c1783"),
    ("V277", "V279"), ("v277", "v279"),
    ("STAGE_ANT_C1774", "STAGE_ANT_C1786"),
    ("*mere", "*croft"),
]:
    out = out.replace(a, b2)
(S / "c1786_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "c1774_scorecard_and_stage.py")
print("OK builder v279 ready")
