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

# *wick ; qty TR 840+760 HO 740+780; PO TR 840+760 HO 780+740; SLA TR 480+520 HO 360+400
T201 = [
    ["ashwick","recv","paid_total","ASHWICK GRAIN RECV","RECV","x"],
    ["cedarwick","wh","qty_sum","WH CEDARWICK BIN","RECV","x"],
    ["dawnwick","refund","refund_done","DAWNWICK PATCH REFUND","DONE","x"],
    ["elmwick","tax","tax_base_paid","ELMWICK TAX SLIP","TAX","x"],
    ["fernwick","pay","payroll_active","FERNWICK PAYROLL","PAY","x"],
    ["glenwick","ship","ship_ok","GLENWICK SHIP DOCK","SHIP","x"],
    ["hazewick","sla","sla_ok_hours","HAZEWICK SLA CARD","SLA","x"],
    ["inkwick","exp","exp_sum","INKWICK EXPENSE","EXP","x"],
    ["jadewick","po","po_open","JADEWICK PO SHEET","PO","x"],
    ["knotwick","order","order_paid","KNOTWICK ORDER","ORD","x"],
    ["lakewick","dup","dup_mark","LAKEWICK DUP MARK","DUP","x"],
    ["mosswick","zero","zero_check","MOSSWICK AIR ZERO","ZERO","x"],
    ["netherwick","ledger","ledger_net","NETHERWICK LEDGER","LED","x"],
    ["oakwick","ui","ui_ok","OAKWICK UI SCAN","UI","x"],
    ["pinewick","stack","stack_count","PINEWICK STACK","STK","x"],
    ["quillwick","fax","fax_pages","QUILLWICK FAX","FAX","x"],
    ["reedwick","glare","glare_ok","REEDWICK GLARE","GLR","x"],
    ["stonewick","tab","tab_index","STONEWICK TAB INDEX","TAB","x"],
]
TR201 = [
    [1402.0, 1419.5, 1212.0],[840, 760, 820],[1325.0, 1354.25, 1192.0],[1458.0, 1475.0, 1282.0],
    [1520.0, 1544.0, 1252.0],[1278, 1294, 1210],[480.0, 520.0, 720.0],[1368.0, 1399.75, 1216.0],
    [840.0, 760.0, 820.0],[1435.0, 1423.0, 1213.0],[1,1,0],[0,0,0],
    [1501.0, 1522.5, 1238.0],[1,0,0],[1050, 1042, 1020],[1068, 1052, 748],[1,0,0],[1094, 1070, 1040],
]
HO201 = [
    [1272.0, 1284.75, 1165.0],[740, 780, 820],[1230.0, 1243.5, 1153.0],[1345.0, 1361.0, 1194.0],
    [1386.0, 1402.0, 1189.0],[1180, 1194, 1158],[360.0, 400.0, 710.0],[1256.0, 1277.75, 1165.0],
    [780.0, 740.0, 820.0],[1303.0, 1289.0, 1160.0],[1,1,0],[0,0,0],
    [1338.0, 1353.5, 1175.0],[1,0,0],[1027, 1022, 1017],[1042, 1036, 1024],[1,0,0],[1052, 1046, 1025],
]
check(TR201, "TR"); check(HO201, "HO")

