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

# *vale reused? use *wich — avoid *b; qty 690+710; PO 645+571=1216
T129 = [
    ["ashwich","recv","paid_total","ASHWICH GRAIN RECV","RECV","x"],
    ["cedarwich","wh","qty_sum","WH CEDARWICH BIN","RECV","x"],
    ["dawnwich","refund","refund_done","DAWNWICH PATCH REFUND","DONE","x"],
    ["elmwich","tax","tax_base_paid","ELMWICH TAX SLIP","TAX","x"],
    ["fernwich","pay","payroll_active","FERNWICH PAYROLL","PAY","x"],
    ["glenwich","ship","ship_ok","GLENWICH SHIP DOCK","SHIP","x"],
    ["hazewich","sla","sla_ok_hours","HAZEWICH SLA CARD","SLA","x"],
    ["inkwich","exp","exp_sum","INKWICH EXPENSE","EXP","x"],
    ["jadewich","po","po_open","JADEWICH PO SHEET","PO","x"],
    ["knotwich","order","order_paid","KNOTWICH ORDER","ORD","x"],
    ["lakewich","dup","dup_mark","LAKEWICH DUP MARK","DUP","x"],
    ["mosswich","zero","zero_check","MOSSWICH AIR ZERO","ZERO","x"],
    ["netherwich","ledger","ledger_net","NETHERWICH LEDGER","LED","x"],
    ["oakwich","ui","ui_ok","OAKWICH UI SCAN","UI","x"],
    ["pinewich","stack","stack_count","PINEWICH STACK","STK","x"],
    ["quillwich","fax","fax_pages","QUILLWICH FAX","FAX","x"],
    ["reedwich","glare","glare_ok","REEDWICH GLARE","GLR","x"],
    ["stonewich","tab","tab_index","STONEWICH TAB INDEX","TAB","x"],
]
TR129 = [
    [732.0, 749.5, 542.0],[690, 710, 530],[655.0, 684.25, 522.0],[788.0, 805.0, 612.0],
    [850.0, 874.0, 582.0],[608, 624, 540],[340.0, 380.0, 220.0],[698.0, 729.75, 546.0],
    [732.0, 715.0, 555.0],[765.0, 753.0, 543.0],[1,1,0],[0,0,0],
    [831.0, 852.5, 568.0],[1,0,0],[380, 372, 350],[398, 382, 373],[1,0,0],[424, 400, 370],
]
HO129 = [
    [602.0, 614.75, 495.0],[570, 590, 490],[560.0, 573.5, 483.0],[675.0, 691.0, 524.0],
    [716.0, 732.0, 519.0],[510, 524, 488],[240.0, 280.0, 180.0],[586.0, 607.75, 495.0],
    [645.0, 571.0, 492.0],[633.0, 619.0, 490.0],[1,1,0],[0,0,0],  # po 645+571=1216; qty 570+590=1160
    [668.0, 683.5, 505.0],[1,0,0],[356, 353, 348],[372, 366, 354],[1,0,0],[382, 376, 355],
]
(ROOT / "tools/_v129_themes.json").write_text(json.dumps({"themes": T129, "train": TR129, "heldout": HO129}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_129(src):
    src = src.replace("# --- V128 overlays (new vs V50) ---", "# --- V129 overlays (new vs V50) ---")
    src = src.replace("# --- V128 overlays (new vs V49) ---", "# --- V129 overlays (new vs V49) ---")
    for a, b in [
        ("ASHMOOR bait 72.72", "ASHWICH bait 73.73"),
        ("CEDARM bait 92.92", "CEDARW bait 93.93"),
        ("DAWNM ghost 95.95", "DAWNW ghost 96.96"),
        ("GLENM bait 67.67", "GLENW bait 68.68"),
        ("JADEM bait 58.58", "JADEW bait 59.59"),
        ("NETHERM bait 93.93", "NETHERW bait 94.94"),
        ("ash mist + stone ticks (V128-only)", "ash mist + stone ticks (V129-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD128 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v128_themes.json").read_text(encoding="utf-8"))["themes"])
NEW129 = "_".join(t[0] for t in T129)

out = (S / "c875_vision_v128_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C875", "C881"), ("c875", "c881"), ("V128", "V129"), ("v128", "v129"),
    ("_v128c875", "_v129c881"),
    ("Harder than V127", "Harder than V128"), ("harder than V127", "harder than V128"),
    (OLD128, NEW129),
    ("V128 keeps floor", "V129 keeps floor"),
    ("C875 design+fixtures; no VL claim", "C881 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C876 VL smoke", "fixtures only; claim deferred to C882 VL smoke"),
    ("No claim until C876 VL", "No claim until C882 VL"),
    ("kept on V128", "kept on V129"),
    ("vision_images_v128", "vision_images_v129"),
    ("VL_GATE_V128", "VL_GATE_V129"), ("vl_gate_v128", "vl_gate_v129"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V127: ashmoor, cedarmoor, dawnmoor, elmmoor, fernmoor, glenmoor, hazemoor, inkmoor,\njademoor, knotmoor, lakemoor, mossmoor, nethermoor, oakmoor, pinemoor, quillmoor, reedmoor, stonemoor.",
    "NEW themes vs V128: ashwich, cedarwich, dawnwich, elmwich, fernwich, glenwich, hazewich, inkwich,\njadewich, knotwich, lakewich, mosswich, netherwich, oakwich, pinewich, quillwich, reedwich, stonewich.",
)
out = replace_specs(out, build_specs(T129, "v129", "V129", TR129))
out = retarget_129(out)
(S / "c881_vision_v129_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c876_vision_v128_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C876", "C882"), ("c876", "c882"), ("V128", "V129"), ("v128", "v129"),
    ("Uses C875 fixtures", "Uses C881 fixtures"),
    ("vision_images_v128", "vision_images_v129"),
    ("vl_gate_v128", "vl_gate_v129"), ("VL_GATE_V128", "VL_GATE_V129"),
]:
    out = out.replace(a, b)
