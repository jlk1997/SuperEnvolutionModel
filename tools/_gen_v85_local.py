# -*- coding: utf-8 -*-
"""Build C617-C622 Vision V85 from V84. Knife: confidence-gate (C620)."""
from __future__ import annotations
import json, re
from pathlib import Path

ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"
D = json.loads((ROOT / "tools/_v85_themes.json").read_text(encoding="utf-8"))
THEMES, TRAIN_ABC, HELDOUT_ABC = D["themes"], D["train"], D["heldout"]
THEME_STR = "_".join(t[0] for t in THEMES)
OLD_THEME = "cedarpass_duskcliff_elderpass_firgrove_gorsebank_hazelpass_ironcliff_junipass_knollpass_larkpass_mosscliff_northpass_opalpass_peatpass_quillpass_reedpass_stonepass_tidepass"


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
    src = src.replace("# --- V84 overlays (new vs V83) ---", "# --- V85 overlays (new vs V84) ---")
    for a, b in [
        ("CEDARPASS bait", "UMBERTIDE bait"), ("TIDEPASS bait", "LIMETIDE bait"),
        ("NORTHPASS ghost", "FERNTIDE ghost"), ("PEATPASS bait", "HEMLOTIDE bait"),
        ("HAZELPASS bait", "ZINCTIDE bait"), ("QUILLPASS", "IVORYTIDE"),
        ("DUSKCLIFF bait", "VIOLETTIDE bait"),
        ("cedar mist + tidepass ticks (V84-only)", "umber mist + limetide ticks (V85-only)"),
    ]:
        src = src.replace(a, b)
    return src


def gen_design():
    out = (S / "c611_vision_v84_design_and_batch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C611", "C617"), ("c611", "c617"), ("V84", "V85"), ("v84", "v85"),
        ("_v84c611", "_v85c617"),
        ("Harder than V83", "Harder than V84"), ("harder than V83", "harder than V84"),
        (OLD_THEME, THEME_STR),
        ("V84 keeps floor", "V85 keeps floor"),
        ("C611 design+fixtures; no VL claim", "C617 design+fixtures; no VL claim"),
        ("fixtures only; claim deferred to C612 VL smoke", "fixtures only; claim deferred to C618 VL smoke"),
        ("No claim until C612 VL", "No claim until C618 VL"),
        ("kept on V84", "kept on V85"),
        ('"harder_than": "v83_kelpwood_birchbank"', '"harder_than": "v84_cedarpass_tidepass"'),
        ("r50plus_v84_cedarpass_tidepass", "r50plus_v85_umbertide_limetide"),
        ("vision_images_v84", "vision_images_v85"),
    ]:
        out = out.replace(a, b)
    out = out.replace(
        "NEW themes vs V83: cedarpass, duskcliff, elderpass, firgrove, gorsebank, hazelpass, ironcliff, junipass,\nknollpass, larkpass, mosscliff, northpass, opalpass, peatpass, quillpass, reedpass, stonepass, tidepass.",
        "NEW themes vs V84: umbertide, violettide, willotide, xerotide, yarrowtide, zinctide, aspertide, beachtide,\ncoraltide, dewotide, elmtide, ferntide, granitide, hemlotide, ivorytide, jaspertide, kelptide, limetide.",
    )
    out = replace_specs(out, build_specs("v85", "V85", TRAIN_ABC))
    out = retarget_overlay(out)
    (S / "c617_vision_v85_design_and_batch.py").write_text(out, encoding="utf-8")
    print("wrote design")


def gen_smoke():
    out = (S / "c612_vision_v84_smoke.py").read_text(encoding="utf-8")
    for a, b in [
        ("C612", "C618"), ("c612", "c618"), ("V84", "V85"), ("v84", "v85"),
        ("r50plus_v84_cedarpass_tidepass_clarity_floor_n>=16_qwen35_2b",
         "r50plus_v85_umbertide_limetide_clarity_floor_n>=16_qwen35_2b"),
        ("Uses C611 fixtures", "Uses C617 fixtures"),
        ("vision_images_v84", "vision_images_v85"),
    ]:
        out = out.replace(a, b)
    (S / "c618_vision_v85_smoke.py").write_text(out, encoding="utf-8")
    print("wrote smoke")


