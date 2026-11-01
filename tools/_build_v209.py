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

# *ford ; qty TR 840+760 HO 740+780; PO TR 840+760 HO 780+740; SLA TR 480+520 HO 360+400
T209 = [
    ["ashford","recv","paid_total","ASHFORD GRAIN RECV","RECV","x"],
    ["cedarford","wh","qty_sum","WH CEDARFORD BIN","RECV","x"],
    ["dawnford","refund","refund_done","DAWNFORD PATCH REFUND","DONE","x"],
    ["elmford","tax","tax_base_paid","ELMFORD TAX SLIP","TAX","x"],
    ["fernford","pay","payroll_active","FERNFORD PAYROLL","PAY","x"],
    ["glenford","ship","ship_ok","GLENFORD SHIP DOCK","SHIP","x"],
    ["hazeford","sla","sla_ok_hours","HAZEFORD SLA CARD","SLA","x"],
    ["inkford","exp","exp_sum","INKFORD EXPENSE","EXP","x"],
    ["jadeford","po","po_open","JADEFORD PO SHEET","PO","x"],
    ["knotford","order","order_paid","KNOTFORD ORDER","ORD","x"],
    ["lakeford","dup","dup_mark","LAKEFORD DUP MARK","DUP","x"],
    ["mossford","zero","zero_check","MOSSFORD AIR ZERO","ZERO","x"],
    ["netherford","ledger","ledger_net","NETHERFORD LEDGER","LED","x"],
    ["oakford","ui","ui_ok","OAKFORD UI SCAN","UI","x"],
    ["pineford","stack","stack_count","PINEFORD STACK","STK","x"],
    ["quillford","fax","fax_pages","QUILLFORD FAX","FAX","x"],
    ["reedford","glare","glare_ok","REEDFORD GLARE","GLR","x"],
    ["stoneford","tab","tab_index","STONEFORD TAB INDEX","TAB","x"],
]
TR209 = [
    [1474.0, 1491.5, 1284.0],[840, 760, 820],[1397.0, 1426.25, 1264.0],[1530.0, 1547.0, 1354.0],
    [1592.0, 1616.0, 1324.0],[1350, 1366, 1282],[480.0, 520.0, 720.0],[1440.0, 1471.75, 1288.0],
    [840.0, 760.0, 820.0],[1507.0, 1495.0, 1285.0],[1,1,0],[0,0,0],
    [1573.0, 1594.5, 1310.0],[1,0,0],[1122, 1114, 1092],[1140, 1124, 748],[1,0,0],[1166, 1142, 1112],
]
HO209 = [
    [1344.0, 1356.75, 1237.0],[740, 780, 820],[1302.0, 1315.5, 1225.0],[1417.0, 1433.0, 1266.0],
    [1458.0, 1474.0, 1261.0],[1252, 1266, 1230],[360.0, 400.0, 710.0],[1328.0, 1349.75, 1237.0],
    [780.0, 740.0, 820.0],[1375.0, 1361.0, 1232.0],[1,1,0],[0,0,0],
    [1410.0, 1425.5, 1247.0],[1,0,0],[1099, 1094, 1089],[1114, 1108, 1096],[1,0,0],[1124, 1118, 1097],
]
check(TR209, "TR"); check(HO209, "HO")

