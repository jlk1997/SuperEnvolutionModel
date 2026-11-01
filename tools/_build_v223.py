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

# *vale ; stack mid-band held ~1180-1200 (anti-creep)
T223 = [
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
TR223 = [
    [1708.0, 1725.5, 1494.0],[840, 760, 820],[1631.0, 1660.25, 1474.0],[1764.0, 1781.0, 1564.0],
    [1826.0, 1850.0, 1534.0],[1584, 1600, 1492],[480.0, 520.0, 740.0],[1674.0, 1705.75, 1498.0],
    [840.0, 760.0, 820.0],[1741.0, 1729.0, 1495.0],[1,1,0],[0,0,0],
    [1807.0, 1828.5, 1520.0],[1,0,0],[1194, 1186, 1166],[1210, 1194, 748],[1,0,0],[1226, 1210, 1188],
]
HO223 = [
    [1554.0, 1566.75, 1423.0],[740, 780, 820],[1512.0, 1525.5, 1411.0],[1627.0, 1643.0, 1452.0],
    [1668.0, 1684.0, 1447.0],[1462, 1476, 1416],[360.0, 400.0, 730.0],[1538.0, 1559.75, 1423.0],
    [780.0, 740.0, 820.0],[1585.0, 1571.0, 1418.0],[1,1,0],[0,0,0],
    [1620.0, 1635.5, 1433.0],[1,0,0],[1171, 1166, 1161],[1186, 1180, 1168],[1,0,0],[1196, 1190, 1169],
]
check(TR223, "TR"); check(HO223, "HO")

(ROOT / "tools/_v223_themes.json").write_text(json.dumps({"themes": T223, "train": TR223, "heldout": HO223}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_223(src):
    src = src.replace("# --- V222 overlays (new vs V50) ---", "# --- V223 overlays (new vs V50) ---")
    src = src.replace("# --- V222 overlays (new vs V49) ---", "# --- V223 overlays (new vs V49) ---")
    for a, b in [
        ("ASHMERE bait 136.46", "ASHVALE bait 137.47"),
        ("CEDARM bait 138.48", "CEDARV bait 139.49"),
        ("DAWNM ghost 61.61", "DAWNV ghost 62.62"),
        ("GLENM bait 131.41", "GLENV bait 132.42"),
        ("JADEM bait 122.32", "JADEV bait 123.33"),
        ("NETHERM bait 139.49", "NETHERV bait 140.50"),
        ("ash mist + stone ticks (V222-only)", "ash mist + stone ticks (V223-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD222 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v222_themes.json").read_text(encoding="utf-8"))["themes"])
NEW223 = "_".join(t[0] for t in T223)

out = (S / "c1439_vision_v222_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1439", "C1445"), ("c1439", "c1445"), ("V222", "V223"), ("v222", "v223"),
    ("_v222c1439", "_v223c1445"),
    ("Harder than V221", "Harder than V222"), ("harder than V221", "harder than V222"),
    (OLD222, NEW223),
    ("V222 keeps floor", "V223 keeps floor"),
    ("C1439 design+fixtures; no VL claim", "C1445 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1440 VL smoke", "fixtures only; claim deferred to C1446 VL smoke"),
    ("No claim until C1440 VL", "No claim until C1446 VL"),
    ("kept on V222", "kept on V223"),
    ("vision_images_v222", "vision_images_v223"),
    ("VL_GATE_V222", "VL_GATE_V223"), ("vl_gate_v222", "vl_gate_v223"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V221:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V222: ashvale, cedarvale, dawnvale, elmvale, fernvale, glenvale, hazevale, inkvale,\njadevale, knotvale, lakevale, mossvale, nethervale, oakvale, pinevale, quillvale, reedvale, stonevale.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T223, "v223", "V223", TR223))
out = retarget_223(out)
(S / "c1445_vision_v223_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1440_vision_v222_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1440", "C1446"), ("c1440", "c1446"), ("V222", "V223"), ("v222", "v223"),
    ("vision_images_v222", "vision_images_v223"),
    ("VL_GATE_V222", "VL_GATE_V223"), ("vl_gate_v222", "vl_gate_v223"),
    ("runs/vision_v222", "runs/vision_v223"),
]:
    out = out.replace(a, b)
(S / "c1446_vision_v223_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1441_vision_v222_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1441", "C1447"), ("c1441", "c1447"), ("V222", "V223"), ("v222", "v223"),
    ("vision_images_v222h", "vision_images_v223h"),
    ("vision_images_v222", "vision_images_v223"),
    ("VL_GATE_V222", "VL_GATE_V223"), ("vl_gate_v222", "vl_gate_v223"),
    ("runs/vision_v222h", "runs/vision_v223h"),
    ("_v222c1439", "_v223c1445"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T223, "v223h", "V223H", HO223))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v223h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v223"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v223" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v223h_c1447"'); seen_run = True; continue
    out2.append(ln)
(S / "c1447_vision_v223_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1436_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1436", "C1448"), ("c1436", "c1448"),
    ("cg93_", "cg94_"),
    ("conf_gate_stretch_c1436", "conf_gate_stretch_c1448"),
    ("confidence_gate_stretch_v156", "confidence_gate_stretch_v157"),
    ("Stretch vs C1424", "Stretch vs C1436"),
]:
    out = out.replace(a, b)
