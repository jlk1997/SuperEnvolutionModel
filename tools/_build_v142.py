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

# *vale — qty TR 780+740 HO 840+760; PO TR 840+760=1600 HO 780+740=1520; SLA 480+520
T142 = [
    ["ashvale","recv","paid_total","ASHVALE GRAIN RECV","RECV","x"],
    ["cedarvale","wh","qty_sum","WH CEDARVALE BIN","RECV","x"],
    ["dawnvale","refund","refund_done","DAWNVALE PATCH REFUND","DONE","x"],
    ["elmvale","tax","tax_base_paid","ELMVALE TAX SLIP","TAX","x"],
    ["fernvale","pay","payroll_active","FERNVALE PAYROLL","PAY","x"],
    ["glenvale","ship","ship_ok","GLENVALE SHIP DOCK","SHIP","x"],
    ["hazevale","sla","sla_ok_hours","HAZEVALE SLA CARD","SLA","x"],
    ["inkvale","exp","exp_sum","INKVALE EXPENSE","EXP","x"],
    ["jadevale","po","po_open","JADEVALE PO SHEET","PO","x"],
    ["knotvale","order","order_paid","KNOTVALE ORDER","ORD","x"],
    ["lakevale","dup","dup_mark","LAKEVALE DUP MARK","DUP","x"],
    ["mossvale","zero","zero_check","MOSSVALE AIR ZERO","ZERO","x"],
    ["nethervale","ledger","ledger_net","NETHERVALE LEDGER","LED","x"],
    ["oakvale","ui","ui_ok","OAKVALE UI SCAN","UI","x"],
    ["pinevale","stack","stack_count","PINEVALE STACK","STK","x"],
    ["quillvale","fax","fax_pages","QUILLVALE FAX","FAX","x"],
    ["reedvale","glare","glare_ok","REEDVALE GLARE","GLR","x"],
    ["stonevale","tab","tab_index","STONEVALE TAB INDEX","TAB","x"],
]
TR142 = [
    [862.0, 879.5, 672.0],[780, 740, 660],[785.0, 814.25, 652.0],[918.0, 935.0, 742.0],
    [980.0, 1004.0, 712.0],[738, 754, 670],[480.0, 520.0, 350.0],[828.0, 859.75, 676.0],
    [840.0, 760.0, 680.0],[895.0, 883.0, 673.0],[1,1,0],[0,0,0],  # po 840+760=1600; qty 780+740=1520
    [961.0, 982.5, 698.0],[1,0,0],[510, 502, 480],[528, 512, 503],[1,0,0],[554, 530, 500],
]
HO142 = [
    [732.0, 744.75, 625.0],[840, 760, 620],[690.0, 703.5, 613.0],[805.0, 821.0, 654.0],
    [846.0, 862.0, 649.0],[640, 654, 618],[370.0, 410.0, 310.0],[716.0, 737.75, 625.0],
    [780.0, 740.0, 622.0],[763.0, 749.0, 620.0],[1,1,0],[0,0,0],  # po 780+740=1520; qty 840+760=1600
    [798.0, 813.5, 635.0],[1,0,0],[486, 483, 478],[502, 496, 484],[1,0,0],[512, 506, 485],
]
(ROOT / "tools/_v142_themes.json").write_text(json.dumps({"themes": T142, "train": TR142, "heldout": HO142}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_142(src):
    src = src.replace("# --- V141 overlays (new vs V50) ---", "# --- V142 overlays (new vs V50) ---")
    src = src.replace("# --- V141 overlays (new vs V49) ---", "# --- V142 overlays (new vs V49) ---")
    for a, b in [
        ("ASHDALE bait 75.75", "ASHVALE bait 76.76"),
        ("CEDARD bait 85.85", "CEDARV bait 86.86"),
        ("DAWND ghost 99.99", "DAWNV ghost 90.90"),
        ("GLEND bait 70.70", "GLENV bait 71.71"),
        ("JADED bait 61.61", "JADEV bait 62.62"),
        ("NETHERD bait 87.87", "NETHERV bait 88.88"),
        ("ash mist + stone ticks (V141-only)", "ash mist + stone ticks (V142-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD141 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v141_themes.json").read_text(encoding="utf-8"))["themes"])
NEW142 = "_".join(t[0] for t in T142)

out = (S / "c953_vision_v141_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C953", "C959"), ("c953", "c959"), ("V141", "V142"), ("v141", "v142"),
    ("_v141c953", "_v142c959"),
    ("Harder than V140", "Harder than V141"), ("harder than V140", "harder than V141"),
    (OLD141, NEW142),
    ("V141 keeps floor", "V142 keeps floor"),
    ("C953 design+fixtures; no VL claim", "C959 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C954 VL smoke", "fixtures only; claim deferred to C960 VL smoke"),
    ("No claim until C954 VL", "No claim until C960 VL"),
    ("kept on V141", "kept on V142"),
    ("vision_images_v141", "vision_images_v142"),
    ("VL_GATE_V141", "VL_GATE_V142"), ("vl_gate_v141", "vl_gate_v142"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V140: ashdale, cedardale, dawndale, elmdale, ferndale, glendale, hazedale, inkdale,\njadedale, knotdale, lakedale, mossdale, netherdale, oakdale, pinedale, quilldale, reeddale, stonedale.",
    "NEW themes vs V141: ashvale, cedarvale, dawnvale, elmvale, fernvale, glenvale, hazevale, inkvale,\njadevale, knotvale, lakevale, mossvale, nethervale, oakvale, pinevale, quillvale, reedvale, stonevale.",
)
out = replace_specs(out, build_specs(T142, "v142", "V142", TR142))
out = retarget_142(out)
(S / "c959_vision_v142_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c954_vision_v141_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C954", "C960"), ("c954", "c960"), ("V141", "V142"), ("v141", "v142"),
    ("vision_images_v141", "vision_images_v142"),
    ("VL_GATE_V141", "VL_GATE_V142"), ("vl_gate_v141", "vl_gate_v142"),
    ("runs/vision_v141", "runs/vision_v142"),
]:
    out = out.replace(a, b)
