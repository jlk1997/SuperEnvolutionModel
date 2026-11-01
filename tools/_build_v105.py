# -*- coding: utf-8 -*-
from __future__ import annotations
import json, re
from pathlib import Path
ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"
THEMES = [
    ["kelpcreek","recv","paid_total","KELPCREEK GRAIN RECV","RECV","x"],
    ["lunargrove","wh","qty_sum","WH LUNARGROVE BIN","RECV","x"],
    ["marlincreek","refund","refund_done","MARLINCREEK PATCH REFUND","DONE","x"],
    ["nimbusgrove","tax","tax_base_paid","NIMBUSGROVE TAX SLIP","TAX","x"],
    ["ottercreek","pay","payroll_active","OTTERCREEK PAYROLL","PAY","x"],
    ["prismgrove","ship","ship_ok","PRISMGROVE SHIP DOCK","SHIP","x"],
    ["quarrycreek","sla","sla_ok_hours","QUARRYCREEK SLA CARD","SLA","x"],
    ["reefgrove","exp","exp_sum","REEFGROVE EXPENSE","EXP","x"],
    ["siltcreek","po","po_open","SILTCREEK PO SHEET","PO","x"],
    ["torngrove","order","order_paid","TORNGROVE ORDER","ORD","x"],
    ["uplandcreek","dup","dup_mark","UPLANDCREEK DUP MARK","DUP","x"],
    ["vale grove".replace(" ",""),"zero","zero_check","VALEGROVE AIR ZERO","ZERO","x"],
    ["weldcreek","ledger","ledger_net","WELDCREEK LEDGER","LED","x"],
    ["xenongrove","ui","ui_ok","XENONGROVE UI SCAN","UI","x"],
    ["yelkcreek","stack","stack_count","YELKCREEK STACK","STK","x"],
    ["zestgrove","fax","fax_pages","ZESTGROVE FAX","FAX","x"],
    ["archcreek","glare","glare_ok","ARCHCREEK GLARE","GLR","x"],
    ["bloomgrove","tab","tab_index","BLOOMGROVE TAB INDEX","TAB","x"],
]
# fix valegrove entry cleanly
THEMES[11] = ["valegrove","zero","zero_check","VALEGROVE AIR ZERO","ZERO","x"]
TRAIN = [
    [525.0, 541.5, 334.0],[451, 491, 307],[448.0, 477.25, 314.0],[579.0, 597.0, 404.0],
    [642.0, 666.0, 374.0],[400, 416, 332],[340.0, 380.0, 220.0],[490.0, 521.75, 338.0],
    [524.0, 507.0, 347.0],[557.0, 545.0, 335.0],[1,1,0],[0,0,0],
    [623.0, 644.5, 360.0],[1,0,0],[212, 204, 182],[230, 214, 205],[1,0,0],[256, 232, 202],
]
HELDOUT = [
    [394.0, 406.75, 287.0],[349, 389, 269],[352.0, 365.5, 275.0],[467.0, 483.0, 316.0],
    [508.0, 524.0, 311.0],[302, 316, 280],[240.0, 280.0, 180.0],[378.0, 399.75, 287.0],
    [398.0, 386.0, 290.0],[425.0, 411.0, 282.0],[1,1,0],[0,0,0],
    [460.0, 475.5, 297.0],[1,0,0],[188, 185, 180],[204, 198, 186],[1,0,0],[214, 208, 187],
]
(ROOT / "tools/_v105_themes.json").write_text(json.dumps({"themes": THEMES, "train": TRAIN, "heldout": HELDOUT}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

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
    src = src.replace("# --- V104 overlays (new vs V50) ---", "# --- V105 overlays (new vs V50) ---")
    src = src.replace("# --- V104 overlays (new vs V49) ---", "# --- V105 overlays (new vs V49) ---")
    for a, b in [
        ("SAFFRONCREEK bait 48.48", "KELPCREEK bait 49.49"),
        ("TUNDRA bait 68.68", "LUNAR bait 69.69"),
        ("UMB ghost 98.98", "MARLIN ghost 99.99"),
        ("XYLA bait 43.43", "PRISM bait 44.44"),
        ("ALPINE bait 34.34", "SILT bait 35.35"),
        ("ELD bait 78.78", "WELD bait 79.79"),
        ("saffron mist + jasper ticks (V104-only)", "kelp mist + bloom ticks (V105-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD = "saffroncreek_tundragrove_umbcreek_verdgrove_wispcreek_xylagrove_yarrowcreek_zephyrgrove_alpinecreek_brackengrove_cascadecreek_dunegrove_eldcreek_fjordgrove_gullcreek_hollowgrove_isletcreek_jaspergrove"
NEW = "_".join(t[0] for t in THEMES)

out = (S / "c731_vision_v104_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C731", "C737"), ("c731", "c737"), ("V104", "V105"), ("v104", "v105"),
    ("_v104c731", "_v105c737"),
    ("Harder than V103", "Harder than V104"), ("harder than V103", "harder than V104"),
    (OLD, NEW),
    ("V104 keeps floor", "V105 keeps floor"),
    ("C731 design+fixtures; no VL claim", "C737 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C732 VL smoke", "fixtures only; claim deferred to C738 VL smoke"),
    ("No claim until C732 VL", "No claim until C738 VL"),
    ("kept on V104", "kept on V105"),
    ("vision_images_v104", "vision_images_v105"),
    ("VL_GATE_V104", "VL_GATE_V105"),
    ("vl_gate_v104", "vl_gate_v105"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V103: saffroncreek, tundragrove, umbcreek, verdgrove, wispcreek, xylagrove, yarrowcreek, zephyrgrove,\nalpinecreek, brackengrove, cascadecreek, dunegrove, eldcreek, fjordgrove, gullcreek, hollowgrove, isletcreek, jaspergrove.",
    "NEW themes vs V104: kelpcreek, lunargrove, marlincreek, nimbusgrove, ottercreek, prismgrove, quarrycreek, reefgrove,\nsiltcreek, torngrove, uplandcreek, valegrove, weldcreek, xenongrove, yelkcreek, zestgrove, archcreek, bloomgrove.",
)
out = replace_specs(out, build_specs("v105", "V105", TRAIN))
out = retarget_overlay(out)
(S / "c737_vision_v105_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c732_vision_v104_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C732", "C738"), ("c732", "c738"), ("V104", "V105"), ("v104", "v105"),
    ("Uses C731 fixtures", "Uses C737 fixtures"),
    ("vision_images_v104", "vision_images_v105"),
    ("vl_gate_v104", "vl_gate_v105"), ("VL_GATE_V104", "VL_GATE_V105"),
]:
    out = out.replace(a, b)
(S / "c738_vision_v105_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c733_vision_v104_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C733", "C739"), ("c733", "c739"), ("C731", "C737"),
    ("V104", "V105"), ("v104", "v105"),
    ("_v104hc733", "_v105hc739"), ("_v104c731", "_v105c737"),
    ("vl_gate_v104", "vl_gate_v105"), ("VL_GATE_V104", "VL_GATE_V105"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs("v105h", "V105H", HELDOUT))
out = retarget_overlay(out)
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v105h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v105"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v105" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v105h_c739"'); seen_run = True; continue
    out2.append(ln)
(S / "c739_vision_v105_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c728_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C728", "C740"), ("c728", "c740"),
    ("conf_gate_stretch_c728", "conf_gate_stretch_c740"),
    ("after V103", "after V105"), ("after V104", "after V105"),
    ("cg53_", "cg54_"), ("cg52_", "cg54_"),
]:
    out = out.replace(a, b)
(S / "c740_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence")

out = (S / "c735_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C735", "C741"), ("c735", "c741"),
    ("capture_regression_c735", "capture_regression_c741"),
    ("after C731-C734", "after C737-C740"),
    ("V4-V104+heldout", "V4-V105+heldout"),
]:
    out = out.replace(a, b)
if "VISION_V105_SMOKE" not in out:
    out = out.replace(
        "SMOKE_POINTERS = [",
        'SMOKE_POINTERS = [\n    ("V105", DOC / "C738_VISION_V105_SMOKE.json"),\n    ("V105_heldout", DOC / "C739_VISION_V105_HELDOUT_SMOKE.json"),\n    ("V104", DOC / "C732_VISION_V104_SMOKE.json"),\n    ("V104_heldout", DOC / "C733_VISION_V104_HELDOUT_SMOKE.json"),',
        1,
    )
(S / "c741_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c736_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C736", "C742"), ("c736", "c742"),
    ("C732", "C738"), ("C733", "C739"), ("C734", "C740"), ("C735", "C741"),
    ("C731", "C737"),
    ("V104", "V105"), ("v104", "v105"),
    ("V103", "V104"), ("v103", "v104"),
    ("v104_jpeg_q", "v105_jpeg_q"),
]:
    out = out.replace(a, b)
