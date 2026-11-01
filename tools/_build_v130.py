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

# *ford — avoid *b / *wich / *moor; qty TR 700+720 HO 580+600; PO HO 652+578=1230; SLA 350+390
T130 = [
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
TR130 = [
    [742.0, 759.5, 552.0],[700, 720, 540],[665.0, 694.25, 532.0],[798.0, 815.0, 622.0],
    [860.0, 884.0, 592.0],[618, 634, 550],[350.0, 390.0, 230.0],[708.0, 739.75, 556.0],
    [742.0, 725.0, 565.0],[775.0, 763.0, 553.0],[1,1,0],[0,0,0],
    [841.0, 862.5, 578.0],[1,0,0],[390, 382, 360],[408, 392, 383],[1,0,0],[434, 410, 380],
]
HO130 = [
    [612.0, 624.75, 505.0],[580, 600, 500],[570.0, 583.5, 493.0],[685.0, 701.0, 534.0],
    [726.0, 742.0, 529.0],[520, 534, 498],[250.0, 290.0, 190.0],[596.0, 617.75, 505.0],
    [652.0, 578.0, 502.0],[643.0, 629.0, 500.0],[1,1,0],[0,0,0],  # po 652+578=1230; qty 580+600=1180
    [678.0, 693.5, 515.0],[1,0,0],[366, 363, 358],[382, 376, 364],[1,0,0],[392, 386, 365],
]
(ROOT / "tools/_v130_themes.json").write_text(json.dumps({"themes": T130, "train": TR130, "heldout": HO130}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_130(src):
    src = src.replace("# --- V129 overlays (new vs V50) ---", "# --- V130 overlays (new vs V50) ---")
    src = src.replace("# --- V129 overlays (new vs V49) ---", "# --- V130 overlays (new vs V49) ---")
    for a, b in [
        ("ASHWICH bait 73.73", "ASHFORD bait 74.74"),
        ("CEDARW bait 93.93", "CEDARF bait 94.94"),
        ("DAWNW ghost 96.96", "DAWNF ghost 97.97"),
        ("GLENW bait 68.68", "GLENF bait 69.69"),
        ("JADEW bait 59.59", "JADEF bait 60.60"),
        ("NETHERW bait 94.94", "NETHERF bait 95.95"),
        ("ash mist + stone ticks (V129-only)", "ash mist + stone ticks (V130-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD129 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v129_themes.json").read_text(encoding="utf-8"))["themes"])
NEW130 = "_".join(t[0] for t in T130)

out = (S / "c881_vision_v129_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C881", "C887"), ("c881", "c887"), ("V129", "V130"), ("v129", "v130"),
    ("_v129c881", "_v130c887"),
    ("Harder than V128", "Harder than V129"), ("harder than V128", "harder than V129"),
    (OLD129, NEW130),
    ("V129 keeps floor", "V130 keeps floor"),
    ("C881 design+fixtures; no VL claim", "C887 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C882 VL smoke", "fixtures only; claim deferred to C888 VL smoke"),
    ("No claim until C882 VL", "No claim until C888 VL"),
    ("kept on V129", "kept on V130"),
    ("vision_images_v129", "vision_images_v130"),
    ("VL_GATE_V129", "VL_GATE_V130"), ("vl_gate_v129", "vl_gate_v130"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V128: ashwich, cedarwich, dawnwich, elmwich, fernwich, glenwich, hazewich, inkwich,\njadewich, knotwich, lakewich, mosswich, netherwich, oakwich, pinewich, quillwich, reedwich, stonewich.",
    "NEW themes vs V129: ashford, cedarford, dawnford, elmford, fernford, glenford, hazeford, inkford,\njadeford, knotford, lakeford, mossford, netherford, oakford, pineford, quillford, reedford, stoneford.",
)
out = replace_specs(out, build_specs(T130, "v130", "V130", TR130))
out = retarget_130(out)
(S / "c887_vision_v130_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c882_vision_v129_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C882", "C888"), ("c882", "c888"), ("V129", "V130"), ("v129", "v130"),
    ("Uses C881 fixtures", "Uses C887 fixtures"),
    ("vision_images_v129", "vision_images_v130"),
    ("vl_gate_v129", "vl_gate_v130"), ("VL_GATE_V129", "VL_GATE_V130"),
]:
    out = out.replace(a, b)
(S / "c888_vision_v130_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c883_vision_v129_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C883", "C889"), ("c883", "c889"), ("C881", "C887"),
    ("V129", "V130"), ("v129", "v130"),
    ("_v129hc883", "_v130hc889"), ("_v129c881", "_v130c887"),
    ("vl_gate_v129", "vl_gate_v130"), ("VL_GATE_V129", "VL_GATE_V130"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T130, "v130h", "V130H", HO130))
