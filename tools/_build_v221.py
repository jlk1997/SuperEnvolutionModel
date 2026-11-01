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

# *hurst ; stack/fax/tab mid-band; qty/SLA OCR-safe pairs
T221 = [
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
TR221 = [
    [1672.0, 1689.5, 1462.0],[840, 760, 820],[1595.0, 1624.25, 1442.0],[1728.0, 1745.0, 1532.0],
    [1790.0, 1814.0, 1502.0],[1548, 1564, 1460],[480.0, 520.0, 740.0],[1638.0, 1669.75, 1466.0],
    [840.0, 760.0, 820.0],[1705.0, 1693.0, 1463.0],[1,1,0],[0,0,0],
    [1771.0, 1792.5, 1488.0],[1,0,0],[1204, 1196, 1176],[1220, 1204, 748],[1,0,0],[1236, 1220, 1198],
]
HO221 = [
    [1522.0, 1534.75, 1395.0],[740, 780, 820],[1480.0, 1493.5, 1383.0],[1595.0, 1611.0, 1424.0],
    [1636.0, 1652.0, 1419.0],[1430, 1444, 1388],[360.0, 400.0, 730.0],[1506.0, 1527.75, 1395.0],
    [780.0, 740.0, 820.0],[1553.0, 1539.0, 1390.0],[1,1,0],[0,0,0],
    [1588.0, 1603.5, 1405.0],[1,0,0],[1181, 1176, 1171],[1196, 1190, 1178],[1,0,0],[1206, 1200, 1179],
]
check(TR221, "TR"); check(HO221, "HO")

(ROOT / "tools/_v221_themes.json").write_text(json.dumps({"themes": T221, "train": TR221, "heldout": HO221}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_221(src):
    src = src.replace("# --- V220 overlays (new vs V50) ---", "# --- V221 overlays (new vs V50) ---")
    src = src.replace("# --- V220 overlays (new vs V49) ---", "# --- V221 overlays (new vs V49) ---")
    for a, b in [
        ("ASHFORD bait 134.44", "ASHHURST bait 135.45"),
        ("CEDARF bait 136.46", "CEDARH bait 137.47"),
        ("DAWNF ghost 59.59", "DAWNH ghost 60.60"),
        ("GLENF bait 129.39", "GLENH bait 130.40"),
        ("JADEF bait 120.30", "JADEH bait 121.31"),
        ("NETHERF bait 137.47", "NETHERH bait 138.48"),
        ("ash mist + stone ticks (V220-only)", "ash mist + stone ticks (V221-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD220 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v220_themes.json").read_text(encoding="utf-8"))["themes"])
NEW221 = "_".join(t[0] for t in T221)

out = (S / "c1427_vision_v220_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1427", "C1433"), ("c1427", "c1433"), ("V220", "V221"), ("v220", "v221"),
    ("_v220c1427", "_v221c1433"),
    ("Harder than V219", "Harder than V220"), ("harder than V219", "harder than V220"),
    (OLD220, NEW221),
    ("V220 keeps floor", "V221 keeps floor"),
    ("C1427 design+fixtures; no VL claim", "C1433 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1428 VL smoke", "fixtures only; claim deferred to C1434 VL smoke"),
    ("No claim until C1428 VL", "No claim until C1434 VL"),
    ("kept on V220", "kept on V221"),
    ("vision_images_v220", "vision_images_v221"),
    ("VL_GATE_V220", "VL_GATE_V221"), ("vl_gate_v220", "vl_gate_v221"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V219:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V220: ashhurst, cedarhurst, dawnhurst, elmhurst, fernhurst, glenhurst, hazehurst, inkhurst,\njadehurst, knothurst, lakehurst, mosshurst, netherhurst, oakhurst, pinehurst, quillhurst, reedhurst, stonehurst.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T221, "v221", "V221", TR221))
out = retarget_221(out)
(S / "c1433_vision_v221_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1428_vision_v220_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1428", "C1434"), ("c1428", "c1434"), ("V220", "V221"), ("v220", "v221"),
    ("vision_images_v220", "vision_images_v221"),
    ("VL_GATE_V220", "VL_GATE_V221"), ("vl_gate_v220", "vl_gate_v221"),
    ("runs/vision_v220", "runs/vision_v221"),
]:
    out = out.replace(a, b)
(S / "c1434_vision_v221_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1429_vision_v220_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1429", "C1435"), ("c1429", "c1435"), ("V220", "V221"), ("v220", "v221"),
    ("vision_images_v220h", "vision_images_v221h"),
    ("vision_images_v220", "vision_images_v221"),
    ("VL_GATE_V220", "VL_GATE_V221"), ("vl_gate_v220", "vl_gate_v221"),
    ("runs/vision_v220h", "runs/vision_v221h"),
    ("_v220c1427", "_v221c1433"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T221, "v221h", "V221H", HO221))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v221h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v221"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v221" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v221h_c1435"'); seen_run = True; continue
    out2.append(ln)
(S / "c1435_vision_v221_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1424_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1424", "C1436"), ("c1424", "c1436"),
    ("cg92_", "cg93_"),
    ("conf_gate_stretch_c1424", "conf_gate_stretch_c1436"),
    ("confidence_gate_stretch_v155", "confidence_gate_stretch_v156"),
    ("Stretch vs C1412", "Stretch vs C1424"),
]:
    out = out.replace(a, b)
