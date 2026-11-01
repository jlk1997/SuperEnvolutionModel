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
T186 = [
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
TR186 = [
    [1267.0, 1284.5, 1077.0],[740, 780, 820],[1190.0, 1219.25, 1057.0],[1323.0, 1340.0, 1147.0],
    [1385.0, 1409.0, 1117.0],[1143, 1159, 1075],[480.0, 520.0, 660.0],[1233.0, 1264.75, 1081.0],
    [780.0, 740.0, 820.0],[1300.0, 1288.0, 1078.0],[1,1,0],[0,0,0],
    [1366.0, 1387.5, 1103.0],[1,0,0],[915, 907, 885],[933, 917, 748],[1,0,0],[959, 935, 905],
]
HO186 = [
    [1137.0, 1149.75, 1030.0],[840, 760, 820],[1095.0, 1108.5, 1018.0],[1210.0, 1226.0, 1059.0],
    [1251.0, 1267.0, 1054.0],[1045, 1059, 1023],[360.0, 400.0, 600.0],[1121.0, 1142.75, 1030.0],
    [840.0, 760.0, 820.0],[1168.0, 1154.0, 1025.0],[1,1,0],[0,0,0],
    [1203.0, 1218.5, 1040.0],[1,0,0],[892, 887, 882],[907, 901, 889],[1,0,0],[917, 911, 890],
]
check(TR186, "TR"); check(HO186, "HO")

(ROOT / "tools/_v186_themes.json").write_text(json.dumps({"themes": T186, "train": TR186, "heldout": HO186}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_186(src):
    src = src.replace("# --- V185 overlays (new vs V50) ---", "# --- V186 overlays (new vs V50) ---")
    src = src.replace("# --- V185 overlays (new vs V49) ---", "# --- V186 overlays (new vs V49) ---")
    for a, b in [
        ("ASHDALE bait 99.99", "ASHVALE bait 100.10"),
        ("CEDARD bait 101.11", "CEDARV bait 102.12"),
        ("DAWND ghost 24.24", "DAWNV ghost 25.25"),
        ("GLEND bait 94.94", "GLENV bait 95.95"),
        ("JADED bait 85.85", "JADEV bait 86.86"),
        ("NETHERD bait 102.12", "NETHERV bait 103.13"),
        ("ash mist + stone ticks (V185-only)", "ash mist + stone ticks (V186-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD185 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v185_themes.json").read_text(encoding="utf-8"))["themes"])
NEW186 = "_".join(t[0] for t in T186)

out = (S / "c1217_vision_v185_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1217", "C1223"), ("c1217", "c1223"), ("V185", "V186"), ("v185", "v186"),
    ("_v185c1217", "_v186c1223"),
    ("Harder than V184", "Harder than V185"), ("harder than V184", "harder than V185"),
    (OLD185, NEW186),
    ("V185 keeps floor", "V186 keeps floor"),
    ("C1217 design+fixtures; no VL claim", "C1223 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1218 VL smoke", "fixtures only; claim deferred to C1224 VL smoke"),
    ("No claim until C1218 VL", "No claim until C1224 VL"),
    ("kept on V185", "kept on V186"),
    ("vision_images_v185", "vision_images_v186"),
    ("VL_GATE_V185", "VL_GATE_V186"), ("vl_gate_v185", "vl_gate_v186"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V184:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V185: ashvale, cedarvale, dawnvale, elmvale, fernvale, glenvale, hazevale, inkvale,\njadevale, knotvale, lakevale, mossvale, nethervale, oakvale, pinevale, quillvale, reedvale, stonevale.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T186, "v186", "V186", TR186))
out = retarget_186(out)
(S / "c1223_vision_v186_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1218_vision_v185_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1218", "C1224"), ("c1218", "c1224"), ("V185", "V186"), ("v185", "v186"),
    ("vision_images_v185", "vision_images_v186"),
    ("VL_GATE_V185", "VL_GATE_V186"), ("vl_gate_v185", "vl_gate_v186"),
    ("runs/vision_v185", "runs/vision_v186"),
]:
    out = out.replace(a, b)
(S / "c1224_vision_v186_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1219_vision_v185_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1219", "C1225"), ("c1219", "c1225"), ("V185", "V186"), ("v185", "v186"),
    ("vision_images_v185h", "vision_images_v186h"),
    ("vision_images_v185", "vision_images_v186"),
    ("VL_GATE_V185", "VL_GATE_V186"), ("vl_gate_v185", "vl_gate_v186"),
    ("runs/vision_v185h", "runs/vision_v186h"),
    ("_v185c1217", "_v186c1223"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T186, "v186h", "V186H", HO186))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v186h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v186"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v186" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v186h_c1225"'); seen_run = True; continue
    out2.append(ln)
(S / "c1225_vision_v186_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1214_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C1214", "C1226"), ("c1214", "c1226"),
    ("product_u2c_c1214", "product_u2c_c1226"),
    ("after V184", "after V186"), ("after V185", "after V186"),
]:
    out = out.replace(a, b)
(S / "c1226_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c1221_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1221", "C1227"), ("c1221", "c1227"),
    ("capture_regression_c1221", "capture_regression_c1227"),
    ("after C1217-C1220", "after C1223-C1226"),
    ("V4-V185+heldout", "V4-V186+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V185", DOC / "C1218_VISION_V185_SMOKE.json"),'
if needle in out and "VISION_V186_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V186", DOC / "C1224_VISION_V186_SMOKE.json"),\n    ("V186_heldout", DOC / "C1225_VISION_V186_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1227_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1216_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1216", "C1228"), ("c1216", "c1228"),
    ("C1212", "C1224"), ("C1213", "C1225"), ("C1215", "C1227"),
    ("C1211", "C1223"), ("C1214", "C1226"),
    ("V184", "V186"), ("v184", "v186"),
    ("V183", "V185"), ("v183", "v185"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C1208_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1220_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace('"source": "C1208"', '"source": "C1220"')
out = out.replace(
    'f"- confidence-gate (prior C1208): pass={conf_pass} rate={conf_rate}"',
    'f"- confidence-gate (prior C1220): pass={conf_pass} rate={conf_rate}"',
)
(S / "c1228_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T186 if t[0].endswith("b")])
print("qty", TR186[1], HO186[1], "po", TR186[8], HO186[8], "sla", TR186[6], HO186[6], "fax", TR186[15], HO186[15])
print("done")
