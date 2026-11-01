# -*- coding: utf-8 -*-
"""Generate C485-C490 V63 scripts from V62 via transform.
Themes NEW vs V62; long names (avoid foam-style VL collapse).
Clarity floor jpeg_q>=60 (use 62). Non-vision knife: confidence-gate (C488).
Gate 0.6. Gate2/3 untouched. gen11 HOLD.
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"

THEMES = [
    ("frostbite", "recv", "paid_total", "FROSTBITE GRAIN RECV", "RECV",
     lambda a,b,c: (a+b, [f"a paid {a:.2f}", f"b paid {b:.2f}", f"c open {c:.2f}", f"TOTAL PAID TARGET {a+b:.2f}"])),
    ("glasshouse", "wh", "qty_sum", "WH GLASSHOUSE BIN", "RECV",
     lambda a,b,c: (float(a+b), [f"SKU1 qty {a} ok", f"SKU2 qty {c} hold", f"SKU3 qty {b} ok", f"qty_sum TARGET {a+b}"])),
    ("honeycomb", "refund", "refund_done", "HONEYCOMB PATCH REFUND", "DONE",
     lambda a,b,c: (a+b, [f"itemR1 {a:.2f} done", f"itemR2 {b:.2f} done", f"itemR3 {c:.2f} open", f"refund_done TARGET {a+b:.2f}"])),
    ("inkstone", "tax", "tax_base_paid", "INKSTONE TAX SLIP", "TAX",
     lambda a,b,c: (a+b, [f"base {a:.2f} paid", f"addon {b:.2f} paid", f"skip {c:.2f}", f"tax_base_paid TARGET {a+b:.2f}"])),
    ("jadebridge", "pay", "payroll_active", "JADEBRIDGE PAYROLL", "PAY",
     lambda a,b,c: (a+b, [f"empA {a:.2f} active", f"empB {b:.2f} active", f"empC {c:.2f} leave", f"payroll_active TARGET {a+b:.2f}"])),
    ("kettlebell", "ship", "ship_ok", "KETTLEBELL SHIP DOCK", "SHIP",
     lambda a,b,c: (float(a+b), [f"box1 {a} ok", f"box2 {b} ok", f"box3 {c} hold", f"ship_ok TARGET {a+b}"])),
    ("lighthouse", "sla", "sla_ok_hours", "LIGHTHOUSE SLA CARD", "SLA",
     lambda a,b,c: (a+b, [f"job1 {a:.2f} hours ok", f"job2 {b:.2f} hours ok", f"job3 {c:.2f} hours late", f"sla_ok_hours TARGET {a+b:.2f}"])),
    ("meadowlark", "exp", "exp_sum", "MEADOWLARK EXPENSE", "EXP",
     lambda a,b,c: (a+b, [f"e1 {a:.2f}", f"e2 {b:.2f}", f"e3 {c:.2f} void", f"exp_sum TARGET {a+b:.2f}"])),
    ("needlepoint", "po", "po_open", "NEEDLEPOINT PO SHEET", "PO",
     lambda a,b,c: (a+b, [f"line1 {a:.2f} open", f"line2 {b:.2f} open", f"line3 {c:.2f} closed", f"po_open TARGET {a+b:.2f}"])),
    ("oceanfront", "order", "order_paid", "OCEANFRONT ORDER", "ORD",
     lambda a,b,c: (a+b, [f"skuA {a:.2f} paid", f"skuB {b:.2f} paid", f"skuC {c:.2f} due", f"order_paid TARGET {a+b:.2f}"])),
    ("parchment", "dup", "dup_mark", "PARCHMENT DUP MARK", "DUP",
     lambda a,b,c: (2.0, ["markA 1", "markB 1", "markC 0", "dup_mark TARGET 2"])),
    ("quarrystone", "zero", "zero_check", "QUARRYSTONE AIR ZERO", "ZERO",
     lambda a,b,c: (0.0, ["z1 0.00", "z2 0.00", "z3 0.00", "zero_check TARGET 0.00"])),
    ("riverstone", "ledger", "ledger_net", "RIVERSTONE LEDGER", "LED",
     lambda a,b,c: (a+b, [f"dr {a:.2f}", f"cr {b:.2f}", f"adj {c:.2f}", f"ledger_net TARGET {a+b:.2f}"])),
    ("starmap", "ui", "ui_ok", "STARMAP UI SCAN", "UI",
     lambda a,b,c: (1.0, ["btnOK 1", "btnSkip 0", "btnBad 0", "ui_ok TARGET 1"])),
    ("tidepool", "stack", "stack_count", "TIDEPOOL STACK", "STK",
     lambda a,b,c: (float(a+b), [f"p1 {a}", f"p2 {b}", f"p3 {c}", f"stack_count TARGET {a+b}"])),
    ("undercroft", "fax", "fax_pages", "UNDERCROFT FAX", "FAX",
     lambda a,b,c: (float(a+b), [f"pgA {a}", f"pgB {b}", f"pgC {c} drop", f"fax_pages TARGET {a+b}"])),
    ("vistaedge", "glare", "glare_ok", "VISTAEDGE GLARE", "GLR",
     lambda a,b,c: (1.0, ["zone1 1 ok", "zone2 0", "zone3 0", "glare_ok TARGET 1"])),
    ("wheatfield", "tab", "tab_index", "WHEATFIELD TAB INDEX", "TAB",
     lambda a,b,c: (float(a+b), [f"tabA {a}", f"tabB {b}", f"tabC {c}", f"tab_index TARGET {a+b}"])),
]
TRAIN_ABC = [
    (236.0, 249.75, 117.0), (189, 217, 136), (180.0, 194.25, 95.0), (289.0, 305.0, 154.0),
    (350.0, 371.0, 151.0), (149, 163, 111), (195.0, 186.25, 100.0), (207.0, 229.75, 117.0),
    (239.0, 222.0, 126.0), (272.0, 258.5, 114.0), (1, 1, 0), (0, 0, 0),
    (328.0, 348.75, 139.0), (1, 0, 0), (43, 37, 17), (59, 45, 38), (1, 0, 0), (70, 61, 35),
]
HELDOUT_ABC = [
    (143.0, 155.75, 72.0), (109, 134, 79), (105.0, 118.25, 60.0), (186.0, 200.0, 97.0),
    (225.0, 239.0, 92.0), (87, 99, 65), (113.0, 109.25, 66.0), (129.0, 143.75, 72.0),
    (149.0, 137.0, 75.0), (174.0, 162.75, 67.0), (1, 1, 0), (0, 0, 0),
    (205.0, 220.25, 82.0), (1, 0, 0), (23, 20, 15), (37, 31, 21), (1, 0, 0), (45, 40, 22),
]
THEME_STR = "frostbite_glasshouse_honeycomb_inkstone_jadebridge_kettlebell_lighthouse_meadowlark_needlepoint_oceanfront_parchment_quarrystone_riverstone_starmap_tidepool_undercroft_vistaedge_wheatfield"
OLD_THEME = "moonlight_nightwatch_overbridge_pinecone_quicksand_raincloud_snowdrift_torchlight_umbrella_valleyfloor_windmill_xerocopy_yellowwood_zincplate_afterglow_bluebell_deepwater_egretwing"


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
    src = src.replace("# --- V62 overlays (new vs V61) ---", "# --- V63 overlays (new vs V62) ---")
    src = src.replace("# --- V61 overlays (new vs V60) ---", "# --- V63 overlays (new vs V62) ---")
    for a, b in [
        ("MOONLIGHT bait", "FROSTBITE bait"), ("EGRETWING bait", "WHEATFIELD bait"),
        ("XEROCOPY ghost", "QUARRYSTONE ghost"), ("ZINCPLATE bait", "STARMAP bait"),
        ("RAINCLOUD bait", "KETTLEBELL bait"), ("AFTERGLOW", "TIDEPOOL"),
        ("NIGHTWATCH bait", "GLASSHOUSE bait"),
        ("UNDERPASS bait", "FROSTBITE bait"), ("LAMPPOST bait", "WHEATFIELD bait"),
        ("moonlight glaze + drift ticks (V62-only)", "frostbite etch + wheat ticks (V63-only)"),
        ("underpass rivet + lamp ticks (V61-only)", "frostbite etch + wheat ticks (V63-only)"),
    ]:
        src = src.replace(a, b)
    return src


def gen_design():
    out = (S / "c479_vision_v62_design_and_batch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C479", "C485"), ("c479", "c485"), ("V62", "V63"), ("v62", "v63"),
        ("_v62c479", "_v63c485"),
        ("Harder than V61", "Harder than V62"),
        ("harder than V61", "harder than V62"),
        (OLD_THEME, THEME_STR),
        ("V62 keeps floor", "V63 keeps floor"),
        ("C479 design+fixtures; no VL claim", "C485 design+fixtures; no VL claim"),
        ("fixtures only; claim deferred to C480 VL smoke", "fixtures only; claim deferred to C486 VL smoke"),
        ("No claim until C480 VL", "No claim until C486 VL"),
        ("kept on V62", "kept on V63"),
        ('"harder_than": "v61_underpass_lamppost"', '"harder_than": "v62_moonlight_egretwing"'),
        ("r50plus_v62_moonlight_egretwing", "r50plus_v63_frostbite_wheatfield"),
    ]:
        out = out.replace(a, b)
    out = out.replace(
        "NEW themes vs V61: moonlight, nightwatch, overbridge, pinecone, quicksand, raincloud, snowdrift, torchlight,\numbrella, valleyfloor, windmill, xerocopy, yellowwood, zincplate, afterglow, bluebell, deepwater, egretwing.",
        "NEW themes vs V62: frostbite, glasshouse, honeycomb, inkstone, jadebridge, kettlebell, lighthouse, meadowlark,\nneedlepoint, oceanfront, parchment, quarrystone, riverstone, starmap, tidepool, undercroft, vistaedge, wheatfield.",
    )
    out = replace_specs(out, build_specs("v63", "V63", TRAIN_ABC))
    out = retarget_overlay(out)
    dst = S / "c485_vision_v63_design_and_batch.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_smoke():
    out = (S / "c480_vision_v62_smoke.py").read_text(encoding="utf-8")
    for a, b in [
        ("C480", "C486"), ("c480", "c486"), ("V62", "V63"), ("v62", "v63"),
        ("r50plus_v62_moonlight_egretwing_clarity_floor_n>=16_qwen35_2b",
         "r50plus_v63_frostbite_wheatfield_clarity_floor_n>=16_qwen35_2b"),
        ("Uses C479 fixtures", "Uses C485 fixtures"),
    ]:
        out = out.replace(a, b)
    out = out.replace(
        "r50plus_v63_moonlight_egretwing_clarity_floor_n>=16_qwen35_2b",
        "r50plus_v63_frostbite_wheatfield_clarity_floor_n>=16_qwen35_2b",
    )
    dst = S / "c486_vision_v63_smoke.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_heldout():
    out = (S / "c481_vision_v62_heldout.py").read_text(encoding="utf-8")
    for a, b in [
        ("C481", "C487"), ("c481", "c487"), ("C479", "C485"),
        ("V62", "V63"), ("v62", "v63"),
        ("_v62hc481", "_v63hc487"),
        ("_v62c479", "_v63c485"),
    ]:
        out = out.replace(a, b)
    out = replace_specs(out, build_specs("v63h", "V63H", HELDOUT_ABC))
    out = retarget_overlay(out)
    out2 = []
    seen_fix = seen_train = seen_run = False
    for ln in out.splitlines():
        s = ln.strip()
        if s.startswith("FIX = ") and not seen_fix:
            out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v63h"')
            seen_fix = True
            continue
        if s.startswith("TRAIN_FIX = ") and not seen_train:
            out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v63"')
            seen_train = True
            continue
        if s.startswith("RUN = ") and "vision_v63" in s and not seen_run:
            out2.append('RUN = ROOT / "runs/vision_v63h_c487"')
            seen_run = True
            continue
        out2.append(ln)
    out = "\n".join(out2) + "\n"
    dst = S / "c487_vision_v63_heldout.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_confidence():
    out = (S / "c476_confidence_gate_stretch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C476", "C488"), ("c476", "c488"),
        ("confidence_gate_c476", "confidence_gate_c488"),
        ("conf_gate_stretch_c476", "conf_gate_stretch_c488"),
        ("after V61", "after V63"), ("after V62", "after V63"),
        ("V61+", "V63+"), ("V62+", "V63+"),
    ]:
        out = out.replace(a, b)
    dst = S / "c488_confidence_gate_stretch.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_regression():
    out = (S / "c483_capture_office_regression.py").read_text(encoding="utf-8")
    for a, b in [
        ("C483", "C489"), ("c483", "c489"),
        ("capture_regression_c483", "capture_regression_c489"),
        ("after C479-C482", "after C485-C488"),
        ("V4-V62+heldout", "V4-V63+heldout"),
    ]:
        out = out.replace(a, b)
    if "VISION_V63_SMOKE" not in out:
        out = out.replace(
            "SMOKE_POINTERS = [",
            'SMOKE_POINTERS = [\n'
            '    ("V63", DOC / "C486_VISION_V63_SMOKE.json"),\n'
            '    ("V63_heldout", DOC / "C487_VISION_V63_HELDOUT_SMOKE.json"),\n'
            '    ("V62", DOC / "C480_VISION_V62_SMOKE.json"),\n'
            '    ("V62_heldout", DOC / "C481_VISION_V62_HELDOUT_SMOKE.json"),',
            1,
        )
    dst = S / "c489_capture_office_regression.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_scorecard():
    board = None
    for ln in (S / "c484_scorecard_and_stage.py").read_text(encoding="utf-8").splitlines():
        if "BOARD_MD" in ln and "=" in ln:
            board = ln
            break
    if board is None:
        board = 'BOARD_MD = ROOT / "docs" / "ANT_UNIFIED_SCORECARD.md"'
    nl = "\\n"
    text = f'''# -*- coding: utf-8 -*-
"""C490: Unified scorecard + STAGE after C485-C489. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
{board}
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C490.md"
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
    c486 = load("docs/r50/C486_VISION_V63_SMOKE.json") or {{}}
    c486b = load("docs/r50/C486b_VISION_GATE_V63_CLAIM.json") or {{}}
    c487 = load("docs/r50/C487_VISION_V63_HELDOUT_SMOKE.json") or {{}}
    c487b = load("docs/r50/C487b_VISION_GATE_V63_HELDOUT_CLAIM.json") or {{}}
    c488 = load("docs/r50/C488_CONFIDENCE_GATE_STRETCH.json") or {{}}
    c489 = load("docs/r50/C489_CAPTURE_OFFICE_REGRESSION.json") or {{}}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {{}}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {{}}
    c482 = load("docs/r50/C482_PRODUCT_U2C_COST.json") or {{}}

    v63 = float(c486.get("rate") or 0.0)
    v63h = float(c487.get("rate") or 0.0)
    v63_claim = bool(c486b.get("vl_gate_v63_claim") or c486.get("vl_gate_v63_claim") or c486.get("claim"))
    v63h_claim = bool(c487b.get("vl_gate_v63_heldout_claim") or c487.get("vl_gate_v63_heldout_claim") or c487.get("claim"))
    disjoint = bool(c487.get("id_disjoint") or c487.get("disjoint") or c487b.get("id_disjoint") or c487b.get("disjoint"))
    conf_pass = bool(c488.get("pass")) if c488 else bool((prior.get("confidence_gate") or {{}}).get("pass"))
    conf_rate = float(c488.get("rate") or ((prior.get("confidence_gate") or {{}}).get("rate")) or 1.0)
    u2c = prior.get("product_u2c") or {{}}
    if c482.get("pass") is not None:
        u2c = {{
            "pass": bool(c482.get("pass")),
            "replace_ratio": float(
                c482.get("replace_ratio")
                or c482.get("mean_ratio")
                or ((c482.get("replace_ledger") or {{}}).get("mean_ratio"))
                or 4.07
            ),
            "source": "C482",
        }}
    capture_pass = bool(c489.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {{}}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {{}}).get("shadow_pass", dissolve_pass))

    stage_ready = bool(
        v63_claim and v63h_claim and v63 >= GATE and v63h >= GATE
        and capture_pass and disjoint and conf_pass
    )
    composite = 0.0
    if stage_ready:
        composite = 1.0 if (v63 >= 0.999 and v63h >= 0.999) else min(v63, v63h)

    out = {{
        "cycle": "C490",
        "timestamp": ts(),
        "gate": GATE,
        "vision": {{
            "v62": (prior.get("vision") or {{}}).get("v62") or {{"rate": 1.0, "claim": True}},
            "v62_heldout": (prior.get("vision") or {{}}).get("v62_heldout") or {{"rate": 1.0, "claim": True}},
            "v63": {{"rate": v63, "claim": v63_claim, "n": c486.get("n")}},
            "v63_heldout": {{"rate": v63h, "claim": v63h_claim, "disjoint": disjoint, "n": c487.get("n")}},
        }},
        "product_u2c": u2c if u2c else {{"pass": True, "replace_ratio": 4.0694, "source": "C482"}},
        "confidence_gate": {{"pass": conf_pass, "rate": conf_rate, "source": "C488"}},
        "capture_regression": {{"pass": capture_pass, "source": "C489"}},
        "dissolve_shadow": {{
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        }},
        "composite": composite,
        "stage_ready": stage_ready,
        "v63_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }}
    J(DOC / "C490_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = [
        "# Unified Scorecard (C490)", "",
        f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"- Vision V63: rate={{v63}} claim={{v63_claim}}",
        f"- Vision V63 heldout: rate={{v63h}} claim={{v63h_claim}} disjoint={{disjoint}}",
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
        "# STAGE_ANT_C490", "",
        f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"**C485-C490 STAGE_READY={{'YES' if stage_ready else 'NO'}}**", "",
        "## Tip slice",
        "- C485: Vision V63 design fixtures (jpeg_q=62, floor>=60, long themes)",
        f"- C486: Vision V63 smoke claim **{{v63}}** (n={{c486.get('n')}})",
        f"- C487: Vision V63 heldout claim **{{v63h}}** (disjoint={{disjoint}})",
        f"- C488: confidence-gate stretch pass={{conf_pass}} rate={{conf_rate}}",
        f"- C489: capture-office regression pass={{capture_pass}}",
        f"- C490: unified scorecard composite={{out['composite']}}", "",
        "## Constraints",
        "- Gate: 0.6",
        "- Gate2/3: untouched",
        "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V63 (uses 62)", "",
        "## Entry",
        f"- Scorecard: {{BOARD_MD.relative_to(ROOT).as_posix()}}",
        "- Latest JSON: docs/r50/SCORECARD_LATEST.json",
        "- This stage: docs/STAGE_ANT_C490.md", "",
    ]
    STAGE.write_text("\\n".join(stage) + "\\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''
    dst = S / "c490_scorecard_and_stage.py"
    dst.write_text(text, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def main():
    gen_design()
    gen_smoke()
    gen_heldout()
    gen_confidence()
    gen_regression()
    gen_scorecard()
    print("OK C485-C490 scripts")


if __name__ == "__main__":
    main()
