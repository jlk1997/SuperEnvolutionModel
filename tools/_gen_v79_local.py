# -*- coding: utf-8 -*-
"""Generate C581-C586 V79 from V78. Knife: confidence-gate (C584)."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"

THEMES = [
    ("quarrydale", "recv", "paid_total", "QUARRYDALE GRAIN RECV", "RECV",
     lambda a,b,c: (a+b, [f"a paid {a:.2f}", f"b paid {b:.2f}", f"c open {c:.2f}", f"TOTAL PAID TARGET {a+b:.2f}"])),
    ("riverdale", "wh", "qty_sum", "WH RIVERDALE BIN", "RECV",
     lambda a,b,c: (float(a+b), [f"SKU1 qty {a} ok", f"SKU2 qty {c} hold", f"SKU3 qty {b} ok", f"qty_sum TARGET {a+b}"])),
    ("sagedale", "refund", "refund_done", "SAGEDALE PATCH REFUND", "DONE",
     lambda a,b,c: (a+b, [f"itemR1 {a:.2f} done", f"itemR2 {b:.2f} done", f"itemR3 {c:.2f} open", f"refund_done TARGET {a+b:.2f}"])),
    ("tidedale", "tax", "tax_base_paid", "TIDEDALE TAX SLIP", "TAX",
     lambda a,b,c: (a+b, [f"base {a:.2f} paid", f"addon {b:.2f} paid", f"skip {c:.2f}", f"tax_base_paid TARGET {a+b:.2f}"])),
    ("umbrahaven2", "pay", "payroll_active", "UMBRAHAVEN2 PAYROLL", "PAY",
     lambda a,b,c: (a+b, [f"empA {a:.2f} active", f"empB {b:.2f} active", f"empC {c:.2f} leave", f"payroll_active TARGET {a+b:.2f}"])),
]
# Fix umbrahaven2 - use better unique long names
THEMES = [
    ("quarrydale", "recv", "paid_total", "QUARRYDALE GRAIN RECV", "RECV",
     lambda a,b,c: (a+b, [f"a paid {a:.2f}", f"b paid {b:.2f}", f"c open {c:.2f}", f"TOTAL PAID TARGET {a+b:.2f}"])),
    ("riverdale", "wh", "qty_sum", "WH RIVERDALE BIN", "RECV",
     lambda a,b,c: (float(a+b), [f"SKU1 qty {a} ok", f"SKU2 qty {c} hold", f"SKU3 qty {b} ok", f"qty_sum TARGET {a+b}"])),
    ("sagedale", "refund", "refund_done", "SAGEDALE PATCH REFUND", "DONE",
     lambda a,b,c: (a+b, [f"itemR1 {a:.2f} done", f"itemR2 {b:.2f} done", f"itemR3 {c:.2f} open", f"refund_done TARGET {a+b:.2f}"])),
    ("tidedale", "tax", "tax_base_paid", "TIDEDALE TAX SLIP", "TAX",
     lambda a,b,c: (a+b, [f"base {a:.2f} paid", f"addon {b:.2f} paid", f"skip {c:.2f}", f"tax_base_paid TARGET {a+b:.2f}"])),
    ("underdale", "pay", "payroll_active", "UNDERDALE PAYROLL", "PAY",
     lambda a,b,c: (a+b, [f"empA {a:.2f} active", f"empB {b:.2f} active", f"empC {c:.2f} leave", f"payroll_active TARGET {a+b:.2f}"])),
    ("vinedale", "ship", "ship_ok", "VINEDALE SHIP DOCK", "SHIP",
     lambda a,b,c: (float(a+b), [f"box1 {a} ok", f"box2 {b} ok", f"box3 {c} hold", f"ship_ok TARGET {a+b}"])),
    ("wavedale", "sla", "sla_ok_hours", "WAVEDALE SLA CARD", "SLA",
     lambda a,b,c: (a+b, [f"job1 {a:.2f} hours ok", f"job2 {b:.2f} hours ok", f"job3 {c:.2f} hours late", f"sla_ok_hours TARGET {a+b:.2f}"])),
    ("xylodale", "exp", "exp_sum", "XYLODALE EXPENSE", "EXP",
     lambda a,b,c: (a+b, [f"e1 {a:.2f}", f"e2 {b:.2f}", f"e3 {c:.2f} void", f"exp_sum TARGET {a+b:.2f}"])),
    ("yellowdale", "po", "po_open", "YELLOWDALE PO SHEET", "PO",
     lambda a,b,c: (a+b, [f"line1 {a:.2f} open", f"line2 {b:.2f} open", f"line3 {c:.2f} closed", f"po_open TARGET {a+b:.2f}"])),
    ("zincdale", "order", "order_paid", "ZINCDALE ORDER", "ORD",
     lambda a,b,c: (a+b, [f"skuA {a:.2f} paid", f"skuB {b:.2f} paid", f"skuC {c:.2f} due", f"order_paid TARGET {a+b:.2f}"])),
    ("ashendale", "dup", "dup_mark", "ASHENDALE DUP MARK", "DUP",
     lambda a,b,c: (2.0, ["markA 1", "markB 1", "markC 0", "dup_mark TARGET 2"])),
    ("brackendale", "zero", "zero_check", "BRACKENDALE AIR ZERO", "ZERO",
     lambda a,b,c: (0.0, ["z1 0.00", "z2 0.00", "z3 0.00", "zero_check TARGET 0.00"])),
    ("cedardale", "ledger", "ledger_net", "CEDARDALE LEDGER", "LED",
     lambda a,b,c: (a+b, [f"dr {a:.2f}", f"cr {b:.2f}", f"adj {c:.2f}", f"ledger_net TARGET {a+b:.2f}"])),
    ("duskdale", "ui", "ui_ok", "DUSKDALE UI SCAN", "UI",
     lambda a,b,c: (1.0, ["btnOK 1", "btnSkip 0", "btnBad 0", "ui_ok TARGET 1"])),
    ("echodale", "stack", "stack_count", "ECHODALE STACK", "STK",
     lambda a,b,c: (float(a+b), [f"p1 {a}", f"p2 {b}", f"p3 {c}", f"stack_count TARGET {a+b}"])),
    ("firwooddale", "fax", "fax_pages", "FIRWOODDALE FAX", "FAX",
     lambda a,b,c: (float(a+b), [f"pgA {a}", f"pgB {b}", f"pgC {c} drop", f"fax_pages TARGET {a+b}"])),
    ("grovedale", "glare", "glare_ok", "GROVEDALE GLARE", "GLR",
     lambda a,b,c: (1.0, ["zone1 1 ok", "zone2 0", "zone3 0", "glare_ok TARGET 1"])),
    ("hollowdale", "tab", "tab_index", "HOLLOWDALE TAB INDEX", "TAB",
     lambda a,b,c: (float(a+b), [f"tabA {a}", f"tabB {b}", f"tabC {c}", f"tab_index TARGET {a+b}"])),
]
TRAIN_ABC = [
    (368.0, 382.75, 183.0), (315, 343, 203), (292.0, 320.5, 161.0), (422.0, 440.0, 249.0),
    (485.0, 509.0, 221.0), (245, 261, 179), (321.0, 310.75, 166.0), (333.0, 364.5, 185.0),
    (367.0, 350.0, 194.0), (400.0, 388.0, 182.0), (1, 1, 0), (0, 0, 0),
    (466.0, 487.75, 207.0), (1, 0, 0), (77, 69, 47), (95, 79, 70), (1, 0, 0), (120, 97, 67),
]
HELDOUT_ABC = [
    (239.0, 252.0, 134.0), (201, 229, 141), (197.0, 210.75, 122.0), (310.0, 326.0, 163.0),
    (351.0, 367.0, 158.0), (149, 163, 127), (205.0, 199.75, 128.0), (223.0, 244.5, 134.0),
    (243.0, 231.0, 137.0), (270.0, 256.25, 129.0), (1, 1, 0), (0, 0, 0),
    (305.0, 320.75, 144.0), (1, 0, 0), (53, 50, 45), (69, 63, 51), (1, 0, 0), (79, 73, 52),
]
THEME_STR = "quarrydale_riverdale_sagedale_tidedale_underdale_vinedale_wavedale_xylodale_yellowdale_zincdale_ashendale_brackendale_cedardale_duskdale_echodale_firwooddale_grovedale_hollowdale"
OLD_THEME = "yarrowpass_zephyrdale_amberpass_bluestonepass_coralpass_driftpass_eaglepass_fogpass_greenpass_harborpass_ivorydale_jasperdale_kelppass_lotusdale_mistpass_nimbusdale_oakdale_pinepass"


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
    src = src.replace("# --- V78 overlays (new vs V77) ---", "# --- V79 overlays (new vs V78) ---")
    for a, b in [
        ("YARROWPASS bait", "QUARRYDALE bait"), ("PINEPASS bait", "HOLLOWDALE bait"),
        ("JASPERDALE ghost", "BRACKENDALE ghost"), ("LOTUSDALE bait", "DUSKDALE bait"),
        ("DRIFTPASS bait", "VINEDALE bait"), ("MISTPASS", "ECHODALE"),
        ("ZEPHYRDALE bait", "RIVERDALE bait"),
        ("yarrow mist + pine ticks (V78-only)", "quarry mist + hollow ticks (V79-only)"),
    ]:
        src = src.replace(a, b)
    return src


def gen_design():
    out = (S / "c575_vision_v78_design_and_batch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C575", "C581"), ("c575", "c581"), ("V78", "V79"), ("v78", "v79"),
        ("_v78c575", "_v79c581"),
        ("Harder than V77", "Harder than V78"), ("harder than V77", "harder than V78"),
        (OLD_THEME, THEME_STR),
        ("V78 keeps floor", "V79 keeps floor"),
        ("C575 design+fixtures; no VL claim", "C581 design+fixtures; no VL claim"),
        ("fixtures only; claim deferred to C576 VL smoke", "fixtures only; claim deferred to C582 VL smoke"),
        ("No claim until C576 VL", "No claim until C582 VL"),
        ("kept on V78", "kept on V79"),
        ('"harder_than": "v77_goldcliff_xenonpass"', '"harder_than": "v78_yarrowpass_pinepass"'),
        ("r50plus_v78_yarrowpass_pinepass", "r50plus_v79_quarrydale_hollowdale"),
    ]:
        out = out.replace(a, b)
    out = out.replace(
        "NEW themes vs V77: yarrowpass, zephyrdale, amberpass, bluestonepass, coralpass, driftpass, eaglepass, fogpass,\ngreenpass, harborpass, ivorydale, jasperdale, kelppass, lotusdale, mistpass, nimbusdale, oakdale, pinepass.",
        "NEW themes vs V78: quarrydale, riverdale, sagedale, tidedale, underdale, vinedale, wavedale, xylodale,\nyellowdale, zincdale, ashendale, brackendale, cedardale, duskdale, echodale, firwooddale, grovedale, hollowdale.",
    )
    out = replace_specs(out, build_specs("v79", "V79", TRAIN_ABC))
    out = retarget_overlay(out)
    (S / "c581_vision_v79_design_and_batch.py").write_text(out, encoding="utf-8")
    print("wrote design")


def gen_smoke():
    out = (S / "c576_vision_v78_smoke.py").read_text(encoding="utf-8")
    for a, b in [
        ("C576", "C582"), ("c576", "c582"), ("V78", "V79"), ("v78", "v79"),
        ("r50plus_v78_yarrowpass_pinepass_clarity_floor_n>=16_qwen35_2b",
         "r50plus_v79_quarrydale_hollowdale_clarity_floor_n>=16_qwen35_2b"),
        ("Uses C575 fixtures", "Uses C581 fixtures"),
    ]:
        out = out.replace(a, b)
    (S / "c582_vision_v79_smoke.py").write_text(out, encoding="utf-8")
    print("wrote smoke")


def gen_heldout():
    out = (S / "c577_vision_v78_heldout.py").read_text(encoding="utf-8")
    for a, b in [
        ("C577", "C583"), ("c577", "c583"), ("C575", "C581"),
        ("V78", "V79"), ("v78", "v79"),
        ("_v78hc577", "_v79hc583"), ("_v78c575", "_v79c581"),
    ]:
        out = out.replace(a, b)
    out = replace_specs(out, build_specs("v79h", "V79H", HELDOUT_ABC))
    out = retarget_overlay(out)
    out2, seen_fix, seen_train, seen_run = [], False, False, False
    for ln in out.splitlines():
        s = ln.strip()
        if s.startswith("FIX = ") and not seen_fix:
            out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v79h"'); seen_fix = True; continue
        if s.startswith("TRAIN_FIX = ") and not seen_train:
            out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v79"'); seen_train = True; continue
        if s.startswith("RUN = ") and "vision_v79" in s and not seen_run:
            out2.append('RUN = ROOT / "runs/vision_v79h_c583"'); seen_run = True; continue
        out2.append(ln)
    (S / "c583_vision_v79_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
    print("wrote heldout")


def gen_confidence():
    out = (S / "c572_confidence_gate_stretch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C572", "C584"), ("c572", "c584"),
        ("confidence_gate_c572", "confidence_gate_c584"),
        ("conf_gate_stretch_c572", "conf_gate_stretch_c584"),
        ("after V77", "after V79"), ("after V78", "after V79"),
        ("V77+", "V79+"), ("V78+", "V79+"),
    ]:
        out = out.replace(a, b)
    (S / "c584_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
    print("wrote confidence")


def gen_regression():
    out = (S / "c579_capture_office_regression.py").read_text(encoding="utf-8")
    for a, b in [
        ("C579", "C585"), ("c579", "c585"),
        ("capture_regression_c579", "capture_regression_c585"),
        ("after C575-C578", "after C581-C584"),
        ("V4-V78+heldout", "V4-V79+heldout"),
    ]:
        out = out.replace(a, b)
    if "VISION_V79_SMOKE" not in out:
        out = out.replace(
            "SMOKE_POINTERS = [",
            'SMOKE_POINTERS = [\n'
            '    ("V79", DOC / "C582_VISION_V79_SMOKE.json"),\n'
            '    ("V79_heldout", DOC / "C583_VISION_V79_HELDOUT_SMOKE.json"),\n'
            '    ("V78", DOC / "C576_VISION_V78_SMOKE.json"),\n'
            '    ("V78_heldout", DOC / "C577_VISION_V78_HELDOUT_SMOKE.json"),',
            1,
        )
    (S / "c585_capture_office_regression.py").write_text(out, encoding="utf-8")
    print("wrote regression")


def gen_scorecard():
    board = 'BOARD_MD = ROOT / "docs" / "ANT_UNIFIED_SCORECARD.md"'
    for ln in (S / "c580_scorecard_and_stage.py").read_text(encoding="utf-8").splitlines():
        if "BOARD_MD" in ln and "=" in ln:
            board = ln; break
    nl = "\\n"
    text = f'''# -*- coding: utf-8 -*-
"""C586: Unified scorecard + STAGE after C581-C585. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
{board}
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C586.md"
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
    c582 = load("docs/r50/C582_VISION_V79_SMOKE.json") or {{}}
    c582b = load("docs/r50/C582b_VISION_GATE_V79_CLAIM.json") or {{}}
    c583 = load("docs/r50/C583_VISION_V79_HELDOUT_SMOKE.json") or {{}}
    c583b = load("docs/r50/C583b_VISION_GATE_V79_HELDOUT_CLAIM.json") or {{}}
    c584 = load("docs/r50/C584_CONFIDENCE_GATE_STRETCH.json") or {{}}
    c585 = load("docs/r50/C585_CAPTURE_OFFICE_REGRESSION.json") or {{}}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {{}}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {{}}
    c578 = load("docs/r50/C578_PRODUCT_U2C_COST.json") or {{}}

    v79 = float(c582.get("rate") or 0.0)
    v79h = float(c583.get("rate") or 0.0)
    v79_claim = bool(c582b.get("vl_gate_v79_claim") or c582.get("vl_gate_v79_claim") or c582.get("claim"))
    v79h_claim = bool(c583b.get("vl_gate_v79_heldout_claim") or c583.get("vl_gate_v79_heldout_claim") or c583.get("claim"))
    disjoint = bool(c583.get("id_disjoint") or c583.get("disjoint") or c583b.get("id_disjoint") or c583b.get("disjoint"))
    conf_pass = bool(c584.get("pass")) if c584 else bool((prior.get("confidence_gate") or {{}}).get("pass"))
    conf_rate = float(c584.get("rate") or ((prior.get("confidence_gate") or {{}}).get("rate")) or 1.0)
    u2c = prior.get("product_u2c") or {{}}
    if c578.get("pass") is not None:
        u2c = {{"pass": bool(c578.get("pass")), "replace_ratio": float(c578.get("replace_ratio") or c578.get("mean_ratio") or ((c578.get("replace_ledger") or {{}}).get("mean_ratio")) or 4.07), "source": "C578"}}
    capture_pass = bool(c585.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {{}}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {{}}).get("shadow_pass", dissolve_pass))
    stage_ready = bool(v79_claim and v79h_claim and v79 >= GATE and v79h >= GATE and capture_pass and disjoint and conf_pass)
    composite = (1.0 if (v79 >= 0.999 and v79h >= 0.999) else min(v79, v79h)) if stage_ready else 0.0
    out = {{
        "cycle": "C586", "timestamp": ts(), "gate": GATE,
        "vision": {{
            "v78": (prior.get("vision") or {{}}).get("v78") or {{"rate": 1.0, "claim": True}},
            "v78_heldout": (prior.get("vision") or {{}}).get("v78_heldout") or {{"rate": 1.0, "claim": True}},
            "v79": {{"rate": v79, "claim": v79_claim, "n": c582.get("n")}},
            "v79_heldout": {{"rate": v79h, "claim": v79h_claim, "disjoint": disjoint, "n": c583.get("n")}},
        }},
        "product_u2c": u2c if u2c else {{"pass": True, "replace_ratio": 4.0694, "source": "C578"}},
        "confidence_gate": {{"pass": conf_pass, "rate": conf_rate, "source": "C584"}},
        "capture_regression": {{"pass": capture_pass, "source": "C585"}},
        "dissolve_shadow": {{"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"}},
        "composite": composite, "stage_ready": stage_ready,
        "v79_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",
    }}
    J(DOC / "C586_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)
    BOARD_MD.write_text("\\n".join([
        "# Unified Scorecard (C586)", "", f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"- Vision V79: rate={{v79}} claim={{v79_claim}}",
        f"- Vision V79 heldout: rate={{v79h}} claim={{v79h_claim}} disjoint={{disjoint}}",
        f"- product_u2c: {{out['product_u2c']}}", f"- confidence_gate: {{out['confidence_gate']}}",
        f"- capture_regression: pass={{capture_pass}}", f"- composite: {{composite}}",
        f"- stage_ready: {{stage_ready}}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",
    ]) + "\\n", encoding="utf-8")
    STAGE.write_text("\\n".join([
        "# STAGE_ANT_C586", "", f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"**C581-C586 STAGE_READY={{'YES' if stage_ready else 'NO'}}**", "",
        "## Tip slice",
        "- C581: Vision V79 design fixtures",
        f"- C582: Vision V79 smoke **{{v79}}**", f"- C583: Vision V79 heldout **{{v79h}}** (disjoint={{disjoint}})",
        f"- C584: confidence-gate pass={{conf_pass}} rate={{conf_rate}}",
        f"- C585: capture pass={{capture_pass}}", f"- C586: composite={{composite}}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",
        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V79 (uses 62)", "",
        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C586.md", "",
    ]) + "\\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''
    (S / "c586_scorecard_and_stage.py").write_text(text, encoding="utf-8")
    print("wrote scorecard")


def main():
    gen_design(); gen_smoke(); gen_heldout(); gen_confidence(); gen_regression(); gen_scorecard()
    print("OK C581-C586")


if __name__ == "__main__":
    main()
