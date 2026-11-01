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

# *mere — qty TR 780+740 HO 840+760; PO TR 780+740=1520 HO 840+760=1600; SLA 500+540
T145 = [
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
TR145 = [
    [892.0, 909.5, 702.0],[780, 740, 690],[815.0, 844.25, 682.0],[948.0, 965.0, 772.0],
    [1010.0, 1034.0, 742.0],[768, 784, 700],[500.0, 540.0, 380.0],[858.0, 889.75, 706.0],
    [780.0, 740.0, 710.0],[925.0, 913.0, 703.0],[1,1,0],[0,0,0],
    [991.0, 1012.5, 728.0],[1,0,0],[540, 532, 510],[558, 542, 533],[1,0,0],[584, 560, 530],
]
HO145 = [
    [762.0, 774.75, 655.0],[840, 760, 650],[720.0, 733.5, 643.0],[835.0, 851.0, 684.0],
    [876.0, 892.0, 679.0],[670, 684, 648],[400.0, 440.0, 340.0],[746.0, 767.75, 655.0],
    [840.0, 760.0, 652.0],[793.0, 779.0, 650.0],[1,1,0],[0,0,0],
    [828.0, 843.5, 665.0],[1,0,0],[516, 513, 508],[532, 526, 514],[1,0,0],[542, 536, 515],
]
(ROOT / "tools/_v145_themes.json").write_text(json.dumps({"themes": T145, "train": TR145, "heldout": HO145}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_145(src):
    src = src.replace("# --- V144 overlays (new vs V50) ---", "# --- V145 overlays (new vs V50) ---")
    src = src.replace("# --- V144 overlays (new vs V49) ---", "# --- V145 overlays (new vs V49) ---")
    for a, b in [
        ("ASHHOLM bait 78.78", "ASHMERE bait 79.79"),
        ("CEDARH bait 80.80", "CEDARM bait 81.81"),
        ("DAWNH ghost 92.92", "DAWNM ghost 93.93"),
        ("GLENH bait 73.73", "GLENM bait 74.74"),
        ("JADEH bait 64.64", "JADEM bait 65.65"),
        ("NETHERH bait 81.81", "NETHERM bait 82.82"),
        ("ash mist + stone ticks (V144-only)", "ash mist + stone ticks (V145-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD144 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v144_themes.json").read_text(encoding="utf-8"))["themes"])
NEW145 = "_".join(t[0] for t in T145)

out = (S / "c971_vision_v144_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C971", "C977"), ("c971", "c977"), ("V144", "V145"), ("v144", "v145"),
    ("_v144c971", "_v145c977"),
    ("Harder than V143", "Harder than V144"), ("harder than V143", "harder than V144"),
    (OLD144, NEW145),
    ("V144 keeps floor", "V145 keeps floor"),
    ("C971 design+fixtures; no VL claim", "C977 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C972 VL smoke", "fixtures only; claim deferred to C978 VL smoke"),
    ("No claim until C972 VL", "No claim until C978 VL"),
    ("kept on V144", "kept on V145"),
    ("vision_images_v144", "vision_images_v145"),
    ("VL_GATE_V144", "VL_GATE_V145"), ("vl_gate_v144", "vl_gate_v145"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V143: ashnolm, cedarholm, dawnholm, elmholm, fernholm, glenholm, hazeholm, inkholm,\njadeholm, knotholm, lakeholm, mossholm, netherholm, oakholm, pineholm, quillholm, reedholm, stoneholm.",
    "NEW themes vs V144: ashmere, cedarmere, dawnmere, elmmere, fernmere, glenmere, hazemere, inkmere,\njademere, knotmere, lakemere, mossmere, nethermere, oakmere, pinemere, quillmere, reedmere, stonemere.",
)
out = replace_specs(out, build_specs(T145, "v145", "V145", TR145))
out = retarget_145(out)
(S / "c977_vision_v145_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c972_vision_v144_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C972", "C978"), ("c972", "c978"), ("V144", "V145"), ("v144", "v145"),
    ("vision_images_v144", "vision_images_v145"),
    ("VL_GATE_V144", "VL_GATE_V145"), ("vl_gate_v144", "vl_gate_v145"),
    ("runs/vision_v144", "runs/vision_v145"),
]:
    out = out.replace(a, b)
(S / "c978_vision_v145_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c973_vision_v144_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C973", "C979"), ("c973", "c979"), ("V144", "V145"), ("v144", "v145"),
    ("vision_images_v144h", "vision_images_v145h"),
    ("vision_images_v144", "vision_images_v145"),
    ("VL_GATE_V144", "VL_GATE_V145"), ("vl_gate_v144", "vl_gate_v145"),
    ("runs/vision_v144h", "runs/vision_v145h"),
    ("_v144c971", "_v145c977"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T145, "v145h", "V145H", HO145))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v145h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v145"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v145" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v145h_c979"'); seen_run = True; continue
    out2.append(ln)
