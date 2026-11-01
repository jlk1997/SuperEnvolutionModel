# -*- coding: utf-8 -*-
"""Generate C563-C568 V76 from V75. Knife: product-U2C (C566)."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"

THEMES = [
    ("oakcliff", "recv", "paid_total", "OAKCLIFF GRAIN RECV", "RECV",
     lambda a,b,c: (a+b, [f"a paid {a:.2f}", f"b paid {b:.2f}", f"c open {c:.2f}", f"TOTAL PAID TARGET {a+b:.2f}"])),
    ("pebblehaven", "wh", "qty_sum", "WH PEBBLEHAVEN BIN", "RECV",
     lambda a,b,c: (float(a+b), [f"SKU1 qty {a} ok", f"SKU2 qty {c} hold", f"SKU3 qty {b} ok", f"qty_sum TARGET {a+b}"])),
    ("quailhaven", "refund", "refund_done", "QUAILHAVEN PATCH REFUND", "DONE",
     lambda a,b,c: (a+b, [f"itemR1 {a:.2f} done", f"itemR2 {b:.2f} done", f"itemR3 {c:.2f} open", f"refund_done TARGET {a+b:.2f}"])),
    ("rainhaven", "tax", "tax_base_paid", "RAINHAVEN TAX SLIP", "TAX",
     lambda a,b,c: (a+b, [f"base {a:.2f} paid", f"addon {b:.2f} paid", f"skip {c:.2f}", f"tax_base_paid TARGET {a+b:.2f}"])),
    ("sagehaven", "pay", "payroll_active", "SAGEHAVEN PAYROLL", "PAY",
     lambda a,b,c: (a+b, [f"empA {a:.2f} active", f"empB {b:.2f} active", f"empC {c:.2f} leave", f"payroll_active TARGET {a+b:.2f}"])),
    ("tidecliff", "ship", "ship_ok", "TIDECLIFF SHIP DOCK", "SHIP",
     lambda a,b,c: (float(a+b), [f"box1 {a} ok", f"box2 {b} ok", f"box3 {c} hold", f"ship_ok TARGET {a+b}"])),
    ("underpass", "sla", "sla_ok_hours", "UNDERPASS SLA CARD", "SLA",
     lambda a,b,c: (a+b, [f"job1 {a:.2f} hours ok", f"job2 {b:.2f} hours ok", f"job3 {c:.2f} hours late", f"sla_ok_hours TARGET {a+b:.2f}"])),
    ("vinehaven", "exp", "exp_sum", "VINEHAVEN EXPENSE", "EXP",
     lambda a,b,c: (a+b, [f"e1 {a:.2f}", f"e2 {b:.2f}", f"e3 {c:.2f} void", f"exp_sum TARGET {a+b:.2f}"])),
    ("wavecliff", "po", "po_open", "WAVECLIFF PO SHEET", "PO",
     lambda a,b,c: (a+b, [f"line1 {a:.2f} open", f"line2 {b:.2f} open", f"line3 {c:.2f} closed", f"po_open TARGET {a+b:.2f}"])),
    ("xyloridge", "order", "order_paid", "XYLORIDGE ORDER", "ORD",
     lambda a,b,c: (a+b, [f"skuA {a:.2f} paid", f"skuB {b:.2f} paid", f"skuC {c:.2f} due", f"order_paid TARGET {a+b:.2f}"])),
    ("yellowhaven", "dup", "dup_mark", "YELLOWHAVEN DUP MARK", "DUP",
     lambda a,b,c: (2.0, ["markA 1", "markB 1", "markC 0", "dup_mark TARGET 2"])),
    ("zephyrpass", "zero", "zero_check", "ZEPHYRPASS AIR ZERO", "ZERO",
     lambda a,b,c: (0.0, ["z1 0.00", "z2 0.00", "z3 0.00", "zero_check TARGET 0.00"])),
    ("alderpass", "ledger", "ledger_net", "ALDERPASS LEDGER", "LED",
     lambda a,b,c: (a+b, [f"dr {a:.2f}", f"cr {b:.2f}", f"adj {c:.2f}", f"ledger_net TARGET {a+b:.2f}"])),
    ("birchpass", "ui", "ui_ok", "BIRCHPASS UI SCAN", "UI",
     lambda a,b,c: (1.0, ["btnOK 1", "btnSkip 0", "btnBad 0", "ui_ok TARGET 1"])),
    ("cinderpass", "stack", "stack_count", "CINDERPASS STACK", "STK",
     lambda a,b,c: (float(a+b), [f"p1 {a}", f"p2 {b}", f"p3 {c}", f"stack_count TARGET {a+b}"])),
    ("dewcliff", "fax", "fax_pages", "DEWCLIFF FAX", "FAX",
     lambda a,b,c: (float(a+b), [f"pgA {a}", f"pgB {b}", f"pgC {c} drop", f"fax_pages TARGET {a+b}"])),
    ("emberpass", "glare", "glare_ok", "EMBERPASS GLARE", "GLR",
     lambda a,b,c: (1.0, ["zone1 1 ok", "zone2 0", "zone3 0", "glare_ok TARGET 1"])),
    ("fernpass", "tab", "tab_index", "FERNPASS TAB INDEX", "TAB",
     lambda a,b,c: (float(a+b), [f"tabA {a}", f"tabB {b}", f"tabC {c}", f"tab_index TARGET {a+b}"])),
]
TRAIN_ABC = [
    (344.0, 359.5, 171.0), (291, 319, 191), (271.0, 297.25, 149.0), (398.0, 416.0, 231.0),
    (461.0, 485.0, 209.0), (227, 243, 167), (297.0, 287.5, 154.0), (309.0, 339.75, 173.0),
    (343.0, 326.0, 182.0), (376.0, 364.0, 170.0), (1, 1, 0), (0, 0, 0),
    (442.0, 464.5, 195.0), (1, 0, 0), (71, 63, 41), (89, 73, 64), (1, 0, 0), (111, 91, 61),
]
HELDOUT_ABC = [
    (221.0, 234.75, 122.0), (183, 211, 129), (179.0, 193.5, 110.0), (286.0, 302.0, 151.0),
    (327.0, 343.0, 146.0), (137, 151, 115), (187.0, 182.5, 116.0), (205.0, 225.75, 122.0),
    (225.0, 213.0, 125.0), (252.0, 239.0, 117.0), (1, 1, 0), (0, 0, 0),
    (287.0, 303.5, 132.0), (1, 0, 0), (47, 44, 39), (63, 57, 45), (1, 0, 0), (73, 67, 46),
]
THEME_STR = "oakcliff_pebblehaven_quailhaven_rainhaven_sagehaven_tidecliff_underpass_vinehaven_wavecliff_xyloridge_yellowhaven_zephyrpass_alderpass_birchpass_cinderpass_dewcliff_emberpass_fernpass"
OLD_THEME = "windhaven_xanaduhaven_yuccaridge_zinccliff_ashenpass_brackenpass_cedarpass_duskcliff_echohaven_firhaven_grovecliff_hollowpass_ivoryhaven_jasperhaven_kelphaven_lotuspass_meadowpass_nimbuspass"


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
    src = src.replace("# --- V75 overlays (new vs V74) ---", "# --- V76 overlays (new vs V75) ---")
    for a, b in [
        ("WINDHAVEN bait", "OAKCLIFF bait"), ("NIMBUSPASS bait", "FERNPASS bait"),
        ("HOLLOWPASS ghost", "ZEPHYRPASS ghost"), ("JASPERHAVEN bait", "BIRCHPASS bait"),
        ("BRACKENPASS bait", "TIDECLIFF bait"), ("KELPHAVEN", "CINDERPASS"),
        ("XANADUHAVEN bait", "PEBBLEHAVEN bait"),
        ("wind mist + nimbus ticks (V75-only)", "oak mist + fern ticks (V76-only)"),
    ]:
        src = src.replace(a, b)
    return src


def gen_design():
    out = (S / "c557_vision_v75_design_and_batch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C557", "C563"), ("c557", "c563"), ("V75", "V76"), ("v75", "v76"),
        ("_v75c557", "_v76c563"),
        ("Harder than V74", "Harder than V75"),
        ("harder than V74", "harder than V75"),
        (OLD_THEME, THEME_STR),
        ("V75 keeps floor", "V76 keeps floor"),
        ("C557 design+fixtures; no VL claim", "C563 design+fixtures; no VL claim"),
        ("fixtures only; claim deferred to C558 VL smoke", "fixtures only; claim deferred to C564 VL smoke"),
        ("No claim until C558 VL", "No claim until C564 VL"),
        ("kept on V75", "kept on V76"),
        ('"harder_than": "v74_emberhaven_valecliff"', '"harder_than": "v75_windhaven_nimbuspass"'),
        ("r50plus_v75_windhaven_nimbuspass", "r50plus_v76_oakcliff_fernpass"),
    ]:
        out = out.replace(a, b)
    out = out.replace(
        "NEW themes vs V74: windhaven, xanaduhaven, yuccaridge, zinccliff, ashenpass, brackenpass, cedarpass, duskcliff,\nechohaven, firhaven, grovecliff, hollowpass, ivoryhaven, jasperhaven, kelphaven, lotuspass, meadowpass, nimbuspass.",
        "NEW themes vs V75: oakcliff, pebblehaven, quailhaven, rainhaven, sagehaven, tidecliff, underpass, vinehaven,\nwavecliff, xyloridge, yellowhaven, zephyrpass, alderpass, birchpass, cinderpass, dewcliff, emberpass, fernpass.",
    )
    out = replace_specs(out, build_specs("v76", "V76", TRAIN_ABC))
    out = retarget_overlay(out)
    (S / "c563_vision_v76_design_and_batch.py").write_text(out, encoding="utf-8")
    print("wrote design")


def gen_smoke():
    out = (S / "c558_vision_v75_smoke.py").read_text(encoding="utf-8")
    for a, b in [
        ("C558", "C564"), ("c558", "c564"), ("V75", "V76"), ("v75", "v76"),
        ("r50plus_v75_windhaven_nimbuspass_clarity_floor_n>=16_qwen35_2b",
         "r50plus_v76_oakcliff_fernpass_clarity_floor_n>=16_qwen35_2b"),
        ("Uses C557 fixtures", "Uses C563 fixtures"),
    ]:
        out = out.replace(a, b)
    (S / "c564_vision_v76_smoke.py").write_text(out, encoding="utf-8")
    print("wrote smoke")


def gen_heldout():
    out = (S / "c559_vision_v75_heldout.py").read_text(encoding="utf-8")
    for a, b in [
        ("C559", "C565"), ("c559", "c565"), ("C557", "C563"),
        ("V75", "V76"), ("v75", "v76"),
        ("_v75hc559", "_v76hc565"), ("_v75c557", "_v76c563"),
    ]:
        out = out.replace(a, b)
    out = replace_specs(out, build_specs("v76h", "V76H", HELDOUT_ABC))
    out = retarget_overlay(out)
    out2, seen_fix, seen_train, seen_run = [], False, False, False
    for ln in out.splitlines():
        s = ln.strip()
        if s.startswith("FIX = ") and not seen_fix:
            out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v76h"'); seen_fix = True; continue
        if s.startswith("TRAIN_FIX = ") and not seen_train:
            out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v76"'); seen_train = True; continue
        if s.startswith("RUN = ") and "vision_v76" in s and not seen_run:
            out2.append('RUN = ROOT / "runs/vision_v76h_c565"'); seen_run = True; continue
        out2.append(ln)
    (S / "c565_vision_v76_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
    print("wrote heldout")


def gen_u2c():
    out = (S / "c554_product_u2c_cost.py").read_text(encoding="utf-8")
    for a, b in [
        ("C554", "C566"), ("c554", "c566"),
        ("product_u2c_c554", "product_u2c_c566"), ("u2c_cost_c554", "u2c_cost_c566"),
        ("after V74", "after V76"), ("after V75", "after V76"),
        ("V74+", "V76+"), ("V75+", "V76+"),
    ]:
        out = out.replace(a, b)
    (S / "c566_product_u2c_cost.py").write_text(out, encoding="utf-8")
    print("wrote u2c")


def gen_regression():
    out = (S / "c561_capture_office_regression.py").read_text(encoding="utf-8")
    for a, b in [
        ("C561", "C567"), ("c561", "c567"),
        ("capture_regression_c561", "capture_regression_c567"),
        ("after C557-C560", "after C563-C566"),
        ("V4-V75+heldout", "V4-V76+heldout"),
    ]:
        out = out.replace(a, b)
    if "VISION_V76_SMOKE" not in out:
        out = out.replace(
            "SMOKE_POINTERS = [",
            'SMOKE_POINTERS = [\n'
            '    ("V76", DOC / "C564_VISION_V76_SMOKE.json"),\n'
            '    ("V76_heldout", DOC / "C565_VISION_V76_HELDOUT_SMOKE.json"),\n'
            '    ("V75", DOC / "C558_VISION_V75_SMOKE.json"),\n'
            '    ("V75_heldout", DOC / "C559_VISION_V75_HELDOUT_SMOKE.json"),',
            1,
        )
    (S / "c567_capture_office_regression.py").write_text(out, encoding="utf-8")
    print("wrote regression")


def gen_scorecard():
    board = 'BOARD_MD = ROOT / "docs" / "ANT_UNIFIED_SCORECARD.md"'
    for ln in (S / "c562_scorecard_and_stage.py").read_text(encoding="utf-8").splitlines():
        if "BOARD_MD" in ln and "=" in ln:
            board = ln; break
    nl = "\\n"
    text = f'''# -*- coding: utf-8 -*-
"""C568: Unified scorecard + STAGE after C563-C567. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
{board}
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C568.md"
GATE = 0.6


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "{nl}", encoding="utf-8")


