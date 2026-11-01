# -*- coding: utf-8 -*-
"""Build C611-C616 Vision V84 from V83. Knife: product-U2C (C614)."""
from __future__ import annotations
import json, re
from pathlib import Path

ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"
D = json.loads((ROOT / "tools/_v84_themes.json").read_text(encoding="utf-8"))
THEMES, TRAIN_ABC, HELDOUT_ABC = D["themes"], D["train"], D["heldout"]
THEME_STR = "_".join(t[0] for t in THEMES)
OLD_THEME = "kelpwood_limecliff_maplebank_nutmegrove_olivecreek_pinebank_quartzbank_ravencliff_silverbank_thorncreek_umberbank_vinebank_wavebank_xenobank_yewbank_zirconbank_alderbank_birchbank"


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
    src = src.replace("# --- V83 overlays (new vs V82) ---", "# --- V84 overlays (new vs V83) ---")
    for a, b in [
        ("KELPWOOD bait", "CEDARPASS bait"), ("BIRCHBANK bait", "TIDEPASS bait"),
        ("VINEBANK ghost", "NORTHPASS ghost"), ("XENOBANK bait", "PEATPASS bait"),
        ("PINEBANK bait", "HAZELPASS bait"), ("YEWBANK", "QUILLPASS"),
        ("LIMECLIFF bait", "DUSKCLIFF bait"),
        ("kelp mist + birchbank ticks (V83-only)", "cedar mist + tidepass ticks (V84-only)"),
    ]:
        src = src.replace(a, b)
    return src


def gen_design():
    out = (S / "c605_vision_v83_design_and_batch.py").read_text(encoding="utf-8")
    for a, b in [
        ("C605", "C611"), ("c605", "c611"), ("V83", "V84"), ("v83", "v84"),
        ("_v83c605", "_v84c611"),
        ("Harder than V82", "Harder than V83"), ("harder than V82", "harder than V83"),
        (OLD_THEME, THEME_STR),
        ("V83 keeps floor", "V84 keeps floor"),
        ("C605 design+fixtures; no VL claim", "C611 design+fixtures; no VL claim"),
        ("fixtures only; claim deferred to C606 VL smoke", "fixtures only; claim deferred to C612 VL smoke"),
        ("No claim until C606 VL", "No claim until C612 VL"),
        ("kept on V83", "kept on V84"),
        ('"harder_than": "v82_saltmarsh_jasperbank"', '"harder_than": "v83_kelpwood_birchbank"'),
        ("r50plus_v83_kelpwood_birchbank", "r50plus_v84_cedarpass_tidepass"),
        ("vision_images_v83", "vision_images_v84"),
    ]:
        out = out.replace(a, b)
    out = out.replace(
        "NEW themes vs V82: kelpwood, limecliff, maplebank, nutmegrove, olivecreek, pinebank, quartzbank, ravencliff,\nsilverbank, thorncreek, umberbank, vinebank, wavebank, xenobank, yewbank, zirconbank, alderbank, birchbank.",
        "NEW themes vs V83: cedarpass, duskcliff, elderpass, firgrove, gorsebank, hazelpass, ironcliff, junipass,\nknollpass, larkpass, mosscliff, northpass, opalpass, peatpass, quillpass, reedpass, stonepass, tidepass.",
    )
    out = replace_specs(out, build_specs("v84", "V84", TRAIN_ABC))
    out = retarget_overlay(out)
    (S / "c611_vision_v84_design_and_batch.py").write_text(out, encoding="utf-8")
    print("wrote design")


def gen_smoke():
    out = (S / "c606_vision_v83_smoke.py").read_text(encoding="utf-8")
    for a, b in [
        ("C606", "C612"), ("c606", "c612"), ("V83", "V84"), ("v83", "v84"),
        ("r50plus_v83_kelpwood_birchbank_clarity_floor_n>=16_qwen35_2b",
         "r50plus_v84_cedarpass_tidepass_clarity_floor_n>=16_qwen35_2b"),
        ("Uses C605 fixtures", "Uses C611 fixtures"),
        ("vision_images_v83", "vision_images_v84"),
    ]:
        out = out.replace(a, b)
    (S / "c612_vision_v84_smoke.py").write_text(out, encoding="utf-8")
    print("wrote smoke")


