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

# *brook — qty TR 840+760 HO 740+780; PO TR 840+760 HO 780+740; SLA TR 460+500 HO 360+400
T151 = [
    ["ashbrook","recv","paid_total","ASHBROOK GRAIN RECV","RECV","x"],
    ["cedarbrook","wh","qty_sum","WH CEDARBROOK BIN","RECV","x"],
    ["dawnbrook","refund","refund_done","DAWNBROOK PATCH REFUND","DONE","x"],
    ["elmbrook","tax","tax_base_paid","ELMBROOK TAX SLIP","TAX","x"],
    ["fernbrook","pay","payroll_active","FERNBROOK PAYROLL","PAY","x"],
    ["glenbrook","ship","ship_ok","GLENBROOK SHIP DOCK","SHIP","x"],
    ["hazebrook","sla","sla_ok_hours","HAZEBROOK SLA CARD","SLA","x"],
    ["inkbrook","exp","exp_sum","INKBROOK EXPENSE","EXP","x"],
    ["jadebrook","po","po_open","JADEBROOK PO SHEET","PO","x"],
    ["knotbrook","order","order_paid","KNOTBROOK ORDER","ORD","x"],
    ["lakebrook","dup","dup_mark","LAKEBROOK DUP MARK","DUP","x"],
    ["mossbrook","zero","zero_check","MOSSBROOK AIR ZERO","ZERO","x"],
    ["netherbrook","ledger","ledger_net","NETHERBROOK LEDGER","LED","x"],
    ["oakbrook","ui","ui_ok","OAKBROOK UI SCAN","UI","x"],
    ["pinebrook","stack","stack_count","PINEBROOK STACK","STK","x"],
    ["quillbrook","fax","fax_pages","QUILLBROOK FAX","FAX","x"],
    ["reedbrook","glare","glare_ok","REEDBROOK GLARE","GLR","x"],
    ["stonebrook","tab","tab_index","STONEBROOK TAB INDEX","TAB","x"],
]
TR151 = [
    [952.0, 969.5, 762.0],[840, 760, 610],[875.0, 904.25, 742.0],[1008.0, 1025.0, 832.0],
    [1070.0, 1094.0, 802.0],[828, 844, 760],[460.0, 500.0, 300.0],[918.0, 949.75, 766.0],
    [840.0, 760.0, 730.0],[985.0, 973.0, 763.0],[1,1,0],[0,0,0],
    [1051.0, 1072.5, 788.0],[1,0,0],[600, 592, 570],[618, 602, 593],[1,0,0],[644, 620, 590],
]
HO151 = [
    [822.0, 834.75, 715.0],[740, 780, 670],[780.0, 793.5, 703.0],[895.0, 911.0, 744.0],
    [936.0, 952.0, 739.0],[730, 744, 708],[360.0, 400.0, 280.0],[806.0, 827.75, 715.0],
    [780.0, 740.0, 712.0],[853.0, 839.0, 710.0],[1,1,0],[0,0,0],
    [888.0, 903.5, 725.0],[1,0,0],[576, 573, 568],[592, 586, 574],[1,0,0],[602, 596, 575],
]
(ROOT / "tools/_v151_themes.json").write_text(json.dumps({"themes": T151, "train": TR151, "heldout": HO151}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_151(src):
    src = src.replace("# --- V150 overlays (new vs V50) ---", "# --- V151 overlays (new vs V50) ---")
    src = src.replace("# --- V150 overlays (new vs V49) ---", "# --- V151 overlays (new vs V49) ---")
    for a, b in [
        ("ASHFEN bait 74.74", "ASHBROOK bait 75.75"),
        ("CEDARF bait 86.86", "CEDARB bait 87.87"),
        ("DAWNF ghost 98.98", "DAWNB ghost 99.99"),
        ("GLENF bait 79.79", "GLENB bait 70.70"),
        ("JADEF bait 60.60", "JADEB bait 61.61"),
        ("NETHERF bait 87.87", "NETHERB bait 88.88"),
        ("ash mist + stone ticks (V150-only)", "ash mist + stone ticks (V151-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD150 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v150_themes.json").read_text(encoding="utf-8"))["themes"])
NEW151 = "_".join(t[0] for t in T151)

out = (S / "c1007_vision_v150_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1007", "C1013"), ("c1007", "c1013"), ("V150", "V151"), ("v150", "v151"),
    ("_v150c1007", "_v151c1013"),
    ("Harder than V149", "Harder than V150"), ("harder than V149", "harder than V150"),
    (OLD150, NEW151),
    ("V150 keeps floor", "V151 keeps floor"),
    ("C1007 design+fixtures; no VL claim", "C1013 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1008 VL smoke", "fixtures only; claim deferred to C1014 VL smoke"),
    ("No claim until C1008 VL", "No claim until C1014 VL"),
    ("kept on V150", "kept on V151"),
    ("vision_images_v150", "vision_images_v151"),
    ("VL_GATE_V150", "VL_GATE_V151"), ("vl_gate_v150", "vl_gate_v151"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V149: ashfen, cedarfen, dawnfen, elmfen, fernfen, glenfen, hazefen, inkfen,\njadefen, knotfen, lakefen, mossfen, netherfen, oakfen, pinefen, quillfen, reedfen, stonefen.",
    "NEW themes vs V150: ashbrook, cedarbrook, dawnbrook, elmbrook, fernbrook, glenbrook, hazebrook, inkbrook,\njadebrook, knotbrook, lakebrook, mossbrook, netherbrook, oakbrook, pinebrook, quillbrook, reedbrook, stonebrook.",
)
out = replace_specs(out, build_specs(T151, "v151", "V151", TR151))
out = retarget_151(out)
(S / "c1013_vision_v151_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1008_vision_v150_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1008", "C1014"), ("c1008", "c1014"), ("V150", "V151"), ("v150", "v151"),
    ("vision_images_v150", "vision_images_v151"),
    ("VL_GATE_V150", "VL_GATE_V151"), ("vl_gate_v150", "vl_gate_v151"),
    ("runs/vision_v150", "runs/vision_v151"),
]:
    out = out.replace(a, b)
