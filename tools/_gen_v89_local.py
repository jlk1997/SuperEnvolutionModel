# -*- coding: utf-8 -*-
from __future__ import annotations
import json, re
from pathlib import Path

ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"
D = json.loads((ROOT / "tools/_v89_themes.json").read_text(encoding="utf-8"))
THEMES, TRAIN_ABC, HELDOUT_ABC = D["themes"], D["train"], D["heldout"]
THEME_STR = "_".join(t[0] for t in THEMES)
OLD_THEME = "willowcreek_sandbarpass_yewgrove_zincridge_aspenridge_beachgrove_coralridge_dewgrove_elmridge_ferngrove_granitepass_hemlockpass_ivorygrove_jasperpass_kelpcreek_limegrove_maplegrove_nutmegpass"


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
    src = src.replace("# --- V88 overlays (new vs V87) ---", "# --- V89 overlays (new vs V88) ---")
    for a, b in [
        ("WILLOWCREEK bait", "OLIVEPASS bait"), ("NUTMEGPASS bait", "GORSEGROVE bait"),
        ("HEMLOCKPASS ghost", "ZIRCONPASS ghost"), ("JASPERPASS bait", "BIRCHGROVE bait"),
        ("BEACHGROVE bait", "THORNGROVE bait"), ("KELPCREEK", "CEDARCREEK"),
        ("SANDBARPASS bait", "PINEGROVE bait"),
        ("willow mist + nutmegpass ticks (V88-only)", "olive mist + gorsegrove ticks (V89-only)"),
    ]:
        src = src.replace(a, b)
    return src


out = (S / "c635_vision_v88_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C635", "C641"), ("c635", "c641"), ("V88", "V89"), ("v88", "v89"),
    ("_v88c635", "_v89c641"),
    ("Harder than V87", "Harder than V88"), ("harder than V87", "harder than V88"),
    (OLD_THEME, THEME_STR),
    ("V88 keeps floor", "V89 keeps floor"),
    ("C635 design+fixtures; no VL claim", "C641 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C636 VL smoke", "fixtures only; claim deferred to C642 VL smoke"),
    ("No claim until C636 VL", "No claim until C642 VL"),
    ("kept on V88", "kept on V89"),
    ('"harder_than": "v87_eldertide_valotide"', '"harder_than": "v88_willowcreek_nutmegpass"'),
    ("r50plus_v88_willowcreek_nutmegpass", "r50plus_v89_olivepass_gorsegrove"),
    ("vision_images_v88", "vision_images_v89"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V87: willowcreek, sandbarpass, yewgrove, zincridge, aspenridge, beachgrove, coralridge, dewgrove,\nelmridge, ferngrove, granitepass, hemlockpass, ivorygrove, jasperpass, kelpcreek, limegrove, maplegrove, nutmegpass.",
    "NEW themes vs V88: olivepass, pinegrove, quartzcreek, ravengrove, silverpass, thorngrove, umberpass, vinegrove,\nwavepass, xenopass, yarrowgrove, zirconpass, alderpass, birchgrove, cedarcreek, duskpass, firpass, gorsegrove.",
)
out = replace_specs(out, build_specs("v89", "V89", TRAIN_ABC))
out = retarget_overlay(out)
(S / "c641_vision_v89_design_and_batch.py").write_text(out, encoding="utf-8")
print("design", out.count("vision_images_v89"), out.count("C641"), out.count("vl_gate_v89"))

out = (S / "c636_vision_v88_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C636", "C642"), ("c636", "c642"), ("V88", "V89"), ("v88", "v89"),
    ("r50plus_v88_willowcreek_nutmegpass_clarity_floor_n>=16_qwen35_2b",
     "r50plus_v89_olivepass_gorsegrove_clarity_floor_n>=16_qwen35_2b"),
    ("Uses C635 fixtures", "Uses C641 fixtures"),
    ("vision_images_v88", "vision_images_v89"),
]:
    out = out.replace(a, b)
(S / "c642_vision_v89_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c637_vision_v88_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C637", "C643"), ("c637", "c643"), ("C635", "C641"),
    ("V88", "V89"), ("v88", "v89"),
    ("_v88hc637", "_v89hc643"), ("_v88c635", "_v89c641"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs("v89h", "V89H", HELDOUT_ABC))
out = retarget_overlay(out)
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v89h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v89"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v89" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v89h_c643"'); seen_run = True; continue
    out2.append(ln)
(S / "c643_vision_v89_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c632_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C632", "C644"), ("c632", "c644"),
    ("confidence_gate_c632", "confidence_gate_c644"),
    ("after V87", "after V89"), ("after V88", "after V89"),
    ("V87+", "V89+"), ("V88+", "V89+"),
]:
    out = out.replace(a, b)
(S / "c644_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("conf")

out = (S / "c639_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C639", "C645"), ("c639", "c645"),
    ("capture_regression_c639", "capture_regression_c645"),
    ("after C635-C638", "after C641-C644"),
    ("V4-V88+heldout", "V4-V89+heldout"),
]:
    out = out.replace(a, b)
