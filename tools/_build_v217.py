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

# *brook ; qty TR 840+760 HO 740+780; PO TR 840+760 HO 780+740; SLA TR 480+520 HO 360+400
T217 = [
    ["ashbrook","recv","paid_total","ASHBROOK GRAIN RECV","RECV","x"],
    ["cedarbrook","wh","qty_sum","WH CEDARBROOK BIN","RECV","x"],
    ["dawnbrook","refund","refund_done","DAWNBROOK PATCH REFUND","DONE","x"],
    ["elmbrook","tax","tax_base_paid","ELMBROOK TAX SLIP","TAX","x"],
    ["fernbrook","pay","payroll_active","FERNBROOK PAYROLL","PAY","x"],
    ["glenbrook","ship","ship_ok","GLENBROOK SHIP DOCK","SHIP","x"],
    ["hazebrook","sla","sla_ok_hours","HAZEBROOK SLA CARD","SLA","x"],
    ["inkbrook","exp","exp_sum","INKBROOK EXPENSE","EXP","x"],
    ["jadebrook","po","po_open","JADEBROOK PO SHEET","PO","x"],
    ["knotbrook","order","order_paid","KNOTBROOK ORDER","ORD","x"],
    ["lakebrook","dup","dup_mark","LAKEBROOK DUP MARK","DUP","x"],
    ["mossbrook","zero","zero_check","MOSSBROOK AIR ZERO","ZERO","x"],
    ["netherbrook","ledger","ledger_net","NETHERBROOK LEDGER","LED","x"],
    ["oakbrook","ui","ui_ok","OAKBROOK UI SCAN","UI","x"],
    ["pinebrook","stack","stack_count","PINEBROOK STACK","STK","x"],
    ["quillbrook","fax","fax_pages","QUILLBROOK FAX","FAX","x"],
    ["reedbrook","glare","glare_ok","REEDBROOK GLARE","GLR","x"],
    ["stonebrook","tab","tab_index","STONEBROOK TAB INDEX","TAB","x"],
]
TR217 = [
    [1600.0, 1617.5, 1398.0],[840, 760, 820],[1523.0, 1552.25, 1378.0],[1656.0, 1673.0, 1468.0],
    [1718.0, 1742.0, 1438.0],[1476, 1492, 1396],[480.0, 520.0, 740.0],[1566.0, 1597.75, 1402.0],
    [840.0, 760.0, 820.0],[1633.0, 1621.0, 1399.0],[1,1,0],[0,0,0],
    [1699.0, 1720.5, 1424.0],[1,0,0],[1236, 1228, 1206],[1254, 1238, 748],[1,0,0],[1280, 1256, 1226],
]
HO217 = [
    [1458.0, 1470.75, 1339.0],[740, 780, 820],[1416.0, 1429.5, 1327.0],[1531.0, 1547.0, 1368.0],
    [1572.0, 1588.0, 1363.0],[1366, 1380, 1332],[360.0, 400.0, 730.0],[1442.0, 1463.75, 1339.0],
    [780.0, 740.0, 820.0],[1489.0, 1475.0, 1334.0],[1,1,0],[0,0,0],
    [1524.0, 1539.5, 1349.0],[1,0,0],[1201, 1196, 1191],[1216, 1210, 1198],[1,0,0],[1226, 1220, 1199],
]
check(TR217, "TR"); check(HO217, "HO")

