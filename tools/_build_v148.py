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

# *hurst — qty TR 740+780 HO 840+760; PO TR 840+760 HO 780+740 (avoid 780+740 TR qty)
T148 = [
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
TR148 = [
    [922.0, 939.5, 732.0],[740, 780, 610],[845.0, 874.25, 712.0],[978.0, 995.0, 802.0],
    [1040.0, 1064.0, 772.0],[798, 814, 730],[530.0, 570.0, 410.0],[888.0, 919.75, 736.0],
    [840.0, 760.0, 740.0],[955.0, 943.0, 733.0],[1,1,0],[0,0,0],
    [1021.0, 1042.5, 758.0],[1,0,0],[570, 562, 540],[588, 572, 563],[1,0,0],[614, 590, 560],
]
HO148 = [
    [792.0, 804.75, 685.0],[840, 760, 640],[750.0, 763.5, 673.0],[865.0, 881.0, 714.0],
    [906.0, 922.0, 709.0],[700, 714, 678],[430.0, 470.0, 370.0],[776.0, 797.75, 685.0],
    [780.0, 740.0, 682.0],[823.0, 809.0, 680.0],[1,1,0],[0,0,0],
    [858.0, 873.5, 695.0],[1,0,0],[546, 543, 538],[562, 556, 544],[1,0,0],[572, 566, 545],
]
(ROOT / "tools/_v148_themes.json").write_text(json.dumps({"themes": T148, "train": TR148, "heldout": HO148}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_148(src):
    src = src.replace("# --- V147 overlays (new vs V50) ---", "# --- V148 overlays (new vs V50) ---")
    src = src.replace("# --- V147 overlays (new vs V49) ---", "# --- V148 overlays (new vs V49) ---")
    for a, b in [
        ("ASHCROFT bait 71.71", "ASHHURST bait 72.72"),
        ("CEDARC bait 83.83", "CEDARH bait 84.84"),
        ("DAWNC ghost 95.95", "DAWNH ghost 96.96"),
        ("GLENC bait 76.76", "GLENH bait 77.77"),
        ("JADEC bait 67.67", "JADEH bait 68.68"),
        ("NETHERC bait 84.84", "NETHERH bait 85.85"),
        ("ash mist + stone ticks (V147-only)", "ash mist + stone ticks (V148-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD147 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v147_themes.json").read_text(encoding="utf-8"))["themes"])
NEW148 = "_".join(t[0] for t in T148)

out = (S / "c989_vision_v147_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C989", "C995"), ("c989", "c995"), ("V147", "V148"), ("v147", "v148"),
    ("_v147c989", "_v148c995"),
    ("Harder than V146", "Harder than V147"), ("harder than V146", "harder than V147"),
    (OLD147, NEW148),
    ("V147 keeps floor", "V148 keeps floor"),
    ("C989 design+fixtures; no VL claim", "C995 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C990 VL smoke", "fixtures only; claim deferred to C996 VL smoke"),
    ("No claim until C990 VL", "No claim until C996 VL"),
    ("kept on V147", "kept on V148"),
    ("vision_images_v147", "vision_images_v148"),
    ("VL_GATE_V147", "VL_GATE_V148"), ("vl_gate_v147", "vl_gate_v148"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V146: ashcroft, cedarcroft, dawncroft, elmcroft, ferncroft, glencroft, hazecroft, inkcroft,\njadecroft, knotcroft, lakecroft, mosscroft, nethercroft, oakcroft, pinecroft, quillcroft, reedcroft, stonecraft.",
    "NEW themes vs V147: ashhurst, cedarhurst, dawnhurst, elmhurst, fernhurst, glenhurst, hazehurst, inkhurst,\njadehurst, knothurst, lakehurst, mosshurst, netherhurst, oakhurst, pinehurst, quillhurst, reedhurst, stonehurst.",
)
out = replace_specs(out, build_specs(T148, "v148", "V148", TR148))
out = retarget_148(out)
(S / "c995_vision_v148_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c990_vision_v147_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C990", "C996"), ("c990", "c996"), ("V147", "V148"), ("v147", "v148"),
    ("vision_images_v147", "vision_images_v148"),
    ("VL_GATE_V147", "VL_GATE_V148"), ("vl_gate_v147", "vl_gate_v148"),
    ("runs/vision_v147", "runs/vision_v148"),
]:
    out = out.replace(a, b)
(S / "c996_vision_v148_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c991_vision_v147_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C991", "C997"), ("c991", "c997"), ("V147", "V148"), ("v147", "v148"),
    ("vision_images_v147h", "vision_images_v148h"),
    ("vision_images_v147", "vision_images_v148"),
    ("VL_GATE_V147", "VL_GATE_V148"), ("vl_gate_v147", "vl_gate_v148"),
    ("runs/vision_v147h", "runs/vision_v148h"),
    ("_v147c989", "_v148c995"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T148, "v148h", "V148H", HO148))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v148h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v148"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v148" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v148h_c997"'); seen_run = True; continue
    out2.append(ln)
