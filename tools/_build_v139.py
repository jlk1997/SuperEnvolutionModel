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

# *field — qty TR 820+860 HO 700+740; PO TR 850+760=1610 HO 740+590=1330; SLA 440+480 (OCR-safe)
T139 = [
    ["ashfield","recv","paid_total","ASHFIELD GRAIN RECV","RECV","x"],
    ["cedarfield","wh","qty_sum","WH CEDARFIELD BIN","RECV","x"],
    ["dawnfield","refund","refund_done","DAWNFIELD PATCH REFUND","DONE","x"],
    ["elmfield","tax","tax_base_paid","ELMFIELD TAX SLIP","TAX","x"],
    ["fernfield","pay","payroll_active","FERNFIELD PAYROLL","PAY","x"],
    ["glenfield","ship","ship_ok","GLENFIELD SHIP DOCK","SHIP","x"],
    ["hazefield","sla","sla_ok_hours","HAZEFIELD SLA CARD","SLA","x"],
    ["inkfield","exp","exp_sum","INKFIELD EXPENSE","EXP","x"],
    ["jadefield","po","po_open","JADEFIELD PO SHEET","PO","x"],
    ["knotfield","order","order_paid","KNOTFIELD ORDER","ORD","x"],
    ["lakefield","dup","dup_mark","LAKEFIELD DUP MARK","DUP","x"],
    ["mossfield","zero","zero_check","MOSSFIELD AIR ZERO","ZERO","x"],
    ["netherfield","ledger","ledger_net","NETHERFIELD LEDGER","LED","x"],
    ["oakfield","ui","ui_ok","OAKFIELD UI SCAN","UI","x"],
    ["pinefield","stack","stack_count","PINEFIELD STACK","STK","x"],
    ["quillfield","fax","fax_pages","QUILLFIELD FAX","FAX","x"],
    ["reedfield","glare","glare_ok","REEDFIELD GLARE","GLR","x"],
    ["stonefield","tab","tab_index","STONEFIELD TAB INDEX","TAB","x"],
]
TR139 = [
    [832.0, 849.5, 642.0],[820, 860, 630],[755.0, 784.25, 622.0],[888.0, 905.0, 712.0],
    [950.0, 974.0, 682.0],[708, 724, 640],[440.0, 480.0, 320.0],[798.0, 829.75, 646.0],
    [850.0, 760.0, 650.0],[865.0, 853.0, 643.0],[1,1,0],[0,0,0],  # po 850+760=1610
    [931.0, 952.5, 668.0],[1,0,0],[480, 472, 450],[498, 482, 473],[1,0,0],[524, 500, 470],
]
HO139 = [
    [702.0, 714.75, 595.0],[700, 740, 590],[660.0, 673.5, 583.0],[775.0, 791.0, 624.0],
    [816.0, 832.0, 619.0],[610, 624, 588],[340.0, 380.0, 280.0],[686.0, 707.75, 595.0],
    [740.0, 590.0, 592.0],[733.0, 719.0, 590.0],[1,1,0],[0,0,0],  # po 740+590=1330; qty 700+740=1440
    [768.0, 783.5, 605.0],[1,0,0],[456, 453, 448],[472, 466, 454],[1,0,0],[482, 476, 455],
]
(ROOT / "tools/_v139_themes.json").write_text(json.dumps({"themes": T139, "train": TR139, "heldout": HO139}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_139(src):
    src = src.replace("# --- V138 overlays (new vs V50) ---", "# --- V139 overlays (new vs V50) ---")
    src = src.replace("# --- V138 overlays (new vs V49) ---", "# --- V139 overlays (new vs V49) ---")
    for a, b in [
        ("ASHCREST bait 72.72", "ASHFIELD bait 73.73"),
        ("CEDARC bait 82.82", "CEDARF bait 83.83"),
        ("DAWNC ghost 96.96", "DAWNF ghost 97.97"),
        ("GLENC bait 77.77", "GLENF bait 78.78"),
        ("JADEC bait 68.68", "JADEF bait 69.69"),
        ("NETHERC bait 84.84", "NETHERF bait 85.85"),
        ("ash mist + stone ticks (V138-only)", "ash mist + stone ticks (V139-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD138 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v138_themes.json").read_text(encoding="utf-8"))["themes"])
NEW139 = "_".join(t[0] for t in T139)

out = (S / "c935_vision_v138_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C935", "C941"), ("c935", "c941"), ("V138", "V139"), ("v138", "v139"),
    ("_v138c935", "_v139c941"),
    ("Harder than V137", "Harder than V138"), ("harder than V137", "harder than V138"),
    (OLD138, NEW139),
    ("V138 keeps floor", "V139 keeps floor"),
    ("C935 design+fixtures; no VL claim", "C941 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C936 VL smoke", "fixtures only; claim deferred to C942 VL smoke"),
    ("No claim until C936 VL", "No claim until C942 VL"),
    ("kept on V138", "kept on V139"),
    ("vision_images_v138", "vision_images_v139"),
    ("VL_GATE_V138", "VL_GATE_V139"), ("vl_gate_v138", "vl_gate_v139"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V137: ashcrest, cedarcrest, dawncrest, elmcrest, ferncrest, glencrest, hazecrest, inkcrest,\njadecrest, knotcrest, lakecrest, mosscrest, nethercrest, oakcrest, pinecrest, quillcrest, reedcrest, stonecrest.",
    "NEW themes vs V138: ashfield, cedarfield, dawnfield, elmfield, fernfield, glenfield, hazefield, inkfield,\njadefield, knotfield, lakefield, mossfield, netherfield, oakfield, pinefield, quillfield, reedfield, stonefield.",
)
out = replace_specs(out, build_specs(T139, "v139", "V139", TR139))
out = retarget_139(out)
(S / "c941_vision_v139_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c936_vision_v138_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C936", "C942"), ("c936", "c942"), ("V138", "V139"), ("v138", "v139"),
    ("Uses C935 fixtures", "Uses C941 fixtures"),
    ("vision_images_v138", "vision_images_v139"),
    ("vl_gate_v138", "vl_gate_v139"), ("VL_GATE_V138", "VL_GATE_V139"),
]:
    out = out.replace(a, b)