(ROOT / "tools/_v209_themes.json").write_text(json.dumps({"themes": T209, "train": TR209, "heldout": HO209}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_209(src):
    src = src.replace("# --- V208 overlays (new vs V50) ---", "# --- V209 overlays (new vs V50) ---")
    src = src.replace("# --- V208 overlays (new vs V49) ---", "# --- V209 overlays (new vs V49) ---")
    for a, b in [
        ("ASHVALE bait 122.32", "ASHFORD bait 123.33"),
        ("CEDARV bait 124.34", "CEDARF bait 125.35"),
        ("DAWNV ghost 47.47", "DAWNF ghost 48.48"),
        ("GLENV bait 117.27", "GLENF bait 118.28"),
        ("JADEV bait 108.18", "JADEF bait 109.19"),
        ("NETHERV bait 125.35", "NETHERF bait 126.36"),
        ("ash mist + stone ticks (V208-only)", "ash mist + stone ticks (V209-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD208 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v208_themes.json").read_text(encoding="utf-8"))["themes"])
NEW209 = "_".join(t[0] for t in T209)

out = (S / "c1355_vision_v208_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1355", "C1361"), ("c1355", "c1361"), ("V208", "V209"), ("v208", "v209"),
    ("_v208c1355", "_v209c1361"),
    ("Harder than V207", "Harder than V208"), ("harder than V207", "harder than V208"),
    (OLD208, NEW209),
    ("V208 keeps floor", "V209 keeps floor"),
    ("C1355 design+fixtures; no VL claim", "C1361 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1356 VL smoke", "fixtures only; claim deferred to C1362 VL smoke"),
    ("No claim until C1356 VL", "No claim until C1362 VL"),
    ("kept on V208", "kept on V209"),
    ("vision_images_v208", "vision_images_v209"),
    ("VL_GATE_V208", "VL_GATE_V209"), ("vl_gate_v208", "vl_gate_v209"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V207:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V208: ashford, cedarford, dawnford, elmford, fernford, glenford, hazeford, inkford,\njadeford, knotford, lakeford, mossford, netherford, oakford, pineford, quillford, reedford, stoneford.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T209, "v209", "V209", TR209))
out = retarget_209(out)
(S / "c1361_vision_v209_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1356_vision_v208_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1356", "C1362"), ("c1356", "c1362"), ("V208", "V209"), ("v208", "v209"),
    ("vision_images_v208", "vision_images_v209"),
    ("VL_GATE_V208", "VL_GATE_V209"), ("vl_gate_v208", "vl_gate_v209"),
    ("runs/vision_v208", "runs/vision_v209"),
]:
    out = out.replace(a, b)
(S / "c1362_vision_v209_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1357_vision_v208_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1357", "C1363"), ("c1357", "c1363"), ("V208", "V209"), ("v208", "v209"),
    ("vision_images_v208h", "vision_images_v209h"),
    ("vision_images_v208", "vision_images_v209"),
    ("VL_GATE_V208", "VL_GATE_V209"), ("vl_gate_v208", "vl_gate_v209"),
    ("runs/vision_v208h", "runs/vision_v209h"),
    ("_v208c1355", "_v209c1361"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T209, "v209h", "V209H", HO209))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v209h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v209"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v209" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v209h_c1363"'); seen_run = True; continue
    out2.append(ln)
(S / "c1363_vision_v209_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1352_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1352", "C1364"), ("c1352", "c1364"),
    ("cg86_", "cg87_"),
    ("conf_gate_stretch_c1352", "conf_gate_stretch_c1364"),
    ("confidence_gate_stretch_v149", "confidence_gate_stretch_v150"),
    ("Stretch vs C1340", "Stretch vs C1352"),
]:
    out = out.replace(a, b)