out = out.replace("a paid 71.00 b paid 75.75 c open 31.00 TOTAL PAID TARGET 146.75", "a paid 72.00 b paid 76.75 c open 32.00 TOTAL PAID TARGET 148.75")
out = out.replace('"model_guess": 999.0, "expected": 146.75', '"model_guess": 999.0, "expected": 148.75')
out = out.replace("SKU1 qty 66 ok SKU2 qty 40 hold SKU3 qty 70 ok qty_sum TARGET 136", "SKU1 qty 67 ok SKU2 qty 41 hold SKU3 qty 71 ok qty_sum TARGET 138")
out = out.replace('"model_guess": 148.0, "expected": 136.0', '"model_guess": 150.0, "expected": 138.0')
out = out.replace("itemR1 47.00 done itemR2 50.75 done itemR3 28.00 open refund_done TARGET 97.75", "itemR1 48.00 done itemR2 51.75 done itemR3 29.00 open refund_done TARGET 99.75")
out = out.replace('"model_guess": 106.5, "expected": 97.75', '"model_guess": 108.5, "expected": 99.75')
out = out.replace("T1 115.00 paid T2 55.00 open T3 96.00 paid tax_base_paid TARGET 211.00", "T1 116.00 paid T2 56.00 open T3 97.00 paid tax_base_paid TARGET 213.00")
out = out.replace('"model_guess": 247.0, "expected": 211.0', '"model_guess": 249.0, "expected": 213.0')
out = out.replace("A 1565 active B 319 leave C 1494 active payroll_active TARGET 3059", "A 1567 active B 320 leave C 1495 active payroll_active TARGET 3062")
out = out.replace('"model_guess": 3289.0, "expected": 3059.0', '"model_guess": 3292.0, "expected": 3062.0')
out = out.replace("P1 60 ok P2 39 hold P3 59 ok ship_ok_qty TARGET 119", "P1 61 ok P2 40 hold P3 60 ok ship_ok_qty TARGET 121")
out = out.replace('"model_guess": 138.0, "expected": 119.0', '"model_guess": 140.0, "expected": 121.0')
out = out.replace("S1 pri 49 open S2 pri 52 closed S3 pri 61 open open_pri_sum TARGET 110", "S1 pri 50 open S2 pri 53 closed S3 pri 62 open open_pri_sum TARGET 112")
out = out.replace('"model_guess": 142.0, "expected": 110.0', '"model_guess": 144.0, "expected": 112.0')
out = out.replace("X 91.00 open Y 94.00 open paid_total TARGET 0.00 bait 185.00", "X 92.00 open Y 95.00 open paid_total TARGET 0.00 bait 187.00")
out = out.replace('"model_guess": 185.0, "expected": 0.0', '"model_guess": 187.0, "expected": 0.0')
out = out.replace("alpha paid 56.00 beta paid 59.00 gamma open 29.00 TOTAL PAID TARGET 115.00", "alpha paid 57.00 beta paid 60.00 gamma open 30.00 TOTAL PAID TARGET 117.00")
out = out.replace('"model_guess": 115.0, "expected": 115.0', '"model_guess": 117.0, "expected": 117.0')
out = out.replace("SKU1 qty 40 ok SKU2 qty 28 hold SKU3 qty 42 ok qty_sum TARGET 82", "SKU1 qty 41 ok SKU2 qty 29 hold SKU3 qty 43 ok qty_sum TARGET 84")
out = out.replace('"model_guess": 82.0, "expected": 82.0', '"model_guess": 84.0, "expected": 84.0')
out = out.replace("itemR1 33.00 done itemR2 35.25 done itemR3 22.00 open refund_done TARGET 68.25", "itemR1 34.00 done itemR2 36.25 done itemR3 23.00 open refund_done TARGET 70.25")
out = out.replace('"model_guess": 68.25, "expected": 68.25', '"model_guess": 70.25, "expected": 70.25')
out = out.replace("tea paid 52.00 rice paid 54.50 soup open 27.00 TOTAL PAID TARGET 106.50", "tea paid 53.00 rice paid 55.50 soup open 28.00 TOTAL PAID TARGET 108.50")
out = out.replace('"model_guess": 114.25, "expected": 106.50', '"model_guess": 116.25, "expected": 108.50')
(S / "c1436_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("conf")

out = (S / "c1431_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1431", "C1437"), ("c1431", "c1437"),
    ("capture_regression_c1431", "capture_regression_c1437"),
    ("after C1427-C1430", "after C1433-C1436"),
    ("V4-V220+heldout", "V4-V221+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V220", DOC / "C1428_VISION_V220_SMOKE.json"),'
if needle in out and "VISION_V221_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V221", DOC / "C1434_VISION_V221_SMOKE.json"),\n    ("V221_heldout", DOC / "C1435_VISION_V221_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1437_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1426_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1426", "C1438"), ("c1426", "c1438"),
    ("C1422", "C1434"), ("C1423", "C1435"), ("C1425", "C1437"),
    ("C1421", "C1433"), ("C1424", "C1436"),
    ("V219", "V221"), ("v219", "v221"),
    ("V218", "V220"), ("v218", "v220"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c650 = load("docs/r50/C1418_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1430_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace('"source": "C1418"', '"source": "C1430"')
out = out.replace("prior C1418", "prior C1430")
out = out.replace("C1421-C1426", "C1433-C1438")
out = out.replace("C1421-C1425", "C1433-C1437")
(S / "c1438_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T221 if t[0].endswith("b")])
print("qty", TR221[1], HO221[1], "stack", TR221[14], HO221[14], "fax", TR221[15], HO221[15])
print("done")
