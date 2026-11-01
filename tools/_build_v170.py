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

# *hurst ; qty TR 740+780 HO 840+760; PO TR 780+740 HO 840+760; SLA TR 480+520 HO 360+400
# OCR-safe: no hold 830/755; no tabA 770; fax drop !=755
T170 = [
    ["ashhurst","recv","paid_total","ASHHURST GRAIN RECV","RECV","x"],
    ["cedarhurst","wh","qty_sum","WH CEDARHURST BIN","RECV","x"],
    ["dawnhurst","refund","refund_done","DAWNHURST PATCH REFUND","DONE","x"],
    ["elmhurst","tax","tax_base_paid","ELMHURST TAX SLIP","TAX","x"],
    ["fernhurst","pay","payroll_active","FERNHURST PAYROLL","PAY","x"],
    ["glenhurst","ship","ship_ok","GLENHURST SHIP DOCK","SHIP","x"],
    ["hazehurst","sla","sla_ok_hours","HAZEHURST SLA CARD","SLA","x"],
    ["inkhurst","exp","exp_sum","INKHURST EXPENSE","EXP","x"],
    ["jadehurst","po","po_open","JADEHURST PO SHEET","PO","x"],
    ["knothurst","order","order_paid","KNOTHURST ORDER","ORD","x"],
    ["lakehurst","dup","dup_mark","LAKEHURST DUP MARK","DUP","x"],
    ["mosshurst","zero","zero_check","MOSSHURST AIR ZERO","ZERO","x"],
    ["netherhurst","ledger","ledger_net","NETHERHURST LEDGER","LED","x"],
    ["oakhurst","ui","ui_ok","OAKHURST UI SCAN","UI","x"],
    ["pinehurst","stack","stack_count","PINEHURST STACK","STK","x"],
    ["quillhurst","fax","fax_pages","QUILLHURST FAX","FAX","x"],
    ["reedhurst","glare","glare_ok","REEDHURST GLARE","GLR","x"],
    ["stonehurst","tab","tab_index","STONEHURST TAB INDEX","TAB","x"],
]
TR170 = [
    [1123.0, 1140.5, 933.0],[740, 780, 800],[1046.0, 1075.25, 913.0],[1179.0, 1196.0, 1003.0],
    [1241.0, 1265.0, 973.0],[999, 1015, 931],[480.0, 520.0, 490.0],[1089.0, 1120.75, 937.0],
    [780.0, 740.0, 740.0],[1156.0, 1144.0, 934.0],[1,1,0],[0,0,0],
    [1222.0, 1243.5, 959.0],[1,0,0],[771, 763, 741],[789, 773, 748],[1,0,0],[815, 791, 761],
]
HO170 = [
    [993.0, 1005.75, 886.0],[840, 760, 820],[951.0, 964.5, 874.0],[1066.0, 1082.0, 915.0],
    [1107.0, 1123.0, 910.0],[901, 915, 879],[360.0, 400.0, 470.0],[977.0, 998.75, 886.0],
    [840.0, 760.0, 720.0],[1024.0, 1010.0, 881.0],[1,1,0],[0,0,0],
    [1059.0, 1074.5, 896.0],[1,0,0],[747, 744, 739],[763, 757, 745],[1,0,0],[773, 767, 746],
]
# sanitize: no 755/830/770 in any abc
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for row in TR170 + HO170:
    for v in row:
        if isinstance(v, (int, float)) and int(v) in BAN:
            raise SystemExit(f"banned value {v} in ABC")

(ROOT / "tools/_v170_themes.json").write_text(json.dumps({"themes": T170, "train": TR170, "heldout": HO170}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_170(src):
    src = src.replace("# --- V169 overlays (new vs V50) ---", "# --- V170 overlays (new vs V50) ---")
    src = src.replace("# --- V169 overlays (new vs V49) ---", "# --- V170 overlays (new vs V49) ---")
    for a, b in [
        ("ASHCROFT bait 83.83", "ASHHURST bait 84.84"),
        ("CEDARC bait 85.85", "CEDARH bait 86.86"),
        ("DAWNC ghost 97.97", "DAWNH ghost 98.98"),
        ("GLENC bait 78.78", "GLENH bait 79.79"),
        ("JADEC bait 69.69", "JADEH bait 70.70"),
        ("NETHERC bait 86.86", "NETHERH bait 87.87"),
        ("ash mist + stone ticks (V169-only)", "ash mist + stone ticks (V170-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD169 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v169_themes.json").read_text(encoding="utf-8"))["themes"])
NEW170 = "_".join(t[0] for t in T170)

out = (S / "c1121_vision_v169_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1121", "C1127"), ("c1121", "c1127"), ("V169", "V170"), ("v169", "v170"),
    ("_v169c1121", "_v170c1127"),
    ("Harder than V168", "Harder than V169"), ("harder than V168", "harder than V169"),
    (OLD169, NEW170),
    ("V169 keeps floor", "V170 keeps floor"),
    ("C1121 design+fixtures; no VL claim", "C1127 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1122 VL smoke", "fixtures only; claim deferred to C1128 VL smoke"),
    ("No claim until C1122 VL", "No claim until C1128 VL"),
    ("kept on V169", "kept on V170"),
    ("vision_images_v169", "vision_images_v170"),
    ("VL_GATE_V169", "VL_GATE_V170"), ("vl_gate_v169", "vl_gate_v170"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V168:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V169: ashhurst, cedarhurst, dawnhurst, elmhurst, fernhurst, glenhurst, hazehurst, inkhurst,\njadehurst, knothurst, lakehurst, mosshurst, netherhurst, oakhurst, pinehurst, quillhurst, reedhurst, stonehurst.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T170, "v170", "V170", TR170))
