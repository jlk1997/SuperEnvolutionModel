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

# *mere ; qty TR 840+760 HO 740+780; PO TR 840+760 HO 780+740; SLA TR 460+500 HO 360+400
T167 = [
    ["ashmere","recv","paid_total","ASHMERE GRAIN RECV","RECV","x"],
    ["cedarmere","wh","qty_sum","WH CEDARMERE BIN","RECV","x"],
    ["dawnmere","refund","refund_done","DAWNMERE PATCH REFUND","DONE","x"],
    ["elmmere","tax","tax_base_paid","ELMMERE TAX SLIP","TAX","x"],
    ["fernmere","pay","payroll_active","FERNMERE PAYROLL","PAY","x"],
    ["glenmere","ship","ship_ok","GLENMERE SHIP DOCK","SHIP","x"],
    ["hazemere","sla","sla_ok_hours","HAZEMERE SLA CARD","SLA","x"],
    ["inkmere","exp","exp_sum","INKMERE EXPENSE","EXP","x"],
    ["jademere","po","po_open","JADEMERE PO SHEET","PO","x"],
    ["knotmere","order","order_paid","KNOTMERE ORDER","ORD","x"],
    ["lakemere","dup","dup_mark","LAKEMERE DUP MARK","DUP","x"],
    ["mossmere","zero","zero_check","MOSSMERE AIR ZERO","ZERO","x"],
    ["nethermere","ledger","ledger_net","NETHERMERE LEDGER","LED","x"],
    ["oakmere","ui","ui_ok","OAKMERE UI SCAN","UI","x"],
    ["pinemere","stack","stack_count","PINEMERE STACK","STK","x"],
    ["quillmere","fax","fax_pages","QUILLMERE FAX","FAX","x"],
    ["reedmere","glare","glare_ok","REEDMERE GLARE","GLR","x"],
    ["stonemere","tab","tab_index","STONEMERE TAB INDEX","TAB","x"],
]
TR167 = [
    [1096.0, 1113.5, 906.0],[840, 760, 770],[1019.0, 1048.25, 886.0],[1152.0, 1169.0, 976.0],
    [1214.0, 1238.0, 946.0],[972, 988, 904],[460.0, 500.0, 460.0],[1062.0, 1093.75, 910.0],
    [840.0, 760.0, 710.0],[1129.0, 1117.0, 907.0],[1,1,0],[0,0,0],
    [1195.0, 1216.5, 932.0],[1,0,0],[744, 736, 714],[762, 746, 737],[1,0,0],[788, 764, 734],
]
HO167 = [
    [966.0, 978.75, 859.0],[740, 780, 820],[924.0, 937.5, 847.0],[1039.0, 1055.0, 888.0],
    [1080.0, 1096.0, 883.0],[874, 888, 852],[360.0, 400.0, 440.0],[950.0, 971.75, 859.0],
    [780.0, 740.0, 690.0],[997.0, 983.0, 854.0],[1,1,0],[0,0,0],
    [1032.0, 1047.5, 869.0],[1,0,0],[720, 717, 712],[736, 730, 718],[1,0,0],[746, 740, 719],
]
(ROOT / "tools/_v167_themes.json").write_text(json.dumps({"themes": T167, "train": TR167, "heldout": HO167}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_167(src):
    src = src.replace("# --- V166 overlays (new vs V50) ---", "# --- V167 overlays (new vs V50) ---")
    src = src.replace("# --- V166 overlays (new vs V49) ---", "# --- V167 overlays (new vs V49) ---")
    for a, b in [
        ("ASHHOLM bait 80.80", "ASHMERE bait 81.81"),
        ("CEDARH bait 82.82", "CEDARM bait 83.83"),
        ("DAWNH ghost 94.94", "DAWNM ghost 95.95"),
        ("GLENH bait 75.75", "GLENM bait 76.76"),
        ("JADEH bait 66.66", "JADEM bait 67.67"),
        ("NETHERH bait 83.83", "NETHERM bait 84.84"),
        ("ash mist + stone ticks (V166-only)", "ash mist + stone ticks (V167-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD166 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v166_themes.json").read_text(encoding="utf-8"))["themes"])
NEW167 = "_".join(t[0] for t in T167)

out = (S / "c1103_vision_v166_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1103", "C1109"), ("c1103", "c1109"), ("V166", "V167"), ("v166", "v167"),
    ("_v166c1103", "_v167c1109"),
    ("Harder than V165", "Harder than V166"), ("harder than V165", "harder than V166"),
    (OLD166, NEW167),
    ("V166 keeps floor", "V167 keeps floor"),
    ("C1103 design+fixtures; no VL claim", "C1109 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1104 VL smoke", "fixtures only; claim deferred to C1110 VL smoke"),
    ("No claim until C1104 VL", "No claim until C1110 VL"),
    ("kept on V166", "kept on V167"),
    ("vision_images_v166", "vision_images_v167"),
    ("VL_GATE_V166", "VL_GATE_V167"), ("vl_gate_v166", "vl_gate_v167"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V165:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V166: ashmere, cedarmere, dawnmere, elmmere, fernmere, glenmere, hazemere, inkmere,\njademere, knotmere, lakemere, mossmere, nethermere, oakmere, pinemere, quillmere, reedmere, stonemere.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T167, "v167", "V167", TR167))
