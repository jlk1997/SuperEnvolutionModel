# -*- coding: utf-8 -*-
"""Bootstrap C320-C325 Vision V36 from V35 + dissolve NV."""
from __future__ import annotations
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCR = ROOT / "scripts"

KINDS = [
    ("teak_recv", "paid_total", "TEAK GRAIN RECV V36", "柚木收款单", "RECV"),
    ("marble_wh", "qty_sum", "WH MARBLE TILE V36", "大理石仓位单", "RECV"),
    ("canvas_refund", "refund_done", "CANVAS PATCH REFUND V36", "帆布补丁退款单", "DONE"),
    ("cobalt_tax", "tax_base_paid", "COBALT TAX SLIP V36", "钴蓝税基单", "TAX"),
    ("mica_pay", "payroll_active", "MICA PAYROLL V36", "云母工资单", "PAY"),
    ("clasp_ship", "ship_ok", "CLASP SHIP DOCK V36", "搭扣出货单", "SHIP"),
    ("garnet_sla", "sla_ok_hours", "GARNET SLA CARD V36", "石榴石SLA卡", "SLA"),
    ("flint_exp", "exp_sum", "FLINT EXPENSE V36", "燧石费用单", "EXP"),
    ("steel_po", "po_open", "STEEL PO SHEET V36", "钢材采购单", "PO"),
    ("kraft_order", "order_paid", "KRAFT ORDER V36", "牛皮纸订单", "ORD"),
    ("flannel_dup", "dup_mark", "FLANNEL DUP MARK V36", "法兰绒重复标记", "DUP"),
    ("empty_zero", "zero_check", "EMPTY VOID ZERO V36", "空值清零单", "ZERO"),
    ("jute_ledger", "ledger_net", "JUTE LEDGER V36", "黄麻账本", "LED"),
    ("glaze_ui", "ui_ok", "GLAZE UI SCAN V36", "釉面界面扫描", "UI"),
    ("sisal_stack", "stack_count", "SISAL STACK V36", "剑麻堆叠单", "STK"),
    ("aubergine_fax", "fax_pages", "AUBERGINE FAX V36", "茄紫传真单", "FAX"),
    ("titanium_glare", "glare_ok", "TITANIUM GLARE V36", "钛光眩光单", "GLR"),
    ("dossier_tab", "tab_index", "DOSSIER TAB INDEX V36", "档案页签索引", "TAB"),
]

TRAIN_NUMS = [
    (134.25, [64.00, 70.25, 19.00]),
    (97.0, [41, 28, 47]),
    (71.5, [34.00, 37.50, 15.00]),
    (201.0, [96.00, 105.00, 42.00]),
    (268.0, [130.00, 138.00, 35.00]),
    (63.0, [31, 17, 22]),
    (81.25, [44.00, 37.25, 20.00]),
    (108.5, [52.00, 56.50, 24.00]),
    (122.0, [66.00, 56.00, 28.00]),
    (147.75, [78.00, 69.75, 21.00]),
    (2.0, [1, 1, 0]),
    (0.0, [0.00, 0.00, 0.00]),
    (231.5, [112.00, 119.50, 36.00]),
    (1.0, [1, 0, 0]),
    (11.0, [5, 4, 2]),
    (16.0, [8, 8, 3]),
    (1.0, [1, 0, 0]),
    (21.0, [12, 9, 2]),
]
HELD_NUMS = [
    (76.5, [36.00, 40.50, 14.00]),
    (54.0, [24, 12, 30]),
    (42.25, [20.00, 22.25, 9.00]),
    (108.0, [52.00, 56.00, 24.00]),
    (142.0, [70.00, 72.00, 20.00]),
    (35.0, [18, 9, 14]),
    (46.5, [25.00, 21.50, 11.00]),
    (58.75, [27.00, 31.75, 13.00]),
    (67.0, [36.00, 31.00, 15.00]),
    (82.25, [44.00, 38.25, 12.00]),
    (2.0, [1, 1, 0]),
    (0.0, [0.00, 0.00, 0.00]),
    (126.5, [60.00, 66.50, 20.00]),
    (1.0, [1, 0, 0]),
    (6.0, [3, 2, 1]),
    (9.0, [5, 4, 2]),
    (1.0, [1, 0, 0]),
    (12.0, [7, 5, 1]),
]

