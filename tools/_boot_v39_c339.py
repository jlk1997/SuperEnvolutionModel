# -*- coding: utf-8 -*-
"""Bootstrap C339-C344 Vision V39 from V38 + confidence-gate NV."""
from __future__ import annotations
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCR = ROOT / "scripts"
SPEC_PATH = ROOT / "tools" / "_v39_specs.json"

KINDS = [
    ("spruce_recv", "paid_total", "SPRUCE GRAIN RECV V39", "云杉收款单", "RECV"),
    ("carnelian_wh", "qty_sum", "WH CARNELIAN TILE V39", "红玉髓仓位单", "RECV"),
    ("voile_refund", "refund_done", "VOILE PATCH REFUND V39", "薄纱补丁退款单", "DONE"),
    ("azure_tax", "tax_base_paid", "AZURE TAX SLIP V39", "霁蓝税基单", "TAX"),
    ("apatite_pay", "payroll_active", "APATITE PAYROLL V39", "磷灰石薪资单", "PAY"),
    ("cleat_ship", "ship_ok", "CLEAT SHIP DOCK V39", "系缆出库单", "SHIP"),
    ("peridot_sla", "sla_ok_hours", "PERIDOT SLA CARD V39", "橄榄石SLA卡", "SLA"),
    ("gneiss_exp", "exp_sum", "GNEISS EXPENSE V39", "片麻岩费用单", "EXP"),
    ("zinc_po", "po_open", "ZINC PO SHEET V39", "锌片采购单", "PO"),
    ("papyrus_order", "order_paid", "PAPYRUS ORDER V39", "莎草纸订单", "ORD"),
    ("houndstooth_dup", "dup_mark", "HOUNDSTOOTH DUP MARK V39", "千鸟格重复标", "DUP"),
    ("empty_zero", "zero_check", "EMPTY VOID ZERO V39", "空仓零检单", "ZERO"),
    ("hessian_ledger", "ledger_net", "HESSIAN LEDGER V39", "粗麻账本", "LED"),
    ("shellac_ui", "ui_ok", "SHELLAC UI SCAN V39", "虫胶界面扫描", "UI"),
    ("sisal_stack", "stack_count", "SISAL STACK V39", "剑麻堆叠单", "STK"),
    ("fig_fax", "fax_pages", "FIG FAX V39", "无花果传真单", "FAX"),
    ("osmium_glare", "glare_ok", "OSMIUM GLARE V39", "锇光眩光单", "GLR"),
    ("quire_tab", "tab_index", "QUIRE TAB INDEX V39", "印张页签索引", "TAB"),
]

TRAIN_NUMS = [
    (131.5, [63.00, 68.50, 20.00]),
    (97.0, [38, 33, 46]),
    (74.25, [36.00, 38.25, 15.00]),
    (193.0, [94.00, 99.00, 43.00]),
    (262.0, [129.00, 133.00, 36.00]),
    (66.0, [31, 18, 22]),
    (84.5, [45.00, 39.50, 21.00]),
    (111.75, [53.00, 58.75, 25.00]),
    (125.0, [67.00, 58.00, 29.00]),
    (151.5, [81.00, 70.50, 22.00]),
    (2.0, [1, 1, 0]),
    (0.0, [0.00, 0.00, 0.00]),
    (227.25, [111.00, 116.25, 37.00]),
    (1.0, [1, 0, 0]),
    (12.0, [5, 4, 3]),
    (17.0, [9, 8, 3]),
    (1.0, [1, 0, 0]),
    (23.0, [13, 10, 2]),
]

HELD_NUMS = [
    (71.5, [34.00, 37.50, 11.00]),
    (52.0, [20, 17, 24]),
    (40.25, [19.00, 21.25, 8.00]),
    (104.0, [51.00, 53.00, 23.00]),
    (141.0, [69.00, 72.00, 19.00]),
    (35.0, [16, 10, 12]),
    (46.25, [25.00, 21.25, 12.00]),
    (60.75, [29.00, 31.75, 14.00]),
    (67.0, [36.00, 31.00, 16.00]),
    (81.5, [43.00, 38.50, 12.00]),
    (2.0, [1, 1, 0]),
    (0.0, [0.00, 0.00, 0.00]),
    (122.25, [60.00, 62.25, 20.00]),
    (1.0, [1, 0, 0]),
    (7.0, [3, 2, 2]),
    (9.0, [5, 4, 2]),
    (1.0, [1, 0, 0]),
    (12.0, [7, 5, 1]),
]

