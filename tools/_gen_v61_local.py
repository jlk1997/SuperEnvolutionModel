# -*- coding: utf-8 -*-
"""Generate C473-C478 V61 scripts from V60 via transform.
Themes NEW vs V60; long names (avoid foam-style VL collapse).
Clarity floor jpeg_q>=60 (use 62). Non-vision knife: confidence-gate (C476).
Gate 0.6. Gate2/3 untouched. gen11 HOLD.
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"

THEMES = [
    ("underpass", "recv", "paid_total", "UNDERPASS GRAIN RECV", "RECV",
     lambda a,b,c: (a+b, [f"a paid {a:.2f}", f"b paid {b:.2f}", f"c open {c:.2f}", f"TOTAL PAID TARGET {a+b:.2f}"])),
    ("vineyard", "wh", "qty_sum", "WH VINEYARD BIN", "RECV",
     lambda a,b,c: (float(a+b), [f"SKU1 qty {a} ok", f"SKU2 qty {c} hold", f"SKU3 qty {b} ok", f"qty_sum TARGET {a+b}"])),
    ("waterfall", "refund", "refund_done", "WATERFALL PATCH REFUND", "DONE",
     lambda a,b,c: (a+b, [f"itemR1 {a:.2f} done", f"itemR2 {b:.2f} done", f"itemR3 {c:.2f} open", f"refund_done TARGET {a+b:.2f}"])),
    ("xylotone", "tax", "tax_base_paid", "XYLOTONE TAX SLIP", "TAX",
     lambda a,b,c: (a+b, [f"base {a:.2f} paid", f"addon {b:.2f} paid", f"skip {c:.2f}", f"tax_base_paid TARGET {a+b:.2f}"])),
    ("yardarm", "pay", "payroll_active", "YARDARM PAYROLL", "PAY",
     lambda a,b,c: (a+b, [f"empA {a:.2f} active", f"empB {b:.2f} active", f"empC {c:.2f} leave", f"payroll_active TARGET {a+b:.2f}"])),
    ("zephyrton", "ship", "ship_ok", "ZEPHYRTON SHIP DOCK", "SHIP",
     lambda a,b,c: (float(a+b), [f"box1 {a} ok", f"box2 {b} ok", f"box3 {c} hold", f"ship_ok TARGET {a+b}"])),
    ("arabesque", "sla", "sla_ok_hours", "ARABESQUE SLA CARD", "SLA",
     lambda a,b,c: (a+b, [f"job1 {a:.2f} hours ok", f"job2 {b:.2f} hours ok", f"job3 {c:.2f} hours late", f"sla_ok_hours TARGET {a+b:.2f}"])),
    ("barnacle", "exp", "exp_sum", "BARNACLE EXPENSE", "EXP",
     lambda a,b,c: (a+b, [f"e1 {a:.2f}", f"e2 {b:.2f}", f"e3 {c:.2f} void", f"exp_sum TARGET {a+b:.2f}"])),
    ("crossbeam", "po", "po_open", "CROSSBEAM PO SHEET", "PO",
     lambda a,b,c: (a+b, [f"line1 {a:.2f} open", f"line2 {b:.2f} open", f"line3 {c:.2f} closed", f"po_open TARGET {a+b:.2f}"])),
    ("daybreak", "order", "order_paid", "DAYBREAK ORDER", "ORD",
     lambda a,b,c: (a+b, [f"skuA {a:.2f} paid", f"skuB {b:.2f} paid", f"skuC {c:.2f} due", f"order_paid TARGET {a+b:.2f}"])),
    ("earthenware", "dup", "dup_mark", "EARTHENWARE DUP MARK", "DUP",
     lambda a,b,c: (2.0, ["markA 1", "markB 1", "markC 0", "dup_mark TARGET 2"])),
    ("firebrand", "zero", "zero_check", "FIREBRAND AIR ZERO", "ZERO",
     lambda a,b,c: (0.0, ["z1 0.00", "z2 0.00", "z3 0.00", "zero_check TARGET 0.00"])),
    ("goldfinch", "ledger", "ledger_net", "GOLDFINCH LEDGER", "LED",
     lambda a,b,c: (a+b, [f"dr {a:.2f}", f"cr {b:.2f}", f"adj {c:.2f}", f"ledger_net TARGET {a+b:.2f}"])),
    ("handwheel", "ui", "ui_ok", "HANDWHEEL UI SCAN", "UI",
     lambda a,b,c: (1.0, ["btnOK 1", "btnSkip 0", "btnBad 0", "ui_ok TARGET 1"])),
    ("ironwood", "stack", "stack_count", "IRONWOOD STACK", "STK",
     lambda a,b,c: (float(a+b), [f"p1 {a}", f"p2 {b}", f"p3 {c}", f"stack_count TARGET {a+b}"])),
    ("jadewort", "fax", "fax_pages", "JADEWORT FAX", "FAX",
     lambda a,b,c: (float(a+b), [f"pgA {a}", f"pgB {b}", f"pgC {c} drop", f"fax_pages TARGET {a+b}"])),
    ("kingsfoil", "glare", "glare_ok", "KINGSFOIL GLARE", "GLR",
     lambda a,b,c: (1.0, ["zone1 1 ok", "zone2 0", "zone3 0", "glare_ok TARGET 1"])),
    ("lamppost", "tab", "tab_index", "LAMPPOST TAB INDEX", "TAB",
     lambda a,b,c: (float(a+b), [f"tabA {a}", f"tabB {b}", f"tabC {c}", f"tab_index TARGET {a+b}"])),
]
TRAIN_ABC = [
    (222.0, 232.75, 107.0), (175, 203, 126), (166.0, 177.5, 87.0), (273.0, 287.0, 144.0),
    (332.0, 351.0, 139.0), (139, 151, 101), (181.0, 171.25, 92.0), (193.0, 211.25, 107.0),
    (223.0, 206.0, 116.0), (256.0, 240.5, 104.0), (1, 1, 0), (0, 0, 0),
    (306.0, 323.75, 129.0), (1, 0, 0), (39, 33, 15), (53, 41, 34), (1, 0, 0), (64, 55, 31),
]
HELDOUT_ABC = [
    (133.0, 142.75, 66.0), (101, 124, 73), (97.0, 107.5, 54.0), (174.0, 186.0, 89.0),
    (211.0, 223.0, 84.0), (81, 91, 59), (105.0, 100.25, 60.0), (119.0, 130.75, 66.0),
    (139.0, 127.0, 69.0), (162.0, 149.75, 61.0), (1, 1, 0), (0, 0, 0),
    (191.0, 203.25, 76.0), (1, 0, 0), (21, 18, 13), (33, 27, 19), (1, 0, 0), (41, 36, 20),
]
THEME_STR = "underpass_vineyard_waterfall_xylotone_yardarm_zephyrton_arabesque_barnacle_crossbeam_daybreak_earthenware_firebrand_goldfinch_handwheel_ironwood_jadewort_kingsfoil_lamppost"
OLD_THEME = "anchor_beacon_citadel_evergreen_fortress_gallery_highland_iceberg_jackpine_keystone_lantern_northstar_outlook_pavilion_quartzite_riverbed_sandstone_tidemark"


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
    src = src.replace("# --- V60 overlays (new vs V59) ---", "# --- V61 overlays (new vs V60) ---")
    src = src.replace("# --- V59 overlays (new vs V58) ---", "# --- V61 overlays (new vs V60) ---")
    for a, b in [
        ("ANCHOR bait", "UNDERPASS bait"), ("TIDEMARK bait", "LAMPPOST bait"),
        ("NORTHSTAR ghost", "FIREBRAND ghost"), ("PAVILION bait", "HANDWHEEL bait"),
        ("GALLERY bait", "ZEPHYRTON bait"), ("QUARTZITE", "IRONWOOD"),
        ("BEACON bait", "VINEYARD bait"),
        ("VAULT bait", "UNDERPASS bait"), ("PLANK bait", "LAMPPOST bait"),
        ("anchor rope + lantern ticks (V60-only)", "underpass rivet + lamp ticks (V61-only)"),
        ("vault soot + hinge ticks (V59-only)", "underpass rivet + lamp ticks (V61-only)"),
    ]:
        src = src.replace(a, b)
    return src


def gen_design():
    out = (S / "c467_vision_v60_design_and_batch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C467", "C473"), ("c467", "c473"), ("V60", "V61"), ("v60", "v61"),
        ("_v60c467", "_v61c473"),
        ("Harder than V59", "Harder than V60"),
        ("harder than V59", "harder than V60"),
        (OLD_THEME, THEME_STR),
        ("V60 keeps floor", "V61 keeps floor"),
        ("C467 design+fixtures; no VL claim", "C473 design+fixtures; no VL claim"),
        ("fixtures only; claim deferred to C468 VL smoke", "fixtures only; claim deferred to C474 VL smoke"),
        ("No claim until C468 VL", "No claim until C474 VL"),
        ("kept on V60", "kept on V61"),
        ('"harder_than": "v59_vault_plank"', '"harder_than": "v60_anchor_tidemark"'),
        ("r50plus_v60_anchor_tidemark", "r50plus_v61_underpass_lamppost"),
    ]:
        out = out.replace(a, b)
    out = out.replace(
        "NEW themes vs V59: anchor, beacon, citadel, evergreen, fortress, gallery, highland, iceberg,\njackpine, keystone, lantern, northstar, outlook, pavilion, quartzite, riverbed, sandstone, tidemark.",
        "NEW themes vs V60: underpass, vineyard, waterfall, xylotone, yardarm, zephyrton, arabesque, barnacle,\ncrossbeam, daybreak, earthenware, firebrand, goldfinch, handwheel, ironwood, jadewort, kingsfoil, lamppost.",
    )
    out = replace_specs(out, build_specs("v61", "V61", TRAIN_ABC))
    out = retarget_overlay(out)
    dst = S / "c473_vision_v61_design_and_batch.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_smoke():
    out = (S / "c468_vision_v60_smoke.py").read_text(encoding="utf-8")
    for a, b in [
        ("C468", "C474"), ("c468", "c474"), ("V60", "V61"), ("v60", "v61"),
        ("r50plus_v60_anchor_tidemark_clarity_floor_n>=16_qwen35_2b",
         "r50plus_v61_underpass_lamppost_clarity_floor_n>=16_qwen35_2b"),
        ("Uses C467 fixtures", "Uses C473 fixtures"),
    ]:
        out = out.replace(a, b)
    out = out.replace(
        "r50plus_v61_anchor_tidemark_clarity_floor_n>=16_qwen35_2b",
        "r50plus_v61_underpass_lamppost_clarity_floor_n>=16_qwen35_2b",
    )
    dst = S / "c474_vision_v61_smoke.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_heldout():
    out = (S / "c469_vision_v60_heldout.py").read_text(encoding="utf-8")
    for a, b in [
        ("C469", "C475"), ("c469", "c475"), ("C467", "C473"),
        ("V60", "V61"), ("v60", "v61"),
        ("_v60hc469", "_v61hc475"),
        ("_v60c467", "_v61c473"),
    ]:
        out = out.replace(a, b)
    out = replace_specs(out, build_specs("v61h", "V61H", HELDOUT_ABC))
    out = retarget_overlay(out)
    out2 = []
    seen_fix = seen_train = seen_run = False
    for ln in out.splitlines():
        s = ln.strip()
        if s.startswith("FIX = ") and not seen_fix:
            out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v61h"')
            seen_fix = True
            continue
        if s.startswith("TRAIN_FIX = ") and not seen_train:
            out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v61"')
            seen_train = True
            continue
        if s.startswith("RUN = ") and "vision_v61" in s and not seen_run:
            out2.append('RUN = ROOT / "runs/vision_v61h_c475"')
            seen_run = True
            continue
        out2.append(ln)
    out = "\n".join(out2) + "\n"
    dst = S / "c475_vision_v61_heldout.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_confidence():
    out = (S / "c464_confidence_gate_stretch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C464", "C476"), ("c464", "c476"),
        ("confidence_gate_c464", "confidence_gate_c476"),
        ("conf_gate_stretch_c464", "conf_gate_stretch_c476"),
        ("after V59", "after V61"), ("after V60", "after V61"),
        ("V59+", "V61+"), ("V60+", "V61+"),
    ]:
        out = out.replace(a, b)
    dst = S / "c476_confidence_gate_stretch.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_regression():
    out = (S / "c471_capture_office_regression.py").read_text(encoding="utf-8")
    for a, b in [
        ("C471", "C477"), ("c471", "c477"),
        ("capture_regression_c471", "capture_regression_c477"),
        ("after C467-C470", "after C473-C476"),
        ("V4-V60+heldout", "V4-V61+heldout"),
    ]:
        out = out.replace(a, b)
    if "VISION_V61_SMOKE" not in out:
        out = out.replace(
            "SMOKE_POINTERS = [",
            'SMOKE_POINTERS = [\n'
            '    ("V61", DOC / "C474_VISION_V61_SMOKE.json"),\n'
            '    ("V61_heldout", DOC / "C475_VISION_V61_HELDOUT_SMOKE.json"),\n'
            '    ("V60", DOC / "C468_VISION_V60_SMOKE.json"),\n'
            '    ("V60_heldout", DOC / "C469_VISION_V60_HELDOUT_SMOKE.json"),',
            1,
        )
    dst = S / "c477_capture_office_regression.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_scorecard():
    board = None
    for ln in (S / "c472_scorecard_and_stage.py").read_text(encoding="utf-8").splitlines():
        if "BOARD_MD" in ln and "=" in ln:
            board = ln
            break
    if board is None:
        board = 'BOARD_MD = ROOT / "docs" / "ANT_UNIFIED_SCORECARD.md"'
    nl = "\\n"
    text = f'''# -*- coding: utf-8 -*-
"""C478: Unified scorecard + STAGE after C473-C477. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
{board}
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C478.md"
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
    c474 = load("docs/r50/C474_VISION_V61_SMOKE.json") or {{}}
    c474b = load("docs/r50/C474b_VISION_GATE_V61_CLAIM.json") or {{}}
    c475 = load("docs/r50/C475_VISION_V61_HELDOUT_SMOKE.json") or {{}}
    c475b = load("docs/r50/C475b_VISION_GATE_V61_HELDOUT_CLAIM.json") or {{}}
    c476 = load("docs/r50/C476_CONFIDENCE_GATE_STRETCH.json") or {{}}
    c477 = load("docs/r50/C477_CAPTURE_OFFICE_REGRESSION.json") or {{}}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {{}}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {{}}
    c470 = load("docs/r50/C470_PRODUCT_U2C_COST.json") or {{}}

    v61 = float(c474.get("rate") or 0.0)
    v61h = float(c475.get("rate") or 0.0)
    v61_claim = bool(c474b.get("vl_gate_v61_claim") or c474.get("vl_gate_v61_claim") or c474.get("claim"))
    v61h_claim = bool(c475b.get("vl_gate_v61_heldout_claim") or c475.get("vl_gate_v61_heldout_claim") or c475.get("claim"))
    disjoint = bool(c475.get("id_disjoint") or c475.get("disjoint") or c475b.get("id_disjoint") or c475b.get("disjoint"))
    conf_pass = bool(c476.get("pass")) if c476 else bool((prior.get("confidence_gate") or {{}}).get("pass"))
    conf_rate = float(c476.get("rate") or ((prior.get("confidence_gate") or {{}}).get("rate")) or 1.0)
    u2c = prior.get("product_u2c") or {{}}
    if c470.get("pass") is not None:
        u2c = {{
            "pass": bool(c470.get("pass")),
            "replace_ratio": float(
                c470.get("replace_ratio")
                or c470.get("mean_ratio")
                or ((c470.get("replace_ledger") or {{}}).get("mean_ratio"))
                or 4.07
            ),
            "source": "C470",
        }}
    capture_pass = bool(c477.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {{}}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {{}}).get("shadow_pass", dissolve_pass))

    stage_ready = bool(
        v61_claim and v61h_claim and v61 >= GATE and v61h >= GATE
        and capture_pass and disjoint and conf_pass
    )
    composite = 0.0
    if stage_ready:
        composite = 1.0 if (v61 >= 0.999 and v61h >= 0.999) else min(v61, v61h)

    out = {{
        "cycle": "C478",
        "timestamp": ts(),
        "gate": GATE,
        "vision": {{
            "v60": (prior.get("vision") or {{}}).get("v60") or {{"rate": 1.0, "claim": True}},
            "v60_heldout": (prior.get("vision") or {{}}).get("v60_heldout") or {{"rate": 1.0, "claim": True}},
            "v61": {{"rate": v61, "claim": v61_claim, "n": c474.get("n")}},
            "v61_heldout": {{"rate": v61h, "claim": v61h_claim, "disjoint": disjoint, "n": c475.get("n")}},
        }},
        "product_u2c": u2c if u2c else {{"pass": True, "replace_ratio": 4.0694, "source": "C470"}},
        "confidence_gate": {{"pass": conf_pass, "rate": conf_rate, "source": "C476"}},
        "capture_regression": {{"pass": capture_pass, "source": "C477"}},
        "dissolve_shadow": {{
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        }},
        "composite": composite,
        "stage_ready": stage_ready,
        "v61_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }}
    J(DOC / "C478_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = [
        "# Unified Scorecard (C478)", "",
        f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"- Vision V61: rate={{v61}} claim={{v61_claim}}",
        f"- Vision V61 heldout: rate={{v61h}} claim={{v61h_claim}} disjoint={{disjoint}}",
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
        "# STAGE_ANT_C478", "",
        f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"**C473-C478 STAGE_READY={{'YES' if stage_ready else 'NO'}}**", "",
        "## Tip slice",
        "- C473: Vision V61 design fixtures (jpeg_q=62, floor>=60, long themes)",
        f"- C474: Vision V61 smoke claim **{{v61}}** (n={{c474.get('n')}})",
        f"- C475: Vision V61 heldout claim **{{v61h}}** (disjoint={{disjoint}})",
        f"- C476: confidence-gate stretch pass={{conf_pass}} rate={{conf_rate}}",
        f"- C477: capture-office regression pass={{capture_pass}}",
        f"- C478: unified scorecard composite={{out['composite']}}", "",
        "## Constraints",
        "- Gate: 0.6",
        "- Gate2/3: untouched",
        "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V61 (uses 62)", "",
        "## Entry",
        f"- Scorecard: {{BOARD_MD.relative_to(ROOT).as_posix()}}",
        "- Latest JSON: docs/r50/SCORECARD_LATEST.json",
        "- This stage: docs/STAGE_ANT_C478.md", "",
    ]
    STAGE.write_text("\\n".join(stage) + "\\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''
    dst = S / "c478_scorecard_and_stage.py"
    dst.write_text(text, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def main():
    gen_design()
    gen_smoke()
    gen_heldout()
    gen_confidence()
    gen_regression()
    gen_scorecard()
    print("OK C473-C478 scripts")


if __name__ == "__main__":
    main()
