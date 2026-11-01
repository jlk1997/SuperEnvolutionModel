# -*- coding: utf-8 -*-
"""Bootstrap C326-C331 Vision V37 from V36 + confidence NV."""
from __future__ import annotations
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCR = ROOT / "scripts"

KINDS = [
    ("walnut_recv", "paid_total", "WALNUT GRAIN RECV V37", "胡桃收款单", "RECV"),
    ("onyx_wh", "qty_sum", "WH ONYX TILE V37", "缟玛瑙仓位单", "RECV"),
    ("linen_refund", "refund_done", "LINEN PATCH REFUND V37", "亚麻补丁退款单", "DONE"),
    ("indigo_tax", "tax_base_paid", "INDIGO TAX SLIP V37", "靛蓝税基单", "TAX"),
    ("quartz_pay", "payroll_active", "QUARTZ PAYROLL V37", "石英薪资单", "PAY"),
    ("latch_ship", "ship_ok", "LATCH SHIP DOCK V37", "锁扣出库单", "SHIP"),
    ("amber_sla", "sla_ok_hours", "AMBER SLA CARD V37", "琥珀SLA卡", "SLA"),
    ("shale_exp", "exp_sum", "SHALE EXPENSE V37", "页岩费用单", "EXP"),
    ("chrome_po", "po_open", "CHROME PO SHEET V37", "铬钢采购单", "PO"),
    ("bond_order", "order_paid", "BOND ORDER V37", "证券纸订单", "ORD"),
    ("tweed_dup", "dup_mark", "TWEED DUP MARK V37", "花呢重复标记", "DUP"),
    ("void_zero", "zero_check", "VOID NIL ZERO V37", "空值清零单", "ZERO"),
    ("hemp_ledger", "ledger_net", "HEMP LEDGER V37", "麻绳账本", "LED"),
    ("enamel_ui", "ui_ok", "ENAMEL UI SCAN V37", "搪瓷界面扫描", "UI"),
    ("raffia_stack", "stack_count", "RAFFIA STACK V37", "酒椰堆叠单", "STK"),
    ("plum_fax", "fax_pages", "PLUM FAX V37", "梅紫传真单", "FAX"),
    ("tungsten_glare", "glare_ok", "TUNGSTEN GLARE V37", "钨钢眩光单", "GLR"),
    ("binder_tab", "tab_index", "BINDER TAB INDEX V37", "活页页签索引", "TAB"),
]