(S / "c979_vision_v145_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c968_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C968", "C980"), ("c968", "c980"),
    ("conf_gate_stretch_c968", "conf_gate_stretch_c980"),
    ("after V143", "after V145"), ("after V144", "after V145"),
    ("cg73_", "cg74_"),
]:
    out = out.replace(a, b)
(S / "c980_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence")

out = (S / "c975_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C975", "C981"), ("c975", "c981"),
    ("capture_regression_c975", "capture_regression_c981"),
    ("after C971-C974", "after C977-C980"),
    ("V4-V144+heldout", "V4-V145+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V144", DOC / "C972_VISION_V144_SMOKE.json"),'
if needle in out and "VISION_V145_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V145", DOC / "C978_VISION_V145_SMOKE.json"),\n    ("V145_heldout", DOC / "C979_VISION_V145_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c981_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c976_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C976", "C982"), ("c976", "c982"),
    ("C972", "C978"), ("C973", "C979"), ("C975", "C981"),
    ("C971", "C977"),
    ("V144", "V145"), ("v144", "v145"),
    ("V143", "V144"), ("v143", "v144"),
]:
    out = out.replace(a, b)
# conf knife this cycle
out = out.replace(
    'c650 = load("docs/r50/C974_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C974_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'c656 = load("docs/r50/C968_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C980_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace('"source": "C974"', '"source": "C974"')
out = out.replace('"source": "C968"', '"source": "C980"')
# C974 may have become C980 via broad replace — fix conf path if broken
out = out.replace(
    'c656 = load("docs/r50/C974_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C980_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    "stage_ready = bool(v145_claim and v145h_claim and v145 >= GATE and v145h >= GATE and capture_pass and disjoint and u2c_pass)",
    "stage_ready = bool(v145_claim and v145h_claim and v145 >= GATE and v145h >= GATE and capture_pass and disjoint and conf_pass)",
)
out = out.replace(
    'f"- C980: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C980: confidence-gate pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- C974: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C980: confidence-gate pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- confidence-gate (prior C968): pass={conf_pass} rate={conf_rate}"',
    'f"- product-U2C (prior C974): replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- confidence-gate (prior C980): pass={conf_pass} rate={conf_rate}"',
    'f"- product-U2C (prior C974): replace={replace} pass={u2c_pass}"',
)
(S / "c982_scorecard_and_stage.py").write_text(out, encoding="utf-8")
for ln in out.splitlines():
    if any(x in ln for x in ("c650 =", "c656 =", "stage_ready =", "C980:", "source")):
        if "load" in ln or "stage_ready" in ln or "C980" in ln or "source" in ln:
            print("CHK", ln.strip()[:180])
print("any_b", [t[0] for t in T145 if t[0].endswith("b")])
print("qty", TR145[1], HO145[1], "po", TR145[8], HO145[8])
print("done")
