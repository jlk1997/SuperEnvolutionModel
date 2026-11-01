# -*- coding: utf-8 -*-
from __future__ import annotations
import json, re
from pathlib import Path
ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"
D = json.loads((ROOT / "tools/_v93_themes.json").read_text(encoding="utf-8"))
THEMES, TRAIN_ABC, HELDOUT_ABC = D["themes"], D["train"], D["heldout"]
THEME_STR = "_".join(t[0] for t in THEMES)
OLD_THEME = "baycreek_coralgrove_dawncreek_embergrove_ferncreek_granitegrove_harborcreek_ivorygrove_jetcreek_kilngrove_lotuscreek_marigoldgrove_nectarcreek_oakgrove_petalcreek_ridgegrove_sagecreek_tulipgrove"

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
    src = src.replace("# --- V92 overlays (new vs V91) ---", "# --- V93 overlays (new vs V92) ---")
    src = src.replace("# --- V91 overlays (new vs V90) ---", "# --- V93 overlays (new vs V92) ---")
    for a, b in [
        ("BAYCREEK bait", "AZURECREEK bait"), ("TULIPGROVE bait", "RIVERGROVE bait"),
        ("LOTUSCREEK bait", "KETTLECREEK bait"), ("KILNGROVE bait", "JASPERGROVE bait"),
        ("MARIGOLDGROVE bait", "LAGOONGROVE bait"), ("SAGECREEK", "QUARRYCREEK"),
        ("CORALGROVE bait", "BLUFFGROVE bait"),
        ("bay mist + tulipgrove ticks (V92-only)", "azure mist + rivergrove ticks (V93-only)"),
        ("jade mist + aspengrove ticks (V91-only)", "azure mist + rivergrove ticks (V93-only)"),
    ]:
        src = src.replace(a, b)
    return src

out = (S / "c659_vision_v92_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C659", "C665"), ("c659", "c665"), ("V92", "V93"), ("v92", "v93"),
    ("_v92c659", "_v93c665"),
    ("Harder than V91", "Harder than V92"), ("harder than V91", "harder than V92"),
    (OLD_THEME, THEME_STR),
    ("V92 keeps floor", "V93 keeps floor"),
    ("C659 design+fixtures; no VL claim", "C665 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C660 VL smoke", "fixtures only; claim deferred to C666 VL smoke"),
    ("No claim until C660 VL", "No claim until C666 VL"),
    ("kept on V92", "kept on V93"),
    ('"harder_than": "v91_jadecreek_aspengrove"', '"harder_than": "v92_baycreek_tulipgrove"'),
    ("r50plus_v92_baycreek_tulipgrove", "r50plus_v93_azurecreek_rivergrove"),
    ("vision_images_v92", "vision_images_v93"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V91: baycreek, coralgrove, dawncreek, embergrove, ferncreek, granitegrove, harborcreek, ivorygrove,\njetcreek, kilngrove, lotuscreek, marigoldgrove, nectarcreek, oakgrove, petalcreek, ridgegrove, sagecreek, tulipgrove.",
    "NEW themes vs V92: azurecreek, bluffgrove, canyoncreek, dellgrove, eddycreek, flintgrove, gorgecreek, hillgrove,\ninletcreek, jaspergrove, kettlecreek, lagoongrove, meadowcreek, nestgrove, orchardcreek, prairiegrove, quarrycreek, rivergrove.",
)
out = replace_specs(out, build_specs("v93", "V93", TRAIN_ABC))
out = retarget_overlay(out)
(S / "c665_vision_v93_design_and_batch.py").write_text(out, encoding="utf-8")
print("design", out.count("vision_images_v93"), out.count("C665"))

out = (S / "c660_vision_v92_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C660", "C666"), ("c660", "c666"), ("V92", "V93"), ("v92", "v93"),
    ("r50plus_v92_baycreek_tulipgrove_clarity_floor_n>=16_qwen35_2b", "r50plus_v93_azurecreek_rivergrove_clarity_floor_n>=16_qwen35_2b"),
    ("Uses C659 fixtures", "Uses C665 fixtures"),
    ("vision_images_v92", "vision_images_v93"),
]:
    out = out.replace(a, b)
(S / "c666_vision_v93_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c661_vision_v92_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C661", "C667"), ("c661", "c667"), ("C659", "C665"),
    ("V92", "V93"), ("v92", "v93"),
    ("_v92hc661", "_v93hc667"), ("_v92c659", "_v93c665"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs("v93h", "V93H", HELDOUT_ABC))
out = retarget_overlay(out)
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v93h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v93"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v93" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v93h_c667"'); seen_run = True; continue
    out2.append(ln)
(S / "c667_vision_v93_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c656_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C656", "C668"), ("c656", "c668"),
    ("conf_gate_stretch_c656", "conf_gate_stretch_c668"),
    ("after V91", "after V93"), ("after V92", "after V93"),
    ("cg49_", "cg50_"),
]:
    out = out.replace(a, b)
(S / "c668_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence")

out = (S / "c663_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C663", "C669"), ("c663", "c669"),
    ("capture_regression_c663", "capture_regression_c669"),
    ("after C659-C662", "after C665-C668"),
    ("V4-V92+heldout", "V4-V93+heldout"),
]:
    out = out.replace(a, b)
if "VISION_V93_SMOKE" not in out:
    out = out.replace(
        "SMOKE_POINTERS = [",
        'SMOKE_POINTERS = [\n    ("V93", DOC / "C666_VISION_V93_SMOKE.json"),\n    ("V93_heldout", DOC / "C667_VISION_V93_HELDOUT_SMOKE.json"),\n    ("V92", DOC / "C660_VISION_V92_SMOKE.json"),\n    ("V92_heldout", DOC / "C661_VISION_V92_HELDOUT_SMOKE.json"),',
        1,
    )
(S / "c669_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c658_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C658", "C670"), ("c658", "c670"),
    ("C654", "C666"), ("C655", "C667"), ("C656", "C668"), ("C657", "C669"),
    ("C653", "C665"),
    ("V91", "V93"), ("v91", "v93"),
    ("V90", "V92"), ("v90", "v92"),
    ("C650", "C662"),
    ("v91_jpeg_q", "v93_jpeg_q"),
]:
    out = out.replace(a, b)
(S / "c670_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard OK")
print("done")