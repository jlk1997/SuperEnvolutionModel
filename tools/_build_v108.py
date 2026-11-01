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

T108 = [
    ["mossridge","recv","paid_total","MOSSRIDGE GRAIN RECV","RECV","x"],
    ["nightridge","wh","qty_sum","WH NIGHTRIDGE BIN","RECV","x"],
    ["oat ridge".replace(" ",""),"refund","refund_done","OATRIDGE PATCH REFUND","DONE","x"],
    ["pine ridge".replace(" ",""),"tax","tax_base_paid","PINERIDGE TAX SLIP","TAX","x"],
    ["quartridge","pay","payroll_active","QUARTRIDGE PAYROLL","PAY","x"],
    ["roseridge","ship","ship_ok","ROSERIDGE SHIP DOCK","SHIP","x"],
    ["spruceridge","sla","sla_ok_hours","SPRUCERIDGE SLA CARD","SLA","x"],
    ["tidalridge","exp","exp_sum","TIDALRIDGE EXPENSE","EXP","x"],
    ["umbra ridge".replace(" ",""),"po","po_open","UMBRARIDGE PO SHEET","PO","x"],
    ["vine ridge".replace(" ",""),"order","order_paid","VINERIDGE ORDER","ORD","x"],
    ["westridge","dup","dup_mark","WESTRIDGE DUP MARK","DUP","x"],
    ["yewridge","zero","zero_check","YEWRIDGE AIR ZERO","ZERO","x"],
    ["zirconridge","ledger","ledger_net","ZIRCONRIDGE LEDGER","LED","x"],
    ["alder ridge".replace(" ",""),"ui","ui_ok","ALDERRIDGE UI SCAN","UI","x"],
    ["basalt ridge".replace(" ",""),"stack","stack_count","BASALTRIDGE STACK","STK","x"],
    ["coral ridge".replace(" ",""),"fax","fax_pages","CORALRIDGE FAX","FAX","x"],
    ["duneridge","glare","glare_ok","DUNERIDGE GLARE","GLR","x"],
    ["elder ridge".replace(" ",""),"tab","tab_index","ELDERRIDGE TAB INDEX","TAB","x"],
]
# clean names that had spaces
fixes = {
    2: ["oatridge","refund","refund_done","OATRIDGE PATCH REFUND","DONE","x"],
    3: ["pineridge","tax","tax_base_paid","PINERIDGE TAX SLIP","TAX","x"],
    8: ["umbraridge","po","po_open","UMBRARIDGE PO SHEET","PO","x"],
    9: ["vineridge","order","order_paid","VINERIDGE ORDER","ORD","x"],
    13: ["alderridge","ui","ui_ok","ALDERRIDGE UI SCAN","UI","x"],
    14: ["basaltridge","stack","stack_count","BASALTRIDGE STACK","STK","x"],
    15: ["coralridge","fax","fax_pages","CORALRIDGE FAX","FAX","x"],
    17: ["elderridge","tab","tab_index","ELDERRIDGE TAB INDEX","TAB","x"],
}
for i, v in fixes.items():
    T108[i] = v
