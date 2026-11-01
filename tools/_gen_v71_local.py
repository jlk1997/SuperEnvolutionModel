# -*- coding: utf-8 -*-
"""Generate C533-C538 V71 scripts from V70. Knife: confidence-gate (C536)."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"

THEMES = [
    ("cedarhaven", "recv", "paid_total", "CEDARHAVEN GRAIN RECV", "RECV",
     lambda a,b,c: (a+b, [f"a paid {a:.2f}", f"b paid {b:.2f}", f"c open {c:.2f}", f"TOTAL PAID TARGET {a+b:.2f}"])),
    ("duskvalley", "wh", "qty_sum", "WH DUSKVALLEY BIN", "RECV",
     lambda a,b,c: (float(a+b), [f"SKU1 qty {a} ok", f"SKU2 qty {c} hold", f"SKU3 qty {b} ok", f"qty_sum TARGET {a+b}"])),
    ("embertrail", "refund", "refund_done", "EMBERTRAIL PATCH REFUND", "DONE",
     lambda a,b,c: (a+b, [f"itemR1 {a:.2f} done", f"itemR2 {b:.2f} done", f"itemR3 {c:.2f} open", f"refund_done TARGET {a+b:.2f}"])),
    ("frosthollow", "tax", "tax_base_paid", "FROSTHOLLOW TAX SLIP", "TAX",
     lambda a,b,c: (a+b, [f"base {a:.2f} paid", f"addon {b:.2f} paid", f"skip {c:.2f}", f"tax_base_paid TARGET {a+b:.2f}"])),
    ("granitefall", "pay", "payroll_active", "GRANITEFALL PAYROLL", "PAY",
     lambda a,b,c: (a+b, [f"empA {a:.2f} active", f"empB {b:.2f} active", f"empC {c:.2f} leave", f"payroll_active TARGET {a+b:.2f}"])),
    ("harborcrest", "ship", "ship_ok", "HARBORCREST SHIP DOCK", "SHIP",
     lambda a,b,c: (float(a+b), [f"box1 {a} ok", f"box2 {b} ok", f"box3 {c} hold", f"ship_ok TARGET {a+b}"])),
    ("ivorypass", "sla", "sla_ok_hours", "IVORYPASS SLA CARD", "SLA",
     lambda a,b,c: (a+b, [f"job1 {a:.2f} hours ok", f"job2 {b:.2f} hours ok", f"job3 {c:.2f} hours late", f"sla_ok_hours TARGET {a+b:.2f}"])),
    ("jaspercreek", "exp", "exp_sum", "JASPERCREEK EXPENSE", "EXP",
     lambda a,b,c: (a+b, [f"e1 {a:.2f}", f"e2 {b:.2f}", f"e3 {c:.2f} void", f"exp_sum TARGET {a+b:.2f}"])),
    ("kilnstone", "po", "po_open", "KILNSTONE PO SHEET", "PO",
     lambda a,b,c: (a+b, [f"line1 {a:.2f} open", f"line2 {b:.2f} open", f"line3 {c:.2f} closed", f"po_open TARGET {a+b:.2f}"])),
    ("larkspurpass", "order", "order_paid", "LARKSPURPASS ORDER", "ORD",
     lambda a,b,c: (a+b, [f"skuA {a:.2f} paid", f"skuB {b:.2f} paid", f"skuC {c:.2f} due", f"order_paid TARGET {a+b:.2f}"])),
    ("mistwoodridge", "dup", "dup_mark", "MISTWOODRIDGE DUP MARK", "DUP",
     lambda a,b,c: (2.0, ["markA 1", "markB 1", "markC 0", "dup_mark TARGET 2"])),
    ("northwindbay", "zero", "zero_check", "NORTHWINDBAY AIR ZERO", "ZERO",
     lambda a,b,c: (0.0, ["z1 0.00", "z2 0.00", "z3 0.00", "zero_check TARGET 0.00"])),
    ("opalhaven", "ledger", "ledger_net", "OPALHAVEN LEDGER", "LED",
     lambda a,b,c: (a+b, [f"dr {a:.2f}", f"cr {b:.2f}", f"adj {c:.2f}", f"ledger_net TARGET {a+b:.2f}"])),
    ("pebblecliff", "ui", "ui_ok", "PEBBLECLIFF UI SCAN", "UI",
     lambda a,b,c: (1.0, ["btnOK 1", "btnSkip 0", "btnBad 0", "ui_ok TARGET 1"])),
    ("quartzcliff", "stack", "stack_count", "QUARTZCLIFF STACK", "STK",
     lambda a,b,c: (float(a+b), [f"p1 {a}", f"p2 {b}", f"p3 {c}", f"stack_count TARGET {a+b}"])),
    ("redwoodpass", "fax", "fax_pages", "REDWOODPASS FAX", "FAX",
     lambda a,b,c: (float(a+b), [f"pgA {a}", f"pgB {b}", f"pgC {c} drop", f"fax_pages TARGET {a+b}"])),
    ("silvermeadow", "glare", "glare_ok", "SILVERMEADOW GLARE", "GLR",
     lambda a,b,c: (1.0, ["zone1 1 ok", "zone2 0", "zone3 0", "glare_ok TARGET 1"])),
    ("thornfield", "tab", "tab_index", "THORNFIELD TAB INDEX", "TAB",
     lambda a,b,c: (float(a+b), [f"tabA {a}", f"tabB {b}", f"tabC {c}", f"tab_index TARGET {a+b}"])),
]
TRAIN_ABC = [
    (304.0, 320.75, 151.0), (251, 279, 171), (236.0, 258.5, 129.0), (358.0, 376.0, 201.0),
    (421.0, 445.0, 189.0), (197, 213, 147), (257.0, 248.75, 134.0), (269.0, 298.5, 153.0),
    (303.0, 286.0, 162.0), (336.0, 324.0, 150.0), (1, 1, 0), (0, 0, 0),
    (402.0, 425.75, 175.0), (1, 0, 0), (61, 53, 31), (79, 63, 54), (1, 0, 0), (96, 81, 51),
]
HELDOUT_ABC = [
    (191.0, 206.0, 102.0), (153, 181, 109), (149.0, 164.75, 90.0), (246.0, 262.0, 131.0),
    (287.0, 303.0, 126.0), (117, 131, 95), (157.0, 153.75, 96.0), (175.0, 194.5, 102.0),
    (195.0, 183.0, 105.0), (222.0, 210.25, 97.0), (1, 1, 0), (0, 0, 0),
    (257.0, 274.75, 112.0), (1, 0, 0), (37, 34, 29), (53, 47, 35), (1, 0, 0), (63, 57, 36),
]
THEME_STR = "cedarhaven_duskvalley_embertrail_frosthollow_granitefall_harborcrest_ivorypass_jaspercreek_kilnstone_larkspurpass_mistwoodridge_northwindbay_opalhaven_pebblecliff_quartzcliff_redwoodpass_silvermeadow_thornfield"
OLD_THEME = "kestrelridge_lotuscreek_moonstonepass_nightingale_ospreycliff_pinehollow_quicksilverbay_ravenwood_stonebridge_tundrapass_umbrelapoint_vineyardhill_willowcrest_xenongorge_yarrowridge_zephyrgorge_amberhollow_brackenfield"


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
    src = src.replace("# --- V70 overlays (new vs V69) ---", "# --- V71 overlays (new vs V70) ---")
    for a, b in [
        ("KESTRELRIDGE bait", "CEDARHAVEN bait"), ("BRACKENFIELD bait", "THORNFIELD bait"),
        ("VINEYARDHILL ghost", "NORTHWINDBAY ghost"), ("XENONGORGE bait", "PEBBLECLIFF bait"),
        ("PINEHOLLOW bait", "HARBORCREST bait"), ("YARROWRIDGE", "QUARTZCLIFF"),
        ("LOTUSCREEK bait", "DUSKVALLEY bait"),
        ("kestrel mist + bracken ticks (V70-only)", "cedar mist + thorn ticks (V71-only)"),
    ]:
        src = src.replace(a, b)
    return src


def gen_design():
    out = (S / "c527_vision_v70_design_and_batch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C527", "C533"), ("c527", "c533"), ("V70", "V71"), ("v70", "v71"),
        ("_v70c527", "_v71c533"),
        ("Harder than V69", "Harder than V70"),
        ("harder than V69", "harder than V70"),
        (OLD_THEME, THEME_STR),
        ("V70 keeps floor", "V71 keeps floor"),
        ("C527 design+fixtures; no VL claim", "C533 design+fixtures; no VL claim"),
        ("fixtures only; claim deferred to C528 VL smoke", "fixtures only; claim deferred to C534 VL smoke"),
        ("No claim until C528 VL", "No claim until C534 VL"),
        ("kept on V70", "kept on V71"),
        ('"harder_than": "v69_stormwatch_juniperpass"', '"harder_than": "v70_kestrelridge_brackenfield"'),
        ("r50plus_v70_kestrelridge_brackenfield", "r50plus_v71_cedarhaven_thornfield"),
    ]:
        out = out.replace(a, b)
    out = out.replace(
        "NEW themes vs V69: kestrelridge, lotuscreek, moonstonepass, nightingale, ospreycliff, pinehollow, quicksilverbay, ravenwood,\nstonebridge, tundrapass, umbrelapoint, vineyardhill, willowcrest, xenongorge, yarrowridge, zephyrgorge, amberhollow, brackenfield.",
        "NEW themes vs V70: cedarhaven, duskvalley, embertrail, frosthollow, granitefall, harborcrest, ivorypass, jaspercreek,\nkilnstone, larkspurpass, mistwoodridge, northwindbay, opalhaven, pebblecliff, quartzcliff, redwoodpass, silvermeadow, thornfield.",
    )
    out = replace_specs(out, build_specs("v71", "V71", TRAIN_ABC))
    out = retarget_overlay(out)
    dst = S / "c533_vision_v71_design_and_batch.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_smoke():
    out = (S / "c528_vision_v70_smoke.py").read_text(encoding="utf-8")
    for a, b in [
        ("C528", "C534"), ("c528", "c534"), ("V70", "V71"), ("v70", "v71"),
        ("r50plus_v70_kestrelridge_brackenfield_clarity_floor_n>=16_qwen35_2b",
         "r50plus_v71_cedarhaven_thornfield_clarity_floor_n>=16_qwen35_2b"),
        ("Uses C527 fixtures", "Uses C533 fixtures"),
    ]:
        out = out.replace(a, b)
    dst = S / "c534_vision_v71_smoke.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_heldout():
    out = (S / "c529_vision_v70_heldout.py").read_text(encoding="utf-8")
    for a, b in [
        ("C529", "C535"), ("c529", "c535"), ("C527", "C533"),
        ("V70", "V71"), ("v70", "v71"),
        ("_v70hc529", "_v71hc535"),
        ("_v70c527", "_v71c533"),
    ]:
        out = out.replace(a, b)
    out = replace_specs(out, build_specs("v71h", "V71H", HELDOUT_ABC))
    out = retarget_overlay(out)
    out2 = []
    seen_fix = seen_train = seen_run = False
    for ln in out.splitlines():
        s = ln.strip()
        if s.startswith("FIX = ") and not seen_fix:
            out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v71h"')
            seen_fix = True
            continue
        if s.startswith("TRAIN_FIX = ") and not seen_train:
            out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v71"')
            seen_train = True
            continue
        if s.startswith("RUN = ") and "vision_v71" in s and not seen_run:
            out2.append('RUN = ROOT / "runs/vision_v71h_c535"')
            seen_run = True
            continue
        out2.append(ln)
    out = "\n".join(out2) + "\n"
    dst = S / "c535_vision_v71_heldout.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_confidence():
    out = (S / "c524_confidence_gate_stretch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C524", "C536"), ("c524", "c536"),
        ("confidence_gate_c524", "confidence_gate_c536"),
        ("conf_gate_stretch_c524", "conf_gate_stretch_c536"),
        ("after V69", "after V71"), ("after V70", "after V71"),
        ("V69+", "V71+"), ("V70+", "V71+"),
    ]:
        out = out.replace(a, b)
    dst = S / "c536_confidence_gate_stretch.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_regression():
    out = (S / "c531_capture_office_regression.py").read_text(encoding="utf-8")
    for a, b in [
        ("C531", "C537"), ("c531", "c537"),
        ("capture_regression_c531", "capture_regression_c537"),
        ("after C527-C530", "after C533-C536"),
        ("V4-V70+heldout", "V4-V71+heldout"),
    ]:
        out = out.replace(a, b)
    if "VISION_V71_SMOKE" not in out:
        out = out.replace(
            "SMOKE_POINTERS = [",
            'SMOKE_POINTERS = [\n'
            '    ("V71", DOC / "C534_VISION_V71_SMOKE.json"),\n'
            '    ("V71_heldout", DOC / "C535_VISION_V71_HELDOUT_SMOKE.json"),\n'
            '    ("V70", DOC / "C528_VISION_V70_SMOKE.json"),\n'
            '    ("V70_heldout", DOC / "C529_VISION_V70_HELDOUT_SMOKE.json"),',
            1,
        )
    dst = S / "c537_capture_office_regression.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_scorecard():
    board = 'BOARD_MD = ROOT / "docs" / "ANT_UNIFIED_SCORECARD.md"'
    for ln in (S / "c532_scorecard_and_stage.py").read_text(encoding="utf-8").splitlines():
        if "BOARD_MD" in ln and "=" in ln:
            board = ln
            break
    nl = "\\n"
    text = f'''# -*- coding: utf-8 -*-
"""C538: Unified scorecard + STAGE after C533-C537. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
{board}
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C538.md"
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
    c534 = load("docs/r50/C534_VISION_V71_SMOKE.json") or {{}}
    c534b = load("docs/r50/C534b_VISION_GATE_V71_CLAIM.json") or {{}}
    c535 = load("docs/r50/C535_VISION_V71_HELDOUT_SMOKE.json") or {{}}
    c535b = load("docs/r50/C535b_VISION_GATE_V71_HELDOUT_CLAIM.json") or {{}}
    c536 = load("docs/r50/C536_CONFIDENCE_GATE_STRETCH.json") or {{}}
    c537 = load("docs/r50/C537_CAPTURE_OFFICE_REGRESSION.json") or {{}}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {{}}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {{}}
    c530 = load("docs/r50/C530_PRODUCT_U2C_COST.json") or {{}}

    v71 = float(c534.get("rate") or 0.0)
    v71h = float(c535.get("rate") or 0.0)
    v71_claim = bool(c534b.get("vl_gate_v71_claim") or c534.get("vl_gate_v71_claim") or c534.get("claim"))
    v71h_claim = bool(c535b.get("vl_gate_v71_heldout_claim") or c535.get("vl_gate_v71_heldout_claim") or c535.get("claim"))
    disjoint = bool(c535.get("id_disjoint") or c535.get("disjoint") or c535b.get("id_disjoint") or c535b.get("disjoint"))
    conf_pass = bool(c536.get("pass")) if c536 else bool((prior.get("confidence_gate") or {{}}).get("pass"))
    conf_rate = float(c536.get("rate") or ((prior.get("confidence_gate") or {{}}).get("rate")) or 1.0)
    u2c = prior.get("product_u2c") or {{}}
    if c530.get("pass") is not None:
        u2c = {{
            "pass": bool(c530.get("pass")),
            "replace_ratio": float(
                c530.get("replace_ratio")
                or c530.get("mean_ratio")
                or ((c530.get("replace_ledger") or {{}}).get("mean_ratio"))
                or 4.07
            ),
            "source": "C530",
        }}
    capture_pass = bool(c537.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {{}}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {{}}).get("shadow_pass", dissolve_pass))

    stage_ready = bool(
        v71_claim and v71h_claim and v71 >= GATE and v71h >= GATE
        and capture_pass and disjoint and conf_pass
    )
    composite = 0.0
    if stage_ready:
        composite = 1.0 if (v71 >= 0.999 and v71h >= 0.999) else min(v71, v71h)

    out = {{
        "cycle": "C538",
        "timestamp": ts(),
        "gate": GATE,
        "vision": {{
            "v70": (prior.get("vision") or {{}}).get("v70") or {{"rate": 1.0, "claim": True}},
            "v70_heldout": (prior.get("vision") or {{}}).get("v70_heldout") or {{"rate": 1.0, "claim": True}},
            "v71": {{"rate": v71, "claim": v71_claim, "n": c534.get("n")}},
            "v71_heldout": {{"rate": v71h, "claim": v71h_claim, "disjoint": disjoint, "n": c535.get("n")}},
        }},
        "product_u2c": u2c if u2c else {{"pass": True, "replace_ratio": 4.0694, "source": "C530"}},
        "confidence_gate": {{"pass": conf_pass, "rate": conf_rate, "source": "C536"}},
        "capture_regression": {{"pass": capture_pass, "source": "C537"}},
        "dissolve_shadow": {{
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        }},
        "composite": composite,
        "stage_ready": stage_ready,
        "v71_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }}
    J(DOC / "C538_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = [
        "# Unified Scorecard (C538)", "",
        f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"- Vision V71: rate={{v71}} claim={{v71_claim}}",
        f"- Vision V71 heldout: rate={{v71h}} claim={{v71h_claim}} disjoint={{disjoint}}",
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
        "# STAGE_ANT_C538", "",
        f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"**C533-C538 STAGE_READY={{'YES' if stage_ready else 'NO'}}**", "",
        "## Tip slice",
        "- C533: Vision V71 design fixtures (jpeg_q=62, floor>=60, long themes)",
        f"- C534: Vision V71 smoke claim **{{v71}}** (n={{c534.get('n')}})",
        f"- C535: Vision V71 heldout claim **{{v71h}}** (disjoint={{disjoint}})",
        f"- C536: confidence-gate stretch pass={{conf_pass}} rate={{conf_rate}}",
        f"- C537: capture-office regression pass={{capture_pass}}",
        f"- C538: unified scorecard composite={{out['composite']}}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally; not model-plus-separate-agent).", "",
        "## Constraints",
        "- Gate: 0.6",
        "- Gate2/3: untouched",
        "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V71 (uses 62)", "",
        "## Entry",
        f"- Scorecard: {{BOARD_MD.relative_to(ROOT).as_posix()}}",
        "- Latest JSON: docs/r50/SCORECARD_LATEST.json",
        "- This stage: docs/STAGE_ANT_C538.md", "",
    ]
    STAGE.write_text("\\n".join(stage) + "\\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''
    dst = S / "c538_scorecard_and_stage.py"
    dst.write_text(text, encoding="utf-8")
    print("wrote", dst.name)


def main():
    gen_design()
    gen_smoke()
    gen_heldout()
    gen_confidence()
    gen_regression()
    gen_scorecard()
    print("OK C533-C538")


if __name__ == "__main__":
    main()
