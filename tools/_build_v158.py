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

# *croft ; qty TR 740+780 HO 840+760; PO TR 780+740 HO 840+760; SLA TR 480+520 HO 360+400
T158 = [
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
TR158 = [
    [1015.0, 1032.5, 825.0],[740, 780, 680],[938.0, 967.25, 805.0],[1071.0, 1088.0, 895.0],
    [1133.0, 1157.0, 865.0],[891, 907, 823],[480.0, 520.0, 370.0],[981.0, 1012.75, 829.0],
    [780.0, 740.0, 710.0],[1048.0, 1036.0, 826.0],[1,1,0],[0,0,0],
    [1114.0, 1135.5, 851.0],[1,0,0],[663, 655, 633],[681, 665, 656],[1,0,0],[707, 683, 653],
]
HO158 = [
    [885.0, 897.75, 778.0],[840, 760, 740],[843.0, 856.5, 766.0],[958.0, 974.0, 807.0],
    [999.0, 1015.0, 802.0],[793, 807, 771],[360.0, 400.0, 350.0],[869.0, 890.75, 778.0],
    [840.0, 760.0, 720.0],[916.0, 902.0, 773.0],[1,1,0],[0,0,0],
    [951.0, 966.5, 788.0],[1,0,0],[639, 636, 631],[655, 649, 637],[1,0,0],[665, 659, 638],
]
(ROOT / "tools/_v158_themes.json").write_text(json.dumps({"themes": T158, "train": TR158, "heldout": HO158}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_158(src):
    src = src.replace("# --- V157 overlays (new vs V50) ---", "# --- V158 overlays (new vs V50) ---")
    src = src.replace("# --- V157 overlays (new vs V49) ---", "# --- V158 overlays (new vs V49) ---")
    for a, b in [
        ("ASHWICK bait 71.71", "ASHCROFT bait 72.72"),
        ("CEDARW bait 83.83", "CEDARC bait 84.84"),
        ("DAWNW ghost 95.95", "DAWNC ghost 96.96"),
        ("GLENW bait 76.76", "GLENC bait 77.77"),
        ("JADEW bait 67.67", "JADEC bait 68.68"),
        ("NETHERW bait 84.84", "NETHERC bait 85.85"),
        ("ash mist + stone ticks (V157-only)", "ash mist + stone ticks (V158-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD157 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v157_themes.json").read_text(encoding="utf-8"))["themes"])
NEW158 = "_".join(t[0] for t in T158)

out = (S / "c1049_vision_v157_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1049", "C1055"), ("c1049", "c1055"), ("V157", "V158"), ("v157", "v158"),
    ("_v157c1049", "_v158c1055"),
    ("Harder than V156", "Harder than V157"), ("harder than V156", "harder than V157"),
    (OLD157, NEW158),
    ("V157 keeps floor", "V158 keeps floor"),
    ("C1049 design+fixtures; no VL claim", "C1055 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1050 VL smoke", "fixtures only; claim deferred to C1056 VL smoke"),
    ("No claim until C1050 VL", "No claim until C1056 VL"),
    ("kept on V157", "kept on V158"),
    ("vision_images_v157", "vision_images_v158"),
    ("VL_GATE_V157", "VL_GATE_V158"), ("vl_gate_v157", "vl_gate_v158"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V156:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V157: ashcroft, cedarcroft, dawncroft, elmcroft, ferncroft, glencroft, hazecroft, inkcroft,\njadecroft, knotcroft, lakecroft, mosscroft, nethercroft, oakcroft, pinecroft, quillcroft, reedcroft, stonecroft.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T158, "v158", "V158", TR158))
out = retarget_158(out)
(S / "c1055_vision_v158_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1050_vision_v157_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1050", "C1056"), ("c1050", "c1056"), ("V157", "V158"), ("v157", "v158"),
    ("vision_images_v157", "vision_images_v158"),
    ("VL_GATE_V157", "VL_GATE_V158"), ("vl_gate_v157", "vl_gate_v158"),
    ("runs/vision_v157", "runs/vision_v158"),
]:
    out = out.replace(a, b)
(S / "c1056_vision_v158_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1051_vision_v157_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1051", "C1057"), ("c1051", "c1057"), ("V157", "V158"), ("v157", "v158"),
    ("vision_images_v157h", "vision_images_v158h"),
    ("vision_images_v157", "vision_images_v158"),
    ("VL_GATE_V157", "VL_GATE_V158"), ("vl_gate_v157", "vl_gate_v158"),
    ("runs/vision_v157h", "runs/vision_v158h"),
    ("_v157c1049", "_v158c1055"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T158, "v158h", "V158H", HO158))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v158h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v158"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v158" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v158h_c1057"'); seen_run = True; continue
    out2.append(ln)
(S / "c1057_vision_v158_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1046_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C1046", "C1058"), ("c1046", "c1058"),
    ("product_u2c_c1046", "product_u2c_c1058"),
    ("after V156", "after V158"), ("after V157", "after V158"),
]:
    out = out.replace(a, b)
(S / "c1058_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c")

out = (S / "c1053_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1053", "C1059"), ("c1053", "c1059"),
    ("capture_regression_c1053", "capture_regression_c1059"),
    ("after C1049-C1052", "after C1055-C1058"),
    ("V4-V157+heldout", "V4-V158+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V157", DOC / "C1050_VISION_V157_SMOKE.json"),'
if needle in out and "VISION_V158_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V158", DOC / "C1056_VISION_V158_SMOKE.json"),\n    ("V158_heldout", DOC / "C1057_VISION_V158_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1059_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1054_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1054", "C1060"), ("c1054", "c1060"),
    ("C1050", "C1056"), ("C1051", "C1057"), ("C1053", "C1059"),
    ("C1049", "C1055"),
    ("V157", "V158"), ("v157", "v158"),
    ("V156", "V157"), ("v156", "v157"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c650 = load("docs/r50/C1046_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1058_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'c656 = load("docs/r50/C1052_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1052_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace('"source": "C1046"', '"source": "C1058"')
out = out.replace('"source": "C1052"', '"source": "C1052"')
out = out.replace(
    "stage_ready = bool(v158_claim and v158h_claim and v158 >= GATE and v158h >= GATE and capture_pass and disjoint and conf_pass)",
    "stage_ready = bool(v158_claim and v158h_claim and v158 >= GATE and v158h >= GATE and capture_pass and disjoint and u2c_pass)",
)
out = out.replace(
    'f"- C1058: confidence-gate pass={conf_pass} rate={conf_rate}"',
    'f"- C1058: product-U2C replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- C1052: confidence-gate pass={conf_pass} rate={conf_rate}"',
    'f"- C1058: product-U2C replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- product-U2C (prior C1046): replace={replace} pass={u2c_pass}"',
    'f"- confidence-gate (prior C1052): pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- product-U2C (prior C1058): replace={replace} pass={u2c_pass}"',
    'f"- confidence-gate (prior C1052): pass={conf_pass} rate={conf_rate}"',
)
(S / "c1060_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T158 if t[0].endswith("b")])
print("qty", TR158[1], HO158[1], "po", TR158[8], HO158[8], "sla", TR158[6], HO158[6])
print("done")
