# -*- coding: utf-8 -*-
from __future__ import annotations
import json, re
from pathlib import Path
ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"
D = json.loads((ROOT / "tools/_v95_themes.json").read_text(encoding="utf-8"))
THEMES, TRAIN_ABC, HELDOUT_ABC = D["themes"], D["train"], D["heldout"]
THEME_STR = "_".join(t[0] for t in THEMES)
OLD_THEME = "summitcreek_tidegrove_uplandcreek_vaultgrove_wintercreek_xeragrove_yellowcreek_zephyrgrove_anchorcreek_bridgegrove_coppercreek_driftgrove_eaglecreek_falcongrove_glaciercreek_havengrove_islandcreek_junipergrove"

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
    src = src.replace("# --- V94 overlays (new vs V93) ---", "# --- V95 overlays (new vs V94) ---")
    for a, b in [
        ("SUMMITCREEK bait", "KETTLERIDGE bait"), ("JUNIPERGROVE bait", "BIRCHRIDGE bait"),
        ("COPPERCREEK bait", "UMBRACREEK bait"), ("BRIDGEGROVE bait", "TOPAZGROVE bait"),
        ("DRIFTGROVE bait", "VIOLETGROVE bait"), ("ISLANDCREEK", "ASPENRIDGE"),
        ("TIDEGROVE bait", "LINENGROVE bait"),
        ("summit mist + junipergrove ticks (V94-only)", "kettle mist + birchridge ticks (V95-only)"),
    ]:
        src = src.replace(a, b)
    return src

out = (S / "c671_vision_v94_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C671", "C677"), ("c671", "c677"), ("V94", "V95"), ("v94", "v95"),
    ("_v94c671", "_v95c677"),
    ("Harder than V93", "Harder than V94"), ("harder than V93", "harder than V94"),
    (OLD_THEME, THEME_STR),
    ("V94 keeps floor", "V95 keeps floor"),
    ("C671 design+fixtures; no VL claim", "C677 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C672 VL smoke", "fixtures only; claim deferred to C678 VL smoke"),
    ("No claim until C672 VL", "No claim until C678 VL"),
    ("kept on V94", "kept on V95"),
    ('"harder_than": "v93_azurecreek_rivergrove"', '"harder_than": "v94_summitcreek_junipergrove"'),
    ("r50plus_v94_summitcreek_junipergrove", "r50plus_v95_kettleridge_birchridge"),
    ("vision_images_v94", "vision_images_v95"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V93: summitcreek, tidegrove, uplandcreek, vaultgrove, wintercreek, xeragrove, yellowcreek, zephyrgrove,\nanchorcreek, bridgegrove, coppercreek, driftgrove, eaglecreek, falcongrove, glaciercreek, havengrove, islandcreek, junipergrove.",
    "NEW themes vs V94: kettleridge, linengrove, marblecreek, nickelgrove, opalcreek, pearlgrove, quartzridge, rubygrove,\nslatecreek, topazgrove, umbracreek, violetgrove, walnutcreek, xenongrove, yarrowcreek, zircongrove, aspenridge, birchridge.",
)
out = replace_specs(out, build_specs("v95", "V95", TRAIN_ABC))
out = retarget_overlay(out)
(S / "c677_vision_v95_design_and_batch.py").write_text(out, encoding="utf-8")
print("design", out.count("vision_images_v95"), out.count("C677"))

out = (S / "c672_vision_v94_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C672", "C678"), ("c672", "c678"), ("V94", "V95"), ("v94", "v95"),
    ("r50plus_v94_summitcreek_junipergrove_clarity_floor_n>=16_qwen35_2b", "r50plus_v95_kettleridge_birchridge_clarity_floor_n>=16_qwen35_2b"),
    ("Uses C671 fixtures", "Uses C677 fixtures"),
    ("vision_images_v94", "vision_images_v95"),
]:
    out = out.replace(a, b)
(S / "c678_vision_v95_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c673_vision_v94_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C673", "C679"), ("c673", "c679"), ("C671", "C677"),
    ("V94", "V95"), ("v94", "v95"),
    ("_v94hc673", "_v95hc679"), ("_v94c671", "_v95c677"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs("v95h", "V95H", HELDOUT_ABC))
out = retarget_overlay(out)
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v95h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v95"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v95" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v95h_c679"'); seen_run = True; continue
    out2.append(ln)
(S / "c679_vision_v95_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c668_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C668", "C680"), ("c668", "c680"),
    ("conf_gate_stretch_c668", "conf_gate_stretch_c680"),
    ("after V93", "after V95"), ("after V94", "after V95"),
    ("cg50_", "cg51_"),
]:
    out = out.replace(a, b)
(S / "c680_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence")

out = (S / "c675_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C675", "C681"), ("c675", "c681"),
    ("capture_regression_c675", "capture_regression_c681"),
    ("after C671-C674", "after C677-C680"),
    ("V4-V94+heldout", "V4-V95+heldout"),
]:
    out = out.replace(a, b)
if "VISION_V95_SMOKE" not in out:
    out = out.replace(
        "SMOKE_POINTERS = [",
        'SMOKE_POINTERS = [\n    ("V95", DOC / "C678_VISION_V95_SMOKE.json"),\n    ("V95_heldout", DOC / "C679_VISION_V95_HELDOUT_SMOKE.json"),\n    ("V94", DOC / "C672_VISION_V94_SMOKE.json"),\n    ("V94_heldout", DOC / "C673_VISION_V94_HELDOUT_SMOKE.json"),',
        1,
    )
(S / "c681_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c670_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C670", "C682"), ("c670", "c682"),
    ("C666", "C678"), ("C667", "C679"), ("C668", "C680"), ("C669", "C681"),
    ("C665", "C677"),
    ("V93", "V95"), ("v93", "v95"),
    ("V92", "V94"), ("v92", "v94"),
    ("C662", "C674"),
    ("v93_jpeg_q", "v95_jpeg_q"),
]:
    out = out.replace(a, b)
(S / "c682_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard OK")
print("done")