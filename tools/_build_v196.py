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

# *dale ; qty TR 740+780 HO 840+760; PO TR 780+740 HO 840+760; SLA TR 480+520 HO 360+400
T196 = [
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
TR196 = [
    [1357.0, 1374.5, 1167.0],[740, 780, 820],[1280.0, 1309.25, 1147.0],[1413.0, 1430.0, 1237.0],
    [1475.0, 1499.0, 1207.0],[1233, 1249, 1165],[480.0, 520.0, 710.0],[1323.0, 1354.75, 1171.0],
    [780.0, 740.0, 820.0],[1390.0, 1378.0, 1168.0],[1,1,0],[0,0,0],
    [1456.0, 1477.5, 1193.0],[1,0,0],[1005, 997, 975],[1023, 1007, 748],[1,0,0],[1049, 1025, 995],
]
HO196 = [
    [1227.0, 1239.75, 1120.0],[840, 760, 820],[1185.0, 1198.5, 1108.0],[1300.0, 1316.0, 1149.0],
    [1341.0, 1357.0, 1144.0],[1135, 1149, 1113],[360.0, 400.0, 700.0],[1211.0, 1232.75, 1120.0],
    [840.0, 760.0, 820.0],[1258.0, 1244.0, 1115.0],[1,1,0],[0,0,0],
    [1293.0, 1308.5, 1130.0],[1,0,0],[982, 977, 972],[997, 991, 979],[1,0,0],[1007, 1001, 980],
]
check(TR196, "TR"); check(HO196, "HO")

(ROOT / "tools/_v196_themes.json").write_text(json.dumps({"themes": T196, "train": TR196, "heldout": HO196}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_196(src):
    src = src.replace("# --- V195 overlays (new vs V50) ---", "# --- V196 overlays (new vs V50) ---")
    src = src.replace("# --- V195 overlays (new vs V49) ---", "# --- V196 overlays (new vs V49) ---")
    for a, b in [
        ("ASHBROOK bait 109.19", "ASHDALE bait 110.20"),
        ("CEDARB bait 111.21", "CEDARD bait 112.22"),
        ("DAWNB ghost 34.34", "DAWND ghost 35.35"),
        ("GLENB bait 104.14", "GLEND bait 105.15"),
        ("JADEB bait 95.95", "JADED bait 96.96"),
        ("NETHERB bait 112.22", "NETHERD bait 113.23"),
        ("ash mist + stone ticks (V195-only)", "ash mist + stone ticks (V196-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD195 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v195_themes.json").read_text(encoding="utf-8"))["themes"])
NEW196 = "_".join(t[0] for t in T196)

out = (S / "c1277_vision_v195_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1277", "C1283"), ("c1277", "c1283"), ("V195", "V196"), ("v195", "v196"),
    ("_v195c1277", "_v196c1283"),
    ("Harder than V194", "Harder than V195"), ("harder than V194", "harder than V195"),
    (OLD195, NEW196),
    ("V195 keeps floor", "V196 keeps floor"),
    ("C1277 design+fixtures; no VL claim", "C1283 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1278 VL smoke", "fixtures only; claim deferred to C1284 VL smoke"),
    ("No claim until C1278 VL", "No claim until C1284 VL"),
    ("kept on V195", "kept on V196"),
    ("vision_images_v195", "vision_images_v196"),
    ("VL_GATE_V195", "VL_GATE_V196"), ("vl_gate_v195", "vl_gate_v196"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V194:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V195: ashdale, cedardale, dawndale, elmdale, ferndale, glendale, hazedale, inkdale,\njadedale, knotdale, lakedale, mossdale, netherdale, oakdale, pinedale, quilldale, reeddale, stonedale.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T196, "v196", "V196", TR196))
out = retarget_196(out)
(S / "c1283_vision_v196_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1278_vision_v195_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1278", "C1284"), ("c1278", "c1284"), ("V195", "V196"), ("v195", "v196"),
    ("vision_images_v195", "vision_images_v196"),
    ("VL_GATE_V195", "VL_GATE_V196"), ("vl_gate_v195", "vl_gate_v196"),
    ("runs/vision_v195", "runs/vision_v196"),
]:
    out = out.replace(a, b)
(S / "c1284_vision_v196_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1279_vision_v195_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1279", "C1285"), ("c1279", "c1285"), ("V195", "V196"), ("v195", "v196"),
    ("vision_images_v195h", "vision_images_v196h"),
    ("vision_images_v195", "vision_images_v196"),
    ("VL_GATE_V195", "VL_GATE_V196"), ("vl_gate_v195", "vl_gate_v196"),
    ("runs/vision_v195h", "runs/vision_v196h"),
    ("_v195c1277", "_v196c1283"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T196, "v196h", "V196H", HO196))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v196h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v196"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v196" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v196h_c1285"'); seen_run = True; continue
    out2.append(ln)
(S / "c1285_vision_v196_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1274_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C1274", "C1286"), ("c1274", "c1286"),
    ("product_u2c_c1274", "product_u2c_c1286"),
    ("after V194", "after V196"), ("after V195", "after V196"),
]:
    out = out.replace(a, b)
(S / "c1286_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c1281_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1281", "C1287"), ("c1281", "c1287"),
    ("capture_regression_c1281", "capture_regression_c1287"),
    ("after C1277-C1280", "after C1283-C1286"),
    ("V4-V195+heldout", "V4-V196+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V195", DOC / "C1278_VISION_V195_SMOKE.json"),'
if needle in out and "VISION_V196_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V196", DOC / "C1284_VISION_V196_SMOKE.json"),\n    ("V196_heldout", DOC / "C1285_VISION_V196_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1287_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1276_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1276", "C1288"), ("c1276", "c1288"),
    ("C1272", "C1284"), ("C1273", "C1285"), ("C1275", "C1287"),
    ("C1271", "C1283"), ("C1274", "C1286"),
    ("V194", "V196"), ("v194", "v196"),
    ("V193", "V195"), ("v193", "v195"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C1268_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1280_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace('"source": "C1268"', '"source": "C1280"')
out = out.replace(
    'f"- confidence-gate (prior C1268): pass={conf_pass} rate={conf_rate}"',
    'f"- confidence-gate (prior C1280): pass={conf_pass} rate={conf_rate}"',
)
(S / "c1288_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T196 if t[0].endswith("b")])
print("qty", TR196[1], HO196[1], "po", TR196[8], HO196[8], "sla", TR196[6], HO196[6], "fax", TR196[15], HO196[15])
print("done")
