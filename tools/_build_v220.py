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

# *ford ; qty TR 840+760 HO 740+780; PO TR 840+760 HO 780+740; SLA TR 480+520 HO 360+400
# stack/fax/tab kept mid-band (V219 crush lesson: do not creep with paid)
T220 = [
    ["ashford","recv","paid_total","ASHFORD GRAIN RECV","RECV","x"],
    ["cedarford","wh","qty_sum","WH CEDARFORD BIN","RECV","x"],
    ["dawnford","refund","refund_done","DAWNFORD PATCH REFUND","DONE","x"],
    ["elmford","tax","tax_base_paid","ELMFORD TAX SLIP","TAX","x"],
    ["fernford","pay","payroll_active","FERNFORD PAYROLL","PAY","x"],
    ["glenford","ship","ship_ok","GLENFORD SHIP DOCK","SHIP","x"],
    ["hazeford","sla","sla_ok_hours","HAZEFORD SLA CARD","SLA","x"],
    ["inkford","exp","exp_sum","INKFORD EXPENSE","EXP","x"],
    ["jadeford","po","po_open","JADEFORD PO SHEET","PO","x"],
    ["knotford","order","order_paid","KNOTFORD ORDER","ORD","x"],
    ["lakeford","dup","dup_mark","LAKEFORD DUP MARK","DUP","x"],
    ["mossford","zero","zero_check","MOSSFORD AIR ZERO","ZERO","x"],
    ["netherford","ledger","ledger_net","NETHERFORD LEDGER","LED","x"],
    ["oakford","ui","ui_ok","OAKFORD UI SCAN","UI","x"],
    ["pineford","stack","stack_count","PINEFORD STACK","STK","x"],
    ["quillford","fax","fax_pages","QUILLFORD FAX","FAX","x"],
    ["reedford","glare","glare_ok","REEDFORD GLARE","GLR","x"],
    ["stoneford","tab","tab_index","STONEFORD TAB INDEX","TAB","x"],
]
TR220 = [
    [1654.0, 1671.5, 1446.0],[840, 760, 820],[1577.0, 1606.25, 1426.0],[1710.0, 1727.0, 1516.0],
    [1772.0, 1796.0, 1486.0],[1530, 1546, 1444],[480.0, 520.0, 740.0],[1620.0, 1651.75, 1450.0],
    [840.0, 760.0, 820.0],[1687.0, 1675.0, 1447.0],[1,1,0],[0,0,0],
    [1753.0, 1774.5, 1472.0],[1,0,0],[1196, 1188, 1168],[1212, 1196, 748],[1,0,0],[1228, 1212, 1190],
]
HO220 = [
    [1506.0, 1518.75, 1381.0],[740, 780, 820],[1464.0, 1477.5, 1369.0],[1579.0, 1595.0, 1410.0],
    [1620.0, 1636.0, 1405.0],[1414, 1428, 1374],[360.0, 400.0, 730.0],[1490.0, 1511.75, 1381.0],
    [780.0, 740.0, 820.0],[1537.0, 1523.0, 1376.0],[1,1,0],[0,0,0],
    [1572.0, 1587.5, 1391.0],[1,0,0],[1173, 1168, 1163],[1188, 1182, 1170],[1,0,0],[1198, 1192, 1171],
]
check(TR220, "TR"); check(HO220, "HO")

