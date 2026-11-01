# -*- coding: utf-8 -*-
from __future__ import annotations
import json, re
from pathlib import Path
ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"

def lines_for_metric(name, kind_suf, metric, title, stamp, a, b, c, tag):
    if metric == "paid_total":
        expected, body = a + b, [f"a paid {a:.2f}", f"b paid {b:.2f}", f"c open {c:.2f}", f"TOTAL PAID TARGET {a+b:.2f}"]
    elif metric == "qty_sum":
        expected = float(a + b); body = [f"SKU1 qty {a} ok", f"SKU2 qty {c} hold", f"SKU3 qty {b} ok", f"qty_sum TARGET {a+b}"]
    elif metric == "refund_done":
        expected, body = a + b, [f"itemR1 {a:.2f} done", f"itemR2 {b:.2f} done", f"itemR3 {c:.2f} open", f"refund_done TARGET {a+b:.2f}"]
    elif metric == "tax_base_paid":
        expected, body = a + b, [f"base {a:.2f} paid", f"addon {b:.2f} paid", f"skip {c:.2f}", f"tax_base_paid TARGET {a+b:.2f}"]
    elif metric == "payroll_active":
        expected, body = a + b, [f"empA {a:.2f} active", f"empB {b:.2f} active", f"empC {c:.2f} leave", f"payroll_active TARGET {a+b:.2f}"]
    elif metric == "ship_ok":
        expected = float(a + b); body = [f"box1 {a} ok", f"box2 {b} ok", f"box3 {c} hold", f"ship_ok TARGET {a+b}"]
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
        expected = float(a + b); body = [f"p1 {a}", f"p2 {b}", f"p3 {c}", f"stack_count TARGET {a+b}"]
    elif metric == "fax_pages":
        expected = float(a + b); body = [f"pgA {a}", f"pgB {b}", f"pgC {c} drop", f"fax_pages TARGET {a+b}"]
    elif metric == "glare_ok":
        expected, body = 1.0, ["zone1 1 ok", "zone2 0", "zone3 0", "glare_ok TARGET 1"]
    elif metric == "tab_index":
        expected = float(a + b); body = [f"tabA {a}", f"tabB {b}", f"tabC {c}", f"tab_index TARGET {a+b}"]
    else:
        raise ValueError(metric)
    return expected, [f"{title} {tag}"] + body

def build_specs(themes, prefix, tag, abcs):
    lines = ["SPECS = ["]
    for i, (t, abc) in enumerate(zip(themes, abcs), 1):
        name, kind_suf, metric, title, stamp, _bk = t
        a, b, c = abc
        expected, body = lines_for_metric(name, kind_suf, metric, title, stamp, a, b, c, tag)
        fid = f"{prefix}_{i:02d}"; kind = f"{name}_{kind_suf}"
        body_l = ",\n     ".join(repr(x) for x in body)
        lines.append(f'    ("{fid}", "{kind}", "{metric}", {repr(float(expected))},\n     [{body_l}],\n     {repr(name)}, "{stamp}"),')
    lines.append("]")
    return "\n".join(lines) + "\n"

def replace_specs(src, new_specs):
    return re.sub(r"SPECS = \[.*?\n\]\n", new_specs + "\n", src, count=1, flags=re.S)

