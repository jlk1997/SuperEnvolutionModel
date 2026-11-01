# -*- coding: utf-8 -*-
"""Generate C605-C610 V83 from V81 using tools/_v83_themes.json. Knife: confidence-gate."""
from __future__ import annotations
import json, re
from pathlib import Path

ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"
D = json.loads((ROOT / "tools/_v83_themes.json").read_text(encoding="utf-8"))
THEMES, TRAIN_ABC, HELDOUT_ABC = D["themes"], D["train"], D["heldout"]
THEME_STR = "_".join(t[0] for t in THEMES)
OLD_THEME = "saltmarsh_tidewater_umbercliff_violetgrove_willowbank_xerocreek_yokecliff_zincbank_aspenbank_beechgrove_coralbank_dewcreek_elmgrove_ferncreek_granitebank_hemlockgrove_ivorybank_jasperbank"
NAMES = [t[0] for t in THEMES]


def body_for(kind, a, b, c):
    a, b, c = float(a), float(b), float(c)
    if kind == "sum_ab":
        return a + b, [f"a paid {a:.2f}", f"b paid {b:.2f}", f"c open {c:.2f}", f"TOTAL PAID TARGET {a+b:.2f}"]
    if kind == "qty_ab":
        return float(int(a) + int(b)) if a == int(a) and b == int(b) else float(a + b), [
            f"SKU1 qty {int(a) if a==int(a) else a} ok", f"SKU2 qty {int(c) if c==int(c) else c} hold",
            f"SKU3 qty {int(b) if b==int(b) else b} ok", f"qty_sum TARGET {int(a+b) if a==int(a) and b==int(b) else a+b}",
        ]
    if kind == "dup2":
        return 2.0, ["markA 1", "markB 1", "markC 0", "dup_mark TARGET 2"]
    if kind == "zero":
        return 0.0, ["z1 0.00", "z2 0.00", "z3 0.00", "zero_check TARGET 0.00"]
    if kind == "ui1":
        return 1.0, ["btnOK 1", "btnSkip 0", "btnBad 0", "ui_ok TARGET 1"]
    raise ValueError(kind)


def fmt_num(x):
    return repr(float(x)) if isinstance(x, float) and not float(x).is_integer() else (repr(int(x)) if float(x).is_integer() and abs(x) < 1e9 else repr(x))


def lines_for_metric(name, kind_suf, metric, title, stamp, body_kind, a, b, c, tag):
    # specialize bodies by metric to match prior pattern
    a, b, c = a, b, c
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
    if isinstance(x, float) and x == int(x) and abs(x) <= 10:
        return repr(float(x))
    if isinstance(x, float) and x != int(x):
        return repr(float(x))
    if isinstance(x, float):
        return repr(float(x))
    return repr(x)


def build_specs(prefix, tag, abcs):
    lines = ["SPECS = ["]
    for i, (t, abc) in enumerate(zip(THEMES, abcs), 1):
        name, kind_suf, metric, title, stamp, _bk = t
        a, b, c = abc
        expected, body = lines_for_metric(name, kind_suf, metric, title, stamp, _bk, a, b, c, tag)
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
    src = src.replace("# --- V81 overlays (new vs V80) ---", "# --- V83 overlays (new vs V82) ---")
    for a, b in [
        ("AMBERFIELD bait", "KELPWOOD bait"), ("RIDGEFIELD bait", "BIRCHBANK bait"),
        ("LOAMFIELD ghost", "VINEBANK ghost"), ("NOOKFIELD bait", "XENOBANK bait"),
        ("FROSTFIELD bait", "PINEBANK bait"), ("OAKFIELD", "YEWBANK"),
        ("BLUFFIELD bait", "LIMECLIFF bait"),
        ("amber mist + ridgefield ticks (V81-only)", "kelp mist + birchbank ticks (V83-only)"),
    ]:
        src = src.replace(a, b)
    return src


