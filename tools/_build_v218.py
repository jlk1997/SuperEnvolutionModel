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

# *dale ; qty TR 840+760 HO 740+780; PO TR 840+760 HO 780+740; SLA TR 480+520 HO 360+400
T218 = [
    ["ashdale","recv","paid_total","ASHDALE GRAIN RECV","RECV","x"],
    ["cedardale","wh","qty_sum","WH CEDARDALE BIN","RECV","x"],
    ["dawndale","refund","refund_done","DAWNDALE PATCH REFUND","DONE","x"],
    ["elmdale","tax","tax_base_paid","ELMDALE TAX SLIP","TAX","x"],
    ["ferndale","pay","payroll_active","FERNDALE PAYROLL","PAY","x"],
    ["glendale","ship","ship_ok","GLENDALE SHIP DOCK","SHIP","x"],
    ["hazedale","sla","sla_ok_hours","HAZEDALE SLA CARD","SLA","x"],
    ["inkdale","exp","exp_sum","INKDALE EXPENSE","EXP","x"],
    ["jadedale","po","po_open","JADEDALE PO SHEET","PO","x"],
    ["knotdale","order","order_paid","KNOTDALE ORDER","ORD","x"],
    ["lakedale","dup","dup_mark","LAKEDALE DUP MARK","DUP","x"],
    ["mossdale","zero","zero_check","MOSSDALE AIR ZERO","ZERO","x"],
    ["netherdale","ledger","ledger_net","NETHERDALE LEDGER","LED","x"],
    ["oakdale","ui","ui_ok","OAKDALE UI SCAN","UI","x"],
    ["pinedale","stack","stack_count","PINEDALE STACK","STK","x"],
    ["quilldale","fax","fax_pages","QUILLDALE FAX","FAX","x"],
    ["reeddale","glare","glare_ok","REEDDALE GLARE","GLR","x"],
    ["stonedale","tab","tab_index","STONEDALE TAB INDEX","TAB","x"],
]
TR218 = [
    [1618.0, 1635.5, 1414.0],[840, 760, 820],[1541.0, 1570.25, 1394.0],[1674.0, 1691.0, 1484.0],
    [1736.0, 1760.0, 1454.0],[1494, 1510, 1412],[480.0, 520.0, 740.0],[1584.0, 1615.75, 1418.0],
    [840.0, 760.0, 820.0],[1651.0, 1639.0, 1415.0],[1,1,0],[0,0,0],
    [1717.0, 1738.5, 1440.0],[1,0,0],[1252, 1244, 1222],[1270, 1254, 748],[1,0,0],[1296, 1272, 1242],
]
HO218 = [
    [1474.0, 1486.75, 1353.0],[740, 780, 820],[1432.0, 1445.5, 1341.0],[1547.0, 1563.0, 1382.0],
    [1588.0, 1604.0, 1377.0],[1382, 1396, 1346],[360.0, 400.0, 730.0],[1458.0, 1479.75, 1353.0],
    [780.0, 740.0, 820.0],[1505.0, 1491.0, 1348.0],[1,1,0],[0,0,0],
    [1540.0, 1555.5, 1363.0],[1,0,0],[1215, 1210, 1205],[1230, 1224, 1212],[1,0,0],[1240, 1234, 1213],
]
check(TR218, "TR"); check(HO218, "HO")

