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

# *moor — qty TR 840+760 HO 740+780; PO TR 840+760 HO 780+740
T149 = [
    ["ashmoor","recv","paid_total","ASHMOOR GRAIN RECV","RECV","x"],
    ["cedarmoor","wh","qty_sum","WH CEDARMOOR BIN","RECV","x"],
    ["dawnmoor","refund","refund_done","DAWNMOOR PATCH REFUND","DONE","x"],
    ["elmmoor","tax","tax_base_paid","ELMMOOR TAX SLIP","TAX","x"],
    ["fernmoor","pay","payroll_active","FERNMOOR PAYROLL","PAY","x"],
    ["glenmoor","ship","ship_ok","GLENMOOR SHIP DOCK","SHIP","x"],
    ["hazemoor","sla","sla_ok_hours","HAZEMOOR SLA CARD","SLA","x"],
    ["inkmoor","exp","exp_sum","INKMOOR EXPENSE","EXP","x"],
    ["jademoor","po","po_open","JADEMOOR PO SHEET","PO","x"],
    ["knotmoor","order","order_paid","KNOTMOOR ORDER","ORD","x"],
    ["lakemoor","dup","dup_mark","LAKEMOOR DUP MARK","DUP","x"],
    ["mossmoor","zero","zero_check","MOSSMOOR AIR ZERO","ZERO","x"],
    ["nethermoor","ledger","ledger_net","NETHERMOOR LEDGER","LED","x"],
    ["oakmoor","ui","ui_ok","OAKMOOR UI SCAN","UI","x"],
    ["pinemoor","stack","stack_count","PINEMOOR STACK","STK","x"],
    ["quillmoor","fax","fax_pages","QUILLMOOR FAX","FAX","x"],
    ["reedmoor","glare","glare_ok","REEDMOOR GLARE","GLR","x"],
    ["stonemoor","tab","tab_index","STONEMOOR TAB INDEX","TAB","x"],
]
TR149 = [
    [932.0, 949.5, 742.0],[840, 760, 610],[855.0, 884.25, 722.0],[988.0, 1005.0, 812.0],
    [1050.0, 1074.0, 782.0],[808, 824, 740],[540.0, 580.0, 420.0],[898.0, 929.75, 746.0],
    [840.0, 760.0, 750.0],[965.0, 953.0, 743.0],[1,1,0],[0,0,0],
    [1031.0, 1052.5, 768.0],[1,0,0],[580, 572, 550],[598, 582, 573],[1,0,0],[624, 600, 570],
]
HO149 = [
    [802.0, 814.75, 695.0],[740, 780, 650],[760.0, 773.5, 683.0],[875.0, 891.0, 724.0],
    [916.0, 932.0, 719.0],[710, 724, 688],[440.0, 480.0, 380.0],[786.0, 807.75, 695.0],
    [780.0, 740.0, 692.0],[833.0, 819.0, 690.0],[1,1,0],[0,0,0],
    [868.0, 883.5, 705.0],[1,0,0],[556, 553, 548],[572, 566, 554],[1,0,0],[582, 576, 555],
]
(ROOT / "tools/_v149_themes.json").write_text(json.dumps({"themes": T149, "train": TR149, "heldout": HO149}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_149(src):
    src = src.replace("# --- V148 overlays (new vs V50) ---", "# --- V149 overlays (new vs V50) ---")
    src = src.replace("# --- V148 overlays (new vs V49) ---", "# --- V149 overlays (new vs V49) ---")
    for a, b in [
        ("ASHHURST bait 72.72", "ASHMOOR bait 73.73"),
        ("CEDARH bait 84.84", "CEDARM bait 85.85"),
        ("DAWNH ghost 96.96", "DAWNM ghost 97.97"),
        ("GLENH bait 77.77", "GLENM bait 78.78"),
        ("JADEH bait 68.68", "JADEM bait 69.69"),
        ("NETHERH bait 85.85", "NETHERM bait 86.86"),
        ("ash mist + stone ticks (V148-only)", "ash mist + stone ticks (V149-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD148 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v148_themes.json").read_text(encoding="utf-8"))["themes"])
NEW149 = "_".join(t[0] for t in T149)

out = (S / "c995_vision_v148_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C995", "C1001"), ("c995", "c1001"), ("V148", "V149"), ("v148", "v149"),
    ("_v148c995", "_v149c1001"),
    ("Harder than V147", "Harder than V148"), ("harder than V147", "harder than V148"),
    (OLD148, NEW149),
    ("V148 keeps floor", "V149 keeps floor"),
    ("C995 design+fixtures; no VL claim", "C1001 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C996 VL smoke", "fixtures only; claim deferred to C1002 VL smoke"),
    ("No claim until C996 VL", "No claim until C1002 VL"),
    ("kept on V148", "kept on V149"),
    ("vision_images_v148", "vision_images_v149"),
    ("VL_GATE_V148", "VL_GATE_V149"), ("vl_gate_v148", "vl_gate_v149"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V147: ashhurst, cedarhurst, dawnhurst, elmhurst, fernhurst, glenhurst, hazehurst, inkhurst,\njadehurst, knothurst, lakehurst, mosshurst, netherhurst, oakhurst, pinehurst, quillhurst, reedhurst, stonehurst.",
    "NEW themes vs V148: ashmoor, cedarmoor, dawnmoor, elmmoor, fernmoor, glenmoor, hazemoor, inkmoor,\njademoor, knotmoor, lakemoor, mossmoor, nethermoor, oakmoor, pinemoor, quillmoor, reedmoor, stonemoor.",
)
out = replace_specs(out, build_specs(T149, "v149", "V149", TR149))
out = retarget_149(out)
(S / "c1001_vision_v149_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c996_vision_v148_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C996", "C1002"), ("c996", "c1002"), ("V148", "V149"), ("v148", "v149"),
    ("vision_images_v148", "vision_images_v149"),
    ("VL_GATE_V148", "VL_GATE_V149"), ("vl_gate_v148", "vl_gate_v149"),
    ("runs/vision_v148", "runs/vision_v149"),
]:
    out = out.replace(a, b)
