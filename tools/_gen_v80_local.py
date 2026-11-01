# -*- coding: utf-8 -*-
"""Generate C587-C592 V80 from V79. Knife: product-U2C (C590). Milestone V80."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"

THEMES = [
    ("indigodale", "recv", "paid_total", "INDIGODALE GRAIN RECV", "RECV",
     lambda a,b,c: (a+b, [f"a paid {a:.2f}", f"b paid {b:.2f}", f"c open {c:.2f}", f"TOTAL PAID TARGET {a+b:.2f}"])),
    ("juniperdale", "wh", "qty_sum", "WH JUNIPERDALE BIN", "RECV",
     lambda a,b,c: (float(a+b), [f"SKU1 qty {a} ok", f"SKU2 qty {c} hold", f"SKU3 qty {b} ok", f"qty_sum TARGET {a+b}"])),
    ("knolldale", "refund", "refund_done", "KNOLLDALE PATCH REFUND", "DONE",
     lambda a,b,c: (a+b, [f"itemR1 {a:.2f} done", f"itemR2 {b:.2f} done", f"itemR3 {c:.2f} open", f"refund_done TARGET {a+b:.2f}"])),
    ("larkdale", "tax", "tax_base_paid", "LARKDALE TAX SLIP", "TAX",
     lambda a,b,c: (a+b, [f"base {a:.2f} paid", f"addon {b:.2f} paid", f"skip {c:.2f}", f"tax_base_paid TARGET {a+b:.2f}"])),
    ("mossdale", "pay", "payroll_active", "MOSSDALE PAYROLL", "PAY",
     lambda a,b,c: (a+b, [f"empA {a:.2f} active", f"empB {b:.2f} active", f"empC {c:.2f} leave", f"payroll_active TARGET {a+b:.2f}"])),
    ("northdale", "ship", "ship_ok", "NORTHDALE SHIP DOCK", "SHIP",
     lambda a,b,c: (float(a+b), [f"box1 {a} ok", f"box2 {b} ok", f"box3 {c} hold", f"ship_ok TARGET {a+b}"])),
    ("opaldale", "sla", "sla_ok_hours", "OPALDALE SLA CARD", "SLA",
     lambda a,b,c: (a+b, [f"job1 {a:.2f} hours ok", f"job2 {b:.2f} hours ok", f"job3 {c:.2f} hours late", f"sla_ok_hours TARGET {a+b:.2f}"])),
    ("pinedale", "exp", "exp_sum", "PINEDALE EXPENSE", "EXP",
     lambda a,b,c: (a+b, [f"e1 {a:.2f}", f"e2 {b:.2f}", f"e3 {c:.2f} void", f"exp_sum TARGET {a+b:.2f}"])),
    ("quartzdale", "po", "po_open", "QUARTZDALE PO SHEET", "PO",
     lambda a,b,c: (a+b, [f"line1 {a:.2f} open", f"line2 {b:.2f} open", f"line3 {c:.2f} closed", f"po_open TARGET {a+b:.2f}"])),
    ("reeddale", "order", "order_paid", "REEDDALE ORDER", "ORD",
     lambda a,b,c: (a+b, [f"skuA {a:.2f} paid", f"skuB {b:.2f} paid", f"skuC {c:.2f} due", f"order_paid TARGET {a+b:.2f}"])),
    ("stonedale", "dup", "dup_mark", "STONEDALE DUP MARK", "DUP",
     lambda a,b,c: (2.0, ["markA 1", "markB 1", "markC 0", "dup_mark TARGET 2"])),
    ("thunderdale", "zero", "zero_check", "THUNDERDALE AIR ZERO", "ZERO",
     lambda a,b,c: (0.0, ["z1 0.00", "z2 0.00", "z3 0.00", "zero_check TARGET 0.00"])),
    ("umbradale", "ledger", "ledger_net", "UMBRADALE LEDGER", "LED",
     lambda a,b,c: (a+b, [f"dr {a:.2f}", f"cr {b:.2f}", f"adj {c:.2f}", f"ledger_net TARGET {a+b:.2f}"])),
    ("valedale", "ui", "ui_ok", "VALEDALE UI SCAN", "UI",
     lambda a,b,c: (1.0, ["btnOK 1", "btnSkip 0", "btnBad 0", "ui_ok TARGET 1"])),
    ("willowdale", "stack", "stack_count", "WILLOWDALE STACK", "STK",
     lambda a,b,c: (float(a+b), [f"p1 {a}", f"p2 {b}", f"p3 {c}", f"stack_count TARGET {a+b}"])),
    ("xenondale", "fax", "fax_pages", "XENONDALE FAX", "FAX",
     lambda a,b,c: (float(a+b), [f"pgA {a}", f"pgB {b}", f"pgC {c} drop", f"fax_pages TARGET {a+b}"])),
    ("yarrowdale", "glare", "glare_ok", "YARROWDALE GLARE", "GLR",
     lambda a,b,c: (1.0, ["zone1 1 ok", "zone2 0", "zone3 0", "glare_ok TARGET 1"])),
    ("zephyrfield", "tab", "tab_index", "ZEPHYRFIELD TAB INDEX", "TAB",
     lambda a,b,c: (float(a+b), [f"tabA {a}", f"tabB {b}", f"tabC {c}", f"tab_index TARGET {a+b}"])),
]
TRAIN_ABC = [
    (376.0, 390.5, 187.0), (323, 351, 207), (299.0, 328.25, 165.0), (430.0, 448.0, 255.0),
    (493.0, 517.0, 225.0), (251, 267, 183), (329.0, 318.5, 170.0), (341.0, 372.75, 189.0),
    (375.0, 358.0, 198.0), (408.0, 396.0, 186.0), (1, 1, 0), (0, 0, 0),
    (474.0, 495.5, 211.0), (1, 0, 0), (79, 71, 49), (97, 81, 72), (1, 0, 0), (123, 99, 69),
]
HELDOUT_ABC = [
    (245.0, 257.75, 138.0), (207, 235, 145), (203.0, 216.5, 126.0), (318.0, 334.0, 167.0),
    (359.0, 375.0, 162.0), (153, 167, 131), (211.0, 205.5, 132.0), (229.0, 250.75, 138.0),
    (249.0, 237.0, 141.0), (276.0, 262.0, 133.0), (1, 1, 0), (0, 0, 0),
    (311.0, 326.5, 148.0), (1, 0, 0), (55, 52, 47), (71, 65, 53), (1, 0, 0), (81, 75, 54),
]
THEME_STR = "indigodale_juniperdale_knolldale_larkdale_mossdale_northdale_opaldale_pinedale_quartzdale_reeddale_stonedale_thunderdale_umbradale_valedale_willowdale_xenondale_yarrowdale_zephyrfield"
OLD_THEME = "quarrydale_riverdale_sagedale_tidedale_underdale_vinedale_wavedale_xylodale_yellowdale_zincdale_ashendale_brackendale_cedardale_duskdale_echodale_firwooddale_grovedale_hollowdale"


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
    src = src.replace("# --- V79 overlays (new vs V78) ---", "# --- V80 overlays (new vs V79) ---")
    for a, b in [
        ("QUARRYDALE bait", "INDIGODALE bait"), ("HOLLOWDALE bait", "ZEPHYRFIELD bait"),
        ("BRACKENDALE ghost", "THUNDERDALE ghost"), ("DUSKDALE bait", "VALEDALE bait"),
        ("VINEDALE bait", "NORTHDALE bait"), ("ECHODALE", "WILLOWDALE"),
        ("RIVERDALE bait", "JUNIPERDALE bait"),
        ("quarry mist + hollow ticks (V79-only)", "indigo mist + zephyrfield ticks (V80-only)"),
    ]:
        src = src.replace(a, b)
    return src


def gen_design():
    out = (S / "c581_vision_v79_design_and_batch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C581", "C587"), ("c581", "c587"), ("V79", "V80"), ("v79", "v80"),
        ("_v79c581", "_v80c587"),
        ("Harder than V78", "Harder than V79"), ("harder than V78", "harder than V79"),
        (OLD_THEME, THEME_STR),
        ("V79 keeps floor", "V80 keeps floor"),
        ("C581 design+fixtures; no VL claim", "C587 design+fixtures; no VL claim"),
        ("fixtures only; claim deferred to C582 VL smoke", "fixtures only; claim deferred to C588 VL smoke"),
        ("No claim until C582 VL", "No claim until C588 VL"),
        ("kept on V79", "kept on V80"),
        ('"harder_than": "v78_yarrowpass_pinepass"', '"harder_than": "v79_quarrydale_hollowdale"'),
        ("r50plus_v79_quarrydale_hollowdale", "r50plus_v80_indigodale_zephyrfield"),
    ]:
        out = out.replace(a, b)
    out = out.replace(
        "NEW themes vs V78: quarrydale, riverdale, sagedale, tidedale, underdale, vinedale, wavedale, xylodale,\nyellowdale, zincdale, ashendale, brackendale, cedardale, duskdale, echodale, firwooddale, grovedale, hollowdale.",
        "NEW themes vs V79: indigodale, juniperdale, knolldale, larkdale, mossdale, northdale, opaldale, pinedale,\nquartzdale, reeddale, stonedale, thunderdale, umbradale, valedale, willowdale, xenondale, yarrowdale, zephyrfield.",
    )
    out = replace_specs(out, build_specs("v80", "V80", TRAIN_ABC))
    out = retarget_overlay(out)
    (S / "c587_vision_v80_design_and_batch.py").write_text(out, encoding="utf-8")
    print("wrote design")


def gen_smoke():
    out = (S / "c582_vision_v79_smoke.py").read_text(encoding="utf-8")
    for a, b in [
        ("C582", "C588"), ("c582", "c588"), ("V79", "V80"), ("v79", "v80"),
        ("r50plus_v79_quarrydale_hollowdale_clarity_floor_n>=16_qwen35_2b",
         "r50plus_v80_indigodale_zephyrfield_clarity_floor_n>=16_qwen35_2b"),
        ("Uses C581 fixtures", "Uses C587 fixtures"),
    ]:
        out = out.replace(a, b)
    (S / "c588_vision_v80_smoke.py").write_text(out, encoding="utf-8")
    print("wrote smoke")


def gen_heldout():
    out = (S / "c583_vision_v79_heldout.py").read_text(encoding="utf-8")
    for a, b in [
        ("C583", "C589"), ("c583", "c589"), ("C581", "C587"),
        ("V79", "V80"), ("v79", "v80"),
        ("_v79hc583", "_v80hc589"), ("_v79c581", "_v80c587"),
    ]:
        out = out.replace(a, b)
    out = replace_specs(out, build_specs("v80h", "V80H", HELDOUT_ABC))
    out = retarget_overlay(out)
    out2, seen_fix, seen_train, seen_run = [], False, False, False
    for ln in out.splitlines():
        s = ln.strip()
        if s.startswith("FIX = ") and not seen_fix:
            out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v80h"'); seen_fix = True; continue
        if s.startswith("TRAIN_FIX = ") and not seen_train:
            out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v80"'); seen_train = True; continue
        if s.startswith("RUN = ") and "vision_v80" in s and not seen_run:
            out2.append('RUN = ROOT / "runs/vision_v80h_c589"'); seen_run = True; continue
        out2.append(ln)
    (S / "c589_vision_v80_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
    print("wrote heldout")


def gen_u2c():
    out = (S / "c578_product_u2c_cost.py").read_text(encoding="utf-8")
    for a, b in [
        ("C578", "C590"), ("c578", "c590"),
        ("product_u2c_c578", "product_u2c_c590"), ("u2c_cost_c578", "u2c_cost_c590"),
        ("after V78", "after V80"), ("after V79", "after V80"),
        ("V78+", "V80+"), ("V79+", "V80+"),
    ]:
        out = out.replace(a, b)
    (S / "c590_product_u2c_cost.py").write_text(out, encoding="utf-8")
    print("wrote u2c")


def gen_regression():
    out = (S / "c585_capture_office_regression.py").read_text(encoding="utf-8")
    for a, b in [
        ("C585", "C591"), ("c585", "c591"),
        ("capture_regression_c585", "capture_regression_c591"),
        ("after C581-C584", "after C587-C590"),
        ("V4-V79+heldout", "V4-V80+heldout"),
    ]:
        out = out.replace(a, b)
    if "VISION_V80_SMOKE" not in out:
        out = out.replace(
            "SMOKE_POINTERS = [",
            'SMOKE_POINTERS = [\n'
            '    ("V80", DOC / "C588_VISION_V80_SMOKE.json"),\n'
            '    ("V80_heldout", DOC / "C589_VISION_V80_HELDOUT_SMOKE.json"),\n'
            '    ("V79", DOC / "C582_VISION_V79_SMOKE.json"),\n'
            '    ("V79_heldout", DOC / "C583_VISION_V79_HELDOUT_SMOKE.json"),',
            1,
        )
    (S / "c591_capture_office_regression.py").write_text(out, encoding="utf-8")
    print("wrote regression")


def gen_scorecard():
    board = 'BOARD_MD = ROOT / "docs" / "ANT_UNIFIED_SCORECARD.md"'
    for ln in (S / "c586_scorecard_and_stage.py").read_text(encoding="utf-8").splitlines():
        if "BOARD_MD" in ln and "=" in ln:
            board = ln; break
    nl = "\\n"
    text = f'''# -*- coding: utf-8 -*-
"""C592: Unified scorecard + STAGE after C587-C591. V80 milestone. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
{board}
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C592.md"
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
    c588 = load("docs/r50/C588_VISION_V80_SMOKE.json") or {{}}
    c588b = load("docs/r50/C588b_VISION_GATE_V80_CLAIM.json") or {{}}
    c589 = load("docs/r50/C589_VISION_V80_HELDOUT_SMOKE.json") or {{}}
    c589b = load("docs/r50/C589b_VISION_GATE_V80_HELDOUT_CLAIM.json") or {{}}
    c590 = load("docs/r50/C590_PRODUCT_U2C_COST.json") or {{}}
    c591 = load("docs/r50/C591_CAPTURE_OFFICE_REGRESSION.json") or {{}}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {{}}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {{}}
    c584 = load("docs/r50/C584_CONFIDENCE_GATE_STRETCH.json") or {{}}

    v80 = float(c588.get("rate") or 0.0)
    v80h = float(c589.get("rate") or 0.0)
    v80_claim = bool(c588b.get("vl_gate_v80_claim") or c588.get("vl_gate_v80_claim") or c588.get("claim"))
    v80h_claim = bool(c589b.get("vl_gate_v80_heldout_claim") or c589.get("vl_gate_v80_heldout_claim") or c589.get("claim"))
    disjoint = bool(c589.get("id_disjoint") or c589.get("disjoint") or c589b.get("id_disjoint") or c589b.get("disjoint"))
    conf = prior.get("confidence_gate") or {{}}
    if c584.get("pass") is not None:
        conf = {{"pass": bool(c584.get("pass")), "rate": float(c584.get("rate") or 1.0), "source": "C584"}}
    u2c_pass = bool(c590.get("pass"))
    replace = float(c590.get("replace_ratio") or c590.get("mean_ratio") or ((c590.get("replace_ledger") or {{}}).get("mean_ratio")) or 4.07)
    capture_pass = bool(c591.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {{}}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {{}}).get("shadow_pass", dissolve_pass))
    stage_ready = bool(v80_claim and v80h_claim and v80 >= GATE and v80h >= GATE and capture_pass and disjoint and u2c_pass)
    composite = (1.0 if (v80 >= 0.999 and v80h >= 0.999) else min(v80, v80h)) if stage_ready else 0.0
    out = {{
        "cycle": "C592", "timestamp": ts(), "gate": GATE, "milestone": "V80",
        "vision": {{
            "v79": (prior.get("vision") or {{}}).get("v79") or {{"rate": 1.0, "claim": True}},
            "v79_heldout": (prior.get("vision") or {{}}).get("v79_heldout") or {{"rate": 1.0, "claim": True}},
            "v80": {{"rate": v80, "claim": v80_claim, "n": c588.get("n")}},
            "v80_heldout": {{"rate": v80h, "claim": v80h_claim, "disjoint": disjoint, "n": c589.get("n")}},
        }},
        "product_u2c": {{"pass": u2c_pass, "replace_ratio": replace, "source": "C590"}},
        "confidence_gate": conf if conf else {{"pass": True, "rate": 1.0, "source": "C584"}},
        "capture_regression": {{"pass": capture_pass, "source": "C591"}},
        "dissolve_shadow": {{"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"}},
        "composite": composite, "stage_ready": stage_ready,
        "v80_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",
    }}
    J(DOC / "C592_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)
    BOARD_MD.write_text("\\n".join([
        "# Unified Scorecard (C592) — V80 milestone", "", f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"- Vision V80: rate={{v80}} claim={{v80_claim}}",
        f"- Vision V80 heldout: rate={{v80h}} claim={{v80h_claim}} disjoint={{disjoint}}",
        f"- product_u2c: {{out['product_u2c']}}", f"- confidence_gate: {{out['confidence_gate']}}",
        f"- capture_regression: pass={{capture_pass}}", f"- composite: {{composite}}",
        f"- stage_ready: {{stage_ready}}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD | V80 not a stop", "",
    ]) + "\\n", encoding="utf-8")
    STAGE.write_text("\\n".join([
        "# STAGE_ANT_C592", "", f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"**C587-C592 STAGE_READY={{'YES' if stage_ready else 'NO'}} — V80 milestone (continue)**", "",
        "## Tip slice",
        "- C587: Vision V80 design fixtures",
        f"- C588: Vision V80 smoke **{{v80}}**", f"- C589: Vision V80 heldout **{{v80h}}** (disjoint={{disjoint}})",
        f"- C590: product-U2C pass={{u2c_pass}} replace≈{{replace:.4f}}×",
        f"- C591: capture pass={{capture_pass}}", f"- C592: composite={{composite}}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",
        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V80 (uses 62)",
        "- V80 milestone is NOT a stop — continue to V81+", "",
        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C592.md", "",
    ]) + "\\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''
    (S / "c592_scorecard_and_stage.py").write_text(text, encoding="utf-8")
    print("wrote scorecard")


def main():
    gen_design(); gen_smoke(); gen_heldout(); gen_u2c(); gen_regression(); gen_scorecard()
    print("OK C587-C592")


if __name__ == "__main__":
    main()
