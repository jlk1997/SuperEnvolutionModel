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

T111 = [
    ["saffronvale","recv","paid_total","SAFFRONVALE GRAIN RECV","RECV","x"],
    ["tundravale","wh","qty_sum","WH TUNDRAVALE BIN","RECV","x"],
    ["umbvale","refund","refund_done","UMBVALE PATCH REFUND","DONE","x"],
    ["verdvale","tax","tax_base_paid","VERDVALE TAX SLIP","TAX","x"],
    ["wispvale","pay","payroll_active","WISPVALE PAYROLL","PAY","x"],
    ["xylavale","ship","ship_ok","XYLAVALE SHIP DOCK","SHIP","x"],
    ["yarrowvale","sla","sla_ok_hours","YARROWVALE SLA CARD","SLA","x"],
    ["zephyrvale","exp","exp_sum","ZEPHYRVALE EXPENSE","EXP","x"],
    ["alpinevale","po","po_open","ALPINEVALE PO SHEET","PO","x"],
    ["brackenvale","order","order_paid","BRACKENVALE ORDER","ORD","x"],
    ["cascadevale","dup","dup_mark","CASCADEVALE DUP MARK","DUP","x"],
    ["dunevale","zero","zero_check","DUNEVALE AIR ZERO","ZERO","x"],
    ["eldvale","ledger","ledger_net","ELDVALE LEDGER","LED","x"],
    ["fjordvale","ui","ui_ok","FJORDVALE UI SCAN","UI","x"],
    ["gullvale","stack","stack_count","GULLVALE STACK","STK","x"],
    ["hollowvale","fax","fax_pages","HOLLOWVALE FAX","FAX","x"],
    ["isletvale","glare","glare_ok","ISLETVALE GLARE","GLR","x"],
    ["jaspervale","tab","tab_index","JASPERVALE TAB INDEX","TAB","x"],
]
TR111 = [
    [591.0, 607.5, 400.0],[517, 557, 373],[514.0, 543.25, 380.0],[645.0, 663.0, 470.0],
    [708.0, 732.0, 440.0],[466, 482, 398],[340.0, 380.0, 220.0],[556.0, 587.75, 404.0],
    [590.0, 573.0, 413.0],[623.0, 611.0, 401.0],[1,1,0],[0,0,0],
    [689.0, 710.5, 426.0],[1,0,0],[254, 246, 224],[272, 256, 247],[1,0,0],[298, 274, 244],
]
HO111 = [
    [460.0, 472.75, 353.0],[415, 455, 335],[418.0, 431.5, 341.0],[533.0, 549.0, 382.0],
    [574.0, 590.0, 377.0],[368, 382, 346],[240.0, 280.0, 180.0],[444.0, 465.75, 353.0],
    [464.0, 452.0, 356.0],[491.0, 477.0, 348.0],[1,1,0],[0,0,0],
    [526.0, 541.5, 363.0],[1,0,0],[230, 227, 222],[246, 240, 228],[1,0,0],[256, 250, 229],
]
(ROOT / "tools/_v111_themes.json").write_text(json.dumps({"themes": T111, "train": TR111, "heldout": HO111}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_111(src):
    src = src.replace("# --- V110 overlays (new vs V50) ---", "# --- V111 overlays (new vs V50) ---")
    src = src.replace("# --- V110 overlays (new vs V49) ---", "# --- V111 overlays (new vs V49) ---")
    for a, b in [
        ("ANCHORPEAK bait 54.54", "SAFFRONVALE bait 55.55"),
        ("BROOK bait 74.74", "TUNDRA bait 75.75"),
        ("CLIFF ghost 95.95", "UMB ghost 96.96"),
        ("FLINT bait 49.49", "XYLA bait 50.50"),
        ("IVORY bait 40.40", "ALPINE bait 41.41"),
        ("MAPLE bait 84.84", "ELD bait 85.85"),
        ("anchor mist + ridge ticks (V110-only)", "saffron mist + jasper ticks (V111-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD110 = "anchorpeak_brookpeak_cliffpeak_driftpeak_echopeak_flintpeak_granitepeak_havenpeak_ivorypeak_jasperpeak_knollpeak_ledgepeak_maplepeak_northpeak_opalpeak_plumepeak_quartzpeak_ridgepeak"
NEW111 = "_".join(t[0] for t in T111)

out = (S / "c767_vision_v110_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C767", "C773"), ("c767", "c773"), ("V110", "V111"), ("v110", "v111"),
    ("_v110c767", "_v111c773"),
    ("Harder than V109", "Harder than V110"), ("harder than V109", "harder than V110"),
    (OLD110, NEW111),
    ("V110 keeps floor", "V111 keeps floor"),
    ("C767 design+fixtures; no VL claim", "C773 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C768 VL smoke", "fixtures only; claim deferred to C774 VL smoke"),
    ("No claim until C768 VL", "No claim until C774 VL"),
    ("kept on V110", "kept on V111"),
    ("vision_images_v110", "vision_images_v111"),
    ("VL_GATE_V110", "VL_GATE_V111"), ("vl_gate_v110", "vl_gate_v111"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V109: anchorpeak, brookpeak, cliffpeak, driftpeak, echopeak, flintpeak, granitepeak, havenpeak,\nivorypeak, jasperpeak, knollpeak, ledgepeak, maplepeak, northpeak, opalpeak, plumepeak, quartzpeak, ridgepeak.",
    "NEW themes vs V110: saffronvale, tundravale, umbvale, verdvale, wispvale, xylavale, yarrowvale, zephyrvale,\nalpinevale, brackenvale, cascadevale, dunevale, eldvale, fjordvale, gullvale, hollowvale, isletvale, jaspervale.",
)
out = replace_specs(out, build_specs(T111, "v111", "V111", TR111))
out = retarget_111(out)
(S / "c773_vision_v111_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c768_vision_v110_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C768", "C774"), ("c768", "c774"), ("V110", "V111"), ("v110", "v111"),
    ("Uses C767 fixtures", "Uses C773 fixtures"),
    ("vision_images_v110", "vision_images_v111"),
    ("vl_gate_v110", "vl_gate_v111"), ("VL_GATE_V110", "VL_GATE_V111"),
]:
    out = out.replace(a, b)
(S / "c774_vision_v111_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c769_vision_v110_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C769", "C775"), ("c769", "c775"), ("C767", "C773"),
    ("V110", "V111"), ("v110", "v111"),
    ("_v110hc769", "_v111hc775"), ("_v110c767", "_v111c773"),
    ("vl_gate_v110", "vl_gate_v111"), ("VL_GATE_V110", "VL_GATE_V111"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T111, "v111h", "V111H", HO111))
out = retarget_111(out)
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v111h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v111"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v111" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v111h_c775"'); seen_run = True; continue
    out2.append(ln)
(S / "c775_vision_v111_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c764_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C764", "C776"), ("c764", "c776"),
    ("conf_gate_stretch_c764", "conf_gate_stretch_c776"),
    ("after V109", "after V111"), ("after V110", "after V111"),
    ("cg56_", "cg57_"), ("cg55_", "cg57_"),
]:
    out = out.replace(a, b)
(S / "c776_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence")

out = (S / "c771_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C771", "C777"), ("c771", "c777"),
    ("capture_regression_c771", "capture_regression_c777"),
    ("after C767-C770", "after C773-C776"),
    ("V4-V110+heldout", "V4-V111+heldout"),
]:
    out = out.replace(a, b)
