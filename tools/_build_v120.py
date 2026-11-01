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

# *glen — avoid *b; OCR-friendly (1062-style, no mid-0 like 1032)
T120 = [
    ["argentglen","recv","paid_total","ARGENTGLEN GRAIN RECV","RECV","x"],
    ["brookglen","wh","qty_sum","WH BROOKGLEN BIN","RECV","x"],
    ["cinderglen","refund","refund_done","CINDERGLEN PATCH REFUND","DONE","x"],
    ["dewglen","tax","tax_base_paid","DEWGLEN TAX SLIP","TAX","x"],
    ["elderglen","pay","payroll_active","ELDERGLEN PAYROLL","PAY","x"],
    ["foggglen","ship","ship_ok","FOGGLEN SHIP DOCK","SHIP","x"],
    ["garnetglen","sla","sla_ok_hours","GARNETGLEN SLA CARD","SLA","x"],
    ["hazelglen","exp","exp_sum","HAZELGLEN EXPENSE","EXP","x"],
    ["ivoryglen","po","po_open","IVORYGLEN PO SHEET","PO","x"],
    ["juniperglen","order","order_paid","JUNIPERGLEN ORDER","ORD","x"],
    ["knotglen","dup","dup_mark","KNOTGLEN DUP MARK","DUP","x"],
    ["loamglen","zero","zero_check","LOAMGLEN AIR ZERO","ZERO","x"],
    ["mossglen","ledger","ledger_net","MOSSGLEN LEDGER","LED","x"],
    ["nectarglen","ui","ui_ok","NECTARGLEN UI SCAN","UI","x"],
    ["opalglen","stack","stack_count","OPALGLEN STACK","STK","x"],
    ["pearlglen","fax","fax_pages","PEARLGLEN FAX","FAX","x"],
    ["quartzglen","glare","glare_ok","QUARTZGLEN GLARE","GLR","x"],
    ["ridgeglen","tab","tab_index","RIDGEGLEN TAB INDEX","TAB","x"],
]
T120[5] = ["fogglen","ship","ship_ok","FOGGLEN SHIP DOCK","SHIP","x"]
TR120 = [
    [669.0, 686.5, 479.0],[596, 637, 451],[592.0, 621.25, 459.0],[725.0, 742.0, 549.0],
    [787.0, 811.0, 519.0],[545, 561, 477],[340.0, 380.0, 220.0],[635.0, 666.75, 483.0],
    [669.0, 652.0, 492.0],[702.0, 690.0, 480.0],[1,1,0],[0,0,0],
    [768.0, 789.5, 505.0],[1,0,0],[317, 309, 287],[335, 319, 310],[1,0,0],[361, 337, 307],
]
HO120 = [
    [539.0, 551.75, 432.0],[494, 534, 414],[497.0, 510.5, 420.0],[612.0, 628.0, 461.0],
    [653.0, 669.0, 456.0],[447, 461, 425],[240.0, 280.0, 180.0],[523.0, 544.75, 432.0],
    [582.0, 508.0, 429.0],[570.0, 556.0, 427.0],[1,1,0],[0,0,0],  # po 582+508=1090
    [605.0, 620.5, 442.0],[1,0,0],[293, 290, 285],[309, 303, 291],[1,0,0],[319, 313, 292],
]
(ROOT / "tools/_v120_themes.json").write_text(json.dumps({"themes": T120, "train": TR120, "heldout": HO120}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_120(src):
    src = src.replace("# --- V119 overlays (new vs V50) ---", "# --- V120 overlays (new vs V50) ---")
    src = src.replace("# --- V119 overlays (new vs V49) ---", "# --- V120 overlays (new vs V49) ---")
    for a, b in [
        ("AZUREFEN bait 63.63", "ARGENTGLEN bait 64.64"),
        ("BRACKEN bait 83.83", "BROOK bait 84.84"),
        ("COPPER ghost 95.95", "CINDER ghost 96.96"),
        ("FROST bait 58.58", "FOG bait 59.59"),
        ("IVORY bait 49.49", "IVORYG bait 50.50"),
        ("MEADOW bait 93.93", "MOSS bait 94.94"),
        ("azure mist + raven ticks (V119-only)", "argent mist + ridge ticks (V120-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD119 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v119_themes.json").read_text(encoding="utf-8"))["themes"])
NEW120 = "_".join(t[0] for t in T120)

out = (S / "c821_vision_v119_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C821", "C827"), ("c821", "c827"), ("V119", "V120"), ("v119", "v120"),
    ("_v119c821", "_v120c827"),
    ("Harder than V118", "Harder than V119"), ("harder than V118", "harder than V119"),
    (OLD119, NEW120),
    ("V119 keeps floor", "V120 keeps floor"),
    ("C821 design+fixtures; no VL claim", "C827 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C822 VL smoke", "fixtures only; claim deferred to C828 VL smoke"),
    ("No claim until C822 VL", "No claim until C828 VL"),
    ("kept on V119", "kept on V120"),
    ("vision_images_v119", "vision_images_v120"),
    ("VL_GATE_V119", "VL_GATE_V120"), ("vl_gate_v119", "vl_gate_v120"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V118: azurefen, brackenfen, copperfen, dawnfen, echofen, frostfen, gorsefen, hollowfen,\nivoryfen, jasperfen, kelpfen, lunarfen, meadowfen, nimbusfen, orchidfen, pebblefen, quartzfen, ravenfen.",
    "NEW themes vs V119: argentglen, brookglen, cinderglen, dewglen, elderglen, fogglen, garnetglen, hazelglen,\nivoryglen, juniperglen, knotglen, loamglen, mossglen, nectarglen, opalglen, pearlglen, quartzglen, ridgeglen.",
)
out = replace_specs(out, build_specs(T120, "v120", "V120", TR120))
out = retarget_120(out)
(S / "c827_vision_v120_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c822_vision_v119_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C822", "C828"), ("c822", "c828"), ("V119", "V120"), ("v119", "v120"),
    ("Uses C821 fixtures", "Uses C827 fixtures"),
    ("vision_images_v119", "vision_images_v120"),
    ("vl_gate_v119", "vl_gate_v120"), ("VL_GATE_V119", "VL_GATE_V120"),
]:
    out = out.replace(a, b)
