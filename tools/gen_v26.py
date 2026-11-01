# -*- coding: utf-8 -*-
"""Generate C260-C265 scripts for Vision V26 + non-vision strengthen."""
from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else r"E:\envolution")
SCR = ROOT / "scripts"

src = (SCR / "c254_vision_v25_design_and_batch.py").read_text(encoding="utf-8")

NEW_SPECS = '''SPECS = [
    ("v26_01", "hl_recv", "paid_total", 91.5,
     ["HIGHLIGHTER BLEED RECV V26", "a paid 44.00", "b paid 47.50", "c open 13.00", "TOTAL PAID TARGET 91.50"],
     "荧光笔污收据", "RECV"),
    ("v26_02", "crumple_wh", "qty_sum", 81.0,
     ["WH CRUMPLE CORNER V26", "SKU1 qty 39 ok", "SKU2 qty 18 hold", "SKU3 qty 42 ok", "qty_sum TARGET 81"],
     "皱角仓单", "RECV"),
    ("v26_03", "rubber_refund", "refund_done", 52.75,
     ["RUBBER BAND REFUND V26", "itemR1 25.00 done", "itemR2 27.75 done", "itemR3 11.00 open", "refund_done TARGET 52.75"],
     "橡皮筋退款", "DONE"),
    ("v26_04", "clip_tax", "tax_base_paid", 156.0,
     ["TAX PAPERCLIP SHADOW V26", "T1 88.00 paid", "T2 35.00 open", "T3 68.00 paid", "tax_base_paid TARGET 156.00"],
     "回形针税基", "RECV"),
    ("v26_05", "grease_pay", "payroll_active", 2680.0,
     ["PAYROLL GREASE SMEAR V26", "A 1380 active", "B 260 leave", "C 1300 active", "payroll_active TARGET 2680"],
     "油渍工资", "OK"),
    ("v26_06", "carbon_ship", "ship_ok_qty", 71.0,
     ["SHIP CARBON COPY V26", "P1 36 ok", "P2 19 hold", "P3 35 ok", "ship_ok_qty TARGET 71"],
     "复写发货", "SHIP"),
    ("v26_07", "stamp_sla", "open_pri_sum", 67.0,
     ["SLA STAMP OVERLAP V26", "S1 pri 28 open", "S2 pri 31 closed", "S3 pri 39 open", "open_pri_sum TARGET 67"],
     "叠章SLA", "OPEN"),
    ("v26_08", "pocket_exp", "paid_total", 118.25,
     ["EXPENSE FOLDED POCKET V26", "E1 58.00 paid", "E2 22.00 void", "E3 60.25 paid", "paid_total TARGET 118.25"],
     "折袋报销", "RECV"),
    ("v26_09", "dust_po", "paid_total", 88.0,
     ["PO-DUST SPECKLE V26", "itemA paid 42.00", "itemB paid 46.00", "itemC open 15.00", "TOTAL PAID TARGET 88.00"],
     "灰尘采购", "RECV"),
    ("v26_10", "binder_order", "paid_total", 76.5,
     ["ORDER BINDER HOLE V26", "A paid 37.00", "B paid 39.50", "C open 12.00", "TOTAL PAID TARGET 76.50"],
     "装订孔订单", "RECV"),
    ("v26_11", "perf_dup", "paid_total", 99.0,
     ["INVOICE #V26-PERF", "line paid 33.00", "line paid 33.00", "line paid 33.00", "TOTAL PAID TARGET 99.00"],
     "齿孔重复", "RECV"),
    ("v26_12", "polaroid_zero", "paid_total", 0.0,
     ["OPEN ONLY V26", "X 64.00 open", "Y 67.00 open", "paid_total TARGET 0.00"],
     "宝丽来未付", "HOLD"),
    ("v26_13", "wb_ledger", "paid_total", 66.25,
     ["LEDGER WHITEBOARD GLARE V26", "rA paid 32.00", "rB paid 34.25", "rC open 9.00", "TOTAL PAID TARGET 66.25"],
     "白板反光台账", "RECV"),
    ("v26_14", "sticky_ui", "paid_total", 71.0,
     ["UI STICKY NOTE COVER V26", "alpha paid 34.50", "beta paid 36.50", "gamma open 12.00", "TOTAL PAID TARGET 71.00"],
     "便利贴窗口", "RECV"),
    ("v26_15", "pen_stack", "paid_total", 104.5,
     ["HEAVY PEN UNDERLINE V26", "x paid 51.00 usd", "y paid 53.50 usd", "z open 18.00 usd", "TOTAL PAID TARGET 104.50"],
     "笔迹下划线堆单", "RECV"),
    ("v26_16", "fax_mix", "paid_total", 63.5,
     ["CN-EN FAX HEADER V26", "tea paid 31.00", "rice paid 32.50", "soup open 10.00", "TOTAL PAID TARGET 63.50"],
     "传真头中英", "RECV"),
    ("v26_17", "env_win", "paid_total", 79.0,
     ["ENVELOPE WINDOW V26", "w1 paid 38.00", "w2 paid 41.00", "w3 open 16.00", "TOTAL PAID TARGET 79.00"],
     "信封窗双栏", "RECV"),
    ("v26_18", "laminate_foot", "paid_total", 48.75,
     ["LAMINATE SHINE FOOT V26", "p1 paid 23.50", "p2 paid 25.25", "p3 open 8.00", "TOTAL PAID TARGET 48.75"],
     "覆膜脚注", "RECV"),
]
'''