def gen_design():
    out = (S / "c599_vision_v82_design_and_batch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C593", "C605"), ("c593", "c605"), ("V82", "V83"), ("v81", "v83"),
        ("_v81c593", "_v83c605"),
        ("Harder than V80", "Harder than V82"), ("harder than V80", "harder than V82"),
        (OLD_THEME, THEME_STR),
        ("V81 keeps floor", "V83 keeps floor"),
        ("C593 design+fixtures; no VL claim", "C605 design+fixtures; no VL claim"),
        ("fixtures only; claim deferred to C594 VL smoke", "fixtures only; claim deferred to C606 VL smoke"),
        ("No claim until C594 VL", "No claim until C606 VL"),
        ("kept on V81", "kept on V83"),
        ('"harder_than": "v80_indigodale_zephyrfield"', '"harder_than": "v82_saltmarsh_jasperbank"'),
        ("r50plus_v81_amberfield_ridgefield", "r50plus_v83_kelpwood_birchbank"),
    ]:
        out = out.replace(a, b)
    out = out.replace(
        "NEW themes vs V80: amberfield, bluffield, cliffield, driftfield, emberfield, frostfield, glenfield, heathfield,\nirisfield, jadeffield, kelpfield, loamfield, marshfield, nookfield, oakfield, peatfield, quillfield, ridgefield.",
        "NEW themes vs V81: saltmarsh, tidewater, umbercliff, violetgrove, willowbank, xerocreek, yokecliff, zincbank,\naspenbank, beechgrove, coralbank, dewcreek, elmgrove, ferncreek, granitebank, hemlockgrove, ivorybank, jasperbank.",
    )
    out = replace_specs(out, build_specs("v83", "V83", TRAIN_ABC))
    out = retarget_overlay(out)
    (S / "c605_vision_v83_design_and_batch.py").write_text(out, encoding="utf-8")
    print("wrote design")


def gen_smoke():
    out = (S / "c600_vision_v82_smoke.py").read_text(encoding="utf-8")
    for a, b in [
        ("C594", "C606"), ("c594", "c606"), ("V82", "V83"), ("v81", "v83"),
        ("r50plus_v81_amberfield_ridgefield_clarity_floor_n>=16_qwen35_2b",
         "r50plus_v83_kelpwood_birchbank_clarity_floor_n>=16_qwen35_2b"),
        ("Uses C593 fixtures", "Uses C605 fixtures"),
    ]:
        out = out.replace(a, b)
    (S / "c606_vision_v83_smoke.py").write_text(out, encoding="utf-8")
    print("wrote smoke")


def gen_heldout():
    out = (S / "c601_vision_v82_heldout.py").read_text(encoding="utf-8")
    for a, b in [
        ("C595", "C607"), ("c595", "c607"), ("C593", "C605"),
        ("V82", "V83"), ("v81", "v83"),
        ("_v81hc595", "_v83hc607"), ("_v81c593", "_v83c605"),
    ]:
        out = out.replace(a, b)
    out = replace_specs(out, build_specs("v83h", "V83H", HELDOUT_ABC))
    out = retarget_overlay(out)
    out2, seen_fix, seen_train, seen_run = [], False, False, False
    for ln in out.splitlines():
        s = ln.strip()
        if s.startswith("FIX = ") and not seen_fix:
            out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v83h"'); seen_fix = True; continue
        if s.startswith("TRAIN_FIX = ") and not seen_train:
            out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v83"'); seen_train = True; continue
        if s.startswith("RUN = ") and "vision_v83" in s and not seen_run:
            out2.append('RUN = ROOT / "runs/vision_v83h_c607"'); seen_run = True; continue
        out2.append(ln)
    (S / "c607_vision_v83_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
    print("wrote heldout")


def gen_conf():
    out = (S / "c596_confidence_gate_stretch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C590", "C608"), ("c590", "c608"),
        ("product_u2c_c590", "confidence_gate_c608"), ("u2c_cost_c590", "confidence_gate_c608"),
        ("after V80", "after V83"), ("after V81", "after V83"),
        ("V80+", "V83+"), ("V81+", "V83+"),
    ]:
        out = out.replace(a, b)
    (S / "c608_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
    print("wrote conf")


def gen_regression():
    out = (S / "c603_capture_office_regression.py").read_text(encoding="utf-8")
    for a, b in [
        ("C597", "C609"), ("c597", "c609"),
        ("capture_regression_c597", "capture_regression_c609"),
        ("after C593-C596", "after C605-C608"),
        ("V4-V81+heldout", "V4-V83+heldout"),
    ]:
        out = out.replace(a, b)
    if "VISION_V83_SMOKE" not in out:
        out = out.replace(
            "SMOKE_POINTERS = [",
            'SMOKE_POINTERS = [\n'
            '    ("V83", DOC / "C606_VISION_V83_SMOKE.json"),\n'
            '    ("V83_heldout", DOC / "C607_VISION_V83_HELDOUT_SMOKE.json"),\n'
            '    ("V82", DOC / "C600_VISION_V82_SMOKE.json"),\n'
            '    ("V82_heldout", DOC / "C601_VISION_V82_HELDOUT_SMOKE.json"),',
            1,
        )
    (S / "c609_capture_office_regression.py").write_text(out, encoding="utf-8")
    print("wrote regression")


def gen_scorecard():
    print("wrote scorecard (prebuilt c610)")


def main():
    gen_design(); gen_smoke(); gen_heldout(); gen_conf(); gen_regression(); gen_scorecard()
    print("OK C605-C610")


if __name__ == "__main__":
    main()
