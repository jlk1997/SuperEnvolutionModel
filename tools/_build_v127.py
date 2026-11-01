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

# *peak — avoid *b; OCR-friendly qty 670+690; PO 631+557=1188
T127 = [
    ["ashpeak","recv","paid_total","ASHPEAK GRAIN RECV","RECV","x"],
    ["cedarpeak","wh","qty_sum","WH CEDARPEAK BIN","RECV","x"],
    ["dawnpeak","refund","refund_done","DAWNPEAK PATCH REFUND","DONE","x"],
    ["elmpeak","tax","tax_base_paid","ELMPEAK TAX SLIP","TAX","x"],
    ["fernpeak","pay","payroll_active","FERNPEAK PAYROLL","PAY","x"],
    ["glenpeak","ship","ship_ok","GLENPEAK SHIP DOCK","SHIP","x"],
    ["hazepeak","sla","sla_ok_hours","HAZEPEAK SLA CARD","SLA","x"],
    ["inkpeak","exp","exp_sum","INKPEAK EXPENSE","EXP","x"],
    ["jadepeak","po","po_open","JADEPEAK PO SHEET","PO","x"],
    ["knotpeak","order","order_paid","KNOTPEAK ORDER","ORD","x"],
    ["lakepeak","dup","dup_mark","LAKEPEAK DUP MARK","DUP","x"],
    ["mosspeak","zero","zero_check","MOSSPEAK AIR ZERO","ZERO","x"],
    ["netherpeak","ledger","ledger_net","NETHERPEAK LEDGER","LED","x"],
    ["oakpeak","ui","ui_ok","OAKPEAK UI SCAN","UI","x"],
    ["pinepeak","stack","stack_count","PINEPEAK STACK","STK","x"],
    ["quillpeak","fax","fax_pages","QUILLPEAK FAX","FAX","x"],
    ["reedpeak","glare","glare_ok","REEDPEAK GLARE","GLR","x"],
    ["stonepeak","tab","tab_index","STONEPEAK TAB INDEX","TAB","x"],
]
TR127 = [
    [718.0, 735.5, 528.0],[670, 690, 510],[641.0, 670.25, 508.0],[774.0, 791.0, 598.0],
    [836.0, 860.0, 568.0],[594, 610, 526],[340.0, 380.0, 220.0],[684.0, 715.75, 532.0],
    [718.0, 701.0, 541.0],[751.0, 739.0, 529.0],[1,1,0],[0,0,0],
    [817.0, 838.5, 554.0],[1,0,0],[366, 358, 336],[384, 368, 359],[1,0,0],[410, 386, 356],
]
HO127 = [
    [588.0, 600.75, 481.0],[550, 570, 470],[546.0, 559.5, 469.0],[661.0, 677.0, 510.0],
    [702.0, 718.0, 505.0],[496, 510, 474],[240.0, 280.0, 180.0],[572.0, 593.75, 481.0],
    [631.0, 557.0, 478.0],[619.0, 605.0, 476.0],[1,1,0],[0,0,0],  # po 631+557=1188; qty 550+570=1120
    [654.0, 669.5, 491.0],[1,0,0],[342, 339, 334],[358, 352, 340],[1,0,0],[368, 362, 341],
]
(ROOT / "tools/_v127_themes.json").write_text(json.dumps({"themes": T127, "train": TR127, "heldout": HO127}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_127(src):
    src = src.replace("# --- V126 overlays (new vs V50) ---", "# --- V127 overlays (new vs V50) ---")
    src = src.replace("# --- V126 overlays (new vs V49) ---", "# --- V127 overlays (new vs V49) ---")
    for a, b in [
        ("AMBERDALE bait 70.70", "ASHPEAK bait 71.71"),
        ("CEDAR bait 90.90", "CEDARP bait 91.91"),
        ("DAWN ghost 93.93", "DAWNP ghost 94.94"),
        ("GLEN bait 65.65", "GLENP bait 66.66"),
        ("JADE bait 56.56", "JADEP bait 57.57"),
        ("NETHER bait 91.91", "NETHERP bait 92.92"),
        ("amber mist + stone ticks (V126-only)", "ash mist + stone ticks (V127-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD126 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v126_themes.json").read_text(encoding="utf-8"))["themes"])
NEW127 = "_".join(t[0] for t in T127)

out = (S / "c863_vision_v126_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C863", "C869"), ("c863", "c869"), ("V126", "V127"), ("v126", "v127"),
    ("_v126c863", "_v127c869"),
    ("Harder than V125", "Harder than V126"), ("harder than V125", "harder than V126"),
    (OLD126, NEW127),
    ("V126 keeps floor", "V127 keeps floor"),
    ("C863 design+fixtures; no VL claim", "C869 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C864 VL smoke", "fixtures only; claim deferred to C870 VL smoke"),
    ("No claim until C864 VL", "No claim until C870 VL"),
    ("kept on V126", "kept on V127"),
    ("vision_images_v126", "vision_images_v127"),
    ("VL_GATE_V126", "VL_GATE_V127"), ("vl_gate_v126", "vl_gate_v127"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V125: amberdale, cedardale, dawndale, elmdale, ferndale, glendale, hazedale, inkdale,\njadedale, knotdale, lakedale, mossdale, netherdale, oakdale, pinedale, quilldale, reeddale, stonedale.",
    "NEW themes vs V126: ashpeak, cedarpeak, dawnpeak, elmpeak, fernpeak, glenpeak, hazepeak, inkpeak,\njadepeak, knotpeak, lakepeak, mosspeak, netherpeak, oakpeak, pinepeak, quillpeak, reedpeak, stonepeak.",
)
out = replace_specs(out, build_specs(T127, "v127", "V127", TR127))
out = retarget_127(out)
(S / "c869_vision_v127_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c864_vision_v126_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C864", "C870"), ("c864", "c870"), ("V126", "V127"), ("v126", "v127"),
    ("Uses C863 fixtures", "Uses C869 fixtures"),
    ("vision_images_v126", "vision_images_v127"),
    ("vl_gate_v126", "vl_gate_v127"), ("VL_GATE_V126", "VL_GATE_V127"),
]:
    out = out.replace(a, b)
