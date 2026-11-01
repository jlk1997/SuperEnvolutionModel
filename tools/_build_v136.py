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

# *ridge — qty TR 760+800 HO 640+680 (avoid 7/5); PO TR 810+740=1550 HO 700+590=1290; SLA 410+450
T136 = [
    ["ashridge","recv","paid_total","ASHRIDGE GRAIN RECV","RECV","x"],
    ["cedarridge","wh","qty_sum","WH CEDARRIDGE BIN","RECV","x"],
    ["dawnridge","refund","refund_done","DAWNRIDGE PATCH REFUND","DONE","x"],
    ["elmridge","tax","tax_base_paid","ELMRIDGE TAX SLIP","TAX","x"],
    ["fernridge","pay","payroll_active","FERNRIDGE PAYROLL","PAY","x"],
    ["glenridge","ship","ship_ok","GLENRIDGE SHIP DOCK","SHIP","x"],
    ["hazeridge","sla","sla_ok_hours","HAZERIDGE SLA CARD","SLA","x"],
    ["inkridge","exp","exp_sum","INKRIDGE EXPENSE","EXP","x"],
    ["jaderidge","po","po_open","JADERIDGE PO SHEET","PO","x"],
    ["knorridge","order","order_paid","KNOTRIDGE ORDER","ORD","x"],
    ["lakeridge","dup","dup_mark","LAKERIDGE DUP MARK","DUP","x"],
    ["mossridge","zero","zero_check","MOSSRIDGE AIR ZERO","ZERO","x"],
    ["netherridge","ledger","ledger_net","NETHERRIDGE LEDGER","LED","x"],
    ["oakridge","ui","ui_ok","OAKRIDGE UI SCAN","UI","x"],
    ["pineridge","stack","stack_count","PINERIDGE STACK","STK","x"],
    ["quillridge","fax","fax_pages","QUILLRIDGE FAX","FAX","x"],
    ["reedridge","glare","glare_ok","REEDRIDGE GLARE","GLR","x"],
    ["stoneridge","tab","tab_index","STONERIDGE TAB INDEX","TAB","x"],
]
# fix knotridge name (not knorridge)
T136[9] = ["knotridge","order","order_paid","KNOTRIDGE ORDER","ORD","x"]
TR136 = [
    [802.0, 819.5, 612.0],[760, 800, 600],[725.0, 754.25, 592.0],[858.0, 875.0, 682.0],
    [920.0, 944.0, 652.0],[678, 694, 610],[410.0, 450.0, 290.0],[768.0, 799.75, 616.0],
    [810.0, 740.0, 620.0],[835.0, 823.0, 613.0],[1,1,0],[0,0,0],  # po 810+740=1550
    [901.0, 922.5, 638.0],[1,0,0],[450, 442, 420],[468, 452, 443],[1,0,0],[494, 470, 440],
]
HO136 = [
    [672.0, 684.75, 565.0],[640, 680, 560],[630.0, 643.5, 553.0],[745.0, 761.0, 594.0],
    [786.0, 802.0, 589.0],[580, 594, 558],[310.0, 350.0, 250.0],[656.0, 677.75, 565.0],
    [700.0, 590.0, 562.0],[703.0, 689.0, 560.0],[1,1,0],[0,0,0],  # po 700+590=1290; qty 640+680=1320
    [738.0, 753.5, 575.0],[1,0,0],[426, 423, 418],[442, 436, 424],[1,0,0],[452, 446, 425],
]
(ROOT / "tools/_v136_themes.json").write_text(json.dumps({"themes": T136, "train": TR136, "heldout": HO136}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_136(src):
    src = src.replace("# --- V135 overlays (new vs V50) ---", "# --- V136 overlays (new vs V50) ---")
    src = src.replace("# --- V135 overlays (new vs V49) ---", "# --- V136 overlays (new vs V49) ---")
    for a, b in [
        ("ASHHOLT bait 79.79", "ASHRIDGE bait 70.70"),
        ("CEDARH bait 89.89", "CEDARR bait 80.80"),
        ("DAWNH ghost 93.93", "DAWNR ghost 94.94"),
        ("GLENH bait 74.74", "GLENR bait 75.75"),
        ("JADEH bait 65.65", "JADER bait 66.66"),
        ("NETHERH bait 81.81", "NETHERR bait 82.82"),
        ("ash mist + stone ticks (V135-only)", "ash mist + stone ticks (V136-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD135 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v135_themes.json").read_text(encoding="utf-8"))["themes"])
NEW136 = "_".join(t[0] for t in T136)

out = (S / "c917_vision_v135_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C917", "C923"), ("c917", "c923"), ("V135", "V136"), ("v135", "v136"),
    ("_v135c917", "_v136c923"),
    ("Harder than V134", "Harder than V135"), ("harder than V134", "harder than V135"),
    (OLD135, NEW136),
    ("V135 keeps floor", "V136 keeps floor"),
    ("C917 design+fixtures; no VL claim", "C923 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C918 VL smoke", "fixtures only; claim deferred to C924 VL smoke"),
    ("No claim until C918 VL", "No claim until C924 VL"),
    ("kept on V135", "kept on V136"),
    ("vision_images_v135", "vision_images_v136"),
    ("VL_GATE_V135", "VL_GATE_V136"), ("vl_gate_v135", "vl_gate_v136"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V134: ashholt, cedarholt, dawnholt, elmholt, fernholt, glenholt, hazeholt, inkholt,\njadeholt, knotholt, lakeholt, mossholt, netherholt, oakholt, pineholt, quillholt, reedholt, stoneholt.",
    "NEW themes vs V135: ashridge, cedarridge, dawnridge, elmridge, fernridge, glenridge, hazeridge, inkridge,\njaderidge, knotridge, lakeridge, mossridge, netherridge, oakridge, pineridge, quillridge, reedridge, stoneridge.",
)
out = replace_specs(out, build_specs(T136, "v136", "V136", TR136))
out = retarget_136(out)
(S / "c923_vision_v136_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c918_vision_v135_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C918", "C924"), ("c918", "c924"), ("V135", "V136"), ("v135", "v136"),
    ("Uses C917 fixtures", "Uses C923 fixtures"),
    ("vision_images_v135", "vision_images_v136"),
    ("vl_gate_v135", "vl_gate_v136"), ("VL_GATE_V135", "VL_GATE_V136"),
]:
    out = out.replace(a, b)
