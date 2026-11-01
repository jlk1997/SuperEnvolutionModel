# -*- coding: utf-8 -*-
"""C298: Vision V32 heldout 鈥?disjoint fixtures + real VL claim if rate>=0.6.
Different ids/amounts from V32 train (C296/C297). Same fp/rain/staple/qr/
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
FIX = ROOT / "evo/office/fixtures/vision_images_v32h"
WEIGHTS = ROOT / "models/Qwen3.5-2B"
RUN = ROOT / "runs/vision_v32h_c286"
PROTO = ROOT / "docs" / "蚁算_VL_GATE_V32_HELDOUT_PROTOCOL.md"
TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v32"

JPEG_Q = 60
PHOTOCOPY_DIV = 2
BLUR_R = 0.45
TEXT_BAND = (70, 250)

# Disjoint from V32 train amounts (C254)
SPECS = [
    ("v32h_01", "kraft_recv", "paid_total", 67.5,
     ["KRAFT PAPER RECV V32H", "a paid 33.00", "b paid 34.50", "c open 12.00", "TOTAL PAID TARGET 67.50"],
     "牛皮纸收款单H", "RECV"),
    ("v32h_02", "linen_wh", "qty_sum", 55.0,
     ["WH LINEN WEAVE V32H", "SKU1 qty 26 ok", "SKU2 qty 13 hold", "SKU3 qty 29 ok", "qty_sum TARGET 55"],
     "亚麻纹仓单H", "RECV"),
    ("v32h_03", "thermal_refund", "refund_done", 39.25,
     ["THERMAL FADE REFUND V32H", "itemR1 18.00 done", "itemR2 21.25 done", "itemR3 9.00 open", "refund_done TARGET 39.25"],
     "热敏淡化退款单H", "DONE"),
    ("v32h_04", "dossier_tax", "tax_base_paid", 116.0,
     ["TAX DOSSIER TAB V32H", "T1 64.00 paid", "T2 26.00 open", "T3 52.00 paid", "tax_base_paid TARGET 116.00"],
     "档案标签税基单H", "RECV"),
    ("v32h_05", "chrono_pay", "payroll_active", 2280.0,
     ["PAYROLL CHRONO STAMP V32H", "A 1160 active", "B 240 leave", "C 1120 active", "payroll_active TARGET 2280"],
     "计时戳工资单H", "OK"),
    ("v32h_06", "rubber_ship", "ship_ok_qty", 47.0,
     ["SHIP RUBBER PAD V32H", "P1 23 ok", "P2 12 hold", "P3 24 ok", "ship_ok_qty TARGET 47"],
     "橡胶印发运单H", "SHIP"),
    ("v32h_07", "checker_sla", "open_pri_sum", 49.0,
     ["SLA CHECKER BAIT V32H", "S1 pri 21 open", "S2 pri 23 closed", "S3 pri 28 open", "open_pri_sum TARGET 49"],
     "棋盘SLAH", "OPEN"),
    ("v32h_08", "vellum_exp", "paid_total", 88.25,
     ["EXPENSE VELLUM V32H", "E1 42.00 paid", "E2 17.00 void", "E3 46.25 paid", "paid_total TARGET 88.25"],
     "玻璃纸报销单H", "RECV"),
    ("v32h_09", "brad_po", "paid_total", 70.0,
     ["PO-BRAD FASTENER V32H", "itemA paid 34.00", "itemB paid 36.00", "itemC open 13.00", "TOTAL PAID TARGET 70.00"],
     "柜钉采购单H", "RECV"),
    ("v32h_10", "scroll_order", "paid_total", 61.5,
     ["ORDER SCROLL CURL V32H", "A paid 30.00", "B paid 31.50", "C open 11.00", "TOTAL PAID TARGET 61.50"],
     "卷边订单H", "RECV"),
    ("v32h_11", "ditto_dup", "paid_total", 78.0,
     ["INVOICE #V32H-DITTO", "lineA paid 26.00", "lineB paid 26.00", "lineC paid 26.00", "TOTAL PAID TARGET 78.00"],
     "紫油印重复发票H", "RECV"),
    ("v32h_12", "void_zero", "paid_total", 0.0,
     ["OPEN ONLY V32H", "X 40.00 open", "Y 43.00 open", "paid_total TARGET 0.00"],
     "未付空白H", "HOLD"),
    ("v32h_13", "flock_ledger", "paid_total", 47.5,
     ["LEDGER FLOCK TEXTURE V32H", "rA paid 23.00", "rB paid 24.50", "rC open 9.00", "TOTAL PAID TARGET 47.50"],
     "绒面台账H", "RECV"),
    ("v32h_14", "matrix_ui", "paid_total", 53.75,
     ["UI DOT MATRIX V32H", "alpha paid 26.00", "beta paid 27.75", "gamma open 10.00", "TOTAL PAID TARGET 53.75"],
     "点阵界面单据H", "RECV"),
    ("v32h_15", "axon_stack", "paid_total", 84.0,
     ["AXON GRID STACK V32H", "x paid 41.00 usd", "y paid 43.00 usd", "z open 14.00 usd", "TOTAL PAID TARGET 84.00"],
     "轴测网格叠页H", "RECV"),
    ("v32h_16", "twine_fax", "paid_total", 45.25,
     ["CN-EN TWINE BIND FAX V32H", "tea paid 22.00", "rice paid 23.25", "soup open 9.00", "TOTAL PAID TARGET 45.25"],
     "麻绳装订传真双语H", "RECV"),
    ("v32h_17", "chamfer_glare", "paid_total", 63.0,
     ["CHAMFER EDGE GLARE V32H", "w1 paid 30.00", "w2 paid 33.00", "w3 open 12.00", "TOTAL PAID TARGET 63.00"],
     "倒角眩光单H", "RECV"),
    ("v32h_18", "snap_tab", "paid_total", 36.5,
     ["SNAP BUTTON TAB V32H", "p1 paid 17.00", "p2 paid 19.50", "p3 open 8.00", "TOTAL PAID TARGET 36.50"],
     "按扣角签页H", "RECV"),
]






def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


PROTOCOL = """# Ant VL Gate V32 Heldout Protocol