(S / "c870_vision_v127_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c865_vision_v126_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C865", "C871"), ("c865", "c871"), ("C863", "C869"),
    ("V126", "V127"), ("v126", "v127"),
    ("_v126hc865", "_v127hc871"), ("_v126c863", "_v127c869"),
    ("vl_gate_v126", "vl_gate_v127"), ("VL_GATE_V126", "VL_GATE_V127"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T127, "v127h", "V127H", HO127))
out = retarget_127(out)
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v127h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v127"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v127" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v127h_c871"'); seen_run = True; continue
    out2.append(ln)
(S / "c871_vision_v127_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c860_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C860", "C872"), ("c860", "c872"),
    ("conf_gate_stretch_c860", "conf_gate_stretch_c872"),
    ("after V125", "after V127"), ("after V126", "after V127"),
    ("cg64_", "cg65_"),
]:
    out = out.replace(a, b)
(S / "c872_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence")

out = (S / "c867_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C867", "C873"), ("c867", "c873"),
    ("capture_regression_c867", "capture_regression_c873"),
    ("after C863-C866", "after C869-C872"),
    ("V4-V126+heldout", "V4-V127+heldout"),
]:
    out = out.replace(a, b)
if "VISION_V127_SMOKE" not in out:
    out = out.replace(
        "SMOKE_POINTERS = [",
        'SMOKE_POINTERS = [\n    ("V127", DOC / "C870_VISION_V127_SMOKE.json"),\n    ("V127_heldout", DOC / "C871_VISION_V127_HELDOUT_SMOKE.json"),\n    ("V126", DOC / "C864_VISION_V126_SMOKE.json"),\n    ("V126_heldout", DOC / "C865_VISION_V126_HELDOUT_SMOKE.json"),',
        1,
    )
(S / "c873_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c868_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C868", "C874"), ("c868", "c874"),
    ("C864", "C870"), ("C865", "C871"), ("C867", "C873"),
    ("C863", "C869"),
    ("V126", "V127"), ("v126", "v127"),
    ("V125", "V126"), ("v125", "v126"),
    ("v126_jpeg_q", "v127_jpeg_q"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C860_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C872_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C866_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C866_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C866"}',
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C866"}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C860"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C872"}',
)
out = out.replace(
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C866"}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C866"}',
)
out = out.replace(
    "product-U2C replace={replace} pass={u2c_pass}",
    "confidence-gate rate={conf_rate} pass={conf_pass}",
)
out = out.replace(
    "stage_ready = bool(v127_claim and v127h_claim and v127 >= GATE and v127h >= GATE and capture_pass and disjoint and u2c_pass)",
    "stage_ready = bool(v127_claim and v127h_claim and v127 >= GATE and v127h >= GATE and capture_pass and disjoint and conf_pass)",
)
out = out.replace(
    'f"- C866: confidence-gate rate={conf_rate} pass={conf_pass}"',
    'f"- C872: confidence-gate rate={conf_rate} pass={conf_pass}"',
)
out = out.replace(
    'f"- C866: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C872: confidence-gate rate={conf_rate} pass={conf_pass}"',
)
(S / "c874_scorecard_and_stage.py").write_text(out, encoding="utf-8")
for ln in out.splitlines():
    if any(x in ln for x in ("c656 =", "c650 =", '"confidence_gate"', '"product_u2c"', "stage_ready =", "confidence-gate", "C872:", "C866:")):
        if "load" in ln or "source" in ln or "stage_ready" in ln or "confidence-gate" in ln or "product" in ln:
            print("CHK", ln.strip()[:150])
print("scorecard OK"); print("done")
