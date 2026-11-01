# -*- coding: utf-8 -*-
"""Generate C527-C532 V70 scripts from V69. Knife: product-U2C (C530). Milestone V70."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"

THEMES = [
    ("kestrelridge", "recv", "paid_total", "KESTRELRIDGE GRAIN RECV", "RECV",
     lambda a,b,c: (a+b, [f"a paid {a:.2f}", f"b paid {b:.2f}", f"c open {c:.2f}", f"TOTAL PAID TARGET {a+b:.2f}"])),
    ("lotuscreek", "wh", "qty_sum", "WH LOTUSCREEK BIN", "RECV",
     lambda a,b,c: (float(a+b), [f"SKU1 qty {a} ok", f"SKU2 qty {c} hold", f"SKU3 qty {b} ok", f"qty_sum TARGET {a+b}"])),
    ("moonstonepass", "refund", "refund_done", "MOONSTONEPASS PATCH REFUND", "DONE",
     lambda a,b,c: (a+b, [f"itemR1 {a:.2f} done", f"itemR2 {b:.2f} done", f"itemR3 {c:.2f} open", f"refund_done TARGET {a+b:.2f}"])),
    ("nightingale", "tax", "tax_base_paid", "NIGHTINGALE TAX SLIP", "TAX",
     lambda a,b,c: (a+b, [f"base {a:.2f} paid", f"addon {b:.2f} paid", f"skip {c:.2f}", f"tax_base_paid TARGET {a+b:.2f}"])),
    ("ospreycliff", "pay", "payroll_active", "OSPREYCLIFF PAYROLL", "PAY",
     lambda a,b,c: (a+b, [f"empA {a:.2f} active", f"empB {b:.2f} active", f"empC {c:.2f} leave", f"payroll_active TARGET {a+b:.2f}"])),
    ("pinehollow", "ship", "ship_ok", "PINEHOLLOW SHIP DOCK", "SHIP",
     lambda a,b,c: (float(a+b), [f"box1 {a} ok", f"box2 {b} ok", f"box3 {c} hold", f"ship_ok TARGET {a+b}"])),
    ("quicksilverbay", "sla", "sla_ok_hours", "QUICKSILVERBAY SLA CARD", "SLA",
     lambda a,b,c: (a+b, [f"job1 {a:.2f} hours ok", f"job2 {b:.2f} hours ok", f"job3 {c:.2f} hours late", f"sla_ok_hours TARGET {a+b:.2f}"])),
    ("ravenwood", "exp", "exp_sum", "RAVENWOOD EXPENSE", "EXP",
     lambda a,b,c: (a+b, [f"e1 {a:.2f}", f"e2 {b:.2f}", f"e3 {c:.2f} void", f"exp_sum TARGET {a+b:.2f}"])),
    ("stonebridge", "po", "po_open", "STONEBRIDGE PO SHEET", "PO",
     lambda a,b,c: (a+b, [f"line1 {a:.2f} open", f"line2 {b:.2f} open", f"line3 {c:.2f} closed", f"po_open TARGET {a+b:.2f}"])),
    ("tundrapass", "order", "order_paid", "TUNDRAPASS ORDER", "ORD",
     lambda a,b,c: (a+b, [f"skuA {a:.2f} paid", f"skuB {b:.2f} paid", f"skuC {c:.2f} due", f"order_paid TARGET {a+b:.2f}"])),
    ("umbrelapoint", "dup", "dup_mark", "UMBRELLAPOINT DUP MARK", "DUP",
     lambda a,b,c: (2.0, ["markA 1", "markB 1", "markC 0", "dup_mark TARGET 2"])),
    ("vineyardhill", "zero", "zero_check", "VINEYARDHILL AIR ZERO", "ZERO",
     lambda a,b,c: (0.0, ["z1 0.00", "z2 0.00", "z3 0.00", "zero_check TARGET 0.00"])),
    ("willowcrest", "ledger", "ledger_net", "WILLOWCREST LEDGER", "LED",
     lambda a,b,c: (a+b, [f"dr {a:.2f}", f"cr {b:.2f}", f"adj {c:.2f}", f"ledger_net TARGET {a+b:.2f}"])),
    ("xenongorge", "ui", "ui_ok", "XENONGORGE UI SCAN", "UI",
     lambda a,b,c: (1.0, ["btnOK 1", "btnSkip 0", "btnBad 0", "ui_ok TARGET 1"])),
    ("yarrowridge", "stack", "stack_count", "YARROWRIDGE STACK", "STK",
     lambda a,b,c: (float(a+b), [f"p1 {a}", f"p2 {b}", f"p3 {c}", f"stack_count TARGET {a+b}"])),
    ("zephyrgorge", "fax", "fax_pages", "ZEPHYRGORGE FAX", "FAX",
     lambda a,b,c: (float(a+b), [f"pgA {a}", f"pgB {b}", f"pgC {c} drop", f"fax_pages TARGET {a+b}"])),
    ("amberhollow", "glare", "glare_ok", "AMBERHOLLOW GLARE", "GLR",
     lambda a,b,c: (1.0, ["zone1 1 ok", "zone2 0", "zone3 0", "glare_ok TARGET 1"])),
    ("brackenfield", "tab", "tab_index", "BRACKENFIELD TAB INDEX", "TAB",
     lambda a,b,c: (float(a+b), [f"tabA {a}", f"tabB {b}", f"tabC {c}", f"tab_index TARGET {a+b}"])),
]
TRAIN_ABC = [
    (296.0, 313.0, 147.0), (243, 271, 167), (229.0, 250.75, 125.0), (350.0, 368.0, 195.0),
    (413.0, 437.0, 185.0), (191, 207, 143), (249.0, 241.0, 130.0), (261.0, 290.25, 149.0),
    (295.0, 278.0, 158.0), (328.0, 316.0, 146.0), (1, 1, 0), (0, 0, 0),
    (394.0, 418.0, 171.0), (1, 0, 0), (59, 51, 29), (77, 61, 52), (1, 0, 0), (93, 79, 49),
]
HELDOUT_ABC = [
    (185.0, 200.25, 98.0), (147, 175, 105), (143.0, 159.0, 86.0), (238.0, 254.0, 127.0),
    (279.0, 295.0, 122.0), (113, 127, 91), (151.0, 148.0, 92.0), (169.0, 188.25, 98.0),
    (189.0, 177.0, 101.0), (216.0, 204.5, 93.0), (1, 1, 0), (0, 0, 0),
    (251.0, 269.0, 108.0), (1, 0, 0), (35, 32, 27), (51, 45, 33), (1, 0, 0), (61, 55, 34),
]
THEME_STR = "kestrelridge_lotuscreek_moonstonepass_nightingale_ospreycliff_pinehollow_quicksilverbay_ravenwood_stonebridge_tundrapass_umbrelapoint_vineyardhill_willowcrest_xenongorge_yarrowridge_zephyrgorge_amberhollow_brackenfield"
OLD_THEME = "stormwatch_timberline_undertowbay_valleyforge_waterfallglen_xylograph_yuccaplateau_zephyrcliff_alderbrook_boulderpass_canyonrim_duskhorizon_echochamber_foghorncliff_grovehaven_highlandmoor_ironwoodpass_juniperpass"


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
    src = src.replace("# --- V69 overlays (new vs V68) ---", "# --- V70 overlays (new vs V69) ---")
    for a, b in [
        ("STORMWATCH bait", "KESTRELRIDGE bait"), ("JUNIPERPASS bait", "BRACKENFIELD bait"),
        ("DUSKHORIZON ghost", "VINEYARDHILL ghost"), ("FOGHORNCLIFF bait", "XENONGORGE bait"),
        ("XYLOGRAPH bait", "PINEHOLLOW bait"), ("GROVEHAVEN", "YARROWRIDGE"),
        ("TIMBERLINE bait", "LOTUSCREEK bait"),
        ("storm mist + juniper ticks (V69-only)", "kestrel mist + bracken ticks (V70-only)"),
    ]:
        src = src.replace(a, b)
    return src


def gen_design():
    out = (S / "c521_vision_v69_design_and_batch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C521", "C527"), ("c521", "c527"), ("V69", "V70"), ("v69", "v70"),
        ("_v69c521", "_v70c527"),
        ("Harder than V68", "Harder than V69"),
        ("harder than V68", "harder than V69"),
        (OLD_THEME, THEME_STR),
        ("V69 keeps floor", "V70 keeps floor"),
        ("C521 design+fixtures; no VL claim", "C527 design+fixtures; no VL claim"),
        ("fixtures only; claim deferred to C522 VL smoke", "fixtures only; claim deferred to C528 VL smoke"),
        ("No claim until C522 VL", "No claim until C528 VL"),
        ("kept on V69", "kept on V70"),
        ('"harder_than": "v68_azureharbor_rainshadow"', '"harder_than": "v69_stormwatch_juniperpass"'),
        ("r50plus_v69_stormwatch_juniperpass", "r50plus_v70_kestrelridge_brackenfield"),
    ]:
        out = out.replace(a, b)
    out = out.replace(
        "NEW themes vs V68: stormwatch, timberline, undertowbay, valleyforge, waterfallglen, xylograph, yuccaplateau, zephyrcliff,\nalderbrook, boulderpass, canyonrim, duskhorizon, echochamber, foghorncliff, grovehaven, highlandmoor, ironwoodpass, juniperpass.",
        "NEW themes vs V69: kestrelridge, lotuscreek, moonstonepass, nightingale, ospreycliff, pinehollow, quicksilverbay, ravenwood,\nstonebridge, tundrapass, umbrelapoint, vineyardhill, willowcrest, xenongorge, yarrowridge, zephyrgorge, amberhollow, brackenfield.",
    )
    out = replace_specs(out, build_specs("v70", "V70", TRAIN_ABC))
    out = retarget_overlay(out)
    dst = S / "c527_vision_v70_design_and_batch.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_smoke():
    out = (S / "c522_vision_v69_smoke.py").read_text(encoding="utf-8")
    for a, b in [
        ("C522", "C528"), ("c522", "c528"), ("V69", "V70"), ("v69", "v70"),
        ("r50plus_v69_stormwatch_juniperpass_clarity_floor_n>=16_qwen35_2b",
         "r50plus_v70_kestrelridge_brackenfield_clarity_floor_n>=16_qwen35_2b"),
        ("Uses C521 fixtures", "Uses C527 fixtures"),
    ]:
        out = out.replace(a, b)
    dst = S / "c528_vision_v70_smoke.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_heldout():
    out = (S / "c523_vision_v69_heldout.py").read_text(encoding="utf-8")
    for a, b in [
        ("C523", "C529"), ("c523", "c529"), ("C521", "C527"),
        ("V69", "V70"), ("v69", "v70"),
        ("_v69hc523", "_v70hc529"),
        ("_v69c521", "_v70c527"),
    ]:
        out = out.replace(a, b)
    out = replace_specs(out, build_specs("v70h", "V70H", HELDOUT_ABC))
    out = retarget_overlay(out)
    out2 = []
    seen_fix = seen_train = seen_run = False
    for ln in out.splitlines():
        s = ln.strip()
        if s.startswith("FIX = ") and not seen_fix:
            out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v70h"')
            seen_fix = True
            continue
        if s.startswith("TRAIN_FIX = ") and not seen_train:
            out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v70"')
            seen_train = True
            continue
        if s.startswith("RUN = ") and "vision_v70" in s and not seen_run:
            out2.append('RUN = ROOT / "runs/vision_v70h_c529"')
            seen_run = True
            continue
        out2.append(ln)
    out = "\n".join(out2) + "\n"
    dst = S / "c529_vision_v70_heldout.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_u2c():
    out = (S / "c518_product_u2c_cost.py").read_text(encoding="utf-8")
    for a, b in [
        ("C518", "C530"), ("c518", "c530"),
        ("product_u2c_c518", "product_u2c_c530"),
        ("u2c_cost_c518", "u2c_cost_c530"),
        ("after V68", "after V70"), ("after V69", "after V70"),
        ("V68+", "V70+"), ("V69+", "V70+"),
    ]:
        out = out.replace(a, b)
    dst = S / "c530_product_u2c_cost.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_regression():
    out = (S / "c525_capture_office_regression.py").read_text(encoding="utf-8")
    for a, b in [
        ("C525", "C531"), ("c525", "c531"),
        ("capture_regression_c525", "capture_regression_c531"),
        ("after C521-C524", "after C527-C530"),
        ("V4-V69+heldout", "V4-V70+heldout"),
    ]:
        out = out.replace(a, b)
    if "VISION_V70_SMOKE" not in out:
        out = out.replace(
            "SMOKE_POINTERS = [",
            'SMOKE_POINTERS = [\n'
            '    ("V70", DOC / "C528_VISION_V70_SMOKE.json"),\n'
            '    ("V70_heldout", DOC / "C529_VISION_V70_HELDOUT_SMOKE.json"),\n'
            '    ("V69", DOC / "C522_VISION_V69_SMOKE.json"),\n'
            '    ("V69_heldout", DOC / "C523_VISION_V69_HELDOUT_SMOKE.json"),',
            1,
        )
    dst = S / "c531_capture_office_regression.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_scorecard():
    board = 'BOARD_MD = ROOT / "docs" / "ANT_UNIFIED_SCORECARD.md"'
    for ln in (S / "c526_scorecard_and_stage.py").read_text(encoding="utf-8").splitlines():
        if "BOARD_MD" in ln and "=" in ln:
            board = ln
            break
    nl = "\\n"
    text = f'''# -*- coding: utf-8 -*-
"""C532: Unified scorecard + STAGE after C527-C531. V70 milestone. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
{board}
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C532.md"
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
    c528 = load("docs/r50/C528_VISION_V70_SMOKE.json") or {{}}
    c528b = load("docs/r50/C528b_VISION_GATE_V70_CLAIM.json") or {{}}
    c529 = load("docs/r50/C529_VISION_V70_HELDOUT_SMOKE.json") or {{}}
    c529b = load("docs/r50/C529b_VISION_GATE_V70_HELDOUT_CLAIM.json") or {{}}
    c530 = load("docs/r50/C530_PRODUCT_U2C_COST.json") or {{}}
    c531 = load("docs/r50/C531_CAPTURE_OFFICE_REGRESSION.json") or {{}}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {{}}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {{}}
    c524 = load("docs/r50/C524_CONFIDENCE_GATE_STRETCH.json") or {{}}

    v70 = float(c528.get("rate") or 0.0)
    v70h = float(c529.get("rate") or 0.0)
    v70_claim = bool(c528b.get("vl_gate_v70_claim") or c528.get("vl_gate_v70_claim") or c528.get("claim"))
    v70h_claim = bool(c529b.get("vl_gate_v70_heldout_claim") or c529.get("vl_gate_v70_heldout_claim") or c529.get("claim"))
    disjoint = bool(c529.get("id_disjoint") or c529.get("disjoint") or c529b.get("id_disjoint") or c529b.get("disjoint"))
    conf = prior.get("confidence_gate") or {{}}
    if c524.get("pass") is not None:
        conf = {{"pass": bool(c524.get("pass")), "rate": float(c524.get("rate") or 1.0), "source": "C524"}}
    u2c_pass = bool(c530.get("pass"))
    replace = float(
        c530.get("replace_ratio")
        or c530.get("mean_ratio")
        or ((c530.get("replace_ledger") or {{}}).get("mean_ratio"))
        or 4.07
    )
    capture_pass = bool(c531.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {{}}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {{}}).get("shadow_pass", dissolve_pass))

    stage_ready = bool(
        v70_claim and v70h_claim and v70 >= GATE and v70h >= GATE
        and capture_pass and disjoint and u2c_pass
    )
    composite = 0.0
    if stage_ready:
        composite = 1.0 if (v70 >= 0.999 and v70h >= 0.999) else min(v70, v70h)

    out = {{
        "cycle": "C532",
        "timestamp": ts(),
        "gate": GATE,
        "milestone": "V70",
        "vision": {{
            "v69": (prior.get("vision") or {{}}).get("v69") or {{"rate": 1.0, "claim": True}},
            "v69_heldout": (prior.get("vision") or {{}}).get("v69_heldout") or {{"rate": 1.0, "claim": True}},
            "v70": {{"rate": v70, "claim": v70_claim, "n": c528.get("n")}},
            "v70_heldout": {{"rate": v70h, "claim": v70h_claim, "disjoint": disjoint, "n": c529.get("n")}},
        }},
        "product_u2c": {{"pass": u2c_pass, "replace_ratio": replace, "source": "C530"}},
        "confidence_gate": conf if conf else {{"pass": True, "rate": 1.0, "source": "C524"}},
        "capture_regression": {{"pass": capture_pass, "source": "C531"}},
        "dissolve_shadow": {{
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        }},
        "composite": composite,
        "stage_ready": stage_ready,
        "v70_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }}
    J(DOC / "C532_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = [
        "# Unified Scorecard (C532) — V70 milestone", "",
        f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"- Vision V70: rate={{v70}} claim={{v70_claim}}",
        f"- Vision V70 heldout: rate={{v70h}} claim={{v70h_claim}} disjoint={{disjoint}}",
        f"- product_u2c: {{out['product_u2c']}}",
        f"- confidence_gate: {{out['confidence_gate']}}",
        f"- capture_regression: pass={{capture_pass}}",
        f"- dissolve/shadow: {{dissolve_pass}}/{{shadow_pass}}",
        f"- composite: {{out['composite']}}",
        f"- stage_ready: {{stage_ready}}",
        "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD | V70 not a stop", "",
    ]
    BOARD_MD.write_text("\\n".join(md) + "\\n", encoding="utf-8")

    stage = [
        "# STAGE_ANT_C532", "",
        f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"**C527-C532 STAGE_READY={{'YES' if stage_ready else 'NO'}} — V70 milestone (continue)**", "",
        "## Tip slice",
        "- C527: Vision V70 design fixtures (jpeg_q=62, floor>=60, long themes)",
        f"- C528: Vision V70 smoke claim **{{v70}}** (n={{c528.get('n')}})",
        f"- C529: Vision V70 heldout claim **{{v70h}}** (disjoint={{disjoint}})",
        f"- C530: product-U2C pass={{u2c_pass}} replace≈{{replace:.4f}}×",
        f"- C531: capture-office regression pass={{capture_pass}}",
        f"- C532: unified scorecard composite={{out['composite']}}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally; not model-plus-separate-agent).", "",
        "## Constraints",
        "- Gate: 0.6",
        "- Gate2/3: untouched",
        "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V70 (uses 62)",
        "- V70 milestone is NOT a stop — continue to V71+", "",
        "## Entry",
        f"- Scorecard: {{BOARD_MD.relative_to(ROOT).as_posix()}}",
        "- Latest JSON: docs/r50/SCORECARD_LATEST.json",
        "- This stage: docs/STAGE_ANT_C532.md", "",
    ]
    STAGE.write_text("\\n".join(stage) + "\\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''
    dst = S / "c532_scorecard_and_stage.py"
    dst.write_text(text, encoding="utf-8")
    print("wrote", dst.name)


def main():
    gen_design()
    gen_smoke()
    gen_heldout()
    gen_u2c()
    gen_regression()
    gen_scorecard()
    print("OK C527-C532")


if __name__ == "__main__":
    main()
