# -*- coding: utf-8 -*-
from __future__ import annotations
import json, re
from pathlib import Path
ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"
D = json.loads((ROOT / "tools/_v94_themes.json").read_text(encoding="utf-8"))
THEMES, TRAIN_ABC, HELDOUT_ABC = D["themes"], D["train"], D["heldout"]
THEME_STR = "_".join(t[0] for t in THEMES)
OLD_THEME = "azurecreek_bluffgrove_canyoncreek_dellgrove_eddycreek_flintgrove_gorgecreek_hillgrove_inletcreek_jaspergrove_kettlecreek_lagoongrove_meadowcreek_nestgrove_orchardcreek_prairiegrove_quarrycreek_rivergrove"

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
    src = src.replace("# --- V93 overlays (new vs V92) ---", "# --- V94 overlays (new vs V93) ---")
    for a, b in [
        ("AZURECREEK bait", "SUMMITCREEK bait"), ("RIVERGROVE bait", "JUNIPERGROVE bait"),
        ("KETTLECREEK bait", "COPPERCREEK bait"), ("JASPERGROVE bait", "BRIDGEGROVE bait"),
        ("LAGOONGROVE bait", "DRIFTGROVE bait"), ("QUARRYCREEK", "ISLANDCREEK"),
        ("BLUFFGROVE bait", "TIDEGROVE bait"),
        ("azure mist + rivergrove ticks (V93-only)", "summit mist + junipergrove ticks (V94-only)"),
    ]:
        src = src.replace(a, b)
    return src

out = (S / "c665_vision_v93_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C665", "C671"), ("c665", "c671"), ("V93", "V94"), ("v93", "v94"),
    ("_v93c665", "_v94c671"),
    ("Harder than V92", "Harder than V93"), ("harder than V92", "harder than V93"),
    (OLD_THEME, THEME_STR),
    ("V93 keeps floor", "V94 keeps floor"),
    ("C665 design+fixtures; no VL claim", "C671 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C666 VL smoke", "fixtures only; claim deferred to C672 VL smoke"),
    ("No claim until C666 VL", "No claim until C672 VL"),
    ("kept on V93", "kept on V94"),
    ('"harder_than": "v92_baycreek_tulipgrove"', '"harder_than": "v93_azurecreek_rivergrove"'),
    ("r50plus_v93_azurecreek_rivergrove", "r50plus_v94_summitcreek_junipergrove"),
    ("vision_images_v93", "vision_images_v94"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V92: azurecreek, bluffgrove, canyoncreek, dellgrove, eddycreek, flintgrove, gorgecreek, hillgrove,\ninletcreek, jaspergrove, kettlecreek, lagoongrove, meadowcreek, nestgrove, orchardcreek, prairiegrove, quarrycreek, rivergrove.",
    "NEW themes vs V93: summitcreek, tidegrove, uplandcreek, vaultgrove, wintercreek, xeragrove, yellowcreek, zephyrgrove,\nanchorcreek, bridgegrove, coppercreek, driftgrove, eaglecreek, falcongrove, glaciercreek, havengrove, islandcreek, junipergrove.",
)
out = replace_specs(out, build_specs("v94", "V94", TRAIN_ABC))
out = retarget_overlay(out)
(S / "c671_vision_v94_design_and_batch.py").write_text(out, encoding="utf-8")
print("design", out.count("vision_images_v94"), out.count("C671"))

out = (S / "c666_vision_v93_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C666", "C672"), ("c666", "c672"), ("V93", "V94"), ("v93", "v94"),
    ("r50plus_v93_azurecreek_rivergrove_clarity_floor_n>=16_qwen35_2b", "r50plus_v94_summitcreek_junipergrove_clarity_floor_n>=16_qwen35_2b"),
    ("Uses C665 fixtures", "Uses C671 fixtures"),
    ("vision_images_v93", "vision_images_v94"),
]:
    out = out.replace(a, b)
(S / "c672_vision_v94_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c667_vision_v93_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C667", "C673"), ("c667", "c673"), ("C665", "C671"),
    ("V93", "V94"), ("v93", "v94"),
    ("_v93hc667", "_v94hc673"), ("_v93c665", "_v94c671"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs("v94h", "V94H", HELDOUT_ABC))
out = retarget_overlay(out)
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v94h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v94"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v94" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v94h_c673"'); seen_run = True; continue
    out2.append(ln)
(S / "c673_vision_v94_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c662_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C662", "C674"), ("c662", "c674"),
    ("product_u2c_c662", "product_u2c_c674"), ("u2c_cost_c662", "u2c_cost_c674"),
    ("after V92", "after V94"), ("after V93", "after V94"),
    ("V92+", "V94+"), ("V93+", "V94+"),
]:
    out = out.replace(a, b)
(S / "c674_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c669_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C669", "C675"), ("c669", "c675"),
    ("capture_regression_c669", "capture_regression_c675"),
    ("after C665-C668", "after C671-C674"),
    ("V4-V93+heldout", "V4-V94+heldout"),
]:
    out = out.replace(a, b)
if "VISION_V94_SMOKE" not in out:
    out = out.replace(
        "SMOKE_POINTERS = [",
        'SMOKE_POINTERS = [\n    ("V94", DOC / "C672_VISION_V94_SMOKE.json"),\n    ("V94_heldout", DOC / "C673_VISION_V94_HELDOUT_SMOKE.json"),\n    ("V93", DOC / "C666_VISION_V93_SMOKE.json"),\n    ("V93_heldout", DOC / "C667_VISION_V93_HELDOUT_SMOKE.json"),',
        1,
    )
(S / "c675_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c664_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C664", "C676"), ("c664", "c676"),
    ("C659", "C671"), ("C660", "C672"), ("C661", "C673"), ("C662", "C674"), ("C663", "C675"),
    ("V92", "V94"), ("v92", "v94"),
    ("V91", "V93"), ("v91", "v93"),
    ("C656", "C668"),
    ("v92_jpeg_q", "v94_jpeg_q"),
    ("V92 slice", "V94 slice"),
]:
    out = out.replace(a, b)
(S / "c676_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard OK")
print("done")