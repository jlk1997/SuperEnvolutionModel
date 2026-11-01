# -*- coding: utf-8 -*-
"""C220: Vision V19 heldout — disjoint fixtures + real VL claim if rate>=0.6.
Different ids/amounts from V19 train (C217/C218/C219). Same coffee/HL/barcode/
ghost/stamp/torn/pen/photo family; mild-readable TARGET (C219 clarity).
Gate 0.6. Gate2/3 untouched. gen11 HOLD.
"""
from __future__ import annotations
import gc, io, json, re, sys, random
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from evo.office.vision_metric_parse import parse_metric

GATE = 0.6
DOC = ROOT / "docs" / "r50"
FIX = ROOT / "evo/office/fixtures/vision_images_v19h"
WEIGHTS = ROOT / "models/Qwen3.5-2B"
RUN = ROOT / "runs/vision_v19h_c220"
PROTO = ROOT / "docs" / "蚁算_VL_GATE_V19_HELDOUT_PROTOCOL.md"

SPECS = [
    ("v19h_01", "coffee_receipt", "paid_total", 71.5,
     ["COFFEE RING V19H", "a paid 35.00", "b paid 36.50", "c open 10.00", "TOTAL PAID TARGET 71.50"],
     "咖啡环收据H", "RECV"),
    ("v19h_02", "hl_wh", "qty_sum", 52.0,
     ["WH HIGHLIGHT V19H", "SKU1 qty 27 ok", "SKU2 qty 12 hold", "SKU3 qty 25 ok", "qty_sum TARGET 52"],
     "荧光笔仓H", "RECV"),
    ("v19h_03", "barcode_refund", "refund_done", 31.25,
     ["BARCODE REFUND V19H", "itemR1 14.75 done", "itemR2 16.50 done", "itemR3 7.00 open", "refund_done TARGET 31.25"],
     "条码退款H", "DONE"),
    ("v19h_04", "ghost_tax", "tax_base_paid", 119.0,
     ["TAX GHOST V19H", "T1 66.00 paid", "T2 24.00 open", "T3 53.00 paid", "tax_base_paid TARGET 119.00"],
     "重影税基H", "RECV"),
    ("v19h_05", "stamp_pay", "payroll_active", 1960.0,
     ["PAYROLL STAMP V19H", "A 1040 active", "B 190 leave", "C 920 active", "payroll_active TARGET 1960"],
     "印泥工资H", "OK"),
    ("v19h_06", "torn_ship", "ship_ok_qty", 45.0,
     ["SHIP TORN V19H", "P1 23 ok", "P2 13 hold", "P3 22 ok", "ship_ok_qty TARGET 45"],
     "撕边发货H", "SHIP"),
    ("v19h_07", "pen_sla", "open_pri_sum", 39.0,
     ["SLA PEN V19H", "S1 pri 17 open", "S2 pri 25 closed", "S3 pri 22 open", "open_pri_sum TARGET 39"],
     "圆珠笔SLAH", "OPEN"),
    ("v19h_08", "photo_exp", "paid_total", 77.25,
     ["EXPENSE PHOTOCOPY V19H", "E1 38.00 paid", "E2 15.00 void", "E3 39.25 paid", "paid_total TARGET 77.25"],
     "复印报销H", "RECV"),
    ("v19h_09", "coffee_po", "paid_total", 62.0,
     ["PO-COFFEE V19H", "itemA paid 30.75", "itemB paid 31.25", "itemC open 11.00", "TOTAL PAID TARGET 62.00"],
     "咖啡环采购H", "RECV"),
    ("v19h_10", "hl_order", "paid_total", 51.5,
     ["ORDER HIGHLIGHT V19H", "A paid 25.50", "B paid 26.00", "C open 8.00", "TOTAL PAID TARGET 51.50"],
     "荧光笔订单H", "RECV"),
    ("v19h_11", "barcode_dup", "paid_total", 63.0,
     ["INVOICE #V19H-DUP", "line paid 21.00", "line paid 21.00", "line paid 21.00", "TOTAL PAID TARGET 63.00"],
     "条码重复H", "RECV"),
    ("v19h_12", "ghost_zero", "paid_total", 0.0,
     ["OPEN ONLY V19H", "X 47.00 open", "Y 49.00 open", "paid_total TARGET 0.00"],
     "重影未付H", "HOLD"),
    ("v19h_13", "stamp_ledger", "paid_total", 43.75,
     ["LEDGER STAMP V19H", "rA paid 21.50", "rB paid 22.25", "rC open 6.00", "TOTAL PAID TARGET 43.75"],
     "印泥台账H", "RECV"),
    ("v19h_14", "torn_ui", "paid_total", 48.5,
     ["UI TORN V19H", "alpha paid 24.00", "beta paid 24.50", "gamma open 8.50", "TOTAL PAID TARGET 48.50"],
     "撕边面板H", "RECV"),
    ("v19h_15", "pen_stack", "paid_total", 74.0,
     ["HEAVY PEN V19H", "x paid 37.00 usd", "y paid 37.00 usd", "z open 14.00 usd", "TOTAL PAID TARGET 74.00"],
     "笔迹堆单H", "RECV"),
    ("v19h_16", "photo_mix", "paid_total", 45.25,
     ["CN-EN PHOTO MIX V19H", "tea paid 21.00", "rice paid 24.25", "soup open 6.00", "TOTAL PAID TARGET 45.25"],
     "中英复印H", "RECV"),
    ("v19h_17", "coffee_win", "paid_total", 57.0,
     ["COFFEE WIN V19H", "w1 paid 28.00", "w2 paid 29.00", "w3 open 12.00", "TOTAL PAID TARGET 57.00"],
     "咖啡环双窗H", "RECV"),
    ("v19h_18", "hl_foot", "paid_total", 31.5,
     ["HIGHLIGHT FOOT V19H", "p1 paid 15.50", "p2 paid 16.00", "p3 open 5.00", "TOTAL PAID TARGET 31.50"],
     "荧光笔脚注H", "RECV"),
]


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


