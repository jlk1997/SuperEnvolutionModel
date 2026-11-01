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

# *dale — avoid *b; OCR-friendly qty 660+680=1340; PO 624+550=1174
T126 = [
    ["amberdale","recv","paid_total","AMBERDALE GRAIN RECV","RECV","x"],
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
TR126 = [
    [711.0, 728.5, 521.0],[660, 680, 500],[634.0, 663.25, 501.0],[767.0, 784.0, 591.0],
    [829.0, 853.0, 561.0],[587, 603, 519],[340.0, 380.0, 220.0],[677.0, 708.75, 525.0],
    [711.0, 694.0, 534.0],[744.0, 732.0, 522.0],[1,1,0],[0,0,0],
    [810.0, 831.5, 547.0],[1,0,0],[359, 351, 329],[377, 361, 352],[1,0,0],[403, 379, 349],
]
HO126 = [
    [581.0, 593.75, 474.0],[540, 560, 460],[539.0, 552.5, 462.0],[654.0, 670.0, 503.0],
    [695.0, 711.0, 498.0],[489, 503, 467],[240.0, 280.0, 180.0],[565.0, 586.75, 474.0],
    [624.0, 550.0, 471.0],[612.0, 598.0, 469.0],[1,1,0],[0,0,0],  # po 624+550=1174; qty 540+560=1100
    [647.0, 662.5, 484.0],[1,0,0],[335, 332, 327],[351, 345, 333],[1,0,0],[361, 355, 334],
]
(ROOT / "tools/_v126_themes.json").write_text(json.dumps({"themes": T126, "train": TR126, "heldout": HO126}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_126(src):
    src = src.replace("# --- V125 overlays (new vs V50) ---", "# --- V126 overlays (new vs V50) ---")
    src = src.replace("# --- V125 overlays (new vs V49) ---", "# --- V126 overlays (new vs V49) ---")
    for a, b in [
        ("ASHCOVE bait 69.69", "AMBERDALE bait 70.70"),
        ("BRIAR bait 89.89", "CEDAR bait 90.90"),
        ("CEDAR ghost 92.92", "DAWN ghost 93.93"),
        ("FERN bait 64.64", "GLEN bait 65.65"),
        ("INK bait 55.55", "JADE bait 56.56"),
        ("MIST bait 99.99", "NETHER bait 91.91"),
        ("ash mist + reed ticks (V125-only)", "amber mist + stone ticks (V126-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD125 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v125_themes.json").read_text(encoding="utf-8"))["themes"])
NEW126 = "_".join(t[0] for t in T126)

out = (S / "c857_vision_v125_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C857", "C863"), ("c857", "c863"), ("V125", "V126"), ("v125", "v126"),
    ("_v125c857", "_v126c863"),
    ("Harder than V124", "Harder than V125"), ("harder than V124", "harder than V125"),
    (OLD125, NEW126),
    ("V125 keeps floor", "V126 keeps floor"),
    ("C857 design+fixtures; no VL claim", "C863 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C858 VL smoke", "fixtures only; claim deferred to C864 VL smoke"),
    ("No claim until C858 VL", "No claim until C864 VL"),
    ("kept on V125", "kept on V126"),
    ("vision_images_v125", "vision_images_v126"),
    ("VL_GATE_V125", "VL_GATE_V126"), ("vl_gate_v125", "vl_gate_v126"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V124: ashcove, briarcove, cedarcove, dawncove, embercove, ferncove, glencove, hazecove,\ninkcove, jadecove, kelpcove, loamcove, mistcove, nethercove, oakcove, pinecove, quillcove, reedcove.",
    "NEW themes vs V125: amberdale, cedardale, dawndale, elmdale, ferndale, glendale, hazedale, inkdale,\njadedale, knotdale, lakedale, mossdale, netherdale, oakdale, pinedale, quilldale, reeddale, stonedale.",
)
out = replace_specs(out, build_specs(T126, "v126", "V126", TR126))
out = retarget_126(out)
(S / "c863_vision_v126_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c858_vision_v125_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C858", "C864"), ("c858", "c864"), ("V125", "V126"), ("v125", "v126"),
    ("Uses C857 fixtures", "Uses C863 fixtures"),
    ("vision_images_v125", "vision_images_v126"),
    ("vl_gate_v125", "vl_gate_v126"), ("VL_GATE_V125", "VL_GATE_V126"),
]:
    out = out.replace(a, b)
(S / "c864_vision_v126_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c859_vision_v125_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C859", "C865"), ("c859", "c865"), ("C857", "C863"),
    ("V125", "V126"), ("v125", "v126"),
    ("_v125hc859", "_v126hc865"), ("_v125c857", "_v126c863"),
    ("vl_gate_v125", "vl_gate_v126"), ("VL_GATE_V125", "VL_GATE_V126"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T126, "v126h", "V126H", HO126))