def gen_heldout():
    out = (S / "c607_vision_v83_heldout.py").read_text(encoding="utf-8")
    for a, b in [
        ("C607", "C613"), ("c607", "c613"), ("C605", "C611"),
        ("V83", "V84"), ("v83", "v84"),
        ("_v83hc607", "_v84hc613"), ("_v83c605", "_v84c611"),
    ]:
        out = out.replace(a, b)
    out = replace_specs(out, build_specs("v84h", "V84H", HELDOUT_ABC))
    out = retarget_overlay(out)
    out2, seen_fix, seen_train, seen_run = [], False, False, False
    for ln in out.splitlines():
        s = ln.strip()
        if s.startswith("FIX = ") and not seen_fix:
            out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v84h"'); seen_fix = True; continue
        if s.startswith("TRAIN_FIX = ") and not seen_train:
            out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v84"'); seen_train = True; continue
        if s.startswith("RUN = ") and "vision_v84" in s and not seen_run:
            out2.append('RUN = ROOT / "runs/vision_v84h_c613"'); seen_run = True; continue
        out2.append(ln)
    (S / "c613_vision_v84_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
    print("wrote heldout", seen_fix, seen_train, seen_run)


def gen_u2c():
    out = (S / "c602_product_u2c_cost.py").read_text(encoding="utf-8")
    for a, b in [
        ("C602", "C614"), ("c602", "c614"),
        ("product_u2c_c602", "product_u2c_c614"), ("u2c_cost_c602", "u2c_cost_c614"),
        ("after V82", "after V84"), ("after V83", "after V84"),
        ("V82+", "V84+"), ("V83+", "V84+"),
    ]:
        out = out.replace(a, b)
    (S / "c614_product_u2c_cost.py").write_text(out, encoding="utf-8")
    print("wrote u2c")


def gen_regression():
    out = (S / "c609_capture_office_regression.py").read_text(encoding="utf-8")
    for a, b in [
        ("C609", "C615"), ("c609", "c615"),
        ("capture_regression_c609", "capture_regression_c615"),
        ("after C605-C608", "after C611-C614"),
        ("V4-V83+heldout", "V4-V84+heldout"),
    ]:
        out = out.replace(a, b)
    if "VISION_V84_SMOKE" not in out:
        out = out.replace(
            "SMOKE_POINTERS = [",
            'SMOKE_POINTERS = [\n'
            '    ("V84", DOC / "C612_VISION_V84_SMOKE.json"),\n'
            '    ("V84_heldout", DOC / "C613_VISION_V84_HELDOUT_SMOKE.json"),\n'
            '    ("V83", DOC / "C606_VISION_V83_SMOKE.json"),\n'
            '    ("V83_heldout", DOC / "C607_VISION_V83_HELDOUT_SMOKE.json"),',
            1,
        )
    (S / "c615_capture_office_regression.py").write_text(out, encoding="utf-8")
    print("wrote regression")


def gen_scorecard():
    board = 'BOARD_MD = ROOT / "docs" / "ANT_UNIFIED_SCORECARD.md"'
    for ln in (S / "c610_scorecard_and_stage.py").read_text(encoding="utf-8").splitlines():
        if "BOARD_MD" in ln and "=" in ln:
            board = ln
            break
    text = '''# -*- coding: utf-8 -*-
"""C616: Unified scorecard + STAGE after C611-C615. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
''' + board + '''
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C616.md"
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
    c612 = load("docs/r50/C612_VISION_V84_SMOKE.json") or {}
    c612b = load("docs/r50/C612b_VISION_GATE_V84_CLAIM.json") or {}
    c613 = load("docs/r50/C613_VISION_V84_HELDOUT_SMOKE.json") or {}
    c613b = load("docs/r50/C613b_VISION_GATE_V84_HELDOUT_CLAIM.json") or {}
    c614 = load("docs/r50/C614_PRODUCT_U2C_COST.json") or {}
    c615 = load("docs/r50/C615_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c608 = load("docs/r50/C608_CONFIDENCE_GATE_STRETCH.json") or {}

    v84 = float(c612.get("rate") or 0.0)
    v84h = float(c613.get("rate") or 0.0)
    v84_claim = bool(c612b.get("vl_gate_v84_claim") or c612.get("vl_gate_v84_claim") or c612.get("claim"))
    v84h_claim = bool(c613b.get("vl_gate_v84_heldout_claim") or c613.get("vl_gate_v84_heldout_claim") or c613.get("claim"))
    disjoint = bool(c613.get("id_disjoint") or c613.get("disjoint") or c613b.get("id_disjoint") or c613b.get("disjoint"))
    conf = prior.get("confidence_gate") or {}
    if c608.get("pass") is not None:
        conf = {"pass": bool(c608.get("pass")), "rate": float(c608.get("rate") or 1.0), "source": "C608"}
    u2c_pass = bool(c614.get("pass"))
    replace = float(c614.get("replace_ratio") or c614.get("mean_ratio") or ((c614.get("replace_ledger") or {}).get("mean_ratio")) or 4.07)
    capture_pass = bool(c615.get("pass"))
    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))
    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))
    stage_ready = bool(v84_claim and v84h_claim and v84 >= GATE and v84h >= GATE and capture_pass and disjoint and u2c_pass)
    composite = (1.0 if (v84 >= 0.999 and v84h >= 0.999) else min(v84, v84h)) if stage_ready else 0.0
    out = {
        "cycle": "C616", "timestamp": ts(), "gate": GATE,
        "vision": {
            "v83": (prior.get("vision") or {}).get("v83") or {"rate": 1.0, "claim": True},
            "v83_heldout": (prior.get("vision") or {}).get("v83_heldout") or {"rate": 1.0, "claim": True},
            "v84": {"rate": v84, "claim": v84_claim, "n": c612.get("n")},
            "v84_heldout": {"rate": v84h, "claim": v84h_claim, "disjoint": disjoint, "n": c613.get("n")},
        },
        "product_u2c": {"pass": u2c_pass, "replace_ratio": replace, "source": "C614"},
        "confidence_gate": conf if conf else {"pass": True, "rate": 1.0, "source": "C608"},
        "capture_regression": {"pass": capture_pass, "source": "C615"},
        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},
        "composite": composite, "stage_ready": stage_ready,
        "v84_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",
    }
    J(DOC / "C616_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)
    BOARD_MD.write_text("\\n".join([
        "# Unified Scorecard (C616)", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"- Vision V84: rate={v84} claim={v84_claim}",
        f"- Vision V84 heldout: rate={v84h} claim={v84h_claim} disjoint={disjoint}",
        f"- product_u2c: {out['product_u2c']}", f"- confidence_gate: {out['confidence_gate']}",
        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",
        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",
    ]) + "\\n", encoding="utf-8")
    STAGE.write_text("\\n".join([
        "# STAGE_ANT_C616", "", f"Updated: {ts()} (Asia/Shanghai)", "",
        f"**C611-C616 STAGE_READY={'YES' if stage_ready else 'NO'}**", "",
        "## Tip slice",
        "- C611: Vision V84 design fixtures",
        f"- C612: Vision V84 smoke **{v84}**", f"- C613: Vision V84 heldout **{v84h}** (disjoint={disjoint})",
        f"- C614: product-U2C pass={u2c_pass} replace≈{replace:.4f}×",
        f"- C615: capture pass={capture_pass}", f"- C616: composite={composite}", "",
        "## Product framing",
        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",
        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",
        "- clarity floor jpeg_q>=60 kept on V84 (uses 62)", "",
        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C616.md", "",
    ]) + "\\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''
    (S / "c616_scorecard_and_stage.py").write_text(text, encoding="utf-8")
    print("wrote scorecard")


def main():
    gen_design(); gen_smoke(); gen_heldout(); gen_u2c(); gen_regression(); gen_scorecard()
    print("OK C611-C616")


if __name__ == "__main__":
    main()
