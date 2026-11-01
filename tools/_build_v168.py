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

# *wick ; qty TR 740+780 HO 840+760; PO TR 780+740 HO 840+760; SLA TR 480+520 HO 360+400
T168 = [
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
TR168 = [
    [1105.0, 1122.5, 915.0],[740, 780, 780],[1028.0, 1057.25, 895.0],[1161.0, 1178.0, 985.0],
    [1223.0, 1247.0, 955.0],[981, 997, 913],[480.0, 520.0, 470.0],[1071.0, 1102.75, 919.0],
    [780.0, 740.0, 720.0],[1138.0, 1126.0, 916.0],[1,1,0],[0,0,0],
    [1204.0, 1225.5, 941.0],[1,0,0],[753, 745, 723],[771, 755, 746],[1,0,0],[797, 773, 743],
]
HO168 = [
    [975.0, 987.75, 868.0],[840, 760, 810],[933.0, 946.5, 856.0],[1048.0, 1064.0, 897.0],
    [1089.0, 1105.0, 892.0],[883, 897, 861],[360.0, 400.0, 450.0],[959.0, 980.75, 868.0],
    [840.0, 760.0, 700.0],[1006.0, 992.0, 863.0],[1,1,0],[0,0,0],
    [1041.0, 1056.5, 878.0],[1,0,0],[729, 726, 721],[745, 739, 727],[1,0,0],[755, 749, 728],
]
(ROOT / "tools/_v168_themes.json").write_text(json.dumps({"themes": T168, "train": TR168, "heldout": HO168}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_168(src):
    src = src.replace("# --- V167 overlays (new vs V50) ---", "# --- V168 overlays (new vs V50) ---")
    src = src.replace("# --- V167 overlays (new vs V49) ---", "# --- V168 overlays (new vs V49) ---")
    for a, b in [
        ("ASHMERE bait 81.81", "ASHWICK bait 82.82"),
        ("CEDARM bait 83.83", "CEDARW bait 84.84"),
        ("DAWNM ghost 95.95", "DAWNW ghost 96.96"),
        ("GLENM bait 76.76", "GLENW bait 77.77"),
        ("JADEM bait 67.67", "JADEW bait 68.68"),
        ("NETHERM bait 84.84", "NETHERW bait 85.85"),
        ("ash mist + stone ticks (V167-only)", "ash mist + stone ticks (V168-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD167 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v167_themes.json").read_text(encoding="utf-8"))["themes"])
NEW168 = "_".join(t[0] for t in T168)

out = (S / "c1109_vision_v167_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1109", "C1115"), ("c1109", "c1115"), ("V167", "V168"), ("v167", "v168"),
    ("_v167c1109", "_v168c1115"),
    ("Harder than V166", "Harder than V167"), ("harder than V166", "harder than V167"),
    (OLD167, NEW168),
    ("V167 keeps floor", "V168 keeps floor"),
    ("C1109 design+fixtures; no VL claim", "C1115 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1110 VL smoke", "fixtures only; claim deferred to C1116 VL smoke"),
    ("No claim until C1110 VL", "No claim until C1116 VL"),
    ("kept on V167", "kept on V168"),
    ("vision_images_v167", "vision_images_v168"),
    ("VL_GATE_V167", "VL_GATE_V168"), ("vl_gate_v167", "vl_gate_v168"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V166:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V167: ashwicк, cedarwick, dawnwick, elmwick, fernwick, glenwick, hazewick, inkwick,\njadewick, knotwick, lakewick, mosswick, netherwick, oakwick, pinewick, quillwick, reedwick, stonewick.".replace("ashwicк", "ashwick"),
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T168, "v168", "V168", TR168))
out = retarget_168(out)
(S / "c1115_vision_v168_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1110_vision_v167_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1110", "C1116"), ("c1110", "c1116"), ("V167", "V168"), ("v167", "v168"),
    ("vision_images_v167", "vision_images_v168"),
    ("VL_GATE_V167", "VL_GATE_V168"), ("vl_gate_v167", "vl_gate_v168"),
    ("runs/vision_v167", "runs/vision_v168"),
]:
    out = out.replace(a, b)
(S / "c1116_vision_v168_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1111_vision_v167_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1111", "C1117"), ("c1111", "c1117"), ("V167", "V168"), ("v167", "v168"),
    ("vision_images_v167h", "vision_images_v168h"),
    ("vision_images_v167", "vision_images_v168"),
    ("VL_GATE_V167", "VL_GATE_V168"), ("vl_gate_v167", "vl_gate_v168"),
    ("runs/vision_v167h", "runs/vision_v168h"),
    ("_v167c1109", "_v168c1115"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T168, "v168h", "V168H", HO168))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v168h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v168"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v168" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v168h_c1117"'); seen_run = True; continue
    out2.append(ln)
(S / "c1117_vision_v168_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1106_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C1106", "C1118"), ("c1106", "c1118"),
    ("product_u2c_c1106", "product_u2c_c1118"),
    ("after V166", "after V168"), ("after V167", "after V168"),
]:
    out = out.replace(a, b)
(S / "c1118_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c1113_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1113", "C1119"), ("c1113", "c1119"),
    ("capture_regression_c1113", "capture_regression_c1119"),
    ("after C1109-C1112", "after C1115-C1118"),
    ("V4-V167+heldout", "V4-V168+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V167", DOC / "C1110_VISION_V167_SMOKE.json"),'
if needle in out and "VISION_V168_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V168", DOC / "C1116_VISION_V168_SMOKE.json"),\n    ("V168_heldout", DOC / "C1117_VISION_V168_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1119_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1114_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1114", "C1120"), ("c1114", "c1120"),
    ("C1110", "C1116"), ("C1111", "C1117"), ("C1113", "C1119"),
    ("C1109", "C1115"),
    ("V167", "V168"), ("v167", "v168"),
    ("V166", "V167"), ("v166", "v167"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C1112_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1112_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C1106_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1118_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace('"source": "C1106"', '"source": "C1118"')
out = out.replace('"source": "C1112"', '"source": "C1112"')
out = out.replace(
    "stage_ready = bool(v168_claim and v168h_claim and v168 >= GATE and v168h >= GATE and capture_pass and disjoint and conf_pass)",
    "stage_ready = bool(v168_claim and v168h_claim and v168 >= GATE and v168h >= GATE and capture_pass and disjoint and u2c_pass)",
)
out = out.replace(
    'f"- C1118: confidence-gate pass={conf_pass} rate={conf_rate}"',
    'f"- C1118: product-U2C replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- C1112: confidence-gate pass={conf_pass} rate={conf_rate}"',
    'f"- C1118: product-U2C replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- product-U2C (prior C1106): replace={replace} pass={u2c_pass}"',
    'f"- confidence-gate (prior C1112): pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- product-U2C (prior C1118): replace={replace} pass={u2c_pass}"',
    'f"- confidence-gate (prior C1112): pass={conf_pass} rate={conf_rate}"',
)
(S / "c1120_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T168 if t[0].endswith("b")])
print("qty", TR168[1], HO168[1], "po", TR168[8], HO168[8], "sla", TR168[6], HO168[6])
# avoid 780+740 TR summing to 1520 which OCR might confuse with 1560 lesson — 780+740=1520 is OK (lesson was 1560 specifically)
print("done")
