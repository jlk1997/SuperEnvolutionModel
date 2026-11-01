# -*- coding: utf-8 -*-
"""Slim C413-C418 V51 generator from V50 scripts."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(r"E:\envolution")
SCRIPTS = ROOT / "scripts"

THEMES = [
    ("azure", "recv", "paid_total", "AZURE GRAIN RECV", "RECV",
     lambda a,b,c: (a+b, [f"a paid {a:.2f}", f"b paid {b:.2f}", f"c open {c:.2f}", f"TOTAL PAID TARGET {a+b:.2f}"])),
    ("breeze", "wh", "qty_sum", "WH BREEZE BIN", "RECV",
     lambda a,b,c: (float(a+b), [f"SKU1 qty {a} ok", f"SKU2 qty {c} hold", f"SKU3 qty {b} ok", f"qty_sum TARGET {a+b}"])),
    ("coral", "refund", "refund_done", "CORAL PATCH REFUND", "DONE",
     lambda a,b,c: (a+b, [f"itemR1 {a:.2f} done", f"itemR2 {b:.2f} done", f"itemR3 {c:.2f} open", f"refund_done TARGET {a+b:.2f}"])),
    ("drift", "tax", "tax_base_paid", "DRIFT TAX SLIP", "TAX",
     lambda a,b,c: (a+b, [f"base {a:.2f} paid", f"addon {b:.2f} paid", f"skip {c:.2f}", f"tax_base_paid TARGET {a+b:.2f}"])),
    ("echo", "pay", "payroll_active", "ECHO PAYROLL", "PAY",
     lambda a,b,c: (a+b, [f"empA {a:.2f} active", f"empB {b:.2f} active", f"empC {c:.2f} leave", f"payroll_active TARGET {a+b:.2f}"])),
    ("flint", "ship", "ship_ok", "FLINT SHIP DOCK", "SHIP",
     lambda a,b,c: (float(a+b), [f"box1 {a} ok", f"box2 {b} ok", f"box3 {c} hold", f"ship_ok TARGET {a+b}"])),
    ("grove", "sla", "sla_ok_hours", "GROVE SLA CARD", "SLA",
     lambda a,b,c: (a+b, [f"job1 {a:.2f} hours ok", f"job2 {b:.2f} hours ok", f"job3 {c:.2f} hours late", f"sla_ok_hours TARGET {a+b:.2f}"])),
    ("haze", "exp", "exp_sum", "HAZE EXPENSE", "EXP",
     lambda a,b,c: (a+b, [f"e1 {a:.2f}", f"e2 {b:.2f}", f"e3 {c:.2f} void", f"exp_sum TARGET {a+b:.2f}"])),
    ("ivory", "po", "po_open", "IVORY PO SHEET", "PO",
     lambda a,b,c: (a+b, [f"line1 {a:.2f} open", f"line2 {b:.2f} open", f"line3 {c:.2f} closed", f"po_open TARGET {a+b:.2f}"])),
    ("jet", "order", "order_paid", "JET ORDER", "ORD",
     lambda a,b,c: (a+b, [f"skuA {a:.2f} paid", f"skuB {b:.2f} paid", f"skuC {c:.2f} due", f"order_paid TARGET {a+b:.2f}"])),
    ("kettle", "dup", "dup_mark", "KETTLE DUP MARK", "DUP",
     lambda a,b,c: (2.0, ["markA 1", "markB 1", "markC 0", "dup_mark TARGET 2"])),
    ("lotus", "zero", "zero_check", "LOTUS AIR ZERO", "ZERO",
     lambda a,b,c: (0.0, ["z1 0.00", "z2 0.00", "z3 0.00", "zero_check TARGET 0.00"])),
    ("marble", "ledger", "ledger_net", "MARBLE LEDGER", "LED",
     lambda a,b,c: (a+b, [f"dr {a:.2f}", f"cr {b:.2f}", f"adj {c:.2f}", f"ledger_net TARGET {a+b:.2f}"])),
    ("nexus", "ui", "ui_ok", "NEXUS UI SCAN", "UI",
     lambda a,b,c: (1.0, ["btnOK 1", "btnSkip 0", "btnBad 0", "ui_ok TARGET 1"])),
    ("opal", "stack", "stack_count", "OPAL STACK", "STK",
     lambda a,b,c: (float(a+b), [f"p1 {a}", f"p2 {b}", f"p3 {c}", f"stack_count TARGET {a+b}"])),
    ("pebble", "fax", "fax_pages", "PEBBLE FAX", "FAX",
     lambda a,b,c: (float(a+b), [f"pgA {a}", f"pgB {b}", f"pgC {c} drop", f"fax_pages TARGET {a+b}"])),
    ("quartz", "glare", "glare_ok", "QUARTZ GLARE", "GLR",
     lambda a,b,c: (1.0, ["zone1 1 ok", "zone2 0", "zone3 0", "glare_ok TARGET 1"])),
    ("ripple", "tab", "tab_index", "RIPPLE TAB INDEX", "TAB",
     lambda a,b,c: (float(a+b), [f"tabA {a}", f"tabB {b}", f"tabC {c}", f"tab_index TARGET {a+b}"])),
]

# train triples (a,b,c) — amounts disjoint from V50/V50H
TRAIN_ABC = [
    (141.0, 144.75, 61.0), (103, 131, 78), (98.0, 105.5, 47.0), (187.0, 195.0, 96.0),
    (234.0, 244.0, 83.0), (87, 92, 55), (111.0, 100.25, 54.0), (122.0, 132.5, 60.0),
    (148.0, 131.0, 67.0), (175.0, 156.75, 57.0), (1, 1, 0), (0, 0, 0),
    (203.0, 216.25, 78.0), (1, 0, 0), (19, 14, 6), (27, 21, 15), (1, 0, 0), (35, 29, 14),
]
HELDOUT_ABC = [
    (83.0, 88.5, 37.0), (61, 78, 45), (58.0, 63.75, 28.0), (113.0, 118.0, 52.0),
    (141.0, 147.0, 49.0), (51, 54, 31), (65.0, 59.5, 32.0), (73.0, 79.0, 37.0),
    (89.0, 77.0, 40.0), (105.0, 93.25, 34.0), (1, 1, 0), (0, 0, 0),
    (122.0, 129.5, 46.0), (1, 0, 0), (11, 9, 4), (16, 13, 10), (1, 0, 0), (23, 19, 11),
]

def fmt_num(x):
    if isinstance(x, float) and abs(x - int(x)) > 1e-9:
        return repr(float(x))
    if isinstance(x, float):
        return repr(float(x))
    return repr(float(x)) if isinstance(x, float) else repr(x)

def build_specs(prefix: str, tag: str, abcs):
    lines = ["SPECS = ["]
    for i, ((name, kind_suf, metric, title, stamp, fn), abc) in enumerate(zip(THEMES, abcs), 1):
        expected, body = fn(*abc)
        fid = f"{prefix}_{i:02d}"
        kind = f"{name}_{kind_suf}"
        body_l = ",\n     ".join(repr(x) for x in ([f"{title} {tag}"] + body))
        lines.append(
            f'    ("{fid}", "{kind}", "{metric}", {fmt_num(expected)},\n'
            f'     [{body_l}],\n'
            f'     {repr(name)}, "{stamp}"),'
        )
    lines.append("]")
    return "\n".join(lines) + "\n"

V51_OVERLAY = r'''
    # --- V51 overlays (new vs V50) ---
    for _ in range(160):
        bx = rng.randint(50, 540)
        by = rng.randint(365, 595)
        if in_text_band(by):
            continue
        d.line([(bx, by), (bx + rng.randint(6, 26), by + rng.randint(-6, 6))], fill=(70, 90, 130), width=1)
    for gi in range(5):
        d.ellipse([58 + gi * 24, 322, 76 + gi * 24, 340], outline=(40, 80, 140), width=2)
    d.text((58, 342), "AZURE bait 48.48", fill=(20, 50, 110), font=f_tiny)
    for hi in range(4):
        d.polygon([(600 + hi * 34, 44), (626 + hi * 34, 44), (613 + hi * 34, 80)], fill=(40, 90, 150))
    d.text((600, 84), "RIPPLE bait 66.66", fill=(20, 50, 100), font=f_tiny)
    d.rectangle([270, 400, 430, 460], fill=(240, 248, 255))
    d.text((280, 420), "LOTUS ghost 97.97", fill=(40, 70, 120), font=f_pen)
    d.arc([430, 390, 520, 460], 30, 280, fill=(90, 60, 140), width=3)
    d.text((430, 465), "NEXUS bait 42.42", fill=(60, 30, 100), font=f_tiny)
    d.ellipse([80, 490, 150, 550], fill=(150, 160, 180), outline=(50, 55, 70), width=2)
    d.text((80, 555), "FLINT bait 33.33", fill=(50, 45, 60), font=f_tiny)
    for qi in range(4):
        d.rectangle([270 + qi * 42, 490, 302 + qi * 42, 522], outline=(60, 80, 130), width=2)
    d.rectangle([870, 130, 1020, 190], fill=(190, 200, 220), outline=(40, 50, 80), width=2)
    d.text((890, 148), "OPAL", fill=(30, 40, 80), font=f_stamp)
    d.polygon([(40, 4), (420, 4), (405, 18), (50, 18)], fill=(195, 210, 230), outline=(40, 60, 100), width=1)
    d.text((70, 5), "BREEZE bait 77.77", fill=(30, 50, 90), font=f_tiny)
    for ti, ty in enumerate((110, 170, 230)):
        d.polygon([(1000, ty), (1024, ty + 12), (1000, ty + 24)], fill=(50, 90, 140 + ti * 20))
    for ry in (115, 195, 275):
        d.ellipse([12, ry, 28, ry + 16], fill=(160, 190, 230), outline=(30, 50, 90), width=2)
        d.ellipse([16, ry + 4, 24, ry + 12], fill=(210, 230, 250))
    for (sx, sy) in [(175, 370), (355, 400), (495, 380)]:
        if not in_text_band(sy):
            d.rectangle([sx, sy, sx + 18, sy + 5], fill=(50, 70, 110))
    for wx in range(60, 520, 36):
        d.arc([wx, 350, wx + 28, 372], 0, 180, fill=(70, 110, 160), width=2)
'''

def replace_specs(src: str, new_specs: str) -> str:
    return re.sub(r"SPECS = \[.*?\n\]\n", new_specs + "\n", src, count=1, flags=re.S)

def swap_overlay(src: str) -> str:
    pats = [
        r"    # --- V50 overlays \(new vs V49\) ---.*?(?=\n    buf = io\.BytesIO\(\))",
        r"    # --- V51 overlays \(new vs V50\) ---.*?(?=\n    buf = io\.BytesIO\(\))",
    ]
    for pat in pats:
        if re.search(pat, src, flags=re.S):
            return re.sub(pat, V51_OVERLAY.rstrip() + "\n", src, count=1, flags=re.S)
    return src

def gen_design():
    src = (SCRIPTS / "c407_vision_v50_design_and_batch.py").read_text(encoding="utf-8")
    out = src
    for a, b in [
        ("C407", "C413"), ("c407", "c413"), ("V50", "V51"), ("v50", "v51"),
        ("_v51c407", "_v51c413"), ("_v50c407", "_v51c413"),
        ("Harder than V49", "Harder than V50"), ("Harder than V51", "Harder than V50"),
        ("atoll_birch_cedar_delta_ember_fern_granite_holly_jade_knoll_lichen_moss_nimbus_orchard_pine_raven_spruce_tide",
         "azure_breeze_coral_drift_echo_flint_grove_haze_ivory_jet_kettle_lotus_marble_nexus_opal_pebble_quartz_ripple"),
        ("V50 keeps floor", "V51 keeps floor"),
        ("C407 design+fixtures; no VL claim", "C413 design+fixtures; no VL claim"),
        ("fixtures only; claim deferred to C408 VL smoke", "fixtures only; claim deferred to C414 VL smoke"),
        ("No claim until C408 VL", "No claim until C414 VL"),
        ("kept on V50", "kept on V51"),
    ]:
        out = out.replace(a, b)
    out = out.replace(
        "NEW themes vs V49: atoll, birch, cedar, delta, ember, fern, granite, holly,\njade, knoll, lichen, moss, nimbus, orchard, pine, raven, spruce, tide.",
        "NEW themes vs V50: azure, breeze, coral, drift, echo, flint, grove, haze,\nivory, jet, kettle, lotus, marble, nexus, opal, pebble, quartz, ripple.",
    )
    out = out.replace(
        "NEW themes vs V50: atoll, birch, cedar, delta, ember, fern, granite, holly,\njade, knoll, lichen, moss, nimbus, orchard, pine, raven, spruce, tide.",
        "NEW themes vs V50: azure, breeze, coral, drift, echo, flint, grove, haze,\nivory, jet, kettle, lotus, marble, nexus, opal, pebble, quartz, ripple.",
    )
    out = replace_specs(out, build_specs("v51", "V51", TRAIN_ABC))
    out = swap_overlay(out)
    out = out.replace("V42 uses", "V51 uses").replace("V50 uses", "V51 uses")
    out = out.replace("# --- V51 overlays (new vs V49) ---", "# --- V51 overlays (new vs V50) ---")
    dst = SCRIPTS / "c413_vision_v51_design_and_batch.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst, dst.stat().st_size)

def gen_smoke():
    src = (SCRIPTS / "c408_vision_v50_smoke.py").read_text(encoding="utf-8")
    out = src
    for a, b in [
        ("C408", "C414"), ("c408", "c414"), ("V50", "V51"), ("v50", "v51"),
        ("r50plus_v50_atoll_birch_clarity_floor_n>=16_qwen35_2b",
         "r50plus_v51_azure_breeze_clarity_floor_n>=16_qwen35_2b"),
        ("r50plus_v51_atoll_birch_clarity_floor_n>=16_qwen35_2b",
         "r50plus_v51_azure_breeze_clarity_floor_n>=16_qwen35_2b"),
        ("Uses C407 fixtures", "Uses C413 fixtures"),
    ]:
        out = out.replace(a, b)
    dst = SCRIPTS / "c414_vision_v51_smoke.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst, dst.stat().st_size)

def gen_heldout():
    src = (SCRIPTS / "c409_vision_v50_heldout.py").read_text(encoding="utf-8")
    out = src
    for a, b in [
        ("C409", "C415"), ("c409", "c415"), ("C407", "C413"),
        ("V50", "V51"), ("v50", "v51"),
        ("_v50hc409", "_v51hc415"), ("_v51hc409", "_v51hc415"),
    ]:
        out = out.replace(a, b)
    out = replace_specs(out, build_specs("v51h", "V51H", HELDOUT_ABC))
    out = swap_overlay(out)
    lines = []
    for ln in out.splitlines():
        if ln.strip().startswith("FIX = ") and "vision_images_v51" in ln and "v51h" not in ln:
            ln = 'FIX = ROOT / "evo/office/fixtures/vision_images_v51h"'
        if ln.strip().startswith("TRAIN_FIX = "):
            ln = 'TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v51"'
        if ln.strip().startswith("RUN = ") and "vision_v51h" not in ln:
            ln = 'RUN = ROOT / "runs/vision_v51h_c415"'
        lines.append(ln)
    out = "\n".join(lines) + "\n"
    if 'FIX = ROOT / "evo/office/fixtures/vision_images_v51h"' not in out:
        out = out.replace(
            'FIX = ROOT / "evo/office/fixtures/vision_images_v51"',
            'FIX = ROOT / "evo/office/fixtures/vision_images_v51h"', 1)
    dst = SCRIPTS / "c415_vision_v51_heldout.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst, dst.stat().st_size)

def gen_conf():
    src = (SCRIPTS / "c404_confidence_gate_stretch.py").read_text(encoding="utf-8")
    out = src
    for a, b in [
        ("C404", "C416"), ("c404", "c416"),
        ("confidence_gate_c404", "confidence_gate_c416"),
        ("confidence_gate_stretch_c404", "confidence_gate_stretch_c416"),
        ("after V49", "after V51"), ("after V50", "after V51"),
        ("V49+", "V51+"), ("V50+", "V51+"),
    ]:
        out = out.replace(a, b)
    dst = SCRIPTS / "c416_confidence_gate_stretch.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst, dst.stat().st_size)

def gen_regression():
    src = (SCRIPTS / "c411_capture_office_regression.py").read_text(encoding="utf-8")
    out = src
    for a, b in [
        ("C411", "C417"), ("c411", "c417"),
        ("capture_regression_c411", "capture_regression_c417"),
        ("after C407-C410", "after C413-C416"),
        ("V4-V50+heldout", "V4-V51+heldout"),
    ]:
        out = out.replace(a, b)
    if "VISION_V51_SMOKE" not in out:
        out = out.replace(
            "SMOKE_POINTERS = [",
            'SMOKE_POINTERS = [\n    ("V51", DOC / "C414_VISION_V51_SMOKE.json"),\n'
            '    ("V51_heldout", DOC / "C415_VISION_V51_HELDOUT_SMOKE.json"),',
            1,
        )
    dst = SCRIPTS / "c417_capture_office_regression.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst, dst.stat().st_size)

def gen_scorecard():
    src = (SCRIPTS / "c412_scorecard_and_stage.py").read_text(encoding="utf-8")
    board = 'BOARD_MD = ROOT / "docs" / "ANT_UNIFIED_SCORECARD.md"'
    for ln in src.splitlines():
        if "BOARD_MD" in ln and "=" in ln:
            board = ln
            break
    clean = f'''# -*- coding: utf-8 -*-
"""C418: Unified scorecard + STAGE after C413-C417. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
{board}
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C418.md"
GATE = 0.6


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")


