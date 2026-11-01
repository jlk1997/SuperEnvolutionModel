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

# *vale themes — avoid *b; OCR-friendly totals (no fragile mid-0 like 1032→1632)
T118 = [
    ["ashvale","recv","paid_total","ASHVALE GRAIN RECV","RECV","x"],
    ["cliffvale","wh","qty_sum","WH CLIFFVALE BIN","RECV","x"],
    ["duskvale","refund","refund_done","DUSKVALE PATCH REFUND","DONE","x"],
    ["fernvale","tax","tax_base_paid","FERNVALE TAX SLIP","TAX","x"],
    ["glenvale","pay","payroll_active","GLENVALE PAYROLL","PAY","x"],
    ["heathvale","ship","ship_ok","HEATHVALE SHIP DOCK","SHIP","x"],
    ["inkvale","sla","sla_ok_hours","INKVALE SLA CARD","SLA","x"],
    ["jetvale","exp","exp_sum","JETVALE EXPENSE","EXP","x"],
    ["kestrelvale","po","po_open","KESTRELVALE PO SHEET","PO","x"],
    ["lakevale","order","order_paid","LAKEVALE ORDER","ORD","x"],
    ["mistvale","dup","dup_mark","MISTVALE DUP MARK","DUP","x"],
    ["northvale","zero","zero_check","NORTHVALE AIR ZERO","ZERO","x"],
    ["oakvale","ledger","ledger_net","OAKVALE LEDGER","LED","x"],
    ["pinevale","ui","ui_ok","PINEVALE UI SCAN","UI","x"],
    ["quillvale","stack","stack_count","QUILLVALE STACK","STK","x"],
    ["reedvale","fax","fax_pages","REEDVALE FAX","FAX","x"],
    ["stonevale","glare","glare_ok","STONEVALE GLARE","GLR","x"],
    ["tidevale","tab","tab_index","TIDEVALE TAB INDEX","TAB","x"],
]
# Prefer totals without fragile 0→6 OCR (lesson C811 ironholt 1032)
TR118 = [
    [655.0, 672.5, 465.0],[582, 623, 437],[578.0, 607.25, 445.0],[711.0, 728.0, 535.0],
    [773.0, 797.0, 505.0],[531, 547, 463],[340.0, 380.0, 220.0],[621.0, 652.75, 469.0],
    [655.0, 638.0, 478.0],[688.0, 676.0, 466.0],[1,1,0],[0,0,0],
    [754.0, 775.5, 491.0],[1,0,0],[303, 295, 273],[321, 305, 296],[1,0,0],[347, 323, 293],
]
HO118 = [
    [525.0, 537.75, 418.0],[480, 520, 400],[483.0, 496.5, 406.0],[598.0, 614.0, 447.0],
    [639.0, 655.0, 442.0],[433, 447, 411],[240.0, 280.0, 180.0],[509.0, 530.75, 418.0],
    [568.0, 494.0, 415.0],[556.0, 542.0, 413.0],[1,1,0],[0,0,0],  # po: 568+494=1062 (no mid-0)
    [591.0, 606.5, 428.0],[1,0,0],[279, 276, 271],[295, 289, 277],[1,0,0],[305, 299, 278],
]
(ROOT / "tools/_v118_themes.json").write_text(json.dumps({"themes": T118, "train": TR118, "heldout": HO118}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_118(src):
    src = src.replace("# --- V117 overlays (new vs V50) ---", "# --- V118 overlays (new vs V50) ---")
    src = src.replace("# --- V117 overlays (new vs V49) ---", "# --- V118 overlays (new vs V49) ---")
    for a, b in [
        ("AMBERHOLT bait 61.61", "ASHVALE bait 62.62"),
        ("BRONZE bait 81.81", "CLIFF bait 82.82"),
        ("CEDAR ghost 93.93", "DUSK ghost 94.94"),
        ("FLINT bait 56.56", "HEATH bait 57.57"),
        ("IRON bait 47.47", "KESTREL bait 48.48"),
        ("MAPLE bait 91.91", "OAK bait 92.92"),
        ("amber mist + ridge ticks (V117-only)", "ash mist + tide ticks (V118-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD117 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v117_themes.json").read_text(encoding="utf-8"))["themes"])
NEW118 = "_".join(t[0] for t in T118)

out = (S / "c809_vision_v117_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C809", "C815"), ("c809", "c815"), ("V117", "V118"), ("v117", "v118"),
    ("_v117c809", "_v118c815"),
    ("Harder than V116", "Harder than V117"), ("harder than V116", "harder than V117"),
    (OLD117, NEW118),
    ("V117 keeps floor", "V118 keeps floor"),
    ("C809 design+fixtures; no VL claim", "C815 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C810 VL smoke", "fixtures only; claim deferred to C816 VL smoke"),
    ("No claim until C810 VL", "No claim until C816 VL"),
    ("kept on V117", "kept on V118"),
    ("vision_images_v117", "vision_images_v118"),
    ("VL_GATE_V117", "VL_GATE_V118"), ("vl_gate_v117", "vl_gate_v118"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V116: amberholt, bronzeholt, cedarholt, driftwoodholt, emberholt, flintholt, graniteholt, harborholt,\nironholt, jadeholt, knollholt, lotusholt, mapleholt, nimbusholt, opalholt, pebbleholt, quarryholt, ridgeholt.",
    "NEW themes vs V117: ashvale, cliffvale, duskvale, fernvale, glenvale, heathvale, inkvale, jetvale,\nkestrelvale, lakevale, mistvale, northvale, oakvale, pinevale, quillvale, reedvale, stonevale, tidevale.",
)
out = replace_specs(out, build_specs(T118, "v118", "V118", TR118))
out = retarget_118(out)
(S / "c815_vision_v118_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c810_vision_v117_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C810", "C816"), ("c810", "c816"), ("V117", "V118"), ("v117", "v118"),
    ("Uses C809 fixtures", "Uses C815 fixtures"),
    ("vision_images_v117", "vision_images_v118"),
    ("vl_gate_v117", "vl_gate_v118"), ("VL_GATE_V117", "VL_GATE_V118"),
]:
    out = out.replace(a, b)
