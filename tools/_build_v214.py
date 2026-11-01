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
T214 = [
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
TR214 = [
    [1546.0, 1563.5, 1350.0],[840, 760, 820],[1469.0, 1498.25, 1330.0],[1602.0, 1619.0, 1420.0],
    [1664.0, 1688.0, 1390.0],[1422, 1438, 1348],[480.0, 520.0, 740.0],[1512.0, 1543.75, 1354.0],
    [840.0, 760.0, 820.0],[1579.0, 1567.0, 1351.0],[1,1,0],[0,0,0],
    [1645.0, 1666.5, 1376.0],[1,0,0],[1188, 1180, 1158],[1206, 1190, 748],[1,0,0],[1232, 1208, 1178],
]
HO214 = [
    [1410.0, 1422.75, 1297.0],[740, 780, 820],[1368.0, 1381.5, 1285.0],[1483.0, 1499.0, 1326.0],
    [1524.0, 1540.0, 1321.0],[1318, 1332, 1290],[360.0, 400.0, 730.0],[1394.0, 1415.75, 1297.0],
    [780.0, 740.0, 820.0],[1441.0, 1427.0, 1292.0],[1,1,0],[0,0,0],
    [1476.0, 1491.5, 1307.0],[1,0,0],[1159, 1154, 1149],[1174, 1168, 1156],[1,0,0],[1184, 1178, 1157],
]
check(TR214, "TR"); check(HO214, "HO")

(ROOT / "tools/_v214_themes.json").write_text(json.dumps({"themes": T214, "train": TR214, "heldout": HO214}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_214(src):
    src = src.replace("# --- V213 overlays (new vs V50) ---", "# --- V214 overlays (new vs V50) ---")
    src = src.replace("# --- V213 overlays (new vs V49) ---", "# --- V214 overlays (new vs V49) ---")
    for a, b in [
        ("ASHCROFT bait 127.37", "ASHHURST bait 128.38"),
        ("CEDARC bait 129.39", "CEDARH bait 130.40"),
        ("DAWNC ghost 52.52", "DAWNH ghost 53.53"),
        ("GLENC bait 122.32", "GLENH bait 123.33"),
        ("JADEC bait 113.23", "JADEH bait 114.24"),
        ("NETHERC bait 130.40", "NETHERH bait 131.41"),
        ("ash mist + stone ticks (V213-only)", "ash mist + stone ticks (V214-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD213 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v213_themes.json").read_text(encoding="utf-8"))["themes"])
NEW214 = "_".join(t[0] for t in T214)

out = (S / "c1385_vision_v213_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1385", "C1391"), ("c1385", "c1391"), ("V213", "V214"), ("v213", "v214"),
    ("_v213c1385", "_v214c1391"),
    ("Harder than V212", "Harder than V213"), ("harder than V212", "harder than V213"),
    (OLD213, NEW214),
    ("V213 keeps floor", "V214 keeps floor"),
    ("C1385 design+fixtures; no VL claim", "C1391 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1386 VL smoke", "fixtures only; claim deferred to C1392 VL smoke"),
    ("No claim until C1386 VL", "No claim until C1392 VL"),
    ("kept on V213", "kept on V214"),
    ("vision_images_v213", "vision_images_v214"),
    ("VL_GATE_V213", "VL_GATE_V214"), ("vl_gate_v213", "vl_gate_v214"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V212:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V213: ashhurst, cedarhurst, dawnhurst, elmhurst, fernhurst, glenhurst, hazehurst, inkhurst,\njadehurst, knothurst, lakehurst, mosshurst, netherhurst, oakhurst, pinehurst, quillhurst, reedhurst, stonehurst.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T214, "v214", "V214", TR214))
out = retarget_214(out)
(S / "c1391_vision_v214_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1386_vision_v213_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1386", "C1392"), ("c1386", "c1392"), ("V213", "V214"), ("v213", "v214"),
    ("vision_images_v213", "vision_images_v214"),
    ("VL_GATE_V213", "VL_GATE_V214"), ("vl_gate_v213", "vl_gate_v214"),
    ("runs/vision_v213", "runs/vision_v214"),
]:
    out = out.replace(a, b)
(S / "c1392_vision_v214_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1387_vision_v213_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1387", "C1393"), ("c1387", "c1393"), ("V213", "V214"), ("v213", "v214"),
    ("vision_images_v213h", "vision_images_v214h"),
    ("vision_images_v213", "vision_images_v214"),
    ("VL_GATE_V213", "VL_GATE_V214"), ("vl_gate_v213", "vl_gate_v214"),
    ("runs/vision_v213h", "runs/vision_v214h"),
    ("_v213c1385", "_v214c1391"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T214, "v214h", "V214H", HO214))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v214h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v214"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v214" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v214h_c1393"'); seen_run = True; continue
    out2.append(ln)
(S / "c1393_vision_v214_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1382_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C1382", "C1394"), ("c1382", "c1394"),
    ("product_u2c_c1382", "product_u2c_c1394"),
]:
    out = out.replace(a, b)
(S / "c1394_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c1389_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1389", "C1395"), ("c1389", "c1395"),
    ("capture_regression_c1389", "capture_regression_c1395"),
    ("after C1385-C1388", "after C1391-C1394"),
    ("V4-V213+heldout", "V4-V214+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V213", DOC / "C1386_VISION_V213_SMOKE.json"),'
if needle in out and "VISION_V214_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V214", DOC / "C1392_VISION_V214_SMOKE.json"),\n    ("V214_heldout", DOC / "C1393_VISION_V214_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1395_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1384_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1384", "C1396"), ("c1384", "c1396"),
    ("C1380", "C1392"), ("C1381", "C1393"), ("C1383", "C1395"),
    ("C1379", "C1391"), ("C1382", "C1394"),
    ("V212", "V214"), ("v212", "v214"),
    ("V211", "V213"), ("v211", "v213"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C1376_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1388_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace('"source": "C1376"', '"source": "C1388"')
out = out.replace(
    'f"- confidence-gate (prior C1376): pass={conf_pass} rate={conf_rate}"',
    'f"- confidence-gate (prior C1388): pass={conf_pass} rate={conf_rate}"',
)
out = out.replace("C1379-C1384", "C1391-C1396")
out = out.replace("C1379-C1383", "C1391-C1395")
(S / "c1396_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T214 if t[0].endswith("b")])
print("qty", TR214[1], HO214[1], "po", TR214[8], HO214[8], "sla", TR214[6], HO214[6], "fax", TR214[15], HO214[15])
print("done")
