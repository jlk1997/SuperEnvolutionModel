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

# *croft — avoid *b; OCR-friendly 1090-style PO
T121 = [
    ["ambercroft","recv","paid_total","AMBERCROFT GRAIN RECV","RECV","x"],
    ["briarcroft","wh","qty_sum","WH BRIARCROFT BIN","RECV","x"],
    ["cedar croft","refund","refund_done","CEDARCROFT PATCH REFUND","DONE","x"],
    ["dunecroft","tax","tax_base_paid","DUNECROFT TAX SLIP","TAX","x"],
    ["embercroft","pay","payroll_active","EMBERCROFT PAYROLL","PAY","x"],
    ["flintcroft","ship","ship_ok","FLINTCROFT SHIP DOCK","SHIP","x"],
    ["gorse croft","sla","sla_ok_hours","GORSECROFT SLA CARD","SLA","x"],
    ["heathcroft","exp","exp_sum","HEATHCROFT EXPENSE","EXP","x"],
    ["inkcroft","po","po_open","INKCROFT PO SHEET","PO","x"],
    ["jade croft","order","order_paid","JADECROFT ORDER","ORD","x"],
    ["kelpcroft","dup","dup_mark","KELPCROFT DUP MARK","DUP","x"],
    ["loamcroft","zero","zero_check","LOAMCROFT AIR ZERO","ZERO","x"],
    ["mistcroft","ledger","ledger_net","MISTCROFT LEDGER","LED","x"],
    ["nethercroft","ui","ui_ok","NETHERCROFT UI SCAN","UI","x"],
    ["oakcroft","stack","stack_count","OAKCROFT STACK","STK","x"],
    ["pinecroft","fax","fax_pages","PINECROFT FAX","FAX","x"],
    ["quillcroft","glare","glare_ok","QUILLCROFT GLARE","GLR","x"],
    ["reedcroft","tab","tab_index","REEDCROFT TAB INDEX","TAB","x"],
]
# fix accidental spaces in names
T121[2] = ["cedarcroft","refund","refund_done","CEDARCROFT PATCH REFUND","DONE","x"]
T121[6] = ["gorsecroft","sla","sla_ok_hours","GORSECROFT SLA CARD","SLA","x"]
T121[9] = ["jadecroft","order","order_paid","JADECROFT ORDER","ORD","x"]
TR121 = [
    [676.0, 693.5, 486.0],[603, 644, 458],[599.0, 628.25, 466.0],[732.0, 749.0, 556.0],
    [794.0, 818.0, 526.0],[552, 568, 484],[340.0, 380.0, 220.0],[642.0, 673.75, 490.0],
    [676.0, 659.0, 499.0],[709.0, 697.0, 487.0],[1,1,0],[0,0,0],
    [775.0, 796.5, 512.0],[1,0,0],[324, 316, 294],[342, 326, 317],[1,0,0],[368, 344, 314],
]
HO121 = [
    [546.0, 558.75, 439.0],[501, 541, 421],[504.0, 517.5, 427.0],[619.0, 635.0, 468.0],
    [660.0, 676.0, 463.0],[454, 468, 432],[240.0, 280.0, 180.0],[530.0, 551.75, 439.0],
    [589.0, 515.0, 436.0],[577.0, 563.0, 434.0],[1,1,0],[0,0,0],  # po 589+515=1104
    [612.0, 627.5, 449.0],[1,0,0],[300, 297, 292],[316, 310, 298],[1,0,0],[326, 320, 299],
]
(ROOT / "tools/_v121_themes.json").write_text(json.dumps({"themes": T121, "train": TR121, "heldout": HO121}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_121(src):
    src = src.replace("# --- V120 overlays (new vs V50) ---", "# --- V121 overlays (new vs V50) ---")
    src = src.replace("# --- V120 overlays (new vs V49) ---", "# --- V121 overlays (new vs V49) ---")
    for a, b in [
        ("ARGENTGLEN bait 64.64", "AMBERCROFT bait 65.65"),
        ("BROOK bait 84.84", "BRIAR bait 85.85"),
        ("CINDER ghost 96.96", "CEDAR ghost 97.97"),
        ("FOG bait 59.59", "FLINT bait 60.60"),
        ("IVORYG bait 50.50", "INK bait 51.51"),
        ("MOSS bait 94.94", "MIST bait 95.95"),
        ("argent mist + ridge ticks (V120-only)", "amber mist + reed ticks (V121-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD120 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v120_themes.json").read_text(encoding="utf-8"))["themes"])
NEW121 = "_".join(t[0] for t in T121)

out = (S / "c827_vision_v120_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C827", "C833"), ("c827", "c833"), ("V120", "V121"), ("v120", "v121"),
    ("_v120c827", "_v121c833"),
    ("Harder than V119", "Harder than V120"), ("harder than V119", "harder than V120"),
    (OLD120, NEW121),
    ("V120 keeps floor", "V121 keeps floor"),
    ("C827 design+fixtures; no VL claim", "C833 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C828 VL smoke", "fixtures only; claim deferred to C834 VL smoke"),
    ("No claim until C828 VL", "No claim until C834 VL"),
    ("kept on V120", "kept on V121"),
    ("vision_images_v120", "vision_images_v121"),
    ("VL_GATE_V120", "VL_GATE_V121"), ("vl_gate_v120", "vl_gate_v121"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V119: argentglen, brookglen, cinderglen, dewglen, elderglen, fogglen, garnetglen, hazelglen,\nivoryglen, juniperglen, knotglen, loamglen, mossglen, nectarglen, opalglen, pearlglen, quartzglen, ridgeglen.",
    "NEW themes vs V120: ambercroft, briarcroft, cedarcroft, dunecroft, embercroft, flintcroft, gorsecroft, heathcroft,\ninkcroft, jadecroft, kelpcroft, loamcroft, mistcroft, nethercroft, oakcroft, pinecroft, quillcroft, reedcroft.",
)
out = replace_specs(out, build_specs(T121, "v121", "V121", TR121))
out = retarget_121(out)
(S / "c833_vision_v121_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c828_vision_v120_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C828", "C834"), ("c828", "c834"), ("V120", "V121"), ("v120", "v121"),
    ("Uses C827 fixtures", "Uses C833 fixtures"),
    ("vision_images_v120", "vision_images_v121"),
    ("vl_gate_v120", "vl_gate_v121"), ("VL_GATE_V120", "VL_GATE_V121"),
]:
    out = out.replace(a, b)
