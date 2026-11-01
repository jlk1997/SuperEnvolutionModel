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

# *moor — avoid *b; OCR-friendly qty 680+700=1380; PO 638+564=1202
T128 = [
    ["ashmoor","recv","paid_total","ASHMOOR GRAIN RECV","RECV","x"],
    ["cedarmoor","wh","qty_sum","WH CEDARMOOR BIN","RECV","x"],
    ["dawnmoor","refund","refund_done","DAWNMOOR PATCH REFUND","DONE","x"],
    ["elmmoor","tax","tax_base_paid","ELMMOOR TAX SLIP","TAX","x"],
    ["fernmoor","pay","payroll_active","FERNMOOR PAYROLL","PAY","x"],
    ["glenmoor","ship","ship_ok","GLENMOOR SHIP DOCK","SHIP","x"],
    ["hazemoor","sla","sla_ok_hours","HAZEMOOR SLA CARD","SLA","x"],
    ["inkmoor","exp","exp_sum","INKMOOR EXPENSE","EXP","x"],
    ["jademoor","po","po_open","JADEMOOR PO SHEET","PO","x"],
    ["knotmoor","order","order_paid","KNOTMOOR ORDER","ORD","x"],
    ["lakemoor","dup","dup_mark","LAKEMOOR DUP MARK","DUP","x"],
    ["mossmoor","zero","zero_check","MOSSMOOR AIR ZERO","ZERO","x"],
    ["nethermoor","ledger","ledger_net","NETHERMOOR LEDGER","LED","x"],
    ["oakmoor","ui","ui_ok","OAKMOOR UI SCAN","UI","x"],
    ["pinemoor","stack","stack_count","PINEMOOR STACK","STK","x"],
    ["quillmoor","fax","fax_pages","QUILLMOOR FAX","FAX","x"],
    ["reedmoor","glare","glare_ok","REEDMOOR GLARE","GLR","x"],
    ["stonemoor","tab","tab_index","STONEMOOR TAB INDEX","TAB","x"],
]
TR128 = [
    [725.0, 742.5, 535.0],[680, 700, 520],[648.0, 677.25, 515.0],[781.0, 798.0, 605.0],
    [843.0, 867.0, 575.0],[601, 617, 533],[340.0, 380.0, 220.0],[691.0, 722.75, 539.0],
    [725.0, 708.0, 548.0],[758.0, 746.0, 536.0],[1,1,0],[0,0,0],
    [824.0, 845.5, 561.0],[1,0,0],[373, 365, 343],[391, 375, 366],[1,0,0],[417, 393, 363],
]
HO128 = [
    [595.0, 607.75, 488.0],[560, 580, 480],[553.0, 566.5, 476.0],[668.0, 684.0, 517.0],
    [709.0, 725.0, 512.0],[503, 517, 481],[240.0, 280.0, 180.0],[579.0, 600.75, 488.0],
    [638.0, 564.0, 485.0],[626.0, 612.0, 483.0],[1,1,0],[0,0,0],  # po 638+564=1202; qty 560+580=1140
    [661.0, 676.5, 498.0],[1,0,0],[349, 346, 341],[365, 359, 347],[1,0,0],[375, 369, 348],
]
(ROOT / "tools/_v128_themes.json").write_text(json.dumps({"themes": T128, "train": TR128, "heldout": HO128}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_128(src):
    src = src.replace("# --- V127 overlays (new vs V50) ---", "# --- V128 overlays (new vs V50) ---")
    src = src.replace("# --- V127 overlays (new vs V49) ---", "# --- V128 overlays (new vs V49) ---")
    for a, b in [
        ("ASHPEAK bait 71.71", "ASHMOOR bait 72.72"),
        ("CEDARP bait 91.91", "CEDARM bait 92.92"),
        ("DAWNP ghost 94.94", "DAWNM ghost 95.95"),
        ("GLENP bait 66.66", "GLENM bait 67.67"),
        ("JADEP bait 57.57", "JADEM bait 58.58"),
        ("NETHERP bait 92.92", "NETHERM bait 93.93"),
        ("ash mist + stone ticks (V127-only)", "ash mist + stone ticks (V128-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD127 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v127_themes.json").read_text(encoding="utf-8"))["themes"])
NEW128 = "_".join(t[0] for t in T128)

out = (S / "c869_vision_v127_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C869", "C875"), ("c869", "c875"), ("V127", "V128"), ("v127", "v128"),
    ("_v127c869", "_v128c875"),
    ("Harder than V126", "Harder than V127"), ("harder than V126", "harder than V127"),
    (OLD127, NEW128),
    ("V127 keeps floor", "V128 keeps floor"),
    ("C869 design+fixtures; no VL claim", "C875 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C870 VL smoke", "fixtures only; claim deferred to C876 VL smoke"),
    ("No claim until C870 VL", "No claim until C876 VL"),
    ("kept on V127", "kept on V128"),
    ("vision_images_v127", "vision_images_v128"),
    ("VL_GATE_V127", "VL_GATE_V128"), ("vl_gate_v127", "vl_gate_v128"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V126: ashpeak, cedarpeak, dawnpeak, elmpeak, fernpeak, glenpeak, hazepeak, inkpeak,\njadepeak, knotpeak, lakepeak, mosspeak, netherpeak, oakpeak, pinepeak, quillpeak, reedpeak, stonepeak.",
    "NEW themes vs V127: ashmoor, cedarmoor, dawnmoor, elmmoor, fernmoor, glenmoor, hazemoor, inkmoor,\njademoor, knotmoor, lakemoor, mossmoor, nethermoor, oakmoor, pinemoor, quillmoor, reedmoor, stonemoor.",
)
out = replace_specs(out, build_specs(T128, "v128", "V128", TR128))
out = retarget_128(out)
(S / "c875_vision_v128_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c870_vision_v127_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C870", "C876"), ("c870", "c876"), ("V127", "V128"), ("v127", "v128"),
    ("Uses C869 fixtures", "Uses C875 fixtures"),
    ("vision_images_v127", "vision_images_v128"),
    ("vl_gate_v127", "vl_gate_v128"), ("VL_GATE_V127", "VL_GATE_V128"),
]:
    out = out.replace(a, b)
