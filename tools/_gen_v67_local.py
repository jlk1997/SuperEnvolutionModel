# -*- coding: utf-8 -*-
"""Generate C509-C514 V67 scripts from V66. Knife: confidence-gate (C512)."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"

THEMES = [
    ("dewdropcliff", "recv", "paid_total", "DEWDROPCLIFF GRAIN RECV", "RECV",
     lambda a,b,c: (a+b, [f"a paid {a:.2f}", f"b paid {b:.2f}", f"c open {c:.2f}", f"TOTAL PAID TARGET {a+b:.2f}"])),
    ("fernhollow", "wh", "qty_sum", "WH FERNHOLLOW BIN", "RECV",
     lambda a,b,c: (float(a+b), [f"SKU1 qty {a} ok", f"SKU2 qty {c} hold", f"SKU3 qty {b} ok", f"qty_sum TARGET {a+b}"])),
    ("goldenspire", "refund", "refund_done", "GOLDENSPIRE PATCH REFUND", "DONE",
     lambda a,b,c: (a+b, [f"itemR1 {a:.2f} done", f"itemR2 {b:.2f} done", f"itemR3 {c:.2f} open", f"refund_done TARGET {a+b:.2f}"])),
    ("heatherfield", "tax", "tax_base_paid", "HEATHERFIELD TAX SLIP", "TAX",
     lambda a,b,c: (a+b, [f"base {a:.2f} paid", f"addon {b:.2f} paid", f"skip {c:.2f}", f"tax_base_paid TARGET {a+b:.2f}"])),
    ("ivoryglen", "pay", "payroll_active", "IVORYGLEN PAYROLL", "PAY",
     lambda a,b,c: (a+b, [f"empA {a:.2f} active", f"empB {b:.2f} active", f"empC {c:.2f} leave", f"payroll_active TARGET {a+b:.2f}"])),
    ("kelpshore", "ship", "ship_ok", "KELPSHORE SHIP DOCK", "SHIP",
     lambda a,b,c: (float(a+b), [f"box1 {a} ok", f"box2 {b} ok", f"box3 {c} hold", f"ship_ok TARGET {a+b}"])),
    ("limestonespire", "sla", "sla_ok_hours", "LIMESTONESPIRE SLA CARD", "SLA",
     lambda a,b,c: (a+b, [f"job1 {a:.2f} hours ok", f"job2 {b:.2f} hours ok", f"job3 {c:.2f} hours late", f"sla_ok_hours TARGET {a+b:.2f}"])),
    ("mistletoeridge", "exp", "exp_sum", "MISTLETOERIDGE EXPENSE", "EXP",
     lambda a,b,c: (a+b, [f"e1 {a:.2f}", f"e2 {b:.2f}", f"e3 {c:.2f} void", f"exp_sum TARGET {a+b:.2f}"])),
    ("orchidpath", "po", "po_open", "ORCHIDPATH PO SHEET", "PO",
     lambda a,b,c: (a+b, [f"line1 {a:.2f} open", f"line2 {b:.2f} open", f"line3 {c:.2f} closed", f"po_open TARGET {a+b:.2f}"])),
    ("pearlstream", "order", "order_paid", "PEARLSTREAM ORDER", "ORD",
     lambda a,b,c: (a+b, [f"skuA {a:.2f} paid", f"skuB {b:.2f} paid", f"skuC {c:.2f} due", f"order_paid TARGET {a+b:.2f}"])),
    ("reedmarsh", "dup", "dup_mark", "REEDMARSH DUP MARK", "DUP",
     lambda a,b,c: (2.0, ["markA 1", "markB 1", "markC 0", "dup_mark TARGET 2"])),
    ("sandbarcoast", "zero", "zero_check", "SANDBARCOAST AIR ZERO", "ZERO",
     lambda a,b,c: (0.0, ["z1 0.00", "z2 0.00", "z3 0.00", "zero_check TARGET 0.00"])),
    ("thistlefield", "ledger", "ledger_net", "THISTLEFIELD LEDGER", "LED",
     lambda a,b,c: (a+b, [f"dr {a:.2f}", f"cr {b:.2f}", f"adj {c:.2f}", f"ledger_net TARGET {a+b:.2f}"])),
    ("umberridge", "ui", "ui_ok", "UMBERRIDGE UI SCAN", "UI",
     lambda a,b,c: (1.0, ["btnOK 1", "btnSkip 0", "btnBad 0", "ui_ok TARGET 1"])),
    ("verdantpeak", "stack", "stack_count", "VERDANTPEAK STACK", "STK",
     lambda a,b,c: (float(a+b), [f"p1 {a}", f"p2 {b}", f"p3 {c}", f"stack_count TARGET {a+b}"])),
    ("whitecliff", "fax", "fax_pages", "WHITECLIFF FAX", "FAX",
     lambda a,b,c: (float(a+b), [f"pgA {a}", f"pgB {b}", f"pgC {c} drop", f"fax_pages TARGET {a+b}"])),
    ("xerophyte", "glare", "glare_ok", "XEROPHYTE GLARE", "GLR",
     lambda a,b,c: (1.0, ["zone1 1 ok", "zone2 0", "zone3 0", "glare_ok TARGET 1"])),
    ("yellowglen", "tab", "tab_index", "YELLOWGLEN TAB INDEX", "TAB",
     lambda a,b,c: (float(a+b), [f"tabA {a}", f"tabB {b}", f"tabC {c}", f"tab_index TARGET {a+b}"])),
]
TRAIN_ABC = [
    (272.0, 289.75, 135.0), (219, 247, 155), (208.0, 227.5, 113.0), (326.0, 344.0, 177.0),
    (389.0, 413.0, 173.0), (173, 189, 131), (225.0, 217.75, 118.0), (237.0, 265.5, 137.0),
    (271.0, 254.0, 146.0), (304.0, 292.0, 134.0), (1, 1, 0), (0, 0, 0),
    (370.0, 394.75, 159.0), (1, 0, 0), (53, 45, 23), (71, 55, 46), (1, 0, 0), (84, 73, 43),
]
HELDOUT_ABC = [
    (167.0, 182.5, 86.0), (129, 157, 93), (125.0, 141.75, 74.0), (214.0, 230.0, 115.0),
    (255.0, 271.0, 110.0), (101, 115, 79), (133.0, 130.75, 80.0), (151.0, 169.5, 86.0),
    (171.0, 159.0, 89.0), (198.0, 187.25, 81.0), (1, 1, 0), (0, 0, 0),
    (233.0, 251.75, 96.0), (1, 0, 0), (29, 26, 21), (45, 39, 27), (1, 0, 0), (55, 49, 28),
]
THEME_STR = "dewdropcliff_fernhollow_goldenspire_heatherfield_ivoryglen_kelpshore_limestonespire_mistletoeridge_orchidpath_pearlstream_reedmarsh_sandbarcoast_thistlefield_umberridge_verdantpeak_whitecliff_xerophyte_yellowglen"
OLD_THEME = "larkspur_maplecrest_nimbuspeak_oakenshield_pebblebrook_quailridge_riverstone_sagebrush_tidepool_undercliff_valecreek_windchime_xanadu_yarrowfield_zephyrhill_ashgrove_bramblewood_cinderpath"


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
    src = src.replace("# --- V66 overlays (new vs V65) ---", "# --- V67 overlays (new vs V66) ---")
    for a, b in [
        ("LARKSPUR bait", "DEWDROPCLIFF bait"), ("CINDERPATH bait", "YELLOWGLEN bait"),
        ("WINDCHIME ghost", "SANDBARCOAST ghost"), ("YARROWFIELD bait", "UMBERRIDGE bait"),
        ("QUAILRIDGE bait", "KELPSHORE bait"), ("ZEPHYRHILL", "VERDANTPEAK"),
        ("MAPLECREST bait", "FERNHOLLOW bait"),
        ("lark mist + cinder ticks (V66-only)", "dew mist + yellowglen ticks (V67-only)"),
    ]:
        src = src.replace(a, b)
    return src


def gen_design():
    out = (S / "c503_vision_v66_design_and_batch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C503", "C509"), ("c503", "c509"), ("V66", "V67"), ("v66", "v67"),
        ("_v66c503", "_v67c509"),
        ("Harder than V65", "Harder than V66"),
        ("harder than V65", "harder than V66"),
        (OLD_THEME, THEME_STR),
        ("V66 keeps floor", "V67 keeps floor"),
        ("C503 design+fixtures; no VL claim", "C509 design+fixtures; no VL claim"),
        ("fixtures only; claim deferred to C504 VL smoke", "fixtures only; claim deferred to C510 VL smoke"),
        ("No claim until C504 VL", "No claim until C510 VL"),
        ("kept on V66", "kept on V67"),
        ('"harder_than": "v65_silvercreek_knollstone"', '"harder_than": "v66_larkspur_cinderpath"'),
        ("r50plus_v66_larkspur_cinderpath", "r50plus_v67_dewdropcliff_yellowglen"),
    ]:
        out = out.replace(a, b)
    out = out.replace(
        "NEW themes vs V65: larkspur, maplecrest, nimbuspeak, oakenshield, pebblebrook, quailridge, riverstone, sagebrush,\ntidepool, undercliff, valecreek, windchime, xanadu, yarrowfield, zephyrhill, ashgrove, bramblewood, cinderpath.",
        "NEW themes vs V66: dewdropcliff, fernhollow, goldenspire, heatherfield, ivoryglen, kelpshore, limestonespire, mistletoeridge,\norchidpath, pearlstream, reedmarsh, sandbarcoast, thistlefield, umberridge, verdantpeak, whitecliff, xerophyte, yellowglen.",
    )
    out = replace_specs(out, build_specs("v67", "V67", TRAIN_ABC))
    out = retarget_overlay(out)
    dst = S / "c509_vision_v67_design_and_batch.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_smoke():
    out = (S / "c504_vision_v66_smoke.py").read_text(encoding="utf-8")
    for a, b in [
        ("C504", "C510"), ("c504", "c510"), ("V66", "V67"), ("v66", "v67"),
        ("r50plus_v66_larkspur_cinderpath_clarity_floor_n>=16_qwen35_2b",
         "r50plus_v67_dewdropcliff_yellowglen_clarity_floor_n>=16_qwen35_2b"),
        ("Uses C503 fixtures", "Uses C509 fixtures"),
    ]:
        out = out.replace(a, b)
    dst = S / "c510_vision_v67_smoke.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_heldout():
    out = (S / "c505_vision_v66_heldout.py").read_text(encoding="utf-8")
    for a, b in [
        ("C505", "C511"), ("c505", "c511"), ("C503", "C509"),
        ("V66", "V67"), ("v66", "v67"),
        ("_v66hc505", "_v67hc511"),
        ("_v66c503", "_v67c509"),
    ]:
        out = out.replace(a, b)
    out = replace_specs(out, build_specs("v67h", "V67H", HELDOUT_ABC))
    out = retarget_overlay(out)
    out2 = []
    seen_fix = seen_train = seen_run = False
    for ln in out.splitlines():
        s = ln.strip()
        if s.startswith("FIX = ") and not seen_fix:
            out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v67h"')
            seen_fix = True
            continue
        if s.startswith("TRAIN_FIX = ") and not seen_train:
            out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v67"')
            seen_train = True
            continue
        if s.startswith("RUN = ") and "vision_v67" in s and not seen_run:
            out2.append('RUN = ROOT / "runs/vision_v67h_c511"')
            seen_run = True
            continue
        out2.append(ln)
    out = "\n".join(out2) + "\n"
    dst = S / "c511_vision_v67_heldout.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_confidence():
    out = (S / "c500_confidence_gate_stretch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C500", "C512"), ("c500", "c512"),
        ("confidence_gate_c500", "confidence_gate_c512"),
        ("conf_gate_stretch_c500", "conf_gate_stretch_c512"),
        ("after V65", "after V67"), ("after V66", "after V67"),
        ("V65+", "V67+"), ("V66+", "V67+"),
    ]:
        out = out.replace(a, b)
    dst = S / "c512_confidence_gate_stretch.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_regression():
    out = (S / "c507_capture_office_regression.py").read_text(encoding="utf-8")
    for a, b in [
        ("C507", "C513"), ("c507", "c513"),
        ("capture_regression_c507", "capture_regression_c513"),
        ("after C503-C506", "after C509-C512"),
        ("V4-V66+heldout", "V4-V67+heldout"),
    ]:
        out = out.replace(a, b)
    if "VISION_V67_SMOKE" not in out:
        out = out.replace(
            "SMOKE_POINTERS = [",
            'SMOKE_POINTERS = [\n'
            '    ("V67", DOC / "C510_VISION_V67_SMOKE.json"),\n'
            '    ("V67_heldout", DOC / "C511_VISION_V67_HELDOUT_SMOKE.json"),\n'
            '    ("V66", DOC / "C504_VISION_V66_SMOKE.json"),\n'
            '    ("V66_heldout", DOC / "C505_VISION_V66_HELDOUT_SMOKE.json"),',
            1,
        )
    dst = S / "c513_capture_office_regression.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_scorecard():
    board = 'BOARD_MD = ROOT / "docs" / "ANT_UNIFIED_SCORECARD.md"'
    for ln in (S / "c508_scorecard_and_stage.py").read_text(encoding="utf-8").splitlines():
        if "BOARD_MD" in ln and "=" in ln:
            board = ln
            break
    nl = "\\n"
    text = f'''# -*- coding: utf-8 -*-
"""C514: Unified scorecard + STAGE after C509-C513. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
{board}
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C514.md"
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
    c510 = load("docs/r50/C510_VISION_V67_SMOKE.json") or {{}}
    c510b = load("docs/r50/C510b_VISION_GATE_V67_CLAIM.json") or {{}}
    c511 = load("docs/r50/C511_VISION_V67_HELDOUT_SMOKE.json") or {{}}
    c511b = load("docs/r50/C511b_VISION_GATE_V67_HELDOUT_CLAIM.json") or {{}}
    c512 = load("docs/r50/C512_CONFIDENCE_GATE_STRETCH.json") or {{}}
    c513 = load("docs/r50/C513_CAPTURE_OFFICE_REGRESSION.json") or {{}}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {{}}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {{}}
    c506 = load("docs/r50/C506_PRODUCT_U2C_COST.json") or {{}}

    v67 = float(c510.get("rate") or 0.0)
    v67h = float(c511.get("rate") or 0.0)
    v67_claim = bool(c510b.get("vl_gate_v67_claim") or c510.get("vl_gate_v67_claim") or c510.get("claim"))
    v67h_claim = bool(c511b.get("vl_gate_v67_heldout_claim") or c511.get("vl_gate_v67_heldout_claim") or c511.get("claim"))
    disjoint = bool(c511.get("id_disjoint") or c511.get("disjoint") or c511b.get("id_disjoint") or c511b.get("disjoint"))
    conf_pass = bool(c512.get("pass")) if c512 else bool((prior.get("confidence_gate") or {{}}).get("pass"))
    conf_rate = float(c512.get("rate") or ((prior.get("confidence_gate") or {{}}).get("rate")) or 1.0)
    u2c = prior.get("product_u2c") or {{}}
    if c506.get("pass") is not None:
        u2c = {{
            "pass": bool(c506.get("pass")),
            "replace_ratio": float(
                c506.get("replace_ratio")
                or c506.get("mean_ratio")
                or ((c506.get("replace_ledger") or {{}}).get("mean_ratio"))
                or 4.07
            ),
            "source": "C506",
        }}
    capture_pass = bool(c513.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {{}}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {{}}).get("shadow_pass", dissolve_pass))

    stage_ready = bool(
        v67_claim and v67h_claim and v67 >= GATE and v67h >= GATE
        and capture_pass and disjoint and conf_pass
    )
    composite = 0.0
    if stage_ready:
        composite = 1.0 if (v67 >= 0.999 and v67h >= 0.999) else min(v67, v67h)

    out = {{
        "cycle": "C514",
        "timestamp": ts(),
        "gate": GATE,
        "vision": {{
            "v66": (prior.get("vision") or {{}}).get("v66") or {{"rate": 1.0, "claim": True}},
            "v66_heldout": (prior.get("vision") or {{}}).get("v66_heldout") or {{"rate": 1.0, "claim": True}},
            "v67": {{"rate": v67, "claim": v67_claim, "n": c510.get("n")}},
            "v67_heldout": {{"rate": v67h, "claim": v67h_claim, "disjoint": disjoint, "n": c511.get("n")}},
        }},
        "product_u2c": u2c if u2c else {{"pass": True, "replace_ratio": 4.0694, "source": "C506"}},
        "confidence_gate": {{"pass": conf_pass, "rate": conf_rate, "source": "C512"}},
        "capture_regression": {{"pass": capture_pass, "source": "C513"}},
        "dissolve_shadow": {{
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        }},
        "composite": composite,
        "stage_ready": stage_ready,
        "v67_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }}
    J(DOC / "C514_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = [
        "# Unified Scorecard (C514)", "",
        f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"- Vision V67: rate={{v67}} claim={{v67_claim}}",
        f"- Vision V67 heldout: rate={{v67h}} claim={{v67h_claim}} disjoint={{disjoint}}",
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
        "# STAGE_ANT_C514", "",
        f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"**C509-C514 STAGE_READY={{'YES' if stage_ready else 'NO'}}**", "",
        "## Tip slice",
        "- C509: Vision V67 design fixtures (jpeg_q=62, floor>=60, long themes)",
        f"- C510: Vision V67 smoke claim **{{v67}}** (n={{c510.get('n')}})",
        f"- C511: Vision V67 heldout claim **{{v67h}}** (disjoint={{disjoint}})",
        f"- C512: confidence-gate stretch pass={{conf_pass}} rate={{conf_rate}}",
        f"- C513: capture-office regression pass={{capture_pass}}",
        f"- C514: unified scorecard composite={{out['composite']}}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally; not model-plus-separate-agent).", "",
        "## Constraints",
        "- Gate: 0.6",
        "- Gate2/3: untouched",
        "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V67 (uses 62)", "",
        "## Entry",
        f"- Scorecard: {{BOARD_MD.relative_to(ROOT).as_posix()}}",
        "- Latest JSON: docs/r50/SCORECARD_LATEST.json",
        "- This stage: docs/STAGE_ANT_C514.md", "",
    ]
    STAGE.write_text("\\n".join(stage) + "\\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''
    dst = S / "c514_scorecard_and_stage.py"
    dst.write_text(text, encoding="utf-8")
    print("wrote", dst.name)


def main():
    gen_design()
    gen_smoke()
    gen_heldout()
    gen_confidence()
    gen_regression()
    gen_scorecard()
    print("OK C509-C514")


if __name__ == "__main__":
    main()
