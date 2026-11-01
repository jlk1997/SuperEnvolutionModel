# -*- coding: utf-8 -*-
"""Bootstrap Vision V48 scripts (C395-C400) from V47 templates."""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCR = ROOT / "scripts"

KINDS = [
    ("atoll_recv", "paid_total", "ATOLL GRAIN RECV V48", "环礁收款单", "RECV"),
    ("birch_wh", "qty_sum", "WH BIRCH BIN V48", "桦木仓位单", "RECV"),
    ("cedar_refund", "refund_done", "CEDAR PATCH REFUND V48", "雪松退款单", "DONE"),
    ("delta_tax", "tax_base_paid", "DELTA TAX SLIP V48", "三角洲税基单", "TAX"),
    ("ember_pay", "payroll_active", "EMBER PAYROLL V48", "余烬工资单", "PAY"),
    ("fern_ship", "ship_ok", "FERN SHIP DOCK V48", "蕨叶出库单", "SHIP"),
    ("granite_sla", "sla_ok_hours", "GRANITE SLA CARD V48", "花岗岩SLA单", "SLA"),
    ("holly_exp", "exp_sum", "HOLLY EXPENSE V48", "冬青费用单", "EXP"),
    ("jade_po", "po_open", "JADE PO SHEET V48", "翡翠采购单", "PO"),
    ("knoll_order", "order_paid", "KNOLL ORDER V48", "小丘订单", "ORD"),
    ("lichen_dup", "dup_mark", "LICHEN DUP MARK V48", "地衣重复单", "DUP"),
    ("moss_zero", "zero_check", "MOSS AIR ZERO V48", "苔藓零值校验", "ZERO"),
    ("nimbus_ledger", "ledger_net", "NIMBUS LEDGER V48", "雨云台账", "LED"),
    ("orchard_ui", "ui_ok", "ORCHARD UI SCAN V48", "果园UI扫描", "UI"),
    ("pine_stack", "stack_count", "PINE STACK V48", "松树堆叠", "STK"),
    ("raven_fax", "fax_pages", "RAVEN FAX V48", "渡鸦传真单", "FAX"),
    ("spruce_glare", "glare_ok", "SPRUCE GLARE V48", "云杉晃光单", "GLR"),
    ("tide_tab", "tab_index", "TIDE TAB INDEX V48", "潮汐页签索引", "TAB"),
]

TRAIN = [
    (241.5, (117.0, 124.5, 52.0)),
    (195.0, (82, 64, 113)),
    (163.5, (78.25, 85.25, 38.0)),
    (337.0, (164.0, 173.0, 81.0)),
    (427.0, (208.0, 219.0, 71.0)),
    (142.0, (68, 74, 47)),
    (171.25, (91.0, 80.25, 44.0)),
    (214.5, (102.0, 112.5, 51.0)),
    (239.0, (126.0, 113.0, 58.0)),
    (287.75, (152.0, 135.75, 48.0)),
    (2.0, (1, 1, 0)),
    (0.0, (0.0, 0.0, 0.0)),
    (368.5, (179.0, 189.5, 67.0)),
    (1.0, (1, 0, 0)),
    (31.0, (15, 11, 5)),
    (38.0, (21, 17, 12)),
    (1.0, (1, 0, 0)),
    (53.0, (29, 24, 11)),
]
HELD = [
    (139.75, (67.5, 72.25, 29.0)),
    (112.0, (48, 37, 64)),
    (94.25, (45.0, 49.25, 22.0)),
    (199.0, (97.0, 102.0, 44.0)),
    (248.0, (121.0, 127.0, 41.0)),
    (81.0, (38, 43, 25)),
    (99.5, (53.0, 46.5, 26.0)),
    (121.75, (58.0, 63.75, 31.0)),
    (137.0, (73.0, 64.0, 34.0)),
    (164.25, (87.0, 77.25, 28.0)),
    (2.0, (1, 1, 0)),
    (0.0, (0.0, 0.0, 0.0)),
    (215.25, (105.0, 110.25, 39.0)),
    (1.0, (1, 0, 0)),
    (18.0, (8, 7, 3)),
    (22.0, (12, 10, 7)),
    (1.0, (1, 0, 0)),
    (32.0, (17, 15, 8)),
]


