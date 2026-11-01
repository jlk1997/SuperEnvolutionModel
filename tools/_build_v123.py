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

# *marsh — avoid *b; OCR-friendly PO 1132
T123 = [
    ["alder marsh","recv","paid_total","ALDERMARSH GRAIN RECV","RECV","x"],
    ["brackenmarsh","wh","qty_sum","WH BRACKENMARSH BIN","RECV","x"],
    ["cedarmarsh","refund","refund_done","CEDARMARSH PATCH REFUND","DONE","x"],
    ["dewmarsh","tax","tax_base_paid","DEWMARSH TAX SLIP","TAX","x"],
    ["echomarsh","pay","payroll_active","ECHOMARSH PAYROLL","PAY","x"],
    ["fernmarsh","ship","ship_ok","FERNMARSH SHIP DOCK","SHIP","x"],
    ["gorsemarsh","sla","sla_ok_hours","GORSEMARSH SLA CARD","SLA","x"],
    ["heathmarsh","exp","exp_sum","HEATHMARSH EXPENSE","EXP","x"],
    ["inkmarsh","po","po_open","INKMARSH PO SHEET","PO","x"],
    ["jademarsh","order","order_paid","JADEMARSH ORDER","ORD","x"],
    ["kelpmarsh","dup","dup_mark","KELPMARSH DUP MARK","DUP","x"],
    ["loammarsh","zero","zero_check","LOAMMARSH AIR ZERO","ZERO","x"],
    ["mistmarsh","ledger","ledger_net","MISTMARSH LEDGER","LED","x"],
    ["nethermarsh","ui","ui_ok","NETHERMARSH UI SCAN","UI","x"],
    ["oakmarsh","stack","stack_count","OAKMARSH STACK","STK","x"],
    ["pinemarsh","fax","fax_pages","PINEMARSH FAX","FAX","x"],
    ["quillmarsh","glare","glare_ok","QUILLMARSH GLARE","GLR","x"],
    ["reedmarsh","tab","tab_index","REEDMARSH TAB INDEX","TAB","x"],
]
T123[0] = ["aldermarsh","recv","paid_total","ALDERMARSH GRAIN RECV","RECV","x"]
TR123 = [
    [690.0, 707.5, 500.0],[617, 658, 472],[613.0, 642.25, 480.0],[746.0, 763.0, 570.0],
    [808.0, 832.0, 540.0],[566, 582, 498],[340.0, 380.0, 220.0],[656.0, 687.75, 504.0],
    [690.0, 673.0, 513.0],[723.0, 711.0, 501.0],[1,1,0],[0,0,0],
    [789.0, 810.5, 526.0],[1,0,0],[338, 330, 308],[356, 340, 331],[1,0,0],[382, 358, 328],
]
HO123 = [
    [560.0, 572.75, 453.0],[515, 555, 435],[518.0, 531.5, 441.0],[633.0, 649.0, 482.0],
    [674.0, 690.0, 477.0],[468, 482, 446],[240.0, 280.0, 180.0],[544.0, 565.75, 453.0],
    [603.0, 529.0, 450.0],[591.0, 577.0, 448.0],[1,1,0],[0,0,0],  # po 603+529=1132
    [626.0, 641.5, 463.0],[1,0,0],[314, 311, 306],[330, 324, 312],[1,0,0],[340, 334, 313],
]
(ROOT / "tools/_v123_themes.json").write_text(json.dumps({"themes": T123, "train": TR123, "heldout": HO123}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_123(src):
    src = src.replace("# --- V122 overlays (new vs V50) ---", "# --- V123 overlays (new vs V50) ---")
    src = src.replace("# --- V122 overlays (new vs V49) ---", "# --- V123 overlays (new vs V49) ---")
    for a, b in [
        ("ASHFORD bait 66.66", "ALDERMARSH bait 67.67"),
        ("CLIFF bait 86.86", "BRACKEN bait 87.87"),
        ("DAWN ghost 98.98", "CEDAR ghost 99.99"),
        ("GLEN bait 61.61", "FERN bait 62.62"),
        ("JADE bait 52.52", "INK bait 53.53"),
        ("NETH bait 96.96", "MIST bait 97.97"),
        ("ash mist + stone ticks (V122-only)", "alder mist + reed ticks (V123-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD122 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v122_themes.json").read_text(encoding="utf-8"))["themes"])
NEW123 = "_".join(t[0] for t in T123)

out = (S / "c839_vision_v122_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C839", "C845"), ("c839", "c845"), ("V122", "V123"), ("v122", "v123"),
    ("_v122c839", "_v123c845"),
    ("Harder than V121", "Harder than V122"), ("harder than V121", "harder than V122"),
    (OLD122, NEW123),
    ("V122 keeps floor", "V123 keeps floor"),
    ("C839 design+fixtures; no VL claim", "C845 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C840 VL smoke", "fixtures only; claim deferred to C846 VL smoke"),
    ("No claim until C840 VL", "No claim until C846 VL"),
    ("kept on V122", "kept on V123"),
    ("vision_images_v122", "vision_images_v123"),
    ("VL_GATE_V122", "VL_GATE_V123"), ("vl_gate_v122", "vl_gate_v123"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V121: ashford, clifford, dawnford, elmford, fernford, glenford, hazeford, inkford,\njadeford, knotford, lakeford, mossford, nethford, oakford, pineford, quillford, reedford, stoneford.",
    "NEW themes vs V122: aldermarsh, brackenmarsh, cedarmarsh, dewmarsh, echomarsh, fernmarsh, gorsemarsh, heathmarsh,\ninkmarsh, jademarsh, kelpmarsh, loammarsh, mistmarsh, nethermarsh, oakmarsh, pinemarsh, quillmarsh, reedmarsh.",
)
out = replace_specs(out, build_specs(T123, "v123", "V123", TR123))
out = retarget_123(out)
(S / "c845_vision_v123_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c840_vision_v122_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C840", "C846"), ("c840", "c846"), ("V122", "V123"), ("v122", "v123"),
    ("Uses C839 fixtures", "Uses C845 fixtures"),
    ("vision_images_v122", "vision_images_v123"),
    ("vl_gate_v122", "vl_gate_v123"), ("VL_GATE_V122", "VL_GATE_V123"),
]:
    out = out.replace(a, b)
