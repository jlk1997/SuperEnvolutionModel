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

# *vale ; qty TR 840+760 HO 740+780; PO TR 840+760 HO 780+740; SLA TR 460+500 HO 360+400
T153 = [
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
TR153 = [
    [970.0, 987.5, 780.0],[840, 760, 630],[893.0, 922.25, 760.0],[1026.0, 1043.0, 850.0],
    [1088.0, 1112.0, 820.0],[846, 862, 778],[460.0, 500.0, 320.0],[936.0, 967.75, 784.0],
    [840.0, 760.0, 730.0],[1003.0, 991.0, 781.0],[1,1,0],[0,0,0],
    [1069.0, 1090.5, 806.0],[1,0,0],[618, 610, 588],[636, 620, 611],[1,0,0],[662, 638, 608],
]
HO153 = [
    [840.0, 852.75, 733.0],[740, 780, 690],[798.0, 811.5, 721.0],[913.0, 929.0, 762.0],
    [954.0, 970.0, 757.0],[748, 762, 726],[360.0, 400.0, 300.0],[824.0, 845.75, 733.0],
    [780.0, 740.0, 730.0],[871.0, 857.0, 728.0],[1,1,0],[0,0,0],
    [906.0, 921.5, 743.0],[1,0,0],[594, 591, 586],[610, 604, 592],[1,0,0],[620, 614, 593],
]
(ROOT / "tools/_v153_themes.json").write_text(json.dumps({"themes": T153, "train": TR153, "heldout": HO153}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_153(src):
    src = src.replace("# --- V152 overlays (new vs V50) ---", "# --- V153 overlays (new vs V50) ---")
    src = src.replace("# --- V152 overlays (new vs V49) ---", "# --- V153 overlays (new vs V49) ---")
    for a, b in [
        ("ASHDALE bait 76.76", "ASHVALE bait 77.77"),
        ("CEDARD bait 88.88", "CEDARV bait 89.89"),
        ("DAWND ghost 90.90", "DAWNV ghost 91.91"),
        ("GLEND bait 71.71", "GLENV bait 72.72"),
        ("JADED bait 62.62", "JADEV bait 63.63"),
        ("NETHERD bait 89.89", "NETHERV bait 80.80"),
        ("ash mist + stone ticks (V152-only)", "ash mist + stone ticks (V153-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD152 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v152_themes.json").read_text(encoding="utf-8"))["themes"])
NEW153 = "_".join(t[0] for t in T153)

out = (S / "c1019_vision_v152_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1019", "C1025"), ("c1019", "c1025"), ("V152", "V153"), ("v152", "v153"),
    ("_v152c1019", "_v153c1025"),
    ("Harder than V151", "Harder than V152"), ("harder than V151", "harder than V152"),
    (OLD152, NEW153),
    ("V152 keeps floor", "V153 keeps floor"),
    ("C1019 design+fixtures; no VL claim", "C1025 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1020 VL smoke", "fixtures only; claim deferred to C1026 VL smoke"),
    ("No claim until C1020 VL", "No claim until C1026 VL"),
    ("kept on V152", "kept on V153"),
    ("vision_images_v152", "vision_images_v153"),
    ("VL_GATE_V152", "VL_GATE_V153"), ("vl_gate_v152", "vl_gate_v153"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V151: ashdale, cedardale, dawndale, elmdale, ferndale, glendale, hazedale, inkdale,\njadedale, knotdale, lakedale, mossdale, netherdale, oakdale, pinedale, quilldale, reeddale, stonedale.",
    "NEW themes vs V152: ashvale, cedarvale, dawnvale, elmvale, fernvale, glenvale, hazevale, inkvale,\njadevale, knotvale, lakevale, mossvale, nethervale, oakvale, pinevale, quillvale, reedvale, stonevale.",
)
out = replace_specs(out, build_specs(T153, "v153", "V153", TR153))
out = retarget_153(out)
(S / "c1025_vision_v153_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1020_vision_v152_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1020", "C1026"), ("c1020", "c1026"), ("V152", "V153"), ("v152", "v153"),
    ("vision_images_v152", "vision_images_v153"),
    ("VL_GATE_V152", "VL_GATE_V153"), ("vl_gate_v152", "vl_gate_v153"),
    ("runs/vision_v152", "runs/vision_v153"),
]:
    out = out.replace(a, b)
(S / "c1026_vision_v153_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1021_vision_v152_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1021", "C1027"), ("c1021", "c1027"), ("V152", "V153"), ("v152", "v153"),
    ("vision_images_v152h", "vision_images_v153h"),
    ("vision_images_v152", "vision_images_v153"),
    ("VL_GATE_V152", "VL_GATE_V153"), ("vl_gate_v152", "vl_gate_v153"),
    ("runs/vision_v152h", "runs/vision_v153h"),
    ("_v152c1019", "_v153c1025"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T153, "v153h", "V153H", HO153))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v153h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v153"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v153" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v153h_c1027"'); seen_run = True; continue
    out2.append(ln)
(S / "c1027_vision_v153_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1016_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1016", "C1028"), ("c1016", "c1028"),
    ("conf_gate_stretch_c1016", "conf_gate_stretch_c1028"),
    ("after V151", "after V153"), ("after V152", "after V153"),
    ("cg77_", "cg78_"),
]:
    out = out.replace(a, b)
(S / "c1028_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence")

out = (S / "c1023_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1023", "C1029"), ("c1023", "c1029"),
    ("capture_regression_c1023", "capture_regression_c1029"),
    ("after C1019-C1022", "after C1025-C1028"),
    ("V4-V152+heldout", "V4-V153+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V152", DOC / "C1020_VISION_V152_SMOKE.json"),'
if needle in out and "VISION_V153_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V153", DOC / "C1026_VISION_V153_SMOKE.json"),\n    ("V153_heldout", DOC / "C1027_VISION_V153_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1029_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1024_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1024", "C1030"), ("c1024", "c1030"),
    ("C1020", "C1026"), ("C1021", "C1027"), ("C1023", "C1029"),
    ("C1019", "C1025"),
    ("V152", "V153"), ("v152", "v153"),
    ("V151", "V152"), ("v151", "v152"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c650 = load("docs/r50/C1022_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1022_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'c656 = load("docs/r50/C1016_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1028_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace('"source": "C1022"', '"source": "C1022"')
out = out.replace('"source": "C1016"', '"source": "C1028"')
out = out.replace(
    "stage_ready = bool(v153_claim and v153h_claim and v153 >= GATE and v153h >= GATE and capture_pass and disjoint and u2c_pass)",
    "stage_ready = bool(v153_claim and v153h_claim and v153 >= GATE and v153h >= GATE and capture_pass and disjoint and conf_pass)",
)
out = out.replace(
    'f"- C1028: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C1028: confidence-gate pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- C1022: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C1028: confidence-gate pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- confidence-gate (prior C1016): pass={conf_pass} rate={conf_rate}"',
    'f"- product-U2C (prior C1022): replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- confidence-gate (prior C1028): pass={conf_pass} rate={conf_rate}"',
    'f"- product-U2C (prior C1022): replace={replace} pass={u2c_pass}"',
)
(S / "c1030_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T153 if t[0].endswith("b")])
print("qty", TR153[1], HO153[1], "po", TR153[8], HO153[8], "sla", TR153[6], HO153[6])
print("done")
