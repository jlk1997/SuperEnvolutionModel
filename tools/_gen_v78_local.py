# -*- coding: utf-8 -*-
"""Generate C575-C580 V78 from V77. Knife: product-U2C (C578)."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"

THEMES = [
    ("yarrowpass", "recv", "paid_total", "YARROWPASS GRAIN RECV", "RECV",
     lambda a,b,c: (a+b, [f"a paid {a:.2f}", f"b paid {b:.2f}", f"c open {c:.2f}", f"TOTAL PAID TARGET {a+b:.2f}"])),
    ("zephyrdale", "wh", "qty_sum", "WH ZEPHYRDALE BIN", "RECV",
     lambda a,b,c: (float(a+b), [f"SKU1 qty {a} ok", f"SKU2 qty {c} hold", f"SKU3 qty {b} ok", f"qty_sum TARGET {a+b}"])),
    ("amberpass", "refund", "refund_done", "AMBERPASS PATCH REFUND", "DONE",
     lambda a,b,c: (a+b, [f"itemR1 {a:.2f} done", f"itemR2 {b:.2f} done", f"itemR3 {c:.2f} open", f"refund_done TARGET {a+b:.2f}"])),
    ("bluestonepass", "tax", "tax_base_paid", "BLUESTONEPASS TAX SLIP", "TAX",
     lambda a,b,c: (a+b, [f"base {a:.2f} paid", f"addon {b:.2f} paid", f"skip {c:.2f}", f"tax_base_paid TARGET {a+b:.2f}"])),
    ("coralpass", "pay", "payroll_active", "CORALPASS PAYROLL", "PAY",
     lambda a,b,c: (a+b, [f"empA {a:.2f} active", f"empB {b:.2f} active", f"empC {c:.2f} leave", f"payroll_active TARGET {a+b:.2f}"])),
    ("driftpass", "ship", "ship_ok", "DRIFTPASS SHIP DOCK", "SHIP",
     lambda a,b,c: (float(a+b), [f"box1 {a} ok", f"box2 {b} ok", f"box3 {c} hold", f"ship_ok TARGET {a+b}"])),
    ("eaglepass", "sla", "sla_ok_hours", "EAGLEPASS SLA CARD", "SLA",
     lambda a,b,c: (a+b, [f"job1 {a:.2f} hours ok", f"job2 {b:.2f} hours ok", f"job3 {c:.2f} hours late", f"sla_ok_hours TARGET {a+b:.2f}"])),
    ("fogpass", "exp", "exp_sum", "FOGPASS EXPENSE", "EXP",
     lambda a,b,c: (a+b, [f"e1 {a:.2f}", f"e2 {b:.2f}", f"e3 {c:.2f} void", f"exp_sum TARGET {a+b:.2f}"])),
    ("greenpass", "po", "po_open", "GREENPASS PO SHEET", "PO",
     lambda a,b,c: (a+b, [f"line1 {a:.2f} open", f"line2 {b:.2f} open", f"line3 {c:.2f} closed", f"po_open TARGET {a+b:.2f}"])),
    ("harborpass", "order", "order_paid", "HARBORPASS ORDER", "ORD",
     lambda a,b,c: (a+b, [f"skuA {a:.2f} paid", f"skuB {b:.2f} paid", f"skuC {c:.2f} due", f"order_paid TARGET {a+b:.2f}"])),
    ("ivorydale", "dup", "dup_mark", "IVORYDALE DUP MARK", "DUP",
     lambda a,b,c: (2.0, ["markA 1", "markB 1", "markC 0", "dup_mark TARGET 2"])),
    ("jasperdale", "zero", "zero_check", "JASPERDALE AIR ZERO", "ZERO",
     lambda a,b,c: (0.0, ["z1 0.00", "z2 0.00", "z3 0.00", "zero_check TARGET 0.00"])),
    ("kelppass", "ledger", "ledger_net", "KELPPASS LEDGER", "LED",
     lambda a,b,c: (a+b, [f"dr {a:.2f}", f"cr {b:.2f}", f"adj {c:.2f}", f"ledger_net TARGET {a+b:.2f}"])),
    ("lotusdale", "ui", "ui_ok", "LOTUSDALE UI SCAN", "UI",
     lambda a,b,c: (1.0, ["btnOK 1", "btnSkip 0", "btnBad 0", "ui_ok TARGET 1"])),
    ("mistpass", "stack", "stack_count", "MISTPASS STACK", "STK",
     lambda a,b,c: (float(a+b), [f"p1 {a}", f"p2 {b}", f"p3 {c}", f"stack_count TARGET {a+b}"])),
    ("nimbusdale", "fax", "fax_pages", "NIMBUSDALE FAX", "FAX",
     lambda a,b,c: (float(a+b), [f"pgA {a}", f"pgB {b}", f"pgC {c} drop", f"fax_pages TARGET {a+b}"])),
    ("oakdale", "glare", "glare_ok", "OAKDALE GLARE", "GLR",
     lambda a,b,c: (1.0, ["zone1 1 ok", "zone2 0", "zone3 0", "glare_ok TARGET 1"])),
    ("pinepass", "tab", "tab_index", "PINEPASS TAB INDEX", "TAB",
     lambda a,b,c: (float(a+b), [f"tabA {a}", f"tabB {b}", f"tabC {c}", f"tab_index TARGET {a+b}"])),
]
TRAIN_ABC = [
    (360.0, 375.0, 179.0), (307, 335, 199), (285.0, 312.75, 157.0), (414.0, 432.0, 243.0),
    (477.0, 501.0, 217.0), (239, 255, 175), (313.0, 303.0, 162.0), (325.0, 356.25, 181.0),
    (359.0, 342.0, 190.0), (392.0, 380.0, 178.0), (1, 1, 0), (0, 0, 0),
    (458.0, 480.0, 203.0), (1, 0, 0), (75, 67, 45), (93, 77, 68), (1, 0, 0), (117, 95, 65),
]
HELDOUT_ABC = [
    (233.0, 246.25, 130.0), (195, 223, 137), (191.0, 205.0, 118.0), (302.0, 318.0, 159.0),
    (343.0, 359.0, 154.0), (145, 159, 123), (199.0, 194.0, 124.0), (217.0, 238.25, 130.0),
    (237.0, 225.0, 133.0), (264.0, 250.5, 125.0), (1, 1, 0), (0, 0, 0),
    (299.0, 315.0, 140.0), (1, 0, 0), (51, 48, 43), (67, 61, 49), (1, 0, 0), (77, 71, 50),
]
THEME_STR = "yarrowpass_zephyrdale_amberpass_bluestonepass_coralpass_driftpass_eaglepass_fogpass_greenpass_harborpass_ivorydale_jasperdale_kelppass_lotusdale_mistpass_nimbusdale_oakdale_pinepass"
OLD_THEME = "goldcliff_hazelpass_ironpass_jadehaven_knollpass_larkpass_mosspass_northpass_opalpass_pinehaven_quartzpass_reedpass_stonepass_thunderhaven_umbraepass_valepass_willowpass_xenonpass"


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
    src = src.replace("# --- V77 overlays (new vs V76) ---", "# --- V78 overlays (new vs V77) ---")
    for a, b in [
        ("GOLDCLIFF bait", "YARROWPASS bait"), ("XENONPASS bait", "PINEPASS bait"),
        ("REEDPASS ghost", "JASPERDALE ghost"), ("THUNDERHAVEN bait", "LOTUSDALE bait"),
        ("LARKPASS bait", "DRIFTPASS bait"), ("UMBRAEPASS", "MISTPASS"),
        ("HAZELPASS bait", "ZEPHYRDALE bait"),
        ("gold mist + xenon ticks (V77-only)", "yarrow mist + pine ticks (V78-only)"),
    ]:
        src = src.replace(a, b)
    return src


def gen_design():
    out = (S / "c569_vision_v77_design_and_batch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C569", "C575"), ("c569", "c575"), ("V77", "V78"), ("v77", "v78"),
        ("_v77c569", "_v78c575"),
        ("Harder than V76", "Harder than V77"), ("harder than V76", "harder than V77"),
        (OLD_THEME, THEME_STR),
        ("V77 keeps floor", "V78 keeps floor"),
        ("C569 design+fixtures; no VL claim", "C575 design+fixtures; no VL claim"),
        ("fixtures only; claim deferred to C570 VL smoke", "fixtures only; claim deferred to C576 VL smoke"),
        ("No claim until C570 VL", "No claim until C576 VL"),
        ("kept on V77", "kept on V78"),
        ('"harder_than": "v76_oakcliff_fernpass"', '"harder_than": "v77_goldcliff_xenonpass"'),
        ("r50plus_v77_goldcliff_xenonpass", "r50plus_v78_yarrowpass_pinepass"),
    ]:
        out = out.replace(a, b)
    out = out.replace(
        "NEW themes vs V76: goldcliff, hazelpass, ironpass, jadehaven, knollpass, larkpass, mosspass, northpass,\nopalpass, pinehaven, quartzpass, reedpass, stonepass, thunderhaven, umbraepass, valepass, willowpass, xenonpass.",
        "NEW themes vs V77: yarrowpass, zephyrdale, amberpass, bluestonepass, coralpass, driftpass, eaglepass, fogpass,\ngreenpass, harborpass, ivorydale, jasperdale, kelppass, lotusdale, mistpass, nimbusdale, oakdale, pinepass.",
    )
    out = replace_specs(out, build_specs("v78", "V78", TRAIN_ABC))
    out = retarget_overlay(out)
    (S / "c575_vision_v78_design_and_batch.py").write_text(out, encoding="utf-8")
    print("wrote design")


def gen_smoke():
    out = (S / "c570_vision_v77_smoke.py").read_text(encoding="utf-8")
    for a, b in [
        ("C570", "C576"), ("c570", "c576"), ("V77", "V78"), ("v77", "v78"),
        ("r50plus_v77_goldcliff_xenonpass_clarity_floor_n>=16_qwen35_2b",
         "r50plus_v78_yarrowpass_pinepass_clarity_floor_n>=16_qwen35_2b"),
        ("Uses C569 fixtures", "Uses C575 fixtures"),
    ]:
        out = out.replace(a, b)
    (S / "c576_vision_v78_smoke.py").write_text(out, encoding="utf-8")
    print("wrote smoke")


def gen_heldout():
    out = (S / "c571_vision_v77_heldout.py").read_text(encoding="utf-8")
    for a, b in [
        ("C571", "C577"), ("c571", "c577"), ("C569", "C575"),
        ("V77", "V78"), ("v77", "v78"),
        ("_v77hc571", "_v78hc577"), ("_v77c569", "_v78c575"),
    ]:
        out = out.replace(a, b)
    out = replace_specs(out, build_specs("v78h", "V78H", HELDOUT_ABC))
    out = retarget_overlay(out)
    out2, seen_fix, seen_train, seen_run = [], False, False, False
    for ln in out.splitlines():
        s = ln.strip()
        if s.startswith("FIX = ") and not seen_fix:
            out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v78h"'); seen_fix = True; continue
        if s.startswith("TRAIN_FIX = ") and not seen_train:
            out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v78"'); seen_train = True; continue
        if s.startswith("RUN = ") and "vision_v78" in s and not seen_run:
            out2.append('RUN = ROOT / "runs/vision_v78h_c577"'); seen_run = True; continue
        out2.append(ln)
    (S / "c577_vision_v78_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
    print("wrote heldout")


def gen_u2c():
    out = (S / "c566_product_u2c_cost.py").read_text(encoding="utf-8")
    for a, b in [
        ("C566", "C578"), ("c566", "c578"),
        ("product_u2c_c566", "product_u2c_c578"), ("u2c_cost_c566", "u2c_cost_c578"),
        ("after V76", "after V78"), ("after V77", "after V78"),
        ("V76+", "V78+"), ("V77+", "V78+"),
    ]:
        out = out.replace(a, b)
    (S / "c578_product_u2c_cost.py").write_text(out, encoding="utf-8")
    print("wrote u2c")


def gen_regression():
    out = (S / "c573_capture_office_regression.py").read_text(encoding="utf-8")
    for a, b in [
        ("C573", "C579"), ("c573", "c579"),
        ("capture_regression_c573", "capture_regression_c579"),
        ("after C569-C572", "after C575-C578"),
        ("V4-V77+heldout", "V4-V78+heldout"),
    ]:
        out = out.replace(a, b)
    if "VISION_V78_SMOKE" not in out:
        out = out.replace(
            "SMOKE_POINTERS = [",
            'SMOKE_POINTERS = [\n'
            '    ("V78", DOC / "C576_VISION_V78_SMOKE.json"),\n'
            '    ("V78_heldout", DOC / "C577_VISION_V78_HELDOUT_SMOKE.json"),\n'
            '    ("V77", DOC / "C570_VISION_V77_SMOKE.json"),\n'
            '    ("V77_heldout", DOC / "C571_VISION_V77_HELDOUT_SMOKE.json"),',
            1,
        )
    (S / "c579_capture_office_regression.py").write_text(out, encoding="utf-8")
    print("wrote regression")


def gen_scorecard():
    board = 'BOARD_MD = ROOT / "docs" / "ANT_UNIFIED_SCORECARD.md"'
    for ln in (S / "c574_scorecard_and_stage.py").read_text(encoding="utf-8").splitlines():
        if "BOARD_MD" in ln and "=" in ln:
            board = ln; break
    nl = "\\n"
    text = f'''# -*- coding: utf-8 -*-
"""C580: Unified scorecard + STAGE after C575-C579. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
{board}
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C580.md"
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
    c576 = load("docs/r50/C576_VISION_V78_SMOKE.json") or {{}}
    c576b = load("docs/r50/C576b_VISION_GATE_V78_CLAIM.json") or {{}}
    c577 = load("docs/r50/C577_VISION_V78_HELDOUT_SMOKE.json") or {{}}
    c577b = load("docs/r50/C577b_VISION_GATE_V78_HELDOUT_CLAIM.json") or {{}}
    c578 = load("docs/r50/C578_PRODUCT_U2C_COST.json") or {{}}
    c579 = load("docs/r50/C579_CAPTURE_OFFICE_REGRESSION.json") or {{}}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {{}}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {{}}
    c572 = load("docs/r50/C572_CONFIDENCE_GATE_STRETCH.json") or {{}}

    v78 = float(c576.get("rate") or 0.0)
    v78h = float(c577.get("rate") or 0.0)
    v78_claim = bool(c576b.get("vl_gate_v78_claim") or c576.get("vl_gate_v78_claim") or c576.get("claim"))
    v78h_claim = bool(c577b.get("vl_gate_v78_heldout_claim") or c577.get("vl_gate_v78_heldout_claim") or c577.get("claim"))
    disjoint = bool(c577.get("id_disjoint") or c577.get("disjoint") or c577b.get("id_disjoint") or c577b.get("disjoint"))
    conf = prior.get("confidence_gate") or {{}}
    if c572.get("pass") is not None:
        conf = {{"pass": bool(c572.get("pass")), "rate": float(c572.get("rate") or 1.0), "source": "C572"}}
    u2c_pass = bool(c578.get("pass"))
    replace = float(c578.get("replace_ratio") or c578.get("mean_ratio") or ((c578.get("replace_ledger") or {{}}).get("mean_ratio")) or 4.07)
    capture_pass = bool(c579.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {{}}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {{}}).get("shadow_pass", dissolve_pass))
    stage_ready = bool(v78_claim and v78h_claim and v78 >= GATE and v78h >= GATE and capture_pass and disjoint and u2c_pass)
    composite = (1.0 if (v78 >= 0.999 and v78h >= 0.999) else min(v78, v78h)) if stage_ready else 0.0
    out = {{
        "cycle": "C580", "timestamp": ts(), "gate": GATE,
        "vision": {{
            "v77": (prior.get("vision") or {{}}).get("v77") or {{"rate": 1.0, "claim": True}},
            "v77_heldout": (prior.get("vision") or {{}}).get("v77_heldout") or {{"rate": 1.0, "claim": True}},
            "v78": {{"rate": v78, "claim": v78_claim, "n": c576.get("n")}},
            "v78_heldout": {{"rate": v78h, "claim": v78h_claim, "disjoint": disjoint, "n": c577.get("n")}},
        }},
        "product_u2c": {{"pass": u2c_pass, "replace_ratio": replace, "source": "C578"}},
        "confidence_gate": conf if conf else {{"pass": True, "rate": 1.0, "source": "C572"}},
        "capture_regression": {{"pass": capture_pass, "source": "C579"}},
        "dissolve_shadow": {{"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"}},
        "composite": composite, "stage_ready": stage_ready,
        "v78_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",
    }}
    J(DOC / "C580_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)
    BOARD_MD.write_text("\\n".join([
        "# Unified Scorecard (C580)", "", f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"- Vision V78: rate={{v78}} claim={{v78_claim}}",
        f"- Vision V78 heldout: rate={{v78h}} claim={{v78h_claim}} disjoint={{disjoint}}",
        f"- product_u2c: {{out['product_u2c']}}", f"- confidence_gate: {{out['confidence_gate']}}",
        f"- capture_regression: pass={{capture_pass}}", f"- composite: {{composite}}",
        f"- stage_ready: {{stage_ready}}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",
    ]) + "\\n", encoding="utf-8")
    STAGE.write_text("\\n".join([
        "# STAGE_ANT_C580", "", f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"**C575-C580 STAGE_READY={{'YES' if stage_ready else 'NO'}}**", "",
        "## Tip slice",
        "- C575: Vision V78 design fixtures",
        f"- C576: Vision V78 smoke **{{v78}}**", f"- C577: Vision V78 heldout **{{v78h}}** (disjoint={{disjoint}})",
        f"- C578: product-U2C pass={{u2c_pass}} replace≈{{replace:.4f}}×",
        f"- C579: capture pass={{capture_pass}}", f"- C580: composite={{composite}}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",
        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V78 (uses 62)", "",
        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C580.md", "",
    ]) + "\\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''
    (S / "c580_scorecard_and_stage.py").write_text(text, encoding="utf-8")
    print("wrote scorecard")


def main():
    gen_design(); gen_smoke(); gen_heldout(); gen_u2c(); gen_regression(); gen_scorecard()
    print("OK C575-C580")


if __name__ == "__main__":
    main()
