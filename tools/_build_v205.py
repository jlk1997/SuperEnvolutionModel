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

# *fen ; qty TR 840+760 HO 740+780; PO TR 840+760 HO 780+740; SLA TR 480+520 HO 360+400
T205 = [
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
TR205 = [
    [1438.0, 1455.5, 1248.0],[840, 760, 820],[1361.0, 1390.25, 1228.0],[1494.0, 1511.0, 1318.0],
    [1556.0, 1580.0, 1288.0],[1314, 1330, 1246],[480.0, 520.0, 720.0],[1404.0, 1435.75, 1252.0],
    [840.0, 760.0, 820.0],[1471.0, 1459.0, 1249.0],[1,1,0],[0,0,0],
    [1537.0, 1558.5, 1274.0],[1,0,0],[1086, 1078, 1056],[1104, 1088, 748],[1,0,0],[1130, 1106, 1076],
]
HO205 = [
    [1308.0, 1320.75, 1201.0],[740, 780, 820],[1266.0, 1279.5, 1189.0],[1381.0, 1397.0, 1230.0],
    [1422.0, 1438.0, 1225.0],[1216, 1230, 1194],[360.0, 400.0, 710.0],[1292.0, 1313.75, 1201.0],
    [780.0, 740.0, 820.0],[1339.0, 1325.0, 1196.0],[1,1,0],[0,0,0],
    [1374.0, 1389.5, 1211.0],[1,0,0],[1063, 1058, 1053],[1078, 1072, 1060],[1,0,0],[1088, 1082, 1061],
]
check(TR205, "TR"); check(HO205, "HO")

(ROOT / "tools/_v205_themes.json").write_text(json.dumps({"themes": T205, "train": TR205, "heldout": HO205}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_205(src):
    src = src.replace("# --- V204 overlays (new vs V50) ---", "# --- V205 overlays (new vs V50) ---")
    src = src.replace("# --- V204 overlays (new vs V49) ---", "# --- V205 overlays (new vs V49) ---")
    for a, b in [
        ("ASHMOOR bait 118.28", "ASHFEN bait 119.29"),
        ("CEDARM bait 120.30", "CEDARF bait 121.31"),
        ("DAWNM ghost 43.43", "DAWNF ghost 44.44"),
        ("GLENM bait 113.23", "GLENF bait 114.24"),
        ("JADEM bait 104.14", "JADEF bait 105.15"),
        ("NETHERM bait 121.31", "NETHERF bait 122.32"),
        ("ash mist + stone ticks (V204-only)", "ash mist + stone ticks (V205-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD204 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v204_themes.json").read_text(encoding="utf-8"))["themes"])
NEW205 = "_".join(t[0] for t in T205)

out = (S / "c1331_vision_v204_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1331", "C1337"), ("c1331", "c1337"), ("V204", "V205"), ("v204", "v205"),
    ("_v204c1331", "_v205c1337"),
    ("Harder than V203", "Harder than V204"), ("harder than V203", "harder than V204"),
    (OLD204, NEW205),
    ("V204 keeps floor", "V205 keeps floor"),
    ("C1331 design+fixtures; no VL claim", "C1337 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1332 VL smoke", "fixtures only; claim deferred to C1338 VL smoke"),
    ("No claim until C1332 VL", "No claim until C1338 VL"),
    ("kept on V204", "kept on V205"),
    ("vision_images_v204", "vision_images_v205"),
    ("VL_GATE_V204", "VL_GATE_V205"), ("vl_gate_v204", "vl_gate_v205"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V203:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V204: ashfen, cedarfen, dawnfen, elmfen, fernfen, glenfen, hazefen, inkfen,\njadefen, knotfen, lakefen, mossfen, netherfen, oakfen, pinefen, quillfen, reedfen, stonefen.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T205, "v205", "V205", TR205))
out = retarget_205(out)
(S / "c1337_vision_v205_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1332_vision_v204_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1332", "C1338"), ("c1332", "c1338"), ("V204", "V205"), ("v204", "v205"),
    ("vision_images_v204", "vision_images_v205"),
    ("VL_GATE_V204", "VL_GATE_V205"), ("vl_gate_v204", "vl_gate_v205"),
    ("runs/vision_v204", "runs/vision_v205"),
]:
    out = out.replace(a, b)
(S / "c1338_vision_v205_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1333_vision_v204_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1333", "C1339"), ("c1333", "c1339"), ("V204", "V205"), ("v204", "v205"),
    ("vision_images_v204h", "vision_images_v205h"),
    ("vision_images_v204", "vision_images_v205"),
    ("VL_GATE_V204", "VL_GATE_V205"), ("vl_gate_v204", "vl_gate_v205"),
    ("runs/vision_v204h", "runs/vision_v205h"),
    ("_v204c1331", "_v205c1337"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T205, "v205h", "V205H", HO205))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v205h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v205"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v205" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v205h_c1339"'); seen_run = True; continue
    out2.append(ln)
(S / "c1339_vision_v205_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1328_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1328", "C1340"), ("c1328", "c1340"),
    ("cg84_", "cg85_"),
    ("conf_gate_stretch_c1328", "conf_gate_stretch_c1340"),
    ("confidence_gate_stretch_v147", "confidence_gate_stretch_v148"),
    ("Stretch vs C1316", "Stretch vs C1328"),
]:
    out = out.replace(a, b)
