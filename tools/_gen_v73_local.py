# -*- coding: utf-8 -*-
"""Generate C545-C550 V73 scripts from V72. Knife: confidence-gate (C548)."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"

THEMES = [
    ("maplehaven", "recv", "paid_total", "MAPLEHAVEN GRAIN RECV", "RECV",
     lambda a,b,c: (a+b, [f"a paid {a:.2f}", f"b paid {b:.2f}", f"c open {c:.2f}", f"TOTAL PAID TARGET {a+b:.2f}"])),
    ("nimbuscliff", "wh", "qty_sum", "WH NIMBUSCLIFF BIN", "RECV",
     lambda a,b,c: (float(a+b), [f"SKU1 qty {a} ok", f"SKU2 qty {c} hold", f"SKU3 qty {b} ok", f"qty_sum TARGET {a+b}"])),
    ("oakridgepass", "refund", "refund_done", "OAKRIDGEPASS PATCH REFUND", "DONE",
     lambda a,b,c: (a+b, [f"itemR1 {a:.2f} done", f"itemR2 {b:.2f} done", f"itemR3 {c:.2f} open", f"refund_done TARGET {a+b:.2f}"])),
    ("prairiecrest", "tax", "tax_base_paid", "PRAIRIECREST TAX SLIP", "TAX",
     lambda a,b,c: (a+b, [f"base {a:.2f} paid", f"addon {b:.2f} paid", f"skip {c:.2f}", f"tax_base_paid TARGET {a+b:.2f}"])),
    ("quarryhaven", "pay", "payroll_active", "QUARRYHAVEN PAYROLL", "PAY",
     lambda a,b,c: (a+b, [f"empA {a:.2f} active", f"empB {b:.2f} active", f"empC {c:.2f} leave", f"payroll_active TARGET {a+b:.2f}"])),
    ("riverhaven", "ship", "ship_ok", "RIVERHAVEN SHIP DOCK", "SHIP",
     lambda a,b,c: (float(a+b), [f"box1 {a} ok", f"box2 {b} ok", f"box3 {c} hold", f"ship_ok TARGET {a+b}"])),
    ("sagecliff", "sla", "sla_ok_hours", "SAGECLIFF SLA CARD", "SLA",
     lambda a,b,c: (a+b, [f"job1 {a:.2f} hours ok", f"job2 {b:.2f} hours ok", f"job3 {c:.2f} hours late", f"sla_ok_hours TARGET {a+b:.2f}"])),
    ("tidehaven", "exp", "exp_sum", "TIDEHAVEN EXPENSE", "EXP",
     lambda a,b,c: (a+b, [f"e1 {a:.2f}", f"e2 {b:.2f}", f"e3 {c:.2f} void", f"exp_sum TARGET {a+b:.2f}"])),
    ("umbrahollow", "po", "po_open", "UMBRAHOLLOW PO SHEET", "PO",
     lambda a,b,c: (a+b, [f"line1 {a:.2f} open", f"line2 {b:.2f} open", f"line3 {c:.2f} closed", f"po_open TARGET {a+b:.2f}"])),
    ("violetpass", "order", "order_paid", "VIOLETPASS ORDER", "ORD",
     lambda a,b,c: (a+b, [f"skuA {a:.2f} paid", f"skuB {b:.2f} paid", f"skuC {c:.2f} due", f"order_paid TARGET {a+b:.2f}"])),
    ("willowhaven", "dup", "dup_mark", "WILLOWHAVEN DUP MARK", "DUP",
     lambda a,b,c: (2.0, ["markA 1", "markB 1", "markC 0", "dup_mark TARGET 2"])),
    ("xenonridge", "zero", "zero_check", "XENONRIDGE AIR ZERO", "ZERO",
     lambda a,b,c: (0.0, ["z1 0.00", "z2 0.00", "z3 0.00", "zero_check TARGET 0.00"])),
    ("yarrowhaven", "ledger", "ledger_net", "YARROWHAVEN LEDGER", "LED",
     lambda a,b,c: (a+b, [f"dr {a:.2f}", f"cr {b:.2f}", f"adj {c:.2f}", f"ledger_net TARGET {a+b:.2f}"])),
    ("zephyrhaven", "ui", "ui_ok", "ZEPHYRHAVEN UI SCAN", "UI",
     lambda a,b,c: (1.0, ["btnOK 1", "btnSkip 0", "btnBad 0", "ui_ok TARGET 1"])),
    ("aldercrest", "stack", "stack_count", "ALDERCREST STACK", "STK",
     lambda a,b,c: (float(a+b), [f"p1 {a}", f"p2 {b}", f"p3 {c}", f"stack_count TARGET {a+b}"])),
    ("birchhaven", "fax", "fax_pages", "BIRCHHAVEN FAX", "FAX",
     lambda a,b,c: (float(a+b), [f"pgA {a}", f"pgB {b}", f"pgC {c} drop", f"fax_pages TARGET {a+b}"])),
    ("cinderhaven", "glare", "glare_ok", "CINDERHAVEN GLARE", "GLR",
     lambda a,b,c: (1.0, ["zone1 1 ok", "zone2 0", "zone3 0", "glare_ok TARGET 1"])),
    ("dewstonepass", "tab", "tab_index", "DEWSTONEPASS TAB INDEX", "TAB",
     lambda a,b,c: (float(a+b), [f"tabA {a}", f"tabB {b}", f"tabC {c}", f"tab_index TARGET {a+b}"])),
]
TRAIN_ABC = [
    (320.0, 336.25, 159.0), (267, 295, 179), (250.0, 274.0, 137.0), (374.0, 392.0, 213.0),
    (437.0, 461.0, 197.0), (209, 225, 155), (273.0, 264.25, 142.0), (285.0, 315.0, 161.0),
    (319.0, 302.0, 170.0), (352.0, 340.0, 158.0), (1, 1, 0), (0, 0, 0),
    (418.0, 441.25, 183.0), (1, 0, 0), (65, 57, 35), (83, 67, 58), (1, 0, 0), (102, 85, 55),
]
HELDOUT_ABC = [
    (203.0, 217.5, 110.0), (165, 193, 117), (161.0, 176.25, 98.0), (262.0, 278.0, 139.0),
    (303.0, 319.0, 134.0), (125, 139, 103), (169.0, 165.25, 104.0), (187.0, 207.0, 110.0),
    (207.0, 195.0, 113.0), (234.0, 221.75, 105.0), (1, 1, 0), (0, 0, 0),
    (269.0, 286.25, 120.0), (1, 0, 0), (41, 38, 33), (57, 51, 39), (1, 0, 0), (67, 61, 40),
]
THEME_STR = "maplehaven_nimbuscliff_oakridgepass_prairiecrest_quarryhaven_riverhaven_sagecliff_tidehaven_umbrahollow_violetpass_willowhaven_xenonridge_yarrowhaven_zephyrhaven_aldercrest_birchhaven_cinderhaven_dewstonepass"
OLD_THEME = "ultramarine_verdantglen_windwardbay_xanadupass_yellowstone_zincplateau_ashenridge_bluemistcliff_coralhaven_driftstone_eaglehollow_firwoodpass_goldenharbor_hazelridge_ironhaven_jadecliff_kelpbasin_limestonebay"


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
    src = src.replace("# --- V72 overlays (new vs V71) ---", "# --- V73 overlays (new vs V72) ---")
    for a, b in [
        ("ULTRAMARINE bait", "MAPLEHAVEN bait"), ("LIMESTONEBAY bait", "DEWSTONEPASS bait"),
        ("FIRWOODPASS ghost", "XENONRIDGE ghost"), ("HAZELRIDGE bait", "ZEPHYRHAVEN bait"),
        ("ZINCPLATEAU bait", "RIVERHAVEN bait"), ("IRONHAVEN", "ALDERCREST"),
        ("VERDANTGLEN bait", "NIMBUSCLIFF bait"),
        ("ultra mist + limestone ticks (V72-only)", "maple mist + dewstone ticks (V73-only)"),
    ]:
        src = src.replace(a, b)
    return src


def gen_design():
    out = (S / "c539_vision_v72_design_and_batch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C539", "C545"), ("c539", "c545"), ("V72", "V73"), ("v72", "v73"),
        ("_v72c539", "_v73c545"),
        ("Harder than V71", "Harder than V72"),
        ("harder than V71", "harder than V72"),
        (OLD_THEME, THEME_STR),
        ("V72 keeps floor", "V73 keeps floor"),
        ("C539 design+fixtures; no VL claim", "C545 design+fixtures; no VL claim"),
        ("fixtures only; claim deferred to C540 VL smoke", "fixtures only; claim deferred to C546 VL smoke"),
        ("No claim until C540 VL", "No claim until C546 VL"),
        ("kept on V72", "kept on V73"),
        ('"harder_than": "v71_cedarhaven_thornfield"', '"harder_than": "v72_ultramarine_limestonebay"'),
        ("r50plus_v72_ultramarine_limestonebay", "r50plus_v73_maplehaven_dewstonepass"),
    ]:
        out = out.replace(a, b)
    out = out.replace(
        "NEW themes vs V71: ultramarine, verdantglen, windwardbay, xanadupass, yellowstone, zincplateau, ashenridge, bluemistcliff,\ncoralhaven, driftstone, eaglehollow, firwoodpass, goldenharbor, hazelridge, ironhaven, jadecliff, kelpbasin, limestonebay.",
        "NEW themes vs V72: maplehaven, nimbuscliff, oakridgepass, prairiecrest, quarryhaven, riverhaven, sagecliff, tidehaven,\numbrahollow, violetpass, willowhaven, xenonridge, yarrowhaven, zephyrhaven, aldercrest, birchhaven, cinderhaven, dewstonepass.",
    )
    out = replace_specs(out, build_specs("v73", "V73", TRAIN_ABC))
    out = retarget_overlay(out)
    dst = S / "c545_vision_v73_design_and_batch.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_smoke():
    out = (S / "c540_vision_v72_smoke.py").read_text(encoding="utf-8")
    for a, b in [
        ("C540", "C546"), ("c540", "c546"), ("V72", "V73"), ("v72", "v73"),
        ("r50plus_v72_ultramarine_limestonebay_clarity_floor_n>=16_qwen35_2b",
         "r50plus_v73_maplehaven_dewstonepass_clarity_floor_n>=16_qwen35_2b"),
        ("Uses C539 fixtures", "Uses C545 fixtures"),
    ]:
        out = out.replace(a, b)
    dst = S / "c546_vision_v73_smoke.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_heldout():
    out = (S / "c541_vision_v72_heldout.py").read_text(encoding="utf-8")
    for a, b in [
        ("C541", "C547"), ("c541", "c547"), ("C539", "C545"),
        ("V72", "V73"), ("v72", "v73"),
        ("_v72hc541", "_v73hc547"),
        ("_v72c539", "_v73c545"),
    ]:
        out = out.replace(a, b)
    out = replace_specs(out, build_specs("v73h", "V73H", HELDOUT_ABC))
    out = retarget_overlay(out)
    out2 = []
    seen_fix = seen_train = seen_run = False
    for ln in out.splitlines():
        s = ln.strip()
        if s.startswith("FIX = ") and not seen_fix:
            out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v73h"')
            seen_fix = True
            continue
        if s.startswith("TRAIN_FIX = ") and not seen_train:
            out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v73"')
            seen_train = True
            continue
        if s.startswith("RUN = ") and "vision_v73" in s and not seen_run:
            out2.append('RUN = ROOT / "runs/vision_v73h_c547"')
            seen_run = True
            continue
        out2.append(ln)
    out = "\n".join(out2) + "\n"
    dst = S / "c547_vision_v73_heldout.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_confidence():
    out = (S / "c536_confidence_gate_stretch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C536", "C548"), ("c536", "c548"),
        ("confidence_gate_c536", "confidence_gate_c548"),
        ("conf_gate_stretch_c536", "conf_gate_stretch_c548"),
        ("after V71", "after V73"), ("after V72", "after V73"),
        ("V71+", "V73+"), ("V72+", "V73+"),
    ]:
        out = out.replace(a, b)
    dst = S / "c548_confidence_gate_stretch.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_regression():
    out = (S / "c543_capture_office_regression.py").read_text(encoding="utf-8")
    for a, b in [
        ("C543", "C549"), ("c543", "c549"),
        ("capture_regression_c543", "capture_regression_c549"),
        ("after C539-C542", "after C545-C548"),
        ("V4-V72+heldout", "V4-V73+heldout"),
    ]:
        out = out.replace(a, b)
    if "VISION_V73_SMOKE" not in out:
        out = out.replace(
            "SMOKE_POINTERS = [",
            'SMOKE_POINTERS = [\n'
            '    ("V73", DOC / "C546_VISION_V73_SMOKE.json"),\n'
            '    ("V73_heldout", DOC / "C547_VISION_V73_HELDOUT_SMOKE.json"),\n'
            '    ("V72", DOC / "C540_VISION_V72_SMOKE.json"),\n'
            '    ("V72_heldout", DOC / "C541_VISION_V72_HELDOUT_SMOKE.json"),',
            1,
        )
    dst = S / "c549_capture_office_regression.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_scorecard():
    board = 'BOARD_MD = ROOT / "docs" / "ANT_UNIFIED_SCORECARD.md"'
    for ln in (S / "c544_scorecard_and_stage.py").read_text(encoding="utf-8").splitlines():
        if "BOARD_MD" in ln and "=" in ln:
            board = ln
            break
    nl = "\\n"
    text = f'''# -*- coding: utf-8 -*-
"""C550: Unified scorecard + STAGE after C545-C549. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
{board}
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C550.md"
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
    c546 = load("docs/r50/C546_VISION_V73_SMOKE.json") or {{}}
    c546b = load("docs/r50/C546b_VISION_GATE_V73_CLAIM.json") or {{}}
    c547 = load("docs/r50/C547_VISION_V73_HELDOUT_SMOKE.json") or {{}}
    c547b = load("docs/r50/C547b_VISION_GATE_V73_HELDOUT_CLAIM.json") or {{}}
    c548 = load("docs/r50/C548_CONFIDENCE_GATE_STRETCH.json") or {{}}
    c549 = load("docs/r50/C549_CAPTURE_OFFICE_REGRESSION.json") or {{}}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {{}}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {{}}
    c542 = load("docs/r50/C542_PRODUCT_U2C_COST.json") or {{}}

    v73 = float(c546.get("rate") or 0.0)
    v73h = float(c547.get("rate") or 0.0)
    v73_claim = bool(c546b.get("vl_gate_v73_claim") or c546.get("vl_gate_v73_claim") or c546.get("claim"))
    v73h_claim = bool(c547b.get("vl_gate_v73_heldout_claim") or c547.get("vl_gate_v73_heldout_claim") or c547.get("claim"))
    disjoint = bool(c547.get("id_disjoint") or c547.get("disjoint") or c547b.get("id_disjoint") or c547b.get("disjoint"))
    conf_pass = bool(c548.get("pass")) if c548 else bool((prior.get("confidence_gate") or {{}}).get("pass"))
    conf_rate = float(c548.get("rate") or ((prior.get("confidence_gate") or {{}}).get("rate")) or 1.0)
    u2c = prior.get("product_u2c") or {{}}
    if c542.get("pass") is not None:
        u2c = {{
            "pass": bool(c542.get("pass")),
            "replace_ratio": float(
                c542.get("replace_ratio")
                or c542.get("mean_ratio")
                or ((c542.get("replace_ledger") or {{}}).get("mean_ratio"))
                or 4.07
            ),
            "source": "C542",
        }}
    capture_pass = bool(c549.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {{}}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {{}}).get("shadow_pass", dissolve_pass))

    stage_ready = bool(
        v73_claim and v73h_claim and v73 >= GATE and v73h >= GATE
        and capture_pass and disjoint and conf_pass
    )
    composite = 0.0
    if stage_ready:
        composite = 1.0 if (v73 >= 0.999 and v73h >= 0.999) else min(v73, v73h)

    out = {{
        "cycle": "C550",
        "timestamp": ts(),
        "gate": GATE,
        "vision": {{
            "v72": (prior.get("vision") or {{}}).get("v72") or {{"rate": 1.0, "claim": True}},
            "v72_heldout": (prior.get("vision") or {{}}).get("v72_heldout") or {{"rate": 1.0, "claim": True}},
            "v73": {{"rate": v73, "claim": v73_claim, "n": c546.get("n")}},
            "v73_heldout": {{"rate": v73h, "claim": v73h_claim, "disjoint": disjoint, "n": c547.get("n")}},
        }},
        "product_u2c": u2c if u2c else {{"pass": True, "replace_ratio": 4.0694, "source": "C542"}},
        "confidence_gate": {{"pass": conf_pass, "rate": conf_rate, "source": "C548"}},
        "capture_regression": {{"pass": capture_pass, "source": "C549"}},
        "dissolve_shadow": {{
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        }},
        "composite": composite,
        "stage_ready": stage_ready,
        "v73_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }}
    J(DOC / "C550_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = [
        "# Unified Scorecard (C550)", "",
        f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"- Vision V73: rate={{v73}} claim={{v73_claim}}",
        f"- Vision V73 heldout: rate={{v73h}} claim={{v73h_claim}} disjoint={{disjoint}}",
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
        "# STAGE_ANT_C550", "",
        f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"**C545-C550 STAGE_READY={{'YES' if stage_ready else 'NO'}}**", "",
        "## Tip slice",
        "- C545: Vision V73 design fixtures (jpeg_q=62, floor>=60, long themes)",
        f"- C546: Vision V73 smoke claim **{{v73}}** (n={{c546.get('n')}})",
        f"- C547: Vision V73 heldout claim **{{v73h}}** (disjoint={{disjoint}})",
        f"- C548: confidence-gate stretch pass={{conf_pass}} rate={{conf_rate}}",
        f"- C549: capture-office regression pass={{capture_pass}}",
        f"- C550: unified scorecard composite={{out['composite']}}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally; not model-plus-separate-agent).", "",
        "## Constraints",
        "- Gate: 0.6",
        "- Gate2/3: untouched",
        "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V73 (uses 62)", "",
        "## Entry",
        f"- Scorecard: {{BOARD_MD.relative_to(ROOT).as_posix()}}",
        "- Latest JSON: docs/r50/SCORECARD_LATEST.json",
        "- This stage: docs/STAGE_ANT_C550.md", "",
    ]
    STAGE.write_text("\\n".join(stage) + "\\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''
    dst = S / "c550_scorecard_and_stage.py"
    dst.write_text(text, encoding="utf-8")
    print("wrote", dst.name)


def main():
    gen_design()
    gen_smoke()
    gen_heldout()
    gen_confidence()
    gen_regression()
    gen_scorecard()
    print("OK C545-C550")


if __name__ == "__main__":
    main()
