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

# *crest — qty TR 800+840 HO 680+720; PO TR 830+740=1570 HO 720+590=1310; SLA 430+470
T138 = [
    ["ashcrest","recv","paid_total","ASHCREST GRAIN RECV","RECV","x"],
    ["cedarcrest","wh","qty_sum","WH CEDARCREST BIN","RECV","x"],
    ["dawncrest","refund","refund_done","DAWNCREST PATCH REFUND","DONE","x"],
    ["elmcrest","tax","tax_base_paid","ELMCREST TAX SLIP","TAX","x"],
    ["ferncrest","pay","payroll_active","FERNCREST PAYROLL","PAY","x"],
    ["glencrest","ship","ship_ok","GLENCREST SHIP DOCK","SHIP","x"],
    ["hazecrest","sla","sla_ok_hours","HAZECREST SLA CARD","SLA","x"],
    ["inkcrest","exp","exp_sum","INKCREST EXPENSE","EXP","x"],
    ["jadecrest","po","po_open","JADECREST PO SHEET","PO","x"],
    ["knotcrest","order","order_paid","KNOTCREST ORDER","ORD","x"],
    ["lakecrest","dup","dup_mark","LAKECREST DUP MARK","DUP","x"],
    ["mosscrest","zero","zero_check","MOSSCREST AIR ZERO","ZERO","x"],
    ["nethercrest","ledger","ledger_net","NETHERCREST LEDGER","LED","x"],
    ["oakcrest","ui","ui_ok","OAKCREST UI SCAN","UI","x"],
    ["pinecrest","stack","stack_count","PINECREST STACK","STK","x"],
    ["quillcrest","fax","fax_pages","QUILLCREST FAX","FAX","x"],
    ["reedcrest","glare","glare_ok","REEDCREST GLARE","GLR","x"],
    ["stonecrest","tab","tab_index","STONECREST TAB INDEX","TAB","x"],
]
TR138 = [
    [822.0, 839.5, 632.0],[800, 840, 620],[745.0, 774.25, 612.0],[878.0, 895.0, 702.0],
    [940.0, 964.0, 672.0],[698, 714, 630],[430.0, 470.0, 310.0],[788.0, 819.75, 636.0],
    [840.0, 760.0, 640.0],[855.0, 843.0, 633.0],[1,1,0],[0,0,0],  # po 830+740=1570
    [921.0, 942.5, 658.0],[1,0,0],[470, 462, 440],[488, 472, 463],[1,0,0],[514, 490, 460],
]
HO138 = [
    [692.0, 704.75, 585.0],[680, 720, 580],[650.0, 663.5, 573.0],[765.0, 781.0, 614.0],
    [806.0, 822.0, 609.0],[600, 614, 578],[330.0, 370.0, 270.0],[676.0, 697.75, 585.0],
    [720.0, 590.0, 582.0],[723.0, 709.0, 580.0],[1,1,0],[0,0,0],  # po 720+590=1310; qty 680+720=1400
    [758.0, 773.5, 595.0],[1,0,0],[446, 443, 438],[462, 456, 444],[1,0,0],[472, 466, 445],
]
(ROOT / "tools/_v138_themes.json").write_text(json.dumps({"themes": T138, "train": TR138, "heldout": HO138}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_138(src):
    src = src.replace("# --- V137 overlays (new vs V50) ---", "# --- V138 overlays (new vs V50) ---")
    src = src.replace("# --- V137 overlays (new vs V49) ---", "# --- V138 overlays (new vs V49) ---")
    for a, b in [
        ("ASHBROOK bait 71.71", "ASHCREST bait 72.72"),
        ("CEDARB bait 81.81", "CEDARC bait 82.82"),
        ("DAWNB ghost 95.95", "DAWNC ghost 96.96"),
        ("GLENB bait 76.76", "GLENC bait 77.77"),
        ("JADEB bait 67.67", "JADEC bait 68.68"),
        ("NETHERB bait 83.83", "NETHERC bait 84.84"),
        ("ash mist + stone ticks (V137-only)", "ash mist + stone ticks (V138-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD137 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v137_themes.json").read_text(encoding="utf-8"))["themes"])
NEW138 = "_".join(t[0] for t in T138)

out = (S / "c929_vision_v137_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C929", "C935"), ("c929", "c935"), ("V137", "V138"), ("v137", "v138"),
    ("_v137c929", "_v138c935"),
    ("Harder than V136", "Harder than V137"), ("harder than V136", "harder than V137"),
    (OLD137, NEW138),
    ("V137 keeps floor", "V138 keeps floor"),
    ("C929 design+fixtures; no VL claim", "C935 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C930 VL smoke", "fixtures only; claim deferred to C936 VL smoke"),
    ("No claim until C930 VL", "No claim until C936 VL"),
    ("kept on V137", "kept on V138"),
    ("vision_images_v137", "vision_images_v138"),
    ("VL_GATE_V137", "VL_GATE_V138"), ("vl_gate_v137", "vl_gate_v138"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V136: ashbrook, cedarbrook, dawnbrook, elmbrook, fernbrook, glenbrook, hazebrook, inkbrook,\njadebrook, knotbrook, lakebrook, mossbrook, netherbrook, oakbrook, pinebrook, quillbrook, reedbrook, stonebrook.",
    "NEW themes vs V137: ashcrest, cedarcrest, dawncrest, elmcrest, ferncrest, glencrest, hazecrest, inkcrest,\njadecrest, knotcrest, lakecrest, mosscrest, nethercrest, oakcrest, pinecrest, quillcrest, reedcrest, stonecrest.",
)
out = replace_specs(out, build_specs(T138, "v138", "V138", TR138))
out = retarget_138(out)
(S / "c935_vision_v138_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c930_vision_v137_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C930", "C936"), ("c930", "c936"), ("V137", "V138"), ("v137", "v138"),
    ("Uses C929 fixtures", "Uses C935 fixtures"),
    ("vision_images_v137", "vision_images_v138"),
    ("vl_gate_v137", "vl_gate_v138"), ("VL_GATE_V137", "VL_GATE_V138"),
]:
    out = out.replace(a, b)
