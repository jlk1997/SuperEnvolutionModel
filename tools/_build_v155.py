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

# *holm ; qty TR 840+760 HO 740+780; PO TR 840+760 HO 780+740; SLA TR 460+500 HO 360+400
T155 = [
    ["ashholm","recv","paid_total","ASHHOLM GRAIN RECV","RECV","x"],
    ["cedarholm","wh","qty_sum","WH CEDARHOLM BIN","RECV","x"],
    ["dawnholm","refund","refund_done","DAWNHOLM PATCH REFUND","DONE","x"],
    ["elmholm","tax","tax_base_paid","ELMHOLM TAX SLIP","TAX","x"],
    ["fernholm","pay","payroll_active","FERNHOLM PAYROLL","PAY","x"],
    ["glenholm","ship","ship_ok","GLENHOLM SHIP DOCK","SHIP","x"],
    ["hazeholm","sla","sla_ok_hours","HAZEHOLM SLA CARD","SLA","x"],
    ["inkholm","exp","exp_sum","INKHOLM EXPENSE","EXP","x"],
    ["jadeholm","po","po_open","JADEHOLM PO SHEET","PO","x"],
    ["knotholm","order","order_paid","KNOTHOLM ORDER","ORD","x"],
    ["lakeholm","dup","dup_mark","LAKEHOLM DUP MARK","DUP","x"],
    ["mossholm","zero","zero_check","MOSSHOLM AIR ZERO","ZERO","x"],
    ["netherholm","ledger","ledger_net","NETHERHOLM LEDGER","LED","x"],
    ["oakholm","ui","ui_ok","OAKHOLM UI SCAN","UI","x"],
    ["pineholm","stack","stack_count","PINEHOLM STACK","STK","x"],
    ["quillholm","fax","fax_pages","QUILLHOLM FAX","FAX","x"],
    ["reedholm","glare","glare_ok","REEDHOLM GLARE","GLR","x"],
    ["stoneholm","tab","tab_index","STONEHOLM TAB INDEX","TAB","x"],
]
TR155 = [
    [988.0, 1005.5, 798.0],[840, 760, 650],[911.0, 940.25, 778.0],[1044.0, 1061.0, 868.0],
    [1106.0, 1130.0, 838.0],[864, 880, 796],[460.0, 500.0, 340.0],[954.0, 985.75, 802.0],
    [840.0, 760.0, 740.0],[1021.0, 1009.0, 799.0],[1,1,0],[0,0,0],
    [1087.0, 1108.5, 824.0],[1,0,0],[636, 628, 606],[654, 638, 629],[1,0,0],[680, 656, 626],
]
HO155 = [
    [858.0, 870.75, 751.0],[740, 780, 710],[816.0, 829.5, 739.0],[931.0, 947.0, 780.0],
    [972.0, 988.0, 775.0],[766, 780, 744],[360.0, 400.0, 320.0],[842.0, 863.75, 751.0],
    [780.0, 740.0, 720.0],[889.0, 875.0, 746.0],[1,1,0],[0,0,0],
    [924.0, 939.5, 761.0],[1,0,0],[612, 609, 604],[628, 622, 610],[1,0,0],[638, 632, 611],
]
(ROOT / "tools/_v155_themes.json").write_text(json.dumps({"themes": T155, "train": TR155, "heldout": HO155}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_155(src):
    src = src.replace("# --- V154 overlays (new vs V50) ---", "# --- V155 overlays (new vs V50) ---")
    src = src.replace("# --- V154 overlays (new vs V49) ---", "# --- V155 overlays (new vs V49) ---")
    for a, b in [
        ("ASHFORD bait 78.78", "ASHHOLM bait 79.79"),
        ("CEDARF bait 80.80", "CEDARH bait 81.81"),
        ("DAWNF ghost 92.92", "DAWNH ghost 93.93"),
        ("GLENF bait 73.73", "GLENH bait 74.74"),
        ("JADEF bait 64.64", "JADEH bait 65.65"),
        ("NETHERF bait 81.81", "NETHERH bait 82.82"),
        ("ash mist + stone ticks (V154-only)", "ash mist + stone ticks (V155-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD154 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v154_themes.json").read_text(encoding="utf-8"))["themes"])
NEW155 = "_".join(t[0] for t in T155)

out = (S / "c1031_vision_v154_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1031", "C1037"), ("c1031", "c1037"), ("V154", "V155"), ("v154", "v155"),
    ("_v154c1031", "_v155c1037"),
    ("Harder than V153", "Harder than V154"), ("harder than V153", "harder than V154"),
    (OLD154, NEW155),
    ("V154 keeps floor", "V155 keeps floor"),
    ("C1031 design+fixtures; no VL claim", "C1037 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1032 VL smoke", "fixtures only; claim deferred to C1038 VL smoke"),
    ("No claim until C1032 VL", "No claim until C1038 VL"),
    ("kept on V154", "kept on V155"),
    ("vision_images_v154", "vision_images_v155"),
    ("VL_GATE_V154", "VL_GATE_V155"), ("vl_gate_v154", "vl_gate_v155"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V153: ashford, cedarford, dawnford, elmford, fernford, glenford, hazeford, inkford,\njadeford, knotford, lakeford, mossford, netherford, oakford, pineford, quillford, reedford, stoneford.",
    "NEW themes vs V154: ashhholm, cedarholm, dawnholm, elmholm, fernholm, glenholm, hazeholm, inkholm,\njadeholm, knotholm, lakeholm, mossholm, netherholm, oakholm, pineholm, quillholm, reedholm, stoneholm.".replace("ashhholm","ashholm"),
)
out = replace_specs(out, build_specs(T155, "v155", "V155", TR155))
out = retarget_155(out)
(S / "c1037_vision_v155_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1032_vision_v154_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1032", "C1038"), ("c1032", "c1038"), ("V154", "V155"), ("v154", "v155"),
    ("vision_images_v154", "vision_images_v155"),
    ("VL_GATE_V154", "VL_GATE_V155"), ("vl_gate_v154", "vl_gate_v155"),
    ("runs/vision_v154", "runs/vision_v155"),
]:
    out = out.replace(a, b)
