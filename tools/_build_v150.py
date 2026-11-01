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

# *fen — qty TR 740+780 HO 840+760; PO TR 840+760 HO 780+740 (avoid 780+740 TR qty)
T150 = [
    ["ashfen","recv","paid_total","ASHFEN GRAIN RECV","RECV","x"],
    ["cedarfen","wh","qty_sum","WH CEDARFEN BIN","RECV","x"],
    ["dawnfen","refund","refund_done","DAWNFEN PATCH REFUND","DONE","x"],
    ["elmfen","tax","tax_base_paid","ELMFEN TAX SLIP","TAX","x"],
    ["fernfen","pay","payroll_active","FERNFEN PAYROLL","PAY","x"],
    ["glenfen","ship","ship_ok","GLENFEN SHIP DOCK","SHIP","x"],
    ["hazefen","sla","sla_ok_hours","HAZEFEN SLA CARD","SLA","x"],
    ["inkfen","exp","exp_sum","INKFEN EXPENSE","EXP","x"],
    ["jadefen","po","po_open","JADEFEN PO SHEET","PO","x"],
    ["knotfen","order","order_paid","KNOTFEN ORDER","ORD","x"],
    ["lakefen","dup","dup_mark","LAKEFEN DUP MARK","DUP","x"],
    ["mossfen","zero","zero_check","MOSSFEN AIR ZERO","ZERO","x"],
    ["netherfen","ledger","ledger_net","NETHERFEN LEDGER","LED","x"],
    ["oakfen","ui","ui_ok","OAKFEN UI SCAN","UI","x"],
    ["pinefen","stack","stack_count","PINEFEN STACK","STK","x"],
    ["quillfen","fax","fax_pages","QUILLFEN FAX","FAX","x"],
    ["reedfen","glare","glare_ok","REEDFEN GLARE","GLR","x"],
    ["stonefen","tab","tab_index","STONEFEN TAB INDEX","TAB","x"],
]
TR150 = [
    [942.0, 959.5, 752.0],[740, 780, 610],[865.0, 894.25, 732.0],[998.0, 1015.0, 822.0],
    [1060.0, 1084.0, 792.0],[818, 834, 750],[550.0, 590.0, 430.0],[908.0, 939.75, 756.0],
    [840.0, 760.0, 720.0],[975.0, 963.0, 753.0],[1,1,0],[0,0,0],
    [1041.0, 1062.5, 778.0],[1,0,0],[590, 582, 560],[608, 592, 583],[1,0,0],[634, 610, 580],
]
HO150 = [
    [812.0, 824.75, 705.0],[840, 760, 660],[770.0, 783.5, 693.0],[885.0, 901.0, 734.0],
    [926.0, 942.0, 729.0],[720, 734, 698],[450.0, 490.0, 390.0],[796.0, 817.75, 705.0],
    [780.0, 740.0, 702.0],[843.0, 829.0, 700.0],[1,1,0],[0,0,0],
    [878.0, 893.5, 715.0],[1,0,0],[566, 563, 558],[582, 576, 564],[1,0,0],[592, 586, 565],
]
(ROOT / "tools/_v150_themes.json").write_text(json.dumps({"themes": T150, "train": TR150, "heldout": HO150}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_150(src):
    src = src.replace("# --- V149 overlays (new vs V50) ---", "# --- V150 overlays (new vs V50) ---")
    src = src.replace("# --- V149 overlays (new vs V49) ---", "# --- V150 overlays (new vs V49) ---")
    for a, b in [
        ("ASHMOOR bait 73.73", "ASHFEN bait 74.74"),
        ("CEDARM bait 85.85", "CEDARF bait 86.86"),
        ("DAWNM ghost 97.97", "DAWNF ghost 98.98"),
        ("GLENM bait 78.78", "GLENF bait 79.79"),
        ("JADEM bait 69.69", "JADEF bait 60.60"),
        ("NETHERM bait 86.86", "NETHERF bait 87.87"),
        ("ash mist + stone ticks (V149-only)", "ash mist + stone ticks (V150-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD149 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v149_themes.json").read_text(encoding="utf-8"))["themes"])
NEW150 = "_".join(t[0] for t in T150)

out = (S / "c1001_vision_v149_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1001", "C1007"), ("c1001", "c1007"), ("V149", "V150"), ("v149", "v150"),
    ("_v149c1001", "_v150c1007"),
    ("Harder than V148", "Harder than V149"), ("harder than V148", "harder than V149"),
    (OLD149, NEW150),
    ("V149 keeps floor", "V150 keeps floor"),
    ("C1001 design+fixtures; no VL claim", "C1007 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1002 VL smoke", "fixtures only; claim deferred to C1008 VL smoke"),
    ("No claim until C1002 VL", "No claim until C1008 VL"),
    ("kept on V149", "kept on V150"),
    ("vision_images_v149", "vision_images_v150"),
    ("VL_GATE_V149", "VL_GATE_V150"), ("vl_gate_v149", "vl_gate_v150"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V148: ashmoor, cedarmoor, dawnmoor, elmmoor, fernmoor, glenmoor, hazemoor, inkmoor,\njademoor, knotmoor, lakemoor, mossmoor, nethermoor, oakmoor, pinemoor, quillmoor, reedmoor, stonemoor.",
    "NEW themes vs V149: ashfen, cedarfen, dawnfen, elmfen, fernfen, glenfen, hazefen, inkfen,\njadefen, knotfen, lakefen, mossfen, netherfen, oakfen, pinefen, quillfen, reedfen, stonefen.",
)
out = replace_specs(out, build_specs(T150, "v150", "V150", TR150))
out = retarget_150(out)
(S / "c1007_vision_v150_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1002_vision_v149_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1002", "C1008"), ("c1002", "c1008"), ("V149", "V150"), ("v149", "v150"),
    ("vision_images_v149", "vision_images_v150"),
    ("VL_GATE_V149", "VL_GATE_V150"), ("vl_gate_v149", "vl_gate_v150"),
    ("runs/vision_v149", "runs/vision_v150"),
]:
    out = out.replace(a, b)