(ROOT / "tools/_v217_themes.json").write_text(json.dumps({"themes": T217, "train": TR217, "heldout": HO217}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_217(src):
    src = src.replace("# --- V216 overlays (new vs V50) ---", "# --- V217 overlays (new vs V50) ---")
    src = src.replace("# --- V216 overlays (new vs V49) ---", "# --- V217 overlays (new vs V49) ---")
    for a, b in [
        ("ASHFEN bait 130.40", "ASHBROOK bait 131.41"),
        ("CEDARF bait 132.42", "CEDARB bait 133.43"),
        ("DAWNF ghost 55.55", "DAWNB ghost 56.56"),
        ("GLENF bait 125.35", "GLENB bait 126.36"),
        ("JADEF bait 116.26", "JADEB bait 117.27"),
        ("NETHERF bait 133.43", "NETHERB bait 134.44"),
        ("ash mist + stone ticks (V216-only)", "ash mist + stone ticks (V217-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD216 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v216_themes.json").read_text(encoding="utf-8"))["themes"])
NEW217 = "_".join(t[0] for t in T217)

out = (S / "c1403_vision_v216_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1403", "C1409"), ("c1403", "c1409"), ("V216", "V217"), ("v216", "v217"),
    ("_v216c1403", "_v217c1409"),
    ("Harder than V215", "Harder than V216"), ("harder than V215", "harder than V216"),
    (OLD216, NEW217),
    ("V216 keeps floor", "V217 keeps floor"),
    ("C1403 design+fixtures; no VL claim", "C1409 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1404 VL smoke", "fixtures only; claim deferred to C1410 VL smoke"),
    ("No claim until C1404 VL", "No claim until C1410 VL"),
    ("kept on V216", "kept on V217"),
    ("vision_images_v216", "vision_images_v217"),
    ("VL_GATE_V216", "VL_GATE_V217"), ("vl_gate_v216", "vl_gate_v217"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V215:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V216: ashbrook, cedarbrook, dawnbrook, elmbrook, fernbrook, glenbrook, hazebrook, inkbrook,\njadebrook, knotbrook, lakebrook, mossbrook, netherbrook, oakbrook, pinebrook, quillbrook, reedbrook, stonebrook.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T217, "v217", "V217", TR217))
out = retarget_217(out)
(S / "c1409_vision_v217_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1404_vision_v216_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1404", "C1410"), ("c1404", "c1410"), ("V216", "V217"), ("v216", "v217"),
    ("vision_images_v216", "vision_images_v217"),
    ("VL_GATE_V216", "VL_GATE_V217"), ("vl_gate_v216", "vl_gate_v217"),
    ("runs/vision_v216", "runs/vision_v217"),
]:
    out = out.replace(a, b)
(S / "c1410_vision_v217_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1405_vision_v216_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1405", "C1411"), ("c1405", "c1411"), ("V216", "V217"), ("v216", "v217"),
    ("vision_images_v216h", "vision_images_v217h"),
    ("vision_images_v216", "vision_images_v217"),
    ("VL_GATE_V216", "VL_GATE_V217"), ("vl_gate_v216", "vl_gate_v217"),
    ("runs/vision_v216h", "runs/vision_v217h"),
    ("_v216c1403", "_v217c1409"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T217, "v217h", "V217H", HO217))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v217h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v217"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v217" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v217h_c1411"'); seen_run = True; continue
    out2.append(ln)
(S / "c1411_vision_v217_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1400_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1400", "C1412"), ("c1400", "c1412"),
    ("cg90_", "cg91_"),
    ("conf_gate_stretch_c1400", "conf_gate_stretch_c1412"),
    ("confidence_gate_stretch_v153", "confidence_gate_stretch_v154"),
    ("Stretch vs C1388", "Stretch vs C1400"),
]:
    out = out.replace(a, b)
