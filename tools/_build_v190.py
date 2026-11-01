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

# *wick ; qty TR 740+780 HO 840+760; PO TR 780+740 HO 840+760; SLA TR 480+520 HO 360+400
T190 = [
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
TR190 = [
    [1303.0, 1320.5, 1113.0],[740, 780, 820],[1226.0, 1255.25, 1093.0],[1359.0, 1376.0, 1183.0],
    [1421.0, 1445.0, 1153.0],[1179, 1195, 1111],[480.0, 520.0, 700.0],[1269.0, 1300.75, 1117.0],
    [780.0, 740.0, 820.0],[1336.0, 1324.0, 1114.0],[1,1,0],[0,0,0],
    [1402.0, 1423.5, 1139.0],[1,0,0],[951, 943, 921],[969, 953, 748],[1,0,0],[995, 971, 941],
]
HO190 = [
    [1173.0, 1185.75, 1066.0],[840, 760, 820],[1131.0, 1144.5, 1054.0],[1246.0, 1262.0, 1095.0],
    [1287.0, 1303.0, 1090.0],[1081, 1095, 1059],[360.0, 400.0, 640.0],[1157.0, 1178.75, 1066.0],
    [840.0, 760.0, 820.0],[1204.0, 1190.0, 1061.0],[1,1,0],[0,0,0],
    [1239.0, 1254.5, 1076.0],[1,0,0],[928, 923, 918],[943, 937, 925],[1,0,0],[953, 947, 926],
]
check(TR190, "TR"); check(HO190, "HO")

(ROOT / "tools/_v190_themes.json").write_text(json.dumps({"themes": T190, "train": TR190, "heldout": HO190}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_190(src):
    src = src.replace("# --- V189 overlays (new vs V50) ---", "# --- V190 overlays (new vs V50) ---")
    src = src.replace("# --- V189 overlays (new vs V49) ---", "# --- V190 overlays (new vs V49) ---")
    for a, b in [
        ("ASHMERE bait 103.13", "ASHWICK bait 104.14"),
        ("CEDARM bait 105.15", "CEDARW bait 106.16"),
        ("DAWNM ghost 28.28", "DAWNW ghost 29.29"),
        ("GLENM bait 98.98", "GLENW bait 99.99"),
        ("JADEM bait 89.89", "JADEW bait 90.90"),
        ("NETHERM bait 106.16", "NETHERW bait 107.17"),
        ("ash mist + stone ticks (V189-only)", "ash mist + stone ticks (V190-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD189 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v189_themes.json").read_text(encoding="utf-8"))["themes"])
NEW190 = "_".join(t[0] for t in T190)

out = (S / "c1241_vision_v189_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1241", "C1247"), ("c1241", "c1247"), ("V189", "V190"), ("v189", "v190"),
    ("_v189c1241", "_v190c1247"),
    ("Harder than V188", "Harder than V189"), ("harder than V188", "harder than V189"),
    (OLD189, NEW190),
    ("V189 keeps floor", "V190 keeps floor"),
    ("C1241 design+fixtures; no VL claim", "C1247 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1242 VL smoke", "fixtures only; claim deferred to C1248 VL smoke"),
    ("No claim until C1242 VL", "No claim until C1248 VL"),
    ("kept on V189", "kept on V190"),
    ("vision_images_v189", "vision_images_v190"),
    ("VL_GATE_V189", "VL_GATE_V190"), ("vl_gate_v189", "vl_gate_v190"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V188:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V189: ashwick, cedarwick, dawnwick, elmwick, fernwick, glenwick, hazewick, inkwick,\njadewick, knotwick, lakewick, mosswick, netherwick, oakwick, pinewick, quillwick, reedwick, stonewick.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T190, "v190", "V190", TR190))
out = retarget_190(out)
(S / "c1247_vision_v190_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1242_vision_v189_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1242", "C1248"), ("c1242", "c1248"), ("V189", "V190"), ("v189", "v190"),
    ("vision_images_v189", "vision_images_v190"),
    ("VL_GATE_V189", "VL_GATE_V190"), ("vl_gate_v189", "vl_gate_v190"),
    ("runs/vision_v189", "runs/vision_v190"),
]:
    out = out.replace(a, b)
(S / "c1248_vision_v190_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1243_vision_v189_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1243", "C1249"), ("c1243", "c1249"), ("V189", "V190"), ("v189", "v190"),
    ("vision_images_v189h", "vision_images_v190h"),
    ("vision_images_v189", "vision_images_v190"),
    ("VL_GATE_V189", "VL_GATE_V190"), ("vl_gate_v189", "vl_gate_v190"),
    ("runs/vision_v189h", "runs/vision_v190h"),
    ("_v189c1241", "_v190c1247"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T190, "v190h", "V190H", HO190))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v190h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v190"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v190" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v190h_c1249"'); seen_run = True; continue
    out2.append(ln)
(S / "c1249_vision_v190_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1238_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C1238", "C1250"), ("c1238", "c1250"),
    ("product_u2c_c1238", "product_u2c_c1250"),
    ("after V188", "after V190"), ("after V189", "after V190"),
]:
    out = out.replace(a, b)
(S / "c1250_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c1245_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1245", "C1251"), ("c1245", "c1251"),
    ("capture_regression_c1245", "capture_regression_c1251"),
    ("after C1241-C1244", "after C1247-C1250"),
    ("V4-V189+heldout", "V4-V190+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V189", DOC / "C1242_VISION_V189_SMOKE.json"),'
if needle in out and "VISION_V190_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V190", DOC / "C1248_VISION_V190_SMOKE.json"),\n    ("V190_heldout", DOC / "C1249_VISION_V190_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1251_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1240_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1240", "C1252"), ("c1240", "c1252"),
    ("C1236", "C1248"), ("C1237", "C1249"), ("C1239", "C1251"),
    ("C1235", "C1247"), ("C1238", "C1250"),
    ("V188", "V190"), ("v188", "v190"),
    ("V187", "V189"), ("v187", "v189"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C1232_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1244_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace('"source": "C1232"', '"source": "C1244"')
out = out.replace(
    'f"- confidence-gate (prior C1232): pass={conf_pass} rate={conf_rate}"',
    'f"- confidence-gate (prior C1244): pass={conf_pass} rate={conf_rate}"',
)
(S / "c1252_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T190 if t[0].endswith("b")])
print("qty", TR190[1], HO190[1], "po", TR190[8], HO190[8], "sla", TR190[6], HO190[6], "fax", TR190[15], HO190[15])
print("done")