(S / "c1038_vision_v155_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1033_vision_v154_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1033", "C1039"), ("c1033", "c1039"), ("V154", "V155"), ("v154", "v155"),
    ("vision_images_v154h", "vision_images_v155h"),
    ("vision_images_v154", "vision_images_v155"),
    ("VL_GATE_V154", "VL_GATE_V155"), ("vl_gate_v154", "vl_gate_v155"),
    ("runs/vision_v154h", "runs/vision_v155h"),
    ("_v154c1031", "_v155c1037"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T155, "v155h", "V155H", HO155))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v155h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v155"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v155" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v155h_c1039"'); seen_run = True; continue
    out2.append(ln)
(S / "c1039_vision_v155_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1028_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1028", "C1040"), ("c1028", "c1040"),
    ("conf_gate_stretch_c1028", "conf_gate_stretch_c1040"),
    ("after V153", "after V155"), ("after V154", "after V155"),
    ("cg78_", "cg79_"),
]:
    out = out.replace(a, b)
(S / "c1040_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence")

out = (S / "c1035_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1035", "C1041"), ("c1035", "c1041"),
    ("capture_regression_c1035", "capture_regression_c1041"),
    ("after C1031-C1034", "after C1037-C1040"),
    ("V4-V154+heldout", "V4-V155+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V154", DOC / "C1032_VISION_V154_SMOKE.json"),'
if needle in out and "VISION_V155_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V155", DOC / "C1038_VISION_V155_SMOKE.json"),\n    ("V155_heldout", DOC / "C1039_VISION_V155_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1041_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1036_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1036", "C1042"), ("c1036", "c1042"),
    ("C1032", "C1038"), ("C1033", "C1039"), ("C1035", "C1041"),
    ("C1031", "C1037"),
    ("V154", "V155"), ("v154", "v155"),
    ("V153", "V154"), ("v153", "v154"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c650 = load("docs/r50/C1034_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1034_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'c656 = load("docs/r50/C1028_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1040_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace('"source": "C1034"', '"source": "C1034"')
out = out.replace('"source": "C1028"', '"source": "C1040"')
out = out.replace(
    "stage_ready = bool(v155_claim and v155h_claim and v155 >= GATE and v155h >= GATE and capture_pass and disjoint and u2c_pass)",
    "stage_ready = bool(v155_claim and v155h_claim and v155 >= GATE and v155h >= GATE and capture_pass and disjoint and conf_pass)",
)
out = out.replace(
    'f"- C1040: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C1040: confidence-gate pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- C1034: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C1040: confidence-gate pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- confidence-gate (prior C1028): pass={conf_pass} rate={conf_rate}"',
    'f"- product-U2C (prior C1034): replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- confidence-gate (prior C1040): pass={conf_pass} rate={conf_rate}"',
    'f"- product-U2C (prior C1034): replace={replace} pass={u2c_pass}"',
)
(S / "c1042_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T155 if t[0].endswith("b")])
print("qty", TR155[1], HO155[1], "po", TR155[8], HO155[8], "sla", TR155[6], HO155[6])
print("done")