(S / "c924_vision_v136_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c919_vision_v135_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C919", "C925"), ("c919", "c925"), ("C917", "C923"),
    ("V135", "V136"), ("v135", "v136"),
    ("_v135hc919", "_v136hc925"), ("_v135c917", "_v136c923"),
    ("vl_gate_v135", "vl_gate_v136"), ("VL_GATE_V135", "VL_GATE_V136"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T136, "v136h", "V136H", HO136))
out = retarget_136(out)
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v136h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v136"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v136" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v136h_c925"'); seen_run = True; continue
    out2.append(ln)
(S / "c925_vision_v136_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c914_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C914", "C926"), ("c914", "c926"),
    ("product_u2c_c914", "product_u2c_c926"),
    ("after V134", "after V136"), ("after V135", "after V136"),
]:
    out = out.replace(a, b)
(S / "c926_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c921_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C921", "C927"), ("c921", "c927"),
    ("capture_regression_c921", "capture_regression_c927"),
    ("after C917-C920", "after C923-C926"),
    ("V4-V135+heldout", "V4-V136+heldout"),
]:
    out = out.replace(a, b)
if "VISION_V136_SMOKE" not in out:
    out = out.replace(
        "SMOKE_POINTERS = [",
        'SMOKE_POINTERS = [\n    ("V136", DOC / "C924_VISION_V136_SMOKE.json"),\n    ("V136_heldout", DOC / "C925_VISION_V136_HELDOUT_SMOKE.json"),\n    ("V135", DOC / "C918_VISION_V135_SMOKE.json"),\n    ("V135_heldout", DOC / "C919_VISION_V135_HELDOUT_SMOKE.json"),',
        1,
    )
(S / "c927_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c922_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C922", "C928"), ("c922", "c928"),
    ("C918", "C924"), ("C919", "C925"), ("C921", "C927"),
    ("C917", "C923"),
    ("V135", "V136"), ("v135", "v136"),
    ("V134", "V135"), ("v134", "v135"),
    ("v135_jpeg_q", "v136_jpeg_q"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C920_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C920_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C914_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C926_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C914"}',
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C926"}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C920"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C920"}',
)
out = out.replace(
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C914"}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C926"}',
)
out = out.replace(
    "confidence-gate rate={conf_rate} pass={conf_pass}",
    "product-U2C replace={replace} pass={u2c_pass}",
)
out = out.replace(
    "stage_ready = bool(v136_claim and v136h_claim and v136 >= GATE and v136h >= GATE and capture_pass and disjoint and conf_pass)",
    "stage_ready = bool(v136_claim and v136h_claim and v136 >= GATE and v136h >= GATE and capture_pass and disjoint and u2c_pass)",
)
out = out.replace(
    'f"- C920: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C926: product-U2C replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- C920: confidence-gate rate={conf_rate} pass={conf_pass}"',
    'f"- C926: product-U2C replace={replace} pass={u2c_pass}"',
)
(S / "c928_scorecard_and_stage.py").write_text(out, encoding="utf-8")
for ln in out.splitlines():
    if any(x in ln for x in ("c656 =", "c650 =", '"confidence_gate"', '"product_u2c"', "stage_ready =", "product-U2C", "C926:", "C920:")):
        if "load" in ln or "source" in ln or "stage_ready" in ln or "product-U2C" in ln or "confidence" in ln:
            print("CHK", ln.strip()[:160])
print("scorecard OK"); print("done")
