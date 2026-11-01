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

# *dale ; qty TR 840+760 HO 740+780; PO TR 840+760 HO 780+740; SLA TR 460+500 HO 360+400
T163 = [
    ["ashdale","recv","paid_total","ASHDALE GRAIN RECV","RECV","x"],
    ["cedardale","wh","qty_sum","WH CEDARDALE BIN","RECV","x"],
    ["dawndale","refund","refund_done","DAWNDALE PATCH REFUND","DONE","x"],
    ["elmdale","tax","tax_base_paid","ELMDALE TAX SLIP","TAX","x"],
    ["ferndale","pay","payroll_active","FERNDALE PAYROLL","PAY","x"],
    ["glendale","ship","ship_ok","GLENDALE SHIP DOCK","SHIP","x"],
    ["hazedale","sla","sla_ok_hours","HAZEDALE SLA CARD","SLA","x"],
    ["inkdale","exp","exp_sum","INKDALE EXPENSE","EXP","x"],
    ["jadedale","po","po_open","JADEDALE PO SHEET","PO","x"],
    ["knotdale","order","order_paid","KNOTDALE ORDER","ORD","x"],
    ["lakedale","dup","dup_mark","LAKEDALE DUP MARK","DUP","x"],
    ["mossdale","zero","zero_check","MOSSDALE AIR ZERO","ZERO","x"],
    ["netherdale","ledger","ledger_net","NETHERDALE LEDGER","LED","x"],
    ["oakdale","ui","ui_ok","OAKDALE UI SCAN","UI","x"],
    ["pinedale","stack","stack_count","PINEDALE STACK","STK","x"],
    ["quilldale","fax","fax_pages","QUILLDALE FAX","FAX","x"],
    ["reeddale","glare","glare_ok","REEDDALE GLARE","GLR","x"],
    ["stonedale","tab","tab_index","STONEDALE TAB INDEX","TAB","x"],
]
TR163 = [
    [1060.0, 1077.5, 870.0],[840, 760, 730],[983.0, 1012.25, 850.0],[1116.0, 1133.0, 940.0],
    [1178.0, 1202.0, 910.0],[936, 952, 868],[460.0, 500.0, 420.0],[1026.0, 1057.75, 874.0],
    [840.0, 760.0, 700.0],[1093.0, 1081.0, 871.0],[1,1,0],[0,0,0],
    [1159.0, 1180.5, 896.0],[1,0,0],[708, 700, 678],[726, 710, 701],[1,0,0],[752, 728, 698],
]
HO163 = [
    [930.0, 942.75, 823.0],[740, 780, 780],[888.0, 901.5, 811.0],[1003.0, 1019.0, 852.0],
    [1044.0, 1060.0, 847.0],[838, 852, 816],[360.0, 400.0, 400.0],[914.0, 935.75, 823.0],
    [780.0, 740.0, 680.0],[961.0, 947.0, 818.0],[1,1,0],[0,0,0],
    [996.0, 1011.5, 833.0],[1,0,0],[684, 681, 676],[700, 694, 682],[1,0,0],[710, 704, 683],
]
(ROOT / "tools/_v163_themes.json").write_text(json.dumps({"themes": T163, "train": TR163, "heldout": HO163}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_163(src):
    src = src.replace("# --- V162 overlays (new vs V50) ---", "# --- V163 overlays (new vs V50) ---")
    src = src.replace("# --- V162 overlays (new vs V49) ---", "# --- V163 overlays (new vs V49) ---")
    for a, b in [
        ("ASHBROOK bait 76.76", "ASHDALE bait 77.77"),
        ("CEDARB bait 88.88", "CEDARD bait 89.89"),
        ("DAWNB ghost 90.90", "DAWND ghost 91.91"),
        ("GLENB bait 71.71", "GLEND bait 72.72"),
        ("JADEB bait 62.62", "JADED bait 63.63"),
        ("NETHERB bait 89.89", "NETHERD bait 80.80"),
        ("ash mist + stone ticks (V162-only)", "ash mist + stone ticks (V163-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD162 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v162_themes.json").read_text(encoding="utf-8"))["themes"])
NEW163 = "_".join(t[0] for t in T163)

out = (S / "c1079_vision_v162_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1079", "C1085"), ("c1079", "c1085"), ("V162", "V163"), ("v162", "v163"),
    ("_v162c1079", "_v163c1085"),
    ("Harder than V161", "Harder than V162"), ("harder than V161", "harder than V162"),
    (OLD162, NEW163),
    ("V162 keeps floor", "V163 keeps floor"),
    ("C1079 design+fixtures; no VL claim", "C1085 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1080 VL smoke", "fixtures only; claim deferred to C1086 VL smoke"),
    ("No claim until C1080 VL", "No claim until C1086 VL"),
    ("kept on V162", "kept on V163"),
    ("vision_images_v162", "vision_images_v163"),
    ("VL_GATE_V162", "VL_GATE_V163"), ("vl_gate_v162", "vl_gate_v163"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V161:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V162: ashdale, cedardale, dawndale, elmdale, ferndale, glendale, hazedale, inkdale,\njadedale, knotdale, lakedale, mossdale, netherdale, oakdale, pinedale, quilldale, reeddale, stonedale.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T163, "v163", "V163", TR163))
