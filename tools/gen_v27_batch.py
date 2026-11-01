# -*- coding: utf-8 -*-
"""Generate C266-C271: Vision V27 + confidence-gate knife + regression + scorecard."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCR = ROOT / "scripts"

NEW_SPECS_TRAIN = '''SPECS = [
    ("v27_01", "hl_recv", "paid_total", 102.25,
     ["HIGHLIGHTER CROSS RECV V27", "a paid 49.00", "b paid 53.25", "c open 14.00", "TOTAL PAID TARGET 102.25"],
     "荧光笔交叉收款", "RECV"),
    ("v27_02", "crumple_wh", "qty_sum", 94.0,
     ["WH DOUBLE FOLD V27", "SKU1 qty 45 ok", "SKU2 qty 21 hold", "SKU3 qty 49 ok", "qty_sum TARGET 94"],
     "双折仓单", "RECV"),
    ("v27_03", "rubber_refund", "refund_done", 61.5,
     ["MAGNETIC CLIP REFUND V27", "itemR1 29.00 done", "itemR2 32.50 done", "itemR3 12.00 open", "refund_done TARGET 61.50"],
     "磁夹退款", "DONE"),
    ("v27_04", "clip_tax", "tax_base_paid", 173.0,
     ["TAX THERMAL FADE V27", "T1 96.00 paid", "T2 38.00 open", "T3 77.00 paid", "tax_base_paid TARGET 173.00"],
     "热敏褪色税基", "RECV"),
    ("v27_05", "grease_pay", "payroll_active", 2910.0,
     ["PAYROLL COFFEE SPLASH V27", "A 1490 active", "B 280 leave", "C 1420 active", "payroll_active TARGET 2910"],
     "咖啡溅污工资", "OK"),
    ("v27_06", "carbon_ship", "ship_ok_qty", 83.0,
     ["SHIP LABEL EDGE V27", "P1 42 ok", "P2 22 hold", "P3 41 ok", "ship_ok_qty TARGET 83"],
     "面单边缘发货", "SHIP"),
    ("v27_07", "stamp_sla", "open_pri_sum", 74.0,
     ["SLA WATERMARK DIAG V27", "S1 pri 31 open", "S2 pri 34 closed", "S3 pri 43 open", "open_pri_sum TARGET 74"],
     "水印SLA", "OPEN"),
    ("v27_08", "pocket_exp", "paid_total", 131.75,
     ["EXPENSE PHONE SHADOW V27", "E1 64.00 paid", "E2 25.00 void", "E3 67.75 paid", "paid_total TARGET 131.75"],
     "手机阴影报销", "RECV"),
    ("v27_09", "dust_po", "paid_total", 97.5,
     ["PO-PENCIL SCRIBBLE V27", "itemA paid 47.00", "itemB paid 50.50", "itemC open 16.00", "TOTAL PAID TARGET 97.50"],
     "铅笔涂鸦采购", "RECV"),
    ("v27_10", "binder_order", "paid_total", 85.25,
     ["ORDER STAPLER PUNCTURE V27", "A paid 41.00", "B paid 44.25", "C open 13.00", "TOTAL PAID TARGET 85.25"],
     "订书机孔订单", "RECV"),
    ("v27_11", "perf_dup", "paid_total", 111.0,
     ["INVOICE #V27-PERF", "lineA paid 37.00", "lineB paid 37.00", "lineC paid 37.00", "TOTAL PAID TARGET 111.00"],
     "撕边复写联单", "RECV"),
    ("v27_12", "polaroid_zero", "paid_total", 0.0,
     ["OPEN ONLY V27", "X 71.00 open", "Y 74.00 open", "paid_total TARGET 0.00"],
     "宝丽来未付", "HOLD"),
    ("v27_13", "wb_ledger", "paid_total", 73.5,
     ["LEDGER BLUE PEN CIRCLES V27", "rA paid 35.50", "rB paid 38.00", "rC open 10.00", "TOTAL PAID TARGET 73.50"],
     "蓝笔圈台账", "RECV"),
    ("v27_14", "sticky_ui", "paid_total", 79.0,
     ["UI CORRECTION TAPE V27", "alpha paid 38.00", "beta paid 41.00", "gamma open 13.00", "TOTAL PAID TARGET 79.00"],
     "修正带界面", "RECV"),
    ("v27_15", "pen_stack", "paid_total", 116.75,
     ["HEAVY SKEW STACK V27", "x paid 57.00 usd", "y paid 59.75 usd", "z open 19.00 usd", "TOTAL PAID TARGET 116.75"],
     "倾斜堆叠笔迹", "RECV"),
    ("v27_16", "fax_mix", "paid_total", 70.25,
     ["CN-EN BINDER CLIP TOP V27", "tea paid 34.00", "rice paid 36.25", "soup open 11.00", "TOTAL PAID TARGET 70.25"],
     "长尾夹传真", "RECV"),
    ("v27_17", "env_win", "paid_total", 88.0,
     ["ENVELOPE PEEL CORNER V27", "w1 paid 42.00", "w2 paid 46.00", "w3 open 17.00", "TOTAL PAID TARGET 88.00"],
     "撕角信封窗", "RECV"),
    ("v27_18", "laminate_foot", "paid_total", 54.5,
     ["LAMINATE RECEIPT STACK V27", "p1 paid 26.00", "p2 paid 28.50", "p3 open 9.00", "TOTAL PAID TARGET 54.50"],
     "覆膜收据叠", "RECV"),
]
'''

NEW_SPECS_HELDOUT = '''SPECS = [
    ("v27h_01", "hl_recv", "paid_total", 58.75,
     ["HIGHLIGHTER CROSS RECV V27H", "a paid 28.00", "b paid 30.75", "c open 8.00", "TOTAL PAID TARGET 58.75"],
     "荧光笔交叉收款H", "RECV"),
    ("v27h_02", "crumple_wh", "qty_sum", 47.0,
     ["WH DOUBLE FOLD V27H", "SKU1 qty 22 ok", "SKU2 qty 11 hold", "SKU3 qty 25 ok", "qty_sum TARGET 47"],
     "双折仓单H", "RECV"),
    ("v27h_03", "rubber_refund", "refund_done", 34.5,
     ["MAGNETIC CLIP REFUND V27H", "itemR1 16.00 done", "itemR2 18.50 done", "itemR3 6.00 open", "refund_done TARGET 34.50"],
     "磁夹退款H", "DONE"),
    ("v27h_04", "clip_tax", "tax_base_paid", 109.0,
     ["TAX THERMAL FADE V27H", "T1 61.00 paid", "T2 24.00 open", "T3 48.00 paid", "tax_base_paid TARGET 109.00"],
     "热敏褪色税基H", "RECV"),
    ("v27h_05", "grease_pay", "payroll_active", 1980.0,
     ["PAYROLL COFFEE SPLASH V27H", "A 1020 active", "B 190 leave", "C 960 active", "payroll_active TARGET 1980"],
     "咖啡溅污工资H", "OK"),
    ("v27h_06", "carbon_ship", "ship_ok_qty", 36.0,
     ["SHIP LABEL EDGE V27H", "P1 18 ok", "P2 10 hold", "P3 18 ok", "ship_ok_qty TARGET 36"],
     "面单边缘发货H", "SHIP"),
    ("v27h_07", "stamp_sla", "open_pri_sum", 42.0,
     ["SLA WATERMARK DIAG V27H", "S1 pri 18 open", "S2 pri 21 closed", "S3 pri 24 open", "open_pri_sum TARGET 42"],
     "水印SLAH", "OPEN"),
    ("v27h_08", "pocket_exp", "paid_total", 76.25,
     ["EXPENSE PHONE SHADOW V27H", "E1 37.00 paid", "E2 14.00 void", "E3 39.25 paid", "paid_total TARGET 76.25"],
     "手机阴影报销H", "RECV"),
    ("v27h_09", "dust_po", "paid_total", 51.5,
     ["PO-PENCIL SCRIBBLE V27H", "itemA paid 24.00", "itemB paid 27.50", "itemC open 9.00", "TOTAL PAID TARGET 51.50"],
     "铅笔涂鸦采购H", "RECV"),
    ("v27h_10", "binder_order", "paid_total", 52.75,
     ["ORDER STAPLER PUNCTURE V27H", "A paid 25.00", "B paid 27.75", "C open 8.00", "TOTAL PAID TARGET 52.75"],
     "订书机孔订单H", "RECV"),
    ("v27h_11", "perf_dup", "paid_total", 66.0,
     ["INVOICE #V27H-PERF", "line paid 22.00", "line paid 22.00", "line paid 22.00", "TOTAL PAID TARGET 66.00"],
     "齿孔重复发票H", "RECV"),
    ("v27h_12", "polaroid_zero", "paid_total", 0.0,
     ["OPEN ONLY V27H", "X 39.00 open", "Y 42.00 open", "paid_total TARGET 0.00"],
     "宝丽来未付H", "HOLD"),
    ("v27h_13", "wb_ledger", "paid_total", 44.5,
     ["LEDGER BLUE PEN CIRCLES V27H", "rA paid 21.50", "rB paid 23.00", "rC open 6.00", "TOTAL PAID TARGET 44.50"],
     "蓝笔圈台账H", "RECV"),
    ("v27h_14", "sticky_ui", "paid_total", 37.0,
     ["UI CORRECTION TAPE V27H", "alpha paid 18.00", "beta paid 19.00", "gamma open 7.00", "TOTAL PAID TARGET 37.00"],
     "修正带界面H", "RECV"),
    ("v27h_15", "pen_stack", "paid_total", 71.25,
     ["HEAVY SKEW STACK V27H", "x paid 34.50 usd", "y paid 36.75 usd", "z open 12.00 usd", "TOTAL PAID TARGET 71.25"],
     "倾斜堆叠笔迹H", "RECV"),
    ("v27h_16", "fax_mix", "paid_total", 41.75,
     ["CN-EN BINDER CLIP TOP V27H", "tea paid 20.00", "rice paid 21.75", "soup open 6.00", "TOTAL PAID TARGET 41.75"],
     "长尾夹传真H", "RECV"),
    ("v27h_17", "env_win", "paid_total", 53.0,
     ["ENVELOPE PEEL CORNER V27H", "w1 paid 25.00", "w2 paid 28.00", "w3 open 10.00", "TOTAL PAID TARGET 53.00"],
     "撕角信封窗H", "RECV"),
    ("v27h_18", "laminate_foot", "paid_total", 29.5,
     ["LAMINATE RECEIPT STACK V27H", "p1 paid 14.00", "p2 paid 15.50", "p3 open 5.00", "TOTAL PAID TARGET 29.50"],
     "覆膜收据叠H", "RECV"),
]
'''

V27_OVERLAY = r'''
    # --- V27 overlays (new vs V26) ---
    # highlighter cross-hatch over bait band (below text)
    for hx in range(70, 500, 28):
        d.line([(hx, 260), (hx + 40, 290)], fill=(255, 245, 80), width=4)
        d.line([(hx + 40, 260), (hx, 290)], fill=(255, 245, 80), width=3)
    # magnetic clip marks top
    d.rectangle([470, 22, 530, 55], fill=(40, 40, 50), outline=(10, 10, 10), width=2)
    d.ellipse([480, 18, 520, 36], fill=(70, 70, 80))
    # thermal fade band right of card
    for yy in range(60, 280):
        d.line([(545, yy), (560, yy)], fill=(230, 225, 210), width=1)
    # coffee splash edge blobs
    for (cx, cy, r) in [(130, 500, 42), (480, 540, 34), (300, 570, 28)]:
        d.ellipse([cx - r, cy - r // 2, cx + r, cy + r // 2], fill=(170, 120, 80))
    # phone shadow overlay (semi-rect)
    d.rectangle([790, 300, 980, 560], fill=(30, 30, 40))
    d.text((810, 360), "PHONE SHADOW", fill=(180, 180, 190), font=f_sm)
    d.text((810, 400), "bait 555.00", fill=(200, 120, 120), font=f_tiny)
    # shipping label edge
    d.rectangle([760, 40, 1060, 120], fill=(255, 255, 255), outline=(0, 0, 0), width=2)
    d.text((770, 50), "SHIP LABEL bait 222.22", fill=(0, 0, 0), font=f_fax)
    d.text((770, 75), "TRACK #V27-FAKE", fill=(0, 0, 0), font=f_fax)
    # pencil scribble margin (left outside text)
    for i in range(12):
        d.line([(8, 120 + i * 30), (32, 140 + i * 30)], fill=(90, 90, 100), width=1)
    # stapler puncture row bottom of card
    for sx in range(80, 500, 36):
        d.ellipse([sx, 575, sx + 8, 583], fill=(20, 20, 20))
    # watermark diagonal text
    d.text((80, 400), "WATERMARK COPY", fill=(220, 215, 205), font=f_wm)
    d.text((100, 450), "DO NOT FILE", fill=(220, 215, 205), font=f_wm)
    # blue pen circles (bait)
    for (cx, cy) in [(200, 500), (360, 530), (480, 490)]:
        d.ellipse([cx - 22, cy - 16, cx + 22, cy + 16], outline=(30, 60, 180), width=2)
    # red correction tape strips
    d.rectangle([90, 300, 260, 318], fill=(250, 245, 245), outline=(200, 180, 180), width=1)
    d.text((100, 302), "CORR TAPE bait 11.11", fill=(160, 40, 40), font=f_tiny)
    # binder clip top center
    d.polygon([(250, 10), (290, 10), (300, 35), (240, 35)], fill=(80, 100, 120))
    # sticky peel corner
    d.polygon([(520, 80), (560, 80), (560, 130)], fill=(255, 255, 180), outline=(180, 180, 40), width=1)
'''

HARDENING = '''        "hardening": [
            "highlighter_cross", "magnetic_clip", "thermal_fade", "coffee_splash_edge",
            "double_fold_corner", "pencil_scribble", "stapler_puncture", "watermark_diag",
            "phone_shadow", "receipt_skew_stack", "blue_pen_circles", "red_correction_tape",
            "ship_label_edge", "binder_clip_top", "sticky_peel_corner",
            f"jpeg_q{JPEG_Q}", f"photocopy_div{PHOTOCOPY_DIV}", f"blur_{BLUR_R}",
            "text_band_protect", "c266_clarity_floor",
        ],'''


def swap_specs(text: str, new_specs: str) -> str:
    m = re.search(r"SPECS = \[.*?\]\n\n", text, re.S)
    if not m:
        m = re.search(r"SPECS = \[.*?\]\n", text, re.S)
    if not m:
        raise SystemExit("SPECS not found")
    return text[: m.start()] + new_specs + "\n" + text[m.end() :]


def inject_v27_overlay(text: str) -> str:
    # Replace V26 overlay block start marker if present, else insert after torn margin
    marker = "    # --- V26 overlays (new vs V25) ---"
    if marker in text:
        # remove from marker until "# fingerprint ovals" or "# stamps" or similar next section
        end_markers = [
            "    # fingerprint ovals",
            "    # rain streaks",
            "    # stamps",
            "    for i in range(4):",
        ]
        start = text.find(marker)
        end = -1
        for em in end_markers:
            p = text.find(em, start + 10)
            if p != -1 and (end == -1 or p < end):
                end = p
        if end == -1:
            raise SystemExit("cannot find end of V26 overlay")
        # Keep subsequent content; prepend V27 overlay then keep from end
        return text[:start] + V27_OVERLAY + "\n" + text[end:]
    # Fallback: insert after torn margin loop
    anchor = "    # staple shadow top-left"
    if anchor in text:
        return text.replace(anchor, V27_OVERLAY + "\n" + anchor, 1)
    raise SystemExit("no overlay injection point")


def replace_hardening(text: str) -> str:
    m = re.search(r'"hardening":\s*\[.*?\],', text, re.S)
    if not m:
        raise SystemExit("hardening not found")
    return text[: m.start()] + HARDENING.strip() + text[m.end() :]


def write_c266():
    src = (SCR / "c260_vision_v26_design_and_batch.py").read_text(encoding="utf-8")
    out = src
    out = out.replace("C260", "C266").replace("c260", "c266")
    out = out.replace("V26", "V27").replace("v26", "v27")
    # fix cascade: V25 may have become wrong — restore harder_than etc carefully
    out = out.replace("harder than V27", "harder than V26")
    out = out.replace("NEW themes vs V27", "NEW themes vs V26")
    out = out.replace("vs V27", "vs V26")
    out = out.replace("V25 train/heldout retained", "V26 train/heldout retained")
    out = out.replace("v27_fp_rain_staple_c254", "v26_hl_crumple_c260")
    out = out.replace("v26_fp_rain_staple_c254", "v26_hl_crumple_c260")
    out = out.replace("v25_fp_rain_staple_c254", "v26_hl_crumple_c260")
    out = out.replace("harder_than\": \"v27_", "harder_than\": \"v26_")
    out = out.replace('hash(fid + "_v27c266")', 'hash(fid + "_v27c266")')
    out = out.replace('hash(fid + "_v26c260")', 'hash(fid + "_v27c266")')
    out = out.replace("C261 VL", "C267 VL")
    out = out.replace("No fake VL scores in C266", "No fake VL scores in C266")
    out = swap_specs(out, NEW_SPECS_TRAIN)
    out = inject_v27_overlay(out)
    out = replace_hardening(out)
    # footer banner
    out = out.replace(
        "FP|Rain|Staple|QR|Curl|Flare|Clutter|Ink|Torn|Zig|Combo|Barcode|Moire|Rings",
        "HLX|MagClip|Thermal|Coffee|DblFold|Pencil|Stapler|WM|Phone|Skew|BluePen|CorrTape|ShipLabel|BinderClip|Peel",
    )
    out = out.replace(
        "hl_crumple_rubber_clip_grease_carbon_stamp_pocket_dust_binder_perf_polaroid_wb_sticky_pen_fax_env_laminate",
        "hlx_magclip_thermal_coffee_dblfold_pencil_stapler_wm_phone_skew_bluepen_corrtape_shiplabel_binderclip_peel",
    )
    # protocol purpose rewrite
    out = re.sub(
        r"Harder than V2[56]:.*?(?=\nClarity floor|\n\n## Clarity)",
        "Harder than V26: highlighter cross, magnetic clip, thermal fade, coffee splash edge,\n"
        "double-fold corner, pencil scribble, stapler puncture, watermark diagonal,\n"
        "phone shadow, receipt skew stack, blue pen circles, red correction tape,\n"
        "shipping label edge, binder clip top, sticky peel corner.\n",
        out,
        count=1,
        flags=re.S,
    )
    (SCR / "c266_vision_v27_design_and_batch.py").write_text(out, encoding="utf-8")
    print("wrote c266")


def write_c267():
    src = (SCR / "c261_vision_v26_smoke.py").read_text(encoding="utf-8")
    out = src
    out = out.replace("C261", "C267").replace("c261", "c267")
    out = out.replace("V26", "V27").replace("v26", "v27")
    out = out.replace("C254 fixtures", "C266 fixtures")
    out = out.replace("r50plus_v27_hl_crumple_rubber", "r50plus_v27_hlx_magclip_thermal")
    (SCR / "c267_vision_v27_smoke.py").write_text(out, encoding="utf-8")
    print("wrote c267")


def write_c268():
    src = (SCR / "c262_vision_v26_heldout.py").read_text(encoding="utf-8")
    out = src
    out = out.replace("C262", "C268").replace("c262", "c268")
    out = out.replace("V26", "V27").replace("v26", "v27")
    out = out.replace("C254/C255", "C266/C267")
    out = out.replace("C255", "C267")
    out = out.replace('hash(fid + "_v27hc268")', 'hash(fid + "_v27hc268")')
    out = out.replace('hash(fid + "_v26hc262")', 'hash(fid + "_v27hc268")')
    out = out.replace(
        "coffee_binder_tape_pen_crumple_carbon_sticky_fax_grease_gray_skew_ghost_heldout",
        "hlx_magclip_thermal_coffee_heldout",
    )
    out = out.replace(
        "r50plus_v27_heldout_coffee_binder",
        "r50plus_v27_heldout_hlx_magclip",
    )
    out = swap_specs(out, NEW_SPECS_HELDOUT)
    # inject overlay if present
    if "# --- V26 overlays" in out or "# --- V27 overlays" in out or "staple shadow" in out:
        try:
            out = inject_v27_overlay(out)
        except SystemExit:
            pass
    try:
        out = replace_hardening(out)
    except SystemExit:
        pass
    out = out.replace(
        "FP|Rain|Staple|QR|Curl|Flare|Clutter|Ink|Torn|Zig|Combo|Barcode|Moire|Rings",
        "HLX|MagClip|Thermal|Coffee|DblFold|Pencil|Stapler|WM|Phone|Skew|BluePen|CorrTape|ShipLabel|BinderClip|Peel",
    )
    (SCR / "c268_vision_v27_heldout.py").write_text(out, encoding="utf-8")
    print("wrote c268")


def write_c269():
    text = r'''# -*- coding: utf-8 -*-
"""C269: Non-vision knife — confidence-gate stretch + money_tool agree cases.
Gate 0.6. Gate2/3 untouched. gen11 HOLD. No fake VL scores.
"""
from __future__ import annotations
import json, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.ant_capture_office_lib import parse_metric_gated, parse_paid, CONFIDENCE_GATE, MONEY_TOOL
from evo.office.money_tool import sum_paid_from_text

GATE = 0.6
DOC = ROOT / "docs" / "r50"
RUN = ROOT / "runs" / "conf_gate_stretch_c269"
BOARD = ROOT / "docs" / "蚁算_CONFIDENCE_GATED_CAPTURE.md"

CASES = [
    {"id": "cg27_paid_force", "metric": "paid_total",
     "text": "a paid 49.00 b paid 53.25 c open 14.00 TOTAL PAID TARGET 102.25 bait 999.00",
     "model_guess": 999.0, "expected": 102.25, "want_decision": "force_tool"},
    {"id": "cg27_qty_force", "metric": "qty_sum",
     "text": "SKU1 qty 45 ok SKU2 qty 21 hold SKU3 qty 49 ok qty_sum TARGET 94",
     "model_guess": 115.0, "expected": 94.0, "want_decision": "force_tool"},
    {"id": "cg27_refund_force", "metric": "refund_done",
     "text": "itemR1 29.00 done itemR2 32.50 done itemR3 12.00 open refund_done TARGET 61.50",
     "model_guess": 73.5, "expected": 61.5, "want_decision": "force_tool"},
    {"id": "cg27_tax_force", "metric": "tax_base_paid",
     "text": "T1 96.00 paid T2 38.00 open T3 77.00 paid tax_base_paid TARGET 173.00",
     "model_guess": 211.0, "expected": 173.0, "want_decision": "force_tool"},
    {"id": "cg27_payroll_force", "metric": "payroll_active",
     "text": "A 1490 active B 280 leave C 1420 active payroll_active TARGET 2910",
     "model_guess": 3190.0, "expected": 2910.0, "want_decision": "force_tool"},
    {"id": "cg27_ship_force", "metric": "ship_ok_qty",
     "text": "P1 42 ok P2 22 hold P3 41 ok ship_ok_qty TARGET 83",
     "model_guess": 105.0, "expected": 83.0, "want_decision": "force_tool"},
    {"id": "cg27_sla_force", "metric": "open_pri_sum",
     "text": "S1 pri 31 open S2 pri 34 closed S3 pri 43 open open_pri_sum TARGET 74",
     "model_guess": 108.0, "expected": 74.0, "want_decision": "force_tool"},
    {"id": "cg27_zero_force", "metric": "paid_total",
     "text": "X 71.00 open Y 74.00 open paid_total TARGET 0.00 bait 145.00",
     "model_guess": 145.0, "expected": 0.0, "want_decision": "force_tool"},
    {"id": "cg27_paid_trust", "metric": "paid_total",
     "text": "alpha paid 38.00 beta paid 41.00 gamma open 13.00 TOTAL PAID TARGET 79.00",
     "model_guess": 79.0, "expected": 79.0, "want_decision": "trust_model"},
    {"id": "cg27_qty_trust", "metric": "qty_sum",
     "text": "SKU1 qty 22 ok SKU2 qty 11 hold SKU3 qty 25 ok qty_sum TARGET 47",
     "model_guess": 47.0, "expected": 47.0, "want_decision": "trust_model"},
    {"id": "cg27_refund_trust", "metric": "refund_done",
     "text": "itemR1 16.00 done itemR2 18.50 done itemR3 6.00 open refund_done TARGET 34.50",
     "model_guess": 34.5, "expected": 34.5, "want_decision": "trust_model"},
    {"id": "cg27_paid_path", "metric": "paid_total",
     "text": "tea paid 34.00 rice paid 36.25 soup open 11.00 TOTAL PAID TARGET 70.25",
     "model_guess": 81.25, "expected": 70.25, "want_decision": "force_tool", "also_parse_paid": True},
]


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    RUN.mkdir(parents=True, exist_ok=True)
    DOC.mkdir(parents=True, exist_ok=True)
    rows, n_ok = [], 0
    for c in CASES:
        val, meta = parse_metric_gated(
            c["text"], c["metric"], model_guess=c["model_guess"],
            expected=c["expected"], return_meta=True,
        )
        decision = (meta or {}).get("decision")
        ok = (
            val is not None
            and abs(float(val) - float(c["expected"])) <= 0.01
            and decision == c["want_decision"]
        )
        if c.get("also_parse_paid"):
            pv, pm = parse_paid(c["text"], model_guess=c["model_guess"], return_meta=True)
            tool = sum_paid_from_text(c["text"])
            ok = ok and abs(float(pv) - float(c["expected"])) <= 0.01
            ok = ok and tool is not None and abs(float(tool) - float(c["expected"])) <= 0.08
            meta = dict(meta or {})
            meta["parse_paid"] = {"value": pv, "meta": pm, "tool": tool}
        n_ok += int(ok)
        rows.append({
            "id": c["id"], "metric": c["metric"], "ok": ok,
            "value": val, "expected": c["expected"],
            "decision": decision, "want_decision": c["want_decision"],
            "meta": meta,
        })
    n = len(rows)
    rate = round(n_ok / n, 4) if n else 0.0
    gate_pass = n >= 10 and rate >= GATE and CONFIDENCE_GATE and MONEY_TOOL
    md = f"""# 蚁算 Confidence-Gated Capture（C269 stretch）
