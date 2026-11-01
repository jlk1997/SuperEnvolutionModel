# -*- coding: utf-8 -*-
from __future__ import annotations
import json, re
from pathlib import Path
ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"
BAN = {755, 756, 770, 750, 830, 1830, 1560}

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

def check(rows, label):
    for i, row in enumerate(rows):
        for v in row:
            if isinstance(v, (int, float)) and int(v) in BAN:
                raise SystemExit(f"banned {v} in {label}[{i}]={row}")

# *vale ; qty TR 840+760 HO 740+780; PO TR 840+760 HO 780+740; SLA TR 460+500 HO 360+400
T175 = [
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
TR175 = [
    [1168.0, 1185.5, 978.0],[840, 760, 820],[1091.0, 1120.25, 958.0],[1224.0, 1241.0, 1048.0],
    [1286.0, 1310.0, 1018.0],[1044, 1060, 976],[460.0, 500.0, 540.0],[1134.0, 1165.75, 982.0],
    [840.0, 760.0, 790.0],[1201.0, 1189.0, 979.0],[1,1,0],[0,0,0],
    [1267.0, 1288.5, 1004.0],[1,0,0],[816, 808, 786],[834, 818, 748],[1,0,0],[860, 836, 806],
]
HO175 = [
    [1038.0, 1050.75, 931.0],[740, 780, 820],[996.0, 1009.5, 919.0],[1111.0, 1127.0, 960.0],
    [1152.0, 1168.0, 955.0],[946, 960, 924],[360.0, 400.0, 520.0],[1022.0, 1043.75, 931.0],
    [780.0, 740.0, 780.0],[1069.0, 1055.0, 926.0],[1,1,0],[0,0,0],
    [1104.0, 1119.5, 941.0],[1,0,0],[794, 789, 784],[808, 802, 790],[1,0,0],[818, 812, 791],
]
check(TR175, "TR"); check(HO175, "HO")

(ROOT / "tools/_v175_themes.json").write_text(json.dumps({"themes": T175, "train": TR175, "heldout": HO175}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_175(src):
    src = src.replace("# --- V174 overlays (new vs V50) ---", "# --- V175 overlays (new vs V50) ---")
    src = src.replace("# --- V174 overlays (new vs V49) ---", "# --- V175 overlays (new vs V49) ---")
    for a, b in [
        ("ASHDALE bait 88.88", "ASHVALE bait 89.89"),
        ("CEDARD bait 90.90", "CEDARV bait 91.91"),
        ("DAWND ghost 13.13", "DAWNV ghost 14.14"),
        ("GLEND bait 83.83", "GLENV bait 84.84"),
        ("JADED bait 74.74", "JADEV bait 75.75"),
        ("NETHERD bait 91.91", "NETHERV bait 92.92"),
        ("ash mist + stone ticks (V174-only)", "ash mist + stone ticks (V175-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD174 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v174_themes.json").read_text(encoding="utf-8"))["themes"])
NEW175 = "_".join(t[0] for t in T175)

out = (S / "c1151_vision_v174_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1151", "C1157"), ("c1151", "c1157"), ("V174", "V175"), ("v174", "v175"),
    ("_v174c1151", "_v175c1157"),
    ("Harder than V173", "Harder than V174"), ("harder than V173", "harder than V174"),
    (OLD174, NEW175),
    ("V174 keeps floor", "V175 keeps floor"),
    ("C1151 design+fixtures; no VL claim", "C1157 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1152 VL smoke", "fixtures only; claim deferred to C1158 VL smoke"),
    ("No claim until C1152 VL", "No claim until C1158 VL"),
    ("kept on V174", "kept on V175"),
    ("vision_images_v174", "vision_images_v175"),
    ("VL_GATE_V174", "VL_GATE_V175"), ("vl_gate_v174", "vl_gate_v175"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V173:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V174: ashvale, cedarvale, dawnvale, elmvale, fernvale, glenvale, hazevale, inkvale,\njadevale, knotvale, lakevale, mossvale, nethervale, oakvale, pinevale, quillvale, reedvale, stonevale.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T175, "v175", "V175", TR175))
out = retarget_175(out)
(S / "c1157_vision_v175_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1152_vision_v174_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1152", "C1158"), ("c1152", "c1158"), ("V174", "V175"), ("v174", "v175"),
    ("vision_images_v174", "vision_images_v175"),
    ("VL_GATE_V174", "VL_GATE_V175"), ("vl_gate_v174", "vl_gate_v175"),
    ("runs/vision_v174", "runs/vision_v175"),
]:
    out = out.replace(a, b)
(S / "c1158_vision_v175_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1153_vision_v174_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1153", "C1159"), ("c1153", "c1159"), ("V174", "V175"), ("v174", "v175"),
    ("vision_images_v174h", "vision_images_v175h"),
    ("vision_images_v174", "vision_images_v175"),
    ("VL_GATE_V174", "VL_GATE_V175"), ("vl_gate_v174", "vl_gate_v175"),
    ("runs/vision_v174h", "runs/vision_v175h"),
    ("_v174c1151", "_v175c1157"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T175, "v175h", "V175H", HO175))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v175h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v175"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v175" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v175h_c1159"'); seen_run = True; continue
    out2.append(ln)
(S / "c1159_vision_v175_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1148_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1148", "C1160"), ("c1148", "c1160"),
    ("conf_gate_stretch_c1148", "conf_gate_stretch_c1160"),
    ("after V173", "after V175"), ("after V174", "after V175"),
    ("cg88_", "cg89_"),
]:
    out = out.replace(a, b)
(S / "c1160_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence")

out = (S / "c1155_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1155", "C1161"), ("c1155", "c1161"),
    ("capture_regression_c1155", "capture_regression_c1161"),
    ("after C1151-C1154", "after C1157-C1160"),
    ("V4-V174+heldout", "V4-V175+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V174", DOC / "C1152_VISION_V174_SMOKE.json"),'
if needle in out and "VISION_V175_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V175", DOC / "C1158_VISION_V175_SMOKE.json"),\n    ("V175_heldout", DOC / "C1159_VISION_V175_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1161_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1156_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1156", "C1162"), ("c1156", "c1162"),
    ("C1152", "C1158"), ("C1153", "C1159"), ("C1155", "C1161"),
    ("C1151", "C1157"),
    ("V174", "V175"), ("v174", "v175"),
    ("V173", "V174"), ("v173", "v174"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C1148_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1160_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C1154_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1154_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace('"source": "C1154"', '"source": "C1154"')
out = out.replace('"source": "C1148"', '"source": "C1160"')
out = out.replace(
    "stage_ready = bool(v175_claim and v175h_claim and v175 >= GATE and v175h >= GATE and capture_pass and disjoint and u2c_pass)",
    "stage_ready = bool(v175_claim and v175h_claim and v175 >= GATE and v175h >= GATE and capture_pass and disjoint and conf_pass)",
)
out = out.replace(
    'f"- C1160: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C1160: confidence-gate pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- C1154: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C1160: confidence-gate pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- confidence-gate (prior C1148): pass={conf_pass} rate={conf_rate}"',
    'f"- product-U2C (prior C1154): replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- confidence-gate (prior C1160): pass={conf_pass} rate={conf_rate}"',
    'f"- product-U2C (prior C1154): replace={replace} pass={u2c_pass}"',
)
(S / "c1162_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T175 if t[0].endswith("b")])
print("qty", TR175[1], HO175[1], "po", TR175[8], HO175[8], "sla", TR175[6], HO175[6], "fax", TR175[15], HO175[15])
print("done")
