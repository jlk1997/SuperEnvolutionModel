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

T113 = [
    ["cedarfen","recv","paid_total","CEDARFEN GRAIN RECV","RECV","x"],
    ["duskfen","wh","qty_sum","WH DUSKFEN BIN","RECV","x"],
    ["emberfen","refund","refund_done","EMBERFEN PATCH REFUND","DONE","x"],
    ["frostfen","tax","tax_base_paid","FROSTFEN TAX SLIP","TAX","x"],
    ["glenfen","pay","payroll_active","GLENFEN PAYROLL","PAY","x"],
    ["hazelfen","ship","ship_ok","HAZELFEN SHIP DOCK","SHIP","x"],
    ["ironfen","sla","sla_ok_hours","IRONFEN SLA CARD","SLA","x"],
    ["jadefen","exp","exp_sum","JADEFEN EXPENSE","EXP","x"],
    ["knollfen","po","po_open","KNOLLFEN PO SHEET","PO","x"],
    ["lotusfen","order","order_paid","LOTUSFEN ORDER","ORD","x"],
    ["meadowfen","dup","dup_mark","MEADOWFEN DUP MARK","DUP","x"],
    ["northfen","zero","zero_check","NORTHFEN AIR ZERO","ZERO","x"],
    ["opalfen","ledger","ledger_net","OPALFEN LEDGER","LED","x"],
    ["pearlfen","ui","ui_ok","PEARLFEN UI SCAN","UI","x"],
    ["quartzfen","stack","stack_count","QUARTZFEN STACK","STK","x"],
    ["ravenfen","fax","fax_pages","RAVENFEN FAX","FAX","x"],
    ["stonefen","glare","glare_ok","STONEFEN GLARE","GLR","x"],
    ["timberfen","tab","tab_index","TIMBERFEN TAB INDEX","TAB","x"],
]
TR113 = [
    [613.0, 629.5, 422.0],[539, 579, 395],[536.0, 565.25, 402.0],[667.0, 685.0, 492.0],
    [730.0, 754.0, 462.0],[488, 504, 420],[340.0, 380.0, 220.0],[578.0, 609.75, 426.0],
    [612.0, 595.0, 435.0],[645.0, 633.0, 423.0],[1,1,0],[0,0,0],
    [711.0, 732.5, 448.0],[1,0,0],[268, 260, 238],[286, 270, 261],[1,0,0],[312, 288, 258],
]
HO113 = [
    [482.0, 494.75, 375.0],[437, 477, 357],[440.0, 453.5, 363.0],[555.0, 571.0, 404.0],
    [596.0, 612.0, 399.0],[390, 404, 368],[240.0, 280.0, 180.0],[466.0, 487.75, 375.0],
    [486.0, 474.0, 378.0],[513.0, 499.0, 370.0],[1,1,0],[0,0,0],
    [548.0, 563.5, 385.0],[1,0,0],[244, 241, 236],[260, 254, 242],[1,0,0],[270, 264, 243],
]
(ROOT / "tools/_v113_themes.json").write_text(json.dumps({"themes": T113, "train": TR113, "heldout": HO113}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_113(src):
    src = src.replace("# --- V112 overlays (new vs V50) ---", "# --- V113 overlays (new vs V50) ---")
    src = src.replace("# --- V112 overlays (new vs V49) ---", "# --- V113 overlays (new vs V49) ---")
    for a, b in [
        ("KELPMERE bait 56.56", "CEDARFEN bait 57.57"),
        ("LUNAR bait 76.76", "DUSK bait 77.77"),
        ("MARLIN ghost 97.97", "EMBER ghost 98.98"),
        ("PRISM bait 51.51", "HAZEL bait 52.52"),
        ("SILT bait 42.42", "KNOLL bait 43.43"),
        ("WELD bait 86.86", "OPAL bait 87.87"),
        ("kelp mist + bloom ticks (V112-only)", "cedar mist + timber ticks (V113-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD112 = "kelpmere_lunarmere_marlinmere_nimbusmere_ottermere_prismmere_quarrymere_reefmere_siltmere_tornmere_uplandmere_valemere_weldmere_xenonmere_yelkmere_zestmere_archmere_bloommere"
NEW113 = "_".join(t[0] for t in T113)

out = (S / "c779_vision_v112_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C779", "C785"), ("c779", "c785"), ("V112", "V113"), ("v112", "v113"),
    ("_v112c779", "_v113c785"),
    ("Harder than V111", "Harder than V112"), ("harder than V111", "harder than V112"),
    (OLD112, NEW113),
    ("V112 keeps floor", "V113 keeps floor"),
    ("C779 design+fixtures; no VL claim", "C785 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C780 VL smoke", "fixtures only; claim deferred to C786 VL smoke"),
    ("No claim until C780 VL", "No claim until C786 VL"),
    ("kept on V112", "kept on V113"),
    ("vision_images_v112", "vision_images_v113"),
    ("VL_GATE_V112", "VL_GATE_V113"), ("vl_gate_v112", "vl_gate_v113"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V111: kelpmere, lunarmere, marlinmere, nimbusmere, ottermere, prismmere, quarrymere, reefmere,\nsiltmere, tornmere, uplandmere, valemere, weldmere, xenonmere, yelkmere, zestmere, archmere, bloommere.",
    "NEW themes vs V112: cedarfen, duskfen, emberfen, frostfen, glenfen, hazelfen, ironfen, jadefen,\nknollfen, lotusfen, meadowfen, northfen, opalfen, pearlfen, quartzfen, ravenfen, stonefen, timberfen.",
)
out = replace_specs(out, build_specs(T113, "v113", "V113", TR113))
out = retarget_113(out)
(S / "c785_vision_v113_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c780_vision_v112_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C780", "C786"), ("c780", "c786"), ("V112", "V113"), ("v112", "v113"),
    ("Uses C779 fixtures", "Uses C785 fixtures"),
    ("vision_images_v112", "vision_images_v113"),
    ("vl_gate_v112", "vl_gate_v113"), ("VL_GATE_V112", "VL_GATE_V113"),
]:
    out = out.replace(a, b)
(S / "c786_vision_v113_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c781_vision_v112_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C781", "C787"), ("c781", "c787"), ("C779", "C785"),
    ("V112", "V113"), ("v112", "v113"),
    ("_v112hc781", "_v113hc787"), ("_v112c779", "_v113c785"),
    ("vl_gate_v112", "vl_gate_v113"), ("VL_GATE_V112", "VL_GATE_V113"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T113, "v113h", "V113H", HO113))
out = retarget_113(out)
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v113h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v113"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v113" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v113h_c787"'); seen_run = True; continue
    out2.append(ln)
(S / "c787_vision_v113_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c776_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C776", "C788"), ("c776", "c788"),
    ("conf_gate_stretch_c776", "conf_gate_stretch_c788"),
    ("after V111", "after V113"), ("after V112", "after V113"),
    ("cg57_", "cg58_"), ("cg56_", "cg58_"),
]:
    out = out.replace(a, b)
(S / "c788_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence")

out = (S / "c783_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C783", "C789"), ("c783", "c789"),
    ("capture_regression_c783", "capture_regression_c789"),
    ("after C779-C782", "after C785-C788"),
    ("V4-V112+heldout", "V4-V113+heldout"),
]:
    out = out.replace(a, b)
