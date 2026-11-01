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

# *brook — qty TR 780+820 HO 660+700; PO TR 820+740=1560 HO 710+590=1300; SLA 420+460 (OCR-safe)
T137 = [
    ["ashbrook","recv","paid_total","ASHBROOK GRAIN RECV","RECV","x"],
    ["cedarbrook","wh","qty_sum","WH CEDARBROOK BIN","RECV","x"],
    ["dawnbrook","refund","refund_done","DAWNBROOK PATCH REFUND","DONE","x"],
    ["elmbrook","tax","tax_base_paid","ELMBROOK TAX SLIP","TAX","x"],
    ["fernbrook","pay","payroll_active","FERNBROOK PAYROLL","PAY","x"],
    ["glenbrook","ship","ship_ok","GLENBROOK SHIP DOCK","SHIP","x"],
    ["hazebrook","sla","sla_ok_hours","HAZEBROOK SLA CARD","SLA","x"],
    ["inkbrook","exp","exp_sum","INKBROOK EXPENSE","EXP","x"],
    ["jadebrook","po","po_open","JADEBROOK PO SHEET","PO","x"],
    ["knotbrook","order","order_paid","KNOTBROOK ORDER","ORD","x"],
    ["lakebrook","dup","dup_mark","LAKEBROOK DUP MARK","DUP","x"],
    ["mossbrook","zero","zero_check","MOSSBROOK AIR ZERO","ZERO","x"],
    ["netherbrook","ledger","ledger_net","NETHERBROOK LEDGER","LED","x"],
    ["oakbrook","ui","ui_ok","OAKBROOK UI SCAN","UI","x"],
    ["pinebrook","stack","stack_count","PINEBROOK STACK","STK","x"],
    ["quillbrook","fax","fax_pages","QUILLBROOK FAX","FAX","x"],
    ["reedbrook","glare","glare_ok","REEDBROOK GLARE","GLR","x"],
    ["stonebrook","tab","tab_index","STONEBROOK TAB INDEX","TAB","x"],
]
TR137 = [
    [812.0, 829.5, 622.0],[780, 820, 610],[735.0, 764.25, 602.0],[868.0, 885.0, 692.0],
    [930.0, 954.0, 662.0],[688, 704, 620],[420.0, 460.0, 300.0],[778.0, 809.75, 626.0],
    [820.0, 740.0, 630.0],[845.0, 833.0, 623.0],[1,1,0],[0,0,0],  # po 820+740=1560
    [911.0, 932.5, 648.0],[1,0,0],[460, 452, 430],[478, 462, 453],[1,0,0],[504, 480, 450],
]
HO137 = [
    [682.0, 694.75, 575.0],[660, 700, 570],[640.0, 653.5, 563.0],[755.0, 771.0, 604.0],
    [796.0, 812.0, 599.0],[590, 604, 568],[320.0, 360.0, 260.0],[666.0, 687.75, 575.0],
    [710.0, 590.0, 572.0],[713.0, 699.0, 570.0],[1,1,0],[0,0,0],  # po 710+590=1300; qty 660+700=1360
    [748.0, 763.5, 585.0],[1,0,0],[436, 433, 428],[452, 446, 434],[1,0,0],[462, 456, 435],
]
(ROOT / "tools/_v137_themes.json").write_text(json.dumps({"themes": T137, "train": TR137, "heldout": HO137}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_137(src):
    src = src.replace("# --- V136 overlays (new vs V50) ---", "# --- V137 overlays (new vs V50) ---")
    src = src.replace("# --- V136 overlays (new vs V49) ---", "# --- V137 overlays (new vs V49) ---")
    for a, b in [
        ("ASHRIDGE bait 70.70", "ASHBROOK bait 71.71"),
        ("CEDARR bait 80.80", "CEDARB bait 81.81"),
        ("DAWNR ghost 94.94", "DAWNB ghost 95.95"),
        ("GLENR bait 75.75", "GLENB bait 76.76"),
        ("JADER bait 66.66", "JADEB bait 67.67"),
        ("NETHERR bait 82.82", "NETHERB bait 83.83"),
        ("ash mist + stone ticks (V136-only)", "ash mist + stone ticks (V137-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD136 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v136_themes.json").read_text(encoding="utf-8"))["themes"])
NEW137 = "_".join(t[0] for t in T137)

out = (S / "c923_vision_v136_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C923", "C929"), ("c923", "c929"), ("V136", "V137"), ("v136", "v137"),
    ("_v136c923", "_v137c929"),
    ("Harder than V135", "Harder than V136"), ("harder than V135", "harder than V136"),
    (OLD136, NEW137),
    ("V136 keeps floor", "V137 keeps floor"),
    ("C923 design+fixtures; no VL claim", "C929 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C924 VL smoke", "fixtures only; claim deferred to C930 VL smoke"),
    ("No claim until C924 VL", "No claim until C930 VL"),
    ("kept on V136", "kept on V137"),
    ("vision_images_v136", "vision_images_v137"),
    ("VL_GATE_V136", "VL_GATE_V137"), ("vl_gate_v136", "vl_gate_v137"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V135: ashridge, cedarridge, dawnridge, elmridge, fernridge, glenridge, hazeridge, inkridge,\njaderidge, knotridge, lakeridge, mossridge, netherridge, oakridge, pineridge, quillridge, reedridge, stoneridge.",
    "NEW themes vs V136: ashbrook, cedarbrook, dawnbrook, elmbrook, fernbrook, glenbrook, hazebrook, inkbrook,\njadebrook, knotbrook, lakebrook, mossbrook, netherbrook, oakbrook, pinebrook, quillbrook, reedbrook, stonebrook.",
)
out = replace_specs(out, build_specs(T137, "v137", "V137", TR137))
out = retarget_137(out)
(S / "c929_vision_v137_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c924_vision_v136_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C924", "C930"), ("c924", "c930"), ("V136", "V137"), ("v136", "v137"),
    ("Uses C923 fixtures", "Uses C929 fixtures"),
    ("vision_images_v136", "vision_images_v137"),
    ("vl_gate_v136", "vl_gate_v137"), ("VL_GATE_V136", "VL_GATE_V137"),
]:
    out = out.replace(a, b)
