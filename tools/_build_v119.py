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

# *fen themes — avoid *b; OCR-friendly (no mid-0 totals like 1032)
T119 = [
    ["azurefen","recv","paid_total","AZUREFEN GRAIN RECV","RECV","x"],
    ["brackenfen","wh","qty_sum","WH BRACKENFEN BIN","RECV","x"],
    ["copperfen","refund","refund_done","COPPERFEN PATCH REFUND","DONE","x"],
    ["dawnfen","tax","tax_base_paid","DAWNFEN TAX SLIP","TAX","x"],
    ["echoofen","pay","payroll_active","ECHOFEN PAYROLL","PAY","x"],
    ["frostfen","ship","ship_ok","FROSTFEN SHIP DOCK","SHIP","x"],
    ["gorsefen","sla","sla_ok_hours","GORSEFEN SLA CARD","SLA","x"],
    ["hollowfen","exp","exp_sum","HOLLOWFEN EXPENSE","EXP","x"],
    ["ivoryfen","po","po_open","IVORYFEN PO SHEET","PO","x"],
    ["jasperfen","order","order_paid","JASPERFEN ORDER","ORD","x"],
    ["kelpfen","dup","dup_mark","KELPFEN DUP MARK","DUP","x"],
    ["lunarfen","zero","zero_check","LUNARFEN AIR ZERO","ZERO","x"],
    ["meadowfen","ledger","ledger_net","MEADOWFEN LEDGER","LED","x"],
    ["nimbusfen","ui","ui_ok","NIMBUSFEN UI SCAN","UI","x"],
    ["orchidfen","stack","stack_count","ORCHIDFEN STACK","STK","x"],
    ["pebblefen","fax","fax_pages","PEBBLEFEN FAX","FAX","x"],
    ["quartzfen","glare","glare_ok","QUARTZFEN GLARE","GLR","x"],
    ["ravenfen","tab","tab_index","RAVENFEN TAB INDEX","TAB","x"],
]
# fix echoofen typo
T119[4] = ["echofen","pay","payroll_active","ECHOFEN PAYROLL","PAY","x"]
TR119 = [
    [662.0, 679.5, 472.0],[589, 630, 444],[585.0, 614.25, 452.0],[718.0, 735.0, 542.0],
    [780.0, 804.0, 512.0],[538, 554, 470],[340.0, 380.0, 220.0],[628.0, 659.75, 476.0],
    [662.0, 645.0, 485.0],[695.0, 683.0, 473.0],[1,1,0],[0,0,0],
    [761.0, 782.5, 498.0],[1,0,0],[310, 302, 280],[328, 312, 303],[1,0,0],[354, 330, 300],
]
HO119 = [
    [532.0, 544.75, 425.0],[487, 527, 407],[490.0, 503.5, 413.0],[605.0, 621.0, 454.0],
    [646.0, 662.0, 449.0],[440, 454, 418],[240.0, 280.0, 180.0],[516.0, 537.75, 425.0],
    [575.0, 501.0, 422.0],[563.0, 549.0, 420.0],[1,1,0],[0,0,0],  # po 575+501=1076
    [598.0, 613.5, 435.0],[1,0,0],[286, 283, 278],[302, 296, 284],[1,0,0],[312, 306, 285],
]
(ROOT / "tools/_v119_themes.json").write_text(json.dumps({"themes": T119, "train": TR119, "heldout": HO119}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_119(src):
    src = src.replace("# --- V118 overlays (new vs V50) ---", "# --- V119 overlays (new vs V50) ---")
    src = src.replace("# --- V118 overlays (new vs V49) ---", "# --- V119 overlays (new vs V49) ---")
    for a, b in [
        ("ASHVALE bait 62.62", "AZUREFEN bait 63.63"),
        ("CLIFF bait 82.82", "BRACKEN bait 83.83"),
        ("DUSK ghost 94.94", "COPPER ghost 95.95"),
        ("HEATH bait 57.57", "FROST bait 58.58"),
        ("KESTREL bait 48.48", "IVORY bait 49.49"),
        ("OAK bait 92.92", "MEADOW bait 93.93"),
        ("ash mist + tide ticks (V118-only)", "azure mist + raven ticks (V119-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD118 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v118_themes.json").read_text(encoding="utf-8"))["themes"])
NEW119 = "_".join(t[0] for t in T119)

out = (S / "c815_vision_v118_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C815", "C821"), ("c815", "c821"), ("V118", "V119"), ("v118", "v119"),
    ("_v118c815", "_v119c821"),
    ("Harder than V117", "Harder than V118"), ("harder than V117", "harder than V118"),
    (OLD118, NEW119),
    ("V118 keeps floor", "V119 keeps floor"),
    ("C815 design+fixtures; no VL claim", "C821 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C816 VL smoke", "fixtures only; claim deferred to C822 VL smoke"),
    ("No claim until C816 VL", "No claim until C822 VL"),
    ("kept on V118", "kept on V119"),
    ("vision_images_v118", "vision_images_v119"),
    ("VL_GATE_V118", "VL_GATE_V119"), ("vl_gate_v118", "vl_gate_v119"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V117: ashvale, cliffvale, duskvale, fernvale, glenvale, heathvale, inkvale, jetvale,\nkestrelvale, lakevale, mistvale, northvale, oakvale, pinevale, quillvale, reedvale, stonevale, tidevale.",
    "NEW themes vs V118: azurefen, brackenfen, copperfen, dawnfen, echofen, frostfen, gorsefen, hollowfen,\nivoryfen, jasperfen, kelpfen, lunarfen, meadowfen, nimbusfen, orchidfen, pebblefen, quartzfen, ravenfen.",
)
out = replace_specs(out, build_specs(T119, "v119", "V119", TR119))
out = retarget_119(out)
(S / "c821_vision_v119_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c816_vision_v118_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C816", "C822"), ("c816", "c822"), ("V118", "V119"), ("v118", "v119"),
    ("Uses C815 fixtures", "Uses C821 fixtures"),
    ("vision_images_v118", "vision_images_v119"),
    ("vl_gate_v118", "vl_gate_v119"), ("VL_GATE_V118", "VL_GATE_V119"),
]:
    out = out.replace(a, b)