out = retarget_130(out)
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v130h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v130"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v130" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v130h_c889"'); seen_run = True; continue
    out2.append(ln)
(S / "c889_vision_v130_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c878_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C878", "C890"), ("c878", "c890"),
    ("product_u2c_c878", "product_u2c_c890"),
    ("after V128", "after V130"), ("after V129", "after V130"),
]:
    out = out.replace(a, b)
(S / "c890_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c885_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C885", "C891"), ("c885", "c891"),
    ("capture_regression_c885", "capture_regression_c891"),
    ("after C881-C884", "after C887-C890"),
    ("V4-V129+heldout", "V4-V130+heldout"),
]:
    out = out.replace(a, b)
if "VISION_V130_SMOKE" not in out:
    out = out.replace(
        "SMOKE_POINTERS = [",
        'SMOKE_POINTERS = [\n    ("V130", DOC / "C888_VISION_V130_SMOKE.json"),\n    ("V130_heldout", DOC / "C889_VISION_V130_HELDOUT_SMOKE.json"),\n    ("V129", DOC / "C882_VISION_V129_SMOKE.json"),\n    ("V129_heldout", DOC / "C883_VISION_V129_HELDOUT_SMOKE.json"),',
        1,
    )
(S / "c891_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c886_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C886", "C892"), ("c886", "c892"),
    ("C882", "C888"), ("C883", "C889"), ("C885", "C891"),
    ("C881", "C887"),
    ("V129", "V130"), ("v129", "v130"),
    ("V128", "V129"), ("v128", "v129"),
    ("v129_jpeg_q", "v130_jpeg_q"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C884_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C884_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C878_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C890_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C878"}',
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C890"}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C884"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C884"}',
)
out = out.replace(
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C878"}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C890"}',
)
out = out.replace(
    "confidence-gate rate={conf_rate} pass={conf_pass}",
    "product-U2C replace={replace} pass={u2c_pass}",
)
out = out.replace(
    "stage_ready = bool(v130_claim and v130h_claim and v130 >= GATE and v130h >= GATE and capture_pass and disjoint and conf_pass)",
    "stage_ready = bool(v130_claim and v130h_claim and v130 >= GATE and v130h >= GATE and capture_pass and disjoint and u2c_pass)",
)
out = out.replace(
    'f"- C884: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C890: product-U2C replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- C884: confidence-gate rate={conf_rate} pass={conf_pass}"',
    'f"- C890: product-U2C replace={replace} pass={u2c_pass}"',
)
(S / "c892_scorecard_and_stage.py").write_text(out, encoding="utf-8")
for ln in out.splitlines():
    if any(x in ln for x in ("c656 =", "c650 =", '"confidence_gate"', '"product_u2c"', "stage_ready =", "product-U2C", "C890:", "C884:")):
        if "load" in ln or "source" in ln or "stage_ready" in ln or "product-U2C" in ln or "confidence" in ln:
            print("CHK", ln.strip()[:160])
print("scorecard OK"); print("done")