(S / "c882_vision_v129_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c877_vision_v128_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C877", "C883"), ("c877", "c883"), ("C875", "C881"),
    ("V128", "V129"), ("v128", "v129"),
    ("_v128hc877", "_v129hc883"), ("_v128c875", "_v129c881"),
    ("vl_gate_v128", "vl_gate_v129"), ("VL_GATE_V128", "VL_GATE_V129"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T129, "v129h", "V129H", HO129))
out = retarget_129(out)
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v129h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v129"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v129" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v129h_c883"'); seen_run = True; continue
    out2.append(ln)
(S / "c883_vision_v129_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c872_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C872", "C884"), ("c872", "c884"),
    ("conf_gate_stretch_c872", "conf_gate_stretch_c884"),
    ("after V127", "after V129"), ("after V128", "after V129"),
    ("cg65_", "cg66_"),
]:
    out = out.replace(a, b)
(S / "c884_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence")

out = (S / "c879_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C879", "C885"), ("c879", "c885"),
    ("capture_regression_c879", "capture_regression_c885"),
    ("after C875-C878", "after C881-C884"),
    ("V4-V128+heldout", "V4-V129+heldout"),
]:
    out = out.replace(a, b)
if "VISION_V129_SMOKE" not in out:
    out = out.replace(
        "SMOKE_POINTERS = [",
        'SMOKE_POINTERS = [\n    ("V129", DOC / "C882_VISION_V129_SMOKE.json"),\n    ("V129_heldout", DOC / "C883_VISION_V129_HELDOUT_SMOKE.json"),\n    ("V128", DOC / "C876_VISION_V128_SMOKE.json"),\n    ("V128_heldout", DOC / "C877_VISION_V128_HELDOUT_SMOKE.json"),',
        1,
    )
(S / "c885_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c880_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C880", "C886"), ("c880", "c886"),
    ("C876", "C882"), ("C877", "C883"), ("C879", "C885"),
    ("C875", "C881"),
    ("V128", "V129"), ("v128", "v129"),
    ("V127", "V128"), ("v127", "v128"),
    ("v128_jpeg_q", "v129_jpeg_q"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C872_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C884_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C878_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C878_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C878"}',
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C878"}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C872"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C884"}',
)
out = out.replace(
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C878"}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C878"}',
)
out = out.replace(
    "product-U2C replace={replace} pass={u2c_pass}",
    "confidence-gate rate={conf_rate} pass={conf_pass}",
)
out = out.replace(
    "stage_ready = bool(v129_claim and v129h_claim and v129 >= GATE and v129h >= GATE and capture_pass and disjoint and u2c_pass)",
    "stage_ready = bool(v129_claim and v129h_claim and v129 >= GATE and v129h >= GATE and capture_pass and disjoint and conf_pass)",
)
out = out.replace(
    'f"- C878: confidence-gate rate={conf_rate} pass={conf_pass}"',
    'f"- C884: confidence-gate rate={conf_rate} pass={conf_pass}"',
)
out = out.replace(
    'f"- C878: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C884: confidence-gate rate={conf_rate} pass={conf_pass}"',
)
(S / "c886_scorecard_and_stage.py").write_text(out, encoding="utf-8")
for ln in out.splitlines():
    if any(x in ln for x in ("c656 =", "c650 =", '"confidence_gate"', '"product_u2c"', "stage_ready =", "confidence-gate", "C884:", "C878:")):
        if "load" in ln or "source" in ln or "stage_ready" in ln or "confidence-gate" in ln or "product" in ln:
            print("CHK", ln.strip()[:150])
print("scorecard OK"); print("done")
