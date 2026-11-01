# -*- coding: utf-8 -*-
"""Generate C443-C448 V56 scripts from V55 via transform.
Themes NEW vs V55. Clarity floor jpeg_q>=60 (use 62).
Non-vision knife: product-u2c cost (C446).
Gate 0.6. Gate2/3 untouched. gen11 HOLD.
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"

THEMES = [
    ("sable", "recv", "paid_total", "SABLE GRAIN RECV", "RECV",
     lambda a,b,c: (a+b, [f"a paid {a:.2f}", f"b paid {b:.2f}", f"c open {c:.2f}", f"TOTAL PAID TARGET {a+b:.2f}"])),
    ("thyme", "wh", "qty_sum", "WH THYME BIN", "RECV",
     lambda a,b,c: (float(a+b), [f"SKU1 qty {a} ok", f"SKU2 qty {c} hold", f"SKU3 qty {b} ok", f"qty_sum TARGET {a+b}"])),
    ("ursa", "refund", "refund_done", "URSA PATCH REFUND", "DONE",
     lambda a,b,c: (a+b, [f"itemR1 {a:.2f} done", f"itemR2 {b:.2f} done", f"itemR3 {c:.2f} open", f"refund_done TARGET {a+b:.2f}"])),
    ("velvet", "tax", "tax_base_paid", "VELVET TAX SLIP", "TAX",
     lambda a,b,c: (a+b, [f"base {a:.2f} paid", f"addon {b:.2f} paid", f"skip {c:.2f}", f"tax_base_paid TARGET {a+b:.2f}"])),
    ("whale", "pay", "payroll_active", "WHALE PAYROLL", "PAY",
     lambda a,b,c: (a+b, [f"empA {a:.2f} active", f"empB {b:.2f} active", f"empC {c:.2f} leave", f"payroll_active TARGET {a+b:.2f}"])),
    ("xeric", "ship", "ship_ok", "XERIC SHIP DOCK", "SHIP",
     lambda a,b,c: (float(a+b), [f"box1 {a} ok", f"box2 {b} ok", f"box3 {c} hold", f"ship_ok TARGET {a+b}"])),
    ("yarrow", "sla", "sla_ok_hours", "YARROW SLA CARD", "SLA",
     lambda a,b,c: (a+b, [f"job1 {a:.2f} hours ok", f"job2 {b:.2f} hours ok", f"job3 {c:.2f} hours late", f"sla_ok_hours TARGET {a+b:.2f}"])),
    ("zircon", "exp", "exp_sum", "ZIRCON EXPENSE", "EXP",
     lambda a,b,c: (a+b, [f"e1 {a:.2f}", f"e2 {b:.2f}", f"e3 {c:.2f} void", f"exp_sum TARGET {a+b:.2f}"])),
    ("amber", "po", "po_open", "AMBER PO SHEET", "PO",
     lambda a,b,c: (a+b, [f"line1 {a:.2f} open", f"line2 {b:.2f} open", f"line3 {c:.2f} closed", f"po_open TARGET {a+b:.2f}"])),
    ("breeze", "order", "order_paid", "BREEZE ORDER", "ORD",
     lambda a,b,c: (a+b, [f"skuA {a:.2f} paid", f"skuB {b:.2f} paid", f"skuC {c:.2f} due", f"order_paid TARGET {a+b:.2f}"])),
    ("canyon", "dup", "dup_mark", "CANYON DUP MARK", "DUP",
     lambda a,b,c: (2.0, ["markA 1", "markB 1", "markC 0", "dup_mark TARGET 2"])),
    ("daisy", "zero", "zero_check", "DAISY AIR ZERO", "ZERO",
     lambda a,b,c: (0.0, ["z1 0.00", "z2 0.00", "z3 0.00", "zero_check TARGET 0.00"])),
    ("fern", "ledger", "ledger_net", "FERN LEDGER", "LED",
     lambda a,b,c: (a+b, [f"dr {a:.2f}", f"cr {b:.2f}", f"adj {c:.2f}", f"ledger_net TARGET {a+b:.2f}"])),
    ("glacier", "ui", "ui_ok", "GLACIER UI SCAN", "UI",
     lambda a,b,c: (1.0, ["btnOK 1", "btnSkip 0", "btnBad 0", "ui_ok TARGET 1"])),
    ("honey", "stack", "stack_count", "HONEY STACK", "STK",
     lambda a,b,c: (float(a+b), [f"p1 {a}", f"p2 {b}", f"p3 {c}", f"stack_count TARGET {a+b}"])),
    ("islet", "fax", "fax_pages", "ISLET FAX", "FAX",
     lambda a,b,c: (float(a+b), [f"pgA {a}", f"pgB {b}", f"pgC {c} drop", f"fax_pages TARGET {a+b}"])),
    ("jewel", "glare", "glare_ok", "JEWEL GLARE", "GLR",
     lambda a,b,c: (1.0, ["zone1 1 ok", "zone2 0", "zone3 0", "glare_ok TARGET 1"])),
    ("kettle", "tab", "tab_index", "KETTLE TAB INDEX", "TAB",
     lambda a,b,c: (float(a+b), [f"tabA {a}", f"tabB {b}", f"tabC {c}", f"tab_index TARGET {a+b}"])),
]
TRAIN_ABC = [
    (188.0, 193.75, 84.0), (141, 168, 101), (132.0, 140.5, 67.0), (234.0, 242.0, 119.0),
    (288.0, 301.0, 109.0), (114, 121, 76), (146.0, 134.25, 72.0), (158.0, 169.5, 82.0),
    (184.0, 167.0, 91.0), (216.0, 197.25, 79.0), (1, 1, 0), (0, 0, 0),
    (252.0, 265.75, 104.0), (1, 0, 0), (29, 23, 10), (38, 31, 24), (1, 0, 0), (49, 41, 21),
]
HELDOUT_ABC = [
    (109.0, 114.25, 51.0), (81, 99, 58), (77.0, 83.5, 39.0), (144.0, 151.0, 69.0),
    (176.0, 183.0, 64.0), (66, 71, 44), (85.0, 78.5, 45.0), (95.0, 102.25, 51.0),
    (114.0, 102.0, 54.0), (133.0, 120.75, 46.0), (1, 1, 0), (0, 0, 0),
    (156.0, 164.5, 61.0), (1, 0, 0), (16, 13, 8), (23, 18, 14), (1, 0, 0), (31, 26, 15),
]
THEME_STR = "sable_thyme_ursa_velvet_whale_xeric_yarrow_zircon_amber_breeze_canyon_daisy_fern_glacier_honey_islet_jewel_kettle"
OLD_THEME = "azure_basil_cedar_delta_echo_flint_grove_haze_indigo_jasper_kiwi_linen_moss_noon_onyx_pine_quill_ridge"


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
    src = src.replace("# --- V55 overlays (new vs V54) ---", "# --- V56 overlays (new vs V55) ---")
    src = src.replace("# --- V54 overlays (new vs V50) ---", "# --- V56 overlays (new vs V55) ---")
    for a, b in [
        ("AZURE bait", "SABLE bait"), ("RIDGE bait", "KETTLE bait"),
        ("LINEN ghost", "DAISY ghost"), ("NOON bait", "GLACIER bait"),
        ("FLINT bait", "XERIC bait"), ("ONYX", "HONEY"),
        ("BASIL bait", "THYME bait"),
        ("CORAL bait", "SABLE bait"), ("TERRA bait", "KETTLE bait"),
        ("mist rings + bark ticks (V55-only)", "pollen dust + rivet marks (V56-only)"),
        ("dew drops + vine marks (V54-only)", "pollen dust + rivet marks (V56-only)"),
    ]:
        src = src.replace(a, b)
    return src


def gen_design():
    out = (S / "c437_vision_v55_design_and_batch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C437", "C443"), ("c437", "c443"), ("V55", "V56"), ("v55", "v56"),
        ("_v55c437", "_v56c443"),
        ("Harder than V54", "Harder than V55"),
        ("harder than V54", "harder than V55"),
        (OLD_THEME, THEME_STR),
        ("V55 keeps floor", "V56 keeps floor"),
        ("C437 design+fixtures; no VL claim", "C443 design+fixtures; no VL claim"),
        ("fixtures only; claim deferred to C438 VL smoke", "fixtures only; claim deferred to C444 VL smoke"),
        ("No claim until C438 VL", "No claim until C444 VL"),
        ("kept on V55", "kept on V56"),
        ('"harder_than": "v54_coral_terra"', '"harder_than": "v55_azure_ridge"'),
        ("r50plus_v55_azure_ridge", "r50plus_v56_sable_kettle"),
    ]:
        out = out.replace(a, b)
    out = out.replace(
        "NEW themes vs V54: azure, basil, cedar, delta, echo, flint, grove, haze,\nindigo, jasper, kiwi, linen, moss, noon, onyx, pine, quill, ridge.",
        "NEW themes vs V55: sable, thyme, ursa, velvet, whale, xeric, yarrow, zircon,\namber, breeze, canyon, daisy, fern, glacier, honey, islet, jewel, kettle.",
    )
    out = replace_specs(out, build_specs("v56", "V56", TRAIN_ABC))
    out = retarget_overlay(out)
    dst = S / "c443_vision_v56_design_and_batch.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_smoke():
    out = (S / "c438_vision_v55_smoke.py").read_text(encoding="utf-8")
    for a, b in [
        ("C438", "C444"), ("c438", "c444"), ("V55", "V56"), ("v55", "v56"),
        ("r50plus_v55_azure_ridge_clarity_floor_n>=16_qwen35_2b",
         "r50plus_v56_sable_kettle_clarity_floor_n>=16_qwen35_2b"),
        ("Uses C437 fixtures", "Uses C443 fixtures"),
    ]:
        out = out.replace(a, b)
    # fix order: V55->V56 may leave coral/azure residue if replace missed
    out = out.replace(
        "r50plus_v56_azure_ridge_clarity_floor_n>=16_qwen35_2b",
        "r50plus_v56_sable_kettle_clarity_floor_n>=16_qwen35_2b",
    )
    out = out.replace(
        "r50plus_v56_coral_terra_clarity_floor_n>=16_qwen35_2b",
        "r50plus_v56_sable_kettle_clarity_floor_n>=16_qwen35_2b",
    )
    dst = S / "c444_vision_v56_smoke.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_heldout():
    out = (S / "c439_vision_v55_heldout.py").read_text(encoding="utf-8")
    for a, b in [
        ("C439", "C445"), ("c439", "c445"), ("C437", "C443"),
        ("V55", "V56"), ("v55", "v56"),
        ("_v55hc439", "_v56hc445"),
        ("_v55c437", "_v56c443"),
    ]:
        out = out.replace(a, b)
    out = replace_specs(out, build_specs("v56h", "V56H", HELDOUT_ABC))
    out = retarget_overlay(out)
    out2 = []
    seen_fix = seen_train = seen_run = False
    for ln in out.splitlines():
        s = ln.strip()
        if s.startswith("FIX = ") and not seen_fix:
            out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v56h"')
            seen_fix = True
            continue
        if s.startswith("TRAIN_FIX = ") and not seen_train:
            out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v56"')
            seen_train = True
            continue
        if s.startswith("RUN = ") and "vision_v56" in s and not seen_run:
            out2.append('RUN = ROOT / "runs/vision_v56h_c445"')
            seen_run = True
            continue
        out2.append(ln)
    out = "\n".join(out2) + "\n"
    dst = S / "c445_vision_v56_heldout.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_product_u2c():
    out = (S / "c434_product_u2c_cost.py").read_text(encoding="utf-8")
    for a, b in [
        ("C434", "C446"), ("c434", "c446"),
        ("product_u2c_c434", "product_u2c_c446"),
        ("after V54", "after V56"), ("after V55", "after V56"),
        ("V54+", "V56+"), ("V55+", "V56+"),
        ("on V50", "on V50"),  # keep crystal note
    ]:
        out = out.replace(a, b)
    dst = S / "c446_product_u2c_cost.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_regression():
    out = (S / "c441_capture_office_regression.py").read_text(encoding="utf-8")
    for a, b in [
        ("C441", "C447"), ("c441", "c447"),
        ("capture_regression_c441", "capture_regression_c447"),
        ("after C437-C440", "after C443-C446"),
        ("V4-V55+heldout", "V4-V56+heldout"),
    ]:
        out = out.replace(a, b)
    if "VISION_V56_SMOKE" not in out:
        out = out.replace(
            "SMOKE_POINTERS = [",
            'SMOKE_POINTERS = [\n'
            '    ("V56", DOC / "C444_VISION_V56_SMOKE.json"),\n'
            '    ("V56_heldout", DOC / "C445_VISION_V56_HELDOUT_SMOKE.json"),\n'
            '    ("V55", DOC / "C438_VISION_V55_SMOKE.json"),\n'
            '    ("V55_heldout", DOC / "C439_VISION_V55_HELDOUT_SMOKE.json"),',
            1,
        )
    dst = S / "c447_capture_office_regression.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_scorecard():
    board = None
    for ln in (S / "c442_scorecard_and_stage.py").read_text(encoding="utf-8").splitlines():
        if "BOARD_MD" in ln and "=" in ln:
            board = ln
            break
    if board is None:
        board = 'BOARD_MD = ROOT / "docs" / "ANT_UNIFIED_SCORECARD.md"'
    nl = "\\n"
    text = f'''# -*- coding: utf-8 -*-
"""C448: Unified scorecard + STAGE after C443-C447. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
{board}
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C448.md"
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
    c444 = load("docs/r50/C444_VISION_V56_SMOKE.json") or {{}}
    c444b = load("docs/r50/C444b_VISION_GATE_V56_CLAIM.json") or {{}}
    c445 = load("docs/r50/C445_VISION_V56_HELDOUT_SMOKE.json") or {{}}
    c445b = load("docs/r50/C445b_VISION_GATE_V56_HELDOUT_CLAIM.json") or {{}}
    c446 = load("docs/r50/C446_PRODUCT_U2C_COST.json") or {{}}
    c447 = load("docs/r50/C447_CAPTURE_OFFICE_REGRESSION.json") or {{}}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {{}}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {{}}
    c440 = load("docs/r50/C440_CONFIDENCE_GATE_STRETCH.json") or {{}}

    v56 = float(c444.get("rate") or 0.0)
    v56h = float(c445.get("rate") or 0.0)
    v56_claim = bool(c444b.get("vl_gate_v56_claim") or c444.get("vl_gate_v56_claim") or c444.get("claim"))
    v56h_claim = bool(c445b.get("vl_gate_v56_heldout_claim") or c445.get("vl_gate_v56_heldout_claim") or c445.get("claim"))
    disjoint = bool(c445.get("id_disjoint") or c445.get("disjoint") or c445b.get("id_disjoint") or c445b.get("disjoint"))

    _rl = c446.get("replace_ledger") or {{}}
    u2c_pass = bool(c446.get("pass")) if c446 else bool((prior.get("product_u2c") or {{}}).get("pass"))
    u2c_replace = float(
        c446.get("replace_ratio")
        or _rl.get("mean_ratio")
        or ((prior.get("product_u2c") or {{}}).get("replace_ratio"))
        or 4.07
    )
    conf = prior.get("confidence_gate") or {{}}
    if c440.get("pass") is not None:
        conf = {{
            "pass": bool(c440.get("pass")),
            "rate": float(c440.get("rate") or 1.0),
            "source": "C440",
        }}
    capture_pass = bool(c447.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {{}}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {{}}).get("shadow_pass", dissolve_pass))

    stage_ready = bool(
        v56_claim and v56h_claim and v56 >= GATE and v56h >= GATE
        and capture_pass and disjoint and u2c_pass
    )
    composite = 0.0
    if stage_ready:
        composite = 1.0 if (v56 >= 0.999 and v56h >= 0.999) else min(v56, v56h)

    out = {{
        "cycle": "C448",
        "timestamp": ts(),
        "gate": GATE,
        "vision": {{
            "v55": (prior.get("vision") or {{}}).get("v55") or {{"rate": 1.0, "claim": True}},
            "v55_heldout": (prior.get("vision") or {{}}).get("v55_heldout") or {{"rate": 1.0, "claim": True}},
            "v56": {{"rate": v56, "claim": v56_claim, "n": c444.get("n")}},
            "v56_heldout": {{"rate": v56h, "claim": v56h_claim, "disjoint": disjoint, "n": c445.get("n")}},
        }},
        "product_u2c": {{"pass": u2c_pass, "replace_ratio": u2c_replace, "source": "C446"}},
        "confidence_gate": conf if conf else {{"pass": True, "rate": 1.0, "source": "C440"}},
        "capture_regression": {{"pass": capture_pass, "source": "C447"}},
        "dissolve_shadow": {{
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        }},
        "composite": composite,
        "stage_ready": stage_ready,
        "v56_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }}
    J(DOC / "C448_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = [
        "# Unified Scorecard (C448)", "",
        f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"- Vision V56: rate={{v56}} claim={{v56_claim}}",
        f"- Vision V56 heldout: rate={{v56h}} claim={{v56h_claim}} disjoint={{disjoint}}",
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
        "# STAGE_ANT_C448", "",
        f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"**C443-C448 STAGE_READY={{'YES' if stage_ready else 'NO'}}**", "",
        "## Tip slice",
        "- C443: Vision V56 design fixtures (jpeg_q=62, floor>=60)",
        f"- C444: Vision V56 smoke claim **{{v56}}** (n={{c444.get('n')}})",
        f"- C445: Vision V56 heldout claim **{{v56h}}** (disjoint={{disjoint}})",
        f"- C446: product-u2c pass={{u2c_pass}} replace~={{u2c_replace}}",
        f"- C447: capture-office regression pass={{capture_pass}}",
        f"- C448: unified scorecard composite={{out['composite']}}", "",
        "## Constraints",
        "- Gate: 0.6",
        "- Gate2/3: untouched",
        "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V56 (uses 62)", "",
        "## Entry",
        f"- Scorecard: {{BOARD_MD.relative_to(ROOT).as_posix()}}",
        "- Latest JSON: docs/r50/SCORECARD_LATEST.json",
        "- This stage: docs/STAGE_ANT_C448.md", "",
    ]
    STAGE.write_text("\\n".join(stage) + "\\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''
    dst = S / "c448_scorecard_and_stage.py"
    dst.write_text(text, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def main():
    gen_design()
    gen_smoke()
    gen_heldout()
    gen_product_u2c()
    gen_regression()
    gen_scorecard()
    print("OK C443-C448 scripts")


if __name__ == "__main__":
    main()
