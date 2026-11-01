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

# *moor ; qty TR 740+780 HO 840+760; PO TR 780+740 HO 840+760; SLA TR 480+520 HO 360+400
T160 = [
    ["ashmoor","recv","paid_total","ASHMOOR GRAIN RECV","RECV","x"],
    ["cedarmoor","wh","qty_sum","WH CEDARMOOR BIN","RECV","x"],
    ["dawnmoor","refund","refund_done","DAWNMOOR PATCH REFUND","DONE","x"],
    ["elmmoor","tax","tax_base_paid","ELMMOOR TAX SLIP","TAX","x"],
    ["fernmoor","pay","payroll_active","FERNMOOR PAYROLL","PAY","x"],
    ["glenmoor","ship","ship_ok","GLENMOOR SHIP DOCK","SHIP","x"],
    ["hazemoor","sla","sla_ok_hours","HAZEMOOR SLA CARD","SLA","x"],
    ["inkmoor","exp","exp_sum","INKMOOR EXPENSE","EXP","x"],
    ["jademoor","po","po_open","JADEMOOR PO SHEET","PO","x"],
    ["knotmoor","order","order_paid","KNOTMOOR ORDER","ORD","x"],
    ["lakemoor","dup","dup_mark","LAKEMOOR DUP MARK","DUP","x"],
    ["mossmoor","zero","zero_check","MOSSMOOR AIR ZERO","ZERO","x"],
    ["nethermoor","ledger","ledger_net","NETHERMOOR LEDGER","LED","x"],
    ["oakmoor","ui","ui_ok","OAKMOOR UI SCAN","UI","x"],
    ["pinemoor","stack","stack_count","PINEMOOR STACK","STK","x"],
    ["quillmoor","fax","fax_pages","QUILLMOOR FAX","FAX","x"],
    ["reedmoor","glare","glare_ok","REEDMOOR GLARE","GLR","x"],
    ["stonemoor","tab","tab_index","STONEMOOR TAB INDEX","TAB","x"],
]
TR160 = [
    [1033.0, 1050.5, 843.0],[740, 780, 700],[956.0, 985.25, 823.0],[1089.0, 1106.0, 913.0],
    [1151.0, 1175.0, 883.0],[909, 925, 841],[480.0, 520.0, 390.0],[999.0, 1030.75, 847.0],
    [780.0, 740.0, 700.0],[1066.0, 1054.0, 844.0],[1,1,0],[0,0,0],
    [1132.0, 1153.5, 869.0],[1,0,0],[681, 673, 651],[699, 683, 674],[1,0,0],[725, 701, 671],
]
HO160 = [
    [903.0, 915.75, 796.0],[840, 760, 750],[861.0, 874.5, 784.0],[976.0, 992.0, 825.0],
    [1017.0, 1033.0, 820.0],[811, 825, 789],[360.0, 400.0, 370.0],[887.0, 908.75, 796.0],
    [840.0, 760.0, 710.0],[934.0, 920.0, 791.0],[1,1,0],[0,0,0],
    [969.0, 984.5, 806.0],[1,0,0],[657, 654, 649],[673, 667, 655],[1,0,0],[683, 677, 656],
]
(ROOT / "tools/_v160_themes.json").write_text(json.dumps({"themes": T160, "train": TR160, "heldout": HO160}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_160(src):
    src = src.replace("# --- V159 overlays (new vs V50) ---", "# --- V160 overlays (new vs V50) ---")
    src = src.replace("# --- V159 overlays (new vs V49) ---", "# --- V160 overlays (new vs V49) ---")
    for a, b in [
        ("ASHHURST bait 73.73", "ASHMOOR bait 74.74"),
        ("CEDARH bait 85.85", "CEDARM bait 86.86"),
        ("DAWNH ghost 97.97", "DAWNM ghost 98.98"),
        ("GLENH bait 78.78", "GLENM bait 79.79"),
        ("JADEH bait 69.69", "JADEM bait 60.60"),
        ("NETHERH bait 86.86", "NETHERM bait 87.87"),
        ("ash mist + stone ticks (V159-only)", "ash mist + stone ticks (V160-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD159 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v159_themes.json").read_text(encoding="utf-8"))["themes"])
NEW160 = "_".join(t[0] for t in T160)

out = (S / "c1061_vision_v159_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1061", "C1067"), ("c1061", "c1067"), ("V159", "V160"), ("v159", "v160"),
    ("_v159c1061", "_v160c1067"),
    ("Harder than V158", "Harder than V159"), ("harder than V158", "harder than V159"),
    (OLD159, NEW160),
    ("V159 keeps floor", "V160 keeps floor"),
    ("C1061 design+fixtures; no VL claim", "C1067 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1062 VL smoke", "fixtures only; claim deferred to C1068 VL smoke"),
    ("No claim until C1062 VL", "No claim until C1068 VL"),
    ("kept on V159", "kept on V160"),
    ("vision_images_v159", "vision_images_v160"),
    ("VL_GATE_V159", "VL_GATE_V160"), ("vl_gate_v159", "vl_gate_v160"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V158:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V159: ashmoor, cedarmoor, dawnmoor, elmmoor, fernmoor, glenmoor, hazemoor, inkmoor,\njademoor, knotmoor, lakemoor, mossmoor, nethermoor, oakmoor, pinemoor, quillmoor, reedmoor, stonemoor.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T160, "v160", "V160", TR160))