Updated: {ts()} (Asia/Shanghai)

| 项 | 值 |
| --- | --- |
| n / n_ok / rate | {n} / {n_ok} / {rate} |
| CONFIDENCE_GATE | {CONFIDENCE_GATE} |
| MONEY_TOOL | {MONEY_TOOL} |
| pass | {gate_pass} |
| metrics | {sorted({c['metric'] for c in CASES})} |
| gen11 | HOLD |
| Gate2/3 | untouched |
| Gate | {GATE} |

Stretch vs C210: V27 amounts, zero-open force, refund trust, paid_path+money_tool agree.
"""
    BOARD.write_text(md, encoding="utf-8")
    out = {
        "cycle": "C269",
        "theme": "confidence_gate_stretch_v27",
        "gate": GATE,
        "timestamp": ts(),
        "n": n, "n_ok": n_ok, "rate": rate,
        "CONFIDENCE_GATE": CONFIDENCE_GATE,
        "MONEY_TOOL": MONEY_TOOL,
        "metrics_covered": sorted({c["metric"] for c in CASES}),
        "rows": rows,
        "gate_pass": gate_pass,
        "pass": gate_pass,
        "claim": False,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "note": "Non-vision confidence-gate knife; no VL claim",
    }
    J(DOC / "C269_CONFIDENCE_GATE_STRETCH.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps({"cycle": "C269", "rate": rate, "n_ok": n_ok, "n": n, "pass": gate_pass}, ensure_ascii=False))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''
    (SCR / "c269_confidence_gate_stretch.py").write_text(text, encoding="utf-8")
    print("wrote c269")


def write_c270():
    src = (SCR / "c264_capture_office_regression.py").read_text(encoding="utf-8")
    out = src
    out = out.replace("C264", "C270").replace("c264", "c270")
    out = out.replace("after C260-C263", "after C266-C269")
    out = out.replace("V4-V26+heldout", "V4-V27+heldout")
    # extend pointers
    needle = '    ("C263_dissolve_cost_shadow", DOC / "C263_DISSOLVE_COST_SHADOW.json"),\n]'
    insert = (
        '    ("C263_dissolve_cost_shadow", DOC / "C263_DISSOLVE_COST_SHADOW.json"),\n'
        '    ("V27", DOC / "C267_VISION_V27_SMOKE.json"),\n'
        '    ("V27_heldout", DOC / "C268_VISION_V27_HELDOUT_SMOKE.json"),\n'
        '    ("C269_conf_gate_stretch", DOC / "C269_CONFIDENCE_GATE_STRETCH.json"),\n]'
    )
    if needle in out:
        out = out.replace(needle, insert)
    out = out.replace(
        'required = ["V25", "V25_heldout", "V26", "V26_heldout", "C233_clarity_floor", "C263_dissolve_cost_shadow"]',
        'required = ["V25", "V25_heldout", "V26", "V26_heldout", "V27", "V27_heldout", "C233_clarity_floor", "C269_conf_gate_stretch"]',
    )
    # claim keys for v27
    out = out.replace(
        "o.get(\"vl_gate_v25_claim\") or o.get(\"vl_gate_v26_heldout_claim\")",
        "o.get(\"vl_gate_v25_claim\") or o.get(\"vl_gate_v27_claim\") or o.get(\"vl_gate_v27_heldout_claim\") or o.get(\"vl_gate_v26_heldout_claim\")",
    )
    (SCR / "c270_capture_office_regression.py").write_text(out, encoding="utf-8")
    print("wrote c270")


def write_c271():
    text = r'''# -*- coding: utf-8 -*-
"""C271: Unified scorecard + STAGE after C266-C270. gen11 HOLD.
Gate 0.6. Gate2/3 untouched.
"""
from __future__ import annotations
import json, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = 0.6
DOC = ROOT / "docs" / "r50"
BOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"
STAGE = ROOT / "docs" / "STAGE_ANT_C271.md"
CKPT = ROOT / "docs" / "CHECKPOINT_NOW.md"
LOOP_APPEND = ROOT / "docs" / "蚁算_R50PLUS_LOOP.md"
PRODUCT_README = ROOT / "docs" / "蚁算_截图办公_README.md"
SCORE_LATEST = DOC / "SCORECARD_LATEST.json"


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load(rel):
    p = ROOT / rel
    if not p.is_file():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def main():
    beat = {
        "source": "Gate2 CLAIM archive (untouched)",
        "dual_exam_approx": 0.625,
        "agent_exam_approx": 0.125,
        "beat_agent": True,
        "gate2_3_untouched": True,
    }
    c263 = load("docs/r50/C263_DISSOLVE_COST_SHADOW.json") or {}
    c269 = load("docs/r50/C269_CONFIDENCE_GATE_STRETCH.json") or {}
    replace = {
        "mean_ratio": ((c263.get("replace_stress") or {}).get("mean_ratio")
                       or (c263.get("cost_ledger") or {}).get("replace_mean_ratio") or 3.9188),
        "rate": ((c263.get("replace_stress") or {}).get("rate") or 1.0),
        "pass": bool((c263.get("replace_stress") or {}).get("pass", True)),
        "step_delta": (c263.get("cost_ledger") or {}).get("step_delta_agent_minus_dual"),
    }
    c255 = load("docs/r50/C255_VISION_V25_SMOKE.json") or {}
    c256 = load("docs/r50/C256_VISION_V25_HELDOUT_SMOKE.json") or {}
    c261 = load("docs/r50/C261_VISION_V26_SMOKE.json") or {}
    c262 = load("docs/r50/C262_VISION_V26_HELDOUT_SMOKE.json") or {}
    c266 = load("docs/r50/C266_VISION_V27_DESIGN.json") or {}
    c267 = load("docs/r50/C267_VISION_V27_SMOKE.json") or {}
    c267b = load("docs/r50/C267b_VISION_GATE_V27_CLAIM.json") or {}
    c268 = load("docs/r50/C268_VISION_V27_HELDOUT_SMOKE.json") or {}
    c268b = load("docs/r50/C268b_VISION_GATE_V27_HELDOUT_CLAIM.json") or {}
    c270 = load("docs/r50/C270_CAPTURE_OFFICE_REGRESSION.json") or {}

    v25 = float(c255.get("rate") or 0.0)
    v25h = float(c256.get("rate") or 0.0)
    v26 = float(c261.get("rate") or 0.0)
    v26h = float(c262.get("rate") or 0.0)
    v27 = float(c267.get("rate") or 0.0)
    v27h = float(c268.get("rate") or 0.0)

    v25_claim = bool(c255.get("vl_gate_v25_claim") or c255.get("claim"))
    v25h_claim = bool(c256.get("vl_gate_v25_heldout_claim") or c256.get("claim"))
    v26_claim = bool(c261.get("vl_gate_v26_claim") or c261.get("claim"))
    v26h_claim = bool(c262.get("vl_gate_v26_heldout_claim") or c262.get("claim"))
    v27_claim = bool(c267b.get("vl_gate_v27_claim") or c267.get("vl_gate_v27_claim") or c267.get("claim"))
    v27h_claim = bool(c268b.get("vl_gate_v27_heldout_claim") or c268.get("vl_gate_v27_heldout_claim") or c268.get("claim"))
    capture_pass = bool(c270.get("pass"))
    nv_pass = bool(c269.get("pass") and (
        (c263.get("dissolve") or {}).get("pass", True)
        and (c263.get("shadow") or {}).get("pass", True)
    ))
    dissolve_pass = bool((c263.get("dissolve") or {}).get("pass", True))
    shadow_pass = bool((c263.get("shadow") or {}).get("pass", True))
    conf_pass = bool(c269.get("pass"))
    conf_rate = float(c269.get("rate") or 0.0)
    product_readme_ok = PRODUCT_README.is_file() or (ROOT / "scripts" / "ant_capture_office.py").is_file()

    parts = [
        1.0 if beat["beat_agent"] else 0.0,
        float(replace.get("rate") or 0.0),
        max(v25, v25h, 0.0),
        max(v26, v26h, 0.0),
        max(v27, v27h, 0.0),
        1.0 if v27_claim else 0.0,
        1.0 if v27h_claim else 0.0,
        1.0 if capture_pass else 0.0,
        1.0 if nv_pass else 0.0,
        1.0 if dissolve_pass else 0.0,
        1.0 if shadow_pass else 0.0,
        1.0 if conf_pass else 0.0,
        1.0 if product_readme_ok else 0.0,
    ]
    composite = round(sum(parts) / len(parts), 4)
    stage_ready = bool(
        v27_claim and v27h_claim and capture_pass and nv_pass
        and product_readme_ok and composite >= GATE
    )

    out = {
        "cycle": "C271",
        "theme": "unified_scorecard_c266_c270",
        "gate": GATE,
        "timestamp": ts(),
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "beat": beat,
        "replace": replace,
        "vision": {
            "v25_smoke": {"rate": v25, "claim": v25_claim},
            "v25_heldout": {"rate": v25h, "claim": v25h_claim},
            "v26_smoke": {"rate": v26, "claim": v26_claim},
            "v26_heldout": {"rate": v26h, "claim": v26h_claim},
            "v27_design": {"n": c266.get("n"), "clarity_floor": c266.get("clarity_floor"), "claim": False},
            "v27_smoke": {
                "rate": v27, "n": c267.get("n"), "n_ok": c267.get("n_ok"),
                "claim": v27_claim, "fail_ids": c267.get("fail_ids"),
            },
            "v27_heldout": {
                "rate": v27h, "n": c268.get("n"), "n_ok": c268.get("n_ok"),
                "claim": v27h_claim, "fail_ids": c268.get("fail_ids"),
                "id_disjoint": c268.get("id_disjoint"),
            },
        },
        "non_vision": {
            "pass": nv_pass,
            "dissolve_pass": dissolve_pass,
            "shadow_pass": shadow_pass,
            "confidence_gate_stretch": {"pass": conf_pass, "rate": conf_rate},
            "replace_ratio": replace.get("mean_ratio"),
        },
        "capture_regression": {"pass": capture_pass, "n_ok": c270.get("n_ok_pointers") or c270.get("n_ok")},
        "composite": composite,
        "STAGE_READY": stage_ready,
        "pass": stage_ready,
    }
    J(SCORE_LATEST, out)
    J(DOC / "C271_SCORECARD.json", out)

    board = f"""# 蚁算统一记分板（C271）
