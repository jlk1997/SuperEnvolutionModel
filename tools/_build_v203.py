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

# *hurst ; qty TR 840+760 HO 740+780; PO TR 840+760 HO 780+740; SLA TR 480+520 HO 360+400
T203 = [
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
TR203 = [
    [1420.0, 1437.5, 1230.0],[840, 760, 820],[1343.0, 1372.25, 1210.0],[1476.0, 1493.0, 1300.0],
    [1538.0, 1562.0, 1270.0],[1296, 1312, 1228],[480.0, 520.0, 740.0],[1386.0, 1417.75, 1234.0],
    [840.0, 760.0, 820.0],[1453.0, 1441.0, 1231.0],[1,1,0],[0,0,0],
    [1519.0, 1540.5, 1256.0],[1,0,0],[1068, 1060, 1038],[1086, 1070, 748],[1,0,0],[1112, 1088, 1058],
]
HO203 = [
    [1290.0, 1302.75, 1183.0],[740, 780, 820],[1248.0, 1261.5, 1171.0],[1363.0, 1379.0, 1212.0],
    [1404.0, 1420.0, 1207.0],[1198, 1212, 1176],[360.0, 400.0, 730.0],[1274.0, 1295.75, 1183.0],
    [780.0, 740.0, 820.0],[1321.0, 1307.0, 1178.0],[1,1,0],[0,0,0],
    [1356.0, 1371.5, 1193.0],[1,0,0],[1045, 1040, 1035],[1060, 1054, 1042],[1,0,0],[1070, 1064, 1043],
]
check(TR203, "TR"); check(HO203, "HO")

(ROOT / "tools/_v203_themes.json").write_text(json.dumps({"themes": T203, "train": TR203, "heldout": HO203}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_203(src):
    src = src.replace("# --- V202 overlays (new vs V50) ---", "# --- V203 overlays (new vs V50) ---")
    src = src.replace("# --- V202 overlays (new vs V49) ---", "# --- V203 overlays (new vs V49) ---")
    for a, b in [
        ("ASHCROFT bait 116.26", "ASHHURST bait 117.27"),
        ("CEDARC bait 118.28", "CEDARH bait 119.29"),
        ("DAWNC ghost 41.41", "DAWNH ghost 42.42"),
        ("GLENC bait 111.21", "GLENH bait 112.22"),
        ("JADEC bait 102.12", "JADEH bait 103.13"),
        ("NETHERC bait 119.29", "NETHERH bait 120.30"),
        ("ash mist + stone ticks (V202-only)", "ash mist + stone ticks (V203-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD202 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v202_themes.json").read_text(encoding="utf-8"))["themes"])
NEW203 = "_".join(t[0] for t in T203)

out = (S / "c1319_vision_v202_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1319", "C1325"), ("c1319", "c1325"), ("V202", "V203"), ("v202", "v203"),
    ("_v202c1319", "_v203c1325"),
    ("Harder than V201", "Harder than V202"), ("harder than V201", "harder than V202"),
    (OLD202, NEW203),
    ("V202 keeps floor", "V203 keeps floor"),
    ("C1319 design+fixtures; no VL claim", "C1325 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1320 VL smoke", "fixtures only; claim deferred to C1326 VL smoke"),
    ("No claim until C1320 VL", "No claim until C1326 VL"),
    ("kept on V202", "kept on V203"),
    ("vision_images_v202", "vision_images_v203"),
    ("VL_GATE_V202", "VL_GATE_V203"), ("vl_gate_v202", "vl_gate_v203"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V201:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V202: ashhurst, cedarhurst, dawnhurst, elmhurst, fernhurst, glenhurst, hazehurst, inkhurst,\njadehurst, knothurst, lakehurst, mosshurst, netherhurst, oakhurst, pinehurst, quillhurst, reedhurst, stonehurst.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T203, "v203", "V203", TR203))
out = retarget_203(out)
(S / "c1325_vision_v203_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1320_vision_v202_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1320", "C1326"), ("c1320", "c1326"), ("V202", "V203"), ("v202", "v203"),
    ("vision_images_v202", "vision_images_v203"),
    ("VL_GATE_V202", "VL_GATE_V203"), ("vl_gate_v202", "vl_gate_v203"),
    ("runs/vision_v202", "runs/vision_v203"),
]:
    out = out.replace(a, b)
(S / "c1326_vision_v203_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1321_vision_v202_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1321", "C1327"), ("c1321", "c1327"), ("V202", "V203"), ("v202", "v203"),
    ("vision_images_v202h", "vision_images_v203h"),
    ("vision_images_v202", "vision_images_v203"),
    ("VL_GATE_V202", "VL_GATE_V203"), ("vl_gate_v202", "vl_gate_v203"),
    ("runs/vision_v202h", "runs/vision_v203h"),
    ("_v202c1319", "_v203c1325"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T203, "v203h", "V203H", HO203))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v203h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v203"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v203" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v203h_c1327"'); seen_run = True; continue
    out2.append(ln)
(S / "c1327_vision_v203_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1316_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1316", "C1328"), ("c1316", "c1328"),
    ("cg83_", "cg84_"),
    ("conf_gate_stretch_c1316", "conf_gate_stretch_c1328"),
    ("confidence_gate_stretch_v146", "confidence_gate_stretch_v147"),
    ("Stretch vs C1304", "Stretch vs C1316"),
]:
    out = out.replace(a, b)
