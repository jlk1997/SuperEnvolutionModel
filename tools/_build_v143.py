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

# *ford — qty TR 740+780 HO 780+740; PO TR 780+740=1520 HO 840+760=1600; SLA 470+510
T143 = [
    ["ashford","recv","paid_total","ASHFORD GRAIN RECV","RECV","x"],
    ["cedarford","wh","qty_sum","WH CEDARFORD BIN","RECV","x"],
    ["dawnford","refund","refund_done","DAWNFORD PATCH REFUND","DONE","x"],
    ["elmford","tax","tax_base_paid","ELMFORD TAX SLIP","TAX","x"],
    ["fernford","pay","payroll_active","FERNFORD PAYROLL","PAY","x"],
    ["glenford","ship","ship_ok","GLENFORD SHIP DOCK","SHIP","x"],
    ["hazeford","sla","sla_ok_hours","HAZEFORD SLA CARD","SLA","x"],
    ["inkford","exp","exp_sum","INKFORD EXPENSE","EXP","x"],
    ["jadeford","po","po_open","JADEFORD PO SHEET","PO","x"],
    ["knotford","order","order_paid","KNOTFORD ORDER","ORD","x"],
    ["lakeford","dup","dup_mark","LAKEFORD DUP MARK","DUP","x"],
    ["mossford","zero","zero_check","MOSSFORD AIR ZERO","ZERO","x"],
    ["netherford","ledger","ledger_net","NETHERFORD LEDGER","LED","x"],
    ["oakford","ui","ui_ok","OAKFORD UI SCAN","UI","x"],
    ["pineford","stack","stack_count","PINEFORD STACK","STK","x"],
    ["quillford","fax","fax_pages","QUILLFORD FAX","FAX","x"],
    ["reedford","glare","glare_ok","REEDFORD GLARE","GLR","x"],
    ["stoneford","tab","tab_index","STONEFORD TAB INDEX","TAB","x"],
]
TR143 = [
    [872.0, 889.5, 682.0],[740, 780, 670],[795.0, 824.25, 662.0],[928.0, 945.0, 752.0],
    [990.0, 1014.0, 722.0],[748, 764, 680],[470.0, 510.0, 360.0],[838.0, 869.75, 686.0],
    [780.0, 740.0, 690.0],[905.0, 893.0, 683.0],[1,1,0],[0,0,0],  # po 780+740=1520; qty 740+780=1520
    [971.0, 992.5, 708.0],[1,0,0],[520, 512, 490],[538, 522, 513],[1,0,0],[564, 540, 510],
]
HO143 = [
    [742.0, 754.75, 635.0],[780, 740, 630],[700.0, 713.5, 623.0],[815.0, 831.0, 664.0],
    [856.0, 872.0, 659.0],[650, 664, 628],[380.0, 420.0, 320.0],[726.0, 747.75, 635.0],
    [840.0, 760.0, 632.0],[773.0, 759.0, 630.0],[1,1,0],[0,0,0],  # po 840+760=1600; qty 780+740=1520
    [808.0, 823.5, 645.0],[1,0,0],[496, 493, 488],[512, 506, 494],[1,0,0],[522, 516, 495],
]
(ROOT / "tools/_v143_themes.json").write_text(json.dumps({"themes": T143, "train": TR143, "heldout": HO143}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_143(src):
    src = src.replace("# --- V142 overlays (new vs V50) ---", "# --- V143 overlays (new vs V50) ---")
    src = src.replace("# --- V142 overlays (new vs V49) ---", "# --- V143 overlays (new vs V49) ---")
    for a, b in [
        ("ASHVALE bait 76.76", "ASHFORD bait 77.77"),
        ("CEDARV bait 86.86", "CEDARF bait 87.87"),
        ("DAWNV ghost 90.90", "DAWNF ghost 91.91"),
        ("GLENV bait 71.71", "GLENF bait 72.72"),
        ("JADEV bait 62.62", "JADEF bait 63.63"),
        ("NETHERV bait 88.88", "NETHERF bait 89.89"),
        ("ash mist + stone ticks (V142-only)", "ash mist + stone ticks (V143-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD142 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v142_themes.json").read_text(encoding="utf-8"))["themes"])
NEW143 = "_".join(t[0] for t in T143)

out = (S / "c959_vision_v142_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C959", "C965"), ("c959", "c965"), ("V142", "V143"), ("v142", "v143"),
    ("_v142c959", "_v143c965"),
    ("Harder than V141", "Harder than V142"), ("harder than V141", "harder than V142"),
    (OLD142, NEW143),
    ("V142 keeps floor", "V143 keeps floor"),
    ("C959 design+fixtures; no VL claim", "C965 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C960 VL smoke", "fixtures only; claim deferred to C966 VL smoke"),
    ("No claim until C960 VL", "No claim until C966 VL"),
    ("kept on V142", "kept on V143"),
    ("vision_images_v142", "vision_images_v143"),
    ("VL_GATE_V142", "VL_GATE_V143"), ("vl_gate_v142", "vl_gate_v143"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V141: ashvale, cedarvale, dawnvale, elmvale, fernvale, glenvale, hazevale, inkvale,\njadevale, knotvale, lakevale, mossvale, nethervale, oakvale, pinevale, quillvale, reedvale, stonevale.",
    "NEW themes vs V142: ashford, cedarford, dawnford, elmford, fernford, glenford, hazeford, inkford,\njadeford, knotford, lakeford, mossford, netherford, oakford, pineford, quillford, reedford, stoneford.",
)
out = replace_specs(out, build_specs(T143, "v143", "V143", TR143))
out = retarget_143(out)
(S / "c965_vision_v143_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c960_vision_v142_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C960", "C966"), ("c960", "c966"), ("V142", "V143"), ("v142", "v143"),
    ("vision_images_v142", "vision_images_v143"),
    ("VL_GATE_V142", "VL_GATE_V143"), ("vl_gate_v142", "vl_gate_v143"),
    ("runs/vision_v142", "runs/vision_v143"),
]:
    out = out.replace(a, b)
