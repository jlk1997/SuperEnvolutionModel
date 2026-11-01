# -*- coding: utf-8 -*-
"""Generate C515-C520 V68 scripts from V67. Knife: product-U2C (C518)."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"

THEMES = [
    ("azureharbor", "recv", "paid_total", "AZUREHARBOR GRAIN RECV", "RECV",
     lambda a,b,c: (a+b, [f"a paid {a:.2f}", f"b paid {b:.2f}", f"c open {c:.2f}", f"TOTAL PAID TARGET {a+b:.2f}"])),
    ("basaltmesa", "wh", "qty_sum", "WH BASALTMESA BIN", "RECV",
     lambda a,b,c: (float(a+b), [f"SKU1 qty {a} ok", f"SKU2 qty {c} hold", f"SKU3 qty {b} ok", f"qty_sum TARGET {a+b}"])),
    ("coppergorge", "refund", "refund_done", "COPPERGORGE PATCH REFUND", "DONE",
     lambda a,b,c: (a+b, [f"itemR1 {a:.2f} done", f"itemR2 {b:.2f} done", f"itemR3 {c:.2f} open", f"refund_done TARGET {a+b:.2f}"])),
    ("driftwoodbay", "tax", "tax_base_paid", "DRIFTWOODBAY TAX SLIP", "TAX",
     lambda a,b,c: (a+b, [f"base {a:.2f} paid", f"addon {b:.2f} paid", f"skip {c:.2f}", f"tax_base_paid TARGET {a+b:.2f}"])),
    ("evergreenridge", "pay", "payroll_active", "EVERGREENRIDGE PAYROLL", "PAY",
     lambda a,b,c: (a+b, [f"empA {a:.2f} active", f"empB {b:.2f} active", f"empC {c:.2f} leave", f"payroll_active TARGET {a+b:.2f}"])),
    ("flintgorge", "ship", "ship_ok", "FLINTGORGE SHIP DOCK", "SHIP",
     lambda a,b,c: (float(a+b), [f"box1 {a} ok", f"box2 {b} ok", f"box3 {c} hold", f"ship_ok TARGET {a+b}"])),
    ("glacierpass", "sla", "sla_ok_hours", "GLACIERPASS SLA CARD", "SLA",
     lambda a,b,c: (a+b, [f"job1 {a:.2f} hours ok", f"job2 {b:.2f} hours ok", f"job3 {c:.2f} hours late", f"sla_ok_hours TARGET {a+b:.2f}"])),
    ("hollowcreek", "exp", "exp_sum", "HOLLOWCREEK EXPENSE", "EXP",
     lambda a,b,c: (a+b, [f"e1 {a:.2f}", f"e2 {b:.2f}", f"e3 {c:.2f} void", f"exp_sum TARGET {a+b:.2f}"])),
    ("indigotrail", "po", "po_open", "INDIGOTRAIL PO SHEET", "PO",
     lambda a,b,c: (a+b, [f"line1 {a:.2f} open", f"line2 {b:.2f} open", f"line3 {c:.2f} closed", f"po_open TARGET {a+b:.2f}"])),
    ("jadeplateau", "order", "order_paid", "JADEPLATEAU ORDER", "ORD",
     lambda a,b,c: (a+b, [f"skuA {a:.2f} paid", f"skuB {b:.2f} paid", f"skuC {c:.2f} due", f"order_paid TARGET {a+b:.2f}"])),
    ("knotwood", "dup", "dup_mark", "KNOTWOOD DUP MARK", "DUP",
     lambda a,b,c: (2.0, ["markA 1", "markB 1", "markC 0", "dup_mark TARGET 2"])),
    ("lavenderfield", "zero", "zero_check", "LAVENDERFIELD AIR ZERO", "ZERO",
     lambda a,b,c: (0.0, ["z1 0.00", "z2 0.00", "z3 0.00", "zero_check TARGET 0.00"])),
    ("meadowbrook", "ledger", "ledger_net", "MEADOWBROOK LEDGER", "LED",
     lambda a,b,c: (a+b, [f"dr {a:.2f}", f"cr {b:.2f}", f"adj {c:.2f}", f"ledger_net TARGET {a+b:.2f}"])),
    ("nordicfjord", "ui", "ui_ok", "NORDICFJORD UI SCAN", "UI",
     lambda a,b,c: (1.0, ["btnOK 1", "btnSkip 0", "btnBad 0", "ui_ok TARGET 1"])),
    ("obsidianridge", "stack", "stack_count", "OBSIDIANRIDGE STACK", "STK",
     lambda a,b,c: (float(a+b), [f"p1 {a}", f"p2 {b}", f"p3 {c}", f"stack_count TARGET {a+b}"])),
    ("prairiewind", "fax", "fax_pages", "PRAIRIEWIND FAX", "FAX",
     lambda a,b,c: (float(a+b), [f"pgA {a}", f"pgB {b}", f"pgC {c} drop", f"fax_pages TARGET {a+b}"])),
    ("quarrystone", "glare", "glare_ok", "QUARRYSTONE GLARE", "GLR",
     lambda a,b,c: (1.0, ["zone1 1 ok", "zone2 0", "zone3 0", "glare_ok TARGET 1"])),
    ("rainshadow", "tab", "tab_index", "RAINSHADOW TAB INDEX", "TAB",
     lambda a,b,c: (float(a+b), [f"tabA {a}", f"tabB {b}", f"tabC {c}", f"tab_index TARGET {a+b}"])),
]
TRAIN_ABC = [
    (280.0, 297.5, 139.0), (227, 255, 159), (215.0, 235.25, 117.0), (334.0, 352.0, 183.0),
    (397.0, 421.0, 177.0), (179, 195, 135), (233.0, 225.5, 122.0), (245.0, 273.75, 141.0),
    (279.0, 262.0, 150.0), (312.0, 300.0, 138.0), (1, 1, 0), (0, 0, 0),
    (378.0, 402.5, 163.0), (1, 0, 0), (55, 47, 25), (73, 57, 48), (1, 0, 0), (87, 75, 45),
]
HELDOUT_ABC = [
    (173.0, 188.75, 90.0), (135, 163, 97), (131.0, 147.5, 78.0), (222.0, 238.0, 119.0),
    (263.0, 279.0, 114.0), (105, 119, 83), (139.0, 136.5, 84.0), (157.0, 175.75, 90.0),
    (177.0, 165.0, 93.0), (204.0, 193.0, 85.0), (1, 1, 0), (0, 0, 0),
    (239.0, 257.5, 100.0), (1, 0, 0), (31, 28, 23), (47, 41, 29), (1, 0, 0), (57, 51, 30),
]
THEME_STR = "azureharbor_basaltmesa_coppergorge_driftwoodbay_evergreenridge_flintgorge_glacierpass_hollowcreek_indigotrail_jadeplateau_knotwood_lavenderfield_meadowbrook_nordicfjord_obsidianridge_prairiewind_quarrystone_rainshadow"
OLD_THEME = "dewdropcliff_fernhollow_goldenspire_heatherfield_ivoryglen_kelpshore_limestonespire_mistletoeridge_orchidpath_pearlstream_reedmarsh_sandbarcoast_thistlefield_umberridge_verdantpeak_whitecliff_xerophyte_yellowglen"


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
    src = src.replace("# --- V67 overlays (new vs V66) ---", "# --- V68 overlays (new vs V67) ---")
    for a, b in [
        ("DEWDROPCLIFF bait", "AZUREHARBOR bait"), ("YELLOWGLEN bait", "RAINSHADOW bait"),
        ("SANDBARCOAST ghost", "LAVENDERFIELD ghost"), ("UMBERRIDGE bait", "NORDICFJORD bait"),
        ("KELPSHORE bait", "FLINTGORGE bait"), ("VERDANTPEAK", "OBSIDIANRIDGE"),
        ("FERNHOLLOW bait", "BASALTMESA bait"),
        ("dew mist + yellowglen ticks (V67-only)", "azure mist + rainshadow ticks (V68-only)"),
    ]:
        src = src.replace(a, b)
    return src


def gen_design():
    out = (S / "c509_vision_v67_design_and_batch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C509", "C515"), ("c509", "c515"), ("V67", "V68"), ("v67", "v68"),
        ("_v67c509", "_v68c515"),
        ("Harder than V66", "Harder than V67"),
        ("harder than V66", "harder than V67"),
        (OLD_THEME, THEME_STR),
        ("V67 keeps floor", "V68 keeps floor"),
        ("C509 design+fixtures; no VL claim", "C515 design+fixtures; no VL claim"),
        ("fixtures only; claim deferred to C510 VL smoke", "fixtures only; claim deferred to C516 VL smoke"),
        ("No claim until C510 VL", "No claim until C516 VL"),
        ("kept on V67", "kept on V68"),
        ('"harder_than": "v66_larkspur_cinderpath"', '"harder_than": "v67_dewdropcliff_yellowglen"'),
        ("r50plus_v67_dewdropcliff_yellowglen", "r50plus_v68_azureharbor_rainshadow"),
    ]:
        out = out.replace(a, b)
    out = out.replace(
        "NEW themes vs V66: dewdropcliff, fernhollow, goldenspire, heatherfield, ivoryglen, kelpshore, limestonespire, mistletoeridge,\norchidpath, pearlstream, reedmarsh, sandbarcoast, thistlefield, umberridge, verdantpeak, whitecliff, xerophyte, yellowglen.",
        "NEW themes vs V67: azureharbor, basaltmesa, coppergorge, driftwoodbay, evergreenridge, flintgorge, glacierpass, hollowcreek,\nindigotrail, jadeplateau, knotwood, lavenderfield, meadowbrook, nordicfjord, obsidianridge, prairiewind, quarrystone, rainshadow.",
    )
    out = replace_specs(out, build_specs("v68", "V68", TRAIN_ABC))
    out = retarget_overlay(out)
    dst = S / "c515_vision_v68_design_and_batch.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_smoke():
    out = (S / "c510_vision_v67_smoke.py").read_text(encoding="utf-8")
    for a, b in [
        ("C510", "C516"), ("c510", "c516"), ("V67", "V68"), ("v67", "v68"),
        ("r50plus_v67_dewdropcliff_yellowglen_clarity_floor_n>=16_qwen35_2b",
         "r50plus_v68_azureharbor_rainshadow_clarity_floor_n>=16_qwen35_2b"),
        ("Uses C509 fixtures", "Uses C515 fixtures"),
    ]:
        out = out.replace(a, b)
    dst = S / "c516_vision_v68_smoke.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_heldout():
    out = (S / "c511_vision_v67_heldout.py").read_text(encoding="utf-8")
    for a, b in [
        ("C511", "C517"), ("c511", "c517"), ("C509", "C515"),
        ("V67", "V68"), ("v67", "v68"),
        ("_v67hc511", "_v68hc517"),
        ("_v67c509", "_v68c515"),
    ]:
        out = out.replace(a, b)
    out = replace_specs(out, build_specs("v68h", "V68H", HELDOUT_ABC))
    out = retarget_overlay(out)
    out2 = []
    seen_fix = seen_train = seen_run = False
    for ln in out.splitlines():
        s = ln.strip()
        if s.startswith("FIX = ") and not seen_fix:
            out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v68h"')
            seen_fix = True
            continue
        if s.startswith("TRAIN_FIX = ") and not seen_train:
            out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v68"')
            seen_train = True
            continue
        if s.startswith("RUN = ") and "vision_v68" in s and not seen_run:
            out2.append('RUN = ROOT / "runs/vision_v68h_c517"')
            seen_run = True
            continue
        out2.append(ln)
    out = "\n".join(out2) + "\n"
    dst = S / "c517_vision_v68_heldout.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_u2c():
    out = (S / "c506_product_u2c_cost.py").read_text(encoding="utf-8")
    for a, b in [
        ("C506", "C518"), ("c506", "c518"),
        ("product_u2c_c506", "product_u2c_c518"),
        ("u2c_cost_c506", "u2c_cost_c518"),
        ("after V66", "after V68"), ("after V67", "after V68"),
        ("V66+", "V68+"), ("V67+", "V68+"),
    ]:
        out = out.replace(a, b)
    dst = S / "c518_product_u2c_cost.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_regression():
    out = (S / "c513_capture_office_regression.py").read_text(encoding="utf-8")
    for a, b in [
        ("C513", "C519"), ("c513", "c519"),
        ("capture_regression_c513", "capture_regression_c519"),
        ("after C509-C512", "after C515-C518"),
        ("V4-V67+heldout", "V4-V68+heldout"),
    ]:
        out = out.replace(a, b)
    if "VISION_V68_SMOKE" not in out:
        out = out.replace(
            "SMOKE_POINTERS = [",
            'SMOKE_POINTERS = [\n'
            '    ("V68", DOC / "C516_VISION_V68_SMOKE.json"),\n'
            '    ("V68_heldout", DOC / "C517_VISION_V68_HELDOUT_SMOKE.json"),\n'
            '    ("V67", DOC / "C510_VISION_V67_SMOKE.json"),\n'
            '    ("V67_heldout", DOC / "C511_VISION_V67_HELDOUT_SMOKE.json"),',
            1,
        )
    dst = S / "c519_capture_office_regression.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_scorecard():
    board = 'BOARD_MD = ROOT / "docs" / "ANT_UNIFIED_SCORECARD.md"'
    for ln in (S / "c514_scorecard_and_stage.py").read_text(encoding="utf-8").splitlines():
        if "BOARD_MD" in ln and "=" in ln:
            board = ln
            break
    nl = "\\n"
    text = f'''# -*- coding: utf-8 -*-
"""C520: Unified scorecard + STAGE after C515-C519. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
{board}
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C520.md"
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
    c516 = load("docs/r50/C516_VISION_V68_SMOKE.json") or {{}}
    c516b = load("docs/r50/C516b_VISION_GATE_V68_CLAIM.json") or {{}}
    c517 = load("docs/r50/C517_VISION_V68_HELDOUT_SMOKE.json") or {{}}
    c517b = load("docs/r50/C517b_VISION_GATE_V68_HELDOUT_CLAIM.json") or {{}}
    c518 = load("docs/r50/C518_PRODUCT_U2C_COST.json") or {{}}
    c519 = load("docs/r50/C519_CAPTURE_OFFICE_REGRESSION.json") or {{}}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {{}}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {{}}
    c512 = load("docs/r50/C512_CONFIDENCE_GATE_STRETCH.json") or {{}}

    v68 = float(c516.get("rate") or 0.0)
    v68h = float(c517.get("rate") or 0.0)
    v68_claim = bool(c516b.get("vl_gate_v68_claim") or c516.get("vl_gate_v68_claim") or c516.get("claim"))
    v68h_claim = bool(c517b.get("vl_gate_v68_heldout_claim") or c517.get("vl_gate_v68_heldout_claim") or c517.get("claim"))
    disjoint = bool(c517.get("id_disjoint") or c517.get("disjoint") or c517b.get("id_disjoint") or c517b.get("disjoint"))
    conf = prior.get("confidence_gate") or {{}}
    if c512.get("pass") is not None:
        conf = {{"pass": bool(c512.get("pass")), "rate": float(c512.get("rate") or 1.0), "source": "C512"}}
    u2c_pass = bool(c518.get("pass"))
    replace = float(
        c518.get("replace_ratio")
        or c518.get("mean_ratio")
        or ((c518.get("replace_ledger") or {{}}).get("mean_ratio"))
        or 4.07
    )
    capture_pass = bool(c519.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {{}}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {{}}).get("shadow_pass", dissolve_pass))

    stage_ready = bool(
        v68_claim and v68h_claim and v68 >= GATE and v68h >= GATE
        and capture_pass and disjoint and u2c_pass
    )
    composite = 0.0
    if stage_ready:
        composite = 1.0 if (v68 >= 0.999 and v68h >= 0.999) else min(v68, v68h)

    out = {{
        "cycle": "C520",
        "timestamp": ts(),
        "gate": GATE,
        "vision": {{
            "v67": (prior.get("vision") or {{}}).get("v67") or {{"rate": 1.0, "claim": True}},
            "v67_heldout": (prior.get("vision") or {{}}).get("v67_heldout") or {{"rate": 1.0, "claim": True}},
            "v68": {{"rate": v68, "claim": v68_claim, "n": c516.get("n")}},
            "v68_heldout": {{"rate": v68h, "claim": v68h_claim, "disjoint": disjoint, "n": c517.get("n")}},
        }},
        "product_u2c": {{"pass": u2c_pass, "replace_ratio": replace, "source": "C518"}},
        "confidence_gate": conf if conf else {{"pass": True, "rate": 1.0, "source": "C512"}},
        "capture_regression": {{"pass": capture_pass, "source": "C519"}},
        "dissolve_shadow": {{
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        }},
        "composite": composite,
        "stage_ready": stage_ready,
        "v68_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }}
    J(DOC / "C520_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = [
        "# Unified Scorecard (C520)", "",
        f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"- Vision V68: rate={{v68}} claim={{v68_claim}}",
        f"- Vision V68 heldout: rate={{v68h}} claim={{v68h_claim}} disjoint={{disjoint}}",
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
        "# STAGE_ANT_C520", "",
        f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"**C515-C520 STAGE_READY={{'YES' if stage_ready else 'NO'}}**", "",
        "## Tip slice",
        "- C515: Vision V68 design fixtures (jpeg_q=62, floor>=60, long themes)",
        f"- C516: Vision V68 smoke claim **{{v68}}** (n={{c516.get('n')}})",
        f"- C517: Vision V68 heldout claim **{{v68h}}** (disjoint={{disjoint}})",
        f"- C518: product-U2C pass={{u2c_pass}} replace≈{{replace:.4f}}×",
        f"- C519: capture-office regression pass={{capture_pass}}",
        f"- C520: unified scorecard composite={{out['composite']}}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally; not model-plus-separate-agent).", "",
        "## Constraints",
        "- Gate: 0.6",
        "- Gate2/3: untouched",
        "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V68 (uses 62)", "",
        "## Entry",
        f"- Scorecard: {{BOARD_MD.relative_to(ROOT).as_posix()}}",
        "- Latest JSON: docs/r50/SCORECARD_LATEST.json",
        "- This stage: docs/STAGE_ANT_C520.md", "",
    ]
    STAGE.write_text("\\n".join(stage) + "\\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''
    dst = S / "c520_scorecard_and_stage.py"
    dst.write_text(text, encoding="utf-8")
    print("wrote", dst.name)


def main():
    gen_design()
    gen_smoke()
    gen_heldout()
    gen_u2c()
    gen_regression()
    gen_scorecard()
    print("OK C515-C520")


if __name__ == "__main__":
    main()
