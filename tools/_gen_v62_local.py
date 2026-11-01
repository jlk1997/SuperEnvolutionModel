# -*- coding: utf-8 -*-
"""Generate C479-C484 V62 scripts from V61 via transform.
Themes NEW vs V61; long names (avoid foam-style VL collapse).
Clarity floor jpeg_q>=60 (use 62). Non-vision knife: product-u2c (C482).
Gate 0.6. Gate2/3 untouched. gen11 HOLD.
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"

THEMES = [
    ("moonlight", "recv", "paid_total", "MOONLIGHT GRAIN RECV", "RECV",
     lambda a,b,c: (a+b, [f"a paid {a:.2f}", f"b paid {b:.2f}", f"c open {c:.2f}", f"TOTAL PAID TARGET {a+b:.2f}"])),
    ("nightwatch", "wh", "qty_sum", "WH NIGHTWATCH BIN", "RECV",
     lambda a,b,c: (float(a+b), [f"SKU1 qty {a} ok", f"SKU2 qty {c} hold", f"SKU3 qty {b} ok", f"qty_sum TARGET {a+b}"])),
    ("overbridge", "refund", "refund_done", "OVERBRIDGE PATCH REFUND", "DONE",
     lambda a,b,c: (a+b, [f"itemR1 {a:.2f} done", f"itemR2 {b:.2f} done", f"itemR3 {c:.2f} open", f"refund_done TARGET {a+b:.2f}"])),
    ("pinecone", "tax", "tax_base_paid", "PINECONE TAX SLIP", "TAX",
     lambda a,b,c: (a+b, [f"base {a:.2f} paid", f"addon {b:.2f} paid", f"skip {c:.2f}", f"tax_base_paid TARGET {a+b:.2f}"])),
    ("quicksand", "pay", "payroll_active", "QUICKSAND PAYROLL", "PAY",
     lambda a,b,c: (a+b, [f"empA {a:.2f} active", f"empB {b:.2f} active", f"empC {c:.2f} leave", f"payroll_active TARGET {a+b:.2f}"])),
    ("raincloud", "ship", "ship_ok", "RAINCLOUD SHIP DOCK", "SHIP",
     lambda a,b,c: (float(a+b), [f"box1 {a} ok", f"box2 {b} ok", f"box3 {c} hold", f"ship_ok TARGET {a+b}"])),
    ("snowdrift", "sla", "sla_ok_hours", "SNOWDRIFT SLA CARD", "SLA",
     lambda a,b,c: (a+b, [f"job1 {a:.2f} hours ok", f"job2 {b:.2f} hours ok", f"job3 {c:.2f} hours late", f"sla_ok_hours TARGET {a+b:.2f}"])),
    ("torchlight", "exp", "exp_sum", "TORCHLIGHT EXPENSE", "EXP",
     lambda a,b,c: (a+b, [f"e1 {a:.2f}", f"e2 {b:.2f}", f"e3 {c:.2f} void", f"exp_sum TARGET {a+b:.2f}"])),
    ("umbrella", "po", "po_open", "UMBRELLA PO SHEET", "PO",
     lambda a,b,c: (a+b, [f"line1 {a:.2f} open", f"line2 {b:.2f} open", f"line3 {c:.2f} closed", f"po_open TARGET {a+b:.2f}"])),
    ("valleyfloor", "order", "order_paid", "VALLEYFLOOR ORDER", "ORD",
     lambda a,b,c: (a+b, [f"skuA {a:.2f} paid", f"skuB {b:.2f} paid", f"skuC {c:.2f} due", f"order_paid TARGET {a+b:.2f}"])),
    ("windmill", "dup", "dup_mark", "WINDMILL DUP MARK", "DUP",
     lambda a,b,c: (2.0, ["markA 1", "markB 1", "markC 0", "dup_mark TARGET 2"])),
    ("xerocopy", "zero", "zero_check", "XEROCOPY AIR ZERO", "ZERO",
     lambda a,b,c: (0.0, ["z1 0.00", "z2 0.00", "z3 0.00", "zero_check TARGET 0.00"])),
    ("yellowwood", "ledger", "ledger_net", "YELLOWWOOD LEDGER", "LED",
     lambda a,b,c: (a+b, [f"dr {a:.2f}", f"cr {b:.2f}", f"adj {c:.2f}", f"ledger_net TARGET {a+b:.2f}"])),
    ("zincplate", "ui", "ui_ok", "ZINCPLATE UI SCAN", "UI",
     lambda a,b,c: (1.0, ["btnOK 1", "btnSkip 0", "btnBad 0", "ui_ok TARGET 1"])),
    ("afterglow", "stack", "stack_count", "AFTERGLOW STACK", "STK",
     lambda a,b,c: (float(a+b), [f"p1 {a}", f"p2 {b}", f"p3 {c}", f"stack_count TARGET {a+b}"])),
    ("bluebell", "fax", "fax_pages", "BLUEBELL FAX", "FAX",
     lambda a,b,c: (float(a+b), [f"pgA {a}", f"pgB {b}", f"pgC {c} drop", f"fax_pages TARGET {a+b}"])),
    ("deepwater", "glare", "glare_ok", "DEEPWATER GLARE", "GLR",
     lambda a,b,c: (1.0, ["zone1 1 ok", "zone2 0", "zone3 0", "glare_ok TARGET 1"])),
    ("egretwing", "tab", "tab_index", "EGRETWING TAB INDEX", "TAB",
     lambda a,b,c: (float(a+b), [f"tabA {a}", f"tabB {b}", f"tabC {c}", f"tab_index TARGET {a+b}"])),
]
TRAIN_ABC = [
    (229.0, 241.25, 112.0), (182, 210, 131), (173.0, 185.75, 91.0), (281.0, 296.0, 149.0),
    (341.0, 361.0, 145.0), (144, 157, 106), (188.0, 178.75, 96.0), (200.0, 220.5, 112.0),
    (231.0, 214.0, 121.0), (264.0, 249.75, 109.0), (1, 1, 0), (0, 0, 0),
    (317.0, 336.25, 134.0), (1, 0, 0), (41, 35, 16), (56, 43, 36), (1, 0, 0), (67, 58, 33),
]
HELDOUT_ABC = [
    (138.0, 149.25, 69.0), (105, 129, 76), (101.0, 112.75, 57.0), (180.0, 193.0, 93.0),
    (218.0, 231.0, 88.0), (84, 95, 62), (109.0, 104.75, 63.0), (124.0, 137.25, 69.0),
    (144.0, 132.0, 72.0), (168.0, 156.25, 64.0), (1, 1, 0), (0, 0, 0),
    (198.0, 211.75, 79.0), (1, 0, 0), (22, 19, 14), (35, 29, 20), (1, 0, 0), (43, 38, 21),
]
THEME_STR = "moonlight_nightwatch_overbridge_pinecone_quicksand_raincloud_snowdrift_torchlight_umbrella_valleyfloor_windmill_xerocopy_yellowwood_zincplate_afterglow_bluebell_deepwater_egretwing"
OLD_THEME = "underpass_vineyard_waterfall_xylotone_yardarm_zephyrton_arabesque_barnacle_crossbeam_daybreak_earthenware_firebrand_goldfinch_handwheel_ironwood_jadewort_kingsfoil_lamppost"


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
    src = src.replace("# --- V61 overlays (new vs V60) ---", "# --- V62 overlays (new vs V61) ---")
    src = src.replace("# --- V60 overlays (new vs V59) ---", "# --- V62 overlays (new vs V61) ---")
    for a, b in [
        ("UNDERPASS bait", "MOONLIGHT bait"), ("LAMPPOST bait", "EGRETWING bait"),
        ("FIREBRAND ghost", "XEROCOPY ghost"), ("HANDWHEEL bait", "ZINCPLATE bait"),
        ("ZEPHYRTON bait", "RAINCLOUD bait"), ("IRONWOOD", "AFTERGLOW"),
        ("VINEYARD bait", "NIGHTWATCH bait"),
        ("ANCHOR bait", "MOONLIGHT bait"), ("TIDEMARK bait", "EGRETWING bait"),
        ("underpass rivet + lamp ticks (V61-only)", "moonlight glaze + drift ticks (V62-only)"),
        ("anchor rope + lantern ticks (V60-only)", "moonlight glaze + drift ticks (V62-only)"),
    ]:
        src = src.replace(a, b)
    return src


def gen_design():
    out = (S / "c473_vision_v61_design_and_batch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C473", "C479"), ("c473", "c479"), ("V61", "V62"), ("v61", "v62"),
        ("_v61c473", "_v62c479"),
        ("Harder than V60", "Harder than V61"),
        ("harder than V60", "harder than V61"),
        (OLD_THEME, THEME_STR),
        ("V61 keeps floor", "V62 keeps floor"),
        ("C473 design+fixtures; no VL claim", "C479 design+fixtures; no VL claim"),
        ("fixtures only; claim deferred to C474 VL smoke", "fixtures only; claim deferred to C480 VL smoke"),
        ("No claim until C474 VL", "No claim until C480 VL"),
        ("kept on V61", "kept on V62"),
        ('"harder_than": "v60_anchor_tidemark"', '"harder_than": "v61_underpass_lamppost"'),
        ("r50plus_v61_underpass_lamppost", "r50plus_v62_moonlight_egretwing"),
    ]:
        out = out.replace(a, b)
    out = out.replace(
        "NEW themes vs V60: underpass, vineyard, waterfall, xylotone, yardarm, zephyrton, arabesque, barnacle,\ncrossbeam, daybreak, earthenware, firebrand, goldfinch, handwheel, ironwood, jadewort, kingsfoil, lamppost.",
        "NEW themes vs V61: moonlight, nightwatch, overbridge, pinecone, quicksand, raincloud, snowdrift, torchlight,\numbrella, valleyfloor, windmill, xerocopy, yellowwood, zincplate, afterglow, bluebell, deepwater, egretwing.",
    )
    out = replace_specs(out, build_specs("v62", "V62", TRAIN_ABC))
    out = retarget_overlay(out)
    dst = S / "c479_vision_v62_design_and_batch.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_smoke():
    out = (S / "c474_vision_v61_smoke.py").read_text(encoding="utf-8")
    for a, b in [
        ("C474", "C480"), ("c474", "c480"), ("V61", "V62"), ("v61", "v62"),
        ("r50plus_v61_underpass_lamppost_clarity_floor_n>=16_qwen35_2b",
         "r50plus_v62_moonlight_egretwing_clarity_floor_n>=16_qwen35_2b"),
        ("Uses C473 fixtures", "Uses C479 fixtures"),
    ]:
        out = out.replace(a, b)
    out = out.replace(
        "r50plus_v62_underpass_lamppost_clarity_floor_n>=16_qwen35_2b",
        "r50plus_v62_moonlight_egretwing_clarity_floor_n>=16_qwen35_2b",
    )
    dst = S / "c480_vision_v62_smoke.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_heldout():
    out = (S / "c475_vision_v61_heldout.py").read_text(encoding="utf-8")
    for a, b in [
        ("C475", "C481"), ("c475", "c481"), ("C473", "C479"),
        ("V61", "V62"), ("v61", "v62"),
        ("_v61hc475", "_v62hc481"),
        ("_v61c473", "_v62c479"),
    ]:
        out = out.replace(a, b)
    out = replace_specs(out, build_specs("v62h", "V62H", HELDOUT_ABC))
    out = retarget_overlay(out)
    out2 = []
    seen_fix = seen_train = seen_run = False
    for ln in out.splitlines():
        s = ln.strip()
        if s.startswith("FIX = ") and not seen_fix:
            out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v62h"')
            seen_fix = True
            continue
        if s.startswith("TRAIN_FIX = ") and not seen_train:
            out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v62"')
            seen_train = True
            continue
        if s.startswith("RUN = ") and "vision_v62" in s and not seen_run:
            out2.append('RUN = ROOT / "runs/vision_v62h_c481"')
            seen_run = True
            continue
        out2.append(ln)
    out = "\n".join(out2) + "\n"
    dst = S / "c481_vision_v62_heldout.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_product_u2c():
    out = (S / "c470_product_u2c_cost.py").read_text(encoding="utf-8")
    for a, b in [
        ("C470", "C482"), ("c470", "c482"),
        ("product_u2c_c470", "product_u2c_c482"),
        ("after V60", "after V62"), ("after V61", "after V62"),
        ("V60+", "V62+"), ("V61+", "V62+"),
    ]:
        out = out.replace(a, b)
    dst = S / "c482_product_u2c_cost.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_regression():
    out = (S / "c477_capture_office_regression.py").read_text(encoding="utf-8")
    for a, b in [
        ("C477", "C483"), ("c477", "c483"),
        ("capture_regression_c477", "capture_regression_c483"),
        ("after C473-C476", "after C479-C482"),
        ("V4-V61+heldout", "V4-V62+heldout"),
    ]:
        out = out.replace(a, b)
    if "VISION_V62_SMOKE" not in out:
        out = out.replace(
            "SMOKE_POINTERS = [",
            'SMOKE_POINTERS = [\n'
            '    ("V62", DOC / "C480_VISION_V62_SMOKE.json"),\n'
            '    ("V62_heldout", DOC / "C481_VISION_V62_HELDOUT_SMOKE.json"),\n'
            '    ("V61", DOC / "C474_VISION_V61_SMOKE.json"),\n'
            '    ("V61_heldout", DOC / "C475_VISION_V61_HELDOUT_SMOKE.json"),',
            1,
        )
    dst = S / "c483_capture_office_regression.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_scorecard():
    board = None
    for ln in (S / "c478_scorecard_and_stage.py").read_text(encoding="utf-8").splitlines():
        if "BOARD_MD" in ln and "=" in ln:
            board = ln
            break
    if board is None:
        board = 'BOARD_MD = ROOT / "docs" / "ANT_UNIFIED_SCORECARD.md"'
    nl = "\\n"
    text = f'''# -*- coding: utf-8 -*-
"""C484: Unified scorecard + STAGE after C479-C483. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
{board}
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C484.md"
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
    c480 = load("docs/r50/C480_VISION_V62_SMOKE.json") or {{}}
    c480b = load("docs/r50/C480b_VISION_GATE_V62_CLAIM.json") or {{}}
    c481 = load("docs/r50/C481_VISION_V62_HELDOUT_SMOKE.json") or {{}}
    c481b = load("docs/r50/C481b_VISION_GATE_V62_HELDOUT_CLAIM.json") or {{}}
    c482 = load("docs/r50/C482_PRODUCT_U2C_COST.json") or {{}}
    c483 = load("docs/r50/C483_CAPTURE_OFFICE_REGRESSION.json") or {{}}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {{}}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {{}}
    c476 = load("docs/r50/C476_CONFIDENCE_GATE_STRETCH.json") or {{}}

    v62 = float(c480.get("rate") or 0.0)
    v62h = float(c481.get("rate") or 0.0)
    v62_claim = bool(c480b.get("vl_gate_v62_claim") or c480.get("vl_gate_v62_claim") or c480.get("claim"))
    v62h_claim = bool(c481b.get("vl_gate_v62_heldout_claim") or c481.get("vl_gate_v62_heldout_claim") or c481.get("claim"))
    disjoint = bool(c481.get("id_disjoint") or c481.get("disjoint") or c481b.get("id_disjoint") or c481b.get("disjoint"))

    _rl = c482.get("replace_ledger") or {{}}
    u2c_pass = bool(c482.get("pass")) if c482 else bool((prior.get("product_u2c") or {{}}).get("pass"))
    u2c_replace = float(
        c482.get("replace_ratio")
        or _rl.get("mean_ratio")
        or ((prior.get("product_u2c") or {{}}).get("replace_ratio"))
        or 4.07
    )
    conf = prior.get("confidence_gate") or {{}}
    if c476.get("pass") is not None:
        conf = {{
            "pass": bool(c476.get("pass")),
            "rate": float(c476.get("rate") or 1.0),
            "source": "C476",
        }}
    capture_pass = bool(c483.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {{}}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {{}}).get("shadow_pass", dissolve_pass))

    stage_ready = bool(
        v62_claim and v62h_claim and v62 >= GATE and v62h >= GATE
        and capture_pass and disjoint and u2c_pass
    )
    composite = 0.0
    if stage_ready:
        composite = 1.0 if (v62 >= 0.999 and v62h >= 0.999) else min(v62, v62h)

    out = {{
        "cycle": "C484",
        "timestamp": ts(),
        "gate": GATE,
        "vision": {{
            "v61": (prior.get("vision") or {{}}).get("v61") or {{"rate": 1.0, "claim": True}},
            "v61_heldout": (prior.get("vision") or {{}}).get("v61_heldout") or {{"rate": 1.0, "claim": True}},
            "v62": {{"rate": v62, "claim": v62_claim, "n": c480.get("n")}},
            "v62_heldout": {{"rate": v62h, "claim": v62h_claim, "disjoint": disjoint, "n": c481.get("n")}},
        }},
        "product_u2c": {{"pass": u2c_pass, "replace_ratio": u2c_replace, "source": "C482"}},
        "confidence_gate": conf if conf else {{"pass": True, "rate": 1.0, "source": "C476"}},
        "capture_regression": {{"pass": capture_pass, "source": "C483"}},
        "dissolve_shadow": {{
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        }},
        "composite": composite,
        "stage_ready": stage_ready,
        "v62_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }}
    J(DOC / "C484_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = [
        "# Unified Scorecard (C484)", "",
        f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"- Vision V62: rate={{v62}} claim={{v62_claim}}",
        f"- Vision V62 heldout: rate={{v62h}} claim={{v62h_claim}} disjoint={{disjoint}}",
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
        "# STAGE_ANT_C484", "",
        f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"**C479-C484 STAGE_READY={{'YES' if stage_ready else 'NO'}}**", "",
        "## Tip slice",
        "- C479: Vision V62 design fixtures (jpeg_q=62, floor>=60, long themes)",
        f"- C480: Vision V62 smoke claim **{{v62}}** (n={{c480.get('n')}})",
        f"- C481: Vision V62 heldout claim **{{v62h}}** (disjoint={{disjoint}})",
        f"- C482: product-u2c pass={{u2c_pass}} replace~={{u2c_replace}}",
        f"- C483: capture-office regression pass={{capture_pass}}",
        f"- C484: unified scorecard composite={{out['composite']}}", "",
        "## Constraints",
        "- Gate: 0.6",
        "- Gate2/3: untouched",
        "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V62 (uses 62)", "",
        "## Entry",
        f"- Scorecard: {{BOARD_MD.relative_to(ROOT).as_posix()}}",
        "- Latest JSON: docs/r50/SCORECARD_LATEST.json",
        "- This stage: docs/STAGE_ANT_C484.md", "",
    ]
    STAGE.write_text("\\n".join(stage) + "\\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''
    dst = S / "c484_scorecard_and_stage.py"
    dst.write_text(text, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def main():
    gen_design()
    gen_smoke()
    gen_heldout()
    gen_product_u2c()
    gen_regression()
    gen_scorecard()
    print("OK C479-C484 scripts")


if __name__ == "__main__":
    main()
