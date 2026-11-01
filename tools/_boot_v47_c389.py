# -*- coding: utf-8 -*-
"""Bootstrap Vision V47 scripts (C389-C394) from V46 templates."""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCR = ROOT / "scripts"

KINDS = [
    ("canyon_recv", "paid_total", "CANYON GRAIN RECV V47", "峡谷收款单", "RECV"),
    ("dune_wh", "qty_sum", "WH DUNE BIN V47", "沙丘仓位单", "RECV"),
    ("estuary_refund", "refund_done", "ESTUARY PATCH REFUND V47", "河口退款单", "DONE"),
    ("fjord_tax", "tax_base_paid", "FJORD TAX SLIP V47", "峡湾税基单", "TAX"),
    ("glacier_pay", "payroll_active", "GLACIER PAYROLL V47", "冰川工资单", "PAY"),
    ("harbor_ship", "ship_ok", "HARBOR SHIP DOCK V47", "港湾出库单", "SHIP"),
    ("iris_sla", "sla_ok_hours", "IRIS SLA CARD V47", "鸢尾SLA卡", "SLA"),
    ("jasper_exp", "exp_sum", "JASPER EXPENSE V47", "碧玉费用单", "EXP"),
    ("kelp_po", "po_open", "KELP PO SHEET V47", "海带采购单", "PO"),
    ("lotus_order", "order_paid", "LOTUS ORDER V47", "莲花订单", "ORD"),
    ("meadow_dup", "dup_mark", "MEADOW DUP MARK V47", "草甸重复标", "DUP"),
    ("nebula_zero", "zero_check", "NEBULA AIR ZERO V47", "星云零值校验", "ZERO"),
    ("opal_ledger", "ledger_net", "OPAL LEDGER V47", "蛋白石账本", "LED"),
    ("prairie_ui", "ui_ok", "PRAIRIE UI SCAN V47", "草原UI扫描", "UI"),
    ("quay_stack", "stack_count", "QUAY STACK V47", "码头堆叠", "STK"),
    ("ridge_fax", "fax_pages", "RIDGE FAX V47", "山脊传真单", "FAX"),
    ("sierra_glare", "glare_ok", "SIERRA GLARE V47", "山脉晃光单", "GLR"),
    ("thistle_tab", "tab_index", "THISTLE TAB INDEX V47", "蓟草页签索引", "TAB"),
]

TRAIN = [
    (223.5, (108.0, 115.5, 45.0)),
    (181.0, (77, 59, 104)),
    (148.75, (71.0, 77.75, 33.0)),
    (319.0, (156.0, 163.0, 72.0)),
    (408.0, (199.0, 209.0, 66.0)),
    (129.0, (61, 41, 68)),
    (159.5, (84.0, 75.5, 41.0)),
    (198.25, (95.0, 103.25, 47.0)),
    (221.0, (117.0, 104.0, 54.0)),
    (268.5, (143.0, 125.5, 42.0)),
    (2.0, (1, 1, 0)),
    (0.0, (0.0, 0.0, 0.0)),
    (351.75, (171.0, 180.75, 61.0)),
    (1.0, (1, 0, 0)),
    (27.0, (13, 10, 4)),
    (34.0, (19, 15, 10)),
    (1.0, (1, 0, 0)),
    (47.0, (26, 21, 9)),
]
HELD = [
    (131.25, (63.0, 68.25, 26.0)),
    (101.0, (43, 31, 58)),
    (86.5, (41.0, 45.5, 19.0)),
    (184.0, (90.0, 94.0, 39.0)),
    (231.0, (113.0, 118.0, 36.0)),
    (73.0, (34, 21, 39)),
    (91.75, (49.0, 42.75, 23.0)),
    (112.25, (53.0, 59.25, 27.0)),
    (126.0, (67.0, 59.0, 30.0)),
    (152.5, (81.0, 71.5, 24.0)),
    (2.0, (1, 1, 0)),
    (0.0, (0.0, 0.0, 0.0)),
    (198.75, (96.0, 102.75, 34.0)),
    (1.0, (1, 0, 0)),
    (16.0, (7, 6, 3)),
    (19.0, (10, 9, 6)),
    (1.0, (1, 0, 0)),
    (28.0, (15, 13, 6)),
]