def build_lines(i, tag, expected, nums):
    kind, metric, title, cn, stamp = KINDS[i]
    a, b, c = nums
    if metric == "paid_total":
        lines = [title, f"a paid {a:.2f}", f"b paid {b:.2f}", f"c open {c:.2f}", f"TOTAL PAID TARGET {expected:.2f}"]
    elif metric == "qty_sum":
        lines = [title, f"SKU1 qty {int(a)} ok", f"SKU2 qty {int(b)} hold", f"SKU3 qty {int(c)} ok", f"qty_sum TARGET {int(expected)}"]
    elif metric == "refund_done":
        lines = [title, f"itemR1 {a:.2f} done", f"itemR2 {b:.2f} done", f"itemR3 {c:.2f} open", f"refund_done TARGET {expected:.2f}"]
    elif metric == "tax_base_paid":
        lines = [title, f"base {a:.2f} paid", f"addon {b:.2f} paid", f"skip {c:.2f}", f"tax_base_paid TARGET {expected:.2f}"]
    elif metric == "payroll_active":
        lines = [title, f"empA {a:.2f} active", f"empB {b:.2f} active", f"empC {c:.2f} leave", f"payroll_active TARGET {expected:.2f}"]
    elif metric == "ship_ok":
        lines = [title, f"box1 {int(a)} ok", f"box2 {int(b)} ok", f"box3 {int(c)} hold", f"ship_ok TARGET {int(expected)}"]
    elif metric == "sla_ok_hours":
        lines = [title, f"job1 {a:.2f}h ok", f"job2 {b:.2f}h ok", f"job3 {c:.2f}h late", f"sla_ok_hours TARGET {expected:.2f}"]
    elif metric == "exp_sum":
        lines = [title, f"e1 {a:.2f}", f"e2 {b:.2f}", f"e3 {c:.2f} void", f"exp_sum TARGET {expected:.2f}"]
    elif metric == "po_open":
        lines = [title, f"line1 {a:.2f} open", f"line2 {b:.2f} open", f"line3 {c:.2f} closed", f"po_open TARGET {expected:.2f}"]
    elif metric == "order_paid":
        lines = [title, f"skuA {a:.2f} paid", f"skuB {b:.2f} paid", f"skuC {c:.2f} due", f"order_paid TARGET {expected:.2f}"]
    elif metric == "dup_mark":
        lines = [title, f"markA {int(a)}", f"markB {int(b)}", f"markC {int(c)}", f"dup_mark TARGET {int(expected)}"]
    elif metric == "zero_check":
        lines = [title, f"z1 {a:.2f}", f"z2 {b:.2f}", f"z3 {c:.2f}", f"zero_check TARGET {expected:.2f}"]
    elif metric == "ledger_net":
        lines = [title, f"dr {a:.2f}", f"cr {b:.2f}", f"adj {c:.2f}", f"ledger_net TARGET {expected:.2f}"]
    elif metric == "ui_ok":
        lines = [title, f"btnOK {int(a)}", f"btnSkip {int(b)}", f"btnBad {int(c)}", f"ui_ok TARGET {int(expected)}"]
    elif metric == "stack_count":
        lines = [title, f"p1 {int(a)}", f"p2 {int(b)}", f"p3 {int(c)}", f"stack_count TARGET {int(expected)}"]
    elif metric == "fax_pages":
        lines = [title, f"pgA {int(a)}", f"pgB {int(b)}", f"pgC {int(c)} drop", f"fax_pages TARGET {int(expected)}"]
    elif metric == "glare_ok":
        lines = [title, f"zone1 {int(a)} ok", f"zone2 {int(b)}", f"zone3 {int(c)}", f"glare_ok TARGET {int(expected)}"]
    else:
        lines = [title, f"tabA {int(a)}", f"tabB {int(b)}", f"tabC {int(c)}", f"tab_index TARGET {int(expected)}"]
    return {
        "id": f"v36{tag}_{i+1:02d}",
        "kind": kind,
        "metric": metric,
        "expected": float(expected),
        "lines": lines,
        "cn": cn if not tag else cn + "H",
        "stamp": stamp,
    }

def specs_to_tuples(specs):
    rows = []
    for s in specs:
        rows.append(
            f'    ("{s["id"]}", "{s["kind"]}", "{s["metric"]}", {s["expected"]},\n'
            f'     {json.dumps(s["lines"], ensure_ascii=False)},\n'
            f'     {json.dumps(s["cn"], ensure_ascii=False)}, {json.dumps(s["stamp"])}),'
        )
    return "SPECS = [\n" + "\n".join(rows) + "\n]"

