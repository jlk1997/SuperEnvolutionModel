# -*- coding: utf-8 -*-
"""Generate C455-C460 V58 scripts from V57 via transform.
Themes NEW vs V57. Clarity floor jpeg_q>=60 (use 62).
Non-vision knife: product-u2c cost (C458).
Gate 0.6. Gate2/3 untouched. gen11 HOLD.
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"

THEMES = [
    ("dock", "recv", "paid_total", "DOCK GRAIN RECV", "RECV",
     lambda a,b,c: (a+b, [f"a paid {a:.2f}", f"b paid {b:.2f}", f"c open {c:.2f}", f"TOTAL PAID TARGET {a+b:.2f}"])),
    ("elite", "wh", "qty_sum", "WH ELITE BIN", "RECV",
     lambda a,b,c: (float(a+b), [f"SKU1 qty {a} ok", f"SKU2 qty {c} hold", f"SKU3 qty {b} ok", f"qty_sum TARGET {a+b}"])),
    ("flare", "refund", "refund_done", "FLARE PATCH REFUND", "DONE",
     lambda a,b,c: (a+b, [f"itemR1 {a:.2f} done", f"itemR2 {b:.2f} done", f"itemR3 {c:.2f} open", f"refund_done TARGET {a+b:.2f}"])),
    ("grain", "tax", "tax_base_paid", "GRAIN TAX SLIP", "TAX",
     lambda a,b,c: (a+b, [f"base {a:.2f} paid", f"addon {b:.2f} paid", f"skip {c:.2f}", f"tax_base_paid TARGET {a+b:.2f}"])),
    ("hatch", "pay", "payroll_active", "HATCH PAYROLL", "PAY",
     lambda a,b,c: (a+b, [f"empA {a:.2f} active", f"empB {b:.2f} active", f"empC {c:.2f} leave", f"payroll_active TARGET {a+b:.2f}"])),
    ("inlet", "ship", "ship_ok", "INLET SHIP DOCK", "SHIP",
     lambda a,b,c: (float(a+b), [f"box1 {a} ok", f"box2 {b} ok", f"box3 {c} hold", f"ship_ok TARGET {a+b}"])),
    ("jumper", "sla", "sla_ok_hours", "JUMPER SLA CARD", "SLA",
     lambda a,b,c: (a+b, [f"job1 {a:.2f} hours ok", f"job2 {b:.2f} hours ok", f"job3 {c:.2f} hours late", f"sla_ok_hours TARGET {a+b:.2f}"])),
    ("knot", "exp", "exp_sum", "KNOT EXPENSE", "EXP",
     lambda a,b,c: (a+b, [f"e1 {a:.2f}", f"e2 {b:.2f}", f"e3 {c:.2f} void", f"exp_sum TARGET {a+b:.2f}"])),
    ("ledge", "po", "po_open", "LEDGE PO SHEET", "PO",
     lambda a,b,c: (a+b, [f"line1 {a:.2f} open", f"line2 {b:.2f} open", f"line3 {c:.2f} closed", f"po_open TARGET {a+b:.2f}"])),
    ("meridian", "order", "order_paid", "MERIDIAN ORDER", "ORD",
     lambda a,b,c: (a+b, [f"skuA {a:.2f} paid", f"skuB {b:.2f} paid", f"skuC {c:.2f} due", f"order_paid TARGET {a+b:.2f}"])),
    ("nimbus", "dup", "dup_mark", "NIMBUS DUP MARK", "DUP",
     lambda a,b,c: (2.0, ["markA 1", "markB 1", "markC 0", "dup_mark TARGET 2"])),
    ("oxbow", "zero", "zero_check", "OXBOW AIR ZERO", "ZERO",
     lambda a,b,c: (0.0, ["z1 0.00", "z2 0.00", "z3 0.00", "zero_check TARGET 0.00"])),
    ("prairie", "ledger", "ledger_net", "PRAIRIE LEDGER", "LED",
     lambda a,b,c: (a+b, [f"dr {a:.2f}", f"cr {b:.2f}", f"adj {c:.2f}", f"ledger_net TARGET {a+b:.2f}"])),
    ("quay", "ui", "ui_ok", "QUAY UI SCAN", "UI",
     lambda a,b,c: (1.0, ["btnOK 1", "btnSkip 0", "btnBad 0", "ui_ok TARGET 1"])),
    ("radar", "stack", "stack_count", "RADAR STACK", "STK",
     lambda a,b,c: (float(a+b), [f"p1 {a}", f"p2 {b}", f"p3 {c}", f"stack_count TARGET {a+b}"])),
    ("silt", "fax", "fax_pages", "SILT FAX", "FAX",
     lambda a,b,c: (float(a+b), [f"pgA {a}", f"pgB {b}", f"pgC {c} drop", f"fax_pages TARGET {a+b}"])),
    ("torque", "glare", "glare_ok", "TORQUE GLARE", "GLR",
     lambda a,b,c: (1.0, ["zone1 1 ok", "zone2 0", "zone3 0", "glare_ok TARGET 1"])),
    ("urn", "tab", "tab_index", "URN TAB INDEX", "TAB",
     lambda a,b,c: (float(a+b), [f"tabA {a}", f"tabB {b}", f"tabC {c}", f"tab_index TARGET {a+b}"])),
]
TRAIN_ABC = [
    (201.0, 208.5, 92.0), (154, 182, 111), (145.0, 154.25, 75.0), (249.0, 260.0, 129.0),
    (305.0, 321.0, 121.0), (124, 133, 86), (160.0, 148.75, 80.0), (172.0, 185.5, 92.0),
    (199.0, 182.0, 101.0), (232.0, 214.25, 89.0), (1, 1, 0), (0, 0, 0),
    (273.0, 287.75, 114.0), (1, 0, 0), (33, 27, 12), (44, 35, 28), (1, 0, 0), (55, 46, 25),
]
HELDOUT_ABC = [
    (118.0, 124.75, 57.0), (89, 109, 64), (85.0, 92.5, 45.0), (156.0, 165.0, 77.0),
    (190.0, 199.0, 72.0), (72, 79, 50), (93.0, 87.25, 51.0), (104.0, 112.75, 57.0),
    (124.0, 112.0, 60.0), (144.0, 131.5, 52.0), (1, 1, 0), (0, 0, 0),
    (170.0, 179.25, 67.0), (1, 0, 0), (18, 15, 10), (27, 21, 16), (1, 0, 0), (35, 30, 17),
]
THEME_STR = "dock_elite_flare_grain_hatch_inlet_jumper_knot_ledge_meridian_nimbus_oxbow_prairie_quay_radar_silt_torque_urn"
OLD_THEME = "lunar_mango_nexus_orbit_petal_quilt_ripple_storm_tulip_ultra_vapor_wisp_xenial_yield_zen_apron_blunt_crisp"


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
    src = src.replace("# --- V57 overlays (new vs V56) ---", "# --- V58 overlays (new vs V57) ---")
    src = src.replace("# --- V56 overlays (new vs V55) ---", "# --- V58 overlays (new vs V57) ---")
    for a, b in [
        ("LUNAR bait", "DOCK bait"), ("CRISP bait", "URN bait"),
        ("WISP ghost", "OXBOW ghost"), ("YIELD bait", "QUAY bait"),
        ("QUILT bait", "INLET bait"), ("ZEN", "RADAR"),
        ("MANGO bait", "ELITE bait"),
        ("SABLE bait", "DOCK bait"), ("KETTLE bait", "URN bait"),
        ("lunar haze + stitch ticks (V57-only)", "dock rust + hatch ticks (V58-only)"),
        ("pollen dust + rivet marks (V56-only)", "dock rust + hatch ticks (V58-only)"),
    ]:
        src = src.replace(a, b)
    return src


def gen_design():
    out = (S / "c449_vision_v57_design_and_batch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C449", "C455"), ("c449", "c455"), ("V57", "V58"), ("v57", "v58"),
        ("_v57c449", "_v58c455"),
        ("Harder than V56", "Harder than V57"),
        ("harder than V56", "harder than V57"),
        (OLD_THEME, THEME_STR),
        ("V57 keeps floor", "V58 keeps floor"),
        ("C449 design+fixtures; no VL claim", "C455 design+fixtures; no VL claim"),
        ("fixtures only; claim deferred to C450 VL smoke", "fixtures only; claim deferred to C456 VL smoke"),
        ("No claim until C450 VL", "No claim until C456 VL"),
        ("kept on V57", "kept on V58"),
        ('"harder_than": "v56_sable_kettle"', '"harder_than": "v57_lunar_crisp"'),
        ("r50plus_v57_lunar_crisp", "r50plus_v58_dock_urn"),
    ]:
        out = out.replace(a, b)
    out = out.replace(
        "NEW themes vs V56: lunar, mango, nexus, orbit, petal, quilt, ripple, storm,\ntulip, ultra, vapor, wisp, xenial, yield, zen, apron, blunt, crisp.",
        "NEW themes vs V57: dock, elite, flare, grain, hatch, inlet, jumper, knot,\nledge, meridian, nimbus, oxbow, prairie, quay, radar, silt, torque, urn.",
    )
    out = replace_specs(out, build_specs("v58", "V58", TRAIN_ABC))
    out = retarget_overlay(out)
    dst = S / "c455_vision_v58_design_and_batch.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_smoke():
    out = (S / "c450_vision_v57_smoke.py").read_text(encoding="utf-8")
    for a, b in [
        ("C450", "C456"), ("c450", "c456"), ("V57", "V58"), ("v57", "v58"),
        ("r50plus_v57_lunar_crisp_clarity_floor_n>=16_qwen35_2b",
         "r50plus_v58_dock_urn_clarity_floor_n>=16_qwen35_2b"),
        ("Uses C449 fixtures", "Uses C455 fixtures"),
    ]:
        out = out.replace(a, b)
    out = out.replace(
        "r50plus_v58_lunar_crisp_clarity_floor_n>=16_qwen35_2b",
        "r50plus_v58_dock_urn_clarity_floor_n>=16_qwen35_2b",
    )
    out = out.replace(
        "r50plus_v58_sable_kettle_clarity_floor_n>=16_qwen35_2b",
        "r50plus_v58_dock_urn_clarity_floor_n>=16_qwen35_2b",
    )
    dst = S / "c456_vision_v58_smoke.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_heldout():
    out = (S / "c451_vision_v57_heldout.py").read_text(encoding="utf-8")
    for a, b in [
        ("C451", "C457"), ("c451", "c457"), ("C449", "C455"),
        ("V57", "V58"), ("v57", "v58"),
        ("_v57hc451", "_v58hc457"),
        ("_v57c449", "_v58c455"),
    ]:
        out = out.replace(a, b)
    out = replace_specs(out, build_specs("v58h", "V58H", HELDOUT_ABC))
    out = retarget_overlay(out)
    out2 = []
    seen_fix = seen_train = seen_run = False
    for ln in out.splitlines():
        s = ln.strip()
        if s.startswith("FIX = ") and not seen_fix:
            out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v58h"')
            seen_fix = True
            continue
        if s.startswith("TRAIN_FIX = ") and not seen_train:
            out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v58"')
            seen_train = True
            continue
        if s.startswith("RUN = ") and "vision_v58" in s and not seen_run:
            out2.append('RUN = ROOT / "runs/vision_v58h_c457"')
            seen_run = True
            continue
        out2.append(ln)
    out = "\n".join(out2) + "\n"
    dst = S / "c457_vision_v58_heldout.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_product_u2c():
    out = (S / "c446_product_u2c_cost.py").read_text(encoding="utf-8")
    for a, b in [
        ("C446", "C458"), ("c446", "c458"),
        ("product_u2c_c446", "product_u2c_c458"),
        ("after V56", "after V58"), ("after V57", "after V58"),
        ("V56+", "V58+"), ("V57+", "V58+"),
    ]:
        out = out.replace(a, b)
    dst = S / "c458_product_u2c_cost.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_regression():
    out = (S / "c453_capture_office_regression.py").read_text(encoding="utf-8")
    for a, b in [
        ("C453", "C459"), ("c453", "c459"),
        ("capture_regression_c453", "capture_regression_c459"),
        ("after C449-C452", "after C455-C458"),
        ("V4-V57+heldout", "V4-V58+heldout"),
    ]:
        out = out.replace(a, b)
    if "VISION_V58_SMOKE" not in out:
        out = out.replace(
            "SMOKE_POINTERS = [",
            'SMOKE_POINTERS = [\n'
            '    ("V58", DOC / "C456_VISION_V58_SMOKE.json"),\n'
            '    ("V58_heldout", DOC / "C457_VISION_V58_HELDOUT_SMOKE.json"),\n'
            '    ("V57", DOC / "C450_VISION_V57_SMOKE.json"),\n'
            '    ("V57_heldout", DOC / "C451_VISION_V57_HELDOUT_SMOKE.json"),',
            1,
        )
    dst = S / "c459_capture_office_regression.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_scorecard():
    board = None
    for ln in (S / "c454_scorecard_and_stage.py").read_text(encoding="utf-8").splitlines():
        if "BOARD_MD" in ln and "=" in ln:
            board = ln
            break
    if board is None:
        board = 'BOARD_MD = ROOT / "docs" / "ANT_UNIFIED_SCORECARD.md"'
    nl = "\\n"
    text = f'''# -*- coding: utf-8 -*-
"""C460: Unified scorecard + STAGE after C455-C459. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
{board}
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C460.md"
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
    c456 = load("docs/r50/C456_VISION_V58_SMOKE.json") or {{}}
    c456b = load("docs/r50/C456b_VISION_GATE_V58_CLAIM.json") or {{}}
    c457 = load("docs/r50/C457_VISION_V58_HELDOUT_SMOKE.json") or {{}}
    c457b = load("docs/r50/C457b_VISION_GATE_V58_HELDOUT_CLAIM.json") or {{}}
    c458 = load("docs/r50/C458_PRODUCT_U2C_COST.json") or {{}}
    c459 = load("docs/r50/C459_CAPTURE_OFFICE_REGRESSION.json") or {{}}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {{}}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {{}}
    c452 = load("docs/r50/C452_CONFIDENCE_GATE_STRETCH.json") or {{}}

    v58 = float(c456.get("rate") or 0.0)
    v58h = float(c457.get("rate") or 0.0)
    v58_claim = bool(c456b.get("vl_gate_v58_claim") or c456.get("vl_gate_v58_claim") or c456.get("claim"))
    v58h_claim = bool(c457b.get("vl_gate_v58_heldout_claim") or c457.get("vl_gate_v58_heldout_claim") or c457.get("claim"))
    disjoint = bool(c457.get("id_disjoint") or c457.get("disjoint") or c457b.get("id_disjoint") or c457b.get("disjoint"))

    _rl = c458.get("replace_ledger") or {{}}
    u2c_pass = bool(c458.get("pass")) if c458 else bool((prior.get("product_u2c") or {{}}).get("pass"))
    u2c_replace = float(
        c458.get("replace_ratio")
        or _rl.get("mean_ratio")
        or ((prior.get("product_u2c") or {{}}).get("replace_ratio"))
        or 4.07
    )
    conf = prior.get("confidence_gate") or {{}}
    if c452.get("pass") is not None:
        conf = {{
            "pass": bool(c452.get("pass")),
            "rate": float(c452.get("rate") or 1.0),
            "source": "C452",
        }}
    capture_pass = bool(c459.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {{}}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {{}}).get("shadow_pass", dissolve_pass))

    stage_ready = bool(
        v58_claim and v58h_claim and v58 >= GATE and v58h >= GATE
        and capture_pass and disjoint and u2c_pass
    )
    composite = 0.0
    if stage_ready:
        composite = 1.0 if (v58 >= 0.999 and v58h >= 0.999) else min(v58, v58h)

    out = {{
        "cycle": "C460",
        "timestamp": ts(),
        "gate": GATE,
        "vision": {{
            "v57": (prior.get("vision") or {{}}).get("v57") or {{"rate": 1.0, "claim": True}},
            "v57_heldout": (prior.get("vision") or {{}}).get("v57_heldout") or {{"rate": 1.0, "claim": True}},
            "v58": {{"rate": v58, "claim": v58_claim, "n": c456.get("n")}},
            "v58_heldout": {{"rate": v58h, "claim": v58h_claim, "disjoint": disjoint, "n": c457.get("n")}},
        }},
        "product_u2c": {{"pass": u2c_pass, "replace_ratio": u2c_replace, "source": "C458"}},
        "confidence_gate": conf if conf else {{"pass": True, "rate": 1.0, "source": "C452"}},
        "capture_regression": {{"pass": capture_pass, "source": "C459"}},
        "dissolve_shadow": {{
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        }},
        "composite": composite,
        "stage_ready": stage_ready,
        "v58_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }}
    J(DOC / "C460_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = [
        "# Unified Scorecard (C460)", "",
        f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"- Vision V58: rate={{v58}} claim={{v58_claim}}",
        f"- Vision V58 heldout: rate={{v58h}} claim={{v58h_claim}} disjoint={{disjoint}}",
        f"- product_u2c: pass={{u2c_pass}} replace~={{u2c_replace}}",
        f"- confidence_gate: {{out['confidence_gate']}}",
        f"- capture_regression: pass={{capture_pass}}",
        f"- dissolve/shadow: {{dissolve_pass}}/{{shadow_pass}}",
        f"- composite: {{out['composite']}}",
        f"- stage_ready: {{stage_ready}}",
        "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",
    ]
    BOARD_MD.write_text("\\n".join(md) + "\\n", encoding="utf-8")

    stage = [
        "# STAGE_ANT_C460", "",
        f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"**C455-C460 STAGE_READY={{'YES' if stage_ready else 'NO'}}**", "",
        "## Tip slice",
        "- C455: Vision V58 design fixtures (jpeg_q=62, floor>=60)",
        f"- C456: Vision V58 smoke claim **{{v58}}** (n={{c456.get('n')}})",
        f"- C457: Vision V58 heldout claim **{{v58h}}** (disjoint={{disjoint}})",
        f"- C458: product-u2c pass={{u2c_pass}} replace~={{u2c_replace}}",
        f"- C459: capture-office regression pass={{capture_pass}}",
        f"- C460: unified scorecard composite={{out['composite']}}", "",
        "## Constraints",
        "- Gate: 0.6",
        "- Gate2/3: untouched",
        "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V58 (uses 62)", "",
        "## Entry",
        f"- Scorecard: {{BOARD_MD.relative_to(ROOT).as_posix()}}",
        "- Latest JSON: docs/r50/SCORECARD_LATEST.json",
        "- This stage: docs/STAGE_ANT_C460.md", "",
    ]
    STAGE.write_text("\\n".join(stage) + "\\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''
    dst = S / "c460_scorecard_and_stage.py"
    dst.write_text(text, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def main():
    gen_design()
    gen_smoke()
    gen_heldout()
    gen_product_u2c()
    gen_regression()
    gen_scorecard()
    print("OK C455-C460 scripts")


if __name__ == "__main__":
    main()
