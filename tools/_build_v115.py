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

T115 = [
    ["mossdell","recv","paid_total","MOSSDELL GRAIN RECV","RECV","x"],
    ["nightdell","wh","qty_sum","WH NIGHTDELL BIN","RECV","x"],
    ["oatdell","refund","refund_done","OATDELL PATCH REFUND","DONE","x"],
    ["pinedell","tax","tax_base_paid","PINEDELL TAX SLIP","TAX","x"],
    ["quartdell","pay","payroll_active","QUARTDELL PAYROLL","PAY","x"],
    ["rosedell","ship","ship_ok","ROSEDELL SHIP DOCK","SHIP","x"],
    ["sprucedell","sla","sla_ok_hours","SPRUCEDELL SLA CARD","SLA","x"],
    ["tidaldell","exp","exp_sum","TIDALDELL EXPENSE","EXP","x"],
    ["umbradel","po","po_open","UMBRADELL PO SHEET","PO","x"],
    ["vinedell","order","order_paid","VINEDELL ORDER","ORD","x"],
    ["westdell","dup","dup_mark","WESTDELL DUP MARK","DUP","x"],
    ["yewdell","zero","zero_check","YEWDELL AIR ZERO","ZERO","x"],
    ["zircondell","ledger","ledger_net","ZIRCONDELL LEDGER","LED","x"],
    ["alderdell","ui","ui_ok","ALDERDELL UI SCAN","UI","x"],
    ["basaltdell","stack","stack_count","BASALTDELL STACK","STK","x"],
    ["coraldell","fax","fax_pages","CORALDELL FAX","FAX","x"],
    ["dunedell","glare","glare_ok","DUNEDELL GLARE","GLR","x"],
    ["elderdell","tab","tab_index","ELDERDELL TAB INDEX","TAB","x"],
]
# fix umbradel typo to umbradell
T115[8] = ["umbradell","po","po_open","UMBRADELL PO SHEET","PO","x"]
TR115 = [
    [635.0, 651.5, 444.0],[561, 601, 417],[558.0, 587.25, 424.0],[689.0, 707.0, 514.0],
    [752.0, 776.0, 484.0],[510, 526, 442],[340.0, 380.0, 220.0],[600.0, 631.75, 448.0],
    [634.0, 617.0, 457.0],[667.0, 655.0, 445.0],[1,1,0],[0,0,0],
    [733.0, 754.5, 470.0],[1,0,0],[282, 274, 252],[300, 284, 275],[1,0,0],[326, 302, 272],
]
HO115 = [
    [504.0, 516.75, 397.0],[459, 499, 379],[462.0, 475.5, 385.0],[577.0, 593.0, 426.0],
    [618.0, 634.0, 421.0],[412, 426, 390],[240.0, 280.0, 180.0],[488.0, 509.75, 397.0],
    [508.0, 496.0, 400.0],[535.0, 521.0, 392.0],[1,1,0],[0,0,0],
    [570.0, 585.5, 407.0],[1,0,0],[258, 255, 250],[274, 268, 256],[1,0,0],[284, 278, 257],
]
(ROOT / "tools/_v115_themes.json").write_text(json.dumps({"themes": T115, "train": TR115, "heldout": HO115}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_115(src):
    src = src.replace("# --- V114 overlays (new vs V50) ---", "# --- V115 overlays (new vs V50) ---")
    src = src.replace("# --- V114 overlays (new vs V49) ---", "# --- V115 overlays (new vs V49) ---")
    for a, b in [
        ("ULTRAWOLD bait 58.58", "MOSSDELL bait 59.59"),
        ("VAPOR bait 78.78", "NIGHT bait 79.79"),
        ("WILLOW ghost 99.99", "OAT ghost 91.91"),
        ("ZINC bait 53.53", "ROSE bait 54.54"),
        ("CLOVER bait 44.44", "UMBRA bait 45.45"),
        ("GORSE bait 88.88", "ZIRCON bait 89.89"),
        ("ultra mist + lark ticks (V114-only)", "moss mist + elder ticks (V115-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD114 = "ultrawold_vaporwold_willowwold_xenowold_yarrowwold_zincwold_asterwold_brinewold_cloverwold_deltaswold_elmwold_firwold_gorsewold_heatherwold_indowold_juniperwold_kestrelwold_larkwold"
NEW115 = "_".join(t[0] for t in T115)

out = (S / "c791_vision_v114_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C791", "C797"), ("c791", "c797"), ("V114", "V115"), ("v114", "v115"),
    ("_v114c791", "_v115c797"),
    ("Harder than V113", "Harder than V114"), ("harder than V113", "harder than V114"),
    (OLD114, NEW115),
    ("V114 keeps floor", "V115 keeps floor"),
    ("C791 design+fixtures; no VL claim", "C797 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C792 VL smoke", "fixtures only; claim deferred to C798 VL smoke"),
    ("No claim until C792 VL", "No claim until C798 VL"),
    ("kept on V114", "kept on V115"),
    ("vision_images_v114", "vision_images_v115"),
    ("VL_GATE_V114", "VL_GATE_V115"), ("vl_gate_v114", "vl_gate_v115"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V113: ultrawold, vaporwold, willowwold, xenowold, yarrowwold, zincwold, asterwold, brinewold,\ncloverwold, deltaswold, elmwold, firwold, gorsewold, heatherwold, indowold, juniperwold, kestrelwold, larkwold.",
    "NEW themes vs V114: mossdell, nightdell, oatdell, pinedell, quartdell, rosedell, sprucedell, tidaldell,\numbradell, vinedell, westdell, yewdell, zircondell, alderdell, basaltdell, coraldell, dunedell, elderdell.",
)
out = replace_specs(out, build_specs(T115, "v115", "V115", TR115))
out = retarget_115(out)
(S / "c797_vision_v115_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c792_vision_v114_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C792", "C798"), ("c792", "c798"), ("V114", "V115"), ("v114", "v115"),
    ("Uses C791 fixtures", "Uses C797 fixtures"),
    ("vision_images_v114", "vision_images_v115"),
    ("vl_gate_v114", "vl_gate_v115"), ("VL_GATE_V114", "VL_GATE_V115"),
]:
    out = out.replace(a, b)
(S / "c798_vision_v115_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c793_vision_v114_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C793", "C799"), ("c793", "c799"), ("C791", "C797"),
    ("V114", "V115"), ("v114", "v115"),
    ("_v114hc793", "_v115hc799"), ("_v114c791", "_v115c797"),
    ("vl_gate_v114", "vl_gate_v115"), ("VL_GATE_V114", "VL_GATE_V115"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T115, "v115h", "V115H", HO115))
out = retarget_115(out)
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v115h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v115"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v115" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v115h_c799"'); seen_run = True; continue
    out2.append(ln)
(S / "c799_vision_v115_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c788_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C788", "C800"), ("c788", "c800"),
    ("conf_gate_stretch_c788", "conf_gate_stretch_c800"),
    ("after V113", "after V115"), ("after V114", "after V115"),
    ("cg58_", "cg59_"), ("cg57_", "cg59_"),
]:
    out = out.replace(a, b)
(S / "c800_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence")

out = (S / "c795_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C795", "C801"), ("c795", "c801"),
    ("capture_regression_c795", "capture_regression_c801"),
    ("after C791-C794", "after C797-C800"),
    ("V4-V114+heldout", "V4-V115+heldout"),
]:
    out = out.replace(a, b)
