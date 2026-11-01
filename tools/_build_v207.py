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

# *dale ; qty TR 840+760 HO 740+780; PO TR 840+760 HO 780+740; SLA TR 480+520 HO 360+400
T207 = [
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
TR207 = [
    [1456.0, 1473.5, 1266.0],[840, 760, 820],[1379.0, 1408.25, 1246.0],[1512.0, 1529.0, 1336.0],
    [1574.0, 1598.0, 1306.0],[1332, 1348, 1264],[480.0, 520.0, 740.0],[1422.0, 1453.75, 1270.0],
    [840.0, 760.0, 820.0],[1489.0, 1477.0, 1267.0],[1,1,0],[0,0,0],
    [1555.0, 1576.5, 1292.0],[1,0,0],[1104, 1096, 1074],[1122, 1106, 748],[1,0,0],[1148, 1124, 1094],
]
HO207 = [
    [1326.0, 1338.75, 1219.0],[740, 780, 820],[1284.0, 1297.5, 1207.0],[1399.0, 1415.0, 1248.0],
    [1440.0, 1456.0, 1243.0],[1234, 1248, 1212],[360.0, 400.0, 730.0],[1310.0, 1331.75, 1219.0],
    [780.0, 740.0, 820.0],[1357.0, 1343.0, 1214.0],[1,1,0],[0,0,0],
    [1392.0, 1407.5, 1229.0],[1,0,0],[1081, 1076, 1071],[1096, 1090, 1078],[1,0,0],[1106, 1100, 1079],
]
check(TR207, "TR"); check(HO207, "HO")

(ROOT / "tools/_v207_themes.json").write_text(json.dumps({"themes": T207, "train": TR207, "heldout": HO207}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_207(src):
    src = src.replace("# --- V206 overlays (new vs V50) ---", "# --- V207 overlays (new vs V50) ---")
    src = src.replace("# --- V206 overlays (new vs V49) ---", "# --- V207 overlays (new vs V49) ---")
    for a, b in [
        ("ASHBROOK bait 120.30", "ASHDALE bait 121.31"),
        ("CEDARB bait 122.32", "CEDARD bait 123.33"),
        ("DAWNB ghost 45.45", "DAWND ghost 46.46"),
        ("GLENB bait 115.25", "GLEND bait 116.26"),
        ("JADEB bait 106.16", "JADED bait 107.17"),
        ("NETHERB bait 123.33", "NETHERD bait 124.34"),
        ("ash mist + stone ticks (V206-only)", "ash mist + stone ticks (V207-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD206 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v206_themes.json").read_text(encoding="utf-8"))["themes"])
NEW207 = "_".join(t[0] for t in T207)

out = (S / "c1343_vision_v206_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1343", "C1349"), ("c1343", "c1349"), ("V206", "V207"), ("v206", "v207"),
    ("_v206c1343", "_v207c1349"),
    ("Harder than V205", "Harder than V206"), ("harder than V205", "harder than V206"),
    (OLD206, NEW207),
    ("V206 keeps floor", "V207 keeps floor"),
    ("C1343 design+fixtures; no VL claim", "C1349 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1344 VL smoke", "fixtures only; claim deferred to C1350 VL smoke"),
    ("No claim until C1344 VL", "No claim until C1350 VL"),
    ("kept on V206", "kept on V207"),
    ("vision_images_v206", "vision_images_v207"),
    ("VL_GATE_V206", "VL_GATE_V207"), ("vl_gate_v206", "vl_gate_v207"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V205:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V206: ashdale, cedardale, dawndale, elmdale, ferndale, glendale, hazedale, inkdale,\njadedale, knotdale, lakedale, mossdale, netherdale, oakdale, pinedale, quilldale, reeddale, stonedale.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T207, "v207", "V207", TR207))
out = retarget_207(out)
(S / "c1349_vision_v207_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1344_vision_v206_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1344", "C1350"), ("c1344", "c1350"), ("V206", "V207"), ("v206", "v207"),
    ("vision_images_v206", "vision_images_v207"),
    ("VL_GATE_V206", "VL_GATE_V207"), ("vl_gate_v206", "vl_gate_v207"),
    ("runs/vision_v206", "runs/vision_v207"),
]:
    out = out.replace(a, b)
(S / "c1350_vision_v207_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1345_vision_v206_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1345", "C1351"), ("c1345", "c1351"), ("V206", "V207"), ("v206", "v207"),
    ("vision_images_v206h", "vision_images_v207h"),
    ("vision_images_v206", "vision_images_v207"),
    ("VL_GATE_V206", "VL_GATE_V207"), ("vl_gate_v206", "vl_gate_v207"),
    ("runs/vision_v206h", "runs/vision_v207h"),
    ("_v206c1343", "_v207c1349"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T207, "v207h", "V207H", HO207))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v207h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v207"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v207" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v207h_c1351"'); seen_run = True; continue
    out2.append(ln)
(S / "c1351_vision_v207_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1340_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1340", "C1352"), ("c1340", "c1352"),
    ("cg85_", "cg86_"),
    ("conf_gate_stretch_c1340", "conf_gate_stretch_c1352"),
    ("confidence_gate_stretch_v148", "confidence_gate_stretch_v149"),
    ("Stretch vs C1328", "Stretch vs C1340"),
]:
    out = out.replace(a, b)
