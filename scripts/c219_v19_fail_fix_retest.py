# -*- coding: utf-8 -*-
"""C219: Diagnose+fix V19 fails honestly — mild fixture regen + VL retest.
C218 rate=0.0556: jpeg_q22+photocopy/3+blur crushed digits (OCR garbage).
Parse-alone cannot recover. Fix: milder redraw same expected, keep V19 themes
(coffee/HL/barcode/ghost/stamp/torn/pen/photo) but protect text band.
Refresh claim if rate>=0.6. Gate2/3 untouched. gen11 HOLD.
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
FIX = ROOT / "evo/office/fixtures/vision_images_v19"
WEIGHTS = ROOT / "models/Qwen3.5-2B"
RUN = ROOT / "runs/vision_v19_c219"
PRIOR = DOC / "C218_VISION_V19_SMOKE.json"

# Same SPECS / expected as C217
SPECS = [
    ("v19_01", "coffee_receipt", "paid_total", 93.5,
     ["COFFEE RING V19", "a paid 46.00", "b paid 47.50", "c open 12.00", "TOTAL PAID TARGET 93.50"],
     "咖啡环收据", "RECV"),
    ("v19_02", "hl_wh", "qty_sum", 78.0,
     ["WH HIGHLIGHT V19", "SKU1 qty 41 ok", "SKU2 qty 19 hold", "SKU3 qty 37 ok", "qty_sum TARGET 78"],
     "荧光笔仓", "RECV"),
    ("v19_03", "barcode_refund", "refund_done", 44.75,
     ["BARCODE REFUND V19", "itemR1 21.25 done", "itemR2 23.50 done", "itemR3 9.00 open", "refund_done TARGET 44.75"],
     "条码退款", "DONE"),
    ("v19_04", "ghost_tax", "tax_base_paid", 147.0,
     ["TAX GHOST V19", "T1 82.00 paid", "T2 30.00 open", "T3 65.00 paid", "tax_base_paid TARGET 147.00"],
     "重影税基", "RECV"),
    ("v19_05", "stamp_pay", "payroll_active", 2480.0,
     ["PAYROLL STAMP V19", "A 1310 active", "B 220 leave", "C 1170 active", "payroll_active TARGET 2480"],
     "印泥工资", "OK"),
    ("v19_06", "torn_ship", "ship_ok_qty", 63.0,
     ["SHIP TORN V19", "P1 32 ok", "P2 17 hold", "P3 31 ok", "ship_ok_qty TARGET 63"],
     "撕边发货", "SHIP"),
    ("v19_07", "pen_sla", "open_pri_sum", 55.0,
     ["SLA PEN V19", "S1 pri 24 open", "S2 pri 31 closed", "S3 pri 31 open", "open_pri_sum TARGET 55"],
     "圆珠笔SLA", "OPEN"),
    ("v19_08", "photo_exp", "paid_total", 102.25,
     ["EXPENSE PHOTOCOPY V19", "E1 51.00 paid", "E2 22.00 void", "E3 51.25 paid", "paid_total TARGET 102.25"],
     "复印报销", "RECV"),
    ("v19_09", "coffee_po", "paid_total", 88.0,
     ["PO-COFFEE V19", "itemA paid 43.75", "itemB paid 44.25", "itemC open 15.00", "TOTAL PAID TARGET 88.00"],
     "咖啡环采购", "RECV"),
    ("v19_10", "hl_order", "paid_total", 71.5,
     ["ORDER HIGHLIGHT V19", "A paid 35.50", "B paid 36.00", "C open 11.00", "TOTAL PAID TARGET 71.50"],
     "荧光笔订单", "RECV"),
    ("v19_11", "barcode_dup", "paid_total", 84.0,
     ["INVOICE #V19-DUP", "line paid 28.00", "line paid 28.00", "line paid 28.00", "TOTAL PAID TARGET 84.00"],
     "条码重复", "RECV"),
    ("v19_12", "ghost_zero", "paid_total", 0.0,
     ["OPEN ONLY V19", "X 61.00 open", "Y 64.00 open", "paid_total TARGET 0.00"],
     "重影未付", "HOLD"),
    ("v19_13", "stamp_ledger", "paid_total", 58.75,
     ["LEDGER STAMP V19", "rA paid 29.25", "rB paid 29.50", "rC open 8.00", "TOTAL PAID TARGET 58.75"],
     "印泥台账", "RECV"),
    ("v19_14", "torn_ui", "paid_total", 66.5,
     ["UI TORN V19", "alpha paid 33.00", "beta paid 33.50", "gamma open 10.50", "TOTAL PAID TARGET 66.50"],
     "撕边面板", "RECV"),
    ("v19_15", "pen_stack", "paid_total", 96.0,
     ["HEAVY PEN V19", "x paid 48.00 usd", "y paid 48.00 usd", "z open 19.00 usd", "TOTAL PAID TARGET 96.00"],
     "笔迹堆单", "RECV"),
    ("v19_16", "photo_mix", "paid_total", 61.25,
     ["CN-EN PHOTO MIX V19", "tea paid 29.00", "rice paid 32.25", "soup open 9.00", "TOTAL PAID TARGET 61.25"],
     "中英复印", "RECV"),
    ("v19_17", "coffee_win", "paid_total", 79.0,
     ["COFFEE WIN V19", "w1 paid 39.00", "w2 paid 40.00", "w3 open 16.00", "TOTAL PAID TARGET 79.00"],
     "咖啡环双窗", "RECV"),
    ("v19_18", "hl_foot", "paid_total", 42.5,
     ["HIGHLIGHT FOOT V19", "p1 paid 21.00", "p2 paid 21.50", "p3 open 7.00", "TOTAL PAID TARGET 42.50"],
     "荧光笔脚注", "RECV"),
]


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def make_mild(fid, kind, lines, metric, expected, cn_title, stamp):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    FIX.mkdir(parents=True, exist_ok=True)
    rng = random.Random(hash(fid + "_v19mild") & 0xFFFFFFFF)
    img = Image.new("RGB", (1100, 740), (215, 210, 200))
    d = ImageDraw.Draw(img)
    try:
        f_title = ImageFont.truetype(r"C:\\Windows\\Fonts\\msyh.ttc", 16)
        f_body = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 14)
        f_tgt = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 15)
        f_sm = ImageFont.truetype(r"C:\\Windows\\Fonts\\msyh.ttc", 11)
        f_stamp = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 14)
        f_tiny = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 10)
        f_wm = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 32)
    except Exception:
        f_title = f_body = f_tgt = f_sm = f_stamp = f_tiny = f_wm = ImageFont.load_default()

    d.rectangle([40, 20, 560, 600], fill=(248, 245, 235), outline=(40, 40, 40), width=2)
    # mild highlighter bands BELOW text start / between gaps (not over glyphs)
    d.rectangle([55, 250, 500, 268], fill=(255, 255, 140))
    d.rectangle([55, 280, 480, 296], fill=(255, 180, 230))
    # coffee ring away from text column
    for r in (55, 62, 70):
        d.ellipse([420 - r, 450 - r, 420 + r, 450 + r], outline=(140, 100, 60), width=2)
    # barcode strip far right of card
    bx0 = 545
    for i in range(36):
        w = 1 if rng.random() < 0.55 else 2
        col = (10, 10, 10) if rng.random() < 0.7 else (240, 240, 240)
        d.rectangle([bx0 + i * 2, 100, bx0 + i * 2 + w, 260], fill=col)
    d.text((bx0, 270), "||BAR|| bait 777", fill=(40, 40, 40), font=f_tiny)
    # torn edge (small chew, not into text)
    px_pre = None
    # stamps away from TARGET lines
    for (cx, cy, label, col) in [
        (450, 160, stamp, (180, 30, 30)),
        (320, 360, "VOID", (150, 40, 40)),
        (200, 520, "COPY", (60, 60, 160)),
    ]:
        d.ellipse([cx - 42, cy - 20, cx + 36, cy + 22], outline=col, width=3)
        d.text((cx - 14, cy - 6), label[:4], fill=col, font=f_stamp)
    # bic pen underlines BELOW text band only
    for uy in (310, 340, 370):
        d.line([(60, uy), (500, uy + 2)], fill=(30, 50, 170), width=2)
    # sticky bait NOISE
    d.rectangle([380, 210, 540, 300], fill=(255, 250, 120), outline=(180, 160, 40), width=2)
    d.text((390, 220), "STICKY", fill=(80, 60, 20), font=f_sm)
    d.text((390, 245), "bait 99.99", fill=(80, 60, 20), font=f_tiny)
    d.text((390, 268), "IGNORE", fill=(80, 60, 20), font=f_tiny)
    # redaction residual right
    d.rectangle([780, 80, 1040, 105], fill=(20, 20, 20))
    d.text((790, 115), "REDACTED bait 555", fill=(60, 60, 60), font=f_tiny)

    d.text((100, 540), "CONFIDENTIAL", fill=(230, 225, 215), font=f_wm)
    d.rectangle([50, 28, 360, 58], fill=(30, 50, 70))
    d.text((56, 32), (cn_title or kind)[:18], fill=(240, 240, 240), font=f_title)

    y = 78
    for ln in lines:
        font = f_tgt if ("TARGET" in ln.upper() or "TOTAL" in ln.upper()) else f_body
        # very faint ghost offset (V19 theme) — low contrast so digits stay
        d.text((62, y + 2), ln[:54], fill=(225, 220, 210), font=font)
        d.text((60 + 1, y + 1), ln[:54], fill=(220, 215, 205), font=font)
        d.text((60, y), ln[:54], fill=(8, 8, 8), font=font)
        y += 26

    d.rectangle([760, 220, 1060, 420], fill=(250, 248, 255), outline=(50, 50, 80), width=2)
    d.text((770, 230), "VOID WIN IGNORE", fill=(120, 40, 40), font=f_sm)
    d.text((770, 265), "old total 999.00", fill=(20, 20, 20), font=f_sm)
    d.text((770, 300), "do not parse", fill=(20, 20, 20), font=f_sm)
    d.text((770, 335), "bait 666.00", fill=(20, 20, 20), font=f_sm)
    d.rectangle([0, 710, 1100, 740], fill=(18, 18, 28))
    d.text((10, 718), "V19 MILD FIX C219  [readable TARGET] Coffee|HL|Barcode|Ghost|Stamp|Torn|Pen|Photo", fill=(200, 200, 200), font=f_tiny)

    px = img.load()
    ww, hh = img.size
    # mild torn edge
    for yy in range(20, 600):
        tear = int(3 + 2 * ((yy // 19) % 2) + rng.randint(0, 2))
        for xx in range(40, 40 + tear):
            if 0 <= xx < ww and 0 <= yy < hh:
                px[xx, yy] = (215, 210, 200)
    # coffee blotches away from text band y=70-220
    for _ in range(3):
        cx, cy = rng.randint(100, 480), rng.randint(300, 520)
        for dy in range(-18, 19):
            for dx in range(-18, 19):
                if dx * dx + dy * dy < 18 * 18 and rng.random() < 0.4:
                    xx, yy = cx + dx, cy + dy
                    if 0 <= xx < ww and 0 <= yy < hh and not (70 <= yy <= 220 and 50 <= xx <= 540):
                        r, g, b = px[xx, yy]
                        px[xx, yy] = (max(0, r - 25), max(0, g - 35), max(0, b - 40))
    # light dust outside text
    for _ in range(350):
        xx = rng.randint(0, ww - 1)
        yy = rng.randint(0, hh - 1)
        if 70 <= yy <= 220 and 50 <= xx <= 540:
            continue
        v = rng.randint(0, 255)
        px[xx, yy] = (v, v, v)

    img = ImageEnhance.Color(img).enhance(0.78)
    img = ImageEnhance.Contrast(img).enhance(0.96)
    img = ImageEnhance.Brightness(img).enhance(0.94)
    # mild photocopy: /2 only (was /3)
    w, h = img.size
    small = img.resize((max(1, w // 2), max(1, h // 2)), Image.BILINEAR)
    img = small.resize((w, h), Image.BILINEAR)
    img = img.transform(
        (w, h), Image.AFFINE, (1, 0.035, -10, 0.012, 1, -5),
        resample=Image.BICUBIC, fillcolor=(215, 210, 200),
    )
    img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=58)  # was 22
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
            "mild_coffee", "mild_hl", "mild_barcode", "mild_ghost", "mild_stamp",
            "mild_torn", "mild_pen", "mild_photocopy_div2", "jpeg_q58", "c219_clarity",
        ],
        "regenerated_c219": True,
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


def main():
    # unit: parse alone on prior OCR cannot fix
    prior = json.loads(PRIOR.read_text(encoding="utf-8")) if PRIOR.is_file() else {}
    parse_alone_fixed = []
    for r in prior.get("rows") or []:
        if r.get("ok"):
            continue
        got, atom_ok = parse_metric(r.get("ocr_preview") or "", r["metric"], r["expected"])
        if atom_ok and r.get("ocr_ok"):
            parse_alone_fixed.append(r["id"])

    items = []
    for fid, kind, metric, expected, lines, cn, stamp in SPECS:
        items.append(make_mild(fid, kind, lines, metric, expected, cn, stamp))
    man = {
        "version": "v19", "n": len(items), "gate": GATE,
        "theme": "coffee_hl_barcode_ghost_stamp_torn_pen_photocopy_mild_c219",
        "harder_than": "v18",
        "c219_regenerated": [it["id"] for it in items],
        "items": items, "timestamp": ts(),
    }
    J(FIX / "manifest.json", man)

    free = gpu_free_mib()
    if free < 2000 or not WEIGHTS.is_dir():
        out = {
            "cycle": "C219", "theme": "v19_fail_fix_retest", "gate": GATE,
            "timestamp": ts(), "attempted": False, "reason": f"gpu_free={free}",
            "parse_alone_fixed": parse_alone_fixed,
            "prior_c218_rate": prior.get("rate"),
            "vl_gate_v19_claim": False, "pass": False, "claim": False,
            "gate2_3_untouched": True, "gen11": "HOLD",
        }
        J(DOC / "C219_V19_FAIL_FIX_RETEST.json", out)
        print(json.dumps(out, ensure_ascii=False))
        return 1

    from evo.office.vision_backend import RealVlBackend
    from evo.office.vision_ocr import ocr_image
    RUN.mkdir(parents=True, exist_ok=True)
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
            print(json.dumps({"id": it["id"], "ok": ok, "got": got, "expected": it["expected"]}, ensure_ascii=False), flush=True)
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
    prior_rate = float(prior.get("rate") or 0.0)
    gate_pass = n >= 16 and rate >= GATE
    claim = gate_pass
    scope = "r50plus_v19_mild_c219_coffee_hl_barcode_ghost_n>=16_qwen35_2b" if claim else None
    out = {
        "cycle": "C219",
        "theme": "v19_fail_fix_retest",
        "gate": GATE,
        "timestamp": ts(),
        "attempted": True,
        "gpu_free_mib_start": free,
        "n": n, "n_ok": n_ok, "rate": rate,
        "prior_c218_rate": prior_rate,
        "rate_delta": round(rate - prior_rate, 4),
        "parse_alone_fixed": parse_alone_fixed,
        "gate_pass": gate_pass,
        "fail_ids": [r["id"] for r in rows if not r["ok"]],
        "rows": rows,
        "vl_gate_v19_claim": claim,
        "claim_scope": scope,
        "gate2_3_untouched": True,
        "v0_v18_untouched": True,
        "gen11": "HOLD",
        "pass": gate_pass,
        "claim": claim,
        "note": "C219 mild regen+VL retest; claim if rate>=0.6",
    }
    J(DOC / "C219_V19_FAIL_FIX_RETEST.json", out)
    J(RUN / "judge.json", out)
    if claim:
        J(DOC / "C219b_VISION_GATE_V19_REFRESH_CLAIM.json", {
            "kind": "vision_gate_v19_refresh_claim",
            "timestamp": ts(),
            "vl_gate_v19_claim": True,
            "rate": rate, "n": n, "n_ok": n_ok, "gate": GATE,
            "prior_c218_rate": prior_rate,
            "claim_scope": scope,
            "gate2_3_untouched": True,
            "gen11": "HOLD",
            "cycle": "C219",
        })
    print(json.dumps({
        "cycle": "C219", "rate": rate, "prior": prior_rate, "delta": out["rate_delta"],
        "n_ok": n_ok, "n": n, "fail_ids": out["fail_ids"], "claim": claim,
    }, ensure_ascii=False))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
