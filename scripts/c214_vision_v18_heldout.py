# -*- coding: utf-8 -*-
"""C214: Vision V18 heldout — disjoint fixtures + real VL claim if rate>=0.6.
Different ids/amounts from V18 train (C208/C209/C213). Same bleach/halftone/
crayon/thermal/punch/clip/redact/finger family; mild-readable TARGET (C213 clarity).
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
FIX = ROOT / "evo/office/fixtures/vision_images_v18h"
WEIGHTS = ROOT / "models/Qwen3.5-2B"
RUN = ROOT / "runs/vision_v18h_c214"
PROTO = ROOT / "docs" / "蚁算_VL_GATE_V18_HELDOUT_PROTOCOL.md"

# Disjoint from V18 train amounts (C208/C213)
SPECS = [
    ("v18h_01", "bleach_receipt", "paid_total", 64.5,
     ["BLEACH WASHOUT V18H", "a paid 31.00", "b paid 33.50", "c open 9.00", "TOTAL PAID TARGET 64.50"],
     "漂白收据H", "RECV"),
    ("v18h_02", "halftone_wh", "qty_sum", 41.0,
     ["WH HALFTONE V18H", "SKU1 qty 22 ok", "SKU2 qty 8 hold", "SKU3 qty 19 ok", "qty_sum TARGET 41"],
     "网点仓库H", "RECV"),
    ("v18h_03", "crayon_refund", "refund_done", 27.5,
     ["CRAYON REFUND V18H", "itemR1 12.25 done", "itemR2 15.25 done", "itemR3 6.00 open", "refund_done TARGET 27.50"],
     "蜡笔退款H", "DONE"),
    ("v18h_04", "thermal_tax", "tax_base_paid", 101.0,
     ["TAX THERMAL V18H", "T1 55.00 paid", "T2 21.00 open", "T3 46.00 paid", "tax_base_paid TARGET 101.00"],
     "热敏税基H", "RECV"),
    ("v18h_05", "punch_pay", "payroll_active", 1730.0,
     ["PAYROLL PUNCH V18H", "A 910 active", "B 160 leave", "C 820 active", "payroll_active TARGET 1730"],
     "打孔薪资H", "OK"),
    ("v18h_06", "clip_ship", "ship_ok_qty", 37.0,
     ["SHIP CLIP V18H", "P1 19 ok", "P2 11 hold", "P3 18 ok", "ship_ok_qty TARGET 37"],
     "夹影发货H", "SHIP"),
    ("v18h_07", "redact_sla", "open_pri_sum", 33.0,
     ["SLA REDACT V18H", "S1 pri 15 open", "S2 pri 22 closed", "S3 pri 18 open", "open_pri_sum TARGET 33"],
     "涂黑SLAH", "OPEN"),
    ("v18h_08", "finger_exp", "paid_total", 69.25,
     ["EXPENSE FINGER V18H", "E1 34.00 paid", "E2 12.00 void", "E3 35.25 paid", "paid_total TARGET 69.25"],
     "指纹报销H", "RECV"),
    ("v18h_09", "bleach_po", "paid_total", 54.0,
     ["PO-BLEACH V18H", "itemA paid 26.75", "itemB paid 27.25", "itemC open 10.00", "TOTAL PAID TARGET 54.00"],
     "漂白采购H", "RECV"),
    ("v18h_10", "halftone_order", "paid_total", 44.5,
     ["ORDER HALFTONE V18H", "A paid 22.00", "B paid 22.50", "C open 7.00", "TOTAL PAID TARGET 44.50"],
     "网点订单H", "RECV"),
    ("v18h_11", "thermal_dup", "paid_total", 54.0,
     ["INVOICE #V18H-DUP", "line paid 18.00", "line paid 18.00", "line paid 18.00", "TOTAL PAID TARGET 54.00"],
     "热敏重复H", "RECV"),
    ("v18h_12", "crayon_zero", "paid_total", 0.0,
     ["OPEN ONLY V18H", "X 39.00 open", "Y 41.00 open", "paid_total TARGET 0.00"],
     "蜡笔未付H", "HOLD"),
    ("v18h_13", "punch_ledger", "paid_total", 37.75,
     ["LEDGER PUNCH V18H", "rA paid 18.50", "rB paid 19.25", "rC open 5.00", "TOTAL PAID TARGET 37.75"],
     "打孔账本H", "RECV"),
    ("v18h_14", "clip_ui", "paid_total", 41.5,
     ["UI CLIP V18H", "alpha paid 20.50", "beta paid 21.00", "gamma open 6.50", "TOTAL PAID TARGET 41.50"],
     "夹影界面H", "RECV"),
    ("v18h_15", "redact_stack", "paid_total", 62.0,
     ["HEAVY REDACT V18H", "x paid 31.00 usd", "y paid 31.00 usd", "z open 12.00 usd", "TOTAL PAID TARGET 62.00"],
     "涂黑堆叠H", "RECV"),
    ("v18h_16", "finger_mix", "paid_total", 38.5,
     ["CN-EN FINGER MIX V18H", "tea paid 18.00", "rice paid 20.50", "soup open 5.00", "TOTAL PAID TARGET 38.50"],
     "中英指纹H", "RECV"),
    ("v18h_17", "bleach_win", "paid_total", 49.0,
     ["BLEACH WIN V18H", "w1 paid 24.00", "w2 paid 25.00", "w3 open 11.00", "TOTAL PAID TARGET 49.00"],
     "漂白双窗H", "RECV"),
    ("v18h_18", "halftone_foot", "paid_total", 26.5,
     ["HALFTONE FOOT V18H", "p1 paid 13.00", "p2 paid 13.50", "p3 open 4.00", "TOTAL PAID TARGET 26.50"],
     "网点脚注H", "RECV"),
]


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


PROTOCOL = """# 蚁算-视 VL Gate V18 Heldout Protocol

