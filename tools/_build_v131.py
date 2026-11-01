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

# *mere — avoid *b/*ford/*wich/*moor; qty TR 710+730 HO 590+610; PO HO 659+581=1240; SLA 360+400
T131 = [
    ["ashmere","recv","paid_total","ASHMERE GRAIN RECV","RECV","x"],
    ["cedarmere","wh","qty_sum","WH CEDARMERE BIN","RECV","x"],
    ["dawnmere","refund","refund_done","DAWNMERE PATCH REFUND","DONE","x"],
    ["elmmere","tax","tax_base_paid","ELMMERE TAX SLIP","TAX","x"],
    ["fernmere","pay","payroll_active","FERNMERE PAYROLL","PAY","x"],
    ["glenmere","ship","ship_ok","GLENMERE SHIP DOCK","SHIP","x"],
    ["hazemere","sla","sla_ok_hours","HAZEMERE SLA CARD","SLA","x"],
    ["inkmere","exp","exp_sum","INKMERE EXPENSE","EXP","x"],
    ["jademere","po","po_open","JADEMERE PO SHEET","PO","x"],
    ["knotmere","order","order_paid","KNOTMERE ORDER","ORD","x"],
    ["lakemere","dup","dup_mark","LAKEMERE DUP MARK","DUP","x"],
    ["mossmere","zero","zero_check","MOSSMERE AIR ZERO","ZERO","x"],
    ["nethermere","ledger","ledger_net","NETHERMERE LEDGER","LED","x"],
    ["oakmere","ui","ui_ok","OAKMERE UI SCAN","UI","x"],
    ["pinemere","stack","stack_count","PINEMERE STACK","STK","x"],
    ["quillmere","fax","fax_pages","QUILLMERE FAX","FAX","x"],
    ["reedmere","glare","glare_ok","REEDMERE GLARE","GLR","x"],
    ["stonemere","tab","tab_index","STONEMERE TAB INDEX","TAB","x"],
]
TR131 = [
    [752.0, 769.5, 562.0],[710, 730, 550],[675.0, 704.25, 542.0],[808.0, 825.0, 632.0],
    [870.0, 894.0, 602.0],[628, 644, 560],[360.0, 400.0, 240.0],[718.0, 749.75, 566.0],
    [752.0, 735.0, 575.0],[785.0, 773.0, 563.0],[1,1,0],[0,0,0],
    [851.0, 872.5, 588.0],[1,0,0],[400, 392, 370],[418, 402, 393],[1,0,0],[444, 420, 390],
]
HO131 = [
    [622.0, 634.75, 515.0],[590, 610, 510],[580.0, 593.5, 503.0],[695.0, 711.0, 544.0],
    [736.0, 752.0, 539.0],[530, 544, 508],[260.0, 300.0, 200.0],[606.0, 627.75, 515.0],
    [659.0, 581.0, 512.0],[653.0, 639.0, 510.0],[1,1,0],[0,0,0],  # po 659+581=1240; qty 590+610=1200
    [688.0, 703.5, 525.0],[1,0,0],[376, 373, 368],[392, 386, 374],[1,0,0],[402, 396, 375],
]
(ROOT / "tools/_v131_themes.json").write_text(json.dumps({"themes": T131, "train": TR131, "heldout": HO131}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_131(src):
    src = src.replace("# --- V130 overlays (new vs V50) ---", "# --- V131 overlays (new vs V50) ---")
    src = src.replace("# --- V130 overlays (new vs V49) ---", "# --- V131 overlays (new vs V49) ---")
    for a, b in [
        ("ASHFORD bait 74.74", "ASHMERE bait 75.75"),
        ("CEDARF bait 94.94", "CEDARM bait 95.95"),
        ("DAWNF ghost 97.97", "DAWNM ghost 98.98"),
        ("GLENF bait 69.69", "GLENM bait 70.70"),
        ("JADEF bait 60.60", "JADEM bait 61.61"),
        ("NETHERF bait 95.95", "NETHERM bait 96.96"),
        ("ash mist + stone ticks (V130-only)", "ash mist + stone ticks (V131-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD130 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v130_themes.json").read_text(encoding="utf-8"))["themes"])
NEW131 = "_".join(t[0] for t in T131)

out = (S / "c887_vision_v130_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C887", "C893"), ("c887", "c893"), ("V130", "V131"), ("v130", "v131"),
    ("_v130c887", "_v131c893"),
    ("Harder than V129", "Harder than V130"), ("harder than V129", "harder than V130"),
    (OLD130, NEW131),
    ("V130 keeps floor", "V131 keeps floor"),
    ("C887 design+fixtures; no VL claim", "C893 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C888 VL smoke", "fixtures only; claim deferred to C894 VL smoke"),
    ("No claim until C888 VL", "No claim until C894 VL"),
    ("kept on V130", "kept on V131"),
    ("vision_images_v130", "vision_images_v131"),
    ("VL_GATE_V130", "VL_GATE_V131"), ("vl_gate_v130", "vl_gate_v131"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V129: ashford, cedarford, dawnford, elmford, fernford, glenford, hazeford, inkford,\njadeford, knotford, lakeford, mossford, netherford, oakford, pineford, quillford, reedford, stoneford.",
    "NEW themes vs V130: ashmere, cedarmere, dawnmere, elmmere, fernmere, glenmere, hazemere, inkmere,\njademere, knotmere, lakemere, mossmere, nethermere, oakmere, pinemere, quillmere, reedmere, stonemere.",
)
out = replace_specs(out, build_specs(T131, "v131", "V131", TR131))
out = retarget_131(out)
(S / "c893_vision_v131_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c888_vision_v130_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C888", "C894"), ("c888", "c894"), ("V130", "V131"), ("v130", "v131"),
    ("Uses C887 fixtures", "Uses C893 fixtures"),
    ("vision_images_v130", "vision_images_v131"),
    ("vl_gate_v130", "vl_gate_v131"), ("VL_GATE_V130", "VL_GATE_V131"),
]:
    out = out.replace(a, b)