out = src
out = out.replace("C254", "C260").replace("c254", "c260")
out = out.replace("V25", "V26").replace("v25", "v26").replace("V24", "V25").replace("v24", "v25")

m = re.search(r"SPECS = \[.*?\]\n", out, re.S)
if not m:
    raise SystemExit("SPECS not found")
out = out[:m.start()] + NEW_SPECS + out[m.end():]

out = out.replace(
    "fingerprint smudge, rain streak, staple shadow, QR bait,\nreceipt curl, fluorescent flare, desk clutter, ink bleed stamp, torn margin,\nzigzag crease, tape+coffee combo, barcode edge, mild moire, water ring stack.",
    "highlighter bleed, crumpled corner, rubber band, paperclip shadow,\ngrease smear, carbon copy, stamp overlap, folded pocket, dust speckle,\nbinder hole, ticket perforation, polaroid frame, whiteboard glare,\nsticky-note cover, pen underline noise, fax header bait, envelope window, laminate shine."
)
out = out.replace(
    "fp_rain_staple_qr_curl_flare_clutter_ink_torn_zig_combo_barcode_moire_rings",
    "hl_crumple_rubber_clip_grease_carbon_stamp_pocket_dust_binder_perf_polaroid_wb_sticky_pen_fax_env_laminate"
)
out = out.replace("v26_coffee_binder_tape_pen_c248", "v25_fp_rain_staple_c254")
out = out.replace("v25_coffee_binder_tape_pen_c248", "v25_fp_rain_staple_c254")
out = out.replace("C255 VL", "C261 VL")
out = out.replace('hash(fid + "_v25c254")', 'hash(fid + "_v26c260")')
out = out.replace("C254 design+fixtures", "C260 design+fixtures")
out = out.replace(
    '"""C260: Vision V26 design + fixtures (harder than V26, clarity floor).\nNEW themes vs V26:',
    '"""C260: Vision V26 design + fixtures (harder than V25, clarity floor).\nNEW themes vs V25:'
)

inject = '''
    # --- V26 overlays (new vs V25) ---
    for hx in range(60, 520, 40):
        d.rectangle([hx, 255, hx + 22, 275], fill=(255, 250, 120))
    d.line([(55, 80), (520, 560)], fill=(40, 40, 50), width=3)
    d.line([(58, 78), (523, 558)], fill=(90, 90, 100), width=1)
    d.rectangle([500, 30, 545, 70], outline=(70, 70, 90), width=2)
    d.ellipse([505, 28, 540, 42], outline=(70, 70, 90), width=2)
    for (gx, gy) in [(120, 480), (480, 520), (300, 560)]:
        d.ellipse([gx - 30, gy - 18, gx + 30, gy + 18], fill=(200, 190, 160))
    for by in (100, 220, 340, 460):
        d.ellipse([18, by, 36, by + 18], fill=bg, outline=(40, 40, 40), width=2)
    d.rectangle([780, 180, 980, 280], fill=(255, 255, 150), outline=(180, 180, 40), width=2)
    d.text((800, 210), "STICKY bait 55.55", fill=(120, 100, 20), font=f_tiny)
    d.text((760, 30), "FAX HEADER bait 88.88 FROM:SPOOF", fill=(40, 40, 120), font=f_fax)
    for sy in (50, 150, 450):
        d.rectangle([50, sy, 540, sy + 8], fill=(255, 255, 255))
'''

