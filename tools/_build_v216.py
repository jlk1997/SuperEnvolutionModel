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
T216 = [
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
TR216 = [
    [1582.0, 1599.5, 1382.0],[840, 760, 820],[1505.0, 1534.25, 1362.0],[1638.0, 1655.0, 1452.0],
    [1700.0, 1724.0, 1422.0],[1458, 1474, 1380],[480.0, 520.0, 740.0],[1548.0, 1579.75, 1386.0],
    [840.0, 760.0, 820.0],[1615.0, 1603.0, 1383.0],[1,1,0],[0,0,0],
    [1681.0, 1702.5, 1408.0],[1,0,0],[1220, 1212, 1190],[1238, 1222, 748],[1,0,0],[1264, 1240, 1210],
]
HO216 = [
    [1442.0, 1454.75, 1325.0],[740, 780, 820],[1400.0, 1413.5, 1313.0],[1515.0, 1531.0, 1354.0],
    [1556.0, 1572.0, 1349.0],[1350, 1364, 1318],[360.0, 400.0, 730.0],[1426.0, 1447.75, 1325.0],
    [780.0, 740.0, 820.0],[1473.0, 1459.0, 1320.0],[1,1,0],[0,0,0],
    [1508.0, 1523.5, 1335.0],[1,0,0],[1187, 1182, 1177],[1202, 1196, 1184],[1,0,0],[1212, 1206, 1185],
]
check(TR216, "TR"); check(HO216, "HO")

(ROOT / "tools/_v216_themes.json").write_text(json.dumps({"themes": T216, "train": TR216, "heldout": HO216}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_216(src):
    src = src.replace("# --- V215 overlays (new vs V50) ---", "# --- V216 overlays (new vs V50) ---")
    src = src.replace("# --- V215 overlays (new vs V49) ---", "# --- V216 overlays (new vs V49) ---")
    for a, b in [
        ("ASHMOOR bait 129.39", "ASHFEN bait 130.40"),
        ("CEDARM bait 131.41", "CEDARF bait 132.42"),
        ("DAWNM ghost 54.54", "DAWNF ghost 55.55"),
        ("GLENM bait 124.34", "GLENF bait 125.35"),
        ("JADEM bait 115.25", "JADEF bait 116.26"),
        ("NETHERM bait 132.42", "NETHERF bait 133.43"),
        ("ash mist + stone ticks (V215-only)", "ash mist + stone ticks (V216-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD215 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v215_themes.json").read_text(encoding="utf-8"))["themes"])
NEW216 = "_".join(t[0] for t in T216)

out = (S / "c1397_vision_v215_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1397", "C1403"), ("c1397", "c1403"), ("V215", "V216"), ("v215", "v216"),
    ("_v215c1397", "_v216c1403"),
    ("Harder than V214", "Harder than V215"), ("harder than V214", "harder than V215"),
    (OLD215, NEW216),
    ("V215 keeps floor", "V216 keeps floor"),
    ("C1397 design+fixtures; no VL claim", "C1403 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1398 VL smoke", "fixtures only; claim deferred to C1404 VL smoke"),
    ("No claim until C1398 VL", "No claim until C1404 VL"),
    ("kept on V215", "kept on V216"),
    ("vision_images_v215", "vision_images_v216"),
    ("VL_GATE_V215", "VL_GATE_V216"), ("vl_gate_v215", "vl_gate_v216"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V214:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V215: ashfen, cedarfen, dawnfen, elmfen, fernfen, glenfen, hazefen, inkfen,\njadefen, knotfen, lakefen, mossfen, netherfen, oakfen, pinefen, quillfen, reedfen, stonefen.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T216, "v216", "V216", TR216))
out = retarget_216(out)
(S / "c1403_vision_v216_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1398_vision_v215_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1398", "C1404"), ("c1398", "c1404"), ("V215", "V216"), ("v215", "v216"),
    ("vision_images_v215", "vision_images_v216"),
    ("VL_GATE_V215", "VL_GATE_V216"), ("vl_gate_v215", "vl_gate_v216"),
    ("runs/vision_v215", "runs/vision_v216"),
]:
    out = out.replace(a, b)
(S / "c1404_vision_v216_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1399_vision_v215_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1399", "C1405"), ("c1399", "c1405"), ("V215", "V216"), ("v215", "v216"),
    ("vision_images_v215h", "vision_images_v216h"),
    ("vision_images_v215", "vision_images_v216"),
    ("VL_GATE_V215", "VL_GATE_V216"), ("vl_gate_v215", "vl_gate_v216"),
    ("runs/vision_v215h", "runs/vision_v216h"),
    ("_v215c1397", "_v216c1403"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T216, "v216h", "V216H", HO216))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v216h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v216"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v216" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v216h_c1405"'); seen_run = True; continue
    out2.append(ln)
(S / "c1405_vision_v216_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1394_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C1394", "C1406"), ("c1394", "c1406"),
    ("product_u2c_c1394", "product_u2c_c1406"),
]:
    out = out.replace(a, b)
(S / "c1406_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c1401_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1401", "C1407"), ("c1401", "c1407"),
    ("capture_regression_c1401", "capture_regression_c1407"),
    ("after C1397-C1400", "after C1403-C1406"),
    ("V4-V215+heldout", "V4-V216+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V215", DOC / "C1398_VISION_V215_SMOKE.json"),'
if needle in out and "VISION_V216_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V216", DOC / "C1404_VISION_V216_SMOKE.json"),\n    ("V216_heldout", DOC / "C1405_VISION_V216_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1407_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1396_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1396", "C1408"), ("c1396", "c1408"),
    ("C1392", "C1404"), ("C1393", "C1405"), ("C1395", "C1407"),
    ("C1391", "C1403"), ("C1394", "C1406"),
    ("V214", "V216"), ("v214", "v216"),
    ("V213", "V215"), ("v213", "v215"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C1388_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1400_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace('"source": "C1388"', '"source": "C1400"')
out = out.replace(
    'f"- confidence-gate (prior C1388): pass={conf_pass} rate={conf_rate}"',
    'f"- confidence-gate (prior C1400): pass={conf_pass} rate={conf_rate}"',
)
out = out.replace("C1391-C1396", "C1403-C1408")
out = out.replace("C1391-C1395", "C1403-C1407")
(S / "c1408_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T216 if t[0].endswith("b")])
print("qty", TR216[1], HO216[1], "po", TR216[8], HO216[8], "sla", TR216[6], HO216[6], "fax", TR216[15], HO216[15])
print("done")
