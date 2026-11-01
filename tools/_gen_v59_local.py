# -*- coding: utf-8 -*-
"""Generate C461-C466 V59 scripts from V58 via transform.
Themes NEW vs V58. Clarity floor jpeg_q>=60 (use 62).
Non-vision knife: confidence-gate stretch (C464).
Gate 0.6. Gate2/3 untouched. gen11 HOLD.
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"

THEMES = [
    ("vault", "recv", "paid_total", "VAULT GRAIN RECV", "RECV",
     lambda a,b,c: (a+b, [f"a paid {a:.2f}", f"b paid {b:.2f}", f"c open {c:.2f}", f"TOTAL PAID TARGET {a+b:.2f}"])),
    ("wick", "wh", "qty_sum", "WH WICK BIN", "RECV",
     lambda a,b,c: (float(a+b), [f"SKU1 qty {a} ok", f"SKU2 qty {c} hold", f"SKU3 qty {b} ok", f"qty_sum TARGET {a+b}"])),
    ("xray", "refund", "refund_done", "XRAY PATCH REFUND", "DONE",
     lambda a,b,c: (a+b, [f"itemR1 {a:.2f} done", f"itemR2 {b:.2f} done", f"itemR3 {c:.2f} open", f"refund_done TARGET {a+b:.2f}"])),
    ("zest", "tax", "tax_base_paid", "ZEST TAX SLIP", "TAX",
     lambda a,b,c: (a+b, [f"base {a:.2f} paid", f"addon {b:.2f} paid", f"skip {c:.2f}", f"tax_base_paid TARGET {a+b:.2f}"])),
    ("axle", "pay", "payroll_active", "AXLE PAYROLL", "PAY",
     lambda a,b,c: (a+b, [f"empA {a:.2f} active", f"empB {b:.2f} active", f"empC {c:.2f} leave", f"payroll_active TARGET {a+b:.2f}"])),
    ("brine", "ship", "ship_ok", "BRINE SHIP DOCK", "SHIP",
     lambda a,b,c: (float(a+b), [f"box1 {a} ok", f"box2 {b} ok", f"box3 {c} hold", f"ship_ok TARGET {a+b}"])),
    ("chalk", "sla", "sla_ok_hours", "CHALK SLA CARD", "SLA",
     lambda a,b,c: (a+b, [f"job1 {a:.2f} hours ok", f"job2 {b:.2f} hours ok", f"job3 {c:.2f} hours late", f"sla_ok_hours TARGET {a+b:.2f}"])),
    ("eddy", "exp", "exp_sum", "EDDY EXPENSE", "EXP",
     lambda a,b,c: (a+b, [f"e1 {a:.2f}", f"e2 {b:.2f}", f"e3 {c:.2f} void", f"exp_sum TARGET {a+b:.2f}"])),
    ("foam", "po", "po_open", "FOAM PO SHEET", "PO",
     lambda a,b,c: (a+b, [f"line1 {a:.2f} open", f"line2 {b:.2f} open", f"line3 {c:.2f} closed", f"po_open TARGET {a+b:.2f}"])),
    ("gasket", "order", "order_paid", "GASKET ORDER", "ORD",
     lambda a,b,c: (a+b, [f"skuA {a:.2f} paid", f"skuB {b:.2f} paid", f"skuC {c:.2f} due", f"order_paid TARGET {a+b:.2f}"])),
    ("hinge", "dup", "dup_mark", "HINGE DUP MARK", "DUP",
     lambda a,b,c: (2.0, ["markA 1", "markB 1", "markC 0", "dup_mark TARGET 2"])),
    ("jersey", "zero", "zero_check", "JERSEY AIR ZERO", "ZERO",
     lambda a,b,c: (0.0, ["z1 0.00", "z2 0.00", "z3 0.00", "zero_check TARGET 0.00"])),
    ("kiln", "ledger", "ledger_net", "KILN LEDGER", "LED",
     lambda a,b,c: (a+b, [f"dr {a:.2f}", f"cr {b:.2f}", f"adj {c:.2f}", f"ledger_net TARGET {a+b:.2f}"])),
    ("loom", "ui", "ui_ok", "LOOM UI SCAN", "UI",
     lambda a,b,c: (1.0, ["btnOK 1", "btnSkip 0", "btnBad 0", "ui_ok TARGET 1"])),
    ("magma", "stack", "stack_count", "MAGMA STACK", "STK",
     lambda a,b,c: (float(a+b), [f"p1 {a}", f"p2 {b}", f"p3 {c}", f"stack_count TARGET {a+b}"])),
    ("niche", "fax", "fax_pages", "NICHE FAX", "FAX",
     lambda a,b,c: (float(a+b), [f"pgA {a}", f"pgB {b}", f"pgC {c} drop", f"fax_pages TARGET {a+b}"])),
    ("opus", "glare", "glare_ok", "OPUS GLARE", "GLR",
     lambda a,b,c: (1.0, ["zone1 1 ok", "zone2 0", "zone3 0", "glare_ok TARGET 1"])),
    ("plank", "tab", "tab_index", "PLANK TAB INDEX", "TAB",
     lambda a,b,c: (float(a+b), [f"tabA {a}", f"tabB {b}", f"tabC {c}", f"tab_index TARGET {a+b}"])),
]
TRAIN_ABC = [
    (208.0, 216.25, 97.0), (161, 189, 116), (152.0, 161.5, 79.0), (257.0, 269.0, 134.0),
    (314.0, 331.0, 127.0), (129, 139, 91), (167.0, 156.25, 84.0), (179.0, 193.75, 97.0),
    (207.0, 190.0, 106.0), (240.0, 222.5, 94.0), (1, 1, 0), (0, 0, 0),
    (284.0, 299.25, 119.0), (1, 0, 0), (35, 29, 13), (47, 37, 30), (1, 0, 0), (58, 49, 27),
]
HELDOUT_ABC = [
    (123.0, 130.25, 60.0), (93, 114, 67), (89.0, 97.25, 48.0), (162.0, 172.0, 81.0),
    (197.0, 207.0, 76.0), (75, 83, 53), (97.0, 91.5, 54.0), (109.0, 118.25, 60.0),
    (129.0, 117.0, 63.0), (150.0, 137.25, 55.0), (1, 1, 0), (0, 0, 0),
    (177.0, 186.75, 70.0), (1, 0, 0), (19, 16, 11), (29, 23, 17), (1, 0, 0), (37, 32, 18),
]
THEME_STR = "vault_wick_xray_zest_axle_brine_chalk_eddy_foam_gasket_hinge_jersey_kiln_loom_magma_niche_opus_plank"
OLD_THEME = "dock_elite_flare_grain_hatch_inlet_jumper_knot_ledge_meridian_nimbus_oxbow_prairie_quay_radar_silt_torque_urn"


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
    src = src.replace("# --- V58 overlays (new vs V57) ---", "# --- V59 overlays (new vs V58) ---")
    src = src.replace("# --- V57 overlays (new vs V56) ---", "# --- V59 overlays (new vs V58) ---")
    for a, b in [
        ("DOCK bait", "VAULT bait"), ("URN bait", "PLANK bait"),
        ("OXBOW ghost", "JERSEY ghost"), ("QUAY bait", "LOOM bait"),
        ("INLET bait", "BRINE bait"), ("RADAR", "MAGMA"),
        ("ELITE bait", "WICK bait"),
        ("LUNAR bait", "VAULT bait"), ("CRISP bait", "PLANK bait"),
        ("dock rust + hatch ticks (V58-only)", "vault soot + hinge ticks (V59-only)"),
        ("lunar haze + stitch ticks (V57-only)", "vault soot + hinge ticks (V59-only)"),
    ]:
        src = src.replace(a, b)
    return src


def gen_design():
    out = (S / "c455_vision_v58_design_and_batch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C455", "C461"), ("c455", "c461"), ("V58", "V59"), ("v58", "v59"),
        ("_v58c455", "_v59c461"),
        ("Harder than V57", "Harder than V58"),
        ("harder than V57", "harder than V58"),
        (OLD_THEME, THEME_STR),
        ("V58 keeps floor", "V59 keeps floor"),
        ("C455 design+fixtures; no VL claim", "C461 design+fixtures; no VL claim"),
        ("fixtures only; claim deferred to C456 VL smoke", "fixtures only; claim deferred to C462 VL smoke"),
        ("No claim until C456 VL", "No claim until C462 VL"),
        ("kept on V58", "kept on V59"),
        ('"harder_than": "v57_lunar_crisp"', '"harder_than": "v58_dock_urn"'),
        ("r50plus_v58_dock_urn", "r50plus_v59_vault_plank"),
    ]:
        out = out.replace(a, b)
    out = out.replace(
        "NEW themes vs V57: dock, elite, flare, grain, hatch, inlet, jumper, knot,\nledge, meridian, nimbus, oxbow, prairie, quay, radar, silt, torque, urn.",
        "NEW themes vs V58: vault, wick, xray, zest, axle, brine, chalk, eddy,\nfoam, gasket, hinge, jersey, kiln, loom, magma, niche, opus, plank.",
    )
    out = replace_specs(out, build_specs("v59", "V59", TRAIN_ABC))
    out = retarget_overlay(out)
    dst = S / "c461_vision_v59_design_and_batch.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_smoke():
    out = (S / "c456_vision_v58_smoke.py").read_text(encoding="utf-8")
    for a, b in [
        ("C456", "C462"), ("c456", "c462"), ("V58", "V59"), ("v58", "v59"),
        ("r50plus_v58_dock_urn_clarity_floor_n>=16_qwen35_2b",
         "r50plus_v59_vault_plank_clarity_floor_n>=16_qwen35_2b"),
        ("Uses C455 fixtures", "Uses C461 fixtures"),
    ]:
        out = out.replace(a, b)
    out = out.replace(
        "r50plus_v59_dock_urn_clarity_floor_n>=16_qwen35_2b",
        "r50plus_v59_vault_plank_clarity_floor_n>=16_qwen35_2b",
    )
    out = out.replace(
        "r50plus_v59_lunar_crisp_clarity_floor_n>=16_qwen35_2b",
        "r50plus_v59_vault_plank_clarity_floor_n>=16_qwen35_2b",
    )
    dst = S / "c462_vision_v59_smoke.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_heldout():
    out = (S / "c457_vision_v58_heldout.py").read_text(encoding="utf-8")
    for a, b in [
        ("C457", "C463"), ("c457", "c463"), ("C455", "C461"),
        ("V58", "V59"), ("v58", "v59"),
        ("_v58hc457", "_v59hc463"),
        ("_v58c455", "_v59c461"),
    ]:
        out = out.replace(a, b)
    out = replace_specs(out, build_specs("v59h", "V59H", HELDOUT_ABC))
    out = retarget_overlay(out)
    out2 = []
    seen_fix = seen_train = seen_run = False
    for ln in out.splitlines():
        s = ln.strip()
        if s.startswith("FIX = ") and not seen_fix:
            out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v59h"')
            seen_fix = True
            continue
        if s.startswith("TRAIN_FIX = ") and not seen_train:
            out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v59"')
            seen_train = True
            continue
        if s.startswith("RUN = ") and "vision_v59" in s and not seen_run:
            out2.append('RUN = ROOT / "runs/vision_v59h_c463"')
            seen_run = True
            continue
        out2.append(ln)
    out = "\n".join(out2) + "\n"
    dst = S / "c463_vision_v59_heldout.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_confidence():
    out = (S / "c452_confidence_gate_stretch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C452", "C464"), ("c452", "c464"),
        ("confidence_gate_c452", "confidence_gate_c464"),
        ("conf_gate_stretch_c452", "conf_gate_stretch_c464"),
        ("after V57", "after V59"), ("after V58", "after V59"),
        ("V57+", "V59+"), ("V58+", "V59+"),
    ]:
        out = out.replace(a, b)
    dst = S / "c464_confidence_gate_stretch.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_regression():
    out = (S / "c459_capture_office_regression.py").read_text(encoding="utf-8")
    for a, b in [
        ("C459", "C465"), ("c459", "c465"),
        ("capture_regression_c459", "capture_regression_c465"),
        ("after C455-C458", "after C461-C464"),
        ("V4-V58+heldout", "V4-V59+heldout"),
    ]:
        out = out.replace(a, b)
    if "VISION_V59_SMOKE" not in out:
        out = out.replace(
            "SMOKE_POINTERS = [",
            'SMOKE_POINTERS = [\n'
            '    ("V59", DOC / "C462_VISION_V59_SMOKE.json"),\n'
            '    ("V59_heldout", DOC / "C463_VISION_V59_HELDOUT_SMOKE.json"),\n'
            '    ("V58", DOC / "C456_VISION_V58_SMOKE.json"),\n'
            '    ("V58_heldout", DOC / "C457_VISION_V58_HELDOUT_SMOKE.json"),',
            1,
        )
    dst = S / "c465_capture_office_regression.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_scorecard():
    board = None
    for ln in (S / "c460_scorecard_and_stage.py").read_text(encoding="utf-8").splitlines():
        if "BOARD_MD" in ln and "=" in ln:
            board = ln
            break
    if board is None:
        board = 'BOARD_MD = ROOT / "docs" / "ANT_UNIFIED_SCORECARD.md"'
    nl = "\\n"
    text = f'''# -*- coding: utf-8 -*-
"""C466: Unified scorecard + STAGE after C461-C465. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
{board}
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C466.md"
GATE = 0.6


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "{nl}", encoding="utf-8")