marker = "    # staple shadow top-left\n    d.ellipse([48, 28, 78, 48], fill=(90, 90, 100))\n    d.ellipse([52, 32, 74, 44], fill=(60, 60, 70))\n"
if marker in out:
    out = out.replace(marker, marker + inject, 1)
else:
    out = out.replace("    # fingerprint ovals", inject + "\n    # fingerprint ovals", 1)

(SCR / "c260_vision_v26_design_and_batch.py").write_text(out, encoding="utf-8")
print("wrote c260", len(out))

s = (SCR / "c255_vision_v25_smoke.py").read_text(encoding="utf-8")
s = s.replace("C255", "C261").replace("c255", "c261")
s = s.replace("V25", "V26").replace("v25", "v26")
s = s.replace(
    "r50plus_v26_fp_rain_staple_n>=16_qwen35_2b_clarity_floor",
    "r50plus_v26_hl_crumple_rubber_n>=16_qwen35_2b_clarity_floor",
)
s = s.replace(
    "r50plus_v25_fp_rain_staple_n>=16_qwen35_2b_clarity_floor",
    "r50plus_v26_hl_crumple_rubber_n>=16_qwen35_2b_clarity_floor",
)
(SCR / "c261_vision_v26_smoke.py").write_text(s, encoding="utf-8")
print("wrote c261")

h = (SCR / "c256_vision_v25_heldout.py").read_text(encoding="utf-8")
h = h.replace("C256", "C262").replace("c256", "c262")
h = h.replace("V25", "V26").replace("v25", "v26")

