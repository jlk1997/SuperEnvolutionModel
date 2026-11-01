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

# *holm ; qty TR 740+780 HO 840+760; PO TR 780+740 HO 840+760; SLA TR 480+520 HO 360+400
T210 = [
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
TR210 = [
    [1483.0, 1500.5, 1293.0],[740, 780, 820],[1406.0, 1435.25, 1273.0],[1539.0, 1556.0, 1363.0],
    [1601.0, 1625.0, 1333.0],[1359, 1375, 1291],[480.0, 520.0, 730.0],[1449.0, 1480.75, 1297.0],
    [780.0, 740.0, 820.0],[1516.0, 1504.0, 1294.0],[1,1,0],[0,0,0],
    [1582.0, 1603.5, 1319.0],[1,0,0],[1131, 1123, 1101],[1149, 1133, 748],[1,0,0],[1175, 1151, 1121],
]
HO210 = [
    [1353.0, 1365.75, 1246.0],[840, 760, 820],[1311.0, 1324.5, 1234.0],[1426.0, 1442.0, 1275.0],
    [1467.0, 1483.0, 1270.0],[1261, 1275, 1239],[360.0, 400.0, 720.0],[1337.0, 1358.75, 1246.0],
    [840.0, 760.0, 820.0],[1384.0, 1370.0, 1241.0],[1,1,0],[0,0,0],
    [1419.0, 1434.5, 1256.0],[1,0,0],[1108, 1103, 1098],[1123, 1117, 1105],[1,0,0],[1133, 1127, 1106],
]
check(TR210, "TR"); check(HO210, "HO")

(ROOT / "tools/_v210_themes.json").write_text(json.dumps({"themes": T210, "train": TR210, "heldout": HO210}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_210(src):
    src = src.replace("# --- V209 overlays (new vs V50) ---", "# --- V210 overlays (new vs V50) ---")
    src = src.replace("# --- V209 overlays (new vs V49) ---", "# --- V210 overlays (new vs V49) ---")
    for a, b in [
        ("ASHFORD bait 123.33", "ASHHOLM bait 124.34"),
        ("CEDARF bait 125.35", "CEDARH bait 126.36"),
        ("DAWNF ghost 48.48", "DAWNH ghost 49.49"),
        ("GLENF bait 118.28", "GLENH bait 119.29"),
        ("JADEF bait 109.19", "JADEH bait 110.20"),
        ("NETHERF bait 126.36", "NETHERH bait 127.37"),
        ("ash mist + stone ticks (V209-only)", "ash mist + stone ticks (V210-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD209 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v209_themes.json").read_text(encoding="utf-8"))["themes"])
NEW210 = "_".join(t[0] for t in T210)

out = (S / "c1361_vision_v209_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1361", "C1367"), ("c1361", "c1367"), ("V209", "V210"), ("v209", "v210"),
    ("_v209c1361", "_v210c1367"),
    ("Harder than V208", "Harder than V209"), ("harder than V208", "harder than V209"),
    (OLD209, NEW210),
    ("V209 keeps floor", "V210 keeps floor"),
    ("C1361 design+fixtures; no VL claim", "C1367 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1362 VL smoke", "fixtures only; claim deferred to C1368 VL smoke"),
    ("No claim until C1362 VL", "No claim until C1368 VL"),
    ("kept on V209", "kept on V210"),
    ("vision_images_v209", "vision_images_v210"),
    ("VL_GATE_V209", "VL_GATE_V210"), ("vl_gate_v209", "vl_gate_v210"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V208:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V209: ashhholm, cedarholm, dawnholm, elmholm, fernholm, glenholm, hazeholm, inkholm,\njadeholm, knotholm, lakeholm, mossholm, netherholm, oakholm, pineholm, quillholm, reedholm, stoneholm.".replace("ashhholm", "ashholm"),
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T210, "v210", "V210", TR210))
out = retarget_210(out)
(S / "c1367_vision_v210_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1362_vision_v209_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1362", "C1368"), ("c1362", "c1368"), ("V209", "V210"), ("v209", "v210"),
    ("vision_images_v209", "vision_images_v210"),
    ("VL_GATE_V209", "VL_GATE_V210"), ("vl_gate_v209", "vl_gate_v210"),
    ("runs/vision_v209", "runs/vision_v210"),
]:
    out = out.replace(a, b)
(S / "c1368_vision_v210_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1363_vision_v209_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1363", "C1369"), ("c1363", "c1369"), ("V209", "V210"), ("v209", "v210"),
    ("vision_images_v209h", "vision_images_v210h"),
    ("vision_images_v209", "vision_images_v210"),
    ("VL_GATE_V209", "VL_GATE_V210"), ("vl_gate_v209", "vl_gate_v210"),
    ("runs/vision_v209h", "runs/vision_v210h"),
    ("_v209c1361", "_v210c1367"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T210, "v210h", "V210H", HO210))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v210h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v210"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v210" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v210h_c1369"'); seen_run = True; continue
    out2.append(ln)
(S / "c1369_vision_v210_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1358_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C1358", "C1370"), ("c1358", "c1370"),
    ("product_u2c_c1358", "product_u2c_c1370"),
    ("after V208", "after V210"), ("after V209", "after V210"),
]:
    out = out.replace(a, b)
(S / "c1370_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c1365_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1365", "C1371"), ("c1365", "c1371"),
    ("capture_regression_c1365", "capture_regression_c1371"),
    ("after C1361-C1364", "after C1367-C1370"),
    ("V4-V209+heldout", "V4-V210+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V209", DOC / "C1362_VISION_V209_SMOKE.json"),'
if needle in out and "VISION_V210_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V210", DOC / "C1368_VISION_V210_SMOKE.json"),\n    ("V210_heldout", DOC / "C1369_VISION_V210_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1371_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1360_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1360", "C1372"), ("c1360", "c1372"),
    ("C1356", "C1368"), ("C1357", "C1369"), ("C1359", "C1371"),
    ("C1355", "C1367"), ("C1358", "C1370"),
    ("V208", "V210"), ("v208", "v210"),
    ("V207", "V209"), ("v207", "v209"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C1352_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1364_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace('"source": "C1352"', '"source": "C1364"')
out = out.replace(
    'f"- confidence-gate (prior C1352): pass={conf_pass} rate={conf_rate}"',
    'f"- confidence-gate (prior C1364): pass={conf_pass} rate={conf_rate}"',
)
(S / "c1372_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T210 if t[0].endswith("b")])
print("qty", TR210[1], HO210[1], "po", TR210[8], HO210[8], "sla", TR210[6], HO210[6], "fax", TR210[15], HO210[15])
print("done")