T114 = [
    ["ultrawold","recv","paid_total","ULTRAWOLD GRAIN RECV","RECV","x"],
    ["vaporwold","wh","qty_sum","WH VAPORWOLD BIN","RECV","x"],
    ["willowwold","refund","refund_done","WILLOWWOLD PATCH REFUND","DONE","x"],
    ["xenowold","tax","tax_base_paid","XENOWOLD TAX SLIP","TAX","x"],
    ["yarrowwold","pay","payroll_active","YARROWWOLD PAYROLL","PAY","x"],
    ["zincwold","ship","ship_ok","ZINCWOLD SHIP DOCK","SHIP","x"],
    ["asterwold","sla","sla_ok_hours","ASTERWOLD SLA CARD","SLA","x"],
    ["brinewold","exp","exp_sum","BRINEWOLD EXPENSE","EXP","x"],
    ["cloverwold","po","po_open","CLOVERWOLD PO SHEET","PO","x"],
    ["deltaswold","order","order_paid","DELTASWOLD ORDER","ORD","x"],
    ["elmwold","dup","dup_mark","ELMWOLD DUP MARK","DUP","x"],
    ["firwold","zero","zero_check","FIRWOLD AIR ZERO","ZERO","x"],
    ["gorsewold","ledger","ledger_net","GORSEWOLD LEDGER","LED","x"],
    ["heatherwold","ui","ui_ok","HEATHERWOLD UI SCAN","UI","x"],
    ["indowold","stack","stack_count","INDOWOLD STACK","STK","x"],
    ["juniperwold","fax","fax_pages","JUNIPERWOLD FAX","FAX","x"],
    ["kestrelwold","glare","glare_ok","KESTRELWOLD GLARE","GLR","x"],
    ["larkwold","tab","tab_index","LARKWOLD TAB INDEX","TAB","x"],
]
TR114 = [
    [624.0, 640.5, 433.0],[550, 590, 406],[547.0, 576.25, 413.0],[678.0, 696.0, 503.0],
    [741.0, 765.0, 473.0],[499, 515, 431],[340.0, 380.0, 220.0],[589.0, 620.75, 437.0],
    [623.0, 606.0, 446.0],[656.0, 644.0, 434.0],[1,1,0],[0,0,0],
    [722.0, 743.5, 459.0],[1,0,0],[275, 267, 245],[293, 277, 268],[1,0,0],[319, 295, 265],
]
HO114 = [
    [493.0, 505.75, 386.0],[448, 488, 368],[451.0, 464.5, 374.0],[566.0, 582.0, 415.0],
    [607.0, 623.0, 410.0],[401, 415, 379],[240.0, 280.0, 180.0],[477.0, 498.75, 386.0],
    [497.0, 485.0, 389.0],[524.0, 510.0, 381.0],[1,1,0],[0,0,0],
    [559.0, 574.5, 396.0],[1,0,0],[251, 248, 243],[267, 261, 249],[1,0,0],[277, 271, 250],
]
(ROOT / "tools/_v114_themes.json").write_text(json.dumps({"themes": T114, "train": TR114, "heldout": HO114}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_114(src):
    src = src.replace("# --- V113 overlays (new vs V50) ---", "# --- V114 overlays (new vs V50) ---")
    src = src.replace("# --- V113 overlays (new vs V49) ---", "# --- V114 overlays (new vs V49) ---")
    for a, b in [
        ("CEDARFEN bait 57.57", "ULTRAWOLD bait 58.58"),
        ("DUSK bait 77.77", "VAPOR bait 78.78"),
        ("EMBER ghost 98.98", "WILLOW ghost 99.99"),
        ("HAZEL bait 52.52", "ZINC bait 53.53"),
        ("KNOLL bait 43.43", "CLOVER bait 44.44"),
        ("OPAL bait 87.87", "GORSE bait 88.88"),
        ("cedar mist + timber ticks (V113-only)", "ultra mist + lark ticks (V114-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD113 = "cedarfen_duskfen_emberfen_frostfen_glenfen_hazelfen_ironfen_jadefen_knollfen_lotusfen_meadowfen_northfen_opalfen_pearlfen_quartzfen_ravenfen_stonefen_timberfen"
NEW114 = "_".join(t[0] for t in T114)

out = (S / "c785_vision_v113_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C785", "C791"), ("c785", "c791"), ("V113", "V114"), ("v113", "v114"),
    ("_v113c785", "_v114c791"),
    ("Harder than V112", "Harder than V113"), ("harder than V112", "harder than V113"),
    (OLD113, NEW114),
    ("V113 keeps floor", "V114 keeps floor"),
    ("C785 design+fixtures; no VL claim", "C791 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C786 VL smoke", "fixtures only; claim deferred to C792 VL smoke"),
    ("No claim until C786 VL", "No claim until C792 VL"),
    ("kept on V113", "kept on V114"),
    ("vision_images_v113", "vision_images_v114"),
    ("VL_GATE_V113", "VL_GATE_V114"), ("vl_gate_v113", "vl_gate_v114"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V112: cedarfen, duskfen, emberfen, frostfen, glenfen, hazelfen, ironfen, jadefen,\nknollfen, lotusfen, meadowfen, northfen, opalfen, pearlfen, quartzfen, ravenfen, stonefen, timberfen.",
    "NEW themes vs V113: ultrawold, vaporwold, willowwold, xenowold, yarrowwold, zincwold, asterwold, brinewold,\ncloverwold, deltaswold, elmwold, firwold, gorsewold, heatherwold, indowold, juniperwold, kestrelwold, larkwold.",
)
out = replace_specs(out, build_specs(T114, "v114", "V114", TR114))
out = retarget_114(out)
(S / "c791_vision_v114_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c786_vision_v113_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C786", "C792"), ("c786", "c792"), ("V113", "V114"), ("v113", "v114"),
    ("Uses C785 fixtures", "Uses C791 fixtures"),
    ("vision_images_v113", "vision_images_v114"),
    ("vl_gate_v113", "vl_gate_v114"), ("VL_GATE_V113", "VL_GATE_V114"),
]:
    out = out.replace(a, b)
(S / "c792_vision_v114_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c787_vision_v113_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C787", "C793"), ("c787", "c793"), ("C785", "C791"),
    ("V113", "V114"), ("v113", "v114"),
    ("_v113hc787", "_v114hc793"), ("_v113c785", "_v114c791"),
    ("vl_gate_v113", "vl_gate_v114"), ("VL_GATE_V113", "VL_GATE_V114"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T114, "v114h", "V114H", HO114))
out = retarget_114(out)
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v114h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v114"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v114" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v114h_c793"'); seen_run = True; continue
    out2.append(ln)
(S / "c793_vision_v114_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c782_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C782", "C794"), ("c782", "c794"),
    ("product_u2c_c782", "product_u2c_c794"),
    ("after V112", "after V114"), ("after V113", "after V114"),
]:
    out = out.replace(a, b)
(S / "c794_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c789_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C789", "C795"), ("c789", "c795"),
    ("capture_regression_c789", "capture_regression_c795"),
    ("after C785-C788", "after C791-C794"),
    ("V4-V113+heldout", "V4-V114+heldout"),
]:
    out = out.replace(a, b)
