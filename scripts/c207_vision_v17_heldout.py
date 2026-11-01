# -*- coding: utf-8 -*-
"""C207: Vision V17 heldout — disjoint fixtures + real VL claim if rate>=0.6.
Different ids/amounts from V17 train (C202/C203). Same oil/frost/ink/carbon/
staple/fold/uv/skew family. Mild-readable TARGET.
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
FIX = ROOT / "evo/office/fixtures/vision_images_v17h"
WEIGHTS = ROOT / "models/Qwen3.5-2B"
RUN = ROOT / "runs/vision_v17h_c207"
PROTO = ROOT / "docs" / "蚁算_VL_GATE_V17_HELDOUT_PROTOCOL.md"

# Disjoint from V17 train amounts (C202/C203)
SPECS = [
    ("v17h_01", "oil_receipt", "paid_total", 53.5,
     ["OIL SMEAR V17H", "a paid 26.00", "b paid 27.50", "c open 9.00", "TOTAL PAID TARGET 53.50"],
     "油污收据H", "RECV"),
    ("v17h_02", "frost_wh", "qty_sum", 38.0,
     ["WH FROST V17H", "SKU1 qty 19 ok", "SKU2 qty 9 hold", "SKU3 qty 19 ok", "qty_sum TARGET 38"],
     "结霜仓库H", "RECV"),
    ("v17h_03", "ink_refund", "refund_done", 28.75,
     ["INK BLEED REFUND V17H", "itemR1 13.25 done", "itemR2 15.50 done", "itemR3 6.00 open", "refund_done TARGET 28.75"],
     "墨渗退款H", "DONE"),
    ("v17h_04", "carbon_tax", "tax_base_paid", 97.0,
     ["TAX CARBON V17H", "T1 52.00 paid", "T2 19.00 open", "T3 45.00 paid", "tax_base_paid TARGET 97.00"],
     "复写税基H", "RECV"),
    ("v17h_05", "staple_pay", "payroll_active", 1560.0,
     ["PAYROLL STAPLE V17H", "A 820 active", "B 140 leave", "C 740 active", "payroll_active TARGET 1560"],
     "钉影薪资H", "OK"),
    ("v17h_06", "fold_ship", "ship_ok_qty", 39.0,
     ["SHIP FOLD V17H", "P1 20 ok", "P2 10 hold", "P3 19 ok", "ship_ok_qty TARGET 39"],
     "折痕发货H", "SHIP"),
    ("v17h_07", "uv_sla", "open_pri_sum", 29.0,
     ["SLA UV V17H", "S1 pri 13 open", "S2 pri 21 closed", "S3 pri 16 open", "open_pri_sum TARGET 29"],
     "紫外SLAH", "OPEN"),
    ("v17h_08", "skew_exp", "paid_total", 71.25,
     ["EXPENSE SKEW V17H", "E1 35.50 paid", "E2 14.00 void", "E3 35.75 paid", "paid_total TARGET 71.25"],
     "斜扫报销H", "RECV"),
    ("v17h_09", "oil_po", "paid_total", 58.0,
     ["PO-OIL V17H", "itemA paid 28.75", "itemB paid 29.25", "itemC open 11.00", "TOTAL PAID TARGET 58.00"],
     "油污采购H", "RECV"),
    ("v17h_10", "frost_order", "paid_total", 42.5,
     ["ORDER FROST V17H", "A paid 21.00", "B paid 21.50", "C open 8.00", "TOTAL PAID TARGET 42.50"],
     "结霜订单H", "RECV"),
    ("v17h_11", "carbon_dup", "paid_total", 57.0,
     ["INVOICE #V17H-DUP", "line paid 19.00", "line paid 19.00", "line paid 19.00", "TOTAL PAID TARGET 57.00"],
     "复写重复H", "RECV"),
    ("v17h_12", "ink_zero", "paid_total", 0.0,
     ["OPEN ONLY V17H", "X 41.00 open", "Y 44.00 open", "paid_total TARGET 0.00"],
     "墨渗未付H", "HOLD"),
    ("v17h_13", "staple_ledger", "paid_total", 39.75,
     ["LEDGER STAPLE V17H", "rA paid 19.50", "rB paid 20.25", "rC open 5.50", "TOTAL PAID TARGET 39.75"],
     "钉影账本H", "RECV"),
    ("v17h_14", "fold_ui", "paid_total", 48.5,
     ["UI FOLD V17H", "alpha paid 24.00", "beta paid 24.50", "gamma open 7.50", "TOTAL PAID TARGET 48.50"],
     "折痕界面H", "RECV"),
    ("v17h_15", "uv_stack", "paid_total", 64.0,
     ["HEAVY UV V17H", "x paid 32.00 usd", "y paid 32.00 usd", "z open 13.00 usd", "TOTAL PAID TARGET 64.00"],
     "紫外堆叠H", "RECV"),
    ("v17h_16", "skew_mix", "paid_total", 36.5,
     ["CN-EN SKEW MIX V17H", "tea paid 17.00", "rice paid 19.50", "soup open 6.00", "TOTAL PAID TARGET 36.50"],
     "中英斜扫H", "RECV"),
    ("v17h_17", "oil_win", "paid_total", 55.0,
     ["OIL WIN V17H", "w1 paid 27.00", "w2 paid 28.00", "w3 open 12.00", "TOTAL PAID TARGET 55.00"],
     "油污双窗H", "RECV"),
    ("v17h_18", "frost_foot", "paid_total", 27.0,
     ["FROST FOOT V17H", "p1 paid 13.25", "p2 paid 13.75", "p3 open 4.50", "TOTAL PAID TARGET 27.00"],
     "结霜脚注H", "RECV"),
]


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


PROTOCOL = """# 蚁算-视 VL Gate V17 Heldout Protocol

