# -*- coding: utf-8 -*-
"""C196: Vision V15 heldout — disjoint fixtures + real VL claim if rate>=0.6.
Different ids/amounts from V15 train (C192/C193). Same blur/barcode/QR/chroma/
dark/tear/polaroid/checker/stamp/xout family. Mild-readable TARGET.
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
FIX = ROOT / "evo/office/fixtures/vision_images_v15h"
WEIGHTS = ROOT / "models/Qwen3.5-2B"
RUN = ROOT / "runs/vision_v15h_c196"
PROTO = ROOT / "docs" / "蚁算_VL_GATE_V15_HELDOUT_PROTOCOL.md"

# Disjoint from V15 train amounts (C192/C193)
SPECS = [
    ("v15h_01", "blur_receipt", "paid_total", 42.25,
     ["BLUR RECEIPT V15H", "a paid 20.00", "b paid 22.25", "c open 6.00", "TOTAL PAID TARGET 42.25"],
     "运动模糊收据H", "RECV"),
    ("v15h_02", "barcode_wh", "qty_sum", 41.0,
     ["WH BARCODE V15H", "SKU1 qty 21 ok", "SKU2 qty 9 hold", "SKU3 qty 20 ok", "qty_sum TARGET 41"],
     "条码仓单H", "RECV"),
    ("v15h_03", "qr_refund", "refund_done", 22.5,
     ["QR REFUND V15H", "itemR1 10.25 done", "itemR2 12.25 done", "itemR3 4.00 open", "refund_done TARGET 22.50"],
     "二维码退款H", "DONE"),
    ("v15h_04", "chroma_tax", "tax_base_paid", 72.0,
     ["TAX CHROMA V15H", "T1 40.00 paid", "T2 15.00 open", "T3 32.00 paid", "tax_base_paid TARGET 72.00"],
     "色散税联H", "RECV"),
    ("v15h_05", "dark_payroll", "payroll_active", 1180.0,
     ["PAYROLL DARK V15H", "A 640 active", "B 110 leave", "C 540 active", "payroll_active TARGET 1180"],
     "欠曝薪资H", "OK"),
    ("v15h_06", "tear_ship", "ship_ok_qty", 31.0,
     ["SHIP TEAR V15H", "P1 16 ok", "P2 9 hold", "P3 15 ok", "ship_ok_qty TARGET 31"],
     "撕角发货H", "SHIP"),
    ("v15h_07", "polaroid_sla", "open_pri_sum", 27.0,
     ["SLA POLAROID V15H", "S1 pri 12 open", "S2 pri 18 closed", "S3 pri 15 open", "open_pri_sum TARGET 27"],
     "拍立得SLAH", "OPEN"),
    ("v15h_08", "checker_exp", "paid_total", 44.75,
     ["EXPENSE CHECKER V15H", "E1 23.50 paid", "E2 9.00 void", "E3 21.25 paid", "paid_total TARGET 44.75"],
     "棋盘报销H", "RECV"),
    ("v15h_09", "stamp_po", "paid_total", 38.25,
     ["PO-STAMP V15H", "itemA paid 19.00", "itemB paid 19.25", "itemC open 7.00", "TOTAL PAID TARGET 38.25"],
     "叠章采购H", "RECV"),
    ("v15h_10", "xout_order", "paid_total", 27.5,
     ["ORDER XOUT V15H", "A paid 14.00", "B paid 13.50", "C open 5.00", "TOTAL PAID TARGET 27.50"],
     "划线订单H", "RECV"),
    ("v15h_11", "persp_dup", "paid_total", 42.0,
     ["INVOICE #V15H-DUP", "line paid 14.00", "line paid 14.00", "line paid 14.00", "TOTAL PAID TARGET 42.00"],
     "透视重复H", "RECV"),
    ("v15h_12", "noise_zero", "paid_total", 0.0,
     ["OPEN ONLY V15H", "X 28.00 open", "Y 31.00 open", "paid_total TARGET 0.00"],
     "噪声未付H", "HOLD"),
    ("v15h_13", "blur_ledger", "paid_total", 21.75,
     ["LEDGER BLUR V15H", "rA paid 10.50", "rB paid 11.25", "rC open 3.50", "TOTAL PAID TARGET 21.75"],
     "模糊账本H", "RECV"),
    ("v15h_14", "barcode_ui", "paid_total", 35.5,
     ["UI BARCODE V15H", "alpha paid 17.25", "beta paid 18.25", "gamma open 6.00", "TOTAL PAID TARGET 35.50"],
     "条码界面H", "RECV"),
    ("v15h_15", "chroma_stack", "paid_total", 52.0,
     ["HEAVY CHROMA V15H", "x paid 26.00 usd", "y paid 26.00 usd", "z open 10.00 usd", "TOTAL PAID TARGET 52.00"],
     "色散叠窗H", "RECV"),
    ("v15h_16", "qr_mix", "paid_total", 25.25,
     ["CN-EN QR MIX V15H", "tea paid 11.00", "rice paid 14.25", "soup open 3.50", "TOTAL PAID TARGET 25.25"],
     "中英二维码H", "RECV"),
    ("v15h_17", "dark_win", "paid_total", 43.0,
     ["DARK WIN V15H", "w1 paid 21.00", "w2 paid 22.00", "w3 open 10.00", "TOTAL PAID TARGET 43.00"],
     "欠曝双窗H", "RECV"),
    ("v15h_18", "tear_foot", "paid_total", 15.75,
     ["TEAR FOOT V15H", "p1 paid 7.50", "p2 paid 8.25", "p3 open 2.50", "TOTAL PAID TARGET 15.75"],
     "撕角脚注H", "RECV"),
]


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


PROTOCOL = """# 蚁算-视 VL Gate V15 Heldout Protocol

