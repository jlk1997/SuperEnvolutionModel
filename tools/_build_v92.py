# -*- coding: utf-8 -*-
from __future__ import annotations
import json, re
from pathlib import Path
ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"
D = json.loads((ROOT / "tools/_v92_themes.json").read_text(encoding="utf-8"))
THEMES, TRAIN_ABC, HELDOUT_ABC = D["themes"], D["train"], D["heldout"]
THEME_STR = "_".join(t[0] for t in THEMES)
OLD_THEME = "jadecreek_kelpgrove_limecreek_maplecreek_nutmegcreek_olivegrove_pinecreek_quartzgrove_ravencreek_silvergrove_thorncreek_umbergrove_vinecreek_wavegrove_xenocreek_yewcreek_zinccreek_aspengrove"

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
    src = src.replace("# --- V91 overlays (new vs V90) ---", "# --- V92 overlays (new vs V91) ---")
    src = src.replace("# --- V90 overlays (new vs V89) ---", "# --- V92 overlays (new vs V91) ---")
    for a, b in [
        ("JADECREEK bait", "BAYCREEK bait"), ("ASPENGROVE bait", "TULIPGROVE bait"),
        ("THORNCREEK bait", "LOTUSCREEK bait"), ("SILVERGROVE bait", "KILNGROVE bait"),
        ("UMBERGROVE bait", "MARIGOLDGROVE bait"), ("ZINCCREEK", "SAGECREEK"),
        ("KELPGROVE bait", "CORALGROVE bait"),
        ("jade mist + aspengrove ticks (V91-only)", "bay mist + tulipgrove ticks (V92-only)"),
        ("heath mist + irongrove ticks (V90-only)", "bay mist + tulipgrove ticks (V92-only)"),
    ]:
        src = src.replace(a, b)
    return src

out = (S / "c653_vision_v91_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C653", "C659"), ("c653", "c659"), ("V91", "V92"), ("v91", "v92"),
    ("_v91c653", "_v92c659"),
    ("Harder than V90", "Harder than V91"), ("harder than V90", "harder than V91"),
    (OLD_THEME, THEME_STR),
    ("V91 keeps floor", "V92 keeps floor"),
    ("C653 design+fixtures; no VL claim", "C659 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C654 VL smoke", "fixtures only; claim deferred to C660 VL smoke"),
    ("No claim until C654 VL", "No claim until C660 VL"),
    ("kept on V91", "kept on V92"),
    ('"harder_than": "v90_heathcreek_irongrove"', '"harder_than": "v91_jadecreek_aspengrove"'),
    ("r50plus_v91_jadecreek_aspengrove", "r50plus_v92_baycreek_tulipgrove"),
    ("vision_images_v91", "vision_images_v92"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V90: jadecreek, kelpgrove, limecreek, maplecreek, nutmegcreek, olivegrove, pinecreek, quartzgrove,\nravencreek, silvergrove, thorncreek, umbergrove, vinecreek, wavegrove, xenocreek, yewcreek, zinccreek, aspengrove.",
    "NEW themes vs V91: baycreek, coralgrove, dawncreek, embergrove, ferncreek, granitegrove, harborcreek, ivorygrove,\njetcreek, kilngrove, lotuscreek, marigoldgrove, nectarcreek, oakgrove, petalcreek, ridgegrove, sagecreek, tulipgrove.",
)
out = replace_specs(out, build_specs("v92", "V92", TRAIN_ABC))
out = retarget_overlay(out)
(S / "c659_vision_v92_design_and_batch.py").write_text(out, encoding="utf-8")
print("design", out.count("vision_images_v92"), out.count("C659"))

out = (S / "c654_vision_v91_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C654", "C660"), ("c654", "c660"), ("V91", "V92"), ("v91", "v92"),
    ("r50plus_v91_jadecreek_aspengrove_clarity_floor_n>=16_qwen35_2b", "r50plus_v92_baycreek_tulipgrove_clarity_floor_n>=16_qwen35_2b"),
    ("Uses C653 fixtures", "Uses C659 fixtures"),
    ("vision_images_v91", "vision_images_v92"),
]:
    out = out.replace(a, b)
(S / "c660_vision_v92_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c655_vision_v91_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C655", "C661"), ("c655", "c661"), ("C653", "C659"),
    ("V91", "V92"), ("v91", "v92"),
    ("_v91hc655", "_v92hc661"), ("_v91c653", "_v92c659"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs("v92h", "V92H", HELDOUT_ABC))
out = retarget_overlay(out)
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v92h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v92"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v92" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v92h_c661"'); seen_run = True; continue
    out2.append(ln)
(S / "c661_vision_v92_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c650_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C650", "C662"), ("c650", "c662"),
    ("product_u2c_c650", "product_u2c_c662"), ("u2c_cost_c650", "u2c_cost_c662"),
    ("after V90", "after V92"), ("after V91", "after V92"),
    ("V90+", "V92+"), ("V91+", "V92+"),
]:
    out = out.replace(a, b)
(S / "c662_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c657_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C657", "C663"), ("c657", "c663"),
    ("capture_regression_c657", "capture_regression_c663"),
    ("after C653-C656", "after C659-C662"),
    ("V4-V91+heldout", "V4-V92+heldout"),
]:
    out = out.replace(a, b)
if "VISION_V92_SMOKE" not in out:
    out = out.replace(
        "SMOKE_POINTERS = [",
        'SMOKE_POINTERS = [\n    ("V92", DOC / "C660_VISION_V92_SMOKE.json"),\n    ("V92_heldout", DOC / "C661_VISION_V92_HELDOUT_SMOKE.json"),\n    ("V91", DOC / "C654_VISION_V91_SMOKE.json"),\n    ("V91_heldout", DOC / "C655_VISION_V91_HELDOUT_SMOKE.json"),',
        1,
    )
(S / "c663_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c652_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C652", "C664"), ("c652", "c664"),
    ("C647", "C659"), ("C648", "C660"), ("C649", "C661"), ("C650", "C662"), ("C651", "C663"),
    ("V90", "V92"), ("v90", "v92"),
    ("V89", "V91"), ("v89", "v91"),
    ("C644", "C656"),
    ("v90_jpeg_q", "v92_jpeg_q"),
    ("V90 milestone", "V92 slice"),
    ("not a stop", "continue"),
]:
    out = out.replace(a, b)
(S / "c664_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard OK")
print("done")