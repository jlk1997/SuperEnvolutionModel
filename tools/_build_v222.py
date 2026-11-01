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

# *mere ; qty/SLA OCR-safe; stack/fax/tab mid-band
T222 = [
    ["ashmere","recv","paid_total","ASHMERE GRAIN RECV","RECV","x"],
    ["cedarmere","wh","qty_sum","WH CEDARMERE BIN","RECV","x"],
    ["dawnmere","refund","refund_done","DAWNMERE PATCH REFUND","DONE","x"],
    ["elmmere","tax","tax_base_paid","ELMMERE TAX SLIP","TAX","x"],
    ["fernmere","pay","payroll_active","FERNMERE PAYROLL","PAY","x"],
    ["glenmere","ship","ship_ok","GLENMERE SHIP DOCK","SHIP","x"],
    ["hazemere","sla","sla_ok_hours","HAZEMERE SLA CARD","SLA","x"],
    ["inkmere","exp","exp_sum","INKMERE EXPENSE","EXP","x"],
    ["jademere","po","po_open","JADEMERE PO SHEET","PO","x"],
    ["knotmere","order","order_paid","KNOTMERE ORDER","ORD","x"],
    ["lakemere","dup","dup_mark","LAKEMERE DUP MARK","DUP","x"],
    ["mossmere","zero","zero_check","MOSSMERE AIR ZERO","ZERO","x"],
    ["nethermere","ledger","ledger_net","NETHERMERE LEDGER","LED","x"],
    ["oakmere","ui","ui_ok","OAKMERE UI SCAN","UI","x"],
    ["pinemere","stack","stack_count","PINEMERE STACK","STK","x"],
    ["quillmere","fax","fax_pages","QUILLMERE FAX","FAX","x"],
    ["reedmere","glare","glare_ok","REEDMERE GLARE","GLR","x"],
    ["stonemere","tab","tab_index","STONEMERE TAB INDEX","TAB","x"],
]
TR222 = [
    [1690.0, 1707.5, 1478.0],[840, 760, 820],[1613.0, 1642.25, 1458.0],[1746.0, 1763.0, 1548.0],
    [1808.0, 1832.0, 1518.0],[1566, 1582, 1476],[480.0, 520.0, 740.0],[1656.0, 1687.75, 1482.0],
    [840.0, 760.0, 820.0],[1723.0, 1711.0, 1479.0],[1,1,0],[0,0,0],
    [1789.0, 1810.5, 1504.0],[1,0,0],[1212, 1204, 1184],[1228, 1212, 748],[1,0,0],[1244, 1228, 1206],
]
HO222 = [
    [1538.0, 1550.75, 1409.0],[740, 780, 820],[1496.0, 1509.5, 1397.0],[1611.0, 1627.0, 1438.0],
    [1652.0, 1668.0, 1433.0],[1446, 1460, 1402],[360.0, 400.0, 730.0],[1522.0, 1543.75, 1409.0],
    [780.0, 740.0, 820.0],[1569.0, 1555.0, 1404.0],[1,1,0],[0,0,0],
    [1604.0, 1619.5, 1419.0],[1,0,0],[1189, 1184, 1179],[1204, 1198, 1186],[1,0,0],[1214, 1208, 1187],
]
check(TR222, "TR"); check(HO222, "HO")

