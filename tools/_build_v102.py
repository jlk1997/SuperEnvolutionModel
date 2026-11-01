# -*- coding: utf-8 -*-
from __future__ import annotations
import json, re
from pathlib import Path
ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"
THEMES = [
    ["harborcreek","recv","paid_total","HARBORCREEK GRAIN RECV","RECV","x"],
    ["ivorygrove","wh","qty_sum","WH IVORYGROVE BIN","RECV","x"],
    ["jaspercreek","refund","refund_done","JASPERCREEK PATCH REFUND","DONE","x"],
    ["kelpgrove","tax","tax_base_paid","KELPGROVE TAX SLIP","TAX","x"],
    ["lanterncreek","pay","payroll_active","LANTERNCREEK PAYROLL","PAY","x"],
    ["maplegrove","ship","ship_ok","MAPLEGROVE SHIP DOCK","SHIP","x"],
    ["nethercreek","sla","sla_ok_hours","NETHERCREEK SLA CARD","SLA","x"],
    ["orchardgrove","exp","exp_sum","ORCHARDGROVE EXPENSE","EXP","x"],
    ["pebblecreek","po","po_open","PEBBLECREEK PO SHEET","PO","x"],
    ["quiltgrove","order","order_paid","QUILTGROVE ORDER","ORD","x"],
    ["rivercreek","dup","dup_mark","RIVERCREEK DUP MARK","DUP","x"],
    ["stonegrove","zero","zero_check","STONEGROVE AIR ZERO","ZERO","x"],
    ["timbercreek","ledger","ledger_net","TIMBERCREEK LEDGER","LED","x"],
    ["ultragrove","ui","ui_ok","ULTRAGROVE UI SCAN","UI","x"],
    ["valleycreek","stack","stack_count","VALLEYCREEK STACK","STK","x"],
    ["willowgrove","fax","fax_pages","WILLOWGROVE FAX","FAX","x"],
    ["yarncreek","glare","glare_ok","YARNCREEK GLARE","GLR","x"],
    ["zenithgrove","tab","tab_index","ZENITHGROVE TAB INDEX","TAB","x"],
]
# OCR-friendly ABC; SLA uses 340+380 style
TRAIN = [
    [492.0, 508.5, 301.0],
    [418, 458, 274],
    [415.0, 444.25, 281.0],
    [546.0, 564.0, 371.0],
    [609.0, 633.0, 341.0],
    [367, 383, 299],
    [340.0, 380.0, 220.0],
    [457.0, 488.75, 305.0],
    [491.0, 474.0, 314.0],
    [524.0, 512.0, 302.0],
    [1, 1, 0],
    [0, 0, 0],
    [590.0, 611.5, 327.0],
    [1, 0, 0],
    [191, 183, 161],
    [209, 193, 184],
    [1, 0, 0],
    [235, 211, 181],
]
HELDOUT = [
    [361.0, 373.75, 254.0],
    [316, 356, 236],
    [319.0, 332.5, 242.0],
    [434.0, 450.0, 283.0],
    [475.0, 491.0, 278.0],
    [269, 283, 247],
    [240.0, 280.0, 180.0],
    [345.0, 366.75, 254.0],
    [365.0, 353.0, 257.0],
    [392.0, 378.0, 249.0],
    [1, 1, 0],
    [0, 0, 0],
    [427.0, 442.5, 264.0],
    [1, 0, 0],
    [167, 164, 159],
    [183, 177, 165],
    [1, 0, 0],
    [193, 187, 166],
]
themes_path = ROOT / "tools/_v102_themes.json"
themes_path.write_text(json.dumps({"themes": THEMES, "train": TRAIN, "heldout": HELDOUT}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("themes", themes_path)

def lines_for_metric(name, kind_suf, metric, title, stamp, a, b, c, tag):
    if metric == "paid_total":
        expected, body = a + b, [f"a paid {a:.2f}", f"b paid {b:.2f}", f"c open {c:.2f}", f"TOTAL PAID TARGET {a+b:.2f}"]
    elif metric == "qty_sum":
        expected = float(a + b)
        body = [f"SKU1 qty {a} ok", f"SKU2 qty {c} hold", f"SKU3 qty {b} ok", f"qty_sum TARGET {a+b}"]
    elif metric == "refund_done":
        expected, body = a + b, [f"itemR1 {a:.2f} done", f"itemR2 {b:.2f} done", f"itemR3 {c:.2f} open", f"refund_done TARGET {a+b:.2f}"]
    elif metric == "tax_base_paid":
        expected, body = a + b, [f"base {a:.2f} paid", f"addon {b:.2f} paid", f"skip {c:.2f}", f"tax_base_paid TARGET {a+b:.2f}"]
    elif metric == "payroll_active":
        expected, body = a + b, [f"empA {a:.2f} active", f"empB {b:.2f} active", f"empC {c:.2f} leave", f"payroll_active TARGET {a+b:.2f}"]
    elif metric == "ship_ok":
        expected = float(a + b)
        body = [f"box1 {a} ok", f"box2 {b} ok", f"box3 {c} hold", f"ship_ok TARGET {a+b}"]
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
        expected = float(a + b)
        body = [f"p1 {a}", f"p2 {b}", f"p3 {c}", f"stack_count TARGET {a+b}"]
    elif metric == "fax_pages":
        expected = float(a + b)
        body = [f"pgA {a}", f"pgB {b}", f"pgC {c} drop", f"fax_pages TARGET {a+b}"]
    elif metric == "glare_ok":
        expected, body = 1.0, ["zone1 1 ok", "zone2 0", "zone3 0", "glare_ok TARGET 1"]
    elif metric == "tab_index":
        expected = float(a + b)
        body = [f"tabA {a}", f"tabB {b}", f"tabC {c}", f"tab_index TARGET {a+b}"]
    else:
        raise ValueError(metric)
    return expected, [f"{title} {tag}"] + body

def fmt_expected(x):
    return repr(float(x))

def build_specs(prefix, tag, abcs):
    lines = ["SPECS = ["]
    for i, (t, abc) in enumerate(zip(THEMES, abcs), 1):
        name, kind_suf, metric, title, stamp, _bk = t
        a, b, c = abc
        expected, body = lines_for_metric(name, kind_suf, metric, title, stamp, a, b, c, tag)
        fid = f"{prefix}_{i:02d}"
        kind = f"{name}_{kind_suf}"
        body_l = ",\n     ".join(repr(x) for x in body)
        lines.append(f'    ("{fid}", "{kind}", "{metric}", {fmt_expected(expected)},\n     [{body_l}],\n     {repr(name)}, "{stamp}"),')
    lines.append("]")
    return "\n".join(lines) + "\n"

def replace_specs(src, new_specs):
    return re.sub(r"SPECS = \[.*?\n\]\n", new_specs + "\n", src, count=1, flags=re.S)

def retarget_overlay(src):
    src = src.replace("# --- V101 overlays (new vs V50) ---", "# --- V102 overlays (new vs V50) ---")
    src = src.replace("# --- V101 overlays (new vs V49) ---", "# --- V102 overlays (new vs V49) ---")
    for a, b in [
        ("PINEHILL bait 45.45", "HARBORCREEK bait 46.46"),
        ("RUBY bait 65.65", "IVORY bait 66.66"),
        ("FERN ghost 95.95", "KELP ghost 96.96"),
        ("TEAL bait 40.40", "MAPLE bait 41.41"),
        ("SURF bait 31.31", "PEBBLE bait 32.32"),
        ("TWIG bait 75.75", "TIMBER bait 76.76"),
        ("dew drops + vine marks (V101-only)", "harbor mist + zenith ticks (V102-only)"),
    ]:
        src = src.replace(a, b)
    return src

THEME_STR = "_".join(t[0] for t in THEMES)
OLD_THEME = "pinehill_quartzhill_ravenhill_silverhill_thornhill_umberhill_vinehill_wavehill_xenoridge_yewhill_zinchill_aspenhill_bayhill_coralhill_dawnhill_emberhill_fernhill_granitehill"

out = (S / "c713_vision_v101_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C713", "C719"), ("c713", "c719"), ("V101", "V102"), ("v101", "v102"),
    ("_v101c713", "_v102c719"),
    ("Harder than V100", "Harder than V101"), ("harder than V100", "harder than V101"),
    (OLD_THEME, THEME_STR),
    ("V101 keeps floor", "V102 keeps floor"),
    ("C713 design+fixtures; no VL claim", "C719 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C714 VL smoke", "fixtures only; claim deferred to C720 VL smoke"),
    ("No claim until C714 VL", "No claim until C720 VL"),
    ("kept on V101", "kept on V102"),
    ("vision_images_v101", "vision_images_v102"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V100: pinehill, quartzhill, ravenhill, silverhill, thornhill, umberhill, vinehill, wavehill,\nxenoridge, yewhill, zinchill, aspenhill, bayhill, coralhill, dawnhill, emberhill, fernhill, granitehill.",
    "NEW themes vs V101: harborcreek, ivorygrove, jaspercreek, kelpgrove, lanterncreek, maplegrove, nethercreek, orchardgrove,\npebblecreek, quiltgrove, rivercreek, stonegrove, timbercreek, ultragrove, valleycreek, willowgrove, yarncreek, zenithgrove.",
)
# protocol path / claim keys
out = out.replace("VL_GATE_V101", "VL_GATE_V102")
out = out.replace("vl_gate_v101", "vl_gate_v102")
out = replace_specs(out, build_specs("v102", "V102", TRAIN))
out = retarget_overlay(out)
(S / "c719_vision_v102_design_and_batch.py").write_text(out, encoding="utf-8")
print("design", out.count("vision_images_v102"), out.count("C719"))

out = (S / "c714_vision_v101_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C714", "C720"), ("c714", "c720"), ("V101", "V102"), ("v101", "v102"),
    ("Uses C713 fixtures", "Uses C719 fixtures"),
    ("vision_images_v101", "vision_images_v102"),
    ("vl_gate_v101", "vl_gate_v102"),
    ("VL_GATE_V101", "VL_GATE_V102"),
]:
    out = out.replace(a, b)
(S / "c720_vision_v102_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c715_vision_v101_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C715", "C721"), ("c715", "c721"), ("C713", "C719"),
    ("V101", "V102"), ("v101", "v102"),
    ("_v101hc715", "_v102hc721"), ("_v101c713", "_v102c719"),
    ("vl_gate_v101", "vl_gate_v102"),
    ("VL_GATE_V101", "VL_GATE_V102"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs("v102h", "V102H", HELDOUT))
out = retarget_overlay(out)
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v102h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v102"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v102" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v102h_c721"'); seen_run = True; continue
    out2.append(ln)
(S / "c721_vision_v102_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# U2C knife from C710
out = (S / "c710_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C710", "C722"), ("c710", "c722"),
    ("product_u2c_c710", "product_u2c_c722"),
    ("after V99", "after V102"), ("after V100", "after V102"),
]:
    out = out.replace(a, b)
(S / "c722_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c717_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C717", "C723"), ("c717", "c723"),
    ("capture_regression_c717", "capture_regression_c723"),
    ("after C713-C716", "after C719-C722"),
    ("V4-V101+heldout", "V4-V102+heldout"),
]:
    out = out.replace(a, b)
