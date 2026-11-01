# -*- coding: utf-8 -*-
"""Bootstrap Vision V45 scripts (C377-C379) from V44 templates."""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCR = ROOT / "scripts"

# NEW themes vs V44 flint/velvet/...
KINDS = [
    ("ember_recv", "paid_total", "EMBER GRAIN RECV V45", "余烬收款单", "RECV"),
    ("frost_wh", "qty_sum", "WH FROST BIN V45", "霜白仓位单", "RECV"),
    ("granite_refund", "refund_done", "GRANITE PATCH REFUND V45", "花岗岩退款单", "DONE"),
    ("amber_tax", "tax_base_paid", "AMBER TAX SLIP V45", "琥珀税基单", "TAX"),
    ("cobalt_pay", "payroll_active", "COBALT PAYROLL V45", "钴蓝工资单", "PAY"),
    ("rust_ship", "ship_ok", "RUST SHIP DOCK V45", "锈色出库单", "SHIP"),
    ("sage_sla", "sla_ok_hours", "SAGE SLA CARD V45", "鼠尾草SLA卡", "SLA"),
    ("coral_exp", "exp_sum", "CORAL EXPENSE V45", "珊瑚费用单", "EXP"),
    ("slate_po", "po_open", "SLATE PO SHEET V45", "石板采购单", "PO"),
    ("pearl_order", "order_paid", "PEARL ORDER V45", "珍珠订单", "ORD"),
    ("onyx_dup", "dup_mark", "ONYX DUP MARK V45", "缟玛瑙重复标", "DUP"),
    ("moss_zero", "zero_check", "MOSS AIR ZERO V45", "苔藓零值校验", "ZERO"),
    ("cedar_ledger", "ledger_net", "CEDAR LEDGER V45", "雪松账本", "LED"),
    ("chrome_ui", "ui_ok", "CHROME UI SCAN V45", "铬面界面扫描", "UI"),
    ("jade_stack", "stack_count", "JADE STACK V45", "翡翠堆叠单", "STK"),
    ("linen_fax", "fax_pages", "LINEN FAX V45", "亚麻传真单", "FAX"),
    ("brass_glare", "glare_ok", "BRASS GLARE V45", "黄铜眩光单", "GLR"),
    ("ink_tab", "tab_index", "INK TAB INDEX V45", "墨迹页签索引", "TAB"),
]

# Disjoint from V44 train/heldout amounts
TRAIN = [
    (196.5, (95.0, 101.5, 38.0)),
    (158.0, (66, 51, 71)),
    (127.75, (61.0, 66.75, 28.0)),
    (288.0, (141.0, 147.0, 64.0)),
    (372.0, (182.0, 190.0, 58.0)),
    (109.0, (51, 31, 36)),
    (136.25, (72.0, 64.25, 35.0)),
    (174.5, (83.0, 91.5, 40.0)),
    (194.0, (103.0, 91.0, 47.0)),
    (234.25, (125.0, 109.25, 36.0)),
    (2.0, (1, 1, 0)),
    (0.0, (0.0, 0.0, 0.0)),
    (318.75, (155.0, 163.75, 53.0)),
    (1.0, (1, 0, 0)),
    (21.0, (10, 8, 3)),
    (28.0, (15, 13, 8)),
    (1.0, (1, 0, 0)),
    (39.0, (22, 17, 7)),
]
HELD = [
    (112.25, (54.0, 58.25, 21.0)),
    (88.0, (37, 24, 42)),
    (71.5, (34.0, 37.5, 15.0)),
    (161.0, (78.0, 83.0, 36.0)),
    (198.0, (97.0, 101.0, 31.0)),
    (58.0, (28, 16, 19)),
    (74.75, (39.0, 35.75, 18.0)),
    (94.25, (44.0, 50.25, 22.0)),
    (106.0, (56.0, 50.0, 25.0)),
    (128.5, (68.0, 60.5, 19.0)),
    (2.0, (1, 1, 0)),
    (0.0, (0.0, 0.0, 0.0)),
    (176.5, (85.0, 91.5, 29.0)),
    (1.0, (1, 0, 0)),
    (12.0, (6, 4, 2)),
    (16.0, (9, 7, 4)),
    (1.0, (1, 0, 0)),
    (24.0, (13, 11, 4)),
]


