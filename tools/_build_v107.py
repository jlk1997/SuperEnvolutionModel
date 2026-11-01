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

# ---- V107 (confidence-gate) ----
T107 = [
    ["ultracreek","recv","paid_total","ULTRACREEK GRAIN RECV","RECV","x"],
    ["vapor grove".replace(" ",""),"wh","qty_sum","WH VAPORGROVE BIN","RECV","x"],
    ["willowcreek","refund","refund_done","WILLOWCREEK PATCH REFUND","DONE","x"],
    ["xenocreek","tax","tax_base_paid","XENOCREEK TAX SLIP","TAX","x"],
    ["yarrowgrove","pay","payroll_active","YARROWGROVE PAYROLL","PAY","x"],
    ["zinccreek","ship","ship_ok","ZINCCREEK SHIP DOCK","SHIP","x"],
    ["astergrove","sla","sla_ok_hours","ASTERGROVE SLA CARD","SLA","x"],
    ["brinecreek","exp","exp_sum","BRINECREEK EXPENSE","EXP","x"],
    ["clovergrove","po","po_open","CLOVERGROVE PO SHEET","PO","x"],
    ["deltascreek","order","order_paid","DELTASCREEK ORDER","ORD","x"],
    ["elmcreek","dup","dup_mark","ELMCREEK DUP MARK","DUP","x"],
    ["firgrove","zero","zero_check","FIRGROVE AIR ZERO","ZERO","x"],
    ["gorsecreek","ledger","ledger_net","GORSECREEK LEDGER","LED","x"],
    ["heathergrove","ui","ui_ok","HEATHERGROVE UI SCAN","UI","x"],
    ["indigocreek","stack","stack_count","INDIGOCREEK STACK","STK","x"],
    ["junipercove","fax","fax_pages","JUNIPERCOVE FAX","FAX","x"],
    ["kestrelcreek","glare","glare_ok","KESTRELCREEK GLARE","GLR","x"],
    ["larkgrove","tab","tab_index","LARKGROVE TAB INDEX","TAB","x"],
]
T107[1] = ["vaporgrove","wh","qty_sum","WH VAPORGROVE BIN","RECV","x"]
TR107 = [
    [547.0, 563.5, 356.0],[473, 513, 329],[470.0, 499.25, 336.0],[601.0, 619.0, 426.0],
    [664.0, 688.0, 396.0],[422, 438, 354],[340.0, 380.0, 220.0],[512.0, 543.75, 360.0],
    [546.0, 529.0, 369.0],[579.0, 567.0, 357.0],[1,1,0],[0,0,0],
    [645.0, 666.5, 382.0],[1,0,0],[226, 218, 196],[244, 228, 219],[1,0,0],[270, 246, 216],
]
HO107 = [
    [416.0, 428.75, 309.0],[371, 411, 291],[374.0, 387.5, 297.0],[489.0, 505.0, 338.0],
    [530.0, 546.0, 333.0],[324, 338, 302],[240.0, 280.0, 180.0],[400.0, 421.75, 309.0],
    [420.0, 408.0, 312.0],[447.0, 433.0, 304.0],[1,1,0],[0,0,0],
    [482.0, 497.5, 319.0],[1,0,0],[202, 199, 194],[218, 212, 200],[1,0,0],[228, 222, 201],
]
(ROOT / "tools/_v107_themes.json").write_text(json.dumps({"themes": T107, "train": TR107, "heldout": HO107}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_107(src):
    src = src.replace("# --- V106 overlays (new vs V50) ---", "# --- V107 overlays (new vs V50) ---")
    src = src.replace("# --- V106 overlays (new vs V49) ---", "# --- V107 overlays (new vs V49) ---")
    for a, b in [
        ("CEDARFALL bait 50.50", "ULTRACREEK bait 51.51"),
        ("DUSK bait 70.70", "VAPOR bait 71.71"),
        ("EMBER ghost 91.91", "WILLOW ghost 92.92"),
        ("HAZEL bait 45.45", "ZINC bait 46.46"),
        ("KNOLL bait 36.36", "CLOVER bait 37.37"),
        ("OPAL bait 80.80", "GORSE bait 81.81"),
        ("cedar mist + timber ticks (V106-only)", "ultra mist + lark ticks (V107-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD106 = "cedarfall_duskfall_emberfall_frostfall_glenfall_hazelfall_ironfall_jadefall_knollfall_lotusfall_meadowfall_northfall_opalfall_pearlfall_quartzfall_ravenfall_stonefall_timberfall"
NEW107 = "_".join(t[0] for t in T107)

out = (S / "c743_vision_v106_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C743", "C749"), ("c743", "c749"), ("V106", "V107"), ("v106", "v107"),
    ("_v106c743", "_v107c749"),
    ("Harder than V105", "Harder than V106"), ("harder than V105", "harder than V106"),
    (OLD106, NEW107),
    ("V106 keeps floor", "V107 keeps floor"),
    ("C743 design+fixtures; no VL claim", "C749 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C744 VL smoke", "fixtures only; claim deferred to C750 VL smoke"),
    ("No claim until C744 VL", "No claim until C750 VL"),
    ("kept on V106", "kept on V107"),
    ("vision_images_v106", "vision_images_v107"),
    ("VL_GATE_V106", "VL_GATE_V107"), ("vl_gate_v106", "vl_gate_v107"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V105: cedarfall, duskfall, emberfall, frostfall, glenfall, hazelfall, ironfall, jadefall,\nknollfall, lotusfall, meadowfall, northfall, opalfall, pearlfall, quartzfall, ravenfall, stonefall, timberfall.",
    "NEW themes vs V106: ultracreek, vaporgrove, willowcreek, xenocreek, yarrowgrove, zinccreek, astergrove, brinecreek,\nclovergrove, deltascreek, elmcreek, firgrove, gorsecreek, heathergrove, indigocreek, junipercove, kestrelcreek, larkgrove.",
)
out = replace_specs(out, build_specs(T107, "v107", "V107", TR107))
out = retarget_107(out)
(S / "c749_vision_v107_design_and_batch.py").write_text(out, encoding="utf-8")
print("v107 design")

out = (S / "c744_vision_v106_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C744", "C750"), ("c744", "c750"), ("V106", "V107"), ("v106", "v107"),
    ("Uses C743 fixtures", "Uses C749 fixtures"),
    ("vision_images_v106", "vision_images_v107"),
    ("vl_gate_v106", "vl_gate_v107"), ("VL_GATE_V106", "VL_GATE_V107"),
]:
    out = out.replace(a, b)
(S / "c750_vision_v107_smoke.py").write_text(out, encoding="utf-8")
print("v107 smoke")

out = (S / "c745_vision_v106_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C745", "C751"), ("c745", "c751"), ("C743", "C749"),
    ("V106", "V107"), ("v106", "v107"),
    ("_v106hc745", "_v107hc751"), ("_v106c743", "_v107c749"),
    ("vl_gate_v106", "vl_gate_v107"), ("VL_GATE_V106", "VL_GATE_V107"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T107, "v107h", "V107H", HO107))
out = retarget_107(out)
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v107h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v107"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v107" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v107h_c751"'); seen_run = True; continue
    out2.append(ln)
(S / "c751_vision_v107_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("v107 heldout", seen_fix, seen_train, seen_run)

out = (S / "c740_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C740", "C752"), ("c740", "c752"),
    ("conf_gate_stretch_c740", "conf_gate_stretch_c752"),
    ("after V105", "after V107"), ("after V106", "after V107"),
    ("cg54_", "cg55_"), ("cg53_", "cg55_"),
]:
    out = out.replace(a, b)
(S / "c752_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("v107 confidence")

out = (S / "c747_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C747", "C753"), ("c747", "c753"),
    ("capture_regression_c747", "capture_regression_c753"),
    ("after C743-C746", "after C749-C752"),
    ("V4-V106+heldout", "V4-V107+heldout"),
]:
    out = out.replace(a, b)
if "VISION_V107_SMOKE" not in out:
    out = out.replace(
        "SMOKE_POINTERS = [",
        'SMOKE_POINTERS = [\n    ("V107", DOC / "C750_VISION_V107_SMOKE.json"),\n    ("V107_heldout", DOC / "C751_VISION_V107_HELDOUT_SMOKE.json"),\n    ("V106", DOC / "C744_VISION_V106_SMOKE.json"),\n    ("V106_heldout", DOC / "C745_VISION_V106_HELDOUT_SMOKE.json"),',
        1,
    )
(S / "c753_capture_office_regression.py").write_text(out, encoding="utf-8")
print("v107 regression")

out = (S / "c748_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C748", "C754"), ("c748", "c754"),
    ("C744", "C750"), ("C745", "C751"), ("C746", "C752"), ("C747", "C753"),
    ("C743", "C749"),
    ("V106", "V107"), ("v106", "v107"),
    ("V105", "V106"), ("v105", "v106"),
    ("v106_jpeg_q", "v107_jpeg_q"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C740_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C752_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c656 = load("docs/r50/C752_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C752_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C752_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C746_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C752"}',
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C746"}',
)
out = out.replace(
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C746"}',
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C746"}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C740"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C752"}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C752"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C752"}',
)
out = out.replace(
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C746"}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C746"}',
)
out = out.replace(
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C752"}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C746"}',
)
out = out.replace(
    "product-U2C replace={replace} pass={u2c_pass}",
    "confidence-gate rate={conf_rate} pass={conf_pass}",
)
out = out.replace(
    "stage_ready = bool(v107_claim and v107h_claim and v107 >= GATE and v107h >= GATE and capture_pass and disjoint and u2c_pass)",
    "stage_ready = bool(v107_claim and v107h_claim and v107 >= GATE and v107h >= GATE and capture_pass and disjoint and conf_pass)",
)
(S / "c754_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("v107 scorecard")
for ln in out.splitlines():
    if any(x in ln for x in ("c656 =", "c650 =", '"confidence_gate"', "stage_ready =", "C752:")):
        if "load" in ln or "source" in ln or "stage_ready" in ln or "confidence-gate" in ln:
            print("CHK107", ln.strip()[:130])
print("done v107")
