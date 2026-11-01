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

# *ford ; qty TR 740+780 HO 840+760; PO TR 780+740 HO 840+760; SLA TR 480+520 HO 360+400
T176 = [
    ["ashford","recv","paid_total","ASHFORD GRAIN RECV","RECV","x"],
    ["cedarford","wh","qty_sum","WH CEDARFORD BIN","RECV","x"],
    ["dawnford","refund","refund_done","DAWNFORD PATCH REFUND","DONE","x"],
    ["elmford","tax","tax_base_paid","ELMFORD TAX SLIP","TAX","x"],
    ["fernford","pay","payroll_active","FERNFORD PAYROLL","PAY","x"],
    ["glenford","ship","ship_ok","GLENFORD SHIP DOCK","SHIP","x"],
    ["hazeford","sla","sla_ok_hours","HAZEFORD SLA CARD","SLA","x"],
    ["inkford","exp","exp_sum","INKFORD EXPENSE","EXP","x"],
    ["jadeford","po","po_open","JADEFORD PO SHEET","PO","x"],
    ["knotford","order","order_paid","KNOTFORD ORDER","ORD","x"],
    ["lakeford","dup","dup_mark","LAKEFORD DUP MARK","DUP","x"],
    ["mossford","zero","zero_check","MOSSFORD AIR ZERO","ZERO","x"],
    ["netherford","ledger","ledger_net","NETHERFORD LEDGER","LED","x"],
    ["oakford","ui","ui_ok","OAKFORD UI SCAN","UI","x"],
    ["pineford","stack","stack_count","PINEFORD STACK","STK","x"],
    ["quillford","fax","fax_pages","QUILLFORD FAX","FAX","x"],
    ["reedford","glare","glare_ok","REEDFORD GLARE","GLR","x"],
    ["stoneford","tab","tab_index","STONEFORD TAB INDEX","TAB","x"],
]
TR176 = [
    [1177.0, 1194.5, 987.0],[740, 780, 820],[1100.0, 1129.25, 967.0],[1233.0, 1250.0, 1057.0],
    [1295.0, 1319.0, 1027.0],[1053, 1069, 985],[480.0, 520.0, 550.0],[1143.0, 1174.75, 991.0],
    [780.0, 740.0, 790.0],[1210.0, 1198.0, 988.0],[1,1,0],[0,0,0],
    [1276.0, 1297.5, 1013.0],[1,0,0],[825, 817, 795],[843, 827, 748],[1,0,0],[869, 845, 815],
]
HO176 = [
    [1047.0, 1059.75, 940.0],[840, 760, 820],[1005.0, 1018.5, 928.0],[1120.0, 1136.0, 969.0],
    [1161.0, 1177.0, 964.0],[955, 969, 933],[360.0, 400.0, 530.0],[1031.0, 1052.75, 940.0],
    [840.0, 760.0, 790.0],[1078.0, 1064.0, 935.0],[1,1,0],[0,0,0],
    [1113.0, 1128.5, 950.0],[1,0,0],[803, 798, 793],[817, 811, 799],[1,0,0],[827, 821, 800],
]
check(TR176, "TR"); check(HO176, "HO")

(ROOT / "tools/_v176_themes.json").write_text(json.dumps({"themes": T176, "train": TR176, "heldout": HO176}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_176(src):
    src = src.replace("# --- V175 overlays (new vs V50) ---", "# --- V176 overlays (new vs V50) ---")
    src = src.replace("# --- V175 overlays (new vs V49) ---", "# --- V176 overlays (new vs V49) ---")
    for a, b in [
        ("ASHVALE bait 89.89", "ASHFORD bait 90.90"),
        ("CEDARV bait 91.91", "CEDARF bait 92.92"),
        ("DAWNV ghost 14.14", "DAWNF ghost 15.15"),
        ("GLENV bait 84.84", "GLENF bait 85.85"),
        ("JADEV bait 75.75", "JADEF bait 76.76"),
        ("NETHERV bait 92.92", "NETHERF bait 93.93"),
        ("ash mist + stone ticks (V175-only)", "ash mist + stone ticks (V176-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD175 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v175_themes.json").read_text(encoding="utf-8"))["themes"])
NEW176 = "_".join(t[0] for t in T176)

out = (S / "c1157_vision_v175_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1157", "C1163"), ("c1157", "c1163"), ("V175", "V176"), ("v175", "v176"),
    ("_v175c1157", "_v176c1163"),
    ("Harder than V174", "Harder than V175"), ("harder than V174", "harder than V175"),
    (OLD175, NEW176),
    ("V175 keeps floor", "V176 keeps floor"),
    ("C1157 design+fixtures; no VL claim", "C1163 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1158 VL smoke", "fixtures only; claim deferred to C1164 VL smoke"),
    ("No claim until C1158 VL", "No claim until C1164 VL"),
    ("kept on V175", "kept on V176"),
    ("vision_images_v175", "vision_images_v176"),
    ("VL_GATE_V175", "VL_GATE_V176"), ("vl_gate_v175", "vl_gate_v176"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V174:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V175: ashford, cedarford, dawnford, elmford, fernford, glenford, hazeford, inkford,\njadeford, knotford, lakeford, mossford, netherford, oakford, pineford, quillford, reedford, stoneford.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T176, "v176", "V176", TR176))