def lines_for(i, ver, expected, nums):
    kind, metric, title, cn, stamp = KINDS[i]
    title = title.replace("V45", ver)
    a, b, c = nums
    if metric == "paid_total":
        ls = [title, f"a paid {a:.2f}", f"b paid {b:.2f}", f"c open {c:.2f}", f"TOTAL PAID TARGET {expected:.2f}"]
    elif metric == "qty_sum":
        ls = [title, f"SKU1 qty {int(a)} ok", f"SKU2 qty {int(b)} hold", f"SKU3 qty {int(c)} ok", f"qty_sum TARGET {int(expected)}"]
    elif metric == "refund_done":
        ls = [title, f"itemR1 {a:.2f} done", f"itemR2 {b:.2f} done", f"itemR3 {c:.2f} open", f"refund_done TARGET {expected:.2f}"]
    elif metric == "tax_base_paid":
        ls = [title, f"base {a:.2f} paid", f"addon {b:.2f} paid", f"skip {c:.2f}", f"tax_base_paid TARGET {expected:.2f}"]
    elif metric == "payroll_active":
        ls = [title, f"empA {a:.2f} active", f"empB {b:.2f} active", f"empC {c:.2f} leave", f"payroll_active TARGET {expected:.2f}"]
    elif metric == "ship_ok":
        ls = [title, f"box1 {int(a)} ok", f"box2 {int(b)} ok", f"box3 {int(c)} hold", f"ship_ok TARGET {int(expected)}"]
    elif metric == "sla_ok_hours":
        ls = [title, f"job1 {a:.2f} hours ok", f"job2 {b:.2f} hours ok", f"job3 {c:.2f} hours late", f"sla_ok_hours TARGET {expected:.2f}"]
    elif metric == "exp_sum":
        ls = [title, f"e1 {a:.2f}", f"e2 {b:.2f}", f"e3 {c:.2f} void", f"exp_sum TARGET {expected:.2f}"]
    elif metric == "po_open":
        ls = [title, f"line1 {a:.2f} open", f"line2 {b:.2f} open", f"line3 {c:.2f} closed", f"po_open TARGET {expected:.2f}"]
    elif metric == "order_paid":
        ls = [title, f"skuA {a:.2f} paid", f"skuB {b:.2f} paid", f"skuC {c:.2f} due", f"order_paid TARGET {expected:.2f}"]
    elif metric == "dup_mark":
        ls = [title, f"markA {int(a)}", f"markB {int(b)}", f"markC {int(c)}", f"dup_mark TARGET {int(expected)}"]
    elif metric == "zero_check":
        ls = [title, f"z1 {a:.2f}", f"z2 {b:.2f}", f"z3 {c:.2f}", f"zero_check TARGET {expected:.2f}"]
    elif metric == "ledger_net":
        ls = [title, f"dr {a:.2f}", f"cr {b:.2f}", f"adj {c:.2f}", f"ledger_net TARGET {expected:.2f}"]
    elif metric == "ui_ok":
        ls = [title, f"btnOK {int(a)}", f"btnSkip {int(b)}", f"btnBad {int(c)}", f"ui_ok TARGET {int(expected)}"]
    elif metric == "stack_count":
        ls = [title, f"p1 {int(a)}", f"p2 {int(b)}", f"p3 {int(c)}", f"stack_count TARGET {int(expected)}"]
    elif metric == "fax_pages":
        ls = [title, f"pgA {int(a)}", f"pgB {int(b)}", f"pgC {int(c)} drop", f"fax_pages TARGET {int(expected)}"]
    elif metric == "glare_ok":
        ls = [title, f"zone1 {int(a)} ok", f"zone2 {int(b)}", f"zone3 {int(c)}", f"glare_ok TARGET {int(expected)}"]
    elif metric == "tab_index":
        ls = [title, f"tabA {int(a)}", f"tabB {int(b)}", f"tabC {int(c)}", f"tab_index TARGET {int(expected)}"]
    else:
        raise ValueError(metric)
    return ls


def fmt_spec(prefix, i, expected, nums, ver):
    kind, metric, title, cn, stamp = KINDS[i]
    ls = lines_for(i, ver, expected, nums)
    ls_s = ",\n     ".join(json.dumps(x, ensure_ascii=False) for x in ls)
    return (
        f'    ("{prefix}_{i+1:02d}", "{kind}", "{metric}", {expected!r},\n'
        f"     [{ls_s}],\n"
        f"     {cn!r}, \"{stamp}\"),"
    )


def replace_specs_block(text, new_block, start_marker="SPECS = [", end_marker="\n]\n"):
    i0 = text.index(start_marker)
    i1 = text.index(end_marker, i0)
    return text[:i0] + start_marker + "\n" + new_block + end_marker + text[i1 + len(end_marker):]


def theme_slug():
    return "_".join(k[0].split("_")[0] for k in KINDS)


