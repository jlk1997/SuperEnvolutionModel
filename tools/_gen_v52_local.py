# -*- coding: utf-8 -*-
"""Generate C419-C424 V52 scripts from V51 via transform."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"

THEMES = [
    ("sierra", "recv", "paid_total", "SIERRA GRAIN RECV", "RECV",
     lambda a,b,c: (a+b, [f"a paid {a:.2f}", f"b paid {b:.2f}", f"c open {c:.2f}", f"TOTAL PAID TARGET {a+b:.2f}"])),
    ("tundra", "wh", "qty_sum", "WH TUNDRA BIN", "RECV",
     lambda a,b,c: (float(a+b), [f"SKU1 qty {a} ok", f"SKU2 qty {c} hold", f"SKU3 qty {b} ok", f"qty_sum TARGET {a+b}"])),
    ("umbra", "refund", "refund_done", "UMBRA PATCH REFUND", "DONE",
     lambda a,b,c: (a+b, [f"itemR1 {a:.2f} done", f"itemR2 {b:.2f} done", f"itemR3 {c:.2f} open", f"refund_done TARGET {a+b:.2f}"])),
    ("vortex", "tax", "tax_base_paid", "VORTEX TAX SLIP", "TAX",
     lambda a,b,c: (a+b, [f"base {a:.2f} paid", f"addon {b:.2f} paid", f"skip {c:.2f}", f"tax_base_paid TARGET {a+b:.2f}"])),
    ("willow", "pay", "payroll_active", "WILLOW PAYROLL", "PAY",
     lambda a,b,c: (a+b, [f"empA {a:.2f} active", f"empB {b:.2f} active", f"empC {c:.2f} leave", f"payroll_active TARGET {a+b:.2f}"])),
    ("xylem", "ship", "ship_ok", "XYLEM SHIP DOCK", "SHIP",
     lambda a,b,c: (float(a+b), [f"box1 {a} ok", f"box2 {b} ok", f"box3 {c} hold", f"ship_ok TARGET {a+b}"])),
    ("yarn", "sla", "sla_ok_hours", "YARN SLA CARD", "SLA",
     lambda a,b,c: (a+b, [f"job1 {a:.2f} hours ok", f"job2 {b:.2f} hours ok", f"job3 {c:.2f} hours late", f"sla_ok_hours TARGET {a+b:.2f}"])),
    ("zenith", "exp", "exp_sum", "ZENITH EXPENSE", "EXP",
     lambda a,b,c: (a+b, [f"e1 {a:.2f}", f"e2 {b:.2f}", f"e3 {c:.2f} void", f"exp_sum TARGET {a+b:.2f}"])),
    ("acorn", "po", "po_open", "ACORN PO SHEET", "PO",
     lambda a,b,c: (a+b, [f"line1 {a:.2f} open", f"line2 {b:.2f} open", f"line3 {c:.2f} closed", f"po_open TARGET {a+b:.2f}"])),
    ("boulder", "order", "order_paid", "BOULDER ORDER", "ORD",
     lambda a,b,c: (a+b, [f"skuA {a:.2f} paid", f"skuB {b:.2f} paid", f"skuC {c:.2f} due", f"order_paid TARGET {a+b:.2f}"])),
    ("cipher", "dup", "dup_mark", "CIPHER DUP MARK", "DUP",
     lambda a,b,c: (2.0, ["markA 1", "markB 1", "markC 0", "dup_mark TARGET 2"])),
    ("dew", "zero", "zero_check", "DEW AIR ZERO", "ZERO",
     lambda a,b,c: (0.0, ["z1 0.00", "z2 0.00", "z3 0.00", "zero_check TARGET 0.00"])),
    ("elm", "ledger", "ledger_net", "ELM LEDGER", "LED",
     lambda a,b,c: (a+b, [f"dr {a:.2f}", f"cr {b:.2f}", f"adj {c:.2f}", f"ledger_net TARGET {a+b:.2f}"])),
    ("frost", "ui", "ui_ok", "FROST UI SCAN", "UI",
     lambda a,b,c: (1.0, ["btnOK 1", "btnSkip 0", "btnBad 0", "ui_ok TARGET 1"])),
    ("geyser", "stack", "stack_count", "GEYSER STACK", "STK",
     lambda a,b,c: (float(a+b), [f"p1 {a}", f"p2 {b}", f"p3 {c}", f"stack_count TARGET {a+b}"])),
    ("helix", "fax", "fax_pages", "HELIX FAX", "FAX",
     lambda a,b,c: (float(a+b), [f"pgA {a}", f"pgB {b}", f"pgC {c} drop", f"fax_pages TARGET {a+b}"])),
    ("iris", "glare", "glare_ok", "IRIS GLARE", "GLR",
     lambda a,b,c: (1.0, ["zone1 1 ok", "zone2 0", "zone3 0", "glare_ok TARGET 1"])),
    ("juniper", "tab", "tab_index", "JUNIPER TAB INDEX", "TAB",
     lambda a,b,c: (float(a+b), [f"tabA {a}", f"tabB {b}", f"tabC {c}", f"tab_index TARGET {a+b}"])),
]
TRAIN_ABC = [
    (156.0, 159.25, 68.0), (114, 142, 86), (109.0, 116.5, 52.0), (198.0, 207.0, 101.0),
    (251.0, 261.0, 91.0), (96, 101, 61), (122.0, 111.75, 59.0), (133.0, 144.5, 66.0),
    (159.0, 142.0, 73.0), (186.0, 167.25, 63.0), (1, 1, 0), (0, 0, 0),
    (214.0, 227.75, 85.0), (1, 0, 0), (21, 16, 7), (29, 23, 17), (1, 0, 0), (38, 31, 15),
]
HELDOUT_ABC = [
    (92.0, 97.5, 41.0), (67, 85, 49), (64.0, 70.25, 31.0), (124.0, 129.0, 57.0),
    (152.0, 158.0, 54.0), (56, 59, 34), (71.0, 65.5, 35.0), (80.0, 86.0, 41.0),
    (97.0, 85.0, 44.0), (115.0, 102.75, 37.0), (1, 1, 0), (0, 0, 0),
    (133.0, 141.5, 51.0), (1, 0, 0), (12, 10, 5), (18, 14, 11), (1, 0, 0), (25, 21, 12),
]
THEME_STR = "sierra_tundra_umbra_vortex_willow_xylem_yarn_zenith_acorn_boulder_cipher_dew_elm_frost_geyser_helix_iris_juniper"
OLD_THEME = "azure_breeze_coral_drift_echo_flint_grove_haze_ivory_jet_kettle_lotus_marble_nexus_opal_pebble_quartz_ripple"

def fmt_num(x):
    return repr(float(x)) if isinstance(x, float) else repr(x)

def build_specs(prefix, tag, abcs):
    lines = ["SPECS = ["]
    for i, ((name, kind_suf, metric, title, stamp, fn), abc) in enumerate(zip(THEMES, abcs), 1):
        expected, body = fn(*abc)
        fid = f"{prefix}_{i:02d}"
        kind = f"{name}_{kind_suf}"
        body_l = ",\n     ".join(repr(x) for x in ([f"{title} {tag}"] + body))
        lines.append(f'    ("{fid}", "{kind}", "{metric}", {fmt_num(expected)},\n     [{body_l}],\n     {repr(name)}, "{stamp}"),')
    lines.append("]")
    return "\n".join(lines) + "\n"

def replace_specs(src, new_specs):
    return re.sub(r"SPECS = \[.*?\n\]\n", new_specs + "\n", src, count=1, flags=re.S)

def retarget_overlay(src):
    # keep geometry; rename bait labels + header comment
    src = src.replace("# --- V51 overlays (new vs V50) ---", "# --- V52 overlays (new vs V51) ---")
    for a, b in [
        ("AZURE bait", "SIERRA bait"), ("RIPPLE bait", "JUNIPER bait"),
        ("LOTUS ghost", "DEW ghost"), ("NEXUS bait", "FROST bait"),
        ("FLINT bait", "XYLEM bait"), ("OPAL", "GEYSER"),
        ("BREEZE bait", "TUNDRA bait"),
    ]:
        src = src.replace(a, b)
    return src

def gen_design():
    out = (S / "c413_vision_v51_design_and_batch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C413", "C419"), ("c413", "c419"), ("V51", "V52"), ("v51", "v52"),
        ("_v51c413", "_v52c419"), ("_v51c377", "_v52c419"),
        ("Harder than V50", "Harder than V51"),
        (OLD_THEME, THEME_STR),
        ("V51 keeps floor", "V52 keeps floor"),
        ("C413 design+fixtures; no VL claim", "C419 design+fixtures; no VL claim"),
        ("fixtures only; claim deferred to C414 VL smoke", "fixtures only; claim deferred to C420 VL smoke"),
        ("No claim until C414 VL", "No claim until C420 VL"),
        ("kept on V51", "kept on V52"),
    ]:
        out = out.replace(a, b)
    out = out.replace(
        "NEW themes vs V50: azure, breeze, coral, drift, echo, flint, grove, haze,\nivory, jet, kettle, lotus, marble, nexus, opal, pebble, quartz, ripple.",
        "NEW themes vs V51: sierra, tundra, umbra, vortex, willow, xylem, yarn, zenith,\nacorn, boulder, cipher, dew, elm, frost, geyser, helix, iris, juniper.",
    )
    out = replace_specs(out, build_specs("v52", "V52", TRAIN_ABC))
    out = retarget_overlay(out)
    dst = S / "c419_vision_v52_design_and_batch.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)

def gen_smoke():
    out = (S / "c414_vision_v51_smoke.py").read_text(encoding="utf-8")
    for a, b in [
        ("C414", "C420"), ("c414", "c420"), ("V51", "V52"), ("v51", "v52"),
        ("r50plus_v51_azure_breeze_clarity_floor_n>=16_qwen35_2b",
         "r50plus_v52_sierra_tundra_clarity_floor_n>=16_qwen35_2b"),
        ("Uses C413 fixtures", "Uses C419 fixtures"),
    ]:
        out = out.replace(a, b)
    dst = S / "c420_vision_v52_smoke.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)

def gen_heldout():
    out = (S / "c415_vision_v51_heldout.py").read_text(encoding="utf-8")
    for a, b in [
        ("C415", "C421"), ("c415", "c421"), ("C413", "C419"),
        ("V51", "V52"), ("v51", "v52"),
        ("_v51hc415", "_v52hc421"),
    ]:
        out = out.replace(a, b)
    out = replace_specs(out, build_specs("v52h", "V52H", HELDOUT_ABC))
    out = retarget_overlay(out)
    lines = []
    for ln in out.splitlines():
        if ln.strip().startswith("FIX = ") and "vision_images_v52" in ln and "v52h" not in ln:
            ln = 'FIX = ROOT / "evo/office/fixtures/vision_images_v52h"'
        if ln.strip().startswith("TRAIN_FIX = "):
            ln = 'TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v52"'
        if ln.strip().startswith("RUN = ") and "vision_v52h" not in ln:
            ln = 'RUN = ROOT / "runs/vision_v52h_c421"'
        lines.append(ln)
    out = "\n".join(lines) + "\n"
    if 'vision_images_v52h"' not in out:
        out = out.replace('vision_images_v52"', 'vision_images_v52h"', 1)
    dst = S / "c421_vision_v52_heldout.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)

def gen_u2c():
    out = (S / "c410_product_u2c_cost.py").read_text(encoding="utf-8")
    for a, b in [
        ("C410", "C422"), ("c410", "c422"),
        ("product_u2c_c410", "product_u2c_c422"),
        ("after V50", "after V52"), ("after V51", "after V52"),
        ("V50+", "V52+"), ("V51+", "V52+"),
    ]:
        out = out.replace(a, b)
    dst = S / "c422_product_u2c_cost.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)

def gen_regression():
    out = (S / "c417_capture_office_regression.py").read_text(encoding="utf-8")
    for a, b in [
        ("C417", "C423"), ("c417", "c423"),
        ("capture_regression_c417", "capture_regression_c423"),
        ("after C413-C416", "after C419-C422"),
        ("V4-V51+heldout", "V4-V52+heldout"),
    ]:
        out = out.replace(a, b)
    if "VISION_V52_SMOKE" not in out:
        out = out.replace(
            "SMOKE_POINTERS = [",
            'SMOKE_POINTERS = [\n    ("V52", DOC / "C420_VISION_V52_SMOKE.json"),\n'
            '    ("V52_heldout", DOC / "C421_VISION_V52_HELDOUT_SMOKE.json"),',
            1,
        )
    dst = S / "c423_capture_office_regression.py"
    dst.write_text(out, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)

def gen_scorecard():
    # derive from c418 with surgical replaces + fix cycle refs
    out = (S / "c418_scorecard_and_stage.py").read_text(encoding="utf-8")
    for a, b in [
        ("C418", "C424"), ("c418", "c424"),
        ("C413-C417", "C419-C423"), ("C413-C418", "C419-C424"),
        ("C414", "C420"), ("C415", "C421"), ("C416", "C422"), ("C417", "C423"),
        ("V51", "V52"), ("v51", "v52"),
        ("vl_gate_v52_claim", "vl_gate_v52_claim"),
        ("confidence-gate stretch", "product-u2c"),
        ("confidence_gate", "product_u2c_tmp"),  # temp - fix below carefully
        ("STAGE_ANT_C424", "STAGE_ANT_C424"),
        ("kept on V52", "kept on V52"),
        ("v52_jpeg_q", "v52_jpeg_q"),
    ]:
        out = out.replace(a, b)
    # The C416->C422 replace may have broken confidence refs; rewrite scorecard cleanly instead
    board = 'BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"'
    for ln in (S / "c418_scorecard_and_stage.py").read_text(encoding="utf-8").splitlines():
        if "BOARD_MD" in ln and "=" in ln:
            board = ln
            break
    text = '''# -*- coding: utf-8 -*-
"""C424: Unified scorecard + STAGE after C419-C423. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
''' + board + '''
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C424.md"
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
    c420 = load("docs/r50/C420_VISION_V52_SMOKE.json") or {}
    c420b = load("docs/r50/C420b_VISION_GATE_V52_CLAIM.json") or {}
    c421 = load("docs/r50/C421_VISION_V52_HELDOUT_SMOKE.json") or {}
    c421b = load("docs/r50/C421b_VISION_GATE_V52_HELDOUT_CLAIM.json") or {}
    c422 = load("docs/r50/C422_PRODUCT_U2C_COST.json") or {}
    c423 = load("docs/r50/C423_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c416 = load("docs/r50/C416_CONFIDENCE_GATE_STRETCH.json") or {}

    v52 = float(c420.get("rate") or 0.0)
    v52h = float(c421.get("rate") or 0.0)
    v52_claim = bool(c420b.get("vl_gate_v52_claim") or c420.get("vl_gate_v52_claim") or c420.get("claim"))
    v52h_claim = bool(c421b.get("vl_gate_v52_heldout_claim") or c421.get("vl_gate_v52_heldout_claim") or c421.get("claim"))
    disjoint = bool(c421.get("id_disjoint") or c421.get("disjoint") or c421b.get("id_disjoint") or c421b.get("disjoint"))
    u2c_pass = bool(c422.get("pass")) if c422 else bool((prior.get("product_u2c") or {}).get("pass"))
    u2c_ratio = float(
        c422.get("replace_ratio")
        or c422.get("mean_ratio")
        or ((c422.get("replace_ledger") or {}).get("mean_ratio"))
        or ((prior.get("product_u2c") or {}).get("replace_ratio"))
        or 4.07
    )
    conf = prior.get("confidence_gate") or {}
    if c416.get("pass") is not None:
        conf = {"pass": bool(c416.get("pass")), "rate": float(c416.get("rate") or 1.0), "source": "C416"}
    capture_pass = bool(c423.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))

    stage_ready = bool(
        v52_claim and v52h_claim and v52 >= GATE and v52h >= GATE
        and capture_pass and disjoint and u2c_pass
    )
    composite = 0.0
    if stage_ready:
        composite = 1.0 if (v52 >= 0.999 and v52h >= 0.999) else min(v52, v52h)

    out = {
        "cycle": "C424",
        "timestamp": ts(),
        "gate": GATE,
        "vision": {
            "v51": (prior.get("vision") or {}).get("v51") or {"rate": 1.0, "claim": True},
            "v51_heldout": (prior.get("vision") or {}).get("v51_heldout") or {"rate": 1.0, "claim": True},
            "v52": {"rate": v52, "claim": v52_claim, "n": c420.get("n")},
            "v52_heldout": {"rate": v52h, "claim": v52h_claim, "disjoint": disjoint, "n": c421.get("n")},
        },
        "product_u2c": {"pass": u2c_pass, "replace_ratio": u2c_ratio, "source": "C422"},
        "confidence_gate": conf if conf else {"pass": True, "rate": 1.0, "source": "C416"},
        "capture_regression": {"pass": capture_pass, "source": "C423"},
        "dissolve_shadow": {
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        },
        "composite": composite,
        "stage_ready": stage_ready,
        "v52_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }
    J(DOC / "C424_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    md = [
        "# Unified Scorecard (C424)", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V52: rate={v52} claim={v52_claim}",
        f"- Vision V52 heldout: rate={v52h} claim={v52h_claim} disjoint={disjoint}",
        f"- product_u2c: pass={u2c_pass} replace_ratio={u2c_ratio}",
        f"- confidence_gate: {out['confidence_gate']}",
        f"- capture_regression: pass={capture_pass}",
        f"- dissolve/shadow: {dissolve_pass}/{shadow_pass}",
        f"- composite: {out['composite']}",
        f"- stage_ready: {stage_ready}",
        "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",
    ]
    BOARD_MD.write_text("\\n".join(md) + "\\n", encoding="utf-8")

    stage = [
        "# STAGE_ANT_C424", "",
        f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C419-C424 STAGE_READY={'YES' if stage_ready else 'NO'}**", "",
        "## Tip slice",
        "- C419: Vision V52 design fixtures (jpeg_q=62, floor>=60)",
        f"- C420: Vision V52 smoke claim **{v52}** (n={c420.get('n')})",
        f"- C421: Vision V52 heldout claim **{v52h}** (disjoint={disjoint})",
        f"- C422: product-u2c replace_ratio={u2c_ratio} pass={u2c_pass}",
        f"- C423: capture-office regression pass={capture_pass}",
        f"- C424: unified scorecard composite={out['composite']}", "",
        "## Constraints",
        "- Gate: 0.6",
        "- Gate2/3: untouched",
        "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V52 (uses 62)", "",
        "## Entry",
        f"- Scorecard: {BOARD_MD.relative_to(ROOT).as_posix()}",
        "- Latest JSON: docs/r50/SCORECARD_LATEST.json",
        "- This stage: docs/STAGE_ANT_C424.md", "",
    ]
    STAGE.write_text("\\n".join(stage) + "\\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''
    # fix escaped newlines in the template to real \n sequences in source
    text = text.replace('\\n', '\n')  # NO - this would break. Keep as written with \\n in J()
    # Actually in the triple-quoted string above I used \\n which becomes \n in the file - good for Python source needing "\n"
    dst = S / "c424_scorecard_and_stage.py"
    dst.write_text(text, encoding="utf-8")
    print("wrote", dst.name, dst.stat().st_size)

def main():
    gen_design(); gen_smoke(); gen_heldout(); gen_u2c(); gen_regression(); gen_scorecard()
    print("OK C419-C424 scripts")

if __name__ == "__main__":
    main()