if "VISION_V115_SMOKE" not in out:
    out = out.replace(
        "SMOKE_POINTERS = [",
        'SMOKE_POINTERS = [\n    ("V115", DOC / "C798_VISION_V115_SMOKE.json"),\n    ("V115_heldout", DOC / "C799_VISION_V115_HELDOUT_SMOKE.json"),\n    ("V114", DOC / "C792_VISION_V114_SMOKE.json"),\n    ("V114_heldout", DOC / "C793_VISION_V114_HELDOUT_SMOKE.json"),',
        1,
    )
(S / "c801_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c796_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C796", "C802"), ("c796", "c802"),
    ("C792", "C798"), ("C793", "C799"), ("C794", "C800"), ("C795", "C801"),
    ("C791", "C797"),
    ("V114", "V115"), ("v114", "v115"),
    ("V113", "V114"), ("v113", "v114"),
    ("v114_jpeg_q", "v115_jpeg_q"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C788_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C800_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C800_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C794_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C800"}',
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C794"}',
)
out = out.replace(
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C794"}',
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C794"}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C788"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C800"}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C800"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C800"}',
)
out = out.replace(
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C794"}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C794"}',
)
out = out.replace(
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C800"}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C794"}',
)
out = out.replace(
    "product-U2C replace={replace} pass={u2c_pass}",
    "confidence-gate rate={conf_rate} pass={conf_pass}",
)
out = out.replace(
    "stage_ready = bool(v115_claim and v115h_claim and v115 >= GATE and v115h >= GATE and capture_pass and disjoint and u2c_pass)",
    "stage_ready = bool(v115_claim and v115h_claim and v115 >= GATE and v115h >= GATE and capture_pass and disjoint and conf_pass)",
)
(S / "c802_scorecard_and_stage.py").write_text(out, encoding="utf-8")
for ln in out.splitlines():
    if any(x in ln for x in ("c656 =", "c650 =", '"confidence_gate"', "stage_ready =", "C800:")):
        if "load" in ln or "source" in ln or "stage_ready" in ln or "confidence-gate" in ln:
            print("CHK", ln.strip()[:130])
print("scorecard OK"); print("done")
