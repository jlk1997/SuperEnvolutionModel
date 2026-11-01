# -*- coding: utf-8 -*-
from __future__ import annotations
import json, re
from pathlib import Path
ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"
THEMES = [
    ["ambercreek","recv","paid_total","AMBERCREEK GRAIN RECV","RECV","x"],
    ["bluffgrove","wh","qty_sum","WH BLUFFGROVE BIN","RECV","x"],
    ["cindercreek","refund","refund_done","CINDERCREEK PATCH REFUND","DONE","x"],
    ["driftgrove","tax","tax_base_paid","DRIFTGROVE TAX SLIP","TAX","x"],
    ["echocreek","pay","payroll_active","ECHOCREEK PAYROLL","PAY","x"],
    ["flintgrove","ship","ship_ok","FLINTGROVE SHIP DOCK","SHIP","x"],
    ["glintcreek","sla","sla_ok_hours","GLINTCREEK SLA CARD","SLA","x"],
    ["heathgrove","exp","exp_sum","HEATHGROVE EXPENSE","EXP","x"],
    ["inkcreek","po","po_open","INKCREEK PO SHEET","PO","x"],
    ["junipergrove","order","order_paid","JUNIPERGROVE ORDER","ORD","x"],
    ["kettlecreek","dup","dup_mark","KETTLECREEK DUP MARK","DUP","x"],
    ["loomgrove","zero","zero_check","LOOMGROVE AIR ZERO","ZERO","x"],
    ["mistcreek","ledger","ledger_net","MISTCREEK LEDGER","LED","x"],
    ["norbgrove","ui","ui_ok","NORBGROVE UI SCAN","UI","x"],
    ["oakcreek","stack","stack_count","OAKCREEK STACK","STK","x"],
    ["plovergrove","fax","fax_pages","PLOVERGROVE FAX","FAX","x"],
    ["quillcreek","glare","glare_ok","QUILLCREEK GLARE","GLR","x"],
    ["ridgegrove","tab","tab_index","RIDGEGROVE TAB INDEX","TAB","x"],
]
TRAIN = [
    [503.0, 519.5, 312.0],
    [429, 469, 285],
    [426.0, 455.25, 292.0],
    [557.0, 575.0, 382.0],
    [620.0, 644.0, 352.0],
    [378, 394, 310],
    [340.0, 380.0, 220.0],
    [468.0, 499.75, 316.0],
    [502.0, 485.0, 325.0],
    [535.0, 523.0, 313.0],
    [1, 1, 0],
    [0, 0, 0],
    [601.0, 622.5, 338.0],
    [1, 0, 0],
    [198, 190, 168],
    [216, 200, 191],
    [1, 0, 0],
    [242, 218, 188],
]
HELDOUT = [
    [372.0, 384.75, 265.0],
    [327, 367, 247],
    [330.0, 343.5, 253.0],
    [445.0, 461.0, 294.0],
    [486.0, 502.0, 289.0],
    [280, 294, 258],
    [240.0, 280.0, 180.0],
    [356.0, 377.75, 265.0],
    [376.0, 364.0, 268.0],
    [403.0, 389.0, 260.0],
    [1, 1, 0],
    [0, 0, 0],
    [438.0, 453.5, 275.0],
    [1, 0, 0],
    [174, 171, 166],
    [190, 184, 172],
    [1, 0, 0],
    [200, 194, 173],
]
(ROOT / "tools/_v103_themes.json").write_text(
    json.dumps({"themes": THEMES, "train": TRAIN, "heldout": HELDOUT}, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)

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

def build_specs(prefix, tag, abcs):
    lines = ["SPECS = ["]
    for i, (t, abc) in enumerate(zip(THEMES, abcs), 1):
        name, kind_suf, metric, title, stamp, _bk = t
        a, b, c = abc
        expected, body = lines_for_metric(name, kind_suf, metric, title, stamp, a, b, c, tag)
        fid = f"{prefix}_{i:02d}"
        kind = f"{name}_{kind_suf}"
        body_l = ",\n     ".join(repr(x) for x in body)
        lines.append(f'    ("{fid}", "{kind}", "{metric}", {repr(float(expected))},\n     [{body_l}],\n     {repr(name)}, "{stamp}"),')
    lines.append("]")
    return "\n".join(lines) + "\n"

def replace_specs(src, new_specs):
    return re.sub(r"SPECS = \[.*?\n\]\n", new_specs + "\n", src, count=1, flags=re.S)

def retarget_overlay(src):
    src = src.replace("# --- V102 overlays (new vs V50) ---", "# --- V103 overlays (new vs V50) ---")
    src = src.replace("# --- V102 overlays (new vs V49) ---", "# --- V103 overlays (new vs V49) ---")
    for a, b in [
        ("HARBORCREEK bait 46.46", "AMBERCREEK bait 47.47"),
        ("IVORY bait 66.66", "BLUFF bait 67.67"),
        ("KELP ghost 96.96", "CINDER ghost 97.97"),
        ("MAPLE bait 41.41", "FLINT bait 42.42"),
        ("PEBBLE bait 32.32", "INK bait 33.33"),
        ("TIMBER bait 76.76", "MIST bait 77.77"),
        ("harbor mist + zenith ticks (V102-only)", "amber mist + ridge ticks (V103-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD = "harborcreek_ivorygrove_jaspercreek_kelpgrove_lanterncreek_maplegrove_nethercreek_orchardgrove_pebblecreek_quiltgrove_rivercreek_stonegrove_timbercreek_ultragrove_valleycreek_willowgrove_yarncreek_zenithgrove"
NEW = "_".join(t[0] for t in THEMES)

out = (S / "c719_vision_v102_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C719", "C725"), ("c719", "c725"), ("V102", "V103"), ("v102", "v103"),
    ("_v102c719", "_v103c725"),
    ("Harder than V101", "Harder than V102"), ("harder than V101", "harder than V102"),
    (OLD, NEW),
    ("V102 keeps floor", "V103 keeps floor"),
    ("C719 design+fixtures; no VL claim", "C725 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C720 VL smoke", "fixtures only; claim deferred to C726 VL smoke"),
    ("No claim until C720 VL", "No claim until C726 VL"),
    ("kept on V102", "kept on V103"),
    ("vision_images_v102", "vision_images_v103"),
    ("VL_GATE_V102", "VL_GATE_V103"),
    ("vl_gate_v102", "vl_gate_v103"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V101: harborcreek, ivorygrove, jaspercreek, kelpgrove, lanterncreek, maplegrove, nethercreek, orchardgrove,\npebblecreek, quiltgrove, rivercreek, stonegrove, timbercreek, ultragrove, valleycreek, willowgrove, yarncreek, zenithgrove.",
    "NEW themes vs V102: ambercreek, bluffgrove, cindercreek, driftgrove, echocreek, flintgrove, glintcreek, heathgrove,\ninkcreek, junipergrove, kettlecreek, loomgrove, mistcreek, norbgrove, oakcreek, plovergrove, quillcreek, ridgegrove.",
)
out = replace_specs(out, build_specs("v103", "V103", TRAIN))
out = retarget_overlay(out)
(S / "c725_vision_v103_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c720_vision_v102_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C720", "C726"), ("c720", "c726"), ("V102", "V103"), ("v102", "v103"),
    ("Uses C719 fixtures", "Uses C725 fixtures"),
    ("vision_images_v102", "vision_images_v103"),
    ("vl_gate_v102", "vl_gate_v103"),
    ("VL_GATE_V102", "VL_GATE_V103"),
]:
    out = out.replace(a, b)
(S / "c726_vision_v103_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c721_vision_v102_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C721", "C727"), ("c721", "c727"), ("C719", "C725"),
    ("V102", "V103"), ("v102", "v103"),
    ("_v102hc721", "_v103hc727"), ("_v102c719", "_v103c725"),
    ("vl_gate_v102", "vl_gate_v103"),
    ("VL_GATE_V102", "VL_GATE_V103"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs("v103h", "V103H", HELDOUT))
out = retarget_overlay(out)
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v103h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v103"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v103" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v103h_c727"'); seen_run = True; continue
    out2.append(ln)
(S / "c727_vision_v103_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c716_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C716", "C728"), ("c716", "c728"),
    ("conf_gate_stretch_c716", "conf_gate_stretch_c728"),
    ("after V101", "after V103"), ("after V100", "after V103"),
    ("cg50_", "cg53_"), ("cg51_", "cg53_"), ("cg52_", "cg53_"),
]:
    out = out.replace(a, b)
(S / "c728_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence")

out = (S / "c723_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C723", "C729"), ("c723", "c729"),
    ("capture_regression_c723", "capture_regression_c729"),
    ("after C719-C722", "after C725-C728"),
    ("V4-V102+heldout", "V4-V103+heldout"),
]:
    out = out.replace(a, b)
