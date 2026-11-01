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

# *holm — qty TR 840+760 HO 740+780; PO TR 840+760=1600 HO 780+740=1520; SLA 490+530
T144 = [
    ["ashholm","recv","paid_total","ASHHOLM GRAIN RECV","RECV","x"],
    ["cedarholm","wh","qty_sum","WH CEDARHOLM BIN","RECV","x"],
    ["dawnholm","refund","refund_done","DAWNHOLM PATCH REFUND","DONE","x"],
    ["elmholm","tax","tax_base_paid","ELMHOLM TAX SLIP","TAX","x"],
    ["fernholm","pay","payroll_active","FERNHOLM PAYROLL","PAY","x"],
    ["glenholm","ship","ship_ok","GLENHOLM SHIP DOCK","SHIP","x"],
    ["hazeholm","sla","sla_ok_hours","HAZEHOLM SLA CARD","SLA","x"],
    ["inkholm","exp","exp_sum","INKHOLM EXPENSE","EXP","x"],
    ["jadeholm","po","po_open","JADEHOLM PO SHEET","PO","x"],
    ["knotholm","order","order_paid","KNOTHOLM ORDER","ORD","x"],
    ["lakeholm","dup","dup_mark","LAKEHOLM DUP MARK","DUP","x"],
    ["mossholm","zero","zero_check","MOSSHOLM AIR ZERO","ZERO","x"],
    ["netherholm","ledger","ledger_net","NETHERHOLM LEDGER","LED","x"],
    ["oakholm","ui","ui_ok","OAKHOLM UI SCAN","UI","x"],
    ["pineholm","stack","stack_count","PINEHOLM STACK","STK","x"],
    ["quillholm","fax","fax_pages","QUILLHOLM FAX","FAX","x"],
    ["reedholm","glare","glare_ok","REEDHOLM GLARE","GLR","x"],
    ["stoneholm","tab","tab_index","STONEHOLM TAB INDEX","TAB","x"],
]
TR144 = [
    [882.0, 899.5, 692.0],[840, 760, 680],[805.0, 834.25, 672.0],[938.0, 955.0, 762.0],
    [1000.0, 1024.0, 732.0],[758, 774, 690],[490.0, 530.0, 370.0],[848.0, 879.75, 696.0],
    [840.0, 760.0, 700.0],[915.0, 903.0, 693.0],[1,1,0],[0,0,0],  # po 840+760=1600; qty 840+760=1600
    [981.0, 1002.5, 718.0],[1,0,0],[530, 522, 500],[548, 532, 523],[1,0,0],[574, 550, 520],
]
HO144 = [
    [752.0, 764.75, 645.0],[740, 780, 640],[710.0, 723.5, 633.0],[825.0, 841.0, 674.0],
    [866.0, 882.0, 669.0],[660, 674, 638],[390.0, 430.0, 330.0],[736.0, 757.75, 645.0],
    [780.0, 740.0, 642.0],[783.0, 769.0, 640.0],[1,1,0],[0,0,0],  # po 780+740=1520; qty 740+780=1520
    [818.0, 833.5, 655.0],[1,0,0],[506, 503, 498],[522, 516, 504],[1,0,0],[532, 526, 505],
]
(ROOT / "tools/_v144_themes.json").write_text(json.dumps({"themes": T144, "train": TR144, "heldout": HO144}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_144(src):
    src = src.replace("# --- V143 overlays (new vs V50) ---", "# --- V144 overlays (new vs V50) ---")
    src = src.replace("# --- V143 overlays (new vs V49) ---", "# --- V144 overlays (new vs V49) ---")
    for a, b in [
        ("ASHFORD bait 77.77", "ASHHOLM bait 78.78"),
        ("CEDARF bait 87.87", "CEDARH bait 80.80"),
        ("DAWNF ghost 91.91", "DAWNH ghost 92.92"),
        ("GLENF bait 72.72", "GLENH bait 73.73"),
        ("JADEF bait 63.63", "JADEH bait 64.64"),
        ("NETHERF bait 89.89", "NETHERH bait 81.81"),
        ("ash mist + stone ticks (V143-only)", "ash mist + stone ticks (V144-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD143 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v143_themes.json").read_text(encoding="utf-8"))["themes"])
NEW144 = "_".join(t[0] for t in T144)

out = (S / "c965_vision_v143_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C965", "C971"), ("c965", "c971"), ("V143", "V144"), ("v143", "v144"),
    ("_v143c965", "_v144c971"),
    ("Harder than V142", "Harder than V143"), ("harder than V142", "harder than V143"),
    (OLD143, NEW144),
    ("V143 keeps floor", "V144 keeps floor"),
    ("C965 design+fixtures; no VL claim", "C971 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C966 VL smoke", "fixtures only; claim deferred to C972 VL smoke"),
    ("No claim until C966 VL", "No claim until C972 VL"),
    ("kept on V143", "kept on V144"),
    ("vision_images_v143", "vision_images_v144"),
    ("VL_GATE_V143", "VL_GATE_V144"), ("vl_gate_v143", "vl_gate_v144"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V142: ashford, cedarford, dawnford, elmford, fernford, glenford, hazeford, inkford,\njadeford, knotford, lakeford, mossford, netherford, oakford, pineford, quillford, reedford, stoneford.",
    "NEW themes vs V143: ashnolm, cedarholm, dawnholm, elmholm, fernholm, glenholm, hazeholm, inkholm,\njadeholm, knotholm, lakeholm, mossholm, netherholm, oakholm, pineholm, quillholm, reedholm, stoneholm.",
)
out = replace_specs(out, build_specs(T144, "v144", "V144", TR144))
out = retarget_144(out)
(S / "c971_vision_v144_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c966_vision_v143_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C966", "C972"), ("c966", "c972"), ("V143", "V144"), ("v143", "v144"),
    ("vision_images_v143", "vision_images_v144"),
    ("VL_GATE_V143", "VL_GATE_V144"), ("vl_gate_v143", "vl_gate_v144"),
    ("runs/vision_v143", "runs/vision_v144"),
]:
    out = out.replace(a, b)