(S / "c894_vision_v131_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c889_vision_v130_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C889", "C895"), ("c889", "c895"), ("C887", "C893"),
    ("V130", "V131"), ("v130", "v131"),
    ("_v130hc889", "_v131hc895"), ("_v130c887", "_v131c893"),
    ("vl_gate_v130", "vl_gate_v131"), ("VL_GATE_V130", "VL_GATE_V131"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T131, "v131h", "V131H", HO131))
out = retarget_131(out)
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v131h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v131"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v131" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v131h_c895"'); seen_run = True; continue
    out2.append(ln)
(S / "c895_vision_v131_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c884_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C884", "C896"), ("c884", "c896"),
    ("conf_gate_stretch_c884", "conf_gate_stretch_c896"),
    ("after V129", "after V131"), ("after V130", "after V131"),
    ("cg66_", "cg67_"),
]:
    out = out.replace(a, b)
(S / "c896_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence")

out = (S / "c891_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C891", "C897"), ("c891", "c897"),
    ("capture_regression_c891", "capture_regression_c897"),
    ("after C887-C890", "after C893-C896"),
    ("V4-V130+heldout", "V4-V131+heldout"),
]:
    out = out.replace(a, b)
if "VISION_V131_SMOKE" not in out:
    out = out.replace(
        "SMOKE_POINTERS = [",
        'SMOKE_POINTERS = [\n    ("V131", DOC / "C894_VISION_V131_SMOKE.json"),\n    ("V131_heldout", DOC / "C895_VISION_V131_HELDOUT_SMOKE.json"),\n    ("V130", DOC / "C888_VISION_V130_SMOKE.json"),\n    ("V130_heldout", DOC / "C889_VISION_V130_HELDOUT_SMOKE.json"),',
        1,
    )
(S / "c897_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c892_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C892", "C898"), ("c892", "c898"),
    ("C888", "C894"), ("C889", "C895"), ("C891", "C897"),
    ("C887", "C893"),
    ("V130", "V131"), ("v130", "v131"),
    ("V129", "V130"), ("v129", "v130"),
    ("v130_jpeg_q", "v131_jpeg_q"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C884_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C896_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C890_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C890_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C890"}',
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C890"}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C884"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C896"}',
)
out = out.replace(
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C890"}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C890"}',
)
out = out.replace(
    "product-U2C replace={replace} pass={u2c_pass}",
    "confidence-gate rate={conf_rate} pass={conf_pass}",
)
out = out.replace(
    "stage_ready = bool(v131_claim and v131h_claim and v131 >= GATE and v131h >= GATE and capture_pass and disjoint and u2c_pass)",
    "stage_ready = bool(v131_claim and v131h_claim and v131 >= GATE and v131h >= GATE and capture_pass and disjoint and conf_pass)",
)
out = out.replace(
    'f"- C890: confidence-gate rate={conf_rate} pass={conf_pass}"',
    'f"- C896: confidence-gate rate={conf_rate} pass={conf_pass}"',
)
out = out.replace(
    'f"- C890: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C896: confidence-gate rate={conf_rate} pass={conf_pass}"',
)
(S / "c898_scorecard_and_stage.py").write_text(out, encoding="utf-8")
for ln in out.splitlines():
    if any(x in ln for x in ("c656 =", "c650 =", '"confidence_gate"', '"product_u2c"', "stage_ready =", "confidence-gate", "C896:", "C890:")):
        if "load" in ln or "source" in ln or "stage_ready" in ln or "confidence-gate" in ln or "product" in ln:
            print("CHK", ln.strip()[:160])
print("scorecard OK"); print("done")
