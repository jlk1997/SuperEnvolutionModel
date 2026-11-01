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

# *vale ; qty TR 740+780 HO 840+760; PO TR 780+740 HO 840+760; SLA TR 480+520 HO 360+400
T208 = [
    ["ashvale","recv","paid_total","ASHVALE GRAIN RECV","RECV","x"],
    ["cedarvale","wh","qty_sum","WH CEDARVALE BIN","RECV","x"],
    ["dawnvale","refund","refund_done","DAWNVALE PATCH REFUND","DONE","x"],
    ["elmvale","tax","tax_base_paid","ELMVALE TAX SLIP","TAX","x"],
    ["fernvale","pay","payroll_active","FERNVALE PAYROLL","PAY","x"],
    ["glenvale","ship","ship_ok","GLENVALE SHIP DOCK","SHIP","x"],
    ["hazevale","sla","sla_ok_hours","HAZEVALE SLA CARD","SLA","x"],
    ["inkvale","exp","exp_sum","INKVALE EXPENSE","EXP","x"],
    ["jadevale","po","po_open","JADEVALE PO SHEET","PO","x"],
    ["knotvale","order","order_paid","KNOTVALE ORDER","ORD","x"],
    ["lakevale","dup","dup_mark","LAKEVALE DUP MARK","DUP","x"],
    ["mossvale","zero","zero_check","MOSSVALE AIR ZERO","ZERO","x"],
    ["nethervale","ledger","ledger_net","NETHERVALE LEDGER","LED","x"],
    ["oakvale","ui","ui_ok","OAKVALE UI SCAN","UI","x"],
    ["pinevale","stack","stack_count","PINEVALE STACK","STK","x"],
    ["quillvale","fax","fax_pages","QUILLVALE FAX","FAX","x"],
    ["reedvale","glare","glare_ok","REEDVALE GLARE","GLR","x"],
    ["stonevale","tab","tab_index","STONEVALE TAB INDEX","TAB","x"],
]
TR208 = [
    [1465.0, 1482.5, 1275.0],[740, 780, 820],[1388.0, 1417.25, 1255.0],[1521.0, 1538.0, 1345.0],
    [1583.0, 1607.0, 1315.0],[1341, 1357, 1273],[480.0, 520.0, 710.0],[1431.0, 1462.75, 1279.0],
    [780.0, 740.0, 820.0],[1498.0, 1486.0, 1276.0],[1,1,0],[0,0,0],
    [1564.0, 1585.5, 1301.0],[1,0,0],[1113, 1105, 1083],[1131, 1115, 748],[1,0,0],[1157, 1133, 1103],
]
HO208 = [
    [1335.0, 1347.75, 1228.0],[840, 760, 820],[1293.0, 1306.5, 1216.0],[1408.0, 1424.0, 1257.0],
    [1449.0, 1465.0, 1252.0],[1243, 1257, 1221],[360.0, 400.0, 740.0],[1319.0, 1340.75, 1228.0],
    [840.0, 760.0, 820.0],[1366.0, 1352.0, 1223.0],[1,1,0],[0,0,0],
    [1401.0, 1416.5, 1238.0],[1,0,0],[1090, 1085, 1080],[1105, 1099, 1087],[1,0,0],[1115, 1109, 1088],
]
check(TR208, "TR"); check(HO208, "HO")

