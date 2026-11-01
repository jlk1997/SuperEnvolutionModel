# -*- coding: utf-8 -*-
"""Build C623-C628 Vision V86 from V84. Knife: product-U2C (C626)."""
from __future__ import annotations
import json, re
from pathlib import Path

ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"
D = json.loads((ROOT / "tools/_v86_themes.json").read_text(encoding="utf-8"))
THEMES, TRAIN_ABC, HELDOUT_ABC = D["themes"], D["train"], D["heldout"]
THEME_STR = "_".join(t[0] for t in THEMES)
OLD_THEME = "umbertide_violettide_willotide_xerotide_yarrowtide_zinctide_aspertide_beachtide_coraltide_dewotide_elmtide_ferntide_granitide_hemlotide_ivorytide_jaspertide_kelptide_limetide"


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
        lines.append(
            f'    ("{fid}", "{kind}", "{metric}", {fmt_expected(expected)},\n'
            f'     [{body_l}],\n     {repr(name)}, "{stamp}"),'
        )
    lines.append("]")
    return "\n".join(lines) + "\n"


def replace_specs(src, new_specs):
    return re.sub(r"SPECS = \[.*?\n\]\n", new_specs + "\n", src, count=1, flags=re.S)


def retarget_overlay(src):
    src = src.replace("# --- V84 overlays (new vs V83) ---", "# --- V86 overlays (new vs V84) ---")
    for a, b in [
        ("CEDARPASS bait", "MAPLETIDE bait"), ("TIDEPASS bait", "DUSKTIDE bait"),
        ("NORTHPASS ghost", "XENOTIDE ghost"), ("PEATPASS bait", "ZIRCTIDE bait"),
        ("HAZELPASS bait", "RAVENTIDE bait"), ("QUILLPASS", "ALDERTIDE"),
        ("DUSKCLIFF bait", "NUTMETIDE bait"),
        ("cedar mist + tidepass ticks (V84-only)", "umber mist + limetide ticks (V86-only)"),
    ]:
        src = src.replace(a, b)
    return src


def gen_design():
    out = (S / "c623_vision_v86_design_and_batch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C611", "C623"), ("c611", "c623"), ("V85", "V86"), ("v84", "v86"),
        ("_v84c611", "_v86c623"),
        ("Harder than V83", "Harder than V85"), ("harder than V83", "harder than V85"),
        (OLD_THEME, THEME_STR),
        ("V84 keeps floor", "V86 keeps floor"),
        ("C611 design+fixtures; no VL claim", "C623 design+fixtures; no VL claim"),
        ("fixtures only; claim deferred to C612 VL smoke", "fixtures only; claim deferred to C624 VL smoke"),
        ("No claim until C612 VL", "No claim until C624 VL"),
        ("kept on V84", "kept on V86"),
        ('"harder_than": "v83_kelpwood_birchbank"', '"harder_than": "v85_umbertide_limetide"'),
        ("r50plus_v86_mapletide_dusktide", "r50plus_v86_umbertide_limetide"),
        ("vision_images_v84", "vision_images_v86"),
    ]:
        out = out.replace(a, b)
    out = out.replace(
        "NEW themes vs V83: cedarpass, duskcliff, elderpass, firgrove, gorsebank, hazelpass, ironcliff, junipass,\nknollpass, larkpass, mosscliff, northpass, opalpass, peatpass, quillpass, reedpass, stonepass, tidepass.",
        "NEW themes vs V84: umbertide, violettide, willotide, xerotide, yarrowtide, zinctide, aspertide, beachtide,\ncoraltide, dewotide, elmtide, ferntide, granitide, hemlotide, ivorytide, jaspertide, kelptide, limetide.",
    )
    out = replace_specs(out, build_specs("v86", "V86", TRAIN_ABC))
    out = retarget_overlay(out)
    (S / "c623_vision_v86_design_and_batch.py").write_text(out, encoding="utf-8")
    print("wrote design")