(S / "c997_vision_v148_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c986_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C986", "C998"), ("c986", "c998"),
    ("product_u2c_c986", "product_u2c_c998"),
    ("after V146", "after V148"), ("after V147", "after V148"),
]:
    out = out.replace(a, b)
(S / "c998_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c")

out = (S / "c993_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C993", "C999"), ("c993", "c999"),
    ("capture_regression_c993", "capture_regression_c999"),
    ("after C989-C992", "after C995-C998"),
    ("V4-V147+heldout", "V4-V148+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V147", DOC / "C990_VISION_V147_SMOKE.json"),'
if needle in out and "VISION_V148_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V148", DOC / "C996_VISION_V148_SMOKE.json"),\n    ("V148_heldout", DOC / "C997_VISION_V148_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c999_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c994_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C994", "C1000"), ("c994", "c1000"),
    ("C990", "C996"), ("C991", "C997"), ("C993", "C999"),
    ("C989", "C995"), ("C992", "C998"),
    ("V147", "V148"), ("v147", "v148"),
    ("V146", "V147"), ("v146", "v147"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c650 = load("docs/r50/C986_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C998_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'c656 = load("docs/r50/C992_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C992_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c656 = load("docs/r50/C998_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C992_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace('"source": "C986"', '"source": "C998"')
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C998"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C992"}',
)
out = out.replace(
    "stage_ready = bool(v148_claim and v148h_claim and v148 >= GATE and v148h >= GATE and capture_pass and disjoint and conf_pass)",
    "stage_ready = bool(v148_claim and v148h_claim and v148 >= GATE and v148h >= GATE and capture_pass and disjoint and u2c_pass)",
)
out = out.replace(
    'f"- C998: confidence-gate pass={conf_pass} rate={conf_rate}"',
    'f"- C998: product-U2C replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- C992: confidence-gate pass={conf_pass} rate={conf_rate}"',
    'f"- C998: product-U2C replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- product-U2C (prior C986): replace={replace} pass={u2c_pass}"',
    'f"- confidence-gate (prior C992): pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- product-U2C (prior C998): replace={replace} pass={u2c_pass}"',
    'f"- confidence-gate (prior C992): pass={conf_pass} rate={conf_rate}"',
)
(S / "c1000_scorecard_and_stage.py").write_text(out, encoding="utf-8")
for ln in out.splitlines():
    if any(x in ln for x in ("c650 =", "c656 =", "stage_ready =", "C998:", "source", "STAGE_ANT")):
        if "load" in ln or "stage_ready" in ln or "C998" in ln or "source" in ln or "STAGE" in ln:
            print("CHK", ln.strip()[:180])
print("any_b", [t[0] for t in T148 if t[0].endswith("b")])
print("qty", TR148[1], HO148[1], "po", TR148[8], HO148[8])
print("done")