out = retarget_167(out)
(S / "c1109_vision_v167_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1104_vision_v166_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1104", "C1110"), ("c1104", "c1110"), ("V166", "V167"), ("v166", "v167"),
    ("vision_images_v166", "vision_images_v167"),
    ("VL_GATE_V166", "VL_GATE_V167"), ("vl_gate_v166", "vl_gate_v167"),
    ("runs/vision_v166", "runs/vision_v167"),
]:
    out = out.replace(a, b)
(S / "c1110_vision_v167_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1105_vision_v166_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1105", "C1111"), ("c1105", "c1111"), ("V166", "V167"), ("v166", "v167"),
    ("vision_images_v166h", "vision_images_v167h"),
    ("vision_images_v166", "vision_images_v167"),
    ("VL_GATE_V166", "VL_GATE_V167"), ("vl_gate_v166", "vl_gate_v167"),
    ("runs/vision_v166h", "runs/vision_v167h"),
    ("_v166c1103", "_v167c1109"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T167, "v167h", "V167H", HO167))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v167h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v167"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v167" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v167h_c1111"'); seen_run = True; continue
    out2.append(ln)
(S / "c1111_vision_v167_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1100_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1100", "C1112"), ("c1100", "c1112"),
    ("conf_gate_stretch_c1100", "conf_gate_stretch_c1112"),
    ("after V165", "after V167"), ("after V166", "after V167"),
    ("cg84_", "cg85_"),
]:
    out = out.replace(a, b)
(S / "c1112_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence")

out = (S / "c1107_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1107", "C1113"), ("c1107", "c1113"),
    ("capture_regression_c1107", "capture_regression_c1113"),
    ("after C1103-C1106", "after C1109-C1112"),
    ("V4-V166+heldout", "V4-V167+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V166", DOC / "C1104_VISION_V166_SMOKE.json"),'
if needle in out and "VISION_V167_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V167", DOC / "C1110_VISION_V167_SMOKE.json"),\n    ("V167_heldout", DOC / "C1111_VISION_V167_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1113_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1108_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1108", "C1114"), ("c1108", "c1114"),
    ("C1104", "C1110"), ("C1105", "C1111"), ("C1107", "C1113"),
    ("C1103", "C1109"),
    ("V166", "V167"), ("v166", "v167"),
    ("V165", "V166"), ("v165", "v166"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C1100_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1112_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C1106_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1106_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace('"source": "C1106"', '"source": "C1106"')
out = out.replace('"source": "C1100"', '"source": "C1112"')
out = out.replace(
    "stage_ready = bool(v167_claim and v167h_claim and v167 >= GATE and v167h >= GATE and capture_pass and disjoint and u2c_pass)",
    "stage_ready = bool(v167_claim and v167h_claim and v167 >= GATE and v167h >= GATE and capture_pass and disjoint and conf_pass)",
)
out = out.replace(
    'f"- C1112: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C1112: confidence-gate pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- C1106: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C1112: confidence-gate pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- confidence-gate (prior C1100): pass={conf_pass} rate={conf_rate}"',
    'f"- product-U2C (prior C1106): replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- confidence-gate (prior C1112): pass={conf_pass} rate={conf_rate}"',
    'f"- product-U2C (prior C1106): replace={replace} pass={u2c_pass}"',
)
(S / "c1114_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T167 if t[0].endswith("b")])
print("qty", TR167[1], HO167[1], "po", TR167[8], HO167[8], "sla", TR167[6], HO167[6])
print("done")
