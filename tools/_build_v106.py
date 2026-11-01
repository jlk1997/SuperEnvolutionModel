# -*- coding: utf-8 -*-
from __future__ import annotations
import json, re
from pathlib import Path
ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"
THEMES = [
    ["cedarfall","recv","paid_total","CEDARFALL GRAIN RECV","RECV","x"],
    ["duskfall","wh","qty_sum","WH DUSKFALL BIN","RECV","x"],
    ["emberfall","refund","refund_done","EMBERFALL PATCH REFUND","DONE","x"],
    ["frostfall","tax","tax_base_paid","FROSTFALL TAX SLIP","TAX","x"],
    ["glenfall","pay","payroll_active","GLENFALL PAYROLL","PAY","x"],
    ["hazelfall","ship","ship_ok","HAZELFALL SHIP DOCK","SHIP","x"],
    ["ironfall","sla","sla_ok_hours","IRONFALL SLA CARD","SLA","x"],
    ["jadefall","exp","exp_sum","JADEFALL EXPENSE","EXP","x"],
    ["knollfall","po","po_open","KNOLLFALL PO SHEET","PO","x"],
    ["lotusfall","order","order_paid","LOTUSFALL ORDER","ORD","x"],
    ["meadowfall","dup","dup_mark","MEADOWFALL DUP MARK","DUP","x"],
    ["northfall","zero","zero_check","NORTHFALL AIR ZERO","ZERO","x"],
    ["opalfall","ledger","ledger_net","OPALFALL LEDGER","LED","x"],
    ["pearlfall","ui","ui_ok","PEARLFALL UI SCAN","UI","x"],
    ["quartzfall","stack","stack_count","QUARTZFALL STACK","STK","x"],
    ["ravenfall","fax","fax_pages","RAVENFALL FAX","FAX","x"],
    ["stonefall","glare","glare_ok","STONEFALL GLARE","GLR","x"],
    ["timberfall","tab","tab_index","TIMBERFALL TAB INDEX","TAB","x"],
]
TRAIN = [
    [536.0, 552.5, 345.0],[462, 502, 318],[459.0, 488.25, 325.0],[590.0, 608.0, 415.0],
    [653.0, 677.0, 385.0],[411, 427, 343],[340.0, 380.0, 220.0],[501.0, 532.75, 349.0],
    [535.0, 518.0, 358.0],[568.0, 556.0, 346.0],[1,1,0],[0,0,0],
    [634.0, 655.5, 371.0],[1,0,0],[219, 211, 189],[237, 221, 212],[1,0,0],[263, 239, 209],
]
HELDOUT = [
    [405.0, 417.75, 298.0],[360, 400, 280],[363.0, 376.5, 286.0],[478.0, 494.0, 327.0],
    [519.0, 535.0, 322.0],[313, 327, 291],[240.0, 280.0, 180.0],[389.0, 410.75, 298.0],
    [409.0, 397.0, 301.0],[436.0, 422.0, 293.0],[1,1,0],[0,0,0],
    [471.0, 486.5, 308.0],[1,0,0],[195, 192, 187],[211, 205, 193],[1,0,0],[221, 215, 194],
]
(ROOT / "tools/_v106_themes.json").write_text(json.dumps({"themes": THEMES, "train": TRAIN, "heldout": HELDOUT}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

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

def build_specs(prefix, tag, abcs):
    lines = ["SPECS = ["]
    for i, (t, abc) in enumerate(zip(THEMES, abcs), 1):
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

def retarget_overlay(src):
    src = src.replace("# --- V105 overlays (new vs V50) ---", "# --- V106 overlays (new vs V50) ---")
    src = src.replace("# --- V105 overlays (new vs V49) ---", "# --- V106 overlays (new vs V49) ---")
    for a, b in [
        ("KELPCREEK bait 49.49", "CEDARFALL bait 50.50"),
        ("LUNAR bait 69.69", "DUSK bait 70.70"),
        ("MARLIN ghost 99.99", "EMBER ghost 91.91"),
        ("PRISM bait 44.44", "HAZEL bait 45.45"),
        ("SILT bait 35.35", "KNOLL bait 36.36"),
        ("WELD bait 79.79", "OPAL bait 80.80"),
        ("kelp mist + bloom ticks (V105-only)", "cedar mist + timber ticks (V106-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD = "kelpcreek_lunargrove_marlincreek_nimbusgrove_ottercreek_prismgrove_quarrycreek_reefgrove_siltcreek_torngrove_uplandcreek_valegrove_weldcreek_xenongrove_yelkcreek_zestgrove_archcreek_bloomgrove"
NEW = "_".join(t[0] for t in THEMES)

out = (S / "c737_vision_v105_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C737", "C743"), ("c737", "c743"), ("V105", "V106"), ("v105", "v106"),
    ("_v105c737", "_v106c743"),
    ("Harder than V104", "Harder than V105"), ("harder than V104", "harder than V105"),
    (OLD, NEW),
    ("V105 keeps floor", "V106 keeps floor"),
    ("C737 design+fixtures; no VL claim", "C743 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C738 VL smoke", "fixtures only; claim deferred to C744 VL smoke"),
    ("No claim until C738 VL", "No claim until C744 VL"),
    ("kept on V105", "kept on V106"),
    ("vision_images_v105", "vision_images_v106"),
    ("VL_GATE_V105", "VL_GATE_V106"),
    ("vl_gate_v105", "vl_gate_v106"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V104: kelpcreek, lunargrove, marlincreek, nimbusgrove, ottercreek, prismgrove, quarrycreek, reefgrove,\nsiltcreek, torngrove, uplandcreek, valegrove, weldcreek, xenongrove, yelkcreek, zestgrove, archcreek, bloomgrove.",
    "NEW themes vs V105: cedarfall, duskfall, emberfall, frostfall, glenfall, hazelfall, ironfall, jadefall,\nknollfall, lotusfall, meadowfall, northfall, opalfall, pearlfall, quartzfall, ravenfall, stonefall, timberfall.",
)
out = replace_specs(out, build_specs("v106", "V106", TRAIN))
out = retarget_overlay(out)
(S / "c743_vision_v106_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c738_vision_v105_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C738", "C744"), ("c738", "c744"), ("V105", "V106"), ("v105", "v106"),
    ("Uses C737 fixtures", "Uses C743 fixtures"),
    ("vision_images_v105", "vision_images_v106"),
    ("vl_gate_v105", "vl_gate_v106"), ("VL_GATE_V105", "VL_GATE_V106"),
]:
    out = out.replace(a, b)
(S / "c744_vision_v106_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c739_vision_v105_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C739", "C745"), ("c739", "c745"), ("C737", "C743"),
    ("V105", "V106"), ("v105", "v106"),
    ("_v105hc739", "_v106hc745"), ("_v105c737", "_v106c743"),
    ("vl_gate_v105", "vl_gate_v106"), ("VL_GATE_V105", "VL_GATE_V106"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs("v106h", "V106H", HELDOUT))
out = retarget_overlay(out)
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v106h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v106"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v106" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v106h_c745"'); seen_run = True; continue
    out2.append(ln)
(S / "c745_vision_v106_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c734_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C734", "C746"), ("c734", "c746"),
    ("product_u2c_c734", "product_u2c_c746"),
    ("after V104", "after V106"), ("after V105", "after V106"),
]:
    out = out.replace(a, b)
(S / "c746_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c741_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C741", "C747"), ("c741", "c747"),
    ("capture_regression_c741", "capture_regression_c747"),
    ("after C737-C740", "after C743-C746"),
    ("V4-V105+heldout", "V4-V106+heldout"),
]:
    out = out.replace(a, b)
if "VISION_V106_SMOKE" not in out:
    out = out.replace(
        "SMOKE_POINTERS = [",
        'SMOKE_POINTERS = [\n    ("V106", DOC / "C744_VISION_V106_SMOKE.json"),\n    ("V106_heldout", DOC / "C745_VISION_V106_HELDOUT_SMOKE.json"),\n    ("V105", DOC / "C738_VISION_V105_SMOKE.json"),\n    ("V105_heldout", DOC / "C739_VISION_V105_HELDOUT_SMOKE.json"),',
        1,
    )
(S / "c747_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c742_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C742", "C748"), ("c742", "c748"),
    ("C738", "C744"), ("C739", "C745"), ("C740", "C746"), ("C741", "C747"),
    ("C737", "C743"),
    ("V105", "V106"), ("v105", "v106"),
    ("V104", "V105"), ("v104", "v105"),
    ("v105_jpeg_q", "v106_jpeg_q"),
]:
    out = out.replace(a, b)
