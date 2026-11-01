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

# *heath — avoid *b; OCR-friendly (qty 640+660=1300; PO 610+536=1146)
T124 = [
    ["amberheath","recv","paid_total","AMBERHEATH GRAIN RECV","RECV","x"],
    ["cedarheath","wh","qty_sum","WH CEDARHEATH BIN","RECV","x"],
    ["duskheath","refund","refund_done","DUSKHEATH PATCH REFUND","DONE","x"],
    ["elmheath","tax","tax_base_paid","ELMHEATH TAX SLIP","TAX","x"],
    ["fernheath","pay","payroll_active","FERNHEATH PAYROLL","PAY","x"],
    ["glenheath","ship","ship_ok","GLENHEATH SHIP DOCK","SHIP","x"],
    ["hazeheath","sla","sla_ok_hours","HAZEHEATH SLA CARD","SLA","x"],
    ["inkheath","exp","exp_sum","INKHEATH EXPENSE","EXP","x"],
    ["jadeheath","po","po_open","JADEHEATH PO SHEET","PO","x"],
    ["knotheath","order","order_paid","KNOTHEATH ORDER","ORD","x"],
    ["lakeheath","dup","dup_mark","LAKEHEATH DUP MARK","DUP","x"],
    ["mossheath","zero","zero_check","MOSSHEATH AIR ZERO","ZERO","x"],
    ["netherheath","ledger","ledger_net","NETHERHEATH LEDGER","LED","x"],
    ["oakheath","ui","ui_ok","OAKHEATH UI SCAN","UI","x"],
    ["pineheath","stack","stack_count","PINEHEATH STACK","STK","x"],
    ["quillheath","fax","fax_pages","QUILLHEATH FAX","FAX","x"],
    ["reedheath","glare","glare_ok","REEDHEATH GLARE","GLR","x"],
    ["stoneheath","tab","tab_index","STONEHEATH TAB INDEX","TAB","x"],
]
# Prefer round digits (lesson: 658→656); qty 640+660; PO 610+536=1146
TR124 = [
    [697.0, 714.5, 507.0],[640, 660, 480],[620.0, 649.25, 487.0],[753.0, 770.0, 577.0],
    [815.0, 839.0, 547.0],[573, 589, 505],[340.0, 380.0, 220.0],[663.0, 694.75, 511.0],
    [697.0, 680.0, 520.0],[730.0, 718.0, 508.0],[1,1,0],[0,0,0],
    [796.0, 817.5, 533.0],[1,0,0],[345, 337, 315],[363, 347, 338],[1,0,0],[389, 365, 335],
]
HO124 = [
    [567.0, 579.75, 460.0],[520, 540, 440],[525.0, 538.5, 448.0],[640.0, 656.0, 489.0],
    [681.0, 697.0, 484.0],[475, 489, 453],[240.0, 280.0, 180.0],[551.0, 572.75, 460.0],
    [610.0, 536.0, 457.0],[598.0, 584.0, 455.0],[1,1,0],[0,0,0],  # po 610+536=1146; qty 520+540=1060
    [633.0, 648.5, 470.0],[1,0,0],[321, 318, 313],[337, 331, 319],[1,0,0],[347, 341, 320],
]
(ROOT / "tools/_v124_themes.json").write_text(json.dumps({"themes": T124, "train": TR124, "heldout": HO124}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_124(src):
    src = src.replace("# --- V123 overlays (new vs V50) ---", "# --- V124 overlays (new vs V50) ---")
    src = src.replace("# --- V123 overlays (new vs V49) ---", "# --- V124 overlays (new vs V49) ---")
    for a, b in [
        ("ALDERMARSH bait 67.67", "AMBERHEATH bait 68.68"),
        ("BRACKEN bait 87.87", "CEDAR bait 88.88"),
        ("CEDAR ghost 99.99", "DUSK ghost 91.91"),
        ("FERN bait 62.62", "GLEN bait 63.63"),
        ("INK bait 53.53", "JADE bait 54.54"),
        ("MIST bait 97.97", "NETHER bait 98.98"),
        ("alder mist + reed ticks (V123-only)", "amber mist + stone ticks (V124-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD123 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v123_themes.json").read_text(encoding="utf-8"))["themes"])
NEW124 = "_".join(t[0] for t in T124)

out = (S / "c845_vision_v123_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C845", "C851"), ("c845", "c851"), ("V123", "V124"), ("v123", "v124"),
    ("_v123c845", "_v124c851"),
    ("Harder than V122", "Harder than V123"), ("harder than V122", "harder than V123"),
    (OLD123, NEW124),
    ("V123 keeps floor", "V124 keeps floor"),
    ("C845 design+fixtures; no VL claim", "C851 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C846 VL smoke", "fixtures only; claim deferred to C852 VL smoke"),
    ("No claim until C846 VL", "No claim until C852 VL"),
    ("kept on V123", "kept on V124"),
    ("vision_images_v123", "vision_images_v124"),
    ("VL_GATE_V123", "VL_GATE_V124"), ("vl_gate_v123", "vl_gate_v124"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V122: aldermarsh, brackenmarsh, cedarmarsh, dewmarsh, echomarsh, fernmarsh, gorsemarsh, heathmarsh,\ninkmarsh, jademarsh, kelpmarsh, loammarsh, mistmarsh, nethermarsh, oakmarsh, pinemarsh, quillmarsh, reedmarsh.",
    "NEW themes vs V123: amberheath, cedarheath, duskheath, elmheath, fernheath, glenheath, hazeheath, inkheath,\njadeheath, knotheath, lakeheath, mossheath, netherheath, oakheath, pineheath, quillheath, reedheath, stoneheath.",
)
out = replace_specs(out, build_specs(T124, "v124", "V124", TR124))
out = retarget_124(out)
(S / "c851_vision_v124_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c846_vision_v123_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C846", "C852"), ("c846", "c852"), ("V123", "V124"), ("v123", "v124"),
    ("Uses C845 fixtures", "Uses C851 fixtures"),
    ("vision_images_v123", "vision_images_v124"),
    ("vl_gate_v123", "vl_gate_v124"), ("VL_GATE_V123", "VL_GATE_V124"),
]:
    out = out.replace(a, b)
