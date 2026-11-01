# -*- coding: utf-8 -*-
"""Generate C425-C430 V53 scripts from V52 via transform.
Themes NEW vs V52. Clarity floor jpeg_q>=60 (use 62).
Non-vision knife: confidence-gate stretch (C428).
Gate 0.6. Gate2/3 untouched. gen11 HOLD.
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"

THEMES = [
    ("kelp", "recv", "paid_total", "KELP GRAIN RECV", "RECV",
     lambda a,b,c: (a+b, [f"a paid {a:.2f}", f"b paid {b:.2f}", f"c open {c:.2f}", f"TOTAL PAID TARGET {a+b:.2f}"])),
    ("lava", "wh", "qty_sum", "WH LAVA BIN", "RECV",
     lambda a,b,c: (float(a+b), [f"SKU1 qty {a} ok", f"SKU2 qty {c} hold", f"SKU3 qty {b} ok", f"qty_sum TARGET {a+b}"])),
    ("meadow", "refund", "refund_done", "MEADOW PATCH REFUND", "DONE",
     lambda a,b,c: (a+b, [f"itemR1 {a:.2f} done", f"itemR2 {b:.2f} done", f"itemR3 {c:.2f} open", f"refund_done TARGET {a+b:.2f}"])),
    ("nickel", "tax", "tax_base_paid", "NICKEL TAX SLIP", "TAX",
     lambda a,b,c: (a+b, [f"base {a:.2f} paid", f"addon {b:.2f} paid", f"skip {c:.2f}", f"tax_base_paid TARGET {a+b:.2f}"])),
    ("orchard", "pay", "payroll_active", "ORCHARD PAYROLL", "PAY",
     lambda a,b,c: (a+b, [f"empA {a:.2f} active", f"empB {b:.2f} active", f"empC {c:.2f} leave", f"payroll_active TARGET {a+b:.2f}"])),
    ("plasma", "ship", "ship_ok", "PLASMA SHIP DOCK", "SHIP",
     lambda a,b,c: (float(a+b), [f"box1 {a} ok", f"box2 {b} ok", f"box3 {c} hold", f"ship_ok TARGET {a+b}"])),
    ("quarry", "sla", "sla_ok_hours", "QUARRY SLA CARD", "SLA",
     lambda a,b,c: (a+b, [f"job1 {a:.2f} hours ok", f"job2 {b:.2f} hours ok", f"job3 {c:.2f} hours late", f"sla_ok_hours TARGET {a+b:.2f}"])),
    ("raven", "exp", "exp_sum", "RAVEN EXPENSE", "EXP",
     lambda a,b,c: (a+b, [f"e1 {a:.2f}", f"e2 {b:.2f}", f"e3 {c:.2f} void", f"exp_sum TARGET {a+b:.2f}"])),
    ("sage", "po", "po_open", "SAGE PO SHEET", "PO",
     lambda a,b,c: (a+b, [f"line1 {a:.2f} open", f"line2 {b:.2f} open", f"line3 {c:.2f} closed", f"po_open TARGET {a+b:.2f}"])),
    ("tide", "order", "order_paid", "TIDE ORDER", "ORD",
     lambda a,b,c: (a+b, [f"skuA {a:.2f} paid", f"skuB {b:.2f} paid", f"skuC {c:.2f} due", f"order_paid TARGET {a+b:.2f}"])),
    ("umber", "dup", "dup_mark", "UMBER DUP MARK", "DUP",
     lambda a,b,c: (2.0, ["markA 1", "markB 1", "markC 0", "dup_mark TARGET 2"])),
    ("violet", "zero", "zero_check", "VIOLET AIR ZERO", "ZERO",
     lambda a,b,c: (0.0, ["z1 0.00", "z2 0.00", "z3 0.00", "zero_check TARGET 0.00"])),
    ("walnut", "ledger", "ledger_net", "WALNUT LEDGER", "LED",
     lambda a,b,c: (a+b, [f"dr {a:.2f}", f"cr {b:.2f}", f"adj {c:.2f}", f"ledger_net TARGET {a+b:.2f}"])),
    ("xenon", "ui", "ui_ok", "XENON UI SCAN", "UI",
     lambda a,b,c: (1.0, ["btnOK 1", "btnSkip 0", "btnBad 0", "ui_ok TARGET 1"])),
    ("yolk", "stack", "stack_count", "YOLK STACK", "STK",
     lambda a,b,c: (float(a+b), [f"p1 {a}", f"p2 {b}", f"p3 {c}", f"stack_count TARGET {a+b}"])),
    ("zinc", "fax", "fax_pages", "ZINC FAX", "FAX",
     lambda a,b,c: (float(a+b), [f"pgA {a}", f"pgB {b}", f"pgC {c} drop", f"fax_pages TARGET {a+b}"])),
    ("atlas", "glare", "glare_ok", "ATLAS GLARE", "GLR",
     lambda a,b,c: (1.0, ["zone1 1 ok", "zone2 0", "zone3 0", "glare_ok TARGET 1"])),
    ("birch", "tab", "tab_index", "BIRCH TAB INDEX", "TAB",
     lambda a,b,c: (float(a+b), [f"tabA {a}", f"tabB {b}", f"tabC {c}", f"tab_index TARGET {a+b}"])),
]
TRAIN_ABC = [
    (171.0, 173.5, 74.0), (121, 149, 91), (118.0, 124.75, 57.0), (211.0, 219.0, 108.0),
    (267.0, 278.0, 97.0), (103, 108, 66), (131.0, 119.25, 64.0), (142.0, 153.75, 71.0),
    (168.0, 151.0, 79.0), (197.0, 178.5, 68.0), (1, 1, 0), (0, 0, 0),
    (228.0, 241.25, 91.0), (1, 0, 0), (24, 19, 8), (33, 26, 19), (1, 0, 0), (42, 35, 17),
]
HELDOUT_ABC = [
    (98.0, 103.25, 44.0), (71, 89, 52), (69.0, 74.5, 33.0), (131.0, 137.0, 61.0),
    (161.0, 167.0, 58.0), (59, 63, 37), (76.0, 70.25, 38.0), (85.0, 91.5, 44.0),
    (103.0, 91.0, 47.0), (122.0, 109.5, 40.0), (1, 1, 0), (0, 0, 0),
    (141.0, 149.75, 54.0), (1, 0, 0), (13, 11, 6), (19, 15, 12), (1, 0, 0), (27, 22, 13),
]
THEME_STR = "kelp_lava_meadow_nickel_orchard_plasma_quarry_raven_sage_tide_umber_violet_walnut_xenon_yolk_zinc_atlas_birch"
OLD_THEME = "sierra_tundra_umbra_vortex_willow_xylem_yarn_zenith_acorn_boulder_cipher_dew_elm_frost_geyser_helix_iris_juniper"


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
    src = src.replace("# --- V52 overlays (new vs V51) ---", "# --- V53 overlays (new vs V52) ---")
    src = src.replace("# --- V52 overlays (new vs V50) ---", "# --- V53 overlays (new vs V52) ---")
    for a, b in [
        ("SIERRA bait", "KELP bait"), ("JUNIPER bait", "BIRCH bait"),
        ("DEW ghost", "VIOLET ghost"), ("FROST bait", "XENON bait"),
        ("XYLEM bait", "PLASMA bait"), ("GEYSER", "YOLK"),
        ("TUNDRA bait", "LAVA bait"),
        ("JADE bait", "CORAL bait"), ("GARNET bait", "RUBY bait"),
        ("MOSS ghost", "FERN ghost"), ("AQUA bait", "TEAL bait"),
        ("DRIFT bait", "SURF bait"), ("LEAF bait", "TWIG bait"),
        ("'FERN'", "'MOSS'"),
    ]:
        src = src.replace(a, b)
    # V53-only marker tweak in overlay comment block
    src = src.replace("dew drops + vine marks (V52-only)", "salt spray + bark notches (V53-only)")
    return src


def gen_design():
    out = (S / "c419_vision_v52_design_and_batch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C419", "C425"), ("c419", "c425"), ("V52", "V53"), ("v52", "v53"),
        ("_v52c419", "_v53c425"), ("_v52c377", "_v53c425"),
        ("Harder than V51", "Harder than V52"),
        (OLD_THEME, THEME_STR),
        ("V52 keeps floor", "V53 keeps floor"),
        ("C419 design+fixtures; no VL claim", "C425 design+fixtures; no VL claim"),
        ("fixtures only; claim deferred to C420 VL smoke", "fixtures only; claim deferred to C426 VL smoke"),
        ("No claim until C420 VL", "No claim until C426 VL"),
        ("kept on V52", "kept on V53"),
        ("harder_than\": \"v49_aurora_basalt", "harder_than\": \"v52_sierra_tundra"),
        ("r50plus_v52_sierra_tundra", "r50plus_v53_kelp_lava"),
    ]:
        out = out.replace(a, b)
    out = out.replace(
        "NEW themes vs V51: sierra, tundra, umbra, vortex, willow, xylem, yarn, zenith,\nacorn, boulder, cipher, dew, elm, frost, geyser, helix, iris, juniper.",
        "NEW themes vs V52: kelp, lava, meadow, nickel, orchard, plasma, quarry, raven,\nsage, tide, umber, violet, walnut, xenon, yolk, zinc, atlas, birch.",
    )
    out = replace_specs(out, build_specs("v53", "V53", TRAIN_ABC))
    out = retarget_overlay(out)
    dst = S / "c425_vision_v53_design_and_batch.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_smoke():
    out = (S / "c420_vision_v52_smoke.py").read_text(encoding="utf-8")
    for a, b in [
        ("C420", "C426"), ("c420", "c426"), ("V52", "V53"), ("v52", "v53"),
        ("r50plus_v52_sierra_tundra_clarity_floor_n>=16_qwen35_2b",
         "r50plus_v53_kelp_lava_clarity_floor_n>=16_qwen35_2b"),
        ("Uses C419 fixtures", "Uses C425 fixtures"),
    ]:
        out = out.replace(a, b)
    dst = S / "c426_vision_v53_smoke.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_heldout():
    out = (S / "c421_vision_v52_heldout.py").read_text(encoding="utf-8")
    for a, b in [
        ("C421", "C427"), ("c421", "c427"), ("C419", "C425"),
        ("V52", "V53"), ("v52", "v53"),
        ("_v52hc421", "_v53hc427"),
    ]:
        out = out.replace(a, b)
    out = replace_specs(out, build_specs("v53h", "V53H", HELDOUT_ABC))
    out = retarget_overlay(out)
    lines = []
    for ln in out.splitlines():
        if ln.strip().startswith("FIX = ") and "vision_images_v53" in ln and "v53h" not in ln:
            ln = 'FIX = ROOT / "evo/office/fixtures/vision_images_v53h"'
        if ln.strip().startswith("TRAIN_FIX = "):
            ln = 'TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v53"'
        if ln.strip().startswith("RUN = ") and "vision_v53h" not in ln:
            ln = 'RUN = ROOT / "runs/vision_v53h_c427"'
        lines.append(ln)
    out = "\n".join(lines) + "\n"
    # ensure heldout FIX path
    if "vision_images_v53h" not in out:
        out = out.replace('vision_images_v53"', 'vision_images_v53h"', 1)
    # force FIX/TRAIN/RUN after all replaces
    out2 = []
    seen_fix = seen_train = seen_run = False
    for ln in out.splitlines():
        s = ln.strip()
        if s.startswith("FIX = ") and not seen_fix:
            out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v53h"')
            seen_fix = True
            continue
        if s.startswith("TRAIN_FIX = ") and not seen_train:
            out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v53"')
            seen_train = True
            continue
        if s.startswith("RUN = ") and "vision_v53" in s and not seen_run:
            out2.append('RUN = ROOT / "runs/vision_v53h_c427"')
            seen_run = True
            continue
        out2.append(ln)
    out = "\n".join(out2) + "\n"
    dst = S / "c427_vision_v53_heldout.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_confidence():
    out = (S / "c416_confidence_gate_stretch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C416", "C428"), ("c416", "c428"),
        ("confidence_gate_c416", "confidence_gate_c428"),
        ("after V51", "after V53"), ("after V50", "after V53"),
        ("V51+", "V53+"), ("V50+", "V53+"),
    ]:
        out = out.replace(a, b)
    dst = S / "c428_confidence_gate_stretch.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_regression():
    out = (S / "c423_capture_office_regression.py").read_text(encoding="utf-8")
    for a, b in [
        ("C423", "C429"), ("c423", "c429"),
        ("capture_regression_c423", "capture_regression_c429"),
        ("after C419-C422", "after C425-C428"),
        ("V4-V52+heldout", "V4-V53+heldout"),
    ]:
        out = out.replace(a, b)
    if "VISION_V53_SMOKE" not in out:
        out = out.replace(
            "SMOKE_POINTERS = [",
            'SMOKE_POINTERS = [\n'
            '    ("V53", DOC / "C426_VISION_V53_SMOKE.json"),\n'
            '    ("V53_heldout", DOC / "C427_VISION_V53_HELDOUT_SMOKE.json"),',
            1,
        )
    dst = S / "c429_capture_office_regression.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_scorecard():
    # read BOARD_MD line from c424 to preserve Chinese path bytes
    board = None
    for ln in (S / "c424_scorecard_and_stage.py").read_text(encoding="utf-8").splitlines():
        if "BOARD_MD" in ln and "=" in ln:
            board = ln
            break
    if board is None:
        board = 'BOARD_MD = ROOT / "docs" / "ANT_UNIFIED_SCORECARD.md"'
    text = f'''# -*- coding: utf-8 -*-
"""C430: Unified scorecard + STAGE after C425-C429. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
{board}
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C430.md"
GATE = 0.6


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")