out = out.replace("a paid 72.00 b paid 76.75 c open 32.00 TOTAL PAID TARGET 148.75", "a paid 73.00 b paid 77.75 c open 33.00 TOTAL PAID TARGET 150.75")
out = out.replace('"model_guess": 999.0, "expected": 148.75', '"model_guess": 999.0, "expected": 150.75')
out = out.replace("SKU1 qty 67 ok SKU2 qty 41 hold SKU3 qty 71 ok qty_sum TARGET 138", "SKU1 qty 68 ok SKU2 qty 42 hold SKU3 qty 72 ok qty_sum TARGET 140")
out = out.replace('"model_guess": 150.0, "expected": 138.0', '"model_guess": 152.0, "expected": 140.0')
out = out.replace("itemR1 48.00 done itemR2 51.75 done itemR3 29.00 open refund_done TARGET 99.75", "itemR1 49.00 done itemR2 52.75 done itemR3 30.00 open refund_done TARGET 101.75")
out = out.replace('"model_guess": 108.5, "expected": 99.75', '"model_guess": 110.5, "expected": 101.75')
out = out.replace("T1 116.00 paid T2 56.00 open T3 97.00 paid tax_base_paid TARGET 213.00", "T1 117.00 paid T2 57.00 open T3 98.00 paid tax_base_paid TARGET 215.00")
out = out.replace('"model_guess": 249.0, "expected": 213.0', '"model_guess": 251.0, "expected": 215.0')
out = out.replace("A 1567 active B 320 leave C 1495 active payroll_active TARGET 3062", "A 1568 active B 321 leave C 1496 active payroll_active TARGET 3064")
out = out.replace('"model_guess": 3292.0, "expected": 3062.0', '"model_guess": 3294.0, "expected": 3064.0')
out = out.replace("P1 61 ok P2 40 hold P3 60 ok ship_ok_qty TARGET 121", "P1 62 ok P2 41 hold P3 61 ok ship_ok_qty TARGET 123")
out = out.replace('"model_guess": 140.0, "expected": 121.0', '"model_guess": 142.0, "expected": 123.0')
out = out.replace("S1 pri 50 open S2 pri 53 closed S3 pri 62 open open_pri_sum TARGET 112", "S1 pri 51 open S2 pri 54 closed S3 pri 63 open open_pri_sum TARGET 114")
out = out.replace('"model_guess": 144.0, "expected": 112.0', '"model_guess": 146.0, "expected": 114.0')
out = out.replace("X 92.00 open Y 95.00 open paid_total TARGET 0.00 bait 187.00", "X 93.00 open Y 96.00 open paid_total TARGET 0.00 bait 189.00")
out = out.replace('"model_guess": 187.0, "expected": 0.0', '"model_guess": 189.0, "expected": 0.0')
out = out.replace("alpha paid 57.00 beta paid 60.00 gamma open 30.00 TOTAL PAID TARGET 117.00", "alpha paid 58.00 beta paid 61.00 gamma open 31.00 TOTAL PAID TARGET 119.00")
out = out.replace('"model_guess": 117.0, "expected": 117.0', '"model_guess": 119.0, "expected": 119.0')
out = out.replace("SKU1 qty 41 ok SKU2 qty 29 hold SKU3 qty 43 ok qty_sum TARGET 84", "SKU1 qty 42 ok SKU2 qty 30 hold SKU3 qty 44 ok qty_sum TARGET 86")
out = out.replace('"model_guess": 84.0, "expected": 84.0', '"model_guess": 86.0, "expected": 86.0')
out = out.replace("itemR1 34.00 done itemR2 36.25 done itemR3 23.00 open refund_done TARGET 70.25", "itemR1 35.00 done itemR2 37.25 done itemR3 24.00 open refund_done TARGET 72.25")
out = out.replace('"model_guess": 70.25, "expected": 70.25', '"model_guess": 72.25, "expected": 72.25')
out = out.replace("tea paid 53.00 rice paid 55.50 soup open 28.00 TOTAL PAID TARGET 108.50", "tea paid 54.00 rice paid 56.50 soup open 29.00 TOTAL PAID TARGET 110.50")
out = out.replace('"model_guess": 116.25, "expected": 108.50', '"model_guess": 118.25, "expected": 110.50')
(S / "c1448_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("conf")

out = (S / "c1443_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1443", "C1449"), ("c1443", "c1449"),
    ("capture_regression_c1443", "capture_regression_c1449"),
    ("after C1439-C1442", "after C1445-C1448"),
    ("V4-V222+heldout", "V4-V223+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V222", DOC / "C1440_VISION_V222_SMOKE.json"),'
if needle in out and "VISION_V223_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V223", DOC / "C1446_VISION_V223_SMOKE.json"),\n    ("V223_heldout", DOC / "C1447_VISION_V223_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1449_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1438_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1438", "C1450"), ("c1438", "c1450"),
    ("C1434", "C1446"), ("C1435", "C1447"), ("C1437", "C1449"),
    ("C1433", "C1445"), ("C1436", "C1448"),
    ("V221", "V223"), ("v221", "v223"),
    ("V220", "V222"), ("v220", "v222"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c650 = load("docs/r50/C1430_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1442_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace('"source": "C1430"', '"source": "C1442"')
out = out.replace("prior C1430", "prior C1442")
out = out.replace("C1433-C1438", "C1445-C1450")
out = out.replace("C1433-C1437", "C1445-C1449")
(S / "c1450_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T223 if t[0].endswith("b")])
print("qty", TR223[1], HO223[1], "stack", TR223[14], HO223[14], "fax", TR223[15], HO223[15])
print("done")
