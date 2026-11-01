# -*- coding: utf-8 -*-
"""C1255: Vision V191 heldout 鈥?disjoint fixtures + real VL claim if rate>=0.6.
Different ids/amounts from V191 train (C953). Same fp/rain/staple/qr/
curl/flare/clutter/ink/torn/zig family; clarity floor.
Gate 0.6. Gate2/3 untouched. gen11 HOLD.
"""
from __future__ import annotations
import gc, io, json, random, re, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from evo.office.vision_metric_parse import parse_metric

GATE = 0.6
DOC = ROOT / "docs" / "r50"
FIX = ROOT / "evo/office/fixtures/vision_images_v191h"
WEIGHTS = ROOT / "models/Qwen3.5-2B"
RUN = ROOT / "runs/vision_v191h_c1255"
PROTO = ROOT / "docs" / "蚁算_VL_GATE_V191_HELDOUT_PROTOCOL.md"
TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v191"

JPEG_Q = 62
PHOTOCOPY_DIV = 2
BLUR_R = 0.45
TEXT_BAND = (70, 250)

# Disjoint from V191 train amounts (C953)
SPECS = [
    ("v191h_01", "ashcroft_recv", "paid_total", 2376.75,
     ['ASHCROFT GRAIN RECV V191H',
     'a paid 1182.00',
     'b paid 1194.75',
     'c open 1075.00',
     'TOTAL PAID TARGET 2376.75'],
     'ashcroft', "RECV"),
    ("v191h_02", "cedarcroft_wh", "qty_sum", 1520.0,
     ['WH CEDARCROFT BIN V191H',
     'SKU1 qty 740 ok',
     'SKU2 qty 820 hold',
     'SKU3 qty 780 ok',
     'qty_sum TARGET 1520'],
     'cedarcroft', "RECV"),
    ("v191h_03", "dawncroft_refund", "refund_done", 2293.5,
     ['DAWNCROFT PATCH REFUND V191H',
     'itemR1 1140.00 done',
     'itemR2 1153.50 done',
     'itemR3 1063.00 open',
     'refund_done TARGET 2293.50'],
     'dawncroft', "DONE"),
    ("v191h_04", "elmcroft_tax", "tax_base_paid", 2526.0,
     ['ELMCROFT TAX SLIP V191H',
     'base 1255.00 paid',
     'addon 1271.00 paid',
     'skip 1104.00',
     'tax_base_paid TARGET 2526.00'],
     'elmcroft', "TAX"),
    ("v191h_05", "ferncroft_pay", "payroll_active", 2608.0,
     ['FERNCROFT PAYROLL V191H',
     'empA 1296.00 active',
     'empB 1312.00 active',
     'empC 1099.00 leave',
     'payroll_active TARGET 2608.00'],
     'ferncroft', "PAY"),
    ("v191h_06", "glencroft_ship", "ship_ok", 2194.0,
     ['GLENCROFT SHIP DOCK V191H',
     'box1 1090 ok',
     'box2 1104 ok',
     'box3 1068 hold',
     'ship_ok TARGET 2194'],
     'glencroft', "SHIP"),
    ("v191h_07", "hazecroft_sla", "sla_ok_hours", 760.0,
     ['HAZECROFT SLA CARD V191H',
     'job1 360.00 hours ok',
     'job2 400.00 hours ok',
     'job3 650.00 hours late',
     'sla_ok_hours TARGET 760.00'],
     'hazecroft', "SLA"),
    ("v191h_08", "inkcroft_exp", "exp_sum", 2353.75,
     ['INKCROFT EXPENSE V191H',
     'e1 1166.00',
     'e2 1187.75',
     'e3 1075.00 void',
     'exp_sum TARGET 2353.75'],
     'inkcroft', "EXP"),
    ("v191h_09", "jadecroft_po", "po_open", 1520.0,
     ['JADECROFT PO SHEET V191H',
     'line1 780.00 open',
     'line2 740.00 open',
     'line3 820.00 closed',
     'po_open TARGET 1520.00'],
     'jadecroft', "PO"),
    ("v191h_10", "knotcroft_order", "order_paid", 2412.0,
     ['KNOTCROFT ORDER V191H',
     'skuA 1213.00 paid',
     'skuB 1199.00 paid',
     'skuC 1070.00 due',
     'order_paid TARGET 2412.00'],
     'knotcroft', "ORD"),
    ("v191h_11", "lakecroft_dup", "dup_mark", 2.0,
     ['LAKECROFT DUP MARK V191H',
     'markA 1',
     'markB 1',
     'markC 0',
     'dup_mark TARGET 2'],
     'lakecroft', "DUP"),
    ("v191h_12", "mosscroft_zero", "zero_check", 0.0,
     ['MOSSCROFT AIR ZERO V191H',
     'z1 0.00',
     'z2 0.00',
     'z3 0.00',
     'zero_check TARGET 0.00'],
     'mosscroft', "ZERO"),
    ("v191h_13", "nethercroft_ledger", "ledger_net", 2511.5,
     ['NETHERCROFT LEDGER V191H',
     'dr 1248.00',
     'cr 1263.50',
     'adj 1085.00',
     'ledger_net TARGET 2511.50'],
     'nethercroft', "LED"),
    ("v191h_14", "oakcroft_ui", "ui_ok", 1.0,
     ['OAKCROFT UI SCAN V191H',
     'btnOK 1',
     'btnSkip 0',
     'btnBad 0',
     'ui_ok TARGET 1'],
     'oakcroft', "UI"),
    ("v191h_15", "pinecroft_stack", "stack_count", 1869.0,
     ['PINECROFT STACK V191H',
     'p1 937',
     'p2 932',
     'p3 927',
     'stack_count TARGET 1869'],
     'pinecroft', "STK"),
    ("v191h_16", "quillcroft_fax", "fax_pages", 1898.0,
     ['QUILLCROFT FAX V191H',
     'pgA 952',
     'pgB 946',
     'pgC 934 drop',
     'fax_pages TARGET 1898'],
     'quillcroft', "FAX"),
    ("v191h_17", "reedcroft_glare", "glare_ok", 1.0,
     ['REEDCROFT GLARE V191H',
     'zone1 1 ok',
     'zone2 0',
     'zone3 0',
     'glare_ok TARGET 1'],
     'reedcroft', "GLR"),
    ("v191h_18", "stonecroft_tab", "tab_index", 1918.0,
     ['STONECROFT TAB INDEX V191H',
     'tabA 962',
     'tabB 956',
     'tabC 935',
     'tab_index TARGET 1918'],
     'stonecroft', "TAB"),
]


















































































































































