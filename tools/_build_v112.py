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

T112 = [
    ["kelpmere","recv","paid_total","KELPMERE GRAIN RECV","RECV","x"],
    ["lunarmere","wh","qty_sum","WH LUNARMERE BIN","RECV","x"],
    ["marlinmere","refund","refund_done","MARLINMERE PATCH REFUND","DONE","x"],
    ["nimbusmere","tax","tax_base_paid","NIMBUSMERE TAX SLIP","TAX","x"],
    ["ottermere","pay","payroll_active","OTTERMERE PAYROLL","PAY","x"],
    ["prismmere","ship","ship_ok","PRISMMERE SHIP DOCK","SHIP","x"],
    ["quarrymere","sla","sla_ok_hours","QUARRYMERE SLA CARD","SLA","x"],
    ["reefmere","exp","exp_sum","REEFMERE EXPENSE","EXP","x"],
    ["siltmere","po","po_open","SILTMERE PO SHEET","PO","x"],
    ["tornmere","order","order_paid","TORNMERE ORDER","ORD","x"],
    ["uplandmere","dup","dup_mark","UPLANDMERE DUP MARK","DUP","x"],
    ["valemere","zero","zero_check","VALEMERE AIR ZERO","ZERO","x"],
    ["weldmere","ledger","ledger_net","WELDMERE LEDGER","LED","x"],
    ["xenonmere","ui","ui_ok","XENONMERE UI SCAN","UI","x"],
    ["yelkmere","stack","stack_count","YELKMERE STACK","STK","x"],
    ["zestmere","fax","fax_pages","ZESTMERE FAX","FAX","x"],
    ["archmere","glare","glare_ok","ARCHMERE GLARE","GLR","x"],
    ["bloommere","tab","tab_index","BLOOMMERE TAB INDEX","TAB","x"],
]
TR112 = [
    [602.0, 618.5, 411.0],[528, 568, 384],[525.0, 554.25, 391.0],[656.0, 674.0, 481.0],
    [719.0, 743.0, 451.0],[477, 493, 409],[340.0, 380.0, 220.0],[567.0, 598.75, 415.0],
    [601.0, 584.0, 424.0],[634.0, 622.0, 412.0],[1,1,0],[0,0,0],
    [700.0, 721.5, 437.0],[1,0,0],[261, 253, 231],[279, 263, 254],[1,0,0],[305, 281, 251],
]
HO112 = [
    [471.0, 483.75, 364.0],[426, 466, 346],[429.0, 442.5, 352.0],[544.0, 560.0, 393.0],
    [585.0, 601.0, 388.0],[379, 393, 357],[240.0, 280.0, 180.0],[455.0, 476.75, 364.0],
    [475.0, 463.0, 367.0],[502.0, 488.0, 359.0],[1,1,0],[0,0,0],
    [537.0, 552.5, 374.0],[1,0,0],[237, 234, 229],[253, 247, 235],[1,0,0],[263, 257, 236],
]
(ROOT / "tools/_v112_themes.json").write_text(json.dumps({"themes": T112, "train": TR112, "heldout": HO112}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_112(src):
    src = src.replace("# --- V111 overlays (new vs V50) ---", "# --- V112 overlays (new vs V50) ---")
    src = src.replace("# --- V111 overlays (new vs V49) ---", "# --- V112 overlays (new vs V49) ---")
    for a, b in [
        ("SAFFRONVALE bait 55.55", "KELPMERE bait 56.56"),
        ("TUNDRA bait 75.75", "LUNAR bait 76.76"),
        ("UMB ghost 96.96", "MARLIN ghost 97.97"),
        ("XYLA bait 50.50", "PRISM bait 51.51"),
        ("ALPINE bait 41.41", "SILT bait 42.42"),
        ("ELD bait 85.85", "WELD bait 86.86"),
        ("saffron mist + jasper ticks (V111-only)", "kelp mist + bloom ticks (V112-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD111 = "saffronvale_tundravale_umbvale_verdvale_wispvale_xylavale_yarrowvale_zephyrvale_alpinevale_brackenvale_cascadevale_dunevale_eldvale_fjordvale_gullvale_hollowvale_isletvale_jaspervale"
NEW112 = "_".join(t[0] for t in T112)

out = (S / "c773_vision_v111_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C773", "C779"), ("c773", "c779"), ("V111", "V112"), ("v111", "v112"),
    ("_v111c773", "_v112c779"),
    ("Harder than V110", "Harder than V111"), ("harder than V110", "harder than V111"),
    (OLD111, NEW112),
    ("V111 keeps floor", "V112 keeps floor"),
    ("C773 design+fixtures; no VL claim", "C779 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C774 VL smoke", "fixtures only; claim deferred to C780 VL smoke"),
    ("No claim until C774 VL", "No claim until C780 VL"),
    ("kept on V111", "kept on V112"),
    ("vision_images_v111", "vision_images_v112"),
    ("VL_GATE_V111", "VL_GATE_V112"), ("vl_gate_v111", "vl_gate_v112"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V110: saffronvale, tundravale, umbvale, verdvale, wispvale, xylavale, yarrowvale, zephyrvale,\nalpinevale, brackenvale, cascadevale, dunevale, eldvale, fjordvale, gullvale, hollowvale, isletvale, jaspervale.",
    "NEW themes vs V111: kelpmere, lunarmere, marlinmere, nimbusmere, ottermere, prismmere, quarrymere, reefmere,\nsiltmere, tornmere, uplandmere, valemere, weldmere, xenonmere, yelkmere, zestmere, archmere, bloommere.",
)
out = replace_specs(out, build_specs(T112, "v112", "V112", TR112))
out = retarget_112(out)
(S / "c779_vision_v112_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c774_vision_v111_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C774", "C780"), ("c774", "c780"), ("V111", "V112"), ("v111", "v112"),
    ("Uses C773 fixtures", "Uses C779 fixtures"),
    ("vision_images_v111", "vision_images_v112"),
    ("vl_gate_v111", "vl_gate_v112"), ("VL_GATE_V111", "VL_GATE_V112"),
]:
    out = out.replace(a, b)
(S / "c780_vision_v112_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c775_vision_v111_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C775", "C781"), ("c775", "c781"), ("C773", "C779"),
    ("V111", "V112"), ("v111", "v112"),
    ("_v111hc775", "_v112hc781"), ("_v111c773", "_v112c779"),
    ("vl_gate_v111", "vl_gate_v112"), ("VL_GATE_V111", "VL_GATE_V112"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T112, "v112h", "V112H", HO112))
out = retarget_112(out)
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v112h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v112"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v112" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v112h_c781"'); seen_run = True; continue
    out2.append(ln)
(S / "c781_vision_v112_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c770_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C770", "C782"), ("c770", "c782"),
    ("product_u2c_c770", "product_u2c_c782"),
    ("after V110", "after V112"), ("after V111", "after V112"),
]:
    out = out.replace(a, b)
(S / "c782_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c777_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C777", "C783"), ("c777", "c783"),
    ("capture_regression_c777", "capture_regression_c783"),
    ("after C773-C776", "after C779-C782"),
    ("V4-V111+heldout", "V4-V112+heldout"),
]:
    out = out.replace(a, b)
