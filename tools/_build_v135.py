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

# *holt — avoid *b/prior; qty TR 750+770 HO 630+650; PO TR 800+740=1540 HO 690+590=1280 (V133 lesson avoid *5->6); SLA 400+440
T135 = [
    ["ashholt","recv","paid_total","ASHHOLT GRAIN RECV","RECV","x"],
    ["cedarholt","wh","qty_sum","WH CEDARHOLT BIN","RECV","x"],
    ["dawnholt","refund","refund_done","DAWNHOLT PATCH REFUND","DONE","x"],
    ["elmholt","tax","tax_base_paid","ELMHOLT TAX SLIP","TAX","x"],
    ["fernholt","pay","payroll_active","FERNHOLT PAYROLL","PAY","x"],
    ["glenholt","ship","ship_ok","GLENHOLT SHIP DOCK","SHIP","x"],
    ["hazeholt","sla","sla_ok_hours","HAZEHOLT SLA CARD","SLA","x"],
    ["inkholt","exp","exp_sum","INKHOLT EXPENSE","EXP","x"],
    ["jadeholt","po","po_open","JADEHOLT PO SHEET","PO","x"],
    ["knotholt","order","order_paid","KNOTHOLT ORDER","ORD","x"],
    ["lakeholt","dup","dup_mark","LAKEHOLT DUP MARK","DUP","x"],
    ["mossholt","zero","zero_check","MOSSHOLT AIR ZERO","ZERO","x"],
    ["netherholt","ledger","ledger_net","NETHERHOLT LEDGER","LED","x"],
    ["oakholt","ui","ui_ok","OAKHOLT UI SCAN","UI","x"],
    ["pineholt","stack","stack_count","PINEHOLT STACK","STK","x"],
    ["quillholt","fax","fax_pages","QUILLHOLT FAX","FAX","x"],
    ["reedholt","glare","glare_ok","REEDHOLT GLARE","GLR","x"],
    ["stoneholt","tab","tab_index","STONEHOLT TAB INDEX","TAB","x"],
]
TR135 = [
    [792.0, 809.5, 602.0],[740, 780, 590],[715.0, 744.25, 582.0],[848.0, 865.0, 672.0],
    [910.0, 934.0, 642.0],[668, 684, 600],[400.0, 440.0, 280.0],[758.0, 789.75, 606.0],
    [800.0, 740.0, 610.0],[825.0, 813.0, 603.0],[1,1,0],[0,0,0],  # po 800+740=1540
    [891.0, 912.5, 628.0],[1,0,0],[440, 432, 410],[458, 442, 433],[1,0,0],[484, 460, 430],
]
HO135 = [
    [662.0, 674.75, 555.0],[630, 650, 550],[620.0, 633.5, 543.0],[735.0, 751.0, 584.0],
    [776.0, 792.0, 579.0],[570, 584, 548],[300.0, 340.0, 240.0],[646.0, 667.75, 555.0],
    [690.0, 590.0, 552.0],[693.0, 679.0, 550.0],[1,1,0],[0,0,0],  # po 690+590=1280; qty 630+650=1280
    [728.0, 743.5, 565.0],[1,0,0],[416, 413, 408],[432, 426, 414],[1,0,0],[442, 436, 415],
]
(ROOT / "tools/_v135_themes.json").write_text(json.dumps({"themes": T135, "train": TR135, "heldout": HO135}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_135(src):
    src = src.replace("# --- V134 overlays (new vs V50) ---", "# --- V135 overlays (new vs V50) ---")
    src = src.replace("# --- V134 overlays (new vs V49) ---", "# --- V135 overlays (new vs V49) ---")
    for a, b in [
        ("ASHVALE bait 78.78", "ASHHOLT bait 79.79"),
        ("CEDARV bait 98.98", "CEDARH bait 89.89"),
        ("DAWNV ghost 92.92", "DAWNH ghost 93.93"),
        ("GLENV bait 73.73", "GLENH bait 74.74"),
        ("JADEV bait 64.64", "JADEH bait 65.65"),
        ("NETHERV bait 99.99", "NETHERH bait 81.81"),
        ("ash mist + stone ticks (V134-only)", "ash mist + stone ticks (V135-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD134 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v134_themes.json").read_text(encoding="utf-8"))["themes"])
NEW135 = "_".join(t[0] for t in T135)

out = (S / "c911_vision_v134_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C911", "C917"), ("c911", "c917"), ("V134", "V135"), ("v134", "v135"),
    ("_v134c911", "_v135c917"),
    ("Harder than V133", "Harder than V134"), ("harder than V133", "harder than V134"),
    (OLD134, NEW135),
    ("V134 keeps floor", "V135 keeps floor"),
    ("C911 design+fixtures; no VL claim", "C917 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C912 VL smoke", "fixtures only; claim deferred to C918 VL smoke"),
    ("No claim until C912 VL", "No claim until C918 VL"),
    ("kept on V134", "kept on V135"),
    ("vision_images_v134", "vision_images_v135"),
    ("VL_GATE_V134", "VL_GATE_V135"), ("vl_gate_v134", "vl_gate_v135"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V133: ashvale, cedarvale, dawnvale, elmvale, fernvale, glenvale, hazevale, inkvale,\njadevale, knotvale, lakevale, mossvale, nethervale, oakvale, pinevale, quillvale, reedvale, stonevale.",
    "NEW themes vs V134: ashholt, cedarholt, dawnholt, elmholt, fernholt, glenholt, hazeholt, inkholt,\njadeholt, knotholt, lakeholt, mossholt, netherholt, oakholt, pineholt, quillholt, reedholt, stoneholt.",
)
out = replace_specs(out, build_specs(T135, "v135", "V135", TR135))
out = retarget_135(out)
(S / "c917_vision_v135_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c912_vision_v134_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C912", "C918"), ("c912", "c918"), ("V134", "V135"), ("v134", "v135"),
    ("Uses C911 fixtures", "Uses C917 fixtures"),
    ("vision_images_v134", "vision_images_v135"),
    ("vl_gate_v134", "vl_gate_v135"), ("VL_GATE_V134", "VL_GATE_V135"),
]:
    out = out.replace(a, b)