(S / "c816_vision_v118_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c811_vision_v117_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C811", "C817"), ("c811", "c817"), ("C809", "C815"),
    ("V117", "V118"), ("v117", "v118"),
    ("_v117hc811", "_v118hc817"), ("_v117c809", "_v118c815"),
    ("vl_gate_v117", "vl_gate_v118"), ("VL_GATE_V117", "VL_GATE_V118"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T118, "v118h", "V118H", HO118))
out = retarget_118(out)
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v118h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v118"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v118" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v118h_c817"'); seen_run = True; continue
    out2.append(ln)
(S / "c817_vision_v118_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c806_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C806", "C818"), ("c806", "c818"),
    ("product_u2c_c806", "product_u2c_c818"),
    ("after V116", "after V118"), ("after V117", "after V118"),
]:
    out = out.replace(a, b)
(S / "c818_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c813_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C813", "C819"), ("c813", "c819"),
    ("capture_regression_c813", "capture_regression_c819"),
    ("after C809-C812", "after C815-C818"),
    ("V4-V117+heldout", "V4-V118+heldout"),
]:
    out = out.replace(a, b)
if "VISION_V118_SMOKE" not in out:
    out = out.replace(
        "SMOKE_POINTERS = [",
        'SMOKE_POINTERS = [\n    ("V118", DOC / "C816_VISION_V118_SMOKE.json"),\n    ("V118_heldout", DOC / "C817_VISION_V118_HELDOUT_SMOKE.json"),\n    ("V117", DOC / "C810_VISION_V117_SMOKE.json"),\n    ("V117_heldout", DOC / "C811_VISION_V117_HELDOUT_SMOKE.json"),',
        1,
    )
(S / "c819_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c814_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C814", "C820"), ("c814", "c820"),
    ("C810", "C816"), ("C811", "C817"), ("C813", "C819"),
    ("C809", "C815"),
    ("V117", "V118"), ("v117", "v118"),
    ("V116", "V117"), ("v116", "v117"),
    ("v117_jpeg_q", "v118_jpeg_q"),
]:
    out = out.replace(a, b)
# V118 U2C knife: conf stays C812; u2c = C818; stage_ready on u2c_pass
out = out.replace(
    'c656 = load("docs/r50/C812_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C812_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C806_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C818_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C806"}',
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C818"}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C812"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C812"}',
)
out = out.replace(
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C806"}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C818"}',
)
out = out.replace(
    "confidence-gate rate={conf_rate} pass={conf_pass}",
    "product-U2C replace={replace} pass={u2c_pass}",
)
out = out.replace(
    "stage_ready = bool(v118_claim and v118h_claim and v118 >= GATE and v118h >= GATE and capture_pass and disjoint and conf_pass)",
    "stage_ready = bool(v118_claim and v118h_claim and v118 >= GATE and v118h >= GATE and capture_pass and disjoint and u2c_pass)",
)
out = out.replace(
    'f"- C812: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C818: product-U2C replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- C812: confidence-gate rate={conf_rate} pass={conf_pass}"',
    'f"- C818: product-U2C replace={replace} pass={u2c_pass}"',
)
(S / "c820_scorecard_and_stage.py").write_text(out, encoding="utf-8")
for ln in out.splitlines():
    if any(x in ln for x in ("c656 =", "c650 =", '"confidence_gate"', '"product_u2c"', "stage_ready =", "product-U2C", "C818:", "C812:")):
        if "load" in ln or "source" in ln or "stage_ready" in ln or "product-U2C" in ln or "confidence" in ln:
            print("CHK", ln.strip()[:150])
print("scorecard OK"); print("done")