(ROOT / "tools/_v220_themes.json").write_text(json.dumps({"themes": T220, "train": TR220, "heldout": HO220}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_220(src):
    src = src.replace("# --- V219 overlays (new vs V50) ---", "# --- V220 overlays (new vs V50) ---")
    src = src.replace("# --- V219 overlays (new vs V49) ---", "# --- V220 overlays (new vs V49) ---")
    for a, b in [
        ("ASHVALE bait 133.43", "ASHFORD bait 134.44"),
        ("CEDARV bait 135.45", "CEDARF bait 136.46"),
        ("DAWNV ghost 58.58", "DAWNF ghost 59.59"),
        ("GLENV bait 128.38", "GLENF bait 129.39"),
        ("JADEV bait 119.29", "JADEF bait 120.30"),
        ("NETHERV bait 136.46", "NETHERF bait 137.47"),
        ("ash mist + stone ticks (V219-only)", "ash mist + stone ticks (V220-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD219 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v219_themes.json").read_text(encoding="utf-8"))["themes"])
NEW220 = "_".join(t[0] for t in T220)

out = (S / "c1421_vision_v219_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1421", "C1427"), ("c1421", "c1427"), ("V219", "V220"), ("v219", "v220"),
    ("_v219c1421", "_v220c1427"),
    ("Harder than V218", "Harder than V219"), ("harder than V218", "harder than V219"),
    (OLD219, NEW220),
    ("V219 keeps floor", "V220 keeps floor"),
    ("C1421 design+fixtures; no VL claim", "C1427 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1422 VL smoke", "fixtures only; claim deferred to C1428 VL smoke"),
    ("No claim until C1422 VL", "No claim until C1428 VL"),
    ("kept on V219", "kept on V220"),
    ("vision_images_v219", "vision_images_v220"),
    ("VL_GATE_V219", "VL_GATE_V220"), ("vl_gate_v219", "vl_gate_v220"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V218:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V219: ashford, cedarford, dawnford, elmford, fernford, glenford, hazeford, inkford,\njadeford, knotford, lakeford, mossford, netherford, oakford, pineford, quillford, reedford, stoneford.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T220, "v220", "V220", TR220))
out = retarget_220(out)
(S / "c1427_vision_v220_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1422_vision_v219_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1422", "C1428"), ("c1422", "c1428"), ("V219", "V220"), ("v219", "v220"),
    ("vision_images_v219", "vision_images_v220"),
    ("VL_GATE_V219", "VL_GATE_V220"), ("vl_gate_v219", "vl_gate_v220"),
    ("runs/vision_v219", "runs/vision_v220"),
]:
    out = out.replace(a, b)
(S / "c1428_vision_v220_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1423_vision_v219_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1423", "C1429"), ("c1423", "c1429"), ("V219", "V220"), ("v219", "v220"),
    ("vision_images_v219h", "vision_images_v220h"),
    ("vision_images_v219", "vision_images_v220"),
    ("VL_GATE_V219", "VL_GATE_V220"), ("vl_gate_v219", "vl_gate_v220"),
    ("runs/vision_v219h", "runs/vision_v220h"),
    ("_v219c1421", "_v220c1427"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T220, "v220h", "V220H", HO220))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v220h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v220"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v220" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v220h_c1429"'); seen_run = True; continue
    out2.append(ln)
(S / "c1429_vision_v220_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1418_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C1418", "C1430"), ("c1418", "c1430"),
    ("product_u2c_c1418", "product_u2c_c1430"),
]:
    out = out.replace(a, b)
(S / "c1430_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c1425_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1425", "C1431"), ("c1425", "c1431"),
    ("capture_regression_c1425", "capture_regression_c1431"),
    ("after C1421-C1424", "after C1427-C1430"),
    ("V4-V219+heldout", "V4-V220+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V219", DOC / "C1422_VISION_V219_SMOKE.json"),'
if needle in out and "VISION_V220_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V220", DOC / "C1428_VISION_V220_SMOKE.json"),\n    ("V220_heldout", DOC / "C1429_VISION_V220_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1431_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1420_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1420", "C1432"), ("c1420", "c1432"),
    ("C1416", "C1428"), ("C1417", "C1429"), ("C1419", "C1431"),
    ("C1415", "C1427"), ("C1418", "C1430"),
    ("V218", "V220"), ("v218", "v220"),
    ("V217", "V219"), ("v217", "v219"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C1412_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1424_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace('"source": "C1412"', '"source": "C1424"')
out = out.replace(
    'f"- confidence-gate (prior C1412): pass={conf_pass} rate={conf_rate}"',
    'f"- confidence-gate (prior C1424): pass={conf_pass} rate={conf_rate}"',
)
out = out.replace("C1415-C1420", "C1427-C1432")
out = out.replace("C1415-C1419", "C1427-C1431")
(S / "c1432_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T220 if t[0].endswith("b")])
print("qty", TR220[1], HO220[1], "po", TR220[8], HO220[8], "sla", TR220[6], HO220[6], "stack", TR220[14], HO220[14], "fax", TR220[15], HO220[15])
print("done")
