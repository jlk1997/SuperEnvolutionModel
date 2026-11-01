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

# *cove — avoid *b; OCR-friendly qty 650+670; PO 617+543=1160
T125 = [
    ["ashcove","recv","paid_total","ASHCOVE GRAIN RECV","RECV","x"],
    ["briarcove","wh","qty_sum","WH BRIARCOVE BIN","RECV","x"],
    ["cedarcove","refund","refund_done","CEDARCOVE PATCH REFUND","DONE","x"],
    ["dawncove","tax","tax_base_paid","DAWNCOVE TAX SLIP","TAX","x"],
    ["embercove","pay","payroll_active","EMBERCOVE PAYROLL","PAY","x"],
    ["ferncove","ship","ship_ok","FERNCOVE SHIP DOCK","SHIP","x"],
    ["glencove","sla","sla_ok_hours","GLENCOVE SLA CARD","SLA","x"],
    ["hazecove","exp","exp_sum","HAZECOVE EXPENSE","EXP","x"],
    ["inkcove","po","po_open","INKCOVE PO SHEET","PO","x"],
    ["jadecove","order","order_paid","JADECOVE ORDER","ORD","x"],
    ["kelpcove","dup","dup_mark","KELPCOVE DUP MARK","DUP","x"],
    ["loamcove","zero","zero_check","LOAMCOVE AIR ZERO","ZERO","x"],
    ["mistcove","ledger","ledger_net","MISTCOVE LEDGER","LED","x"],
    ["nethercove","ui","ui_ok","NETHERCOVE UI SCAN","UI","x"],
    ["oakcove","stack","stack_count","OAKCOVE STACK","STK","x"],
    ["pinecove","fax","fax_pages","PINECOVE FAX","FAX","x"],
    ["quillcove","glare","glare_ok","QUILLCOVE GLARE","GLR","x"],
    ["reedcove","tab","tab_index","REEDCOVE TAB INDEX","TAB","x"],
]
TR125 = [
    [704.0, 721.5, 514.0],[650, 670, 490],[627.0, 656.25, 494.0],[760.0, 777.0, 584.0],
    [822.0, 846.0, 554.0],[580, 596, 512],[340.0, 380.0, 220.0],[670.0, 701.75, 518.0],
    [704.0, 687.0, 527.0],[737.0, 725.0, 515.0],[1,1,0],[0,0,0],
    [803.0, 824.5, 540.0],[1,0,0],[352, 344, 322],[370, 354, 345],[1,0,0],[396, 372, 342],
]
HO125 = [
    [574.0, 586.75, 467.0],[530, 550, 450],[532.0, 545.5, 455.0],[647.0, 663.0, 496.0],
    [688.0, 704.0, 491.0],[482, 496, 460],[240.0, 280.0, 180.0],[558.0, 579.75, 467.0],
    [617.0, 543.0, 464.0],[605.0, 591.0, 462.0],[1,1,0],[0,0,0],  # po 617+543=1160; qty 530+550=1080
    [640.0, 655.5, 477.0],[1,0,0],[328, 325, 320],[344, 338, 326],[1,0,0],[354, 348, 327],
]
(ROOT / "tools/_v125_themes.json").write_text(json.dumps({"themes": T125, "train": TR125, "heldout": HO125}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_125(src):
    src = src.replace("# --- V124 overlays (new vs V50) ---", "# --- V125 overlays (new vs V50) ---")
    src = src.replace("# --- V124 overlays (new vs V49) ---", "# --- V125 overlays (new vs V49) ---")
    for a, b in [
        ("AMBERHEATH bait 68.68", "ASHCOVE bait 69.69"),
        ("CEDAR bait 88.88", "BRIAR bait 89.89"),
        ("DUSK ghost 91.91", "CEDAR ghost 92.92"),
        ("GLEN bait 63.63", "FERN bait 64.64"),
        ("JADE bait 54.54", "INK bait 55.55"),
        ("NETHER bait 98.98", "MIST bait 99.99"),
        ("amber mist + stone ticks (V124-only)", "ash mist + reed ticks (V125-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD124 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v124_themes.json").read_text(encoding="utf-8"))["themes"])
NEW125 = "_".join(t[0] for t in T125)

out = (S / "c851_vision_v124_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C851", "C857"), ("c851", "c857"), ("V124", "V125"), ("v124", "v125"),
    ("_v124c851", "_v125c857"),
    ("Harder than V123", "Harder than V124"), ("harder than V123", "harder than V124"),
    (OLD124, NEW125),
    ("V124 keeps floor", "V125 keeps floor"),
    ("C851 design+fixtures; no VL claim", "C857 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C852 VL smoke", "fixtures only; claim deferred to C858 VL smoke"),
    ("No claim until C852 VL", "No claim until C858 VL"),
    ("kept on V124", "kept on V125"),
    ("vision_images_v124", "vision_images_v125"),
    ("VL_GATE_V124", "VL_GATE_V125"), ("vl_gate_v124", "vl_gate_v125"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V123: amberheath, cedarheath, duskheath, elmheath, fernheath, glenheath, hazeheath, inkheath,\njadeheath, knotheath, lakeheath, mossheath, netherheath, oakheath, pineheath, quillheath, reedheath, stoneheath.",
    "NEW themes vs V124: ashcove, briarcove, cedarcove, dawncove, embercove, ferncove, glencove, hazecove,\ninkcove, jadecove, kelpcove, loamcove, mistcove, nethercove, oakcove, pinecove, quillcove, reedcove.",
)
out = replace_specs(out, build_specs(T125, "v125", "V125", TR125))
out = retarget_125(out)
(S / "c857_vision_v125_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c852_vision_v124_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C852", "C858"), ("c852", "c858"), ("V124", "V125"), ("v124", "v125"),
    ("Uses C851 fixtures", "Uses C857 fixtures"),
    ("vision_images_v124", "vision_images_v125"),
    ("vl_gate_v124", "vl_gate_v125"), ("VL_GATE_V124", "VL_GATE_V125"),
]:
    out = out.replace(a, b)
