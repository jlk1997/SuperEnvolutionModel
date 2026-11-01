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

# *wick ; qty TR 840+760 HO 740+780; PO TR 840+760 HO 780+740; SLA TR 460+500 HO 360+400
T157 = [
    ["ashwick","recv","paid_total","ASHWICK GRAIN RECV","RECV","x"],
    ["cedarwick","wh","qty_sum","WH CEDARWICK BIN","RECV","x"],
    ["dawnwick","refund","refund_done","DAWNWICK PATCH REFUND","DONE","x"],
    ["elmwick","tax","tax_base_paid","ELMWICK TAX SLIP","TAX","x"],
    ["fernwick","pay","payroll_active","FERNWICK PAYROLL","PAY","x"],
    ["glenwick","ship","ship_ok","GLENWICK SHIP DOCK","SHIP","x"],
    ["hazewick","sla","sla_ok_hours","HAZEWICK SLA CARD","SLA","x"],
    ["inkwick","exp","exp_sum","INKWICK EXPENSE","EXP","x"],
    ["jadewick","po","po_open","JADEWICK PO SHEET","PO","x"],
    ["knotwick","order","order_paid","KNOTWICK ORDER","ORD","x"],
    ["lakewick","dup","dup_mark","LAKEWICK DUP MARK","DUP","x"],
    ["mosswick","zero","zero_check","MOSSWICK AIR ZERO","ZERO","x"],
    ["netherwick","ledger","ledger_net","NETHERWICK LEDGER","LED","x"],
    ["oakwick","ui","ui_ok","OAKWICK UI SCAN","UI","x"],
    ["pinewick","stack","stack_count","PINEWICK STACK","STK","x"],
    ["quillwick","fax","fax_pages","QUILLWICK FAX","FAX","x"],
    ["reedwick","glare","glare_ok","REEDWICK GLARE","GLR","x"],
    ["stonewick","tab","tab_index","STONEWICK TAB INDEX","TAB","x"],
]
TR157 = [
    [1006.0, 1023.5, 816.0],[840, 760, 670],[929.0, 958.25, 796.0],[1062.0, 1079.0, 886.0],
    [1124.0, 1148.0, 856.0],[882, 898, 814],[460.0, 500.0, 360.0],[972.0, 1003.75, 820.0],
    [840.0, 760.0, 730.0],[1039.0, 1027.0, 817.0],[1,1,0],[0,0,0],
    [1105.0, 1126.5, 842.0],[1,0,0],[654, 646, 624],[672, 656, 647],[1,0,0],[698, 674, 644],
]
HO157 = [
    [876.0, 888.75, 769.0],[740, 780, 730],[834.0, 847.5, 757.0],[949.0, 965.0, 798.0],
    [990.0, 1006.0, 793.0],[784, 798, 762],[360.0, 400.0, 340.0],[860.0, 881.75, 769.0],
    [780.0, 740.0, 710.0],[907.0, 893.0, 764.0],[1,1,0],[0,0,0],
    [942.0, 957.5, 779.0],[1,0,0],[630, 627, 622],[646, 640, 628],[1,0,0],[656, 650, 629],
]
(ROOT / "tools/_v157_themes.json").write_text(json.dumps({"themes": T157, "train": TR157, "heldout": HO157}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_157(src):
    src = src.replace("# --- V156 overlays (new vs V50) ---", "# --- V157 overlays (new vs V50) ---")
    src = src.replace("# --- V156 overlays (new vs V49) ---", "# --- V157 overlays (new vs V49) ---")
    for a, b in [
        ("ASHMERE bait 70.70", "ASHWICK bait 71.71"),
        ("CEDARM bait 82.82", "CEDARW bait 83.83"),
        ("DAWNM ghost 94.94", "DAWNW ghost 95.95"),
        ("GLENM bait 75.75", "GLENW bait 76.76"),
        ("JADEM bait 66.66", "JADEW bait 67.67"),
        ("NETHERM bait 83.83", "NETHERW bait 84.84"),
        ("ash mist + stone ticks (V156-only)", "ash mist + stone ticks (V157-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD156 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v156_themes.json").read_text(encoding="utf-8"))["themes"])
NEW157 = "_".join(t[0] for t in T157)

out = (S / "c1043_vision_v156_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1043", "C1049"), ("c1043", "c1049"), ("V156", "V157"), ("v156", "v157"),
    ("_v156c1043", "_v157c1049"),
    ("Harder than V155", "Harder than V156"), ("harder than V155", "harder than V156"),
    (OLD156, NEW157),
    ("V156 keeps floor", "V157 keeps floor"),
    ("C1043 design+fixtures; no VL claim", "C1049 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1044 VL smoke", "fixtures only; claim deferred to C1050 VL smoke"),
    ("No claim until C1044 VL", "No claim until C1050 VL"),
    ("kept on V156", "kept on V157"),
    ("vision_images_v156", "vision_images_v157"),
    ("VL_GATE_V156", "VL_GATE_V157"), ("vl_gate_v156", "vl_gate_v157"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V155:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V156: ashwich, cedarwick, dawnwick, elmwick, fernwick, glenwick, hazewick, inkwick,\njadewick, knotwick, lakewick, mosswick, netherwick, oakwick, pinewick, quillwick, reedwick, stonewick.".replace("ashwich","ashwick"),
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T157, "v157", "V157", TR157))
out = retarget_157(out)
(S / "c1049_vision_v157_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1044_vision_v156_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1044", "C1050"), ("c1044", "c1050"), ("V156", "V157"), ("v156", "v157"),
    ("vision_images_v156", "vision_images_v157"),
    ("VL_GATE_V156", "VL_GATE_V157"), ("vl_gate_v156", "vl_gate_v157"),
    ("runs/vision_v156", "runs/vision_v157"),
]:
    out = out.replace(a, b)
