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

T116 = [
    ["fernmere","recv","paid_total","FERNMERE GRAIN RECV","RECV","x"],
    ["glaciermere","wh","qty_sum","WH GLACIERMERE BIN","RECV","x"],
    ["hazelmere","refund","refund_done","HAZELMERE PATCH REFUND","DONE","x"],
    ["ivorymere","tax","tax_base_paid","IVORYMERE TAX SLIP","TAX","x"],
    ["jaspermere","pay","payroll_active","JASPERMERE PAYROLL","PAY","x"],
    ["kelpmere","ship","ship_ok","KELPMERE SHIP DOCK","SHIP","x"],
    ["limemere","sla","sla_ok_hours","LIMEMERE SLA CARD","SLA","x"],
    ["mintmere","exp","exp_sum","MINTMERE EXPENSE","EXP","x"],
    ["nutmegmere","po","po_open","NUTMEGMERE PO SHEET","PO","x"],
    ["olivemere","order","order_paid","OLIVEMERE ORDER","ORD","x"],
    ["pearlmere","dup","dup_mark","PEARLMERE DUP MARK","DUP","x"],
    ["quartzmere","zero","zero_check","QUARTZMERE AIR ZERO","ZERO","x"],
    ["rivermere","ledger","ledger_net","RIVERMERE LEDGER","LED","x"],
    ["silkmere","ui","ui_ok","SILKMERE UI SCAN","UI","x"],
    ["tuffmere","stack","stack_count","TUFFMERE STACK","STK","x"],
    ["umbermere","fax","fax_pages","UMBERMERE FAX","FAX","x"],
    ["velvetmere","glare","glare_ok","VELVETMERE GLARE","GLR","x"],
    ["woolmere","tab","tab_index","WOOLMERE TAB INDEX","TAB","x"],
]
TR116 = [
    [641.0, 658.5, 451.0],[568, 609, 423],[564.0, 593.25, 431.0],[696.0, 714.0, 521.0],
    [759.0, 783.0, 491.0],[517, 533, 449],[340.0, 380.0, 220.0],[607.0, 638.75, 455.0],
    [641.0, 624.0, 464.0],[674.0, 662.0, 452.0],[1,1,0],[0,0,0],
    [740.0, 761.5, 477.0],[1,0,0],[289, 281, 259],[307, 291, 282],[1,0,0],[333, 309, 279],
]
HO116 = [
    [511.0, 523.75, 404.0],[466, 506, 386],[469.0, 482.5, 392.0],[584.0, 600.0, 433.0],
    [625.0, 641.0, 428.0],[419, 433, 397],[240.0, 280.0, 180.0],[495.0, 516.75, 404.0],
    [515.0, 503.0, 407.0],[542.0, 528.0, 399.0],[1,1,0],[0,0,0],
    [577.0, 592.5, 414.0],[1,0,0],[265, 262, 257],[281, 275, 263],[1,0,0],[291, 285, 264],
]
(ROOT / "tools/_v116_themes.json").write_text(json.dumps({"themes": T116, "train": TR116, "heldout": HO116}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_116(src):
    src = src.replace("# --- V115 overlays (new vs V50) ---", "# --- V116 overlays (new vs V50) ---")
    src = src.replace("# --- V115 overlays (new vs V49) ---", "# --- V116 overlays (new vs V49) ---")
    for a, b in [
        ("MOSSDELL bait 59.59", "FERNMERE bait 60.60"),
        ("NIGHT bait 79.79", "GLACIER bait 80.80"),
        ("OAT ghost 91.91", "HAZEL ghost 92.92"),
        ("ROSE bait 54.54", "KELP bait 55.55"),
        ("UMBRA bait 45.45", "NUTMEG bait 46.46"),
        ("ZIRCON bait 89.89", "RIVER bait 90.90"),
        ("moss mist + elder ticks (V115-only)", "fern mist + wool ticks (V116-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD115 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v115_themes.json").read_text(encoding="utf-8"))["themes"])
NEW116 = "_".join(t[0] for t in T116)

out = (S / "c797_vision_v115_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C797", "C803"), ("c797", "c803"), ("V115", "V116"), ("v115", "v116"),
    ("_v115c797", "_v116c803"),
    ("Harder than V114", "Harder than V115"), ("harder than V114", "harder than V115"),
    (OLD115, NEW116),
    ("V115 keeps floor", "V116 keeps floor"),
    ("C797 design+fixtures; no VL claim", "C803 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C798 VL smoke", "fixtures only; claim deferred to C804 VL smoke"),
    ("No claim until C798 VL", "No claim until C804 VL"),
    ("kept on V115", "kept on V116"),
    ("vision_images_v115", "vision_images_v116"),
    ("VL_GATE_V115", "VL_GATE_V116"), ("vl_gate_v115", "vl_gate_v116"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V114: mossdell, nightdell, oatdell, pinedell, quartdell, rosedell, sprucedell, tidaldell,\numbradell, vinedell, westdell, yewdell, zircondell, alderdell, basaltdell, coraldell, dunedell, elderdell.",
    "NEW themes vs V115: fernmere, glaciermere, hazelmere, ivorymere, jaspermere, kelpmere, limemere, mintmere,\nnutmegmere, olivemere, pearlmere, quartzmere, rivermere, silkmere, tuffmere, umbermere, velvetmere, woolmere.",
)
out = replace_specs(out, build_specs(T116, "v116", "V116", TR116))
out = retarget_116(out)
(S / "c803_vision_v116_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c798_vision_v115_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C798", "C804"), ("c798", "c804"), ("V115", "V116"), ("v115", "v116"),
    ("Uses C797 fixtures", "Uses C803 fixtures"),
    ("vision_images_v115", "vision_images_v116"),
    ("vl_gate_v115", "vl_gate_v116"), ("VL_GATE_V115", "VL_GATE_V116"),
]:
    out = out.replace(a, b)
