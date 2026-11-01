# -*- coding: utf-8 -*-
from __future__ import annotations
import json, re
from pathlib import Path
ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"

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

# *croft ; qty TR 840+760 HO 740+780; PO TR 840+760 HO 780+740; SLA TR 460+500 HO 360+400
# avoid hold 830; avoid tab 770->750 traps; fax hold not 755
T169 = [
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
TR169 = [
    [1114.0, 1131.5, 924.0],[840, 760, 790],[1037.0, 1066.25, 904.0],[1170.0, 1187.0, 994.0],
    [1232.0, 1256.0, 964.0],[990, 1006, 922],[460.0, 500.0, 480.0],[1080.0, 1111.75, 928.0],
    [840.0, 760.0, 730.0],[1147.0, 1135.0, 925.0],[1,1,0],[0,0,0],
    [1213.0, 1234.5, 950.0],[1,0,0],[762, 754, 732],[780, 764, 748],[1,0,0],[806, 782, 752],
]
HO169 = [
    [984.0, 996.75, 877.0],[740, 780, 820],[942.0, 955.5, 865.0],[1057.0, 1073.0, 906.0],
    [1098.0, 1114.0, 901.0],[892, 906, 870],[360.0, 400.0, 460.0],[968.0, 989.75, 877.0],
    [780.0, 740.0, 710.0],[1015.0, 1001.0, 872.0],[1,1,0],[0,0,0],
    [1050.0, 1065.5, 887.0],[1,0,0],[738, 735, 730],[754, 748, 736],[1,0,0],[764, 758, 737],
]
(ROOT / "tools/_v169_themes.json").write_text(json.dumps({"themes": T169, "train": TR169, "heldout": HO169}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_169(src):
    src = src.replace("# --- V168 overlays (new vs V50) ---", "# --- V169 overlays (new vs V50) ---")
    src = src.replace("# --- V168 overlays (new vs V49) ---", "# --- V169 overlays (new vs V49) ---")
    for a, b in [
        ("ASHWICK bait 82.82", "ASHCROFT bait 83.83"),
        ("CEDARW bait 84.84", "CEDARC bait 85.85"),
        ("DAWNW ghost 96.96", "DAWNC ghost 97.97"),
        ("GLENW bait 77.77", "GLENC bait 78.78"),
        ("JADEW bait 68.68", "JADEC bait 69.69"),
        ("NETHERW bait 85.85", "NETHERC bait 86.86"),
        ("ash mist + stone ticks (V168-only)", "ash mist + stone ticks (V169-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD168 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v168_themes.json").read_text(encoding="utf-8"))["themes"])
NEW169 = "_".join(t[0] for t in T169)

out = (S / "c1115_vision_v168_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1115", "C1121"), ("c1115", "c1121"), ("V168", "V169"), ("v168", "v169"),
    ("_v168c1115", "_v169c1121"),
    ("Harder than V167", "Harder than V168"), ("harder than V167", "harder than V168"),
    (OLD168, NEW169),
    ("V168 keeps floor", "V169 keeps floor"),
    ("C1115 design+fixtures; no VL claim", "C1121 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1116 VL smoke", "fixtures only; claim deferred to C1122 VL smoke"),
    ("No claim until C1116 VL", "No claim until C1122 VL"),
    ("kept on V168", "kept on V169"),
    ("vision_images_v168", "vision_images_v169"),
    ("VL_GATE_V168", "VL_GATE_V169"), ("vl_gate_v168", "vl_gate_v169"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V167:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V168: ashcroft, cedarcroft, dawncroft, elmcroft, ferncroft, glencroft, hazecroft, inkcroft,\njadecroft, knotcroft, lakecroft, mosscroft, nethercroft, oakcroft, pinecroft, quillcroft, reedcroft, stonecroft.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T169, "v169", "V169", TR169))
out = retarget_169(out)
(S / "c1121_vision_v169_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1116_vision_v168_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1116", "C1122"), ("c1116", "c1122"), ("V168", "V169"), ("v168", "v169"),
    ("vision_images_v168", "vision_images_v169"),
    ("VL_GATE_V168", "VL_GATE_V169"), ("vl_gate_v168", "vl_gate_v169"),
    ("runs/vision_v168", "runs/vision_v169"),
]:
    out = out.replace(a, b)
(S / "c1122_vision_v169_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1117_vision_v168_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1117", "C1123"), ("c1117", "c1123"), ("V168", "V169"), ("v168", "v169"),
    ("vision_images_v168h", "vision_images_v169h"),
    ("vision_images_v168", "vision_images_v169"),
    ("VL_GATE_V168", "VL_GATE_V169"), ("vl_gate_v168", "vl_gate_v169"),
    ("runs/vision_v168h", "runs/vision_v169h"),
    ("_v168c1115", "_v169c1121"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T169, "v169h", "V169H", HO169))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v169h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v169"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v169" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v169h_c1123"'); seen_run = True; continue
    out2.append(ln)
(S / "c1123_vision_v169_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1112_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1112", "C1124"), ("c1112", "c1124"),
    ("conf_gate_stretch_c1112", "conf_gate_stretch_c1124"),
    ("after V167", "after V169"), ("after V168", "after V169"),
    ("cg85_", "cg86_"),
]:
    out = out.replace(a, b)
(S / "c1124_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence")

out = (S / "c1119_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1119", "C1125"), ("c1119", "c1125"),
    ("capture_regression_c1119", "capture_regression_c1125"),
    ("after C1115-C1118", "after C1121-C1124"),
    ("V4-V168+heldout", "V4-V169+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V168", DOC / "C1116_VISION_V168_SMOKE.json"),'
if needle in out and "VISION_V169_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V169", DOC / "C1122_VISION_V169_SMOKE.json"),\n    ("V169_heldout", DOC / "C1123_VISION_V169_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1125_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1120_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1120", "C1126"), ("c1120", "c1126"),
    ("C1116", "C1122"), ("C1117", "C1123"), ("C1119", "C1125"),
    ("C1115", "C1121"),
    ("V168", "V169"), ("v168", "v169"),
    ("V167", "V168"), ("v167", "v168"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C1112_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1124_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C1118_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1118_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace('"source": "C1118"', '"source": "C1118"')
out = out.replace('"source": "C1112"', '"source": "C1124"')
out = out.replace(
    "stage_ready = bool(v169_claim and v169h_claim and v169 >= GATE and v169h >= GATE and capture_pass and disjoint and u2c_pass)",
    "stage_ready = bool(v169_claim and v169h_claim and v169 >= GATE and v169h >= GATE and capture_pass and disjoint and conf_pass)",
)
out = out.replace(
    'f"- C1124: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C1124: confidence-gate pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- C1118: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C1124: confidence-gate pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- confidence-gate (prior C1112): pass={conf_pass} rate={conf_rate}"',
    'f"- product-U2C (prior C1118): replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- confidence-gate (prior C1124): pass={conf_pass} rate={conf_rate}"',
    'f"- product-U2C (prior C1118): replace={replace} pass={u2c_pass}"',
)
(S / "c1126_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T169 if t[0].endswith("b")])
print("qty", TR169[1], HO169[1], "po", TR169[8], HO169[8], "sla", TR169[6], HO169[6])
print("done")