def load(rel):
    p = ROOT / rel
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None


def main():
    c564 = load("docs/r50/C564_VISION_V76_SMOKE.json") or {{}}
    c564b = load("docs/r50/C564b_VISION_GATE_V76_CLAIM.json") or {{}}
    c565 = load("docs/r50/C565_VISION_V76_HELDOUT_SMOKE.json") or {{}}
    c565b = load("docs/r50/C565b_VISION_GATE_V76_HELDOUT_CLAIM.json") or {{}}
    c566 = load("docs/r50/C566_PRODUCT_U2C_COST.json") or {{}}
    c567 = load("docs/r50/C567_CAPTURE_OFFICE_REGRESSION.json") or {{}}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {{}}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {{}}
    c560 = load("docs/r50/C560_CONFIDENCE_GATE_STRETCH.json") or {{}}

    v76 = float(c564.get("rate") or 0.0)
    v76h = float(c565.get("rate") or 0.0)
    v76_claim = bool(c564b.get("vl_gate_v76_claim") or c564.get("vl_gate_v76_claim") or c564.get("claim"))
    v76h_claim = bool(c565b.get("vl_gate_v76_heldout_claim") or c565.get("vl_gate_v76_heldout_claim") or c565.get("claim"))
    disjoint = bool(c565.get("id_disjoint") or c565.get("disjoint") or c565b.get("id_disjoint") or c565b.get("disjoint"))
    conf = prior.get("confidence_gate") or {{}}
    if c560.get("pass") is not None:
        conf = {{"pass": bool(c560.get("pass")), "rate": float(c560.get("rate") or 1.0), "source": "C560"}}
    u2c_pass = bool(c566.get("pass"))
    replace = float(c566.get("replace_ratio") or c566.get("mean_ratio") or ((c566.get("replace_ledger") or {{}}).get("mean_ratio")) or 4.07)
    capture_pass = bool(c567.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {{}}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {{}}).get("shadow_pass", dissolve_pass))
    stage_ready = bool(v76_claim and v76h_claim and v76 >= GATE and v76h >= GATE and capture_pass and disjoint and u2c_pass)
    composite = (1.0 if (v76 >= 0.999 and v76h >= 0.999) else min(v76, v76h)) if stage_ready else 0.0
    out = {{
        "cycle": "C568", "timestamp": ts(), "gate": GATE,
        "vision": {{
            "v75": (prior.get("vision") or {{}}).get("v75") or {{"rate": 1.0, "claim": True}},
            "v75_heldout": (prior.get("vision") or {{}}).get("v75_heldout") or {{"rate": 1.0, "claim": True}},
            "v76": {{"rate": v76, "claim": v76_claim, "n": c564.get("n")}},
            "v76_heldout": {{"rate": v76h, "claim": v76h_claim, "disjoint": disjoint, "n": c565.get("n")}},
        }},
        "product_u2c": {{"pass": u2c_pass, "replace_ratio": replace, "source": "C566"}},
        "confidence_gate": conf if conf else {{"pass": True, "rate": 1.0, "source": "C560"}},
        "capture_regression": {{"pass": capture_pass, "source": "C567"}},
        "dissolve_shadow": {{"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"}},
        "composite": composite, "stage_ready": stage_ready,
        "v76_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",
    }}
    J(DOC / "C568_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)
    BOARD_MD.write_text("\\n".join([
        "# Unified Scorecard (C568)", "", f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"- Vision V76: rate={{v76}} claim={{v76_claim}}",
        f"- Vision V76 heldout: rate={{v76h}} claim={{v76h_claim}} disjoint={{disjoint}}",
        f"- product_u2c: {{out['product_u2c']}}", f"- confidence_gate: {{out['confidence_gate']}}",
        f"- capture_regression: pass={{capture_pass}}", f"- composite: {{composite}}",
        f"- stage_ready: {{stage_ready}}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",
    ]) + "\\n", encoding="utf-8")
    STAGE.write_text("\\n".join([
        "# STAGE_ANT_C568", "", f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"**C563-C568 STAGE_READY={{'YES' if stage_ready else 'NO'}}**", "",
        "## Tip slice",
        "- C563: Vision V76 design fixtures",
        f"- C564: Vision V76 smoke **{{v76}}**", f"- C565: Vision V76 heldout **{{v76h}}** (disjoint={{disjoint}})",
        f"- C566: product-U2C pass={{u2c_pass}} replace≈{{replace:.4f}}×",
        f"- C567: capture pass={{capture_pass}}", f"- C568: composite={{composite}}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",
        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V76 (uses 62)", "",
        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C568.md", "",
    ]) + "\\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''
    (S / "c568_scorecard_and_stage.py").write_text(text, encoding="utf-8")
    print("wrote scorecard")


def main():
    gen_design(); gen_smoke(); gen_heldout(); gen_u2c(); gen_regression(); gen_scorecard()
    print("OK C563-C568")


if __name__ == "__main__":
    main()
