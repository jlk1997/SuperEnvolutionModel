# -*- coding: utf-8 -*-
"""Bootstrap C314-C319 Vision V35 from V34 + product-u2c NV."""
from __future__ import annotations
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCR = ROOT / "scripts"

# New themes vs V34 bamboo/...
KINDS = [
    ("jade_recv", "paid_total", "JADE GRAIN RECV V35", "玉纹收款单", "RECV"),
    ("granite_wh", "qty_sum", "WH GRANITE TILE V35", "花岗岩仓位单", "RECV"),
    ("suede_refund", "refund_done", "SUEDE PATCH REFUND V35", "麂皮补丁退款单", "DONE"),
    ("bronze_tax", "tax_base_paid", "BRONZE TAX SLIP V35", "青铜税基单", "TAX"),
    ("opal_pay", "payroll_active", "OPAL PAYROLL V35", "蛋白石工资单", "PAY"),
    ("hinge_ship", "ship_ok", "HINGE SHIP DOCK V35", "铰链发运单", "SHIP"),
    ("citrine_sla", "sla_ok_hours", "CITRINE SLA CARD V35", "黄水晶SLA卡", "SLA"),
    ("basalt_exp", "exp_sum", "BASALT EXPENSE V35", "玄武岩费用单", "EXP"),
    ("pewter_po", "po_open", "PEWTER PO SHEET V35", "白镴采购单", "PO"),
    ("vellum_order", "order_paid", "VELLUM ORDER V35", "羊皮纸订单", "ORD"),
    ("fleece_dup", "dup_mark", "FLEECE DUP MARK V35", "绒布重复标记", "DUP"),
    ("null_zero", "zero_check", "NULL VOID ZERO V35", "空值归零单", "ZERO"),
    ("burlap_ledger", "ledger_net", "BURLAP LEDGER V35", "麻袋账本", "LED"),
    ("porcelain_ui", "ui_ok", "PORCELAIN UI SCAN V35", "瓷面界面扫描", "UI"),
    ("twine_stack", "stack_count", "TWINE STACK V35", "麻绳堆叠单", "STK"),
    ("mulberry_fax", "fax_pages", "MULBERRY FAX V35", "桑皮传真单", "FAX"),
    ("nickel_glare", "glare_ok", "NICKEL GLARE V35", "镍面眩光单", "GLR"),
    ("folio_tab", "tab_index", "FOLIO TAB INDEX V35", "对开页签索引", "TAB"),
]

def money_lines(kind_prefix, a, b, c_open, target, metric_label):
    return [
        kind_prefix,
        f"a paid {a:.2f}" if "paid" in metric_label or metric_label=="paid_total" else f"SKU1 qty {int(a)} ok" if metric_label=="qty_sum" else f"row1 {a:.2f}",
    ]

# Explicit train/held numeric specs mirroring V34 structure
TRAIN_NUMS = [
    # id_suffix kind metric expected lines_extra handled below
    (121.5, [58.00, 63.50, 17.00]),
    (103.0, [48, 22, 55]),  # qty
    (67.25, [31.00, 36.25, 14.00]),
    (188.0, [90.00, 98.00, 40.00]),
    (244.0, [120.00, 124.00, 30.00]),
    (56.0, [28, 14, 20]),
    (72.5, [40.00, 32.50, 18.00]),
    (95.75, [45.25, 50.50, 22.00]),
    (110.0, [60.00, 50.00, 25.00]),
    (133.5, [70.00, 63.50, 19.00]),
    (2.0, [1, 1, 0]),
    (0.0, [0.00, 0.00, 0.00]),
    (210.25, [100.00, 110.25, 33.00]),
    (1.0, [1, 0, 0]),
    (9.0, [4, 3, 2]),
    (14.0, [7, 7, 3]),
    (1.0, [1, 0, 0]),
    (18.0, [10, 8, 2]),
]
HELD_NUMS = [
    (69.5, [33.00, 36.50, 13.00]),
    (58.0, [26, 13, 32]),
    (38.5, [18.00, 20.50, 8.00]),
    (99.0, [48.00, 51.00, 22.00]),
    (130.0, [64.00, 66.00, 18.00]),
    (31.0, [16, 8, 12]),
    (41.0, [22.00, 19.00, 10.00]),
    (52.25, [24.00, 28.25, 12.00]),
    (60.0, [32.00, 28.00, 14.00]),
    (74.5, [40.00, 34.50, 11.00]),
    (2.0, [1, 1, 0]),
    (0.0, [0.00, 0.00, 0.00]),
    (115.0, [55.00, 60.00, 18.00]),
    (1.0, [1, 0, 0]),
    (5.0, [2, 2, 1]),
    (8.0, [4, 4, 2]),
    (1.0, [1, 0, 0]),
    (10.0, [6, 4, 1]),
]

