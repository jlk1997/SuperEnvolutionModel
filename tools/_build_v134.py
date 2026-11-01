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

# *vale — avoid prior; qty TR 740+760 HO 620+640; PO TR 790+740=1530 HO 680+590=1270 (round; lesson V133 755->756); SLA 390+430
T134 = [
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
TR134 = [
    [782.0, 799.5, 592.0],[740, 760, 580],[705.0, 734.25, 572.0],[838.0, 855.0, 662.0],
    [900.0, 924.0, 632.0],[658, 674, 590],[390.0, 430.0, 270.0],[748.0, 779.75, 596.0],
    [790.0, 740.0, 600.0],[815.0, 803.0, 593.0],[1,1,0],[0,0,0],  # po 790+740=1530
    [881.0, 902.5, 618.0],[1,0,0],[430, 422, 400],[448, 432, 423],[1,0,0],[474, 450, 420],
]
HO134 = [
    [652.0, 664.75, 545.0],[620, 640, 540],[610.0, 623.5, 533.0],[725.0, 741.0, 574.0],
    [766.0, 782.0, 569.0],[560, 574, 538],[290.0, 330.0, 230.0],[636.0, 657.75, 545.0],
    [680.0, 590.0, 542.0],[683.0, 669.0, 540.0],[1,1,0],[0,0,0],  # po 680+590=1270; qty 620+640=1260
    [718.0, 733.5, 555.0],[1,0,0],[406, 403, 398],[422, 416, 404],[1,0,0],[432, 426, 405],
]
(ROOT / "tools/_v134_themes.json").write_text(json.dumps({"themes": T134, "train": TR134, "heldout": HO134}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_134(src):
    src = src.replace("# --- V133 overlays (new vs V50) ---", "# --- V134 overlays (new vs V50) ---")
    src = src.replace("# --- V133 overlays (new vs V49) ---", "# --- V134 overlays (new vs V49) ---")
    for a, b in [
        ("ASHHAVEN bait 77.77", "ASHVALE bait 78.78"),
        ("CEDARH bait 97.97", "CEDARV bait 98.98"),
        ("DAWNH ghost 91.91", "DAWNV ghost 92.92"),
        ("GLENH bait 72.72", "GLENV bait 73.73"),
        ("JADEH bait 63.63", "JADEV bait 64.64"),
        ("NETHERH bait 98.98", "NETHERV bait 99.99"),
        ("ash mist + stone ticks (V133-only)", "ash mist + stone ticks (V134-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD133 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v133_themes.json").read_text(encoding="utf-8"))["themes"])
NEW134 = "_".join(t[0] for t in T134)

out = (S / "c905_vision_v133_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C905", "C911"), ("c905", "c911"), ("V133", "V134"), ("v133", "v134"),
    ("_v133c905", "_v134c911"),
    ("Harder than V132", "Harder than V133"), ("harder than V132", "harder than V133"),
    (OLD133, NEW134),
    ("V133 keeps floor", "V134 keeps floor"),
    ("C905 design+fixtures; no VL claim", "C911 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C906 VL smoke", "fixtures only; claim deferred to C912 VL smoke"),
    ("No claim until C906 VL", "No claim until C912 VL"),
    ("kept on V133", "kept on V134"),
    ("vision_images_v133", "vision_images_v134"),
    ("VL_GATE_V133", "VL_GATE_V134"), ("vl_gate_v133", "vl_gate_v134"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V132: ashhaven, cedarhaven, dawnhaven, elmhaven, fernhaven, glenhaven, hazehaven, inkhaven,\njadehaven, knothaven, lakehaven, mosshaven, netherhaven, oakhaven, pinehaven, quillhaven, reedhaven, stonehaven.",
    "NEW themes vs V133: ashvale, cedarvale, dawnvale, elmvale, fernvale, glenvale, hazevale, inkvale,\njadevale, knotvale, lakevale, mossvale, nethervale, oakvale, pinevale, quillvale, reedvale, stonevale.",
)
out = replace_specs(out, build_specs(T134, "v134", "V134", TR134))
out = retarget_134(out)
(S / "c911_vision_v134_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c906_vision_v133_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C906", "C912"), ("c906", "c912"), ("V133", "V134"), ("v133", "v134"),
    ("Uses C905 fixtures", "Uses C911 fixtures"),
    ("vision_images_v133", "vision_images_v134"),
    ("vl_gate_v133", "vl_gate_v134"), ("VL_GATE_V133", "VL_GATE_V134"),
]:
    out = out.replace(a, b)
(S / "c912_vision_v134_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c907_vision_v133_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C907", "C913"), ("c907", "c913"), ("C905", "C911"),
    ("V133", "V134"), ("v133", "v134"),
    ("_v133hc907", "_v134hc913"), ("_v133c905", "_v134c911"),
    ("vl_gate_v133", "vl_gate_v134"), ("VL_GATE_V133", "VL_GATE_V134"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T134, "v134h", "V134H", HO134))