THEMES = "spruce/carnelian/voile/azure/apatite/cleat/peridot/gneiss/zinc/papyrus/houndstooth/empty/hessian/shellac/sisal/fig/osmium/quire"
OLD_THEMES = "cedar/jasper/gauze/cyan/feldspar/hinge/citrine/basalt/pewter/parchment/herringbone/nil/burlap/lacquer/coir/mulberry/iridium/folio"


def build_lines(i, tag, a, b, c, expected):
    kind, metric, title, cn, stamp = KINDS[i]
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
        # C338 lesson: spell hours for OCR; parser also accepts Nh ok
        lines = [title, f"job1 {a:.2f} hours ok", f"job2 {b:.2f} hours ok", f"job3 {c:.2f} hours late", f"sla_ok_hours TARGET {expected:.2f}"]
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
        "id": f"v39{tag}_{i+1:02d}",
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


train = [build_lines(i, "", *TRAIN_NUMS[i][1], TRAIN_NUMS[i][0]) for i in range(18)]
# fix call - build_lines(i, tag, a, b, c, expected)
train = []
held = []
for i in range(18):
    exp, abc = TRAIN_NUMS[i]
    train.append(build_lines(i, "", abc[0], abc[1], abc[2], exp))
for i in range(18):
    exp, abc = HELD_NUMS[i]
    held.append(build_lines(i, "h", abc[0], abc[1], abc[2], exp))