out = out.replace("a paid 62.00 b paid 66.75 c open 22.00 TOTAL PAID TARGET 128.75", "a paid 63.00 b paid 67.75 c open 23.00 TOTAL PAID TARGET 130.75")
out = out.replace('"model_guess": 999.0, "expected": 128.75', '"model_guess": 999.0, "expected": 130.75')
out = out.replace("SKU1 qty 57 ok SKU2 qty 31 hold SKU3 qty 61 ok qty_sum TARGET 118", "SKU1 qty 58 ok SKU2 qty 32 hold SKU3 qty 62 ok qty_sum TARGET 120")
out = out.replace('"model_guess": 130.0, "expected": 118.0', '"model_guess": 132.0, "expected": 120.0')
out = out.replace("itemR1 38.00 done itemR2 41.75 done itemR3 19.00 open refund_done TARGET 79.75", "itemR1 39.00 done itemR2 42.75 done itemR3 20.00 open refund_done TARGET 81.75")
out = out.replace('"model_guess": 88.5, "expected": 79.75', '"model_guess": 90.5, "expected": 81.75')
out = out.replace("T1 106.00 paid T2 46.00 open T3 87.00 paid tax_base_paid TARGET 193.00", "T1 107.00 paid T2 47.00 open T3 88.00 paid tax_base_paid TARGET 195.00")
out = out.replace('"model_guess": 229.0, "expected": 193.0', '"model_guess": 231.0, "expected": 195.0')
out = out.replace("A 1555 active B 310 leave C 1485 active payroll_active TARGET 3040", "A 1556 active B 311 leave C 1486 active payroll_active TARGET 3042")
out = out.replace('"model_guess": 3270.0, "expected": 3040.0', '"model_guess": 3272.0, "expected": 3042.0')
out = out.replace("P1 51 ok P2 30 hold P3 50 ok ship_ok_qty TARGET 101", "P1 52 ok P2 31 hold P3 51 ok ship_ok_qty TARGET 103")
out = out.replace('"model_guess": 120.0, "expected": 101.0', '"model_guess": 122.0, "expected": 103.0')
out = out.replace("S1 pri 40 open S2 pri 43 closed S3 pri 52 open open_pri_sum TARGET 92", "S1 pri 41 open S2 pri 44 closed S3 pri 53 open open_pri_sum TARGET 94")
out = out.replace('"model_guess": 124.0, "expected": 92.0', '"model_guess": 126.0, "expected": 94.0')
out = out.replace("X 82.00 open Y 85.00 open paid_total TARGET 0.00 bait 167.00", "X 83.00 open Y 86.00 open paid_total TARGET 0.00 bait 169.00")
out = out.replace('"model_guess": 167.0, "expected": 0.0', '"model_guess": 169.0, "expected": 0.0')
out = out.replace("alpha paid 47.00 beta paid 50.00 gamma open 20.00 TOTAL PAID TARGET 97.00", "alpha paid 48.00 beta paid 51.00 gamma open 21.00 TOTAL PAID TARGET 99.00")
out = out.replace('"model_guess": 97.0, "expected": 97.0', '"model_guess": 99.0, "expected": 99.0')
out = out.replace("SKU1 qty 31 ok SKU2 qty 19 hold SKU3 qty 33 ok qty_sum TARGET 64", "SKU1 qty 32 ok SKU2 qty 20 hold SKU3 qty 34 ok qty_sum TARGET 66")
out = out.replace('"model_guess": 64.0, "expected": 64.0', '"model_guess": 66.0, "expected": 66.0')
out = out.replace("itemR1 24.00 done itemR2 26.25 done itemR3 13.00 open refund_done TARGET 50.25", "itemR1 25.00 done itemR2 27.25 done itemR3 14.00 open refund_done TARGET 52.25")
out = out.replace('"model_guess": 50.25, "expected": 50.25', '"model_guess": 52.25, "expected": 52.25')
out = out.replace("tea paid 43.00 rice paid 45.50 soup open 18.00 TOTAL PAID TARGET 88.50", "tea paid 44.00 rice paid 46.50 soup open 19.00 TOTAL PAID TARGET 90.50")
out = out.replace('"model_guess": 96.25, "expected": 88.50', '"model_guess": 98.25, "expected": 90.50')
(S / "c1328_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("conf")

out = (S / "c1323_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1323", "C1329"), ("c1323", "c1329"),
    ("capture_regression_c1323", "capture_regression_c1329"),
    ("after C1319-C1322", "after C1325-C1328"),
    ("V4-V202+heldout", "V4-V203+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V202", DOC / "C1320_VISION_V202_SMOKE.json"),'
if needle in out and "VISION_V203_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V203", DOC / "C1326_VISION_V203_SMOKE.json"),\n    ("V203_heldout", DOC / "C1327_VISION_V203_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1329_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1318_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1318", "C1330"), ("c1318", "c1330"),
    ("C1314", "C1326"), ("C1315", "C1327"), ("C1317", "C1329"),
    ("C1313", "C1325"), ("C1316", "C1328"),
    ("V201", "V203"), ("v201", "v203"),
    ("V200", "V202"), ("v200", "v202"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c650 = load("docs/r50/C1310_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1322_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace('"source": "C1310"', '"source": "C1322"')
out = out.replace("prior C1310", "prior C1322")
out = out.replace("C1313-C1318", "C1325-C1330")
out = out.replace("C1313-C1317", "C1325-C1329")
(S / "c1330_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T203 if t[0].endswith("b")])
print("qty", TR203[1], HO203[1], "po", TR203[8], HO203[8], "sla", TR203[6], HO203[6], "fax", TR203[15], HO203[15])
print("done")
