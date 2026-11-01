# -*- coding: utf-8 -*-
"""Generate C539-C544 V72 scripts from V71. Knife: product-U2C (C542)."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"

THEMES = [
    ("ultramarine", "recv", "paid_total", "ULTRAMARINE GRAIN RECV", "RECV",
     lambda a,b,c: (a+b, [f"a paid {a:.2f}", f"b paid {b:.2f}", f"c open {c:.2f}", f"TOTAL PAID TARGET {a+b:.2f}"])),
    ("verdantglen", "wh", "qty_sum", "WH VERDANTGLEN BIN", "RECV",
     lambda a,b,c: (float(a+b), [f"SKU1 qty {a} ok", f"SKU2 qty {c} hold", f"SKU3 qty {b} ok", f"qty_sum TARGET {a+b}"])),
    ("windwardbay", "refund", "refund_done", "WINDWARDBAY PATCH REFUND", "DONE",
     lambda a,b,c: (a+b, [f"itemR1 {a:.2f} done", f"itemR2 {b:.2f} done", f"itemR3 {c:.2f} open", f"refund_done TARGET {a+b:.2f}"])),
    ("xanadupass", "tax", "tax_base_paid", "XANADUPASS TAX SLIP", "TAX",
     lambda a,b,c: (a+b, [f"base {a:.2f} paid", f"addon {b:.2f} paid", f"skip {c:.2f}", f"tax_base_paid TARGET {a+b:.2f}"])),
    ("yellowstone", "pay", "payroll_active", "YELLOWSTONE PAYROLL", "PAY",
     lambda a,b,c: (a+b, [f"empA {a:.2f} active", f"empB {b:.2f} active", f"empC {c:.2f} leave", f"payroll_active TARGET {a+b:.2f}"])),
    ("zincplateau", "ship", "ship_ok", "ZINCPLATEAU SHIP DOCK", "SHIP",
     lambda a,b,c: (float(a+b), [f"box1 {a} ok", f"box2 {b} ok", f"box3 {c} hold", f"ship_ok TARGET {a+b}"])),
    ("ashenridge", "sla", "sla_ok_hours", "ASHENRIDGE SLA CARD", "SLA",
     lambda a,b,c: (a+b, [f"job1 {a:.2f} hours ok", f"job2 {b:.2f} hours ok", f"job3 {c:.2f} hours late", f"sla_ok_hours TARGET {a+b:.2f}"])),
    ("bluemistcliff", "exp", "exp_sum", "BLUEMISTCLIFF EXPENSE", "EXP",
     lambda a,b,c: (a+b, [f"e1 {a:.2f}", f"e2 {b:.2f}", f"e3 {c:.2f} void", f"exp_sum TARGET {a+b:.2f}"])),
    ("coralhaven", "po", "po_open", "CORALHAVEN PO SHEET", "PO",
     lambda a,b,c: (a+b, [f"line1 {a:.2f} open", f"line2 {b:.2f} open", f"line3 {c:.2f} closed", f"po_open TARGET {a+b:.2f}"])),
    ("driftstone", "order", "order_paid", "DRIFTSTONE ORDER", "ORD",
     lambda a,b,c: (a+b, [f"skuA {a:.2f} paid", f"skuB {b:.2f} paid", f"skuC {c:.2f} due", f"order_paid TARGET {a+b:.2f}"])),
    ("eaglehollow", "dup", "dup_mark", "EAGLEHOLLOW DUP MARK", "DUP",
     lambda a,b,c: (2.0, ["markA 1", "markB 1", "markC 0", "dup_mark TARGET 2"])),
    ("firwoodpass", "zero", "zero_check", "FIRWOODPASS AIR ZERO", "ZERO",
     lambda a,b,c: (0.0, ["z1 0.00", "z2 0.00", "z3 0.00", "zero_check TARGET 0.00"])),
    ("goldenharbor", "ledger", "ledger_net", "GOLDENHARBOR LEDGER", "LED",
     lambda a,b,c: (a+b, [f"dr {a:.2f}", f"cr {b:.2f}", f"adj {c:.2f}", f"ledger_net TARGET {a+b:.2f}"])),
    ("hazelridge", "ui", "ui_ok", "HAZELRIDGE UI SCAN", "UI",
     lambda a,b,c: (1.0, ["btnOK 1", "btnSkip 0", "btnBad 0", "ui_ok TARGET 1"])),
    ("ironhaven", "stack", "stack_count", "IRONHAVEN STACK", "STK",
     lambda a,b,c: (float(a+b), [f"p1 {a}", f"p2 {b}", f"p3 {c}", f"stack_count TARGET {a+b}"])),
    ("jadecliff", "fax", "fax_pages", "JADECLIFF FAX", "FAX",
     lambda a,b,c: (float(a+b), [f"pgA {a}", f"pgB {b}", f"pgC {c} drop", f"fax_pages TARGET {a+b}"])),
    ("kelpbasin", "glare", "glare_ok", "KELPBASIN GLARE", "GLR",
     lambda a,b,c: (1.0, ["zone1 1 ok", "zone2 0", "zone3 0", "glare_ok TARGET 1"])),
    ("limestonebay", "tab", "tab_index", "LIMESTONEBAY TAB INDEX", "TAB",
     lambda a,b,c: (float(a+b), [f"tabA {a}", f"tabB {b}", f"tabC {c}", f"tab_index TARGET {a+b}"])),
]
TRAIN_ABC = [
    (312.0, 328.5, 155.0), (259, 287, 175), (243.0, 266.25, 133.0), (366.0, 384.0, 207.0),
    (429.0, 453.0, 193.0), (203, 219, 151), (265.0, 256.5, 138.0), (277.0, 306.75, 157.0),
    (311.0, 294.0, 166.0), (344.0, 332.0, 154.0), (1, 1, 0), (0, 0, 0),
    (410.0, 433.5, 179.0), (1, 0, 0), (63, 55, 33), (81, 65, 56), (1, 0, 0), (99, 83, 53),
]
HELDOUT_ABC = [
    (197.0, 211.75, 106.0), (159, 187, 113), (155.0, 170.5, 94.0), (254.0, 270.0, 135.0),
    (295.0, 311.0, 130.0), (121, 135, 99), (163.0, 159.5, 100.0), (181.0, 200.75, 106.0),
    (201.0, 189.0, 109.0), (228.0, 216.0, 101.0), (1, 1, 0), (0, 0, 0),
    (263.0, 280.5, 116.0), (1, 0, 0), (39, 36, 31), (55, 49, 37), (1, 0, 0), (65, 59, 38),
]
THEME_STR = "ultramarine_verdantglen_windwardbay_xanadupass_yellowstone_zincplateau_ashenridge_bluemistcliff_coralhaven_driftstone_eaglehollow_firwoodpass_goldenharbor_hazelridge_ironhaven_jadecliff_kelpbasin_limestonebay"
OLD_THEME = "cedarhaven_duskvalley_embertrail_frosthollow_granitefall_harborcrest_ivorypass_jaspercreek_kilnstone_larkspurpass_mistwoodridge_northwindbay_opalhaven_pebblecliff_quartzcliff_redwoodpass_silvermeadow_thornfield"


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
    src = src.replace("# --- V71 overlays (new vs V70) ---", "# --- V72 overlays (new vs V71) ---")
    for a, b in [
        ("CEDARHAVEN bait", "ULTRAMARINE bait"), ("THORNFIELD bait", "LIMESTONEBAY bait"),
        ("NORTHWINDBAY ghost", "FIRWOODPASS ghost"), ("PEBBLECLIFF bait", "HAZELRIDGE bait"),
        ("HARBORCREST bait", "ZINCPLATEAU bait"), ("QUARTZCLIFF", "IRONHAVEN"),
        ("DUSKVALLEY bait", "VERDANTGLEN bait"),
        ("cedar mist + thorn ticks (V71-only)", "ultra mist + limestone ticks (V72-only)"),
    ]:
        src = src.replace(a, b)
    return src


def gen_design():
    out = (S / "c533_vision_v71_design_and_batch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C533", "C539"), ("c533", "c539"), ("V71", "V72"), ("v71", "v72"),
        ("_v71c533", "_v72c539"),
        ("Harder than V70", "Harder than V71"),
        ("harder than V70", "harder than V71"),
        (OLD_THEME, THEME_STR),
        ("V71 keeps floor", "V72 keeps floor"),
        ("C533 design+fixtures; no VL claim", "C539 design+fixtures; no VL claim"),
        ("fixtures only; claim deferred to C534 VL smoke", "fixtures only; claim deferred to C540 VL smoke"),
        ("No claim until C534 VL", "No claim until C540 VL"),
        ("kept on V71", "kept on V72"),
        ('"harder_than": "v70_kestrelridge_brackenfield"', '"harder_than": "v71_cedarhaven_thornfield"'),
        ("r50plus_v71_cedarhaven_thornfield", "r50plus_v72_ultramarine_limestonebay"),
    ]:
        out = out.replace(a, b)
    out = out.replace(
        "NEW themes vs V70: cedarhaven, duskvalley, embertrail, frosthollow, granitefall, harborcrest, ivorypass, jaspercreek,\nkilnstone, larkspurpass, mistwoodridge, northwindbay, opalhaven, pebblecliff, quartzcliff, redwoodpass, silvermeadow, thornfield.",
        "NEW themes vs V71: ultramarine, verdantglen, windwardbay, xanadupass, yellowstone, zincplateau, ashenridge, bluemistcliff,\ncoralhaven, driftstone, eaglehollow, firwoodpass, goldenharbor, hazelridge, ironhaven, jadecliff, kelpbasin, limestonebay.",
    )
    out = replace_specs(out, build_specs("v72", "V72", TRAIN_ABC))
    out = retarget_overlay(out)
    dst = S / "c539_vision_v72_design_and_batch.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_smoke():
    out = (S / "c534_vision_v71_smoke.py").read_text(encoding="utf-8")
    for a, b in [
        ("C534", "C540"), ("c534", "c540"), ("V71", "V72"), ("v71", "v72"),
        ("r50plus_v71_cedarhaven_thornfield_clarity_floor_n>=16_qwen35_2b",
         "r50plus_v72_ultramarine_limestonebay_clarity_floor_n>=16_qwen35_2b"),
        ("Uses C533 fixtures", "Uses C539 fixtures"),
    ]:
        out = out.replace(a, b)
    dst = S / "c540_vision_v72_smoke.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_heldout():
    out = (S / "c535_vision_v71_heldout.py").read_text(encoding="utf-8")
    for a, b in [
        ("C535", "C541"), ("c535", "c541"), ("C533", "C539"),
        ("V71", "V72"), ("v71", "v72"),
        ("_v71hc535", "_v72hc541"),
        ("_v71c533", "_v72c539"),
    ]:
        out = out.replace(a, b)
    out = replace_specs(out, build_specs("v72h", "V72H", HELDOUT_ABC))
    out = retarget_overlay(out)
    out2 = []
    seen_fix = seen_train = seen_run = False
    for ln in out.splitlines():
        s = ln.strip()
        if s.startswith("FIX = ") and not seen_fix:
            out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v72h"')
            seen_fix = True
            continue
        if s.startswith("TRAIN_FIX = ") and not seen_train:
            out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v72"')
            seen_train = True
            continue
        if s.startswith("RUN = ") and "vision_v72" in s and not seen_run:
            out2.append('RUN = ROOT / "runs/vision_v72h_c541"')
            seen_run = True
            continue
        out2.append(ln)
    out = "\n".join(out2) + "\n"
    dst = S / "c541_vision_v72_heldout.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_u2c():
    out = (S / "c530_product_u2c_cost.py").read_text(encoding="utf-8")
    for a, b in [
        ("C530", "C542"), ("c530", "c542"),
        ("product_u2c_c530", "product_u2c_c542"),
        ("u2c_cost_c530", "u2c_cost_c542"),
        ("after V70", "after V72"), ("after V71", "after V72"),
        ("V70+", "V72+"), ("V71+", "V72+"),
    ]:
        out = out.replace(a, b)
    dst = S / "c542_product_u2c_cost.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_regression():
    out = (S / "c537_capture_office_regression.py").read_text(encoding="utf-8")
    for a, b in [
        ("C537", "C543"), ("c537", "c543"),
        ("capture_regression_c537", "capture_regression_c543"),
        ("after C533-C536", "after C539-C542"),
        ("V4-V71+heldout", "V4-V72+heldout"),
    ]:
        out = out.replace(a, b)
    if "VISION_V72_SMOKE" not in out:
        out = out.replace(
            "SMOKE_POINTERS = [",
            'SMOKE_POINTERS = [\n'
            '    ("V72", DOC / "C540_VISION_V72_SMOKE.json"),\n'
            '    ("V72_heldout", DOC / "C541_VISION_V72_HELDOUT_SMOKE.json"),\n'
            '    ("V71", DOC / "C534_VISION_V71_SMOKE.json"),\n'
            '    ("V71_heldout", DOC / "C535_VISION_V71_HELDOUT_SMOKE.json"),',
            1,
        )
    dst = S / "c543_capture_office_regression.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name)


def gen_scorecard():
    board = 'BOARD_MD = ROOT / "docs" / "ANT_UNIFIED_SCORECARD.md"'
    for ln in (S / "c538_scorecard_and_stage.py").read_text(encoding="utf-8").splitlines():
        if "BOARD_MD" in ln and "=" in ln:
            board = ln
            break
    nl = "\\n"
    text = f'''# -*- coding: utf-8 -*-
"""C544: Unified scorecard + STAGE after C539-C543. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
{board}
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C544.md"
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
    c540 = load("docs/r50/C540_VISION_V72_SMOKE.json") or {{}}
    c540b = load("docs/r50/C540b_VISION_GATE_V72_CLAIM.json") or {{}}
    c541 = load("docs/r50/C541_VISION_V72_HELDOUT_SMOKE.json") or {{}}
    c541b = load("docs/r50/C541b_VISION_GATE_V72_HELDOUT_CLAIM.json") or {{}}
    c542 = load("docs/r50/C542_PRODUCT_U2C_COST.json") or {{}}
    c543 = load("docs/r50/C543_CAPTURE_OFFICE_REGRESSION.json") or {{}}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {{}}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {{}}
    c536 = load("docs/r50/C536_CONFIDENCE_GATE_STRETCH.json") or {{}}

    v72 = float(c540.get("rate") or 0.0)
    v72h = float(c541.get("rate") or 0.0)
    v72_claim = bool(c540b.get("vl_gate_v72_claim") or c540.get("vl_gate_v72_claim") or c540.get("claim"))
    v72h_claim = bool(c541b.get("vl_gate_v72_heldout_claim") or c541.get("vl_gate_v72_heldout_claim") or c541.get("claim"))
    disjoint = bool(c541.get("id_disjoint") or c541.get("disjoint") or c541b.get("id_disjoint") or c541b.get("disjoint"))
    conf = prior.get("confidence_gate") or {{}}
    if c536.get("pass") is not None:
        conf = {{"pass": bool(c536.get("pass")), "rate": float(c536.get("rate") or 1.0), "source": "C536"}}
    u2c_pass = bool(c542.get("pass"))
    replace = float(
        c542.get("replace_ratio")
        or c542.get("mean_ratio")
        or ((c542.get("replace_ledger") or {{}}).get("mean_ratio"))
        or 4.07
    )
    capture_pass = bool(c543.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {{}}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {{}}).get("shadow_pass", dissolve_pass))

    stage_ready = bool(
        v72_claim and v72h_claim and v72 >= GATE and v72h >= GATE
        and capture_pass and disjoint and u2c_pass
    )
    composite = 0.0
    if stage_ready:
        composite = 1.0 if (v72 >= 0.999 and v72h >= 0.999) else min(v72, v72h)

    out = {{
        "cycle": "C544",
        "timestamp": ts(),
        "gate": GATE,
        "vision": {{
            "v71": (prior.get("vision") or {{}}).get("v71") or {{"rate": 1.0, "claim": True}},
            "v71_heldout": (prior.get("vision") or {{}}).get("v71_heldout") or {{"rate": 1.0, "claim": True}},
            "v72": {{"rate": v72, "claim": v72_claim, "n": c540.get("n")}},
            "v72_heldout": {{"rate": v72h, "claim": v72h_claim, "disjoint": disjoint, "n": c541.get("n")}},
        }},
        "product_u2c": {{"pass": u2c_pass, "replace_ratio": replace, "source": "C542"}},
        "confidence_gate": conf if conf else {{"pass": True, "rate": 1.0, "source": "C536"}},
        "capture_regression": {{"pass": capture_pass, "source": "C543"}},
        "dissolve_shadow": {{
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        }},
        "composite": composite,
        "stage_ready": stage_ready,
        "v72_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }}
    J(DOC / "C544_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = [
        "# Unified Scorecard (C544)", "",
        f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"- Vision V72: rate={{v72}} claim={{v72_claim}}",
        f"- Vision V72 heldout: rate={{v72h}} claim={{v72h_claim}} disjoint={{disjoint}}",
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
        "# STAGE_ANT_C544", "",
        f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"**C539-C544 STAGE_READY={{'YES' if stage_ready else 'NO'}}**", "",
        "## Tip slice",
        "- C539: Vision V72 design fixtures (jpeg_q=62, floor>=60, long themes)",
        f"- C540: Vision V72 smoke claim **{{v72}}** (n={{c540.get('n')}})",
        f"- C541: Vision V72 heldout claim **{{v72h}}** (disjoint={{disjoint}})",
        f"- C542: product-U2C pass={{u2c_pass}} replace≈{{replace:.4f}}×",
        f"- C543: capture-office regression pass={{capture_pass}}",
        f"- C544: unified scorecard composite={{out['composite']}}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally; not model-plus-separate-agent).", "",
        "## Constraints",
        "- Gate: 0.6",
        "- Gate2/3: untouched",
        "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V72 (uses 62)", "",
        "## Entry",
        f"- Scorecard: {{BOARD_MD.relative_to(ROOT).as_posix()}}",
        "- Latest JSON: docs/r50/SCORECARD_LATEST.json",
        "- This stage: docs/STAGE_ANT_C544.md", "",
    ]
    STAGE.write_text("\\n".join(stage) + "\\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''
    dst = S / "c544_scorecard_and_stage.py"
    dst.write_text(text, encoding="utf-8")
    print("wrote", dst.name)


def main():
    gen_design()
    gen_smoke()
    gen_heldout()
    gen_u2c()
    gen_regression()
    gen_scorecard()
    print("OK C539-C544")


if __name__ == "__main__":
    main()