Updated: {ts} (Asia/Shanghai)

## Purpose
Disjoint heldout for V17 train (C202/C203). Different ids/amounts;
same oil/frost/ink/carbon/staple/fold/uv/skew family; mild-readable TARGET.

## Gate
- rate >= **0.6**, n >= 16, real VL
- Claim only on PASS

## Honesty
- Gate2/3 untouched. V0-V16 untouched. gen11 HOLD.
"""


def make_fixture(fid, kind, lines, metric, expected, cn_title, stamp):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    FIX.mkdir(parents=True, exist_ok=True)
    rng = random.Random(hash(fid + "_v17h") & 0xFFFFFFFF)
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
    d.text((10, 718), "V17H HELDOUT C207  [readable TARGET]", fill=(200, 200, 200), font=f_tiny)
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
    # V17-family: slightly harder jpeg/skew than V16h
    img = ImageEnhance.Color(img).enhance(0.55)
    img = ImageEnhance.Contrast(img).enhance(0.78)
    img = ImageEnhance.Brightness(img).enhance(0.70)
    w, h = img.size
    img = img.transform(
        (w, h), Image.AFFINE, (1, 0.085, -28, 0.03, 1, -10),
        resample=Image.BICUBIC, fillcolor=(188, 182, 172),
    )
    img = img.filter(ImageFilter.GaussianBlur(radius=1.15))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=32)
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
            "oil_smear", "frost_glass", "ink_bleed", "carbon_copy_ghost",
            "stapler_shadow", "fold_crease_stack", "uv_purple_cast",
            "scanner_skew_plus", "jpeg_q32",
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
        "version": "v17_heldout", "n": len(items), "gate": GATE,
        "theme": "v17_heldout_disjoint", "harder_than": "v16_heldout",
        "items": items, "timestamp": ts(),
    }
    J(FIX / "manifest.json", man)

    free = gpu_free_mib()
    if free < 2000 or not WEIGHTS.is_dir():
        out = {
            "cycle": "C207", "theme": "vision_v17_heldout", "gate": GATE,
            "timestamp": ts(), "attempted": False, "reason": f"gpu_free={free}",
            "vl_gate_v17_heldout_claim": False, "pass": False, "claim": False,
            "gate2_3_untouched": True, "gen11": "HOLD",
        }
        J(DOC / "C207_VISION_V17_HELDOUT_SMOKE.json", out)
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
    scope = "r50plus_v17_heldout_disjoint_n>=16_c162_parse_qwen35_2b_c207" if claim else None
    out = {
        "cycle": "C207",
        "theme": "vision_v17_heldout",
        "gate": GATE,
        "timestamp": ts(),
        "attempted": True,
        "gpu_free_mib_start": free,
        "n": n, "n_ok": n_ok, "rate": rate,
        "gate_pass": gate_pass,
        "fail_ids": [r["id"] for r in rows if not r["ok"]],
        "rows": rows,
        "vl_gate_v17_heldout_claim": claim,
        "claim_scope": scope,
        "train_ref": "docs/r50/C203b_VISION_GATE_V17_CLAIM.json",
        "disjoint": True,
        "gate2_3_untouched": True,
        "v0_v16_untouched": True,
        "gen11": "HOLD",
        "pass": gate_pass,
        "claim": claim,
        "note": "V17 heldout real VL; claim only if rate>=0.6",
    }
    J(DOC / "C207_VISION_V17_HELDOUT_SMOKE.json", out)
    J(RUN / "judge.json", out)
    if claim:
        J(DOC / "C207b_VISION_GATE_V17_HELDOUT_CLAIM.json", {
            "kind": "vision_gate_v17_heldout_claim",
            "timestamp": ts(),
            "vl_gate_v17_heldout_claim": True,
            "rate": rate, "n": n, "n_ok": n_ok, "gate": GATE,
            "claim_scope": scope,
            "gate2_3_untouched": True,
            "v0_v16_untouched": True,
            "gen11": "HOLD",
            "cycle": "C207",
        })
    print(json.dumps({
        "cycle": "C207", "rate": rate, "n_ok": n_ok, "n": n,
        "fail_ids": out["fail_ids"], "claim": claim, "pass": gate_pass,
    }, ensure_ascii=False))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
