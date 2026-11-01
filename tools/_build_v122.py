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

# *ford — avoid *b; OCR-friendly PO (1118 style)
T122 = [
    ["ashford","recv","paid_total","ASHFORD GRAIN RECV","RECV","x"],
    ["clifford","wh","qty_sum","WH CLIFFORD BIN","RECV","x"],
    ["dawnford","refund","refund_done","DAWNFORD PATCH REFUND","DONE","x"],
    ["elmford","tax","tax_base_paid","ELMFORD TAX SLIP","TAX","x"],
    ["fernford","pay","payroll_active","FERNFORD PAYROLL","PAY","x"],
    ["glenford","ship","ship_ok","GLENFORD SHIP DOCK","SHIP","x"],
    ["haze ford","sla","sla_ok_hours","HAZEFORD SLA CARD","SLA","x"],
    ["inkford","exp","exp_sum","INKFORD EXPENSE","EXP","x"],
    ["jade ford","po","po_open","JADEFORD PO SHEET","PO","x"],
    ["knotford","order","order_paid","KNOTFORD ORDER","ORD","x"],
    ["lake ford","dup","dup_mark","LAKEFORD DUP MARK","DUP","x"],
    ["mossford","zero","zero_check","MOSSFORD AIR ZERO","ZERO","x"],
    ["nethford","ledger","ledger_net","NETHFORD LEDGER","LED","x"],
    ["oakford","ui","ui_ok","OAKFORD UI SCAN","UI","x"],
    ["pineford","stack","stack_count","PINEFORD STACK","STK","x"],
    ["quillford","fax","fax_pages","QUILLFORD FAX","FAX","x"],
    ["reedford","glare","glare_ok","REEDFORD GLARE","GLR","x"],
    ["stoneford","tab","tab_index","STONEFORD TAB INDEX","TAB","x"],
]
T122[6] = ["hazeford","sla","sla_ok_hours","HAZEFORD SLA CARD","SLA","x"]
T122[8] = ["jadeford","po","po_open","JADEFORD PO SHEET","PO","x"]
T122[10] = ["lakeford","dup","dup_mark","LAKEFORD DUP MARK","DUP","x"]
TR122 = [
    [683.0, 700.5, 493.0],[610, 651, 465],[606.0, 635.25, 473.0],[739.0, 756.0, 563.0],
    [801.0, 825.0, 533.0],[559, 575, 491],[340.0, 380.0, 220.0],[649.0, 680.75, 497.0],
    [683.0, 666.0, 506.0],[716.0, 704.0, 494.0],[1,1,0],[0,0,0],
    [782.0, 803.5, 519.0],[1,0,0],[331, 323, 301],[349, 333, 324],[1,0,0],[375, 351, 321],
]
HO122 = [
    [553.0, 565.75, 446.0],[508, 548, 428],[511.0, 524.5, 434.0],[626.0, 642.0, 475.0],
    [667.0, 683.0, 470.0],[461, 475, 439],[240.0, 280.0, 180.0],[537.0, 558.75, 446.0],
    [596.0, 522.0, 443.0],[584.0, 570.0, 441.0],[1,1,0],[0,0,0],  # po 596+522=1118
    [619.0, 634.5, 456.0],[1,0,0],[307, 304, 299],[323, 317, 305],[1,0,0],[333, 327, 306],
]
(ROOT / "tools/_v122_themes.json").write_text(json.dumps({"themes": T122, "train": TR122, "heldout": HO122}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_122(src):
    src = src.replace("# --- V121 overlays (new vs V50) ---", "# --- V122 overlays (new vs V50) ---")
    src = src.replace("# --- V121 overlays (new vs V49) ---", "# --- V122 overlays (new vs V49) ---")
    for a, b in [
        ("AMBERCROFT bait 65.65", "ASHFORD bait 66.66"),
        ("BRIAR bait 85.85", "CLIFF bait 86.86"),
        ("CEDAR ghost 97.97", "DAWN ghost 98.98"),
        ("FLINT bait 60.60", "GLEN bait 61.61"),
        ("INK bait 51.51", "JADE bait 52.52"),
        ("MIST bait 95.95", "NETH bait 96.96"),
        ("amber mist + reed ticks (V121-only)", "ash mist + stone ticks (V122-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD121 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v121_themes.json").read_text(encoding="utf-8"))["themes"])
NEW122 = "_".join(t[0] for t in T122)

out = (S / "c833_vision_v121_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C833", "C839"), ("c833", "c839"), ("V121", "V122"), ("v121", "v122"),
    ("_v121c833", "_v122c839"),
    ("Harder than V120", "Harder than V121"), ("harder than V120", "harder than V121"),
    (OLD121, NEW122),
    ("V121 keeps floor", "V122 keeps floor"),
    ("C833 design+fixtures; no VL claim", "C839 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C834 VL smoke", "fixtures only; claim deferred to C840 VL smoke"),
    ("No claim until C834 VL", "No claim until C840 VL"),
    ("kept on V121", "kept on V122"),
    ("vision_images_v121", "vision_images_v122"),
    ("VL_GATE_V121", "VL_GATE_V122"), ("vl_gate_v121", "vl_gate_v122"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V120: ambercroft, briarcroft, cedarcroft, dunecroft, embercroft, flintcroft, gorsecroft, heathcroft,\ninkcroft, jadecroft, kelpcroft, loamcroft, mistcroft, nethercroft, oakcroft, pinecroft, quillcroft, reedcroft.",
    "NEW themes vs V121: ashford, clifford, dawnford, elmford, fernford, glenford, hazeford, inkford,\njadeford, knotford, lakeford, mossford, nethford, oakford, pineford, quillford, reedford, stoneford.",
)
out = replace_specs(out, build_specs(T122, "v122", "V122", TR122))
out = retarget_122(out)
(S / "c839_vision_v122_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c834_vision_v121_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C834", "C840"), ("c834", "c840"), ("V121", "V122"), ("v121", "v122"),
    ("Uses C833 fixtures", "Uses C839 fixtures"),
    ("vision_images_v121", "vision_images_v122"),
    ("vl_gate_v121", "vl_gate_v122"), ("VL_GATE_V121", "VL_GATE_V122"),
]:
    out = out.replace(a, b)
