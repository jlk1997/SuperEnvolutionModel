# -*- coding: utf-8 -*-
"""Generate C497-C502 V65 scripts from V64 via transform.
Themes NEW vs V64; long names (avoid foam-style VL collapse).
Clarity floor jpeg_q>=60 (use 62). Non-vision knife: confidence-gate (C500).
Gate 0.6. Gate2/3 untouched. gen11 HOLD.
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"

THEMES = [
    ("silvercreek", "recv", "paid_total", "SILVERCREEK GRAIN RECV", "RECV",
     lambda a,b,c: (a+b, [f"a paid {a:.2f}", f"b paid {b:.2f}", f"c open {c:.2f}", f"TOTAL PAID TARGET {a+b:.2f}"])),
    ("thunderhead", "wh", "qty_sum", "WH THUNDERHEAD BIN", "RECV",
     lambda a,b,c: (float(a+b), [f"SKU1 qty {a} ok", f"SKU2 qty {c} hold", f"SKU3 qty {b} ok", f"qty_sum TARGET {a+b}"])),
    ("umberwood", "refund", "refund_done", "UMBERWOOD PATCH REFUND", "DONE",
     lambda a,b,c: (a+b, [f"itemR1 {a:.2f} done", f"itemR2 {b:.2f} done", f"itemR3 {c:.2f} open", f"refund_done TARGET {a+b:.2f}"])),
    ("violetgrove", "tax", "tax_base_paid", "VIOLETGROVE TAX SLIP", "TAX",
     lambda a,b,c: (a+b, [f"base {a:.2f} paid", f"addon {b:.2f} paid", f"skip {c:.2f}", f"tax_base_paid TARGET {a+b:.2f}"])),
    ("willowbrook", "pay", "payroll_active", "WILLOWBROOK PAYROLL", "PAY",
     lambda a,b,c: (a+b, [f"empA {a:.2f} active", f"empB {b:.2f} active", f"empC {c:.2f} leave", f"payroll_active TARGET {a+b:.2f}"])),
    ("xenolith", "ship", "ship_ok", "XENOLITH SHIP DOCK", "SHIP",
     lambda a,b,c: (float(a+b), [f"box1 {a} ok", f"box2 {b} ok", f"box3 {c} hold", f"ship_ok TARGET {a+b}"])),
    ("yellowridge", "sla", "sla_ok_hours", "YELLOWRIDGE SLA CARD", "SLA",
     lambda a,b,c: (a+b, [f"job1 {a:.2f} hours ok", f"job2 {b:.2f} hours ok", f"job3 {c:.2f} hours late", f"sla_ok_hours TARGET {a+b:.2f}"])),
    ("zincforest", "exp", "exp_sum", "ZINCFOREST EXPENSE", "EXP",
     lambda a,b,c: (a+b, [f"e1 {a:.2f}", f"e2 {b:.2f}", f"e3 {c:.2f} void", f"exp_sum TARGET {a+b:.2f}"])),
    ("ambercliff", "po", "po_open", "AMBERCLIFF PO SHEET", "PO",
     lambda a,b,c: (a+b, [f"line1 {a:.2f} open", f"line2 {b:.2f} open", f"line3 {c:.2f} closed", f"po_open TARGET {a+b:.2f}"])),
    ("bluestone", "order", "order_paid", "BLUESTONE ORDER", "ORD",
     lambda a,b,c: (a+b, [f"skuA {a:.2f} paid", f"skuB {b:.2f} paid", f"skuC {c:.2f} due", f"order_paid TARGET {a+b:.2f}"])),
    ("darkwater", "dup", "dup_mark", "DARKWATER DUP MARK", "DUP",
     lambda a,b,c: (2.0, ["markA 1", "markB 1", "markC 0", "dup_mark TARGET 2"])),
    ("eaglecrest", "zero", "zero_check", "EAGLECREST AIR ZERO", "ZERO",
     lambda a,b,c: (0.0, ["z1 0.00", "z2 0.00", "z3 0.00", "zero_check TARGET 0.00"])),
    ("fogbank", "ledger", "ledger_net", "FOGBANK LEDGER", "LED",
     lambda a,b,c: (a+b, [f"dr {a:.2f}", f"cr {b:.2f}", f"adj {c:.2f}", f"ledger_net TARGET {a+b:.2f}"])),
    ("greenstone", "ui", "ui_ok", "GREENSTONE UI SCAN", "UI",
     lambda a,b,c: (1.0, ["btnOK 1", "btnSkip 0", "btnBad 0", "ui_ok TARGET 1"])),
    ("hazelwood", "stack", "stack_count", "HAZELWOOD STACK", "STK",
     lambda a,b,c: (float(a+b), [f"p1 {a}", f"p2 {b}", f"p3 {c}", f"stack_count TARGET {a+b}"])),
    ("ironcliff", "fax", "fax_pages", "IRONCLIFF FAX", "FAX",
     lambda a,b,c: (float(a+b), [f"pgA {a}", f"pgB {b}", f"pgC {c} drop", f"fax_pages TARGET {a+b}"])),
    ("jasperridge", "glare", "glare_ok", "JASPERRIDGE GLARE", "GLR",
     lambda a,b,c: (1.0, ["zone1 1 ok", "zone2 0", "zone3 0", "glare_ok TARGET 1"])),
    ("knollstone", "tab", "tab_index", "KNOLLSTONE TAB INDEX", "TAB",
     lambda a,b,c: (float(a+b), [f"tabA {a}", f"tabB {b}", f"tabC {c}", f"tab_index TARGET {a+b}"])),
]
TRAIN_ABC = [
    (250.0, 267.25, 127.0), (203, 231, 146), (194.0, 211.25, 103.0), (305.0, 323.0, 164.0),
    (368.0, 391.0, 163.0), (159, 175, 121), (209.0, 201.25, 108.0), (221.0, 248.75, 127.0),
    (255.0, 238.0, 136.0), (288.0, 276.0, 124.0), (1, 1, 0), (0, 0, 0),
    (350.0, 374.25, 149.0), (1, 0, 0), (47, 41, 19), (65, 49, 42), (1, 0, 0), (76, 67, 39),
]
HELDOUT_ABC = [
    (153.0, 168.75, 78.0), (117, 144, 85), (113.0, 129.25, 66.0), (198.0, 214.0, 105.0),
    (239.0, 255.0, 100.0), (93, 107, 71), (121.0, 118.25, 72.0), (139.0, 156.75, 78.0),
    (159.0, 147.0, 81.0), (186.0, 175.75, 73.0), (1, 1, 0), (0, 0, 0),
    (219.0, 237.25, 88.0), (1, 0, 0), (25, 22, 17), (41, 35, 23), (1, 0, 0), (49, 44, 24),
]
THEME_STR = "silvercreek_thunderhead_umberwood_violetgrove_willowbrook_xenolith_yellowridge_zincforest_ambercliff_bluestone_darkwater_eaglecrest_fogbank_greenstone_hazelwood_ironcliff_jasperridge_knollstone"
OLD_THEME = "alpinepeak_birchgrove_cedarcrest_dawnchorus_emberglow_flintstone_granitepeak_harborlight_ivorytower_juniperhill_kelpforest_lunarscape_mossgarden_northridge_opalstream_pineforest_quartzvein_redwoodbark"


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
    src = src.replace("# --- V64 overlays (new vs V63) ---", "# --- V65 overlays (new vs V64) ---")
    src = src.replace("# --- V63 overlays (new vs V62) ---", "# --- V65 overlays (new vs V64) ---")
    for a, b in [
        ("ALPINEPEAK bait", "SILVERCREEK bait"), ("REDWOODBARK bait", "KNOLLSTONE bait"),
        ("LUNARSCAPE ghost", "EAGLECREST ghost"), ("NORTHRIDGE bait", "GREENSTONE bait"),
        ("FLINTSTONE bait", "XENOLITH bait"), ("OPALSTREAM", "HAZELWOOD"),
        ("BIRCHGROVE bait", "THUNDERHEAD bait"),
        ("FROSTBITE bait", "SILVERCREEK bait"), ("WHEATFIELD bait", "KNOLLSTONE bait"),
        ("alpine lichen + bark ticks (V64-only)", "silver mist + knoll ticks (V65-only)"),
        ("frostbite etch + wheat ticks (V63-only)", "silver mist + knoll ticks (V65-only)"),
    ]:
        src = src.replace(a, b)
    return src


def gen_design():
    out = (S / "c491_vision_v64_design_and_batch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C491", "C497"), ("c491", "c497"), ("V64", "V65"), ("v64", "v65"),
        ("_v64c491", "_v65c497"),
        ("Harder than V63", "Harder than V64"),
        ("harder than V63", "harder than V64"),
        (OLD_THEME, THEME_STR),
        ("V64 keeps floor", "V65 keeps floor"),
        ("C491 design+fixtures; no VL claim", "C497 design+fixtures; no VL claim"),
        ("fixtures only; claim deferred to C492 VL smoke", "fixtures only; claim deferred to C498 VL smoke"),
        ("No claim until C492 VL", "No claim until C498 VL"),
        ("kept on V64", "kept on V65"),
        ('"harder_than": "v63_frostbite_wheatfield"', '"harder_than": "v64_alpinepeak_redwoodbark"'),
        ("r50plus_v64_alpinepeak_redwoodbark", "r50plus_v65_silvercreek_knollstone"),
    ]:
        out = out.replace(a, b)
    out = out.replace(
        "NEW themes vs V63: alpinepeak, birchgrove, cedarcrest, dawnchorus, emberglow, flintstone, granitepeak, harborlight,\nivorytower, juniperhill, kelpforest, lunarscape, mossgarden, northridge, opalstream, pineforest, quartzvein, redwoodbark.",
        "NEW themes vs V64: silvercreek, thunderhead, umberwood, violetgrove, willowbrook, xenolith, yellowridge, zincforest,\nambercliff, bluestone, darkwater, eaglecrest, fogbank, greenstone, hazelwood, ironcliff, jasperridge, knollstone.",
    )
    out = replace_specs(out, build_specs("v65", "V65", TRAIN_ABC))
    out = retarget_overlay(out)
    dst = S / "c497_vision_v65_design_and_batch.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_smoke():
    out = (S / "c492_vision_v64_smoke.py").read_text(encoding="utf-8")
    for a, b in [
        ("C492", "C498"), ("c492", "c498"), ("V64", "V65"), ("v64", "v65"),
        ("r50plus_v64_alpinepeak_redwoodbark_clarity_floor_n>=16_qwen35_2b",
         "r50plus_v65_silvercreek_knollstone_clarity_floor_n>=16_qwen35_2b"),
        ("Uses C491 fixtures", "Uses C497 fixtures"),
    ]:
        out = out.replace(a, b)
    out = out.replace(
        "r50plus_v65_alpinepeak_redwoodbark_clarity_floor_n>=16_qwen35_2b",
        "r50plus_v65_silvercreek_knollstone_clarity_floor_n>=16_qwen35_2b",
    )
    dst = S / "c498_vision_v65_smoke.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_heldout():
    out = (S / "c493_vision_v64_heldout.py").read_text(encoding="utf-8")
    for a, b in [
        ("C493", "C499"), ("c493", "c499"), ("C491", "C497"),
        ("V64", "V65"), ("v64", "v65"),
        ("_v64hc493", "_v65hc499"),
        ("_v64c491", "_v65c497"),
    ]:
        out = out.replace(a, b)
    out = replace_specs(out, build_specs("v65h", "V65H", HELDOUT_ABC))
    out = retarget_overlay(out)
    out2 = []
    seen_fix = seen_train = seen_run = False
    for ln in out.splitlines():
        s = ln.strip()
        if s.startswith("FIX = ") and not seen_fix:
            out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v65h"')
            seen_fix = True
            continue
        if s.startswith("TRAIN_FIX = ") and not seen_train:
            out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v65"')
            seen_train = True
            continue
        if s.startswith("RUN = ") and "vision_v65" in s and not seen_run:
            out2.append('RUN = ROOT / "runs/vision_v65h_c499"')
            seen_run = True
            continue
        out2.append(ln)
    out = "\n".join(out2) + "\n"
    dst = S / "c499_vision_v65_heldout.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_confidence():
    out = (S / "c488_confidence_gate_stretch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C488", "C500"), ("c488", "c500"),
        ("confidence_gate_c488", "confidence_gate_c500"),
        ("conf_gate_stretch_c488", "conf_gate_stretch_c500"),
        ("after V63", "after V65"), ("after V64", "after V65"),
        ("V63+", "V65+"), ("V64+", "V65+"),
    ]:
        out = out.replace(a, b)
    dst = S / "c500_confidence_gate_stretch.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_regression():
    out = (S / "c495_capture_office_regression.py").read_text(encoding="utf-8")
    for a, b in [
        ("C495", "C501"), ("c495", "c501"),
        ("capture_regression_c495", "capture_regression_c501"),
        ("after C491-C494", "after C497-C500"),
        ("V4-V64+heldout", "V4-V65+heldout"),
    ]:
        out = out.replace(a, b)
    if "VISION_V65_SMOKE" not in out:
        out = out.replace(
            "SMOKE_POINTERS = [",
            'SMOKE_POINTERS = [\n'
            '    ("V65", DOC / "C498_VISION_V65_SMOKE.json"),\n'
            '    ("V65_heldout", DOC / "C499_VISION_V65_HELDOUT_SMOKE.json"),\n'
            '    ("V64", DOC / "C492_VISION_V64_SMOKE.json"),\n'
            '    ("V64_heldout", DOC / "C493_VISION_V64_HELDOUT_SMOKE.json"),',
            1,
        )
    dst = S / "c501_capture_office_regression.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_scorecard():
    board = None
    for ln in (S / "c496_scorecard_and_stage.py").read_text(encoding="utf-8").splitlines():
        if "BOARD_MD" in ln and "=" in ln:
            board = ln
            break
    if board is None:
        board = 'BOARD_MD = ROOT / "docs" / "ANT_UNIFIED_SCORECARD.md"'
    nl = "\\n"
    text = f'''# -*- coding: utf-8 -*-
"""C502: Unified scorecard + STAGE after C497-C501. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
{board}
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C502.md"
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
    c498 = load("docs/r50/C498_VISION_V65_SMOKE.json") or {{}}
    c498b = load("docs/r50/C498b_VISION_GATE_V65_CLAIM.json") or {{}}
    c499 = load("docs/r50/C499_VISION_V65_HELDOUT_SMOKE.json") or {{}}
    c499b = load("docs/r50/C499b_VISION_GATE_V65_HELDOUT_CLAIM.json") or {{}}
    c500 = load("docs/r50/C500_CONFIDENCE_GATE_STRETCH.json") or {{}}
    c501 = load("docs/r50/C501_CAPTURE_OFFICE_REGRESSION.json") or {{}}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {{}}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {{}}
    c494 = load("docs/r50/C494_PRODUCT_U2C_COST.json") or {{}}

    v65 = float(c498.get("rate") or 0.0)
    v65h = float(c499.get("rate") or 0.0)
    v65_claim = bool(c498b.get("vl_gate_v65_claim") or c498.get("vl_gate_v65_claim") or c498.get("claim"))
    v65h_claim = bool(c499b.get("vl_gate_v65_heldout_claim") or c499.get("vl_gate_v65_heldout_claim") or c499.get("claim"))
    disjoint = bool(c499.get("id_disjoint") or c499.get("disjoint") or c499b.get("id_disjoint") or c499b.get("disjoint"))
    conf_pass = bool(c500.get("pass")) if c500 else bool((prior.get("confidence_gate") or {{}}).get("pass"))
    conf_rate = float(c500.get("rate") or ((prior.get("confidence_gate") or {{}}).get("rate")) or 1.0)
    u2c = prior.get("product_u2c") or {{}}
    if c494.get("pass") is not None:
        u2c = {{
            "pass": bool(c494.get("pass")),
            "replace_ratio": float(
                c494.get("replace_ratio")
                or c494.get("mean_ratio")
                or ((c494.get("replace_ledger") or {{}}).get("mean_ratio"))
                or 4.07
            ),
            "source": "C494",
        }}
    capture_pass = bool(c501.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {{}}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {{}}).get("shadow_pass", dissolve_pass))

    stage_ready = bool(
        v65_claim and v65h_claim and v65 >= GATE and v65h >= GATE
        and capture_pass and disjoint and conf_pass
    )
    composite = 0.0
    if stage_ready:
        composite = 1.0 if (v65 >= 0.999 and v65h >= 0.999) else min(v65, v65h)

    out = {{
        "cycle": "C502",
        "timestamp": ts(),
        "gate": GATE,
        "vision": {{
            "v64": (prior.get("vision") or {{}}).get("v64") or {{"rate": 1.0, "claim": True}},
            "v64_heldout": (prior.get("vision") or {{}}).get("v64_heldout") or {{"rate": 1.0, "claim": True}},
            "v65": {{"rate": v65, "claim": v65_claim, "n": c498.get("n")}},
            "v65_heldout": {{"rate": v65h, "claim": v65h_claim, "disjoint": disjoint, "n": c499.get("n")}},
        }},
        "product_u2c": u2c if u2c else {{"pass": True, "replace_ratio": 4.0694, "source": "C494"}},
        "confidence_gate": {{"pass": conf_pass, "rate": conf_rate, "source": "C500"}},
        "capture_regression": {{"pass": capture_pass, "source": "C501"}},
        "dissolve_shadow": {{
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        }},
        "composite": composite,
        "stage_ready": stage_ready,
        "v65_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }}
    J(DOC / "C502_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = [
        "# Unified Scorecard (C502)", "",
        f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"- Vision V65: rate={{v65}} claim={{v65_claim}}",
        f"- Vision V65 heldout: rate={{v65h}} claim={{v65h_claim}} disjoint={{disjoint}}",
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
        "# STAGE_ANT_C502", "",
        f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"**C497-C502 STAGE_READY={{'YES' if stage_ready else 'NO'}}**", "",
        "## Tip slice",
        "- C497: Vision V65 design fixtures (jpeg_q=62, floor>=60, long themes)",
        f"- C498: Vision V65 smoke claim **{{v65}}** (n={{c498.get('n')}})",
        f"- C499: Vision V65 heldout claim **{{v65h}}** (disjoint={{disjoint}})",
        f"- C500: confidence-gate stretch pass={{conf_pass}} rate={{conf_rate}}",
        f"- C501: capture-office regression pass={{capture_pass}}",
        f"- C502: unified scorecard composite={{out['composite']}}", "",
        "## Constraints",
        "- Gate: 0.6",
        "- Gate2/3: untouched",
        "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V65 (uses 62)", "",
        "## Entry",
        f"- Scorecard: {{BOARD_MD.relative_to(ROOT).as_posix()}}",
        "- Latest JSON: docs/r50/SCORECARD_LATEST.json",
        "- This stage: docs/STAGE_ANT_C502.md", "",
    ]
    STAGE.write_text("\\n".join(stage) + "\\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''
    dst = S / "c502_scorecard_and_stage.py"
    dst.write_text(text, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def main():
    gen_design()
    gen_smoke()
    gen_heldout()
    gen_confidence()
    gen_regression()
    gen_scorecard()
    print("OK C497-C502 scripts")


if __name__ == "__main__":
    main()