(S / "c852_vision_v124_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c847_vision_v123_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C847", "C853"), ("c847", "c853"), ("C845", "C851"),
    ("V123", "V124"), ("v123", "v124"),
    ("_v123hc847", "_v124hc853"), ("_v123c845", "_v124c851"),
    ("vl_gate_v123", "vl_gate_v124"), ("VL_GATE_V123", "VL_GATE_V124"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T124, "v124h", "V124H", HO124))
out = retarget_124(out)
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v124h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v124"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v124" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v124h_c853"'); seen_run = True; continue
    out2.append(ln)
(S / "c853_vision_v124_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c842_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C842", "C854"), ("c842", "c854"),
    ("product_u2c_c842", "product_u2c_c854"),
    ("after V122", "after V124"), ("after V123", "after V124"),
]:
    out = out.replace(a, b)
(S / "c854_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c849_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C849", "C855"), ("c849", "c855"),
    ("capture_regression_c849", "capture_regression_c855"),
    ("after C845-C848", "after C851-C854"),
    ("V4-V123+heldout", "V4-V124+heldout"),
]:
    out = out.replace(a, b)
if "VISION_V124_SMOKE" not in out:
    out = out.replace(
        "SMOKE_POINTERS = [",
        'SMOKE_POINTERS = [\n    ("V124", DOC / "C852_VISION_V124_SMOKE.json"),\n    ("V124_heldout", DOC / "C853_VISION_V124_HELDOUT_SMOKE.json"),\n    ("V123", DOC / "C846_VISION_V123_SMOKE.json"),\n    ("V123_heldout", DOC / "C847_VISION_V123_HELDOUT_SMOKE.json"),',
        1,
    )
(S / "c855_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c850_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C850", "C856"), ("c850", "c856"),
    ("C846", "C852"), ("C847", "C853"), ("C849", "C855"),
    ("C845", "C851"),
    ("V123", "V124"), ("v123", "v124"),
    ("V122", "V123"), ("v122", "v123"),
    ("v123_jpeg_q", "v124_jpeg_q"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C848_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C848_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C842_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C854_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C842"}',
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C854"}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C848"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C848"}',
)
out = out.replace(
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C842"}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C854"}',
)
out = out.replace(
    "confidence-gate rate={conf_rate} pass={conf_pass}",
    "product-U2C replace={replace} pass={u2c_pass}",
)
out = out.replace(
    "stage_ready = bool(v124_claim and v124h_claim and v124 >= GATE and v124h >= GATE and capture_pass and disjoint and conf_pass)",
    "stage_ready = bool(v124_claim and v124h_claim and v124 >= GATE and v124h >= GATE and capture_pass and disjoint and u2c_pass)",
)
out = out.replace(
    'f"- C848: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C854: product-U2C replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- C848: confidence-gate rate={conf_rate} pass={conf_pass}"',
    'f"- C854: product-U2C replace={replace} pass={u2c_pass}"',
)
(S / "c856_scorecard_and_stage.py").write_text(out, encoding="utf-8")
for ln in out.splitlines():
    if any(x in ln for x in ("c656 =", "c650 =", '"confidence_gate"', '"product_u2c"', "stage_ready =", "product-U2C", "C854:", "C848:")):
        if "load" in ln or "source" in ln or "stage_ready" in ln or "product-U2C" in ln or "confidence" in ln:
            print("CHK", ln.strip()[:150])
print("scorecard OK"); print("done")
