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

# *dale — qty TR 860+900 HO 740+780; PO TR 870+760=1630 HO 780+590=1370; SLA 460+500
T141 = [
    ["ashdale","recv","paid_total","ASHDALE GRAIN RECV","RECV","x"],
    ["cedardale","wh","qty_sum","WH CEDARDALE BIN","RECV","x"],
    ["dawndale","refund","refund_done","DAWNDALE PATCH REFUND","DONE","x"],
    ["elmdale","tax","tax_base_paid","ELMDALE TAX SLIP","TAX","x"],
    ["ferndale","pay","payroll_active","FERNDALE PAYROLL","PAY","x"],
    ["glendale","ship","ship_ok","GLENDALE SHIP DOCK","SHIP","x"],
    ["hazedale","sla","sla_ok_hours","HAZEDALE SLA CARD","SLA","x"],
    ["inkdale","exp","exp_sum","INKDALE EXPENSE","EXP","x"],
    ["jadedale","po","po_open","JADEDALE PO SHEET","PO","x"],
    ["knotdale","order","order_paid","KNOTDALE ORDER","ORD","x"],
    ["lakedale","dup","dup_mark","LAKEDALE DUP MARK","DUP","x"],
    ["mossdale","zero","zero_check","MOSSDALE AIR ZERO","ZERO","x"],
    ["netherdale","ledger","ledger_net","NETHERDALE LEDGER","LED","x"],
    ["oakdale","ui","ui_ok","OAKDALE UI SCAN","UI","x"],
    ["pinedale","stack","stack_count","PINEDALE STACK","STK","x"],
    ["quilldale","fax","fax_pages","QUILLDALE FAX","FAX","x"],
    ["reeddale","glare","glare_ok","REEDDALE GLARE","GLR","x"],
    ["stonedale","tab","tab_index","STONEDALE TAB INDEX","TAB","x"],
]
TR141 = [
    [852.0, 869.5, 662.0],[860, 900, 650],[775.0, 804.25, 642.0],[908.0, 925.0, 732.0],
    [970.0, 994.0, 702.0],[728, 744, 660],[460.0, 500.0, 340.0],[818.0, 849.75, 666.0],
    [870.0, 760.0, 670.0],[885.0, 873.0, 663.0],[1,1,0],[0,0,0],  # po 870+760=1630
    [951.0, 972.5, 688.0],[1,0,0],[500, 492, 470],[518, 502, 493],[1,0,0],[544, 520, 490],
]
HO141 = [
    [722.0, 734.75, 615.0],[740, 780, 610],[680.0, 693.5, 603.0],[795.0, 811.0, 644.0],
    [836.0, 852.0, 639.0],[630, 644, 608],[360.0, 400.0, 300.0],[706.0, 727.75, 615.0],
    [780.0, 590.0, 612.0],[753.0, 739.0, 610.0],[1,1,0],[0,0,0],  # po 780+590=1370; qty 740+780=1520
    [788.0, 803.5, 625.0],[1,0,0],[476, 473, 468],[492, 486, 474],[1,0,0],[502, 496, 475],
]
(ROOT / "tools/_v141_themes.json").write_text(json.dumps({"themes": T141, "train": TR141, "heldout": HO141}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_141(src):
    src = src.replace("# --- V140 overlays (new vs V50) ---", "# --- V141 overlays (new vs V50) ---")
    src = src.replace("# --- V140 overlays (new vs V49) ---", "# --- V141 overlays (new vs V49) ---")
    for a, b in [
        ("ASHGROVE bait 74.74", "ASHDALE bait 75.75"),
        ("CEDARG bait 84.84", "CEDARD bait 85.85"),
        ("DAWNG ghost 98.98", "DAWND ghost 99.99"),
        ("GLENG bait 79.79", "GLEND bait 70.70"),
        ("JADEG bait 60.60", "JADED bait 61.61"),
        ("NETHERG bait 86.86", "NETHERD bait 87.87"),
        ("ash mist + stone ticks (V140-only)", "ash mist + stone ticks (V141-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD140 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v140_themes.json").read_text(encoding="utf-8"))["themes"])
NEW141 = "_".join(t[0] for t in T141)

out = (S / "c947_vision_v140_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C947", "C953"), ("c947", "c953"), ("V140", "V141"), ("v140", "v141"),
    ("_v140c947", "_v141c953"),
    ("Harder than V139", "Harder than V140"), ("harder than V139", "harder than V140"),
    (OLD140, NEW141),
    ("V140 keeps floor", "V141 keeps floor"),
    ("C947 design+fixtures; no VL claim", "C953 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C948 VL smoke", "fixtures only; claim deferred to C954 VL smoke"),
    ("No claim until C948 VL", "No claim until C954 VL"),
    ("kept on V140", "kept on V141"),
    ("vision_images_v140", "vision_images_v141"),
    ("VL_GATE_V140", "VL_GATE_V141"), ("vl_gate_v140", "vl_gate_v141"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V139: ashgrove, cedargrove, dawngrove, elmgrove, ferngrove, glengrove, hazegrove, inkgrove,\njadegrove, knotgrove, lakegrove, mossgrove, nethergrove, oakgrove, pinegrove, quillgrove, reedgrove, stonegrove.",
    "NEW themes vs V140: ashdale, cedardale, dawndale, elmdale, ferndale, glendale, hazedale, inkdale,\njadedale, knotdale, lakedale, mossdale, netherdale, oakdale, pinedale, quilldale, reeddale, stonedale.",
)
out = replace_specs(out, build_specs(T141, "v141", "V141", TR141))
out = retarget_141(out)
(S / "c953_vision_v141_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c948_vision_v140_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C948", "C954"), ("c948", "c954"), ("V140", "V141"), ("v140", "v141"),
    ("Uses C947 fixtures", "Uses C953 fixtures"),
    ("vision_images_v140", "vision_images_v141"),
    ("vl_gate_v140", "vl_gate_v141"), ("VL_GATE_V140", "VL_GATE_V141"),
]:
    out = out.replace(a, b)
