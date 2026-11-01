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

# *dale ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T263 = [
    ["ashdale","recv","paid_total","ASHDALE GRAIN RECV","RECV","x"],
    ["cedardale","wh","qty_sum","WH CEDARDALE BIN","RECV","x"],
    ["dawndale","refund","refund_done","DAWNDALE PATCH REFUND","DONE","x"],
    ["elmdale","tax","tax_base_paid","ELMDALE TAX SLIP","TAX","x"],
    ["ferndale","pay","payroll_active","FERNDALE PAYROLL","PAY","x"],
    ["glendale","ship","ship_ok","GLENDALE SHIP DOCK","SHIP","x"],
    ["hazedale","sla","sla_ok_hours","HAZEDALE SLA CARD","SLA","x"],
    ["inkdale","exp","exp_sum","INKDALE EXPENSE","EXP","x"],
    ["jadedale","po","po_open","JADEDALE PO SHEET","PO","x"],
    ["knotdale","order","order_paid","KNOTDALE ORDER","ORD","x"],
    ["lakedale","dup","dup_mark","LAKEDALE DUP MARK","DUP","x"],
    ["mossdale","zero","zero_check","MOSSDALE AIR ZERO","ZERO","x"],
    ["netherdale","ledger","ledger_net","NETHERDALE LEDGER","LED","x"],
    ["oakdale","ui","ui_ok","OAKDALE UI SCAN","UI","x"],
    ["pinedale","stack","stack_count","PINEDALE STACK","STK","x"],
    ["quilldale","fax","fax_pages","QUILLDALE FAX","FAX","x"],
    ["reeddale","glare","glare_ok","REEDDALE GLARE","GLR","x"],
    ["stonedale","tab","tab_index","STONEDALE TAB INDEX","TAB","x"],
]
TR263 = [
    [2172.0, 2189.5, 1912.0],[840, 760, 820],[2095.0, 2124.25, 1890.0],[2228.0, 2245.0, 1980.0],
    [2290.0, 2314.0, 1950.0],[2008, 2024, 1908],[480.0, 520.0, 740.0],[2138.0, 2169.75, 1914.0],
    [840.0, 760.0, 820.0],[2205.0, 2193.0, 1911.0],[1,1,0],[0,0,0],
    [2271.0, 2292.5, 1936.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO263 = [
    [1970.0, 1982.75, 1831.0],[740, 780, 820],[1913.0, 1927.5, 1806.0],[2043.0, 2059.0, 1862.0],
    [2084.0, 2100.0, 1855.0],[1866, 1878, 1824],[360.0, 400.0, 730.0],[1954.0, 1975.75, 1831.0],
    [780.0, 740.0, 820.0],[2001.0, 1987.0, 1826.0],[1,1,0],[0,0,0],
    [2036.0, 2051.5, 1841.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR263, "TR"); check(HO263, "HO")

(ROOT / "tools/_v263_themes.json").write_text(json.dumps({"themes": T263, "train": TR263, "heldout": HO263}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_262(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V263 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V263 overlays (new vs V49) ---")
    for a, b in [
        ("ASHDALE bait 140.50", "ASHDALE bait 176.86"),
        ("CEDARW bait 142.52", "CEDARD bait 178.88"),
        ("DAWNW ghost 65.65", "DAWND ghost 101.11"),
        ("GLENW bait 135.45", "GLEND bait 171.81"),
        ("JADEW bait 126.36", "JADED bait 162.72"),
        ("NETHERW bait 143.53", "NETHERD bait 179.89"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V263-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD262 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v262_themes.json").read_text(encoding="utf-8"))["themes"])
NEW263 = "_".join(t[0] for t in T263)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1685"), ("c1463", "c1685"), ("V226", "V263"), ("v226", "v263"),
    ("_v226c1463", "_v263c1685"),
    ("Harder than V225", "Harder than V261"), ("harder than V225", "harder than V261"),
    (OLD262, NEW263),
    ("V226 keeps floor", "V263 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1685 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1686 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1686 VL"),
    ("kept on V226", "kept on V263"),
    ("vision_images_v226", "vision_images_v263"),
    ("VL_GATE_V226", "VL_GATE_V263"), ("vl_gate_v226", "vl_gate_v263"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V261: ashdale, cedardale, dawndale, elmdale, ferndale, glendale, hazedale, inkdale,\njadedale, knotdale, lakedale, mossdale, netherdale, oakdale, pinedale, quilldale, reeddale, stonedale.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T263, "v263", "V263", TR263))
out = retarget_262(out)
(S / "c1685_vision_v263_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1686"), ("c1464", "c1686"), ("V226", "V263"), ("v226", "v263"),
    ("vision_images_v226", "vision_images_v263"),
    ("VL_GATE_V226", "VL_GATE_V263"), ("vl_gate_v226", "vl_gate_v263"),
    ("runs/vision_v226", "runs/vision_v263"),
]:
    out = out.replace(a, b)
(S / "c1686_vision_v263_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1687"), ("c1465", "c1687"), ("V226", "V263"), ("v226", "v263"),
    ("vision_images_v226h", "vision_images_v263h"),
    ("vision_images_v226", "vision_images_v263"),
    ("VL_GATE_V226", "VL_GATE_V263"), ("vl_gate_v226", "vl_gate_v263"),
    ("runs/vision_v226h", "runs/vision_v263h"),
    ("_v226c1463", "_v263c1685"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T263, "v263h", "V263H", HO263))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v263h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v263"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v263" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v263h_c1687"'); seen_run = True; continue
    out2.append(ln)
(S / "c1687_vision_v263_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V263 knife = confidence-gate (alternating; V262 was product-U2C)
out = (S / "c1676_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1676", "C1688"), ("c1676", "c1688"),
    ("C1664", "C1688"), ("c1664", "c1688"),
    ("cg113_", "cg114_"),
    ("conf_gate_stretch_c1676", "conf_gate_stretch_c1688"),
    ("confidence_gate_stretch_v176", "confidence_gate_stretch_v177"),
    ("Stretch vs C1664", "Stretch vs C1676"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 92.00 b paid 96.75 c open 52.00 TOTAL PAID TARGET 188.75", "a paid 93.00 b paid 97.75 c open 53.00 TOTAL PAID TARGET 190.75")
out = out.replace('"model_guess": 999.0, "expected": 188.75', '"model_guess": 999.0, "expected": 190.75')
out = out.replace("SKU1 qty 87 ok SKU2 qty 61 hold SKU3 qty 91 ok qty_sum TARGET 178", "SKU1 qty 88 ok SKU2 qty 62 hold SKU3 qty 92 ok qty_sum TARGET 180")
out = out.replace('"model_guess": 190.0, "expected": 178.0', '"model_guess": 192.0, "expected": 180.0')
out = out.replace("itemR1 68.00 done itemR2 71.75 done itemR3 49.00 open refund_done TARGET 139.75", "itemR1 69.00 done itemR2 72.75 done itemR3 50.00 open refund_done TARGET 141.75")
out = out.replace('"model_guess": 148.5, "expected": 139.75', '"model_guess": 150.5, "expected": 141.75')
out = out.replace("T1 136.00 paid T2 76.00 open T3 117.00 paid tax_base_paid TARGET 253.00", "T1 137.00 paid T2 77.00 open T3 118.00 paid tax_base_paid TARGET 255.00")
out = out.replace('"model_guess": 289.0, "expected": 253.0', '"model_guess": 291.0, "expected": 255.0')
out = out.replace("A 1605 active B 340 leave C 1515 active payroll_active TARGET 3120", "A 1607 active B 341 leave C 1516 active payroll_active TARGET 3123")
out = out.replace('"model_guess": 3350.0, "expected": 3120.0', '"model_guess": 3353.0, "expected": 3123.0')
out = out.replace("P1 81 ok P2 60 hold P3 80 ok ship_ok_qty TARGET 161", "P1 82 ok P2 61 hold P3 81 ok ship_ok_qty TARGET 163")
out = out.replace('"model_guess": 180.0, "expected": 161.0', '"model_guess": 182.0, "expected": 163.0')
out = out.replace("S1 pri 70 open S2 pri 73 closed S3 pri 82 open open_pri_sum TARGET 152", "S1 pri 71 open S2 pri 74 closed S3 pri 83 open open_pri_sum TARGET 154")
out = out.replace('"model_guess": 184.0, "expected": 152.0', '"model_guess": 186.0, "expected": 154.0')
out = out.replace("X 112.00 open Y 115.00 open paid_total TARGET 0.00 bait 227.00", "X 113.00 open Y 116.00 open paid_total TARGET 0.00 bait 229.00")
out = out.replace('"model_guess": 227.0, "expected": 0.0', '"model_guess": 229.0, "expected": 0.0')
out = out.replace("alpha paid 77.00 beta paid 80.00 gamma open 50.00 TOTAL PAID TARGET 157.00", "alpha paid 78.00 beta paid 81.00 gamma open 51.00 TOTAL PAID TARGET 159.00")
out = out.replace('"model_guess": 157.0, "expected": 157.0', '"model_guess": 159.0, "expected": 159.0')
out = out.replace("SKU1 qty 61 ok SKU2 qty 49 hold SKU3 qty 63 ok qty_sum TARGET 124", "SKU1 qty 62 ok SKU2 qty 50 hold SKU3 qty 64 ok qty_sum TARGET 126")
out = out.replace('"model_guess": 124.0, "expected": 124.0', '"model_guess": 126.0, "expected": 126.0')
out = out.replace("itemR1 54.00 done itemR2 56.25 done itemR3 43.00 open refund_done TARGET 110.25", "itemR1 55.00 done itemR2 57.25 done itemR3 44.00 open refund_done TARGET 112.25")
out = out.replace('"model_guess": 110.25, "expected": 110.25', '"model_guess": 112.25, "expected": 112.25')
out = out.replace("tea paid 73.00 rice paid 75.50 soup open 48.00 TOTAL PAID TARGET 148.50", "tea paid 74.00 rice paid 76.50 soup open 49.00 TOTAL PAID TARGET 150.50")
out = out.replace('"model_guess": 156.25, "expected": 148.50', '"model_guess": 158.25, "expected": 150.50')
(S / "c1688_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c1676_confidence_gate_stretch.py")

out = (S / "c1683_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1683", "C1689"), ("c1683", "c1689")]:
    out = out.replace(a, b2)
(S / "c1689_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1678_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1678", "C1690"), ("c1678", "c1690"),
    ("C1676", "C1688"), ("c1676", "c1688"),
    ("C1677", "C1689"), ("c1677", "c1689"),
    ("C1674", "C1686"), ("c1674", "c1686"),
    ("C1675", "C1687"), ("c1675", "c1687"),
    ("V261", "V263"), ("v261", "v263"),
    ("STAGE_ANT_C1678", "STAGE_ANT_C1690"),
    ("*fen", "*dale"),
]:
    out = out.replace(a, b2)
(S / "c1690_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "c1678_scorecard_and_stage.py")
print("OK builder v263 ready")