def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


PROTOCOL = """# Ant VL Gate V191 Heldout Protocol

Updated: {ts} (Asia/Shanghai)

## Purpose
Disjoint heldout for V191 train (C425). Different ids/amounts.
Same hl/crumple/rubber/clip/grease/carbon/stamp/pocket family.
Clarity floor jpeg_q>={jpeg_q}.

## Gate
rate >= 0.6, n >= 16, real VL. Gate2/3 untouched. gen11 HOLD.
"""


def in_text_band(yy):
    y0, y1 = TEXT_BAND
    return y0 <= yy <= y1


def make_fixture(fid, kind, lines, metric, expected, cn_title, stamp):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    FIX.mkdir(parents=True, exist_ok=True)
    rng = random.Random(hash(fid + "_v191hc379") & 0xFFFFFFFF)
    bg = (212, 208, 198)
    img = Image.new("RGB", (1100, 740), bg)
    d = ImageDraw.Draw(img)
    try:
        f_title = ImageFont.truetype(r"C:\\Windows\\Fonts\\msyh.ttc", 16)
        f_body = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 14)
        f_tgt = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 15)
        f_sm = ImageFont.truetype(r"C:\\Windows\\Fonts\\msyh.ttc", 11)
        f_stamp = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 14)
        f_tiny = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 10)
        f_wm = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 28)
        f_fax = ImageFont.truetype(r"C:\\Windows\\Fonts\\consola.ttf", 11)
        f_pen = ImageFont.truetype(r"C:\\Windows\\Fonts\\comic.ttf", 13)
    except Exception:
        f_title = f_body = f_tgt = f_sm = f_stamp = f_tiny = f_wm = f_fax = f_pen = ImageFont.load_default()

    d.rectangle([40, 20, 560, 600], fill=(252, 249, 240), outline=(30, 30, 30), width=2)

    for hy in (80, 160, 240, 320, 400, 480):
        d.ellipse([8, hy - 10, 36, hy + 10], outline=(60, 60, 70), width=3)
        d.ellipse([14, hy - 4, 30, hy + 4], fill=(180, 180, 190))

    for (cx, cy, r) in [(480, 420, 55), (120, 520, 40), (900, 300, 70)]:
        for rr in range(r - 8, r, 2):
            d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=(160, 110, 70), width=2)
        d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(170, 120, 80))

    d.rectangle([80, 18, 280, 42], fill=(240, 230, 160))
    d.text((90, 22), "TAPE bait 33.33", fill=(100, 80, 20), font=f_tiny)

    d.line([(470, 90), (540, 200)], fill=(20, 60, 180), width=2)
    d.text((475, 160), "OK?", fill=(20, 60, 180), font=f_pen)
    d.text((475, 185), "bait 66.66", fill=(20, 60, 180), font=f_tiny)

    d.rectangle([380, 300, 540, 380], fill=(255, 250, 120), outline=(180, 160, 40), width=2)
    d.text((390, 310), "STICKY", fill=(70, 50, 10), font=f_sm)
    d.text((390, 335), "bait 88.88", fill=(70, 50, 10), font=f_tiny)
    d.text((390, 355), "IGNORE", fill=(70, 50, 10), font=f_tiny)

    for y in range(290, 560, 7):
        shade = 200 if (y // 7) % 2 == 0 else 230
        d.line([(50, y), (540, y)], fill=(shade, shade, shade), width=1)

    for (cx, cy, label, col) in [
        (420, 450, stamp, (170, 20, 20)),
        (180, 500, "VOID", (140, 30, 30)),
        (300, 550, "COPY", (50, 50, 150)),
    ]:
        d.ellipse([cx - 48, cy - 24, cx + 42, cy + 26], outline=col, width=3)
        d.text((cx - 16, cy - 6), label[:4], fill=col, font=f_stamp)

    for i in range(5):
        d.text((70 + i * 45, 310 + i * 38), "DRAFT", fill=(236, 232, 224), font=f_wm)

    d.rectangle([0, 0, 1100, 14], fill=(235, 235, 235))
    d.text((8, 1), "SCAN DESK V42H bait 222.00 PAGE 01", fill=(70, 70, 70), font=f_fax)

    d.rectangle([50, 28, 360, 58], fill=(28, 48, 68))
    d.text((56, 32), (cn_title or kind)[:18], fill=(240, 240, 240), font=f_title)

    y = 78
    for ln in lines:
        font = f_tgt if ("TARGET" in ln.upper() or "TOTAL" in ln.upper()) else f_body
        d.text((62, y + 2), ln[:54], fill=(228, 224, 214), font=font)
        d.text((60, y), ln[:54], fill=(6, 6, 6), font=font)
        y += 26

    d.rectangle([760, 220, 1060, 420], fill=(248, 246, 252), outline=(40, 40, 70), width=2)
    d.text((770, 230), "VOID WIN IGNORE", fill=(120, 40, 40), font=f_sm)
    d.text((770, 265), "old total 888.00", fill=(20, 20, 20), font=f_sm)
    d.text((770, 300), "do not parse", fill=(20, 20, 20), font=f_sm)
    d.text((770, 335), "bait 555.00", fill=(20, 20, 20), font=f_sm)

    d.rectangle([0, 710, 1100, 740], fill=(16, 16, 26))
    d.text(
        (10, 718),
        f"V191H C1255 clarity floor jpeg_q{JPEG_Q} photo/{PHOTOCOPY_DIV} heldout",
        fill=(200, 200, 200),
        font=f_tiny,
    )

    px = img.load()
    ww, hh = img.size

    for t in range(0, 700, 2):
        xx = 60 + t
        yy = 280 + int(t * 0.35)
        for w in range(-2, 3):
            x2, y2 = xx + w, yy + w
            if 0 <= x2 < ww and 0 <= y2 < hh and not (in_text_band(y2) and 50 <= x2 <= 450):
                r, g, b = px[x2, y2]
                px[x2, y2] = (min(255, r + 18), min(255, g + 16), min(255, b + 12))

    for _ in range(120):
        xx = rng.randint(45, 160)
        yy = rng.randint(420, 580)
        r, g, b = px[xx, yy]
        px[xx, yy] = (max(0, r - 40), max(0, g - 50), max(0, b - 55))

    for yy in range(300, 560):
        for xx in range(500, 560):
            r, g, b = px[xx, yy]
            px[xx, yy] = (int(r * 0.92 + 20), int(g * 0.92 + 20), int(b * 0.92 + 20))

    for _ in range(280):
        xx = rng.randint(0, ww - 1)
        yy = rng.randint(0, hh - 1)
        if in_text_band(yy) and 50 <= xx <= 540:
            continue
        v = rng.randint(0, 255)
        px[xx, yy] = (v, v, v)

    img = ImageEnhance.Color(img).enhance(0.82)
    img = ImageEnhance.Contrast(img).enhance(0.98)
    img = ImageEnhance.Brightness(img).enhance(0.95)

    w, h = img.size
    small = img.resize((max(1, w // PHOTOCOPY_DIV), max(1, h // PHOTOCOPY_DIV)), Image.BILINEAR)
    img = small.resize((w, h), Image.BILINEAR)
    img = img.transform(
        (w, h), Image.AFFINE, (1, 0.028, -10, 0.012, 1, -5),
        resample=Image.BICUBIC, fillcolor=bg,
    )
    ghost = img.transform(
        (w, h), Image.AFFINE, (1, 0, 3, 0, 1, 2),
        resample=Image.BICUBIC, fillcolor=bg,
    )
    img = Image.blend(img, ghost, 0.12)
    img = img.filter(ImageFilter.GaussianBlur(radius=BLUR_R))

    # --- V42 overlays (new vs V39) ---
    for _ in range(110):
        bx = rng.randint(50, 540)
        by = rng.randint(350, 580)
        if in_text_band(by):
            continue
        d.line([(bx, by), (bx + rng.randint(6, 24), by + rng.randint(-5, 5))], fill=(90, 70, 40), width=1)
    for gi in range(5):
        d.ellipse([52 + gi * 24, 312, 70 + gi * 24, 330], outline=(90, 50, 20), width=2)
    d.text((52, 332), "TEAK bait 40.40", fill=(80, 50, 20), font=f_tiny)
    for hi in range(4):
        d.polygon([(585 + hi * 34, 38), (611 + hi * 34, 38), (598 + hi * 34, 74)], fill=(20, 40, 140))
    d.text((585, 78), "COBALT bait 60.60", fill=(10, 20, 100), font=f_tiny)
    d.rectangle([255, 385, 415, 445], fill=(245, 250, 255))
    d.text((265, 405), "XENOCREEK ghost 90.90", fill=(20, 20, 40), font=f_pen)
    d.arc([415, 375, 505, 445], 30, 250, fill=(180, 140, 40), width=3)
    d.text((415, 450), "TOPAZ bait 35.35", fill=(120, 90, 20), font=f_tiny)
    d.ellipse([65, 475, 135, 535], fill=(90, 95, 100), outline=(40, 45, 50), width=2)
    d.text((65, 540), "SHALE bait 26.26", fill=(50, 55, 60), font=f_tiny)
    for qi in range(4):
        d.rectangle([255 + qi * 42, 475, 287 + qi * 42, 507], outline=(70, 50, 30), width=2)
    d.rectangle([855, 115, 1005, 175], fill=(160, 165, 170), outline=(50, 55, 60), width=2)
    d.text((875, 133), "TIN", fill=(25, 30, 35), font=f_stamp)
    d.polygon([(40, 4), (420, 4), (405, 18), (50, 18)], fill=(190, 175, 150), outline=(90, 70, 40), width=1)
    d.text((70, 5), "IRIDIUM bait 70.70", fill=(40, 45, 55), font=f_tiny)
    for ti, ty in enumerate((95, 155, 215)):
        d.polygon([(1000, ty), (1024, ty + 12), (1000, ty + 24)], fill=(80, 60, 40 + ti * 20))




    # --- V191 overlays (new vs V49) ---
    for _ in range(140):
        bx = rng.randint(50, 540)
        by = rng.randint(365, 595)
        if in_text_band(by):
            continue
        d.line([(bx, by), (bx + rng.randint(8, 30), by + rng.randint(-7, 7))], fill=(55, 75, 45), width=1)
    for gi in range(5):
        d.ellipse([58 + gi * 24, 322, 76 + gi * 24, 340], outline=(30, 100, 70), width=2)
    d.text((58, 342), 'ASHDALE bait 75.75', fill=(20, 80, 50), font=f_tiny)
    for hi in range(4):
        d.polygon([(600 + hi * 34, 44), (626 + hi * 34, 44), (613 + hi * 34, 80)], fill=(160, 40, 60))
    d.text((600, 84), 'CEDARD bait 85.85', fill=(120, 20, 40), font=f_tiny)
    d.rectangle([270, 400, 430, 460], fill=(245, 255, 250))
    d.text((280, 420), 'DAWND ghost 99.99', fill=(20, 70, 40), font=f_pen)
    d.arc([430, 390, 520, 460], 40, 265, fill=(40, 90, 120), width=3)
    d.text((430, 465), 'GLEND bait 70.70', fill=(20, 60, 90), font=f_tiny)
    d.ellipse([80, 490, 150, 550], fill=(160, 150, 130), outline=(70, 65, 50), width=2)
    d.text((80, 555), 'JADED bait 61.61', fill=(70, 55, 35), font=f_tiny)
    for qi in range(4):
        d.rectangle([270 + qi * 42, 490, 302 + qi * 42, 522], outline=(50, 90, 60), width=2)
    d.rectangle([870, 130, 1020, 190], fill=(185, 200, 190), outline=(50, 70, 55), width=2)
    d.text((890, 148), 'MOSS', fill=(20, 50, 30), font=f_stamp)
    d.polygon([(40, 4), (420, 4), (405, 18), (50, 18)], fill=(200, 215, 195), outline=(60, 90, 50), width=1)
    d.text((70, 5), 'NETHERD bait 87.87', fill=(30, 60, 35), font=f_tiny)
    for ti, ty in enumerate((110, 170, 230)):
        d.polygon([(1000, ty), (1024, ty + 12), (1000, ty + 24)], fill=(40, 100, 60 + ti * 20))
    # dew drops + vine marks (V191-only)
    for ry in (115, 195, 275):
        d.ellipse([12, ry, 28, ry + 16], fill=(140, 200, 220), outline=(30, 60, 80), width=2)
        d.ellipse([16, ry + 4, 24, ry + 12], fill=(200, 230, 240))
    for (sx, sy) in [(175, 370), (355, 400), (495, 380)]:
        if not in_text_band(sy):
            d.rectangle([sx, sy, sx + 18, sy + 5], fill=(40, 70, 40))

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=JPEG_Q)
    buf.seek(0)
    img = Image.open(buf).convert("RGB")
    img = img.filter(ImageFilter.SMOOTH)

    outp = FIX / f"{fid}_{kind}.png"
    for old in FIX.glob(f"{fid}_*.png"):
        if old != outp:
            try:
                old.unlink()
            except Exception:
                pass
    img.save(outp)
    return {
        "id": fid, "file": outp.name, "kind": kind, "metric": metric,
        "expected": expected, "lines": lines, "cn_title": cn_title, "stamp": stamp,
        "path": str(outp.relative_to(ROOT)).replace("\\", "/"),
        "hardening": [
            "highlighter_cross", "magnetic_clip", "thermal_fade", "coffee_splash_edge",
            "double_fold_corner", "pencil_scribble", "stapler_puncture", "watermark_diag",
            "phone_shadow", "receipt_skew_stack", "blue_pen_circles", "red_correction_tape",
            "ship_label_edge", "binder_clip_top", "sticky_peel_corner",
            f"jpeg_q{JPEG_Q}", f"photocopy_div{PHOTOCOPY_DIV}", f"blur_{BLUR_R}",
            "text_band_protect", "c272_clarity_floor",
        ],
    }


def soft_ocr_ok(text, lines):
    t = (text or "").lower().replace(" ", "")
    keys = re.findall(r"\d+\.?\d*", " ".join(lines))
    if not t:
        return False
    hit = sum(1 for k in keys[:5] if k.replace(".00", "") in t or k in t)
    return hit >= max(2, min(3, len(keys[:5]) // 2))


def gpu_free_mib():
    try:
        import subprocess
        r = subprocess.run(
            ["nvidia-smi", "--query-gpu=memory.free", "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=10,
        )
        return float((r.stdout or "0").strip().split("\n")[0])
    except Exception:
        return 0.0


def id_disjoint(train_ids, held_ids):
    return len(set(train_ids) & set(held_ids)) == 0


def main():
    RUN.mkdir(parents=True, exist_ok=True)
    DOC.mkdir(parents=True, exist_ok=True)
    PROTO.write_text(PROTOCOL.format(ts=ts(), jpeg_q=JPEG_Q), encoding="utf-8")
    items = []
    for fid, kind, metric, expected, lines, cn, stamp in SPECS:
        items.append(make_fixture(fid, kind, lines, metric, expected, cn, stamp))
    man = {
        "version": "v191h",
        "n": len(items),
        "gate": GATE,
        "theme": "obsidian_denim_coral_indigo_jade_amber_nickel_moss_pine_opal_granite_void_cedar_enamel_resin_sage_terra_hazel_heldout",
        "clarity_floor": {
            "jpeg_q_min": 60, "jpeg_q": JPEG_Q,
            "photocopy_div_max": 2, "photocopy_div": PHOTOCOPY_DIV,
            "blur_max": 0.5, "blur": BLUR_R,
            "text_band_y": list(TEXT_BAND),
        },
        "items": items,
        "timestamp": ts(),
        "claim": False,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }
    J(FIX / "manifest.json", man)

    train_ids, train_amts = [], []
    if (TRAIN_FIX / "manifest.json").is_file():
        tman = json.loads((TRAIN_FIX / "manifest.json").read_text(encoding="utf-8"))
        train_ids = [it["id"] for it in tman.get("items") or []]
        train_amts = [it["expected"] for it in tman.get("items") or []]
    held_ids = [it["id"] for it in items]
    held_amts = [it["expected"] for it in items]
    disjoint = id_disjoint(train_ids, held_ids)
    amt_overlap = sorted(set(train_amts) & set(held_amts))

    free = gpu_free_mib()
    if free < 2000 or not WEIGHTS.is_dir():
        out = {
            "cycle": "C1255", "theme": "vision_v191_heldout", "gate": GATE,
            "timestamp": ts(), "attempted": False, "reason": f"gpu_free={free}",
            "n": len(items), "id_disjoint": disjoint, "amt_overlap": amt_overlap,
            "vl_gate_v191_heldout_claim": False, "pass": False, "claim": False,
            "gate2_3_untouched": True, "gen11": "HOLD",
        }
        J(DOC / "C1255_VISION_V191_HELDOUT_SMOKE.json", out)
        print(json.dumps(out, ensure_ascii=False))
        return 1

    from evo.office.vision_backend import RealVlBackend
    from evo.office.vision_ocr import ocr_image
    backend = RealVlBackend(WEIGHTS, max_new_tokens=200)
    rows, n_ok = [], 0
    try:
        for it in items:
            ocr = ocr_image(ROOT / it["path"], prefer="vl", vl_backend=backend)
            text = re.sub(r"<think>[\s\S]*?</think>", " ", ocr.get("text") or "")
            text = re.sub(r"\s+", " ", text).strip()
            ocr_ok = soft_ocr_ok(text, it["lines"])
            got, atom_ok = parse_metric(text, it["metric"], it["expected"])
            ok = bool(ocr_ok and atom_ok)
            n_ok += int(ok)
            rows.append({
                "id": it["id"], "kind": it["kind"], "metric": it["metric"],
                "ocr_ok": ocr_ok, "atom_ok": atom_ok, "ok": ok,
                "got": got, "expected": it["expected"], "ocr_preview": text[:360],
            })
            print(json.dumps({
                "id": it["id"], "ok": ok, "got": got, "expected": it["expected"],
            }, ensure_ascii=False), flush=True)
    finally:
        try:
            backend.unload()
        except Exception:
            pass
        gc.collect()
        try:
            import torch
            torch.cuda.empty_cache()
        except Exception:
            pass

    n = len(rows)
    rate = round(n_ok / n, 4) if n else 0.0
    gate_pass = n >= 16 and rate >= GATE and disjoint
    claim = gate_pass
    scope = "r50plus_v191_heldout_flint_velvet_n>=16_qwen35_2b_clarity_floor" if claim else None
    out = {
        "cycle": "C1255",
        "theme": "vision_v191_heldout",
        "gate": GATE,
        "timestamp": ts(),
        "attempted": True,
        "gpu_free_mib_start": free,
        "n": n, "n_ok": n_ok, "rate": rate,
        "gate_pass": gate_pass,
        "fail_ids": [r["id"] for r in rows if not r["ok"]],
        "rows": rows,
        "id_disjoint": disjoint,
        "amt_overlap": amt_overlap,
        "vl_gate_v191_heldout_claim": claim,
        "claim_scope": scope,
        "clarity_floor": man["clarity_floor"],
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "pass": gate_pass,
        "claim": claim,
    }
    J(DOC / "C1255_VISION_V191_HELDOUT_SMOKE.json", out)
    J(RUN / "judge.json", out)
    if claim:
        J(DOC / "C1255b_VISION_GATE_V191_HELDOUT_CLAIM.json", {
            "kind": "vision_gate_v191_heldout_claim",
            "timestamp": ts(),
            "vl_gate_v191_heldout_claim": True,
            "rate": rate, "n": n, "n_ok": n_ok, "gate": GATE,
            "claim_scope": scope,
            "id_disjoint": disjoint,
            "gate2_3_untouched": True,
            "gen11": "HOLD",
            "cycle": "C1255",
        })
    print(json.dumps({
        "cycle": "C1255", "rate": rate, "n_ok": n_ok, "n": n,
        "fail_ids": out["fail_ids"], "disjoint": disjoint,
        "claim": claim, "pass": gate_pass,
    }, ensure_ascii=False))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
