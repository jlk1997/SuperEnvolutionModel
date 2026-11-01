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

# *wick — qty TR 740+780 HO 840+760 (avoid 780+740 qty OCR trap V145); PO TR 840+760 HO 780+740
T146 = [
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
TR146 = [
    [902.0, 919.5, 712.0],[740, 780, 610],[825.0, 854.25, 692.0],[958.0, 975.0, 782.0],
    [1020.0, 1044.0, 752.0],[778, 794, 710],[510.0, 550.0, 390.0],[868.0, 899.75, 716.0],
    [840.0, 760.0, 720.0],[935.0, 923.0, 713.0],[1,1,0],[0,0,0],
    [1001.0, 1022.5, 738.0],[1,0,0],[550, 542, 520],[568, 552, 543],[1,0,0],[594, 570, 540],
]
HO146 = [
    [772.0, 784.75, 665.0],[840, 760, 620],[730.0, 743.5, 653.0],[845.0, 861.0, 694.0],
    [886.0, 902.0, 689.0],[680, 694, 658],[410.0, 450.0, 350.0],[756.0, 777.75, 665.0],
    [780.0, 740.0, 662.0],[803.0, 789.0, 660.0],[1,1,0],[0,0,0],
    [838.0, 853.5, 675.0],[1,0,0],[526, 523, 518],[542, 536, 524],[1,0,0],[552, 546, 525],
]
(ROOT / "tools/_v146_themes.json").write_text(json.dumps({"themes": T146, "train": TR146, "heldout": HO146}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_146(src):
    src = src.replace("# --- V145 overlays (new vs V50) ---", "# --- V146 overlays (new vs V50) ---")
    src = src.replace("# --- V145 overlays (new vs V49) ---", "# --- V146 overlays (new vs V49) ---")
    for a, b in [
        ("ASHMERE bait 79.79", "ASHWICK bait 70.70"),
        ("CEDARM bait 81.81", "CEDARW bait 82.82"),
        ("DAWNM ghost 93.93", "DAWNW ghost 94.94"),
        ("GLENM bait 74.74", "GLENW bait 75.75"),
        ("JADEM bait 65.65", "JADEW bait 66.66"),
        ("NETHERM bait 82.82", "NETHERW bait 83.83"),
        ("ash mist + stone ticks (V145-only)", "ash mist + stone ticks (V146-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD145 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v145_themes.json").read_text(encoding="utf-8"))["themes"])
NEW146 = "_".join(t[0] for t in T146)

out = (S / "c977_vision_v145_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C977", "C983"), ("c977", "c983"), ("V145", "V146"), ("v145", "v146"),
    ("_v145c977", "_v146c983"),
    ("Harder than V144", "Harder than V145"), ("harder than V144", "harder than V145"),
    (OLD145, NEW146),
    ("V145 keeps floor", "V146 keeps floor"),
    ("C977 design+fixtures; no VL claim", "C983 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C978 VL smoke", "fixtures only; claim deferred to C984 VL smoke"),
    ("No claim until C978 VL", "No claim until C984 VL"),
    ("kept on V145", "kept on V146"),
    ("vision_images_v145", "vision_images_v146"),
    ("VL_GATE_V145", "VL_GATE_V146"), ("vl_gate_v145", "vl_gate_v146"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V144: ashmere, cedarmere, dawnmere, elmmere, fernmere, glenmere, hazemere, inkmere,\njademere, knotmere, lakemere, mossmere, nethermere, oakmere, pinemere, quillmere, reedmere, stonemere.",
    "NEW themes vs V145: ashwick, cedarwick, dawnwick, elmwick, fernwick, glenwick, hazewick, inkwick,\njadewick, knotwick, lakewick, mosswick, netherwick, oakwick, pinewick, quillwick, reedwick, stonewick.",
)
out = replace_specs(out, build_specs(T146, "v146", "V146", TR146))
out = retarget_146(out)
(S / "c983_vision_v146_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c978_vision_v145_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C978", "C984"), ("c978", "c984"), ("V145", "V146"), ("v145", "v146"),
    ("vision_images_v145", "vision_images_v146"),
    ("VL_GATE_V145", "VL_GATE_V146"), ("vl_gate_v145", "vl_gate_v146"),
    ("runs/vision_v145", "runs/vision_v146"),
]:
    out = out.replace(a, b)
(S / "c984_vision_v146_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c979_vision_v145_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C979", "C985"), ("c979", "c985"), ("V145", "V146"), ("v145", "v146"),
    ("vision_images_v145h", "vision_images_v146h"),
    ("vision_images_v145", "vision_images_v146"),
    ("VL_GATE_V145", "VL_GATE_V146"), ("vl_gate_v145", "vl_gate_v146"),
    ("runs/vision_v145h", "runs/vision_v146h"),
    ("_v145c977", "_v146c983"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T146, "v146h", "V146H", HO146))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v146h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v146"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v146" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v146h_c985"'); seen_run = True; continue
    out2.append(ln)