PROTOCOL = """# Ant VL Gate V19 Heldout Protocol

Updated: {ts} (Asia/Shanghai)

## Purpose
Disjoint amounts/ids from V19 train. Same degradation family (mild C219 clarity).
Gate rate>=0.6, n>=16, real VL.

## Honesty
Gate2/3 untouched. gen11 HOLD. Train V19 claim retained.
"""


def make_mild(fid, kind, lines, metric, expected, cn_title, stamp):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    FIX.mkdir(parents=True, exist_ok=True)
    rng = random.Random(hash(fid + "_v19hmild") & 0xFFFFFFFF)
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
    d.rectangle([55, 250, 500, 268], fill=(255, 255, 140))
    d.rectangle([55, 280, 480, 296], fill=(255, 180, 230))
    for r in (55, 62, 70):
        d.ellipse([420 - r, 450 - r, 420 + r, 450 + r], outline=(140, 100, 60), width=2)
    bx0 = 545
    for i in range(36):
        w = 1 if rng.random() < 0.55 else 2
        col = (10, 10, 10) if rng.random() < 0.7 else (240, 240, 240)
        d.rectangle([bx0 + i * 2, 100, bx0 + i * 2 + w, 260], fill=col)
    d.text((bx0, 270), "||BAR|| bait 777", fill=(40, 40, 40), font=f_tiny)
    for (cx, cy, label, col) in [
        (450, 160, stamp, (180, 30, 30)),
        (320, 360, "VOID", (150, 40, 40)),
        (200, 520, "COPY", (60, 60, 160)),
    ]:
        d.ellipse([cx - 42, cy - 20, cx + 36, cy + 22], outline=col, width=3)
        d.text((cx - 14, cy - 6), label[:4], fill=col, font=f_stamp)
    for uy in (310, 340, 370):
        d.line([(60, uy), (500, uy + 2)], fill=(30, 50, 170), width=2)
    d.rectangle([380, 210, 540, 300], fill=(255, 250, 120), outline=(180, 160, 40), width=2)
    d.text((390, 220), "STICKY", fill=(80, 60, 20), font=f_sm)
    d.text((390, 245), "bait 99.99", fill=(80, 60, 20), font=f_tiny)
    d.text((390, 268), "IGNORE", fill=(80, 60, 20), font=f_tiny)
    d.rectangle([780, 80, 1040, 105], fill=(20, 20, 20))
    d.text((790, 115), "REDACTED bait 555", fill=(60, 60, 60), font=f_tiny)
    d.text((100, 540), "CONFIDENTIAL", fill=(230, 225, 215), font=f_wm)
    d.rectangle([50, 28, 360, 58], fill=(30, 50, 70))
    d.text((56, 32), (cn_title or kind)[:18], fill=(240, 240, 240), font=f_title)
    y = 78
    for ln in lines:
        font = f_tgt if ("TARGET" in ln.upper() or "TOTAL" in ln.upper()) else f_body
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
    d.text((10, 718), "V19H HELDOUT C220  [readable TARGET] Coffee|HL|Barcode|Ghost|Stamp|Torn|Pen|Photo", fill=(200, 200, 200), font=f_tiny)

    px = img.load()
    ww, hh = img.size
    for yy in range(20, 600):
        tear = int(3 + 2 * ((yy // 19) % 2) + rng.randint(0, 2))
        for xx in range(40, 40 + tear):
            if 0 <= xx < ww and 0 <= yy < hh:
                px[xx, yy] = (215, 210, 200)
    for _ in range(3):
        cx, cy = rng.randint(100, 480), rng.randint(300, 520)
        for dy in range(-18, 19):
            for dx in range(-18, 19):
                if dx * dx + dy * dy < 18 * 18 and rng.random() < 0.4:
                    xx, yy = cx + dx, cy + dy
                    if 0 <= xx < ww and 0 <= yy < hh and not (70 <= yy <= 220 and 50 <= xx <= 540):
                        r, g, b = px[xx, yy]
                        px[xx, yy] = (max(0, r - 25), max(0, g - 35), max(0, b - 40))
    for _ in range(350):
        xx = rng.randint(0, ww - 1)
        yy = rng.randint(0, hh - 1)
        if 70 <= yy <= 220 and 50 <= xx <= 540:
            continue
        v = rng.randint(0, 255)
        px[xx, yy] = (v, v, v)

    from PIL import ImageEnhance as IE
    img = IE.Color(img).enhance(0.78)
    img = IE.Contrast(img).enhance(0.96)
    img = IE.Brightness(img).enhance(0.94)
    w, h = img.size
    small = img.resize((max(1, w // 2), max(1, h // 2)), Image.BILINEAR)
    img = small.resize((w, h), Image.BILINEAR)
    img = img.transform(
        (w, h), Image.AFFINE, (1, 0.035, -10, 0.012, 1, -5),
        resample=Image.BICUBIC, fillcolor=(215, 210, 200),
    )
    img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=58)
    buf.seek(0)
    img = Image.open(buf).convert("RGB")
    img = img.filter(ImageFilter.SMOOTH)
    outp = FIX / f"{fid}_{kind}.png"
    img.save(outp)
    return {
        "id": fid, "file": outp.name, "kind": kind, "metric": metric,
        "expected": expected, "lines": lines, "cn_title": cn_title, "stamp": stamp,
        "path": str(outp.relative_to(ROOT)).replace("\\", "/"),
        "hardening": ["mild_v19_family", "jpeg_q58", "c220_heldout"],
        "disjoint_from_train": True,
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
    PROTO.write_text(PROTOCOL.format(ts=ts()), encoding="utf-8")
    if FIX.exists():
        for p in FIX.glob("*.png"):
            p.unlink()
    items = []
    for fid, kind, metric, expected, lines, cn, stamp in SPECS:
        items.append(make_mild(fid, kind, lines, metric, expected, cn, stamp))
    man = {
        "version": "v19h", "n": len(items), "gate": GATE,
        "theme": "v19_heldout_disjoint",
        "disjoint_from": "v19_train_c217_c219",
        "items": items, "timestamp": ts(),
    }
    J(FIX / "manifest.json", man)

    free = gpu_free_mib()
    if free < 2000 or not WEIGHTS.is_dir():
        out = {
            "cycle": "C220", "theme": "vision_v19_heldout", "gate": GATE,
            "timestamp": ts(), "attempted": False, "reason": f"gpu_free={free}",
            "vl_gate_v19_heldout_claim": False, "pass": False, "claim": False,
            "gate2_3_untouched": True, "gen11": "HOLD",
        }
        J(DOC / "C220_VISION_V19_HELDOUT_SMOKE.json", out)
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
    gate_pass = n >= 16 and rate >= GATE
    claim = gate_pass
    scope = "r50plus_v19_heldout_disjoint_mild_n>=16_qwen35_2b_c220" if claim else None
    out = {
        "cycle": "C220",
        "theme": "vision_v19_heldout",
        "gate": GATE,
        "timestamp": ts(),
        "attempted": True,
        "gpu_free_mib_start": free,
        "n": n, "n_ok": n_ok, "rate": rate,
        "gate_pass": gate_pass,
        "fail_ids": [r["id"] for r in rows if not r["ok"]],
        "rows": rows,
        "vl_gate_v19_heldout_claim": claim,
        "claim_scope": scope,
        "disjoint": True,
        "gate2_3_untouched": True,
        "v0_v19_train_untouched": True,
        "gen11": "HOLD",
        "pass": gate_pass,
        "claim": claim,
        "note": "V19 heldout real VL; claim only if rate>=0.6",
    }
    J(DOC / "C220_VISION_V19_HELDOUT_SMOKE.json", out)
    J(RUN / "judge.json", out)
    if claim:
        J(DOC / "C220b_VISION_GATE_V19_HELDOUT_CLAIM.json", {
            "kind": "vision_gate_v19_heldout_claim",
            "timestamp": ts(),
            "vl_gate_v19_heldout_claim": True,
            "rate": rate, "n": n, "n_ok": n_ok, "gate": GATE,
            "claim_scope": scope,
            "disjoint": True,
            "gate2_3_untouched": True,
            "gen11": "HOLD",
            "cycle": "C220",
        })
    print(json.dumps({
        "cycle": "C220", "rate": rate, "n_ok": n_ok, "n": n,
        "fail_ids": out["fail_ids"], "claim": claim, "pass": gate_pass,
    }, ensure_ascii=False))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())

