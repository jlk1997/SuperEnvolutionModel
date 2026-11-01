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

# *haven — avoid *b and prior; qty TR 730+750 HO 610+630; PO HO 673+587=1260; SLA 380+420
T133 = [
    ["ashhaven","recv","paid_total","ASHHAVEN GRAIN RECV","RECV","x"],
    ["cedarhaven","wh","qty_sum","WH CEDARHAVEN BIN","RECV","x"],
    ["dawnhaven","refund","refund_done","DAWNHAVEN PATCH REFUND","DONE","x"],
    ["elmhaven","tax","tax_base_paid","ELMHAVEN TAX SLIP","TAX","x"],
    ["fernhaven","pay","payroll_active","FERNHAVEN PAYROLL","PAY","x"],
    ["glenhaven","ship","ship_ok","GLENHAVEN SHIP DOCK","SHIP","x"],
    ["hazehaven","sla","sla_ok_hours","HAZEHAVEN SLA CARD","SLA","x"],
    ["inkhaven","exp","exp_sum","INKHAVEN EXPENSE","EXP","x"],
    ["jadehaven","po","po_open","JADEHAVEN PO SHEET","PO","x"],
    ["knothaven","order","order_paid","KNOTHAVEN ORDER","ORD","x"],
    ["lakehaven","dup","dup_mark","LAKEHAVEN DUP MARK","DUP","x"],
    ["mosshaven","zero","zero_check","MOSSHAVEN AIR ZERO","ZERO","x"],
    ["netherhaven","ledger","ledger_net","NETHERHAVEN LEDGER","LED","x"],
    ["oakhaven","ui","ui_ok","OAKHAVEN UI SCAN","UI","x"],
    ["pinehaven","stack","stack_count","PINEHAVEN STACK","STK","x"],
    ["quillhaven","fax","fax_pages","QUILLHAVEN FAX","FAX","x"],
    ["reedhaven","glare","glare_ok","REEDHAVEN GLARE","GLR","x"],
    ["stonehaven","tab","tab_index","STONEHAVEN TAB INDEX","TAB","x"],
]
TR133 = [
    [772.0, 789.5, 582.0],[730, 750, 570],[695.0, 724.25, 562.0],[828.0, 845.0, 652.0],
    [890.0, 914.0, 622.0],[648, 664, 580],[380.0, 420.0, 260.0],[738.0, 769.75, 586.0],
    [780.0, 740.0, 590.0],[805.0, 793.0, 583.0],[1,1,0],[0,0,0],
    [871.0, 892.5, 608.0],[1,0,0],[420, 412, 390],[438, 422, 413],[1,0,0],[464, 440, 410],
]
HO133 = [
    [642.0, 654.75, 535.0],[610, 630, 530],[600.0, 613.5, 523.0],[715.0, 731.0, 564.0],
    [756.0, 772.0, 559.0],[550, 564, 528],[280.0, 320.0, 220.0],[626.0, 647.75, 535.0],
    [673.0, 587.0, 532.0],[673.0, 659.0, 530.0],[1,1,0],[0,0,0],  # po 673+587=1260; qty 610+630=1240
    [708.0, 723.5, 545.0],[1,0,0],[396, 393, 388],[412, 406, 394],[1,0,0],[422, 416, 395],
]
(ROOT / "tools/_v133_themes.json").write_text(json.dumps({"themes": T133, "train": TR133, "heldout": HO133}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_133(src):
    src = src.replace("# --- V132 overlays (new vs V50) ---", "# --- V133 overlays (new vs V50) ---")
    src = src.replace("# --- V132 overlays (new vs V49) ---", "# --- V133 overlays (new vs V49) ---")
    for a, b in [
        ("ASHCROFT bait 76.76", "ASHHAVEN bait 77.77"),
        ("CEDARC bait 96.96", "CEDARH bait 97.97"),
        ("DAWNC ghost 99.99", "DAWNH ghost 91.91"),
        ("GLENC bait 71.71", "GLENH bait 72.72"),
        ("JADEC bait 62.62", "JADEH bait 63.63"),
        ("NETHERC bait 97.97", "NETHERH bait 98.98"),
        ("ash mist + stone ticks (V132-only)", "ash mist + stone ticks (V133-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD132 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v132_themes.json").read_text(encoding="utf-8"))["themes"])
NEW133 = "_".join(t[0] for t in T133)

out = (S / "c899_vision_v132_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C899", "C905"), ("c899", "c905"), ("V132", "V133"), ("v132", "v133"),
    ("_v132c899", "_v133c905"),
    ("Harder than V131", "Harder than V132"), ("harder than V131", "harder than V132"),
    (OLD132, NEW133),
    ("V132 keeps floor", "V133 keeps floor"),
    ("C899 design+fixtures; no VL claim", "C905 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C900 VL smoke", "fixtures only; claim deferred to C906 VL smoke"),
    ("No claim until C900 VL", "No claim until C906 VL"),
    ("kept on V132", "kept on V133"),
    ("vision_images_v132", "vision_images_v133"),
    ("VL_GATE_V132", "VL_GATE_V133"), ("vl_gate_v132", "vl_gate_v133"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V131: ashcroft, cedarcroft, dawncroft, elmcroft, ferncroft, glencroft, hazecroft, inkcroft,\njadecroft, knotcroft, lakecroft, mosscroft, nethercroft, oakcroft, pinecroft, quillcroft, reedcroft, stonecroft.",
    "NEW themes vs V132: ashhaven, cedarhaven, dawnhaven, elmhaven, fernhaven, glenhaven, hazehaven, inkhaven,\njadehaven, knothaven, lakehaven, mosshaven, netherhaven, oakhaven, pinehaven, quillhaven, reedhaven, stonehaven.",
)
out = replace_specs(out, build_specs(T133, "v133", "V133", TR133))
out = retarget_133(out)
(S / "c905_vision_v133_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c900_vision_v132_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C900", "C906"), ("c900", "c906"), ("V132", "V133"), ("v132", "v133"),
    ("Uses C899 fixtures", "Uses C905 fixtures"),
    ("vision_images_v132", "vision_images_v133"),
    ("vl_gate_v132", "vl_gate_v133"), ("VL_GATE_V132", "VL_GATE_V133"),
]:
    out = out.replace(a, b)