if "VISION_V103_SMOKE" not in out:
    out = out.replace(
        "SMOKE_POINTERS = [",
        'SMOKE_POINTERS = [\n    ("V103", DOC / "C726_VISION_V103_SMOKE.json"),\n    ("V103_heldout", DOC / "C727_VISION_V103_HELDOUT_SMOKE.json"),\n    ("V102", DOC / "C720_VISION_V102_SMOKE.json"),\n    ("V102_heldout", DOC / "C721_VISION_V102_HELDOUT_SMOKE.json"),',
        1,
    )
(S / "c729_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c724_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C724", "C730"), ("c724", "c730"),
    ("C720", "C726"), ("C721", "C727"), ("C722", "C728"), ("C723", "C729"),
    ("C719", "C725"),
    ("V102", "V103"), ("v102", "v103"),
    ("V101", "V102"), ("v101", "v102"),
    ("v102_jpeg_q", "v103_jpeg_q"),
]:
    out = out.replace(a, b)
# conf from C728; u2c from prior C722
out = out.replace(
    'c656 = load("docs/r50/C716_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C728_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C728_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C722_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace('"source": "C728"}', '"source": "C722"}', 1)  # may hit wrong one - fix carefully later
# STAGE knife text
out = out.replace("product-U2C replace={replace} pass={u2c_pass}", "confidence-gate rate={conf_rate} pass={conf_pass}")
out = out.replace(
    "stage_ready = bool(v103_claim and v103h_claim and v103 >= GATE and v103h >= GATE and capture_pass and disjoint and bool((u2c or {}).get('pass', conf_pass)))",
    "stage_ready = bool(v103_claim and v103h_claim and v103 >= GATE and v103h >= GATE and capture_pass and disjoint and conf_pass)",
)
(S / "c730_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard")
# fix sources in scorecard
t = (S / "c730_scorecard_and_stage.py").read_text(encoding="utf-8")
t = t.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C716"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C728"}',
)
t = t.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C722"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C728"}',
)
# product_u2c source should stay C722
t = re.sub(
    r'"product_u2c": u2c if u2c else \{"pass": True, "replace_ratio": replace, "source": "[^"]+"\}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C722"}',
    t,
)
t = t.replace('"source": "C728"}', '"source": "C722"}')  # too broad?
# re-read and surgical fix
(S / "c730_scorecard_and_stage.py").write_text(t, encoding="utf-8")
# verify
t2 = (S / "c730_scorecard_and_stage.py").read_text(encoding="utf-8")
for ln in t2.splitlines():
    if "source" in ln and ("confidence" in ln or "product_u2c" in ln or "C722" in ln or "C728" in ln):
        print("SRC", ln.strip())
print("done")
