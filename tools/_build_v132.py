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

# *croft — avoid prior suffixes; qty TR 720+740 HO 600+620; PO HO 666+584=1250; SLA 370+410
T132 = [
    ["ashcroft","recv","paid_total","ASHCROFT GRAIN RECV","RECV","x"],
    ["cedarcroft","wh","qty_sum","WH CEDARCROFT BIN","RECV","x"],
    ["dawncroft","refund","refund_done","DAWNCROFT PATCH REFUND","DONE","x"],
    ["elmcroft","tax","tax_base_paid","ELMCROFT TAX SLIP","TAX","x"],
    ["ferncroft","pay","payroll_active","FERNCROFT PAYROLL","PAY","x"],
    ["glencroft","ship","ship_ok","GLENCROFT SHIP DOCK","SHIP","x"],
    ["hazecroft","sla","sla_ok_hours","HAZECROFT SLA CARD","SLA","x"],
    ["inkcroft","exp","exp_sum","INKCROFT EXPENSE","EXP","x"],
    ["jadecroft","po","po_open","JADECROFT PO SHEET","PO","x"],
    ["knotcroft","order","order_paid","KNOTCROFT ORDER","ORD","x"],
    ["lakecroft","dup","dup_mark","LAKECROFT DUP MARK","DUP","x"],
    ["mosscroft","zero","zero_check","MOSSCROFT AIR ZERO","ZERO","x"],
    ["nethercroft","ledger","ledger_net","NETHERCROFT LEDGER","LED","x"],
    ["oakcroft","ui","ui_ok","OAKCROFT UI SCAN","UI","x"],
    ["pinecroft","stack","stack_count","PINECROFT STACK","STK","x"],
    ["quillcroft","fax","fax_pages","QUILLCROFT FAX","FAX","x"],
    ["reedcroft","glare","glare_ok","REEDCROFT GLARE","GLR","x"],
    ["stonecroft","tab","tab_index","STONECROFT TAB INDEX","TAB","x"],
]
TR132 = [
    [762.0, 779.5, 572.0],[720, 740, 560],[685.0, 714.25, 552.0],[818.0, 835.0, 642.0],
    [880.0, 904.0, 612.0],[638, 654, 570],[370.0, 410.0, 250.0],[728.0, 759.75, 576.0],
    [762.0, 745.0, 585.0],[795.0, 783.0, 573.0],[1,1,0],[0,0,0],
    [861.0, 882.5, 598.0],[1,0,0],[410, 402, 380],[428, 412, 403],[1,0,0],[454, 430, 400],
]
HO132 = [
    [632.0, 644.75, 525.0],[600, 620, 520],[590.0, 603.5, 513.0],[705.0, 721.0, 554.0],
    [746.0, 762.0, 549.0],[540, 554, 518],[270.0, 310.0, 210.0],[616.0, 637.75, 525.0],
    [666.0, 584.0, 522.0],[663.0, 649.0, 520.0],[1,1,0],[0,0,0],  # po 666+584=1250; qty 600+620=1220
    [698.0, 713.5, 535.0],[1,0,0],[386, 383, 378],[402, 396, 384],[1,0,0],[412, 406, 385],
]
(ROOT / "tools/_v132_themes.json").write_text(json.dumps({"themes": T132, "train": TR132, "heldout": HO132}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_132(src):
    src = src.replace("# --- V131 overlays (new vs V50) ---", "# --- V132 overlays (new vs V50) ---")
    src = src.replace("# --- V131 overlays (new vs V49) ---", "# --- V132 overlays (new vs V49) ---")
    for a, b in [
        ("ASHMERE bait 75.75", "ASHCROFT bait 76.76"),
        ("CEDARM bait 95.95", "CEDARC bait 96.96"),
        ("DAWNM ghost 98.98", "DAWNC ghost 99.99"),
        ("GLENM bait 70.70", "GLENC bait 71.71"),
        ("JADEM bait 61.61", "JADEC bait 62.62"),
        ("NETHERM bait 96.96", "NETHERC bait 97.97"),
        ("ash mist + stone ticks (V131-only)", "ash mist + stone ticks (V132-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD131 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v131_themes.json").read_text(encoding="utf-8"))["themes"])
NEW132 = "_".join(t[0] for t in T132)

out = (S / "c893_vision_v131_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C893", "C899"), ("c893", "c899"), ("V131", "V132"), ("v131", "v132"),
    ("_v131c893", "_v132c899"),
    ("Harder than V130", "Harder than V131"), ("harder than V130", "harder than V131"),
    (OLD131, NEW132),
    ("V131 keeps floor", "V132 keeps floor"),
    ("C893 design+fixtures; no VL claim", "C899 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C894 VL smoke", "fixtures only; claim deferred to C900 VL smoke"),
    ("No claim until C894 VL", "No claim until C900 VL"),
    ("kept on V131", "kept on V132"),
    ("vision_images_v131", "vision_images_v132"),
    ("VL_GATE_V131", "VL_GATE_V132"), ("vl_gate_v131", "vl_gate_v132"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V130: ashmere, cedarmere, dawnmere, elmmere, fernmere, glenmere, hazemere, inkmere,\njademere, knotmere, lakemere, mossmere, nethermere, oakmere, pinemere, quillmere, reedmere, stonemere.",
    "NEW themes vs V131: ashcroft, cedarcroft, dawncroft, elmcroft, ferncroft, glencroft, hazecroft, inkcroft,\njadecroft, knotcroft, lakecroft, mosscroft, nethercroft, oakcroft, pinecroft, quillcroft, reedcroft, stonecroft.",
)
out = replace_specs(out, build_specs(T132, "v132", "V132", TR132))
out = retarget_132(out)
(S / "c899_vision_v132_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c894_vision_v131_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C894", "C900"), ("c894", "c900"), ("V131", "V132"), ("v131", "v132"),
    ("Uses C893 fixtures", "Uses C899 fixtures"),
    ("vision_images_v131", "vision_images_v132"),
    ("vl_gate_v131", "vl_gate_v132"), ("VL_GATE_V131", "VL_GATE_V132"),
]:
    out = out.replace(a, b)