(S / "c966_vision_v143_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c961_vision_v142_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C961", "C967"), ("c961", "c967"), ("V142", "V143"), ("v142", "v143"),
    ("vision_images_v142h", "vision_images_v143h"),
    ("vision_images_v142", "vision_images_v143"),
    ("VL_GATE_V142", "VL_GATE_V143"), ("vl_gate_v142", "vl_gate_v143"),
    ("runs/vision_v142h", "runs/vision_v143h"),
    ("_v142c959", "_v143c965"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T143, "v143h", "V143H", HO143))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v143h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v143"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v143" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v143h_c967"'); seen_run = True; continue
    out2.append(ln)
(S / "c967_vision_v143_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c956_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C956", "C968"), ("c956", "c968"),
    ("conf_gate_stretch_c956", "conf_gate_stretch_c968"),
    ("after V141", "after V143"), ("after V142", "after V143"),
    ("cg72_", "cg73_"),
]:
    out = out.replace(a, b)
(S / "c968_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence")

out = (S / "c963_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C963", "C969"), ("c963", "c969"),
    ("capture_regression_c963", "capture_regression_c969"),
    ("after C959-C962", "after C965-C968"),
    ("V4-V142+heldout", "V4-V143+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V142", DOC / "C960_VISION_V142_SMOKE.json"),'
if needle in out and "VISION_V143_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V143", DOC / "C966_VISION_V143_SMOKE.json"),\n    ("V143_heldout", DOC / "C967_VISION_V143_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c969_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c964_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C964", "C970"), ("c964", "c970"),
    ("C960", "C966"), ("C961", "C967"), ("C963", "C969"),
    ("C959", "C965"),
    ("V142", "V143"), ("v142", "v143"),
    ("V141", "V142"), ("v141", "v142"),
]:
    out = out.replace(a, b)
# conf knife this cycle
out = out.replace(
    'c650 = load("docs/r50/C962_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C962_PRODUCT_U2C_COST.json") or {}',  # keep prior u2c
)
out = out.replace(
    'c656 = load("docs/r50/C956_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C968_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace('"source": "C962"', '"source": "C962"')  # u2c prior
out = out.replace('"source": "C956"', '"source": "C968"')
out = out.replace(
    "stage_ready = bool(v143_claim and v143h_claim and v143 >= GATE and v143h >= GATE and capture_pass and disjoint and u2c_pass)",
    "stage_ready = bool(v143_claim and v143h_claim and v143 >= GATE and v143h >= GATE and capture_pass and disjoint and conf_pass)",
)
out = out.replace(
    'f"- C968: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C968: confidence-gate pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- C962: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C968: confidence-gate pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- confidence-gate (prior C956): pass={conf_pass} rate={conf_rate}"',
    'f"- product-U2C (prior C962): replace={replace} pass={u2c_pass}"',
)
(S / "c970_scorecard_and_stage.py").write_text(out, encoding="utf-8")
for ln in out.splitlines():
    if any(x in ln for x in ("c650 =", "c656 =", "stage_ready =", "C968:", "source")):
        if "load" in ln or "stage_ready" in ln or "C968" in ln or "source" in ln:
            print("CHK", ln.strip()[:180])
print("scorecard OK")
print("themes", [t[0] for t in T143])
print("qtyTR", TR143[1], "qtyHO", HO143[1], "poTR", TR143[8], "poHO", HO143[8])
print("any_b", [t[0] for t in T143 if t[0].endswith("b")])
print("done")
