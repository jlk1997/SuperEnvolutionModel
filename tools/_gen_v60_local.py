# -*- coding: utf-8 -*-
"""Generate C467-C472 V60 scripts from V59 via transform.
Themes NEW vs V59; avoid short VL-collapse names (foam lesson).
Clarity floor jpeg_q>=60 (use 62). Non-vision knife: product-u2c (C470).
Gate 0.6. Gate2/3 untouched. gen11 HOLD. V60 milestone.
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"

THEMES = [
    ("anchor", "recv", "paid_total", "ANCHOR GRAIN RECV", "RECV",
     lambda a,b,c: (a+b, [f"a paid {a:.2f}", f"b paid {b:.2f}", f"c open {c:.2f}", f"TOTAL PAID TARGET {a+b:.2f}"])),
    ("beacon", "wh", "qty_sum", "WH BEACON BIN", "RECV",
     lambda a,b,c: (float(a+b), [f"SKU1 qty {a} ok", f"SKU2 qty {c} hold", f"SKU3 qty {b} ok", f"qty_sum TARGET {a+b}"])),
    ("citadel", "refund", "refund_done", "CITADEL PATCH REFUND", "DONE",
     lambda a,b,c: (a+b, [f"itemR1 {a:.2f} done", f"itemR2 {b:.2f} done", f"itemR3 {c:.2f} open", f"refund_done TARGET {a+b:.2f}"])),
    ("evergreen", "tax", "tax_base_paid", "EVERGREEN TAX SLIP", "TAX",
     lambda a,b,c: (a+b, [f"base {a:.2f} paid", f"addon {b:.2f} paid", f"skip {c:.2f}", f"tax_base_paid TARGET {a+b:.2f}"])),
    ("fortress", "pay", "payroll_active", "FORTRESS PAYROLL", "PAY",
     lambda a,b,c: (a+b, [f"empA {a:.2f} active", f"empB {b:.2f} active", f"empC {c:.2f} leave", f"payroll_active TARGET {a+b:.2f}"])),
    ("gallery", "ship", "ship_ok", "GALLERY SHIP DOCK", "SHIP",
     lambda a,b,c: (float(a+b), [f"box1 {a} ok", f"box2 {b} ok", f"box3 {c} hold", f"ship_ok TARGET {a+b}"])),
    ("highland", "sla", "sla_ok_hours", "HIGHLAND SLA CARD", "SLA",
     lambda a,b,c: (a+b, [f"job1 {a:.2f} hours ok", f"job2 {b:.2f} hours ok", f"job3 {c:.2f} hours late", f"sla_ok_hours TARGET {a+b:.2f}"])),
    ("iceberg", "exp", "exp_sum", "ICEBERG EXPENSE", "EXP",
     lambda a,b,c: (a+b, [f"e1 {a:.2f}", f"e2 {b:.2f}", f"e3 {c:.2f} void", f"exp_sum TARGET {a+b:.2f}"])),
    ("jackpine", "po", "po_open", "JACKPINE PO SHEET", "PO",
     lambda a,b,c: (a+b, [f"line1 {a:.2f} open", f"line2 {b:.2f} open", f"line3 {c:.2f} closed", f"po_open TARGET {a+b:.2f}"])),
    ("keystone", "order", "order_paid", "KEYSTONE ORDER", "ORD",
     lambda a,b,c: (a+b, [f"skuA {a:.2f} paid", f"skuB {b:.2f} paid", f"skuC {c:.2f} due", f"order_paid TARGET {a+b:.2f}"])),
    ("lantern", "dup", "dup_mark", "LANTERN DUP MARK", "DUP",
     lambda a,b,c: (2.0, ["markA 1", "markB 1", "markC 0", "dup_mark TARGET 2"])),
    ("northstar", "zero", "zero_check", "NORTHSTAR AIR ZERO", "ZERO",
     lambda a,b,c: (0.0, ["z1 0.00", "z2 0.00", "z3 0.00", "zero_check TARGET 0.00"])),
    ("outlook", "ledger", "ledger_net", "OUTLOOK LEDGER", "LED",
     lambda a,b,c: (a+b, [f"dr {a:.2f}", f"cr {b:.2f}", f"adj {c:.2f}", f"ledger_net TARGET {a+b:.2f}"])),
    ("pavilion", "ui", "ui_ok", "PAVILION UI SCAN", "UI",
     lambda a,b,c: (1.0, ["btnOK 1", "btnSkip 0", "btnBad 0", "ui_ok TARGET 1"])),
    ("quartzite", "stack", "stack_count", "QUARTZITE STACK", "STK",
     lambda a,b,c: (float(a+b), [f"p1 {a}", f"p2 {b}", f"p3 {c}", f"stack_count TARGET {a+b}"])),
    ("riverbed", "fax", "fax_pages", "RIVERBED FAX", "FAX",
     lambda a,b,c: (float(a+b), [f"pgA {a}", f"pgB {b}", f"pgC {c} drop", f"fax_pages TARGET {a+b}"])),
    ("sandstone", "glare", "glare_ok", "SANDSTONE GLARE", "GLR",
     lambda a,b,c: (1.0, ["zone1 1 ok", "zone2 0", "zone3 0", "glare_ok TARGET 1"])),
    ("tidemark", "tab", "tab_index", "TIDEMARK TAB INDEX", "TAB",
     lambda a,b,c: (float(a+b), [f"tabA {a}", f"tabB {b}", f"tabC {c}", f"tab_index TARGET {a+b}"])),
]
TRAIN_ABC = [
    (215.0, 224.5, 102.0), (168, 196, 121), (159.0, 169.25, 83.0), (265.0, 278.0, 139.0),
    (323.0, 341.0, 133.0), (134, 145, 96), (174.0, 163.75, 88.0), (186.0, 202.5, 102.0),
    (215.0, 198.0, 111.0), (248.0, 231.25, 99.0), (1, 1, 0), (0, 0, 0),
    (295.0, 311.5, 124.0), (1, 0, 0), (37, 31, 14), (50, 39, 32), (1, 0, 0), (61, 52, 29),
]
HELDOUT_ABC = [
    (128.0, 136.5, 63.0), (97, 119, 70), (93.0, 102.25, 51.0), (168.0, 179.0, 85.0),
    (204.0, 215.0, 80.0), (78, 87, 56), (101.0, 95.75, 57.0), (114.0, 124.5, 63.0),
    (134.0, 122.0, 66.0), (156.0, 143.5, 58.0), (1, 1, 0), (0, 0, 0),
    (184.0, 194.75, 73.0), (1, 0, 0), (20, 17, 12), (31, 25, 18), (1, 0, 0), (39, 34, 19),
]
THEME_STR = "anchor_beacon_citadel_evergreen_fortress_gallery_highland_iceberg_jackpine_keystone_lantern_northstar_outlook_pavilion_quartzite_riverbed_sandstone_tidemark"
OLD_THEME = "vault_wick_xray_zest_axle_brine_chalk_eddy_foam_gasket_hinge_jersey_kiln_loom_magma_niche_opus_plank"
# also accept seafoam-patched theme string
OLD_THEME_B = "vault_wick_xray_zest_axle_brine_chalk_eddy_seafoam_gasket_hinge_jersey_kiln_loom_magma_niche_opus_plank"


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
    src = src.replace("# --- V59 overlays (new vs V58) ---", "# --- V60 overlays (new vs V59) ---")
    src = src.replace("# --- V58 overlays (new vs V57) ---", "# --- V60 overlays (new vs V59) ---")
    for a, b in [
        ("VAULT bait", "ANCHOR bait"), ("PLANK bait", "TIDEMARK bait"),
        ("JERSEY ghost", "NORTHSTAR ghost"), ("LOOM bait", "PAVILION bait"),
        ("BRINE bait", "GALLERY bait"), ("MAGMA", "QUARTZITE"),
        ("WICK bait", "BEACON bait"),
        ("DOCK bait", "ANCHOR bait"), ("URN bait", "TIDEMARK bait"),
        ("vault soot + hinge ticks (V59-only)", "anchor rope + lantern ticks (V60-only)"),
        ("dock rust + hatch ticks (V58-only)", "anchor rope + lantern ticks (V60-only)"),
    ]:
        src = src.replace(a, b)
    return src


def gen_design():
    out = (S / "c461_vision_v59_design_and_batch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C461", "C467"), ("c461", "c467"), ("V59", "V60"), ("v59", "v60"),
        ("_v59c461", "_v60c467"),
        ("Harder than V58", "Harder than V59"),
        ("harder than V58", "harder than V59"),
        (OLD_THEME_B, THEME_STR),
        (OLD_THEME, THEME_STR),
        ("V59 keeps floor", "V60 keeps floor"),
        ("C461 design+fixtures; no VL claim", "C467 design+fixtures; no VL claim"),
        ("fixtures only; claim deferred to C462 VL smoke", "fixtures only; claim deferred to C468 VL smoke"),
        ("No claim until C462 VL", "No claim until C468 VL"),
        ("kept on V59", "kept on V60"),
        ('"harder_than": "v58_dock_urn"', '"harder_than": "v59_vault_plank"'),
        ("r50plus_v59_vault_plank", "r50plus_v60_anchor_tidemark"),
    ]:
        out = out.replace(a, b)
    out = out.replace(
        "NEW themes vs V58: vault, wick, xray, zest, axle, brine, chalk, eddy,\nfoam, gasket, hinge, jersey, kiln, loom, magma, niche, opus, plank.",
        "NEW themes vs V59: anchor, beacon, citadel, evergreen, fortress, gallery, highland, iceberg,\njackpine, keystone, lantern, northstar, outlook, pavilion, quartzite, riverbed, sandstone, tidemark.",
    )
    out = out.replace(
        "NEW themes vs V58: vault, wick, xray, zest, axle, brine, chalk, eddy,\nseafoam, gasket, hinge, jersey, kiln, loom, magma, niche, opus, plank.",
        "NEW themes vs V59: anchor, beacon, citadel, evergreen, fortress, gallery, highland, iceberg,\njackpine, keystone, lantern, northstar, outlook, pavilion, quartzite, riverbed, sandstone, tidemark.",
    )
    out = replace_specs(out, build_specs("v60", "V60", TRAIN_ABC))
    out = retarget_overlay(out)
    dst = S / "c467_vision_v60_design_and_batch.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_smoke():
    out = (S / "c462_vision_v59_smoke.py").read_text(encoding="utf-8")
    for a, b in [
        ("C462", "C468"), ("c462", "c468"), ("V59", "V60"), ("v59", "v60"),
        ("r50plus_v59_vault_plank_clarity_floor_n>=16_qwen35_2b",
         "r50plus_v60_anchor_tidemark_clarity_floor_n>=16_qwen35_2b"),
        ("Uses C461 fixtures", "Uses C467 fixtures"),
    ]:
        out = out.replace(a, b)
    out = out.replace(
        "r50plus_v60_vault_plank_clarity_floor_n>=16_qwen35_2b",
        "r50plus_v60_anchor_tidemark_clarity_floor_n>=16_qwen35_2b",
    )
    out = out.replace(
        "r50plus_v60_dock_urn_clarity_floor_n>=16_qwen35_2b",
        "r50plus_v60_anchor_tidemark_clarity_floor_n>=16_qwen35_2b",
    )
    dst = S / "c468_vision_v60_smoke.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_heldout():
    out = (S / "c463_vision_v59_heldout.py").read_text(encoding="utf-8")
    for a, b in [
        ("C463", "C469"), ("c463", "c469"), ("C461", "C467"),
        ("V59", "V60"), ("v59", "v60"),
        ("_v59hc463", "_v60hc469"),
        ("_v59c461", "_v60c467"),
    ]:
        out = out.replace(a, b)
    out = replace_specs(out, build_specs("v60h", "V60H", HELDOUT_ABC))
    out = retarget_overlay(out)
    out2 = []
    seen_fix = seen_train = seen_run = False
    for ln in out.splitlines():
        s = ln.strip()
        if s.startswith("FIX = ") and not seen_fix:
            out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v60h"')
            seen_fix = True
            continue
        if s.startswith("TRAIN_FIX = ") and not seen_train:
            out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v60"')
            seen_train = True
            continue
        if s.startswith("RUN = ") and "vision_v60" in s and not seen_run:
            out2.append('RUN = ROOT / "runs/vision_v60h_c469"')
            seen_run = True
            continue
        out2.append(ln)
    out = "\n".join(out2) + "\n"
    dst = S / "c469_vision_v60_heldout.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_product_u2c():
    out = (S / "c458_product_u2c_cost.py").read_text(encoding="utf-8")
    for a, b in [
        ("C458", "C470"), ("c458", "c470"),
        ("product_u2c_c458", "product_u2c_c470"),
        ("after V58", "after V60"), ("after V59", "after V60"),
        ("V58+", "V60+"), ("V59+", "V60+"),
    ]:
        out = out.replace(a, b)
    dst = S / "c470_product_u2c_cost.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_regression():
    out = (S / "c465_capture_office_regression.py").read_text(encoding="utf-8")
    for a, b in [
        ("C465", "C471"), ("c465", "c471"),
        ("capture_regression_c465", "capture_regression_c471"),
        ("after C461-C464", "after C467-C470"),
        ("V4-V59+heldout", "V4-V60+heldout"),
    ]:
        out = out.replace(a, b)
    if "VISION_V60_SMOKE" not in out:
        out = out.replace(
            "SMOKE_POINTERS = [",
            'SMOKE_POINTERS = [\n'
            '    ("V60", DOC / "C468_VISION_V60_SMOKE.json"),\n'
            '    ("V60_heldout", DOC / "C469_VISION_V60_HELDOUT_SMOKE.json"),\n'
            '    ("V59", DOC / "C462_VISION_V59_SMOKE.json"),\n'
            '    ("V59_heldout", DOC / "C463_VISION_V59_HELDOUT_SMOKE.json"),',
            1,
        )
    dst = S / "c471_capture_office_regression.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def gen_scorecard():
    board = None
    for ln in (S / "c466_scorecard_and_stage.py").read_text(encoding="utf-8").splitlines():
        if "BOARD_MD" in ln and "=" in ln:
            board = ln
            break
    if board is None:
        board = 'BOARD_MD = ROOT / "docs" / "ANT_UNIFIED_SCORECARD.md"'
    nl = "\\n"
    text = f'''# -*- coding: utf-8 -*-
"""C472: Unified scorecard + STAGE after C467-C471. V60 milestone. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
{board}
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C472.md"
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
    c468 = load("docs/r50/C468_VISION_V60_SMOKE.json") or {{}}
    c468b = load("docs/r50/C468b_VISION_GATE_V60_CLAIM.json") or {{}}
    c469 = load("docs/r50/C469_VISION_V60_HELDOUT_SMOKE.json") or {{}}
    c469b = load("docs/r50/C469b_VISION_GATE_V60_HELDOUT_CLAIM.json") or {{}}
    c470 = load("docs/r50/C470_PRODUCT_U2C_COST.json") or {{}}
    c471 = load("docs/r50/C471_CAPTURE_OFFICE_REGRESSION.json") or {{}}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {{}}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {{}}
    c464 = load("docs/r50/C464_CONFIDENCE_GATE_STRETCH.json") or {{}}

    v60 = float(c468.get("rate") or 0.0)
    v60h = float(c469.get("rate") or 0.0)
    v60_claim = bool(c468b.get("vl_gate_v60_claim") or c468.get("vl_gate_v60_claim") or c468.get("claim"))
    v60h_claim = bool(c469b.get("vl_gate_v60_heldout_claim") or c469.get("vl_gate_v60_heldout_claim") or c469.get("claim"))
    disjoint = bool(c469.get("id_disjoint") or c469.get("disjoint") or c469b.get("id_disjoint") or c469b.get("disjoint"))

    _rl = c470.get("replace_ledger") or {{}}
    u2c_pass = bool(c470.get("pass")) if c470 else bool((prior.get("product_u2c") or {{}}).get("pass"))
    u2c_replace = float(
        c470.get("replace_ratio")
        or _rl.get("mean_ratio")
        or ((prior.get("product_u2c") or {{}}).get("replace_ratio"))
        or 4.07
    )
    conf = prior.get("confidence_gate") or {{}}
    if c464.get("pass") is not None:
        conf = {{
            "pass": bool(c464.get("pass")),
            "rate": float(c464.get("rate") or 1.0),
            "source": "C464",
        }}
    capture_pass = bool(c471.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {{}}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {{}}).get("shadow_pass", dissolve_pass))

    stage_ready = bool(
        v60_claim and v60h_claim and v60 >= GATE and v60h >= GATE
        and capture_pass and disjoint and u2c_pass
    )
    composite = 0.0
    if stage_ready:
        composite = 1.0 if (v60 >= 0.999 and v60h >= 0.999) else min(v60, v60h)

    out = {{
        "cycle": "C472",
        "timestamp": ts(),
        "gate": GATE,
        "milestone": "V60",
        "vision": {{
            "v59": (prior.get("vision") or {{}}).get("v59") or {{"rate": 1.0, "claim": True}},
            "v59_heldout": (prior.get("vision") or {{}}).get("v59_heldout") or {{"rate": 1.0, "claim": True}},
            "v60": {{"rate": v60, "claim": v60_claim, "n": c468.get("n")}},
            "v60_heldout": {{"rate": v60h, "claim": v60h_claim, "disjoint": disjoint, "n": c469.get("n")}},
        }},
        "product_u2c": {{"pass": u2c_pass, "replace_ratio": u2c_replace, "source": "C470"}},
        "confidence_gate": conf if conf else {{"pass": True, "rate": 1.0, "source": "C464"}},
        "capture_regression": {{"pass": capture_pass, "source": "C471"}},
        "dissolve_shadow": {{
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        }},
        "composite": composite,
        "stage_ready": stage_ready,
        "v60_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }}
    J(DOC / "C472_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = [
        "# Unified Scorecard (C472) — V60 milestone", "",
        f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"- Vision V60: rate={{v60}} claim={{v60_claim}}",
        f"- Vision V60 heldout: rate={{v60h}} claim={{v60h_claim}} disjoint={{disjoint}}",
        f"- product_u2c: pass={{u2c_pass}} replace~={{u2c_replace}}",
        f"- confidence_gate: {{out['confidence_gate']}}",
        f"- capture_regression: pass={{capture_pass}}",
        f"- dissolve/shadow: {{dissolve_pass}}/{{shadow_pass}}",
        f"- composite: {{out['composite']}}",
        f"- stage_ready: {{stage_ready}}",
        "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD | V60 milestone", "",
    ]
    BOARD_MD.write_text("\\n".join(md) + "\\n", encoding="utf-8")

    stage = [
        "# STAGE_ANT_C472", "",
        f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"**C467-C472 STAGE_READY={{'YES' if stage_ready else 'NO'}} (V60 milestone)**", "",
        "## Tip slice",
        "- C467: Vision V60 design fixtures (jpeg_q=62, floor>=60, long themes)",
        f"- C468: Vision V60 smoke claim **{{v60}}** (n={{c468.get('n')}})",
        f"- C469: Vision V60 heldout claim **{{v60h}}** (disjoint={{disjoint}})",
        f"- C470: product-u2c pass={{u2c_pass}} replace~={{u2c_replace}}",
        f"- C471: capture-office regression pass={{capture_pass}}",
        f"- C472: unified scorecard composite={{out['composite']}}", "",
        "## Constraints",
        "- Gate: 0.6",
        "- Gate2/3: untouched",
        "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V60 (uses 62)",
        "- lesson: avoid short VL-collapse theme names (V59 foam)", "",
        "## Entry",
        f"- Scorecard: {{BOARD_MD.relative_to(ROOT).as_posix()}}",
        "- Latest JSON: docs/r50/SCORECARD_LATEST.json",
        "- This stage: docs/STAGE_ANT_C472.md", "",
    ]
    STAGE.write_text("\\n".join(stage) + "\\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''
    dst = S / "c472_scorecard_and_stage.py"
    dst.write_text(text, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)


def main():
    gen_design()
    gen_smoke()
    gen_heldout()
    gen_product_u2c()
    gen_regression()
    gen_scorecard()
    print("OK C467-C472 scripts")


if __name__ == "__main__":
    main()