(ROOT / "tools/_v208_themes.json").write_text(json.dumps({"themes": T208, "train": TR208, "heldout": HO208}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_208(src):
    src = src.replace("# --- V207 overlays (new vs V50) ---", "# --- V208 overlays (new vs V50) ---")
    src = src.replace("# --- V207 overlays (new vs V49) ---", "# --- V208 overlays (new vs V49) ---")
    for a, b in [
        ("ASHDALE bait 121.31", "ASHVALE bait 122.32"),
        ("CEDARD bait 123.33", "CEDARV bait 124.34"),
        ("DAWND ghost 46.46", "DAWNV ghost 47.47"),
        ("GLEND bait 116.26", "GLENV bait 117.27"),
        ("JADED bait 107.17", "JADEV bait 108.18"),
        ("NETHERD bait 124.34", "NETHERV bait 125.35"),
        ("ash mist + stone ticks (V207-only)", "ash mist + stone ticks (V208-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD207 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v207_themes.json").read_text(encoding="utf-8"))["themes"])
NEW208 = "_".join(t[0] for t in T208)

out = (S / "c1349_vision_v207_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1349", "C1355"), ("c1349", "c1355"), ("V207", "V208"), ("v207", "v208"),
    ("_v207c1349", "_v208c1355"),
    ("Harder than V206", "Harder than V207"), ("harder than V206", "harder than V207"),
    (OLD207, NEW208),
    ("V207 keeps floor", "V208 keeps floor"),
    ("C1349 design+fixtures; no VL claim", "C1355 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1350 VL smoke", "fixtures only; claim deferred to C1356 VL smoke"),
    ("No claim until C1350 VL", "No claim until C1356 VL"),
    ("kept on V207", "kept on V208"),
    ("vision_images_v207", "vision_images_v208"),
    ("VL_GATE_V207", "VL_GATE_V208"), ("vl_gate_v207", "vl_gate_v208"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V206:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V207: ashvale, cedarvale, dawnvale, elmvale, fernvale, glenvale, hazevale, inkvale,\njadevale, knotvale, lakevale, mossvale, nethervale, oakvale, pinevale, quillvale, reedvale, stonevale.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T208, "v208", "V208", TR208))
out = retarget_208(out)
(S / "c1355_vision_v208_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1350_vision_v207_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1350", "C1356"), ("c1350", "c1356"), ("V207", "V208"), ("v207", "v208"),
    ("vision_images_v207", "vision_images_v208"),
    ("VL_GATE_V207", "VL_GATE_V208"), ("vl_gate_v207", "vl_gate_v208"),
    ("runs/vision_v207", "runs/vision_v208"),
]:
    out = out.replace(a, b)
(S / "c1356_vision_v208_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1351_vision_v207_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1351", "C1357"), ("c1351", "c1357"), ("V207", "V208"), ("v207", "v208"),
    ("vision_images_v207h", "vision_images_v208h"),
    ("vision_images_v207", "vision_images_v208"),
    ("VL_GATE_V207", "VL_GATE_V208"), ("vl_gate_v207", "vl_gate_v208"),
    ("runs/vision_v207h", "runs/vision_v208h"),
    ("_v207c1349", "_v208c1355"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T208, "v208h", "V208H", HO208))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v208h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v208"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v208" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v208h_c1357"'); seen_run = True; continue
    out2.append(ln)
(S / "c1357_vision_v208_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1346_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C1346", "C1358"), ("c1346", "c1358"),
    ("product_u2c_c1346", "product_u2c_c1358"),
    ("after V206", "after V208"), ("after V207", "after V208"),
]:
    out = out.replace(a, b)
(S / "c1358_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c1353_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1353", "C1359"), ("c1353", "c1359"),
    ("capture_regression_c1353", "capture_regression_c1359"),
    ("after C1349-C1352", "after C1355-C1358"),
    ("V4-V207+heldout", "V4-V208+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V207", DOC / "C1350_VISION_V207_SMOKE.json"),'
if needle in out and "VISION_V208_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V208", DOC / "C1356_VISION_V208_SMOKE.json"),\n    ("V208_heldout", DOC / "C1357_VISION_V208_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1359_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1348_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1348", "C1360"), ("c1348", "c1360"),
    ("C1344", "C1356"), ("C1345", "C1357"), ("C1347", "C1359"),
    ("C1343", "C1355"), ("C1346", "C1358"),
    ("V206", "V208"), ("v206", "v208"),
    ("V205", "V207"), ("v205", "v207"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C1340_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1352_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace('"source": "C1340"', '"source": "C1352"')
out = out.replace(
    'f"- confidence-gate (prior C1340): pass={conf_pass} rate={conf_rate}"',
    'f"- confidence-gate (prior C1352): pass={conf_pass} rate={conf_rate}"',
)
(S / "c1360_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T208 if t[0].endswith("b")])
print("qty", TR208[1], HO208[1], "po", TR208[8], HO208[8], "sla", TR208[6], HO208[6], "fax", TR208[15], HO208[15])
print("done")
