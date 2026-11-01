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

T117 = [
    ["amberholt","recv","paid_total","AMBERHOLT GRAIN RECV","RECV","x"],
    ["bronzeholt","wh","qty_sum","WH BRONZEHOLT BIN","RECV","x"],
    ["cedarholt","refund","refund_done","CEDARHOLT PATCH REFUND","DONE","x"],
    ["driftwoodholt","tax","tax_base_paid","DRIFTWOODHOLT TAX SLIP","TAX","x"],
    ["emberholt","pay","payroll_active","EMBERHOLT PAYROLL","PAY","x"],
    ["flintholt","ship","ship_ok","FLINTHOLT SHIP DOCK","SHIP","x"],
    ["graniteholt","sla","sla_ok_hours","GRANITEHOLT SLA CARD","SLA","x"],
    ["harborholt","exp","exp_sum","HARBORHOLT EXPENSE","EXP","x"],
    ["ironholt","po","po_open","IRONHOLT PO SHEET","PO","x"],
    ["jadeholt","order","order_paid","JADEHOLT ORDER","ORD","x"],
    ["knollholt","dup","dup_mark","KNOLLHOLT DUP MARK","DUP","x"],
    ["lotusholt","zero","zero_check","LOTUSHOLT AIR ZERO","ZERO","x"],
    ["mapleholt","ledger","ledger_net","MAPLEHOLT LEDGER","LED","x"],
    ["nimbusholt","ui","ui_ok","NIMBUSHOLT UI SCAN","UI","x"],
    ["opalholt","stack","stack_count","OPALHOLT STACK","STK","x"],
    ["pebbleholt","fax","fax_pages","PEBBLEHOLT FAX","FAX","x"],
    ["quarryholt","glare","glare_ok","QUARRYHOLT GLARE","GLR","x"],
    ["ridgeholt","tab","tab_index","RIDGEHOLT TAB INDEX","TAB","x"],
]
TR117 = [
    [648.0, 665.5, 458.0],[575, 616, 430],[571.0, 600.25, 438.0],[703.0, 721.0, 528.0],
    [766.0, 790.0, 498.0],[524, 540, 456],[340.0, 380.0, 220.0],[614.0, 645.75, 462.0],
    [648.0, 631.0, 471.0],[681.0, 669.0, 459.0],[1,1,0],[0,0,0],
    [747.0, 768.5, 484.0],[1,0,0],[296, 288, 266],[314, 298, 289],[1,0,0],[340, 316, 286],
]
HO117 = [
    [518.0, 530.75, 411.0],[473, 513, 393],[476.0, 489.5, 399.0],[591.0, 607.0, 440.0],
    [632.0, 648.0, 435.0],[426, 440, 404],[240.0, 280.0, 180.0],[502.0, 523.75, 411.0],
    [522.0, 510.0, 414.0],[549.0, 535.0, 406.0],[1,1,0],[0,0,0],
    [584.0, 599.5, 421.0],[1,0,0],[272, 269, 264],[288, 282, 270],[1,0,0],[298, 292, 271],
]
(ROOT / "tools/_v117_themes.json").write_text(json.dumps({"themes": T117, "train": TR117, "heldout": HO117}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_117(src):
    src = src.replace("# --- V116 overlays (new vs V50) ---", "# --- V117 overlays (new vs V50) ---")
    src = src.replace("# --- V116 overlays (new vs V49) ---", "# --- V117 overlays (new vs V49) ---")
    for a, b in [
        ("FERNMERE bait 60.60", "AMBERHOLT bait 61.61"),
        ("GLACIER bait 80.80", "BRONZE bait 81.81"),
        ("HAZEL ghost 92.92", "CEDAR ghost 93.93"),
        ("KELP bait 55.55", "FLINT bait 56.56"),
        ("NUTMEG bait 46.46", "IRON bait 47.47"),
        ("RIVER bait 90.90", "MAPLE bait 91.91"),
        ("fern mist + wool ticks (V116-only)", "amber mist + ridge ticks (V117-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD116 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v116_themes.json").read_text(encoding="utf-8"))["themes"])
NEW117 = "_".join(t[0] for t in T117)

out = (S / "c803_vision_v116_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C803", "C809"), ("c803", "c809"), ("V116", "V117"), ("v116", "v117"),
    ("_v116c803", "_v117c809"),
    ("Harder than V115", "Harder than V116"), ("harder than V115", "harder than V116"),
    (OLD116, NEW117),
    ("V116 keeps floor", "V117 keeps floor"),
    ("C803 design+fixtures; no VL claim", "C809 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C804 VL smoke", "fixtures only; claim deferred to C810 VL smoke"),
    ("No claim until C804 VL", "No claim until C810 VL"),
    ("kept on V116", "kept on V117"),
    ("vision_images_v116", "vision_images_v117"),
    ("VL_GATE_V116", "VL_GATE_V117"), ("vl_gate_v116", "vl_gate_v117"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V115: fernmere, glaciermere, hazelmere, ivorymere, jaspermere, kelpmere, limemere, mintmere,\nnutmegmere, olivemere, pearlmere, quartzmere, rivermere, silkmere, tuffmere, umbermere, velvetmere, woolmere.",
    "NEW themes vs V116: amberholt, bronzeholt, cedarholt, driftwoodholt, emberholt, flintholt, graniteholt, harborholt,\nironholt, jadeholt, knollholt, lotusholt, mapleholt, nimbusholt, opalholt, pebbleholt, quarryholt, ridgeholt.",
)
out = replace_specs(out, build_specs(T117, "v117", "V117", TR117))
out = retarget_117(out)
(S / "c809_vision_v117_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c804_vision_v116_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C804", "C810"), ("c804", "c810"), ("V116", "V117"), ("v116", "v117"),
    ("Uses C803 fixtures", "Uses C809 fixtures"),
    ("vision_images_v116", "vision_images_v117"),
    ("vl_gate_v116", "vl_gate_v117"), ("VL_GATE_V116", "VL_GATE_V117"),
]:
    out = out.replace(a, b)