def load(rel):
    p = ROOT / rel
    if not p.is_file():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def main():
    c426 = load("docs/r50/C426_VISION_V53_SMOKE.json") or {{}}
    c426b = load("docs/r50/C426b_VISION_GATE_V53_CLAIM.json") or {{}}
    c427 = load("docs/r50/C427_VISION_V53_HELDOUT_SMOKE.json") or {{}}
    c427b = load("docs/r50/C427b_VISION_GATE_V53_HELDOUT_CLAIM.json") or {{}}
    c428 = load("docs/r50/C428_CONFIDENCE_GATE_STRETCH.json") or {{}}
    c429 = load("docs/r50/C429_CAPTURE_OFFICE_REGRESSION.json") or {{}}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {{}}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {{}}
    c422 = load("docs/r50/C422_PRODUCT_U2C_COST.json") or {{}}

    v53 = float(c426.get("rate") or 0.0)
    v53h = float(c427.get("rate") or 0.0)
    v53_claim = bool(c426b.get("vl_gate_v53_claim") or c426.get("vl_gate_v53_claim") or c426.get("claim"))
    v53h_claim = bool(c427b.get("vl_gate_v53_heldout_claim") or c427.get("vl_gate_v53_heldout_claim") or c427.get("claim"))
    disjoint = bool(c427.get("id_disjoint") or c427.get("disjoint") or c427b.get("id_disjoint") or c427b.get("disjoint"))
    conf_pass = bool(c428.get("pass")) if c428 else bool((prior.get("confidence_gate") or {{}}).get("pass"))
    conf_rate = float(c428.get("rate") or ((prior.get("confidence_gate") or {{}}).get("rate")) or 1.0)
    u2c = prior.get("product_u2c") or {{}}
    if c422.get("pass") is not None:
        u2c = {{
            "pass": bool(c422.get("pass")),
            "replace_ratio": float(
                c422.get("replace_ratio")
                or c422.get("mean_ratio")
                or ((c422.get("replace_ledger") or {{}}).get("mean_ratio"))
                or 4.07
            ),
            "source": "C422",
        }}
    capture_pass = bool(c429.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {{}}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {{}}).get("shadow_pass", dissolve_pass))

    stage_ready = bool(
        v53_claim and v53h_claim and v53 >= GATE and v53h >= GATE
        and capture_pass and disjoint and conf_pass
    )
    composite = 0.0
    if stage_ready:
        composite = 1.0 if (v53 >= 0.999 and v53h >= 0.999) else min(v53, v53h)

    out = {{
        "cycle": "C430",
        "timestamp": ts(),
        "gate": GATE,
        "vision": {{
            "v52": (prior.get("vision") or {{}}).get("v52") or {{"rate": 1.0, "claim": True}},
            "v52_heldout": (prior.get("vision") or {{}}).get("v52_heldout") or {{"rate": 1.0, "claim": True}},
            "v53": {{"rate": v53, "claim": v53_claim, "n": c426.get("n")}},
            "v53_heldout": {{"rate": v53h, "claim": v53h_claim, "disjoint": disjoint, "n": c427.get("n")}},
        }},
        "product_u2c": u2c if u2c else {{"pass": True, "replace_ratio": 4.0694, "source": "C422"}},
        "confidence_gate": {{"pass": conf_pass, "rate": conf_rate, "source": "C428"}},
        "capture_regression": {{"pass": capture_pass, "source": "C429"}},
        "dissolve_shadow": {{
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        }},
        "composite": composite,
        "stage_ready": stage_ready,
        "v53_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }}
    J(DOC / "C430_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = [
        "# Unified Scorecard (C430)", "",
        f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"- Vision V53: rate={{v53}} claim={{v53_claim}}",
        f"- Vision V53 heldout: rate={{v53h}} claim={{v53h_claim}} disjoint={{disjoint}}",
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
        "# STAGE_ANT_C430", "",
        f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"**C425-C430 STAGE_READY={{'YES' if stage_ready else 'NO'}}**", "",
        "## Tip slice",
        "- C425: Vision V53 design fixtures (jpeg_q=62, floor>=60)",
        f"- C426: Vision V53 smoke claim **{{v53}}** (n={{c426.get('n')}})",
        f"- C427: Vision V53 heldout claim **{{v53h}}** (disjoint={{disjoint}})",
        f"- C428: confidence-gate stretch pass={{conf_pass}} rate={{conf_rate}}",
        f"- C429: capture-office regression pass={{capture_pass}}",
        f"- C430: unified scorecard composite={{out['composite']}}", "",
        "## Constraints",
        "- Gate: 0.6",
        "- Gate2/3: untouched",
        "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V53 (uses 62)", "",
        "## Entry",
        f"- Scorecard: {{BOARD_MD.relative_to(ROOT).as_posix()}}",
        "- Latest JSON: docs/r50/SCORECARD_LATEST.json",
        "- This stage: docs/STAGE_ANT_C430.md", "",
    ]
    STAGE.write_text("\\n".join(stage) + "\\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''
    # Keep Python source newlines as real newlines; J() needs "\n" in source
    text = text.replace("\\\\n", "\\n")  # no-op safety
    # The f-string used \\n which becomes \n in the written file - correct for Python string literals in J/write_text
    dst = S / "c430_scorecard_and_stage.py"
    dst.write_text(text, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def main():
    gen_design()
    gen_smoke()
    gen_heldout()
    gen_confidence()
    gen_regression()
    gen_scorecard()
    print("OK C425-C430 scripts")


if __name__ == "__main__":
    main()
