# -*- coding: utf-8 -*-
"""Bootstrap C332-C337 Vision V38 from V37 + product U2C NV."""
from __future__ import annotations
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCR = ROOT / "scripts"

KINDS = [
    ("cedar_recv", "paid_total", "CEDAR GRAIN RECV V38", "柏木收款单", "RECV"),
    ("jasper_wh", "qty_sum", "WH JASPER TILE V38", "碧玉仓位单", "RECV"),
    ("gauze_refund", "refund_done", "GAUZE PATCH REFUND V38", "纱布补丁退款单", "DONE"),
    ("cyan_tax", "tax_base_paid", "CYAN TAX SLIP V38", "青空税基单", "TAX"),
    ("feldspar_pay", "payroll_active", "FELDSPAR PAYROLL V38", "长石薪资单", "PAY"),
    ("hinge_ship", "ship_ok", "HINGE SHIP DOCK V38", "铰链出库单", "SHIP"),
    ("citrine_sla", "sla_ok_hours", "CITRINE SLA CARD V38", "黄水晶SLA卡", "SLA"),
    ("basalt_exp", "exp_sum", "BASALT EXPENSE V38", "玄武岩费用单", "EXP"),
    ("pewter_po", "po_open", "PEWTER PO SHEET V38", "白镴采购单", "PO"),
    ("parchment_order", "order_paid", "PARCHMENT ORDER V38", "羊皮纸订单", "ORD"),
    ("herringbone_dup", "dup_mark", "HERRINGBONE DUP MARK V38", "鱼骨纹重复标", "DUP"),
    ("nil_zero", "zero_check", "NIL VOID ZERO V38", "空值零检单", "ZERO"),
    ("burlap_ledger", "ledger_net", "BURLAP LEDGER V38", "麻布账本", "LED"),
    ("lacquer_ui", "ui_ok", "LACQUER UI SCAN V38", "漆面界面扫描", "UI"),
    ("coir_stack", "stack_count", "COIR STACK V38", "棕丝堆叠单", "STK"),
    ("mulberry_fax", "fax_pages", "MULBERRY FAX V38", "桑档传真单", "FAX"),
    ("iridium_glare", "glare_ok", "IRIDIUM GLARE V38", "铱光眩光单", "GLR"),
    ("folio_tab", "tab_index", "FOLIO TAB INDEX V38", "简册页签索引", "TAB"),
]