(S / "c858_vision_v125_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c853_vision_v124_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C853", "C859"), ("c853", "c859"), ("C851", "C857"),
    ("V124", "V125"), ("v124", "v125"),
    ("_v124hc853", "_v125hc859"), ("_v124c851", "_v125c857"),
    ("vl_gate_v124", "vl_gate_v125"), ("VL_GATE_V124", "VL_GATE_V125"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T125, "v125h", "V125H", HO125))
out = retarget_125(out)
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v125h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v125"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v125" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v125h_c859"'); seen_run = True; continue
    out2.append(ln)
(S / "c859_vision_v125_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c848_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C848", "C860"), ("c848", "c860"),
    ("conf_gate_stretch_c848", "conf_gate_stretch_c860"),
    ("after V123", "after V125"), ("after V124", "after V125"),
    ("cg63_", "cg64_"),
]:
    out = out.replace(a, b)
(S / "c860_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence")

out = (S / "c855_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C855", "C861"), ("c855", "c861"),
    ("capture_regression_c855", "capture_regression_c861"),
    ("after C851-C854", "after C857-C860"),
    ("V4-V124+heldout", "V4-V125+heldout"),
]:
    out = out.replace(a, b)
if "VISION_V125_SMOKE" not in out:
    out = out.replace(
        "SMOKE_POINTERS = [",
        'SMOKE_POINTERS = [\n    ("V125", DOC / "C858_VISION_V125_SMOKE.json"),\n    ("V125_heldout", DOC / "C859_VISION_V125_HELDOUT_SMOKE.json"),\n    ("V124", DOC / "C852_VISION_V124_SMOKE.json"),\n    ("V124_heldout", DOC / "C853_VISION_V124_HELDOUT_SMOKE.json"),',
        1,
    )
(S / "c861_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c856_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C856", "C862"), ("c856", "c862"),
    ("C852", "C858"), ("C853", "C859"), ("C855", "C861"),
    ("C851", "C857"),
    ("V124", "V125"), ("v124", "v125"),
    ("V123", "V124"), ("v123", "v124"),
    ("v124_jpeg_q", "v125_jpeg_q"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C848_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C860_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C854_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C854_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C854"}',
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C854"}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C848"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C860"}',
)
out = out.replace(
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C854"}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C854"}',
)
out = out.replace(
    "product-U2C replace={replace} pass={u2c_pass}",
    "confidence-gate rate={conf_rate} pass={conf_pass}",
)
out = out.replace(
    "stage_ready = bool(v125_claim and v125h_claim and v125 >= GATE and v125h >= GATE and capture_pass and disjoint and u2c_pass)",
    "stage_ready = bool(v125_claim and v125h_claim and v125 >= GATE and v125h >= GATE and capture_pass and disjoint and conf_pass)",
)
out = out.replace(
    'f"- C854: confidence-gate rate={conf_rate} pass={conf_pass}"',
    'f"- C860: confidence-gate rate={conf_rate} pass={conf_pass}"',
)
out = out.replace(
    'f"- C854: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C860: confidence-gate rate={conf_rate} pass={conf_pass}"',
)
(S / "c862_scorecard_and_stage.py").write_text(out, encoding="utf-8")
for ln in out.splitlines():
    if any(x in ln for x in ("c656 =", "c650 =", '"confidence_gate"', '"product_u2c"', "stage_ready =", "confidence-gate", "C860:", "C854:")):
        if "load" in ln or "source" in ln or "stage_ready" in ln or "confidence-gate" in ln or "product" in ln:
            print("CHK", ln.strip()[:150])
print("scorecard OK"); print("done")
