# -*- coding: utf-8 -*-
from __future__ import annotations
import json, re
from pathlib import Path
ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"
THEMES = [
    ["saffroncreek","recv","paid_total","SAFFRONCREEK GRAIN RECV","RECV","x"],
    ["tundragrove","wh","qty_sum","WH TUNDRAGROVE BIN","RECV","x"],
    ["umbcreek","refund","refund_done","UMBCREEK PATCH REFUND","DONE","x"],
    ["verdgrove","tax","tax_base_paid","VERDGROVE TAX SLIP","TAX","x"],
    ["wispcreek","pay","payroll_active","WISPCREEK PAYROLL","PAY","x"],
    ["xylagrove","ship","ship_ok","XYLAGROVE SHIP DOCK","SHIP","x"],
    ["yarrowcreek","sla","sla_ok_hours","YARROWCREEK SLA CARD","SLA","x"],
    ["zephyrgrove","exp","exp_sum","ZEPHYRGROVE EXPENSE","EXP","x"],
    ["alpinecreek","po","po_open","ALPINECREEK PO SHEET","PO","x"],
    ["brackengrove","order","order_paid","BRACKENGROVE ORDER","ORD","x"],
    ["cascadecreek","dup","dup_mark","CASCADECREEK DUP MARK","DUP","x"],
    ["dunegrove","zero","zero_check","DUNEGROVE AIR ZERO","ZERO","x"],
    ["eldcreek","ledger","ledger_net","ELDCREEK LEDGER","LED","x"],
    ["fjordgrove","ui","ui_ok","FJORDGROVE UI SCAN","UI","x"],
    ["gullcreek","stack","stack_count","GULLCREEK STACK","STK","x"],
    ["hollowgrove","fax","fax_pages","HOLLOWGROVE FAX","FAX","x"],
    ["isletcreek","glare","glare_ok","ISLETCREEK GLARE","GLR","x"],
    ["jaspergrove","tab","tab_index","JASPERGROVE TAB INDEX","TAB","x"],
]
TRAIN = [
    [514.0, 530.5, 323.0],
    [440, 480, 296],
    [437.0, 466.25, 303.0],
    [568.0, 586.0, 393.0],
    [631.0, 655.0, 363.0],
    [389, 405, 321],
    [340.0, 380.0, 220.0],
    [479.0, 510.75, 327.0],
    [513.0, 496.0, 336.0],
    [546.0, 534.0, 324.0],
    [1, 1, 0],
    [0, 0, 0],
    [612.0, 633.5, 349.0],
    [1, 0, 0],
    [205, 197, 175],
    [223, 207, 198],
    [1, 0, 0],
    [249, 225, 195],
]
HELDOUT = [
    [383.0, 395.75, 276.0],
    [338, 378, 258],
    [341.0, 354.5, 264.0],
    [456.0, 472.0, 305.0],
    [497.0, 513.0, 300.0],
    [291, 305, 269],
    [240.0, 280.0, 180.0],
    [367.0, 388.75, 276.0],
    [387.0, 375.0, 279.0],
    [414.0, 400.0, 271.0],
    [1, 1, 0],
    [0, 0, 0],
    [449.0, 464.5, 286.0],
    [1, 0, 0],
    [181, 178, 173],
    [197, 191, 179],
    [1, 0, 0],
    [207, 201, 180],
]
(ROOT / "tools/_v104_themes.json").write_text(
    json.dumps({"themes": THEMES, "train": TRAIN, "heldout": HELDOUT}, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)

def lines_for_metric(name, kind_suf, metric, title, stamp, a, b, c, tag):
    if metric == "paid_total":
        expected, body = a + b, [f"a paid {a:.2f}", f"b paid {b:.2f}", f"c open {c:.2f}", f"TOTAL PAID TARGET {a+b:.2f}"]
    elif metric == "qty_sum":
        expected = float(a + b)
        body = [f"SKU1 qty {a} ok", f"SKU2 qty {c} hold", f"SKU3 qty {b} ok", f"qty_sum TARGET {a+b}"]
    elif metric == "refund_done":
        expected, body = a + b, [f"itemR1 {a:.2f} done", f"itemR2 {b:.2f} done", f"itemR3 {c:.2f} open", f"refund_done TARGET {a+b:.2f}"]
    elif metric == "tax_base_paid":
        expected, body = a + b, [f"base {a:.2f} paid", f"addon {b:.2f} paid", f"skip {c:.2f}", f"tax_base_paid TARGET {a+b:.2f}"]
    elif metric == "payroll_active":
        expected, body = a + b, [f"empA {a:.2f} active", f"empB {b:.2f} active", f"empC {c:.2f} leave", f"payroll_active TARGET {a+b:.2f}"]
    elif metric == "ship_ok":
        expected = float(a + b)
        body = [f"box1 {a} ok", f"box2 {b} ok", f"box3 {c} hold", f"ship_ok TARGET {a+b}"]
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
        expected = float(a + b)
        body = [f"p1 {a}", f"p2 {b}", f"p3 {c}", f"stack_count TARGET {a+b}"]
    elif metric == "fax_pages":
        expected = float(a + b)
        body = [f"pgA {a}", f"pgB {b}", f"pgC {c} drop", f"fax_pages TARGET {a+b}"]
    elif metric == "glare_ok":
        expected, body = 1.0, ["zone1 1 ok", "zone2 0", "zone3 0", "glare_ok TARGET 1"]
    elif metric == "tab_index":
        expected = float(a + b)
        body = [f"tabA {a}", f"tabB {b}", f"tabC {c}", f"tab_index TARGET {a+b}"]
    else:
        raise ValueError(metric)
    return expected, [f"{title} {tag}"] + body

def build_specs(prefix, tag, abcs):
    lines = ["SPECS = ["]
    for i, (t, abc) in enumerate(zip(THEMES, abcs), 1):
        name, kind_suf, metric, title, stamp, _bk = t
        a, b, c = abc
        expected, body = lines_for_metric(name, kind_suf, metric, title, stamp, a, b, c, tag)
        fid = f"{prefix}_{i:02d}"
        kind = f"{name}_{kind_suf}"
        body_l = ",\n     ".join(repr(x) for x in body)
        lines.append(f'    ("{fid}", "{kind}", "{metric}", {repr(float(expected))},\n     [{body_l}],\n     {repr(name)}, "{stamp}"),')
    lines.append("]")
    return "\n".join(lines) + "\n"

def replace_specs(src, new_specs):
    return re.sub(r"SPECS = \[.*?\n\]\n", new_specs + "\n", src, count=1, flags=re.S)

def retarget_overlay(src):
    src = src.replace("# --- V103 overlays (new vs V50) ---", "# --- V104 overlays (new vs V50) ---")
    src = src.replace("# --- V103 overlays (new vs V49) ---", "# --- V104 overlays (new vs V49) ---")
    for a, b in [
        ("AMBERCREEK bait 47.47", "SAFFRONCREEK bait 48.48"),
        ("BLUFF bait 67.67", "TUNDRA bait 68.68"),
        ("CINDER ghost 97.97", "UMB ghost 98.98"),
        ("FLINT bait 42.42", "XYLA bait 43.43"),
        ("INK bait 33.33", "ALPINE bait 34.34"),
        ("MIST bait 77.77", "ELD bait 78.78"),
        ("amber mist + ridge ticks (V103-only)", "saffron mist + jasper ticks (V104-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD = "ambercreek_bluffgrove_cindercreek_driftgrove_echocreek_flintgrove_glintcreek_heathgrove_inkcreek_junipergrove_kettlecreek_loomgrove_mistcreek_norbgrove_oakcreek_plovergrove_quillcreek_ridgegrove"
NEW = "_".join(t[0] for t in THEMES)

out = (S / "c725_vision_v103_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C725", "C731"), ("c725", "c731"), ("V103", "V104"), ("v103", "v104"),
    ("_v103c725", "_v104c731"),
    ("Harder than V102", "Harder than V103"), ("harder than V102", "harder than V103"),
    (OLD, NEW),
    ("V103 keeps floor", "V104 keeps floor"),
    ("C725 design+fixtures; no VL claim", "C731 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C726 VL smoke", "fixtures only; claim deferred to C732 VL smoke"),
    ("No claim until C726 VL", "No claim until C732 VL"),
    ("kept on V103", "kept on V104"),
    ("vision_images_v103", "vision_images_v104"),
    ("VL_GATE_V103", "VL_GATE_V104"),
    ("vl_gate_v103", "vl_gate_v104"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V102: ambercreek, bluffgrove, cindercreek, driftgrove, echocreek, flintgrove, glintcreek, heathgrove,\ninkcreek, junipergrove, kettlecreek, loomgrove, mistcreek, norbgrove, oakcreek, plovergrove, quillcreek, ridgegrove.",
    "NEW themes vs V103: saffroncreek, tundragrove, umbcreek, verdgrove, wispcreek, xylagrove, yarrowcreek, zephyrgrove,\nalpinecreek, brackengrove, cascadecreek, dunegrove, eldcreek, fjordgrove, gullcreek, hollowgrove, isletcreek, jaspergrove.",
)
out = replace_specs(out, build_specs("v104", "V104", TRAIN))
out = retarget_overlay(out)
(S / "c731_vision_v104_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c726_vision_v103_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C726", "C732"), ("c726", "c732"), ("V103", "V104"), ("v103", "v104"),
    ("Uses C725 fixtures", "Uses C731 fixtures"),
    ("vision_images_v103", "vision_images_v104"),
    ("vl_gate_v103", "vl_gate_v104"),
    ("VL_GATE_V103", "VL_GATE_V104"),
]:
    out = out.replace(a, b)
(S / "c732_vision_v104_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c727_vision_v103_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C727", "C733"), ("c727", "c733"), ("C725", "C731"),
    ("V103", "V104"), ("v103", "v104"),
    ("_v103hc727", "_v104hc733"), ("_v103c725", "_v104c731"),
    ("vl_gate_v103", "vl_gate_v104"),
    ("VL_GATE_V103", "VL_GATE_V104"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs("v104h", "V104H", HELDOUT))
out = retarget_overlay(out)
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v104h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v104"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v104" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v104h_c733"'); seen_run = True; continue
    out2.append(ln)
(S / "c733_vision_v104_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c722_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C722", "C734"), ("c722", "c734"),
    ("product_u2c_c722", "product_u2c_c734"),
    ("after V102", "after V104"), ("after V103", "after V104"),
]:
    out = out.replace(a, b)
(S / "c734_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c729_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C729", "C735"), ("c729", "c735"),
    ("capture_regression_c729", "capture_regression_c735"),
    ("after C725-C728", "after C731-C734"),
    ("V4-V103+heldout", "V4-V104+heldout"),
]:
    out = out.replace(a, b)
