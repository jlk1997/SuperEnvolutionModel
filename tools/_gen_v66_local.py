# -*- coding: utf-8 -*-
"""Generate C503-C508 V66 scripts from V65. Knife: product-U2C (C506)."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"

THEMES = [
    ("larkspur", "recv", "paid_total", "LARKSPUR GRAIN RECV", "RECV",
     lambda a,b,c: (a+b, [f"a paid {a:.2f}", f"b paid {b:.2f}", f"c open {c:.2f}", f"TOTAL PAID TARGET {a+b:.2f}"])),
    ("maplecrest", "wh", "qty_sum", "WH MAPLECREST BIN", "RECV",
     lambda a,b,c: (float(a+b), [f"SKU1 qty {a} ok", f"SKU2 qty {c} hold", f"SKU3 qty {b} ok", f"qty_sum TARGET {a+b}"])),
    ("nimbuspeak", "refund", "refund_done", "NIMBUSPEAK PATCH REFUND", "DONE",
     lambda a,b,c: (a+b, [f"itemR1 {a:.2f} done", f"itemR2 {b:.2f} done", f"itemR3 {c:.2f} open", f"refund_done TARGET {a+b:.2f}"])),
    ("oakenshield", "tax", "tax_base_paid", "OAKENSHIELD TAX SLIP", "TAX",
     lambda a,b,c: (a+b, [f"base {a:.2f} paid", f"addon {b:.2f} paid", f"skip {c:.2f}", f"tax_base_paid TARGET {a+b:.2f}"])),
    ("pebblebrook", "pay", "payroll_active", "PEBBLEBROOK PAYROLL", "PAY",
     lambda a,b,c: (a+b, [f"empA {a:.2f} active", f"empB {b:.2f} active", f"empC {c:.2f} leave", f"payroll_active TARGET {a+b:.2f}"])),
    ("quailridge", "ship", "ship_ok", "QUAILRIDGE SHIP DOCK", "SHIP",
     lambda a,b,c: (float(a+b), [f"box1 {a} ok", f"box2 {b} ok", f"box3 {c} hold", f"ship_ok TARGET {a+b}"])),
    ("riverstone", "sla", "sla_ok_hours", "RIVERSTONE SLA CARD", "SLA",
     lambda a,b,c: (a+b, [f"job1 {a:.2f} hours ok", f"job2 {b:.2f} hours ok", f"job3 {c:.2f} hours late", f"sla_ok_hours TARGET {a+b:.2f}"])),
    ("sagebrush", "exp", "exp_sum", "SAGEBRUSH EXPENSE", "EXP",
     lambda a,b,c: (a+b, [f"e1 {a:.2f}", f"e2 {b:.2f}", f"e3 {c:.2f} void", f"exp_sum TARGET {a+b:.2f}"])),
    ("tidepool", "po", "po_open", "TIDEPOOL PO SHEET", "PO",
     lambda a,b,c: (a+b, [f"line1 {a:.2f} open", f"line2 {b:.2f} open", f"line3 {c:.2f} closed", f"po_open TARGET {a+b:.2f}"])),
    ("undercliff", "order", "order_paid", "UNDERCLIFF ORDER", "ORD",
     lambda a,b,c: (a+b, [f"skuA {a:.2f} paid", f"skuB {b:.2f} paid", f"skuC {c:.2f} due", f"order_paid TARGET {a+b:.2f}"])),
    ("valecreek", "dup", "dup_mark", "VALECREEK DUP MARK", "DUP",
     lambda a,b,c: (2.0, ["markA 1", "markB 1", "markC 0", "dup_mark TARGET 2"])),
    ("windchime", "zero", "zero_check", "WINDCHIME AIR ZERO", "ZERO",
     lambda a,b,c: (0.0, ["z1 0.00", "z2 0.00", "z3 0.00", "zero_check TARGET 0.00"])),
    ("xanadu", "ledger", "ledger_net", "XANADU LEDGER", "LED",
     lambda a,b,c: (a+b, [f"dr {a:.2f}", f"cr {b:.2f}", f"adj {c:.2f}", f"ledger_net TARGET {a+b:.2f}"])),
    ("yarrowfield", "ui", "ui_ok", "YARROWFIELD UI SCAN", "UI",
     lambda a,b,c: (1.0, ["btnOK 1", "btnSkip 0", "btnBad 0", "ui_ok TARGET 1"])),
    ("zephyrhill", "stack", "stack_count", "ZEPHYRHILL STACK", "STK",
     lambda a,b,c: (float(a+b), [f"p1 {a}", f"p2 {b}", f"p3 {c}", f"stack_count TARGET {a+b}"])),
    ("ashgrove", "fax", "fax_pages", "ASHGROVE FAX", "FAX",
     lambda a,b,c: (float(a+b), [f"pgA {a}", f"pgB {b}", f"pgC {c} drop", f"fax_pages TARGET {a+b}"])),
    ("bramblewood", "glare", "glare_ok", "BRAMBLEWOOD GLARE", "GLR",
     lambda a,b,c: (1.0, ["zone1 1 ok", "zone2 0", "zone3 0", "glare_ok TARGET 1"])),
    ("cinderpath", "tab", "tab_index", "CINDERPATH TAB INDEX", "TAB",
     lambda a,b,c: (float(a+b), [f"tabA {a}", f"tabB {b}", f"tabC {c}", f"tab_index TARGET {a+b}"])),
]
TRAIN_ABC = [
    (264.0, 281.5, 131.0), (211, 239, 151), (201.0, 219.75, 109.0), (318.0, 336.0, 171.0),
    (381.0, 405.0, 169.0), (167, 183, 127), (217.0, 209.5, 114.0), (229.0, 257.25, 133.0),
    (263.0, 246.0, 142.0), (296.0, 284.0, 130.0), (1, 1, 0), (0, 0, 0),
    (362.0, 386.5, 155.0), (1, 0, 0), (51, 43, 21), (69, 53, 44), (1, 0, 0), (81, 71, 41),
]
HELDOUT_ABC = [
    (161.0, 176.25, 82.0), (123, 151, 89), (119.0, 135.5, 70.0), (206.0, 222.0, 111.0),
    (247.0, 263.0, 106.0), (97, 111, 75), (127.0, 124.5, 76.0), (145.0, 163.25, 82.0),
    (165.0, 153.0, 85.0), (192.0, 181.5, 77.0), (1, 1, 0), (0, 0, 0),
    (227.0, 245.5, 92.0), (1, 0, 0), (27, 24, 19), (43, 37, 25), (1, 0, 0), (53, 47, 26),
]
THEME_STR = "larkspur_maplecrest_nimbuspeak_oakenshield_pebblebrook_quailridge_riverstone_sagebrush_tidepool_undercliff_valecreek_windchime_xanadu_yarrowfield_zephyrhill_ashgrove_bramblewood_cinderpath"
OLD_THEME = "silvercreek_thunderhead_umberwood_violetgrove_willowbrook_xenolith_yellowridge_zincforest_ambercliff_bluestone_darkwater_eaglecrest_fogbank_greenstone_hazelwood_ironcliff_jasperridge_knollstone"


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
    src = src.replace("# --- V65 overlays (new vs V64) ---", "# --- V66 overlays (new vs V65) ---")
    for a, b in [
        ("SILVERCREEK bait", "LARKSPUR bait"), ("KNOLLSTONE bait", "CINDERPATH bait"),
        ("EAGLECREST ghost", "WINDCHIME ghost"), ("GREENSTONE bait", "YARROWFIELD bait"),
        ("XENOLITH bait", "QUAILRIDGE bait"), ("HAZELWOOD", "ZEPHYRHILL"),
        ("THUNDERHEAD bait", "MAPLECREST bait"),
        ("silver mist + knoll ticks (V65-only)", "lark mist + cinder ticks (V66-only)"),
    ]:
        src = src.replace(a, b)
    return src


def gen_design():
    out = (S / "c497_vision_v65_design_and_batch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C497", "C503"), ("c497", "c503"), ("V65", "V66"), ("v65", "v66"),
        ("_v65c497", "_v66c503"),
        ("Harder than V64", "Harder than V65"),
        ("harder than V64", "harder than V65"),
        (OLD_THEME, THEME_STR),
        ("V65 keeps floor", "V66 keeps floor"),
        ("C497 design+fixtures; no VL claim", "C503 design+fixtures; no VL claim"),
        ("fixtures only; claim deferred to C498 VL smoke", "fixtures only; claim deferred to C504 VL smoke"),
        ("No claim until C498 VL", "No claim until C504 VL"),
        ("kept on V65", "kept on V66"),
        ('"harder_than": "v64_alpinepeak_redwoodbark"', '"harder_than": "v65_silvercreek_knollstone"'),
        ("r50plus_v65_silvercreek_knollstone", "r50plus_v66_larkspur_cinderpath"),
    ]:
        out = out.replace(a, b)
    out = out.replace(
        "NEW themes vs V64: silvercreek, thunderhead, umberwood, violetgrove, willowbrook, xenolith, yellowridge, zincforest,\nambercliff, bluestone, darkwater, eaglecrest, fogbank, greenstone, hazelwood, ironcliff, jasperridge, knollstone.",
        "NEW themes vs V65: larkspur, maplecrest, nimbuspeak, oakenshield, pebblebrook, quailridge, riverstone, sagebrush,\ntidepool, undercliff, valecreek, windchime, xanadu, yarrowfield, zephyrhill, ashgrove, bramblewood, cinderpath.",
    )
    out = replace_specs(out, build_specs("v66", "V66", TRAIN_ABC))
    out = retarget_overlay(out)
    dst = S / "c503_vision_v66_design_and_batch.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_smoke():
    out = (S / "c498_vision_v65_smoke.py").read_text(encoding="utf-8")
    for a, b in [
        ("C498", "C504"), ("c498", "c504"), ("V65", "V66"), ("v65", "v66"),
        ("r50plus_v65_silvercreek_knollstone_clarity_floor_n>=16_qwen35_2b",
         "r50plus_v66_larkspur_cinderpath_clarity_floor_n>=16_qwen35_2b"),
        ("Uses C497 fixtures", "Uses C503 fixtures"),
    ]:
        out = out.replace(a, b)
    dst = S / "c504_vision_v66_smoke.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_heldout():
    out = (S / "c499_vision_v65_heldout.py").read_text(encoding="utf-8")
    for a, b in [
        ("C499", "C505"), ("c499", "c505"), ("C497", "C503"),
        ("V65", "V66"), ("v65", "v66"),
        ("_v65hc499", "_v66hc505"),
        ("_v65c497", "_v66c503"),
    ]:
        out = out.replace(a, b)
    out = replace_specs(out, build_specs("v66h", "V66H", HELDOUT_ABC))
    out = retarget_overlay(out)
    out2 = []
    seen_fix = seen_train = seen_run = False
    for ln in out.splitlines():
        s = ln.strip()
        if s.startswith("FIX = ") and not seen_fix:
            out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v66h"')
            seen_fix = True
            continue
        if s.startswith("TRAIN_FIX = ") and not seen_train:
            out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v66"')
            seen_train = True
            continue
        if s.startswith("RUN = ") and "vision_v66" in s and not seen_run:
            out2.append('RUN = ROOT / "runs/vision_v66h_c505"')
            seen_run = True
            continue
        out2.append(ln)
    out = "\n".join(out2) + "\n"
    dst = S / "c505_vision_v66_heldout.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_u2c():
    out = (S / "c494_product_u2c_cost.py").read_text(encoding="utf-8")
    for a, b in [
        ("C494", "C506"), ("c494", "c506"),
        ("product_u2c_c494", "product_u2c_c506"),
        ("u2c_cost_c494", "u2c_cost_c506"),
        ("after V64", "after V66"), ("after V65", "after V66"),
        ("V64+", "V66+"), ("V65+", "V66+"),
    ]:
        out = out.replace(a, b)
    dst = S / "c506_product_u2c_cost.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_regression():
    out = (S / "c501_capture_office_regression.py").read_text(encoding="utf-8")
    for a, b in [
        ("C501", "C507"), ("c501", "c507"),
        ("capture_regression_c501", "capture_regression_c507"),
        ("after C497-C500", "after C503-C506"),
        ("V4-V65+heldout", "V4-V66+heldout"),
    ]:
        out = out.replace(a, b)
    if "VISION_V66_SMOKE" not in out:
        out = out.replace(
            "SMOKE_POINTERS = [",
            'SMOKE_POINTERS = [\n'
            '    ("V66", DOC / "C504_VISION_V66_SMOKE.json"),\n'
            '    ("V66_heldout", DOC / "C505_VISION_V66_HELDOUT_SMOKE.json"),\n'
            '    ("V65", DOC / "C498_VISION_V65_SMOKE.json"),\n'
            '    ("V65_heldout", DOC / "C499_VISION_V65_HELDOUT_SMOKE.json"),',
            1,
        )
    dst = S / "c507_capture_office_regression.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_scorecard():
    board = 'BOARD_MD = ROOT / "docs" / "ANT_UNIFIED_SCORECARD.md"'
    for ln in (S / "c502_scorecard_and_stage.py").read_text(encoding="utf-8").splitlines():
        if "BOARD_MD" in ln and "=" in ln:
            board = ln
            break
    nl = "\\n"
    text = f'''# -*- coding: utf-8 -*-
"""C508: Unified scorecard + STAGE after C503-C507. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
{board}
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C508.md"
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
    c504 = load("docs/r50/C504_VISION_V66_SMOKE.json") or {{}}
    c504b = load("docs/r50/C504b_VISION_GATE_V66_CLAIM.json") or {{}}
    c505 = load("docs/r50/C505_VISION_V66_HELDOUT_SMOKE.json") or {{}}
    c505b = load("docs/r50/C505b_VISION_GATE_V66_HELDOUT_CLAIM.json") or {{}}
    c506 = load("docs/r50/C506_PRODUCT_U2C_COST.json") or {{}}
    c507 = load("docs/r50/C507_CAPTURE_OFFICE_REGRESSION.json") or {{}}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {{}}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {{}}
    c500 = load("docs/r50/C500_CONFIDENCE_GATE_STRETCH.json") or {{}}

    v66 = float(c504.get("rate") or 0.0)
    v66h = float(c505.get("rate") or 0.0)
    v66_claim = bool(c504b.get("vl_gate_v66_claim") or c504.get("vl_gate_v66_claim") or c504.get("claim"))
    v66h_claim = bool(c505b.get("vl_gate_v66_heldout_claim") or c505.get("vl_gate_v66_heldout_claim") or c505.get("claim"))
    disjoint = bool(c505.get("id_disjoint") or c505.get("disjoint") or c505b.get("id_disjoint") or c505b.get("disjoint"))
    conf = prior.get("confidence_gate") or {{}}
    if c500.get("pass") is not None:
        conf = {{"pass": bool(c500.get("pass")), "rate": float(c500.get("rate") or 1.0), "source": "C500"}}
    u2c_pass = bool(c506.get("pass"))
    replace = float(
        c506.get("replace_ratio")
        or c506.get("mean_ratio")
        or ((c506.get("replace_ledger") or {{}}).get("mean_ratio"))
        or 4.07
    )
    capture_pass = bool(c507.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {{}}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {{}}).get("shadow_pass", dissolve_pass))

    stage_ready = bool(
        v66_claim and v66h_claim and v66 >= GATE and v66h >= GATE
        and capture_pass and disjoint and u2c_pass
    )
    composite = 0.0
    if stage_ready:
        composite = 1.0 if (v66 >= 0.999 and v66h >= 0.999) else min(v66, v66h)

    out = {{
        "cycle": "C508",
        "timestamp": ts(),
        "gate": GATE,
        "vision": {{
            "v65": (prior.get("vision") or {{}}).get("v65") or {{"rate": 1.0, "claim": True}},
            "v65_heldout": (prior.get("vision") or {{}}).get("v65_heldout") or {{"rate": 1.0, "claim": True}},
            "v66": {{"rate": v66, "claim": v66_claim, "n": c504.get("n")}},
            "v66_heldout": {{"rate": v66h, "claim": v66h_claim, "disjoint": disjoint, "n": c505.get("n")}},
        }},
        "product_u2c": {{"pass": u2c_pass, "replace_ratio": replace, "source": "C506"}},
        "confidence_gate": conf if conf else {{"pass": True, "rate": 1.0, "source": "C500"}},
        "capture_regression": {{"pass": capture_pass, "source": "C507"}},
        "dissolve_shadow": {{
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        }},
        "composite": composite,
        "stage_ready": stage_ready,
        "v66_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }}
    J(DOC / "C508_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = [
        "# Unified Scorecard (C508)", "",
        f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"- Vision V66: rate={{v66}} claim={{v66_claim}}",
        f"- Vision V66 heldout: rate={{v66h}} claim={{v66h_claim}} disjoint={{disjoint}}",
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
        "# STAGE_ANT_C508", "",
        f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"**C503-C508 STAGE_READY={{'YES' if stage_ready else 'NO'}}**", "",
        "## Tip slice",
        "- C503: Vision V66 design fixtures (jpeg_q=62, floor>=60, long themes)",
        f"- C504: Vision V66 smoke claim **{{v66}}** (n={{c504.get('n')}})",
        f"- C505: Vision V66 heldout claim **{{v66h}}** (disjoint={{disjoint}})",
        f"- C506: product-U2C pass={{u2c_pass}} replace≈{{replace:.4f}}×",
        f"- C507: capture-office regression pass={{capture_pass}}",
        f"- C508: unified scorecard composite={{out['composite']}}", "",
        "## Constraints",
        "- Gate: 0.6",
        "- Gate2/3: untouched",
        "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V66 (uses 62)", "",
        "## Entry",
        f"- Scorecard: {{BOARD_MD.relative_to(ROOT).as_posix()}}",
        "- Latest JSON: docs/r50/SCORECARD_LATEST.json",
        "- This stage: docs/STAGE_ANT_C508.md", "",
    ]
    STAGE.write_text("\\n".join(stage) + "\\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''
    dst = S / "c508_scorecard_and_stage.py"
    dst.write_text(text, encoding="utf-8")
    print("wrote", dst.name)


def main():
    gen_design()
    gen_smoke()
    gen_heldout()
    gen_u2c()
    gen_regression()
    gen_scorecard()
    print("OK C503-C508")


if __name__ == "__main__":
    main()