(S / "c846_vision_v123_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c841_vision_v122_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C841", "C847"), ("c841", "c847"), ("C839", "C845"),
    ("V122", "V123"), ("v122", "v123"),
    ("_v122hc841", "_v123hc847"), ("_v122c839", "_v123c845"),
    ("vl_gate_v122", "vl_gate_v123"), ("VL_GATE_V122", "VL_GATE_V123"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T123, "v123h", "V123H", HO123))
out = retarget_123(out)
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v123h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v123"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v123" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v123h_c847"'); seen_run = True; continue
    out2.append(ln)
(S / "c847_vision_v123_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c836_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C836", "C848"), ("c836", "c848"),
    ("conf_gate_stretch_c836", "conf_gate_stretch_c848"),
    ("after V121", "after V123"), ("after V122", "after V123"),
    ("cg62_", "cg63_"),
]:
    out = out.replace(a, b)
(S / "c848_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence")

out = (S / "c843_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C843", "C849"), ("c843", "c849"),
    ("capture_regression_c843", "capture_regression_c849"),
    ("after C839-C842", "after C845-C848"),
    ("V4-V122+heldout", "V4-V123+heldout"),
]:
    out = out.replace(a, b)
if "VISION_V123_SMOKE" not in out:
    out = out.replace(
        "SMOKE_POINTERS = [",
        'SMOKE_POINTERS = [\n    ("V123", DOC / "C846_VISION_V123_SMOKE.json"),\n    ("V123_heldout", DOC / "C847_VISION_V123_HELDOUT_SMOKE.json"),\n    ("V122", DOC / "C840_VISION_V122_SMOKE.json"),\n    ("V122_heldout", DOC / "C841_VISION_V122_HELDOUT_SMOKE.json"),',
        1,
    )
(S / "c849_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c844_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C844", "C850"), ("c844", "c850"),
    ("C840", "C846"), ("C841", "C847"), ("C843", "C849"),
    ("C839", "C845"),
    ("V122", "V123"), ("v122", "v123"),
    ("V121", "V122"), ("v121", "v122"),
    ("v122_jpeg_q", "v123_jpeg_q"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C836_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C848_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C842_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C842_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C842"}',
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C842"}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C836"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C848"}',
)
out = out.replace(
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C842"}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C842"}',
)
out = out.replace(
    "product-U2C replace={replace} pass={u2c_pass}",
    "confidence-gate rate={conf_rate} pass={conf_pass}",
)
out = out.replace(
    "stage_ready = bool(v123_claim and v123h_claim and v123 >= GATE and v123h >= GATE and capture_pass and disjoint and u2c_pass)",
    "stage_ready = bool(v123_claim and v123h_claim and v123 >= GATE and v123h >= GATE and capture_pass and disjoint and conf_pass)",
)
out = out.replace(
    'f"- C842: confidence-gate rate={conf_rate} pass={conf_pass}"',
    'f"- C848: confidence-gate rate={conf_rate} pass={conf_pass}"',
)
out = out.replace(
    'f"- C842: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C848: confidence-gate rate={conf_rate} pass={conf_pass}"',
)
(S / "c850_scorecard_and_stage.py").write_text(out, encoding="utf-8")
for ln in out.splitlines():
    if any(x in ln for x in ("c656 =", "c650 =", '"confidence_gate"', '"product_u2c"', "stage_ready =", "confidence-gate", "C848:", "C842:")):
        if "load" in ln or "source" in ln or "stage_ready" in ln or "confidence-gate" in ln or "product" in ln:
            print("CHK", ln.strip()[:150])
print("scorecard OK"); print("done")