out = retarget_176(out)
(S / "c1163_vision_v176_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1158_vision_v175_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1158", "C1164"), ("c1158", "c1164"), ("V175", "V176"), ("v175", "v176"),
    ("vision_images_v175", "vision_images_v176"),
    ("VL_GATE_V175", "VL_GATE_V176"), ("vl_gate_v175", "vl_gate_v176"),
    ("runs/vision_v175", "runs/vision_v176"),
]:
    out = out.replace(a, b)
(S / "c1164_vision_v176_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1159_vision_v175_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1159", "C1165"), ("c1159", "c1165"), ("V175", "V176"), ("v175", "v176"),
    ("vision_images_v175h", "vision_images_v176h"),
    ("vision_images_v175", "vision_images_v176"),
    ("VL_GATE_V175", "VL_GATE_V176"), ("vl_gate_v175", "vl_gate_v176"),
    ("runs/vision_v175h", "runs/vision_v176h"),
    ("_v175c1157", "_v176c1163"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T176, "v176h", "V176H", HO176))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v176h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v176"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v176" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v176h_c1165"'); seen_run = True; continue
    out2.append(ln)
(S / "c1165_vision_v176_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1154_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C1154", "C1166"), ("c1154", "c1166"),
    ("product_u2c_c1154", "product_u2c_c1166"),
    ("after V174", "after V176"), ("after V175", "after V176"),
]:
    out = out.replace(a, b)
(S / "c1166_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c1161_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1161", "C1167"), ("c1161", "c1167"),
    ("capture_regression_c1161", "capture_regression_c1167"),
    ("after C1157-C1160", "after C1163-C1166"),
    ("V4-V175+heldout", "V4-V176+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V175", DOC / "C1158_VISION_V175_SMOKE.json"),'
if needle in out and "VISION_V176_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V176", DOC / "C1164_VISION_V176_SMOKE.json"),\n    ("V176_heldout", DOC / "C1165_VISION_V176_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1167_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1162_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1162", "C1168"), ("c1162", "c1168"),
    ("C1158", "C1164"), ("C1159", "C1165"), ("C1161", "C1167"),
    ("C1157", "C1163"),
    ("V175", "V176"), ("v175", "v176"),
    ("V174", "V175"), ("v174", "v175"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C1160_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1160_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C1154_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1166_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace('"source": "C1154"', '"source": "C1166"')
out = out.replace('"source": "C1160"', '"source": "C1160"')
out = out.replace(
    "stage_ready = bool(v176_claim and v176h_claim and v176 >= GATE and v176h >= GATE and capture_pass and disjoint and conf_pass)",
    "stage_ready = bool(v176_claim and v176h_claim and v176 >= GATE and v176h >= GATE and capture_pass and disjoint and u2c_pass)",
)
out = out.replace(
    'f"- C1166: confidence-gate pass={conf_pass} rate={conf_rate}"',
    'f"- C1166: product-U2C replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- C1160: confidence-gate pass={conf_pass} rate={conf_rate}"',
    'f"- C1166: product-U2C replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- product-U2C (prior C1154): replace={replace} pass={u2c_pass}"',
    'f"- confidence-gate (prior C1160): pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- product-U2C (prior C1166): replace={replace} pass={u2c_pass}"',
    'f"- confidence-gate (prior C1160): pass={conf_pass} rate={conf_rate}"',
)
(S / "c1168_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T176 if t[0].endswith("b")])
print("qty", TR176[1], HO176[1], "po", TR176[8], HO176[8], "sla", TR176[6], HO176[6], "fax", TR176[15], HO176[15])
print("done")
