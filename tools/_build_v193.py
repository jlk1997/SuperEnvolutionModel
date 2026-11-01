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

# *moor ; qty TR 840+760 HO 740+780; PO TR 840+760 HO 780+740; SLA TR 480+520 HO 360+400
T193 = [
    ["ashmoor","recv","paid_total","ASHMOOR GRAIN RECV","RECV","x"],
    ["cedarmoor","wh","qty_sum","WH CEDARMOOR BIN","RECV","x"],
    ["dawnmoor","refund","refund_done","DAWNMOOR PATCH REFUND","DONE","x"],
    ["elmmoor","tax","tax_base_paid","ELMMOOR TAX SLIP","TAX","x"],
    ["fernmoor","pay","payroll_active","FERNMOOR PAYROLL","PAY","x"],
    ["glenmoor","ship","ship_ok","GLENMOOR SHIP DOCK","SHIP","x"],
    ["hazemoor","sla","sla_ok_hours","HAZEMOOR SLA CARD","SLA","x"],
    ["inkmoor","exp","exp_sum","INKMOOR EXPENSE","EXP","x"],
    ["jademoor","po","po_open","JADEMOOR PO SHEET","PO","x"],
    ["knotmoor","order","order_paid","KNOTMOOR ORDER","ORD","x"],
    ["lakemoor","dup","dup_mark","LAKEMOOR DUP MARK","DUP","x"],
    ["mossmoor","zero","zero_check","MOSSMOOR AIR ZERO","ZERO","x"],
    ["nethermoor","ledger","ledger_net","NETHERMOOR LEDGER","LED","x"],
    ["oakmoor","ui","ui_ok","OAKMOOR UI SCAN","UI","x"],
    ["pinemoor","stack","stack_count","PINEMOOR STACK","STK","x"],
    ["quillmoor","fax","fax_pages","QUILLMOOR FAX","FAX","x"],
    ["reedmoor","glare","glare_ok","REEDMOOR GLARE","GLR","x"],
    ["stonemoor","tab","tab_index","STONEMOOR TAB INDEX","TAB","x"],
]
TR193 = [
    [1330.0, 1347.5, 1140.0],[840, 760, 820],[1253.0, 1282.25, 1120.0],[1386.0, 1403.0, 1210.0],
    [1448.0, 1472.0, 1180.0],[1206, 1222, 1138],[480.0, 520.0, 730.0],[1296.0, 1327.75, 1144.0],
    [840.0, 760.0, 820.0],[1363.0, 1351.0, 1141.0],[1,1,0],[0,0,0],
    [1429.0, 1450.5, 1166.0],[1,0,0],[978, 970, 948],[996, 980, 748],[1,0,0],[1022, 998, 968],
]
HO193 = [
    [1200.0, 1212.75, 1093.0],[740, 780, 820],[1158.0, 1171.5, 1081.0],[1273.0, 1289.0, 1122.0],
    [1314.0, 1330.0, 1117.0],[1108, 1122, 1086],[360.0, 400.0, 670.0],[1184.0, 1205.75, 1093.0],
    [780.0, 740.0, 820.0],[1231.0, 1217.0, 1088.0],[1,1,0],[0,0,0],
    [1266.0, 1281.5, 1103.0],[1,0,0],[955, 950, 945],[970, 964, 952],[1,0,0],[980, 974, 953],
]
check(TR193, "TR"); check(HO193, "HO")

