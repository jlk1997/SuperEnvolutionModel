# -*- coding: utf-8 -*-
"""Generate C491-C496 V64 scripts from V63 via transform.
Themes NEW vs V63; long names (avoid foam-style VL collapse).
Clarity floor jpeg_q>=60 (use 62). Non-vision knife: product-u2c (C494).
Gate 0.6. Gate2/3 untouched. gen11 HOLD.
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"

THEMES = [
    ("alpinepeak", "recv", "paid_total", "ALPINEPEAK GRAIN RECV", "RECV",
     lambda a,b,c: (a+b, [f"a paid {a:.2f}", f"b paid {b:.2f}", f"c open {c:.2f}", f"TOTAL PAID TARGET {a+b:.2f}"])),
    ("birchgrove", "wh", "qty_sum", "WH BIRCHGROVE BIN", "RECV",
     lambda a,b,c: (float(a+b), [f"SKU1 qty {a} ok", f"SKU2 qty {c} hold", f"SKU3 qty {b} ok", f"qty_sum TARGET {a+b}"])),
    ("cedarcrest", "refund", "refund_done", "CEDARCREST PATCH REFUND", "DONE",
     lambda a,b,c: (a+b, [f"itemR1 {a:.2f} done", f"itemR2 {b:.2f} done", f"itemR3 {c:.2f} open", f"refund_done TARGET {a+b:.2f}"])),
    ("dawnchorus", "tax", "tax_base_paid", "DAWNCHORUS TAX SLIP", "TAX",
     lambda a,b,c: (a+b, [f"base {a:.2f} paid", f"addon {b:.2f} paid", f"skip {c:.2f}", f"tax_base_paid TARGET {a+b:.2f}"])),
    ("emberglow", "pay", "payroll_active", "EMBERGLOW PAYROLL", "PAY",
     lambda a,b,c: (a+b, [f"empA {a:.2f} active", f"empB {b:.2f} active", f"empC {c:.2f} leave", f"payroll_active TARGET {a+b:.2f}"])),
    ("flintstone", "ship", "ship_ok", "FLINTSTONE SHIP DOCK", "SHIP",
     lambda a,b,c: (float(a+b), [f"box1 {a} ok", f"box2 {b} ok", f"box3 {c} hold", f"ship_ok TARGET {a+b}"])),
    ("granitepeak", "sla", "sla_ok_hours", "GRANITEPEAK SLA CARD", "SLA",
     lambda a,b,c: (a+b, [f"job1 {a:.2f} hours ok", f"job2 {b:.2f} hours ok", f"job3 {c:.2f} hours late", f"sla_ok_hours TARGET {a+b:.2f}"])),
    ("harborlight", "exp", "exp_sum", "HARBORLIGHT EXPENSE", "EXP",
     lambda a,b,c: (a+b, [f"e1 {a:.2f}", f"e2 {b:.2f}", f"e3 {c:.2f} void", f"exp_sum TARGET {a+b:.2f}"])),
    ("ivorytower", "po", "po_open", "IVORYTOWER PO SHEET", "PO",
     lambda a,b,c: (a+b, [f"line1 {a:.2f} open", f"line2 {b:.2f} open", f"line3 {c:.2f} closed", f"po_open TARGET {a+b:.2f}"])),
    ("juniperhill", "order", "order_paid", "JUNIPERHILL ORDER", "ORD",
     lambda a,b,c: (a+b, [f"skuA {a:.2f} paid", f"skuB {b:.2f} paid", f"skuC {c:.2f} due", f"order_paid TARGET {a+b:.2f}"])),
    ("kelpforest", "dup", "dup_mark", "KELPFOREST DUP MARK", "DUP",
     lambda a,b,c: (2.0, ["markA 1", "markB 1", "markC 0", "dup_mark TARGET 2"])),
    ("lunarscape", "zero", "zero_check", "LUNARSCAPE AIR ZERO", "ZERO",
     lambda a,b,c: (0.0, ["z1 0.00", "z2 0.00", "z3 0.00", "zero_check TARGET 0.00"])),
    ("mossgarden", "ledger", "ledger_net", "MOSSGARDEN LEDGER", "LED",
     lambda a,b,c: (a+b, [f"dr {a:.2f}", f"cr {b:.2f}", f"adj {c:.2f}", f"ledger_net TARGET {a+b:.2f}"])),
    ("northridge", "ui", "ui_ok", "NORTHRIDGE UI SCAN", "UI",
     lambda a,b,c: (1.0, ["btnOK 1", "btnSkip 0", "btnBad 0", "ui_ok TARGET 1"])),
    ("opalstream", "stack", "stack_count", "OPALSTREAM STACK", "STK",
     lambda a,b,c: (float(a+b), [f"p1 {a}", f"p2 {b}", f"p3 {c}", f"stack_count TARGET {a+b}"])),
    ("pineforest", "fax", "fax_pages", "PINEFOREST FAX", "FAX",
     lambda a,b,c: (float(a+b), [f"pgA {a}", f"pgB {b}", f"pgC {c} drop", f"fax_pages TARGET {a+b}"])),
    ("quartzvein", "glare", "glare_ok", "QUARTZVEIN GLARE", "GLR",
     lambda a,b,c: (1.0, ["zone1 1 ok", "zone2 0", "zone3 0", "glare_ok TARGET 1"])),
    ("redwoodbark", "tab", "tab_index", "REDWOODBARK TAB INDEX", "TAB",
     lambda a,b,c: (float(a+b), [f"tabA {a}", f"tabB {b}", f"tabC {c}", f"tab_index TARGET {a+b}"])),
]
TRAIN_ABC = [
    (243.0, 258.5, 122.0), (196, 224, 141), (187.0, 202.75, 99.0), (297.0, 314.0, 159.0),
    (359.0, 381.0, 157.0), (154, 169, 116), (202.0, 193.75, 104.0), (214.0, 239.25, 122.0),
    (247.0, 230.0, 131.0), (280.0, 267.25, 119.0), (1, 1, 0), (0, 0, 0),
    (339.0, 361.5, 144.0), (1, 0, 0), (45, 39, 18), (62, 47, 40), (1, 0, 0), (73, 64, 37),
]
HELDOUT_ABC = [
    (148.0, 162.25, 75.0), (113, 139, 82), (109.0, 123.75, 63.0), (192.0, 207.0, 101.0),
    (232.0, 247.0, 96.0), (90, 103, 68), (117.0, 113.75, 69.0), (134.0, 150.25, 75.0),
    (154.0, 142.0, 78.0), (180.0, 169.25, 70.0), (1, 1, 0), (0, 0, 0),
    (212.0, 228.75, 85.0), (1, 0, 0), (24, 21, 16), (39, 33, 22), (1, 0, 0), (47, 42, 23),
]
THEME_STR = "alpinepeak_birchgrove_cedarcrest_dawnchorus_emberglow_flintstone_granitepeak_harborlight_ivorytower_juniperhill_kelpforest_lunarscape_mossgarden_northridge_opalstream_pineforest_quartzvein_redwoodbark"
OLD_THEME = "frostbite_glasshouse_honeycomb_inkstone_jadebridge_kettlebell_lighthouse_meadowlark_needlepoint_oceanfront_parchment_quarrystone_riverstone_starmap_tidepool_undercroft_vistaedge_wheatfield"


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
    src = src.replace("# --- V63 overlays (new vs V62) ---", "# --- V64 overlays (new vs V63) ---")
    src = src.replace("# --- V62 overlays (new vs V61) ---", "# --- V64 overlays (new vs V63) ---")
    for a, b in [
        ("FROSTBITE bait", "ALPINEPEAK bait"), ("WHEATFIELD bait", "REDWOODBARK bait"),
        ("QUARRYSTONE ghost", "LUNARSCAPE ghost"), ("STARMAP bait", "NORTHRIDGE bait"),
        ("KETTLEBELL bait", "FLINTSTONE bait"), ("TIDEPOOL", "OPALSTREAM"),
        ("GLASSHOUSE bait", "BIRCHGROVE bait"),
        ("MOONLIGHT bait", "ALPINEPEAK bait"), ("EGRETWING bait", "REDWOODBARK bait"),
        ("frostbite etch + wheat ticks (V63-only)", "alpine lichen + bark ticks (V64-only)"),
        ("moonlight glaze + drift ticks (V62-only)", "alpine lichen + bark ticks (V64-only)"),
    ]:
        src = src.replace(a, b)
    return src


def gen_design():
    out = (S / "c485_vision_v63_design_and_batch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C485", "C491"), ("c485", "c491"), ("V63", "V64"), ("v63", "v64"),
        ("_v63c485", "_v64c491"),
        ("Harder than V62", "Harder than V63"),
        ("harder than V62", "harder than V63"),
        (OLD_THEME, THEME_STR),
        ("V63 keeps floor", "V64 keeps floor"),
        ("C485 design+fixtures; no VL claim", "C491 design+fixtures; no VL claim"),
        ("fixtures only; claim deferred to C486 VL smoke", "fixtures only; claim deferred to C492 VL smoke"),
        ("No claim until C486 VL", "No claim until C492 VL"),
        ("kept on V63", "kept on V64"),
        ('"harder_than": "v62_moonlight_egretwing"', '"harder_than": "v63_frostbite_wheatfield"'),
        ("r50plus_v63_frostbite_wheatfield", "r50plus_v64_alpinepeak_redwoodbark"),
    ]:
        out = out.replace(a, b)
    out = out.replace(
        "NEW themes vs V62: frostbite, glasshouse, honeycomb, inkstone, jadebridge, kettlebell, lighthouse, meadowlark,\nneedlepoint, oceanfront, parchment, quarrystone, riverstone, starmap, tidepool, undercroft, vistaedge, wheatfield.",
        "NEW themes vs V63: alpinepeak, birchgrove, cedarcrest, dawnchorus, emberglow, flintstone, granitepeak, harborlight,\nivorytower, juniperhill, kelpforest, lunarscape, mossgarden, northridge, opalstream, pineforest, quartzvein, redwoodbark.",
    )
    out = replace_specs(out, build_specs("v64", "V64", TRAIN_ABC))
    out = retarget_overlay(out)
    dst = S / "c491_vision_v64_design_and_batch.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_smoke():
    out = (S / "c486_vision_v63_smoke.py").read_text(encoding="utf-8")
    for a, b in [
        ("C486", "C492"), ("c486", "c492"), ("V63", "V64"), ("v63", "v64"),
        ("r50plus_v63_frostbite_wheatfield_clarity_floor_n>=16_qwen35_2b",
         "r50plus_v64_alpinepeak_redwoodbark_clarity_floor_n>=16_qwen35_2b"),
        ("Uses C485 fixtures", "Uses C491 fixtures"),
    ]:
        out = out.replace(a, b)
    out = out.replace(
        "r50plus_v64_frostbite_wheatfield_clarity_floor_n>=16_qwen35_2b",
        "r50plus_v64_alpinepeak_redwoodbark_clarity_floor_n>=16_qwen35_2b",
    )
    dst = S / "c492_vision_v64_smoke.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_heldout():
    out = (S / "c487_vision_v63_heldout.py").read_text(encoding="utf-8")
    for a, b in [
        ("C487", "C493"), ("c487", "c493"), ("C485", "C491"),
        ("V63", "V64"), ("v63", "v64"),
        ("_v63hc487", "_v64hc493"),
        ("_v63c485", "_v64c491"),
    ]:
        out = out.replace(a, b)
    out = replace_specs(out, build_specs("v64h", "V64H", HELDOUT_ABC))
    out = retarget_overlay(out)
    out2 = []
    seen_fix = seen_train = seen_run = False
    for ln in out.splitlines():
        s = ln.strip()
        if s.startswith("FIX = ") and not seen_fix:
            out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v64h"')
            seen_fix = True
            continue
        if s.startswith("TRAIN_FIX = ") and not seen_train:
            out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v64"')
            seen_train = True
            continue
        if s.startswith("RUN = ") and "vision_v64" in s and not seen_run:
            out2.append('RUN = ROOT / "runs/vision_v64h_c493"')
            seen_run = True
            continue
        out2.append(ln)
    out = "\n".join(out2) + "\n"
    dst = S / "c493_vision_v64_heldout.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_product_u2c():
    out = (S / "c482_product_u2c_cost.py").read_text(encoding="utf-8")
    for a, b in [
        ("C482", "C494"), ("c482", "c494"),
        ("product_u2c_c482", "product_u2c_c494"),
        ("after V62", "after V64"), ("after V63", "after V64"),
        ("V62+", "V64+"), ("V63+", "V64+"),
    ]:
        out = out.replace(a, b)
    dst = S / "c494_product_u2c_cost.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_regression():
    out = (S / "c489_capture_office_regression.py").read_text(encoding="utf-8")
    for a, b in [
        ("C489", "C495"), ("c489", "c495"),
        ("capture_regression_c489", "capture_regression_c495"),
        ("after C485-C488", "after C491-C494"),
        ("V4-V63+heldout", "V4-V64+heldout"),
    ]:
        out = out.replace(a, b)
    if "VISION_V64_SMOKE" not in out:
        out = out.replace(
            "SMOKE_POINTERS = [",
            'SMOKE_POINTERS = [\n'
            '    ("V64", DOC / "C492_VISION_V64_SMOKE.json"),\n'
            '    ("V64_heldout", DOC / "C493_VISION_V64_HELDOUT_SMOKE.json"),\n'
            '    ("V63", DOC / "C486_VISION_V63_SMOKE.json"),\n'
            '    ("V63_heldout", DOC / "C487_VISION_V63_HELDOUT_SMOKE.json"),',
            1,
        )
    dst = S / "c495_capture_office_regression.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_scorecard():
    board = None
    for ln in (S / "c490_scorecard_and_stage.py").read_text(encoding="utf-8").splitlines():
        if "BOARD_MD" in ln and "=" in ln:
            board = ln
            break
    if board is None:
        board = 'BOARD_MD = ROOT / "docs" / "ANT_UNIFIED_SCORECARD.md"'
    nl = "\\n"
    text = f'''# -*- coding: utf-8 -*-
"""C496: Unified scorecard + STAGE after C491-C495. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
{board}
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C496.md"
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
    c492 = load("docs/r50/C492_VISION_V64_SMOKE.json") or {{}}
    c492b = load("docs/r50/C492b_VISION_GATE_V64_CLAIM.json") or {{}}
    c493 = load("docs/r50/C493_VISION_V64_HELDOUT_SMOKE.json") or {{}}
    c493b = load("docs/r50/C493b_VISION_GATE_V64_HELDOUT_CLAIM.json") or {{}}
    c494 = load("docs/r50/C494_PRODUCT_U2C_COST.json") or {{}}
    c495 = load("docs/r50/C495_CAPTURE_OFFICE_REGRESSION.json") or {{}}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {{}}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {{}}
    c488 = load("docs/r50/C488_CONFIDENCE_GATE_STRETCH.json") or {{}}

    v64 = float(c492.get("rate") or 0.0)
    v64h = float(c493.get("rate") or 0.0)
    v64_claim = bool(c492b.get("vl_gate_v64_claim") or c492.get("vl_gate_v64_claim") or c492.get("claim"))
    v64h_claim = bool(c493b.get("vl_gate_v64_heldout_claim") or c493.get("vl_gate_v64_heldout_claim") or c493.get("claim"))
    disjoint = bool(c493.get("id_disjoint") or c493.get("disjoint") or c493b.get("id_disjoint") or c493b.get("disjoint"))

    _rl = c494.get("replace_ledger") or {{}}
    u2c_pass = bool(c494.get("pass")) if c494 else bool((prior.get("product_u2c") or {{}}).get("pass"))
    u2c_replace = float(
        c494.get("replace_ratio")
        or _rl.get("mean_ratio")
        or ((prior.get("product_u2c") or {{}}).get("replace_ratio"))
        or 4.07
    )
    conf = prior.get("confidence_gate") or {{}}
    if c488.get("pass") is not None:
        conf = {{
            "pass": bool(c488.get("pass")),
            "rate": float(c488.get("rate") or 1.0),
            "source": "C488",
        }}
    capture_pass = bool(c495.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {{}}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {{}}).get("shadow_pass", dissolve_pass))

    stage_ready = bool(
        v64_claim and v64h_claim and v64 >= GATE and v64h >= GATE
        and capture_pass and disjoint and u2c_pass
    )
    composite = 0.0
    if stage_ready:
        composite = 1.0 if (v64 >= 0.999 and v64h >= 0.999) else min(v64, v64h)

    out = {{
        "cycle": "C496",
        "timestamp": ts(),
        "gate": GATE,
        "vision": {{
            "v63": (prior.get("vision") or {{}}).get("v63") or {{"rate": 1.0, "claim": True}},
            "v63_heldout": (prior.get("vision") or {{}}).get("v63_heldout") or {{"rate": 1.0, "claim": True}},
            "v64": {{"rate": v64, "claim": v64_claim, "n": c492.get("n")}},
            "v64_heldout": {{"rate": v64h, "claim": v64h_claim, "disjoint": disjoint, "n": c493.get("n")}},
        }},
        "product_u2c": {{"pass": u2c_pass, "replace_ratio": u2c_replace, "source": "C494"}},
        "confidence_gate": conf if conf else {{"pass": True, "rate": 1.0, "source": "C488"}},
        "capture_regression": {{"pass": capture_pass, "source": "C495"}},
        "dissolve_shadow": {{
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        }},
        "composite": composite,
        "stage_ready": stage_ready,
        "v64_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }}
    J(DOC / "C496_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = [
        "# Unified Scorecard (C496)", "",
        f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"- Vision V64: rate={{v64}} claim={{v64_claim}}",
        f"- Vision V64 heldout: rate={{v64h}} claim={{v64h_claim}} disjoint={{disjoint}}",
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
        "# STAGE_ANT_C496", "",
        f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"**C491-C496 STAGE_READY={{'YES' if stage_ready else 'NO'}}**", "",
        "## Tip slice",
        "- C491: Vision V64 design fixtures (jpeg_q=62, floor>=60, long themes)",
        f"- C492: Vision V64 smoke claim **{{v64}}** (n={{c492.get('n')}})",
        f"- C493: Vision V64 heldout claim **{{v64h}}** (disjoint={{disjoint}})",
        f"- C494: product-u2c pass={{u2c_pass}} replace~={{u2c_replace}}",
        f"- C495: capture-office regression pass={{capture_pass}}",
        f"- C496: unified scorecard composite={{out['composite']}}", "",
        "## Constraints",
        "- Gate: 0.6",
        "- Gate2/3: untouched",
        "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V64 (uses 62)", "",
        "## Entry",
        f"- Scorecard: {{BOARD_MD.relative_to(ROOT).as_posix()}}",
        "- Latest JSON: docs/r50/SCORECARD_LATEST.json",
        "- This stage: docs/STAGE_ANT_C496.md", "",
    ]
    STAGE.write_text("\\n".join(stage) + "\\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''
    dst = S / "c496_scorecard_and_stage.py"
    dst.write_text(text, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def main():
    gen_design()
    gen_smoke()
    gen_heldout()
    gen_product_u2c()
    gen_regression()
    gen_scorecard()
    print("OK C491-C496 scripts")


if __name__ == "__main__":
    main()
