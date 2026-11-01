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
T289 = [
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
TR289 = [
    [2242.0, 2259.5, 1982.0],[840, 760, 820],[2165.0, 2194.25, 1960.0],[2298.0, 2315.0, 2050.0],
    [2360.0, 2384.0, 2020.0],[2078, 2094, 1978],[490.0, 530.0, 760.0],[2208.0, 2239.75, 1984.0],
    [840.0, 760.0, 820.0],[2275.0, 2263.0, 1981.0],[1,1,0],[0,0,0],
    [2341.0, 2362.5, 2006.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO289 = [
    [2040.0, 2052.75, 1901.0],[640, 660, 820],[1983.0, 1997.5, 1876.0],[2113.0, 2129.0, 1932.0],
    [2154.0, 2170.0, 1925.0],[1936, 1948, 1896],[420.0, 460.0, 740.0],[2024.0, 2045.75, 1901.0],
    [740.0, 780.0, 820.0],[2071.0, 2057.0, 1898.0],[1,1,0],[0,0,0],
    [2106.0, 2121.5, 1911.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR289, "TR"); check(HO289, "HO")

(ROOT / "tools/_v289_themes.json").write_text(json.dumps({"themes": T289, "train": TR289, "heldout": HO289}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_288(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V289 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V289 overlays (new vs V49) ---")
    for a, b in [
        ("ASHVALE bait 140.50", "ASHVALE bait 185.95"),
        ("CEDARW bait 142.52", "CEDARV bait 204.14"),
        ("DAWNW ghost 65.65", "DAWNV ghost 127.37"),
        ("GLENW bait 135.45", "GLENV bait 197.07"),
        ("JADEW bait 126.36", "JADEV bait 188.98"),
        ("NETHERW bait 143.53", "NETHERV bait 205.15"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V289-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD288 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v288_themes.json").read_text(encoding="utf-8"))["themes"])
NEW289 = "_".join(t[0] for t in T289)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1841"), ("c1463", "c1841"), ("V226", "V289"), ("v226", "v289"),
    ("_v226c1463", "_v289c1841"),
    ("Harder than V225", "Harder than V287"), ("harder than V225", "harder than V287"),
    (OLD288, NEW289),
    ("V226 keeps floor", "V289 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1841 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1842 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1842 VL"),
    ("kept on V226", "kept on V289"),
    ("vision_images_v226", "vision_images_v289"),
    ("VL_GATE_V226", "VL_GATE_V289"), ("vl_gate_v226", "vl_gate_v289"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V287: ashvale, cedarvale, dawnvale, elmvale, fernvale, glenvale, hazevale, inkvale,\njadevale, knotvale, lakevale, mossvale, nethervale, oakvale, pinevale, quillvale, reedvale, stonevale.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T289, "v289", "V289", TR289))
out = retarget_288(out)
(S / "c1841_vision_v289_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1842"), ("c1464", "c1842"), ("V226", "V289"), ("v226", "v289"),
    ("vision_images_v226", "vision_images_v289"),
    ("VL_GATE_V226", "VL_GATE_V289"), ("vl_gate_v226", "vl_gate_v289"),
    ("runs/vision_v226", "runs/vision_v289"),
]:
    out = out.replace(a, b)
(S / "c1842_vision_v289_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1843"), ("c1465", "c1843"), ("V226", "V289"), ("v226", "v289"),
    ("vision_images_v226h", "vision_images_v289h"),
    ("vision_images_v226", "vision_images_v289"),
    ("VL_GATE_V226", "VL_GATE_V289"), ("vl_gate_v226", "vl_gate_v289"),
    ("runs/vision_v226h", "runs/vision_v289h"),
    ("_v226c1463", "_v289c1841"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T289, "v289h", "V289H", HO289))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v289h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v289"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v289" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v289h_c1843"'); seen_run = True; continue
    out2.append(ln)
(S / "c1843_vision_v289_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V289 knife = confidence-gate (alternating; V288 was product-U2C; theme wrap *mere→*vale)
out = (S / "c1832_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1832", "C1844"), ("c1832", "c1844"),
    ("C1820", "C1844"), ("c1820", "c1844"),
    ("cg126_", "cg127_"),
    ("conf_gate_stretch_c1832", "conf_gate_stretch_c1844"),
    ("confidence_gate_stretch_v189", "confidence_gate_stretch_v190"),
    ("Stretch vs C1820", "Stretch vs C1832"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 105.00 b paid 109.75 c open 65.00 TOTAL PAID TARGET 214.75", "a paid 106.00 b paid 110.75 c open 66.00 TOTAL PAID TARGET 216.75")
out = out.replace('"model_guess": 999.0, "expected": 214.75', '"model_guess": 999.0, "expected": 216.75')
out = out.replace("SKU1 qty 100 ok SKU2 qty 74 hold SKU3 qty 104 ok qty_sum TARGET 204", "SKU1 qty 101 ok SKU2 qty 75 hold SKU3 qty 105 ok qty_sum TARGET 206")
out = out.replace('"model_guess": 216.0, "expected": 204.0', '"model_guess": 218.0, "expected": 206.0')
out = out.replace("itemR1 81.00 done itemR2 84.75 done itemR3 62.00 open refund_done TARGET 165.75", "itemR1 82.00 done itemR2 85.75 done itemR3 63.00 open refund_done TARGET 167.75")
out = out.replace('"model_guess": 174.5, "expected": 165.75', '"model_guess": 176.5, "expected": 167.75')
out = out.replace("T1 149.00 paid T2 89.00 open T3 130.00 paid tax_base_paid TARGET 279.00", "T1 150.00 paid T2 90.00 open T3 131.00 paid tax_base_paid TARGET 281.00")
out = out.replace('"model_guess": 315.0, "expected": 279.0', '"model_guess": 317.0, "expected": 281.0')
out = out.replace("A 1631 active B 353 leave C 1528 active payroll_active TARGET 3159", "A 1633 active B 354 leave C 1529 active payroll_active TARGET 3162")
out = out.replace('"model_guess": 3389.0, "expected": 3159.0', '"model_guess": 3392.0, "expected": 3162.0')
out = out.replace("P1 94 ok P2 73 hold P3 93 ok ship_ok_qty TARGET 187", "P1 95 ok P2 74 hold P3 94 ok ship_ok_qty TARGET 189")
out = out.replace('"model_guess": 206.0, "expected": 187.0', '"model_guess": 208.0, "expected": 189.0')
out = out.replace("S1 pri 83 open S2 pri 86 closed S3 pri 95 open open_pri_sum TARGET 178", "S1 pri 84 open S2 pri 87 closed S3 pri 96 open open_pri_sum TARGET 180")
out = out.replace('"model_guess": 210.0, "expected": 178.0', '"model_guess": 212.0, "expected": 180.0')
out = out.replace("X 125.00 open Y 128.00 open paid_total TARGET 0.00 bait 253.00", "X 126.00 open Y 129.00 open paid_total TARGET 0.00 bait 255.00")
out = out.replace('"model_guess": 253.0, "expected": 0.0', '"model_guess": 255.0, "expected": 0.0')
out = out.replace("alpha paid 90.00 beta paid 93.00 gamma open 63.00 TOTAL PAID TARGET 183.00", "alpha paid 91.00 beta paid 94.00 gamma open 64.00 TOTAL PAID TARGET 185.00")
out = out.replace('"model_guess": 183.0, "expected": 183.0', '"model_guess": 185.0, "expected": 185.0')
out = out.replace("SKU1 qty 74 ok SKU2 qty 62 hold SKU3 qty 76 ok qty_sum TARGET 150", "SKU1 qty 75 ok SKU2 qty 63 hold SKU3 qty 77 ok qty_sum TARGET 152")
out = out.replace('"model_guess": 150.0, "expected": 150.0', '"model_guess": 152.0, "expected": 152.0')
out = out.replace("itemR1 67.00 done itemR2 69.25 done itemR3 56.00 open refund_done TARGET 136.25", "itemR1 68.00 done itemR2 70.25 done itemR3 57.00 open refund_done TARGET 138.25")
out = out.replace('"model_guess": 136.25, "expected": 136.25', '"model_guess": 138.25, "expected": 138.25')
out = out.replace("tea paid 86.00 rice paid 88.50 soup open 61.00 TOTAL PAID TARGET 174.50", "tea paid 87.00 rice paid 89.50 soup open 62.00 TOTAL PAID TARGET 176.50")
out = out.replace('"model_guess": 182.25, "expected": 174.50', '"model_guess": 184.25, "expected": 176.50')
(S / "c1844_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c1832_confidence_gate_stretch.py")

out = (S / "c1839_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1839", "C1845"), ("c1839", "c1845")]:
    out = out.replace(a, b2)
(S / "c1845_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1834_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1834", "C1846"), ("c1834", "c1846"),
    ("C1832", "C1844"), ("c1832", "c1844"),
    ("C1833", "C1845"), ("c1833", "c1845"),
    ("C1830", "C1842"), ("c1830", "c1842"),
    ("C1831", "C1843"), ("c1831", "c1843"),
    ("V287", "V289"), ("v287", "v289"),
    ("STAGE_ANT_C1834", "STAGE_ANT_C1846"),
    ("*hurst", "*vale"),
]:
    out = out.replace(a, b2)
(S / "c1846_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "c1834_scorecard_and_stage.py")
print("OK builder v289 ready")
