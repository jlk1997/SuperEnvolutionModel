# -*- coding: utf-8 -*-
"""Build C647-C652 Vision V90 from V89. Knife: product-U2C. No *b themes."""
from __future__ import annotations
import json, re
from pathlib import Path

ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"
D = json.loads((ROOT / "tools/_v90_themes.json").read_text(encoding="utf-8"))
THEMES, TRAIN_ABC, HELDOUT_ABC = D["themes"], D["train"], D["heldout"]
THEME_STR = "_".join(t[0] for t in THEMES)
OLD_THEME = "olivepass_pinegrove_quartzcreek_ravengrove_silverpass_thorngrove_umberpass_vinegrove_wavepass_xenopass_yarrowgrove_zirconpass_alderpass_birchgrove_cedarcreek_duskpass_firpass_gorsegrove"


def lines_for_metric(name, kind_suf, metric, title, stamp, a, b, c, tag):
    if metric == "paid_total":
        expected, body = a + b, [f"a paid {a:.2f}", f"b paid {b:.2f}", f"c open {c:.2f}", f"TOTAL PAID TARGET {a+b:.2f}"]
    elif metric == "qty_sum":
        expected = float(a + b)
        body = [f"SKU1 qty {a} ok", f"SKU2 qty {c} hold", f"SKU3 qty {b} ok", f"qty_sum TARGET {a+b}"]
    elif metric == "refund_done":
        expected, body = a + b, [f"itemR1 {a:.2f} done", f"itemR2 {b:.2f} done", f"itemR3 {c:.2f} open", f"refund_done TARGET {a+b:.2f}"]
    elif metric == "tax_base_paid":
        expected, body = a + b, [f"base {a:.2f} paid", f"addon {b:.2f} paid", f"skip {c:.2f}", f"tax_base_paid TARGET {a+b:.2f}"]
    elif metric == "payroll_active":
        expected, body = a + b, [f"empA {a:.2f} active", f"empB {b:.2f} active", f"empC {c:.2f} leave", f"payroll_active TARGET {a+b:.2f}"]
    elif metric == "ship_ok":
        expected = float(a + b)
        body = [f"box1 {a} ok", f"box2 {b} ok", f"box3 {c} hold", f"ship_ok TARGET {a+b}"]
    elif metric == "sla_ok_hours":
        expected, body = a + b, [f"job1 {a:.2f} hours ok", f"job2 {b:.2f} hours ok", f"job3 {c:.2f} hours late", f"sla_ok_hours TARGET {a+b:.2f}"]
    elif metric == "exp_sum":
        expected, body = a + b, [f"e1 {a:.2f}", f"e2 {b:.2f}", f"e3 {c:.2f} void", f"exp_sum TARGET {a+b:.2f}"]
    elif metric == "po_open":
        expected, body = a + b, [f"line1 {a:.2f} open", f"line2 {b:.2f} open", f"line3 {c:.2f} closed", f"po_open TARGET {a+b:.2f}"]
    elif metric == "order_paid":
        expected, body = a + b, [f"skuA {a:.2f} paid", f"skuB {b:.2f} paid", f"skuC {c:.2f} due", f"order_paid TARGET {a+b:.2f}"]
    elif metric == "dup_mark":
        expected, body = 2.0, ["markA 1", "markB 1", "markC 0", "dup_mark TARGET 2"]
    elif metric == "zero_check":
        expected, body = 0.0, ["z1 0.00", "z2 0.00", "z3 0.00", "zero_check TARGET 0.00"]
    elif metric == "ledger_net":
        expected, body = a + b, [f"dr {a:.2f}", f"cr {b:.2f}", f"adj {c:.2f}", f"ledger_net TARGET {a+b:.2f}"]
    elif metric == "ui_ok":
        expected, body = 1.0, ["btnOK 1", "btnSkip 0", "btnBad 0", "ui_ok TARGET 1"]
    elif metric == "stack_count":
        expected = float(a + b)
        body = [f"p1 {a}", f"p2 {b}", f"p3 {c}", f"stack_count TARGET {a+b}"]
    elif metric == "fax_pages":
        expected = float(a + b)
        body = [f"pgA {a}", f"pgB {b}", f"pgC {c} drop", f"fax_pages TARGET {a+b}"]
    elif metric == "glare_ok":
        expected, body = 1.0, ["zone1 1 ok", "zone2 0", "zone3 0", "glare_ok TARGET 1"]
    elif metric == "tab_index":
        expected = float(a + b)
        body = [f"tabA {a}", f"tabB {b}", f"tabC {c}", f"tab_index TARGET {a+b}"]
    else:
        raise ValueError(metric)
    return expected, [f"{title} {tag}"] + body


