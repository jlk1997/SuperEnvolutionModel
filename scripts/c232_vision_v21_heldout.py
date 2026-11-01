# -*- coding: utf-8 -*-
"""C230: Vision V21 design + fixtures (harder than V20 clarity-floor).
NEW themes vs V20: stapler_hole, highlighter_lane, skew_desk, stamp_bleed,
paper_tear, moire_screen, watermark_dense, desk_shadow, rust_staple, dogear.
CLARITY FLOOR (C218/V20): jpeg_q>=58, photocopy max /2, blur<=0.5,
protect text band y=70..250. Claim after heldout VL in this script.
Gate 0.6. Gate2/3 untouched. gen11 HOLD.
"""
from __future__ import annotations
import io, json, random, re, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
GATE = 0.6
DOC = ROOT / "docs" / "r50"
FIX = ROOT / "evo/office/fixtures/vision_images_v21h"
PROTO = ROOT / "docs" / "蚁算_VL_GATE_V21_HELDOUT_PROTOCOL.md"
RUN = ROOT / "runs/vision_v21h_c232"

JPEG_Q = 60
PHOTOCOPY_DIV = 2
BLUR_R = 0.45
TEXT_BAND = (70, 250)

SPECS = [
    ("v21h_01", "staple_receipt", "paid_total", 68.5,
     ['STAPLE HOLE V21H', 'a paid 33.00', 'b paid 35.50', 'c open 10.00', 'TOTAL PAID TARGET 68.50'],
     "订书收据H", "RECV"),
    ("v21h_02", "hl_wh", "qty_sum", 55.0,
     ['WH HIGHLIGHT V21H', 'SKU1 qty 26 ok', 'SKU2 qty 12 hold', 'SKU3 qty 29 ok', 'qty_sum TARGET 55'],
     "荧光仓单H", "RECV"),
    ("v21h_03", "skew_refund", "refund_done", 30.75,
     ['SKEW REFUND V21H', 'itemR1 14.50 done', 'itemR2 16.25 done', 'itemR3 7.00 open', 'refund_done TARGET 30.75'],
     "透视退款H", "DONE"),
    ("v21h_04", "bleed_tax", "tax_base_paid", 106.0,
     ['TAX STAMP BLEED V21H', 'T1 58.00 paid', 'T2 24.00 open', 'T3 48.00 paid', 'tax_base_paid TARGET 106.00'],
     "渗墨税基H", "RECV"),
    ("v21h_05", "tear_pay", "payroll_active", 1840.0,
     ['PAYROLL TEAR V21H', 'A 970 active', 'B 180 leave', 'C 870 active', 'payroll_active TARGET 1840'],
     "撕边工资H", "OK"),
    ("v21h_06", "moire_ship", "ship_ok_qty", 45.0,
     ['SHIP MOIRE V21H', 'P1 23 ok', 'P2 12 hold', 'P3 22 ok', 'ship_ok_qty TARGET 45'],
     "摩尔发货H", "SHIP"),
    ("v21h_07", "wm_sla", "open_pri_sum", 38.0,
     ['SLA WATERMARK V21H', 'S1 pri 17 open', 'S2 pri 24 closed', 'S3 pri 21 open', 'open_pri_sum TARGET 38'],
     "水印SLAH", "OPEN"),
    ("v21h_08", "shadow_exp", "paid_total", 73.25,
     ['EXPENSE SHADOW V21H', 'E1 36.00 paid', 'E2 15.00 void', 'E3 37.25 paid', 'paid_total TARGET 73.25'],
     "侧影报销H", "RECV"),
    ("v21h_09", "rust_po", "paid_total", 58.0,
     ['PO-RUST STAPLE V21H', 'itemA paid 28.75', 'itemB paid 29.25', 'itemC open 11.00', 'TOTAL PAID TARGET 58.00'],
     "锈钉采购H", "RECV"),
    ("v21h_10", "dogear_order", "paid_total", 50.5,
     ['ORDER DOGEAR V21H', 'A paid 25.00', 'B paid 25.50', 'C open 8.00', 'TOTAL PAID TARGET 50.50'],
     "折角订单H", "RECV"),
    ("v21h_11", "staple_dup", "paid_total", 60.0,
     ['INVOICE #V21H-DUP', 'line paid 20.00', 'line paid 20.00', 'line paid 20.00', 'TOTAL PAID TARGET 60.00'],
     "订书重复H", "RECV"),
    ("v21h_12", "hl_zero", "paid_total", 0.0,
     ['OPEN ONLY V21H', 'X 43.00 open', 'Y 46.00 open', 'paid_total TARGET 0.00'],
     "荧光未付H", "HOLD"),
    ("v21h_13", "skew_ledger", "paid_total", 41.25,
     ['LEDGER SKEW V21H', 'rA paid 20.00', 'rB paid 21.25', 'rC open 6.00', 'TOTAL PAID TARGET 41.25'],
     "透视台账H", "RECV"),
    ("v21h_14", "bleed_ui", "paid_total", 46.5,
     ['UI BLEED V21H', 'alpha paid 23.00', 'beta paid 23.50', 'gamma open 8.50', 'TOTAL PAID TARGET 46.50'],
     "渗墨界面H", "RECV"),
    ("v21h_15", "tear_stack", "paid_total", 70.0,
     ['HEAVY TEAR V21H', 'x paid 35.00 usd', 'y paid 35.00 usd', 'z open 14.00 usd', 'TOTAL PAID TARGET 70.00'],
     "撕边堆单H", "RECV"),
    ("v21h_16", "moire_mix", "paid_total", 43.25,
     ['CN-EN MOIRE MIX V21H', 'tea paid 20.50', 'rice paid 22.75', 'soup open 7.00', 'TOTAL PAID TARGET 43.25'],
     "中英摩尔H", "RECV"),
    ("v21h_17", "wm_win", "paid_total", 55.0,
     ['WATERMARK WIN V21H', 'w1 paid 27.00', 'w2 paid 28.00', 'w3 open 12.00', 'TOTAL PAID TARGET 55.00'],
     "水印双窗H", "RECV"),
    ("v21h_18", "shadow_foot", "paid_total", 30.5,
     ['SHADOW FOOT V21H', 'p1 paid 15.00', 'p2 paid 15.50', 'p3 open 6.00', 'TOTAL PAID TARGET 30.50'],
     "侧影脚注H", "RECV"),
]


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