train = [build_lines(i, "", TRAIN_NUMS[i][0], TRAIN_NUMS[i][1]) for i in range(18)]
held = [build_lines(i, "h", HELD_NUMS[i][0], HELD_NUMS[i][1]) for i in range(18)]
for i, s in enumerate(train):
    s["id"] = f"v36_{i+1:02d}"
for i, s in enumerate(held):
    s["id"] = f"v36h_{i+1:02d}"

SPEC_PATH = ROOT / "tools" / "_v36_specs.json"
SPEC_PATH.write_text(json.dumps({"train": train, "held": held}, ensure_ascii=False, indent=2), encoding="utf-8")
print("wrote", SPEC_PATH)

V36_OVERLAY = r'''
    # --- V36 overlays (new vs V35) ---
    for _ in range(90):
        bx = rng.randint(60, 520)
        by = rng.randint(340, 570)
        if in_text_band(by):
            continue
        d.line([(bx, by), (bx + rng.randint(8, 22), by + rng.randint(-2, 2))], fill=(90, 110, 140), width=1)
    for gi in range(7):
        d.ellipse([30 + gi * 20, 300, 46 + gi * 20, 316], outline=(40, 90, 120), width=2)
    d.text((30, 318), "TEAK bait 36.36", fill=(80, 50, 20), font=f_tiny)
    for hi in range(4):
        d.polygon([(580 + hi * 32, 40), (604 + hi * 32, 40), (592 + hi * 32, 72)], fill=(40, 80, 160))
    d.text((580, 76), "COBALT bait 48.48", fill=(20, 40, 100), font=f_tiny)
    d.rectangle([240, 370, 400, 430], fill=(235, 245, 255))
    d.text((250, 390), "MICA ghost 88.88", fill=(60, 90, 110), font=f_pen)
    d.arc([400, 360, 490, 430], 20, 220, fill=(120, 40, 60), width=3)
    d.text((400, 435), "GARNET bait 27.27", fill=(100, 20, 40), font=f_tiny)
    d.ellipse([60, 460, 130, 520], fill=(180, 160, 90), outline=(120, 100, 40), width=2)
    d.text((60, 525), "FLINT bait 19.19", fill=(90, 70, 30), font=f_tiny)
    for qi in range(4):
        d.rectangle([240 + qi * 40, 460, 270 + qi * 40, 490], outline=(70, 90, 110), width=2)
    d.rectangle([850, 110, 990, 170], fill=(140, 150, 160), outline=(50, 60, 70), width=2)
    d.text((870, 128), "STEEL", fill=(20, 25, 30), font=f_stamp)
    d.polygon([(40, 8), (400, 8), (385, 22), (50, 22)], fill=(210, 200, 180), outline=(90, 70, 50), width=1)
    d.text((60, 9), "TITANIUM bait 63.63", fill=(50, 55, 60), font=f_tiny)
    for ti, ty in enumerate((90, 150, 210)):
        d.polygon([(1000, ty), (1024, ty + 12), (1000, ty + 24)], fill=(100, 60, 140 + ti * 15))
'''

THEMES = "teak/marble/canvas/cobalt/mica/clasp/garnet/flint/steel/kraft/flannel/empty/jute/glaze/sisal/aubergine/titanium/dossier"
OLD_THEMES = "jade/granite/suede/bronze/opal/hinge/citrine/basalt/pewter/vellum/fleece/null/burlap/porcelain/twine/mulberry/nickel/folio"

def inject_overlay(text: str) -> str:
    soft = "    img.save(buf"
    text2 = re.sub(r"\n    # --- V35 overlays.*?\n(?=    img\.save\(buf)", "\n", text, count=1, flags=re.S)
    if soft in text2 and "TEAK bait" not in text2:
        text2 = text2.replace(soft, V36_OVERLAY + "\n" + soft, 1)
    return text2

def xform_train(text, train_specs_src):
    reps = [
        ("C314", "C320"), ("c314", "c320"),
        ("vision_images_v35", "vision_images_v36"),
        ("vision_v35", "vision_v36"),
        ("VL_GATE_V35", "VL_GATE_V36"),
        ("vl_gate_v35", "vl_gate_v36"),
        ("vision_gate_v35", "vision_gate_v36"),
        ("r50plus_v35", "r50plus_v36"),
        ("SCAN DESK V35", "SCAN DESK V36"),
        ("V35 C314", "V36 C320"), ("V35 C320", "V36 C320"),
        ("V35 keeps floor", "V36 keeps floor"),
        ("jade_recv", "teak_recv"),
        ("JADE bait", "TEAK bait"),
    ]
    for a, b in reps:
        text = text.replace(a, b)
    pat = re.compile(r"SPECS = \[\s*\(\s*\"v3[56]_01\".*?^\]", re.S | re.M)
    m = pat.search(text)
    if not m:
        pat = re.compile(r"SPECS = \[.*?\n\]", re.S)
        m = pat.search(text)
    if m:
        text = text[:m.start()] + train_specs_src + text[m.end():]
    return inject_overlay(text)