(S / "c936_vision_v138_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c931_vision_v137_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C931", "C937"), ("c931", "c937"), ("C929", "C935"),
    ("V137", "V138"), ("v137", "v138"),
    ("_v137hc931", "_v138hc937"), ("_v137c929", "_v138c935"),
    ("vl_gate_v137", "vl_gate_v138"), ("VL_GATE_V137", "VL_GATE_V138"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T138, "v138h", "V138H", HO138))
out = retarget_138(out)
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v138h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v138"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v138" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v138h_c937"'); seen_run = True; continue
    out2.append(ln)
(S / "c937_vision_v138_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c926_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C926", "C938"), ("c926", "c938"),
    ("product_u2c_c926", "product_u2c_c938"),
    ("after V136", "after V138"), ("after V137", "after V138"),
]:
    out = out.replace(a, b)
(S / "c938_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c933_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C933", "C939"), ("c933", "c939"),
    ("capture_regression_c933", "capture_regression_c939"),
    ("after C929-C932", "after C935-C938"),
    ("V4-V137+heldout", "V4-V138+heldout"),
]:
    out = out.replace(a, b)
if "VISION_V138_SMOKE" not in out:
    out = out.replace(
        "SMOKE_POINTERS = [",
        'SMOKE_POINTERS = [\n    ("V138", DOC / "C936_VISION_V138_SMOKE.json"),\n    ("V138_heldout", DOC / "C937_VISION_V138_HELDOUT_SMOKE.json"),\n    ("V137", DOC / "C930_VISION_V137_SMOKE.json"),\n    ("V137_heldout", DOC / "C931_VISION_V137_HELDOUT_SMOKE.json"),',
        1,
    )
(S / "c939_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c934_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C934", "C940"), ("c934", "c940"),
    ("C930", "C936"), ("C931", "C937"), ("C933", "C939"),
    ("C929", "C935"),
    ("V137", "V138"), ("v137", "v138"),
    ("V136", "V137"), ("v136", "v137"),
    ("v137_jpeg_q", "v138_jpeg_q"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C932_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C932_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C926_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C938_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C926"}',
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C938"}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C932"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C932"}',
)
out = out.replace(
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C926"}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C938"}',
)
out = out.replace(
    "confidence-gate rate={conf_rate} pass={conf_pass}",
    "product-U2C replace={replace} pass={u2c_pass}",
)
out = out.replace(
    "stage_ready = bool(v138_claim and v138h_claim and v138 >= GATE and v138h >= GATE and capture_pass and disjoint and conf_pass)",
    "stage_ready = bool(v138_claim and v138h_claim and v138 >= GATE and v138h >= GATE and capture_pass and disjoint and u2c_pass)",
)
out = out.replace(
    'f"- C932: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C938: product-U2C replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- C932: confidence-gate rate={conf_rate} pass={conf_pass}"',
    'f"- C938: product-U2C replace={replace} pass={u2c_pass}"',
)
(S / "c940_scorecard_and_stage.py").write_text(out, encoding="utf-8")
for ln in out.splitlines():
    if any(x in ln for x in ("c656 =", "c650 =", '"confidence_gate"', '"product_u2c"', "stage_ready =", "product-U2C", "C938:", "C932:")):
        if "load" in ln or "source" in ln or "stage_ready" in ln or "product-U2C" in ln or "confidence" in ln:
            print("CHK", ln.strip()[:160])
print("scorecard OK"); print("done")