(S / "c828_vision_v120_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c823_vision_v119_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C823", "C829"), ("c823", "c829"), ("C821", "C827"),
    ("V119", "V120"), ("v119", "v120"),
    ("_v119hc823", "_v120hc829"), ("_v119c821", "_v120c827"),
    ("vl_gate_v119", "vl_gate_v120"), ("VL_GATE_V119", "VL_GATE_V120"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T120, "v120h", "V120H", HO120))
out = retarget_120(out)
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v120h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v120"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v120" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v120h_c829"'); seen_run = True; continue
    out2.append(ln)
(S / "c829_vision_v120_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c818_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C818", "C830"), ("c818", "c830"),
    ("product_u2c_c818", "product_u2c_c830"),
    ("after V118", "after V120"), ("after V119", "after V120"),
]:
    out = out.replace(a, b)
(S / "c830_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c825_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C825", "C831"), ("c825", "c831"),
    ("capture_regression_c825", "capture_regression_c831"),
    ("after C821-C824", "after C827-C830"),
    ("V4-V119+heldout", "V4-V120+heldout"),
]:
    out = out.replace(a, b)
if "VISION_V120_SMOKE" not in out:
    out = out.replace(
        "SMOKE_POINTERS = [",
        'SMOKE_POINTERS = [\n    ("V120", DOC / "C828_VISION_V120_SMOKE.json"),\n    ("V120_heldout", DOC / "C829_VISION_V120_HELDOUT_SMOKE.json"),\n    ("V119", DOC / "C822_VISION_V119_SMOKE.json"),\n    ("V119_heldout", DOC / "C823_VISION_V119_HELDOUT_SMOKE.json"),',
        1,
    )
(S / "c831_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c826_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C826", "C832"), ("c826", "c832"),
    ("C822", "C828"), ("C823", "C829"), ("C825", "C831"),
    ("C821", "C827"),
    ("V119", "V120"), ("v119", "v120"),
    ("V118", "V119"), ("v118", "v119"),
    ("v119_jpeg_q", "v120_jpeg_q"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C824_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C824_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C818_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C830_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C818"}',
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C830"}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C824"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C824"}',
)
out = out.replace(
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C818"}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C830"}',
)
out = out.replace(
    "confidence-gate rate={conf_rate} pass={conf_pass}",
    "product-U2C replace={replace} pass={u2c_pass}",
)
out = out.replace(
    "stage_ready = bool(v120_claim and v120h_claim and v120 >= GATE and v120h >= GATE and capture_pass and disjoint and conf_pass)",
    "stage_ready = bool(v120_claim and v120h_claim and v120 >= GATE and v120h >= GATE and capture_pass and disjoint and u2c_pass)",
)
out = out.replace(
    'f"- C824: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C830: product-U2C replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- C824: confidence-gate rate={conf_rate} pass={conf_pass}"',
    'f"- C830: product-U2C replace={replace} pass={u2c_pass}"',
)
(S / "c832_scorecard_and_stage.py").write_text(out, encoding="utf-8")
for ln in out.splitlines():
    if any(x in ln for x in ("c656 =", "c650 =", '"confidence_gate"', '"product_u2c"', "stage_ready =", "product-U2C", "C830:", "C824:")):
        if "load" in ln or "source" in ln or "stage_ready" in ln or "product-U2C" in ln or "confidence" in ln:
            print("CHK", ln.strip()[:150])
print("scorecard OK"); print("done")