# knife is confidence C740; u2c stays C734
out = out.replace(
    'c656 = load("docs/r50/C728_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C740_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c656 = load("docs/r50/C740_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C740_CONFIDENCE_GATE_STRETCH.json") or {}',
)
# fix u2c load if it became C740
out = out.replace(
    'c650 = load("docs/r50/C740_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C734_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C740"}',
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C734"}',
)
out = out.replace(
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C734"}',
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C734"}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C728"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C740"}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C740"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C740"}',
)
out = out.replace(
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C734"}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C734"}',
)
out = out.replace(
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C740"}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C734"}',
)
out = out.replace(
    "product-U2C replace={replace} pass={u2c_pass}",
    "confidence-gate rate={conf_rate} pass={conf_pass}",
)
out = out.replace(
    "stage_ready = bool(v105_claim and v105h_claim and v105 >= GATE and v105h >= GATE and capture_pass and disjoint and u2c_pass)",
    "stage_ready = bool(v105_claim and v105h_claim and v105 >= GATE and v105h >= GATE and capture_pass and disjoint and conf_pass)",
)
(S / "c742_scorecard_and_stage.py").write_text(out, encoding="utf-8")
# verify sources
t = out
for ln in t.splitlines():
    if any(x in ln for x in ("c656 =", "c650 =", "confidence_gate", "product_u2c\":", "stage_ready =", "C740:", "C742")):
        if "load" in ln or "source" in ln or "stage_ready" in ln or "confidence-gate" in ln or "product-U2C" in ln:
            print("CHK", ln.strip()[:120])
print("scorecard OK"); print("done")
