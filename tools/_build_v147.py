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

# *croft — qty TR 840+760 HO 740+780 (avoid 780+740 TR qty OCR trap); PO TR 840+760 HO 780+740
T147 = [
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
    ["stonecraft","tab","tab_index","STONECROFT TAB INDEX","TAB","x"],
]
TR147 = [
    [912.0, 929.5, 722.0],[840, 760, 610],[835.0, 864.25, 702.0],[968.0, 985.0, 792.0],
    [1030.0, 1054.0, 762.0],[788, 804, 720],[520.0, 560.0, 400.0],[878.0, 909.75, 726.0],
    [840.0, 760.0, 730.0],[945.0, 933.0, 723.0],[1,1,0],[0,0,0],
    [1011.0, 1032.5, 748.0],[1,0,0],[560, 552, 530],[578, 562, 553],[1,0,0],[604, 580, 550],
]
HO147 = [
    [782.0, 794.75, 675.0],[740, 780, 630],[740.0, 753.5, 663.0],[855.0, 871.0, 704.0],
    [896.0, 912.0, 699.0],[690, 704, 668],[420.0, 460.0, 360.0],[766.0, 787.75, 675.0],
    [780.0, 740.0, 672.0],[813.0, 799.0, 670.0],[1,1,0],[0,0,0],
    [848.0, 863.5, 685.0],[1,0,0],[536, 533, 528],[552, 546, 534],[1,0,0],[562, 556, 535],
]
(ROOT / "tools/_v147_themes.json").write_text(json.dumps({"themes": T147, "train": TR147, "heldout": HO147}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_147(src):
    src = src.replace("# --- V146 overlays (new vs V50) ---", "# --- V147 overlays (new vs V50) ---")
    src = src.replace("# --- V146 overlays (new vs V49) ---", "# --- V147 overlays (new vs V49) ---")
    for a, b in [
        ("ASHWICK bait 70.70", "ASHCROFT bait 71.71"),
        ("CEDARW bait 82.82", "CEDARC bait 83.83"),
        ("DAWNW ghost 94.94", "DAWNC ghost 95.95"),
        ("GLENW bait 75.75", "GLENC bait 76.76"),
        ("JADEW bait 66.66", "JADEC bait 67.67"),
        ("NETHERW bait 83.83", "NETHERC bait 84.84"),
        ("ash mist + stone ticks (V146-only)", "ash mist + stone ticks (V147-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD146 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v146_themes.json").read_text(encoding="utf-8"))["themes"])
NEW147 = "_".join(t[0] for t in T147)

out = (S / "c983_vision_v146_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C983", "C989"), ("c983", "c989"), ("V146", "V147"), ("v146", "v147"),
    ("_v146c983", "_v147c989"),
    ("Harder than V145", "Harder than V146"), ("harder than V145", "harder than V146"),
    (OLD146, NEW147),
    ("V146 keeps floor", "V147 keeps floor"),
    ("C983 design+fixtures; no VL claim", "C989 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C984 VL smoke", "fixtures only; claim deferred to C990 VL smoke"),
    ("No claim until C984 VL", "No claim until C990 VL"),
    ("kept on V146", "kept on V147"),
    ("vision_images_v146", "vision_images_v147"),
    ("VL_GATE_V146", "VL_GATE_V147"), ("vl_gate_v146", "vl_gate_v147"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V145: ashwick, cedarwick, dawnwick, elmwick, fernwick, glenwick, hazewick, inkwick,\njadewick, knotwick, lakewick, mosswick, netherwick, oakwick, pinewick, quillwick, reedwick, stonewick.",
    "NEW themes vs V146: ashcroft, cedarcroft, dawncroft, elmcroft, ferncroft, glencroft, hazecroft, inkcroft,\njadecroft, knotcroft, lakecroft, mosscroft, nethercroft, oakcroft, pinecroft, quillcroft, reedcroft, stonecraft.",
)
out = replace_specs(out, build_specs(T147, "v147", "V147", TR147))
out = retarget_147(out)
(S / "c989_vision_v147_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c984_vision_v146_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C984", "C990"), ("c984", "c990"), ("V146", "V147"), ("v146", "v147"),
    ("vision_images_v146", "vision_images_v147"),
    ("VL_GATE_V146", "VL_GATE_V147"), ("vl_gate_v146", "vl_gate_v147"),
    ("runs/vision_v146", "runs/vision_v147"),
]:
    out = out.replace(a, b)
