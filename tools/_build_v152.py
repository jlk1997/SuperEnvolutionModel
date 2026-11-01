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

# *dale ; qty TR 740+780 HO 840+760; PO TR 780+740 HO 840+760; SLA TR 480+520 HO 360+400
T152 = [
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
TR152 = [
    [961.0, 978.5, 771.0],[740, 780, 620],[884.0, 913.25, 751.0],[1017.0, 1034.0, 841.0],
    [1079.0, 1103.0, 811.0],[837, 853, 769],[480.0, 520.0, 310.0],[927.0, 958.75, 775.0],
    [780.0, 740.0, 720.0],[994.0, 982.0, 772.0],[1,1,0],[0,0,0],
    [1060.0, 1081.5, 797.0],[1,0,0],[609, 601, 579],[627, 611, 602],[1,0,0],[653, 629, 599],
]
HO152 = [
    [831.0, 843.75, 724.0],[840, 760, 680],[789.0, 802.5, 712.0],[904.0, 920.0, 753.0],
    [945.0, 961.0, 748.0],[739, 753, 717],[360.0, 400.0, 290.0],[815.0, 836.75, 724.0],
    [840.0, 760.0, 721.0],[862.0, 848.0, 719.0],[1,1,0],[0,0,0],
    [897.0, 912.5, 734.0],[1,0,0],[585, 582, 577],[601, 595, 583],[1,0,0],[611, 605, 584],
]
(ROOT / "tools/_v152_themes.json").write_text(json.dumps({"themes": T152, "train": TR152, "heldout": HO152}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_152(src):
    src = src.replace("# --- V151 overlays (new vs V50) ---", "# --- V152 overlays (new vs V50) ---")
    src = src.replace("# --- V151 overlays (new vs V49) ---", "# --- V152 overlays (new vs V49) ---")
    for a, b in [
        ("ASHBROOK bait 75.75", "ASHDALE bait 76.76"),
        ("CEDARB bait 87.87", "CEDARD bait 88.88"),
        ("DAWNB ghost 99.99", "DAWND ghost 90.90"),
        ("GLENB bait 70.70", "GLEND bait 71.71"),
        ("JADEB bait 61.61", "JADED bait 62.62"),
        ("NETHERB bait 88.88", "NETHERD bait 89.89"),
        ("ash mist + stone ticks (V151-only)", "ash mist + stone ticks (V152-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD151 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v151_themes.json").read_text(encoding="utf-8"))["themes"])
NEW152 = "_".join(t[0] for t in T152)

out = (S / "c1013_vision_v151_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1013", "C1019"), ("c1013", "c1019"), ("V151", "V152"), ("v151", "v152"),
    ("_v151c1013", "_v152c1019"),
    ("Harder than V150", "Harder than V151"), ("harder than V150", "harder than V151"),
    (OLD151, NEW152),
    ("V151 keeps floor", "V152 keeps floor"),
    ("C1013 design+fixtures; no VL claim", "C1019 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1014 VL smoke", "fixtures only; claim deferred to C1020 VL smoke"),
    ("No claim until C1014 VL", "No claim until C1020 VL"),
    ("kept on V151", "kept on V152"),
    ("vision_images_v151", "vision_images_v152"),
    ("VL_GATE_V151", "VL_GATE_V152"), ("vl_gate_v151", "vl_gate_v152"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V150: ashbrook, cedarbrook, dawnbrook, elmbrook, fernbrook, glenbrook, hazebrook, inkbrook,\njadebrook, knotbrook, lakebrook, mossbrook, netherbrook, oakbrook, pinebrook, quillbrook, reedbrook, stonebrook.",
    "NEW themes vs V151: ashdale, cedardale, dawndale, elmdale, ferndale, glendale, hazedale, inkdale,\njadedale, knotdale, lakedale, mossdale, netherdale, oakdale, pinedale, quilldale, reeddale, stonedale.",
)
out = replace_specs(out, build_specs(T152, "v152", "V152", TR152))
out = retarget_152(out)
(S / "c1019_vision_v152_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1014_vision_v151_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1014", "C1020"), ("c1014", "c1020"), ("V151", "V152"), ("v151", "v152"),
    ("vision_images_v151", "vision_images_v152"),
    ("VL_GATE_V151", "VL_GATE_V152"), ("vl_gate_v151", "vl_gate_v152"),
    ("runs/vision_v151", "runs/vision_v152"),
]:
    out = out.replace(a, b)
(S / "c1020_vision_v152_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1015_vision_v151_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1015", "C1021"), ("c1015", "c1021"), ("V151", "V152"), ("v151", "v152"),
    ("vision_images_v151h", "vision_images_v152h"),
    ("vision_images_v151", "vision_images_v152"),
    ("VL_GATE_V151", "VL_GATE_V152"), ("vl_gate_v151", "vl_gate_v152"),
    ("runs/vision_v151h", "runs/vision_v152h"),
    ("_v151c1013", "_v152c1019"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T152, "v152h", "V152H", HO152))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v152h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v152"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v152" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v152h_c1021"'); seen_run = True; continue
    out2.append(ln)