out = retarget_163(out)
(S / "c1085_vision_v163_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1080_vision_v162_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1080", "C1086"), ("c1080", "c1086"), ("V162", "V163"), ("v162", "v163"),
    ("vision_images_v162", "vision_images_v163"),
    ("VL_GATE_V162", "VL_GATE_V163"), ("vl_gate_v162", "vl_gate_v163"),
    ("runs/vision_v162", "runs/vision_v163"),
]:
    out = out.replace(a, b)
(S / "c1086_vision_v163_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1081_vision_v162_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1081", "C1087"), ("c1081", "c1087"), ("V162", "V163"), ("v162", "v163"),
    ("vision_images_v162h", "vision_images_v163h"),
    ("vision_images_v162", "vision_images_v163"),
    ("VL_GATE_V162", "VL_GATE_V163"), ("vl_gate_v162", "vl_gate_v163"),
    ("runs/vision_v162h", "runs/vision_v163h"),
    ("_v162c1079", "_v163c1085"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T163, "v163h", "V163H", HO163))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v163h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v163"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v163" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v163h_c1087"'); seen_run = True; continue
    out2.append(ln)
(S / "c1087_vision_v163_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1076_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1076", "C1088"), ("c1076", "c1088"),
    ("conf_gate_stretch_c1076", "conf_gate_stretch_c1088"),
    ("after V161", "after V163"), ("after V162", "after V163"),
    ("cg82_", "cg83_"),
]:
    out = out.replace(a, b)
(S / "c1088_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence")

out = (S / "c1083_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1083", "C1089"), ("c1083", "c1089"),
    ("capture_regression_c1083", "capture_regression_c1089"),
    ("after C1079-C1082", "after C1085-C1088"),
    ("V4-V162+heldout", "V4-V163+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V162", DOC / "C1080_VISION_V162_SMOKE.json"),'
if needle in out and "VISION_V163_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V163", DOC / "C1086_VISION_V163_SMOKE.json"),\n    ("V163_heldout", DOC / "C1087_VISION_V163_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1089_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1084_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1084", "C1090"), ("c1084", "c1090"),
    ("C1080", "C1086"), ("C1081", "C1087"), ("C1083", "C1089"),
    ("C1079", "C1085"),
    ("V162", "V163"), ("v162", "v163"),
    ("V161", "V162"), ("v161", "v162"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c650 = load("docs/r50/C1082_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1082_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'c656 = load("docs/r50/C1076_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1088_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace('"source": "C1082"', '"source": "C1082"')
out = out.replace('"source": "C1076"', '"source": "C1088"')
out = out.replace(
    "stage_ready = bool(v163_claim and v163h_claim and v163 >= GATE and v163h >= GATE and capture_pass and disjoint and u2c_pass)",
    "stage_ready = bool(v163_claim and v163h_claim and v163 >= GATE and v163h >= GATE and capture_pass and disjoint and conf_pass)",
)
out = out.replace(
    'f"- C1088: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C1088: confidence-gate pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- C1082: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C1088: confidence-gate pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- confidence-gate (prior C1076): pass={conf_pass} rate={conf_rate}"',
    'f"- product-U2C (prior C1082): replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- confidence-gate (prior C1088): pass={conf_pass} rate={conf_rate}"',
    'f"- product-U2C (prior C1082): replace={replace} pass={u2c_pass}"',
)
(S / "c1090_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T163 if t[0].endswith("b")])
print("qty", TR163[1], HO163[1], "po", TR163[8], HO163[8], "sla", TR163[6], HO163[6])
print("done")
