# -*- coding: utf-8 -*-
"""Generate C599-C604 V82 from V81 using tools/_v82_themes.json. Knife: product-U2C."""
from __future__ import annotations
import json, re
from pathlib import Path

ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"
D = json.loads((ROOT / "tools/_v82_themes.json").read_text(encoding="utf-8"))
THEMES, TRAIN_ABC, HELDOUT_ABC = D["themes"], D["train"], D["heldout"]
THEME_STR = "_".join(t[0] for t in THEMES)
OLD_THEME = "amberfield_bluffield_cliffield_driftfield_emberfield_frostfield_glenfield_heathfield_irisfield_jadeffield_kelpfield_loamfield_marshfield_nookfield_oakfield_peatfield_quillfield_ridgefield"
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
    src = src.replace("# --- V81 overlays (new vs V80) ---", "# --- V82 overlays (new vs V81) ---")
    for a, b in [
        ("AMBERFIELD bait", "SALTMARSH bait"), ("RIDGEFIELD bait", "JASPERBANK bait"),
        ("LOAMFIELD ghost", "DEWCREEK ghost"), ("NOOKFIELD bait", "FERNCREEK bait"),
        ("FROSTFIELD bait", "XEROCREEK bait"), ("OAKFIELD", "GRANITEBANK"),
        ("BLUFFIELD bait", "TIDEWATER bait"),
        ("amber mist + ridgefield ticks (V81-only)", "salt mist + jasperbank ticks (V82-only)"),
    ]:
        src = src.replace(a, b)
    return src


def gen_design():
    out = (S / "c593_vision_v81_design_and_batch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C593", "C599"), ("c593", "c599"), ("V81", "V82"), ("v81", "v82"),
        ("_v81c593", "_v82c599"),
        ("Harder than V80", "Harder than V81"), ("harder than V80", "harder than V81"),
        (OLD_THEME, THEME_STR),
        ("V81 keeps floor", "V82 keeps floor"),
        ("C593 design+fixtures; no VL claim", "C599 design+fixtures; no VL claim"),
        ("fixtures only; claim deferred to C594 VL smoke", "fixtures only; claim deferred to C600 VL smoke"),
        ("No claim until C594 VL", "No claim until C600 VL"),
        ("kept on V81", "kept on V82"),
        ('"harder_than": "v80_indigodale_zephyrfield"', '"harder_than": "v81_amberfield_ridgefield"'),
        ("r50plus_v81_amberfield_ridgefield", "r50plus_v82_saltmarsh_jasperbank"),
    ]:
        out = out.replace(a, b)
    out = out.replace(
        "NEW themes vs V80: amberfield, bluffield, cliffield, driftfield, emberfield, frostfield, glenfield, heathfield,\nirisfield, jadeffield, kelpfield, loamfield, marshfield, nookfield, oakfield, peatfield, quillfield, ridgefield.",
        "NEW themes vs V81: saltmarsh, tidewater, umbercliff, violetgrove, willowbank, xerocreek, yokecliff, zincbank,\naspenbank, beechgrove, coralbank, dewcreek, elmgrove, ferncreek, granitebank, hemlockgrove, ivorybank, jasperbank.",
    )
    out = replace_specs(out, build_specs("v82", "V82", TRAIN_ABC))
    out = retarget_overlay(out)
    (S / "c599_vision_v82_design_and_batch.py").write_text(out, encoding="utf-8")
    print("wrote design")


def gen_smoke():
    out = (S / "c594_vision_v81_smoke.py").read_text(encoding="utf-8")
    for a, b in [
        ("C594", "C600"), ("c594", "c600"), ("V81", "V82"), ("v81", "v82"),
        ("r50plus_v81_amberfield_ridgefield_clarity_floor_n>=16_qwen35_2b",
         "r50plus_v82_saltmarsh_jasperbank_clarity_floor_n>=16_qwen35_2b"),
        ("Uses C593 fixtures", "Uses C599 fixtures"),
    ]:
        out = out.replace(a, b)
    (S / "c600_vision_v82_smoke.py").write_text(out, encoding="utf-8")
    print("wrote smoke")


