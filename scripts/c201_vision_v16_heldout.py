# -*- coding: utf-8 -*-
"""C201: Vision V16 heldout — disjoint fixtures + real VL claim if rate>=0.6.
Different ids/amounts from V16 train (C197/C198). Same dbl/LED/rain/crumple/
postage/wrap/hl/dust/sepia family. Mild-readable TARGET.
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
FIX = ROOT / "evo/office/fixtures/vision_images_v16h"
WEIGHTS = ROOT / "models/Qwen3.5-2B"
RUN = ROOT / "runs/vision_v16h_c201"
PROTO = ROOT / "docs" / "蚁算_VL_GATE_V16_HELDOUT_PROTOCOL.md"

# Disjoint from V16 train amounts (C197/C198)
SPECS = [
    ("v16h_01", "dbl_receipt", "paid_total", 47.75,
     ["DBL EXPOSURE V16H", "a paid 23.50", "b paid 24.25", "c open 8.00", "TOTAL PAID TARGET 47.75"],
     "双曝收据H", "RECV"),
    ("v16h_02", "led_wh", "qty_sum", 44.0,
     ["WH LED BAND V16H", "SKU1 qty 22 ok", "SKU2 qty 11 hold", "SKU3 qty 22 ok", "qty_sum TARGET 44"],
     "灯带仓库H", "RECV"),
    ("v16h_03", "rain_refund", "refund_done", 25.5,
     ["RAIN REFUND V16H", "itemR1 12.00 done", "itemR2 13.50 done", "itemR3 5.00 open", "refund_done TARGET 25.50"],
     "雨纹退款H", "DONE"),
    ("v16h_04", "crumple_tax", "tax_base_paid", 81.0,
     ["TAX CRUMPLE V16H", "T1 45.00 paid", "T2 18.00 open", "T3 36.00 paid", "tax_base_paid TARGET 81.00"],
     "皱影税基H", "RECV"),
    ("v16h_05", "postage_pay", "payroll_active", 1420.0,
     ["PAYROLL POSTAGE V16H", "A 760 active", "B 130 leave", "C 660 active", "payroll_active TARGET 1420"],
     "邮戳薪资H", "OK"),
    ("v16h_06", "wrap_ship", "ship_ok_qty", 34.0,
     ["SHIP WRAP V16H", "P1 17 ok", "P2 11 hold", "P3 17 ok", "ship_ok_qty TARGET 34"],
     "膜光发货H", "SHIP"),
    ("v16h_07", "hl_sla", "open_pri_sum", 31.0,
     ["SLA HIGHLIGHT V16H", "S1 pri 14 open", "S2 pri 19 closed", "S3 pri 17 open", "open_pri_sum TARGET 31"],
     "荧光笔SLAH", "OPEN"),
    ("v16h_08", "torn_exp", "paid_total", 58.5,
     ["EXPENSE TORNBC V16H", "E1 29.00 paid", "E2 12.00 void", "E3 29.50 paid", "paid_total TARGET 58.50"],
     "撕条报销H", "RECV"),
    ("v16h_09", "mw_po", "paid_total", 51.25,
     ["PO-MICROWAVE V16H", "itemA paid 25.50", "itemB paid 25.75", "itemC open 9.00", "TOTAL PAID TARGET 51.25"],
     "微波采购H", "RECV"),
    ("v16h_10", "dust_order", "paid_total", 37.0,
     ["ORDER DUST V16H", "A paid 18.00", "B paid 19.00", "C open 7.00", "TOTAL PAID TARGET 37.00"],
     "尘斑订单H", "RECV"),
    ("v16h_11", "sepia_dup", "paid_total", 48.0,
     ["INVOICE #V16H-DUP", "line paid 16.00", "line paid 16.00", "line paid 16.00", "TOTAL PAID TARGET 48.00"],
     "老化重复H", "RECV"),
    ("v16h_12", "rain_zero", "paid_total", 0.0,
     ["OPEN ONLY V16H", "X 33.00 open", "Y 36.00 open", "paid_total TARGET 0.00"],
     "雨纹未付H", "HOLD"),
    ("v16h_13", "dbl_ledger", "paid_total", 33.5,
     ["LEDGER DBL V16H", "rA paid 16.50", "rB paid 17.00", "rC open 4.50", "TOTAL PAID TARGET 33.50"],
     "双曝账本H", "RECV"),
    ("v16h_14", "led_ui", "paid_total", 41.75,
     ["UI LED V16H", "alpha paid 20.50", "beta paid 21.25", "gamma open 6.50", "TOTAL PAID TARGET 41.75"],
     "灯带界面H", "RECV"),
    ("v16h_15", "wrap_stack", "paid_total", 59.0,
     ["HEAVY WRAP V16H", "x paid 29.50 usd", "y paid 29.50 usd", "z open 12.00 usd", "TOTAL PAID TARGET 59.00"],
     "膜光堆叠H", "RECV"),
    ("v16h_16", "hl_mix", "paid_total", 33.25,
     ["CN-EN HL MIX V16H", "tea paid 15.00", "rice paid 18.25", "soup open 5.00", "TOTAL PAID TARGET 33.25"],
     "中英荧光笔H", "RECV"),
    ("v16h_17", "crumple_win", "paid_total", 49.0,
     ["CRUMPLE WIN V16H", "w1 paid 24.00", "w2 paid 25.00", "w3 open 11.00", "TOTAL PAID TARGET 49.00"],
     "皱影双窗H", "RECV"),
    ("v16h_18", "postage_foot", "paid_total", 22.75,
     ["POSTAGE FOOT V16H", "p1 paid 11.00", "p2 paid 11.75", "p3 open 4.00", "TOTAL PAID TARGET 22.75"],
     "邮戳脚注H", "RECV"),
]


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


PROTOCOL = """# 蚁算-视 VL Gate V16 Heldout Protocol