(S / "c834_vision_v121_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c829_vision_v120_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C829", "C835"), ("c829", "c835"), ("C827", "C833"),
    ("V120", "V121"), ("v120", "v121"),
    ("_v120hc829", "_v121hc835"), ("_v120c827", "_v121c833"),
    ("vl_gate_v120", "vl_gate_v121"), ("VL_GATE_V120", "VL_GATE_V121"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T121, "v121h", "V121H", HO121))
out = retarget_121(out)
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v121h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v121"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v121" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v121h_c835"'); seen_run = True; continue
    out2.append(ln)
(S / "c835_vision_v121_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c824_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C824", "C836"), ("c824", "c836"),
    ("conf_gate_stretch_c824", "conf_gate_stretch_c836"),
    ("after V119", "after V121"), ("after V120", "after V121"),
    ("cg61_", "cg62_"),
]:
    out = out.replace(a, b)
(S / "c836_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence")

out = (S / "c831_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C831", "C837"), ("c831", "c837"),
    ("capture_regression_c831", "capture_regression_c837"),
    ("after C827-C830", "after C833-C836"),
    ("V4-V120+heldout", "V4-V121+heldout"),
]:
    out = out.replace(a, b)
if "VISION_V121_SMOKE" not in out:
    out = out.replace(
        "SMOKE_POINTERS = [",
        'SMOKE_POINTERS = [\n    ("V121", DOC / "C834_VISION_V121_SMOKE.json"),\n    ("V121_heldout", DOC / "C835_VISION_V121_HELDOUT_SMOKE.json"),\n    ("V120", DOC / "C828_VISION_V120_SMOKE.json"),\n    ("V120_heldout", DOC / "C829_VISION_V120_HELDOUT_SMOKE.json"),',
        1,
    )
(S / "c837_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c832_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C832", "C838"), ("c832", "c838"),
    ("C828", "C834"), ("C829", "C835"), ("C831", "C837"),
    ("C827", "C833"),
    ("V120", "V121"), ("v120", "v121"),
    ("V119", "V120"), ("v119", "v120"),
    ("v120_jpeg_q", "v121_jpeg_q"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C824_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C836_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C830_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C830_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C830"}',
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C830"}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C824"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C836"}',
)
out = out.replace(
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C830"}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C830"}',
)
out = out.replace(
    "product-U2C replace={replace} pass={u2c_pass}",
    "confidence-gate rate={conf_rate} pass={conf_pass}",
)
out = out.replace(
    "stage_ready = bool(v121_claim and v121h_claim and v121 >= GATE and v121h >= GATE and capture_pass and disjoint and u2c_pass)",
    "stage_ready = bool(v121_claim and v121h_claim and v121 >= GATE and v121h >= GATE and capture_pass and disjoint and conf_pass)",
)
out = out.replace(
    'f"- C830: confidence-gate rate={conf_rate} pass={conf_pass}"',
    'f"- C836: confidence-gate rate={conf_rate} pass={conf_pass}"',
)
out = out.replace(
    'f"- C830: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C836: confidence-gate rate={conf_rate} pass={conf_pass}"',
)
(S / "c838_scorecard_and_stage.py").write_text(out, encoding="utf-8")
for ln in out.splitlines():
    if any(x in ln for x in ("c656 =", "c650 =", '"confidence_gate"', '"product_u2c"', "stage_ready =", "confidence-gate", "C836:", "C830:")):
        if "load" in ln or "source" in ln or "stage_ready" in ln or "confidence-gate" in ln or "product" in ln:
            print("CHK", ln.strip()[:150])
print("scorecard OK"); print("done")
