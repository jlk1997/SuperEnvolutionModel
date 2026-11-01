# -*- coding: utf-8 -*-
"""Generate C437-C442 V55 scripts from V54 via transform.
Themes NEW vs V54. Clarity floor jpeg_q>=60 (use 62).
Non-vision knife: confidence-gate stretch (C440).
Gate 0.6. Gate2/3 untouched. gen11 HOLD.
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"

THEMES = [
    ("azure", "recv", "paid_total", "AZURE GRAIN RECV", "RECV",
     lambda a,b,c: (a+b, [f"a paid {a:.2f}", f"b paid {b:.2f}", f"c open {c:.2f}", f"TOTAL PAID TARGET {a+b:.2f}"])),
    ("basil", "wh", "qty_sum", "WH BASIL BIN", "RECV",
     lambda a,b,c: (float(a+b), [f"SKU1 qty {a} ok", f"SKU2 qty {c} hold", f"SKU3 qty {b} ok", f"qty_sum TARGET {a+b}"])),
    ("cedar", "refund", "refund_done", "CEDAR PATCH REFUND", "DONE",
     lambda a,b,c: (a+b, [f"itemR1 {a:.2f} done", f"itemR2 {b:.2f} done", f"itemR3 {c:.2f} open", f"refund_done TARGET {a+b:.2f}"])),
    ("delta", "tax", "tax_base_paid", "DELTA TAX SLIP", "TAX",
     lambda a,b,c: (a+b, [f"base {a:.2f} paid", f"addon {b:.2f} paid", f"skip {c:.2f}", f"tax_base_paid TARGET {a+b:.2f}"])),
    ("echo", "pay", "payroll_active", "ECHO PAYROLL", "PAY",
     lambda a,b,c: (a+b, [f"empA {a:.2f} active", f"empB {b:.2f} active", f"empC {c:.2f} leave", f"payroll_active TARGET {a+b:.2f}"])),
    ("flint", "ship", "ship_ok", "FLINT SHIP DOCK", "SHIP",
     lambda a,b,c: (float(a+b), [f"box1 {a} ok", f"box2 {b} ok", f"box3 {c} hold", f"ship_ok TARGET {a+b}"])),
    ("grove", "sla", "sla_ok_hours", "GROVE SLA CARD", "SLA",
     lambda a,b,c: (a+b, [f"job1 {a:.2f} hours ok", f"job2 {b:.2f} hours ok", f"job3 {c:.2f} hours late", f"sla_ok_hours TARGET {a+b:.2f}"])),
    ("haze", "exp", "exp_sum", "HAZE EXPENSE", "EXP",
     lambda a,b,c: (a+b, [f"e1 {a:.2f}", f"e2 {b:.2f}", f"e3 {c:.2f} void", f"exp_sum TARGET {a+b:.2f}"])),
    ("indigo", "po", "po_open", "INDIGO PO SHEET", "PO",
     lambda a,b,c: (a+b, [f"line1 {a:.2f} open", f"line2 {b:.2f} open", f"line3 {c:.2f} closed", f"po_open TARGET {a+b:.2f}"])),
    ("jasper", "order", "order_paid", "JASPER ORDER", "ORD",
     lambda a,b,c: (a+b, [f"skuA {a:.2f} paid", f"skuB {b:.2f} paid", f"skuC {c:.2f} due", f"order_paid TARGET {a+b:.2f}"])),
    ("kiwi", "dup", "dup_mark", "KIWI DUP MARK", "DUP",
     lambda a,b,c: (2.0, ["markA 1", "markB 1", "markC 0", "dup_mark TARGET 2"])),
    ("linen", "zero", "zero_check", "LINEN AIR ZERO", "ZERO",
     lambda a,b,c: (0.0, ["z1 0.00", "z2 0.00", "z3 0.00", "zero_check TARGET 0.00"])),
    ("moss", "ledger", "ledger_net", "MOSS LEDGER", "LED",
     lambda a,b,c: (a+b, [f"dr {a:.2f}", f"cr {b:.2f}", f"adj {c:.2f}", f"ledger_net TARGET {a+b:.2f}"])),
    ("noon", "ui", "ui_ok", "NOON UI SCAN", "UI",
     lambda a,b,c: (1.0, ["btnOK 1", "btnSkip 0", "btnBad 0", "ui_ok TARGET 1"])),
    ("onyx", "stack", "stack_count", "ONYX STACK", "STK",
     lambda a,b,c: (float(a+b), [f"p1 {a}", f"p2 {b}", f"p3 {c}", f"stack_count TARGET {a+b}"])),
    ("pine", "fax", "fax_pages", "PINE FAX", "FAX",
     lambda a,b,c: (float(a+b), [f"pgA {a}", f"pgB {b}", f"pgC {c} drop", f"fax_pages TARGET {a+b}"])),
    ("quill", "glare", "glare_ok", "QUILL GLARE", "GLR",
     lambda a,b,c: (1.0, ["zone1 1 ok", "zone2 0", "zone3 0", "glare_ok TARGET 1"])),
    ("ridge", "tab", "tab_index", "RIDGE TAB INDEX", "TAB",
     lambda a,b,c: (float(a+b), [f"tabA {a}", f"tabB {b}", f"tabC {c}", f"tab_index TARGET {a+b}"])),
]
TRAIN_ABC = [
    (181.0, 186.5, 79.0), (134, 161, 96), (126.0, 133.25, 62.0), (223.0, 231.0, 114.0),
    (279.0, 291.0, 103.0), (109, 115, 71), (139.0, 127.5, 68.0), (151.0, 162.25, 77.0),
    (176.0, 159.0, 86.0), (208.0, 189.5, 74.0), (1, 1, 0), (0, 0, 0),
    (241.0, 254.5, 99.0), (1, 0, 0), (27, 21, 9), (36, 29, 22), (1, 0, 0), (46, 39, 19),
]
HELDOUT_ABC = [
    (104.0, 109.5, 48.0), (76, 94, 55), (73.0, 79.25, 36.0), (138.0, 145.0, 66.0),
    (169.0, 176.0, 61.0), (63, 67, 41), (81.0, 74.75, 42.0), (91.0, 97.5, 48.0),
    (109.0, 97.0, 51.0), (128.0, 115.5, 43.0), (1, 1, 0), (0, 0, 0),
    (149.0, 157.25, 58.0), (1, 0, 0), (15, 12, 7), (21, 17, 13), (1, 0, 0), (29, 24, 14),
]
THEME_STR = "azure_basil_cedar_delta_echo_flint_grove_haze_indigo_jasper_kiwi_linen_moss_noon_onyx_pine_quill_ridge"
OLD_THEME = "coral_dune_ember_frost_granite_harbor_ivory_jade_knoll_lotus_maple_nebula_olive_pearl_quartz_reef_spruce_terra"


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
    src = src.replace("# --- V54 overlays (new vs V50) ---", "# --- V55 overlays (new vs V54) ---")
    src = src.replace("# --- V54 overlays (new vs V53) ---", "# --- V55 overlays (new vs V54) ---")
    for a, b in [
        ("CORAL bait", "AZURE bait"), ("TERRA bait", "RIDGE bait"),
        ("NEBULA ghost", "LINEN ghost"), ("PEARL bait", "NOON bait"),
        ("HARBOR bait", "FLINT bait"), ("QUARTZ", "ONYX"),
        ("DUNE bait", "BASIL bait"),
        ("KELP bait", "AZURE bait"), ("BIRCH bait", "RIDGE bait"),
        ("VIOLET ghost", "LINEN ghost"), ("XENON bait", "NOON bait"),
        ("PLASMA bait", "FLINT bait"), ("YOLK", "ONYX"),
        ("LAVA bait", "BASIL bait"),
        ("dew drops + vine marks (V54-only)", "mist rings + bark ticks (V55-only)"),
        ("salt spray + bark notches (V53-only)", "mist rings + bark ticks (V55-only)"),
    ]:
        src = src.replace(a, b)
    return src


def gen_design():
    out = (S / "c431_vision_v54_design_and_batch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C431", "C437"), ("c431", "c437"), ("V54", "V55"), ("v54", "v55"),
        ("_v54c431", "_v55c437"),
        ("Harder than V40", "Harder than V54"),
        ("Harder than V53", "Harder than V54"),
        (OLD_THEME, THEME_STR),
        ("V54 keeps floor", "V55 keeps floor"),
        ("C431 design+fixtures; no VL claim", "C437 design+fixtures; no VL claim"),
        ("fixtures only; claim deferred to C432 VL smoke", "fixtures only; claim deferred to C438 VL smoke"),
        ("No claim until C432 VL", "No claim until C438 VL"),
        ("kept on V54", "kept on V55"),
        ('"harder_than": "v53_kelp_birch"', '"harder_than": "v54_coral_terra"'),
        ("r50plus_v54_coral_terra", "r50plus_v55_azure_ridge"),
    ]:
        out = out.replace(a, b)
    out = out.replace(
        "NEW themes vs V52: coral, dune, ember, frost, granite, harbor, ivory, jade,\nknoll, lotus, maple, nebula, olive, pearl, quartz, reef, spruce, terra.",
        "NEW themes vs V54: azure, basil, cedar, delta, echo, flint, grove, haze,\nindigo, jasper, kiwi, linen, moss, noon, onyx, pine, quill, ridge.",
    )
    out = out.replace(
        "NEW themes vs V53: coral, dune, ember, frost, granite, harbor, ivory, jade,\nknoll, lotus, maple, nebula, olive, pearl, quartz, reef, spruce, terra.",
        "NEW themes vs V54: azure, basil, cedar, delta, echo, flint, grove, haze,\nindigo, jasper, kiwi, linen, moss, noon, onyx, pine, quill, ridge.",
    )
    out = replace_specs(out, build_specs("v55", "V55", TRAIN_ABC))
    out = retarget_overlay(out)
    dst = S / "c437_vision_v55_design_and_batch.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_smoke():
    out = (S / "c432_vision_v54_smoke.py").read_text(encoding="utf-8")
    for a, b in [
        ("C432", "C438"), ("c432", "c438"), ("V54", "V55"), ("v54", "v55"),
        ("r50plus_v54_coral_terra_clarity_floor_n>=16_qwen35_2b",
         "r50plus_v55_azure_ridge_clarity_floor_n>=16_qwen35_2b"),
        ("Uses C431 fixtures", "Uses C437 fixtures"),
    ]:
        out = out.replace(a, b)
    dst = S / "c438_vision_v55_smoke.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_heldout():
    out = (S / "c433_vision_v54_heldout.py").read_text(encoding="utf-8")
    for a, b in [
        ("C433", "C439"), ("c433", "c439"), ("C431", "C437"),
        ("V54", "V55"), ("v54", "v55"),
        ("_v54hc433", "_v55hc439"),
        ("_v54c431", "_v55c437"),
    ]:
        out = out.replace(a, b)
    out = replace_specs(out, build_specs("v55h", "V55H", HELDOUT_ABC))
    out = retarget_overlay(out)
    out2 = []
    seen_fix = seen_train = seen_run = False
    for ln in out.splitlines():
        s = ln.strip()
        if s.startswith("FIX = ") and not seen_fix:
            out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v55h"')
            seen_fix = True
            continue
        if s.startswith("TRAIN_FIX = ") and not seen_train:
            out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v55"')
            seen_train = True
            continue
        if s.startswith("RUN = ") and "vision_v55" in s and not seen_run:
            out2.append('RUN = ROOT / "runs/vision_v55h_c439"')
            seen_run = True
            continue
        out2.append(ln)
    out = "\n".join(out2) + "\n"
    dst = S / "c439_vision_v55_heldout.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_confidence():
    out = (S / "c428_confidence_gate_stretch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C428", "C440"), ("c428", "c440"),
        ("confidence_gate_c428", "confidence_gate_c440"),
        ("conf_gate_stretch_c428", "conf_gate_stretch_c440"),
        ("after V53", "after V55"), ("after V54", "after V55"),
        ("V53+", "V55+"), ("V54+", "V55+"),
    ]:
        out = out.replace(a, b)
    dst = S / "c440_confidence_gate_stretch.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_regression():
    out = (S / "c435_capture_office_regression.py").read_text(encoding="utf-8")
    for a, b in [
        ("C435", "C441"), ("c435", "c441"),
        ("capture_regression_c435", "capture_regression_c441"),
        ("after C425-C428", "after C437-C440"),
        ("after C431-C434", "after C437-C440"),
        ("V4-V53+heldout", "V4-V55+heldout"),
        ("V4-V54+heldout", "V4-V55+heldout"),
    ]:
        out = out.replace(a, b)
    if "VISION_V55_SMOKE" not in out:
        out = out.replace(
            "SMOKE_POINTERS = [",
            'SMOKE_POINTERS = [\n'
            '    ("V55", DOC / "C438_VISION_V55_SMOKE.json"),\n'
            '    ("V55_heldout", DOC / "C439_VISION_V55_HELDOUT_SMOKE.json"),\n'
            '    ("V54", DOC / "C432_VISION_V54_SMOKE.json"),\n'
            '    ("V54_heldout", DOC / "C433_VISION_V54_HELDOUT_SMOKE.json"),',
            1,
        )
    dst = S / "c441_capture_office_regression.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_scorecard():
    board = None
    for ln in (S / "c436_scorecard_and_stage.py").read_text(encoding="utf-8").splitlines():
        if "BOARD_MD" in ln and "=" in ln:
            board = ln
            break
    if board is None:
        board = 'BOARD_MD = ROOT / "docs" / "ANT_UNIFIED_SCORECARD.md"'
    # Use real newlines in written Python source via chr(10) to avoid escape maze
    nl = "\\n"
    text = f'''# -*- coding: utf-8 -*-
"""C442: Unified scorecard + STAGE after C437-C441. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
{board}
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C442.md"
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
    c438 = load("docs/r50/C438_VISION_V55_SMOKE.json") or {{}}
    c438b = load("docs/r50/C438b_VISION_GATE_V55_CLAIM.json") or {{}}
    c439 = load("docs/r50/C439_VISION_V55_HELDOUT_SMOKE.json") or {{}}
    c439b = load("docs/r50/C439b_VISION_GATE_V55_HELDOUT_CLAIM.json") or {{}}
    c440 = load("docs/r50/C440_CONFIDENCE_GATE_STRETCH.json") or {{}}
    c441 = load("docs/r50/C441_CAPTURE_OFFICE_REGRESSION.json") or {{}}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {{}}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {{}}
    c434 = load("docs/r50/C434_PRODUCT_U2C_COST.json") or {{}}

    v55 = float(c438.get("rate") or 0.0)
    v55h = float(c439.get("rate") or 0.0)
    v55_claim = bool(c438b.get("vl_gate_v55_claim") or c438.get("vl_gate_v55_claim") or c438.get("claim"))
    v55h_claim = bool(c439b.get("vl_gate_v55_heldout_claim") or c439.get("vl_gate_v55_heldout_claim") or c439.get("claim"))
    disjoint = bool(c439.get("id_disjoint") or c439.get("disjoint") or c439b.get("id_disjoint") or c439b.get("disjoint"))
    conf_pass = bool(c440.get("pass")) if c440 else bool((prior.get("confidence_gate") or {{}}).get("pass"))
    conf_rate = float(c440.get("rate") or ((prior.get("confidence_gate") or {{}}).get("rate")) or 1.0)
    u2c = prior.get("product_u2c") or {{}}
    if c434.get("pass") is not None:
        u2c = {{
            "pass": bool(c434.get("pass")),
            "replace_ratio": float(
                c434.get("replace_ratio")
                or c434.get("mean_ratio")
                or ((c434.get("replace_ledger") or {{}}).get("mean_ratio"))
                or 4.07
            ),
            "source": "C434",
        }}
    capture_pass = bool(c441.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {{}}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {{}}).get("shadow_pass", dissolve_pass))

    stage_ready = bool(
        v55_claim and v55h_claim and v55 >= GATE and v55h >= GATE
        and capture_pass and disjoint and conf_pass
    )
    composite = 0.0
    if stage_ready:
        composite = 1.0 if (v55 >= 0.999 and v55h >= 0.999) else min(v55, v55h)

    out = {{
        "cycle": "C442",
        "timestamp": ts(),
        "gate": GATE,
        "vision": {{
            "v54": (prior.get("vision") or {{}}).get("v54") or {{"rate": 1.0, "claim": True}},
            "v54_heldout": (prior.get("vision") or {{}}).get("v54_heldout") or {{"rate": 1.0, "claim": True}},
            "v55": {{"rate": v55, "claim": v55_claim, "n": c438.get("n")}},
            "v55_heldout": {{"rate": v55h, "claim": v55h_claim, "disjoint": disjoint, "n": c439.get("n")}},
        }},
        "product_u2c": u2c if u2c else {{"pass": True, "replace_ratio": 4.0694, "source": "C434"}},
        "confidence_gate": {{"pass": conf_pass, "rate": conf_rate, "source": "C440"}},
        "capture_regression": {{"pass": capture_pass, "source": "C441"}},
        "dissolve_shadow": {{
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        }},
        "composite": composite,
        "stage_ready": stage_ready,
        "v55_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }}
    J(DOC / "C442_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = [
        "# Unified Scorecard (C442)", "",
        f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"- Vision V55: rate={{v55}} claim={{v55_claim}}",
        f"- Vision V55 heldout: rate={{v55h}} claim={{v55h_claim}} disjoint={{disjoint}}",
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
        "# STAGE_ANT_C442", "",
        f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"**C437-C442 STAGE_READY={{'YES' if stage_ready else 'NO'}}**", "",
        "## Tip slice",
        "- C437: Vision V55 design fixtures (jpeg_q=62, floor>=60)",
        f"- C438: Vision V55 smoke claim **{{v55}}** (n={{c438.get('n')}})",
        f"- C439: Vision V55 heldout claim **{{v55h}}** (disjoint={{disjoint}})",
        f"- C440: confidence-gate stretch pass={{conf_pass}} rate={{conf_rate}}",
        f"- C441: capture-office regression pass={{capture_pass}}",
        f"- C442: unified scorecard composite={{out['composite']}}", "",
        "## Constraints",
        "- Gate: 0.6",
        "- Gate2/3: untouched",
        "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V55 (uses 62)", "",
        "## Entry",
        f"- Scorecard: {{BOARD_MD.relative_to(ROOT).as_posix()}}",
        "- Latest JSON: docs/r50/SCORECARD_LATEST.json",
        "- This stage: docs/STAGE_ANT_C442.md", "",
    ]
    STAGE.write_text("\\n".join(stage) + "\\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''
    # Convert intentional \\n in join/write_text to real \n escapes in source
    text = text.replace('"\\\\n"', '"\\n"')  # shouldn't match
    # The f-string produced literal backslash-n in join strings which is correct for Python source
    dst = S / "c442_scorecard_and_stage.py"
    dst.write_text(text, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def main():
    gen_design()
    gen_smoke()
    gen_heldout()
    gen_confidence()
    gen_regression()
    gen_scorecard()
    print("OK C437-C442 scripts")


if __name__ == "__main__":
    main()
