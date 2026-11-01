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
T267 = [
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
TR267 = [
    [2180.0, 2197.5, 1920.0],[840, 760, 820],[2103.0, 2132.25, 1898.0],[2236.0, 2253.0, 1988.0],
    [2298.0, 2322.0, 1958.0],[2016, 2032, 1916],[480.0, 520.0, 740.0],[2146.0, 2177.75, 1922.0],
    [840.0, 760.0, 820.0],[2213.0, 2201.0, 1919.0],[1,1,0],[0,0,0],
    [2279.0, 2300.5, 1944.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO267 = [
    [1978.0, 1990.75, 1839.0],[740, 780, 820],[1921.0, 1935.5, 1814.0],[2051.0, 2067.0, 1870.0],
    [2092.0, 2108.0, 1863.0],[1874, 1886, 1834],[360.0, 400.0, 730.0],[1962.0, 1983.75, 1839.0],
    [780.0, 740.0, 820.0],[2009.0, 1995.0, 1836.0],[1,1,0],[0,0,0],
    [2044.0, 2059.5, 1849.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR267, "TR"); check(HO267, "HO")

(ROOT / "tools/_v267_themes.json").write_text(json.dumps({"themes": T267, "train": TR267, "heldout": HO267}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_266(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V267 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V267 overlays (new vs V49) ---")
    for a, b in [
        ("ASHVALE bait 140.50", "ASHVALE bait 180.90"),
        ("CEDARW bait 142.52", "CEDARV bait 182.92"),
        ("DAWNW ghost 65.65", "DAWNV ghost 105.15"),
        ("GLENW bait 135.45", "GLENV bait 175.85"),
        ("JADEW bait 126.36", "JADEV bait 166.76"),
        ("NETHERW bait 143.53", "NETHERV bait 183.93"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V267-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD266 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v266_themes.json").read_text(encoding="utf-8"))["themes"])
NEW267 = "_".join(t[0] for t in T267)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1709"), ("c1463", "c1709"), ("V226", "V267"), ("v226", "v267"),
    ("_v226c1463", "_v267c1709"),
    ("Harder than V225", "Harder than V265"), ("harder than V225", "harder than V265"),
    (OLD266, NEW267),
    ("V226 keeps floor", "V267 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1709 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1710 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1710 VL"),
    ("kept on V226", "kept on V267"),
    ("vision_images_v226", "vision_images_v267"),
    ("VL_GATE_V226", "VL_GATE_V267"), ("vl_gate_v226", "vl_gate_v267"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V265: ashvale, cedarvale, dawnvale, elmvale, fernvale, glenvale, hazevale, inkvale,\njadevale, knotvale, lakevale, mossvale, nethervale, oakvale, pinevale, quillvale, reedvale, stonevale.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T267, "v267", "V267", TR267))
out = retarget_266(out)
(S / "c1709_vision_v267_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1710"), ("c1464", "c1710"), ("V226", "V267"), ("v226", "v267"),
    ("vision_images_v226", "vision_images_v267"),
    ("VL_GATE_V226", "VL_GATE_V267"), ("vl_gate_v226", "vl_gate_v267"),
    ("runs/vision_v226", "runs/vision_v267"),
]:
    out = out.replace(a, b)
(S / "c1710_vision_v267_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1711"), ("c1465", "c1711"), ("V226", "V267"), ("v226", "v267"),
    ("vision_images_v226h", "vision_images_v267h"),
    ("vision_images_v226", "vision_images_v267"),
    ("VL_GATE_V226", "VL_GATE_V267"), ("vl_gate_v226", "vl_gate_v267"),
    ("runs/vision_v226h", "runs/vision_v267h"),
    ("_v226c1463", "_v267c1709"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T267, "v267h", "V267H", HO267))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v267h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v267"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v267" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v267h_c1711"'); seen_run = True; continue
    out2.append(ln)
(S / "c1711_vision_v267_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V267 knife = confidence-gate (alternating; V266 was product-U2C); theme wrap *vale
out = (S / "c1700_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1700", "C1712"), ("c1700", "c1712"),
    ("C1688", "C1712"), ("c1688", "c1712"),
    ("cg115_", "cg116_"),
    ("conf_gate_stretch_c1700", "conf_gate_stretch_c1712"),
    ("confidence_gate_stretch_v178", "confidence_gate_stretch_v179"),
    ("Stretch vs C1688", "Stretch vs C1700"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 94.00 b paid 98.75 c open 54.00 TOTAL PAID TARGET 192.75", "a paid 95.00 b paid 99.75 c open 55.00 TOTAL PAID TARGET 194.75")
out = out.replace('"model_guess": 999.0, "expected": 192.75', '"model_guess": 999.0, "expected": 194.75')
out = out.replace("SKU1 qty 89 ok SKU2 qty 63 hold SKU3 qty 93 ok qty_sum TARGET 182", "SKU1 qty 90 ok SKU2 qty 64 hold SKU3 qty 94 ok qty_sum TARGET 184")
out = out.replace('"model_guess": 194.0, "expected": 182.0', '"model_guess": 196.0, "expected": 184.0')
out = out.replace("itemR1 70.00 done itemR2 73.75 done itemR3 51.00 open refund_done TARGET 143.75", "itemR1 71.00 done itemR2 74.75 done itemR3 52.00 open refund_done TARGET 145.75")
out = out.replace('"model_guess": 152.5, "expected": 143.75', '"model_guess": 154.5, "expected": 145.75')
out = out.replace("T1 138.00 paid T2 78.00 open T3 119.00 paid tax_base_paid TARGET 257.00", "T1 139.00 paid T2 79.00 open T3 120.00 paid tax_base_paid TARGET 259.00")
out = out.replace('"model_guess": 293.0, "expected": 257.0', '"model_guess": 295.0, "expected": 259.0')
out = out.replace("A 1609 active B 342 leave C 1517 active payroll_active TARGET 3126", "A 1611 active B 343 leave C 1518 active payroll_active TARGET 3129")
out = out.replace('"model_guess": 3356.0, "expected": 3126.0', '"model_guess": 3359.0, "expected": 3129.0')
out = out.replace("P1 83 ok P2 62 hold P3 82 ok ship_ok_qty TARGET 165", "P1 84 ok P2 63 hold P3 83 ok ship_ok_qty TARGET 167")
out = out.replace('"model_guess": 184.0, "expected": 165.0', '"model_guess": 186.0, "expected": 167.0')
out = out.replace("S1 pri 72 open S2 pri 75 closed S3 pri 84 open open_pri_sum TARGET 156", "S1 pri 73 open S2 pri 76 closed S3 pri 85 open open_pri_sum TARGET 158")
out = out.replace('"model_guess": 188.0, "expected": 156.0', '"model_guess": 190.0, "expected": 158.0')
out = out.replace("X 114.00 open Y 117.00 open paid_total TARGET 0.00 bait 231.00", "X 115.00 open Y 118.00 open paid_total TARGET 0.00 bait 233.00")
out = out.replace('"model_guess": 231.0, "expected": 0.0', '"model_guess": 233.0, "expected": 0.0')
out = out.replace("alpha paid 79.00 beta paid 82.00 gamma open 52.00 TOTAL PAID TARGET 161.00", "alpha paid 80.00 beta paid 83.00 gamma open 53.00 TOTAL PAID TARGET 163.00")
out = out.replace('"model_guess": 161.0, "expected": 161.0', '"model_guess": 163.0, "expected": 163.0')
out = out.replace("SKU1 qty 63 ok SKU2 qty 51 hold SKU3 qty 65 ok qty_sum TARGET 128", "SKU1 qty 64 ok SKU2 qty 52 hold SKU3 qty 66 ok qty_sum TARGET 130")
out = out.replace('"model_guess": 128.0, "expected": 128.0', '"model_guess": 130.0, "expected": 130.0')
out = out.replace("itemR1 56.00 done itemR2 58.25 done itemR3 45.00 open refund_done TARGET 114.25", "itemR1 57.00 done itemR2 59.25 done itemR3 46.00 open refund_done TARGET 116.25")
out = out.replace('"model_guess": 114.25, "expected": 114.25', '"model_guess": 116.25, "expected": 116.25')
out = out.replace("tea paid 75.00 rice paid 77.50 soup open 50.00 TOTAL PAID TARGET 152.50", "tea paid 76.00 rice paid 78.50 soup open 51.00 TOTAL PAID TARGET 154.50")
out = out.replace('"model_guess": 160.25, "expected": 152.50', '"model_guess": 162.25, "expected": 154.50')
(S / "c1712_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c1700_confidence_gate_stretch.py")

out = (S / "c1707_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1707", "C1713"), ("c1707", "c1713")]:
    out = out.replace(a, b2)
(S / "c1713_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1702_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1702", "C1714"), ("c1702", "c1714"),
    ("C1700", "C1712"), ("c1700", "c1712"),
    ("C1701", "C1713"), ("c1701", "c1713"),
    ("C1698", "C1710"), ("c1698", "c1710"),
    ("C1699", "C1711"), ("c1699", "c1711"),
    ("V265", "V267"), ("v265", "v267"),
    ("STAGE_ANT_C1702", "STAGE_ANT_C1714"),
    ("*hurst", "*vale"),
]:
    out = out.replace(a, b2)
(S / "c1714_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "c1702_scorecard_and_stage.py")
print("OK builder v267 ready")