(S / "c900_vision_v132_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c895_vision_v131_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C895", "C901"), ("c895", "c901"), ("C893", "C899"),
    ("V131", "V132"), ("v131", "v132"),
    ("_v131hc895", "_v132hc901"), ("_v131c893", "_v132c899"),
    ("vl_gate_v131", "vl_gate_v132"), ("VL_GATE_V131", "VL_GATE_V132"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T132, "v132h", "V132H", HO132))
out = retarget_132(out)
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v132h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v132"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v132" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v132h_c901"'); seen_run = True; continue
    out2.append(ln)
(S / "c901_vision_v132_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c890_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C890", "C902"), ("c890", "c902"),
    ("product_u2c_c890", "product_u2c_c902"),
    ("after V130", "after V132"), ("after V131", "after V132"),
]:
    out = out.replace(a, b)
(S / "c902_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c897_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C897", "C903"), ("c897", "c903"),
    ("capture_regression_c897", "capture_regression_c903"),
    ("after C893-C896", "after C899-C902"),
    ("V4-V131+heldout", "V4-V132+heldout"),
]:
    out = out.replace(a, b)
if "VISION_V132_SMOKE" not in out:
    out = out.replace(
        "SMOKE_POINTERS = [",
        'SMOKE_POINTERS = [\n    ("V132", DOC / "C900_VISION_V132_SMOKE.json"),\n    ("V132_heldout", DOC / "C901_VISION_V132_HELDOUT_SMOKE.json"),\n    ("V131", DOC / "C894_VISION_V131_SMOKE.json"),\n    ("V131_heldout", DOC / "C895_VISION_V131_HELDOUT_SMOKE.json"),',
        1,
    )
(S / "c903_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c898_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C898", "C904"), ("c898", "c904"),
    ("C894", "C900"), ("C895", "C901"), ("C897", "C903"),
    ("C893", "C899"),
    ("V131", "V132"), ("v131", "v132"),
    ("V130", "V131"), ("v130", "v131"),
    ("v131_jpeg_q", "v132_jpeg_q"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C896_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C896_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C890_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C902_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C890"}',
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C902"}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C896"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C896"}',
)
out = out.replace(
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C890"}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C902"}',
)
out = out.replace(
    "confidence-gate rate={conf_rate} pass={conf_pass}",
    "product-U2C replace={replace} pass={u2c_pass}",
)
out = out.replace(
    "stage_ready = bool(v132_claim and v132h_claim and v132 >= GATE and v132h >= GATE and capture_pass and disjoint and conf_pass)",
    "stage_ready = bool(v132_claim and v132h_claim and v132 >= GATE and v132h >= GATE and capture_pass and disjoint and u2c_pass)",
)
out = out.replace(
    'f"- C896: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C902: product-U2C replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- C896: confidence-gate rate={conf_rate} pass={conf_pass}"',
    'f"- C902: product-U2C replace={replace} pass={u2c_pass}"',
)
(S / "c904_scorecard_and_stage.py").write_text(out, encoding="utf-8")
for ln in out.splitlines():
    if any(x in ln for x in ("c656 =", "c650 =", '"confidence_gate"', '"product_u2c"', "stage_ready =", "product-U2C", "C902:", "C896:")):
        if "load" in ln or "source" in ln or "stage_ready" in ln or "product-U2C" in ln or "confidence" in ln:
            print("CHK", ln.strip()[:160])
print("scorecard OK"); print("done")