(S / "c972_vision_v144_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c967_vision_v143_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C967", "C973"), ("c967", "c973"), ("V143", "V144"), ("v143", "v144"),
    ("vision_images_v143h", "vision_images_v144h"),
    ("vision_images_v143", "vision_images_v144"),
    ("VL_GATE_V143", "VL_GATE_V144"), ("vl_gate_v143", "vl_gate_v144"),
    ("runs/vision_v143h", "runs/vision_v144h"),
    ("_v143c965", "_v144c971"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T144, "v144h", "V144H", HO144))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v144h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v144"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v144" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v144h_c973"'); seen_run = True; continue
    out2.append(ln)
(S / "c973_vision_v144_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c962_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C962", "C974"), ("c962", "c974"),
    ("product_u2c_c962", "product_u2c_c974"),
    ("after V142", "after V144"), ("after V143", "after V144"),
]:
    out = out.replace(a, b)
(S / "c974_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c")

out = (S / "c969_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C969", "C975"), ("c969", "c975"),
    ("capture_regression_c969", "capture_regression_c975"),
    ("after C965-C968", "after C971-C974"),
    ("V4-V143+heldout", "V4-V144+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V143", DOC / "C966_VISION_V143_SMOKE.json"),'
if needle in out and "VISION_V144_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V144", DOC / "C972_VISION_V144_SMOKE.json"),\n    ("V144_heldout", DOC / "C973_VISION_V144_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c975_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c970_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C970", "C976"), ("c970", "c976"),
    ("C966", "C972"), ("C967", "C973"), ("C969", "C975"),
    ("C965", "C971"), ("C968", "C974"),
    ("V143", "V144"), ("v143", "v144"),
    ("V142", "V143"), ("v142", "v143"),
]:
    out = out.replace(a, b)
# product knife: load C974 for u2c; keep C968 conf as prior
out = out.replace(
    'c650 = load("docs/r50/C962_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C974_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'c656 = load("docs/r50/C968_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C968_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace('"source": "C962"', '"source": "C974"')
# C968 -> C974 replace may have broken conf source; fix
out = out.replace(
    'c656 = load("docs/r50/C974_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C968_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C974"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C968"}',
)
out = out.replace(
    "stage_ready = bool(v144_claim and v144h_claim and v144 >= GATE and v144h >= GATE and capture_pass and disjoint and conf_pass)",
    "stage_ready = bool(v144_claim and v144h_claim and v144 >= GATE and v144h >= GATE and capture_pass and disjoint and u2c_pass)",
)
out = out.replace(
    'f"- C974: confidence-gate pass={conf_pass} rate={conf_rate}"',
    'f"- C974: product-U2C replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- product-U2C (prior C962): replace={replace} pass={u2c_pass}"',
    'f"- confidence-gate (prior C968): pass={conf_pass} rate={conf_rate}"',
)
(S / "c976_scorecard_and_stage.py").write_text(out, encoding="utf-8")
for ln in out.splitlines():
    if any(x in ln for x in ("c650 =", "c656 =", "stage_ready =", "C974:", "source")):
        if "load" in ln or "stage_ready" in ln or "C974" in ln or "source" in ln:
            print("CHK", ln.strip()[:180])
print("any_b", [t[0] for t in T144 if t[0].endswith("b")])
print("qty", TR144[1], HO144[1], "po", TR144[8], HO144[8])
print("done")