(S / "c1014_vision_v151_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1009_vision_v150_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1009", "C1015"), ("c1009", "c1015"), ("V150", "V151"), ("v150", "v151"),
    ("vision_images_v150h", "vision_images_v151h"),
    ("vision_images_v150", "vision_images_v151"),
    ("VL_GATE_V150", "VL_GATE_V151"), ("vl_gate_v150", "vl_gate_v151"),
    ("runs/vision_v150h", "runs/vision_v151h"),
    ("_v150c1007", "_v151c1013"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T151, "v151h", "V151H", HO151))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v151h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v151"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v151" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v151h_c1015"'); seen_run = True; continue
    out2.append(ln)
(S / "c1015_vision_v151_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1004_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1004", "C1016"), ("c1004", "c1016"),
    ("conf_gate_stretch_c1004", "conf_gate_stretch_c1016"),
    ("after V149", "after V151"), ("after V150", "after V151"),
    ("cg76_", "cg77_"),
]:
    out = out.replace(a, b)
(S / "c1016_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence")

out = (S / "c1011_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1011", "C1017"), ("c1011", "c1017"),
    ("capture_regression_c1011", "capture_regression_c1017"),
    ("after C1007-C1010", "after C1013-C1016"),
    ("V4-V150+heldout", "V4-V151+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V150", DOC / "C1008_VISION_V150_SMOKE.json"),'
if needle in out and "VISION_V151_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V151", DOC / "C1014_VISION_V151_SMOKE.json"),\n    ("V151_heldout", DOC / "C1015_VISION_V151_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1017_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1012_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1012", "C1018"), ("c1012", "c1018"),
    ("C1008", "C1014"), ("C1009", "C1015"), ("C1011", "C1017"),
    ("C1007", "C1013"),
    ("V150", "V151"), ("v150", "v151"),
    ("V149", "V150"), ("v149", "v150"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c650 = load("docs/r50/C1010_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1010_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'c656 = load("docs/r50/C1004_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1016_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace('"source": "C1010"', '"source": "C1010"')
out = out.replace('"source": "C1004"', '"source": "C1016"')
out = out.replace(
    'c656 = load("docs/r50/C1010_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1016_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    "stage_ready = bool(v151_claim and v151h_claim and v151 >= GATE and v151h >= GATE and capture_pass and disjoint and u2c_pass)",
    "stage_ready = bool(v151_claim and v151h_claim and v151 >= GATE and v151h >= GATE and capture_pass and disjoint and conf_pass)",
)
out = out.replace(
    'f"- C1016: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C1016: confidence-gate pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- C1010: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C1016: confidence-gate pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- confidence-gate (prior C1004): pass={conf_pass} rate={conf_rate}"',
    'f"- product-U2C (prior C1010): replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- confidence-gate (prior C1016): pass={conf_pass} rate={conf_rate}"',
    'f"- product-U2C (prior C1010): replace={replace} pass={u2c_pass}"',
)
(S / "c1018_scorecard_and_stage.py").write_text(out, encoding="utf-8")
for ln in out.splitlines():
    if any(x in ln for x in ("c650 =", "c656 =", "stage_ready =", "C1016:", "source")):
        if "load" in ln or "stage_ready" in ln or "C1016" in ln or "source" in ln:
            print("CHK", ln.strip()[:180])
print("any_b", [t[0] for t in T151 if t[0].endswith("b")])
print("qty", TR151[1], HO151[1], "sla", TR151[6], HO151[6])
print("done")