out = retarget_160(out)
(S / "c1067_vision_v160_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1062_vision_v159_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1062", "C1068"), ("c1062", "c1068"), ("V159", "V160"), ("v159", "v160"),
    ("vision_images_v159", "vision_images_v160"),
    ("VL_GATE_V159", "VL_GATE_V160"), ("vl_gate_v159", "vl_gate_v160"),
    ("runs/vision_v159", "runs/vision_v160"),
]:
    out = out.replace(a, b)
(S / "c1068_vision_v160_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1063_vision_v159_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1063", "C1069"), ("c1063", "c1069"), ("V159", "V160"), ("v159", "v160"),
    ("vision_images_v159h", "vision_images_v160h"),
    ("vision_images_v159", "vision_images_v160"),
    ("VL_GATE_V159", "VL_GATE_V160"), ("vl_gate_v159", "vl_gate_v160"),
    ("runs/vision_v159h", "runs/vision_v160h"),
    ("_v159c1061", "_v160c1067"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T160, "v160h", "V160H", HO160))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v160h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v160"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v160" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v160h_c1069"'); seen_run = True; continue
    out2.append(ln)
(S / "c1069_vision_v160_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1058_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C1058", "C1070"), ("c1058", "c1070"),
    ("product_u2c_c1058", "product_u2c_c1070"),
    ("after V158", "after V160"), ("after V159", "after V160"),
]:
    out = out.replace(a, b)
(S / "c1070_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c")

out = (S / "c1065_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1065", "C1071"), ("c1065", "c1071"),
    ("capture_regression_c1065", "capture_regression_c1071"),
    ("after C1061-C1064", "after C1067-C1070"),
    ("V4-V159+heldout", "V4-V160+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V159", DOC / "C1062_VISION_V159_SMOKE.json"),'
if needle in out and "VISION_V160_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V160", DOC / "C1068_VISION_V160_SMOKE.json"),\n    ("V160_heldout", DOC / "C1069_VISION_V160_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1071_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1066_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1066", "C1072"), ("c1066", "c1072"),
    ("C1062", "C1068"), ("C1063", "C1069"), ("C1065", "C1071"),
    ("C1061", "C1067"),
    ("V159", "V160"), ("v159", "v160"),
    ("V158", "V159"), ("v158", "v159"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c650 = load("docs/r50/C1058_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1070_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'c656 = load("docs/r50/C1064_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1064_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace('"source": "C1058"', '"source": "C1070"')
out = out.replace('"source": "C1064"', '"source": "C1064"')
out = out.replace(
    "stage_ready = bool(v160_claim and v160h_claim and v160 >= GATE and v160h >= GATE and capture_pass and disjoint and conf_pass)",
    "stage_ready = bool(v160_claim and v160h_claim and v160 >= GATE and v160h >= GATE and capture_pass and disjoint and u2c_pass)",
)
out = out.replace(
    'f"- C1070: confidence-gate pass={conf_pass} rate={conf_rate}"',
    'f"- C1070: product-U2C replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- C1064: confidence-gate pass={conf_pass} rate={conf_rate}"',
    'f"- C1070: product-U2C replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- product-U2C (prior C1058): replace={replace} pass={u2c_pass}"',
    'f"- confidence-gate (prior C1064): pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- product-U2C (prior C1070): replace={replace} pass={u2c_pass}"',
    'f"- confidence-gate (prior C1064): pass={conf_pass} rate={conf_rate}"',
)
(S / "c1072_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T160 if t[0].endswith("b")])
print("qty", TR160[1], HO160[1], "po", TR160[8], HO160[8], "sla", TR160[6], HO160[6])
print("done")
