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

# *grove — qty TR 840+880 HO 720+760; PO TR 860+760=1620 HO 760+590=1350; SLA 450+490
T140 = [
    ["ashgrove","recv","paid_total","ASHGROVE GRAIN RECV","RECV","x"],
    ["cedargrove","wh","qty_sum","WH CEDARGROVE BIN","RECV","x"],
    ["dawngrove","refund","refund_done","DAWNGROVE PATCH REFUND","DONE","x"],
    ["elmgrove","tax","tax_base_paid","ELMGROVE TAX SLIP","TAX","x"],
    ["ferngrove","pay","payroll_active","FERNGROVE PAYROLL","PAY","x"],
    ["glengrove","ship","ship_ok","GLENGROVE SHIP DOCK","SHIP","x"],
    ["hazegrove","sla","sla_ok_hours","HAZEGROVE SLA CARD","SLA","x"],
    ["inkgrove","exp","exp_sum","INKGROVE EXPENSE","EXP","x"],
    ["jadegrove","po","po_open","JADEGROVE PO SHEET","PO","x"],
    ["knotgrove","order","order_paid","KNOTGROVE ORDER","ORD","x"],
    ["lakegrove","dup","dup_mark","LAKEGROVE DUP MARK","DUP","x"],
    ["mossgrove","zero","zero_check","MOSSGROVE AIR ZERO","ZERO","x"],
    ["nethergrove","ledger","ledger_net","NETHERGROVE LEDGER","LED","x"],
    ["oakgrove","ui","ui_ok","OAKGROVE UI SCAN","UI","x"],
    ["pinegrove","stack","stack_count","PINEGROVE STACK","STK","x"],
    ["quillgrove","fax","fax_pages","QUILLGROVE FAX","FAX","x"],
    ["reedgrove","glare","glare_ok","REEDGROVE GLARE","GLR","x"],
    ["stonegrove","tab","tab_index","STONEGROVE TAB INDEX","TAB","x"],
]
TR140 = [
    [842.0, 859.5, 652.0],[840, 880, 640],[765.0, 794.25, 632.0],[898.0, 915.0, 722.0],
    [960.0, 984.0, 692.0],[718, 734, 650],[450.0, 490.0, 330.0],[808.0, 839.75, 656.0],
    [860.0, 760.0, 660.0],[875.0, 863.0, 653.0],[1,1,0],[0,0,0],  # po 860+760=1620
    [941.0, 962.5, 678.0],[1,0,0],[490, 482, 460],[508, 492, 483],[1,0,0],[534, 510, 480],
]
HO140 = [
    [712.0, 724.75, 605.0],[720, 760, 600],[670.0, 683.5, 593.0],[785.0, 801.0, 634.0],
    [826.0, 842.0, 629.0],[620, 634, 598],[350.0, 390.0, 290.0],[696.0, 717.75, 605.0],
    [760.0, 590.0, 602.0],[743.0, 729.0, 600.0],[1,1,0],[0,0,0],  # po 760+590=1350; qty 720+760=1480
    [778.0, 793.5, 615.0],[1,0,0],[466, 463, 458],[482, 476, 464],[1,0,0],[492, 486, 465],
]
(ROOT / "tools/_v140_themes.json").write_text(json.dumps({"themes": T140, "train": TR140, "heldout": HO140}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_140(src):
    src = src.replace("# --- V139 overlays (new vs V50) ---", "# --- V140 overlays (new vs V50) ---")
    src = src.replace("# --- V139 overlays (new vs V49) ---", "# --- V140 overlays (new vs V49) ---")
    for a, b in [
        ("ASHFIELD bait 73.73", "ASHGROVE bait 74.74"),
        ("CEDARF bait 83.83", "CEDARG bait 84.84"),
        ("DAWNF ghost 97.97", "DAWNG ghost 98.98"),
        ("GLENF bait 78.78", "GLENG bait 79.79"),
        ("JADEF bait 69.69", "JADEG bait 60.60"),
        ("NETHERF bait 85.85", "NETHERG bait 86.86"),
        ("ash mist + stone ticks (V139-only)", "ash mist + stone ticks (V140-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD139 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v139_themes.json").read_text(encoding="utf-8"))["themes"])
NEW140 = "_".join(t[0] for t in T140)

out = (S / "c941_vision_v139_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C941", "C947"), ("c941", "c947"), ("V139", "V140"), ("v139", "v140"),
    ("_v139c941", "_v140c947"),
    ("Harder than V138", "Harder than V139"), ("harder than V138", "harder than V139"),
    (OLD139, NEW140),
    ("V139 keeps floor", "V140 keeps floor"),
    ("C941 design+fixtures; no VL claim", "C947 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C942 VL smoke", "fixtures only; claim deferred to C948 VL smoke"),
    ("No claim until C942 VL", "No claim until C948 VL"),
    ("kept on V139", "kept on V140"),
    ("vision_images_v139", "vision_images_v140"),
    ("VL_GATE_V139", "VL_GATE_V140"), ("vl_gate_v139", "vl_gate_v140"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V138: ashfield, cedarfield, dawnfield, elmfield, fernfield, glenfield, hazefield, inkfield,\njadefield, knotfield, lakefield, mossfield, netherfield, oakfield, pinefield, quillfield, reedfield, stonefield.",
    "NEW themes vs V139: ashgrove, cedargrove, dawngrove, elmgrove, ferngrove, glengrove, hazegrove, inkgrove,\njadegrove, knotgrove, lakegrove, mossgrove, nethergrove, oakgrove, pinegrove, quillgrove, reedgrove, stonegrove.",
)
out = replace_specs(out, build_specs(T140, "v140", "V140", TR140))
out = retarget_140(out)
(S / "c947_vision_v140_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c942_vision_v139_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C942", "C948"), ("c942", "c948"), ("V139", "V140"), ("v139", "v140"),
    ("Uses C941 fixtures", "Uses C947 fixtures"),
    ("vision_images_v139", "vision_images_v140"),
    ("vl_gate_v139", "vl_gate_v140"), ("VL_GATE_V139", "VL_GATE_V140"),
]:
    out = out.replace(a, b)
