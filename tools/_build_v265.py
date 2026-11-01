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
T265 = [
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
TR265 = [
    [2176.0, 2193.5, 1916.0],[840, 760, 820],[2099.0, 2128.25, 1894.0],[2232.0, 2249.0, 1984.0],
    [2294.0, 2318.0, 1954.0],[2012, 2028, 1912],[480.0, 520.0, 740.0],[2142.0, 2173.75, 1918.0],
    [840.0, 760.0, 820.0],[2209.0, 2197.0, 1915.0],[1,1,0],[0,0,0],
    [2275.0, 2296.5, 1940.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO265 = [
    [1974.0, 1986.75, 1835.0],[740, 780, 820],[1917.0, 1931.5, 1810.0],[2047.0, 2063.0, 1866.0],
    [2088.0, 2104.0, 1859.0],[1870, 1882, 1828],[360.0, 400.0, 730.0],[1958.0, 1979.75, 1835.0],
    [780.0, 740.0, 820.0],[2005.0, 1991.0, 1832.0],[1,1,0],[0,0,0],
    [2040.0, 2055.5, 1845.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR265, "TR"); check(HO265, "HO")

(ROOT / "tools/_v265_themes.json").write_text(json.dumps({"themes": T265, "train": TR265, "heldout": HO265}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_264(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V265 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V265 overlays (new vs V49) ---")
    for a, b in [
        ("ASHHURST bait 140.50", "ASHHURST bait 178.88"),
        ("CEDARW bait 142.52", "CEDARH bait 180.90"),
        ("DAWNW ghost 65.65", "DAWNH ghost 103.13"),
        ("GLENW bait 135.45", "GLENH bait 173.83"),
        ("JADEW bait 126.36", "JADEH bait 164.74"),
        ("NETHERW bait 143.53", "NETHERH bait 181.91"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V265-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD264 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v264_themes.json").read_text(encoding="utf-8"))["themes"])
NEW265 = "_".join(t[0] for t in T265)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1697"), ("c1463", "c1697"), ("V226", "V265"), ("v226", "v265"),
    ("_v226c1463", "_v265c1697"),
    ("Harder than V225", "Harder than V263"), ("harder than V225", "harder than V263"),
    (OLD264, NEW265),
    ("V226 keeps floor", "V265 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1697 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1698 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1698 VL"),
    ("kept on V226", "kept on V265"),
    ("vision_images_v226", "vision_images_v265"),
    ("VL_GATE_V226", "VL_GATE_V265"), ("vl_gate_v226", "vl_gate_v265"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V263: ashhurst, cedarhurst, dawnhurst, elmhurst, fernhurst, glenhurst, hazehurst, inkhurst,\njadehurst, knothurst, lakehurst, mosshurst, netherhurst, oakhurst, pinehurst, quillhurst, reedhurst, stonehurst.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T265, "v265", "V265", TR265))
out = retarget_264(out)
(S / "c1697_vision_v265_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1698"), ("c1464", "c1698"), ("V226", "V265"), ("v226", "v265"),
    ("vision_images_v226", "vision_images_v265"),
    ("VL_GATE_V226", "VL_GATE_V265"), ("vl_gate_v226", "vl_gate_v265"),
    ("runs/vision_v226", "runs/vision_v265"),
]:
    out = out.replace(a, b)
(S / "c1698_vision_v265_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1699"), ("c1465", "c1699"), ("V226", "V265"), ("v226", "v265"),
    ("vision_images_v226h", "vision_images_v265h"),
    ("vision_images_v226", "vision_images_v265"),
    ("VL_GATE_V226", "VL_GATE_V265"), ("vl_gate_v226", "vl_gate_v265"),
    ("runs/vision_v226h", "runs/vision_v265h"),
    ("_v226c1463", "_v265c1697"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T265, "v265h", "V265H", HO265))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v265h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v265"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v265" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v265h_c1699"'); seen_run = True; continue
    out2.append(ln)
(S / "c1699_vision_v265_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V265 knife = confidence-gate (alternating; V264 was product-U2C)
out = (S / "c1688_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1688", "C1700"), ("c1688", "c1700"),
    ("C1676", "C1700"), ("c1676", "c1700"),
    ("cg114_", "cg115_"),
    ("conf_gate_stretch_c1688", "conf_gate_stretch_c1700"),
    ("confidence_gate_stretch_v177", "confidence_gate_stretch_v178"),
    ("Stretch vs C1676", "Stretch vs C1688"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 93.00 b paid 97.75 c open 53.00 TOTAL PAID TARGET 190.75", "a paid 94.00 b paid 98.75 c open 54.00 TOTAL PAID TARGET 192.75")
out = out.replace('"model_guess": 999.0, "expected": 190.75', '"model_guess": 999.0, "expected": 192.75')
out = out.replace("SKU1 qty 88 ok SKU2 qty 62 hold SKU3 qty 92 ok qty_sum TARGET 180", "SKU1 qty 89 ok SKU2 qty 63 hold SKU3 qty 93 ok qty_sum TARGET 182")
out = out.replace('"model_guess": 192.0, "expected": 180.0', '"model_guess": 194.0, "expected": 182.0')
out = out.replace("itemR1 69.00 done itemR2 72.75 done itemR3 50.00 open refund_done TARGET 141.75", "itemR1 70.00 done itemR2 73.75 done itemR3 51.00 open refund_done TARGET 143.75")
out = out.replace('"model_guess": 150.5, "expected": 141.75', '"model_guess": 152.5, "expected": 143.75')
out = out.replace("T1 137.00 paid T2 77.00 open T3 118.00 paid tax_base_paid TARGET 255.00", "T1 138.00 paid T2 78.00 open T3 119.00 paid tax_base_paid TARGET 257.00")
out = out.replace('"model_guess": 291.0, "expected": 255.0', '"model_guess": 293.0, "expected": 257.0')
out = out.replace("A 1607 active B 341 leave C 1516 active payroll_active TARGET 3123", "A 1609 active B 342 leave C 1517 active payroll_active TARGET 3126")
out = out.replace('"model_guess": 3353.0, "expected": 3123.0', '"model_guess": 3356.0, "expected": 3126.0')
out = out.replace("P1 82 ok P2 61 hold P3 81 ok ship_ok_qty TARGET 163", "P1 83 ok P2 62 hold P3 82 ok ship_ok_qty TARGET 165")
out = out.replace('"model_guess": 182.0, "expected": 163.0', '"model_guess": 184.0, "expected": 165.0')
out = out.replace("S1 pri 71 open S2 pri 74 closed S3 pri 83 open open_pri_sum TARGET 154", "S1 pri 72 open S2 pri 75 closed S3 pri 84 open open_pri_sum TARGET 156")
out = out.replace('"model_guess": 186.0, "expected": 154.0', '"model_guess": 188.0, "expected": 156.0')
out = out.replace("X 113.00 open Y 116.00 open paid_total TARGET 0.00 bait 229.00", "X 114.00 open Y 117.00 open paid_total TARGET 0.00 bait 231.00")
out = out.replace('"model_guess": 229.0, "expected": 0.0', '"model_guess": 231.0, "expected": 0.0')
out = out.replace("alpha paid 78.00 beta paid 81.00 gamma open 51.00 TOTAL PAID TARGET 159.00", "alpha paid 79.00 beta paid 82.00 gamma open 52.00 TOTAL PAID TARGET 161.00")
out = out.replace('"model_guess": 159.0, "expected": 159.0', '"model_guess": 161.0, "expected": 161.0')
out = out.replace("SKU1 qty 62 ok SKU2 qty 50 hold SKU3 qty 64 ok qty_sum TARGET 126", "SKU1 qty 63 ok SKU2 qty 51 hold SKU3 qty 65 ok qty_sum TARGET 128")
out = out.replace('"model_guess": 126.0, "expected": 126.0', '"model_guess": 128.0, "expected": 128.0')
out = out.replace("itemR1 55.00 done itemR2 57.25 done itemR3 44.00 open refund_done TARGET 112.25", "itemR1 56.00 done itemR2 58.25 done itemR3 45.00 open refund_done TARGET 114.25")
out = out.replace('"model_guess": 112.25, "expected": 112.25', '"model_guess": 114.25, "expected": 114.25')
out = out.replace("tea paid 74.00 rice paid 76.50 soup open 49.00 TOTAL PAID TARGET 150.50", "tea paid 75.00 rice paid 77.50 soup open 50.00 TOTAL PAID TARGET 152.50")
out = out.replace('"model_guess": 158.25, "expected": 150.50', '"model_guess": 160.25, "expected": 152.50')
(S / "c1700_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c1688_confidence_gate_stretch.py")

out = (S / "c1695_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1695", "C1701"), ("c1695", "c1701")]:
    out = out.replace(a, b2)
(S / "c1701_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1690_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1690", "C1702"), ("c1690", "c1702"),
    ("C1688", "C1700"), ("c1688", "c1700"),
    ("C1689", "C1701"), ("c1689", "c1701"),
    ("C1686", "C1698"), ("c1686", "c1698"),
    ("C1687", "C1699"), ("c1687", "c1699"),
    ("V263", "V265"), ("v263", "v265"),
    ("STAGE_ANT_C1690", "STAGE_ANT_C1702"),
    ("*dale", "*hurst"),
]:
    out = out.replace(a, b2)
(S / "c1702_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "c1690_scorecard_and_stage.py")
print("OK builder v265 ready")
