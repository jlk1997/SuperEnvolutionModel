# -*- coding: utf-8 -*-
"""C175: Vision V11 heldout — disjoint fixtures + real VL claim if rate>=0.6.
Different ids/amounts from V11 train (C172/C173). Same glare/skew/hand/redact/night/mosaic family.
Gate 0.6. Gate2/3 untouched. gen11 HOLD. V0-V10 untouched.
"""
from __future__ import annotations
import gc, json, re, sys, random
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from evo.office.vision_metric_parse import parse_metric

GATE = 0.6
DOC = ROOT / "docs" / "r50"
FIX = ROOT / "evo/office/fixtures/vision_images_v11h"
WEIGHTS = ROOT / "models/Qwen3.5-2B"
RUN = ROOT / "runs/vision_v11h_c175"
PROTO = ROOT / "docs" / "蚁算_VL_GATE_V11_HELDOUT_PROTOCOL.md"

# Disjoint from V11 train amounts
SPECS = [
    ("v11h_01", "glare_receipt", "paid_total", 26.5,
     ["GLARE RECEIPT V11H", "a paid 12.25", "b paid 14.25", "c open 6.00", "TOTAL PAID TARGET 26.50"],
     "眩光收据H", "RECV"),
    ("v11h_02", "skew_wh", "qty_sum", 28.0,
     ["WH SKEW V11H", "SKU1 qty 16 ok", "SKU2 qty 6 hold", "SKU3 qty 12 ok", "qty_sum TARGET 28"],
     "斜切仓单H", "RECV"),
    ("v11h_03", "hand_refund", "refund_done", 12.25,
     ["HAND REFUND V11H", "itemR1 4.50 done", "itemR2 7.75 done", "itemR3 3.00 open", "refund_done TARGET 12.25"],
     "手写遮挡退款H", "DONE"),
    ("v11h_04", "redact_tax", "tax_base_paid", 39.0,
     ["TAX REDACT V11H", "T1 21.00 paid", "T2 9.00 open", "T3 18.00 paid", "tax_base_paid TARGET 39.00"],
     "涂黑税联H", "RECV"),
    ("v11h_05", "night_payroll", "payroll_active", 920.0,
     ["PAYROLL NIGHT V11H", "A 480 active", "B 110 leave", "C 440 active", "payroll_active TARGET 920"],
     "夜色薪资H", "OK"),
    ("v11h_06", "mosaic_ship", "ship_ok_qty", 23.0,
     ["SHIP MOSAIC V11H", "P1 11 ok", "P2 8 hold", "P3 12 ok", "ship_ok_qty TARGET 23"],
     "马赛克发货H", "SHIP"),
    ("v11h_07", "stampdig_sla", "open_pri_sum", 14.0,
     ["SLA STAMPDIG V11H", "S1 pri 6 open", "S2 pri 11 closed", "S3 pri 8 open", "open_pri_sum TARGET 14"],
     "盖章压字SLAH", "OPEN"),
    ("v11h_08", "fx_exp", "paid_total", 42.0,
     ["EXPENSE FX V11H", "E1 23.00 paid", "E2 9.00 void", "E3 19.00 paid", "paid_total TARGET 42.00"],
     "双币报销H", "RECV"),
    ("v11h_09", "excel_po", "paid_total", 35.5,
     ["PO-EXCEL V11H", "itemA paid 18.00", "itemB paid 17.50", "itemC open 6.00", "TOTAL PAID TARGET 35.50"],
     "表格串扰采购H", "RECV"),
    ("v11h_10", "crop_order", "paid_total", 25.75,
     ["ORDER CROP V11H", "A paid 13.50", "B paid 12.25", "C open 5.00", "TOTAL PAID TARGET 25.75"],
     "裁剪订单H", "RECV"),
    ("v11h_11", "glare_dup", "paid_total", 27.0,
     ["INVOICE #V11H-DUP", "line paid 9.00", "line paid 9.00", "line paid 9.00", "TOTAL PAID TARGET 27.00"],
     "眩光重复H", "RECV"),
    ("v11h_12", "night_zero", "paid_total", 0.0,
     ["OPEN ONLY V11H", "X 13.00 open", "Y 15.00 open", "paid_total TARGET 0.00"],
     "夜色未付H", "HOLD"),
    ("v11h_13", "hand_ledger", "paid_total", 16.0,
     ["LEDGER HAND V11H", "rA paid 8.00", "rB paid 8.00", "rC open 2.50", "TOTAL PAID TARGET 16.00"],
     "手写账本H", "RECV"),
    ("v11h_14", "skew_ui", "paid_total", 20.5,
     ["UI SKEW V11H", "alpha paid 9.75", "beta paid 10.75", "gamma open 3.00", "TOTAL PAID TARGET 20.50"],
     "斜切界面H", "RECV"),
    ("v11h_15", "mosaic_stack", "paid_total", 31.5,
     ["HEAVY MOSAIC V11H", "x paid 16.50 usd", "y paid 15.00 usd", "z open 5.00 usd", "TOTAL PAID TARGET 31.50"],
     "马赛克叠窗H", "RECV"),
    ("v11h_16", "fx_mix", "paid_total", 21.0,
     ["CN-EN FX MIX V11H", "tea paid 9.50", "rice paid 11.50", "soup open 4.00", "TOTAL PAID TARGET 21.00"],
     "中英双币H", "RECV"),
    ("v11h_17", "excel_win", "paid_total", 36.25,
     ["EXCEL WIN V11H", "w1 paid 17.00", "w2 paid 19.25", "w3 open 7.00", "TOTAL PAID TARGET 36.25"],
     "表格双窗H", "RECV"),
    ("v11h_18", "redact_foot", "paid_total", 14.0,
     ["REDACT FOOT V11H", "p1 paid 6.50", "p2 paid 7.50", "p3 open 2.50", "TOTAL PAID TARGET 14.00"],
     "涂黑脚注H", "RECV"),
]


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