(S / "c906_vision_v133_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c901_vision_v132_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C901", "C907"), ("c901", "c907"), ("C899", "C905"),
    ("V132", "V133"), ("v132", "v133"),
    ("_v132hc901", "_v133hc907"), ("_v132c899", "_v133c905"),
    ("vl_gate_v132", "vl_gate_v133"), ("VL_GATE_V132", "VL_GATE_V133"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T133, "v133h", "V133H", HO133))
out = retarget_133(out)
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v133h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v133"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v133" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v133h_c907"'); seen_run = True; continue
    out2.append(ln)
(S / "c907_vision_v133_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c896_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C896", "C908"), ("c896", "c908"),
    ("conf_gate_stretch_c896", "conf_gate_stretch_c908"),
    ("after V131", "after V133"), ("after V132", "after V133"),
    ("cg67_", "cg68_"),
]:
    out = out.replace(a, b)
(S / "c908_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence")

out = (S / "c903_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C903", "C909"), ("c903", "c909"),
    ("capture_regression_c903", "capture_regression_c909"),
    ("after C899-C902", "after C905-C908"),
    ("V4-V132+heldout", "V4-V133+heldout"),
]:
    out = out.replace(a, b)
if "VISION_V133_SMOKE" not in out:
    out = out.replace(
        "SMOKE_POINTERS = [",
        'SMOKE_POINTERS = [\n    ("V133", DOC / "C906_VISION_V133_SMOKE.json"),\n    ("V133_heldout", DOC / "C907_VISION_V133_HELDOUT_SMOKE.json"),\n    ("V132", DOC / "C900_VISION_V132_SMOKE.json"),\n    ("V132_heldout", DOC / "C901_VISION_V132_HELDOUT_SMOKE.json"),',
        1,
    )
(S / "c909_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c904_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C904", "C910"), ("c904", "c910"),
    ("C900", "C906"), ("C901", "C907"), ("C903", "C909"),
    ("C899", "C905"),
    ("V132", "V133"), ("v132", "v133"),
    ("V131", "V132"), ("v131", "v132"),
    ("v132_jpeg_q", "v133_jpeg_q"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C896_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C908_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C902_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C902_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C902"}',
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C902"}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C896"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C908"}',
)
out = out.replace(
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C902"}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C902"}',
)
out = out.replace(
    "product-U2C replace={replace} pass={u2c_pass}",
    "confidence-gate rate={conf_rate} pass={conf_pass}",
)
out = out.replace(
    "stage_ready = bool(v133_claim and v133h_claim and v133 >= GATE and v133h >= GATE and capture_pass and disjoint and u2c_pass)",
    "stage_ready = bool(v133_claim and v133h_claim and v133 >= GATE and v133h >= GATE and capture_pass and disjoint and conf_pass)",
)
out = out.replace(
    'f"- C902: confidence-gate rate={conf_rate} pass={conf_pass}"',
    'f"- C908: confidence-gate rate={conf_rate} pass={conf_pass}"',
)
out = out.replace(
    'f"- C902: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C908: confidence-gate rate={conf_rate} pass={conf_pass}"',
)
(S / "c910_scorecard_and_stage.py").write_text(out, encoding="utf-8")
for ln in out.splitlines():
    if any(x in ln for x in ("c656 =", "c650 =", '"confidence_gate"', '"product_u2c"', "stage_ready =", "confidence-gate", "C908:", "C902:")):
        if "load" in ln or "source" in ln or "stage_ready" in ln or "confidence-gate" in ln or "product" in ln:
            print("CHK", ln.strip()[:160])
print("scorecard OK"); print("done")
