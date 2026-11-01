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
T195 = [
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
TR195 = [
    [1348.0, 1365.5, 1158.0],[840, 760, 820],[1271.0, 1300.25, 1138.0],[1404.0, 1421.0, 1228.0],
    [1466.0, 1490.0, 1198.0],[1224, 1240, 1156],[480.0, 520.0, 760.0],[1314.0, 1345.75, 1162.0],
    [840.0, 760.0, 820.0],[1381.0, 1369.0, 1159.0],[1,1,0],[0,0,0],
    [1447.0, 1468.5, 1184.0],[1,0,0],[996, 988, 966],[1014, 998, 748],[1,0,0],[1040, 1016, 986],
]
HO195 = [
    [1218.0, 1230.75, 1111.0],[740, 780, 820],[1176.0, 1189.5, 1099.0],[1291.0, 1307.0, 1140.0],
    [1332.0, 1348.0, 1135.0],[1126, 1140, 1104],[360.0, 400.0, 690.0],[1202.0, 1223.75, 1111.0],
    [780.0, 740.0, 820.0],[1249.0, 1235.0, 1106.0],[1,1,0],[0,0,0],
    [1284.0, 1299.5, 1121.0],[1,0,0],[973, 968, 963],[988, 982, 970],[1,0,0],[998, 992, 971],
]
check(TR195, "TR"); check(HO195, "HO")

(ROOT / "tools/_v195_themes.json").write_text(json.dumps({"themes": T195, "train": TR195, "heldout": HO195}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_195(src):
    src = src.replace("# --- V194 overlays (new vs V50) ---", "# --- V195 overlays (new vs V50) ---")
    src = src.replace("# --- V194 overlays (new vs V49) ---", "# --- V195 overlays (new vs V49) ---")
    for a, b in [
        ("ASHFEN bait 108.18", "ASHBROOK bait 109.19"),
        ("CEDARF bait 110.20", "CEDARB bait 111.21"),
        ("DAWNF ghost 33.33", "DAWNB ghost 34.34"),
        ("GLENF bait 103.13", "GLENB bait 104.14"),
        ("JADEF bait 94.94", "JADEB bait 95.95"),
        ("NETHERF bait 111.21", "NETHERB bait 112.22"),
        ("ash mist + stone ticks (V194-only)", "ash mist + stone ticks (V195-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD194 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v194_themes.json").read_text(encoding="utf-8"))["themes"])
NEW195 = "_".join(t[0] for t in T195)

out = (S / "c1271_vision_v194_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1271", "C1277"), ("c1271", "c1277"), ("V194", "V195"), ("v194", "v195"),
    ("_v194c1271", "_v195c1277"),
    ("Harder than V193", "Harder than V194"), ("harder than V193", "harder than V194"),
    (OLD194, NEW195),
    ("V194 keeps floor", "V195 keeps floor"),
    ("C1271 design+fixtures; no VL claim", "C1277 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1272 VL smoke", "fixtures only; claim deferred to C1278 VL smoke"),
    ("No claim until C1272 VL", "No claim until C1278 VL"),
    ("kept on V194", "kept on V195"),
    ("vision_images_v194", "vision_images_v195"),
    ("VL_GATE_V194", "VL_GATE_V195"), ("vl_gate_v194", "vl_gate_v195"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V193:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V194: ashbrook, cedarbrook, dawnbrook, elmbrook, fernbrook, glenbrook, hazebrook, inkbrook,\njadebrook, knotbrook, lakebrook, mossbrook, netherbrook, oakbrook, pinebrook, quillbrook, reedbrook, stonebrook.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T195, "v195", "V195", TR195))
out = retarget_195(out)
(S / "c1277_vision_v195_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1272_vision_v194_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1272", "C1278"), ("c1272", "c1278"), ("V194", "V195"), ("v194", "v195"),
    ("vision_images_v194", "vision_images_v195"),
    ("VL_GATE_V194", "VL_GATE_V195"), ("vl_gate_v194", "vl_gate_v195"),
    ("runs/vision_v194", "runs/vision_v195"),
]:
    out = out.replace(a, b)
(S / "c1278_vision_v195_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1273_vision_v194_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1273", "C1279"), ("c1273", "c1279"), ("V194", "V195"), ("v194", "v195"),
    ("vision_images_v194h", "vision_images_v195h"),
    ("vision_images_v194", "vision_images_v195"),
    ("VL_GATE_V194", "VL_GATE_V195"), ("vl_gate_v194", "vl_gate_v195"),
    ("runs/vision_v194h", "runs/vision_v195h"),
    ("_v194c1271", "_v195c1277"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T195, "v195h", "V195H", HO195))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v195h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v195"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v195" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v195h_c1279"'); seen_run = True; continue
    out2.append(ln)
(S / "c1279_vision_v195_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1268_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1268", "C1280"), ("c1268", "c1280"),
    ("cg79_", "cg80_"),
    ("conf_gate_stretch_c1268", "conf_gate_stretch_c1280"),
    ("confidence_gate_stretch_v142", "confidence_gate_stretch_v143"),
    ("Stretch vs C1256", "Stretch vs C1268"),
]:
    out = out.replace(a, b)
