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

# *ford ; qty TR 740+780 HO 840+760; PO TR 780+740 HO 840+760; SLA TR 480+520 HO 360+400
T198 = [
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
TR198 = [
    [1375.0, 1392.5, 1185.0],[740, 780, 820],[1298.0, 1327.25, 1165.0],[1431.0, 1448.0, 1255.0],
    [1493.0, 1517.0, 1225.0],[1251, 1267, 1183],[480.0, 520.0, 730.0],[1341.0, 1372.75, 1189.0],
    [780.0, 740.0, 820.0],[1408.0, 1396.0, 1186.0],[1,1,0],[0,0,0],
    [1474.0, 1495.5, 1211.0],[1,0,0],[1023, 1015, 993],[1041, 1025, 748],[1,0,0],[1067, 1043, 1013],
]
HO198 = [
    [1245.0, 1257.75, 1138.0],[840, 760, 820],[1203.0, 1216.5, 1126.0],[1318.0, 1334.0, 1167.0],
    [1359.0, 1375.0, 1162.0],[1153, 1167, 1131],[360.0, 400.0, 720.0],[1229.0, 1250.75, 1138.0],
    [840.0, 760.0, 820.0],[1276.0, 1262.0, 1133.0],[1,1,0],[0,0,0],
    [1311.0, 1326.5, 1148.0],[1,0,0],[1000, 995, 990],[1015, 1009, 997],[1,0,0],[1025, 1019, 998],
]
check(TR198, "TR"); check(HO198, "HO")

(ROOT / "tools/_v198_themes.json").write_text(json.dumps({"themes": T198, "train": TR198, "heldout": HO198}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_198(src):
    src = src.replace("# --- V197 overlays (new vs V50) ---", "# --- V198 overlays (new vs V50) ---")
    src = src.replace("# --- V197 overlays (new vs V49) ---", "# --- V198 overlays (new vs V49) ---")
    for a, b in [
        ("ASHVALE bait 111.21", "ASHFORD bait 112.22"),
        ("CEDARV bait 113.23", "CEDARF bait 114.24"),
        ("DAWNV ghost 36.36", "DAWNF ghost 37.37"),
        ("GLENV bait 106.16", "GLENF bait 107.17"),
        ("JADEV bait 97.97", "JADEF bait 98.98"),
        ("NETHERV bait 114.24", "NETHERF bait 115.25"),
        ("ash mist + stone ticks (V197-only)", "ash mist + stone ticks (V198-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD197 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v197_themes.json").read_text(encoding="utf-8"))["themes"])
NEW198 = "_".join(t[0] for t in T198)

out = (S / "c1289_vision_v197_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1289", "C1295"), ("c1289", "c1295"), ("V197", "V198"), ("v197", "v198"),
    ("_v197c1289", "_v198c1295"),
    ("Harder than V196", "Harder than V197"), ("harder than V196", "harder than V197"),
    (OLD197, NEW198),
    ("V197 keeps floor", "V198 keeps floor"),
    ("C1289 design+fixtures; no VL claim", "C1295 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1290 VL smoke", "fixtures only; claim deferred to C1296 VL smoke"),
    ("No claim until C1290 VL", "No claim until C1296 VL"),
    ("kept on V197", "kept on V198"),
    ("vision_images_v197", "vision_images_v198"),
    ("VL_GATE_V197", "VL_GATE_V198"), ("vl_gate_v197", "vl_gate_v198"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V196:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V197: ashford, cedarford, dawnford, elmford, fernford, glenford, hazeford, inkford,\njadeford, knotford, lakeford, mossford, netherford, oakford, pineford, quillford, reedford, stoneford.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T198, "v198", "V198", TR198))
out = retarget_198(out)
(S / "c1295_vision_v198_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1290_vision_v197_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1290", "C1296"), ("c1290", "c1296"), ("V197", "V198"), ("v197", "v198"),
    ("vision_images_v197", "vision_images_v198"),
    ("VL_GATE_V197", "VL_GATE_V198"), ("vl_gate_v197", "vl_gate_v198"),
    ("runs/vision_v197", "runs/vision_v198"),
]:
    out = out.replace(a, b)
(S / "c1296_vision_v198_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1291_vision_v197_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1291", "C1297"), ("c1291", "c1297"), ("V197", "V198"), ("v197", "v198"),
    ("vision_images_v197h", "vision_images_v198h"),
    ("vision_images_v197", "vision_images_v198"),
    ("VL_GATE_V197", "VL_GATE_V198"), ("vl_gate_v197", "vl_gate_v198"),
    ("runs/vision_v197h", "runs/vision_v198h"),
    ("_v197c1289", "_v198c1295"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T198, "v198h", "V198H", HO198))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v198h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v198"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v198" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v198h_c1297"'); seen_run = True; continue
    out2.append(ln)
(S / "c1297_vision_v198_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1286_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C1286", "C1298"), ("c1286", "c1298"),
    ("product_u2c_c1286", "product_u2c_c1298"),
    ("after V196", "after V198"), ("after V197", "after V198"),
]:
    out = out.replace(a, b)
(S / "c1298_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c1293_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1293", "C1299"), ("c1293", "c1299"),
    ("capture_regression_c1293", "capture_regression_c1299"),
    ("after C1289-C1292", "after C1295-C1298"),
    ("V4-V197+heldout", "V4-V198+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V197", DOC / "C1290_VISION_V197_SMOKE.json"),'
if needle in out and "VISION_V198_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V198", DOC / "C1296_VISION_V198_SMOKE.json"),\n    ("V198_heldout", DOC / "C1297_VISION_V198_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1299_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1288_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1288", "C1300"), ("c1288", "c1300"),
    ("C1284", "C1296"), ("C1285", "C1297"), ("C1287", "C1299"),
    ("C1283", "C1295"), ("C1286", "C1298"),
    ("V196", "V198"), ("v196", "v198"),
    ("V195", "V197"), ("v195", "v197"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C1280_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1292_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace('"source": "C1280"', '"source": "C1292"')
out = out.replace(
    'f"- confidence-gate (prior C1280): pass={conf_pass} rate={conf_rate}"',
    'f"- confidence-gate (prior C1292): pass={conf_pass} rate={conf_rate}"',
)
(S / "c1300_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T198 if t[0].endswith("b")])
print("qty", TR198[1], HO198[1], "po", TR198[8], HO198[8], "sla", TR198[6], HO198[6], "fax", TR198[15], HO198[15])
print("done")