if "VISION_V114_SMOKE" not in out:
    out = out.replace(
        "SMOKE_POINTERS = [",
        'SMOKE_POINTERS = [\n    ("V114", DOC / "C792_VISION_V114_SMOKE.json"),\n    ("V114_heldout", DOC / "C793_VISION_V114_HELDOUT_SMOKE.json"),\n    ("V113", DOC / "C786_VISION_V113_SMOKE.json"),\n    ("V113_heldout", DOC / "C787_VISION_V113_HELDOUT_SMOKE.json"),',
        1,
    )
(S / "c795_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c790_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C790", "C796"), ("c790", "c796"),
    ("C786", "C792"), ("C787", "C793"), ("C788", "C794"), ("C789", "C795"),
    ("C785", "C791"),
    ("V113", "V114"), ("v113", "v114"),
    ("V112", "V113"), ("v112", "v113"),
    ("v113_jpeg_q", "v114_jpeg_q"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C794_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C788_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C782_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C794_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C782"}',
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C794"}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C788"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C788"}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C794"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C788"}',
)
out = out.replace(
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C782"}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C794"}',
)
out = out.replace(
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C794"}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C794"}',
)
out = out.replace(
    "confidence-gate rate={conf_rate} pass={conf_pass}",
    "product-U2C replace={replace} pass={u2c_pass}",
)
out = out.replace(
    "stage_ready = bool(v114_claim and v114h_claim and v114 >= GATE and v114h >= GATE and capture_pass and disjoint and conf_pass)",
    "stage_ready = bool(v114_claim and v114h_claim and v114 >= GATE and v114h >= GATE and capture_pass and disjoint and u2c_pass)",
)
if "u2c_pass =" not in out:
    out = out.replace(
        'replace = float(u2c.get("replace_ratio") or 4.07)',
        'replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))',
    )
(S / "c796_scorecard_and_stage.py").write_text(out, encoding="utf-8")
for ln in out.splitlines():
    if any(x in ln for x in ("c656 =", "c650 =", '"confidence_gate"', "stage_ready =", "C794:")):
        if "load" in ln or "source" in ln or "stage_ready" in ln or "product-U2C" in ln:
            print("CHK", ln.strip()[:130])
print("scorecard OK"); print("done")