(ROOT / "tools/_v193_themes.json").write_text(json.dumps({"themes": T193, "train": TR193, "heldout": HO193}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_193(src):
    src = src.replace("# --- V192 overlays (new vs V50) ---", "# --- V193 overlays (new vs V50) ---")
    src = src.replace("# --- V192 overlays (new vs V49) ---", "# --- V193 overlays (new vs V49) ---")
    for a, b in [
        ("ASHHURST bait 106.16", "ASHMOOR bait 107.17"),
        ("CEDARH bait 108.18", "CEDARM bait 109.19"),
        ("DAWNH ghost 31.31", "DAWNM ghost 32.32"),
        ("GLENH bait 101.11", "GLENM bait 102.12"),
        ("JADEH bait 92.92", "JADEM bait 93.93"),
        ("NETHERH bait 109.19", "NETHERM bait 110.20"),
        ("ash mist + stone ticks (V192-only)", "ash mist + stone ticks (V193-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD192 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v192_themes.json").read_text(encoding="utf-8"))["themes"])
NEW193 = "_".join(t[0] for t in T193)

out = (S / "c1259_vision_v192_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1259", "C1265"), ("c1259", "c1265"), ("V192", "V193"), ("v192", "v193"),
    ("_v192c1259", "_v193c1265"),
    ("Harder than V191", "Harder than V192"), ("harder than V191", "harder than V192"),
    (OLD192, NEW193),
    ("V192 keeps floor", "V193 keeps floor"),
    ("C1259 design+fixtures; no VL claim", "C1265 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1260 VL smoke", "fixtures only; claim deferred to C1266 VL smoke"),
    ("No claim until C1260 VL", "No claim until C1266 VL"),
    ("kept on V192", "kept on V193"),
    ("vision_images_v192", "vision_images_v193"),
    ("VL_GATE_V192", "VL_GATE_V193"), ("vl_gate_v192", "vl_gate_v193"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V191:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V192: ashmoor, cedarmoor, dawnmoor, elmmoor, fernmoor, glenmoor, hazemoor, inkmoor,\njademoor, knotmoor, lakemoor, mossmoor, nethermoor, oakmoor, pinemoor, quillmoor, reedmoor, stonemoor.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T193, "v193", "V193", TR193))
out = retarget_193(out)
(S / "c1265_vision_v193_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1260_vision_v192_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1260", "C1266"), ("c1260", "c1266"), ("V192", "V193"), ("v192", "v193"),
    ("vision_images_v192", "vision_images_v193"),
    ("VL_GATE_V192", "VL_GATE_V193"), ("vl_gate_v192", "vl_gate_v193"),
    ("runs/vision_v192", "runs/vision_v193"),
]:
    out = out.replace(a, b)
(S / "c1266_vision_v193_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1261_vision_v192_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1261", "C1267"), ("c1261", "c1267"), ("V192", "V193"), ("v192", "v193"),
    ("vision_images_v192h", "vision_images_v193h"),
    ("vision_images_v192", "vision_images_v193"),
    ("VL_GATE_V192", "VL_GATE_V193"), ("vl_gate_v192", "vl_gate_v193"),
    ("runs/vision_v192h", "runs/vision_v193h"),
    ("_v192c1259", "_v193c1265"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T193, "v193h", "V193H", HO193))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v193h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v193"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v193" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v193h_c1267"'); seen_run = True; continue
    out2.append(ln)
(S / "c1267_vision_v193_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# confidence-gate stretch from C1256
out = (S / "c1256_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1256", "C1268"), ("c1256", "c1268"),
    ("cg78_", "cg79_"),
    ("conf_gate_stretch_c1256", "conf_gate_stretch_c1268"),
    ("confidence_gate_stretch_v141", "confidence_gate_stretch_v142"),
    ("Stretch vs C210", "Stretch vs C1256"),
]:
    out = out.replace(a, b)