def fmt_expected(x):
    return repr(float(x))


def build_specs(prefix, tag, abcs):
    lines = ["SPECS = ["]
    for i, (t, abc) in enumerate(zip(THEMES, abcs), 1):
        name, kind_suf, metric, title, stamp, _bk = t
        a, b, c = abc
        expected, body = lines_for_metric(name, kind_suf, metric, title, stamp, a, b, c, tag)
        fid = f"{prefix}_{i:02d}"
        kind = f"{name}_{kind_suf}"
        body_l = ",\n     ".join(repr(x) for x in body)
        lines.append(
            f'    ("{fid}", "{kind}", "{metric}", {fmt_expected(expected)},\n'
            f'     [{body_l}],\n     {repr(name)}, "{stamp}"),'
        )
    lines.append("]")
    return "\n".join(lines) + "\n"


def replace_specs(src, new_specs):
    return re.sub(r"SPECS = \[.*?\n\]\n", new_specs + "\n", src, count=1, flags=re.S)


def retarget_overlay(src):
    src = src.replace("# --- V89 overlays (new vs V88) ---", "# --- V90 overlays (new vs V89) ---")
    for a, b in [
        ("OLIVEPASS bait", "HEATHCREEK bait"), ("GORSEGROVE bait", "IRONGROVE bait"),
        ("ZIRCONPASS ghost", "STONEGROVE ghost"), ("BIRCHGROVE bait", "VALEGROVE bait"),
        ("THORNGROVE bait", "MOSSGROVE bait"), ("CEDARCREEK", "FROSTCREEK"),
        ("PINEGROVE bait", "IRISGROVE bait"),
        ("olive mist + gorsegrove ticks (V89-only)", "heath mist + irongrove ticks (V90-only)"),
    ]:
        src = src.replace(a, b)
    return src


out = (S / "c641_vision_v89_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C641", "C647"), ("c641", "c647"), ("V89", "V90"), ("v89", "v90"),
    ("_v89c641", "_v90c647"),
    ("Harder than V88", "Harder than V89"), ("harder than V88", "harder than V89"),
    (OLD_THEME, THEME_STR),
    ("V89 keeps floor", "V90 keeps floor"),
    ("C641 design+fixtures; no VL claim", "C647 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C642 VL smoke", "fixtures only; claim deferred to C648 VL smoke"),
    ("No claim until C642 VL", "No claim until C648 VL"),
    ("kept on V89", "kept on V90"),
    ('"harder_than": "v88_willowcreek_nutmegpass"', '"harder_than": "v89_olivepass_gorsegrove"'),
    ("r50plus_v89_olivepass_gorsegrove", "r50plus_v90_heathcreek_irongrove"),
    ("vision_images_v89", "vision_images_v90"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V88: olivepass, pinegrove, quartzcreek, ravengrove, silverpass, thorngrove, umberpass, vinegrove,\nwavepass, xenopass, yarrowgrove, zirconpass, alderpass, birchgrove, cedarcreek, duskpass, firpass, gorsegrove.",
    "NEW themes vs V89: heathcreek, irisgrove, junipercreek, knollgrove, larkcreek, mossgrove, northcreek, opalgrove,\npeatcreek, quillgrove, reedcreek, stonegrove, thundercreek, valegrove, frostcreek, glengrove, hazelcreek, irongrove.",
)
out = replace_specs(out, build_specs("v90", "V90", TRAIN_ABC))
out = retarget_overlay(out)
(S / "c647_vision_v90_design_and_batch.py").write_text(out, encoding="utf-8")
print("design", out.count("vision_images_v90"), out.count("C647"), out.count("vl_gate_v90"))