Updated: {ts} (Asia/Shanghai)

## Purpose
Disjoint heldout for V18 train (C208/C209/C213). Different ids/amounts;
same bleach/halftone/crayon/thermal/punch/clip/redact/finger family;
mild-readable TARGET (C213 clarity level).

## Gate
- rate >= **0.6**, n >= 16, real VL
- Claim only after smoke

## Honesty
- V18 train claim retained/refreshed separately (C213)
- Gate2/3 untouched. gen11 HOLD. No fake VL scores.
"""


def make_mild(fid, kind, lines, metric, expected, cn_title, stamp):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    FIX.mkdir(parents=True, exist_ok=True)
    rng = random.Random(hash(fid + "_v18h") & 0xFFFFFFFF)
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
    for _ in range(6):
        x0 = rng.randint(45, 500)
        y0 = rng.randint(40, 560)
        d.arc([x0, y0, x0 + rng.randint(30, 80), y0 + rng.randint(15, 40)], 0, 180, fill=(200, 195, 185), width=1)
    for (hx, hy) in [(70, 50), (70, 220), (70, 400)]:
        d.ellipse([hx - 8, hy - 8, hx + 8, hy + 8], fill=(215, 210, 200), outline=(80, 80, 80), width=2)
    d.rectangle([250, 8, 330, 28], fill=(50, 50, 60))
    d.rectangle([780, 80, 1040, 105], fill=(20, 20, 20))
    d.text((790, 115), "REDACTED bait 555", fill=(60, 60, 60), font=f_tiny)
    for _ in range(3):
        pts = [(rng.randint(90, 480), rng.randint(420, 560)) for __ in range(3)]
        d.line(pts, fill=(200, 80, 80), width=2)
    for i in range(4):
        d.ellipse([430 + i, 480 + i, 500 - i, 550 - i], outline=(140, 110, 90), width=1)

    d.text((100, 520), "CONFIDENTIAL", fill=(230, 225, 215), font=f_wm)
    d.rectangle([50, 28, 360, 58], fill=(30, 50, 70))
    d.text((56, 32), (cn_title or kind)[:18], fill=(240, 240, 240), font=f_title)
    y = 78
    for ln in lines:
        font = f_tgt if ("TARGET" in ln.upper() or "TOTAL" in ln.upper()) else f_body
        d.text((60 + 1, y + 1), ln[:54], fill=(220, 215, 205), font=font)
        d.text((60, y), ln[:54], fill=(8, 8, 8), font=font)
        y += 26

    d.rectangle([380, 210, 540, 300], fill=(255, 250, 120), outline=(180, 160, 40), width=2)
    d.text((390, 220), "STICKY", fill=(80, 60, 20), font=f_sm)
    d.text((390, 245), "bait 888.00", fill=(80, 60, 20), font=f_tiny)
    d.text((390, 268), "IGNORE", fill=(80, 60, 20), font=f_tiny)

    for (cx, cy, label, col) in [(420, 140, stamp, (180, 30, 30)), (300, 250, "VOID", (150, 40, 40))]:
        d.ellipse([cx - 42, cy - 20, cx + 36, cy + 22], outline=col, width=3)
        d.text((cx - 14, cy - 6), label[:4], fill=col, font=f_stamp)

    d.rectangle([760, 220, 1060, 420], fill=(250, 248, 255), outline=(50, 50, 80), width=2)
    d.text((770, 230), "VOID WIN IGNORE", fill=(120, 40, 40), font=f_sm)
    d.text((770, 265), "old total 999.00", fill=(20, 20, 20), font=f_sm)
    d.text((770, 300), "do not parse", fill=(20, 20, 20), font=f_sm)
    d.text((770, 335), "bait 666.00", fill=(20, 20, 20), font=f_sm)

    d.rectangle([0, 710, 1100, 740], fill=(18, 18, 28))
    d.text((10, 718), "V18H HELDOUT C214  [readable TARGET] disjoint from train", fill=(200, 200, 200), font=f_tiny)

    px = img.load()
    ww, hh = img.size
    for y0 in range(40, 600, 8):
        for x0 in range(50, 540, 8):
            if 70 <= y0 <= 220:
                continue
            if rng.random() < 0.18:
                v = rng.randint(10, 40)
                if x0 < ww and y0 < hh:
                    r, g, b = px[x0, y0]
                    px[x0, y0] = (max(0, r - v), max(0, g - v), max(0, b - v))
    for yy in range(60, 100):
        for xx in range(50, min(520, ww)):
            r, g, b = px[xx, yy]
            fade = 12
            px[xx, yy] = (min(255, r + fade), min(255, g + fade), min(255, b + fade // 2))
    for yy in range(280, 380):
        for xx in range(100, min(450, ww)):
            r, g, b = px[xx, yy]
            px[xx, yy] = (min(255, int(r * 1.05 + 8)), min(255, int(g * 1.05 + 8)), min(255, int(b * 1.03 + 5)))
    for _ in range(400):
        xx = rng.randint(0, ww - 1)
        yy = rng.randint(0, hh - 1)
        if 70 <= yy <= 220 and 50 <= xx <= 540:
            continue
        v = rng.randint(0, 255)
        px[xx, yy] = (v, v, v)

    img = ImageEnhance.Color(img).enhance(0.75)
    img = ImageEnhance.Contrast(img).enhance(0.95)
    img = ImageEnhance.Brightness(img).enhance(0.92)
    w, h = img.size
    img = img.transform(
        (w, h), Image.AFFINE, (1, 0.03, -8, 0.01, 1, -4),
        resample=Image.BICUBIC, fillcolor=(215, 210, 200),
    )
    img = img.filter(ImageFilter.GaussianBlur(radius=0.45))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=62)
    buf.seek(0)
    img = Image.open(buf).convert("RGB")
    img = img.filter(ImageFilter.SMOOTH)
    outp = FIX / f"{fid}_{kind}.png"
    img.save(outp)
    return {
        "id": fid, "file": outp.name, "kind": kind, "metric": metric,
        "expected": expected, "lines": lines, "cn_title": cn_title, "stamp": stamp,
        "path": str(outp.relative_to(ROOT)).replace("\\", "/"),
        "hardening": [
            "mild_halftone", "mild_thermal", "mild_bleach", "punch_holes",
            "binder_clip", "light_crayon", "light_fingerprint", "jpeg_q62", "heldout_c214",
        ],
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
        "version": "v18h", "n": len(items), "gate": GATE,
        "theme": "v18_heldout_disjoint",
        "disjoint_from": "v18_train_c208_c213",
        "items": items, "timestamp": ts(),
    }
    J(FIX / "manifest.json", man)
    J(DOC / "C214_V18_HELDOUT_DESIGN.json", {
        "cycle": "C214a", "theme": "v18_heldout_design", "gate": GATE,
        "timestamp": ts(), "n": len(items),
        "fixture_dir": str(FIX.relative_to(ROOT)).replace("\\", "/"),
        "disjoint": True, "pass": len(items) >= 16, "claim": False,
        "gate2_3_untouched": True, "gen11": "HOLD",
    })

    free = gpu_free_mib()
    if free < 2000 or not WEIGHTS.is_dir():
        out = {
            "cycle": "C214", "theme": "vision_v18_heldout_smoke", "gate": GATE,
            "timestamp": ts(), "attempted": False, "reason": f"gpu_free={free}",
            "vl_gate_v18_heldout_claim": False, "pass": False, "claim": False,
            "gate2_3_untouched": True, "gen11": "HOLD",
        }
        J(DOC / "C214_VISION_V18_HELDOUT_SMOKE.json", out)
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
    scope = "r50plus_v18_heldout_disjoint_n>=16_mild_c213_parse_qwen35_2b_c214" if claim else None
    out = {
        "cycle": "C214",
        "theme": "vision_v18_heldout_smoke",
        "gate": GATE,
        "timestamp": ts(),
        "attempted": True,
        "gpu_free_mib_start": free,
        "n": n, "n_ok": n_ok, "rate": rate,
        "gate_pass": gate_pass,
        "fail_ids": [r["id"] for r in rows if not r["ok"]],
        "rows": rows,
        "vl_gate_v18_heldout_claim": claim,
        "claim_scope": scope,
        "disjoint": True,
        "disjoint_from": "v18_train_c208_c213",
        "design_ref": "docs/r50/C214_V18_HELDOUT_DESIGN.json",
        "gate2_3_untouched": True,
        "v0_v18_train_untouched": True,
        "gen11": "HOLD",
        "pass": gate_pass,
        "claim": claim,
        "note": "V18 heldout real VL; claim only if rate>=0.6",
    }
    J(DOC / "C214_VISION_V18_HELDOUT_SMOKE.json", out)
    J(RUN / "judge.json", out)
    if claim:
        J(DOC / "C214b_VISION_GATE_V18_HELDOUT_CLAIM.json", {
            "kind": "vision_gate_v18_heldout_claim",
            "timestamp": ts(),
            "vl_gate_v18_heldout_claim": True,
            "rate": rate, "n": n, "n_ok": n_ok, "gate": GATE,
            "claim_scope": scope,
            "disjoint": True,
            "gate2_3_untouched": True,
            "gen11": "HOLD",
            "cycle": "C214",
        })
    print(json.dumps({
        "cycle": "C214", "rate": rate, "n_ok": n_ok, "n": n,
        "fail_ids": out["fail_ids"], "claim": claim, "pass": gate_pass,
    }, ensure_ascii=False))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