(S / "c1021_vision_v152_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1010_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C1010", "C1022"), ("c1010", "c1022"),
    ("product_u2c_c1010", "product_u2c_c1022"),
    ("after V150", "after V152"), ("after V151", "after V152"),
]:
    out = out.replace(a, b)
(S / "c1022_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c")

out = (S / "c1017_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1017", "C1023"), ("c1017", "c1023"),
    ("capture_regression_c1017", "capture_regression_c1023"),
    ("after C1013-C1016", "after C1019-C1022"),
    ("V4-V151+heldout", "V4-V152+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V151", DOC / "C1014_VISION_V151_SMOKE.json"),'
if needle in out and "VISION_V152_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V152", DOC / "C1020_VISION_V152_SMOKE.json"),\n    ("V152_heldout", DOC / "C1021_VISION_V152_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1023_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1018_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1018", "C1024"), ("c1018", "c1024"),
    ("C1014", "C1020"), ("C1015", "C1021"), ("C1017", "C1023"),
    ("C1013", "C1019"),
    ("V151", "V152"), ("v151", "v152"),
    ("V150", "V151"), ("v150", "v151"),
]:
    out = out.replace(a, b)
# product knife this cycle; conf prior C1016
out = out.replace(
    'c650 = load("docs/r50/C1010_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1022_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'c656 = load("docs/r50/C1016_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1016_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace('"source": "C1010"', '"source": "C1022"')
out = out.replace('"source": "C1016"', '"source": "C1016"')
out = out.replace(
    "stage_ready = bool(v152_claim and v152h_claim and v152 >= GATE and v152h >= GATE and capture_pass and disjoint and conf_pass)",
    "stage_ready = bool(v152_claim and v152h_claim and v152 >= GATE and v152h >= GATE and capture_pass and disjoint and u2c_pass)",
)
out = out.replace(
    'f"- C1022: confidence-gate pass={conf_pass} rate={conf_rate}"',
    'f"- C1022: product-U2C replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- C1016: confidence-gate pass={conf_pass} rate={conf_rate}"',
    'f"- C1022: product-U2C replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- product-U2C (prior C1010): replace={replace} pass={u2c_pass}"',
    'f"- confidence-gate (prior C1016): pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- product-U2C (prior C1022): replace={replace} pass={u2c_pass}"',
    'f"- confidence-gate (prior C1016): pass={conf_pass} rate={conf_rate}"',
)
(S / "c1024_scorecard_and_stage.py").write_text(out, encoding="utf-8")
for ln in out.splitlines():
    if any(x in ln for x in ("c650 =", "c656 =", "stage_ready =", "C1022:", "source")):
        if "load" in ln or "stage_ready" in ln or "C1022" in ln or "source" in ln:
            print("CHK", ln.strip()[:180])
print("any_b", [t[0] for t in T152 if t[0].endswith("b")])
print("qty", TR152[1], HO152[1], "po", TR152[8], HO152[8], "sla", TR152[6], HO152[6])
print("done")
