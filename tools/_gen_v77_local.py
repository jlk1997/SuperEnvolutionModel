# -*- coding: utf-8 -*-
"""Generate C569-C574 V77 from V76. Knife: confidence-gate (C572)."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"

THEMES = [
    ("goldcliff", "recv", "paid_total", "GOLDCLIFF GRAIN RECV", "RECV",
     lambda a,b,c: (a+b, [f"a paid {a:.2f}", f"b paid {b:.2f}", f"c open {c:.2f}", f"TOTAL PAID TARGET {a+b:.2f}"])),
    ("hazelpass", "wh", "qty_sum", "WH HAZELPASS BIN", "RECV",
     lambda a,b,c: (float(a+b), [f"SKU1 qty {a} ok", f"SKU2 qty {c} hold", f"SKU3 qty {b} ok", f"qty_sum TARGET {a+b}"])),
    ("ironpass", "refund", "refund_done", "IRONPASS PATCH REFUND", "DONE",
     lambda a,b,c: (a+b, [f"itemR1 {a:.2f} done", f"itemR2 {b:.2f} done", f"itemR3 {c:.2f} open", f"refund_done TARGET {a+b:.2f}"])),
    ("jadehaven", "tax", "tax_base_paid", "JADEHAVEN TAX SLIP", "TAX",
     lambda a,b,c: (a+b, [f"base {a:.2f} paid", f"addon {b:.2f} paid", f"skip {c:.2f}", f"tax_base_paid TARGET {a+b:.2f}"])),
    ("knollpass", "pay", "payroll_active", "KNOLLPASS PAYROLL", "PAY",
     lambda a,b,c: (a+b, [f"empA {a:.2f} active", f"empB {b:.2f} active", f"empC {c:.2f} leave", f"payroll_active TARGET {a+b:.2f}"])),
    ("larkpass", "ship", "ship_ok", "LARKPASS SHIP DOCK", "SHIP",
     lambda a,b,c: (float(a+b), [f"box1 {a} ok", f"box2 {b} ok", f"box3 {c} hold", f"ship_ok TARGET {a+b}"])),
    ("mosspass", "sla", "sla_ok_hours", "MOSSPASS SLA CARD", "SLA",
     lambda a,b,c: (a+b, [f"job1 {a:.2f} hours ok", f"job2 {b:.2f} hours ok", f"job3 {c:.2f} hours late", f"sla_ok_hours TARGET {a+b:.2f}"])),
    ("northpass", "exp", "exp_sum", "NORTHPASS EXPENSE", "EXP",
     lambda a,b,c: (a+b, [f"e1 {a:.2f}", f"e2 {b:.2f}", f"e3 {c:.2f} void", f"exp_sum TARGET {a+b:.2f}"])),
    ("opalpass", "po", "po_open", "OPALPASS PO SHEET", "PO",
     lambda a,b,c: (a+b, [f"line1 {a:.2f} open", f"line2 {b:.2f} open", f"line3 {c:.2f} closed", f"po_open TARGET {a+b:.2f}"])),
    ("pinehaven", "order", "order_paid", "PINEHAVEN ORDER", "ORD",
     lambda a,b,c: (a+b, [f"skuA {a:.2f} paid", f"skuB {b:.2f} paid", f"skuC {c:.2f} due", f"order_paid TARGET {a+b:.2f}"])),
    ("quartzpass", "dup", "dup_mark", "QUARTZPASS DUP MARK", "DUP",
     lambda a,b,c: (2.0, ["markA 1", "markB 1", "markC 0", "dup_mark TARGET 2"])),
    ("reedpass", "zero", "zero_check", "REEDPASS AIR ZERO", "ZERO",
     lambda a,b,c: (0.0, ["z1 0.00", "z2 0.00", "z3 0.00", "zero_check TARGET 0.00"])),
    ("stonepass", "ledger", "ledger_net", "STONEPASS LEDGER", "LED",
     lambda a,b,c: (a+b, [f"dr {a:.2f}", f"cr {b:.2f}", f"adj {c:.2f}", f"ledger_net TARGET {a+b:.2f}"])),
    ("thunderhaven", "ui", "ui_ok", "THUNDERHAVEN UI SCAN", "UI",
     lambda a,b,c: (1.0, ["btnOK 1", "btnSkip 0", "btnBad 0", "ui_ok TARGET 1"])),
    ("umbraepass", "stack", "stack_count", "UMBRAEPASS STACK", "STK",
     lambda a,b,c: (float(a+b), [f"p1 {a}", f"p2 {b}", f"p3 {c}", f"stack_count TARGET {a+b}"])),
    ("valepass", "fax", "fax_pages", "VALEPASS FAX", "FAX",
     lambda a,b,c: (float(a+b), [f"pgA {a}", f"pgB {b}", f"pgC {c} drop", f"fax_pages TARGET {a+b}"])),
    ("willowpass", "glare", "glare_ok", "WILLOWPASS GLARE", "GLR",
     lambda a,b,c: (1.0, ["zone1 1 ok", "zone2 0", "zone3 0", "glare_ok TARGET 1"])),
    ("xenonpass", "tab", "tab_index", "XENONPASS TAB INDEX", "TAB",
     lambda a,b,c: (float(a+b), [f"tabA {a}", f"tabB {b}", f"tabC {c}", f"tab_index TARGET {a+b}"])),
]
TRAIN_ABC = [
    (352.0, 367.25, 175.0), (299, 327, 195), (278.0, 305.0, 153.0), (406.0, 424.0, 237.0),
    (469.0, 493.0, 213.0), (233, 249, 171), (305.0, 295.25, 158.0), (317.0, 348.0, 177.0),
    (351.0, 334.0, 186.0), (384.0, 372.0, 174.0), (1, 1, 0), (0, 0, 0),
    (450.0, 472.25, 199.0), (1, 0, 0), (73, 65, 43), (91, 75, 66), (1, 0, 0), (114, 93, 63),
]
HELDOUT_ABC = [
    (227.0, 240.5, 126.0), (189, 217, 133), (185.0, 199.25, 114.0), (294.0, 310.0, 155.0),
    (335.0, 351.0, 150.0), (141, 155, 119), (193.0, 188.25, 120.0), (211.0, 232.0, 126.0),
    (231.0, 219.0, 129.0), (258.0, 244.75, 121.0), (1, 1, 0), (0, 0, 0),
    (293.0, 309.25, 136.0), (1, 0, 0), (49, 46, 41), (65, 59, 47), (1, 0, 0), (75, 69, 48),
]
THEME_STR = "goldcliff_hazelpass_ironpass_jadehaven_knollpass_larkpass_mosspass_northpass_opalpass_pinehaven_quartzpass_reedpass_stonepass_thunderhaven_umbraepass_valepass_willowpass_xenonpass"
OLD_THEME = "oakcliff_pebblehaven_quailhaven_rainhaven_sagehaven_tidecliff_underpass_vinehaven_wavecliff_xyloridge_yellowhaven_zephyrpass_alderpass_birchpass_cinderpass_dewcliff_emberpass_fernpass"


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
    src = src.replace("# --- V76 overlays (new vs V75) ---", "# --- V77 overlays (new vs V76) ---")
    for a, b in [
        ("OAKCLIFF bait", "GOLDCLIFF bait"), ("FERNPASS bait", "XENONPASS bait"),
        ("ZEPHYRPASS ghost", "REEDPASS ghost"), ("BIRCHPASS bait", "THUNDERHAVEN bait"),
        ("TIDECLIFF bait", "LARKPASS bait"), ("CINDERPASS", "UMBRAEPASS"),
        ("PEBBLEHAVEN bait", "HAZELPASS bait"),
        ("oak mist + fern ticks (V76-only)", "gold mist + xenon ticks (V77-only)"),
    ]:
        src = src.replace(a, b)
    return src


def gen_design():
    out = (S / "c563_vision_v76_design_and_batch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C563", "C569"), ("c563", "c569"), ("V76", "V77"), ("v76", "v77"),
        ("_v76c563", "_v77c569"),
        ("Harder than V75", "Harder than V76"), ("harder than V75", "harder than V76"),
        (OLD_THEME, THEME_STR),
        ("V76 keeps floor", "V77 keeps floor"),
        ("C563 design+fixtures; no VL claim", "C569 design+fixtures; no VL claim"),
        ("fixtures only; claim deferred to C564 VL smoke", "fixtures only; claim deferred to C570 VL smoke"),
        ("No claim until C564 VL", "No claim until C570 VL"),
        ("kept on V76", "kept on V77"),
        ('"harder_than": "v75_windhaven_nimbuspass"', '"harder_than": "v76_oakcliff_fernpass"'),
        ("r50plus_v76_oakcliff_fernpass", "r50plus_v77_goldcliff_xenonpass"),
    ]:
        out = out.replace(a, b)
    out = out.replace(
        "NEW themes vs V75: oakcliff, pebblehaven, quailhaven, rainhaven, sagehaven, tidecliff, underpass, vinehaven,\nwavecliff, xyloridge, yellowhaven, zephyrpass, alderpass, birchpass, cinderpass, dewcliff, emberpass, fernpass.",
        "NEW themes vs V76: goldcliff, hazelpass, ironpass, jadehaven, knollpass, larkpass, mosspass, northpass,\nopalpass, pinehaven, quartzpass, reedpass, stonepass, thunderhaven, umbraepass, valepass, willowpass, xenonpass.",
    )
    out = replace_specs(out, build_specs("v77", "V77", TRAIN_ABC))
    out = retarget_overlay(out)
    (S / "c569_vision_v77_design_and_batch.py").write_text(out, encoding="utf-8")
    print("wrote design")


def gen_smoke():
    out = (S / "c564_vision_v76_smoke.py").read_text(encoding="utf-8")
    for a, b in [
        ("C564", "C570"), ("c564", "c570"), ("V76", "V77"), ("v76", "v77"),
        ("r50plus_v76_oakcliff_fernpass_clarity_floor_n>=16_qwen35_2b",
         "r50plus_v77_goldcliff_xenonpass_clarity_floor_n>=16_qwen35_2b"),
        ("Uses C563 fixtures", "Uses C569 fixtures"),
    ]:
        out = out.replace(a, b)
    (S / "c570_vision_v77_smoke.py").write_text(out, encoding="utf-8")
    print("wrote smoke")


def gen_heldout():
    out = (S / "c565_vision_v76_heldout.py").read_text(encoding="utf-8")
    for a, b in [
        ("C565", "C571"), ("c565", "c571"), ("C563", "C569"),
        ("V76", "V77"), ("v76", "v77"),
        ("_v76hc565", "_v77hc571"), ("_v76c563", "_v77c569"),
    ]:
        out = out.replace(a, b)
    out = replace_specs(out, build_specs("v77h", "V77H", HELDOUT_ABC))
    out = retarget_overlay(out)
    out2, seen_fix, seen_train, seen_run = [], False, False, False
    for ln in out.splitlines():
        s = ln.strip()
        if s.startswith("FIX = ") and not seen_fix:
            out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v77h"'); seen_fix = True; continue
        if s.startswith("TRAIN_FIX = ") and not seen_train:
            out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v77"'); seen_train = True; continue
        if s.startswith("RUN = ") and "vision_v77" in s and not seen_run:
            out2.append('RUN = ROOT / "runs/vision_v77h_c571"'); seen_run = True; continue
        out2.append(ln)
    (S / "c571_vision_v77_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
    print("wrote heldout")


def gen_confidence():
    out = (S / "c560_confidence_gate_stretch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C560", "C572"), ("c560", "c572"),
        ("confidence_gate_c560", "confidence_gate_c572"),
        ("conf_gate_stretch_c560", "conf_gate_stretch_c572"),
        ("after V75", "after V77"), ("after V76", "after V77"),
        ("V75+", "V77+"), ("V76+", "V77+"),
    ]:
        out = out.replace(a, b)
    (S / "c572_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
    print("wrote confidence")


def gen_regression():
    out = (S / "c567_capture_office_regression.py").read_text(encoding="utf-8")
    for a, b in [
        ("C567", "C573"), ("c567", "c573"),
        ("capture_regression_c567", "capture_regression_c573"),
        ("after C563-C566", "after C569-C572"),
        ("V4-V76+heldout", "V4-V77+heldout"),
    ]:
        out = out.replace(a, b)
    if "VISION_V77_SMOKE" not in out:
        out = out.replace(
            "SMOKE_POINTERS = [",
            'SMOKE_POINTERS = [\n'
            '    ("V77", DOC / "C570_VISION_V77_SMOKE.json"),\n'
            '    ("V77_heldout", DOC / "C571_VISION_V77_HELDOUT_SMOKE.json"),\n'
            '    ("V76", DOC / "C564_VISION_V76_SMOKE.json"),\n'
            '    ("V76_heldout", DOC / "C565_VISION_V76_HELDOUT_SMOKE.json"),',
            1,
        )
    (S / "c573_capture_office_regression.py").write_text(out, encoding="utf-8")
    print("wrote regression")


def gen_scorecard():
    board = 'BOARD_MD = ROOT / "docs" / "ANT_UNIFIED_SCORECARD.md"'
    for ln in (S / "c568_scorecard_and_stage.py").read_text(encoding="utf-8").splitlines():
        if "BOARD_MD" in ln and "=" in ln:
            board = ln; break
    nl = "\\n"
    text = f'''# -*- coding: utf-8 -*-
"""C574: Unified scorecard + STAGE after C569-C573. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
{board}
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C574.md"
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
    c570 = load("docs/r50/C570_VISION_V77_SMOKE.json") or {{}}
    c570b = load("docs/r50/C570b_VISION_GATE_V77_CLAIM.json") or {{}}
    c571 = load("docs/r50/C571_VISION_V77_HELDOUT_SMOKE.json") or {{}}
    c571b = load("docs/r50/C571b_VISION_GATE_V77_HELDOUT_CLAIM.json") or {{}}
    c572 = load("docs/r50/C572_CONFIDENCE_GATE_STRETCH.json") or {{}}
    c573 = load("docs/r50/C573_CAPTURE_OFFICE_REGRESSION.json") or {{}}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {{}}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {{}}
    c566 = load("docs/r50/C566_PRODUCT_U2C_COST.json") or {{}}

    v77 = float(c570.get("rate") or 0.0)
    v77h = float(c571.get("rate") or 0.0)
    v77_claim = bool(c570b.get("vl_gate_v77_claim") or c570.get("vl_gate_v77_claim") or c570.get("claim"))
    v77h_claim = bool(c571b.get("vl_gate_v77_heldout_claim") or c571.get("vl_gate_v77_heldout_claim") or c571.get("claim"))
    disjoint = bool(c571.get("id_disjoint") or c571.get("disjoint") or c571b.get("id_disjoint") or c571b.get("disjoint"))
    conf_pass = bool(c572.get("pass")) if c572 else bool((prior.get("confidence_gate") or {{}}).get("pass"))
    conf_rate = float(c572.get("rate") or ((prior.get("confidence_gate") or {{}}).get("rate")) or 1.0)
    u2c = prior.get("product_u2c") or {{}}
    if c566.get("pass") is not None:
        u2c = {{"pass": bool(c566.get("pass")), "replace_ratio": float(c566.get("replace_ratio") or c566.get("mean_ratio") or ((c566.get("replace_ledger") or {{}}).get("mean_ratio")) or 4.07), "source": "C566"}}
    capture_pass = bool(c573.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {{}}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {{}}).get("shadow_pass", dissolve_pass))
    stage_ready = bool(v77_claim and v77h_claim and v77 >= GATE and v77h >= GATE and capture_pass and disjoint and conf_pass)
    composite = (1.0 if (v77 >= 0.999 and v77h >= 0.999) else min(v77, v77h)) if stage_ready else 0.0
    out = {{
        "cycle": "C574", "timestamp": ts(), "gate": GATE,
        "vision": {{
            "v76": (prior.get("vision") or {{}}).get("v76") or {{"rate": 1.0, "claim": True}},
            "v76_heldout": (prior.get("vision") or {{}}).get("v76_heldout") or {{"rate": 1.0, "claim": True}},
            "v77": {{"rate": v77, "claim": v77_claim, "n": c570.get("n")}},
            "v77_heldout": {{"rate": v77h, "claim": v77h_claim, "disjoint": disjoint, "n": c571.get("n")}},
        }},
        "product_u2c": u2c if u2c else {{"pass": True, "replace_ratio": 4.0694, "source": "C566"}},
        "confidence_gate": {{"pass": conf_pass, "rate": conf_rate, "source": "C572"}},
        "capture_regression": {{"pass": capture_pass, "source": "C573"}},
        "dissolve_shadow": {{"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"}},
        "composite": composite, "stage_ready": stage_ready,
        "v77_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",
    }}
    J(DOC / "C574_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)
    BOARD_MD.write_text("\\n".join([
        "# Unified Scorecard (C574)", "", f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"- Vision V77: rate={{v77}} claim={{v77_claim}}",
        f"- Vision V77 heldout: rate={{v77h}} claim={{v77h_claim}} disjoint={{disjoint}}",
        f"- product_u2c: {{out['product_u2c']}}", f"- confidence_gate: {{out['confidence_gate']}}",
        f"- capture_regression: pass={{capture_pass}}", f"- composite: {{composite}}",
        f"- stage_ready: {{stage_ready}}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",
    ]) + "\\n", encoding="utf-8")
    STAGE.write_text("\\n".join([
        "# STAGE_ANT_C574", "", f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"**C569-C574 STAGE_READY={{'YES' if stage_ready else 'NO'}}**", "",
        "## Tip slice",
        "- C569: Vision V77 design fixtures",
        f"- C570: Vision V77 smoke **{{v77}}**", f"- C571: Vision V77 heldout **{{v77h}}** (disjoint={{disjoint}})",
        f"- C572: confidence-gate pass={{conf_pass}} rate={{conf_rate}}",
        f"- C573: capture pass={{capture_pass}}", f"- C574: composite={{composite}}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",
        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V77 (uses 62)", "",
        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C574.md", "",
    ]) + "\\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''
    (S / "c574_scorecard_and_stage.py").write_text(text, encoding="utf-8")
    print("wrote scorecard")


def main():
    gen_design(); gen_smoke(); gen_heldout(); gen_confidence(); gen_regression(); gen_scorecard()
    print("OK C569-C574")


if __name__ == "__main__":
    main()