(S / "c930_vision_v137_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c925_vision_v136_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C925", "C931"), ("c925", "c931"), ("C923", "C929"),
    ("V136", "V137"), ("v136", "v137"),
    ("_v136hc925", "_v137hc931"), ("_v136c923", "_v137c929"),
    ("vl_gate_v136", "vl_gate_v137"), ("VL_GATE_V136", "VL_GATE_V137"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T137, "v137h", "V137H", HO137))
out = retarget_137(out)
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v137h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v137"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v137" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v137h_c931"'); seen_run = True; continue
    out2.append(ln)
(S / "c931_vision_v137_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c920_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C920", "C932"), ("c920", "c932"),
    ("conf_gate_stretch_c920", "conf_gate_stretch_c932"),
    ("after V135", "after V137"), ("after V136", "after V137"),
    ("cg69_", "cg70_"),
]:
    out = out.replace(a, b)
(S / "c932_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence")

out = (S / "c927_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C927", "C933"), ("c927", "c933"),
    ("capture_regression_c927", "capture_regression_c933"),
    ("after C923-C926", "after C929-C932"),
    ("V4-V136+heldout", "V4-V137+heldout"),
]:
    out = out.replace(a, b)
if "VISION_V137_SMOKE" not in out:
    out = out.replace(
        "SMOKE_POINTERS = [",
        'SMOKE_POINTERS = [\n    ("V137", DOC / "C930_VISION_V137_SMOKE.json"),\n    ("V137_heldout", DOC / "C931_VISION_V137_HELDOUT_SMOKE.json"),\n    ("V136", DOC / "C924_VISION_V136_SMOKE.json"),\n    ("V136_heldout", DOC / "C925_VISION_V136_HELDOUT_SMOKE.json"),',
        1,
    )
(S / "c933_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c928_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C928", "C934"), ("c928", "c934"),
    ("C924", "C930"), ("C925", "C931"), ("C927", "C933"),
    ("C923", "C929"),
    ("V136", "V137"), ("v136", "v137"),
    ("V135", "V136"), ("v135", "v136"),
    ("v136_jpeg_q", "v137_jpeg_q"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C920_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C932_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C926_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C926_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C926"}',
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C926"}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C920"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C932"}',
)
out = out.replace(
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C926"}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C926"}',
)
out = out.replace(
    "product-U2C replace={replace} pass={u2c_pass}",
    "confidence-gate rate={conf_rate} pass={conf_pass}",
)
out = out.replace(
    "stage_ready = bool(v137_claim and v137h_claim and v137 >= GATE and v137h >= GATE and capture_pass and disjoint and u2c_pass)",
    "stage_ready = bool(v137_claim and v137h_claim and v137 >= GATE and v137h >= GATE and capture_pass and disjoint and conf_pass)",
)
out = out.replace(
    'f"- C926: confidence-gate rate={conf_rate} pass={conf_pass}"',
    'f"- C932: confidence-gate rate={conf_rate} pass={conf_pass}"',
)
out = out.replace(
    'f"- C926: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C932: confidence-gate rate={conf_rate} pass={conf_pass}"',
)
(S / "c934_scorecard_and_stage.py").write_text(out, encoding="utf-8")
for ln in out.splitlines():
    if any(x in ln for x in ("c656 =", "c650 =", '"confidence_gate"', '"product_u2c"', "stage_ready =", "confidence-gate", "C932:", "C926:")):
        if "load" in ln or "source" in ln or "stage_ready" in ln or "confidence-gate" in ln or "product" in ln:
            print("CHK", ln.strip()[:160])
print("scorecard OK"); print("done")