def gen_smoke():
    out = (S / "c624_vision_v86_smoke.py").read_text(encoding="utf-8")
    for a, b in [
        ("C612", "C624"), ("c612", "c624"), ("V85", "V86"), ("v84", "v86"),
        ("r50plus_v86_mapletide_dusktide_clarity_floor_n>=16_qwen35_2b",
         "r50plus_v86_umbertide_limetide_clarity_floor_n>=16_qwen35_2b"),
        ("Uses C611 fixtures", "Uses C623 fixtures"),
        ("vision_images_v84", "vision_images_v86"),
    ]:
        out = out.replace(a, b)
    (S / "c624_vision_v86_smoke.py").write_text(out, encoding="utf-8")
    print("wrote smoke")


def gen_heldout():
    out = (S / "c625_vision_v86_heldout.py").read_text(encoding="utf-8")
    for a, b in [
        ("C613", "C625"), ("c613", "c625"), ("C611", "C623"),
        ("V85", "V86"), ("v84", "v86"),
        ("_v84hc613", "_v86hc625"), ("_v84c611", "_v86c623"),
    ]:
        out = out.replace(a, b)
    out = replace_specs(out, build_specs("v86h", "V86H", HELDOUT_ABC))
    out = retarget_overlay(out)
    out2, seen_fix, seen_train, seen_run = [], False, False, False
    for ln in out.splitlines():
        s = ln.strip()
        if s.startswith("FIX = ") and not seen_fix:
            out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v86h"'); seen_fix = True; continue
        if s.startswith("TRAIN_FIX = ") and not seen_train:
            out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v86"'); seen_train = True; continue
        if s.startswith("RUN = ") and "vision_v86" in s and not seen_run:
            out2.append('RUN = ROOT / "runs/vision_v86h_c625"'); seen_run = True; continue
        out2.append(ln)
    (S / "c625_vision_v86_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
    print("wrote heldout", seen_fix, seen_train, seen_run)


def gen_u2c():
    out = (S / "c614_product_u2c_cost.py").read_text(encoding="utf-8")
    for a, b in [
        ("C608", "C626"), ("c608", "c626"),
        ("confidence_gate_c608", "product_u2c_c626"),
        ("after V83", "after V86"), ("after V84", "after V86"),
        ("V83+", "V86+"), ("V84+", "V86+"),
    ]:
        out = out.replace(a, b)
    (S / "c626_product_u2c_cost.py").write_text(out, encoding="utf-8")
    print("wrote u2c")


def gen_regression():
    out = (S / "c627_capture_office_regression.py").read_text(encoding="utf-8")
    for a, b in [
        ("C615", "C627"), ("c615", "c627"),
        ("capture_regression_c615", "capture_regression_c627"),
        ("after C611-C614", "after C623-C626"),
        ("V4-V84+heldout", "V4-V86+heldout"),
    ]:
        out = out.replace(a, b)
    if "VISION_V86_SMOKE" not in out:
        out = out.replace(
            "SMOKE_POINTERS = [",
            'SMOKE_POINTERS = [\n'
            '    ("V86", DOC / "C624_VISION_V86_SMOKE.json"),\n'
            '    ("V86_heldout", DOC / "C625_VISION_V86_HELDOUT_SMOKE.json"),\n'
            '    ("V85", DOC / "C618_VISION_V85_SMOKE.json"),\n'
            '    ("V85_heldout", DOC / "C619_VISION_V85_HELDOUT_SMOKE.json"),',
            1,
        )
    (S / "c627_capture_office_regression.py").write_text(out, encoding="utf-8")
    print("wrote regression")


def gen_scorecard():
    print("wrote scorecard (prebuilt)")


def main():
    gen_design(); gen_smoke(); gen_heldout(); gen_u2c(); gen_regression(); gen_scorecard()
    print("OK C623-C628")


if __name__ == "__main__":
    main()