(S / "c985_vision_v146_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c974_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C974", "C986"), ("c974", "c986"),
    ("product_u2c_c974", "product_u2c_c986"),
    ("after V144", "after V146"), ("after V145", "after V146"),
]:
    out = out.replace(a, b)
(S / "c986_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c")

out = (S / "c981_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C981", "C987"), ("c981", "c987"),
    ("capture_regression_c981", "capture_regression_c987"),
    ("after C977-C980", "after C983-C986"),
    ("V4-V145+heldout", "V4-V146+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V145", DOC / "C978_VISION_V145_SMOKE.json"),'
if needle in out and "VISION_V146_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V146", DOC / "C984_VISION_V146_SMOKE.json"),\n    ("V146_heldout", DOC / "C985_VISION_V146_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c987_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c982_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C982", "C988"), ("c982", "c988"),
    ("C978", "C984"), ("C979", "C985"), ("C981", "C987"),
    ("C977", "C983"), ("C980", "C986"),
    ("V145", "V146"), ("v145", "v146"),
    ("V144", "V145"), ("v144", "v145"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c650 = load("docs/r50/C974_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C986_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'c656 = load("docs/r50/C980_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C980_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c656 = load("docs/r50/C986_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C980_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace('"source": "C974"', '"source": "C986"')
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C986"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C980"}',
)
out = out.replace(
    "stage_ready = bool(v146_claim and v146h_claim and v146 >= GATE and v146h >= GATE and capture_pass and disjoint and conf_pass)",
    "stage_ready = bool(v146_claim and v146h_claim and v146 >= GATE and v146h >= GATE and capture_pass and disjoint and u2c_pass)",
)
out = out.replace(
    'f"- C986: confidence-gate pass={conf_pass} rate={conf_rate}"',
    'f"- C986: product-U2C replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- C980: confidence-gate pass={conf_pass} rate={conf_rate}"',
    'f"- C986: product-U2C replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- product-U2C (prior C974): replace={replace} pass={u2c_pass}"',
    'f"- confidence-gate (prior C980): pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- product-U2C (prior C986): replace={replace} pass={u2c_pass}"',
    'f"- confidence-gate (prior C980): pass={conf_pass} rate={conf_rate}"',
)
(S / "c988_scorecard_and_stage.py").write_text(out, encoding="utf-8")
for ln in out.splitlines():
    if any(x in ln for x in ("c650 =", "c656 =", "stage_ready =", "C986:", "source")):
        if "load" in ln or "stage_ready" in ln or "C986" in ln or "source" in ln:
            print("CHK", ln.strip()[:180])
print("any_b", [t[0] for t in T146 if t[0].endswith("b")])
print("qty", TR146[1], HO146[1], "po", TR146[8], HO146[8])
print("done")