(ROOT / "tools/_v201_themes.json").write_text(json.dumps({"themes": T201, "train": TR201, "heldout": HO201}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_201(src):
    src = src.replace("# --- V200 overlays (new vs V50) ---", "# --- V201 overlays (new vs V50) ---")
    src = src.replace("# --- V200 overlays (new vs V49) ---", "# --- V201 overlays (new vs V49) ---")
    for a, b in [
        ("ASHMERE bait 114.24", "ASHWICK bait 115.25"),
        ("CEDARM bait 116.26", "CEDARW bait 117.27"),
        ("DAWNM ghost 39.39", "DAWNW ghost 40.40"),
        ("GLENM bait 109.19", "GLENW bait 110.20"),
        ("JADEM bait 100.10", "JADEW bait 101.11"),
        ("NETHERM bait 117.27", "NETHERW bait 118.28"),
        ("ash mist + stone ticks (V200-only)", "ash mist + stone ticks (V201-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD200 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v200_themes.json").read_text(encoding="utf-8"))["themes"])
NEW201 = "_".join(t[0] for t in T201)

out = (S / "c1307_vision_v200_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1307", "C1313"), ("c1307", "c1313"), ("V200", "V201"), ("v200", "v201"),
    ("_v200c1307", "_v201c1313"),
    ("Harder than V199", "Harder than V200"), ("harder than V199", "harder than V200"),
    (OLD200, NEW201),
    ("V200 keeps floor", "V201 keeps floor"),
    ("C1307 design+fixtures; no VL claim", "C1313 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1308 VL smoke", "fixtures only; claim deferred to C1314 VL smoke"),
    ("No claim until C1308 VL", "No claim until C1314 VL"),
    ("kept on V200", "kept on V201"),
    ("vision_images_v200", "vision_images_v201"),
    ("VL_GATE_V200", "VL_GATE_V201"), ("vl_gate_v200", "vl_gate_v201"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V199:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V200: ashwick, cedarwick, dawnwick, elmwick, fernwick, glenwick, hazewick, inkwick,\njadewick, knotwick, lakewick, mosswick, netherwick, oakwick, pinewick, quillwick, reedwick, stonewick.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T201, "v201", "V201", TR201))
out = retarget_201(out)
(S / "c1313_vision_v201_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1308_vision_v200_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1308", "C1314"), ("c1308", "c1314"), ("V200", "V201"), ("v200", "v201"),
    ("vision_images_v200", "vision_images_v201"),
    ("VL_GATE_V200", "VL_GATE_V201"), ("vl_gate_v200", "vl_gate_v201"),
    ("runs/vision_v200", "runs/vision_v201"),
]:
    out = out.replace(a, b)
(S / "c1314_vision_v201_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1309_vision_v200_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1309", "C1315"), ("c1309", "c1315"), ("V200", "V201"), ("v200", "v201"),
    ("vision_images_v200h", "vision_images_v201h"),
    ("vision_images_v200", "vision_images_v201"),
    ("VL_GATE_V200", "VL_GATE_V201"), ("vl_gate_v200", "vl_gate_v201"),
    ("runs/vision_v200h", "runs/vision_v201h"),
    ("_v200c1307", "_v201c1313"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T201, "v201h", "V201H", HO201))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v201h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v201"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v201" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v201h_c1315"'); seen_run = True; continue
    out2.append(ln)
(S / "c1315_vision_v201_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1304_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1304", "C1316"), ("c1304", "c1316"),
    ("cg82_", "cg83_"),
    ("conf_gate_stretch_c1304", "conf_gate_stretch_c1316"),
    ("confidence_gate_stretch_v145", "confidence_gate_stretch_v146"),
    ("Stretch vs C1292", "Stretch vs C1304"),
]:
    out = out.replace(a, b)