(S / "c810_vision_v117_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c805_vision_v116_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C805", "C811"), ("c805", "c811"), ("C803", "C809"),
    ("V116", "V117"), ("v116", "v117"),
    ("_v116hc805", "_v117hc811"), ("_v116c803", "_v117c809"),
    ("vl_gate_v116", "vl_gate_v117"), ("VL_GATE_V116", "VL_GATE_V117"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T117, "v117h", "V117H", HO117))
out = retarget_117(out)
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v117h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v117"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v117" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v117h_c811"'); seen_run = True; continue
    out2.append(ln)
(S / "c811_vision_v117_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c800_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C800", "C812"), ("c800", "c812"),
    ("conf_gate_stretch_c800", "conf_gate_stretch_c812"),
    ("after V115", "after V117"), ("after V116", "after V117"),
    ("cg59_", "cg60_"),
]:
    out = out.replace(a, b)
(S / "c812_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence")

out = (S / "c807_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C807", "C813"), ("c807", "c813"),
    ("capture_regression_c807", "capture_regression_c813"),
    ("after C803-C806", "after C809-C812"),
    ("V4-V116+heldout", "V4-V117+heldout"),
]:
    out = out.replace(a, b)
if "VISION_V117_SMOKE" not in out:
    out = out.replace(
        "SMOKE_POINTERS = [",
        'SMOKE_POINTERS = [\n    ("V117", DOC / "C810_VISION_V117_SMOKE.json"),\n    ("V117_heldout", DOC / "C811_VISION_V117_HELDOUT_SMOKE.json"),\n    ("V116", DOC / "C804_VISION_V116_SMOKE.json"),\n    ("V116_heldout", DOC / "C805_VISION_V116_HELDOUT_SMOKE.json"),',
        1,
    )
(S / "c813_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c808_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C808", "C814"), ("c808", "c814"),
    ("C804", "C810"), ("C805", "C811"), ("C807", "C813"),
    ("C803", "C809"),
    ("V116", "V117"), ("v116", "v117"),
    ("V115", "V116"), ("v115", "v116"),
    ("v116_jpeg_q", "v117_jpeg_q"),
]:
    out = out.replace(a, b)
# V117 confidence knife: conf=C812, u2c stays C806; stage_ready on conf_pass
out = out.replace(
    'c656 = load("docs/r50/C800_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C812_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C806_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C806_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C806"}',
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C806"}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C800"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C812"}',
)
out = out.replace(
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C806"}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C806"}',
)
out = out.replace(
    "product-U2C replace={replace} pass={u2c_pass}",
    "confidence-gate rate={conf_rate} pass={conf_pass}",
)
out = out.replace(
    "stage_ready = bool(v117_claim and v117h_claim and v117 >= GATE and v117h >= GATE and capture_pass and disjoint and u2c_pass)",
    "stage_ready = bool(v117_claim and v117h_claim and v117 >= GATE and v117h >= GATE and capture_pass and disjoint and conf_pass)",
)
out = out.replace(
    'f"- C806: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C812: confidence-gate rate={conf_rate} pass={conf_pass}"',
)
# after prior replaces the STAGE line may already be confidence form with wrong cycle
out = out.replace(
    'f"- C806: confidence-gate rate={conf_rate} pass={conf_pass}"',
    'f"- C812: confidence-gate rate={conf_rate} pass={conf_pass}"',
)
(S / "c814_scorecard_and_stage.py").write_text(out, encoding="utf-8")
for ln in out.splitlines():
    if any(x in ln for x in ("c656 =", "c650 =", '"confidence_gate"', '"product_u2c"', "stage_ready =", "confidence-gate", "C812:", "C806:")):
        if "load" in ln or "source" in ln or "stage_ready" in ln or "confidence-gate" in ln or "product" in ln:
            print("CHK", ln.strip()[:150])
print("scorecard OK"); print("done")