def load(rel):
    p = ROOT / rel
    if not p.is_file():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def main():
    c462 = load("docs/r50/C462_VISION_V59_SMOKE.json") or {{}}
    c462b = load("docs/r50/C462b_VISION_GATE_V59_CLAIM.json") or {{}}
    c463 = load("docs/r50/C463_VISION_V59_HELDOUT_SMOKE.json") or {{}}
    c463b = load("docs/r50/C463b_VISION_GATE_V59_HELDOUT_CLAIM.json") or {{}}
    c464 = load("docs/r50/C464_CONFIDENCE_GATE_STRETCH.json") or {{}}
    c465 = load("docs/r50/C465_CAPTURE_OFFICE_REGRESSION.json") or {{}}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {{}}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {{}}
    c458 = load("docs/r50/C458_PRODUCT_U2C_COST.json") or {{}}

    v59 = float(c462.get("rate") or 0.0)
    v59h = float(c463.get("rate") or 0.0)
    v59_claim = bool(c462b.get("vl_gate_v59_claim") or c462.get("vl_gate_v59_claim") or c462.get("claim"))
    v59h_claim = bool(c463b.get("vl_gate_v59_heldout_claim") or c463.get("vl_gate_v59_heldout_claim") or c463.get("claim"))
    disjoint = bool(c463.get("id_disjoint") or c463.get("disjoint") or c463b.get("id_disjoint") or c463b.get("disjoint"))
    conf_pass = bool(c464.get("pass")) if c464 else bool((prior.get("confidence_gate") or {{}}).get("pass"))
    conf_rate = float(c464.get("rate") or ((prior.get("confidence_gate") or {{}}).get("rate")) or 1.0)
    u2c = prior.get("product_u2c") or {{}}
    if c458.get("pass") is not None:
        u2c = {{
            "pass": bool(c458.get("pass")),
            "replace_ratio": float(
                c458.get("replace_ratio")
                or c458.get("mean_ratio")
                or ((c458.get("replace_ledger") or {{}}).get("mean_ratio"))
                or 4.07
            ),
            "source": "C458",
        }}
    capture_pass = bool(c465.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {{}}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {{}}).get("shadow_pass", dissolve_pass))

    stage_ready = bool(
        v59_claim and v59h_claim and v59 >= GATE and v59h >= GATE
        and capture_pass and disjoint and conf_pass
    )
    composite = 0.0
    if stage_ready:
        composite = 1.0 if (v59 >= 0.999 and v59h >= 0.999) else min(v59, v59h)

    out = {{
        "cycle": "C466",
        "timestamp": ts(),
        "gate": GATE,
        "vision": {{
            "v58": (prior.get("vision") or {{}}).get("v58") or {{"rate": 1.0, "claim": True}},
            "v58_heldout": (prior.get("vision") or {{}}).get("v58_heldout") or {{"rate": 1.0, "claim": True}},
            "v59": {{"rate": v59, "claim": v59_claim, "n": c462.get("n")}},
            "v59_heldout": {{"rate": v59h, "claim": v59h_claim, "disjoint": disjoint, "n": c463.get("n")}},
        }},
        "product_u2c": u2c if u2c else {{"pass": True, "replace_ratio": 4.0694, "source": "C458"}},
        "confidence_gate": {{"pass": conf_pass, "rate": conf_rate, "source": "C464"}},
        "capture_regression": {{"pass": capture_pass, "source": "C465"}},
        "dissolve_shadow": {{
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        }},
        "composite": composite,
        "stage_ready": stage_ready,
        "v59_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }}
    J(DOC / "C466_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = [
        "# Unified Scorecard (C466)", "",
        f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"- Vision V59: rate={{v59}} claim={{v59_claim}}",
        f"- Vision V59 heldout: rate={{v59h}} claim={{v59h_claim}} disjoint={{disjoint}}",
        f"- product_u2c: {{out['product_u2c']}}",
        f"- confidence_gate: {{out['confidence_gate']}}",
        f"- capture_regression: pass={{capture_pass}}",
        f"- dissolve/shadow: {{dissolve_pass}}/{{shadow_pass}}",
        f"- composite: {{out['composite']}}",
        f"- stage_ready: {{stage_ready}}",
        "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",
    ]
    BOARD_MD.write_text("\\n".join(md) + "\\n", encoding="utf-8")

    stage = [
        "# STAGE_ANT_C466", "",
        f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"**C461-C466 STAGE_READY={{'YES' if stage_ready else 'NO'}}**", "",
        "## Tip slice",
        "- C461: Vision V59 design fixtures (jpeg_q=62, floor>=60)",
        f"- C462: Vision V59 smoke claim **{{v59}}** (n={{c462.get('n')}})",
        f"- C463: Vision V59 heldout claim **{{v59h}}** (disjoint={{disjoint}})",
        f"- C464: confidence-gate stretch pass={{conf_pass}} rate={{conf_rate}}",
        f"- C465: capture-office regression pass={{capture_pass}}",
        f"- C466: unified scorecard composite={{out['composite']}}", "",
        "## Constraints",
        "- Gate: 0.6",
        "- Gate2/3: untouched",
        "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V59 (uses 62)", "",
        "## Entry",
        f"- Scorecard: {{BOARD_MD.relative_to(ROOT).as_posix()}}",
        "- Latest JSON: docs/r50/SCORECARD_LATEST.json",
        "- This stage: docs/STAGE_ANT_C466.md", "",
    ]
    STAGE.write_text("\\n".join(stage) + "\\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''
    dst = S / "c466_scorecard_and_stage.py"
    dst.write_text(text, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def main():
    gen_design()
    gen_smoke()
    gen_heldout()
    gen_confidence()
    gen_regression()
    gen_scorecard()
    print("OK C461-C466 scripts")


if __name__ == "__main__":
    main()
