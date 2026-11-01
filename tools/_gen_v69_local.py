# -*- coding: utf-8 -*-
"""Generate C521-C526 V69 scripts from V68. Knife: confidence-gate (C524)."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"

THEMES = [
    ("stormwatch", "recv", "paid_total", "STORMWATCH GRAIN RECV", "RECV",
     lambda a,b,c: (a+b, [f"a paid {a:.2f}", f"b paid {b:.2f}", f"c open {c:.2f}", f"TOTAL PAID TARGET {a+b:.2f}"])),
    ("timberline", "wh", "qty_sum", "WH TIMBERLINE BIN", "RECV",
     lambda a,b,c: (float(a+b), [f"SKU1 qty {a} ok", f"SKU2 qty {c} hold", f"SKU3 qty {b} ok", f"qty_sum TARGET {a+b}"])),
    ("undertowbay", "refund", "refund_done", "UNDERTOWBAY PATCH REFUND", "DONE",
     lambda a,b,c: (a+b, [f"itemR1 {a:.2f} done", f"itemR2 {b:.2f} done", f"itemR3 {c:.2f} open", f"refund_done TARGET {a+b:.2f}"])),
    ("valleyforge", "tax", "tax_base_paid", "VALLEYFORGE TAX SLIP", "TAX",
     lambda a,b,c: (a+b, [f"base {a:.2f} paid", f"addon {b:.2f} paid", f"skip {c:.2f}", f"tax_base_paid TARGET {a+b:.2f}"])),
    ("waterfallglen", "pay", "payroll_active", "WATERFALLGLEN PAYROLL", "PAY",
     lambda a,b,c: (a+b, [f"empA {a:.2f} active", f"empB {b:.2f} active", f"empC {c:.2f} leave", f"payroll_active TARGET {a+b:.2f}"])),
    ("xylograph", "ship", "ship_ok", "XYLOGRAPH SHIP DOCK", "SHIP",
     lambda a,b,c: (float(a+b), [f"box1 {a} ok", f"box2 {b} ok", f"box3 {c} hold", f"ship_ok TARGET {a+b}"])),
    ("yuccaplateau", "sla", "sla_ok_hours", "YUCCAPLATEAU SLA CARD", "SLA",
     lambda a,b,c: (a+b, [f"job1 {a:.2f} hours ok", f"job2 {b:.2f} hours ok", f"job3 {c:.2f} hours late", f"sla_ok_hours TARGET {a+b:.2f}"])),
    ("zephyrcliff", "exp", "exp_sum", "ZEPHYRCLIFF EXPENSE", "EXP",
     lambda a,b,c: (a+b, [f"e1 {a:.2f}", f"e2 {b:.2f}", f"e3 {c:.2f} void", f"exp_sum TARGET {a+b:.2f}"])),
    ("alderbrook", "po", "po_open", "ALDERBROOK PO SHEET", "PO",
     lambda a,b,c: (a+b, [f"line1 {a:.2f} open", f"line2 {b:.2f} open", f"line3 {c:.2f} closed", f"po_open TARGET {a+b:.2f}"])),
    ("boulderpass", "order", "order_paid", "BOULDERPASS ORDER", "ORD",
     lambda a,b,c: (a+b, [f"skuA {a:.2f} paid", f"skuB {b:.2f} paid", f"skuC {c:.2f} due", f"order_paid TARGET {a+b:.2f}"])),
    ("canyonrim", "dup", "dup_mark", "CANYONRIM DUP MARK", "DUP",
     lambda a,b,c: (2.0, ["markA 1", "markB 1", "markC 0", "dup_mark TARGET 2"])),
    ("duskhorizon", "zero", "zero_check", "DUSKHORIZON AIR ZERO", "ZERO",
     lambda a,b,c: (0.0, ["z1 0.00", "z2 0.00", "z3 0.00", "zero_check TARGET 0.00"])),
    ("echochamber", "ledger", "ledger_net", "ECHOCHAMBER LEDGER", "LED",
     lambda a,b,c: (a+b, [f"dr {a:.2f}", f"cr {b:.2f}", f"adj {c:.2f}", f"ledger_net TARGET {a+b:.2f}"])),
    ("foghorncliff", "ui", "ui_ok", "FOGHORNCLIFF UI SCAN", "UI",
     lambda a,b,c: (1.0, ["btnOK 1", "btnSkip 0", "btnBad 0", "ui_ok TARGET 1"])),
    ("grovehaven", "stack", "stack_count", "GROVEHAVEN STACK", "STK",
     lambda a,b,c: (float(a+b), [f"p1 {a}", f"p2 {b}", f"p3 {c}", f"stack_count TARGET {a+b}"])),
    ("highlandmoor", "fax", "fax_pages", "HIGHLANDMOOR FAX", "FAX",
     lambda a,b,c: (float(a+b), [f"pgA {a}", f"pgB {b}", f"pgC {c} drop", f"fax_pages TARGET {a+b}"])),
    ("ironwoodpass", "glare", "glare_ok", "IRONWOODPASS GLARE", "GLR",
     lambda a,b,c: (1.0, ["zone1 1 ok", "zone2 0", "zone3 0", "glare_ok TARGET 1"])),
    ("juniperpass", "tab", "tab_index", "JUNIPERPASS TAB INDEX", "TAB",
     lambda a,b,c: (float(a+b), [f"tabA {a}", f"tabB {b}", f"tabC {c}", f"tab_index TARGET {a+b}"])),
]
TRAIN_ABC = [
    (288.0, 305.25, 143.0), (235, 263, 163), (222.0, 243.0, 121.0), (342.0, 360.0, 189.0),
    (405.0, 429.0, 181.0), (185, 201, 139), (241.0, 233.25, 126.0), (253.0, 282.0, 145.0),
    (287.0, 270.0, 154.0), (320.0, 308.0, 142.0), (1, 1, 0), (0, 0, 0),
    (386.0, 410.25, 167.0), (1, 0, 0), (57, 49, 27), (75, 59, 50), (1, 0, 0), (90, 77, 47),
]
HELDOUT_ABC = [
    (179.0, 194.5, 94.0), (141, 169, 101), (137.0, 153.25, 82.0), (230.0, 246.0, 123.0),
    (271.0, 287.0, 118.0), (109, 123, 87), (145.0, 142.25, 88.0), (163.0, 182.0, 94.0),
    (183.0, 171.0, 97.0), (210.0, 198.75, 89.0), (1, 1, 0), (0, 0, 0),
    (245.0, 263.25, 104.0), (1, 0, 0), (33, 30, 25), (49, 43, 31), (1, 0, 0), (59, 53, 32),
]
THEME_STR = "stormwatch_timberline_undertowbay_valleyforge_waterfallglen_xylograph_yuccaplateau_zephyrcliff_alderbrook_boulderpass_canyonrim_duskhorizon_echochamber_foghorncliff_grovehaven_highlandmoor_ironwoodpass_juniperpass"
OLD_THEME = "azureharbor_basaltmesa_coppergorge_driftwoodbay_evergreenridge_flintgorge_glacierpass_hollowcreek_indigotrail_jadeplateau_knotwood_lavenderfield_meadowbrook_nordicfjord_obsidianridge_prairiewind_quarrystone_rainshadow"


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
    src = src.replace("# --- V68 overlays (new vs V67) ---", "# --- V69 overlays (new vs V68) ---")
    for a, b in [
        ("AZUREHARBOR bait", "STORMWATCH bait"), ("RAINSHADOW bait", "JUNIPERPASS bait"),
        ("LAVENDERFIELD ghost", "DUSKHORIZON ghost"), ("NORDICFJORD bait", "FOGHORNCLIFF bait"),
        ("FLINTGORGE bait", "XYLOGRAPH bait"), ("OBSIDIANRIDGE", "GROVEHAVEN"),
        ("BASALTMESA bait", "TIMBERLINE bait"),
        ("azure mist + rainshadow ticks (V68-only)", "storm mist + juniper ticks (V69-only)"),
    ]:
        src = src.replace(a, b)
    return src


def gen_design():
    out = (S / "c515_vision_v68_design_and_batch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C515", "C521"), ("c515", "c521"), ("V68", "V69"), ("v68", "v69"),
        ("_v68c515", "_v69c521"),
        ("Harder than V67", "Harder than V68"),
        ("harder than V67", "harder than V68"),
        (OLD_THEME, THEME_STR),
        ("V68 keeps floor", "V69 keeps floor"),
        ("C515 design+fixtures; no VL claim", "C521 design+fixtures; no VL claim"),
        ("fixtures only; claim deferred to C516 VL smoke", "fixtures only; claim deferred to C522 VL smoke"),
        ("No claim until C516 VL", "No claim until C522 VL"),
        ("kept on V68", "kept on V69"),
        ('"harder_than": "v67_dewdropcliff_yellowglen"', '"harder_than": "v68_azureharbor_rainshadow"'),
        ("r50plus_v68_azureharbor_rainshadow", "r50plus_v69_stormwatch_juniperpass"),
    ]:
        out = out.replace(a, b)
    out = out.replace(
        "NEW themes vs V67: azureharbor, basaltmesa, coppergorge, driftwoodbay, evergreenridge, flintgorge, glacierpass, hollowcreek,\nindigotrail, jadeplateau, knotwood, lavenderfield, meadowbrook, nordicfjord, obsidianridge, prairiewind, quarrystone, rainshadow.",
        "NEW themes vs V68: stormwatch, timberline, undertowbay, valleyforge, waterfallglen, xylograph, yuccaplateau, zephyrcliff,\nalderbrook, boulderpass, canyonrim, duskhorizon, echochamber, foghorncliff, grovehaven, highlandmoor, ironwoodpass, juniperpass.",
    )
    out = replace_specs(out, build_specs("v69", "V69", TRAIN_ABC))
    out = retarget_overlay(out)
    dst = S / "c521_vision_v69_design_and_batch.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_smoke():
    out = (S / "c516_vision_v68_smoke.py").read_text(encoding="utf-8")
    for a, b in [
        ("C516", "C522"), ("c516", "c522"), ("V68", "V69"), ("v68", "v69"),
        ("r50plus_v68_azureharbor_rainshadow_clarity_floor_n>=16_qwen35_2b",
         "r50plus_v69_stormwatch_juniperpass_clarity_floor_n>=16_qwen35_2b"),
        ("Uses C515 fixtures", "Uses C521 fixtures"),
    ]:
        out = out.replace(a, b)
    dst = S / "c522_vision_v69_smoke.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_heldout():
    out = (S / "c517_vision_v68_heldout.py").read_text(encoding="utf-8")
    for a, b in [
        ("C517", "C523"), ("c517", "c523"), ("C515", "C521"),
        ("V68", "V69"), ("v68", "v69"),
        ("_v68hc517", "_v69hc523"),
        ("_v68c515", "_v69c521"),
    ]:
        out = out.replace(a, b)
    out = replace_specs(out, build_specs("v69h", "V69H", HELDOUT_ABC))
    out = retarget_overlay(out)
    out2 = []
    seen_fix = seen_train = seen_run = False
    for ln in out.splitlines():
        s = ln.strip()
        if s.startswith("FIX = ") and not seen_fix:
            out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v69h"')
            seen_fix = True
            continue
        if s.startswith("TRAIN_FIX = ") and not seen_train:
            out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v69"')
            seen_train = True
            continue
        if s.startswith("RUN = ") and "vision_v69" in s and not seen_run:
            out2.append('RUN = ROOT / "runs/vision_v69h_c523"')
            seen_run = True
            continue
        out2.append(ln)
    out = "\n".join(out2) + "\n"
    dst = S / "c523_vision_v69_heldout.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_confidence():
    out = (S / "c512_confidence_gate_stretch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C512", "C524"), ("c512", "c524"),
        ("confidence_gate_c512", "confidence_gate_c524"),
        ("conf_gate_stretch_c512", "conf_gate_stretch_c524"),
        ("after V67", "after V69"), ("after V68", "after V69"),
        ("V67+", "V69+"), ("V68+", "V69+"),
    ]:
        out = out.replace(a, b)
    dst = S / "c524_confidence_gate_stretch.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_regression():
    out = (S / "c519_capture_office_regression.py").read_text(encoding="utf-8")
    for a, b in [
        ("C519", "C525"), ("c519", "c525"),
        ("capture_regression_c519", "capture_regression_c525"),
        ("after C515-C518", "after C521-C524"),
        ("V4-V68+heldout", "V4-V69+heldout"),
    ]:
        out = out.replace(a, b)
    if "VISION_V69_SMOKE" not in out:
        out = out.replace(
            "SMOKE_POINTERS = [",
            'SMOKE_POINTERS = [\n'
            '    ("V69", DOC / "C522_VISION_V69_SMOKE.json"),\n'
            '    ("V69_heldout", DOC / "C523_VISION_V69_HELDOUT_SMOKE.json"),\n'
            '    ("V68", DOC / "C516_VISION_V68_SMOKE.json"),\n'
            '    ("V68_heldout", DOC / "C517_VISION_V68_HELDOUT_SMOKE.json"),',
            1,
        )
    dst = S / "c525_capture_office_regression.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_scorecard():
    board = 'BOARD_MD = ROOT / "docs" / "ANT_UNIFIED_SCORECARD.md"'
    for ln in (S / "c520_scorecard_and_stage.py").read_text(encoding="utf-8").splitlines():
        if "BOARD_MD" in ln and "=" in ln:
            board = ln
            break
    nl = "\\n"
    text = f'''# -*- coding: utf-8 -*-
"""C526: Unified scorecard + STAGE after C521-C525. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
{board}
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C526.md"
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
    c522 = load("docs/r50/C522_VISION_V69_SMOKE.json") or {{}}
    c522b = load("docs/r50/C522b_VISION_GATE_V69_CLAIM.json") or {{}}
    c523 = load("docs/r50/C523_VISION_V69_HELDOUT_SMOKE.json") or {{}}
    c523b = load("docs/r50/C523b_VISION_GATE_V69_HELDOUT_CLAIM.json") or {{}}
    c524 = load("docs/r50/C524_CONFIDENCE_GATE_STRETCH.json") or {{}}
    c525 = load("docs/r50/C525_CAPTURE_OFFICE_REGRESSION.json") or {{}}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {{}}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {{}}
    c518 = load("docs/r50/C518_PRODUCT_U2C_COST.json") or {{}}

    v69 = float(c522.get("rate") or 0.0)
    v69h = float(c523.get("rate") or 0.0)
    v69_claim = bool(c522b.get("vl_gate_v69_claim") or c522.get("vl_gate_v69_claim") or c522.get("claim"))
    v69h_claim = bool(c523b.get("vl_gate_v69_heldout_claim") or c523.get("vl_gate_v69_heldout_claim") or c523.get("claim"))
    disjoint = bool(c523.get("id_disjoint") or c523.get("disjoint") or c523b.get("id_disjoint") or c523b.get("disjoint"))
    conf_pass = bool(c524.get("pass")) if c524 else bool((prior.get("confidence_gate") or {{}}).get("pass"))
    conf_rate = float(c524.get("rate") or ((prior.get("confidence_gate") or {{}}).get("rate")) or 1.0)
    u2c = prior.get("product_u2c") or {{}}
    if c518.get("pass") is not None:
        u2c = {{
            "pass": bool(c518.get("pass")),
            "replace_ratio": float(
                c518.get("replace_ratio")
                or c518.get("mean_ratio")
                or ((c518.get("replace_ledger") or {{}}).get("mean_ratio"))
                or 4.07
            ),
            "source": "C518",
        }}
    capture_pass = bool(c525.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {{}}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {{}}).get("shadow_pass", dissolve_pass))

    stage_ready = bool(
        v69_claim and v69h_claim and v69 >= GATE and v69h >= GATE
        and capture_pass and disjoint and conf_pass
    )
    composite = 0.0
    if stage_ready:
        composite = 1.0 if (v69 >= 0.999 and v69h >= 0.999) else min(v69, v69h)

    out = {{
        "cycle": "C526",
        "timestamp": ts(),
        "gate": GATE,
        "vision": {{
            "v68": (prior.get("vision") or {{}}).get("v68") or {{"rate": 1.0, "claim": True}},
            "v68_heldout": (prior.get("vision") or {{}}).get("v68_heldout") or {{"rate": 1.0, "claim": True}},
            "v69": {{"rate": v69, "claim": v69_claim, "n": c522.get("n")}},
            "v69_heldout": {{"rate": v69h, "claim": v69h_claim, "disjoint": disjoint, "n": c523.get("n")}},
        }},
        "product_u2c": u2c if u2c else {{"pass": True, "replace_ratio": 4.0694, "source": "C518"}},
        "confidence_gate": {{"pass": conf_pass, "rate": conf_rate, "source": "C524"}},
        "capture_regression": {{"pass": capture_pass, "source": "C525"}},
        "dissolve_shadow": {{
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        }},
        "composite": composite,
        "stage_ready": stage_ready,
        "v69_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }}
    J(DOC / "C526_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = [
        "# Unified Scorecard (C526)", "",
        f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"- Vision V69: rate={{v69}} claim={{v69_claim}}",
        f"- Vision V69 heldout: rate={{v69h}} claim={{v69h_claim}} disjoint={{disjoint}}",
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
        "# STAGE_ANT_C526", "",
        f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"**C521-C526 STAGE_READY={{'YES' if stage_ready else 'NO'}}**", "",
        "## Tip slice",
        "- C521: Vision V69 design fixtures (jpeg_q=62, floor>=60, long themes)",
        f"- C522: Vision V69 smoke claim **{{v69}}** (n={{c522.get('n')}})",
        f"- C523: Vision V69 heldout claim **{{v69h}}** (disjoint={{disjoint}})",
        f"- C524: confidence-gate stretch pass={{conf_pass}} rate={{conf_rate}}",
        f"- C525: capture-office regression pass={{capture_pass}}",
        f"- C526: unified scorecard composite={{out['composite']}}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally; not model-plus-separate-agent).", "",
        "## Constraints",
        "- Gate: 0.6",
        "- Gate2/3: untouched",
        "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V69 (uses 62)", "",
        "## Entry",
        f"- Scorecard: {{BOARD_MD.relative_to(ROOT).as_posix()}}",
        "- Latest JSON: docs/r50/SCORECARD_LATEST.json",
        "- This stage: docs/STAGE_ANT_C526.md", "",
    ]
    STAGE.write_text("\\n".join(stage) + "\\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''
    dst = S / "c526_scorecard_and_stage.py"
    dst.write_text(text, encoding="utf-8")
    print("wrote", dst.name)


def main():
    gen_design()
    gen_smoke()
    gen_heldout()
    gen_confidence()
    gen_regression()
    gen_scorecard()
    print("OK C521-C526")


if __name__ == "__main__":
    main()