TRAIN_NUMS = [
    (127.5, [61.00, 66.50, 19.00]),
    (94.0, [36, 31, 44]),
    (71.25, [34.00, 37.25, 14.00]),
    (188.0, [91.00, 97.00, 41.00]),
    (256.0, [126.00, 130.00, 34.00]),
    (63.0, [29, 17, 21]),
    (81.5, [43.00, 38.50, 20.00]),
    (107.75, [51.00, 56.75, 24.00]),
    (121.0, [65.00, 56.00, 28.00]),
    (146.5, [78.00, 68.50, 21.00]),
    (2.0, [1, 1, 0]),
    (0.0, [0.00, 0.00, 0.00]),
    (221.25, [108.00, 113.25, 36.00]),
    (1.0, [1, 0, 0]),
    (11.0, [5, 4, 2]),
    (16.0, [8, 8, 3]),
    (1.0, [1, 0, 0]),
    (21.0, [12, 9, 2]),
]
HELD_NUMS = [
    (74.75, [36.00, 38.75, 15.00]),
    (53.0, [23, 12, 30]),
    (42.5, [20.00, 22.50, 9.00]),
    (104.0, [51.00, 53.00, 24.00]),
    (138.0, [69.00, 69.00, 19.00]),
    (35.0, [17, 9, 13]),
    (45.25, [24.00, 21.25, 11.00]),
    (58.5, [28.00, 30.50, 13.00]),
    (66.0, [35.00, 31.00, 15.00]),
    (81.25, [43.00, 38.25, 12.00]),
    (2.0, [1, 1, 0]),
    (0.0, [0.00, 0.00, 0.00]),
    (123.75, [59.00, 64.75, 19.00]),
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
        "id": f"v38{tag}_{i+1:02d}",
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
    s["id"] = f"v38_{i+1:02d}"
for i, s in enumerate(held):
    s["id"] = f"v38h_{i+1:02d}"

SPEC_PATH = ROOT / "tools" / "_v38_specs.json"
SPEC_PATH.write_text(json.dumps({"train": train, "held": held}, ensure_ascii=False, indent=2), encoding="utf-8")
print("wrote", SPEC_PATH)

V38_OVERLAY = r'''
    # --- V38 overlays (new vs V37) ---
    for _ in range(100):
        bx = rng.randint(50, 540)
        by = rng.randint(350, 580)
        if in_text_band(by):
            continue
        d.line([(bx, by), (bx + rng.randint(5, 22), by + rng.randint(-4, 4))], fill=(90, 70, 40), width=1)
    for gi in range(5):
        d.ellipse([48 + gi * 24, 308, 66 + gi * 24, 326], outline=(40, 90, 50), width=2)
    d.text((48, 328), "CEDAR bait 38.38", fill=(80, 50, 20), font=f_tiny)
    for hi in range(4):
        d.polygon([(580 + hi * 34, 36), (606 + hi * 34, 36), (593 + hi * 34, 72)], fill=(20, 90, 140))
    d.text((580, 76), "CYAN bait 58.58", fill=(10, 40, 80), font=f_tiny)
    d.rectangle([250, 380, 410, 440], fill=(245, 250, 255))
    d.text((260, 400), "FELDSPAR ghost 88.88", fill=(40, 70, 90), font=f_pen)
    d.arc([410, 370, 500, 440], 20, 240, fill=(160, 120, 20), width=3)
    d.text((410, 445), "CITRINE bait 33.33", fill=(130, 90, 10), font=f_tiny)
    d.ellipse([60, 470, 130, 530], fill=(90, 95, 100), outline=(40, 45, 50), width=2)
    d.text((60, 535), "BASALT bait 24.24", fill=(50, 55, 60), font=f_tiny)
    for qi in range(4):
        d.rectangle([250 + qi * 42, 470, 282 + qi * 42, 502], outline=(80, 70, 50), width=2)
    d.rectangle([850, 110, 1000, 170], fill=(170, 175, 180), outline=(50, 55, 60), width=2)
    d.text((870, 128), "PEWTER", fill=(20, 25, 30), font=f_stamp)
    d.polygon([(40, 4), (420, 4), (405, 18), (50, 18)], fill=(210, 200, 180), outline=(90, 70, 50), width=1)
    d.text((70, 5), "IRIDIUM bait 68.68", fill=(30, 35, 45), font=f_tiny)
    for ti, ty in enumerate((90, 150, 210)):
        d.polygon([(1000, ty), (1024, ty + 12), (1000, ty + 24)], fill=(70, 100, 60 + ti * 20))
'''

THEMES = "cedar/jasper/gauze/cyan/feldspar/hinge/citrine/basalt/pewter/parchment/herringbone/nil/burlap/lacquer/coir/mulberry/iridium/folio"
OLD_THEMES = "walnut/onyx/linen/indigo/quartz/latch/amber/shale/chrome/bond/tweed/void/hemp/enamel/raffia/plum/tungsten/binder"

def inject_overlay(text: str) -> str:
    soft = "    buf = io.BytesIO()"
    text2 = re.sub(r"\n    # --- V37 overlays.*?\n(?=    img\.save\(buf)", "\n", text, count=1, flags=re.S)
    if soft not in text2:
        soft = "    img.save(buf"
    if "CEDAR bait" not in text2 and soft in text2:
        text2 = text2.replace(soft, V38_OVERLAY + "\n" + soft, 1)
    return text2

def xform_train(text, train_specs_src):
    reps = [
        ("C326", "C332"), ("c326", "c332"),
        ("vision_images_v37", "vision_images_v38"),
        ("vision_v37", "vision_v38"),
        ("VL_GATE_V37", "VL_GATE_V38"),
        ("vl_gate_v37", "vl_gate_v38"),
        ("vision_gate_v37", "vision_gate_v38"),
        ("r50plus_v37", "r50plus_v38"),
        ("SCAN DESK V37", "SCAN DESK V38"),
        ("V37 C326", "V38 C332"), ("V37 C332", "V38 C332"),
        ("V37 keeps floor", "V38 keeps floor"),
        ("walnut_recv", "cedar_recv"),
        ("WALNUT bait", "CEDAR bait"),
    ]
    for a, b in reps:
        text = text.replace(a, b)
    pat = re.compile(r"SPECS = \[\s*\(\s*\"v3[78]_01\".*?^\]", re.S | re.M)
    m = pat.search(text)
    if not m:
        pat = re.compile(r"SPECS = \[.*?\n\]", re.S)
        m = pat.search(text)
    if m:
        text = text[:m.start()] + train_specs_src + text[m.end():]
    return inject_overlay(text)

def xform_smoke(text):
    for a, b in [
        ("C327", "C333"), ("c327", "c333"),
        ("vision_images_v37", "vision_images_v38"),
        ("vision_v37_c327", "vision_v38_c333"),
        ("vision_v37", "vision_v38"),
        ("VL_GATE_V37", "VL_GATE_V38"),
        ("vl_gate_v37", "vl_gate_v38"),
        ("r50plus_v37", "r50plus_v38"),
        ("C327_VISION_V37", "C333_VISION_V38"),
        ("C327b_VISION_GATE_V37", "C333b_VISION_GATE_V38"),
        ("VISION_V37_SMOKE", "VISION_V38_SMOKE"),
        ("VISION_GATE_V37_CLAIM", "VISION_GATE_V38_CLAIM"),
    ]:
        text = text.replace(a, b)
    return text

def xform_heldout(text, held_specs_src):
    for a, b in [
        ("C328", "C334"), ("c328", "c334"),
        ("vision_images_v37h", "vision_images_v38h"),
        ("vision_images_v37", "vision_images_v38"),
        ("vision_v37h_c328", "vision_v38h_c334"),
        ("VL_GATE_V37_HELDOUT", "VL_GATE_V38_HELDOUT"),
        ("vl_gate_v37_heldout", "vl_gate_v38_heldout"),
        ("vision_gate_v37_heldout", "vision_gate_v38_heldout"),
        ("r50plus_v37_heldout", "r50plus_v38_heldout"),
        ("vision_v37_heldout", "vision_v38_heldout"),
        ("SCAN DESK V37H", "SCAN DESK V38H"),
        ("V37H C328", "V38H C334"), ("V37H C334", "V38H C334"),
        ("VISION_V37_HELDOUT", "VISION_V38_HELDOUT"),
        ("VISION_GATE_V37_HELDOUT", "VISION_GATE_V38_HELDOUT"),
        ("_v37hc328", "_v38hc334"),
        ('"version": "v37h"', '"version": "v38h"'),
    ]:
        text = text.replace(a, b)
    pat = re.compile(r"SPECS = \[\s*\(\s*\"v3[78]h_01\".*?^\]", re.S | re.M)
    m = pat.search(text)
    if not m:
        pat = re.compile(r"SPECS = \[.*?\n\]", re.S)
        m = pat.search(text)
    if m:
        text = text[:m.start()] + held_specs_src + text[m.end():]
    return text

def xform_nv(text):
    text = text.replace("C317", "C335").replace("c317", "c335")
    text = text.replace("product_u2c_cost_c317", "product_u2c_cost_c335")
    text = text.replace("C317_PRODUCT_U2C_COST.json", "C335_PRODUCT_U2C_COST.json")
    return text

def xform_reg(text):
    text = text.replace("C330", "C336").replace("c330", "c336")
    text = text.replace("C326-C329", "C332-C335")
    text = text.replace("c326_c329", "c332_c335")
    text = text.replace("capture_regression_c330", "capture_regression_c336")
    needle = '("V37_heldout", DOC / "C328_VISION_V37_HELDOUT_SMOKE.json"),'
    if needle in text and '("V38"' not in text:
        text = text.replace(
            needle,
            needle
            + '\n    ("V38", DOC / "C333_VISION_V38_SMOKE.json"),'
            + '\n    ("V38_heldout", DOC / "C334_VISION_V38_HELDOUT_SMOKE.json"),',
        )
    needle2 = '("C329_confidence_gate_stretch", DOC / "C329_CONFIDENCE_GATE_STRETCH.json"),'
    if needle2 in text and "C335_product" not in text:
        text = text.replace(
            needle2,
            needle2
            + '\n    ("C335_product_u2c_cost", DOC / "C335_PRODUCT_U2C_COST.json"),',
        )
    text = text.replace(
        '"V37", "V37_heldout", "V38", "V38_heldout", "C233_clarity_floor", "C335_product_u2c_cost"]',
        '"V37", "V37_heldout", "V38", "V38_heldout", "C233_clarity_floor", "C335_product_u2c_cost"]',
    )
    text = text.replace('DOC / "C330_CAPTURE_OFFICE_REGRESSION.json"', 'DOC / "C336_CAPTURE_OFFICE_REGRESSION.json"')
    return text

def xform_score(text):
    text = text.replace("C331", "C337").replace("c331", "c337")
    text = text.replace("c326_c330", "c332_c336")
    text = text.replace("STAGE_ANT_C331.md", "STAGE_ANT_C337.md")
    text = text.replace("C326-C330", "C332-C336")
    text = text.replace("C326-C331", "C332-C337")
    text = text.replace("unified_scorecard_c326_c330", "unified_scorecard_c332_c336")
    text = text.replace("unified_scorecard_c326_c331", "unified_scorecard_c332_c337")
    text = text.replace("C326_VISION_V37_DESIGN", "C332_VISION_V38_DESIGN")
    text = text.replace("C327_VISION_V37_SMOKE", "C333_VISION_V38_SMOKE")
    text = text.replace("C327b_VISION_GATE_V37_CLAIM", "C333b_VISION_GATE_V38_CLAIM")
    text = text.replace("C328_VISION_V37_HELDOUT_SMOKE", "C334_VISION_V38_HELDOUT_SMOKE")
    text = text.replace("C328b_VISION_GATE_V37_HELDOUT_CLAIM", "C334b_VISION_GATE_V38_HELDOUT_CLAIM")
    text = text.replace("C330_CAPTURE_OFFICE_REGRESSION", "C336_CAPTURE_OFFICE_REGRESSION")
    text = text.replace("vl_gate_v37", "vl_gate_v38")
    text = text.replace("v37_claim", "v38_claim").replace("v37h_claim", "v38h_claim")
    text = text.replace("v37 =", "v38 =").replace("v37h =", "v38h =")
    text = text.replace("max(v37, v37h", "max(v38, v38h")
    text = text.replace('"v37_design"', '"v38_design"')
    text = text.replace('"v37_smoke"', '"v38_smoke"')
    text = text.replace('"v37_heldout"', '"v38_heldout"')
    text = text.replace(OLD_THEMES, THEMES)
    text = text.replace("walnut/onyx/linen/indigo/...", "cedar/jasper/gauze/cyan/...")
    text = text.replace("confidence/gate/stretch", "product/u2c/cost")
    text = text.replace("confidence/stretch", "product/u2c")
    text = text.replace('c269 = load("docs/r50/C329_CONFIDENCE_GATE_STRETCH.json")', 'c269 = load("docs/r50/C335_PRODUCT_U2C_COST.json")')
    text = text.replace('c311 = load("docs/r50/C329_CONFIDENCE_GATE_STRETCH.json")', 'c311 = load("docs/r50/C335_PRODUCT_U2C_COST.json")')
    text = text.replace('"source": "C329"', '"source": "C335"')
    text = text.replace('"confidence_gate_stretch"', '"product_u2c_cost"')
    return text

def main():
    train_src = specs_to_tuples(train)
    held_src = specs_to_tuples(held)
    mapping = [
        ("c326_vision_v37_design_and_batch.py", "c332_vision_v38_design_and_batch.py", lambda t: xform_train(t, train_src)),
        ("c327_vision_v37_smoke.py", "c333_vision_v38_smoke.py", xform_smoke),
        ("c328_vision_v37_heldout.py", "c334_vision_v38_heldout.py", lambda t: xform_heldout(t, held_src)),
        ("c317_product_u2c_cost.py", "c335_product_u2c_cost.py", xform_nv),
        ("c330_capture_office_regression.py", "c336_capture_office_regression.py", xform_reg),
        ("c331_scorecard_and_stage.py", "c337_scorecard_and_stage.py", xform_score),
    ]
    for src, dst, fn in mapping:
        t = (SCR / src).read_text(encoding="utf-8")
        out = fn(t)
        (SCR / dst).write_text(out, encoding="utf-8")
        print("wrote", dst, len(out.encode("utf-8")))
    d = (SCR / "c332_vision_v38_design_and_batch.py").read_text(encoding="utf-8")
    assert "vision_images_v38" in d and "v38_01" in d
    assert "CEDAR bait" in d
    assert "cedar_recv" in d
    assert "JPEG_Q = 60" in d
    s = (SCR / "c337_scorecard_and_stage.py").read_text(encoding="utf-8")
    assert "STAGE_ANT_C337.md" in s
    assert "C333_VISION_V38_SMOKE" in s
    print("ok")

if __name__ == "__main__":
    main()