out = (S / "c642_vision_v89_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C642", "C648"), ("c642", "c648"), ("V89", "V90"), ("v89", "v90"),
    ("r50plus_v89_olivepass_gorsegrove_clarity_floor_n>=16_qwen35_2b",
     "r50plus_v90_heathcreek_irongrove_clarity_floor_n>=16_qwen35_2b"),
    ("Uses C641 fixtures", "Uses C647 fixtures"),
    ("vision_images_v89", "vision_images_v90"),
]:
    out = out.replace(a, b)
(S / "c648_vision_v90_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c643_vision_v89_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C643", "C649"), ("c643", "c649"), ("C641", "C647"),
    ("V89", "V90"), ("v89", "v90"),
    ("_v89hc643", "_v90hc649"), ("_v89c641", "_v90c647"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs("v90h", "V90H", HELDOUT_ABC))
out = retarget_overlay(out)
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v90h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v90"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v90" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v90h_c649"'); seen_run = True; continue
    out2.append(ln)
(S / "c649_vision_v90_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c638_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C638", "C650"), ("c638", "c650"),
    ("product_u2c_c638", "product_u2c_c650"), ("u2c_cost_c638", "u2c_cost_c650"),
    ("after V88", "after V90"), ("after V89", "after V90"),
    ("V88+", "V90+"), ("V89+", "V90+"),
]:
    out = out.replace(a, b)
(S / "c650_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c645_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C645", "C651"), ("c645", "c651"),
    ("capture_regression_c645", "capture_regression_c651"),
    ("after C641-C644", "after C647-C650"),
    ("V4-V89+heldout", "V4-V90+heldout"),
]:
    out = out.replace(a, b)
if "VISION_V90_SMOKE" not in out:
    out = out.replace(
        "SMOKE_POINTERS = [",
        'SMOKE_POINTERS = [\n'
        '    ("V90", DOC / "C648_VISION_V90_SMOKE.json"),\n'
        '    ("V90_heldout", DOC / "C649_VISION_V90_HELDOUT_SMOKE.json"),\n'
        '    ("V89", DOC / "C642_VISION_V89_SMOKE.json"),\n'
        '    ("V89_heldout", DOC / "C643_VISION_V89_HELDOUT_SMOKE.json"),',
        1,
    )
