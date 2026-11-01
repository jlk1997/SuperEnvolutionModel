# -*- coding: utf-8 -*-
"""Bootstrap Vision V42 scripts (C359-C361) from V41 templates."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCR = ROOT / "scripts"

# New themes vs V41
KINDS = [
    ("obsidian_recv", "paid_total", "OBSIDIAN GRAIN RECV V42", "黑曜收款单", "RECV"),
    ("denim_wh", "qty_sum", "WH DENIM BIN V42", "牛仔仓位单", "RECV"),
    ("coral_refund", "refund_done", "CORAL PATCH REFUND V42", "珊瑚退款单", "DONE"),
    ("indigo_tax", "tax_base_paid", "INDIGO TAX SLIP V42", "靛蓝税基单", "TAX"),
    ("jade_pay", "payroll_active", "JADE PAYROLL V42", "翡翠工资单", "PAY"),
    ("amber_ship", "ship_ok", "AMBER SHIP DOCK V42", "琥珀出库单", "SHIP"),
    ("nickel_sla", "sla_ok_hours", "NICKEL SLA CARD V42", "镍片SLA卡", "SLA"),
    ("moss_exp", "exp_sum", "MOSS EXPENSE V42", "苔藓费用单", "EXP"),
    ("pine_po", "po_open", "PINE PO SHEET V42", "松木采购单", "PO"),
    ("opal_order", "order_paid", "OPAL ORDER V42", "蛋白石订单", "ORD"),
    ("granite_dup", "dup_mark", "GRANITE DUP MARK V42", "花岗岩重复标", "DUP"),
    ("void_zero", "zero_check", "VOID AIR ZERO V42", "空值校验单", "ZERO"),
    ("cedar_ledger", "ledger_net", "CEDAR LEDGER V42", "雪松账本", "LED"),
    ("enamel_ui", "ui_ok", "ENAMEL UI SCAN V42", "搪瓷界面扫描", "UI"),
    ("resin_stack", "stack_count", "RESIN STACK V42", "树脂堆垛单", "STK"),
    ("sage_fax", "fax_pages", "SAGE FAX V42", "鼠尾草传真单", "FAX"),
    ("terra_glare", "glare_ok", "TERRA GLARE V42", "陶土眩光单", "GLR"),
    ("hazel_tab", "tab_index", "HAZEL TAB INDEX V42", "榛木页签索引", "TAB"),
]

# Train expected / a,b,c — TARGET is authoritative (ship_ok etc may not equal a+b)
TRAIN = [
    (168.75, (81.00, 87.75, 30.00)),
    (127.0, (51, 42, 56)),
    (101.25, (49.00, 52.25, 21.00)),
    (248.0, (121.00, 127.00, 55.00)),
    (322.0, (158.00, 164.00, 48.00)),
    (86.0, (41, 24, 29)),
    (111.75, (59.00, 52.75, 28.00)),
    (144.5, (69.00, 75.50, 32.00)),
    (161.0, (86.00, 75.00, 38.00)),
    (196.25, (104.00, 92.25, 29.00)),
    (2.0, (1, 1, 0)),
    (0.0, (0.00, 0.00, 0.00)),
    (289.5, (141.00, 148.50, 47.00)),
    (1.0, (1, 0, 0)),
    (18.0, (8, 7, 3)),
    (24.0, (13, 11, 6)),
    (1.0, (1, 0, 0)),
    (34.0, (19, 15, 5)),
]
HELD = [
    (92.5, (44.00, 48.50, 17.00)),
    (71.0, (29, 18, 34)),
    (56.75, (27.00, 29.75, 12.00)),
    (134.0, (65.00, 69.00, 30.00)),
    (171.0, (84.00, 87.00, 26.00)),
    (47.0, (23, 13, 16)),
    (61.25, (33.00, 28.25, 15.00)),
    (78.5, (37.00, 41.50, 18.00)),
    (88.0, (47.00, 41.00, 20.00)),
    (106.75, (57.00, 49.75, 16.00)),
    (2.0, (1, 1, 0)),
    (0.0, (0.00, 0.00, 0.00)),
    (155.25, (75.00, 80.25, 25.00)),
    (1.0, (1, 0, 0)),
    (10.0, (4, 4, 2)),
    (13.0, (7, 6, 3)),
    (1.0, (1, 0, 0)),
    (19.0, (11, 8, 3)),
]


def lines_for(i, ver, expected, nums):
    kind, metric, title, cn, stamp = KINDS[i]
    title = title.replace("V42", ver)
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
    ls_s = ",\n     ".join(json_str(x) for x in ls)
    # use repr for cn to keep unicode
    return (
        f'    ("{prefix}_{i+1:02d}", "{kind}", "{metric}", {expected!r},\n'
        f"     [{ls_s}],\n"
        f"     {cn!r}, \"{stamp}\"),"
    )


def json_str(s):
    return json.dumps(s, ensure_ascii=False)


import json


def replace_specs_block(text, new_block, start_marker="SPECS = [", end_marker="\n]\n"):
    i0 = text.index(start_marker)
    i1 = text.index(end_marker, i0)
    return text[:i0] + start_marker + "\n" + new_block + end_marker + text[i1 + len(end_marker):]


def theme_slug():
    return "_".join(k[0].split("_")[0] for k in KINDS)


def main():
    theme = theme_slug()
    # --- design from c352 ---
    src = (SCR / "c352_vision_v41_design_and_batch.py").read_text(encoding="utf-8")
    train_block = "\n".join(fmt_spec("v42", i, TRAIN[i][0], TRAIN[i][1], "V42") for i in range(18))
    t = src
    reps = [
        ("C352", "C359"),
        ("c352", "c359"),
        ("V41", "V42"),
        ("v41", "v42"),
        ("vision_images_v41", "vision_images_v42"),
        ("vision_v41_c352", "vision_v42_c359"),
        ("VL_GATE_V41_PROTOCOL", "VL_GATE_V42_PROTOCOL"),
        ("basalt_velvet_bronze_silk_graphite_flint_pewter_gauze_walnut_mica_slate_air_bamboo_lacquer_quartz_parchment_rivet_canvas", theme),
        ("v40_teak_onyx_chiffon", "v41_basalt_velvet"),
        ("Basalt|Velvet|Bronze|Silk|Graphite|Flint|Pewter|Gauze|Walnut|Mica|Slate|Air|Bamboo|Lacquer|Quartz|Parchment|Rivet|Canvas",
         "Obsidian|Denim|Coral|Indigo|Jade|Amber|Nickel|Moss|Pine|Opal|Granite|Void|Cedar|Enamel|Resin|Sage|Terra|Hazel"),
        ("BASALT bait 41.41", "OBSIDIAN bait 42.42"),
        ("BRONZE bait 61.61", "CORAL bait 62.62"),
        ("VELVET ghost 91.91", "DENIM ghost 92.92"),
        ("GRAPHITE bait 36.36", "JADE bait 37.37"),
        ("WALNUT bait 27.27", "PINE bait 28.28"),
        ('d.text((880, 138), "FLINT"', 'd.text((880, 138), "AMBER"'),
        ("RIVET bait 71.71", "HAZEL bait 72.72"),
        ('"_v41c352"', '"_v42c359"'),
        ("hash(fid + \"_v41c352\")", "hash(fid + \"_v42c359\")"),
        ("NEW themes vs V40:", "NEW themes vs V41:"),
        ("basalt, velvet, bronze, silk, graphite, flint, pewter, gauze,", "obsidian, denim, coral, indigo, jade, amber, nickel, moss,"),
        # keep jpeg floor
    ]
    for a, b in reps:
        t = t.replace(a, b)
    # fix double-replacements from V41->V42 then protocol path
    t = t.replace("VL_GATE_V42_PROTOCOL.md", "蚁算_VL_GATE_V42_PROTOCOL.md") if "蚁算" not in t[t.find("PROTO"):t.find("PROTO")+80] else t
    # SPECS replace
    t = replace_specs_block(t, train_block)
    # V42-only overlay comment
    t = t.replace("# --- V41 overlays (new vs V40) ---", "# --- V42 overlays (new vs V41) ---")
    t = t.replace("# --- V40 overlays kept; V41 overlays follow ---", "# --- V41 overlays kept; V42 overlays follow ---")
    # ensure PROTO path uses Chinese prefix if original had it
    if "PROTO = ROOT" in t:
        t = re.sub(
            r'PROTO = ROOT / "docs" / "[^"]*VL_GATE_V42_PROTOCOL\.md"',
            'PROTO = ROOT / "docs" / "蚁算_VL_GATE_V42_PROTOCOL.md"',
            t,
            count=1,
        )
    (SCR / "c359_vision_v42_design_and_batch.py").write_text(t, encoding="utf-8")
    print("wrote c359", "SPECS" in t, theme)

    # --- smoke from c353 ---
    s = (SCR / "c353_vision_v41_smoke.py").read_text(encoding="utf-8")
    for a, b in [
        ("C353", "C360"), ("c353", "c360"), ("V41", "V42"), ("v41", "v42"),
        ("vision_images_v41", "vision_images_v42"),
        ("vision_v41_c353", "vision_v42_c360"),
        ("vl_gate_v41_claim", "vl_gate_v42_claim"),
        ("VISION_GATE_V41", "VISION_GATE_V42"),
        ("VISION_V41_SMOKE", "VISION_V42_SMOKE"),
        ("r50plus_v41_teak_onyx_clarity_floor", "r50plus_v42_obsidian_denim_clarity_floor"),
        ("Uses C352 fixtures", "Uses C359 fixtures"),
    ]:
        s = s.replace(a, b)
    (SCR / "c360_vision_v42_smoke.py").write_text(s, encoding="utf-8")
    print("wrote c360")

    # --- heldout from c354 ---
    h = (SCR / "c354_vision_v41_heldout.py").read_text(encoding="utf-8")
    held_block = "\n".join(fmt_spec("v42h", i, HELD[i][0], HELD[i][1], "V42H") for i in range(18))
    # heldout uses SPECS differently - check
    if "SPECS = [" in h:
        h2 = replace_specs_block(h, held_block)
    else:
        h2 = h
    for a, b in [
        ("C354", "C361"), ("c354", "c361"), ("C352", "C359"), ("c352", "c359"),
        ("V41", "V42"), ("v41", "v42"), ("V41H", "V42H"), ("v41h", "v42h"),
        ("vision_images_v41h", "vision_images_v42h"),
        ("vision_images_v41", "vision_images_v42"),
        ("vl_gate_v41_heldout_claim", "vl_gate_v42_heldout_claim"),
        ("VISION_GATE_V41_HELDOUT", "VISION_GATE_V42_HELDOUT"),
        ("VISION_V41_HELDOUT", "VISION_V42_HELDOUT"),
        ("VL_GATE_V41_HELDOUT", "VL_GATE_V42_HELDOUT"),
        ("basalt_velvet_bronze_silk_graphite_flint_pewter_gauze_walnut_mica_slate_air_bamboo_lacquer_quartz_parchment_rivet_canvas_heldout", theme + "_heldout"),
        ("v41_train_c352", "v42_train_c359"),
        ("_v41hc354", "_v42hc361"),
        ("r50plus_v41", "r50plus_v42"),
    ]:
        h2 = h2.replace(a, b)
    h2 = re.sub(
        r'PROTO = ROOT / "docs" / "[^"]*VL_GATE_V42_HELDOUT_PROTOCOL\.md"',
        'PROTO = ROOT / "docs" / "蚁算_VL_GATE_V42_HELDOUT_PROTOCOL.md"',
        h2,
        count=1,
    )
    (SCR / "c361_vision_v42_heldout.py").write_text(h2, encoding="utf-8")
    print("wrote c361")
    print("theme", theme)


if __name__ == "__main__":
    main()