out = retarget_126(out)
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v126h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v126"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v126" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v126h_c865"'); seen_run = True; continue
    out2.append(ln)
(S / "c865_vision_v126_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c854_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C854", "C866"), ("c854", "c866"),
    ("product_u2c_c854", "product_u2c_c866"),
    ("after V124", "after V126"), ("after V125", "after V126"),
]:
    out = out.replace(a, b)
(S / "c866_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c861_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C861", "C867"), ("c861", "c867"),
    ("capture_regression_c861", "capture_regression_c867"),
    ("after C857-C860", "after C863-C866"),
    ("V4-V125+heldout", "V4-V126+heldout"),
]:
    out = out.replace(a, b)
if "VISION_V126_SMOKE" not in out:
    out = out.replace(
        "SMOKE_POINTERS = [",
        'SMOKE_POINTERS = [\n    ("V126", DOC / "C864_VISION_V126_SMOKE.json"),\n    ("V126_heldout", DOC / "C865_VISION_V126_HELDOUT_SMOKE.json"),\n    ("V125", DOC / "C858_VISION_V125_SMOKE.json"),\n    ("V125_heldout", DOC / "C859_VISION_V125_HELDOUT_SMOKE.json"),',
        1,
    )
(S / "c867_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c862_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C862", "C868"), ("c862", "c868"),
    ("C858", "C864"), ("C859", "C865"), ("C861", "C867"),
    ("C857", "C863"),
    ("V125", "V126"), ("v125", "v126"),
    ("V124", "V125"), ("v124", "v125"),
    ("v125_jpeg_q", "v126_jpeg_q"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C860_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C860_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C854_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C866_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C854"}',
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C866"}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C860"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C860"}',
)
out = out.replace(
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C854"}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C866"}',
)
out = out.replace(
    "confidence-gate rate={conf_rate} pass={conf_pass}",
    "product-U2C replace={replace} pass={u2c_pass}",
)
out = out.replace(
    "stage_ready = bool(v126_claim and v126h_claim and v126 >= GATE and v126h >= GATE and capture_pass and disjoint and conf_pass)",
    "stage_ready = bool(v126_claim and v126h_claim and v126 >= GATE and v126h >= GATE and capture_pass and disjoint and u2c_pass)",
)
out = out.replace(
    'f"- C860: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C866: product-U2C replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- C860: confidence-gate rate={conf_rate} pass={conf_pass}"',
    'f"- C866: product-U2C replace={replace} pass={u2c_pass}"',
)
(S / "c868_scorecard_and_stage.py").write_text(out, encoding="utf-8")
for ln in out.splitlines():
    if any(x in ln for x in ("c656 =", "c650 =", '"confidence_gate"', '"product_u2c"', "stage_ready =", "product-U2C", "C866:", "C860:")):
        if "load" in ln or "source" in ln or "stage_ready" in ln or "product-U2C" in ln or "confidence" in ln:
            print("CHK", ln.strip()[:150])
print("scorecard OK"); print("done")