def xform_smoke(text):
    for a, b in [
        ("C315", "C321"), ("c315", "c321"),
        ("vision_images_v35", "vision_images_v36"),
        ("vision_v35_c315", "vision_v36_c321"),
        ("vision_v35", "vision_v36"),
        ("VL_GATE_V35", "VL_GATE_V36"),
        ("vl_gate_v35", "vl_gate_v36"),
        ("r50plus_v35", "r50plus_v36"),
        ("C315_VISION_V35", "C321_VISION_V36"),
        ("C315b_VISION_GATE_V35", "C321b_VISION_GATE_V36"),
        ("VISION_V35_SMOKE", "VISION_V36_SMOKE"),
        ("VISION_GATE_V35_CLAIM", "VISION_GATE_V36_CLAIM"),
    ]:
        text = text.replace(a, b)
    return text

def xform_heldout(text, held_specs_src):
    for a, b in [
        ("C316", "C322"), ("c316", "c322"),
        ("vision_images_v35h", "vision_images_v36h"),
        ("vision_images_v35", "vision_images_v36"),
        ("vision_v35h_c316", "vision_v36h_c322"),
        ("VL_GATE_V35_HELDOUT", "VL_GATE_V36_HELDOUT"),
        ("vl_gate_v35_heldout", "vl_gate_v36_heldout"),
        ("vision_gate_v35_heldout", "vision_gate_v36_heldout"),
        ("r50plus_v35_heldout", "r50plus_v36_heldout"),
        ("vision_v35_heldout", "vision_v36_heldout"),
        ("SCAN DESK V35H", "SCAN DESK V36H"),
        ("V35H C316", "V36H C322"), ("V35H C322", "V36H C322"),
        ("VISION_V35_HELDOUT", "VISION_V36_HELDOUT"),
        ("VISION_GATE_V35_HELDOUT", "VISION_GATE_V36_HELDOUT"),
        ("_v35hc316", "_v36hc322"),
        ('"version": "v35h"', '"version": "v36h"'),
    ]:
        text = text.replace(a, b)
    pat = re.compile(r"SPECS = \[\s*\(\s*\"v3[56]h_01\".*?^\]", re.S | re.M)
    m = pat.search(text)
    if not m:
        pat = re.compile(r"SPECS = \[.*?\n\]", re.S)
        m = pat.search(text)
    if m:
        text = text[:m.start()] + held_specs_src + text[m.end():]
    return text

def xform_nv(text):
    text = text.replace("C311", "C323").replace("c311", "c323")
    text = text.replace("dissolve_cost_shadow_c311", "dissolve_cost_shadow_c323")
    text = text.replace("C311_DISSOLVE_COST_SHADOW.json", "C323_DISSOLVE_COST_SHADOW.json")
    return text

def xform_reg(text):
    text = text.replace("C318", "C324").replace("c318", "c324")
    text = text.replace("C314-C317", "C320-C323")
    text = text.replace("c314_c317", "c320_c323")
    text = text.replace("capture_regression_c318", "capture_regression_c324")
    needle = '("V35_heldout", DOC / "C316_VISION_V35_HELDOUT_SMOKE.json"),'
    if needle in text and '("V36"' not in text:
        text = text.replace(
            needle,
            needle
            + '\n    ("V36", DOC / "C321_VISION_V36_SMOKE.json"),'
            + '\n    ("V36_heldout", DOC / "C322_VISION_V36_HELDOUT_SMOKE.json"),',
        )
    needle2 = '("C317_product_u2c_cost", DOC / "C317_PRODUCT_U2C_COST.json"),'
    if needle2 in text and "C323_dissolve" not in text:
        text = text.replace(
            needle2,
            needle2
            + '\n    ("C323_dissolve_cost_shadow", DOC / "C323_DISSOLVE_COST_SHADOW.json"),',
        )
    text = text.replace(
        '"V35", "V35_heldout", "C233_clarity_floor", "C317_product_u2c_cost"]',
        '"V35", "V35_heldout", "V36", "V36_heldout", "C233_clarity_floor", "C323_dissolve_cost_shadow"]',
    )
    text = text.replace('DOC / "C318_CAPTURE_OFFICE_REGRESSION.json"', 'DOC / "C324_CAPTURE_OFFICE_REGRESSION.json"')
    return text

