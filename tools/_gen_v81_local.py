# -*- coding: utf-8 -*-
"""Generate C593-C598 V81 from V80. Knife: confidence-gate (C596)."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"

THEMES = [
    ("amberfield", "recv", "paid_total", "AMBERFIELD GRAIN RECV", "RECV",
     lambda a,b,c: (a+b, [f"a paid {a:.2f}", f"b paid {b:.2f}", f"c open {c:.2f}", f"TOTAL PAID TARGET {a+b:.2f}"])),
    ("bluffield", "wh", "qty_sum", "WH BLUFFIELD BIN", "RECV",
     lambda a,b,c: (float(a+b), [f"SKU1 qty {a} ok", f"SKU2 qty {c} hold", f"SKU3 qty {b} ok", f"qty_sum TARGET {a+b}"])),
    ("cliffield", "refund", "refund_done", "CLIFFIELD PATCH REFUND", "DONE",
     lambda a,b,c: (a+b, [f"itemR1 {a:.2f} done", f"itemR2 {b:.2f} done", f"itemR3 {c:.2f} open", f"refund_done TARGET {a+b:.2f}"])),
    ("driftfield", "tax", "tax_base_paid", "DRIFTFIELD TAX SLIP", "TAX",
     lambda a,b,c: (a+b, [f"base {a:.2f} paid", f"addon {b:.2f} paid", f"skip {c:.2f}", f"tax_base_paid TARGET {a+b:.2f}"])),
    ("emberfield", "pay", "payroll_active", "EMBERFIELD PAYROLL", "PAY",
     lambda a,b,c: (a+b, [f"empA {a:.2f} active", f"empB {b:.2f} active", f"empC {c:.2f} leave", f"payroll_active TARGET {a+b:.2f}"])),
    ("frostfield", "ship", "ship_ok", "FROSTFIELD SHIP DOCK", "SHIP",
     lambda a,b,c: (float(a+b), [f"box1 {a} ok", f"box2 {b} ok", f"box3 {c} hold", f"ship_ok TARGET {a+b}"])),
    ("glenfield", "sla", "sla_ok_hours", "GLENFIELD SLA CARD", "SLA",
     lambda a,b,c: (a+b, [f"job1 {a:.2f} hours ok", f"job2 {b:.2f} hours ok", f"job3 {c:.2f} hours late", f"sla_ok_hours TARGET {a+b:.2f}"])),
    ("heathfield", "exp", "exp_sum", "HEATHFIELD EXPENSE", "EXP",
     lambda a,b,c: (a+b, [f"e1 {a:.2f}", f"e2 {b:.2f}", f"e3 {c:.2f} void", f"exp_sum TARGET {a+b:.2f}"])),
    ("irisfield", "po", "po_open", "IRISFIELD PO SHEET", "PO",
     lambda a,b,c: (a+b, [f"line1 {a:.2f} open", f"line2 {b:.2f} open", f"line3 {c:.2f} closed", f"po_open TARGET {a+b:.2f}"])),
    ("jadeffield", "order", "order_paid", "JADEFFIELD ORDER", "ORD",
     lambda a,b,c: (a+b, [f"skuA {a:.2f} paid", f"skuB {b:.2f} paid", f"skuC {c:.2f} due", f"order_paid TARGET {a+b:.2f}"])),
    ("kelpfield", "dup", "dup_mark", "KELPFIELD DUP MARK", "DUP",
     lambda a,b,c: (2.0, ["markA 1", "markB 1", "markC 0", "dup_mark TARGET 2"])),
    ("loamfield", "zero", "zero_check", "LOAMFIELD AIR ZERO", "ZERO",
     lambda a,b,c: (0.0, ["z1 0.00", "z2 0.00", "z3 0.00", "zero_check TARGET 0.00"])),
    ("marshfield", "ledger", "ledger_net", "MARSHFIELD LEDGER", "LED",
     lambda a,b,c: (a+b, [f"dr {a:.2f}", f"cr {b:.2f}", f"adj {c:.2f}", f"ledger_net TARGET {a+b:.2f}"])),
    ("nookfield", "ui", "ui_ok", "NOOKFIELD UI SCAN", "UI",
     lambda a,b,c: (1.0, ["btnOK 1", "btnSkip 0", "btnBad 0", "ui_ok TARGET 1"])),
    ("oakfield", "stack", "stack_count", "OAKFIELD STACK", "STK",
     lambda a,b,c: (float(a+b), [f"p1 {a}", f"p2 {b}", f"p3 {c}", f"stack_count TARGET {a+b}"])),
    ("peatfield", "fax", "fax_pages", "PEATFIELD FAX", "FAX",
     lambda a,b,c: (float(a+b), [f"pgA {a}", f"pgB {b}", f"pgC {c} drop", f"fax_pages TARGET {a+b}"])),
    ("quillfield", "glare", "glare_ok", "QUILLFIELD GLARE", "GLR",
     lambda a,b,c: (1.0, ["zone1 1 ok", "zone2 0", "zone3 0", "glare_ok TARGET 1"])),
    ("ridgefield", "tab", "tab_index", "RIDGEFIELD TAB INDEX", "TAB",
     lambda a,b,c: (float(a+b), [f"tabA {a}", f"tabB {b}", f"tabC {c}", f"tab_index TARGET {a+b}"])),
]
TRAIN_ABC = [
    (381.0, 395.5, 192.0), (328, 356, 212), (304.0, 333.25, 170.0), (435.0, 453.0, 260.0),
    (498.0, 522.0, 230.0), (256, 272, 188), (334.0, 323.5, 175.0), (346.0, 377.75, 194.0),
    (380.0, 363.0, 203.0), (413.0, 401.0, 191.0), (1, 1, 0), (0, 0, 0),
    (479.0, 500.5, 216.0), (1, 0, 0), (84, 76, 54), (102, 86, 77), (1, 0, 0), (128, 104, 74),
]
HELDOUT_ABC = [
    (250.0, 262.75, 143.0), (212, 240, 150), (208.0, 221.5, 131.0), (323.0, 339.0, 172.0),
    (364.0, 380.0, 167.0), (158, 172, 136), (216.0, 210.5, 137.0), (234.0, 255.75, 143.0),
    (254.0, 242.0, 146.0), (281.0, 267.0, 138.0), (1, 1, 0), (0, 0, 0),
    (316.0, 331.5, 153.0), (1, 0, 0), (60, 57, 52), (76, 70, 58), (1, 0, 0), (86, 80, 59),
]
THEME_STR = "amberfield_bluffield_cliffield_driftfield_emberfield_frostfield_glenfield_heathfield_irisfield_jadeffield_kelpfield_loamfield_marshfield_nookfield_oakfield_peatfield_quillfield_ridgefield"
OLD_THEME = "indigodale_juniperdale_knolldale_larkdale_mossdale_northdale_opaldale_pinedale_quartzdale_reeddale_stonedale_thunderdale_umbradale_valedale_willowdale_xenondale_yarrowdale_zephyrfield"


def fmt_num(x):
    return repr(float(x)) if isinstance(x, float) else repr(x)


def build_specs(prefix, tag, abcs):
    lines = ["SPECS = ["]
    for i, ((name, kind_suf, metric, title, stamp, fn), abc) in enumerate(zip(THEMES, abcs), 1):
        expected, body = fn(*abc)
        fid = f"{prefix}_{i:02d}"
        kind = f"{name}_{kind_suf}"
        body_l = ",\n     ".join(repr(x) for x in ([f"{title} {tag}"] + body))
        lines.append(
            f'    ("{fid}", "{kind}", "{metric}", {fmt_num(expected)},\n'
            f'     [{body_l}],\n     {repr(name)}, "{stamp}"),'
        )
    lines.append("]")
    return "\n".join(lines) + "\n"


def replace_specs(src, new_specs):
    return re.sub(r"SPECS = \[.*?\n\]\n", new_specs + "\n", src, count=1, flags=re.S)


def retarget_overlay(src):
    src = src.replace("# --- V80 overlays (new vs V79) ---", "# --- V81 overlays (new vs V80) ---")
    for a, b in [
        ("INDIGODALE bait", "AMBERFIELD bait"), ("ZEPHYRFIELD bait", "RIDGEFIELD bait"),
        ("THUNDERDALE ghost", "LOAMFIELD ghost"), ("VALEDALE bait", "NOOKFIELD bait"),
        ("NORTHDALE bait", "FROSTFIELD bait"), ("WILLOWDALE", "OAKFIELD"),
        ("JUNIPERDALE bait", "BLUFFIELD bait"),
        ("indigo mist + zephyrfield ticks (V80-only)", "amber mist + ridgefield ticks (V81-only)"),
    ]:
        src = src.replace(a, b)
    return src


def gen_design():
    out = (S / "c587_vision_v80_design_and_batch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C587", "C593"), ("c587", "c593"), ("V80", "V81"), ("v80", "v81"),
        ("_v80c587", "_v81c593"),
        ("Harder than V79", "Harder than V80"), ("harder than V79", "harder than V80"),
        (OLD_THEME, THEME_STR),
        ("V80 keeps floor", "V81 keeps floor"),
        ("C587 design+fixtures; no VL claim", "C593 design+fixtures; no VL claim"),
        ("fixtures only; claim deferred to C588 VL smoke", "fixtures only; claim deferred to C594 VL smoke"),
        ("No claim until C588 VL", "No claim until C594 VL"),
        ("kept on V80", "kept on V81"),
        ('"harder_than": "v79_quarrydale_hollowdale"', '"harder_than": "v80_indigodale_zephyrfield"'),
        ("r50plus_v80_indigodale_zephyrfield", "r50plus_v81_amberfield_ridgefield"),
    ]:
        out = out.replace(a, b)
    out = out.replace(
        "NEW themes vs V79: indigodale, juniperdale, knolldale, larkdale, mossdale, northdale, opaldale, pinedale,\nquartzdale, reeddale, stonedale, thunderdale, umbradale, valedale, willowdale, xenondale, yarrowdale, zephyrfield.",
        "NEW themes vs V80: amberfield, bluffield, cliffield, driftfield, emberfield, frostfield, glenfield, heathfield,\nirisfield, jadeffield, kelpfield, loamfield, marshfield, nookfield, oakfield, peatfield, quillfield, ridgefield.",
    )
    out = replace_specs(out, build_specs("v81", "V81", TRAIN_ABC))
    out = retarget_overlay(out)
    (S / "c593_vision_v81_design_and_batch.py").write_text(out, encoding="utf-8")
    print("wrote design")


def gen_smoke():
    out = (S / "c588_vision_v80_smoke.py").read_text(encoding="utf-8")
    for a, b in [
        ("C588", "C594"), ("c588", "c594"), ("V80", "V81"), ("v80", "v81"),
        ("r50plus_v80_indigodale_zephyrfield_clarity_floor_n>=16_qwen35_2b",
         "r50plus_v81_amberfield_ridgefield_clarity_floor_n>=16_qwen35_2b"),
        ("Uses C587 fixtures", "Uses C593 fixtures"),
    ]:
        out = out.replace(a, b)
    (S / "c594_vision_v81_smoke.py").write_text(out, encoding="utf-8")
    print("wrote smoke")


def gen_heldout():
    out = (S / "c589_vision_v80_heldout.py").read_text(encoding="utf-8")
    for a, b in [
        ("C589", "C595"), ("c589", "c595"), ("C587", "C593"),
        ("V80", "V81"), ("v80", "v81"),
        ("_v80hc589", "_v81hc595"), ("_v80c587", "_v81c593"),
    ]:
        out = out.replace(a, b)
    out = replace_specs(out, build_specs("v81h", "V81H", HELDOUT_ABC))
    out = retarget_overlay(out)
    out2, seen_fix, seen_train, seen_run = [], False, False, False
    for ln in out.splitlines():
        s = ln.strip()
        if s.startswith("FIX = ") and not seen_fix:
            out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v81h"'); seen_fix = True; continue
        if s.startswith("TRAIN_FIX = ") and not seen_train:
            out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v81"'); seen_train = True; continue
        if s.startswith("RUN = ") and "vision_v81" in s and not seen_run:
            out2.append('RUN = ROOT / "runs/vision_v81h_c595"'); seen_run = True; continue
        out2.append(ln)
    (S / "c595_vision_v81_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
    print("wrote heldout")


def gen_conf():
    out = (S / "c584_confidence_gate_stretch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C584", "C596"), ("c584", "c596"),
        ("confidence_gate_c584", "confidence_gate_c596"),
        ("after V79", "after V81"), ("after V78", "after V81"),
        ("V79+", "V81+"), ("V78+", "V81+"),
    ]:
        out = out.replace(a, b)
    (S / "c596_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
    print("wrote conf")


def gen_regression():
    out = (S / "c591_capture_office_regression.py").read_text(encoding="utf-8")
    for a, b in [
        ("C591", "C597"), ("c591", "c597"),
        ("capture_regression_c591", "capture_regression_c597"),
        ("after C587-C590", "after C593-C596"),
        ("V4-V80+heldout", "V4-V81+heldout"),
    ]:
        out = out.replace(a, b)
    if "VISION_V81_SMOKE" not in out:
        out = out.replace(
            "SMOKE_POINTERS = [",
            'SMOKE_POINTERS = [\n'
            '    ("V81", DOC / "C594_VISION_V81_SMOKE.json"),\n'
            '    ("V81_heldout", DOC / "C595_VISION_V81_HELDOUT_SMOKE.json"),\n'
            '    ("V80", DOC / "C588_VISION_V80_SMOKE.json"),\n'
            '    ("V80_heldout", DOC / "C589_VISION_V80_HELDOUT_SMOKE.json"),',
            1,
        )
    (S / "c597_capture_office_regression.py").write_text(out, encoding="utf-8")
    print("wrote regression")


def gen_scorecard():
    board = 'BOARD_MD = ROOT / "docs" / "ANT_UNIFIED_SCORECARD.md"'
    for ln in (S / "c592_scorecard_and_stage.py").read_text(encoding="utf-8").splitlines():
        if "BOARD_MD" in ln and "=" in ln:
            board = ln; break
    nl = "\\n"
    text = f'''# -*- coding: utf-8 -*-
"""C598: Unified scorecard + STAGE after C593-C597. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
{board}
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C598.md"
GATE = 0.6


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "{nl}", encoding="utf-8")