if "VISION_V102_SMOKE" not in out:
    out = out.replace(
        "SMOKE_POINTERS = [",
        'SMOKE_POINTERS = [\n    ("V102", DOC / "C720_VISION_V102_SMOKE.json"),\n    ("V102_heldout", DOC / "C721_VISION_V102_HELDOUT_SMOKE.json"),\n    ("V101", DOC / "C714_VISION_V101_SMOKE.json"),\n    ("V101_heldout", DOC / "C715_VISION_V101_HELDOUT_SMOKE.json"),',
        1,
    )
(S / "c723_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

# scorecard: clone C718 then retarget to V102 + U2C knife
out = (S / "c718_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C718", "C724"), ("c718", "c724"),
    ("C714", "C720"), ("C715", "C721"), ("C716", "C722"), ("C717", "C723"),
    ("C713", "C719"),
    ("V101", "V102"), ("v101", "v102"),
    ("V100", "V101"), ("v100", "v101"),
    ("C710", "C722"),
    ("v101_jpeg_q", "v102_jpeg_q"),
]:
    out = out.replace(a, b)
# fix: confidence_gate from prior; product_u2c from C722
out = out.replace(
    'c656 = load("docs/r50/C722_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C716_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C722_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C722_PRODUCT_U2C_COST.json") or {}',
)
# STAGE text: knife is U2C
out = out.replace("confidence-gate stretch", "product-U2C")
out = out.replace('"source": "C716"', '"source": "C716"')  # conf stays prior
out = out.replace(
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C722"}',
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C722"}',
)
# stage_ready should require u2c pass for this slice
out = out.replace(
    "stage_ready = bool(v102_claim and v102h_claim and v102 >= GATE and v102h >= GATE and capture_pass and disjoint and conf_pass)",
    "stage_ready = bool(v102_claim and v102h_claim and v102 >= GATE and v102h >= GATE and capture_pass and disjoint and bool((u2c or {}).get('pass', conf_pass)))",
)
(S / "c724_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard OK")
print("done")