(ROOT / "tools/_v222_themes.json").write_text(json.dumps({"themes": T222, "train": TR222, "heldout": HO222}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_222(src):
    src = src.replace("# --- V221 overlays (new vs V50) ---", "# --- V222 overlays (new vs V50) ---")
    src = src.replace("# --- V221 overlays (new vs V49) ---", "# --- V222 overlays (new vs V49) ---")
    for a, b in [
        ("ASHHURST bait 135.45", "ASHMERE bait 136.46"),
        ("CEDARH bait 137.47", "CEDARM bait 138.48"),
        ("DAWNH ghost 60.60", "DAWNM ghost 61.61"),
        ("GLENH bait 130.40", "GLENM bait 131.41"),
        ("JADEH bait 121.31", "JADEM bait 122.32"),
        ("NETHERH bait 138.48", "NETHERM bait 139.49"),
        ("ash mist + stone ticks (V221-only)", "ash mist + stone ticks (V222-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD221 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v221_themes.json").read_text(encoding="utf-8"))["themes"])
NEW222 = "_".join(t[0] for t in T222)

out = (S / "c1433_vision_v221_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1433", "C1439"), ("c1433", "c1439"), ("V221", "V222"), ("v221", "v222"),
    ("_v221c1433", "_v222c1439"),
    ("Harder than V220", "Harder than V221"), ("harder than V220", "harder than V221"),
    (OLD221, NEW222),
    ("V221 keeps floor", "V222 keeps floor"),
    ("C1433 design+fixtures; no VL claim", "C1439 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1434 VL smoke", "fixtures only; claim deferred to C1440 VL smoke"),
    ("No claim until C1434 VL", "No claim until C1440 VL"),
    ("kept on V221", "kept on V222"),
    ("vision_images_v221", "vision_images_v222"),
    ("VL_GATE_V221", "VL_GATE_V222"), ("vl_gate_v221", "vl_gate_v222"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V220:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V221: ashmere, cedarmere, dawnmere, elmmere, fernmere, glenmere, hazemere, inkmere,\njademere, knotmere, lakemere, mossmere, nethermere, oakmere, pinemere, quillmere, reedmere, stonemere.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T222, "v222", "V222", TR222))
out = retarget_222(out)
(S / "c1439_vision_v222_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1434_vision_v221_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1434", "C1440"), ("c1434", "c1440"), ("V221", "V222"), ("v221", "v222"),
    ("vision_images_v221", "vision_images_v222"),
    ("VL_GATE_V221", "VL_GATE_V222"), ("vl_gate_v221", "vl_gate_v222"),
    ("runs/vision_v221", "runs/vision_v222"),
]:
    out = out.replace(a, b)
(S / "c1440_vision_v222_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1435_vision_v221_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1435", "C1441"), ("c1435", "c1441"), ("V221", "V222"), ("v221", "v222"),
    ("vision_images_v221h", "vision_images_v222h"),
    ("vision_images_v221", "vision_images_v222"),
    ("VL_GATE_V221", "VL_GATE_V222"), ("vl_gate_v221", "vl_gate_v222"),
    ("runs/vision_v221h", "runs/vision_v222h"),
    ("_v221c1433", "_v222c1439"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T222, "v222h", "V222H", HO222))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v222h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v222"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v222" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v222h_c1441"'); seen_run = True; continue
    out2.append(ln)
(S / "c1441_vision_v222_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1430_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C1430", "C1442"), ("c1430", "c1442"),
    ("product_u2c_c1430", "product_u2c_c1442"),
]:
    out = out.replace(a, b)
(S / "c1442_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c1437_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1437", "C1443"), ("c1437", "c1443"),
    ("capture_regression_c1437", "capture_regression_c1443"),
    ("after C1433-C1436", "after C1439-C1442"),
    ("V4-V221+heldout", "V4-V222+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V221", DOC / "C1434_VISION_V221_SMOKE.json"),'
if needle in out and "VISION_V222_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V222", DOC / "C1440_VISION_V222_SMOKE.json"),\n    ("V222_heldout", DOC / "C1441_VISION_V222_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1443_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1432_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1432", "C1444"), ("c1432", "c1444"),
    ("C1428", "C1440"), ("C1429", "C1441"), ("C1431", "C1443"),
    ("C1427", "C1439"), ("C1430", "C1442"),
    ("V220", "V222"), ("v220", "v222"),
    ("V219", "V221"), ("v219", "v221"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C1424_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1436_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace('"source": "C1424"', '"source": "C1436"')
out = out.replace(
    'f"- confidence-gate (prior C1424): pass={conf_pass} rate={conf_rate}"',
    'f"- confidence-gate (prior C1436): pass={conf_pass} rate={conf_rate}"',
)
out = out.replace("C1427-C1432", "C1439-C1444")
out = out.replace("C1427-C1431", "C1439-C1443")
(S / "c1444_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T222 if t[0].endswith("b")])
print("qty", TR222[1], HO222[1], "stack", TR222[14], HO222[14], "fax", TR222[15], HO222[15])
print("done")
