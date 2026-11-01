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

# *fen ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T261 = [
    ["ashfen","recv","paid_total","ASHFEN GRAIN RECV","RECV","x"],
    ["cedarfen","wh","qty_sum","WH CEDARFEN BIN","RECV","x"],
    ["dawnfen","refund","refund_done","DAWNFEN PATCH REFUND","DONE","x"],
    ["elmfen","tax","tax_base_paid","ELMFEN TAX SLIP","TAX","x"],
    ["fernfen","pay","payroll_active","FERNFEN PAYROLL","PAY","x"],
    ["glenfen","ship","ship_ok","GLENFEN SHIP DOCK","SHIP","x"],
    ["hazefen","sla","sla_ok_hours","HAZEFEN SLA CARD","SLA","x"],
    ["inkfen","exp","exp_sum","INKFEN EXPENSE","EXP","x"],
    ["jadefen","po","po_open","JADEFEN PO SHEET","PO","x"],
    ["knotfen","order","order_paid","KNOTFEN ORDER","ORD","x"],
    ["lakefen","dup","dup_mark","LAKEFEN DUP MARK","DUP","x"],
    ["mossfen","zero","zero_check","MOSSFEN AIR ZERO","ZERO","x"],
    ["netherfen","ledger","ledger_net","NETHERFEN LEDGER","LED","x"],
    ["oakfen","ui","ui_ok","OAKFEN UI SCAN","UI","x"],
    ["pinefen","stack","stack_count","PINEFEN STACK","STK","x"],
    ["quillfen","fax","fax_pages","QUILLFEN FAX","FAX","x"],
    ["reedfen","glare","glare_ok","REEDFEN GLARE","GLR","x"],
    ["stonefen","tab","tab_index","STONEFEN TAB INDEX","TAB","x"],
]
TR261 = [
    [2168.0, 2185.5, 1908.0],[840, 760, 820],[2091.0, 2120.25, 1886.0],[2224.0, 2241.0, 1976.0],
    [2286.0, 2310.0, 1946.0],[2004, 2020, 1904],[480.0, 520.0, 740.0],[2134.0, 2165.75, 1910.0],
    [840.0, 760.0, 820.0],[2201.0, 2189.0, 1907.0],[1,1,0],[0,0,0],
    [2267.0, 2288.5, 1932.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO261 = [
    [1966.0, 1978.75, 1827.0],[740, 780, 820],[1909.0, 1923.5, 1802.0],[2039.0, 2055.0, 1858.0],
    [2080.0, 2096.0, 1851.0],[1862, 1874, 1820],[360.0, 400.0, 730.0],[1950.0, 1971.75, 1827.0],
    [780.0, 740.0, 820.0],[1997.0, 1983.0, 1822.0],[1,1,0],[0,0,0],
    [2032.0, 2047.5, 1837.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR261, "TR"); check(HO261, "HO")

(ROOT / "tools/_v261_themes.json").write_text(json.dumps({"themes": T261, "train": TR261, "heldout": HO261}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_260(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V261 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V261 overlays (new vs V49) ---")
    for a, b in [
        ("ASHFEN bait 140.50", "ASHFEN bait 174.84"),
        ("CEDARW bait 142.52", "CEDARF bait 176.86"),
        ("DAWNW ghost 65.65", "DAWNF ghost 99.99"),
        ("GLENW bait 135.45", "GLENF bait 169.79"),
        ("JADEW bait 126.36", "JADEF bait 160.70"),
        ("NETHERW bait 143.53", "NETHERF bait 177.87"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V261-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD260 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v260_themes.json").read_text(encoding="utf-8"))["themes"])
NEW261 = "_".join(t[0] for t in T261)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1673"), ("c1463", "c1673"), ("V226", "V261"), ("v226", "v261"),
    ("_v226c1463", "_v261c1673"),
    ("Harder than V225", "Harder than V259"), ("harder than V225", "harder than V259"),
    (OLD260, NEW261),
    ("V226 keeps floor", "V261 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1673 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1674 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1674 VL"),
    ("kept on V226", "kept on V261"),
    ("vision_images_v226", "vision_images_v261"),
    ("VL_GATE_V226", "VL_GATE_V261"), ("vl_gate_v226", "vl_gate_v261"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V259: ashfen, cedarfen, dawnfen, elmfen, fernfen, glenfen, hazefen, inkfen,\njadefen, knotfen, lakefen, mossfen, netherfen, oakfen, pinefen, quillfen, reedfen, stonefen.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T261, "v261", "V261", TR261))
out = retarget_260(out)
(S / "c1673_vision_v261_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1674"), ("c1464", "c1674"), ("V226", "V261"), ("v226", "v261"),
    ("vision_images_v226", "vision_images_v261"),
    ("VL_GATE_V226", "VL_GATE_V261"), ("vl_gate_v226", "vl_gate_v261"),
    ("runs/vision_v226", "runs/vision_v261"),
]:
    out = out.replace(a, b)
(S / "c1674_vision_v261_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1675"), ("c1465", "c1675"), ("V226", "V261"), ("v226", "v261"),
    ("vision_images_v226h", "vision_images_v261h"),
    ("vision_images_v226", "vision_images_v261"),
    ("VL_GATE_V226", "VL_GATE_V261"), ("vl_gate_v226", "vl_gate_v261"),
    ("runs/vision_v226h", "runs/vision_v261h"),
    ("_v226c1463", "_v261c1673"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T261, "v261h", "V261H", HO261))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v261h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v261"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v261" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v261h_c1675"'); seen_run = True; continue
    out2.append(ln)
(S / "c1675_vision_v261_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V261 knife = confidence-gate (alternating; V260 was product-U2C)
out = (S / "c1664_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1664", "C1676"), ("c1664", "c1676"),
    ("C1652", "C1676"), ("c1652", "c1676"),
    ("cg112_", "cg113_"),
    ("conf_gate_stretch_c1664", "conf_gate_stretch_c1676"),
    ("confidence_gate_stretch_v175", "confidence_gate_stretch_v176"),
    ("Stretch vs C1652", "Stretch vs C1664"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 91.00 b paid 95.75 c open 51.00 TOTAL PAID TARGET 186.75", "a paid 92.00 b paid 96.75 c open 52.00 TOTAL PAID TARGET 188.75")
out = out.replace('"model_guess": 999.0, "expected": 186.75', '"model_guess": 999.0, "expected": 188.75')
out = out.replace("SKU1 qty 86 ok SKU2 qty 60 hold SKU3 qty 90 ok qty_sum TARGET 176", "SKU1 qty 87 ok SKU2 qty 61 hold SKU3 qty 91 ok qty_sum TARGET 178")
out = out.replace('"model_guess": 188.0, "expected": 176.0', '"model_guess": 190.0, "expected": 178.0')
out = out.replace("itemR1 67.00 done itemR2 70.75 done itemR3 48.00 open refund_done TARGET 137.75", "itemR1 68.00 done itemR2 71.75 done itemR3 49.00 open refund_done TARGET 139.75")
out = out.replace('"model_guess": 146.5, "expected": 137.75', '"model_guess": 148.5, "expected": 139.75')
out = out.replace("T1 135.00 paid T2 75.00 open T3 116.00 paid tax_base_paid TARGET 251.00", "T1 136.00 paid T2 76.00 open T3 117.00 paid tax_base_paid TARGET 253.00")
out = out.replace('"model_guess": 287.0, "expected": 251.0', '"model_guess": 289.0, "expected": 253.0')
out = out.replace("A 1603 active B 339 leave C 1514 active payroll_active TARGET 3117", "A 1605 active B 340 leave C 1515 active payroll_active TARGET 3120")
out = out.replace('"model_guess": 3347.0, "expected": 3117.0', '"model_guess": 3350.0, "expected": 3120.0')
out = out.replace("P1 80 ok P2 59 hold P3 79 ok ship_ok_qty TARGET 159", "P1 81 ok P2 60 hold P3 80 ok ship_ok_qty TARGET 161")
out = out.replace('"model_guess": 178.0, "expected": 159.0', '"model_guess": 180.0, "expected": 161.0')
out = out.replace("S1 pri 69 open S2 pri 72 closed S3 pri 81 open open_pri_sum TARGET 150", "S1 pri 70 open S2 pri 73 closed S3 pri 82 open open_pri_sum TARGET 152")
out = out.replace('"model_guess": 182.0, "expected": 150.0', '"model_guess": 184.0, "expected": 152.0')
out = out.replace("X 111.00 open Y 114.00 open paid_total TARGET 0.00 bait 225.00", "X 112.00 open Y 115.00 open paid_total TARGET 0.00 bait 227.00")
out = out.replace('"model_guess": 225.0, "expected": 0.0', '"model_guess": 227.0, "expected": 0.0')
out = out.replace("alpha paid 76.00 beta paid 79.00 gamma open 49.00 TOTAL PAID TARGET 155.00", "alpha paid 77.00 beta paid 80.00 gamma open 50.00 TOTAL PAID TARGET 157.00")
out = out.replace('"model_guess": 155.0, "expected": 155.0', '"model_guess": 157.0, "expected": 157.0')
out = out.replace("SKU1 qty 60 ok SKU2 qty 48 hold SKU3 qty 62 ok qty_sum TARGET 122", "SKU1 qty 61 ok SKU2 qty 49 hold SKU3 qty 63 ok qty_sum TARGET 124")
out = out.replace('"model_guess": 122.0, "expected": 122.0', '"model_guess": 124.0, "expected": 124.0')
out = out.replace("itemR1 53.00 done itemR2 55.25 done itemR3 42.00 open refund_done TARGET 108.25", "itemR1 54.00 done itemR2 56.25 done itemR3 43.00 open refund_done TARGET 110.25")
out = out.replace('"model_guess": 108.25, "expected": 108.25', '"model_guess": 110.25, "expected": 110.25')
out = out.replace("tea paid 72.00 rice paid 74.50 soup open 47.00 TOTAL PAID TARGET 146.50", "tea paid 73.00 rice paid 75.50 soup open 48.00 TOTAL PAID TARGET 148.50")
out = out.replace('"model_guess": 154.25, "expected": 146.50', '"model_guess": 156.25, "expected": 148.50')
(S / "c1676_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c1664_confidence_gate_stretch.py")

out = (S / "c1671_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1671", "C1677"), ("c1671", "c1677")]:
    out = out.replace(a, b2)
(S / "c1677_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1666_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1666", "C1678"), ("c1666", "c1678"),
    ("C1664", "C1676"), ("c1664", "c1676"),
    ("C1665", "C1677"), ("c1665", "c1677"),
    ("C1662", "C1674"), ("c1662", "c1674"),
    ("C1663", "C1675"), ("c1663", "c1675"),
    ("V259", "V261"), ("v259", "v261"),
    ("STAGE_ANT_C1666", "STAGE_ANT_C1678"),
    ("*wick", "*fen"),
]:
    out = out.replace(a, b2)
(S / "c1678_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "c1666_scorecard_and_stage.py")
print("OK builder v261 ready")
