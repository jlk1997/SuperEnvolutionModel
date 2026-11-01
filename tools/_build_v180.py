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

# *croft ; qty TR 740+780 HO 840+760; PO TR 780+740 HO 840+760; SLA TR 510+550 HO 390+430
T180 = [
    ["ashcroft","recv","paid_total","ASHCROFT GRAIN RECV","RECV","x"],
    ["cedarcroft","wh","qty_sum","WH CEDARCROFT BIN","RECV","x"],
    ["dawncroft","refund","refund_done","DAWNCROFT PATCH REFUND","DONE","x"],
    ["elmcroft","tax","tax_base_paid","ELMCROFT TAX SLIP","TAX","x"],
    ["ferncroft","pay","payroll_active","FERNCROFT PAYROLL","PAY","x"],
    ["glencroft","ship","ship_ok","GLENCROFT SHIP DOCK","SHIP","x"],
    ["hazecroft","sla","sla_ok_hours","HAZECROFT SLA CARD","SLA","x"],
    ["inkcroft","exp","exp_sum","INKCROFT EXPENSE","EXP","x"],
    ["jadecroft","po","po_open","JADECROFT PO SHEET","PO","x"],
    ["knotcroft","order","order_paid","KNOTCROFT ORDER","ORD","x"],
    ["lakecroft","dup","dup_mark","LAKECROFT DUP MARK","DUP","x"],
    ["mosscroft","zero","zero_check","MOSSCROFT AIR ZERO","ZERO","x"],
    ["nethercroft","ledger","ledger_net","NETHERCROFT LEDGER","LED","x"],
    ["oakcroft","ui","ui_ok","OAKCROFT UI SCAN","UI","x"],
    ["pinecroft","stack","stack_count","PINECROFT STACK","STK","x"],
    ["quillcroft","fax","fax_pages","QUILLCROFT FAX","FAX","x"],
    ["reedcroft","glare","glare_ok","REEDCROFT GLARE","GLR","x"],
    ["stonecroft","tab","tab_index","STONECROFT TAB INDEX","TAB","x"],
]
TR180 = [
    [1213.0, 1230.5, 1023.0],[740, 780, 820],[1136.0, 1165.25, 1003.0],[1269.0, 1286.0, 1093.0],
    [1331.0, 1355.0, 1063.0],[1089, 1105, 1021],[510.0, 550.0, 590.0],[1179.0, 1210.75, 1027.0],
    [780.0, 740.0, 830.0],[1246.0, 1234.0, 1024.0],[1,1,0],[0,0,0],
    [1312.0, 1333.5, 1049.0],[1,0,0],[861, 853, 831],[879, 863, 748],[1,0,0],[905, 881, 851],
]
# PO closed line used 830 banned — scrub to 820
TR180[8] = [780.0, 740.0, 820.0]
# stack p3 831 ok; tabC 851 ok — check fax 748 hold
HO180 = [
    [1083.0, 1095.75, 976.0],[840, 760, 820],[1041.0, 1054.5, 964.0],[1156.0, 1172.0, 1005.0],
    [1197.0, 1213.0, 1000.0],[991, 1005, 969],[390.0, 430.0, 570.0],[1067.0, 1088.75, 976.0],
    [840.0, 760.0, 820.0],[1114.0, 1100.0, 971.0],[1,1,0],[0,0,0],
    [1149.0, 1164.5, 986.0],[1,0,0],[838, 833, 828],[853, 847, 835],[1,0,0],[863, 857, 836],
]
check(TR180, "TR"); check(HO180, "HO")