(S / "c942_vision_v139_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c937_vision_v138_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C937", "C943"), ("c937", "c943"), ("C935", "C941"),
    ("V138", "V139"), ("v138", "v139"),
    ("_v138hc937", "_v139hc943"), ("_v138c935", "_v139c941"),
    ("vl_gate_v138", "vl_gate_v139"), ("VL_GATE_V138", "VL_GATE_V139"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T139, "v139h", "V139H", HO139))
out = retarget_139(out)
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v139h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v139"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v139" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v139h_c943"'); seen_run = True; continue
    out2.append(ln)
(S / "c943_vision_v139_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c932_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C932", "C944"), ("c932", "c944"),
    ("conf_gate_stretch_c932", "conf_gate_stretch_c944"),
    ("after V137", "after V139"), ("after V138", "after V139"),
    ("cg70_", "cg71_"),
]:
    out = out.replace(a, b)
(S / "c944_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence")

out = (S / "c939_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C939", "C945"), ("c939", "c945"),
    ("capture_regression_c939", "capture_regression_c945"),
    ("after C935-C938", "after C941-C944"),
    ("V4-V138+heldout", "V4-V139+heldout"),
]:
    out = out.replace(a, b)
if "VISION_V139_SMOKE" not in out:
    out = out.replace(
        "SMOKE_POINTERS = [",
        'SMOKE_POINTERS = [\n    ("V139", DOC / "C942_VISION_V139_SMOKE.json"),\n    ("V139_heldout", DOC / "C943_VISION_V139_HELDOUT_SMOKE.json"),\n    ("V138", DOC / "C936_VISION_V138_SMOKE.json"),\n    ("V138_heldout", DOC / "C937_VISION_V138_HELDOUT_SMOKE.json"),',
        1,
    )
(S / "c945_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c940_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C940", "C946"), ("c940", "c946"),
    ("C936", "C942"), ("C937", "C943"), ("C939", "C945"),
    ("C935", "C941"),
    ("V138", "V139"), ("v138", "v139"),
    ("V137", "V138"), ("v137", "v138"),
    ("v138_jpeg_q", "v139_jpeg_q"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C932_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C944_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C938_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C938_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C938"}',
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C938"}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C932"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C944"}',
)
out = out.replace(
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C938"}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C938"}',
)
out = out.replace(
    "product-U2C replace={replace} pass={u2c_pass}",
    "confidence-gate rate={conf_rate} pass={conf_pass}",
)
out = out.replace(
    "stage_ready = bool(v139_claim and v139h_claim and v139 >= GATE and v139h >= GATE and capture_pass and disjoint and u2c_pass)",
    "stage_ready = bool(v139_claim and v139h_claim and v139 >= GATE and v139h >= GATE and capture_pass and disjoint and conf_pass)",
)
out = out.replace(
    'f"- C938: confidence-gate rate={conf_rate} pass={conf_pass}"',
    'f"- C944: confidence-gate rate={conf_rate} pass={conf_pass}"',
)
out = out.replace(
    'f"- C938: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C944: confidence-gate rate={conf_rate} pass={conf_pass}"',
)
(S / "c946_scorecard_and_stage.py").write_text(out, encoding="utf-8")
for ln in out.splitlines():
    if any(x in ln for x in ("c656 =", "c650 =", '"confidence_gate"', '"product_u2c"', "stage_ready =", "confidence-gate", "C944:", "C938:")):
        if "load" in ln or "source" in ln or "stage_ready" in ln or "confidence-gate" in ln or "product" in ln:
            print("CHK", ln.strip()[:160])
print("scorecard OK"); print("done")