out = out.replace("a paid 58.00 b paid 62.75 c open 18.00 TOTAL PAID TARGET 120.75", "a paid 59.00 b paid 63.75 c open 19.00 TOTAL PAID TARGET 122.75")
out = out.replace('"model_guess": 999.0, "expected": 120.75', '"model_guess": 999.0, "expected": 122.75')
out = out.replace("SKU1 qty 53 ok SKU2 qty 27 hold SKU3 qty 57 ok qty_sum TARGET 110", "SKU1 qty 54 ok SKU2 qty 28 hold SKU3 qty 58 ok qty_sum TARGET 112")
out = out.replace('"model_guess": 122.0, "expected": 110.0', '"model_guess": 124.0, "expected": 112.0')
out = out.replace("itemR1 34.00 done itemR2 37.75 done itemR3 15.00 open refund_done TARGET 71.75", "itemR1 35.00 done itemR2 38.75 done itemR3 16.00 open refund_done TARGET 73.75")
out = out.replace('"model_guess": 80.5, "expected": 71.75', '"model_guess": 82.5, "expected": 73.75')
out = out.replace("T1 102.00 paid T2 42.00 open T3 83.00 paid tax_base_paid TARGET 185.00", "T1 103.00 paid T2 43.00 open T3 84.00 paid tax_base_paid TARGET 187.00")
out = out.replace('"model_guess": 221.0, "expected": 185.0', '"model_guess": 223.0, "expected": 187.0')
out = out.replace("A 1551 active B 306 leave C 1481 active payroll_active TARGET 3032", "A 1552 active B 307 leave C 1482 active payroll_active TARGET 3034")
out = out.replace('"model_guess": 3262.0, "expected": 3032.0', '"model_guess": 3264.0, "expected": 3034.0')
out = out.replace("P1 47 ok P2 26 hold P3 46 ok ship_ok_qty TARGET 93", "P1 48 ok P2 27 hold P3 47 ok ship_ok_qty TARGET 95")
out = out.replace('"model_guess": 112.0, "expected": 93.0', '"model_guess": 114.0, "expected": 95.0')
out = out.replace("S1 pri 36 open S2 pri 39 closed S3 pri 48 open open_pri_sum TARGET 84", "S1 pri 37 open S2 pri 40 closed S3 pri 49 open open_pri_sum TARGET 86")
out = out.replace('"model_guess": 116.0, "expected": 84.0', '"model_guess": 118.0, "expected": 86.0')
out = out.replace("X 78.00 open Y 81.00 open paid_total TARGET 0.00 bait 159.00", "X 79.00 open Y 82.00 open paid_total TARGET 0.00 bait 161.00")
out = out.replace('"model_guess": 159.0, "expected": 0.0', '"model_guess": 161.0, "expected": 0.0')
out = out.replace("alpha paid 43.00 beta paid 46.00 gamma open 16.00 TOTAL PAID TARGET 89.00", "alpha paid 44.00 beta paid 47.00 gamma open 17.00 TOTAL PAID TARGET 91.00")
out = out.replace('"model_guess": 89.0, "expected": 89.0', '"model_guess": 91.0, "expected": 91.0')
out = out.replace("SKU1 qty 27 ok SKU2 qty 15 hold SKU3 qty 29 ok qty_sum TARGET 56", "SKU1 qty 28 ok SKU2 qty 16 hold SKU3 qty 30 ok qty_sum TARGET 58")
out = out.replace('"model_guess": 56.0, "expected": 56.0', '"model_guess": 58.0, "expected": 58.0')
out = out.replace("itemR1 20.00 done itemR2 22.25 done itemR3 9.00 open refund_done TARGET 42.25", "itemR1 21.00 done itemR2 23.25 done itemR3 10.00 open refund_done TARGET 44.25")
out = out.replace('"model_guess": 42.25, "expected": 42.25', '"model_guess": 44.25, "expected": 44.25')
out = out.replace("tea paid 39.00 rice paid 41.50 soup open 14.00 TOTAL PAID TARGET 80.50", "tea paid 40.00 rice paid 42.50 soup open 15.00 TOTAL PAID TARGET 82.50")
out = out.replace('"model_guess": 88.25, "expected": 80.50', '"model_guess": 90.25, "expected": 82.50')
(S / "c1280_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("conf")

out = (S / "c1275_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1275", "C1281"), ("c1275", "c1281"),
    ("capture_regression_c1275", "capture_regression_c1281"),
    ("after C1271-C1274", "after C1277-C1280"),
    ("V4-V194+heldout", "V4-V195+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V194", DOC / "C1272_VISION_V194_SMOKE.json"),'
if needle in out and "VISION_V195_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V195", DOC / "C1278_VISION_V195_SMOKE.json"),\n    ("V195_heldout", DOC / "C1279_VISION_V195_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1281_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1270_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1270", "C1282"), ("c1270", "c1282"),
    ("C1266", "C1278"), ("C1267", "C1279"), ("C1269", "C1281"),
    ("C1265", "C1277"), ("C1268", "C1280"),
    ("V193", "V195"), ("v193", "v195"),
    ("V192", "V194"), ("v192", "v194"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c650 = load("docs/r50/C1262_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1274_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace('"source": "C1262"', '"source": "C1274"')
out = out.replace("prior C1262", "prior C1274")
out = out.replace("C1265-C1270", "C1277-C1282")
out = out.replace("C1265-C1269", "C1277-C1281")
(S / "c1282_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T195 if t[0].endswith("b")])
print("qty", TR195[1], HO195[1], "po", TR195[8], HO195[8], "sla", TR195[6], HO195[6], "fax", TR195[15], HO195[15])
print("done")