(S / "c1050_vision_v157_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1045_vision_v156_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1045", "C1051"), ("c1045", "c1051"), ("V156", "V157"), ("v156", "v157"),
    ("vision_images_v156h", "vision_images_v157h"),
    ("vision_images_v156", "vision_images_v157"),
    ("VL_GATE_V156", "VL_GATE_V157"), ("vl_gate_v156", "vl_gate_v157"),
    ("runs/vision_v156h", "runs/vision_v157h"),
    ("_v156c1043", "_v157c1049"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T157, "v157h", "V157H", HO157))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v157h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v157"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v157" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v157h_c1051"'); seen_run = True; continue
    out2.append(ln)
(S / "c1051_vision_v157_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1040_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1040", "C1052"), ("c1040", "c1052"),
    ("conf_gate_stretch_c1040", "conf_gate_stretch_c1052"),
    ("after V155", "after V157"), ("after V156", "after V157"),
    ("cg79_", "cg80_"),
]:
    out = out.replace(a, b)
(S / "c1052_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence")

out = (S / "c1047_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1047", "C1053"), ("c1047", "c1053"),
    ("capture_regression_c1047", "capture_regression_c1053"),
    ("after C1043-C1046", "after C1049-C1052"),
    ("V4-V156+heldout", "V4-V157+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V156", DOC / "C1044_VISION_V156_SMOKE.json"),'
if needle in out and "VISION_V157_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V157", DOC / "C1050_VISION_V157_SMOKE.json"),\n    ("V157_heldout", DOC / "C1051_VISION_V157_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1053_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1048_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1048", "C1054"), ("c1048", "c1054"),
    ("C1044", "C1050"), ("C1045", "C1051"), ("C1047", "C1053"),
    ("C1043", "C1049"),
    ("V156", "V157"), ("v156", "v157"),
    ("V155", "V156"), ("v155", "v156"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c650 = load("docs/r50/C1046_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1046_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'c656 = load("docs/r50/C1040_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1052_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace('"source": "C1046"', '"source": "C1046"')
out = out.replace('"source": "C1040"', '"source": "C1052"')
out = out.replace(
    "stage_ready = bool(v157_claim and v157h_claim and v157 >= GATE and v157h >= GATE and capture_pass and disjoint and u2c_pass)",
    "stage_ready = bool(v157_claim and v157h_claim and v157 >= GATE and v157h >= GATE and capture_pass and disjoint and conf_pass)",
)
out = out.replace(
    'f"- C1052: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C1052: confidence-gate pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- C1046: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C1052: confidence-gate pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- confidence-gate (prior C1040): pass={conf_pass} rate={conf_rate}"',
    'f"- product-U2C (prior C1046): replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- confidence-gate (prior C1052): pass={conf_pass} rate={conf_rate}"',
    'f"- product-U2C (prior C1046): replace={replace} pass={u2c_pass}"',
)
(S / "c1054_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T157 if t[0].endswith("b")])
print("qty", TR157[1], HO157[1], "po", TR157[8], HO157[8], "sla", TR157[6], HO157[6])
print("done")