(S / "c948_vision_v140_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c943_vision_v139_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C943", "C949"), ("c943", "c949"), ("C941", "C947"),
    ("V139", "V140"), ("v139", "v140"),
    ("_v139hc943", "_v140hc949"), ("_v139c941", "_v140c947"),
    ("vl_gate_v139", "vl_gate_v140"), ("VL_GATE_V139", "VL_GATE_V140"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T140, "v140h", "V140H", HO140))
out = retarget_140(out)
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v140h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v140"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v140" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v140h_c949"'); seen_run = True; continue
    out2.append(ln)
(S / "c949_vision_v140_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c938_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C938", "C950"), ("c938", "c950"),
    ("product_u2c_c938", "product_u2c_c950"),
    ("after V138", "after V140"), ("after V139", "after V140"),
]:
    out = out.replace(a, b)
(S / "c950_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c945_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C945", "C951"), ("c945", "c951"),
    ("capture_regression_c945", "capture_regression_c951"),
    ("after C941-C944", "after C947-C950"),
    ("V4-V139+heldout", "V4-V140+heldout"),
]:
    out = out.replace(a, b)
if "VISION_V140_SMOKE" not in out:
    out = out.replace(
        "SMOKE_POINTERS = [",
        'SMOKE_POINTERS = [\n    ("V140", DOC / "C948_VISION_V140_SMOKE.json"),\n    ("V140_heldout", DOC / "C949_VISION_V140_HELDOUT_SMOKE.json"),\n    ("V139", DOC / "C942_VISION_V139_SMOKE.json"),\n    ("V139_heldout", DOC / "C943_VISION_V139_HELDOUT_SMOKE.json"),',
        1,
    )
(S / "c951_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c946_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C946", "C952"), ("c946", "c952"),
    ("C942", "C948"), ("C943", "C949"), ("C945", "C951"),
    ("C941", "C947"),
    ("V139", "V140"), ("v139", "v140"),
    ("V138", "V139"), ("v138", "v139"),
    ("v139_jpeg_q", "v140_jpeg_q"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C944_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C944_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C938_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C950_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C938"}',
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C950"}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C944"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C944"}',
)
out = out.replace(
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C938"}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C950"}',
)
out = out.replace(
    "confidence-gate rate={conf_rate} pass={conf_pass}",
    "product-U2C replace={replace} pass={u2c_pass}",
)
out = out.replace(
    "stage_ready = bool(v140_claim and v140h_claim and v140 >= GATE and v140h >= GATE and capture_pass and disjoint and conf_pass)",
    "stage_ready = bool(v140_claim and v140h_claim and v140 >= GATE and v140h >= GATE and capture_pass and disjoint and u2c_pass)",
)
out = out.replace(
    'f"- C944: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C950: product-U2C replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- C944: confidence-gate rate={conf_rate} pass={conf_pass}"',
    'f"- C950: product-U2C replace={replace} pass={u2c_pass}"',
)
(S / "c952_scorecard_and_stage.py").write_text(out, encoding="utf-8")
for ln in out.splitlines():
    if any(x in ln for x in ("c656 =", "c650 =", '"confidence_gate"', '"product_u2c"', "stage_ready =", "product-U2C", "C950:", "C944:")):
        if "load" in ln or "source" in ln or "stage_ready" in ln or "product-U2C" in ln or "confidence" in ln:
            print("CHK", ln.strip()[:160])
print("scorecard OK"); print("done")