Updated: {ts} (Asia/Shanghai)

## Purpose
Disjoint heldout for V16 train (C197/C198). Different ids/amounts;
same dbl/LED/rain/crumple/postage/wrap/hl/dust/sepia family; mild-readable TARGET.

## Gate
- rate >= **0.6**, n >= 16, real VL
- Claim only on PASS

## Honesty
- Gate2/3 untouched. V0-V15 untouched. gen11 HOLD.
"""


def make_fixture(fid, kind, lines, metric, expected, cn_title, stamp):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    FIX.mkdir(parents=True, exist_ok=True)
    rng = random.Random(hash(fid + "_v16h") & 0xFFFFFFFF)
    img = Image.new("RGB", (1100, 740), (188, 182, 172))
    d = ImageDraw.Draw(img)
    try:
        f_title = ImageFont.truetype(r"C:\\Windows\\Fonts\\msyh.ttc", 15)
        f_body = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 13)
        f_tgt = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 14)
        f_sm = ImageFont.truetype(r"C:\\Windows\\Fonts\\msyh.ttc", 11)
        f_stamp = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 14)
        f_tiny = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 10)
        f_wm = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 36)
    except Exception:
        f_title = f_body = f_tgt = f_sm = f_stamp = f_tiny = f_wm = ImageFont.load_default()

    d.rectangle([40, 20, 560, 600], fill=(238, 230, 218), outline=(40, 40, 40), width=2)
    for _ in range(18):
        x0 = rng.randint(45, 520)
        y0 = rng.randint(40, 560)
        d.arc([x0, y0, x0 + rng.randint(50, 140), y0 + rng.randint(25, 70)], 0, 200, fill=(175, 168, 155), width=2)
    d.rectangle([55, 100, 520, 124], fill=(255, 255, 90))
    d.rectangle([55, 170, 430, 194], fill=(255, 120, 220))
    d.rectangle([370, 210, 540, 300], fill=(255, 248, 100), outline=(180, 160, 40), width=2)
    d.text((380, 220), "STICKY", fill=(80, 60, 20), font=f_sm)
    d.text((380, 245), "bait 888.00", fill=(80, 60, 20), font=f_tiny)
    d.text((380, 268), "IGNORE", fill=(80, 60, 20), font=f_tiny)
    for by in range(30, 580, 11):
        d.rectangle([40, by, 560, by + 2], fill=(210, 220, 230))
    for bx in range(580, 650, 2):
        d.line([(bx, 90), (bx, 300)], fill=(5, 5, 5), width=2)
    d.polygon([(580, 90), (650, 90), (640, 140), (590, 145)], fill=(188, 182, 172))
    d.text((580, 310), "TORN BARCODE", fill=(60, 60, 60), font=f_tiny)
    for i, (sx, sy) in enumerate([(700, 80), (780, 80), (700, 160)]):
        d.rectangle([sx, sy, sx + 60, sy + 50], outline=(120, 40, 40), width=2)
        d.text((sx + 6, sy + 12), f"POST{i+1}", fill=(120, 40, 40), font=f_tiny)
        d.text((sx + 6, sy + 28), "9.99", fill=(80, 80, 80), font=f_tiny)
    for _ in range(40):
        rx = rng.randint(40, 1050)
        ry = rng.randint(20, 700)
        d.line([(rx, ry), (rx + 2, ry + rng.randint(20, 50))], fill=(160, 170, 190), width=1)
    wrap = Image.new("RGBA", img.size, (0, 0, 0, 0))
    wd = ImageDraw.Draw(wrap)
    wd.ellipse([120, 40, 400, 180], fill=(255, 255, 255, 45))
    wd.ellipse([450, 400, 700, 620], fill=(200, 220, 255, 35))
    img = Image.alpha_composite(img.convert("RGBA"), wrap).convert("RGB")
    d = ImageDraw.Draw(img)
    coffee = Image.new("RGBA", img.size, (0, 0, 0, 0))
    cd = ImageDraw.Draw(coffee)
    cd.ellipse([90, 420, 240, 560], outline=(110, 60, 25, 100), width=12)
    cd.ellipse([110, 440, 220, 540], fill=(130, 70, 35, 45))
    img = Image.alpha_composite(img.convert("RGBA"), coffee).convert("RGB")
    d = ImageDraw.Draw(img)
    d.text((90, 330), "CONFIDENTIAL", fill=(210, 200, 190), font=f_wm)
    d.text((110, 470), "COPY bait 777", fill=(220, 212, 200), font=f_sm)
    d.rectangle([50, 28, 340, 58], fill=(30, 50, 70))
    d.text((56, 32), (cn_title or kind)[:20], fill=(240, 240, 240), font=f_title)
    y = 72
    for ln in lines:
        font = f_tgt if ("TARGET" in ln.upper() or "TOTAL" in ln.upper()) else f_body
        d.text((58 + 2, y + 1), ln[:54], fill=(200, 195, 185), font=font)
        d.text((58, y), ln[:54], fill=(10, 10, 10), font=font)
        y += 22
    for (cx, cy, label, col) in [(400, 145, stamp, (180, 30, 30)), (290, 255, "作废", (140, 50, 50)), (450, 320, "VOID", (150, 40, 40))]:
        d.ellipse([cx - 46, cy - 22, cx + 40, cy + 26], outline=col, width=3)
        d.text((cx - 14, cy - 6), label[:4], fill=col, font=f_stamp)
    d.rectangle([760, 220, 1060, 450], fill=(250, 248, 255), outline=(50, 50, 80), width=2)
    d.text((770, 230), "VOID WIN IGNORE", fill=(120, 40, 40), font=f_sm)
    d.text((770, 265), "old total 999.00", fill=(20, 20, 20), font=f_sm)
    d.text((770, 300), "do not parse", fill=(20, 20, 20), font=f_sm)
    d.rectangle([0, 710, 1100, 740], fill=(18, 18, 28))
    d.text((10, 718), "V16H HELDOUT C201  [readable TARGET]", fill=(200, 200, 200), font=f_tiny)
    px = img.load()
    ww, hh = img.size
    for _ in range(2200):
        xx = rng.randint(0, ww - 1)
        yy = rng.randint(0, hh - 1)
        v = rng.randint(0, 255)
        px[xx, yy] = (v, v, v)
    for yy in range(100, 220):
        for xx in range(50, min(520, ww - 4)):
            r, g, b = px[xx, yy]
            px[xx, yy] = (min(255, r + 22), g, max(0, b - 10))
            if xx + 3 < ww:
                r2, g2, b2 = px[xx + 3, yy]
                px[xx + 3, yy] = (max(0, r2 - 10), g2, min(255, b2 + 22))
    for mx in range(45, 540, 4):
        for my in range(30, 590, 7):
            r, g, b = px[mx, my]
            px[mx, my] = (min(255, r + 8), g, min(255, b + 8))
    img = ImageEnhance.Color(img).enhance(0.55)
    img = ImageEnhance.Contrast(img).enhance(0.82)
    img = ImageEnhance.Brightness(img).enhance(0.72)
    w, h = img.size
    img = img.transform(
        (w, h), Image.AFFINE, (1, 0.06, -20, 0.022, 1, -7),
        resample=Image.BICUBIC, fillcolor=(188, 182, 172),
    )
    img = img.filter(ImageFilter.GaussianBlur(radius=1.05))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=36)
    buf.seek(0)
    img = Image.open(buf).convert("RGB")
    img = img.filter(ImageFilter.SMOOTH)
    outp = FIX / f"{fid}_{kind}.png"
    img.save(outp)
    return {
        "id": fid, "file": outp.name, "kind": kind, "metric": metric,
        "expected": expected, "lines": lines, "cn_title": cn_title, "stamp": stamp,
        "path": str(outp.relative_to(ROOT)).replace("\\", "/"),
        "disjoint_from_train": True,
        "hardening": [
            "double_exposure", "led_banding", "rain_streaks", "crumpled_shadow",
            "postage_stamp_stack", "plastic_wrap_glare", "highlighter_bleed",
            "torn_barcode", "microwave_moire", "dust_speckle", "sepia_age", "jpeg_q36",
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


def main():
    PROTO.write_text(PROTOCOL.format(ts=ts()), encoding="utf-8")
    if FIX.exists():
        for p in FIX.glob("*.png"):
            p.unlink()
    items = []
    for fid, kind, metric, expected, lines, cn, stamp in SPECS:
        items.append(make_fixture(fid, kind, lines, metric, expected, cn, stamp))
    man = {
        "version": "v16_heldout", "n": len(items), "gate": GATE,
        "theme": "v16_heldout_disjoint", "harder_than": "v15_heldout",
        "items": items, "timestamp": ts(),
    }
    J(FIX / "manifest.json", man)

    free = gpu_free_mib()
    if free < 2000 or not WEIGHTS.is_dir():
        out = {
            "cycle": "C201", "theme": "vision_v16_heldout", "gate": GATE,
            "timestamp": ts(), "attempted": False, "reason": f"gpu_free={free}",
            "vl_gate_v16_heldout_claim": False, "pass": False, "claim": False,
            "gate2_3_untouched": True, "gen11": "HOLD",
        }
        J(DOC / "C201_VISION_V16_HELDOUT_SMOKE.json", out)
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
    scope = "r50plus_v16_heldout_disjoint_n>=16_c162_parse_qwen35_2b_c201" if claim else None
    out = {
        "cycle": "C201",
        "theme": "vision_v16_heldout",
        "gate": GATE,
        "timestamp": ts(),
        "attempted": True,
        "gpu_free_mib_start": free,
        "n": n, "n_ok": n_ok, "rate": rate,
        "gate_pass": gate_pass,
        "fail_ids": [r["id"] for r in rows if not r["ok"]],
        "rows": rows,
        "vl_gate_v16_heldout_claim": claim,
        "claim_scope": scope,
        "train_ref": "docs/r50/C198b_VISION_GATE_V16_CLAIM.json",
        "disjoint": True,
        "gate2_3_untouched": True,
        "v0_v15_untouched": True,
        "gen11": "HOLD",
        "pass": gate_pass,
        "claim": claim,
        "note": "V16 heldout real VL; claim only if rate>=0.6",
    }
    J(DOC / "C201_VISION_V16_HELDOUT_SMOKE.json", out)
    J(RUN / "judge.json", out)
    if claim:
        J(DOC / "C201b_VISION_GATE_V16_HELDOUT_CLAIM.json", {
            "kind": "vision_gate_v16_heldout_claim",
            "timestamp": ts(),
            "vl_gate_v16_heldout_claim": True,
            "rate": rate, "n": n, "n_ok": n_ok, "gate": GATE,
            "claim_scope": scope,
            "gate2_3_untouched": True,
            "v0_v15_untouched": True,
            "gen11": "HOLD",
            "cycle": "C201",
        })
    print(json.dumps({
        "cycle": "C201", "rate": rate, "n_ok": n_ok, "n": n,
        "fail_ids": out["fail_ids"], "claim": claim, "pass": gate_pass,
    }, ensure_ascii=False))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