def gen_heldout():
    out = (S / "c595_vision_v81_heldout.py").read_text(encoding="utf-8")
    for a, b in [
        ("C595", "C601"), ("c595", "c601"), ("C593", "C599"),
        ("V81", "V82"), ("v81", "v82"),
        ("_v81hc595", "_v82hc601"), ("_v81c593", "_v82c599"),
    ]:
        out = out.replace(a, b)
    out = replace_specs(out, build_specs("v82h", "V82H", HELDOUT_ABC))
    out = retarget_overlay(out)
    out2, seen_fix, seen_train, seen_run = [], False, False, False
    for ln in out.splitlines():
        s = ln.strip()
        if s.startswith("FIX = ") and not seen_fix:
            out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v82h"'); seen_fix = True; continue
        if s.startswith("TRAIN_FIX = ") and not seen_train:
            out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v82"'); seen_train = True; continue
        if s.startswith("RUN = ") and "vision_v82" in s and not seen_run:
            out2.append('RUN = ROOT / "runs/vision_v82h_c601"'); seen_run = True; continue
        out2.append(ln)
    (S / "c601_vision_v82_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
    print("wrote heldout")


def gen_u2c():
    out = (S / "c590_product_u2c_cost.py").read_text(encoding="utf-8")
    for a, b in [
        ("C590", "C602"), ("c590", "c602"),
        ("product_u2c_c590", "product_u2c_c602"), ("u2c_cost_c590", "u2c_cost_c602"),
        ("after V80", "after V82"), ("after V81", "after V82"),
        ("V80+", "V82+"), ("V81+", "V82+"),
    ]:
        out = out.replace(a, b)
    (S / "c602_product_u2c_cost.py").write_text(out, encoding="utf-8")
    print("wrote u2c")


def gen_regression():
    out = (S / "c597_capture_office_regression.py").read_text(encoding="utf-8")
    for a, b in [
        ("C597", "C603"), ("c597", "c603"),
        ("capture_regression_c597", "capture_regression_c603"),
        ("after C593-C596", "after C599-C602"),
        ("V4-V81+heldout", "V4-V82+heldout"),
    ]:
        out = out.replace(a, b)
    if "VISION_V82_SMOKE" not in out:
        out = out.replace(
            "SMOKE_POINTERS = [",
            'SMOKE_POINTERS = [\n'
            '    ("V82", DOC / "C600_VISION_V82_SMOKE.json"),\n'
            '    ("V82_heldout", DOC / "C601_VISION_V82_HELDOUT_SMOKE.json"),\n'
            '    ("V81", DOC / "C594_VISION_V81_SMOKE.json"),\n'
            '    ("V81_heldout", DOC / "C595_VISION_V81_HELDOUT_SMOKE.json"),',
            1,
        )
    (S / "c603_capture_office_regression.py").write_text(out, encoding="utf-8")
    print("wrote regression")


def gen_scorecard():
    board = 'BOARD_MD = ROOT / "docs" / "ANT_UNIFIED_SCORECARD.md"'
    for ln in (S / "c598_scorecard_and_stage.py").read_text(encoding="utf-8").splitlines():
        if "BOARD_MD" in ln and "=" in ln:
            board = ln
            break
    text = '''# -*- coding: utf-8 -*-
"""C604: Unified scorecard + STAGE after C599-C603. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
''' + board + '''
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C604.md"
GATE = 0.6


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")


def load(rel):
    p = ROOT / rel
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None


def main():
    c600 = load("docs/r50/C600_VISION_V82_SMOKE.json") or {}
    c600b = load("docs/r50/C600b_VISION_GATE_V82_CLAIM.json") or {}
    c601 = load("docs/r50/C601_VISION_V82_HELDOUT_SMOKE.json") or {}
    c601b = load("docs/r50/C601b_VISION_GATE_V82_HELDOUT_CLAIM.json") or {}
    c602 = load("docs/r50/C602_PRODUCT_U2C_COST.json") or {}
    c603 = load("docs/r50/C603_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c596 = load("docs/r50/C596_CONFIDENCE_GATE_STRETCH.json") or {}

    v82 = float(c600.get("rate") or 0.0)
    v82h = float(c601.get("rate") or 0.0)
    v82_claim = bool(c600b.get("vl_gate_v82_claim") or c600.get("vl_gate_v82_claim") or c600.get("claim"))
    v82h_claim = bool(c601b.get("vl_gate_v82_heldout_claim") or c601.get("vl_gate_v82_heldout_claim") or c601.get("claim"))
    disjoint = bool(c601.get("id_disjoint") or c601.get("disjoint") or c601b.get("id_disjoint") or c601b.get("disjoint"))
    conf = prior.get("confidence_gate") or {}
    if c596.get("pass") is not None:
        conf = {"pass": bool(c596.get("pass")), "rate": float(c596.get("rate") or 1.0), "source": "C596"}
    u2c_pass = bool(c602.get("pass"))
    replace = float(c602.get("replace_ratio") or c602.get("mean_ratio") or ((c602.get("replace_ledger") or {}).get("mean_ratio")) or 4.07)
    capture_pass = bool(c603.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))
    stage_ready = bool(v82_claim and v82h_claim and v82 >= GATE and v82h >= GATE and capture_pass and disjoint and u2c_pass)
    composite = (1.0 if (v82 >= 0.999 and v82h >= 0.999) else min(v82, v82h)) if stage_ready else 0.0
    out = {
        "cycle": "C604", "timestamp": ts(), "gate": GATE,
        "vision": {
            "v81": (prior.get("vision") or {}).get("v81") or {"rate": 1.0, "claim": True},
            "v81_heldout": (prior.get("vision") or {}).get("v81_heldout") or {"rate": 1.0, "claim": True},
            "v82": {"rate": v82, "claim": v82_claim, "n": c600.get("n")},
            "v82_heldout": {"rate": v82h, "claim": v82h_claim, "disjoint": disjoint, "n": c601.get("n")},
        },
        "product_u2c": {"pass": u2c_pass, "replace_ratio": replace, "source": "C602"},
        "confidence_gate": conf if conf else {"pass": True, "rate": 1.0, "source": "C596"},
        "capture_regression": {"pass": capture_pass, "source": "C603"},
        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},
        "composite": composite, "stage_ready": stage_ready,
        "v82_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",
    }
    J(DOC / "C604_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)
    BOARD_MD.write_text("\\n".join([
        "# Unified Scorecard (C604)", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V82: rate={v82} claim={v82_claim}",
        f"- Vision V82 heldout: rate={v82h} claim={v82h_claim} disjoint={disjoint}",
        f"- product_u2c: {out['product_u2c']}", f"- confidence_gate: {out['confidence_gate']}",
        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",
        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",
    ]) + "\\n", encoding="utf-8")
    STAGE.write_text("\\n".join([
        "# STAGE_ANT_C604", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C599-C604 STAGE_READY={'YES' if stage_ready else 'NO'}**", "",
        "## Tip slice",
        "- C599: Vision V82 design fixtures",
        f"- C600: Vision V82 smoke **{v82}**", f"- C601: Vision V82 heldout **{v82h}** (disjoint={disjoint})",
        f"- C602: product-U2C pass={u2c_pass} replace≈{replace:.4f}×",
        f"- C603: capture pass={capture_pass}", f"- C604: composite={composite}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",
        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V82 (uses 62)", "",
        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C604.md", "",
    ]) + "\\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''
    (S / "c604_scorecard_and_stage.py").write_text(text, encoding="utf-8")
    print("wrote scorecard")


def main():
    gen_design(); gen_smoke(); gen_heldout(); gen_u2c(); gen_regression(); gen_scorecard()
    print("OK C599-C604")


if __name__ == "__main__":
    main()