TR108 = [
    [558.0, 574.5, 367.0],[484, 524, 340],[481.0, 510.25, 347.0],[612.0, 630.0, 437.0],
    [675.0, 699.0, 407.0],[433, 449, 365],[340.0, 380.0, 220.0],[523.0, 554.75, 371.0],
    [557.0, 540.0, 380.0],[590.0, 578.0, 368.0],[1,1,0],[0,0,0],
    [656.0, 677.5, 393.0],[1,0,0],[233, 225, 203],[251, 235, 226],[1,0,0],[277, 253, 223],
]
HO108 = [
    [427.0, 439.75, 320.0],[382, 422, 302],[385.0, 398.5, 308.0],[500.0, 516.0, 349.0],
    [541.0, 557.0, 344.0],[335, 349, 313],[240.0, 280.0, 180.0],[411.0, 432.75, 320.0],
    [431.0, 419.0, 323.0],[458.0, 444.0, 315.0],[1,1,0],[0,0,0],
    [493.0, 508.5, 330.0],[1,0,0],[209, 206, 201],[225, 219, 207],[1,0,0],[235, 229, 208],
]
(ROOT / "tools/_v108_themes.json").write_text(json.dumps({"themes": T108, "train": TR108, "heldout": HO108}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_108(src):
    src = src.replace("# --- V107 overlays (new vs V50) ---", "# --- V108 overlays (new vs V50) ---")
    src = src.replace("# --- V107 overlays (new vs V49) ---", "# --- V108 overlays (new vs V49) ---")
    for a, b in [
        ("ULTRACREEK bait 51.51", "MOSSRIDGE bait 52.52"),
        ("VAPOR bait 71.71", "NIGHT bait 72.72"),
        ("WILLOW ghost 92.92", "OAT ghost 93.93"),
        ("ZINC bait 46.46", "ROSE bait 47.47"),
        ("CLOVER bait 37.37", "UMBRA bait 38.38"),
        ("GORSE bait 81.81", "ZIRCON bait 82.82"),
        ("ultra mist + lark ticks (V107-only)", "moss mist + elder ticks (V108-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD107 = "ultracreek_vaporgrove_willowcreek_xenocreek_yarrowgrove_zinccreek_astergrove_brinecreek_clovergrove_deltascreek_elmcreek_firgrove_gorsecreek_heathergrove_indigocreek_junipercove_kestrelcreek_larkgrove"
NEW108 = "_".join(t[0] for t in T108)

out = (S / "c749_vision_v107_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C749", "C755"), ("c749", "c755"), ("V107", "V108"), ("v107", "v108"),
    ("_v107c749", "_v108c755"),
    ("Harder than V106", "Harder than V107"), ("harder than V106", "harder than V107"),
    (OLD107, NEW108),
    ("V107 keeps floor", "V108 keeps floor"),
    ("C749 design+fixtures; no VL claim", "C755 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C750 VL smoke", "fixtures only; claim deferred to C756 VL smoke"),
    ("No claim until C750 VL", "No claim until C756 VL"),
    ("kept on V107", "kept on V108"),
    ("vision_images_v107", "vision_images_v108"),
    ("VL_GATE_V107", "VL_GATE_V108"), ("vl_gate_v107", "vl_gate_v108"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V106: ultracreek, vaporgrove, willowcreek, xenocreek, yarrowgrove, zinccreek, astergrove, brinecreek,\nclovergrove, deltascreek, elmcreek, firgrove, gorsecreek, heathergrove, indigocreek, junipercove, kestrelcreek, larkgrove.",
    "NEW themes vs V107: mossridge, nightridge, oatridge, pineridge, quartridge, roseridge, spruceridge, tidalridge,\numbraridge, vineridge, westridge, yewridge, zirconridge, alderridge, basaltridge, coralridge, duneridge, elderridge.",
)
out = replace_specs(out, build_specs(T108, "v108", "V108", TR108))
out = retarget_108(out)
(S / "c755_vision_v108_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c750_vision_v107_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C750", "C756"), ("c750", "c756"), ("V107", "V108"), ("v107", "v108"),
    ("Uses C749 fixtures", "Uses C755 fixtures"),
    ("vision_images_v107", "vision_images_v108"),
    ("vl_gate_v107", "vl_gate_v108"), ("VL_GATE_V107", "VL_GATE_V108"),
]:
    out = out.replace(a, b)
(S / "c756_vision_v108_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c751_vision_v107_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C751", "C757"), ("c751", "c757"), ("C749", "C755"),
    ("V107", "V108"), ("v107", "v108"),
    ("_v107hc751", "_v108hc757"), ("_v107c749", "_v108c755"),
    ("vl_gate_v107", "vl_gate_v108"), ("VL_GATE_V107", "VL_GATE_V108"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T108, "v108h", "V108H", HO108))
out = retarget_108(out)
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v108h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v108"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v108" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v108h_c757"'); seen_run = True; continue
    out2.append(ln)
(S / "c757_vision_v108_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c746_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C746", "C758"), ("c746", "c758"),
    ("product_u2c_c746", "product_u2c_c758"),
    ("after V106", "after V108"), ("after V107", "after V108"),
]:
    out = out.replace(a, b)
(S / "c758_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c753_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C753", "C759"), ("c753", "c759"),
    ("capture_regression_c753", "capture_regression_c759"),
    ("after C749-C752", "after C755-C758"),
    ("V4-V107+heldout", "V4-V108+heldout"),
]:
    out = out.replace(a, b)
if "VISION_V108_SMOKE" not in out:
    out = out.replace(
        "SMOKE_POINTERS = [",
        'SMOKE_POINTERS = [\n    ("V108", DOC / "C756_VISION_V108_SMOKE.json"),\n    ("V108_heldout", DOC / "C757_VISION_V108_HELDOUT_SMOKE.json"),\n    ("V107", DOC / "C750_VISION_V107_SMOKE.json"),\n    ("V107_heldout", DOC / "C751_VISION_V107_HELDOUT_SMOKE.json"),',
        1,
    )
(S / "c759_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c754_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C754", "C760"), ("c754", "c760"),
    ("C750", "C756"), ("C751", "C757"), ("C752", "C758"), ("C753", "C759"),
    ("C749", "C755"),
    ("V107", "V108"), ("v107", "v108"),
    ("V106", "V107"), ("v106", "v107"),
    ("v107_jpeg_q", "v108_jpeg_q"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C758_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C752_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C746_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C758_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C746"}',
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C758"}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C752"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C752"}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C758"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C752"}',
)
out = out.replace(
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C746"}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C758"}',
)
out = out.replace(
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C758"}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C758"}',
)
out = out.replace(
    "confidence-gate rate={conf_rate} pass={conf_pass}",
    "product-U2C replace={replace} pass={u2c_pass}",
)
out = out.replace(
    "stage_ready = bool(v108_claim and v108h_claim and v108 >= GATE and v108h >= GATE and capture_pass and disjoint and conf_pass)",
    "stage_ready = bool(v108_claim and v108h_claim and v108 >= GATE and v108h >= GATE and capture_pass and disjoint and u2c_pass)",
)
if "u2c_pass =" not in out:
    out = out.replace(
        'replace = float(u2c.get("replace_ratio") or 4.07)',
        'replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))',
    )
(S / "c760_scorecard_and_stage.py").write_text(out, encoding="utf-8")
for ln in out.splitlines():
    if any(x in ln for x in ("c656 =", "c650 =", '"confidence_gate"', "stage_ready =", "C758:")):
        if "load" in ln or "source" in ln or "stage_ready" in ln or "product-U2C" in ln:
            print("CHK", ln.strip()[:130])
print("scorecard OK"); print("done")
