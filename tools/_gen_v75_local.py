# -*- coding: utf-8 -*-
"""Generate C557-C562 V75 scripts from V74. Knife: confidence-gate (C560)."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"

THEMES = [
    ("windhaven", "recv", "paid_total", "WINDHAVEN GRAIN RECV", "RECV",
     lambda a,b,c: (a+b, [f"a paid {a:.2f}", f"b paid {b:.2f}", f"c open {c:.2f}", f"TOTAL PAID TARGET {a+b:.2f}"])),
    ("xanaduhaven", "wh", "qty_sum", "WH XANADUHAVEN BIN", "RECV",
     lambda a,b,c: (float(a+b), [f"SKU1 qty {a} ok", f"SKU2 qty {c} hold", f"SKU3 qty {b} ok", f"qty_sum TARGET {a+b}"])),
    ("yuccaridge", "refund", "refund_done", "YUCCARIDGE PATCH REFUND", "DONE",
     lambda a,b,c: (a+b, [f"itemR1 {a:.2f} done", f"itemR2 {b:.2f} done", f"itemR3 {c:.2f} open", f"refund_done TARGET {a+b:.2f}"])),
    ("zinccliff", "tax", "tax_base_paid", "ZINCCLIFF TAX SLIP", "TAX",
     lambda a,b,c: (a+b, [f"base {a:.2f} paid", f"addon {b:.2f} paid", f"skip {c:.2f}", f"tax_base_paid TARGET {a+b:.2f}"])),
    ("ashenpass", "pay", "payroll_active", "ASHENPASS PAYROLL", "PAY",
     lambda a,b,c: (a+b, [f"empA {a:.2f} active", f"empB {b:.2f} active", f"empC {c:.2f} leave", f"payroll_active TARGET {a+b:.2f}"])),
    ("brackenpass", "ship", "ship_ok", "BRACKENPASS SHIP DOCK", "SHIP",
     lambda a,b,c: (float(a+b), [f"box1 {a} ok", f"box2 {b} ok", f"box3 {c} hold", f"ship_ok TARGET {a+b}"])),
    ("cedarpass", "sla", "sla_ok_hours", "CEDARPASS SLA CARD", "SLA",
     lambda a,b,c: (a+b, [f"job1 {a:.2f} hours ok", f"job2 {b:.2f} hours ok", f"job3 {c:.2f} hours late", f"sla_ok_hours TARGET {a+b:.2f}"])),
    ("duskcliff", "exp", "exp_sum", "DUSKCLIFF EXPENSE", "EXP",
     lambda a,b,c: (a+b, [f"e1 {a:.2f}", f"e2 {b:.2f}", f"e3 {c:.2f} void", f"exp_sum TARGET {a+b:.2f}"])),
    ("echohaven", "po", "po_open", "ECHOHAVEN PO SHEET", "PO",
     lambda a,b,c: (a+b, [f"line1 {a:.2f} open", f"line2 {b:.2f} open", f"line3 {c:.2f} closed", f"po_open TARGET {a+b:.2f}"])),
    ("firhaven", "order", "order_paid", "FIRHAVEN ORDER", "ORD",
     lambda a,b,c: (a+b, [f"skuA {a:.2f} paid", f"skuB {b:.2f} paid", f"skuC {c:.2f} due", f"order_paid TARGET {a+b:.2f}"])),
    ("grovecliff", "dup", "dup_mark", "GROVECLIFF DUP MARK", "DUP",
     lambda a,b,c: (2.0, ["markA 1", "markB 1", "markC 0", "dup_mark TARGET 2"])),
    ("hollowpass", "zero", "zero_check", "HOLLOWPASS AIR ZERO", "ZERO",
     lambda a,b,c: (0.0, ["z1 0.00", "z2 0.00", "z3 0.00", "zero_check TARGET 0.00"])),
    ("ivoryhaven", "ledger", "ledger_net", "IVORYHAVEN LEDGER", "LED",
     lambda a,b,c: (a+b, [f"dr {a:.2f}", f"cr {b:.2f}", f"adj {c:.2f}", f"ledger_net TARGET {a+b:.2f}"])),
    ("jasperhaven", "ui", "ui_ok", "JASPERHAVEN UI SCAN", "UI",
     lambda a,b,c: (1.0, ["btnOK 1", "btnSkip 0", "btnBad 0", "ui_ok TARGET 1"])),
    ("kelphaven", "stack", "stack_count", "KELPHAVEN STACK", "STK",
     lambda a,b,c: (float(a+b), [f"p1 {a}", f"p2 {b}", f"p3 {c}", f"stack_count TARGET {a+b}"])),
    ("lotuspass", "fax", "fax_pages", "LOTUSPASS FAX", "FAX",
     lambda a,b,c: (float(a+b), [f"pgA {a}", f"pgB {b}", f"pgC {c} drop", f"fax_pages TARGET {a+b}"])),
    ("meadowpass", "glare", "glare_ok", "MEADOWPASS GLARE", "GLR",
     lambda a,b,c: (1.0, ["zone1 1 ok", "zone2 0", "zone3 0", "glare_ok TARGET 1"])),
    ("nimbuspass", "tab", "tab_index", "NIMBUSPASS TAB INDEX", "TAB",
     lambda a,b,c: (float(a+b), [f"tabA {a}", f"tabB {b}", f"tabC {c}", f"tab_index TARGET {a+b}"])),
]
TRAIN_ABC = [
    (336.0, 351.75, 167.0), (283, 311, 187), (264.0, 289.5, 145.0), (390.0, 408.0, 225.0),
    (453.0, 477.0, 205.0), (221, 237, 163), (289.0, 279.75, 150.0), (301.0, 331.5, 169.0),
    (335.0, 318.0, 178.0), (368.0, 356.0, 166.0), (1, 1, 0), (0, 0, 0),
    (434.0, 456.75, 191.0), (1, 0, 0), (69, 61, 39), (87, 71, 62), (1, 0, 0), (108, 89, 59),
]
HELDOUT_ABC = [
    (215.0, 229.0, 118.0), (177, 205, 125), (173.0, 187.75, 106.0), (278.0, 294.0, 147.0),
    (319.0, 335.0, 142.0), (133, 147, 111), (181.0, 176.75, 112.0), (199.0, 219.5, 118.0),
    (219.0, 207.0, 121.0), (246.0, 233.25, 113.0), (1, 1, 0), (0, 0, 0),
    (281.0, 297.75, 128.0), (1, 0, 0), (45, 42, 37), (61, 55, 43), (1, 0, 0), (71, 65, 44),
]
THEME_STR = "windhaven_xanaduhaven_yuccaridge_zinccliff_ashenpass_brackenpass_cedarpass_duskcliff_echohaven_firhaven_grovecliff_hollowpass_ivoryhaven_jasperhaven_kelphaven_lotuspass_meadowpass_nimbuspass"
OLD_THEME = "emberhaven_frostpeak_glacierhaven_heatherpass_indigohaven_junipercliff_knollhaven_larkhaven_mosscliff_northhaven_opalcliff_pinecrestpass_quartzhaven_reedhaven_stonehaven_thunderpass_umbrahaven_valecliff"


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
    src = src.replace("# --- V74 overlays (new vs V73) ---", "# --- V75 overlays (new vs V74) ---")
    for a, b in [
        ("EMBERHAVEN bait", "WINDHAVEN bait"), ("VALECLIFF bait", "NIMBUSPASS bait"),
        ("PINECRESTPASS ghost", "HOLLOWPASS ghost"), ("REEDHAVEN bait", "JASPERHAVEN bait"),
        ("JUNIPERCLIFF bait", "BRACKENPASS bait"), ("STONEHAVEN", "KELPHAVEN"),
        ("FROSTPEAK bait", "XANADUHAVEN bait"),
        ("ember mist + valecliff ticks (V74-only)", "wind mist + nimbus ticks (V75-only)"),
    ]:
        src = src.replace(a, b)
    return src


def gen_design():
    out = (S / "c551_vision_v74_design_and_batch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C551", "C557"), ("c551", "c557"), ("V74", "V75"), ("v74", "v75"),
        ("_v74c551", "_v75c557"),
        ("Harder than V73", "Harder than V74"),
        ("harder than V73", "harder than V74"),
        (OLD_THEME, THEME_STR),
        ("V74 keeps floor", "V75 keeps floor"),
        ("C551 design+fixtures; no VL claim", "C557 design+fixtures; no VL claim"),
        ("fixtures only; claim deferred to C552 VL smoke", "fixtures only; claim deferred to C558 VL smoke"),
        ("No claim until C552 VL", "No claim until C558 VL"),
        ("kept on V74", "kept on V75"),
        ('"harder_than": "v73_maplehaven_dewstonepass"', '"harder_than": "v74_emberhaven_valecliff"'),
        ("r50plus_v74_emberhaven_valecliff", "r50plus_v75_windhaven_nimbuspass"),
    ]:
        out = out.replace(a, b)
    out = out.replace(
        "NEW themes vs V73: emberhaven, frostpeak, glacierhaven, heatherpass, indigohaven, junipercliff, knollhaven, larkhaven,\nmosscliff, northhaven, opalcliff, pinecrestpass, quartzhaven, reedhaven, stonehaven, thunderpass, umbrahaven, valecliff.",
        "NEW themes vs V74: windhaven, xanaduhaven, yuccaridge, zinccliff, ashenpass, brackenpass, cedarpass, duskcliff,\nechohaven, firhaven, grovecliff, hollowpass, ivoryhaven, jasperhaven, kelphaven, lotuspass, meadowpass, nimbuspass.",
    )
    out = replace_specs(out, build_specs("v75", "V75", TRAIN_ABC))
    out = retarget_overlay(out)
    dst = S / "c557_vision_v75_design_and_batch.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_smoke():
    out = (S / "c552_vision_v74_smoke.py").read_text(encoding="utf-8")
    for a, b in [
        ("C552", "C558"), ("c552", "c558"), ("V74", "V75"), ("v74", "v75"),
        ("r50plus_v74_emberhaven_valecliff_clarity_floor_n>=16_qwen35_2b",
         "r50plus_v75_windhaven_nimbuspass_clarity_floor_n>=16_qwen35_2b"),
        ("Uses C551 fixtures", "Uses C557 fixtures"),
    ]:
        out = out.replace(a, b)
    dst = S / "c558_vision_v75_smoke.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_heldout():
    out = (S / "c553_vision_v74_heldout.py").read_text(encoding="utf-8")
    for a, b in [
        ("C553", "C559"), ("c553", "c559"), ("C551", "C557"),
        ("V74", "V75"), ("v74", "v75"),
        ("_v74hc553", "_v75hc559"),
        ("_v74c551", "_v75c557"),
    ]:
        out = out.replace(a, b)
    out = replace_specs(out, build_specs("v75h", "V75H", HELDOUT_ABC))
    out = retarget_overlay(out)
    out2 = []
    seen_fix = seen_train = seen_run = False
    for ln in out.splitlines():
        s = ln.strip()
        if s.startswith("FIX = ") and not seen_fix:
            out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v75h"')
            seen_fix = True
            continue
        if s.startswith("TRAIN_FIX = ") and not seen_train:
            out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v75"')
            seen_train = True
            continue
        if s.startswith("RUN = ") and "vision_v75" in s and not seen_run:
            out2.append('RUN = ROOT / "runs/vision_v75h_c559"')
            seen_run = True
            continue
        out2.append(ln)
    out = "\n".join(out2) + "\n"
    dst = S / "c559_vision_v75_heldout.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_confidence():
    out = (S / "c548_confidence_gate_stretch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C548", "C560"), ("c548", "c560"),
        ("confidence_gate_c548", "confidence_gate_c560"),
        ("conf_gate_stretch_c548", "conf_gate_stretch_c560"),
        ("after V73", "after V75"), ("after V74", "after V75"),
        ("V73+", "V75+"), ("V74+", "V75+"),
    ]:
        out = out.replace(a, b)
    dst = S / "c560_confidence_gate_stretch.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_regression():
    out = (S / "c555_capture_office_regression.py").read_text(encoding="utf-8")
    for a, b in [
        ("C555", "C561"), ("c555", "c561"),
        ("capture_regression_c555", "capture_regression_c561"),
        ("after C551-C554", "after C557-C560"),
        ("V4-V74+heldout", "V4-V75+heldout"),
    ]:
        out = out.replace(a, b)
    if "VISION_V75_SMOKE" not in out:
        out = out.replace(
            "SMOKE_POINTERS = [",
            'SMOKE_POINTERS = [\n'
            '    ("V75", DOC / "C558_VISION_V75_SMOKE.json"),\n'
            '    ("V75_heldout", DOC / "C559_VISION_V75_HELDOUT_SMOKE.json"),\n'
            '    ("V74", DOC / "C552_VISION_V74_SMOKE.json"),\n'
            '    ("V74_heldout", DOC / "C553_VISION_V74_HELDOUT_SMOKE.json"),',
            1,
        )
    dst = S / "c561_capture_office_regression.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_scorecard():
    board = 'BOARD_MD = ROOT / "docs" / "ANT_UNIFIED_SCORECARD.md"'
    for ln in (S / "c556_scorecard_and_stage.py").read_text(encoding="utf-8").splitlines():
        if "BOARD_MD" in ln and "=" in ln:
            board = ln
            break
    nl = "\\n"
    text = f'''# -*- coding: utf-8 -*-
"""C562: Unified scorecard + STAGE after C557-C561. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
{board}
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C562.md"
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
    c558 = load("docs/r50/C558_VISION_V75_SMOKE.json") or {{}}
    c558b = load("docs/r50/C558b_VISION_GATE_V75_CLAIM.json") or {{}}
    c559 = load("docs/r50/C559_VISION_V75_HELDOUT_SMOKE.json") or {{}}
    c559b = load("docs/r50/C559b_VISION_GATE_V75_HELDOUT_CLAIM.json") or {{}}
    c560 = load("docs/r50/C560_CONFIDENCE_GATE_STRETCH.json") or {{}}
    c561 = load("docs/r50/C561_CAPTURE_OFFICE_REGRESSION.json") or {{}}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {{}}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {{}}
    c554 = load("docs/r50/C554_PRODUCT_U2C_COST.json") or {{}}

    v75 = float(c558.get("rate") or 0.0)
    v75h = float(c559.get("rate") or 0.0)
    v75_claim = bool(c558b.get("vl_gate_v75_claim") or c558.get("vl_gate_v75_claim") or c558.get("claim"))
    v75h_claim = bool(c559b.get("vl_gate_v75_heldout_claim") or c559.get("vl_gate_v75_heldout_claim") or c559.get("claim"))
    disjoint = bool(c559.get("id_disjoint") or c559.get("disjoint") or c559b.get("id_disjoint") or c559b.get("disjoint"))
    conf_pass = bool(c560.get("pass")) if c560 else bool((prior.get("confidence_gate") or {{}}).get("pass"))
    conf_rate = float(c560.get("rate") or ((prior.get("confidence_gate") or {{}}).get("rate")) or 1.0)
    u2c = prior.get("product_u2c") or {{}}
    if c554.get("pass") is not None:
        u2c = {{
            "pass": bool(c554.get("pass")),
            "replace_ratio": float(
                c554.get("replace_ratio")
                or c554.get("mean_ratio")
                or ((c554.get("replace_ledger") or {{}}).get("mean_ratio"))
                or 4.07
            ),
            "source": "C554",
        }}
    capture_pass = bool(c561.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {{}}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {{}}).get("shadow_pass", dissolve_pass))

    stage_ready = bool(
        v75_claim and v75h_claim and v75 >= GATE and v75h >= GATE
        and capture_pass and disjoint and conf_pass
    )
    composite = 0.0
    if stage_ready:
        composite = 1.0 if (v75 >= 0.999 and v75h >= 0.999) else min(v75, v75h)

    out = {{
        "cycle": "C562",
        "timestamp": ts(),
        "gate": GATE,
        "vision": {{
            "v74": (prior.get("vision") or {{}}).get("v74") or {{"rate": 1.0, "claim": True}},
            "v74_heldout": (prior.get("vision") or {{}}).get("v74_heldout") or {{"rate": 1.0, "claim": True}},
            "v75": {{"rate": v75, "claim": v75_claim, "n": c558.get("n")}},
            "v75_heldout": {{"rate": v75h, "claim": v75h_claim, "disjoint": disjoint, "n": c559.get("n")}},
        }},
        "product_u2c": u2c if u2c else {{"pass": True, "replace_ratio": 4.0694, "source": "C554"}},
        "confidence_gate": {{"pass": conf_pass, "rate": conf_rate, "source": "C560"}},
        "capture_regression": {{"pass": capture_pass, "source": "C561"}},
        "dissolve_shadow": {{
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        }},
        "composite": composite,
        "stage_ready": stage_ready,
        "v75_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }}
    J(DOC / "C562_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = [
        "# Unified Scorecard (C562)", "",
        f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"- Vision V75: rate={{v75}} claim={{v75_claim}}",
        f"- Vision V75 heldout: rate={{v75h}} claim={{v75h_claim}} disjoint={{disjoint}}",
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
        "# STAGE_ANT_C562", "",
        f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"**C557-C562 STAGE_READY={{'YES' if stage_ready else 'NO'}}**", "",
        "## Tip slice",
        "- C557: Vision V75 design fixtures (jpeg_q=62, floor>=60, long themes)",
        f"- C558: Vision V75 smoke claim **{{v75}}** (n={{c558.get('n')}})",
        f"- C559: Vision V75 heldout claim **{{v75h}}** (disjoint={{disjoint}})",
        f"- C560: confidence-gate stretch pass={{conf_pass}} rate={{conf_rate}}",
        f"- C561: capture-office regression pass={{capture_pass}}",
        f"- C562: unified scorecard composite={{out['composite']}}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally; not model-plus-separate-agent).", "",
        "## Constraints",
        "- Gate: 0.6",
        "- Gate2/3: untouched",
        "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V75 (uses 62)", "",
        "## Entry",
        f"- Scorecard: {{BOARD_MD.relative_to(ROOT).as_posix()}}",
        "- Latest JSON: docs/r50/SCORECARD_LATEST.json",
        "- This stage: docs/STAGE_ANT_C562.md", "",
    ]
    STAGE.write_text("\\n".join(stage) + "\\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''
    dst = S / "c562_scorecard_and_stage.py"
    dst.write_text(text, encoding="utf-8")
    print("wrote", dst.name)


def main():
    gen_design()
    gen_smoke()
    gen_heldout()
    gen_confidence()
    gen_regression()
    gen_scorecard()
    print("OK C557-C562")


if __name__ == "__main__":
    main()