(S / "c822_vision_v119_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c817_vision_v118_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C817", "C823"), ("c817", "c823"), ("C815", "C821"),
    ("V118", "V119"), ("v118", "v119"),
    ("_v118hc817", "_v119hc823"), ("_v118c815", "_v119c821"),
    ("vl_gate_v118", "vl_gate_v119"), ("VL_GATE_V118", "VL_GATE_V119"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T119, "v119h", "V119H", HO119))
out = retarget_119(out)
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v119h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v119"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v119" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v119h_c823"'); seen_run = True; continue
    out2.append(ln)
(S / "c823_vision_v119_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c812_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C812", "C824"), ("c812", "c824"),
    ("conf_gate_stretch_c812", "conf_gate_stretch_c824"),
    ("after V117", "after V119"), ("after V118", "after V119"),
    ("cg60_", "cg61_"),
]:
    out = out.replace(a, b)
(S / "c824_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence")

out = (S / "c819_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C819", "C825"), ("c819", "c825"),
    ("capture_regression_c819", "capture_regression_c825"),
    ("after C815-C818", "after C821-C824"),
    ("V4-V118+heldout", "V4-V119+heldout"),
]:
    out = out.replace(a, b)
if "VISION_V119_SMOKE" not in out:
    out = out.replace(
        "SMOKE_POINTERS = [",
        'SMOKE_POINTERS = [\n    ("V119", DOC / "C822_VISION_V119_SMOKE.json"),\n    ("V119_heldout", DOC / "C823_VISION_V119_HELDOUT_SMOKE.json"),\n    ("V118", DOC / "C816_VISION_V118_SMOKE.json"),\n    ("V118_heldout", DOC / "C817_VISION_V118_HELDOUT_SMOKE.json"),',
        1,
    )
(S / "c825_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c820_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C820", "C826"), ("c820", "c826"),
    ("C816", "C822"), ("C817", "C823"), ("C819", "C825"),
    ("C815", "C821"),
    ("V118", "V119"), ("v118", "v119"),
    ("V117", "V118"), ("v117", "v118"),
    ("v118_jpeg_q", "v119_jpeg_q"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C812_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C824_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C818_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C818_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C818"}',
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C818"}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C812"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C824"}',
)
out = out.replace(
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C818"}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C818"}',
)
out = out.replace(
    "product-U2C replace={replace} pass={u2c_pass}",
    "confidence-gate rate={conf_rate} pass={conf_pass}",
)
out = out.replace(
    "stage_ready = bool(v119_claim and v119h_claim and v119 >= GATE and v119h >= GATE and capture_pass and disjoint and u2c_pass)",
    "stage_ready = bool(v119_claim and v119h_claim and v119 >= GATE and v119h >= GATE and capture_pass and disjoint and conf_pass)",
)
out = out.replace(
    'f"- C818: confidence-gate rate={conf_rate} pass={conf_pass}"',
    'f"- C824: confidence-gate rate={conf_rate} pass={conf_pass}"',
)
out = out.replace(
    'f"- C818: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C824: confidence-gate rate={conf_rate} pass={conf_pass}"',
)
(S / "c826_scorecard_and_stage.py").write_text(out, encoding="utf-8")
for ln in out.splitlines():
    if any(x in ln for x in ("c656 =", "c650 =", '"confidence_gate"', '"product_u2c"', "stage_ready =", "confidence-gate", "C824:", "C818:")):
        if "load" in ln or "source" in ln or "stage_ready" in ln or "confidence-gate" in ln or "product" in ln:
            print("CHK", ln.strip()[:150])
print("scorecard OK"); print("done")
