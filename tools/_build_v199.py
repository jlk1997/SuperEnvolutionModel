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

# *holm ; qty TR 840+760 HO 740+780; PO TR 840+760 HO 780+740; SLA TR 480+520 HO 360+400
T199 = [
    ["ashholm","recv","paid_total","ASHHOLM GRAIN RECV","RECV","x"],
    ["cedarholm","wh","qty_sum","WH CEDARHOLM BIN","RECV","x"],
    ["dawnholm","refund","refund_done","DAWNHOLM PATCH REFUND","DONE","x"],
    ["elmholm","tax","tax_base_paid","ELMHOLM TAX SLIP","TAX","x"],
    ["fernholm","pay","payroll_active","FERNHOLM PAYROLL","PAY","x"],
    ["glenholm","ship","ship_ok","GLENHOLM SHIP DOCK","SHIP","x"],
    ["hazeholm","sla","sla_ok_hours","HAZEHOLM SLA CARD","SLA","x"],
    ["inkholm","exp","exp_sum","INKHOLM EXPENSE","EXP","x"],
    ["jadeholm","po","po_open","JADEHOLM PO SHEET","PO","x"],
    ["knotholm","order","order_paid","KNOTHOLM ORDER","ORD","x"],
    ["lakeholm","dup","dup_mark","LAKEHOLM DUP MARK","DUP","x"],
    ["mossholm","zero","zero_check","MOSSHOLM AIR ZERO","ZERO","x"],
    ["netherholm","ledger","ledger_net","NETHERHOLM LEDGER","LED","x"],
    ["oakholm","ui","ui_ok","OAKHOLM UI SCAN","UI","x"],
    ["pineholm","stack","stack_count","PINEHOLM STACK","STK","x"],
    ["quillholm","fax","fax_pages","QUILLHOLM FAX","FAX","x"],
    ["reedholm","glare","glare_ok","REEDHOLM GLARE","GLR","x"],
    ["stoneholm","tab","tab_index","STONEHOLM TAB INDEX","TAB","x"],
]
TR199 = [
    [1384.0, 1401.5, 1194.0],[840, 760, 820],[1307.0, 1336.25, 1174.0],[1440.0, 1457.0, 1264.0],
    [1502.0, 1526.0, 1234.0],[1260, 1276, 1192],[480.0, 520.0, 740.0],[1350.0, 1381.75, 1198.0],
    [840.0, 760.0, 820.0],[1417.0, 1405.0, 1195.0],[1,1,0],[0,0,0],
    [1483.0, 1504.5, 1220.0],[1,0,0],[1032, 1024, 1002],[1050, 1034, 748],[1,0,0],[1076, 1052, 1022],
]
HO199 = [
    [1254.0, 1266.75, 1147.0],[740, 780, 820],[1212.0, 1225.5, 1135.0],[1327.0, 1343.0, 1176.0],
    [1368.0, 1384.0, 1171.0],[1162, 1176, 1140],[360.0, 400.0, 730.0],[1238.0, 1259.75, 1147.0],
    [780.0, 740.0, 820.0],[1285.0, 1271.0, 1142.0],[1,1,0],[0,0,0],
    [1320.0, 1335.5, 1157.0],[1,0,0],[1009, 1004, 999],[1024, 1018, 1006],[1,0,0],[1034, 1028, 1007],
]
check(TR199, "TR"); check(HO199, "HO")