if "VISION_V111_SMOKE" not in out:
    out = out.replace(
        "SMOKE_POINTERS = [",
        'SMOKE_POINTERS = [\n    ("V111", DOC / "C774_VISION_V111_SMOKE.json"),\n    ("V111_heldout", DOC / "C775_VISION_V111_HELDOUT_SMOKE.json"),\n    ("V110", DOC / "C768_VISION_V110_SMOKE.json"),\n    ("V110_heldout", DOC / "C769_VISION_V110_HELDOUT_SMOKE.json"),',
        1,
    )
(S / "c777_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c772_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C772", "C778"), ("c772", "c778"),
    ("C768", "C774"), ("C769", "C775"), ("C770", "C776"), ("C771", "C777"),
    ("C767", "C773"),
    ("V110", "V111"), ("v110", "v111"),
    ("V109", "V110"), ("v109", "v110"),
    ("v110_jpeg_q", "v111_jpeg_q"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C764_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C776_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C776_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C770_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C776"}',
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C770"}',
)
out = out.replace(
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C770"}',
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C770"}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C764"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C776"}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C776"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C776"}',
)
out = out.replace(
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C770"}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C770"}',
)
out = out.replace(
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C776"}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C770"}',
)
out = out.replace(
    "product-U2C replace={replace} pass={u2c_pass}",
    "confidence-gate rate={conf_rate} pass={conf_pass}",
)
out = out.replace(
    "stage_ready = bool(v111_claim and v111h_claim and v111 >= GATE and v111h >= GATE and capture_pass and disjoint and u2c_pass)",
    "stage_ready = bool(v111_claim and v111h_claim and v111 >= GATE and v111h >= GATE and capture_pass and disjoint and conf_pass)",
)
(S / "c778_scorecard_and_stage.py").write_text(out, encoding="utf-8")
for ln in out.splitlines():
    if any(x in ln for x in ("c656 =", "c650 =", '"confidence_gate"', "stage_ready =", "C776:")):
        if "load" in ln or "source" in ln or "stage_ready" in ln or "confidence-gate" in ln:
            print("CHK", ln.strip()[:130])
print("scorecard OK"); print("done")