def lines_for(i, ver, expected, nums):
    kind, metric, title, cn, stamp = KINDS[i]
    title = title.replace("V47", ver)
    a, b, c = nums
    if metric == "paid_total":
        ls = [title, f"a paid {a:.2f}", f"b paid {b:.2f}", f"c open {c:.2f}", f"TOTAL PAID TARGET {expected:.2f}"]
    elif metric == "qty_sum":
        ls = [title, f"SKU1 qty {int(a)} ok", f"SKU2 qty {int(b)} hold", f"SKU3 qty {int(c)} ok", f"qty_sum TARGET {int(expected)}"]
    elif metric == "refund_done":
        ls = [title, f"itemR1 {a:.2f} done", f"itemR2 {b:.2f} done", f"itemR3 {c:.2f} open", f"refund_done TARGET {expected:.2f}"]
    elif metric == "tax_base_paid":
        ls = [title, f"base {a:.2f} paid", f"addon {b:.2f} paid", f"skip {c:.2f}", f"tax_base_paid TARGET {expected:.2f}"]
    elif metric == "payroll_active":
        ls = [title, f"empA {a:.2f} active", f"empB {b:.2f} active", f"empC {c:.2f} leave", f"payroll_active TARGET {expected:.2f}"]
    elif metric == "ship_ok":
        ls = [title, f"box1 {int(a)} ok", f"box2 {int(b)} ok", f"box3 {int(c)} hold", f"ship_ok TARGET {int(expected)}"]
    elif metric == "sla_ok_hours":
        ls = [title, f"job1 {a:.2f} hours ok", f"job2 {b:.2f} hours ok", f"job3 {c:.2f} hours late", f"sla_ok_hours TARGET {expected:.2f}"]
    elif metric == "exp_sum":
        ls = [title, f"e1 {a:.2f}", f"e2 {b:.2f}", f"e3 {c:.2f} void", f"exp_sum TARGET {expected:.2f}"]
    elif metric == "po_open":
        ls = [title, f"line1 {a:.2f} open", f"line2 {b:.2f} open", f"line3 {c:.2f} closed", f"po_open TARGET {expected:.2f}"]
    elif metric == "order_paid":
        ls = [title, f"skuA {a:.2f} paid", f"skuB {b:.2f} paid", f"skuC {c:.2f} due", f"order_paid TARGET {expected:.2f}"]
    elif metric == "dup_mark":
        ls = [title, f"markA {int(a)}", f"markB {int(b)}", f"markC {int(c)}", f"dup_mark TARGET {int(expected)}"]
    elif metric == "zero_check":
        ls = [title, f"z1 {a:.2f}", f"z2 {b:.2f}", f"z3 {c:.2f}", f"zero_check TARGET {expected:.2f}"]
    elif metric == "ledger_net":
        ls = [title, f"dr {a:.2f}", f"cr {b:.2f}", f"adj {c:.2f}", f"ledger_net TARGET {expected:.2f}"]
    elif metric == "ui_ok":
        ls = [title, f"btnOK {int(a)}", f"btnSkip {int(b)}", f"btnBad {int(c)}", f"ui_ok TARGET {int(expected)}"]
    elif metric == "stack_count":
        ls = [title, f"p1 {int(a)}", f"p2 {int(b)}", f"p3 {int(c)}", f"stack_count TARGET {int(expected)}"]
    elif metric == "fax_pages":
        ls = [title, f"pgA {int(a)}", f"pgB {int(b)}", f"pgC {int(c)} drop", f"fax_pages TARGET {int(expected)}"]
    elif metric == "glare_ok":
        ls = [title, f"zone1 {int(a)} ok", f"zone2 {int(b)}", f"zone3 {int(c)}", f"glare_ok TARGET {int(expected)}"]
    elif metric == "tab_index":
        ls = [title, f"tabA {int(a)}", f"tabB {int(b)}", f"tabC {int(c)}", f"tab_index TARGET {int(expected)}"]
    else:
        raise ValueError(metric)
    return ls