out = out.replace("a paid 63.00 b paid 67.75 c open 23.00 TOTAL PAID TARGET 130.75", "a paid 64.00 b paid 68.75 c open 24.00 TOTAL PAID TARGET 132.75")
out = out.replace('"model_guess": 999.0, "expected": 130.75', '"model_guess": 999.0, "expected": 132.75')
out = out.replace("SKU1 qty 58 ok SKU2 qty 32 hold SKU3 qty 62 ok qty_sum TARGET 120", "SKU1 qty 59 ok SKU2 qty 33 hold SKU3 qty 63 ok qty_sum TARGET 122")
out = out.replace('"model_guess": 132.0, "expected": 120.0', '"model_guess": 134.0, "expected": 122.0')
out = out.replace("itemR1 39.00 done itemR2 42.75 done itemR3 20.00 open refund_done TARGET 81.75", "itemR1 40.00 done itemR2 43.75 done itemR3 21.00 open refund_done TARGET 83.75")
out = out.replace('"model_guess": 90.5, "expected": 81.75', '"model_guess": 92.5, "expected": 83.75')
out = out.replace("T1 107.00 paid T2 47.00 open T3 88.00 paid tax_base_paid TARGET 195.00", "T1 108.00 paid T2 48.00 open T3 89.00 paid tax_base_paid TARGET 197.00")
out = out.replace('"model_guess": 231.0, "expected": 195.0', '"model_guess": 233.0, "expected": 197.0')
out = out.replace("A 1556 active B 311 leave C 1486 active payroll_active TARGET 3042", "A 1557 active B 312 leave C 1487 active payroll_active TARGET 3044")
out = out.replace('"model_guess": 3272.0, "expected": 3042.0', '"model_guess": 3274.0, "expected": 3044.0')
out = out.replace("P1 52 ok P2 31 hold P3 51 ok ship_ok_qty TARGET 103", "P1 53 ok P2 32 hold P3 52 ok ship_ok_qty TARGET 105")
out = out.replace('"model_guess": 122.0, "expected": 103.0', '"model_guess": 124.0, "expected": 105.0')
out = out.replace("S1 pri 41 open S2 pri 44 closed S3 pri 53 open open_pri_sum TARGET 94", "S1 pri 42 open S2 pri 45 closed S3 pri 54 open open_pri_sum TARGET 96")
out = out.replace('"model_guess": 126.0, "expected": 94.0', '"model_guess": 128.0, "expected": 96.0')
out = out.replace("X 83.00 open Y 86.00 open paid_total TARGET 0.00 bait 169.00", "X 84.00 open Y 87.00 open paid_total TARGET 0.00 bait 171.00")
out = out.replace('"model_guess": 169.0, "expected": 0.0', '"model_guess": 171.0, "expected": 0.0')
out = out.replace("alpha paid 48.00 beta paid 51.00 gamma open 21.00 TOTAL PAID TARGET 99.00", "alpha paid 49.00 beta paid 52.00 gamma open 22.00 TOTAL PAID TARGET 101.00")
out = out.replace('"model_guess": 99.0, "expected": 99.0', '"model_guess": 101.0, "expected": 101.0')
out = out.replace("SKU1 qty 32 ok SKU2 qty 20 hold SKU3 qty 34 ok qty_sum TARGET 66", "SKU1 qty 33 ok SKU2 qty 21 hold SKU3 qty 35 ok qty_sum TARGET 68")
out = out.replace('"model_guess": 66.0, "expected": 66.0', '"model_guess": 68.0, "expected": 68.0')
out = out.replace("itemR1 25.00 done itemR2 27.25 done itemR3 14.00 open refund_done TARGET 52.25", "itemR1 26.00 done itemR2 28.25 done itemR3 15.00 open refund_done TARGET 54.25")
out = out.replace('"model_guess": 52.25, "expected": 52.25', '"model_guess": 54.25, "expected": 54.25')
out = out.replace("tea paid 44.00 rice paid 46.50 soup open 19.00 TOTAL PAID TARGET 90.50", "tea paid 45.00 rice paid 47.50 soup open 20.00 TOTAL PAID TARGET 92.50")
out = out.replace('"model_guess": 98.25, "expected": 90.50', '"model_guess": 100.25, "expected": 92.50')
(S / "c1340_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("conf")

out = (S / "c1335_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1335", "C1341"), ("c1335", "c1341"),
    ("capture_regression_c1335", "capture_regression_c1341"),
    ("after C1331-C1334", "after C1337-C1340"),
    ("V4-V204+heldout", "V4-V205+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V204", DOC / "C1332_VISION_V204_SMOKE.json"),'
if needle in out and "VISION_V205_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V205", DOC / "C1338_VISION_V205_SMOKE.json"),\n    ("V205_heldout", DOC / "C1339_VISION_V205_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1341_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1330_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1330", "C1342"), ("c1330", "c1342"),
    ("C1326", "C1338"), ("C1327", "C1339"), ("C1329", "C1341"),
    ("C1325", "C1337"), ("C1328", "C1340"),
    ("V203", "V205"), ("v203", "v205"),
    ("V202", "V204"), ("v202", "v204"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c650 = load("docs/r50/C1322_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1334_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace('"source": "C1322"', '"source": "C1334"')
out = out.replace("prior C1322", "prior C1334")
out = out.replace("C1325-C1330", "C1337-C1342")
out = out.replace("C1325-C1329", "C1337-C1341")
(S / "c1342_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T205 if t[0].endswith("b")])
print("qty", TR205[1], HO205[1], "po", TR205[8], HO205[8], "sla", TR205[6], HO205[6], "fax", TR205[15], HO205[15])
print("done")
