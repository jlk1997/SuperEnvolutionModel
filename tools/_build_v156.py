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

# *mere ; qty TR 740+780 HO 840+760; PO TR 780+740 HO 840+760; SLA TR 480+520 HO 360+400
T156 = [
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
TR156 = [
    [997.0, 1014.5, 807.0],[740, 780, 660],[920.0, 949.25, 787.0],[1053.0, 1070.0, 877.0],
    [1115.0, 1139.0, 847.0],[873, 889, 805],[480.0, 520.0, 350.0],[963.0, 994.75, 811.0],
    [780.0, 740.0, 720.0],[1030.0, 1018.0, 808.0],[1,1,0],[0,0,0],
    [1096.0, 1117.5, 833.0],[1,0,0],[645, 637, 615],[663, 647, 638],[1,0,0],[689, 665, 635],
]
HO156 = [
    [867.0, 879.75, 760.0],[840, 760, 720],[825.0, 838.5, 748.0],[940.0, 956.0, 789.0],
    [981.0, 997.0, 784.0],[775, 789, 753],[360.0, 400.0, 330.0],[851.0, 872.75, 760.0],
    [840.0, 760.0, 730.0],[898.0, 884.0, 755.0],[1,1,0],[0,0,0],
    [933.0, 948.5, 770.0],[1,0,0],[621, 618, 613],[637, 631, 619],[1,0,0],[647, 641, 620],
]
(ROOT / "tools/_v156_themes.json").write_text(json.dumps({"themes": T156, "train": TR156, "heldout": HO156}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_156(src):
    src = src.replace("# --- V155 overlays (new vs V50) ---", "# --- V156 overlays (new vs V50) ---")
    src = src.replace("# --- V155 overlays (new vs V49) ---", "# --- V156 overlays (new vs V49) ---")
    for a, b in [
        ("ASHHOLM bait 79.79", "ASHMERE bait 70.70"),
        ("CEDARH bait 81.81", "CEDARM bait 82.82"),
        ("DAWNH ghost 93.93", "DAWNM ghost 94.94"),
        ("GLENH bait 74.74", "GLENM bait 75.75"),
        ("JADEH bait 65.65", "JADEM bait 66.66"),
        ("NETHERH bait 82.82", "NETHERM bait 83.83"),
        ("ash mist + stone ticks (V155-only)", "ash mist + stone ticks (V156-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD155 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v155_themes.json").read_text(encoding="utf-8"))["themes"])
NEW156 = "_".join(t[0] for t in T156)

out = (S / "c1037_vision_v155_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1037", "C1043"), ("c1037", "c1043"), ("V155", "V156"), ("v155", "v156"),
    ("_v155c1037", "_v156c1043"),
    ("Harder than V154", "Harder than V155"), ("harder than V154", "harder than V155"),
    (OLD155, NEW156),
    ("V155 keeps floor", "V156 keeps floor"),
    ("C1037 design+fixtures; no VL claim", "C1043 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1038 VL smoke", "fixtures only; claim deferred to C1044 VL smoke"),
    ("No claim until C1038 VL", "No claim until C1044 VL"),
    ("kept on V155", "kept on V156"),
    ("vision_images_v155", "vision_images_v156"),
    ("VL_GATE_V155", "VL_GATE_V156"), ("vl_gate_v155", "vl_gate_v156"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V154: ashhholm, cedarholm, dawnholm, elmholm, fernholm, glenholm, hazeholm, inkholm,\njadeholm, knotholm, lakeholm, mossholm, netherholm, oakholm, pineholm, quillholm, reedholm, stoneholm.".replace("ashhholm","ashholm"),
    "NEW themes vs V155: ashmere, cedarmere, dawnmere, elmmere, fernmere, glenmere, hazemere, inkmere,\njademere, knotmere, lakemere, mossmere, nethermere, oakmere, pinemere, quillmere, reedmere, stonemere.",
)
# also try without typo variant
out = out.replace(
    "NEW themes vs V154: ashhholm, cedarholm, dawnholm, elmholm, fernholm, glenholm, hazeholm, inkholm,\njadeholm, knotholm, lakeholm, mossholm, netherholm, oakholm, pineholm, quillholm, reedholm, stoneholm.",
    "NEW themes vs V155: ashmere, cedarmere, dawnmere, elmmere, fernmere, glenmere, hazemere, inkmere,\njademere, knotmere, lakemere, mossmere, nethermere, oakmere, pinemere, quillmere, reedmere, stonemere.",
)
out = out.replace(
    "NEW themes vs V154: ashhholm, cedarholm, dawnholm, elmholm, fernholm, glenholm, hazeholm, inkholm,\njadeholm, knotholm, lakeholm, mossholm, netherholm, oakholm, pineholm, quillholm, reedholm, stoneholm.",
    "NEW themes vs V155: ashmere, cedarmere, dawnmere, elmmere, fernmere, glenmere, hazemere, inkmere,\njademere, knotmere, lakemere, mossmere, nethermere, oakmere, pinemere, quillmere, reedmere, stonemere.",
)
if "ashholm" in out and "NEW themes vs V154" in out:
    out = out.replace(
        "NEW themes vs V154: ashhholm, cedarholm, dawnholm, elmholm, fernholm, glenholm, hazeholm, inkholm,\njadeholm, knotholm, lakeholm, mossholm, netherholm, oakholm, pineholm, quillholm, reedholm, stoneholm.".replace("ashhholm","ashholm"),
        "NEW themes vs V155: ashmere, cedarmere, dawnmere, elmmere, fernmere, glenmere, hazemere, inkmere,\njademere, knotmere, lakemere, mossmere, nethermere, oakmere, pinemere, quillmere, reedmere, stonemere.",
    )
# robust themes line replace
import re as _re
out = _re.sub(
    r"NEW themes vs V154:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V155: ashmere, cedarmere, dawnmere, elmmere, fernmere, glenmere, hazemere, inkmere,\njademere, knotmere, lakemere, mossmere, nethermere, oakmere, pinemere, quillmere, reedmere, stonemere.",
    out,
    count=1,
    flags=_re.S,
)
out = replace_specs(out, build_specs(T156, "v156", "V156", TR156))
out = retarget_156(out)
(S / "c1043_vision_v156_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1038_vision_v155_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1038", "C1044"), ("c1038", "c1044"), ("V155", "V156"), ("v155", "v156"),
    ("vision_images_v155", "vision_images_v156"),
    ("VL_GATE_V155", "VL_GATE_V156"), ("vl_gate_v155", "vl_gate_v156"),
    ("runs/vision_v155", "runs/vision_v156"),
]:
    out = out.replace(a, b)
(S / "c1044_vision_v156_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1039_vision_v155_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1039", "C1045"), ("c1039", "c1045"), ("V155", "V156"), ("v155", "v156"),
    ("vision_images_v155h", "vision_images_v156h"),
    ("vision_images_v155", "vision_images_v156"),
    ("VL_GATE_V155", "VL_GATE_V156"), ("vl_gate_v155", "vl_gate_v156"),
    ("runs/vision_v155h", "runs/vision_v156h"),
    ("_v155c1037", "_v156c1043"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T156, "v156h", "V156H", HO156))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v156h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v156"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v156" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v156h_c1045"'); seen_run = True; continue
    out2.append(ln)