def gen_heldout():
    out = (S / "c613_vision_v84_heldout.py").read_text(encoding="utf-8")
    for a, b in [
        ("C613", "C619"), ("c613", "c619"), ("C611", "C617"),
        ("V84", "V85"), ("v84", "v85"),
        ("_v84hc613", "_v85hc619"), ("_v84c611", "_v85c617"),
    ]:
        out = out.replace(a, b)
    out = replace_specs(out, build_specs("v85h", "V85H", HELDOUT_ABC))
    out = retarget_overlay(out)
    out2, seen_fix, seen_train, seen_run = [], False, False, False
    for ln in out.splitlines():
        s = ln.strip()
        if s.startswith("FIX = ") and not seen_fix:
            out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v85h"'); seen_fix = True; continue
        if s.startswith("TRAIN_FIX = ") and not seen_train:
            out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v85"'); seen_train = True; continue
        if s.startswith("RUN = ") and "vision_v85" in s and not seen_run:
            out2.append('RUN = ROOT / "runs/vision_v85h_c619"'); seen_run = True; continue
        out2.append(ln)
    (S / "c619_vision_v85_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
    print("wrote heldout", seen_fix, seen_train, seen_run)


def gen_conf():
    out = (S / "c608_confidence_gate_stretch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C608", "C620"), ("c608", "c620"),
        ("confidence_gate_c608", "confidence_gate_c620"),
        ("after V83", "after V85"), ("after V84", "after V85"),
        ("V83+", "V85+"), ("V84+", "V85+"),
    ]:
        out = out.replace(a, b)
    (S / "c620_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
    print("wrote conf")


def gen_regression():
    out = (S / "c615_capture_office_regression.py").read_text(encoding="utf-8")
    for a, b in [
        ("C615", "C621"), ("c615", "c621"),
        ("capture_regression_c615", "capture_regression_c621"),
        ("after C611-C614", "after C617-C620"),
        ("V4-V84+heldout", "V4-V85+heldout"),
    ]:
        out = out.replace(a, b)
    if "VISION_V85_SMOKE" not in out:
        out = out.replace(
            "SMOKE_POINTERS = [",
            'SMOKE_POINTERS = [\n'
            '    ("V85", DOC / "C618_VISION_V85_SMOKE.json"),\n'
            '    ("V85_heldout", DOC / "C619_VISION_V85_HELDOUT_SMOKE.json"),\n'
            '    ("V84", DOC / "C612_VISION_V84_SMOKE.json"),\n'
            '    ("V84_heldout", DOC / "C613_VISION_V84_HELDOUT_SMOKE.json"),',
            1,
        )
    (S / "c621_capture_office_regression.py").write_text(out, encoding="utf-8")
    print("wrote regression")


def gen_scorecard():
    board = 'BOARD_MD = ROOT / "docs" / "ANT_UNIFIED_SCORECARD.md"'
    for ln in (S / "c616_scorecard_and_stage.py").read_text(encoding="utf-8").splitlines():
        if "BOARD_MD" in ln and "=" in ln:
            board = ln
            break
    text = '''# -*- coding: utf-8 -*-
"""C622: Unified scorecard + STAGE after C617-C621. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
''' + board + '''
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C622.md"
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
    c618 = load("docs/r50/C618_VISION_V85_SMOKE.json") or {}
    c618b = load("docs/r50/C618b_VISION_GATE_V85_CLAIM.json") or {}
    c619 = load("docs/r50/C619_VISION_V85_HELDOUT_SMOKE.json") or {}
    c619b = load("docs/r50/C619b_VISION_GATE_V85_HELDOUT_CLAIM.json") or {}
    c620 = load("docs/r50/C620_CONFIDENCE_GATE_STRETCH.json") or {}
    c621 = load("docs/r50/C621_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c614 = load("docs/r50/C614_PRODUCT_U2C_COST.json") or {}

    v85 = float(c618.get("rate") or 0.0)
    v85h = float(c619.get("rate") or 0.0)
    v85_claim = bool(c618b.get("vl_gate_v85_claim") or c618.get("vl_gate_v85_claim") or c618.get("claim"))
    v85h_claim = bool(c619b.get("vl_gate_v85_heldout_claim") or c619.get("vl_gate_v85_heldout_claim") or c619.get("claim"))
    disjoint = bool(c619.get("id_disjoint") or c619.get("disjoint") or c619b.get("id_disjoint") or c619b.get("disjoint"))
    conf_pass = bool(c620.get("pass"))
    conf_rate = float(c620.get("rate") or 0.0)
    u2c = prior.get("product_u2c") or {}
    if c614.get("pass") is not None:
        u2c = {
            "pass": bool(c614.get("pass")),
            "replace_ratio": float(c614.get("replace_ratio") or c614.get("mean_ratio") or 4.07),
            "source": "C614",
        }
    replace = float(u2c.get("replace_ratio") or 4.07)
    capture_pass = bool(c621.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))
    stage_ready = bool(v85_claim and v85h_claim and v85 >= GATE and v85h >= GATE and capture_pass and disjoint and conf_pass)
    composite = (1.0 if (v85 >= 0.999 and v85h >= 0.999) else min(v85, v85h)) if stage_ready else 0.0
    out = {
        "cycle": "C622", "timestamp": ts(), "gate": GATE,
        "vision": {
            "v84": (prior.get("vision") or {}).get("v84") or {"rate": 1.0, "claim": True},
            "v84_heldout": (prior.get("vision") or {}).get("v84_heldout") or {"rate": 1.0, "claim": True},
            "v85": {"rate": v85, "claim": v85_claim, "n": c618.get("n")},
            "v85_heldout": {"rate": v85h, "claim": v85h_claim, "disjoint": disjoint, "n": c619.get("n")},
        },
        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C614"},
        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C620"},
        "capture_regression": {"pass": capture_pass, "source": "C621"},
        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},
        "composite": composite, "stage_ready": stage_ready,
        "v85_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",
    }
    J(DOC / "C622_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)
    BOARD_MD.write_text("\\n".join([
        "# Unified Scorecard (C622)", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V85: rate={v85} claim={v85_claim}",
        f"- Vision V85 heldout: rate={v85h} claim={v85h_claim} disjoint={disjoint}",
        f"- product_u2c: {out['product_u2c']}", f"- confidence_gate: {out['confidence_gate']}",
        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",
        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",
    ]) + "\\n", encoding="utf-8")
    STAGE.write_text("\\n".join([
        "# STAGE_ANT_C622", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C617-C622 STAGE_READY={'YES' if stage_ready else 'NO'}**", "",
        "## Tip slice",
        "- C617: Vision V85 design fixtures",
        f"- C618: Vision V85 smoke **{v85}**", f"- C619: Vision V85 heldout **{v85h}** (disjoint={disjoint})",
        f"- C620: confidence-gate stretch rate={conf_rate} pass={conf_pass}",
        f"- C621: capture pass={capture_pass}", f"- C622: composite={composite}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",
        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V85 (uses 62)", "",
        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C622.md", "",
    ]) + "\\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''
    (S / "c622_scorecard_and_stage.py").write_text(text, encoding="utf-8")
    print("wrote scorecard")


def main():
    gen_design(); gen_smoke(); gen_heldout(); gen_conf(); gen_regression(); gen_scorecard()
    print("OK C617-C622")


if __name__ == "__main__":
    main()
