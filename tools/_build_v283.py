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
T283 = [
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
TR283 = [
    [2224.0, 2241.5, 1964.0],[840, 760, 820],[2147.0, 2176.25, 1942.0],[2280.0, 2297.0, 2032.0],
    [2342.0, 2366.0, 2002.0],[2060, 2076, 1960],[490.0, 530.0, 760.0],[2190.0, 2221.75, 1966.0],
    [840.0, 760.0, 820.0],[2257.0, 2245.0, 1963.0],[1,1,0],[0,0,0],
    [2323.0, 2344.5, 1988.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO283 = [
    [2022.0, 2034.75, 1883.0],[640, 660, 820],[1965.0, 1979.5, 1858.0],[2095.0, 2111.0, 1914.0],
    [2136.0, 2152.0, 1907.0],[1918, 1930, 1878],[420.0, 460.0, 740.0],[2006.0, 2027.75, 1883.0],
    [740.0, 780.0, 820.0],[2053.0, 2039.0, 1880.0],[1,1,0],[0,0,0],
    [2088.0, 2103.5, 1893.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR283, "TR"); check(HO283, "HO")

(ROOT / "tools/_v283_themes.json").write_text(json.dumps({"themes": T283, "train": TR283, "heldout": HO283}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_282(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V283 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V283 overlays (new vs V49) ---")
    for a, b in [
        ("ASHFEN bait 140.50", "ASHFEN bait 185.95"),
        ("CEDARW bait 142.52", "CEDARF bait 198.08"),
        ("DAWNW ghost 65.65", "DAWNF ghost 121.31"),
        ("GLENW bait 135.45", "GLENF bait 191.01"),
        ("JADEW bait 126.36", "JADEF bait 182.92"),
        ("NETHERW bait 143.53", "NETHERF bait 199.09"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V283-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD282 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v282_themes.json").read_text(encoding="utf-8"))["themes"])
NEW283 = "_".join(t[0] for t in T283)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1805"), ("c1463", "c1805"), ("V226", "V283"), ("v226", "v283"),
    ("_v226c1463", "_v283c1805"),
    ("Harder than V225", "Harder than V281"), ("harder than V225", "harder than V281"),
    (OLD282, NEW283),
    ("V226 keeps floor", "V283 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1805 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1806 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1806 VL"),
    ("kept on V226", "kept on V283"),
    ("vision_images_v226", "vision_images_v283"),
    ("VL_GATE_V226", "VL_GATE_V283"), ("vl_gate_v226", "vl_gate_v283"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V281: ashfen, cedarfen, dawnfen, elmfen, fernfen, glenfen, hazefen, inkfen,\njadefen, knotfen, lakefen, mossfen, netherfen, oakfen, pinefen, quillfen, reedfen, stonefen.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T283, "v283", "V283", TR283))
out = retarget_282(out)
(S / "c1805_vision_v283_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1806"), ("c1464", "c1806"), ("V226", "V283"), ("v226", "v283"),
    ("vision_images_v226", "vision_images_v283"),
    ("VL_GATE_V226", "VL_GATE_V283"), ("vl_gate_v226", "vl_gate_v283"),
    ("runs/vision_v226", "runs/vision_v283"),
]:
    out = out.replace(a, b)
(S / "c1806_vision_v283_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1807"), ("c1465", "c1807"), ("V226", "V283"), ("v226", "v283"),
    ("vision_images_v226h", "vision_images_v283h"),
    ("vision_images_v226", "vision_images_v283"),
    ("VL_GATE_V226", "VL_GATE_V283"), ("vl_gate_v226", "vl_gate_v283"),
    ("runs/vision_v226h", "runs/vision_v283h"),
    ("_v226c1463", "_v283c1805"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T283, "v283h", "V283H", HO283))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v283h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v283"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v283" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v283h_c1807"'); seen_run = True; continue
    out2.append(ln)
(S / "c1807_vision_v283_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V283 knife = confidence-gate (alternating; V282 was product-U2C)
out = (S / "c1796_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1796", "C1808"), ("c1796", "c1808"),
    ("C1784", "C1808"), ("c1784", "c1808"),
    ("cg123_", "cg124_"),
    ("conf_gate_stretch_c1796", "conf_gate_stretch_c1808"),
    ("confidence_gate_stretch_v186", "confidence_gate_stretch_v187"),
    ("Stretch vs C1784", "Stretch vs C1796"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 102.00 b paid 106.75 c open 62.00 TOTAL PAID TARGET 208.75", "a paid 103.00 b paid 107.75 c open 63.00 TOTAL PAID TARGET 210.75")
out = out.replace('"model_guess": 999.0, "expected": 208.75', '"model_guess": 999.0, "expected": 210.75')
out = out.replace("SKU1 qty 97 ok SKU2 qty 71 hold SKU3 qty 101 ok qty_sum TARGET 198", "SKU1 qty 98 ok SKU2 qty 72 hold SKU3 qty 102 ok qty_sum TARGET 200")
out = out.replace('"model_guess": 210.0, "expected": 198.0', '"model_guess": 212.0, "expected": 200.0')
out = out.replace("itemR1 78.00 done itemR2 81.75 done itemR3 59.00 open refund_done TARGET 159.75", "itemR1 79.00 done itemR2 82.75 done itemR3 60.00 open refund_done TARGET 161.75")
out = out.replace('"model_guess": 168.5, "expected": 159.75', '"model_guess": 170.5, "expected": 161.75')
out = out.replace("T1 146.00 paid T2 86.00 open T3 127.00 paid tax_base_paid TARGET 273.00", "T1 147.00 paid T2 87.00 open T3 128.00 paid tax_base_paid TARGET 275.00")
out = out.replace('"model_guess": 309.0, "expected": 273.0', '"model_guess": 311.0, "expected": 275.0')
out = out.replace("A 1625 active B 350 leave C 1525 active payroll_active TARGET 3150", "A 1627 active B 351 leave C 1526 active payroll_active TARGET 3153")
out = out.replace('"model_guess": 3380.0, "expected": 3150.0', '"model_guess": 3383.0, "expected": 3153.0')
out = out.replace("P1 91 ok P2 70 hold P3 90 ok ship_ok_qty TARGET 181", "P1 92 ok P2 71 hold P3 91 ok ship_ok_qty TARGET 183")
out = out.replace('"model_guess": 200.0, "expected": 181.0', '"model_guess": 202.0, "expected": 183.0')
out = out.replace("S1 pri 80 open S2 pri 83 closed S3 pri 92 open open_pri_sum TARGET 172", "S1 pri 81 open S2 pri 84 closed S3 pri 93 open open_pri_sum TARGET 174")
out = out.replace('"model_guess": 204.0, "expected": 172.0', '"model_guess": 206.0, "expected": 174.0')
out = out.replace("X 122.00 open Y 125.00 open paid_total TARGET 0.00 bait 247.00", "X 123.00 open Y 126.00 open paid_total TARGET 0.00 bait 249.00")
out = out.replace('"model_guess": 247.0, "expected": 0.0', '"model_guess": 249.0, "expected": 0.0')
out = out.replace("alpha paid 87.00 beta paid 90.00 gamma open 60.00 TOTAL PAID TARGET 177.00", "alpha paid 88.00 beta paid 91.00 gamma open 61.00 TOTAL PAID TARGET 179.00")
out = out.replace('"model_guess": 177.0, "expected": 177.0', '"model_guess": 179.0, "expected": 179.0')
out = out.replace("SKU1 qty 71 ok SKU2 qty 59 hold SKU3 qty 73 ok qty_sum TARGET 144", "SKU1 qty 72 ok SKU2 qty 60 hold SKU3 qty 74 ok qty_sum TARGET 146")
out = out.replace('"model_guess": 144.0, "expected": 144.0', '"model_guess": 146.0, "expected": 146.0')
out = out.replace("itemR1 64.00 done itemR2 66.25 done itemR3 53.00 open refund_done TARGET 130.25", "itemR1 65.00 done itemR2 67.25 done itemR3 54.00 open refund_done TARGET 132.25")
out = out.replace('"model_guess": 130.25, "expected": 130.25', '"model_guess": 132.25, "expected": 132.25')
out = out.replace("tea paid 83.00 rice paid 85.50 soup open 58.00 TOTAL PAID TARGET 168.50", "tea paid 84.00 rice paid 86.50 soup open 59.00 TOTAL PAID TARGET 170.50")
out = out.replace('"model_guess": 176.25, "expected": 168.50', '"model_guess": 178.25, "expected": 170.50')
(S / "c1808_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c1796_confidence_gate_stretch.py")

out = (S / "c1803_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1803", "C1809"), ("c1803", "c1809")]:
    out = out.replace(a, b2)
(S / "c1809_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1798_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1798", "C1810"), ("c1798", "c1810"),
    ("C1796", "C1808"), ("c1796", "c1808"),
    ("C1797", "C1809"), ("c1797", "c1809"),
    ("C1794", "C1806"), ("c1794", "c1806"),
    ("C1795", "C1807"), ("c1795", "c1807"),
    ("V281", "V283"), ("v281", "v283"),
    ("STAGE_ANT_C1798", "STAGE_ANT_C1810"),
    ("*wick", "*fen"),
]:
    out = out.replace(a, b2)
(S / "c1810_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "c1798_scorecard_and_stage.py")
print("OK builder v283 ready")