if "VISION_V113_SMOKE" not in out:
    out = out.replace(
        "SMOKE_POINTERS = [",
        'SMOKE_POINTERS = [\n    ("V113", DOC / "C786_VISION_V113_SMOKE.json"),\n    ("V113_heldout", DOC / "C787_VISION_V113_HELDOUT_SMOKE.json"),\n    ("V112", DOC / "C780_VISION_V112_SMOKE.json"),\n    ("V112_heldout", DOC / "C781_VISION_V112_HELDOUT_SMOKE.json"),',
        1,
    )
(S / "c789_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c784_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C784", "C790"), ("c784", "c790"),
    ("C780", "C786"), ("C781", "C787"), ("C782", "C788"), ("C783", "C789"),
    ("C779", "C785"),
    ("V112", "V113"), ("v112", "v113"),
    ("V111", "V112"), ("v111", "v112"),
    ("v112_jpeg_q", "v113_jpeg_q"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C776_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C788_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C788_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C782_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C788"}',
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C782"}',
)
out = out.replace(
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C782"}',
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C782"}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C776"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C788"}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C788"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C788"}',
)
out = out.replace(
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C782"}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C782"}',
)
out = out.replace(
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C788"}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C782"}',
)
out = out.replace(
    "product-U2C replace={replace} pass={u2c_pass}",
    "confidence-gate rate={conf_rate} pass={conf_pass}",
)
out = out.replace(
    "stage_ready = bool(v113_claim and v113h_claim and v113 >= GATE and v113h >= GATE and capture_pass and disjoint and u2c_pass)",
    "stage_ready = bool(v113_claim and v113h_claim and v113 >= GATE and v113h >= GATE and capture_pass and disjoint and conf_pass)",
)
(S / "c790_scorecard_and_stage.py").write_text(out, encoding="utf-8")
for ln in out.splitlines():
    if any(x in ln for x in ("c656 =", "c650 =", '"confidence_gate"', "stage_ready =", "C788:")):
        if "load" in ln or "source" in ln or "stage_ready" in ln or "confidence-gate" in ln:
            print("CHK", ln.strip()[:130])
print("scorecard OK"); print("done")