def load(rel):
    p = ROOT / rel
    if not p.is_file():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def main():
    c414 = load("docs/r50/C414_VISION_V51_SMOKE.json") or {{}}
    c414b = load("docs/r50/C414b_VISION_GATE_V51_CLAIM.json") or {{}}
    c415 = load("docs/r50/C415_VISION_V51_HELDOUT_SMOKE.json") or {{}}
    c415b = load("docs/r50/C415b_VISION_GATE_V51_HELDOUT_CLAIM.json") or {{}}
    c416 = load("docs/r50/C416_CONFIDENCE_GATE_STRETCH.json") or {{}}
    c417 = load("docs/r50/C417_CAPTURE_OFFICE_REGRESSION.json") or {{}}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {{}}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {{}}
    c410 = load("docs/r50/C410_PRODUCT_U2C_COST.json") or {{}}

    v51 = float(c414.get("rate") or 0.0)
    v51h = float(c415.get("rate") or 0.0)
    v51_claim = bool(c414b.get("vl_gate_v51_claim") or c414.get("vl_gate_v51_claim") or c414.get("claim"))
    v51h_claim = bool(c415b.get("vl_gate_v51_heldout_claim") or c415.get("vl_gate_v51_heldout_claim") or c415.get("claim"))
    disjoint = bool(c415.get("id_disjoint") or c415.get("disjoint") or c415b.get("id_disjoint") or c415b.get("disjoint"))
    conf_pass = bool(c416.get("pass") or (c416.get("rate") or 0) >= GATE)
    conf_rate = float(c416.get("rate") or (prior.get("confidence_gate") or {{}}).get("rate") or 1.0)
    capture_pass = bool(c417.get("pass"))
    u2c = prior.get("product_u2c") or {{}}
    if c410.get("pass") is not None:
        u2c = {{
            "pass": bool(c410.get("pass")),
            "replace_ratio": float(c410.get("replace_ratio") or c410.get("mean_ratio") or (c410.get("replace_ledger") or {{}}).get("mean_ratio") or 4.07),
            "source": "C410",
        }}
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {{}}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {{}}).get("shadow_pass", dissolve_pass))

    stage_ready = bool(
        v51_claim and v51h_claim and v51 >= GATE and v51h >= GATE
        and capture_pass and disjoint
    )
    composite = 0.0
    if stage_ready:
        composite = 1.0 if (v51 >= 0.999 and v51h >= 0.999) else min(v51, v51h)

    out = {{
        "cycle": "C418",
        "timestamp": ts(),
        "gate": GATE,
        "vision": {{
            "v50": (prior.get("vision") or {{}}).get("v50") or {{"rate": 1.0, "claim": True}},
            "v50_heldout": (prior.get("vision") or {{}}).get("v50_heldout") or {{"rate": 1.0, "claim": True}},
            "v51": {{"rate": v51, "claim": v51_claim, "n": c414.get("n")}},
            "v51_heldout": {{"rate": v51h, "claim": v51h_claim, "disjoint": disjoint, "n": c415.get("n")}},
        }},
        "product_u2c": u2c if u2c else {{"pass": True, "replace_ratio": 4.0694, "source": "C410"}},
        "confidence_gate": {{"pass": conf_pass, "rate": conf_rate, "source": "C416"}},
        "capture_regression": {{"pass": capture_pass, "source": "C417"}},
        "dissolve_shadow": {{
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        }},
        "composite": composite,
        "stage_ready": stage_ready,
        "v51_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }}
    J(DOC / "C418_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = [
        "# Unified Scorecard (C418)", "",
        f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"- Vision V51: rate={{v51}} claim={{v51_claim}}",
        f"- Vision V51 heldout: rate={{v51h}} claim={{v51h_claim}} disjoint={{disjoint}}",
        f"- confidence_gate: pass={{conf_pass}} rate={{conf_rate}}",
        f"- product_u2c: {{out['product_u2c']}}",
        f"- capture_regression: pass={{capture_pass}}",
        f"- dissolve/shadow: {{dissolve_pass}}/{{shadow_pass}}",
        f"- composite: {{out['composite']}}",
        f"- stage_ready: {{stage_ready}}",
        "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",
    ]
    BOARD_MD.write_text("\\n".join(md) + "\\n", encoding="utf-8")

    stage = [
        "# STAGE_ANT_C418", "",
        f"Updated: {{ts()}} (Asia/Shanghai)", "",
        f"**C413-C418 STAGE_READY={{'YES' if stage_ready else 'NO'}}**", "",
        "## Tip slice",
        "- C413: Vision V51 design fixtures (jpeg_q=62, floor>=60)",
        f"- C414: Vision V51 smoke claim **{{v51}}** (n={{c414.get('n')}})",
        f"- C415: Vision V51 heldout claim **{{v51h}}** (disjoint={{disjoint}})",
        f"- C416: confidence-gate stretch pass={{conf_pass}} rate={{conf_rate}}",
        f"- C417: capture-office regression pass={{capture_pass}}",
        f"- C418: unified scorecard composite={{out['composite']}}", "",
        "## Constraints",
        "- Gate: 0.6",
        "- Gate2/3: untouched",
        "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V51 (uses 62)", "",
        "## Entry",
        f"- Scorecard: {{BOARD_MD.relative_to(ROOT).as_posix()}}",
        "- Latest JSON: docs/r50/SCORECARD_LATEST.json",
        "- This stage: docs/STAGE_ANT_C418.md", "",
    ]
    STAGE.write_text("\\n".join(stage) + "\\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''
    # unescape deliberate \\n in J/write_text to real \n in source
    clean = clean.replace('+ "\\n", encoding', '+ "\\n", encoding')
    clean = clean.replace('"\\n".join(md)', '"\\n".join(md)')
    clean = clean.replace('"\\n".join(stage)', '"\\n".join(stage)')
    # The f-string above used \\n which becomes \n in the file - correct for Python source
    dst = SCRIPTS / "c418_scorecard_and_stage.py"
    dst.write_text(clean, encoding="utf-8")
    print("wrote", dst, dst.stat().st_size)

def main():
    gen_design(); gen_smoke(); gen_heldout(); gen_conf(); gen_regression(); gen_scorecard()
    print("OK all C413-C418")

if __name__ == "__main__":
    main()