(S / "c804_vision_v116_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c799_vision_v115_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C799", "C805"), ("c799", "c805"), ("C797", "C803"),
    ("V115", "V116"), ("v115", "v116"),
    ("_v115hc799", "_v116hc805"), ("_v115c797", "_v116c803"),
    ("vl_gate_v115", "vl_gate_v116"), ("VL_GATE_V115", "VL_GATE_V116"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T116, "v116h", "V116H", HO116))
out = retarget_116(out)
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v116h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v116"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v116" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v116h_c805"'); seen_run = True; continue
    out2.append(ln)
(S / "c805_vision_v116_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c794_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C794", "C806"), ("c794", "c806"),
    ("product_u2c_c794", "product_u2c_c806"),
    ("after V114", "after V116"), ("after V115", "after V116"),
]:
    out = out.replace(a, b)
(S / "c806_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c801_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C801", "C807"), ("c801", "c807"),
    ("capture_regression_c801", "capture_regression_c807"),
    ("after C797-C800", "after C803-C806"),
    ("V4-V115+heldout", "V4-V116+heldout"),
]:
    out = out.replace(a, b)
if "VISION_V116_SMOKE" not in out:
    out = out.replace(
        "SMOKE_POINTERS = [",
        'SMOKE_POINTERS = [\n    ("V116", DOC / "C804_VISION_V116_SMOKE.json"),\n    ("V116_heldout", DOC / "C805_VISION_V116_HELDOUT_SMOKE.json"),\n    ("V115", DOC / "C798_VISION_V115_SMOKE.json"),\n    ("V115_heldout", DOC / "C799_VISION_V115_HELDOUT_SMOKE.json"),',
        1,
    )
(S / "c807_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c802_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C802", "C808"), ("c802", "c808"),
    ("C798", "C804"), ("C799", "C805"), ("C801", "C807"),
    ("C797", "C803"),
    ("V115", "V116"), ("v115", "v116"),
    ("V114", "V115"), ("v114", "v115"),
    ("v115_jpeg_q", "v116_jpeg_q"),
]:
    out = out.replace(a, b)
# V116 is U2C knife: conf stays C800; u2c becomes C806; stage_ready gates on u2c_pass
out = out.replace(
    'c656 = load("docs/r50/C800_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C800_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C794_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C806_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C794"}',
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C806"}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C800"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C800"}',
)
out = out.replace(
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C794"}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C806"}',
)
out = out.replace(
    "confidence-gate rate={conf_rate} pass={conf_pass}",
    "product-U2C replace={replace} pass={u2c_pass}",
)
out = out.replace(
    "stage_ready = bool(v116_claim and v116h_claim and v116 >= GATE and v116h >= GATE and capture_pass and disjoint and conf_pass)",
    "stage_ready = bool(v116_claim and v116h_claim and v116 >= GATE and v116h >= GATE and capture_pass and disjoint and u2c_pass)",
)
# also catch if double-replace left conf_pass in stage_ready from intermediate
out = out.replace(
    "stage_ready = bool(v116_claim and v116h_claim and v116 >= GATE and v116h >= GATE and capture_pass and disjoint and conf_pass)",
    "stage_ready = bool(v116_claim and v116h_claim and v116 >= GATE and v116h >= GATE and capture_pass and disjoint and u2c_pass)",
)
(S / "c808_scorecard_and_stage.py").write_text(out, encoding="utf-8")
for ln in out.splitlines():
    if any(x in ln for x in ("c656 =", "c650 =", '"confidence_gate"', '"product_u2c"', "stage_ready =", "product-U2C", "C806:", "C800:")):
        if "load" in ln or "source" in ln or "stage_ready" in ln or "product-U2C" in ln or "confidence" in ln:
            print("CHK", ln.strip()[:140])
print("scorecard OK"); print("done")
