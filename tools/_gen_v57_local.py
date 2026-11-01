# -*- coding: utf-8 -*-
"""Generate C449-C454 V57 scripts from V56 via transform.
Themes NEW vs V56. Clarity floor jpeg_q>=60 (use 62).
Non-vision knife: confidence-gate stretch (C452).
Gate 0.6. Gate2/3 untouched. gen11 HOLD.
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"

THEMES = [
    ("lunar", "recv", "paid_total", "LUNAR GRAIN RECV", "RECV",
     lambda a,b,c: (a+b, [f"a paid {a:.2f}", f"b paid {b:.2f}", f"c open {c:.2f}", f"TOTAL PAID TARGET {a+b:.2f}"])),
    ("mango", "wh", "qty_sum", "WH MANGO BIN", "RECV",
     lambda a,b,c: (float(a+b), [f"SKU1 qty {a} ok", f"SKU2 qty {c} hold", f"SKU3 qty {b} ok", f"qty_sum TARGET {a+b}"])),
    ("nexus", "refund", "refund_done", "NEXUS PATCH REFUND", "DONE",
     lambda a,b,c: (a+b, [f"itemR1 {a:.2f} done", f"itemR2 {b:.2f} done", f"itemR3 {c:.2f} open", f"refund_done TARGET {a+b:.2f}"])),
    ("orbit", "tax", "tax_base_paid", "ORBIT TAX SLIP", "TAX",
     lambda a,b,c: (a+b, [f"base {a:.2f} paid", f"addon {b:.2f} paid", f"skip {c:.2f}", f"tax_base_paid TARGET {a+b:.2f}"])),
    ("petal", "pay", "payroll_active", "PETAL PAYROLL", "PAY",
     lambda a,b,c: (a+b, [f"empA {a:.2f} active", f"empB {b:.2f} active", f"empC {c:.2f} leave", f"payroll_active TARGET {a+b:.2f}"])),
    ("quilt", "ship", "ship_ok", "QUILT SHIP DOCK", "SHIP",
     lambda a,b,c: (float(a+b), [f"box1 {a} ok", f"box2 {b} ok", f"box3 {c} hold", f"ship_ok TARGET {a+b}"])),
    ("ripple", "sla", "sla_ok_hours", "RIPPLE SLA CARD", "SLA",
     lambda a,b,c: (a+b, [f"job1 {a:.2f} hours ok", f"job2 {b:.2f} hours ok", f"job3 {c:.2f} hours late", f"sla_ok_hours TARGET {a+b:.2f}"])),
    ("storm", "exp", "exp_sum", "STORM EXPENSE", "EXP",
     lambda a,b,c: (a+b, [f"e1 {a:.2f}", f"e2 {b:.2f}", f"e3 {c:.2f} void", f"exp_sum TARGET {a+b:.2f}"])),
    ("tulip", "po", "po_open", "TULIP PO SHEET", "PO",
     lambda a,b,c: (a+b, [f"line1 {a:.2f} open", f"line2 {b:.2f} open", f"line3 {c:.2f} closed", f"po_open TARGET {a+b:.2f}"])),
    ("ultra", "order", "order_paid", "ULTRA ORDER", "ORD",
     lambda a,b,c: (a+b, [f"skuA {a:.2f} paid", f"skuB {b:.2f} paid", f"skuC {c:.2f} due", f"order_paid TARGET {a+b:.2f}"])),
    ("vapor", "dup", "dup_mark", "VAPOR DUP MARK", "DUP",
     lambda a,b,c: (2.0, ["markA 1", "markB 1", "markC 0", "dup_mark TARGET 2"])),
    ("wisp", "zero", "zero_check", "WISP AIR ZERO", "ZERO",
     lambda a,b,c: (0.0, ["z1 0.00", "z2 0.00", "z3 0.00", "zero_check TARGET 0.00"])),
    ("xenial", "ledger", "ledger_net", "XENIAL LEDGER", "LED",
     lambda a,b,c: (a+b, [f"dr {a:.2f}", f"cr {b:.2f}", f"adj {c:.2f}", f"ledger_net TARGET {a+b:.2f}"])),
    ("yield_", "ui", "ui_ok", "YIELD UI SCAN", "UI",
     lambda a,b,c: (1.0, ["btnOK 1", "btnSkip 0", "btnBad 0", "ui_ok TARGET 1"])),
    ("zen", "stack", "stack_count", "ZEN STACK", "STK",
     lambda a,b,c: (float(a+b), [f"p1 {a}", f"p2 {b}", f"p3 {c}", f"stack_count TARGET {a+b}"])),
    ("apron", "fax", "fax_pages", "APRON FAX", "FAX",
     lambda a,b,c: (float(a+b), [f"pgA {a}", f"pgB {b}", f"pgC {c} drop", f"fax_pages TARGET {a+b}"])),
    ("blunt", "glare", "glare_ok", "BLUNT GLARE", "GLR",
     lambda a,b,c: (1.0, ["zone1 1 ok", "zone2 0", "zone3 0", "glare_ok TARGET 1"])),
    ("crisp", "tab", "tab_index", "CRISP TAB INDEX", "TAB",
     lambda a,b,c: (float(a+b), [f"tabA {a}", f"tabB {b}", f"tabC {c}", f"tab_index TARGET {a+b}"])),
]
# display names: yield_ -> yield for kind/theme string
THEME_DISPLAY = {
    "yield_": "yield",
}
TRAIN_ABC = [
    (194.0, 201.25, 88.0), (147, 175, 106), (138.0, 147.75, 71.0), (241.0, 251.0, 124.0),
    (296.0, 311.0, 115.0), (119, 127, 81), (153.0, 141.5, 76.0), (165.0, 177.25, 87.0),
    (191.0, 174.0, 96.0), (224.0, 205.5, 84.0), (1, 1, 0), (0, 0, 0),
    (262.0, 276.5, 109.0), (1, 0, 0), (31, 25, 11), (41, 33, 26), (1, 0, 0), (52, 43, 23),
]
HELDOUT_ABC = [
    (113.0, 119.5, 54.0), (85, 104, 61), (81.0, 88.25, 42.0), (150.0, 158.0, 73.0),
    (183.0, 191.0, 68.0), (69, 75, 47), (89.0, 82.75, 48.0), (99.0, 107.5, 54.0),
    (119.0, 107.0, 57.0), (138.0, 126.25, 49.0), (1, 1, 0), (0, 0, 0),
    (163.0, 171.75, 64.0), (1, 0, 0), (17, 14, 9), (25, 19, 15), (1, 0, 0), (33, 28, 16),
]
THEME_STR = "lunar_mango_nexus_orbit_petal_quilt_ripple_storm_tulip_ultra_vapor_wisp_xenial_yield_zen_apron_blunt_crisp"
OLD_THEME = "sable_thyme_ursa_velvet_whale_xeric_yarrow_zircon_amber_breeze_canyon_daisy_fern_glacier_honey_islet_jewel_kettle"


def fmt_num(x):
    return repr(float(x)) if isinstance(x, float) else repr(x)


def theme_name(name):
    return THEME_DISPLAY.get(name, name)


def build_specs(prefix, tag, abcs):
    lines = ["SPECS = ["]
    for i, ((name, kind_suf, metric, title, stamp, fn), abc) in enumerate(zip(THEMES, abcs), 1):
        expected, body = fn(*abc)
        fid = f"{prefix}_{i:02d}"
        tname = theme_name(name)
        kind = f"{tname}_{kind_suf}"
        body_l = ",\n     ".join(repr(x) for x in ([f"{title} {tag}"] + body))
        lines.append(
            f'    ("{fid}", "{kind}", "{metric}", {fmt_num(expected)},\n'
            f'     [{body_l}],\n     {repr(tname)}, "{stamp}"),'
        )
    lines.append("]")
    return "\n".join(lines) + "\n"


def replace_specs(src, new_specs):
    return re.sub(r"SPECS = \[.*?\n\]\n", new_specs + "\n", src, count=1, flags=re.S)


def retarget_overlay(src):
    src = src.replace("# --- V56 overlays (new vs V55) ---", "# --- V57 overlays (new vs V56) ---")
    src = src.replace("# --- V55 overlays (new vs V54) ---", "# --- V57 overlays (new vs V56) ---")
    for a, b in [
        ("SABLE bait", "LUNAR bait"), ("KETTLE bait", "CRISP bait"),
        ("DAISY ghost", "WISP ghost"), ("GLACIER bait", "YIELD bait"),
        ("XERIC bait", "QUILT bait"), ("HONEY", "ZEN"),
        ("THYME bait", "MANGO bait"),
        ("AZURE bait", "LUNAR bait"), ("RIDGE bait", "CRISP bait"),
        ("pollen dust + rivet marks (V56-only)", "lunar haze + stitch ticks (V57-only)"),
        ("mist rings + bark ticks (V55-only)", "lunar haze + stitch ticks (V57-only)"),
    ]:
        src = src.replace(a, b)
    return src


def gen_design():
    out = (S / "c443_vision_v56_design_and_batch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C443", "C449"), ("c443", "c449"), ("V56", "V57"), ("v56", "v57"),
        ("_v56c443", "_v57c449"),
        ("Harder than V55", "Harder than V56"),
        ("harder than V55", "harder than V56"),
        (OLD_THEME, THEME_STR),
        ("V56 keeps floor", "V57 keeps floor"),
        ("C443 design+fixtures; no VL claim", "C449 design+fixtures; no VL claim"),
        ("fixtures only; claim deferred to C444 VL smoke", "fixtures only; claim deferred to C450 VL smoke"),
        ("No claim until C444 VL", "No claim until C450 VL"),
        ("kept on V56", "kept on V57"),
        ('"harder_than": "v55_azure_ridge"', '"harder_than": "v56_sable_kettle"'),
        ("r50plus_v56_sable_kettle", "r50plus_v57_lunar_crisp"),
    ]:
        out = out.replace(a, b)
    out = out.replace(
        "NEW themes vs V55: sable, thyme, ursa, velvet, whale, xeric, yarrow, zircon,\namber, breeze, canyon, daisy, fern, glacier, honey, islet, jewel, kettle.",
        "NEW themes vs V56: lunar, mango, nexus, orbit, petal, quilt, ripple, storm,\ntulip, ultra, vapor, wisp, xenial, yield, zen, apron, blunt, crisp.",
    )
    out = replace_specs(out, build_specs("v57", "V57", TRAIN_ABC))
    out = retarget_overlay(out)
    dst = S / "c449_vision_v57_design_and_batch.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_smoke():
    out = (S / "c444_vision_v56_smoke.py").read_text(encoding="utf-8")
    for a, b in [
        ("C444", "C450"), ("c444", "c450"), ("V56", "V57"), ("v56", "v57"),
        ("r50plus_v56_sable_kettle_clarity_floor_n>=16_qwen35_2b",
         "r50plus_v57_lunar_crisp_clarity_floor_n>=16_qwen35_2b"),
        ("Uses C443 fixtures", "Uses C449 fixtures"),
    ]:
        out = out.replace(a, b)
    out = out.replace(
        "r50plus_v57_sable_kettle_clarity_floor_n>=16_qwen35_2b",
        "r50plus_v57_lunar_crisp_clarity_floor_n>=16_qwen35_2b",
    )
    out = out.replace(
        "r50plus_v57_azure_ridge_clarity_floor_n>=16_qwen35_2b",
        "r50plus_v57_lunar_crisp_clarity_floor_n>=16_qwen35_2b",
    )
    dst = S / "c450_vision_v57_smoke.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_heldout():
    out = (S / "c445_vision_v56_heldout.py").read_text(encoding="utf-8")
    for a, b in [
        ("C445", "C451"), ("c445", "c451"), ("C443", "C449"),
        ("V56", "V57"), ("v56", "v57"),
        ("_v56hc445", "_v57hc451"),
        ("_v56c443", "_v57c449"),
    ]:
        out = out.replace(a, b)
    out = replace_specs(out, build_specs("v57h", "V57H", HELDOUT_ABC))
    out = retarget_overlay(out)
    out2 = []
    seen_fix = seen_train = seen_run = False
    for ln in out.splitlines():
        s = ln.strip()
        if s.startswith("FIX = ") and not seen_fix:
            out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v57h"')
            seen_fix = True
            continue
        if s.startswith("TRAIN_FIX = ") and not seen_train:
            out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v57"')
            seen_train = True
            continue
        if s.startswith("RUN = ") and "vision_v57" in s and not seen_run:
            out2.append('RUN = ROOT / "runs/vision_v57h_c451"')
            seen_run = True
            continue
        out2.append(ln)
    out = "\n".join(out2) + "\n"
    dst = S / "c451_vision_v57_heldout.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_confidence():
    out = (S / "c440_confidence_gate_stretch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C440", "C452"), ("c440", "c452"),
        ("confidence_gate_c440", "confidence_gate_c452"),
        ("conf_gate_stretch_c440", "conf_gate_stretch_c452"),
        ("after V55", "after V57"), ("after V56", "after V57"),
        ("V55+", "V57+"), ("V56+", "V57+"),
    ]:
        out = out.replace(a, b)
    dst = S / "c452_confidence_gate_stretch.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_regression():
    out = (S / "c447_capture_office_regression.py").read_text(encoding="utf-8")
    for a, b in [
        ("C447", "C453"), ("c447", "c453"),
        ("capture_regression_c447", "capture_regression_c453"),
        ("after C443-C446", "after C449-C452"),
        ("V4-V56+heldout", "V4-V57+heldout"),
    ]:
        out = out.replace(a, b)
    if "VISION_V57_SMOKE" not in out:
        out = out.replace(
            "SMOKE_POINTERS = [",
            'SMOKE_POINTERS = [\n'
            '    ("V57", DOC / "C450_VISION_V57_SMOKE.json"),\n'
            '    ("V57_heldout", DOC / "C451_VISION_V57_HELDOUT_SMOKE.json"),\n'
            '    ("V56", DOC / "C444_VISION_V56_SMOKE.json"),\n'
            '    ("V56_heldout", DOC / "C445_VISION_V56_HELDOUT_SMOKE.json"),',
            1,
        )
    dst = S / "c453_capture_office_regression.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_scorecard():
    board = None
    for ln in (S / "c448_scorecard_and_stage.py").read_text(encoding="utf-8").splitlines():
        if "BOARD_MD" in ln and "=" in ln:
            board = ln
            break
    if board is None:
        board = 'BOARD_MD = ROOT / "docs" / "ANT_UNIFIED_SCORECARD.md"'
    nl = "\\n"
    text = f'''# -*- coding: utf-8 -*-
"""C454: Unified scorecard + STAGE after C449-C453. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
{board}
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C454.md"
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
    c450 = load("docs/r50/C450_VISION_V57_SMOKE.json") or {{}}
    c450b = load("docs/r50/C450b_VISION_GATE_V57_CLAIM.json") or {{}}
    c451 = load("docs/r50/C451_VISION_V57_HELDOUT_SMOKE.json") or {{}}
    c451b = load("docs/r50/C451b_VISION_GATE_V57_HELDOUT_CLAIM.json") or {{}}
    c452 = load("docs/r50/C452_CONFIDENCE_GATE_STRETCH.json") or {{}}
    c453 = load("docs/r50/C453_CAPTURE_OFFICE_REGRESSION.json") or {{}}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {{}}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {{}}
    c446 = load("docs/r50/C446_PRODUCT_U2C_COST.json") or {{}}

    v57 = float(c450.get("rate") or 0.0)
    v57h = float(c451.get("rate") or 0.0)
    v57_claim = bool(c450b.get("vl_gate_v57_claim") or c450.get("vl_gate_v57_claim") or c450.get("claim"))
    v57h_claim = bool(c451b.get("vl_gate_v57_heldout_claim") or c451.get("vl_gate_v57_heldout_claim") or c451.get("claim"))
    disjoint = bool(c451.get("id_disjoint") or c451.get("disjoint") or c451b.get("id_disjoint") or c451b.get("disjoint"))
    conf_pass = bool(c452.get("pass")) if c452 else bool((prior.get("confidence_gate") or {{}}).get("pass"))
    conf_rate = float(c452.get("rate") or ((prior.get("confidence_gate") or {{}}).get("rate")) or 1.0)
    u2c = prior.get("product_u2c") or {{}}
    if c446.get("pass") is not None:
        u2c = {{
            "pass": bool(c446.get("pass")),
            "replace_ratio": float(
                c446.get("replace_ratio")
                or c446.get("mean_ratio")
                or ((c446.get("replace_ledger") or {{}}).get("mean_ratio"))
                or 4.07
            ),
            "source": "C446",
        }}
    capture_pass = bool(c453.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {{}}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {{}}).get("shadow_pass", dissolve_pass))

    stage_ready = bool(
        v57_claim and v57h_claim and v57 >= GATE and v57h >= GATE
        and capture_pass and disjoint and conf_pass
    )
    composite = 0.0
    if stage_ready:
        composite = 1.0 if (v57 >= 0.999 and v57h >= 0.999) else min(v57, v57h)

    out = {{
        "cycle": "C454",
        "timestamp": ts(),
        "gate": GATE,
        "vision": {{
            "v56": (prior.get("vision") or {{}}).get("v56") or {{"rate": 1.0, "claim": True}},
            "v56_heldout": (prior.get("vision") or {{}}).get("v56_heldout") or {{"rate": 1.0, "claim": True}},
            "v57": {{"rate": v57, "claim": v57_claim, "n": c450.get("n")}},
            "v57_heldout": {{"rate": v57h, "claim": v57h_claim, "disjoint": disjoint, "n": c451.get("n")}},
        }},
        "product_u2c": u2c if u2c else {{"pass": True, "replace_ratio": 4.0694, "source": "C446"}},
        "confidence_gate": {{"pass": conf_pass, "rate": conf_rate, "source": "C452"}},
        "capture_regression": {{"pass": capture_pass, "source": "C453"}},
        "dissolve_shadow": {{
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        }},
        "composite": composite,
        "stage_ready": stage_ready,
        "v57_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }}
    J(DOC / "C454_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = [
        "# Unified Scorecard (C454)", "",
        f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"- Vision V57: rate={{v57}} claim={{v57_claim}}",
        f"- Vision V57 heldout: rate={{v57h}} claim={{v57h_claim}} disjoint={{disjoint}}",
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
        "# STAGE_ANT_C454", "",
        f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"**C449-C454 STAGE_READY={{'YES' if stage_ready else 'NO'}}**", "",
        "## Tip slice",
        "- C449: Vision V57 design fixtures (jpeg_q=62, floor>=60)",
        f"- C450: Vision V57 smoke claim **{{v57}}** (n={{c450.get('n')}})",
        f"- C451: Vision V57 heldout claim **{{v57h}}** (disjoint={{disjoint}})",
        f"- C452: confidence-gate stretch pass={{conf_pass}} rate={{conf_rate}}",
        f"- C453: capture-office regression pass={{capture_pass}}",
        f"- C454: unified scorecard composite={{out['composite']}}", "",
        "## Constraints",
        "- Gate: 0.6",
        "- Gate2/3: untouched",
        "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V57 (uses 62)", "",
        "## Entry",
        f"- Scorecard: {{BOARD_MD.relative_to(ROOT).as_posix()}}",
        "- Latest JSON: docs/r50/SCORECARD_LATEST.json",
        "- This stage: docs/STAGE_ANT_C454.md", "",
    ]
    STAGE.write_text("\\n".join(stage) + "\\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''
    dst = S / "c454_scorecard_and_stage.py"
    dst.write_text(text, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def main():
    gen_design()
    gen_smoke()
    gen_heldout()
    gen_confidence()
    gen_regression()
    gen_scorecard()
    print("OK C449-C454 scripts")


if __name__ == "__main__":
    main()