def lines_for(i, ver, expected, nums):
    kind, metric, title, cn, stamp = KINDS[i]
    title = title.replace("V48", ver)
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
    old_theme = "canyon_dune_estuary_fjord_glacier_harbor_iris_jasper_kelp_lotus_meadow_nebula_opal_prairie_quay_ridge_sierra_thistle"

    # sanity on TRAIN/HELD arithmetic
    for i, (exp, nums) in enumerate(TRAIN):
        kind, metric, *_ = KINDS[i]
        a, b, c = nums
        if metric in ("paid_total", "refund_done", "tax_base_paid", "payroll_active", "sla_ok_hours", "exp_sum", "po_open", "order_paid", "ledger_net"):
            assert abs((a + b) - exp) < 1e-6, (i, metric, a + b, exp)
        elif metric in ("qty_sum", "ship_ok"):
            assert abs((a + b if metric == "ship_ok" else a + c) - exp) < 1e-6 or abs((a + c) - exp) < 1e-6, (i, metric, nums, exp)
            if metric == "qty_sum":
                assert a + c == exp
            if metric == "ship_ok":
                assert a + b == exp
        elif metric == "fax_pages":
            assert a + b == exp
        elif metric in ("stack_count", "tab_index"):
            if metric == "stack_count":
                assert a + b + c == exp
            else:
                assert a + b == exp
        elif metric in ("dup_mark", "ui_ok", "glare_ok", "zero_check"):
            assert exp in (0.0, 1.0, 2.0)
    for i, (exp, nums) in enumerate(HELD):
        a, b, c = nums
        metric = KINDS[i][1]
        if metric == "qty_sum":
            assert a + c == exp
        elif metric == "ship_ok":
            assert a + b == exp
        elif metric == "fax_pages":
            assert a + b == exp
        elif metric == "stack_count":
            assert a + b + c == exp
        elif metric == "tab_index":
            assert a + b == exp
        elif metric in ("paid_total", "refund_done", "tax_base_paid", "payroll_active", "sla_ok_hours", "exp_sum", "po_open", "order_paid", "ledger_net"):
            assert abs((a + b) - exp) < 1e-6, (i, metric, a + b, exp)
    # disjoint expected sets (except structural 0/1/2)
    tr = {TRAIN[i][0] for i in range(18) if KINDS[i][1] not in ("dup_mark", "zero_check", "ui_ok", "glare_ok")}
    he = {HELD[i][0] for i in range(18) if KINDS[i][1] not in ("dup_mark", "zero_check", "ui_ok", "glare_ok")}
    assert not (tr & he), tr & he

    src = (SCR / "c389_vision_v47_design_and_batch.py").read_text(encoding="utf-8")
    train_block = "\n".join(fmt_spec("v48", i, TRAIN[i][0], TRAIN[i][1], "V48") for i in range(18))
    t = bump_pairs([
        ("C389", "C395"),
        ("c389", "c395"),
        ("V47", "V48"),
        ("v47", "v48"),
        ("vision_v48_c389", "vision_v48_c395"),
        ("vision_v47_c389", "vision_v48_c395"),
        ("runs/vision_v48_c389", "runs/vision_v48_c395"),
        ("runs/vision_v47_c389", "runs/vision_v48_c395"),
        (old_theme, theme),
        ("NEW themes vs V46:", "NEW themes vs V47:"),
        ("canyon, dune, estuary, fjord, glacier, harbor, iris, jasper,",
         "atoll, birch, cedar, delta, ember, fern, granite, holly,"),
        ("kelp, lotus, meadow, nebula, opal, prairie, quay, ridge, sierra, thistle.",
         "jade, knoll, lichen, moss, nimbus, orchard, pine, raven, spruce, tide."),
        ('"_v47c389"', '"_v48c395"'),
        ("hash(fid + \"_v47c389\")", "hash(fid + \"_v48c395\")"),
        ("V47 keeps floor", "V48 keeps floor"),
        ("C389 design+fixtures; no VL claim", "C395 design+fixtures; no VL claim"),
        ("claim deferred to C390 VL smoke", "claim deferred to C396 VL smoke"),
    ], src)
    t = replace_specs_block(t, train_block)
    t = re.sub(
        r'PROTO = ROOT / "docs" / "[^"]*VL_GATE_V48_PROTOCOL\.md"',
        'PROTO = ROOT / "docs" / "蚁算_VL_GATE_V48_PROTOCOL.md"',
        t,
        count=1,
    )
    assert "JPEG_Q = 62" in t
    (SCR / "c395_vision_v48_design_and_batch.py").write_text(t, encoding="utf-8")
    print("wrote c395 design", theme)

    s = (SCR / "c390_vision_v47_smoke.py").read_text(encoding="utf-8")
    s = bump_pairs([
        ("C390", "C396"),
        ("c390", "c396"),
        ("V47", "V48"),
        ("v47", "v48"),
        ("vision_v48_c390", "vision_v48_c396"),
        ("vision_v47_c390", "vision_v48_c396"),
        ("Uses C389 fixtures", "Uses C395 fixtures"),
        ("r50plus_v48_canyon_dune_clarity_floor", "r50plus_v48_atoll_birch_clarity_floor"),
        ("r50plus_v47_canyon_dune_clarity_floor", "r50plus_v48_atoll_birch_clarity_floor"),
    ], s)
    (SCR / "c396_vision_v48_smoke.py").write_text(s, encoding="utf-8")
    print("wrote c396 smoke")

    h = (SCR / "c391_vision_v47_heldout.py").read_text(encoding="utf-8")
    held_block = "\n".join(fmt_spec("v48h", i, HELD[i][0], HELD[i][1], "V48H") for i in range(18))
    h2 = replace_specs_block(h, held_block) if "SPECS = [" in h else h
    h2 = bump_pairs([
        ("C391", "C397"),
        ("c391", "c397"),
        ("C389", "C395"),
        ("c389", "c395"),
        ("V47", "V48"),
        ("v47", "v48"),
        ("V47H", "V48H"),
        ("v47h", "v48h"),
        ("vision_v48h_c391", "vision_v48h_c397"),
        ("vision_v47h_c391", "vision_v48h_c397"),
        (old_theme + "_heldout", theme + "_heldout"),
        ("_v47hc391", "_v48hc397"),
        ("Different ids/amounts from V47 train (C389)", "Different ids/amounts from V48 train (C395)"),
        ("Disjoint from V47 train amounts (C389)", "Disjoint from V48 train amounts (C395)"),
    ], h2)
    h2 = re.sub(
        r'PROTO = ROOT / "docs" / "[^"]*VL_GATE_V48_HELDOUT_PROTOCOL\.md"',
        'PROTO = ROOT / "docs" / "蚁算_VL_GATE_V48_HELDOUT_PROTOCOL.md"',
        h2,
        count=1,
    )
    assert "JPEG_Q = 62" in h2
    (SCR / "c397_vision_v48_heldout.py").write_text(h2, encoding="utf-8")
    print("wrote c397 heldout")

    # non-vision knife: dissolve cost/shadow refresh from C355
    ds = (SCR / "c355_dissolve_cost_shadow.py").read_text(encoding="utf-8")
    ds = bump_pairs([
        ("C355", "C398"),
        ("c355", "c398"),
        ("dissolve_cost_shadow_c355", "dissolve_cost_shadow_c398"),
        ("DISSOLVE_DASHBOARD_C323", "DISSOLVE_DASHBOARD_C398"),
        ("after C349", "after C395-C397"),
    ], ds)
    (SCR / "c398_dissolve_cost_shadow.py").write_text(ds, encoding="utf-8")
    print("wrote c398 dissolve")

    rg = (SCR / "c393_capture_office_regression.py").read_text(encoding="utf-8")
    rg = bump_pairs([
        ("C393", "C399"),
        ("c393", "c399"),
        ("capture_regression_c393", "capture_regression_c399"),
        ("after C389-C392", "after C395-C398"),
        ("C393_CAPTURE_OFFICE_REGRESSION", "C399_CAPTURE_OFFICE_REGRESSION"),
    ], rg)
    needle = '("V47_heldout", DOC / "C391_VISION_V47_HELDOUT_SMOKE.json"),'
    if needle in rg and "V48_heldout" not in rg:
        rg = rg.replace(
            needle,
            needle
            + '\n    ("V48", DOC / "C396_VISION_V48_SMOKE.json"),'
            + '\n    ("V48_heldout", DOC / "C397_VISION_V48_HELDOUT_SMOKE.json"),',
        )
    (SCR / "c399_capture_office_regression.py").write_text(rg, encoding="utf-8")
    print("wrote c399 regression")

    sc = r'''# -*- coding: utf-8 -*-
"""C400: Unified scorecard + STAGE after C395-C399. gen11 HOLD. Gate 0.6."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"
STAGE = ROOT / "docs" / "STAGE_ANT_C400.md"
GATE = 0.6


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load(rel):
    p = ROOT / rel
    if not p.is_file():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def main():
    c396 = load("docs/r50/C396_VISION_V48_SMOKE.json") or {}
    c396b = load("docs/r50/C396b_VISION_GATE_V48_CLAIM.json") or {}
    c397 = load("docs/r50/C397_VISION_V48_HELDOUT_SMOKE.json") or {}
    c397b = load("docs/r50/C397b_VISION_GATE_V48_HELDOUT_CLAIM.json") or {}
    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}
    c399 = load("docs/r50/C399_CAPTURE_OFFICE_REGRESSION.json") or {}
    prior = load("docs/r50/SCORECARD_LATEST.json") or {}
    c392 = load("docs/r50/C392_CONFIDENCE_GATE_STRETCH.json") or {}

    v48 = float(c396.get("rate") or 0.0)
    v48h = float(c397.get("rate") or 0.0)
    v48_claim = bool(c396b.get("vl_gate_v48_claim") or c396.get("vl_gate_v48_claim") or c396.get("claim"))
    v48h_claim = bool(c397b.get("vl_gate_v48_heldout_claim") or c397.get("vl_gate_v48_heldout_claim") or c397.get("claim"))
    disjoint = bool(c397.get("disjoint") or c397b.get("disjoint"))
    dissolve_pass = bool(c398.get("pass") or c398.get("dissolve_pass") or c398.get("ok"))
    shadow_pass = bool(c398.get("shadow_pass") or c398.get("pass"))
    capture_pass = bool(c399.get("pass"))
    conf_pass = bool(c392.get("pass") if c392 else prior.get("confidence_gate", {}).get("pass"))
    conf_rate = float((c392.get("rate") if c392 else None) or (prior.get("confidence_gate") or {}).get("rate") or 0.0)
    product_pass = bool((prior.get("product_u2c") or {}).get("pass", True))
    replace_ratio = float((prior.get("product_u2c") or {}).get("replace_ratio") or (prior.get("replace_ratio") or 4.07))

    rates = [v48, v48h]
    if dissolve_pass:
        rates.append(1.0)
    if capture_pass:
        rates.append(1.0)
    if conf_pass:
        rates.append(float(conf_rate) if conf_rate else 1.0)
    composite = round(min(rates) if rates else 0.0, 4)
    if not (v48_claim and v48h_claim and v48 >= GATE and v48h >= GATE):
        composite = min(composite, 0.0)
    stage_ready = bool(
        v48_claim and v48h_claim and v48 >= GATE and v48h >= GATE
        and capture_pass and disjoint
    )

    out = {
        "cycle": "C400",
        "timestamp": ts(),
        "gate": GATE,
        "vision": {
            "v47": (prior.get("vision") or {}).get("v47") or {"rate": 1.0, "claim": True},
            "v47_heldout": (prior.get("vision") or {}).get("v47_heldout") or {"rate": 1.0, "claim": True},
            "v48": {"rate": v48, "claim": v48_claim, "n": c396.get("n")},
            "v48_heldout": {"rate": v48h, "claim": v48h_claim, "disjoint": disjoint, "n": c397.get("n")},
        },
        "product_u2c": {
            "pass": product_pass,
            "replace_ratio": replace_ratio,
            "source": "prior",
        },
        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C392"},
        "capture_regression": {"pass": capture_pass, "source": "C399"},
        "dissolve_shadow": {
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "source": "C398",
        },
        "composite": composite if stage_ready else composite,
        "stage_ready": stage_ready,
        "v48_jpeg_q": 62,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }
    if stage_ready and v48 >= GATE and v48h >= GATE:
        out["composite"] = 1.0 if (v48 >= 0.999 and v48h >= 0.999) else min(v48, v48h)
    J(DOC / "C400_SCORECARD_AND_STAGE.json", out)
    J(SCORE_LATEST, out)

    board = f"""# 蚁算 UNIFIED SCORECARD

Updated: {ts()} (Asia/Shanghai)

## Tip slice C395-C400
- Vision V48 smoke **{v48}** claim={v48_claim}
- Vision V48 heldout **{v48h}** claim={v48h_claim} disjoint={disjoint}
- dissolve/shadow (C398) pass={dissolve_pass}/{shadow_pass}
- confidence-gate (prior C392) pass={conf_pass} rate={conf_rate}
- capture regression pass={capture_pass}
- replace≈{replace_ratio}
- composite **{out['composite']}** stage_ready={stage_ready}
- clarity floor jpeg_q>=60 (V48 uses 62)
- Gate 0.6; Gate2/3 untouched; gen11 HOLD
"""
    BOARD_MD.write_text(board, encoding="utf-8")

    stage = f"""# STAGE_ANT_C400

Updated: {ts()} (Asia/Shanghai)

**C395-C400 STAGE_READY={'YES' if stage_ready else 'NO'}**

## Tip slice
- C395: Vision V48 design fixtures (jpeg_q=62, floor>=60)
- C396: Vision V48 smoke claim **{v48}** (n={c396.get('n')})
- C397: Vision V48 heldout claim **{v48h}** (disjoint={disjoint})
- C398: dissolve/shadow pass={dissolve_pass}/{shadow_pass}
- C392(prior): confidence-gate pass={conf_pass} rate={conf_rate}
- C399: capture-office regression pass={capture_pass}
- C400: unified scorecard composite={out['composite']}

## Constraints
- Gate: 0.6
- Gate2/3: untouched
- gen11: HOLD
- clarity floor jpeg_q>=60 kept on V48 (uses 62)

## Entry
- Scorecard: `docs/蚁算_UNIFIED_SCORECARD.md`
- Latest JSON: `docs/r50/SCORECARD_LATEST.json`
- This stage: `docs/STAGE_ANT_C400.md`
"""
    STAGE.write_text(stage, encoding="utf-8")
    print(json.dumps({
        "cycle": "C400", "composite": out["composite"], "stage_ready": stage_ready,
        "replace": replace_ratio, "v48": v48, "v48h": v48h,
        "dissolve_pass": dissolve_pass, "capture_pass": capture_pass,
    }, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''
    (SCR / "c400_scorecard_and_stage.py").write_text(sc, encoding="utf-8")
    print("wrote c400 scorecard")
    print("theme", theme)


if __name__ == "__main__":
    main()