out = out.replace("a paid 61.00 b paid 65.75 c open 21.00 TOTAL PAID TARGET 126.75", "a paid 62.00 b paid 66.75 c open 22.00 TOTAL PAID TARGET 128.75")
out = out.replace('"model_guess": 999.0, "expected": 126.75', '"model_guess": 999.0, "expected": 128.75')
out = out.replace("SKU1 qty 56 ok SKU2 qty 30 hold SKU3 qty 60 ok qty_sum TARGET 116", "SKU1 qty 57 ok SKU2 qty 31 hold SKU3 qty 61 ok qty_sum TARGET 118")
out = out.replace('"model_guess": 128.0, "expected": 116.0', '"model_guess": 130.0, "expected": 118.0')
out = out.replace("itemR1 37.00 done itemR2 40.75 done itemR3 18.00 open refund_done TARGET 77.75", "itemR1 38.00 done itemR2 41.75 done itemR3 19.00 open refund_done TARGET 79.75")
out = out.replace('"model_guess": 86.5, "expected": 77.75', '"model_guess": 88.5, "expected": 79.75')
out = out.replace("T1 105.00 paid T2 45.00 open T3 86.00 paid tax_base_paid TARGET 191.00", "T1 106.00 paid T2 46.00 open T3 87.00 paid tax_base_paid TARGET 193.00")
out = out.replace('"model_guess": 227.0, "expected": 191.0', '"model_guess": 229.0, "expected": 193.0')
out = out.replace("A 1554 active B 309 leave C 1484 active payroll_active TARGET 3038", "A 1555 active B 310 leave C 1485 active payroll_active TARGET 3040")
out = out.replace('"model_guess": 3268.0, "expected": 3038.0', '"model_guess": 3270.0, "expected": 3040.0')
out = out.replace("P1 50 ok P2 29 hold P3 49 ok ship_ok_qty TARGET 99", "P1 51 ok P2 30 hold P3 50 ok ship_ok_qty TARGET 101")
out = out.replace('"model_guess": 118.0, "expected": 99.0', '"model_guess": 120.0, "expected": 101.0')
out = out.replace("S1 pri 39 open S2 pri 42 closed S3 pri 51 open open_pri_sum TARGET 90", "S1 pri 40 open S2 pri 43 closed S3 pri 52 open open_pri_sum TARGET 92")
out = out.replace('"model_guess": 122.0, "expected": 90.0', '"model_guess": 124.0, "expected": 92.0')
out = out.replace("X 81.00 open Y 84.00 open paid_total TARGET 0.00 bait 165.00", "X 82.00 open Y 85.00 open paid_total TARGET 0.00 bait 167.00")
out = out.replace('"model_guess": 165.0, "expected": 0.0', '"model_guess": 167.0, "expected": 0.0')
out = out.replace("alpha paid 46.00 beta paid 49.00 gamma open 19.00 TOTAL PAID TARGET 95.00", "alpha paid 47.00 beta paid 50.00 gamma open 20.00 TOTAL PAID TARGET 97.00")
out = out.replace('"model_guess": 95.0, "expected": 95.0', '"model_guess": 97.0, "expected": 97.0')
out = out.replace("SKU1 qty 30 ok SKU2 qty 18 hold SKU3 qty 32 ok qty_sum TARGET 62", "SKU1 qty 31 ok SKU2 qty 19 hold SKU3 qty 33 ok qty_sum TARGET 64")
out = out.replace('"model_guess": 62.0, "expected": 62.0', '"model_guess": 64.0, "expected": 64.0')
out = out.replace("itemR1 23.00 done itemR2 25.25 done itemR3 12.00 open refund_done TARGET 48.25", "itemR1 24.00 done itemR2 26.25 done itemR3 13.00 open refund_done TARGET 50.25")
out = out.replace('"model_guess": 48.25, "expected": 48.25', '"model_guess": 50.25, "expected": 50.25')
out = out.replace("tea paid 42.00 rice paid 44.50 soup open 17.00 TOTAL PAID TARGET 86.50", "tea paid 43.00 rice paid 45.50 soup open 18.00 TOTAL PAID TARGET 88.50")
out = out.replace('"model_guess": 94.25, "expected": 86.50', '"model_guess": 96.25, "expected": 88.50')
(S / "c1316_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("conf")

out = (S / "c1311_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1311", "C1317"), ("c1311", "c1317"),
    ("capture_regression_c1311", "capture_regression_c1317"),
    ("after C1307-C1310", "after C1313-C1316"),
    ("V4-V200+heldout", "V4-V201+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V200", DOC / "C1308_VISION_V200_SMOKE.json"),'
if needle in out and "VISION_V201_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V201", DOC / "C1314_VISION_V201_SMOKE.json"),\n    ("V201_heldout", DOC / "C1315_VISION_V201_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1317_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1306_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1306", "C1318"), ("c1306", "c1318"),
    ("C1302", "C1314"), ("C1303", "C1315"), ("C1305", "C1317"),
    ("C1301", "C1313"), ("C1304", "C1316"),
    ("V199", "V201"), ("v199", "v201"),
    ("V198", "V200"), ("v198", "v200"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c650 = load("docs/r50/C1298_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1310_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace('"source": "C1298"', '"source": "C1310"')
out = out.replace("prior C1298", "prior C1310")
out = out.replace("C1301-C1306", "C1313-C1318")
out = out.replace("C1301-C1305", "C1313-C1317")
(S / "c1318_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T201 if t[0].endswith("b")])
print("qty", TR201[1], HO201[1], "po", TR201[8], HO201[8], "sla", TR201[6], HO201[6], "fax", TR201[15], HO201[15])
print("done")