(ROOT / "tools/_v180_themes.json").write_text(json.dumps({"themes": T180, "train": TR180, "heldout": HO180}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_180(src):
    src = src.replace("# --- V179 overlays (new vs V50) ---", "# --- V180 overlays (new vs V50) ---")
    src = src.replace("# --- V179 overlays (new vs V49) ---", "# --- V180 overlays (new vs V49) ---")
    for a, b in [
        ("ASHWICK bait 93.93", "ASHCROFT bait 94.94"),
        ("CEDARW bait 95.95", "CEDARC bait 96.96"),
        ("DAWNW ghost 18.18", "DAWNC ghost 19.19"),
        ("GLENW bait 88.88", "GLENC bait 89.89"),
        ("JADEW bait 79.79", "JADEC bait 80.80"),
        ("NETHERW bait 96.96", "NETHERC bait 97.97"),
        ("ash mist + stone ticks (V179-only)", "ash mist + stone ticks (V180-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD179 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v179_themes.json").read_text(encoding="utf-8"))["themes"])
NEW180 = "_".join(t[0] for t in T180)

out = (S / "c1181_vision_v179_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1181", "C1187"), ("c1181", "c1187"), ("V179", "V180"), ("v179", "v180"),
    ("_v179c1181", "_v180c1187"),
    ("Harder than V178", "Harder than V179"), ("harder than V178", "harder than V179"),
    (OLD179, NEW180),
    ("V179 keeps floor", "V180 keeps floor"),
    ("C1181 design+fixtures; no VL claim", "C1187 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1182 VL smoke", "fixtures only; claim deferred to C1188 VL smoke"),
    ("No claim until C1182 VL", "No claim until C1188 VL"),
    ("kept on V179", "kept on V180"),
    ("vision_images_v179", "vision_images_v180"),
    ("VL_GATE_V179", "VL_GATE_V180"), ("vl_gate_v179", "vl_gate_v180"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V178:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V179: ashcroft, cedarcroft, dawncroft, elmcroft, ferncroft, glencroft, hazecroft, inkcroft,\njadecroft, knotcroft, lakecroft, mosscroft, nethercroft, oakcroft, pinecroft, quillcroft, reedcroft, stonecroft.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T180, "v180", "V180", TR180))
out = retarget_180(out)
(S / "c1187_vision_v180_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1182_vision_v179_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1182", "C1188"), ("c1182", "c1188"), ("V179", "V180"), ("v179", "v180"),
    ("vision_images_v179", "vision_images_v180"),
    ("VL_GATE_V179", "VL_GATE_V180"), ("vl_gate_v179", "vl_gate_v180"),
    ("runs/vision_v179", "runs/vision_v180"),
]:
    out = out.replace(a, b)
(S / "c1188_vision_v180_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1183_vision_v179_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1183", "C1189"), ("c1183", "c1189"), ("V179", "V180"), ("v179", "v180"),
    ("vision_images_v179h", "vision_images_v180h"),
    ("vision_images_v179", "vision_images_v180"),
    ("VL_GATE_V179", "VL_GATE_V180"), ("vl_gate_v179", "vl_gate_v180"),
    ("runs/vision_v179h", "runs/vision_v180h"),
    ("_v179c1181", "_v180c1187"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T180, "v180h", "V180H", HO180))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v180h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v180"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v180" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v180h_c1189"'); seen_run = True; continue
    out2.append(ln)
(S / "c1189_vision_v180_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1178_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C1178", "C1190"), ("c1178", "c1190"),
    ("product_u2c_c1178", "product_u2c_c1190"),
    ("after V178", "after V180"), ("after V179", "after V180"),
]:
    out = out.replace(a, b)
(S / "c1190_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c1185_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1185", "C1191"), ("c1185", "c1191"),
    ("capture_regression_c1185", "capture_regression_c1191"),
    ("after C1181-C1184", "after C1187-C1190"),
    ("V4-V179+heldout", "V4-V180+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V179", DOC / "C1182_VISION_V179_SMOKE.json"),'
if needle in out and "VISION_V180_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V180", DOC / "C1188_VISION_V180_SMOKE.json"),\n    ("V180_heldout", DOC / "C1189_VISION_V180_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1191_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1180_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1180", "C1192"), ("c1180", "c1192"),
    ("C1176", "C1188"), ("C1177", "C1189"), ("C1179", "C1191"),
    ("C1175", "C1187"), ("C1178", "C1190"),
    ("V178", "V180"), ("v178", "v180"),
    ("V177", "V179"), ("v177", "v179"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C1172_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1184_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace('"source": "C1172"', '"source": "C1184"')
out = out.replace(
    'f"- confidence-gate (prior C1172): pass={conf_pass} rate={conf_rate}"',
    'f"- confidence-gate (prior C1184): pass={conf_pass} rate={conf_rate}"',
)
(S / "c1192_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T180 if t[0].endswith("b")])
print("qty", TR180[1], HO180[1], "po", TR180[8], HO180[8], "sla", TR180[6], HO180[6], "fax", TR180[15], HO180[15])
print("done")