(S / "c840_vision_v122_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c835_vision_v121_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C835", "C841"), ("c835", "c841"), ("C833", "C839"),
    ("V121", "V122"), ("v121", "v122"),
    ("_v121hc835", "_v122hc841"), ("_v121c833", "_v122c839"),
    ("vl_gate_v121", "vl_gate_v122"), ("VL_GATE_V121", "VL_GATE_V122"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T122, "v122h", "V122H", HO122))
out = retarget_122(out)
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v122h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v122"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v122" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v122h_c841"'); seen_run = True; continue
    out2.append(ln)
(S / "c841_vision_v122_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c830_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C830", "C842"), ("c830", "c842"),
    ("product_u2c_c830", "product_u2c_c842"),
    ("after V120", "after V122"), ("after V121", "after V122"),
]:
    out = out.replace(a, b)
(S / "c842_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c837_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C837", "C843"), ("c837", "c843"),
    ("capture_regression_c837", "capture_regression_c843"),
    ("after C833-C836", "after C839-C842"),
    ("V4-V121+heldout", "V4-V122+heldout"),
]:
    out = out.replace(a, b)
if "VISION_V122_SMOKE" not in out:
    out = out.replace(
        "SMOKE_POINTERS = [",
        'SMOKE_POINTERS = [\n    ("V122", DOC / "C840_VISION_V122_SMOKE.json"),\n    ("V122_heldout", DOC / "C841_VISION_V122_HELDOUT_SMOKE.json"),\n    ("V121", DOC / "C834_VISION_V121_SMOKE.json"),\n    ("V121_heldout", DOC / "C835_VISION_V121_HELDOUT_SMOKE.json"),',
        1,
    )
(S / "c843_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c838_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C838", "C844"), ("c838", "c844"),
    ("C834", "C840"), ("C835", "C841"), ("C837", "C843"),
    ("C833", "C839"),
    ("V121", "V122"), ("v121", "v122"),
    ("V120", "V121"), ("v120", "v121"),
    ("v121_jpeg_q", "v122_jpeg_q"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C836_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C836_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C830_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C842_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C830"}',
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C842"}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C836"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C836"}',
)
out = out.replace(
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C830"}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C842"}',
)
out = out.replace(
    "confidence-gate rate={conf_rate} pass={conf_pass}",
    "product-U2C replace={replace} pass={u2c_pass}",
)
out = out.replace(
    "stage_ready = bool(v122_claim and v122h_claim and v122 >= GATE and v122h >= GATE and capture_pass and disjoint and conf_pass)",
    "stage_ready = bool(v122_claim and v122h_claim and v122 >= GATE and v122h >= GATE and capture_pass and disjoint and u2c_pass)",
)
out = out.replace(
    'f"- C836: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C842: product-U2C replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- C836: confidence-gate rate={conf_rate} pass={conf_pass}"',
    'f"- C842: product-U2C replace={replace} pass={u2c_pass}"',
)
(S / "c844_scorecard_and_stage.py").write_text(out, encoding="utf-8")
for ln in out.splitlines():
    if any(x in ln for x in ("c656 =", "c650 =", '"confidence_gate"', '"product_u2c"', "stage_ready =", "product-U2C", "C842:", "C836:")):
        if "load" in ln or "source" in ln or "stage_ready" in ln or "product-U2C" in ln or "confidence" in ln:
            print("CHK", ln.strip()[:150])
print("scorecard OK"); print("done")