(S / "c960_vision_v142_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c955_vision_v141_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C955", "C961"), ("c955", "c961"), ("V141", "V142"), ("v141", "v142"),
    ("vision_images_v141h", "vision_images_v142h"),
    ("vision_images_v141", "vision_images_v142"),
    ("VL_GATE_V141", "VL_GATE_V142"), ("vl_gate_v141", "vl_gate_v142"),
    ("runs/vision_v141h", "runs/vision_v142h"),
    ("_v141c953", "_v142c959"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T142, "v142h", "V142H", HO142))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v142h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v142"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v142" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v142h_c961"'); seen_run = True; continue
    out2.append(ln)
(S / "c961_vision_v142_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c950_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C950", "C962"), ("c950", "c962"),
    ("product_u2c_c950", "product_u2c_c962"),
    ("after V140", "after V142"), ("after V139", "after V142"),
]:
    out = out.replace(a, b)
(S / "c962_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c")

out = (S / "c957_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C957", "C963"), ("c957", "c963"),
    ("capture_regression_c957", "capture_regression_c963"),
    ("after C953-C956", "after C959-C962"),
    ("V4-V141+heldout", "V4-V142+heldout"),
]:
    out = out.replace(a, b)
if "VISION_V142_SMOKE" not in out:
    out = out.replace(
        'SMOKE_POINTERS = [',
        'SMOKE_POINTERS = [\n    ("V142", DOC / "C960_VISION_V142_SMOKE.json"),\n    ("V142_heldout", DOC / "C961_VISION_V142_HELDOUT_SMOKE.json"),',
        1,
    )
    # also try CHECKS style
    needle = '    ("V141", DOC / "C954_VISION_V141_SMOKE.json"),'
    if needle in out:
        out = out.replace(
            needle,
            '    ("V142", DOC / "C960_VISION_V142_SMOKE.json"),\n    ("V142_heldout", DOC / "C961_VISION_V142_HELDOUT_SMOKE.json"),\n' + needle,
            1,
        )
(S / "c963_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c958_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C958", "C964"), ("c958", "c964"),
    ("C954", "C960"), ("C955", "C961"), ("C957", "C963"),
    ("C953", "C959"), ("C956", "C962"),
    ("V141", "V142"), ("v141", "v142"),
    ("V140", "V141"), ("v140", "v141"),
]:
    out = out.replace(a, b)
# product knife this cycle: load C962 for u2c, keep C956 conf as prior
out = out.replace(
    'c650 = load("docs/r50/C950_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C962_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'c656 = load("docs/r50/C956_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C956_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace('"source": "C950"', '"source": "C962"')
out = out.replace('"source": "C956"', '"source": "C956"')  # conf prior
out = out.replace(
    "stage_ready = bool(v142_claim and v142h_claim and v142 >= GATE and v142h >= GATE and capture_pass and disjoint and conf_pass)",
    "stage_ready = bool(v142_claim and v142h_claim and v142 >= GATE and v142h >= GATE and capture_pass and disjoint and u2c_pass)",
)
# STAGE bullets: C962 should be product-U2C
out = out.replace(
    'f"- C962: confidence-gate pass={conf_pass} rate={conf_rate}"',
    'f"- C962: product-U2C replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- C962: confidence-gate rate={conf_rate} pass={conf_pass}"',
    'f"- C962: product-U2C replace={replace} pass={u2c_pass}"',
)
# if still has product-U2C (prior C950) line from c958, retarget
out = out.replace(
    'f"- product-U2C (prior C950): replace={replace} pass={u2c_pass}"',
    'f"- confidence-gate (prior C956): pass={conf_pass} rate={conf_rate}"',
)
(S / "c964_scorecard_and_stage.py").write_text(out, encoding="utf-8")
for ln in out.splitlines():
    if any(x in ln for x in ("c650 =", "c656 =", "stage_ready =", "C962:", "C959:", "source")):
        if "load" in ln or "stage_ready" in ln or "C962" in ln or "source" in ln:
            print("CHK", ln.strip()[:180])
print("scorecard OK"); print("done")