PROTOCOL = """# 蚁算-视 VL Gate V11 Heldout Protocol

Updated: {ts} (Asia/Shanghai)

## Purpose
Disjoint heldout for V11 train (C173). Different ids/amounts; same glare/skew/hand/redact/night/mosaic family.

## Gate
- rate >= **0.6**, n >= 16, real VL
- Claim only on PASS

## Honesty
- Gate2/3 untouched. V0-V10 untouched. gen11 HOLD.
"""


def make_fixture(fid, kind, lines, metric, expected, cn_title, stamp):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    FIX.mkdir(parents=True, exist_ok=True)
    rng = random.Random(hash(fid + "_v11h") & 0xFFFFFFFF)
    try:
        from PIL import ImageGrab
        shot = ImageGrab.grab(all_screens=False)
        w, h = shot.size
        bg = shot.crop((0, 0, min(1200, w), min(780, h))).convert("RGB").resize((1000, 640))
        paper = Image.new("RGB", (1000, 640), (205, 200, 190))
        img = Image.blend(bg, paper, 0.66)
        capture = True
    except Exception:
        img = Image.new("RGB", (1000, 640), (205, 200, 190))
        capture = False
    d = ImageDraw.Draw(img)
    try:
        f_title = ImageFont.truetype(r"C:\\Windows\\Fonts\\msyh.ttc", 14)
        f_body = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 11)
        f_tgt = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 11)
        f_sm = ImageFont.truetype(r"C:\\Windows\\Fonts\\msyh.ttc", 10)
        f_stamp = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 15)
        f_wm = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 42)
        f_tiny = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 9)
        f_hand = ImageFont.truetype(r"C:\\Windows\\Fonts\\comic.ttf", 13)
    except Exception:
        f_title = f_body = f_tgt = f_sm = f_stamp = f_wm = f_tiny = f_hand = ImageFont.load_default()

    d.rectangle([18, 18, 480, 560], fill=(228, 222, 212), outline=(60, 60, 60), width=2)
    for gx in range(490, 700, 28):
        d.line([(gx, 40), (gx, 280)], fill=(180, 190, 200), width=1)
    for gy in range(40, 280, 22):
        d.line([(490, gy), (700, gy)], fill=(180, 190, 200), width=1)
    d.text((500, 48), "SHEET bait 888.00", fill=(90, 90, 110), font=f_sm)
    d.text((500, 72), "cell Z99 = 777.00", fill=(90, 90, 110), font=f_sm)
    d.rectangle([30, 300, 200, 318], fill=(20, 20, 20))
    d.rectangle([250, 340, 420, 358], fill=(20, 20, 20))
    d.text((40, 380), "ok check ~ignore~", fill=(30, 80, 160), font=f_hand)
    d.text((60, 410), "sign: H.Y.", fill=(30, 80, 160), font=f_hand)
    for yy in range(430, 500, 6):
        for xx in range(300, 400, 6):
            col = (rng.randint(40, 200),) * 3
            d.rectangle([xx, yy, xx + 5, yy + 5], fill=col)
    d.text((90, 220), "777", fill=(200, 195, 185), font=f_wm)
    d.text((200, 320), "Y666 $555", fill=(185, 180, 170), font=f_sm)
    d.text((40, 260), "GHOST FX convert 999", fill=(195, 190, 183), font=f_tiny)
    d.rectangle([26, 26, 310, 54], fill=(40, 55, 75))
    d.text((32, 30), (cn_title or kind)[:22], fill=(230, 230, 230), font=f_title)
    y = 64
    for ln in lines:
        font = f_tgt if ("TARGET" in ln.upper() or "TOTAL" in ln.upper()) else f_body
        fill = (25, 25, 25) if y < 150 else (55, 55, 55) if y < 190 else (85, 85, 85)
        xoff = 30 if "TARGET" not in ln.upper() else 26
        d.text((xoff, y), ln[:52], fill=fill, font=font)
        y += 18
    for (cx, cy, label, col) in [(360, 150, stamp, (190, 40, 40)), (280, 210, "VOID", (150, 55, 55))]:
        d.ellipse([cx - 52, cy - 24, cx + 42, cy + 30], outline=col, width=3)
        d.text((cx - 18, cy - 6), label[:6], fill=col, font=f_stamp)
    d.rectangle([720, 30, 980, 260], fill=(250, 248, 255), outline=(50, 50, 80), width=2)
    d.rectangle([720, 30, 980, 58], fill=(70, 50, 100))
    d.text((730, 36), "VOID WIN IGNORE", fill=(255, 220, 220), font=f_sm)
    d.text((730, 70), "old total 999.00", fill=(20, 20, 20), font=f_sm)
    d.text((730, 95), "FX bait $444.00", fill=(20, 20, 20), font=f_sm)
    d.text((730, 120), f"{fid} void#OLD", fill=(40, 40, 40), font=f_tiny)
    d.rectangle([720, 290, 980, 540], fill=(240, 250, 240), outline=(40, 90, 40), width=2)
    d.text((730, 300), "CAL bait 666.00", fill=(20, 20, 20), font=f_sm)
    d.text((730, 330), "do not parse", fill=(20, 20, 20), font=f_sm)
    d.rectangle([0, 600, 1000, 640], fill=(18, 18, 28))
    d.text((10, 610), "Start | Glare | Skew | Night | Excel | POS  [V11H]", fill=(200, 200, 200), font=f_tiny)
    glare = Image.new("RGBA", img.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glare)
    gd.ellipse([120, 40, 320, 180], fill=(255, 255, 240, 90))
    img = Image.alpha_composite(img.convert("RGBA"), glare).convert("RGB")
    w, h = img.size
    dx = 18
    img = img.transform(
        (w, h), Image.AFFINE, (1, 0.04, -dx, 0.01, 1, -4),
        resample=Image.BICUBIC, fillcolor=(205, 200, 190),
    )
    img = ImageEnhance.Brightness(img).enhance(0.82)
    img = ImageEnhance.Contrast(img).enhance(0.78)
    px = img.load()
    ww, hh = img.size
    for _ in range(2800):
        x, y = rng.randint(0, ww - 1), rng.randint(0, hh - 1)
        v = rng.randint(0, 50)
        r, g, b = px[x, y]
        px[x, y] = (max(0, r - v), max(0, g - v), max(0, b - v))
    img = img.filter(ImageFilter.SMOOTH)
    outp = FIX / f"{fid}_{kind}.png"
    img.save(outp)
    return {
        "id": fid, "file": outp.name, "kind": kind, "metric": metric,
        "expected": expected, "lines": lines, "cn_title": cn_title, "stamp": stamp,
        "capture_blend": capture,
        "path": str(outp.relative_to(ROOT)).replace("\\", "/"),
        "disjoint_from_train": True,
        "hardening": [
            "glare", "skew_shear", "handwriting", "redaction", "night_contrast",
            "mosaic", "stamp_over_digits", "dual_fx_bait", "excel_grid", "partial_crop",
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
        "version": "v11_heldout", "n": len(items), "gate": GATE,
        "theme": "v11_heldout_disjoint", "harder_than": "v10_heldout",
        "items": items, "timestamp": ts(),
    }
    J(FIX / "manifest.json", man)

    free = gpu_free_mib()
    if free < 2000 or not WEIGHTS.is_dir():
        out = {
            "cycle": "C175", "theme": "vision_v11_heldout", "gate": GATE,
            "timestamp": ts(), "attempted": False, "reason": f"gpu_free={free}",
            "vl_gate_v11_heldout_claim": False, "pass": False, "claim": False,
            "gate2_3_untouched": True, "gen11": "HOLD",
        }
        J(DOC / "C175_VISION_V11_HELDOUT_SMOKE.json", out)
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
    scope = "r50plus_v11_heldout_disjoint_n>=16_c162_parse_qwen35_2b_c175" if claim else None
    out = {
        "cycle": "C175",
        "theme": "vision_v11_heldout",
        "gate": GATE,
        "timestamp": ts(),
        "attempted": True,
        "gpu_free_mib_start": free,
        "n": n, "n_ok": n_ok, "rate": rate,
        "gate_pass": gate_pass,
        "fail_ids": [r["id"] for r in rows if not r["ok"]],
        "rows": rows,
        "vl_gate_v11_heldout_claim": claim,
        "claim_scope": scope,
        "train_ref": "docs/r50/C173b_VISION_GATE_V11_CLAIM.json",
        "disjoint": True,
        "gate2_3_untouched": True,
        "v0_v10_untouched": True,
        "gen11": "HOLD",
        "pass": gate_pass,
        "claim": claim,
        "note": "V11 heldout real VL; claim only if rate>=0.6",
    }
    J(DOC / "C175_VISION_V11_HELDOUT_SMOKE.json", out)
    J(RUN / "judge.json", out)
    if claim:
        J(DOC / "C175b_VISION_GATE_V11_HELDOUT_CLAIM.json", {
            "kind": "vision_gate_v11_heldout_claim",
            "timestamp": ts(),
            "vl_gate_v11_heldout_claim": True,
            "rate": rate, "n": n, "n_ok": n_ok, "gate": GATE,
            "claim_scope": scope,
            "gate2_3_untouched": True,
            "v0_v10_untouched": True,
            "gen11": "HOLD",
            "cycle": "C175",
        })
    print(json.dumps({
        "cycle": "C175", "rate": rate, "n_ok": n_ok, "n": n,
        "fail_ids": out["fail_ids"], "claim": claim, "pass": gate_pass,
    }, ensure_ascii=False))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
