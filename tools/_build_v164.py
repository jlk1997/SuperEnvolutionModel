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

# *vale ; qty TR 740+780 HO 840+760; PO TR 780+740 HO 840+760; SLA TR 480+520 HO 360+400
T164 = [
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
TR164 = [
    [1069.0, 1086.5, 879.0],[740, 780, 740],[992.0, 1021.25, 859.0],[1125.0, 1142.0, 949.0],
    [1187.0, 1211.0, 919.0],[945, 961, 877],[480.0, 520.0, 430.0],[1035.0, 1066.75, 883.0],
    [780.0, 740.0, 680.0],[1102.0, 1090.0, 880.0],[1,1,0],[0,0,0],
    [1168.0, 1189.5, 905.0],[1,0,0],[717, 709, 687],[735, 719, 710],[1,0,0],[761, 737, 707],
]
HO164 = [
    [939.0, 951.75, 832.0],[840, 760, 790],[897.0, 910.5, 820.0],[1012.0, 1028.0, 861.0],
    [1053.0, 1069.0, 856.0],[847, 861, 825],[360.0, 400.0, 410.0],[923.0, 944.75, 832.0],
    [840.0, 760.0, 690.0],[970.0, 956.0, 827.0],[1,1,0],[0,0,0],
    [1005.0, 1020.5, 842.0],[1,0,0],[693, 690, 685],[709, 703, 691],[1,0,0],[719, 713, 692],
]
(ROOT / "tools/_v164_themes.json").write_text(json.dumps({"themes": T164, "train": TR164, "heldout": HO164}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_164(src):
    src = src.replace("# --- V163 overlays (new vs V50) ---", "# --- V164 overlays (new vs V50) ---")
    src = src.replace("# --- V163 overlays (new vs V49) ---", "# --- V164 overlays (new vs V49) ---")
    for a, b in [
        ("ASHDALE bait 77.77", "ASHVALE bait 78.78"),
        ("CEDARD bait 89.89", "CEDARV bait 80.80"),
        ("DAWND ghost 91.91", "DAWNV ghost 92.92"),
        ("GLEND bait 72.72", "GLENV bait 73.73"),
        ("JADED bait 63.63", "JADEV bait 64.64"),
        ("NETHERD bait 80.80", "NETHERV bait 81.81"),
        ("ash mist + stone ticks (V163-only)", "ash mist + stone ticks (V164-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD163 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v163_themes.json").read_text(encoding="utf-8"))["themes"])
NEW164 = "_".join(t[0] for t in T164)

out = (S / "c1085_vision_v163_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1085", "C1091"), ("c1085", "c1091"), ("V163", "V164"), ("v163", "v164"),
    ("_v163c1085", "_v164c1091"),
    ("Harder than V162", "Harder than V163"), ("harder than V162", "harder than V163"),
    (OLD163, NEW164),
    ("V163 keeps floor", "V164 keeps floor"),
    ("C1085 design+fixtures; no VL claim", "C1091 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1086 VL smoke", "fixtures only; claim deferred to C1092 VL smoke"),
    ("No claim until C1086 VL", "No claim until C1092 VL"),
    ("kept on V163", "kept on V164"),
    ("vision_images_v163", "vision_images_v164"),
    ("VL_GATE_V163", "VL_GATE_V164"), ("vl_gate_v163", "vl_gate_v164"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V162:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V163: ashvale, cedarvale, dawnvale, elmvale, fernvale, glenvale, hazevale, inkvale,\njadevale, knotvale, lakevale, mossvale, nethervale, oakvale, pinevale, quillvale, reedvale, stonevale.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T164, "v164", "V164", TR164))
out = retarget_164(out)
(S / "c1091_vision_v164_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1086_vision_v163_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1086", "C1092"), ("c1086", "c1092"), ("V163", "V164"), ("v163", "v164"),
    ("vision_images_v163", "vision_images_v164"),
    ("VL_GATE_V163", "VL_GATE_V164"), ("vl_gate_v163", "vl_gate_v164"),
    ("runs/vision_v163", "runs/vision_v164"),
]:
    out = out.replace(a, b)
(S / "c1092_vision_v164_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1087_vision_v163_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1087", "C1093"), ("c1087", "c1093"), ("V163", "V164"), ("v163", "v164"),
    ("vision_images_v163h", "vision_images_v164h"),
    ("vision_images_v163", "vision_images_v164"),
    ("VL_GATE_V163", "VL_GATE_V164"), ("vl_gate_v163", "vl_gate_v164"),
    ("runs/vision_v163h", "runs/vision_v164h"),
    ("_v163c1085", "_v164c1091"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T164, "v164h", "V164H", HO164))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v164h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v164"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v164" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v164h_c1093"'); seen_run = True; continue
    out2.append(ln)
(S / "c1093_vision_v164_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1082_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C1082", "C1094"), ("c1082", "c1094"),
    ("product_u2c_c1082", "product_u2c_c1094"),
    ("after V162", "after V164"), ("after V163", "after V164"),
]:
    out = out.replace(a, b)
(S / "c1094_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c")

out = (S / "c1089_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1089", "C1095"), ("c1089", "c1095"),
    ("capture_regression_c1089", "capture_regression_c1095"),
    ("after C1085-C1088", "after C1091-C1094"),
    ("V4-V163+heldout", "V4-V164+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V163", DOC / "C1086_VISION_V163_SMOKE.json"),'
if needle in out and "VISION_V164_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V164", DOC / "C1092_VISION_V164_SMOKE.json"),\n    ("V164_heldout", DOC / "C1093_VISION_V164_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1095_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1090_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1090", "C1096"), ("c1090", "c1096"),
    ("C1086", "C1092"), ("C1087", "C1093"), ("C1089", "C1095"),
    ("C1085", "C1091"),
    ("V163", "V164"), ("v163", "v164"),
    ("V162", "V163"), ("v162", "v163"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c650 = load("docs/r50/C1082_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1094_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'c656 = load("docs/r50/C1088_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1088_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace('"source": "C1082"', '"source": "C1094"')
out = out.replace('"source": "C1088"', '"source": "C1088"')
out = out.replace(
    "stage_ready = bool(v164_claim and v164h_claim and v164 >= GATE and v164h >= GATE and capture_pass and disjoint and conf_pass)",
    "stage_ready = bool(v164_claim and v164h_claim and v164 >= GATE and v164h >= GATE and capture_pass and disjoint and u2c_pass)",
)
out = out.replace(
    'f"- C1094: confidence-gate pass={conf_pass} rate={conf_rate}"',
    'f"- C1094: product-U2C replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- C1088: confidence-gate pass={conf_pass} rate={conf_rate}"',
    'f"- C1094: product-U2C replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- product-U2C (prior C1082): replace={replace} pass={u2c_pass}"',
    'f"- confidence-gate (prior C1088): pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- product-U2C (prior C1094): replace={replace} pass={u2c_pass}"',
    'f"- confidence-gate (prior C1088): pass={conf_pass} rate={conf_rate}"',
)
(S / "c1096_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T164 if t[0].endswith("b")])
print("qty", TR164[1], HO164[1], "po", TR164[8], HO164[8], "sla", TR164[6], HO164[6])
print("done")