Updated: {ts} (Asia/Shanghai)

## Purpose
Disjoint heldout for V15 train (C192/C193). Different ids/amounts;
same blur/barcode/QR/chroma/dark/tear/polaroid/checker/stamp/xout family; mild-readable TARGET.

## Gate
- rate >= **0.6**, n >= 16, real VL
- Claim only on PASS

## Honesty
- Gate2/3 untouched. V0-V14 untouched. gen11 HOLD.
"""


def make_fixture(fid, kind, lines, metric, expected, cn_title, stamp):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    FIX.mkdir(parents=True, exist_ok=True)
    rng = random.Random(hash(fid + "_v15h") & 0xFFFFFFFF)
    img = Image.new("RGB", (1080, 720), (198, 194, 186))
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

    d.rectangle([36, 18, 540, 580], fill=(242, 236, 226), outline=(35, 35, 35), width=2)
    for _ in range(14):
        x0 = rng.randint(40, 500)
        y0 = rng.randint(40, 540)
        d.arc([x0, y0, x0 + rng.randint(40, 120), y0 + rng.randint(20, 60)], 0, 180, fill=(200, 195, 185), width=1)
    d.rectangle([50, 95, 500, 118], fill=(255, 255, 120))
    d.rectangle([50, 160, 420, 182], fill=(180, 255, 180))
    d.rectangle([360, 200, 520, 280], fill=(255, 250, 120), outline=(180, 160, 40), width=2)
    d.text((370, 210), "STICKY", fill=(80, 60, 20), font=f_sm)
    d.text((370, 235), "bait 888.00", fill=(80, 60, 20), font=f_tiny)
    d.text((370, 255), "IGNORE", fill=(80, 60, 20), font=f_tiny)
    for bx in range(560, 620, 3):
        d.line([(bx, 80), (bx, 280)], fill=(10, 10, 10), width=2)
    d.text((560, 290), "BARCODE bait", fill=(60, 60, 60), font=f_tiny)
    for qi in range(8):
        for qj in range(8):
            if (qi + qj) % 2 == 0:
                d.rectangle([640 + qi * 8, 80 + qj * 8, 647 + qi * 8, 87 + qj * 8], fill=(0, 0, 0))
    d.text((640, 150), "QR bait 777", fill=(80, 80, 80), font=f_tiny)
    d.line([(50, 300), (200, 320)], fill=(180, 30, 30), width=2)
    d.line([(55, 320), (195, 300)], fill=(180, 30, 30), width=2)
    d.polygon([(36, 18), (120, 18), (36, 100)], fill=(198, 194, 186))
    d.line([(36, 100), (120, 18)], fill=(80, 60, 40), width=2)

    coffee = Image.new("RGBA", img.size, (0, 0, 0, 0))
    cd = ImageDraw.Draw(coffee)
    cd.ellipse([80, 400, 220, 540], outline=(120, 70, 30, 90), width=10)
    cd.ellipse([100, 420, 200, 520], fill=(140, 80, 40, 40))
    img = Image.alpha_composite(img.convert("RGBA"), coffee).convert("RGB")
    d = ImageDraw.Draw(img)

    for hy in (60, 200, 340, 480):
        d.ellipse([18, hy, 34, hy + 16], fill=(210, 205, 195), outline=(40, 40, 40), width=1)
    for fy in range(30, 570, 7):
        if rng.random() > 0.35:
            d.line([(40, fy), (540, fy)], fill=(195, 190, 185), width=1)

    d.text((80, 320), "CONFIDENTIAL", fill=(220, 210, 200), font=f_wm)
    d.text((100, 450), "COPY bait 777", fill=(225, 218, 208), font=f_sm)

    d.rectangle([46, 26, 330, 56], fill=(25, 45, 65))
    d.text((52, 30), (cn_title or kind)[:20], fill=(240, 240, 240), font=f_title)
    y = 70
    for ln in lines:
        font = f_tgt if ("TARGET" in ln.upper() or "TOTAL" in ln.upper()) else f_body
        d.text((55, y), ln[:54], fill=(8, 8, 8), font=font)
        y += 22

    for (cx, cy, label, col) in [(390, 140, stamp, (180, 30, 30)), (280, 250, "作废", (140, 50, 50)), (430, 300, "VOID", (150, 40, 40))]:
        d.ellipse([cx - 46, cy - 22, cx + 40, cy + 26], outline=col, width=3)
        d.text((cx - 14, cy - 6), label[:4], fill=col, font=f_stamp)

    d.rectangle([740, 200, 1020, 420], fill=(250, 248, 255), outline=(50, 50, 80), width=2)
    d.text((750, 210), "VOID WIN IGNORE", fill=(120, 40, 40), font=f_sm)
    d.text((750, 245), "old total 999.00", fill=(20, 20, 20), font=f_sm)
    d.text((750, 280), "do not parse", fill=(20, 20, 20), font=f_sm)

    d.rectangle([0, 690, 1080, 720], fill=(18, 18, 28))
    d.text((10, 698), "V15H HELDOUT C196  [readable TARGET]", fill=(200, 200, 200), font=f_tiny)

    px = img.load()
    ww, hh = img.size
    for yy in range(120, 200):
        for xx in range(50, min(500, ww - 4)):
            r, g, b = px[xx, yy]
            px[xx, yy] = (min(255, r + 18), g, max(0, b - 8))
            if xx + 2 < ww:
                r2, g2, b2 = px[xx + 2, yy]
                px[xx + 2, yy] = (max(0, r2 - 8), g2, min(255, b2 + 18))

    glare = Image.new("RGBA", img.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glare)
    gd.ellipse([140, 30, 360, 160], fill=(255, 255, 220, 55))
    img = Image.alpha_composite(img.convert("RGBA"), glare).convert("RGB")

    w, h = img.size
    img = img.transform(
        (w, h), Image.AFFINE, (1, 0.055, -18, 0.02, 1, -6),
        resample=Image.BICUBIC, fillcolor=(198, 194, 186),
    )
    img = ImageEnhance.Contrast(img).enhance(0.85)
    img = ImageEnhance.Brightness(img).enhance(0.78)
    img = img.filter(ImageFilter.GaussianBlur(radius=0.9))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=40)
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
            "motion_blur", "barcode_stripe", "qr_bait", "chromatic_fringe",
            "underexposure", "polaroid_crop", "corner_tear", "checker_jpeg",
            "overstamp_stack", "crossout_near_target", "stronger_affine", "jpeg_q40",
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
        "version": "v15_heldout", "n": len(items), "gate": GATE,
        "theme": "v15_heldout_disjoint", "harder_than": "v14_heldout",
        "items": items, "timestamp": ts(),
    }
    J(FIX / "manifest.json", man)

    free = gpu_free_mib()
    if free < 2000 or not WEIGHTS.is_dir():
        out = {
            "cycle": "C196", "theme": "vision_v15_heldout", "gate": GATE,
            "timestamp": ts(), "attempted": False, "reason": f"gpu_free={free}",
            "vl_gate_v15_heldout_claim": False, "pass": False, "claim": False,
            "gate2_3_untouched": True, "gen11": "HOLD",
        }
        J(DOC / "C196_VISION_V15_HELDOUT_SMOKE.json", out)
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
    scope = "r50plus_v15_heldout_disjoint_n>=16_c162_parse_qwen35_2b_c196" if claim else None
    out = {
        "cycle": "C196",
        "theme": "vision_v15_heldout",
        "gate": GATE,
        "timestamp": ts(),
        "attempted": True,
        "gpu_free_mib_start": free,
        "n": n, "n_ok": n_ok, "rate": rate,
        "gate_pass": gate_pass,
        "fail_ids": [r["id"] for r in rows if not r["ok"]],
        "rows": rows,
        "vl_gate_v15_heldout_claim": claim,
        "claim_scope": scope,
        "train_ref": "docs/r50/C193b_VISION_GATE_V15_CLAIM.json",
        "disjoint": True,
        "gate2_3_untouched": True,
        "v0_v14_untouched": True,
        "gen11": "HOLD",
        "pass": gate_pass,
        "claim": claim,
        "note": "V15 heldout real VL; claim only if rate>=0.6",
    }
    J(DOC / "C196_VISION_V15_HELDOUT_SMOKE.json", out)
    J(RUN / "judge.json", out)
    if claim:
        J(DOC / "C196b_VISION_GATE_V15_HELDOUT_CLAIM.json", {
            "kind": "vision_gate_v15_heldout_claim",
            "timestamp": ts(),
            "vl_gate_v15_heldout_claim": True,
            "rate": rate, "n": n, "n_ok": n_ok, "gate": GATE,
            "claim_scope": scope,
            "gate2_3_untouched": True,
            "v0_v14_untouched": True,
            "gen11": "HOLD",
            "cycle": "C196",
        })
    print(json.dumps({
        "cycle": "C196", "rate": rate, "n_ok": n_ok, "n": n,
        "fail_ids": out["fail_ids"], "claim": claim, "pass": gate_pass,
    }, ensure_ascii=False))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
