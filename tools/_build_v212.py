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
T212 = [
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
TR212 = [
    [1510.0, 1527.5, 1318.0],[840, 760, 820],[1433.0, 1462.25, 1298.0],[1566.0, 1583.0, 1388.0],
    [1628.0, 1652.0, 1358.0],[1386, 1402, 1316],[480.0, 520.0, 740.0],[1476.0, 1507.75, 1322.0],
    [840.0, 760.0, 820.0],[1543.0, 1531.0, 1319.0],[1,1,0],[0,0,0],
    [1609.0, 1630.5, 1344.0],[1,0,0],[1156, 1148, 1126],[1174, 1158, 748],[1,0,0],[1200, 1176, 1146],
]
HO212 = [
    [1378.0, 1390.75, 1269.0],[740, 780, 820],[1336.0, 1349.5, 1257.0],[1451.0, 1467.0, 1298.0],
    [1492.0, 1508.0, 1293.0],[1286, 1300, 1262],[360.0, 400.0, 730.0],[1362.0, 1383.75, 1269.0],
    [780.0, 740.0, 820.0],[1409.0, 1395.0, 1264.0],[1,1,0],[0,0,0],
    [1444.0, 1459.5, 1279.0],[1,0,0],[1131, 1126, 1121],[1146, 1140, 1128],[1,0,0],[1156, 1150, 1129],
]
check(TR212, "TR"); check(HO212, "HO")

(ROOT / "tools/_v212_themes.json").write_text(json.dumps({"themes": T212, "train": TR212, "heldout": HO212}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_212(src):
    src = src.replace("# --- V211 overlays (new vs V50) ---", "# --- V212 overlays (new vs V50) ---")
    src = src.replace("# --- V211 overlays (new vs V49) ---", "# --- V212 overlays (new vs V49) ---")
    for a, b in [
        ("ASHMERE bait 125.35", "ASHWICK bait 126.36"),
        ("CEDARM bait 127.37", "CEDARW bait 128.38"),
        ("DAWNM ghost 50.50", "DAWNW ghost 51.51"),
        ("GLENM bait 120.30", "GLENW bait 121.31"),
        ("JADEM bait 111.21", "JADEW bait 112.22"),
        ("NETHERM bait 128.38", "NETHERW bait 129.39"),
        ("ash mist + stone ticks (V211-only)", "ash mist + stone ticks (V212-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD211 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v211_themes.json").read_text(encoding="utf-8"))["themes"])
NEW212 = "_".join(t[0] for t in T212)

out = (S / "c1373_vision_v211_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1373", "C1379"), ("c1373", "c1379"), ("V211", "V212"), ("v211", "v212"),
    ("_v211c1373", "_v212c1379"),
    ("Harder than V210", "Harder than V211"), ("harder than V210", "harder than V211"),
    (OLD211, NEW212),
    ("V211 keeps floor", "V212 keeps floor"),
    ("C1373 design+fixtures; no VL claim", "C1379 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1374 VL smoke", "fixtures only; claim deferred to C1380 VL smoke"),
    ("No claim until C1374 VL", "No claim until C1380 VL"),
    ("kept on V211", "kept on V212"),
    ("vision_images_v211", "vision_images_v212"),
    ("VL_GATE_V211", "VL_GATE_V212"), ("vl_gate_v211", "vl_gate_v212"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V210:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V211: ashwich, cedarwick, dawnwick, elmwick, fernwick, glenwick, hazewick, inkwick,\njadewick, knotwick, lakewick, mosswick, netherwick, oakwick, pinewick, quillwick, reedwick, stonewick.",
    out, count=1, flags=re.S,
)
# fix typo ashwich -> ashwick in prose if any; themes list uses ashwick
out = out.replace("ashwich", "ashwick")
out = replace_specs(out, build_specs(T212, "v212", "V212", TR212))
out = retarget_212(out)
(S / "c1379_vision_v212_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1374_vision_v211_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1374", "C1380"), ("c1374", "c1380"), ("V211", "V212"), ("v211", "v212"),
    ("vision_images_v211", "vision_images_v212"),
    ("VL_GATE_V211", "VL_GATE_V212"), ("vl_gate_v211", "vl_gate_v212"),
    ("runs/vision_v211", "runs/vision_v212"),
]:
    out = out.replace(a, b)
(S / "c1380_vision_v212_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1375_vision_v211_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1375", "C1381"), ("c1375", "c1381"), ("V211", "V212"), ("v211", "v212"),
    ("vision_images_v211h", "vision_images_v212h"),
    ("vision_images_v211", "vision_images_v212"),
    ("VL_GATE_V211", "VL_GATE_V212"), ("vl_gate_v211", "vl_gate_v212"),
    ("runs/vision_v211h", "runs/vision_v212h"),
    ("_v211c1373", "_v212c1379"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T212, "v212h", "V212H", HO212))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v212h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v212"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v212" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v212h_c1381"'); seen_run = True; continue
    out2.append(ln)
(S / "c1381_vision_v212_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1370_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C1370", "C1382"), ("c1370", "c1382"),
    ("product_u2c_c1370", "product_u2c_c1382"),
]:
    out = out.replace(a, b)
(S / "c1382_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c1377_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1377", "C1383"), ("c1377", "c1383"),
    ("capture_regression_c1377", "capture_regression_c1383"),
    ("after C1373-C1376", "after C1379-C1382"),
    ("V4-V211+heldout", "V4-V212+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V211", DOC / "C1374_VISION_V211_SMOKE.json"),'
if needle in out and "VISION_V212_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V212", DOC / "C1380_VISION_V212_SMOKE.json"),\n    ("V212_heldout", DOC / "C1381_VISION_V212_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1383_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1372_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1372", "C1384"), ("c1372", "c1384"),
    ("C1368", "C1380"), ("C1369", "C1381"), ("C1371", "C1383"),
    ("C1367", "C1379"), ("C1370", "C1382"),
    ("V210", "V212"), ("v210", "v212"),
    ("V209", "V211"), ("v209", "v211"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C1364_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1376_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace('"source": "C1364"', '"source": "C1376"')
out = out.replace(
    'f"- confidence-gate (prior C1364): pass={conf_pass} rate={conf_rate}"',
    'f"- confidence-gate (prior C1376): pass={conf_pass} rate={conf_rate}"',
)
out = out.replace("C1367-C1372", "C1379-C1384")
out = out.replace("C1367-C1371", "C1379-C1383")
(S / "c1384_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T212 if t[0].endswith("b")])
print("qty", TR212[1], HO212[1], "po", TR212[8], HO212[8], "sla", TR212[6], HO212[6], "fax", TR212[15], HO212[15])
print("done")