TRAIN_NUMS = [
    (118.5, [55.00, 63.50, 17.00]),
    (88.0, [33, 29, 41]),
    (64.75, [30.00, 34.75, 12.00]),
    (176.0, [84.00, 92.00, 38.00]),
    (241.0, [118.00, 123.00, 31.00]),
    (57.0, [27, 15, 19]),
    (73.5, [39.00, 34.50, 18.00]),
    (99.25, [47.00, 52.25, 22.00]),
    (113.0, [61.00, 52.00, 26.00]),
    (135.5, [72.00, 63.50, 19.00]),
    (2.0, [1, 1, 0]),
    (0.0, [0.00, 0.00, 0.00]),
    (208.75, [101.00, 107.75, 33.00]),
    (1.0, [1, 0, 0]),
    (10.0, [4, 4, 2]),
    (14.0, [7, 7, 3]),
    (1.0, [1, 0, 0]),
    (19.0, [11, 8, 2]),
]
HELD_NUMS = [
    (69.25, [33.00, 36.25, 13.00]),
    (49.0, [21, 11, 28]),
    (38.5, [18.00, 20.50, 8.00]),
    (97.0, [47.00, 50.00, 22.00]),
    (129.0, [64.00, 65.00, 18.00]),
    (32.0, [16, 8, 12]),
    (41.75, [22.00, 19.75, 10.00]),
    (53.5, [25.00, 28.50, 12.00]),
    (61.0, [33.00, 28.00, 14.00]),
    (74.75, [40.00, 34.75, 11.00]),
    (2.0, [1, 1, 0]),
    (0.0, [0.00, 0.00, 0.00]),
    (115.25, [55.00, 60.25, 18.00]),
    (1.0, [1, 0, 0]),
    (5.0, [2, 2, 1]),
    (8.0, [4, 4, 2]),
    (1.0, [1, 0, 0]),
    (11.0, [6, 5, 1]),
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
        "id": f"v37{tag}_{i+1:02d}",
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
    s["id"] = f"v37_{i+1:02d}"
for i, s in enumerate(held):
    s["id"] = f"v37h_{i+1:02d}"

SPEC_PATH = ROOT / "tools" / "_v37_specs.json"
SPEC_PATH.write_text(json.dumps({"train": train, "held": held}, ensure_ascii=False, indent=2), encoding="utf-8")
print("wrote", SPEC_PATH)

V37_OVERLAY = r'''
    # --- V37 overlays (new vs V36) ---
    for _ in range(95):
        bx = rng.randint(55, 530)
        by = rng.randint(345, 575)
        if in_text_band(by):
            continue
        d.line([(bx, by), (bx + rng.randint(6, 24), by + rng.randint(-3, 3))], fill=(70, 100, 130), width=1)
    for gi in range(6):
        d.ellipse([40 + gi * 22, 305, 56 + gi * 22, 321], outline=(30, 70, 110), width=2)
    d.text((40, 323), "WALNUT bait 37.37", fill=(70, 40, 20), font=f_tiny)
    for hi in range(4):
        d.polygon([(575 + hi * 34, 38), (601 + hi * 34, 38), (588 + hi * 34, 74)], fill=(30, 60, 140))
    d.text((575, 78), "INDIGO bait 51.51", fill=(15, 30, 90), font=f_tiny)
    d.rectangle([245, 375, 405, 435], fill=(240, 248, 255))
    d.text((255, 395), "QUARTZ ghost 77.77", fill=(50, 80, 100), font=f_pen)
    d.arc([405, 365, 495, 435], 15, 230, fill=(140, 80, 20), width=3)
    d.text((405, 440), "AMBER bait 29.29", fill=(120, 60, 10), font=f_tiny)
    d.ellipse([55, 465, 125, 525], fill=(160, 150, 100), outline=(100, 90, 40), width=2)
    d.text((55, 530), "SHALE bait 21.21", fill=(80, 70, 40), font=f_tiny)
    for qi in range(4):
        d.rectangle([245 + qi * 42, 465, 277 + qi * 42, 497], outline=(60, 80, 100), width=2)
    d.rectangle([845, 105, 995, 165], fill=(150, 155, 165), outline=(40, 50, 60), width=2)
    d.text((865, 123), "CHROME", fill=(15, 20, 25), font=f_stamp)
    d.polygon([(45, 6), (410, 6), (395, 20), (55, 20)], fill=(200, 195, 185), outline=(80, 60, 45), width=1)
    d.text((65, 7), "TUNGSTEN bait 67.67", fill=(40, 45, 50), font=f_tiny)
    for ti, ty in enumerate((95, 155, 215)):
        d.polygon([(1000, ty), (1024, ty + 12), (1000, ty + 24)], fill=(90, 50, 130 + ti * 15))
'''

THEMES = "walnut/onyx/linen/indigo/quartz/latch/amber/shale/chrome/bond/tweed/void/hemp/enamel/raffia/plum/tungsten/binder"
OLD_THEMES = "teak/marble/canvas/cobalt/mica/clasp/garnet/flint/steel/kraft/flannel/empty/jute/glaze/sisal/aubergine/titanium/dossier"

def inject_overlay(text: str) -> str:
    soft = "    buf = io.BytesIO()"
    text2 = re.sub(r"\n    # --- V36 overlays.*?\n(?=    img\.save\(buf)", "\n", text, count=1, flags=re.S)
    if soft in text2 and "WALNUT bait" not in text2:
        if soft not in text2:
        soft = "    img.save(buf"
    text2 = text2.replace(soft, V37_OVERLAY + "\n" + soft, 1)
    return text2

def xform_train(text, train_specs_src):
    reps = [
        ("C320", "C326"), ("c320", "c326"),
        ("vision_images_v36", "vision_images_v37"),
        ("vision_v36", "vision_v37"),
        ("VL_GATE_V36", "VL_GATE_V37"),
        ("vl_gate_v36", "vl_gate_v37"),
        ("vision_gate_v36", "vision_gate_v37"),
        ("r50plus_v36", "r50plus_v37"),
        ("SCAN DESK V36", "SCAN DESK V37"),
        ("V36 C320", "V37 C326"), ("V36 C326", "V37 C326"),
        ("V36 keeps floor", "V37 keeps floor"),
        ("teak_recv", "walnut_recv"),
        ("TEAK bait", "WALNUT bait"),
    ]
    for a, b in reps:
        text = text.replace(a, b)
    pat = re.compile(r"SPECS = \[\s*\(\s*\"v3[67]_01\".*?^\]", re.S | re.M)
    m = pat.search(text)
    if not m:
        pat = re.compile(r"SPECS = \[.*?\n\]", re.S)
        m = pat.search(text)
    if m:
        text = text[:m.start()] + train_specs_src + text[m.end():]
    return inject_overlay(text)

def xform_smoke(text):
    for a, b in [
        ("C321", "C327"), ("c321", "c327"),
        ("vision_images_v36", "vision_images_v37"),
        ("vision_v36_c321", "vision_v37_c327"),
        ("vision_v36", "vision_v37"),
        ("VL_GATE_V36", "VL_GATE_V37"),
        ("vl_gate_v36", "vl_gate_v37"),
        ("r50plus_v36", "r50plus_v37"),
        ("C321_VISION_V36", "C327_VISION_V37"),
        ("C321b_VISION_GATE_V36", "C327b_VISION_GATE_V37"),
        ("VISION_V36_SMOKE", "VISION_V37_SMOKE"),
        ("VISION_GATE_V36_CLAIM", "VISION_GATE_V37_CLAIM"),
    ]:
        text = text.replace(a, b)
    return text

def xform_heldout(text, held_specs_src):
    for a, b in [
        ("C322", "C328"), ("c322", "c328"),
        ("vision_images_v36h", "vision_images_v37h"),
        ("vision_images_v36", "vision_images_v37"),
        ("vision_v36h_c322", "vision_v37h_c328"),
        ("VL_GATE_V36_HELDOUT", "VL_GATE_V37_HELDOUT"),
        ("vl_gate_v36_heldout", "vl_gate_v37_heldout"),
        ("vision_gate_v36_heldout", "vision_gate_v37_heldout"),
        ("r50plus_v36_heldout", "r50plus_v37_heldout"),
        ("vision_v36_heldout", "vision_v37_heldout"),
        ("SCAN DESK V36H", "SCAN DESK V37H"),
        ("V36H C322", "V37H C328"), ("V36H C328", "V37H C328"),
        ("VISION_V36_HELDOUT", "VISION_V37_HELDOUT"),
        ("VISION_GATE_V36_HELDOUT", "VISION_GATE_V37_HELDOUT"),
        ("_v36hc322", "_v37hc328"),
        ('"version": "v36h"', '"version": "v37h"'),
    ]:
        text = text.replace(a, b)
    pat = re.compile(r"SPECS = \[\s*\(\s*\"v3[67]h_01\".*?^\]", re.S | re.M)
    m = pat.search(text)
    if not m:
        pat = re.compile(r"SPECS = \[.*?\n\]", re.S)
        m = pat.search(text)
    if m:
        text = text[:m.start()] + held_specs_src + text[m.end():]
    return text

def xform_nv(text):
    text = text.replace("C305", "C329").replace("c305", "c329")
    text = text.replace("confidence_gate_stretch_c305", "confidence_gate_stretch_c329")
    text = text.replace("C305_CONFIDENCE_GATE_STRETCH.json", "C329_CONFIDENCE_GATE_STRETCH.json")
    return text

def xform_reg(text):
    text = text.replace("C324", "C330").replace("c324", "c330")
    text = text.replace("C320-C323", "C326-C329")
    text = text.replace("c320_c323", "c326_c329")
    text = text.replace("capture_regression_c324", "capture_regression_c330")
    needle = '("V36_heldout", DOC / "C322_VISION_V36_HELDOUT_SMOKE.json"),'
    if needle in text and '("V37"' not in text:
        text = text.replace(
            needle,
            needle
            + '\n    ("V37", DOC / "C327_VISION_V37_SMOKE.json"),'
            + '\n    ("V37_heldout", DOC / "C328_VISION_V37_HELDOUT_SMOKE.json"),',
        )
    needle2 = '("C323_dissolve_cost_shadow", DOC / "C323_DISSOLVE_COST_SHADOW.json"),'
    if needle2 in text and "C329_confidence" not in text:
        text = text.replace(
            needle2,
            needle2
            + '\n    ("C329_confidence_gate_stretch", DOC / "C329_CONFIDENCE_GATE_STRETCH.json"),',
        )
    text = text.replace(
        '"V36", "V36_heldout", "C233_clarity_floor", "C323_dissolve_cost_shadow"]',
        '"V36", "V36_heldout", "V37", "V37_heldout", "C233_clarity_floor", "C329_confidence_gate_stretch"]',
    )
    text = text.replace('DOC / "C324_CAPTURE_OFFICE_REGRESSION.json"', 'DOC / "C330_CAPTURE_OFFICE_REGRESSION.json"')
    return text

def xform_score(text):
    text = text.replace("C325", "C331").replace("c325", "c331")
    text = text.replace("c320_c324", "c326_c330")
    text = text.replace("STAGE_ANT_C325.md", "STAGE_ANT_C331.md")
    text = text.replace("C320-C324", "C326-C330")
    text = text.replace("C320-C325", "C326-C331")
    text = text.replace("unified_scorecard_c320_c324", "unified_scorecard_c326_c330")
    text = text.replace("unified_scorecard_c320_c325", "unified_scorecard_c326_c331")
    text = text.replace("C320_VISION_V36_DESIGN", "C326_VISION_V37_DESIGN")
    text = text.replace("C321_VISION_V36_SMOKE", "C327_VISION_V37_SMOKE")
    text = text.replace("C321b_VISION_GATE_V36_CLAIM", "C327b_VISION_GATE_V37_CLAIM")
    text = text.replace("C322_VISION_V36_HELDOUT_SMOKE", "C328_VISION_V37_HELDOUT_SMOKE")
    text = text.replace("C322b_VISION_GATE_V36_HELDOUT_CLAIM", "C328b_VISION_GATE_V37_HELDOUT_CLAIM")
    text = text.replace("C324_CAPTURE_OFFICE_REGRESSION", "C330_CAPTURE_OFFICE_REGRESSION")
    text = text.replace("vl_gate_v36", "vl_gate_v37")
    text = text.replace("v36_claim", "v37_claim").replace("v36h_claim", "v37h_claim")
    text = text.replace("v36 =", "v37 =").replace("v36h =", "v37h =")
    text = text.replace("max(v36, v36h", "max(v37, v37h")
    text = text.replace('"v36_design"', '"v37_design"')
    text = text.replace('"v36_smoke"', '"v37_smoke"')
    text = text.replace('"v36_heldout"', '"v37_heldout"')
    text = text.replace(OLD_THEMES, THEMES)
    text = text.replace("teak/marble/canvas/cobalt/...", "walnut/onyx/linen/indigo/...")
    text = text.replace("dissolve/cost/shadow", "confidence/gate/stretch")
    text = text.replace("dissolve/shadow", "confidence/stretch")
    text = text.replace('c269 = load("docs/r50/C323_DISSOLVE_COST_SHADOW.json")', 'c269 = load("docs/r50/C329_CONFIDENCE_GATE_STRETCH.json")')
    text = text.replace('c311 = load("docs/r50/C323_DISSOLVE_COST_SHADOW.json")', 'c311 = load("docs/r50/C329_CONFIDENCE_GATE_STRETCH.json")')
    text = text.replace('"source": "C323"', '"source": "C329"')
    text = text.replace('"dissolve_cost_shadow"', '"confidence_gate_stretch"')
    return text

def main():
    train_src = specs_to_tuples(train)
    held_src = specs_to_tuples(held)
    mapping = [
        ("c320_vision_v36_design_and_batch.py", "c326_vision_v37_design_and_batch.py", lambda t: xform_train(t, train_src)),
        ("c321_vision_v36_smoke.py", "c327_vision_v37_smoke.py", xform_smoke),
        ("c322_vision_v36_heldout.py", "c328_vision_v37_heldout.py", lambda t: xform_heldout(t, held_src)),
        ("c305_confidence_gate_stretch.py", "c329_confidence_gate_stretch.py", xform_nv),
        ("c324_capture_office_regression.py", "c330_capture_office_regression.py", xform_reg),
        ("c325_scorecard_and_stage.py", "c331_scorecard_and_stage.py", xform_score),
    ]
    for src, dst, fn in mapping:
        t = (SCR / src).read_text(encoding="utf-8")
        out = fn(t)
        (SCR / dst).write_text(out, encoding="utf-8")
        print("wrote", dst, len(out.encode("utf-8")))
    d = (SCR / "c326_vision_v37_design_and_batch.py").read_text(encoding="utf-8")
    assert "vision_images_v37" in d and "v37_01" in d
    assert "WALNUT bait" in d
    assert "walnut_recv" in d
    assert "JPEG_Q = 60" in d
    s = (SCR / "c331_scorecard_and_stage.py").read_text(encoding="utf-8")
    assert "STAGE_ANT_C331.md" in s
    assert "C327_VISION_V37_SMOKE" in s
    print("ok")

if __name__ == "__main__":
    main()