(ROOT / "tools/_v218_themes.json").write_text(json.dumps({"themes": T218, "train": TR218, "heldout": HO218}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_218(src):
    src = src.replace("# --- V217 overlays (new vs V50) ---", "# --- V218 overlays (new vs V50) ---")
    src = src.replace("# --- V217 overlays (new vs V49) ---", "# --- V218 overlays (new vs V49) ---")
    for a, b in [
        ("ASHBROOK bait 131.41", "ASHDALE bait 132.42"),
        ("CEDARB bait 133.43", "CEDARD bait 134.44"),
        ("DAWNB ghost 56.56", "DAWND ghost 57.57"),
        ("GLENB bait 126.36", "GLEND bait 127.37"),
        ("JADEB bait 117.27", "JADED bait 118.28"),
        ("NETHERB bait 134.44", "NETHERD bait 135.45"),
        ("ash mist + stone ticks (V217-only)", "ash mist + stone ticks (V218-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD217 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v217_themes.json").read_text(encoding="utf-8"))["themes"])
NEW218 = "_".join(t[0] for t in T218)

out = (S / "c1409_vision_v217_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1409", "C1415"), ("c1409", "c1415"), ("V217", "V218"), ("v217", "v218"),
    ("_v217c1409", "_v218c1415"),
    ("Harder than V216", "Harder than V217"), ("harder than V216", "harder than V217"),
    (OLD217, NEW218),
    ("V217 keeps floor", "V218 keeps floor"),
    ("C1409 design+fixtures; no VL claim", "C1415 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1410 VL smoke", "fixtures only; claim deferred to C1416 VL smoke"),
    ("No claim until C1410 VL", "No claim until C1416 VL"),
    ("kept on V217", "kept on V218"),
    ("vision_images_v217", "vision_images_v218"),
    ("VL_GATE_V217", "VL_GATE_V218"), ("vl_gate_v217", "vl_gate_v218"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V216:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V217: ashdale, cedardale, dawndale, elmdale, ferndale, glendale, hazedale, inkdale,\njadedale, knotdale, lakedale, mossdale, netherdale, oakdale, pinedale, quilldale, reeddale, stonedale.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T218, "v218", "V218", TR218))
out = retarget_218(out)
(S / "c1415_vision_v218_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1410_vision_v217_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1410", "C1416"), ("c1410", "c1416"), ("V217", "V218"), ("v217", "v218"),
    ("vision_images_v217", "vision_images_v218"),
    ("VL_GATE_V217", "VL_GATE_V218"), ("vl_gate_v217", "vl_gate_v218"),
    ("runs/vision_v217", "runs/vision_v218"),
]:
    out = out.replace(a, b)
(S / "c1416_vision_v218_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1411_vision_v217_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1411", "C1417"), ("c1411", "c1417"), ("V217", "V218"), ("v217", "v218"),
    ("vision_images_v217h", "vision_images_v218h"),
    ("vision_images_v217", "vision_images_v218"),
    ("VL_GATE_V217", "VL_GATE_V218"), ("vl_gate_v217", "vl_gate_v218"),
    ("runs/vision_v217h", "runs/vision_v218h"),
    ("_v217c1409", "_v218c1415"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T218, "v218h", "V218H", HO218))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v218h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v218"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v218" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v218h_c1417"'); seen_run = True; continue
    out2.append(ln)
(S / "c1417_vision_v218_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1406_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C1406", "C1418"), ("c1406", "c1418"),
    ("product_u2c_c1406", "product_u2c_c1418"),
]:
    out = out.replace(a, b)
(S / "c1418_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c1413_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1413", "C1419"), ("c1413", "c1419"),
    ("capture_regression_c1413", "capture_regression_c1419"),
    ("after C1409-C1412", "after C1415-C1418"),
    ("V4-V217+heldout", "V4-V218+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V217", DOC / "C1410_VISION_V217_SMOKE.json"),'
if needle in out and "VISION_V218_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V218", DOC / "C1416_VISION_V218_SMOKE.json"),\n    ("V218_heldout", DOC / "C1417_VISION_V218_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1419_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1408_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1408", "C1420"), ("c1408", "c1420"),
    ("C1404", "C1416"), ("C1405", "C1417"), ("C1407", "C1419"),
    ("C1403", "C1415"), ("C1406", "C1418"),
    ("V216", "V218"), ("v216", "v218"),
    ("V215", "V217"), ("v215", "v217"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C1400_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1412_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace('"source": "C1400"', '"source": "C1412"')
out = out.replace(
    'f"- confidence-gate (prior C1400): pass={conf_pass} rate={conf_rate}"',
    'f"- confidence-gate (prior C1412): pass={conf_pass} rate={conf_rate}"',
)
out = out.replace("C1403-C1408", "C1415-C1420")
out = out.replace("C1403-C1407", "C1415-C1419")
(S / "c1420_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T218 if t[0].endswith("b")])
print("qty", TR218[1], HO218[1], "po", TR218[8], HO218[8], "sla", TR218[6], HO218[6], "fax", TR218[15], HO218[15])
print("done")