out = retarget_170(out)
(S / "c1127_vision_v170_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1122_vision_v169_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1122", "C1128"), ("c1122", "c1128"), ("V169", "V170"), ("v169", "v170"),
    ("vision_images_v169", "vision_images_v170"),
    ("VL_GATE_V169", "VL_GATE_V170"), ("vl_gate_v169", "vl_gate_v170"),
    ("runs/vision_v169", "runs/vision_v170"),
]:
    out = out.replace(a, b)
(S / "c1128_vision_v170_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1123_vision_v169_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1123", "C1129"), ("c1123", "c1129"), ("V169", "V170"), ("v169", "v170"),
    ("vision_images_v169h", "vision_images_v170h"),
    ("vision_images_v169", "vision_images_v170"),
    ("VL_GATE_V169", "VL_GATE_V170"), ("vl_gate_v169", "vl_gate_v170"),
    ("runs/vision_v169h", "runs/vision_v170h"),
    ("_v169c1121", "_v170c1127"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T170, "v170h", "V170H", HO170))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v170h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v170"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v170" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v170h_c1129"'); seen_run = True; continue
    out2.append(ln)
(S / "c1129_vision_v170_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1118_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C1118", "C1130"), ("c1118", "c1130"),
    ("product_u2c_c1118", "product_u2c_c1130"),
    ("after V168", "after V170"), ("after V169", "after V170"),
]:
    out = out.replace(a, b)
(S / "c1130_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c1125_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1125", "C1131"), ("c1125", "c1131"),
    ("capture_regression_c1125", "capture_regression_c1131"),
    ("after C1121-C1124", "after C1127-C1130"),
    ("V4-V169+heldout", "V4-V170+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V169", DOC / "C1122_VISION_V169_SMOKE.json"),'
if needle in out and "VISION_V170_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V170", DOC / "C1128_VISION_V170_SMOKE.json"),\n    ("V170_heldout", DOC / "C1129_VISION_V170_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1131_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1126_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1126", "C1132"), ("c1126", "c1132"),
    ("C1122", "C1128"), ("C1123", "C1129"), ("C1125", "C1131"),
    ("C1121", "C1127"),
    ("V169", "V170"), ("v169", "v170"),
    ("V168", "V169"), ("v168", "v169"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C1124_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1124_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C1118_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1130_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace('"source": "C1118"', '"source": "C1130"')
out = out.replace('"source": "C1124"', '"source": "C1124"')
out = out.replace(
    "stage_ready = bool(v170_claim and v170h_claim and v170 >= GATE and v170h >= GATE and capture_pass and disjoint and conf_pass)",
    "stage_ready = bool(v170_claim and v170h_claim and v170 >= GATE and v170h >= GATE and capture_pass and disjoint and u2c_pass)",
)
out = out.replace(
    'f"- C1130: confidence-gate pass={conf_pass} rate={conf_rate}"',
    'f"- C1130: product-U2C replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- C1124: confidence-gate pass={conf_pass} rate={conf_rate}"',
    'f"- C1130: product-U2C replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- product-U2C (prior C1118): replace={replace} pass={u2c_pass}"',
    'f"- confidence-gate (prior C1124): pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- product-U2C (prior C1130): replace={replace} pass={u2c_pass}"',
    'f"- confidence-gate (prior C1124): pass={conf_pass} rate={conf_rate}"',
)
(S / "c1132_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T170 if t[0].endswith("b")])
print("qty", TR170[1], HO170[1], "po", TR170[8], HO170[8], "sla", TR170[6], HO170[6], "fax", TR170[15], HO170[15])
print("done")