# conf stays C740; u2c from C746
out = out.replace(
    'c656 = load("docs/r50/C746_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C740_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C734_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C746_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C734"}',
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C746"}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C740"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C740"}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C746"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C740"}',
)
out = out.replace(
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C734"}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C746"}',
)
out = out.replace(
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C746"}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C746"}',
)
out = out.replace(
    "confidence-gate rate={conf_rate} pass={conf_pass}",
    "product-U2C replace={replace} pass={u2c_pass}",
)
out = out.replace(
    "stage_ready = bool(v106_claim and v106h_claim and v106 >= GATE and v106h >= GATE and capture_pass and disjoint and conf_pass)",
    "stage_ready = bool(v106_claim and v106h_claim and v106 >= GATE and v106h >= GATE and capture_pass and disjoint and u2c_pass)",
)
if "u2c_pass =" not in out:
    out = out.replace(
        'replace = float(u2c.get("replace_ratio") or 4.07)',
        'replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))',
    )
(S / "c748_scorecard_and_stage.py").write_text(out, encoding="utf-8")
for ln in out.splitlines():
    if any(x in ln for x in ("c656 =", "c650 =", '"confidence_gate"', '"product_u2c"', "stage_ready =", "C746:")):
        if "load" in ln or "source" in ln or "stage_ready" in ln or "product-U2C" in ln or "confidence" in ln:
            print("CHK", ln.strip()[:130])
print("scorecard OK"); print("done")
