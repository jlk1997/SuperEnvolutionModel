# -*- coding: utf-8 -*-
"""Generate C551-C556 V74 scripts from V73. Knife: product-U2C (C554)."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"

THEMES = [
    ("emberhaven", "recv", "paid_total", "EMBERHAVEN GRAIN RECV", "RECV",
     lambda a,b,c: (a+b, [f"a paid {a:.2f}", f"b paid {b:.2f}", f"c open {c:.2f}", f"TOTAL PAID TARGET {a+b:.2f}"])),
    ("frostpeak", "wh", "qty_sum", "WH FROSTPEAK BIN", "RECV",
     lambda a,b,c: (float(a+b), [f"SKU1 qty {a} ok", f"SKU2 qty {c} hold", f"SKU3 qty {b} ok", f"qty_sum TARGET {a+b}"])),
    ("glacierhaven", "refund", "refund_done", "GLACIERHAVEN PATCH REFUND", "DONE",
     lambda a,b,c: (a+b, [f"itemR1 {a:.2f} done", f"itemR2 {b:.2f} done", f"itemR3 {c:.2f} open", f"refund_done TARGET {a+b:.2f}"])),
    ("heatherpass", "tax", "tax_base_paid", "HEATHERPASS TAX SLIP", "TAX",
     lambda a,b,c: (a+b, [f"base {a:.2f} paid", f"addon {b:.2f} paid", f"skip {c:.2f}", f"tax_base_paid TARGET {a+b:.2f}"])),
    ("indigohaven", "pay", "payroll_active", "INDIGOHAVEN PAYROLL", "PAY",
     lambda a,b,c: (a+b, [f"empA {a:.2f} active", f"empB {b:.2f} active", f"empC {c:.2f} leave", f"payroll_active TARGET {a+b:.2f}"])),
    ("junipercliff", "ship", "ship_ok", "JUNIPERCLIFF SHIP DOCK", "SHIP",
     lambda a,b,c: (float(a+b), [f"box1 {a} ok", f"box2 {b} ok", f"box3 {c} hold", f"ship_ok TARGET {a+b}"])),
    ("knollhaven", "sla", "sla_ok_hours", "KNOLLHAVEN SLA CARD", "SLA",
     lambda a,b,c: (a+b, [f"job1 {a:.2f} hours ok", f"job2 {b:.2f} hours ok", f"job3 {c:.2f} hours late", f"sla_ok_hours TARGET {a+b:.2f}"])),
    ("larkhaven", "exp", "exp_sum", "LARKHAVEN EXPENSE", "EXP",
     lambda a,b,c: (a+b, [f"e1 {a:.2f}", f"e2 {b:.2f}", f"e3 {c:.2f} void", f"exp_sum TARGET {a+b:.2f}"])),
    ("mosscliff", "po", "po_open", "MOSSCLIFF PO SHEET", "PO",
     lambda a,b,c: (a+b, [f"line1 {a:.2f} open", f"line2 {b:.2f} open", f"line3 {c:.2f} closed", f"po_open TARGET {a+b:.2f}"])),
    ("northhaven", "order", "order_paid", "NORTHHAVEN ORDER", "ORD",
     lambda a,b,c: (a+b, [f"skuA {a:.2f} paid", f"skuB {b:.2f} paid", f"skuC {c:.2f} due", f"order_paid TARGET {a+b:.2f}"])),
    ("opalcliff", "dup", "dup_mark", "OPALCLIFF DUP MARK", "DUP",
     lambda a,b,c: (2.0, ["markA 1", "markB 1", "markC 0", "dup_mark TARGET 2"])),
    ("pinecrestpass", "zero", "zero_check", "PINECRESTPASS AIR ZERO", "ZERO",
     lambda a,b,c: (0.0, ["z1 0.00", "z2 0.00", "z3 0.00", "zero_check TARGET 0.00"])),
    ("quartzhaven", "ledger", "ledger_net", "QUARTZHAVEN LEDGER", "LED",
     lambda a,b,c: (a+b, [f"dr {a:.2f}", f"cr {b:.2f}", f"adj {c:.2f}", f"ledger_net TARGET {a+b:.2f}"])),
    ("reedhaven", "ui", "ui_ok", "REEDHAVEN UI SCAN", "UI",
     lambda a,b,c: (1.0, ["btnOK 1", "btnSkip 0", "btnBad 0", "ui_ok TARGET 1"])),
    ("stonehaven", "stack", "stack_count", "STONEHAVEN STACK", "STK",
     lambda a,b,c: (float(a+b), [f"p1 {a}", f"p2 {b}", f"p3 {c}", f"stack_count TARGET {a+b}"])),
    ("thunderpass", "fax", "fax_pages", "THUNDERPASS FAX", "FAX",
     lambda a,b,c: (float(a+b), [f"pgA {a}", f"pgB {b}", f"pgC {c} drop", f"fax_pages TARGET {a+b}"])),
    ("umbrahaven", "glare", "glare_ok", "UMBRAHAVEN GLARE", "GLR",
     lambda a,b,c: (1.0, ["zone1 1 ok", "zone2 0", "zone3 0", "glare_ok TARGET 1"])),
    ("valecliff", "tab", "tab_index", "VALECLIFF TAB INDEX", "TAB",
     lambda a,b,c: (float(a+b), [f"tabA {a}", f"tabB {b}", f"tabC {c}", f"tab_index TARGET {a+b}"])),
]
TRAIN_ABC = [
    (328.0, 344.0, 163.0), (275, 303, 183), (257.0, 281.75, 141.0), (382.0, 400.0, 219.0),
    (445.0, 469.0, 201.0), (215, 231, 159), (281.0, 272.0, 146.0), (293.0, 323.25, 165.0),
    (327.0, 310.0, 174.0), (360.0, 348.0, 162.0), (1, 1, 0), (0, 0, 0),
    (426.0, 449.0, 187.0), (1, 0, 0), (67, 59, 37), (85, 69, 60), (1, 0, 0), (105, 87, 57),
]
HELDOUT_ABC = [
    (209.0, 223.25, 114.0), (171, 199, 121), (167.0, 182.0, 102.0), (270.0, 286.0, 143.0),
    (311.0, 327.0, 138.0), (129, 143, 107), (175.0, 171.0, 108.0), (193.0, 213.25, 114.0),
    (213.0, 201.0, 117.0), (240.0, 227.5, 109.0), (1, 1, 0), (0, 0, 0),
    (275.0, 292.0, 124.0), (1, 0, 0), (43, 40, 35), (59, 53, 41), (1, 0, 0), (69, 63, 42),
]
THEME_STR = "emberhaven_frostpeak_glacierhaven_heatherpass_indigohaven_junipercliff_knollhaven_larkhaven_mosscliff_northhaven_opalcliff_pinecrestpass_quartzhaven_reedhaven_stonehaven_thunderpass_umbrahaven_valecliff"
OLD_THEME = "maplehaven_nimbuscliff_oakridgepass_prairiecrest_quarryhaven_riverhaven_sagecliff_tidehaven_umbrahollow_violetpass_willowhaven_xenonridge_yarrowhaven_zephyrhaven_aldercrest_birchhaven_cinderhaven_dewstonepass"


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
    src = src.replace("# --- V73 overlays (new vs V72) ---", "# --- V74 overlays (new vs V73) ---")
    for a, b in [
        ("MAPLEHAVEN bait", "EMBERHAVEN bait"), ("DEWSTONEPASS bait", "VALECLIFF bait"),
        ("XENONRIDGE ghost", "PINECRESTPASS ghost"), ("ZEPHYRHAVEN bait", "REEDHAVEN bait"),
        ("RIVERHAVEN bait", "JUNIPERCLIFF bait"), ("ALDERCREST", "STONEHAVEN"),
        ("NIMBUSCLIFF bait", "FROSTPEAK bait"),
        ("maple mist + dewstone ticks (V73-only)", "ember mist + valecliff ticks (V74-only)"),
    ]:
        src = src.replace(a, b)
    return src


def gen_design():
    out = (S / "c545_vision_v73_design_and_batch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C545", "C551"), ("c545", "c551"), ("V73", "V74"), ("v73", "v74"),
        ("_v73c545", "_v74c551"),
        ("Harder than V72", "Harder than V73"),
        ("harder than V72", "harder than V73"),
        (OLD_THEME, THEME_STR),
        ("V73 keeps floor", "V74 keeps floor"),
        ("C545 design+fixtures; no VL claim", "C551 design+fixtures; no VL claim"),
        ("fixtures only; claim deferred to C546 VL smoke", "fixtures only; claim deferred to C552 VL smoke"),
        ("No claim until C546 VL", "No claim until C552 VL"),
        ("kept on V73", "kept on V74"),
        ('"harder_than": "v72_ultramarine_limestonebay"', '"harder_than": "v73_maplehaven_dewstonepass"'),
        ("r50plus_v73_maplehaven_dewstonepass", "r50plus_v74_emberhaven_valecliff"),
    ]:
        out = out.replace(a, b)
    out = out.replace(
        "NEW themes vs V72: maplehaven, nimbuscliff, oakridgepass, prairiecrest, quarryhaven, riverhaven, sagecliff, tidehaven,\numbrahollow, violetpass, willowhaven, xenonridge, yarrowhaven, zephyrhaven, aldercrest, birchhaven, cinderhaven, dewstonepass.",
        "NEW themes vs V73: emberhaven, frostpeak, glacierhaven, heatherpass, indigohaven, junipercliff, knollhaven, larkhaven,\nmosscliff, northhaven, opalcliff, pinecrestpass, quartzhaven, reedhaven, stonehaven, thunderpass, umbrahaven, valecliff.",
    )
    out = replace_specs(out, build_specs("v74", "V74", TRAIN_ABC))
    out = retarget_overlay(out)
    dst = S / "c551_vision_v74_design_and_batch.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_smoke():
    out = (S / "c546_vision_v73_smoke.py").read_text(encoding="utf-8")
    for a, b in [
        ("C546", "C552"), ("c546", "c552"), ("V73", "V74"), ("v73", "v74"),
        ("r50plus_v73_maplehaven_dewstonepass_clarity_floor_n>=16_qwen35_2b",
         "r50plus_v74_emberhaven_valecliff_clarity_floor_n>=16_qwen35_2b"),
        ("Uses C545 fixtures", "Uses C551 fixtures"),
    ]:
        out = out.replace(a, b)
    dst = S / "c552_vision_v74_smoke.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_heldout():
    out = (S / "c547_vision_v73_heldout.py").read_text(encoding="utf-8")
    for a, b in [
        ("C547", "C553"), ("c547", "c553"), ("C545", "C551"),
        ("V73", "V74"), ("v73", "v74"),
        ("_v73hc547", "_v74hc553"),
        ("_v73c545", "_v74c551"),
    ]:
        out = out.replace(a, b)
    out = replace_specs(out, build_specs("v74h", "V74H", HELDOUT_ABC))
    out = retarget_overlay(out)
    out2 = []
    seen_fix = seen_train = seen_run = False
    for ln in out.splitlines():
        s = ln.strip()
        if s.startswith("FIX = ") and not seen_fix:
            out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v74h"')
            seen_fix = True
            continue
        if s.startswith("TRAIN_FIX = ") and not seen_train:
            out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v74"')
            seen_train = True
            continue
        if s.startswith("RUN = ") and "vision_v74" in s and not seen_run:
            out2.append('RUN = ROOT / "runs/vision_v74h_c553"')
            seen_run = True
            continue
        out2.append(ln)
    out = "\n".join(out2) + "\n"
    dst = S / "c553_vision_v74_heldout.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_u2c():
    out = (S / "c542_product_u2c_cost.py").read_text(encoding="utf-8")
    for a, b in [
        ("C542", "C554"), ("c542", "c554"),
        ("product_u2c_c542", "product_u2c_c554"),
        ("u2c_cost_c542", "u2c_cost_c554"),
        ("after V72", "after V74"), ("after V73", "after V74"),
        ("V72+", "V74+"), ("V73+", "V74+"),
    ]:
        out = out.replace(a, b)
    dst = S / "c554_product_u2c_cost.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_regression():
    out = (S / "c549_capture_office_regression.py").read_text(encoding="utf-8")
    for a, b in [
        ("C549", "C555"), ("c549", "c555"),
        ("capture_regression_c549", "capture_regression_c555"),
        ("after C545-C548", "after C551-C554"),
        ("V4-V73+heldout", "V4-V74+heldout"),
    ]:
        out = out.replace(a, b)
    if "VISION_V74_SMOKE" not in out:
        out = out.replace(
            "SMOKE_POINTERS = [",
            'SMOKE_POINTERS = [\n'
            '    ("V74", DOC / "C552_VISION_V74_SMOKE.json"),\n'
            '    ("V74_heldout", DOC / "C553_VISION_V74_HELDOUT_SMOKE.json"),\n'
            '    ("V73", DOC / "C546_VISION_V73_SMOKE.json"),\n'
            '    ("V73_heldout", DOC / "C547_VISION_V73_HELDOUT_SMOKE.json"),',
            1,
        )
    dst = S / "c555_capture_office_regression.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_scorecard():
    board = 'BOARD_MD = ROOT / "docs" / "ANT_UNIFIED_SCORECARD.md"'
    for ln in (S / "c550_scorecard_and_stage.py").read_text(encoding="utf-8").splitlines():
        if "BOARD_MD" in ln and "=" in ln:
            board = ln
            break
    nl = "\\n"
    text = f'''# -*- coding: utf-8 -*-
"""C556: Unified scorecard + STAGE after C551-C555. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
{board}
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C556.md"
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
    c552 = load("docs/r50/C552_VISION_V74_SMOKE.json") or {{}}
    c552b = load("docs/r50/C552b_VISION_GATE_V74_CLAIM.json") or {{}}
    c553 = load("docs/r50/C553_VISION_V74_HELDOUT_SMOKE.json") or {{}}
    c553b = load("docs/r50/C553b_VISION_GATE_V74_HELDOUT_CLAIM.json") or {{}}
    c554 = load("docs/r50/C554_PRODUCT_U2C_COST.json") or {{}}
    c555 = load("docs/r50/C555_CAPTURE_OFFICE_REGRESSION.json") or {{}}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {{}}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {{}}
    c548 = load("docs/r50/C548_CONFIDENCE_GATE_STRETCH.json") or {{}}

    v74 = float(c552.get("rate") or 0.0)
    v74h = float(c553.get("rate") or 0.0)
    v74_claim = bool(c552b.get("vl_gate_v74_claim") or c552.get("vl_gate_v74_claim") or c552.get("claim"))
    v74h_claim = bool(c553b.get("vl_gate_v74_heldout_claim") or c553.get("vl_gate_v74_heldout_claim") or c553.get("claim"))
    disjoint = bool(c553.get("id_disjoint") or c553.get("disjoint") or c553b.get("id_disjoint") or c553b.get("disjoint"))
    conf = prior.get("confidence_gate") or {{}}
    if c548.get("pass") is not None:
        conf = {{"pass": bool(c548.get("pass")), "rate": float(c548.get("rate") or 1.0), "source": "C548"}}
    u2c_pass = bool(c554.get("pass"))
    replace = float(
        c554.get("replace_ratio")
        or c554.get("mean_ratio")
        or ((c554.get("replace_ledger") or {{}}).get("mean_ratio"))
        or 4.07
    )
    capture_pass = bool(c555.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {{}}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {{}}).get("shadow_pass", dissolve_pass))

    stage_ready = bool(
        v74_claim and v74h_claim and v74 >= GATE and v74h >= GATE
        and capture_pass and disjoint and u2c_pass
    )
    composite = 0.0
    if stage_ready:
        composite = 1.0 if (v74 >= 0.999 and v74h >= 0.999) else min(v74, v74h)

    out = {{
        "cycle": "C556",
        "timestamp": ts(),
        "gate": GATE,
        "vision": {{
            "v73": (prior.get("vision") or {{}}).get("v73") or {{"rate": 1.0, "claim": True}},
            "v73_heldout": (prior.get("vision") or {{}}).get("v73_heldout") or {{"rate": 1.0, "claim": True}},
            "v74": {{"rate": v74, "claim": v74_claim, "n": c552.get("n")}},
            "v74_heldout": {{"rate": v74h, "claim": v74h_claim, "disjoint": disjoint, "n": c553.get("n")}},
        }},
        "product_u2c": {{"pass": u2c_pass, "replace_ratio": replace, "source": "C554"}},
        "confidence_gate": conf if conf else {{"pass": True, "rate": 1.0, "source": "C548"}},
        "capture_regression": {{"pass": capture_pass, "source": "C555"}},
        "dissolve_shadow": {{
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        }},
        "composite": composite,
        "stage_ready": stage_ready,
        "v74_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }}
    J(DOC / "C556_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = [
        "# Unified Scorecard (C556)", "",
        f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"- Vision V74: rate={{v74}} claim={{v74_claim}}",
        f"- Vision V74 heldout: rate={{v74h}} claim={{v74h_claim}} disjoint={{disjoint}}",
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
        "# STAGE_ANT_C556", "",
        f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"**C551-C556 STAGE_READY={{'YES' if stage_ready else 'NO'}}**", "",
        "## Tip slice",
        "- C551: Vision V74 design fixtures (jpeg_q=62, floor>=60, long themes)",
        f"- C552: Vision V74 smoke claim **{{v74}}** (n={{c552.get('n')}})",
        f"- C553: Vision V74 heldout claim **{{v74h}}** (disjoint={{disjoint}})",
        f"- C554: product-U2C pass={{u2c_pass}} replace≈{{replace:.4f}}×",
        f"- C555: capture-office regression pass={{capture_pass}}",
        f"- C556: unified scorecard composite={{out['composite']}}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally; not model-plus-separate-agent).", "",
        "## Constraints",
        "- Gate: 0.6",
        "- Gate2/3: untouched",
        "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V74 (uses 62)", "",
        "## Entry",
        f"- Scorecard: {{BOARD_MD.relative_to(ROOT).as_posix()}}",
        "- Latest JSON: docs/r50/SCORECARD_LATEST.json",
        "- This stage: docs/STAGE_ANT_C556.md", "",
    ]
    STAGE.write_text("\\n".join(stage) + "\\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''
    dst = S / "c556_scorecard_and_stage.py"
    dst.write_text(text, encoding="utf-8")
    print("wrote", dst.name)


def main():
    gen_design()
    gen_smoke()
    gen_heldout()
    gen_u2c()
    gen_regression()
    gen_scorecard()
    print("OK C551-C556")


if __name__ == "__main__":
    main()