(S / "c954_vision_v141_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c949_vision_v140_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C949", "C955"), ("c949", "c955"), ("C947", "C953"),
    ("V140", "V141"), ("v140", "v141"),
    ("_v140hc949", "_v141hc955"), ("_v140c947", "_v141c953"),
    ("vl_gate_v140", "vl_gate_v141"), ("VL_GATE_V140", "VL_GATE_V141"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T141, "v141h", "V141H", HO141))
out = retarget_141(out)
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v141h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v141"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v141" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v141h_c955"'); seen_run = True; continue
    out2.append(ln)
(S / "c955_vision_v141_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c944_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C944", "C956"), ("c944", "c956"),
    ("conf_gate_stretch_c944", "conf_gate_stretch_c956"),
    ("after V139", "after V141"), ("after V140", "after V141"),
    ("cg71_", "cg72_"),
]:
    out = out.replace(a, b)
(S / "c956_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence")

out = (S / "c951_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C951", "C957"), ("c951", "c957"),
    ("capture_regression_c951", "capture_regression_c957"),
    ("after C947-C950", "after C953-C956"),
    ("V4-V140+heldout", "V4-V141+heldout"),
]:
    out = out.replace(a, b)
if "VISION_V141_SMOKE" not in out:
    out = out.replace(
        "SMOKE_POINTERS = [",
        'SMOKE_POINTERS = [\n    ("V141", DOC / "C954_VISION_V141_SMOKE.json"),\n    ("V141_heldout", DOC / "C955_VISION_V141_HELDOUT_SMOKE.json"),\n    ("V140", DOC / "C948_VISION_V140_SMOKE.json"),\n    ("V140_heldout", DOC / "C949_VISION_V140_HELDOUT_SMOKE.json"),',
        1,
    )
(S / "c957_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c952_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C952", "C958"), ("c952", "c958"),
    ("C948", "C954"), ("C949", "C955"), ("C951", "C957"),
    ("C947", "C953"),
    ("V140", "V141"), ("v140", "v141"),
    ("V139", "V140"), ("v139", "v140"),
    ("v140_jpeg_q", "v141_jpeg_q"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C944_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C956_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C950_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C950_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C950"}',
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C950"}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C944"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C956"}',
)
out = out.replace(
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C950"}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C950"}',
)
out = out.replace(
    "product-U2C replace={replace} pass={u2c_pass}",
    "confidence-gate rate={conf_rate} pass={conf_pass}",
)
out = out.replace(
    "stage_ready = bool(v141_claim and v141h_claim and v141 >= GATE and v141h >= GATE and capture_pass and disjoint and u2c_pass)",
    "stage_ready = bool(v141_claim and v141h_claim and v141 >= GATE and v141h >= GATE and capture_pass and disjoint and conf_pass)",
)
out = out.replace(
    'f"- C950: confidence-gate rate={conf_rate} pass={conf_pass}"',
    'f"- C956: confidence-gate rate={conf_rate} pass={conf_pass}"',
)
out = out.replace(
    'f"- C950: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C956: confidence-gate rate={conf_rate} pass={conf_pass}"',
)
(S / "c958_scorecard_and_stage.py").write_text(out, encoding="utf-8")
for ln in out.splitlines():
    if any(x in ln for x in ("c656 =", "c650 =", '"confidence_gate"', '"product_u2c"', "stage_ready =", "confidence-gate", "C956:", "C950:")):
        if "load" in ln or "source" in ln or "stage_ready" in ln or "confidence-gate" in ln or "product" in ln:
            print("CHK", ln.strip()[:160])
print("scorecard OK"); print("done")