if "VISION_V112_SMOKE" not in out:
    out = out.replace(
        "SMOKE_POINTERS = [",
        'SMOKE_POINTERS = [\n    ("V112", DOC / "C780_VISION_V112_SMOKE.json"),\n    ("V112_heldout", DOC / "C781_VISION_V112_HELDOUT_SMOKE.json"),\n    ("V111", DOC / "C774_VISION_V111_SMOKE.json"),\n    ("V111_heldout", DOC / "C775_VISION_V111_HELDOUT_SMOKE.json"),',
        1,
    )
(S / "c783_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c778_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C778", "C784"), ("c778", "c784"),
    ("C774", "C780"), ("C775", "C781"), ("C776", "C782"), ("C777", "C783"),
    ("C773", "C779"),
    ("V111", "V112"), ("v111", "v112"),
    ("V110", "V111"), ("v110", "v111"),
    ("v111_jpeg_q", "v112_jpeg_q"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C782_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C776_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C770_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C782_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C770"}',
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C782"}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C776"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C776"}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C782"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C776"}',
)
out = out.replace(
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C770"}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C782"}',
)
out = out.replace(
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C782"}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C782"}',
)
out = out.replace(
    "confidence-gate rate={conf_rate} pass={conf_pass}",
    "product-U2C replace={replace} pass={u2c_pass}",
)
out = out.replace(
    "stage_ready = bool(v112_claim and v112h_claim and v112 >= GATE and v112h >= GATE and capture_pass and disjoint and conf_pass)",
    "stage_ready = bool(v112_claim and v112h_claim and v112 >= GATE and v112h >= GATE and capture_pass and disjoint and u2c_pass)",
)
if "u2c_pass =" not in out:
    out = out.replace(
        'replace = float(u2c.get("replace_ratio") or 4.07)',
        'replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))',
    )
(S / "c784_scorecard_and_stage.py").write_text(out, encoding="utf-8")
for ln in out.splitlines():
    if any(x in ln for x in ("c656 =", "c650 =", '"confidence_gate"', "stage_ready =", "C782:")):
        if "load" in ln or "source" in ln or "stage_ready" in ln or "product-U2C" in ln:
            print("CHK", ln.strip()[:130])
print("scorecard OK"); print("done")