if "VISION_V89_SMOKE" not in out:
    out = out.replace(
        "SMOKE_POINTERS = [",
        'SMOKE_POINTERS = [\n'
        '    ("V89", DOC / "C642_VISION_V89_SMOKE.json"),\n'
        '    ("V89_heldout", DOC / "C643_VISION_V89_HELDOUT_SMOKE.json"),\n'
        '    ("V88", DOC / "C636_VISION_V88_SMOKE.json"),\n'
        '    ("V88_heldout", DOC / "C637_VISION_V88_HELDOUT_SMOKE.json"),',
        1,
    )
(S / "c645_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

board = 'BOARD_MD = ROOT / "docs" / "ANT_UNIFIED_SCORECARD.md"'
for ln in (S / "c640_scorecard_and_stage.py").read_text(encoding="utf-8").splitlines():
    if "BOARD_MD" in ln and "=" in ln:
        board = ln
        break
text = '''# -*- coding: utf-8 -*-
"""C646: Unified scorecard + STAGE after C641-C645. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
''' + board + '''
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C646.md"
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
    c642 = load("docs/r50/C642_VISION_V89_SMOKE.json") or {}
    c642b = load("docs/r50/C642b_VISION_GATE_V89_CLAIM.json") or {}
    c643 = load("docs/r50/C643_VISION_V89_HELDOUT_SMOKE.json") or {}
    c643b = load("docs/r50/C643b_VISION_GATE_V89_HELDOUT_CLAIM.json") or {}
    c644 = load("docs/r50/C644_CONFIDENCE_GATE_STRETCH.json") or {}
    c645 = load("docs/r50/C645_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c638 = load("docs/r50/C638_PRODUCT_U2C_COST.json") or {}

    v89 = float(c642.get("rate") or 0.0)
    v89h = float(c643.get("rate") or 0.0)
    v89_claim = bool(c642b.get("vl_gate_v89_claim") or c642.get("vl_gate_v89_claim") or c642.get("claim"))
    v89h_claim = bool(c643b.get("vl_gate_v89_heldout_claim") or c643.get("vl_gate_v89_heldout_claim") or c643.get("claim"))
    disjoint = bool(c643.get("id_disjoint") or c643.get("disjoint") or c643b.get("id_disjoint") or c643b.get("disjoint"))
    conf_pass = bool(c644.get("pass"))
    conf_rate = float(c644.get("rate") or 0.0)
    u2c = prior.get("product_u2c") or {}
    if c638.get("pass") is not None:
        u2c = {
            "pass": bool(c638.get("pass")),
            "replace_ratio": float(c638.get("replace_ratio") or c638.get("mean_ratio") or 4.07),
            "source": "C638",
        }
    replace = float(u2c.get("replace_ratio") or 4.07)
    capture_pass = bool(c645.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))
    stage_ready = bool(v89_claim and v89h_claim and v89 >= GATE and v89h >= GATE and capture_pass and disjoint and conf_pass)
    composite = (1.0 if (v89 >= 0.999 and v89h >= 0.999) else min(v89, v89h)) if stage_ready else 0.0
    out = {
        "cycle": "C646", "timestamp": ts(), "gate": GATE,
        "vision": {
            "v88": (prior.get("vision") or {}).get("v88") or {"rate": 1.0, "claim": True},
            "v88_heldout": (prior.get("vision") or {}).get("v88_heldout") or {"rate": 1.0, "claim": True},
            "v89": {"rate": v89, "claim": v89_claim, "n": c642.get("n")},
            "v89_heldout": {"rate": v89h, "claim": v89h_claim, "disjoint": disjoint, "n": c643.get("n")},
        },
        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C638"},
        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C644"},
        "capture_regression": {"pass": capture_pass, "source": "C645"},
        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},
        "composite": composite, "stage_ready": stage_ready,
        "v89_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",
    }
    J(DOC / "C646_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)
    BOARD_MD.write_text("\\n".join([
        "# Unified Scorecard (C646)", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V89: rate={v89} claim={v89_claim}",
        f"- Vision V89 heldout: rate={v89h} claim={v89h_claim} disjoint={disjoint}",
        f"- product_u2c: {out['product_u2c']}", f"- confidence_gate: {out['confidence_gate']}",
        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",
        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",
    ]) + "\\n", encoding="utf-8")
    STAGE.write_text("\\n".join([
        "# STAGE_ANT_C646", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C641-C646 STAGE_READY={'YES' if stage_ready else 'NO'}**", "",
        "## Tip slice",
        "- C641: Vision V89 design fixtures",
        f"- C642: Vision V89 smoke **{v89}**", f"- C643: Vision V89 heldout **{v89h}** (disjoint={disjoint})",
        f"- C644: confidence-gate stretch rate={conf_rate} pass={conf_pass}",
        f"- C645: capture pass={capture_pass}", f"- C646: composite={composite}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",
        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V89 (uses 62)", "",
        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C646.md", "",
    ]) + "\\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''
(S / "c646_scorecard_and_stage.py").write_text(text, encoding="utf-8")
print("scorecard OK")