def xform_score(text):
    text = text.replace("C319", "C325").replace("c319", "c325")
    text = text.replace("c314_c318", "c320_c324")
    text = text.replace("STAGE_ANT_C319.md", "STAGE_ANT_C325.md")
    text = text.replace("C314-C318", "C320-C324")
    text = text.replace("C314-C319", "C320-C325")
    text = text.replace("unified_scorecard_c314_c318", "unified_scorecard_c320_c324")
    text = text.replace("unified_scorecard_c314_c319", "unified_scorecard_c320_c325")
    text = text.replace("C314_VISION_V35_DESIGN", "C320_VISION_V36_DESIGN")
    text = text.replace("C315_VISION_V35_SMOKE", "C321_VISION_V36_SMOKE")
    text = text.replace("C315b_VISION_GATE_V35_CLAIM", "C321b_VISION_GATE_V36_CLAIM")
    text = text.replace("C316_VISION_V35_HELDOUT_SMOKE", "C322_VISION_V36_HELDOUT_SMOKE")
    text = text.replace("C316b_VISION_GATE_V35_HELDOUT_CLAIM", "C322b_VISION_GATE_V36_HELDOUT_CLAIM")
    text = text.replace("C318_CAPTURE_OFFICE_REGRESSION", "C324_CAPTURE_OFFICE_REGRESSION")
    text = text.replace("vl_gate_v35", "vl_gate_v36")
    text = text.replace("v35_claim", "v36_claim").replace("v35h_claim", "v36h_claim")
    text = text.replace("v35 =", "v36 =").replace("v35h =", "v36h =")
    text = text.replace("max(v35, v35h", "max(v36, v36h")
    text = text.replace('"v35_design"', '"v36_design"')
    text = text.replace('"v35_smoke"', '"v36_smoke"')
    text = text.replace('"v35_heldout"', '"v36_heldout"')
    text = text.replace(OLD_THEMES, THEMES)
    text = text.replace("jade/granite/suede/bronze/...", "teak/marble/canvas/cobalt/...")
    text = text.replace("product/u2c/cost", "dissolve/cost/shadow")
    text = text.replace("product/u2c", "dissolve/shadow")
    text = text.replace('c269 = load("docs/r50/C317_PRODUCT_U2C_COST.json")', 'c269 = load("docs/r50/C323_DISSOLVE_COST_SHADOW.json")')
    text = text.replace('c311 = load("docs/r50/C311_DISSOLVE_COST_SHADOW.json")', 'c311 = load("docs/r50/C323_DISSOLVE_COST_SHADOW.json")')
    text = text.replace('"source": "C317"', '"source": "C323"')
    text = text.replace('"product_u2c_cost"', '"dissolve_cost_shadow"')
    return text

def main():
    train_src = specs_to_tuples(train)
    held_src = specs_to_tuples(held)
    mapping = [
        ("c314_vision_v35_design_and_batch.py", "c320_vision_v36_design_and_batch.py", lambda t: xform_train(t, train_src)),
        ("c315_vision_v35_smoke.py", "c321_vision_v36_smoke.py", xform_smoke),
        ("c316_vision_v35_heldout.py", "c322_vision_v36_heldout.py", lambda t: xform_heldout(t, held_src)),
        ("c311_dissolve_cost_shadow.py", "c323_dissolve_cost_shadow.py", xform_nv),
        ("c318_capture_office_regression.py", "c324_capture_office_regression.py", xform_reg),
        ("c319_scorecard_and_stage.py", "c325_scorecard_and_stage.py", xform_score),
    ]
    for src, dst, fn in mapping:
        t = (SCR / src).read_text(encoding="utf-8")
        out = fn(t)
        (SCR / dst).write_text(out, encoding="utf-8")
        print("wrote", dst, len(out.encode("utf-8")))
    d = (SCR / "c320_vision_v36_design_and_batch.py").read_text(encoding="utf-8")
    assert "vision_images_v36" in d and "v36_01" in d
    assert "TEAK bait" in d
    assert "teak_recv" in d
    assert "JPEG_Q = 60" in d
    s = (SCR / "c325_scorecard_and_stage.py").read_text(encoding="utf-8")
    assert "STAGE_ANT_C325.md" in s
    assert "C321_VISION_V36_SMOKE" in s
    print("ok")

if __name__ == "__main__":
    main()