(ROOT / "tools/_v199_themes.json").write_text(json.dumps({"themes": T199, "train": TR199, "heldout": HO199}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_199(src):
    src = src.replace("# --- V198 overlays (new vs V50) ---", "# --- V199 overlays (new vs V50) ---")
    src = src.replace("# --- V198 overlays (new vs V49) ---", "# --- V199 overlays (new vs V49) ---")
    for a, b in [
        ("ASHFORD bait 112.22", "ASHHOLM bait 113.23"),
        ("CEDARF bait 114.24", "CEDARH bait 115.25"),
        ("DAWNF ghost 37.37", "DAWNH ghost 38.38"),
        ("GLENF bait 107.17", "GLENH bait 108.18"),
        ("JADEF bait 98.98", "JADEH bait 99.99"),
        ("NETHERF bait 115.25", "NETHERH bait 116.26"),
        ("ash mist + stone ticks (V198-only)", "ash mist + stone ticks (V199-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD198 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v198_themes.json").read_text(encoding="utf-8"))["themes"])
NEW199 = "_".join(t[0] for t in T199)

out = (S / "c1295_vision_v198_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1295", "C1301"), ("c1295", "c1301"), ("V198", "V199"), ("v198", "v199"),
    ("_v198c1295", "_v199c1301"),
    ("Harder than V197", "Harder than V198"), ("harder than V197", "harder than V198"),
    (OLD198, NEW199),
    ("V198 keeps floor", "V199 keeps floor"),
    ("C1295 design+fixtures; no VL claim", "C1301 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1296 VL smoke", "fixtures only; claim deferred to C1302 VL smoke"),
    ("No claim until C1296 VL", "No claim until C1302 VL"),
    ("kept on V198", "kept on V199"),
    ("vision_images_v198", "vision_images_v199"),
    ("VL_GATE_V198", "VL_GATE_V199"), ("vl_gate_v198", "vl_gate_v199"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V197:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V198: ashhholm, cedarholm, dawnholm, elmholm, fernholm, glenholm, hazeholm, inkholm,\njadeholm, knotholm, lakeholm, mossholm, netherholm, oakholm, pineholm, quillholm, reedholm, stoneholm.".replace("ashhholm", "ashholm"),
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T199, "v199", "V199", TR199))
out = retarget_199(out)
(S / "c1301_vision_v199_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1296_vision_v198_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1296", "C1302"), ("c1296", "c1302"), ("V198", "V199"), ("v198", "v199"),
    ("vision_images_v198", "vision_images_v199"),
    ("VL_GATE_V198", "VL_GATE_V199"), ("vl_gate_v198", "vl_gate_v199"),
    ("runs/vision_v198", "runs/vision_v199"),
]:
    out = out.replace(a, b)
(S / "c1302_vision_v199_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1297_vision_v198_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1297", "C1303"), ("c1297", "c1303"), ("V198", "V199"), ("v198", "v199"),
    ("vision_images_v198h", "vision_images_v199h"),
    ("vision_images_v198", "vision_images_v199"),
    ("VL_GATE_V198", "VL_GATE_V199"), ("vl_gate_v198", "vl_gate_v199"),
    ("runs/vision_v198h", "runs/vision_v199h"),
    ("_v198c1295", "_v199c1301"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T199, "v199h", "V199H", HO199))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v199h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v199"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v199" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v199h_c1303"'); seen_run = True; continue
    out2.append(ln)
(S / "c1303_vision_v199_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1292_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1292", "C1304"), ("c1292", "c1304"),
    ("cg81_", "cg82_"),
    ("conf_gate_stretch_c1292", "conf_gate_stretch_c1304"),
    ("confidence_gate_stretch_v144", "confidence_gate_stretch_v145"),
    ("Stretch vs C1280", "Stretch vs C1292"),
]:
    out = out.replace(a, b)