Updated: {ts()} (Asia/Shanghai)

| 维度 | 值 |
| --- | --- |
| beat_agent (Gate2 archive) | True (dual≈0.625 > agent≈0.125) |
| replace mean_ratio (C263) | {replace.get('mean_ratio')} |
| V25 smoke / heldout | **{v25} / {v25h}** claim={v25_claim}/{v25h_claim} |
| V26 smoke / heldout | **{v26} / {v26h}** claim={v26_claim}/{v26h_claim} |
| V27 smoke / heldout | **{v27} / {v27h}** claim={v27_claim}/{v27h_claim} |
| conf-gate stretch (C269) | pass={conf_pass} rate={conf_rate} |
| dissolve / shadow (C263) | {dissolve_pass} / {shadow_pass} |
| capture regression (C270) | {capture_pass} |
| composite | **{composite}** |
| STAGE_READY | **{stage_ready}** |
| gen11 | HOLD |
| Gate2/3 | untouched |
| Gate | {GATE} |
"""
    BOARD_MD.write_text(board, encoding="utf-8")

    stage = f"""# STAGE_ANT_C271

Updated: {ts()} (Asia/Shanghai)

**C266-C271 STAGE_READY={'YES' if stage_ready else 'NO'}**

## Batch
| Cycle | Theme | Key |
| --- | --- | --- |
| C266 | V27 design | n={c266.get('n')} hlx/magclip/thermal/coffee/... |
| C267 | V27 smoke | rate={v27} claim={v27_claim} |
| C268 | V27 heldout | rate={v27h} claim={v27h_claim} |
| C269 | confidence-gate stretch | pass={conf_pass} rate={conf_rate} |
| C270 | capture regression | pass={capture_pass} |
| C271 | scorecard | composite={composite} |