out = retarget_134(out)
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v134h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v134"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v134" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v134h_c913"'); seen_run = True; continue
    out2.append(ln)
(S / "c913_vision_v134_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c902_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C902", "C914"), ("c902", "c914"),
    ("product_u2c_c902", "product_u2c_c914"),
    ("after V132", "after V134"), ("after V133", "after V134"),
]:
    out = out.replace(a, b)
(S / "c914_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c909_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C909", "C915"), ("c909", "c915"),
    ("capture_regression_c909", "capture_regression_c915"),
    ("after C905-C908", "after C911-C914"),
    ("V4-V133+heldout", "V4-V134+heldout"),
]:
    out = out.replace(a, b)
if "VISION_V134_SMOKE" not in out:
    out = out.replace(
        "SMOKE_POINTERS = [",
        'SMOKE_POINTERS = [\n    ("V134", DOC / "C912_VISION_V134_SMOKE.json"),\n    ("V134_heldout", DOC / "C913_VISION_V134_HELDOUT_SMOKE.json"),\n    ("V133", DOC / "C906_VISION_V133_SMOKE.json"),\n    ("V133_heldout", DOC / "C907_VISION_V133_HELDOUT_SMOKE.json"),',
        1,
    )
(S / "c915_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c910_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C910", "C916"), ("c910", "c916"),
    ("C906", "C912"), ("C907", "C913"), ("C909", "C915"),
    ("C905", "C911"),
    ("V133", "V134"), ("v133", "v134"),
    ("V132", "V133"), ("v132", "v133"),
    ("v133_jpeg_q", "v134_jpeg_q"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C908_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C908_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C902_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C914_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C902"}',
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C914"}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C908"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C908"}',
)
out = out.replace(
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C902"}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C914"}',
)
out = out.replace(
    "confidence-gate rate={conf_rate} pass={conf_pass}",
    "product-U2C replace={replace} pass={u2c_pass}",
)
out = out.replace(
    "stage_ready = bool(v134_claim and v134h_claim and v134 >= GATE and v134h >= GATE and capture_pass and disjoint and conf_pass)",
    "stage_ready = bool(v134_claim and v134h_claim and v134 >= GATE and v134h >= GATE and capture_pass and disjoint and u2c_pass)",
)
out = out.replace(
    'f"- C908: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C914: product-U2C replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- C908: confidence-gate rate={conf_rate} pass={conf_pass}"',
    'f"- C914: product-U2C replace={replace} pass={u2c_pass}"',
)
(S / "c916_scorecard_and_stage.py").write_text(out, encoding="utf-8")
for ln in out.splitlines():
    if any(x in ln for x in ("c656 =", "c650 =", '"confidence_gate"', '"product_u2c"', "stage_ready =", "product-U2C", "C914:", "C908:")):
        if "load" in ln or "source" in ln or "stage_ready" in ln or "product-U2C" in ln or "confidence" in ln:
            print("CHK", ln.strip()[:160])
print("scorecard OK"); print("done")