(S / "c990_vision_v147_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c985_vision_v146_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C985", "C991"), ("c985", "c991"), ("V146", "V147"), ("v146", "v147"),
    ("vision_images_v146h", "vision_images_v147h"),
    ("vision_images_v146", "vision_images_v147"),
    ("VL_GATE_V146", "VL_GATE_V147"), ("vl_gate_v146", "vl_gate_v147"),
    ("runs/vision_v146h", "runs/vision_v147h"),
    ("_v146c983", "_v147c989"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T147, "v147h", "V147H", HO147))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v147h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v147"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v147" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v147h_c991"'); seen_run = True; continue
    out2.append(ln)
(S / "c991_vision_v147_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c980_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C980", "C992"), ("c980", "c992"),
    ("conf_gate_stretch_c980", "conf_gate_stretch_c992"),
    ("after V145", "after V147"), ("after V146", "after V147"),
    ("cg74_", "cg75_"),
]:
    out = out.replace(a, b)
(S / "c992_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence")

out = (S / "c987_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C987", "C993"), ("c987", "c993"),
    ("capture_regression_c987", "capture_regression_c993"),
    ("after C983-C986", "after C989-C992"),
    ("V4-V146+heldout", "V4-V147+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V146", DOC / "C984_VISION_V146_SMOKE.json"),'
if needle in out and "VISION_V147_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V147", DOC / "C990_VISION_V147_SMOKE.json"),\n    ("V147_heldout", DOC / "C991_VISION_V147_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c993_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c988_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C988", "C994"), ("c988", "c994"),
    ("C984", "C990"), ("C985", "C991"), ("C987", "C993"),
    ("C983", "C989"),
    ("V146", "V147"), ("v146", "v147"),
    ("V145", "V146"), ("v145", "v146"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c650 = load("docs/r50/C986_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C986_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'c656 = load("docs/r50/C980_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C992_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace('"source": "C986"', '"source": "C986"')
out = out.replace('"source": "C980"', '"source": "C992"')
out = out.replace(
    'c656 = load("docs/r50/C986_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C992_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    "stage_ready = bool(v147_claim and v147h_claim and v147 >= GATE and v147h >= GATE and capture_pass and disjoint and u2c_pass)",
    "stage_ready = bool(v147_claim and v147h_claim and v147 >= GATE and v147h >= GATE and capture_pass and disjoint and conf_pass)",
)
out = out.replace(
    'f"- C992: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C992: confidence-gate pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- C986: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C992: confidence-gate pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- confidence-gate (prior C980): pass={conf_pass} rate={conf_rate}"',
    'f"- product-U2C (prior C986): replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- confidence-gate (prior C992): pass={conf_pass} rate={conf_rate}"',
    'f"- product-U2C (prior C986): replace={replace} pass={u2c_pass}"',
)
(S / "c994_scorecard_and_stage.py").write_text(out, encoding="utf-8")
for ln in out.splitlines():
    if any(x in ln for x in ("c650 =", "c656 =", "stage_ready =", "C992:", "source")):
        if "load" in ln or "stage_ready" in ln or "C992" in ln or "source" in ln:
            print("CHK", ln.strip()[:180])
print("any_b", [t[0] for t in T147 if t[0].endswith("b")])
print("qty", TR147[1], HO147[1], "po", TR147[8], HO147[8])
print("done")