METRICS = [
    "paid_total","qty_sum","refund_done","tax_base_paid","payroll_active","ship_ok",
    "sla_ok_hours","exp_sum","po_open","order_paid","dup_mark","zero_check",
    "ledger_net","ui_ok","stack_count","fax_pages","glare_ok","tab_index",
]

def build_lines(i, tag, expected, nums):
    kind, metric, title, cn, stamp = KINDS[i]
    a,b,c = nums
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
    else:  # tab_index
        lines = [title, f"tabA {int(a)}", f"tabB {int(b)}", f"tabC {int(c)}", f"tab_index TARGET {int(expected)}"]
    return {
        "id": f"v35{tag}_{i+1:02d}",
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
# fix ids: v35_01 not v35_01 from tag ""
for i,s in enumerate(train):
    s["id"] = f"v35_{i+1:02d}"
for i,s in enumerate(held):
    s["id"] = f"v35h_{i+1:02d}"

SPEC_PATH = ROOT / "tools" / "_v35_specs.json"
SPEC_PATH.write_text(json.dumps({"train": train, "held": held}, ensure_ascii=False, indent=2), encoding="utf-8")
print("wrote", SPEC_PATH)

V35_OVERLAY = r'''
    # --- V35 overlays (new vs V34) ---
    for _ in range(80):
        bx = rng.randint(80, 500)
        by = rng.randint(330, 560)
        if in_text_band(by):
            continue
        d.line([(bx, by), (bx + rng.randint(6, 18), by)], fill=(120, 140, 160), width=1)
    for gi in range(6):
        d.ellipse([40 + gi * 18, 310, 54 + gi * 18, 324], outline=(60, 100, 80), width=2)
    d.text((40, 328), "JADE bait 35.35", fill=(20, 80, 50), font=f_tiny)
    for hi in range(5):
        d.polygon([(600 + hi * 30, 50), (620 + hi * 30, 50), (610 + hi * 30, 78)], fill=(180, 90, 40))
    d.text((600, 82), "BRONZE bait 42.42", fill=(100, 50, 20), font=f_tiny)
    d.rectangle([250, 360, 390, 420], fill=(245, 235, 255))
    d.text((260, 380), "OPAL ghost 77.77", fill=(120, 80, 140), font=f_pen)
    d.arc([420, 350, 500, 420], 30, 200, fill=(70, 70, 90), width=3)
    d.text((420, 425), "HINGE bait 23.23", fill=(40, 40, 60), font=f_tiny)
    d.ellipse([70, 450, 140, 510], fill=(200, 170, 40), outline=(140, 110, 20), width=2)
    d.text((70, 515), "CITRINE bait 16.16", fill=(120, 90, 10), font=f_tiny)
    for qi in range(3):
        d.rectangle([250 + qi * 45, 450, 285 + qi * 45, 485], outline=(90, 90, 100), width=2)
    d.rectangle([860, 120, 990, 175], fill=(160, 165, 170), outline=(70, 75, 80), width=2)
    d.text((880, 138), "PEWTER", fill=(30, 30, 40), font=f_stamp)
    d.polygon([(50, 10), (380, 10), (365, 24), (60, 24)], fill=(190, 210, 200), outline=(70, 90, 80), width=1)
    d.text((70, 11), "NICKEL bait 51.51", fill=(40, 50, 60), font=f_tiny)
    for ti, ty in enumerate((100, 160, 220)):
        d.polygon([(1000, ty), (1024, ty + 10), (1000, ty + 20)], fill=(80, 120, 160 + ti * 20))
'''

THEMES = "jade/granite/suede/bronze/opal/hinge/citrine/basalt/pewter/vellum/fleece/null/burlap/porcelain/twine/mulberry/nickel/folio"

def inject_overlay(text: str) -> str:
    soft = "    img.save(buf"
    text2 = re.sub(r"\n    # --- V34 overlays.*?\n(?=    img\.save\(buf)", "\n", text, count=1, flags=re.S)
    if soft in text2 and "JADE bait" not in text2:
        text2 = text2.replace(soft, V35_OVERLAY + "\n" + soft, 1)
    return text2

def xform_train(text, train_specs_src):
    reps = [
        ("C308","C314"),("c308","c314"),
        ("vision_images_v34","vision_images_v35"),
        ("vision_v34","vision_v35"),
        ("VL_GATE_V34","VL_GATE_V35"),
        ("vl_gate_v34","vl_gate_v35"),
        ("vision_gate_v34","vision_gate_v35"),
        ("r50plus_v34","r50plus_v35"),
        ("SCAN DESK V34","SCAN DESK V35"),
        ("V34 C308","V35 C314"),("V34 C314","V35 C314"),
        ("V34 keeps floor","V35 keeps floor"),
        ("bamboo_recv","jade_recv"),
    ]
    for a,b in reps: text=text.replace(a,b)
    # replace SPECS block
    pat = re.compile(r"SPECS = \[\s*\(\s*\"v3[45]_01\".*?^\]", re.S|re.M)
    m = pat.search(text)
    if not m:
        pat = re.compile(r"SPECS = \[.*?\n\]", re.S)
        m = pat.search(text)
    if m:
        text = text[:m.start()] + train_specs_src + text[m.end():]
    return inject_overlay(text)

def xform_smoke(text):
    for a,b in [
        ("C309","C315"),("c309","c315"),
        ("vision_images_v34","vision_images_v35"),
        ("vision_v34_c309","vision_v35_c315"),
        ("vision_v34","vision_v35"),
        ("VL_GATE_V34","VL_GATE_V35"),
        ("vl_gate_v34","vl_gate_v35"),
        ("r50plus_v34","r50plus_v35"),
        ("C315_VISION_V34","C315_VISION_V35"),
        ("C315b_VISION_GATE_V34","C315b_VISION_GATE_V35"),
        ("VISION_V34_SMOKE","VISION_V35_SMOKE"),
        ("VISION_GATE_V34_CLAIM","VISION_GATE_V35_CLAIM"),
    ]:
        text=text.replace(a,b)
    return text

def xform_heldout(text, held_specs_src):
    for a,b in [
        ("C310","C316"),("c310","c316"),
        ("vision_images_v34h","vision_images_v35h"),
        ("vision_images_v34","vision_images_v35"),
        ("vision_v34h_c310","vision_v35h_c316"),
        ("VL_GATE_V34_HELDOUT","VL_GATE_V35_HELDOUT"),
        ("vl_gate_v34_heldout","vl_gate_v35_heldout"),
        ("vision_gate_v34_heldout","vision_gate_v35_heldout"),
        ("r50plus_v34_heldout","r50plus_v35_heldout"),
        ("vision_v34_heldout","vision_v35_heldout"),
        ("SCAN DESK V34H","SCAN DESK V35H"),
        ("V34H C310","V35H C316"),("V34H C316","V35H C316"),
        ("VISION_V34_HELDOUT","VISION_V35_HELDOUT"),
        ("VISION_GATE_V34_HELDOUT","VISION_GATE_V35_HELDOUT"),
        ("_v34hc310","_v35hc316"),
        ('"version": "v34h"','"version": "v35h"'),
    ]:
        text=text.replace(a,b)
    pat = re.compile(r"SPECS = \[\s*\(\s*\"v3[45]h_01\".*?^\]", re.S|re.M)
    m = pat.search(text)
    if not m:
        pat = re.compile(r"SPECS = \[.*?\n\]", re.S)
        m = pat.search(text)
    if m:
        text = text[:m.start()] + held_specs_src + text[m.end():]
    return text

def xform_nv(text):
    text = text.replace("C299","C317").replace("c299","c317")
    text = text.replace("product_u2c_cost_c299","product_u2c_cost_c317")
    text = text.replace("C299_PRODUCT_U2C_COST.json","C317_PRODUCT_U2C_COST.json")
    return text

def xform_reg(text):
    text = text.replace("C312","C318").replace("c312","c318")
    text = text.replace("C308-C311","C314-C317")
    text = text.replace("c308_c311","c314_c317")
    text = text.replace("capture_regression_c312","capture_regression_c318")
    needle = '("V34_heldout", DOC / "C310_VISION_V34_HELDOUT_SMOKE.json"),'
    if needle in text and '("V35"' not in text:
        text = text.replace(
            needle,
            needle
            + '\n    ("V35", DOC / "C315_VISION_V35_SMOKE.json"),'
            + '\n    ("V35_heldout", DOC / "C316_VISION_V35_HELDOUT_SMOKE.json"),',
        )
    needle2 = '("C311_dissolve_cost_shadow", DOC / "C311_DISSOLVE_COST_SHADOW.json"),'
    if needle2 in text and "C317_product" not in text:
        text = text.replace(
            needle2,
            needle2
            + '\n    ("C317_product_u2c_cost", DOC / "C317_PRODUCT_U2C_COST.json"),',
        )
    text = text.replace(
        '"V34", "V34_heldout", "C233_clarity_floor", "C311_dissolve_cost_shadow"]',
        '"V34", "V34_heldout", "V35", "V35_heldout", "C233_clarity_floor", "C317_product_u2c_cost"]',
    )
    text = text.replace('DOC / "C312_CAPTURE_OFFICE_REGRESSION.json"', 'DOC / "C318_CAPTURE_OFFICE_REGRESSION.json"')
    return text

def xform_score(text):
    text = text.replace("C313","C319").replace("c313","c319")
    text = text.replace("c308_c312","c314_c318")
    text = text.replace("STAGE_ANT_C313.md","STAGE_ANT_C319.md")
    text = text.replace("C308-C312","C314-C318")
    text = text.replace("C308-C313","C314-C319")
    text = text.replace("unified_scorecard_c308_c312","unified_scorecard_c314_c318")
    text = text.replace("C308_VISION_V34_DESIGN","C314_VISION_V35_DESIGN")
    text = text.replace("C309_VISION_V34_SMOKE","C315_VISION_V35_SMOKE")
    text = text.replace("C309b_VISION_GATE_V34_CLAIM","C315b_VISION_GATE_V35_CLAIM")
    text = text.replace("C310_VISION_V34_HELDOUT_SMOKE","C316_VISION_V35_HELDOUT_SMOKE")
    text = text.replace("C310b_VISION_GATE_V34_HELDOUT_CLAIM","C316b_VISION_GATE_V35_HELDOUT_CLAIM")
    text = text.replace("C312_CAPTURE_OFFICE_REGRESSION","C318_CAPTURE_OFFICE_REGRESSION")
    text = text.replace("C311_DISSOLVE_COST_SHADOW","C317_PRODUCT_U2C_COST")
    text = text.replace('"dissolve_cost_shadow"','"product_u2c_cost"')
    text = text.replace('"source": "C311"','"source": "C317"')
    text = text.replace("V34","V35").replace("v34","v35")
    text = text.replace(
        "bamboo/slate/denim/brass/prism/latch/amber/quarry/tin/mylar/felt/void/stitch/enamel/cord/rice/chrome/index",
        THEMES,
    )
    text = text.replace("bamboo/slate/denim/brass/...","jade/granite/suede/bronze/...")
    text = text.replace("dissolve/shadow","product/u2c")
    text = text.replace("dissolve/cost/shadow","product/u2c/cost")
    return text

def main():
    train_src = specs_to_tuples(train)
    held_src = specs_to_tuples(held)
    mapping = [
        ("c308_vision_v34_design_and_batch.py","c314_vision_v35_design_and_batch.py", lambda t: xform_train(t, train_src)),
        ("c309_vision_v34_smoke.py","c315_vision_v35_smoke.py", xform_smoke),
        ("c310_vision_v34_heldout.py","c316_vision_v35_heldout.py", lambda t: xform_heldout(t, held_src)),
        ("c299_product_u2c_cost.py","c317_product_u2c_cost.py", xform_nv),
        ("c312_capture_office_regression.py","c318_capture_office_regression.py", xform_reg),
        ("c313_scorecard_and_stage.py","c319_scorecard_and_stage.py", xform_score),
    ]
    for src,dst,fn in mapping:
        t=(SCR/src).read_text(encoding="utf-8")
        out=fn(t)
        (SCR/dst).write_text(out, encoding="utf-8")
        print("wrote", dst, len(out.encode("utf-8")))
    d=(SCR/"c314_vision_v35_design_and_batch.py").read_text(encoding="utf-8")
    assert "vision_images_v35" in d and "v35_01" in d
    assert "JADE bait" in d
    assert "jade_recv" in d
    assert "JPEG_Q = 60" in d
    s=(SCR/"c319_scorecard_and_stage.py").read_text(encoding="utf-8")
    assert "STAGE_ANT_C319.md" in s
    assert "C315_VISION_V35_SMOKE" in s
    print("ok")

if __name__ == "__main__":
    main()