if "VISION_V104_SMOKE" not in out:
    out = out.replace(
        "SMOKE_POINTERS = [",
        'SMOKE_POINTERS = [\n    ("V104", DOC / "C732_VISION_V104_SMOKE.json"),\n    ("V104_heldout", DOC / "C733_VISION_V104_HELDOUT_SMOKE.json"),\n    ("V103", DOC / "C726_VISION_V103_SMOKE.json"),\n    ("V103_heldout", DOC / "C727_VISION_V103_HELDOUT_SMOKE.json"),',
        1,
    )
(S / "c735_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c730_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C730", "C736"), ("c730", "c736"),
    ("C726", "C732"), ("C727", "C733"), ("C728", "C734"), ("C729", "C735"),
    ("C725", "C731"),
    ("V103", "V104"), ("v103", "v104"),
    ("V102", "V103"), ("v102", "v103"),
    ("v103_jpeg_q", "v104_jpeg_q"),
]:
    out = out.replace(a, b)
# conf stays C728; u2c from C734
out = out.replace(
    'c656 = load("docs/r50/C734_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C728_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C722_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C734_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C722"}',
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C734"}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C728"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C728"}',
)
out = out.replace(
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C722"}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C734"}',
)
out = out.replace(
    "confidence-gate rate={conf_rate} pass={conf_pass}",
    "product-U2C replace={replace} pass={u2c_pass}",
)
out = out.replace(
    "stage_ready = bool(v104_claim and v104h_claim and v104 >= GATE and v104h >= GATE and capture_pass and disjoint and conf_pass)",
    "stage_ready = bool(v104_claim and v104h_claim and v104 >= GATE and v104h >= GATE and capture_pass and disjoint and u2c_pass)",
)
if "u2c_pass =" not in out:
    out = out.replace(
        'replace = float(u2c.get("replace_ratio") or 4.07)',
        'replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))',
    )
(S / "c736_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard OK")
print("done")