def main():
    theme = theme_slug()
    old_theme = "flint_velvet_bronze_ivory_sapphire_copper_pewter_willow_mahogany_silk_basalt_ozone_teak_lacquer_quartz_parchment_rivet_canvas"

    # --- design from c371 ---
    src = (SCR / "c371_vision_v44_design_and_batch.py").read_text(encoding="utf-8")
    train_block = "\n".join(fmt_spec("v45", i, TRAIN[i][0], TRAIN[i][1], "V45") for i in range(18))
    t = src
    for a, b in [
        ("C371", "C377"),
        ("c371", "c377"),
        ("V44", "V45"),
        ("v44", "v45"),
        ("vision_images_v45", "vision_images_v45"),
        ("vision_v45_c377", "vision_v45_c377"),
        ("VL_GATE_V45_PROTOCOL", "VL_GATE_V45_PROTOCOL"),
        (old_theme, theme),
        ("v43_marble_linen", "v44_flint_velvet"),
        ("NEW themes vs V43:", "NEW themes vs V44:"),
        ("flint, velvet, bronze, ivory, sapphire, copper, pewter, willow,",
         "ember, frost, granite, amber, cobalt, rust, sage, coral,"),
        ("mahogany, silk, basalt, ozone, teak, lacquer, quartz, parchment, rivet, canvas.",
         "slate, pearl, onyx, moss, cedar, chrome, jade, linen, brass, ink."),
        ('"_v44c371"', '"_v45c377"'),
        ("hash(fid + \"_v44c371\")", "hash(fid + \"_v45c377\")"),
        ("V44 keeps floor", "V45 keeps floor"),
        ("C371 design+fixtures; no VL claim", "C377 design+fixtures; no VL claim"),
    ]:
        t = t.replace(a, b)
    t = replace_specs_block(t, train_block)
    t = re.sub(
        r'PROTO = ROOT / "docs" / "[^"]*VL_GATE_V45_PROTOCOL\.md"',
        'PROTO = ROOT / "docs" / "蚁算_VL_GATE_V45_PROTOCOL.md"',
        t,
        count=1,
    )
    # keep jpeg_q=62
    assert "JPEG_Q = 62" in t
    (SCR / "c377_vision_v45_design_and_batch.py").write_text(t, encoding="utf-8")
    print("wrote c377 design", theme)

    # --- smoke from c372 ---
    s = (SCR / "c372_vision_v44_smoke.py").read_text(encoding="utf-8")
    for a, b in [
        ("C372", "C378"),
        ("c372", "c378"),
        ("V44", "V45"),
        ("v44", "v45"),
        ("vision_images_v45", "vision_images_v45"),
        ("vision_v45_c378", "vision_v45_c378"),
        ("vl_gate_v45_claim", "vl_gate_v45_claim"),
        ("VISION_GATE_V45", "VISION_GATE_V45"),
        ("VISION_V45_SMOKE", "VISION_V45_SMOKE"),
        ("Uses C371 fixtures", "Uses C377 fixtures"),
        ("Uses C377 fixtures with clarity floor", "Uses C377 fixtures with clarity floor"),
    ]:
        s = s.replace(a, b)
    # fix double-bump C371-> already handled if any leftover C372b naming
    s = s.replace("C378b_VISION_GATE_V45_CLAIM.json", "C378b_VISION_GATE_V45_CLAIM.json")
    (SCR / "c378_vision_v45_smoke.py").write_text(s, encoding="utf-8")
    print("wrote c378 smoke")

    # --- heldout from c373 ---
    h = (SCR / "c373_vision_v44_heldout.py").read_text(encoding="utf-8")
    held_block = "\n".join(fmt_spec("v45h", i, HELD[i][0], HELD[i][1], "V45H") for i in range(18))
    h2 = replace_specs_block(h, held_block) if "SPECS = [" in h else h
    for a, b in [
        ("C373", "C379"),
        ("c373", "c379"),
        ("C371", "C377"),
        ("c371", "c377"),
        ("V44", "V45"),
        ("v44", "v45"),
        ("V44H", "V45H"),
        ("v44h", "v45h"),
        ("vision_images_v45h", "vision_images_v45h"),
        ("vision_images_v45", "vision_images_v45"),
        ("vl_gate_v45_heldout_claim", "vl_gate_v45_heldout_claim"),
        ("VISION_GATE_V45_HELDOUT", "VISION_GATE_V45_HELDOUT"),
        ("VISION_V45_HELDOUT", "VISION_V45_HELDOUT"),
        ("VL_GATE_V45_HELDOUT", "VL_GATE_V45_HELDOUT"),
        (old_theme + "_heldout", theme + "_heldout"),
        ("_v44hc373", "_v45hc379"),
        ("Different ids/amounts from V45 train (C377)", "Different ids/amounts from V45 train (C377)"),
        ("Different ids/amounts from V44 train (C371)", "Different ids/amounts from V45 train (C377)"),
        ("Disjoint from V45 train amounts (C377)", "Disjoint from V45 train amounts (C377)"),
        ("Disjoint from V44 train amounts (C254)", "Disjoint from V45 train amounts (C377)"),
    ]:
        h2 = h2.replace(a, b)
    h2 = re.sub(
        r'PROTO = ROOT / "docs" / "[^"]*VL_GATE_V45_HELDOUT_PROTOCOL\.md"',
        'PROTO = ROOT / "docs" / "蚁算_VL_GATE_V45_HELDOUT_PROTOCOL.md"',
        h2,
        count=1,
    )
    assert "JPEG_Q = 62" in h2
    (SCR / "c379_vision_v45_heldout.py").write_text(h2, encoding="utf-8")
    print("wrote c379 heldout")
    print("theme", theme)


if __name__ == "__main__":
    main()