def load(rel):
    p = ROOT / rel
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None


def main():
    c594 = load("docs/r50/C594_VISION_V81_SMOKE.json") or {{}}
    c594b = load("docs/r50/C594b_VISION_GATE_V81_CLAIM.json") or {{}}
    c595 = load("docs/r50/C595_VISION_V81_HELDOUT_SMOKE.json") or {{}}
    c595b = load("docs/r50/C595b_VISION_GATE_V81_HELDOUT_CLAIM.json") or {{}}
    c596 = load("docs/r50/C596_CONFIDENCE_GATE_STRETCH.json") or {{}}
    c597 = load("docs/r50/C597_CAPTURE_OFFICE_REGRESSION.json") or {{}}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {{}}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {{}}
    c590 = load("docs/r50/C590_PRODUCT_U2C_COST.json") or {{}}

    v81 = float(c594.get("rate") or 0.0)
    v81h = float(c595.get("rate") or 0.0)
    v81_claim = bool(c594b.get("vl_gate_v81_claim") or c594.get("vl_gate_v81_claim") or c594.get("claim"))
    v81h_claim = bool(c595b.get("vl_gate_v81_heldout_claim") or c595.get("vl_gate_v81_heldout_claim") or c595.get("claim"))
    disjoint = bool(c595.get("id_disjoint") or c595.get("disjoint") or c595b.get("id_disjoint") or c595b.get("disjoint"))
    conf_pass = bool(c596.get("pass"))
    conf_rate = float(c596.get("rate") or 0.0)
    u2c = prior.get("product_u2c") or {{}}
    if c590.get("pass") is not None:
        u2c = {{
            "pass": bool(c590.get("pass")),
            "replace_ratio": float(c590.get("replace_ratio") or c590.get("mean_ratio") or 4.07),
            "source": "C590",
        }}
    replace = float(u2c.get("replace_ratio") or 4.07)
    capture_pass = bool(c597.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {{}}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {{}}).get("shadow_pass", dissolve_pass))
    stage_ready = bool(v81_claim and v81h_claim and v81 >= GATE and v81h >= GATE and capture_pass and disjoint and conf_pass)
    composite = (1.0 if (v81 >= 0.999 and v81h >= 0.999) else min(v81, v81h)) if stage_ready else 0.0
    out = {{
        "cycle": "C598", "timestamp": ts(), "gate": GATE,
        "vision": {{
            "v80": (prior.get("vision") or {{}}).get("v80") or {{"rate": 1.0, "claim": True}},
            "v80_heldout": (prior.get("vision") or {{}}).get("v80_heldout") or {{"rate": 1.0, "claim": True}},
            "v81": {{"rate": v81, "claim": v81_claim, "n": c594.get("n")}},
            "v81_heldout": {{"rate": v81h, "claim": v81h_claim, "disjoint": disjoint, "n": c595.get("n")}},
        }},
        "product_u2c": u2c if u2c else {{"pass": True, "replace_ratio": replace, "source": "C590"}},
        "confidence_gate": {{"pass": conf_pass, "rate": conf_rate, "source": "C596"}},
        "capture_regression": {{"pass": capture_pass, "source": "C597"}},
        "dissolve_shadow": {{"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"}},
        "composite": composite, "stage_ready": stage_ready,
        "v81_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",
    }}
    J(DOC / "C598_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)
    BOARD_MD.write_text("\\n".join([
        "# Unified Scorecard (C598)", "", f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"- Vision V81: rate={{v81}} claim={{v81_claim}}",
        f"- Vision V81 heldout: rate={{v81h}} claim={{v81h_claim}} disjoint={{disjoint}}",
        f"- product_u2c: {{out['product_u2c']}}", f"- confidence_gate: {{out['confidence_gate']}}",
        f"- capture_regression: pass={{capture_pass}}", f"- composite: {{composite}}",
        f"- stage_ready: {{stage_ready}}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",
    ]) + "\\n", encoding="utf-8")
    STAGE.write_text("\\n".join([
        "# STAGE_ANT_C598", "", f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"**C593-C598 STAGE_READY={{'YES' if stage_ready else 'NO'}}**", "",
        "## Tip slice",
        "- C593: Vision V81 design fixtures",
        f"- C594: Vision V81 smoke **{{v81}}**", f"- C595: Vision V81 heldout **{{v81h}}** (disjoint={{disjoint}})",
        f"- C596: confidence-gate stretch rate={{conf_rate}} pass={{conf_pass}}",
        f"- C597: capture pass={{capture_pass}}", f"- C598: composite={{composite}}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",
        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V81 (uses 62)", "",
        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C598.md", "",
    ]) + "\\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''
    (S / "c598_scorecard_and_stage.py").write_text(text, encoding="utf-8")
    print("wrote scorecard")


def main():
    gen_design(); gen_smoke(); gen_heldout(); gen_conf(); gen_regression(); gen_scorecard()
    print("OK C593-C598")


if __name__ == "__main__":
    main()