# nudge amounts slightly so cases are distinct
out = out.replace("a paid 57.00 b paid 61.75 c open 17.00 TOTAL PAID TARGET 118.75", "a paid 58.00 b paid 62.75 c open 18.00 TOTAL PAID TARGET 120.75")
out = out.replace('"model_guess": 999.0, "expected": 118.75', '"model_guess": 999.0, "expected": 120.75')
out = out.replace("SKU1 qty 52 ok SKU2 qty 26 hold SKU3 qty 56 ok qty_sum TARGET 108", "SKU1 qty 53 ok SKU2 qty 27 hold SKU3 qty 57 ok qty_sum TARGET 110")
out = out.replace('"model_guess": 120.0, "expected": 108.0', '"model_guess": 122.0, "expected": 110.0')
out = out.replace("itemR1 33.00 done itemR2 36.75 done itemR3 14.00 open refund_done TARGET 69.75", "itemR1 34.00 done itemR2 37.75 done itemR3 15.00 open refund_done TARGET 71.75")
out = out.replace('"model_guess": 78.5, "expected": 69.75', '"model_guess": 80.5, "expected": 71.75')
out = out.replace("T1 101.00 paid T2 41.00 open T3 82.00 paid tax_base_paid TARGET 183.00", "T1 102.00 paid T2 42.00 open T3 83.00 paid tax_base_paid TARGET 185.00")
out = out.replace('"model_guess": 219.0, "expected": 183.0', '"model_guess": 221.0, "expected": 185.0')
out = out.replace("A 1550 active B 305 leave C 1480 active payroll_active TARGET 3030", "A 1551 active B 306 leave C 1481 active payroll_active TARGET 3032")
out = out.replace('"model_guess": 3260.0, "expected": 3030.0', '"model_guess": 3262.0, "expected": 3032.0')
out = out.replace("P1 46 ok P2 25 hold P3 45 ok ship_ok_qty TARGET 91", "P1 47 ok P2 26 hold P3 46 ok ship_ok_qty TARGET 93")
out = out.replace('"model_guess": 110.0, "expected": 91.0', '"model_guess": 112.0, "expected": 93.0')
out = out.replace("S1 pri 35 open S2 pri 38 closed S3 pri 47 open open_pri_sum TARGET 82", "S1 pri 36 open S2 pri 39 closed S3 pri 48 open open_pri_sum TARGET 84")
out = out.replace('"model_guess": 114.0, "expected": 82.0', '"model_guess": 116.0, "expected": 84.0')
out = out.replace("X 77.00 open Y 80.00 open paid_total TARGET 0.00 bait 157.00", "X 78.00 open Y 81.00 open paid_total TARGET 0.00 bait 159.00")
out = out.replace('"model_guess": 157.0, "expected": 0.0', '"model_guess": 159.0, "expected": 0.0')
out = out.replace("alpha paid 42.00 beta paid 45.00 gamma open 15.00 TOTAL PAID TARGET 87.00", "alpha paid 43.00 beta paid 46.00 gamma open 16.00 TOTAL PAID TARGET 89.00")
out = out.replace('"model_guess": 87.0, "expected": 87.0', '"model_guess": 89.0, "expected": 89.0')
out = out.replace("SKU1 qty 26 ok SKU2 qty 14 hold SKU3 qty 28 ok qty_sum TARGET 54", "SKU1 qty 27 ok SKU2 qty 15 hold SKU3 qty 29 ok qty_sum TARGET 56")
out = out.replace('"model_guess": 54.0, "expected": 54.0', '"model_guess": 56.0, "expected": 56.0')
out = out.replace("itemR1 19.00 done itemR2 21.25 done itemR3 8.00 open refund_done TARGET 40.25", "itemR1 20.00 done itemR2 22.25 done itemR3 9.00 open refund_done TARGET 42.25")
out = out.replace('"model_guess": 40.25, "expected": 40.25', '"model_guess": 42.25, "expected": 42.25')
out = out.replace("tea paid 38.00 rice paid 40.50 soup open 13.00 TOTAL PAID TARGET 78.50", "tea paid 39.00 rice paid 41.50 soup open 14.00 TOTAL PAID TARGET 80.50")
out = out.replace('"model_guess": 86.25, "expected": 78.50', '"model_guess": 88.25, "expected": 80.50')
(S / "c1268_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("conf")

out = (S / "c1263_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1263", "C1269"), ("c1263", "c1269"),
    ("capture_regression_c1263", "capture_regression_c1269"),
    ("after C1259-C1262", "after C1265-C1268"),
    ("V4-V192+heldout", "V4-V193+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V192", DOC / "C1260_VISION_V192_SMOKE.json"),'
if needle in out and "VISION_V193_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V193", DOC / "C1266_VISION_V193_SMOKE.json"),\n    ("V193_heldout", DOC / "C1267_VISION_V193_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1269_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

# scorecard from C1258 (confidence-gate knife pattern)
out = (S / "c1258_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1258", "C1270"), ("c1258", "c1270"),
    ("C1254", "C1266"), ("C1255", "C1267"), ("C1257", "C1269"),
    ("C1253", "C1265"), ("C1256", "C1268"),
    ("V191", "V193"), ("v191", "v193"),
    ("V190", "V192"), ("v190", "v192"),
]:
    out = out.replace(a, b)
# prior u2c from C1262
out = out.replace(
    'c650 = load("docs/r50/C1250_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1262_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace('"source": "C1250"', '"source": "C1262"')
out = out.replace("prior C1250", "prior C1262")
out = out.replace("C1253-C1258", "C1265-C1270")
out = out.replace("C1253-C1257", "C1265-C1269")
(S / "c1270_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T193 if t[0].endswith("b")])
print("qty", TR193[1], HO193[1], "po", TR193[8], HO193[8], "sla", TR193[6], HO193[6], "fax", TR193[15], HO193[15])
print("done")