(S / "c876_vision_v128_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c871_vision_v127_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C871", "C877"), ("c871", "c877"), ("C869", "C875"),
    ("V127", "V128"), ("v127", "v128"),
    ("_v127hc871", "_v128hc877"), ("_v127c869", "_v128c875"),
    ("vl_gate_v127", "vl_gate_v128"), ("VL_GATE_V127", "VL_GATE_V128"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T128, "v128h", "V128H", HO128))
out = retarget_128(out)
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v128h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v128"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v128" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v128h_c877"'); seen_run = True; continue
    out2.append(ln)
(S / "c877_vision_v128_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c866_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C866", "C878"), ("c866", "c878"),
    ("product_u2c_c866", "product_u2c_c878"),
    ("after V126", "after V128"), ("after V127", "after V128"),
]:
    out = out.replace(a, b)
(S / "c878_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c873_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C873", "C879"), ("c873", "c879"),
    ("capture_regression_c873", "capture_regression_c879"),
    ("after C869-C872", "after C875-C878"),
    ("V4-V127+heldout", "V4-V128+heldout"),
]:
    out = out.replace(a, b)
if "VISION_V128_SMOKE" not in out:
    out = out.replace(
        "SMOKE_POINTERS = [",
        'SMOKE_POINTERS = [\n    ("V128", DOC / "C876_VISION_V128_SMOKE.json"),\n    ("V128_heldout", DOC / "C877_VISION_V128_HELDOUT_SMOKE.json"),\n    ("V127", DOC / "C870_VISION_V127_SMOKE.json"),\n    ("V127_heldout", DOC / "C871_VISION_V127_HELDOUT_SMOKE.json"),',
        1,
    )
(S / "c879_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c874_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C874", "C880"), ("c874", "c880"),
    ("C870", "C876"), ("C871", "C877"), ("C873", "C879"),
    ("C869", "C875"),
    ("V127", "V128"), ("v127", "v128"),
    ("V126", "V127"), ("v126", "v127"),
    ("v127_jpeg_q", "v128_jpeg_q"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C872_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C872_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C866_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C878_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C866"}',
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C878"}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C872"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C872"}',
)
out = out.replace(
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C866"}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C878"}',
)
out = out.replace(
    "confidence-gate rate={conf_rate} pass={conf_pass}",
    "product-U2C replace={replace} pass={u2c_pass}",
)
out = out.replace(
    "stage_ready = bool(v128_claim and v128h_claim and v128 >= GATE and v128h >= GATE and capture_pass and disjoint and conf_pass)",
    "stage_ready = bool(v128_claim and v128h_claim and v128 >= GATE and v128h >= GATE and capture_pass and disjoint and u2c_pass)",
)
out = out.replace(
    'f"- C872: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C878: product-U2C replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- C872: confidence-gate rate={conf_rate} pass={conf_pass}"',
    'f"- C878: product-U2C replace={replace} pass={u2c_pass}"',
)
(S / "c880_scorecard_and_stage.py").write_text(out, encoding="utf-8")
for ln in out.splitlines():
    if any(x in ln for x in ("c656 =", "c650 =", '"confidence_gate"', '"product_u2c"', "stage_ready =", "product-U2C", "C878:", "C872:")):
        if "load" in ln or "source" in ln or "stage_ready" in ln or "product-U2C" in ln or "confidence" in ln:
            print("CHK", ln.strip()[:150])
print("scorecard OK"); print("done")