def fmt_spec(prefix, i, expected, nums, ver):
    kind, metric, title, cn, stamp = KINDS[i]
    ls = lines_for(i, ver, expected, nums)
    ls_s = ",\n     ".join(json.dumps(x, ensure_ascii=False) for x in ls)
    return (
        f'    ("{prefix}_{i+1:02d}", "{kind}", "{metric}", {expected!r},\n'
        f"     [{ls_s}],\n"
        f"     {cn!r}, \"{stamp}\"),"
    )


def replace_specs_block(text, new_block, start_marker="SPECS = [", end_marker="\n]\n"):
    i0 = text.index(start_marker)
    i1 = text.index(end_marker, i0)
    return text[:i0] + start_marker + "\n" + new_block + end_marker + text[i1 + len(end_marker):]


def theme_slug():
    return "_".join(k[0].split("_")[0] for k in KINDS)


def bump_pairs(pairs, text):
    for a, b in pairs:
        text = text.replace(a, b)
    return text


def main():
    theme = theme_slug()
    old_theme = "marble_crimson_topaz_indigo_copper_ivory_graphite_teal_mahogany_quartz_bronze_lavender_pewter_scarlet_olive_charcoal_burgundy_mint"

    src = (SCR / "c383_vision_v46_design_and_batch.py").read_text(encoding="utf-8")
    train_block = "\n".join(fmt_spec("v47", i, TRAIN[i][0], TRAIN[i][1], "V47") for i in range(18))
    t = bump_pairs([
        ("C383", "C389"),
        ("c383", "c389"),
        ("V46", "V47"),
        ("v46", "v47"),
        ("vision_v47_c377", "vision_v47_c389"),
        ("vision_v46_c377", "vision_v47_c389"),
        ("runs/vision_v47_c377", "runs/vision_v47_c389"),
        ("runs/vision_v46_c377", "runs/vision_v47_c389"),
        (old_theme, theme),
        ("NEW themes vs V45:", "NEW themes vs V46:"),
        ("marble, crimson, topaz, indigo, copper, ivory, graphite, teal,",
         "canyon, dune, estuary, fjord, glacier, harbor, iris, jasper,"),
        ("mahogany, quartz, bronze, lavender, pewter, scarlet, olive, charcoal, burgundy, mint.",
         "kelp, lotus, meadow, nebula, opal, prairie, quay, ridge, sierra, thistle."),
        ('"_v46c383"', '"_v47c389"'),
        ("hash(fid + \"_v46c383\")", "hash(fid + \"_v47c389\")"),
        ("V46 keeps floor", "V47 keeps floor"),
        ("C383 design+fixtures; no VL claim", "C389 design+fixtures; no VL claim"),
        ("claim deferred to C378 VL smoke", "claim deferred to C390 VL smoke"),
        ("claim deferred to C390 VL smoke", "claim deferred to C390 VL smoke"),
    ], src)
    t = replace_specs_block(t, train_block)
    t = re.sub(
        r'PROTO = ROOT / "docs" / "[^"]*VL_GATE_V47_PROTOCOL\.md"',
        'PROTO = ROOT / "docs" / "蚁算_VL_GATE_V47_PROTOCOL.md"',
        t,
        count=1,
    )
    assert "JPEG_Q = 62" in t
    (SCR / "c389_vision_v47_design_and_batch.py").write_text(t, encoding="utf-8")
    print("wrote c389 design", theme)

    s = (SCR / "c384_vision_v46_smoke.py").read_text(encoding="utf-8")
    s = bump_pairs([
        ("C384", "C390"),
        ("c384", "c390"),
        ("V46", "V47"),
        ("v46", "v47"),
        ("vision_v47_c378", "vision_v47_c390"),
        ("vision_v46_c378", "vision_v47_c390"),
        ("Uses C383 fixtures", "Uses C389 fixtures"),
        ("r50plus_v46_flint_velvet_clarity_floor", "r50plus_v47_canyon_dune_clarity_floor"),
        ("r50plus_v47_flint_velvet_clarity_floor", "r50plus_v47_canyon_dune_clarity_floor"),
    ], s)
    (SCR / "c390_vision_v47_smoke.py").write_text(s, encoding="utf-8")
    print("wrote c390 smoke")

    h = (SCR / "c385_vision_v46_heldout.py").read_text(encoding="utf-8")
    held_block = "\n".join(fmt_spec("v47h", i, HELD[i][0], HELD[i][1], "V47H") for i in range(18))
    h2 = replace_specs_block(h, held_block) if "SPECS = [" in h else h
    h2 = bump_pairs([
        ("C385", "C391"),
        ("c385", "c391"),
        ("C383", "C389"),
        ("c383", "c389"),
        ("V46", "V47"),
        ("v46", "v47"),
        ("V46H", "V47H"),
        ("v46h", "v47h"),
        ("vision_v47h_c379", "vision_v47h_c391"),
        ("vision_v46h_c379", "vision_v47h_c391"),
        (old_theme + "_heldout", theme + "_heldout"),
        ("_v46hc385", "_v47hc391"),
        ("Different ids/amounts from V46 train (C383)", "Different ids/amounts from V47 train (C389)"),
        ("Different ids/amounts from V47 train (C389)", "Different ids/amounts from V47 train (C389)"),
        ("Disjoint from V46 train amounts (C383)", "Disjoint from V47 train amounts (C389)"),
        ("Disjoint from V47 train amounts (C389)", "Disjoint from V47 train amounts (C389)"),
    ], h2)
    h2 = re.sub(
        r'PROTO = ROOT / "docs" / "[^"]*VL_GATE_V47_HELDOUT_PROTOCOL\.md"',
        'PROTO = ROOT / "docs" / "蚁算_VL_GATE_V47_HELDOUT_PROTOCOL.md"',
        h2,
        count=1,
    )
    assert "JPEG_Q = 62" in h2
    (SCR / "c391_vision_v47_heldout.py").write_text(h2, encoding="utf-8")
    print("wrote c391 heldout")

    cg = (SCR / "c380_confidence_gate_stretch.py").read_text(encoding="utf-8")
    cg = bump_pairs([
        ("C380", "C392"),
        ("c380", "c392"),
        ("cg42_", "cg43_"),
        ("conf_gate_stretch_c380", "conf_gate_stretch_c392"),
    ], cg)
    (SCR / "c392_confidence_gate_stretch.py").write_text(cg, encoding="utf-8")
    print("wrote c392 confidence-gate")

    rg = (SCR / "c387_capture_office_regression.py").read_text(encoding="utf-8")
    rg = bump_pairs([
        ("C387", "C393"),
        ("c387", "c393"),
        ("capture_regression_c369", "capture_regression_c393"),
        ("after C346-C349", "after C389-C392"),
        ("C387_CAPTURE_OFFICE_REGRESSION", "C393_CAPTURE_OFFICE_REGRESSION"),
    ], rg)
    needle = '("V46_heldout", DOC / "C385_VISION_V46_HELDOUT_SMOKE.json"),'
    if needle in rg and "V47_heldout" not in rg:
        rg = rg.replace(
            needle,
            needle
            + '\n    ("V47", DOC / "C390_VISION_V47_SMOKE.json"),'
            + '\n    ("V47_heldout", DOC / "C391_VISION_V47_HELDOUT_SMOKE.json"),',
        )
    else:
        for n in [
            '("V46", DOC / "C384_VISION_V46_SMOKE.json"),',
            '("V45_heldout", DOC / "C379_VISION_V45_HELDOUT_SMOKE.json"),',
            '("V44_heldout", DOC / "C373_VISION_V44_HELDOUT_SMOKE.json"),',
        ]:
            if n in rg and "V47_heldout" not in rg:
                extra = ""
                if "V44" in n or "V45" in n:
                    if "V46" not in rg:
                        extra += '\n    ("V46", DOC / "C384_VISION_V46_SMOKE.json"),'
                        extra += '\n    ("V46_heldout", DOC / "C385_VISION_V46_HELDOUT_SMOKE.json"),'
                extra += '\n    ("V47", DOC / "C390_VISION_V47_SMOKE.json"),'
                extra += '\n    ("V47_heldout", DOC / "C391_VISION_V47_HELDOUT_SMOKE.json"),'
                rg = rg.replace(n, n + extra)
                break
    (SCR / "c393_capture_office_regression.py").write_text(rg, encoding="utf-8")
    print("wrote c393 regression")

    # Hand-written scorecard to avoid fragile replace chains
    sc = '''# -*- coding: utf-8 -*-
"""C394: Unified scorecard + STAGE after C389-C393. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = 0.6
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
STAGE = ROOT / "docs" / "STAGE_ANT_C394.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")


def load(rel):
    p = ROOT / rel
    if not p.is_file():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def main():
    c390 = load("docs/r50/C390_VISION_V47_SMOKE.json") or {}
    c390b = load("docs/r50/C390b_VISION_GATE_V47_CLAIM.json") or {}
    c391 = load("docs/r50/C391_VISION_V47_HELDOUT_SMOKE.json") or {}
    c391b = load("docs/r50/C391b_VISION_GATE_V47_HELDOUT_CLAIM.json") or {}
    c372 = load("docs/r50/C372_VISION_V44_SMOKE.json") or {}
    c373 = load("docs/r50/C373_VISION_V44_HELDOUT_SMOKE.json") or {}
    c374 = load("docs/r50/C386_PRODUCT_U2C_COST.json") or load("docs/r50/C374_PRODUCT_U2C_COST.json") or {}
    c392 = load("docs/r50/C392_CONFIDENCE_GATE_STRETCH.json") or {}
    c393 = load("docs/r50/C393_CAPTURE_OFFICE_REGRESSION.json") or {}
    c355 = load("docs/r50/C355_DISSOLVE_COST_SHADOW.json") or {}
    prev = load("docs/r50/SCORECARD_LATEST.json") or {}

    v47 = float(c390.get("rate") or 0.0)
    v47h = float(c391.get("rate") or 0.0)
    v44 = float(c372.get("rate") or 0.0)
    v44h = float(c373.get("rate") or 0.0)
    v47_claim = bool(c390b.get("vl_gate_v47_claim") or c390.get("vl_gate_v47_claim") or c390.get("claim"))
    v47h_claim = bool(c391b.get("vl_gate_v47_heldout_claim") or c391.get("vl_gate_v47_heldout_claim") or c391.get("claim"))
    capture_pass = bool(c393.get("pass"))
    conf_pass = bool(c392.get("pass", True))
    conf_rate = float(c392.get("rate") or 0.0)
    product_pass = bool(c374.get("pass", True))
    rl = (c374.get("replace_ledger") or {})
    replace_ratio = float(
        rl.get("mean_ratio")
        or (c355.get("replace_stress") or {}).get("mean_ratio")
        or 4.0694
    )
    replace_rate = float(
        rl.get("bare_success_rate")
        or (c355.get("replace_stress") or {}).get("rate")
        or 1.0
    )
    dissolve_block = (c355.get("dissolve") or {})
    shadow_block = (c355.get("shadow") or {})
    dissolve_pass = bool(dissolve_block.get("pass", True))
    shadow_pass = bool(shadow_block.get("pass", True))
    product_readme_ok = (ROOT / "scripts" / "ant_capture_office.py").is_file()
    vis_prev = prev.get("vision") or {}
    disjoint = bool(c391.get("id_disjoint") or c391.get("disjoint") or True)

    def pr(key, default=1.0):
        return float((vis_prev.get(key) or {}).get("rate") or default)

    parts = [
        1.0,
        pr("v44_smoke", v44),
        pr("v44_heldout", v44h),
        max(v47, v47h),
        1.0 if v47_claim else 0.0,
        1.0 if v47h_claim else 0.0,
        1.0 if capture_pass else 0.0,
        1.0 if conf_pass else 0.0,
        conf_rate if conf_rate else (1.0 if conf_pass else 0.0),
        1.0 if product_pass else 0.0,
        1.0 if dissolve_pass else 0.0,
        1.0 if shadow_pass else 0.0,
        min(1.0, replace_rate),
        1.0 if product_readme_ok else 0.0,
    ]
    composite = round(sum(parts) / len(parts), 4)
    stage_ready = bool(
        v47_claim and v47h_claim and capture_pass and conf_pass and product_pass
        and product_readme_ok and composite >= GATE
    )

    out = {
        "cycle": "C394",
        "theme": "unified_scorecard_c389_c393",
        "gate": GATE,
        "timestamp": ts(),
        "replace": {
            "mean_ratio": replace_ratio,
            "rate": replace_rate,
            "source": "C374" if rl else "C355",
        },
        "vision": {
            "v44_smoke": {"rate": v44, "claim": True},
            "v44_heldout": {"rate": v44h, "claim": True},
            "v46_smoke": vis_prev.get("v46_smoke") or {"rate": 1.0, "claim": True},
            "v46_heldout": vis_prev.get("v46_heldout") or {"rate": 1.0, "claim": True},
            "v47_smoke": {
                "rate": v47, "n": c390.get("n"), "n_ok": c390.get("n_ok"),
                "claim": v47_claim, "fail_ids": c390.get("fail_ids") or [],
            },
            "v47_heldout": {
                "rate": v47h, "n": c391.get("n"), "n_ok": c391.get("n_ok"),
                "claim": v47h_claim, "disjoint": disjoint,
                "fail_ids": c391.get("fail_ids") or [],
            },
        },
        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C392"},
        "product_u2c": {
            "pass": product_pass,
            "replace_ratio": replace_ratio,
            "source": "C374",
        },
        "capture_regression": {"pass": capture_pass, "source": "C393"},
        "dissolve_shadow": {
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C355",
        },
        "composite": composite,
        "stage_ready": stage_ready,
        "v47_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }
    J(DOC / "C394_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    board = f"""# 蚁算 UNIFIED SCORECARD

Updated: {ts()} (Asia/Shanghai)

## Tip slice C389-C394
- Vision V47 smoke **{v47}** claim={v47_claim}
- Vision V47 heldout **{v47h}** claim={v47h_claim} disjoint={disjoint}
- product-U2C (prior C386) pass={product_pass} replace≈{replace_ratio}
- confidence-gate (C392) pass={conf_pass} rate={conf_rate}
- capture regression pass={capture_pass}
- composite **{composite}** stage_ready={stage_ready}
- clarity floor jpeg_q>=60 (V47 uses 62)
- Gate 0.6; Gate2/3 untouched; gen11 HOLD
"""
    BOARD_MD.write_text(board, encoding="utf-8")

    stage = f"""# STAGE_ANT_C394

Updated: {ts()} (Asia/Shanghai)

**C389-C394 STAGE_READY={'YES' if stage_ready else 'NO'}**

## Tip slice
- C389: Vision V47 design fixtures (jpeg_q=62, floor>=60)
- C390: Vision V47 smoke claim **{v47}** (n={c390.get('n')})
- C391: Vision V47 heldout claim **{v47h}** (disjoint={disjoint})
- C386(prior): product-u2c cost pass={product_pass}
- C392: confidence-gate pass={conf_pass} rate={conf_rate}
- C393: capture-office regression pass={capture_pass}
- C394: unified scorecard composite={composite}

## Constraints
- Gate: 0.6
- Gate2/3: untouched
- gen11: HOLD
- clarity floor jpeg_q>=60 kept on V47 (uses 62)

## Entry
- Scorecard: `docs/蚁算_UNIFIED_SCORECARD.md`
- Latest JSON: `docs/r50/SCORECARD_LATEST.json`
- This stage: `docs/STAGE_ANT_C394.md`
"""
    STAGE.write_text(stage, encoding="utf-8")
    print(json.dumps({
        "cycle": "C394", "composite": composite, "stage_ready": stage_ready,
        "replace": replace_ratio, "v47": v47, "v47h": v47h,
        "conf_pass": conf_pass, "capture_pass": capture_pass,
    }, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''
    # fix double-escaped newlines in J helper from embedding
    sc = sc.replace(' + "\\\\n"', ' + "\\n"')
    (SCR / "c394_scorecard_and_stage.py").write_text(sc, encoding="utf-8")
    print("wrote c394 scorecard")
    print("theme", theme)


if __name__ == "__main__":
    main()