out = out.replace("a paid 64.00 b paid 68.75 c open 24.00 TOTAL PAID TARGET 132.75", "a paid 65.00 b paid 69.75 c open 25.00 TOTAL PAID TARGET 134.75")
out = out.replace('"model_guess": 999.0, "expected": 132.75', '"model_guess": 999.0, "expected": 134.75')
out = out.replace("SKU1 qty 59 ok SKU2 qty 33 hold SKU3 qty 63 ok qty_sum TARGET 122", "SKU1 qty 60 ok SKU2 qty 34 hold SKU3 qty 64 ok qty_sum TARGET 124")
out = out.replace('"model_guess": 134.0, "expected": 122.0', '"model_guess": 136.0, "expected": 124.0')
out = out.replace("itemR1 40.00 done itemR2 43.75 done itemR3 21.00 open refund_done TARGET 83.75", "itemR1 41.00 done itemR2 44.75 done itemR3 22.00 open refund_done TARGET 85.75")
out = out.replace('"model_guess": 92.5, "expected": 83.75', '"model_guess": 94.5, "expected": 85.75')
out = out.replace("T1 108.00 paid T2 48.00 open T3 89.00 paid tax_base_paid TARGET 197.00", "T1 109.00 paid T2 49.00 open T3 90.00 paid tax_base_paid TARGET 199.00")
out = out.replace('"model_guess": 233.0, "expected": 197.0', '"model_guess": 235.0, "expected": 199.0')
out = out.replace("A 1557 active B 312 leave C 1487 active payroll_active TARGET 3044", "A 1558 active B 313 leave C 1488 active payroll_active TARGET 3046")
out = out.replace('"model_guess": 3274.0, "expected": 3044.0', '"model_guess": 3276.0, "expected": 3046.0')
out = out.replace("P1 53 ok P2 32 hold P3 52 ok ship_ok_qty TARGET 105", "P1 54 ok P2 33 hold P3 53 ok ship_ok_qty TARGET 107")
out = out.replace('"model_guess": 124.0, "expected": 105.0', '"model_guess": 126.0, "expected": 107.0')
out = out.replace("S1 pri 42 open S2 pri 45 closed S3 pri 54 open open_pri_sum TARGET 96", "S1 pri 43 open S2 pri 46 closed S3 pri 55 open open_pri_sum TARGET 98")
out = out.replace('"model_guess": 128.0, "expected": 96.0', '"model_guess": 130.0, "expected": 98.0')
out = out.replace("X 84.00 open Y 87.00 open paid_total TARGET 0.00 bait 171.00", "X 85.00 open Y 88.00 open paid_total TARGET 0.00 bait 173.00")
out = out.replace('"model_guess": 171.0, "expected": 0.0', '"model_guess": 173.0, "expected": 0.0')
out = out.replace("alpha paid 49.00 beta paid 52.00 gamma open 22.00 TOTAL PAID TARGET 101.00", "alpha paid 50.00 beta paid 53.00 gamma open 23.00 TOTAL PAID TARGET 103.00")
out = out.replace('"model_guess": 101.0, "expected": 101.0', '"model_guess": 103.0, "expected": 103.0')
out = out.replace("SKU1 qty 33 ok SKU2 qty 21 hold SKU3 qty 35 ok qty_sum TARGET 68", "SKU1 qty 34 ok SKU2 qty 22 hold SKU3 qty 36 ok qty_sum TARGET 70")
out = out.replace('"model_guess": 68.0, "expected": 68.0', '"model_guess": 70.0, "expected": 70.0')
out = out.replace("itemR1 26.00 done itemR2 28.25 done itemR3 15.00 open refund_done TARGET 54.25", "itemR1 27.00 done itemR2 29.25 done itemR3 16.00 open refund_done TARGET 56.25")
out = out.replace('"model_guess": 54.25, "expected": 54.25', '"model_guess": 56.25, "expected": 56.25')
out = out.replace("tea paid 45.00 rice paid 47.50 soup open 20.00 TOTAL PAID TARGET 92.50", "tea paid 46.00 rice paid 48.50 soup open 21.00 TOTAL PAID TARGET 94.50")
out = out.replace('"model_guess": 100.25, "expected": 92.50', '"model_guess": 102.25, "expected": 94.50')
(S / "c1352_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("conf")

out = (S / "c1347_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1347", "C1353"), ("c1347", "c1353"),
    ("capture_regression_c1347", "capture_regression_c1353"),
    ("after C1343-C1346", "after C1349-C1352"),
    ("V4-V206+heldout", "V4-V207+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V206", DOC / "C1344_VISION_V206_SMOKE.json"),'
if needle in out and "VISION_V207_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V207", DOC / "C1350_VISION_V207_SMOKE.json"),\n    ("V207_heldout", DOC / "C1351_VISION_V207_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1353_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1342_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1342", "C1354"), ("c1342", "c1354"),
    ("C1338", "C1350"), ("C1339", "C1351"), ("C1341", "C1353"),
    ("C1337", "C1349"), ("C1340", "C1352"),
    ("V205", "V207"), ("v205", "v207"),
    ("V204", "V206"), ("v204", "v206"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c650 = load("docs/r50/C1334_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1346_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace('"source": "C1334"', '"source": "C1346"')
out = out.replace("prior C1334", "prior C1346")
out = out.replace("C1337-C1342", "C1349-C1354")
out = out.replace("C1337-C1341", "C1349-C1353")
(S / "c1354_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T207 if t[0].endswith("b")])
print("qty", TR207[1], HO207[1], "po", TR207[8], HO207[8], "sla", TR207[6], HO207[6], "fax", TR207[15], HO207[15])
print("done")
