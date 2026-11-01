# -*- coding: utf-8 -*-
"""Bootstrap Vision V43 scripts (C365-C367) from V42 templates."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCR = ROOT / "scripts"

# New themes vs V41
KINDS = [
    ('marble_recv', 'paid_total', 'MARBLE GRAIN RECV V43', '大理石收款单', 'RECV'),
    ('linen_wh', 'qty_sum', 'WH LINEN BIN V43', '亚麻仓位单', 'RECV'),
    ('crimson_refund', 'refund_done', 'CRIMSON PATCH REFUND V43', '绯红退款单', 'DONE'),
    ('cobalt_tax', 'tax_base_paid', 'COBALT TAX SLIP V43', '钻蓝税基单', 'TAX'),
    ('emerald_pay', 'payroll_active', 'EMERALD PAYROLL V43', '翠绿工资单', 'PAY'),
    ('topaz_ship', 'ship_ok', 'TOPAZ SHIP DOCK V43', '黄玉出库单', 'SHIP'),
    ('chrome_sla', 'sla_ok_hours', 'CHROME SLA CARD V43', '铬片SLA卡', 'SLA'),
    ('fern_exp', 'exp_sum', 'FERN EXPENSE V43', '蕨叶费用单', 'EXP'),
    ('spruce_po', 'po_open', 'SPRUCE PO SHEET V43', '云杉采购单', 'PO'),
    ('pearl_order', 'order_paid', 'PEARL ORDER V43', '珍珠订单', 'ORD'),
    ('shale_dup', 'dup_mark', 'SHALE DUP MARK V43', '页岩重复标', 'DUP'),
    ('vacuum_zero', 'zero_check', 'VACUUM AIR ZERO V43', '真空零值校验', 'ZERO'),
    ('cypress_ledger', 'ledger_net', 'CYPRESS LEDGER V43', '柏木账本', 'LED'),
    ('glaze_ui', 'ui_ok', 'GLAZE UI SCAN V43', '釉面界面扫描', 'UI'),
    ('epoxy_stack', 'stack_count', 'EPOXY STACK V43', '环氧堆叠单', 'STK'),
    ('mint_fax', 'fax_pages', 'MINT FAX V43', '薄荷传真单', 'FAX'),
    ('clay_glare', 'glare_ok', 'CLAY GLARE V43', '陶土眩光单', 'GLR'),
    ('cork_tab', 'tab_index', 'CORK TAB INDEX V43', '软木页签索引', 'TAB'),
]


# Train expected / a,b,c — TARGET is authoritative (ship_ok etc may not equal a+b)
TRAIN = [
    (175.5, (84.0, 91.5, 32.0)),
    (133.0, (54, 44, 59)),
    (108.5, (52.0, 56.5, 23.0)),
    (259.0, (126.0, 133.0, 58.0)),
    (337.0, (165.0, 172.0, 51.0)),
    (91.0, (43, 26, 31)),
    (117.25, (62.0, 55.25, 30.0)),
    (151.75, (72.0, 79.75, 34.0)),
    (169.0, (90.0, 79.0, 40.0)),
    (205.5, (109.0, 96.5, 31.0)),
    (2.0, (1, 1, 0)),
    (0.0, (0.0, 0.0, 0.0)),
    (302.25, (147.0, 155.25, 50.0)),
    (1.0, (1, 0, 0)),
    (19.0, (9, 7, 3)),
    (26.0, (14, 12, 7)),
    (1.0, (1, 0, 0)),
    (36.0, (20, 16, 6)),
]
HELD = [
    (97.25, (46.0, 51.25, 18.0)),
    (76.0, (31, 20, 36)),
    (60.5, (29.0, 31.5, 13.0)),
    (141.0, (68.0, 73.0, 32.0)),
    (179.0, (88.0, 91.0, 28.0)),
    (51.0, (25, 14, 17)),
    (65.75, (35.0, 30.75, 16.0)),
    (83.25, (39.0, 44.25, 19.0)),
    (93.0, (49.0, 44.0, 22.0)),
    (112.5, (60.0, 52.5, 17.0)),
    (2.0, (1, 1, 0)),
    (0.0, (0.0, 0.0, 0.0)),
    (163.5, (79.0, 84.5, 27.0)),
    (1.0, (1, 0, 0)),
    (11.0, (5, 4, 2)),
    (14.0, (8, 6, 3)),
    (1.0, (1, 0, 0)),
    (21.0, (12, 9, 3)),
]


def lines_for(i, ver, expected, nums):
    kind, metric, title, cn, stamp = KINDS[i]
    title = title.replace("V43", ver)
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
    src = (SCR / "c359_vision_v42_design_and_batch.py").read_text(encoding="utf-8")
    train_block = "\n".join(fmt_spec("v43", i, TRAIN[i][0], TRAIN[i][1], "V43") for i in range(18))
    t = src
    reps = [
        ("C359", "C365"),
        ("c359", "c365"),
        ("V41", "V43"),
        ("v42", "v43"),
        ("vision_images_v43", "vision_images_v43"),
        ("vision_v43_c365", "vision_v43_c365"),
        ("VL_GATE_V43_PROTOCOL", "VL_GATE_V43_PROTOCOL"),
        ("marble_linen_crimson_cobalt_emerald_topaz_chrome_fern_spruce_pearl_shale_vacuum_cypress_glaze_epoxy_mint_clay_cork", theme),
        ("v42_obsidian_denim", "v42_obsidian_denim"),
        ("Marble|Linen|Crimson|Cobalt|Emerald|Topaz|Chrome|Fern|Spruce|Pearl|Shale|Vacuum|Cypress|Glaze|Epoxy|Mint|Clay|Cork",
         "Marble|Linen|Crimson|Cobalt|Emerald|Topaz|Chrome|Fern|Spruce|Pearl|Shale|Vacuum|Cypress|Glaze|Epoxy|Mint|Clay|Cork"),
        ("MARBLE bait 43.43", "MARBLE bait 43.43"),
        ("CRIMSON bait 63.63", "CRIMSON bait 63.63"),
        ("LINEN ghost 93.93", "LINEN ghost 93.93"),
        ("EMERALD bait 38.38", "EMERALD bait 38.38"),
        ("SPRUCE bait 29.29", "SPRUCE bait 29.29"),
        ('d.text((880, 138), "TOPAZ"', 'd.text((880, 138), "TOPAZ"'),
        ("CORK bait 73.73", "CORK bait 73.73"),
        ('"_v43c365"', '"_v43c365"'),
        ("hash(fid + \"_v43c365\")", "hash(fid + \"_v43c365\")"),
        ("NEW themes vs V42:", "NEW themes vs V42:"),
        ("marble, linen, crimson, cobalt, emerald, topaz, chrome, fern,", "marble, linen, crimson, cobalt, emerald, topaz, chrome, fern,"),
        # keep jpeg floor
    ]
    for a, b in reps:
        t = t.replace(a, b)
    # fix double-replacements from V41->V42 then protocol path
    t = t.replace("蚁算_VL_GATE_V43_PROTOCOL.md", "蚁算_VL_GATE_V43_PROTOCOL.md") if "蚁算" not in t[t.find("PROTO"):t.find("PROTO")+80] else t
    # SPECS replace
    t = replace_specs_block(t, train_block)
    # V42-only overlay comment
    t = t.replace("# --- V43 overlays (new vs V42) ---", "# --- V43 overlays (new vs V42) ---")
    t = t.replace("# --- V42 overlays kept; V43 overlays follow ---", "# --- V42 overlays kept; V43 overlays follow ---")
    # ensure PROTO path uses Chinese prefix if original had it
    if "PROTO = ROOT" in t:
        t = re.sub(
            r'PROTO = ROOT / "docs" / "[^"]*VL_GATE_V43_PROTOCOL\.md"',
            'PROTO = ROOT / "docs" / "蚁算_VL_GATE_V43_PROTOCOL.md"',
            t,
            count=1,
        )
    (SCR / "c365_vision_v43_design_and_batch.py").write_text(t, encoding="utf-8")
    print("wrote c359", "SPECS" in t, theme)

    # --- smoke from c353 ---
    s = (SCR / "c360_vision_v42_smoke.py").read_text(encoding="utf-8")
    for a, b in [
        ("C360", "C366"), ("c360", "c366"), ("V41", "V43"), ("v42", "v43"),
        ("vision_images_v43", "vision_images_v43"),
        ("vision_v43_c366", "vision_v43_c366"),
        ("vl_gate_v43_claim", "vl_gate_v43_claim"),
        ("VISION_GATE_V43", "VISION_GATE_V43"),
        ("VISION_V43_SMOKE", "VISION_V43_SMOKE"),
        ("r50plus_v43_marble_linen_clarity_floor", "r50plus_v43_marble_linen_clarity_floor"),
        ("Uses C365 fixtures", "Uses C365 fixtures"),
    ]:
        s = s.replace(a, b)
    (SCR / "c366_vision_v43_smoke.py").write_text(s, encoding="utf-8")
    print("wrote c360")

    # --- heldout from c354 ---
    h = (SCR / "c361_vision_v42_heldout.py").read_text(encoding="utf-8")
    held_block = "\n".join(fmt_spec("v43h", i, HELD[i][0], HELD[i][1], "V43H") for i in range(18))
    # heldout uses SPECS differently - check
    if "SPECS = [" in h:
        h2 = replace_specs_block(h, held_block)
    else:
        h2 = h
    for a, b in [
        ("C361", "C367"), ("c361", "c367"), ("C359", "C365"), ("c359", "c365"),
        ("V41", "V43"), ("v42", "v43"), ("V41H", "V43H"), ("v42h", "v43h"),
        ("vision_images_v43h", "vision_images_v43h"),
        ("vision_images_v43", "vision_images_v43"),
        ("vl_gate_v43_heldout_claim", "vl_gate_v43_heldout_claim"),
        ("VISION_GATE_V43_HELDOUT", "VISION_GATE_V43_HELDOUT"),
        ("VISION_V43_HELDOUT", "VISION_V43_HELDOUT"),
        ("VL_GATE_V43_HELDOUT", "VL_GATE_V43_HELDOUT"),
        ("marble_linen_crimson_cobalt_emerald_topaz_chrome_fern_spruce_pearl_shale_vacuum_cypress_glaze_epoxy_mint_clay_cork_heldout", theme + "_heldout"),
        ("v43_train_c365", "v43_train_c365"),
        ("_v43hc367", "_v43hc367"),
        ("r50plus_v42", "r50plus_v42"),
    ]:
        h2 = h2.replace(a, b)
    h2 = re.sub(
        r'PROTO = ROOT / "docs" / "[^"]*VL_GATE_V43_HELDOUT_PROTOCOL\.md"',
        'PROTO = ROOT / "docs" / "蚁算_VL_GATE_V43_HELDOUT_PROTOCOL.md"',
        h2,
        count=1,
    )
    (SCR / "c367_vision_v43_heldout.py").write_text(h2, encoding="utf-8")
    print("wrote c361")

    # V43 clarity: jpeg_q=62 (>=60 floor)
    p365 = SCR / 'c365_vision_v43_design_and_batch.py'
    tt = p365.read_text(encoding='utf-8')
    tt = tt.replace('JPEG_Q = 60', 'JPEG_Q = 62')
    tt = tt.replace('"jpeg_q": 60', '"jpeg_q": 62')
    tt = tt.replace('jpeg_q60', 'jpeg_q62')
    p365.write_text(tt, encoding='utf-8')
    p367 = SCR / 'c367_vision_v43_heldout.py'
    hh = p367.read_text(encoding='utf-8')
    hh = hh.replace('JPEG_Q = 60', 'JPEG_Q = 62')
    p367.write_text(hh, encoding='utf-8')

    print("theme", theme)


if __name__ == "__main__":
    main()