(S / "c1008_vision_v150_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1003_vision_v149_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1003", "C1009"), ("c1003", "c1009"), ("V149", "V150"), ("v149", "v150"),
    ("vision_images_v149h", "vision_images_v150h"),
    ("vision_images_v149", "vision_images_v150"),
    ("VL_GATE_V149", "VL_GATE_V150"), ("vl_gate_v149", "vl_gate_v150"),
    ("runs/vision_v149h", "runs/vision_v150h"),
    ("_v149c1001", "_v150c1007"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T150, "v150h", "V150H", HO150))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v150h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v150"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v150" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v150h_c1009"'); seen_run = True; continue
    out2.append(ln)
(S / "c1009_vision_v150_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c998_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C998", "C1010"), ("c998", "c1010"),
    ("product_u2c_c998", "product_u2c_c1010"),
    ("after V148", "after V150"), ("after V149", "after V150"),
]:
    out = out.replace(a, b)
(S / "c1010_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c")

out = (S / "c1005_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1005", "C1011"), ("c1005", "c1011"),
    ("capture_regression_c1005", "capture_regression_c1011"),
    ("after C1001-C1004", "after C1007-C1010"),
    ("V4-V149+heldout", "V4-V150+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V149", DOC / "C1002_VISION_V149_SMOKE.json"),'
if needle in out and "VISION_V150_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V150", DOC / "C1008_VISION_V150_SMOKE.json"),\n    ("V150_heldout", DOC / "C1009_VISION_V150_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1011_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1006_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1006", "C1012"), ("c1006", "c1012"),
    ("C1002", "C1008"), ("C1003", "C1009"), ("C1005", "C1011"),
    ("C1001", "C1007"), ("C1004", "C1010"),
    ("V149", "V150"), ("v149", "v150"),
    ("V148", "V149"), ("v148", "v149"),
]:
    out = out.replace(a, b)
# product knife this cycle
out = out.replace(
    'c650 = load("docs/r50/C998_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1010_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'c656 = load("docs/r50/C1004_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1004_CONFIDENCE_GATE_STRETCH.json") or {}',
)
# undo accidental C1004->C1010 on conf path
out = out.replace(
    'c656 = load("docs/r50/C1010_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1004_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace('"source": "C998"', '"source": "C1010"')
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C1010"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C1004"}',
)
out = out.replace(
    "stage_ready = bool(v150_claim and v150h_claim and v150 >= GATE and v150h >= GATE and capture_pass and disjoint and conf_pass)",
    "stage_ready = bool(v150_claim and v150h_claim and v150 >= GATE and v150h >= GATE and capture_pass and disjoint and u2c_pass)",
)
out = out.replace(
    'f"- C1010: confidence-gate pass={conf_pass} rate={conf_rate}"',
    'f"- C1010: product-U2C replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- C1004: confidence-gate pass={conf_pass} rate={conf_rate}"',
    'f"- C1010: product-U2C replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- product-U2C (prior C998): replace={replace} pass={u2c_pass}"',
    'f"- confidence-gate (prior C1004): pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- product-U2C (prior C1010): replace={replace} pass={u2c_pass}"',
    'f"- confidence-gate (prior C1004): pass={conf_pass} rate={conf_rate}"',
)
(S / "c1012_scorecard_and_stage.py").write_text(out, encoding="utf-8")
for ln in out.splitlines():
    if any(x in ln for x in ("c650 =", "c656 =", "stage_ready =", "C1010:", "source", "STAGE_ANT")):
        if "load" in ln or "stage_ready" in ln or "C1010" in ln or "source" in ln or "STAGE" in ln:
            print("CHK", ln.strip()[:180])
print("any_b", [t[0] for t in T150 if t[0].endswith("b")])
print("qty", TR150[1], HO150[1], "po", TR150[8], HO150[8])
print("done")