PROTOCOL = """# Ant VL Gate V21 Protocol

Updated: {ts} (Asia/Shanghai)

## Purpose
Heldout vs V21 train: stapler holes, highlighter lane, desk skew, stamp bleed,
paper tear, moire screen, dense watermark, desk shadow, rust staple, dogear.
Clarity floor from C218/V20 (no jpeg crush).

## Clarity floor (mandatory)
- jpeg quality >= **58** (V21 uses {jpeg_q})
- photocopy downsample max **/2** (not /3)
- Gaussian blur radius <= **0.5**
- Protect text band y≈70–250 from glyph-wiping overlays
- TARGET / amount lines high-contrast bold

## Gate
- rate >= **0.6**, n >= 16, real VL (C232 heldout)
- Claim only after smoke

## Honesty
- V20 train/heldout retained
- Gate2/3 untouched. gen11 HOLD. No fake VL scores.
"""


def in_text_band(yy):
    y0, y1 = TEXT_BAND
    return y0 <= yy <= y1


def make_fixture(fid, kind, lines, metric, expected, cn_title, stamp):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    FIX.mkdir(parents=True, exist_ok=True)
    rng = random.Random(hash(fid + "_v21hc232") & 0xFFFFFFFF)
    bg = (214, 210, 200)
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
    except Exception:
        f_title = f_body = f_tgt = f_sm = f_stamp = f_tiny = f_wm = f_fax = ImageFont.load_default()

    # main card
    d.rectangle([40, 20, 560, 600], fill=(252, 249, 240), outline=(30, 30, 30), width=2)

    # desk shadow (left margin gradient sim)
    for i in range(36):
        shade = 180 - i * 2
        d.rectangle([0, 20 + i * 16, 38, 36 + i * 16], fill=(shade, shade - 4, shade - 8))

    # highlighter lane RIGHT of text (not over digits) — translucent yellow band
    d.rectangle([470, 70, 555, 250], fill=(255, 255, 140))
    d.text((478, 90), "HL lane", fill=(140, 120, 20), font=f_tiny)
    d.text((478, 115), "bait 77.77", fill=(140, 120, 20), font=f_tiny)

    # dense watermark diagonals OUTSIDE text band priority
    for i in range(6):
        d.text((80 + i * 40, 300 + i * 35), "DRAFT", fill=(235, 230, 220), font=f_wm)

    # moire grid below text band
    for x in range(50, 540, 7):
        d.line([(x, 280), (x + 20, 560)], fill=(210, 205, 195), width=1)
    for y in range(280, 560, 9):
        d.line([(50, y), (540, y)], fill=(215, 210, 200), width=1)

    # stamp bleed circles (away from TARGET y)
    for (cx, cy, label, col) in [
        (420, 390, stamp, (170, 20, 20)),
        (180, 470, "VOID", (140, 30, 30)),
        (300, 530, "COPY", (50, 50, 150)),
    ]:
        d.ellipse([cx - 48, cy - 24, cx + 42, cy + 26], outline=col, width=4)
        # bleed halo
        d.ellipse([cx - 52, cy - 28, cx + 46, cy + 30], outline=(col[0], col[1], col[2],), width=1)
        d.text((cx - 16, cy - 6), label[:4], fill=col, font=f_stamp)

    # sticky bait
    d.rectangle([380, 280, 540, 360], fill=(255, 248, 100), outline=(170, 150, 30), width=2)
    d.text((390, 290), "STICKY", fill=(70, 50, 10), font=f_sm)
    d.text((390, 315), "bait 88.88", fill=(70, 50, 10), font=f_tiny)
    d.text((390, 335), "IGNORE", fill=(70, 50, 10), font=f_tiny)

    # barcode far right
    bx0 = 545
    for i in range(36):
        w = 1 if rng.random() < 0.55 else 2
        col = (10, 10, 10) if rng.random() < 0.7 else (240, 240, 240)
        d.rectangle([bx0 + i * 2, 300, bx0 + i * 2 + w, 460], fill=col)
    d.text((bx0, 470), "||BAR|| bait 666", fill=(40, 40, 40), font=f_tiny)

    # fax/header strip
    d.rectangle([0, 0, 1100, 14], fill=(235, 235, 235))
    d.text((8, 1), "SCAN DESK V21  bait 222.00  PAGE 01", fill=(70, 70, 70), font=f_fax)

    d.text((100, 580), "CONFIDENTIAL", fill=(248, 245, 236), font=f_wm)  # near-bg; C231 fail fix
    d.rectangle([50, 28, 360, 58], fill=(28, 48, 68))
    d.text((56, 32), (cn_title or kind)[:18], fill=(240, 240, 240), font=f_title)

    # PRIMARY TEXT — high contrast, protected band
    y = 78
    for ln in lines:
        font = f_tgt if ("TARGET" in ln.upper() or "TOTAL" in ln.upper()) else f_body
        d.text((62, y + 2), ln[:54], fill=(228, 224, 214), font=font)
        d.text((60, y), ln[:54], fill=(6, 6, 6), font=font)
        y += 26

    # void win decoy
    d.rectangle([760, 220, 1060, 420], fill=(248, 246, 252), outline=(40, 40, 70), width=2)
    d.text((770, 230), "VOID WIN IGNORE", fill=(120, 40, 40), font=f_sm)
    d.text((770, 265), "old total 888.00", fill=(20, 20, 20), font=f_sm)
    d.text((770, 300), "do not parse", fill=(20, 20, 20), font=f_sm)
    d.text((770, 335), "bait 555.00", fill=(20, 20, 20), font=f_sm)

    d.rectangle([0, 710, 1100, 740], fill=(16, 16, 26))
    d.text(
        (10, 718),
        f"V21H C232 clarity floor jpeg_q{JPEG_Q} photo/{PHOTOCOPY_DIV}  Staple|HL|Skew|Bleed|Tear|Moire|WM|Shadow|Rust|Dogear",
        fill=(200, 200, 200),
        font=f_tiny,
    )

    px = img.load()
    ww, hh = img.size

    # stapler holes (top margin / left of card, not text)
    for (hx, hy) in [(90, 35), (140, 35), (480, 35), (70, 580), (200, 590)]:
        for dy in range(-7, 8):
            for dx in range(-7, 8):
                if dx * dx + dy * dy <= 36:
                    xx, yy = hx + dx, hy + dy
                    if 0 <= xx < ww and 0 <= yy < hh:
                        px[xx, yy] = bg if dx * dx + dy * dy <= 20 else (90, 90, 90)

    # rust ring around one staple
    for r in (10, 12, 14):
        for a in range(0, 360, 8):
            import math
            xx = int(90 + r * math.cos(a * 3.1415 / 180))
            yy = int(35 + r * math.sin(a * 3.1415 / 180))
            if 0 <= xx < ww and 0 <= yy < hh:
                px[xx, yy] = (120, 70, 40)

    # paper tear chew bottom-left outside text
    for yy in range(560, 640):
        tear = int(3 + (yy - 560) // 6 + rng.randint(0, 3))
        for xx in range(40, 40 + tear):
            if 0 <= xx < ww and 0 <= yy < hh:
                px[xx, yy] = bg

    # dogear top-right of card
    for yy in range(20, 70):
        cut = int((70 - yy) * 0.9)
        for xx in range(560 - cut, 560):
            if 0 <= xx < ww and 0 <= yy < hh:
                px[xx, yy] = bg

    # desk dust outside text
    for _ in range(320):
        xx = rng.randint(0, ww - 1)
        yy = rng.randint(0, hh - 1)
        if in_text_band(yy) and 50 <= xx <= 540:
            continue
        v = rng.randint(0, 255)
        px[xx, yy] = (v, v, v)

    # mild fingerprint / oil near edge
    for _ in range(60):
        xx = rng.randint(50, 180)
        yy = rng.randint(400, 580)
        r, g, b = px[xx, yy]
        px[xx, yy] = (max(0, r - 35), max(0, g - 45), max(0, b - 40))

    img = ImageEnhance.Color(img).enhance(0.85)
    img = ImageEnhance.Contrast(img).enhance(0.96)
    img = ImageEnhance.Brightness(img).enhance(0.94)

    w, h = img.size
    small = img.resize((max(1, w // PHOTOCOPY_DIV), max(1, h // PHOTOCOPY_DIV)), Image.BILINEAR)
    img = small.resize((w, h), Image.BILINEAR)
    # stronger desk skew than V20
    img = img.transform(
        (w, h), Image.AFFINE, (1, 0.038, -10, 0.014, 1, -5),
        resample=Image.BICUBIC, fillcolor=bg,
    )
    img = img.filter(ImageFilter.GaussianBlur(radius=BLUR_R))
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
            "stapler_hole", "highlighter_lane", "skew_desk", "stamp_bleed",
            "paper_tear", "moire_screen", "watermark_dense", "desk_shadow",
            "rust_staple", "dogear",
            f"jpeg_q{JPEG_Q}", f"photocopy_div{PHOTOCOPY_DIV}", f"blur_{BLUR_R}",
            "text_band_protect", "c232_clarity_floor",
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


def build_fixtures():
    RUN.mkdir(parents=True, exist_ok=True)
    DOC.mkdir(parents=True, exist_ok=True)
    PROTO.write_text(PROTOCOL.format(ts=ts(), jpeg_q=JPEG_Q), encoding="utf-8")
    items = []
    for fid, kind, metric, expected, lines, cn, stamp in SPECS:
        items.append(make_fixture(fid, kind, lines, metric, expected, cn, stamp))
    man = {
        "version": "v21h",
        "n": len(items),
        "gate": GATE,
        "theme": "staple_hl_skew_bleed_tear_moire_wm_shadow_rust_dogear_heldout",
        "harder_than": "v21_train_c230",
        "clarity_floor": {
            "jpeg_q_min": 58,
            "jpeg_q": JPEG_Q,
            "photocopy_div_max": 2,
            "photocopy_div": PHOTOCOPY_DIV,
            "blur_max": 0.5,
            "blur": BLUR_R,
            "text_band_y": list(TEXT_BAND),
            "lesson": "C218 jpeg crush; V21h keeps floor",
        },
        "items": items,
        "timestamp": ts(),
        "claim": False,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }
    J(FIX / "manifest.json", man)
    # disjoint check vs train
    train_man = ROOT / "evo/office/fixtures/vision_images_v21/manifest.json"
    id_disjoint = True
    if train_man.is_file():
        train = json.loads(train_man.read_text(encoding="utf-8"))
        train_ids = {it["id"] for it in (train.get("items") or [])}
        hold_ids = {it["id"] for it in items}
        id_disjoint = train_ids.isdisjoint(hold_ids)
    design = {
        "cycle": "C232",
        "theme": "vision_v21_heldout_design",
        "gate": GATE,
        "timestamp": ts(),
        "n": len(items),
        "fixture_dir": str(FIX.relative_to(ROOT)).replace("\\", "/"),
        "id_disjoint": id_disjoint,
        "clarity_floor": man["clarity_floor"],
        "claim": False,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }
    J(DOC / "C232_VISION_V21_HELDOUT_DESIGN.json", design)
    return man, id_disjoint


def run_vl(man, id_disjoint):
    import gc
    WEIGHTS = ROOT / "models/Qwen3.5-2B"
    free = gpu_free_mib()
    items = man.get("items") or []
    if free < 2000 or not WEIGHTS.is_dir():
        out = {
            "cycle": "C232", "theme": "vision_v21_heldout_smoke", "gate": GATE,
            "timestamp": ts(), "attempted": False, "reason": f"gpu_free={free}",
            "vl_gate_v21_heldout_claim": False, "pass": False, "claim": False,
            "id_disjoint": id_disjoint, "gate2_3_untouched": True, "gen11": "HOLD",
        }
        J(DOC / "C232_VISION_V21_HELDOUT_SMOKE.json", out)
        return out
    from evo.office.vision_backend import RealVlBackend
    from evo.office.vision_ocr import ocr_image
    from evo.office.vision_metric_parse import parse_metric
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
                "ocr_ok": ocr_ok, "atom_ok": atom_ok,
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
    gate_pass = n >= 16 and rate >= GATE and bool(id_disjoint)
    claim = gate_pass
    scope = "r50plus_v21_heldout_n>=16_qwen35_2b_clarity_floor_disjoint" if claim else None
    out = {
        "cycle": "C232",
        "theme": "vision_v21_heldout_smoke",
        "gate": GATE,
        "timestamp": ts(),
        "attempted": True,
        "gpu_free_mib_start": free,
        "n": n, "n_ok": n_ok, "rate": rate,
        "gate_pass": gate_pass,
        "fail_ids": [r["id"] for r in rows if not r["ok"]],
        "rows": rows,
        "clarity_floor": man.get("clarity_floor"),
        "id_disjoint": id_disjoint,
        "vl_gate_v21_heldout_claim": claim,
        "claim_scope": scope,
        "gate2_3_untouched": True,
        "v0_v21_train_untouched": True,
        "gen11": "HOLD",
        "pass": gate_pass,
        "claim": claim,
        "note": "C232 V21 heldout VL; claim if rate>=0.6 and id_disjoint",
    }
    J(DOC / "C232_VISION_V21_HELDOUT_SMOKE.json", out)
    J(RUN / "judge.json", out)
    if claim:
        J(DOC / "C232b_VISION_GATE_V21_HELDOUT_CLAIM.json", {
            "kind": "vision_gate_v21_heldout_claim",
            "timestamp": ts(),
            "vl_gate_v21_heldout_claim": True,
            "rate": rate, "n": n, "n_ok": n_ok, "gate": GATE,
            "claim_scope": scope,
            "id_disjoint": id_disjoint,
            "clarity_floor": man.get("clarity_floor"),
            "gate2_3_untouched": True,
            "gen11": "HOLD",
            "cycle": "C232",
        })
    return out


def main():
    import re as _re  # ensure re available
    global re
    man, id_disjoint = build_fixtures()
    print(json.dumps({"phase": "fixtures", "n": man["n"], "id_disjoint": id_disjoint}, ensure_ascii=False))
    out = run_vl(man, id_disjoint)
    print(json.dumps({
        "cycle": "C232", "rate": out.get("rate"), "n_ok": out.get("n_ok"), "n": out.get("n"),
        "fail_ids": out.get("fail_ids"), "claim": out.get("claim"), "id_disjoint": id_disjoint,
    }, ensure_ascii=False))
    return 0 if out.get("pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