(S / "c918_vision_v135_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c913_vision_v134_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C913", "C919"), ("c913", "c919"), ("C911", "C917"),
    ("V134", "V135"), ("v134", "v135"),
    ("_v134hc913", "_v135hc919"), ("_v134c911", "_v135c917"),
    ("vl_gate_v134", "vl_gate_v135"), ("VL_GATE_V134", "VL_GATE_V135"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T135, "v135h", "V135H", HO135))
out = retarget_135(out)
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v135h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v135"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v135" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v135h_c919"'); seen_run = True; continue
    out2.append(ln)
(S / "c919_vision_v135_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c908_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C908", "C920"), ("c908", "c920"),
    ("conf_gate_stretch_c908", "conf_gate_stretch_c920"),
    ("after V133", "after V135"), ("after V134", "after V135"),
    ("cg68_", "cg69_"),
]:
    out = out.replace(a, b)
(S / "c920_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence")

out = (S / "c915_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C915", "C921"), ("c915", "c921"),
    ("capture_regression_c915", "capture_regression_c921"),
    ("after C911-C914", "after C917-C920"),
    ("V4-V134+heldout", "V4-V135+heldout"),
]:
    out = out.replace(a, b)
if "VISION_V135_SMOKE" not in out:
    out = out.replace(
        "SMOKE_POINTERS = [",
        'SMOKE_POINTERS = [\n    ("V135", DOC / "C918_VISION_V135_SMOKE.json"),\n    ("V135_heldout", DOC / "C919_VISION_V135_HELDOUT_SMOKE.json"),\n    ("V134", DOC / "C912_VISION_V134_SMOKE.json"),\n    ("V134_heldout", DOC / "C913_VISION_V134_HELDOUT_SMOKE.json"),',
        1,
    )
(S / "c921_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c916_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C916", "C922"), ("c916", "c922"),
    ("C912", "C918"), ("C913", "C919"), ("C915", "C921"),
    ("C911", "C917"),
    ("V134", "V135"), ("v134", "v135"),
    ("V133", "V134"), ("v133", "v134"),
    ("v134_jpeg_q", "v135_jpeg_q"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C908_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C920_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C914_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C914_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C914"}',
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C914"}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C908"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C920"}',
)
out = out.replace(
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C914"}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C914"}',
)
out = out.replace(
    "product-U2C replace={replace} pass={u2c_pass}",
    "confidence-gate rate={conf_rate} pass={conf_pass}",
)
out = out.replace(
    "stage_ready = bool(v135_claim and v135h_claim and v135 >= GATE and v135h >= GATE and capture_pass and disjoint and u2c_pass)",
    "stage_ready = bool(v135_claim and v135h_claim and v135 >= GATE and v135h >= GATE and capture_pass and disjoint and conf_pass)",
)
out = out.replace(
    'f"- C914: confidence-gate rate={conf_rate} pass={conf_pass}"',
    'f"- C920: confidence-gate rate={conf_rate} pass={conf_pass}"',
)
out = out.replace(
    'f"- C914: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C920: confidence-gate rate={conf_rate} pass={conf_pass}"',
)
(S / "c922_scorecard_and_stage.py").write_text(out, encoding="utf-8")
for ln in out.splitlines():
    if any(x in ln for x in ("c656 =", "c650 =", '"confidence_gate"', '"product_u2c"', "stage_ready =", "confidence-gate", "C920:", "C914:")):
        if "load" in ln or "source" in ln or "stage_ready" in ln or "confidence-gate" in ln or "product" in ln:
            print("CHK", ln.strip()[:160])
print("scorecard OK"); print("done")