HELDOUT_SPECS = '''SPECS = [
    ("v26h_01", "hl_recv", "paid_total", 64.5,
     ["HIGHLIGHTER BLEED RECV V26H", "a paid 31.00", "b paid 33.50", "c open 9.00", "TOTAL PAID TARGET 64.50"],
     "荧光笔污收据H", "RECV"),
    ("v26h_02", "crumple_wh", "qty_sum", 54.0,
     ["WH CRUMPLE CORNER V26H", "SKU1 qty 26 ok", "SKU2 qty 12 hold", "SKU3 qty 28 ok", "qty_sum TARGET 54"],
     "皱角仓单H", "RECV"),
    ("v26h_03", "rubber_refund", "refund_done", 37.25,
     ["RUBBER BAND REFUND V26H", "itemR1 17.00 done", "itemR2 20.25 done", "itemR3 7.00 open", "refund_done TARGET 37.25"],
     "橡皮筋退款H", "DONE"),
    ("v26h_04", "clip_tax", "tax_base_paid", 121.0,
     ["TAX PAPERCLIP SHADOW V26H", "T1 68.00 paid", "T2 27.00 open", "T3 53.00 paid", "tax_base_paid TARGET 121.00"],
     "回形针税基H", "RECV"),
    ("v26h_05", "grease_pay", "payroll_active", 2110.0,
     ["PAYROLL GREASE SMEAR V26H", "A 1090 active", "B 210 leave", "C 1020 active", "payroll_active TARGET 2110"],
     "油渍工资H", "OK"),
    ("v26h_06", "carbon_ship", "ship_ok_qty", 41.0,
     ["SHIP CARBON COPY V26H", "P1 21 ok", "P2 11 hold", "P3 20 ok", "ship_ok_qty TARGET 41"],
     "复写发货H", "SHIP"),
    ("v26h_07", "stamp_sla", "open_pri_sum", 49.0,
     ["SLA STAMP OVERLAP V26H", "S1 pri 20 open", "S2 pri 24 closed", "S3 pri 29 open", "open_pri_sum TARGET 49"],
     "叠章SLAH", "OPEN"),
    ("v26h_08", "pocket_exp", "paid_total", 84.75,
     ["EXPENSE FOLDED POCKET V26H", "E1 41.00 paid", "E2 16.00 void", "E3 43.75 paid", "paid_total TARGET 84.75"],
     "折袋报销H", "RECV"),
    ("v26h_09", "dust_po", "paid_total", 55.0,
     ["PO-DUST SPECKLE V26H", "itemA paid 26.00", "itemB paid 29.00", "itemC open 10.00", "TOTAL PAID TARGET 55.00"],
     "灰尘采购H", "RECV"),
    ("v26h_10", "binder_order", "paid_total", 58.5,
     ["ORDER BINDER HOLE V26H", "A paid 28.00", "B paid 30.50", "C open 9.00", "TOTAL PAID TARGET 58.50"],
     "装订孔订单H", "RECV"),
    ("v26h_11", "perf_dup", "paid_total", 72.0,
     ["INVOICE #V26H-PERF", "line paid 24.00", "line paid 24.00", "line paid 24.00", "TOTAL PAID TARGET 72.00"],
     "齿孔重复H", "RECV"),
    ("v26h_12", "polaroid_zero", "paid_total", 0.0,
     ["OPEN ONLY V26H", "X 45.00 open", "Y 48.00 open", "paid_total TARGET 0.00"],
     "宝丽来未付H", "HOLD"),
    ("v26h_13", "wb_ledger", "paid_total", 49.25,
     ["LEDGER WHITEBOARD GLARE V26H", "rA paid 24.00", "rB paid 25.25", "rC open 7.00", "TOTAL PAID TARGET 49.25"],
     "白板反光台账H", "RECV"),
    ("v26h_14", "sticky_ui", "paid_total", 40.5,
     ["UI STICKY NOTE COVER V26H", "alpha paid 19.50", "beta paid 21.00", "gamma open 8.00", "TOTAL PAID TARGET 40.50"],
     "便利贴窗口H", "RECV"),
    ("v26h_15", "pen_stack", "paid_total", 78.0,
     ["HEAVY PEN UNDERLINE V26H", "x paid 38.00 usd", "y paid 40.00 usd", "z open 14.00 usd", "TOTAL PAID TARGET 78.00"],
     "笔迹下划线堆单H", "RECV"),
    ("v26h_16", "fax_mix", "paid_total", 46.5,
     ["CN-EN FAX HEADER V26H", "tea paid 23.00", "rice paid 23.50", "soup open 7.00", "TOTAL PAID TARGET 46.50"],
     "传真头中英H", "RECV"),
    ("v26h_17", "env_win", "paid_total", 57.0,
     ["ENVELOPE WINDOW V26H", "w1 paid 28.00", "w2 paid 29.00", "w3 open 11.00", "TOTAL PAID TARGET 57.00"],
     "信封窗双栏H", "RECV"),
    ("v26h_18", "laminate_foot", "paid_total", 33.75,
     ["LAMINATE SHINE FOOT V26H", "p1 paid 16.25", "p2 paid 17.50", "p3 open 6.00", "TOTAL PAID TARGET 33.75"],
     "覆膜脚注H", "RECV"),
]
'''
m = re.search(r"SPECS = \[.*?\]\n", h, re.S)
if not m:
    raise SystemExit("heldout SPECS not found")
h = h[:m.start()] + HELDOUT_SPECS + h[m.end():]
h = h.replace('hash(fid + "_v25hc256")', 'hash(fid + "_v26hc262")')
h = h.replace(
    "Same fp/rain/staple/qr/curl/flare/clutter/ink/torn/zig family",
    "Same hl/crumple/rubber/clip/grease/carbon/stamp/pocket family",
)
(SCR / "c262_vision_v26_heldout.py").write_text(h, encoding="utf-8")
print("wrote c262")
print("DONE design/smoke/heldout")