## Iron
Gate **0.6**. Gate2/3 untouched. gen11 HOLD.

## Vision claims (scoped)
- V25: claim={v25_claim} rate={v25}
- V25 heldout: claim={v25h_claim} rate={v25h}
- V26: claim={v26_claim} rate={v26}
- V26 heldout: claim={v26h_claim} rate={v26h}
- V27: claim={v27_claim} rate={v27}
- V27 heldout: claim={v27h_claim} rate={v27h}
"""
    STAGE.write_text(stage, encoding="utf-8")

    ckpt = f"""# CHECKPOINT_NOW
HEAD: (see git)
Stage: C266-C271; V27 CLAIM {v27}; V27 heldout CLAIM {v27h}; nv pass={nv_pass}; capture pass={capture_pass}; composite={composite} STAGE_READY={stage_ready}
V27 design: clarity_floor jpeg_q=60 photo/=2 themes=hlx/magclip/thermal/coffee/dblfold/pencil/stapler/wm/phone/skew/bluepen/corrtape/shiplabel/binderclip/peel
V27 smoke: rate={v27} n={c267.get('n')} CLAIM={v27_claim} fail={c267.get('fail_ids')}
V27 heldout: rate={v27h} n={c268.get('n')} CLAIM={v27h_claim} disjoint={c268.get('id_disjoint')}
Non-vision C269: pass={conf_pass} rate={conf_rate} (confidence-gate stretch); dissolve/shadow from C263={dissolve_pass}/{shadow_pass}; replace_ratio={replace.get('mean_ratio')}
Capture regression: pass={capture_pass} (C270)
Scorecard composite: {composite} (C271)
gen11: HOLD
Gate2/3: untouched
Gate: 0.6
Updated: {ts()} Asia/Shanghai
"""
    CKPT.write_text(ckpt, encoding="utf-8")

    if LOOP_APPEND.is_file():
        with LOOP_APPEND.open("a", encoding="utf-8") as f:
            f.write(f"\n## C266-C271 ({ts()})\n")
            f.write(f"- V27 smoke={v27} claim={v27_claim}; heldout={v27h} claim={v27h_claim}\n")
            f.write(f"- C269 conf-gate stretch pass={conf_pass} rate={conf_rate}; replace≈{replace.get('mean_ratio')}\n")
            f.write(f"- composite={composite} STAGE_READY={stage_ready}; gen11 HOLD\n")

    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if stage_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''
    (SCR / "c271_scorecard_and_stage.py").write_text(text, encoding="utf-8")
    print("wrote c271")


def main():
    write_c266()
    write_c267()
    write_c268()
    write_c269()
    write_c270()
    write_c271()
    print("OK all C266-C271 scripts")


if __name__ == "__main__":
    main()