SPEC_PATH.write_text(json.dumps({"train": train, "held": held}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", SPEC_PATH)

V39_OVERLAY = r'''
    # --- V39 overlays (new vs V38) ---
    for _ in range(100):
        bx = rng.randint(50, 540)
        by = rng.randint(350, 580)
        if in_text_band(by):
            continue
        d.line([(bx, by), (bx + rng.randint(5, 22), by + rng.randint(-4, 4))], fill=(70, 90, 50), width=1)
    for gi in range(5):
        d.ellipse([48 + gi * 24, 308, 66 + gi * 24, 326], outline=(20, 70, 110), width=2)
    d.text((48, 328), "SPRUCE bait 39.39", fill=(40, 70, 30), font=f_tiny)
    for hi in range(4):
        d.polygon([(580 + hi * 34, 36), (606 + hi * 34, 36), (593 + hi * 34, 72)], fill=(30, 60, 160))
    d.text((580, 76), "AZURE bait 59.59", fill=(10, 30, 90), font=f_tiny)
    d.rectangle([250, 380, 410, 440], fill=(250, 245, 255))
    d.text((260, 400), "APATITE ghost 89.89", fill=(30, 60, 80), font=f_pen)
    d.arc([410, 370, 500, 440], 20, 240, fill=(40, 140, 60), width=3)
    d.text((410, 445), "PERIDOT bait 34.34", fill=(20, 100, 40), font=f_tiny)
    d.ellipse([60, 470, 130, 530], fill=(100, 100, 95), outline=(50, 50, 45), width=2)
    d.text((60, 535), "GNEISS bait 25.25", fill=(55, 55, 50), font=f_tiny)
    for qi in range(4):
        d.rectangle([250 + qi * 42, 470, 282 + qi * 42, 502], outline=(60, 80, 50), width=2)
    d.rectangle([850, 110, 1000, 170], fill=(180, 185, 175), outline=(55, 60, 50), width=2)
    d.text((870, 128), "ZINC", fill=(25, 30, 25), font=f_stamp)
    d.polygon([(40, 4), (420, 4), (405, 18), (50, 18)], fill=(200, 210, 190), outline=(70, 90, 50), width=1)
    d.text((70, 5), "OSMIUM bait 69.69", fill=(35, 40, 50), font=f_tiny)
    for ti, ty in enumerate((90, 150, 210)):
        d.polygon([(1000, ty), (1024, ty + 12), (1000, ty + 24)], fill=(50, 110, 70 + ti * 20))
'''


def inject_overlay(text: str) -> str:
    # Remove prior V38 overlay block only (keep buf = io.BytesIO()).
    text2 = re.sub(
        r"\n    # --- V38 overlays.*?\n(?=    buf = io\.BytesIO\(\))",
        "\n",
        text,
        count=1,
        flags=re.S,
    )
    soft = "    buf = io.BytesIO()"
    if "SPRUCE bait" not in text2 and soft in text2:
        text2 = text2.replace(soft, V39_OVERLAY + "\n" + soft, 1)
    elif "SPRUCE bait" not in text2 and "img.save(buf" in text2 and "buf = io.BytesIO()" not in text2:
        text2 = text2.replace(
            "    img.save(buf",
            V39_OVERLAY + "\n    buf = io.BytesIO()\n    img.save(buf",
            1,
        )
    return text2


def xform_train(text, train_specs_src):
    reps = [
        ("C332", "C339"), ("c332", "c339"),
        ("vision_images_v38", "vision_images_v39"),
        ("vision_v38", "vision_v39"),
        ("VL_GATE_V38", "VL_GATE_V39"),
        ("vl_gate_v38", "vl_gate_v39"),
        ("vision_gate_v38", "vision_gate_v39"),
        ("r50plus_v38", "r50plus_v39"),
        ("SCAN DESK V38", "SCAN DESK V39"),
        ("V38 C332", "V39 C339"), ("V38 C339", "V39 C339"),
        ("V38 keeps floor", "V39 keeps floor"),
        ("cedar_recv", "spruce_recv"),
        ("CEDAR bait", "SPRUCE bait"),
        ("CITRINE bait", "PERIDOT bait"),
    ]
    for a, b in reps:
        text = text.replace(a, b)
    # version labels in titles already via SPECS replace
    pat = re.compile(r"SPECS = \[\s*\(\s*\"v3[89]_01\".*?^\]", re.S | re.M)
    m = pat.search(text)
    if not m:
        pat = re.compile(r"SPECS = \[.*?\n\]", re.S)
        m = pat.search(text)
    if m:
        text = text[: m.start()] + train_specs_src + text[m.end() :]
    return inject_overlay(text)


def xform_smoke(text):
    for a, b in [
        ("C333", "C340"), ("c333", "c340"),
        ("vision_images_v38", "vision_images_v39"),
        ("vision_v38_c333", "vision_v39_c340"),
        ("vision_v38", "vision_v39"),
        ("VL_GATE_V38", "VL_GATE_V39"),
        ("vl_gate_v38", "vl_gate_v39"),
        ("r50plus_v38", "r50plus_v39"),
        ("C333_VISION_V38", "C340_VISION_V39"),
        ("C333b_VISION_GATE_V38", "C340b_VISION_GATE_V39"),
        ("VISION_V38_SMOKE", "VISION_V39_SMOKE"),
        ("VISION_GATE_V38_CLAIM", "VISION_GATE_V39_CLAIM"),
    ]:
        text = text.replace(a, b)
    return text


def xform_heldout(text, held_specs_src):
    for a, b in [
        ("C334", "C341"), ("c334", "c341"),
        ("vision_images_v38h", "vision_images_v39h"),
        ("vision_images_v38", "vision_images_v39"),
        ("vision_v38h_c334", "vision_v39h_c341"),
        ("VL_GATE_V38_HELDOUT", "VL_GATE_V39_HELDOUT"),
        ("vl_gate_v38_heldout", "vl_gate_v39_heldout"),
        ("vision_gate_v38_heldout", "vision_gate_v39_heldout"),
        ("r50plus_v38_heldout", "r50plus_v39_heldout"),
        ("vision_v38_heldout", "vision_v39_heldout"),
        ("SCAN DESK V38H", "SCAN DESK V39H"),
        ("V38H C334", "V39H C341"), ("V38H C341", "V39H C341"),
        ("VISION_V38_HELDOUT", "VISION_V39_HELDOUT"),
        ("VISION_GATE_V38_HELDOUT", "VISION_GATE_V39_HELDOUT"),
        ("C334_VISION_V38_HELDOUT", "C341_VISION_V39_HELDOUT"),
        ("C334b_VISION_GATE_V38_HELDOUT", "C341b_VISION_GATE_V39_HELDOUT"),
    ]:
        text = text.replace(a, b)
    pat = re.compile(r"SPECS = \[\s*\(\s*\"v3[89]h_01\".*?^\]", re.S | re.M)
    m = pat.search(text)
    if not m:
        pat = re.compile(r"SPECS = \[.*?\n\]", re.S)
        m = pat.search(text)
    if m:
        text = text[: m.start()] + held_specs_src + text[m.end() :]
    return text


def xform_nv(text):
    # confidence-gate stretch from C329 template path via C335 product → replace content source
    for a, b in [
        ("C335", "C342"), ("c335", "c342"),
        ("product_u2c_cost", "confidence_gate_stretch"),
        ("PRODUCT_U2C_COST", "CONFIDENCE_GATE_STRETCH"),
        ("Product U2C", "Confidence-gate"),
        ("product/u2c/cost", "confidence/gate/stretch"),
        ("product/u2c", "confidence/stretch"),
        ("C317", "C329"), ("c317", "c329"),
    ]:
        text = text.replace(a, b)
    # Prefer cloning from c329 if mapping uses it
    return text


def xform_reg(text):
    for a, b in [
        ("C336", "C343"), ("c336", "c343"),
        ("C330_CAPTURE_OFFICE_REGRESSION", "C343_CAPTURE_OFFICE_REGRESSION"),
        ("vl_gate_v38", "vl_gate_v39"),
        ("v38_claim", "v39_claim"),
        ("v38h_claim", "v39h_claim"),
        ("VISION_V38", "VISION_V39"),
        ("vision_v38", "vision_v39"),
    ]:
        text = text.replace(a, b)
    return text


def xform_score(text):
    text = text.replace("C337", "C344").replace("c337", "c344")
    text = text.replace("STAGE_ANT_C337.md", "STAGE_ANT_C344.md")
    text = text.replace("C333_VISION_V38_SMOKE", "C340_VISION_V39_SMOKE")
    text = text.replace("C333b_VISION_GATE_V38", "C340b_VISION_GATE_V39")
    text = text.replace("C334_VISION_V38_HELDOUT", "C341_VISION_V39_HELDOUT")
    text = text.replace("C334b_VISION_GATE_V38_HELDOUT", "C341b_VISION_GATE_V39_HELDOUT")
    text = text.replace("C332_VISION_V38_DESIGN", "C339_VISION_V39_DESIGN")
    text = text.replace("C335_PRODUCT_U2C_COST", "C342_CONFIDENCE_GATE_STRETCH")
    text = text.replace("C336_CAPTURE_OFFICE_REGRESSION", "C343_CAPTURE_OFFICE_REGRESSION")
    text = text.replace("vl_gate_v38", "vl_gate_v39")
    text = text.replace("v38_claim", "v39_claim").replace("v38h_claim", "v39h_claim")
    text = text.replace("v38 =", "v39 =").replace("v38h =", "v39h =")
    text = text.replace("max(v38, v38h", "max(v39, v39h")
    text = text.replace('"v38_design"', '"v39_design"')
    text = text.replace('"v38_smoke"', '"v39_smoke"')
    text = text.replace('"v38_heldout"', '"v39_heldout"')
    text = text.replace(OLD_THEMES, THEMES)
    text = text.replace("cedar/jasper/gauze/cyan/...", "spruce/carnelian/voile/azure/...")
    text = text.replace("product/u2c/cost", "confidence/gate/stretch")
    text = text.replace("product/u2c", "confidence/stretch")
    text = text.replace('c269 = load("docs/r50/C335_PRODUCT_U2C_COST.json")', 'c269 = load("docs/r50/C342_CONFIDENCE_GATE_STRETCH.json")')
    text = text.replace('c311 = load("docs/r50/C335_PRODUCT_U2C_COST.json")', 'c311 = load("docs/r50/C342_CONFIDENCE_GATE_STRETCH.json")')
    text = text.replace('"source": "C335"', '"source": "C342"')
    text = text.replace('"product_u2c_cost"', '"confidence_gate_stretch"')
    return text


def main():
    train_src = specs_to_tuples(train)
    held_src = specs_to_tuples(held)
    mapping = [
        ("c332_vision_v38_design_and_batch.py", "c339_vision_v39_design_and_batch.py", lambda t: xform_train(t, train_src)),
        ("c333_vision_v38_smoke.py", "c340_vision_v39_smoke.py", xform_smoke),
        ("c334_vision_v38_heldout.py", "c341_vision_v39_heldout.py", lambda t: xform_heldout(t, held_src)),
        ("c329_confidence_gate_stretch.py", "c342_confidence_gate_stretch.py", xform_nv),
        ("c336_capture_office_regression.py", "c343_capture_office_regression.py", xform_reg),
        ("c337_scorecard_and_stage.py", "c344_scorecard_and_stage.py", xform_score),
    ]
    for src, dst, fn in mapping:
        t = (SCR / src).read_text(encoding="utf-8")
        out = fn(t)
        (SCR / dst).write_text(out, encoding="utf-8")
        print("wrote", dst, len(out.encode("utf-8")))
    d = (SCR / "c339_vision_v39_design_and_batch.py").read_text(encoding="utf-8")
    assert "vision_images_v39" in d and "v39_01" in d
    assert "SPRUCE bait" in d
    assert "spruce_recv" in d
    assert "JPEG_Q = 60" in d
    assert "hours ok" in d
    s = (SCR / "c344_scorecard_and_stage.py").read_text(encoding="utf-8")
    assert "STAGE_ANT_C344.md" in s
    assert "C340_VISION_V39_SMOKE" in s
    print("ok")


if __name__ == "__main__":
    main()