(S / "c1002_vision_v149_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c997_vision_v148_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C997", "C1003"), ("c997", "c1003"), ("V148", "V149"), ("v148", "v149"),
    ("vision_images_v148h", "vision_images_v149h"),
    ("vision_images_v148", "vision_images_v149"),
    ("VL_GATE_V148", "VL_GATE_V149"), ("vl_gate_v148", "vl_gate_v149"),
    ("runs/vision_v148h", "runs/vision_v149h"),
    ("_v148c995", "_v149c1001"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T149, "v149h", "V149H", HO149))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v149h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v149"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v149" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v149h_c1003"'); seen_run = True; continue
    out2.append(ln)
(S / "c1003_vision_v149_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c992_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C992", "C1004"), ("c992", "c1004"),
    ("conf_gate_stretch_c992", "conf_gate_stretch_c1004"),
    ("after V147", "after V149"), ("after V148", "after V149"),
    ("cg75_", "cg76_"),
]:
    out = out.replace(a, b)
(S / "c1004_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence")

out = (S / "c999_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C999", "C1005"), ("c999", "c1005"),
    ("capture_regression_c999", "capture_regression_c1005"),
    ("after C995-C998", "after C1001-C1004"),
    ("V4-V148+heldout", "V4-V149+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V148", DOC / "C996_VISION_V148_SMOKE.json"),'
if needle in out and "VISION_V149_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V149", DOC / "C1002_VISION_V149_SMOKE.json"),\n    ("V149_heldout", DOC / "C1003_VISION_V149_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1005_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1000_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1000", "C1006"), ("c1000", "c1006"),
    ("C996", "C1002"), ("C997", "C1003"), ("C999", "C1005"),
    ("C995", "C1001"), ("C998", "C1004"),
    ("V148", "V149"), ("v148", "v149"),
    ("V147", "V148"), ("v147", "v148"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c650 = load("docs/r50/C998_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C998_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'c656 = load("docs/r50/C992_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1004_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace('"source": "C998"', '"source": "C998"')
out = out.replace('"source": "C992"', '"source": "C1004"')
out = out.replace(
    'c656 = load("docs/r50/C998_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1004_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    "stage_ready = bool(v149_claim and v149h_claim and v149 >= GATE and v149h >= GATE and capture_pass and disjoint and u2c_pass)",
    "stage_ready = bool(v149_claim and v149h_claim and v149 >= GATE and v149h >= GATE and capture_pass and disjoint and conf_pass)",
)
out = out.replace(
    'f"- C1004: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C1004: confidence-gate pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- C998: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C1004: confidence-gate pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- confidence-gate (prior C992): pass={conf_pass} rate={conf_rate}"',
    'f"- product-U2C (prior C998): replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- confidence-gate (prior C1004): pass={conf_pass} rate={conf_rate}"',
    'f"- product-U2C (prior C998): replace={replace} pass={u2c_pass}"',
)
(S / "c1006_scorecard_and_stage.py").write_text(out, encoding="utf-8")
for ln in out.splitlines():
    if any(x in ln for x in ("c650 =", "c656 =", "stage_ready =", "C1004:", "source")):
        if "load" in ln or "stage_ready" in ln or "C1004" in ln or "source" in ln:
            print("CHK", ln.strip()[:180])
print("any_b", [t[0] for t in T149 if t[0].endswith("b")])
print("qty", TR149[1], HO149[1])
print("done")