(S / "c1045_vision_v156_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1034_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C1034", "C1046"), ("c1034", "c1046"),
    ("product_u2c_c1034", "product_u2c_c1046"),
    ("after V154", "after V156"), ("after V155", "after V156"),
]:
    out = out.replace(a, b)
(S / "c1046_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c")

out = (S / "c1041_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1041", "C1047"), ("c1041", "c1047"),
    ("capture_regression_c1041", "capture_regression_c1047"),
    ("after C1037-C1040", "after C1043-C1046"),
    ("V4-V155+heldout", "V4-V156+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V155", DOC / "C1038_VISION_V155_SMOKE.json"),'
if needle in out and "VISION_V156_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V156", DOC / "C1044_VISION_V156_SMOKE.json"),\n    ("V156_heldout", DOC / "C1045_VISION_V156_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1047_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1042_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1042", "C1048"), ("c1042", "c1048"),
    ("C1038", "C1044"), ("C1039", "C1045"), ("C1041", "C1047"),
    ("C1037", "C1043"),
    ("V155", "V156"), ("v155", "v156"),
    ("V154", "V155"), ("v154", "v155"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c650 = load("docs/r50/C1034_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1046_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'c656 = load("docs/r50/C1040_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1040_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace('"source": "C1034"', '"source": "C1046"')
out = out.replace('"source": "C1040"', '"source": "C1040"')
out = out.replace(
    "stage_ready = bool(v156_claim and v156h_claim and v156 >= GATE and v156h >= GATE and capture_pass and disjoint and conf_pass)",
    "stage_ready = bool(v156_claim and v156h_claim and v156 >= GATE and v156h >= GATE and capture_pass and disjoint and u2c_pass)",
)
out = out.replace(
    'f"- C1046: confidence-gate pass={conf_pass} rate={conf_rate}"',
    'f"- C1046: product-U2C replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- C1040: confidence-gate pass={conf_pass} rate={conf_rate}"',
    'f"- C1046: product-U2C replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- product-U2C (prior C1034): replace={replace} pass={u2c_pass}"',
    'f"- confidence-gate (prior C1040): pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- product-U2C (prior C1046): replace={replace} pass={u2c_pass}"',
    'f"- confidence-gate (prior C1040): pass={conf_pass} rate={conf_rate}"',
)
(S / "c1048_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T156 if t[0].endswith("b")])
print("qty", TR156[1], HO156[1], "po", TR156[8], HO156[8], "sla", TR156[6], HO156[6])
print("done")