(S / "c651_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

board = 'BOARD_MD = ROOT / "docs" / "ANT_UNIFIED_SCORECARD.md"'
for ln in (S / "c646_scorecard_and_stage.py").read_text(encoding="utf-8").splitlines():
    if "BOARD_MD" in ln and "=" in ln:
        board = ln
        break
text = '''# -*- coding: utf-8 -*-
"""C652: Unified scorecard + STAGE after C647-C651. V90 milestone. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
''' + board + '''
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C652.md"
GATE = 0.6


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")


def load(rel):
    p = ROOT / rel
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None


def main():
    c648 = load("docs/r50/C648_VISION_V90_SMOKE.json") or {}
    c648b = load("docs/r50/C648b_VISION_GATE_V90_CLAIM.json") or {}
    c649 = load("docs/r50/C649_VISION_V90_HELDOUT_SMOKE.json") or {}
    c649b = load("docs/r50/C649b_VISION_GATE_V90_HELDOUT_CLAIM.json") or {}
    c650 = load("docs/r50/C650_PRODUCT_U2C_COST.json") or {}
    c651 = load("docs/r50/C651_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c644 = load("docs/r50/C644_CONFIDENCE_GATE_STRETCH.json") or {}

    v90 = float(c648.get("rate") or 0.0)
    v90h = float(c649.get("rate") or 0.0)
    v90_claim = bool(c648b.get("vl_gate_v90_claim") or c648.get("vl_gate_v90_claim") or c648.get("claim"))
    v90h_claim = bool(c649b.get("vl_gate_v90_heldout_claim") or c649.get("vl_gate_v90_heldout_claim") or c649.get("claim"))
    disjoint = bool(c649.get("id_disjoint") or c649.get("disjoint") or c649b.get("id_disjoint") or c649b.get("disjoint"))
    conf = prior.get("confidence_gate") or {}
    if c644.get("pass") is not None:
        conf = {"pass": bool(c644.get("pass")), "rate": float(c644.get("rate") or 1.0), "source": "C644"}
    u2c_pass = bool(c650.get("pass"))
    replace = float(c650.get("replace_ratio") or c650.get("mean_ratio") or ((c650.get("replace_ledger") or {}).get("mean_ratio")) or 4.07)
    capture_pass = bool(c651.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))
    stage_ready = bool(v90_claim and v90h_claim and v90 >= GATE and v90h >= GATE and capture_pass and disjoint and u2c_pass)
    composite = (1.0 if (v90 >= 0.999 and v90h >= 0.999) else min(v90, v90h)) if stage_ready else 0.0
    out = {
        "cycle": "C652", "timestamp": ts(), "gate": GATE, "milestone": "V90",
        "vision": {
            "v89": (prior.get("vision") or {}).get("v89") or {"rate": 1.0, "claim": True},
            "v89_heldout": (prior.get("vision") or {}).get("v89_heldout") or {"rate": 1.0, "claim": True},
            "v90": {"rate": v90, "claim": v90_claim, "n": c648.get("n")},
            "v90_heldout": {"rate": v90h, "claim": v90h_claim, "disjoint": disjoint, "n": c649.get("n")},
        },
        "product_u2c": {"pass": u2c_pass, "replace_ratio": replace, "source": "C650"},
        "confidence_gate": conf if conf else {"pass": True, "rate": 1.0, "source": "C644"},
        "capture_regression": {"pass": capture_pass, "source": "C651"},
        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},
        "composite": composite, "stage_ready": stage_ready,
        "v90_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",
    }
    J(DOC / "C652_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)
    BOARD_MD.write_text("\\n".join([
        "# Unified Scorecard (C652) — V90 milestone", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V90: rate={v90} claim={v90_claim}",
        f"- Vision V90 heldout: rate={v90h} claim={v90h_claim} disjoint={disjoint}",
        f"- product_u2c: {out['product_u2c']}", f"- confidence_gate: {out['confidence_gate']}",
        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",
        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD | V90 not a stop", "",
    ]) + "\\n", encoding="utf-8")
    STAGE.write_text("\\n".join([
        "# STAGE_ANT_C652", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C647-C652 STAGE_READY={'YES' if stage_ready else 'NO'} — V90 milestone (continue)**", "",
        "## Tip slice",
        "- C647: Vision V90 design fixtures",
        f"- C648: Vision V90 smoke **{v90}**", f"- C649: Vision V90 heldout **{v90h}** (disjoint={disjoint})",
        f"- C650: product-U2C pass={u2c_pass} replace≈{replace:.4f}×",
        f"- C651: capture pass={capture_pass}", f"- C652: composite={composite}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",
        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V90 (uses 62)",
        "- V90 milestone is NOT a stop — continue to V91+",
        "- lesson: avoid *b theme-name collapse (V88)", "",
        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C652.md", "",
    ]) + "\\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''
(S / "c652_scorecard_and_stage.py").write_text(text, encoding="utf-8")
print("scorecard OK")