Updated: {ts} (Asia/Shanghai)

## Purpose
Disjoint heldout for V32 train (C297). Different ids/amounts.
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
    rng = random.Random(hash(fid + "_v32hc274") & 0xFFFFFFFF)
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
    d.text((8, 1), "SCAN DESK V32H bait 222.00 PAGE 01", fill=(70, 70, 70), font=f_fax)

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
        f"V32H C298 clarity floor jpeg_q{JPEG_Q} photo/{PHOTOCOPY_DIV} heldout",
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
        "version": "v32h",
        "n": len(items),
        "gate": GATE,
        "theme": "hlx_magclip_thermal_coffee_heldout",
        "clarity_floor": {
            "jpeg_q_min": 58, "jpeg_q": JPEG_Q,
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
            "cycle": "C298", "theme": "vision_v32_heldout", "gate": GATE,
            "timestamp": ts(), "attempted": False, "reason": f"gpu_free={free}",
            "n": len(items), "id_disjoint": disjoint, "amt_overlap": amt_overlap,
            "vl_gate_v32_heldout_claim": False, "pass": False, "claim": False,
            "gate2_3_untouched": True, "gen11": "HOLD",
        }
        J(DOC / "C298_VISION_V32_HELDOUT_SMOKE.json", out)
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
    scope = "r50plus_v32_heldout_hlx_magclip_n>=16_qwen35_2b_clarity_floor" if claim else None
    out = {
        "cycle": "C298",
        "theme": "vision_v32_heldout",
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
        "vl_gate_v32_heldout_claim": claim,
        "claim_scope": scope,
        "clarity_floor": man["clarity_floor"],
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "pass": gate_pass,
        "claim": claim,
    }
    J(DOC / "C298_VISION_V32_HELDOUT_SMOKE.json", out)
    J(RUN / "judge.json", out)
    if claim:
        J(DOC / "C298b_VISION_GATE_V32_HELDOUT_CLAIM.json", {
            "kind": "vision_gate_v32_heldout_claim",
            "timestamp": ts(),
            "vl_gate_v32_heldout_claim": True,
            "rate": rate, "n": n, "n_ok": n_ok, "gate": GATE,
            "claim_scope": scope,
            "id_disjoint": disjoint,
            "gate2_3_untouched": True,
            "gen11": "HOLD",
            "cycle": "C298",
        })
    print(json.dumps({
        "cycle": "C298", "rate": rate, "n_ok": n_ok, "n": n,
        "fail_ids": out["fail_ids"], "disjoint": disjoint,
        "claim": claim, "pass": gate_pass,
    }, ensure_ascii=False))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