out = out.replace("a paid 69.00 b paid 73.75 c open 29.00 TOTAL PAID TARGET 142.75", "a paid 70.00 b paid 74.75 c open 30.00 TOTAL PAID TARGET 144.75")
out = out.replace('"model_guess": 999.0, "expected": 142.75', '"model_guess": 999.0, "expected": 144.75')
out = out.replace("SKU1 qty 64 ok SKU2 qty 38 hold SKU3 qty 68 ok qty_sum TARGET 132", "SKU1 qty 65 ok SKU2 qty 39 hold SKU3 qty 69 ok qty_sum TARGET 134")
out = out.replace('"model_guess": 144.0, "expected": 132.0', '"model_guess": 146.0, "expected": 134.0')
out = out.replace("itemR1 45.00 done itemR2 48.75 done itemR3 26.00 open refund_done TARGET 93.75", "itemR1 46.00 done itemR2 49.75 done itemR3 27.00 open refund_done TARGET 95.75")
out = out.replace('"model_guess": 102.5, "expected": 93.75', '"model_guess": 104.5, "expected": 95.75')
out = out.replace("T1 113.00 paid T2 53.00 open T3 94.00 paid tax_base_paid TARGET 207.00", "T1 114.00 paid T2 54.00 open T3 95.00 paid tax_base_paid TARGET 209.00")
out = out.replace('"model_guess": 243.0, "expected": 207.0', '"model_guess": 245.0, "expected": 209.0')
out = out.replace("A 1563 active B 317 leave C 1492 active payroll_active TARGET 3055", "A 1564 active B 318 leave C 1493 active payroll_active TARGET 3057")
out = out.replace('"model_guess": 3285.0, "expected": 3055.0', '"model_guess": 3287.0, "expected": 3057.0')
out = out.replace("P1 58 ok P2 37 hold P3 57 ok ship_ok_qty TARGET 115", "P1 59 ok P2 38 hold P3 58 ok ship_ok_qty TARGET 117")
out = out.replace('"model_guess": 134.0, "expected": 115.0', '"model_guess": 136.0, "expected": 117.0')
out = out.replace("S1 pri 47 open S2 pri 50 closed S3 pri 59 open open_pri_sum TARGET 106", "S1 pri 48 open S2 pri 51 closed S3 pri 60 open open_pri_sum TARGET 108")
out = out.replace('"model_guess": 138.0, "expected": 106.0', '"model_guess": 140.0, "expected": 108.0')
out = out.replace("X 89.00 open Y 92.00 open paid_total TARGET 0.00 bait 181.00", "X 90.00 open Y 93.00 open paid_total TARGET 0.00 bait 183.00")
out = out.replace('"model_guess": 181.0, "expected": 0.0', '"model_guess": 183.0, "expected": 0.0')
out = out.replace("alpha paid 54.00 beta paid 57.00 gamma open 27.00 TOTAL PAID TARGET 111.00", "alpha paid 55.00 beta paid 58.00 gamma open 28.00 TOTAL PAID TARGET 113.00")
out = out.replace('"model_guess": 111.0, "expected": 111.0', '"model_guess": 113.0, "expected": 113.0')
out = out.replace("SKU1 qty 38 ok SKU2 qty 26 hold SKU3 qty 40 ok qty_sum TARGET 78", "SKU1 qty 39 ok SKU2 qty 27 hold SKU3 qty 41 ok qty_sum TARGET 80")
out = out.replace('"model_guess": 78.0, "expected": 78.0', '"model_guess": 80.0, "expected": 80.0')
out = out.replace("itemR1 31.00 done itemR2 33.25 done itemR3 20.00 open refund_done TARGET 64.25", "itemR1 32.00 done itemR2 34.25 done itemR3 21.00 open refund_done TARGET 66.25")
out = out.replace('"model_guess": 64.25, "expected": 64.25', '"model_guess": 66.25, "expected": 66.25')
out = out.replace("tea paid 50.00 rice paid 52.50 soup open 25.00 TOTAL PAID TARGET 102.50", "tea paid 51.00 rice paid 53.50 soup open 26.00 TOTAL PAID TARGET 104.50")
out = out.replace('"model_guess": 110.25, "expected": 102.50', '"model_guess": 112.25, "expected": 104.50')
(S / "c1412_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("conf")

out = (S / "c1407_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1407", "C1413"), ("c1407", "c1413"),
    ("capture_regression_c1407", "capture_regression_c1413"),
    ("after C1403-C1406", "after C1409-C1412"),
    ("V4-V216+heldout", "V4-V217+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V216", DOC / "C1404_VISION_V216_SMOKE.json"),'
if needle in out and "VISION_V217_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V217", DOC / "C1410_VISION_V217_SMOKE.json"),\n    ("V217_heldout", DOC / "C1411_VISION_V217_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1413_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1402_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1402", "C1414"), ("c1402", "c1414"),
    ("C1398", "C1410"), ("C1399", "C1411"), ("C1401", "C1413"),
    ("C1397", "C1409"), ("C1400", "C1412"),
    ("V215", "V217"), ("v215", "v217"),
    ("V214", "V216"), ("v214", "v216"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c650 = load("docs/r50/C1394_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1406_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace('"source": "C1394"', '"source": "C1406"')
out = out.replace("prior C1394", "prior C1406")
out = out.replace("C1397-C1402", "C1409-C1414")
out = out.replace("C1397-C1401", "C1409-C1413")
(S / "c1414_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T217 if t[0].endswith("b")])
print("qty", TR217[1], HO217[1], "po", TR217[8], HO217[8], "sla", TR217[6], HO217[6], "fax", TR217[15], HO217[15])
print("done")