out = out.replace("a paid 60.00 b paid 64.75 c open 20.00 TOTAL PAID TARGET 124.75", "a paid 61.00 b paid 65.75 c open 21.00 TOTAL PAID TARGET 126.75")
out = out.replace('"model_guess": 999.0, "expected": 124.75', '"model_guess": 999.0, "expected": 126.75')
out = out.replace("SKU1 qty 55 ok SKU2 qty 29 hold SKU3 qty 59 ok qty_sum TARGET 114", "SKU1 qty 56 ok SKU2 qty 30 hold SKU3 qty 60 ok qty_sum TARGET 116")
out = out.replace('"model_guess": 126.0, "expected": 114.0', '"model_guess": 128.0, "expected": 116.0')
out = out.replace("itemR1 36.00 done itemR2 39.75 done itemR3 17.00 open refund_done TARGET 75.75", "itemR1 37.00 done itemR2 40.75 done itemR3 18.00 open refund_done TARGET 77.75")
out = out.replace('"model_guess": 84.5, "expected": 75.75', '"model_guess": 86.5, "expected": 77.75')
out = out.replace("T1 104.00 paid T2 44.00 open T3 85.00 paid tax_base_paid TARGET 189.00", "T1 105.00 paid T2 45.00 open T3 86.00 paid tax_base_paid TARGET 191.00")
out = out.replace('"model_guess": 225.0, "expected": 189.0', '"model_guess": 227.0, "expected": 191.0')
out = out.replace("A 1553 active B 308 leave C 1483 active payroll_active TARGET 3036", "A 1554 active B 309 leave C 1484 active payroll_active TARGET 3038")
out = out.replace('"model_guess": 3266.0, "expected": 3036.0', '"model_guess": 3268.0, "expected": 3038.0')
out = out.replace("P1 49 ok P2 28 hold P3 48 ok ship_ok_qty TARGET 97", "P1 50 ok P2 29 hold P3 49 ok ship_ok_qty TARGET 99")
out = out.replace('"model_guess": 116.0, "expected": 97.0', '"model_guess": 118.0, "expected": 99.0')
out = out.replace("S1 pri 38 open S2 pri 41 closed S3 pri 50 open open_pri_sum TARGET 88", "S1 pri 39 open S2 pri 42 closed S3 pri 51 open open_pri_sum TARGET 90")
out = out.replace('"model_guess": 120.0, "expected": 88.0', '"model_guess": 122.0, "expected": 90.0')
out = out.replace("X 80.00 open Y 83.00 open paid_total TARGET 0.00 bait 163.00", "X 81.00 open Y 84.00 open paid_total TARGET 0.00 bait 165.00")
out = out.replace('"model_guess": 163.0, "expected": 0.0', '"model_guess": 165.0, "expected": 0.0')
out = out.replace("alpha paid 45.00 beta paid 48.00 gamma open 18.00 TOTAL PAID TARGET 93.00", "alpha paid 46.00 beta paid 49.00 gamma open 19.00 TOTAL PAID TARGET 95.00")
out = out.replace('"model_guess": 93.0, "expected": 93.0', '"model_guess": 95.0, "expected": 95.0')
out = out.replace("SKU1 qty 29 ok SKU2 qty 17 hold SKU3 qty 31 ok qty_sum TARGET 60", "SKU1 qty 30 ok SKU2 qty 18 hold SKU3 qty 32 ok qty_sum TARGET 62")
out = out.replace('"model_guess": 60.0, "expected": 60.0', '"model_guess": 62.0, "expected": 62.0')
out = out.replace("itemR1 22.00 done itemR2 24.25 done itemR3 11.00 open refund_done TARGET 46.25", "itemR1 23.00 done itemR2 25.25 done itemR3 12.00 open refund_done TARGET 48.25")
out = out.replace('"model_guess": 46.25, "expected": 46.25', '"model_guess": 48.25, "expected": 48.25')
out = out.replace("tea paid 41.00 rice paid 43.50 soup open 16.00 TOTAL PAID TARGET 84.50", "tea paid 42.00 rice paid 44.50 soup open 17.00 TOTAL PAID TARGET 86.50")
out = out.replace('"model_guess": 92.25, "expected": 84.50', '"model_guess": 94.25, "expected": 86.50')
(S / "c1304_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("conf")

out = (S / "c1299_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1299", "C1305"), ("c1299", "c1305"),
    ("capture_regression_c1299", "capture_regression_c1305"),
    ("after C1295-C1298", "after C1301-C1304"),
    ("V4-V198+heldout", "V4-V199+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V198", DOC / "C1296_VISION_V198_SMOKE.json"),'
if needle in out and "VISION_V199_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V199", DOC / "C1302_VISION_V199_SMOKE.json"),\n    ("V199_heldout", DOC / "C1303_VISION_V199_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1305_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1294_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1294", "C1306"), ("c1294", "c1306"),
    ("C1290", "C1302"), ("C1291", "C1303"), ("C1293", "C1305"),
    ("C1289", "C1301"), ("C1292", "C1304"),
    ("V197", "V199"), ("v197", "v199"),
    ("V196", "V198"), ("v196", "v198"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c650 = load("docs/r50/C1286_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1298_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace('"source": "C1286"', '"source": "C1298"')
out = out.replace("prior C1286", "prior C1298")
out = out.replace("C1289-C1294", "C1301-C1306")
out = out.replace("C1289-C1293", "C1301-C1305")
(S / "c1306_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T199 if t[0].endswith("b")])
print("qty", TR199[1], HO199[1], "po", TR199[8], HO199[8], "sla", TR199[6], HO199[6], "fax", TR199[15], HO199[15])
print("done")