out = out.replace("a paid 65.00 b paid 69.75 c open 25.00 TOTAL PAID TARGET 134.75", "a paid 66.00 b paid 70.75 c open 26.00 TOTAL PAID TARGET 136.75")
out = out.replace('"model_guess": 999.0, "expected": 134.75', '"model_guess": 999.0, "expected": 136.75')
out = out.replace("SKU1 qty 60 ok SKU2 qty 34 hold SKU3 qty 64 ok qty_sum TARGET 124", "SKU1 qty 61 ok SKU2 qty 35 hold SKU3 qty 65 ok qty_sum TARGET 126")
out = out.replace('"model_guess": 136.0, "expected": 124.0', '"model_guess": 138.0, "expected": 126.0')
out = out.replace("itemR1 41.00 done itemR2 44.75 done itemR3 22.00 open refund_done TARGET 85.75", "itemR1 42.00 done itemR2 45.75 done itemR3 23.00 open refund_done TARGET 87.75")
out = out.replace('"model_guess": 94.5, "expected": 85.75', '"model_guess": 96.5, "expected": 87.75')
out = out.replace("T1 109.00 paid T2 49.00 open T3 90.00 paid tax_base_paid TARGET 199.00", "T1 110.00 paid T2 50.00 open T3 91.00 paid tax_base_paid TARGET 201.00")
out = out.replace('"model_guess": 235.0, "expected": 199.0', '"model_guess": 237.0, "expected": 201.0')
out = out.replace("A 1558 active B 313 leave C 1488 active payroll_active TARGET 3046", "A 1559 active B 314 leave C 1489 active payroll_active TARGET 3048")
out = out.replace('"model_guess": 3276.0, "expected": 3046.0', '"model_guess": 3278.0, "expected": 3048.0')
out = out.replace("P1 54 ok P2 33 hold P3 53 ok ship_ok_qty TARGET 107", "P1 55 ok P2 34 hold P3 54 ok ship_ok_qty TARGET 109")
out = out.replace('"model_guess": 126.0, "expected": 107.0', '"model_guess": 128.0, "expected": 109.0')
out = out.replace("S1 pri 43 open S2 pri 46 closed S3 pri 55 open open_pri_sum TARGET 98", "S1 pri 44 open S2 pri 47 closed S3 pri 56 open open_pri_sum TARGET 100")
out = out.replace('"model_guess": 130.0, "expected": 98.0', '"model_guess": 132.0, "expected": 100.0')
out = out.replace("X 85.00 open Y 88.00 open paid_total TARGET 0.00 bait 173.00", "X 86.00 open Y 89.00 open paid_total TARGET 0.00 bait 175.00")
out = out.replace('"model_guess": 173.0, "expected": 0.0', '"model_guess": 175.0, "expected": 0.0')
out = out.replace("alpha paid 50.00 beta paid 53.00 gamma open 23.00 TOTAL PAID TARGET 103.00", "alpha paid 51.00 beta paid 54.00 gamma open 24.00 TOTAL PAID TARGET 105.00")
out = out.replace('"model_guess": 103.0, "expected": 103.0', '"model_guess": 105.0, "expected": 105.0')
out = out.replace("SKU1 qty 34 ok SKU2 qty 22 hold SKU3 qty 36 ok qty_sum TARGET 70", "SKU1 qty 35 ok SKU2 qty 23 hold SKU3 qty 37 ok qty_sum TARGET 72")
out = out.replace('"model_guess": 70.0, "expected": 70.0', '"model_guess": 72.0, "expected": 72.0')
out = out.replace("itemR1 27.00 done itemR2 29.25 done itemR3 16.00 open refund_done TARGET 56.25", "itemR1 28.00 done itemR2 30.25 done itemR3 17.00 open refund_done TARGET 58.25")
out = out.replace('"model_guess": 56.25, "expected": 56.25', '"model_guess": 58.25, "expected": 58.25')
out = out.replace("tea paid 46.00 rice paid 48.50 soup open 21.00 TOTAL PAID TARGET 94.50", "tea paid 47.00 rice paid 49.50 soup open 22.00 TOTAL PAID TARGET 96.50")
out = out.replace('"model_guess": 102.25, "expected": 94.50', '"model_guess": 104.25, "expected": 96.50')
(S / "c1364_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("conf")

out = (S / "c1359_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1359", "C1365"), ("c1359", "c1365"),
    ("capture_regression_c1359", "capture_regression_c1365"),
    ("after C1355-C1358", "after C1361-C1364"),
    ("V4-V208+heldout", "V4-V209+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V208", DOC / "C1356_VISION_V208_SMOKE.json"),'
if needle in out and "VISION_V209_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V209", DOC / "C1362_VISION_V209_SMOKE.json"),\n    ("V209_heldout", DOC / "C1363_VISION_V209_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1365_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1354_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1354", "C1366"), ("c1354", "c1366"),
    ("C1350", "C1362"), ("C1351", "C1363"), ("C1353", "C1365"),
    ("C1349", "C1361"), ("C1352", "C1364"),
    ("V207", "V209"), ("v207", "v209"),
    ("V206", "V208"), ("v206", "v208"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c650 = load("docs/r50/C1346_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1358_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace('"source": "C1346"', '"source": "C1358"')
out = out.replace("prior C1346", "prior C1358")
out = out.replace("C1349-C1354", "C1361-C1366")
out = out.replace("C1349-C1353", "C1361-C1365")
(S / "c1366_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T209 if t[0].endswith("b")])
print("qty", TR209[1], HO209[1], "po", TR209[8], HO209[8], "sla", TR209[6], HO209[6], "fax", TR209[15], HO209[15])
print("done")
