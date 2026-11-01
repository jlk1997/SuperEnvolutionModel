# -*- coding: utf-8 -*-
"""C250: Vision V24 heldout — disjoint fixtures + real VL claim if rate>=0.6.
Different ids/amounts from V24 train (C248/C249). Same coffee/binder/tape/pen/
crumple/carbon/sticky/fax/grease/contrast family; clarity floor.
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
FIX = ROOT / "evo/office/fixtures/vision_images_v24h"
WEIGHTS = ROOT / "models/Qwen3.5-2B"
RUN = ROOT / "runs/vision_v24h_c250"
PROTO = ROOT / "docs" / "蚁算_VL_GATE_V24_HELDOUT_PROTOCOL.md"
TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v24"

JPEG_Q = 60
PHOTOCOPY_DIV = 2
BLUR_R = 0.45
TEXT_BAND = (70, 250)

# Disjoint from V24 train amounts (C248)
SPECS = [
    ("v24h_01", "coffee_recv", "paid_total", 67.5,
     ["COFFEE RING RECV V24H", "a paid 33.00", "b paid 34.50", "c open 9.00", "TOTAL PAID TARGET 67.50"],
     "咖啡渍收据H", "RECV"),
    ("v24h_02", "binder_wh", "qty_sum", 51.0,
     ["WH BINDER TEETH V24H", "SKU1 qty 24 ok", "SKU2 qty 11 hold", "SKU3 qty 27 ok", "qty_sum TARGET 51"],
     "活页夹仓单H", "RECV"),
    ("v24h_03", "tape_refund", "refund_done", 28.75,
     ["YELLOW TAPE REFUND V24H", "itemR1 13.00 done", "itemR2 15.75 done", "itemR3 6.00 open", "refund_done TARGET 28.75"],
     "黄胶带退款H", "DONE"),
    ("v24h_04", "pen_tax", "tax_base_paid", 96.0,
     ["TAX PEN SCRIBBLE V24H", "T1 54.00 paid", "T2 22.00 open", "T3 42.00 paid", "tax_base_paid TARGET 96.00"],
     "笔迹税基H", "RECV"),
    ("v24h_05", "crumple_pay", "payroll_active", 1680.0,
     ["PAYROLL CRUMPLE X V24H", "A 870 active", "B 170 leave", "C 810 active", "payroll_active TARGET 1680"],
     "皱折工资H", "OK"),
    ("v24h_06", "carbon_ship", "ship_ok_qty", 41.0,
     ["SHIP CARBON GHOST V24H", "P1 21 ok", "P2 11 hold", "P3 20 ok", "ship_ok_qty TARGET 41"],
     "复写发货H", "SHIP"),
    ("v24h_07", "sticky_sla", "open_pri_sum", 37.0,
     ["SLA STICKY STACK V24H", "S1 pri 16 open", "S2 pri 20 closed", "S3 pri 21 open", "open_pri_sum TARGET 37"],
     "便利贴SLAH", "OPEN"),
    ("v24h_08", "fax_exp", "paid_total", 68.25,
     ["EXPENSE FAX STREAK V24H", "E1 33.00 paid", "E2 14.00 void", "E3 35.25 paid", "paid_total TARGET 68.25"],
     "传真条纹报销H", "RECV"),
    ("v24h_09", "grease_po", "paid_total", 55.0,
     ["PO-GREASE BLOT V24H", "itemA paid 27.00", "itemB paid 28.00", "itemC open 10.00", "TOTAL PAID TARGET 55.00"],
     "油渍采购H", "RECV"),
    ("v24h_10", "gray_order", "paid_total", 45.5,
     ["ORDER GRAY FADE V24H", "A paid 22.00", "B paid 23.50", "C open 7.00", "TOTAL PAID TARGET 45.50"],
     "低对比订单H", "RECV"),
    ("v24h_11", "coffee_dup", "paid_total", 54.0,
     ["INVOICE #V24H-DUP", "line paid 18.00", "line paid 18.00", "line paid 18.00", "TOTAL PAID TARGET 54.00"],
     "咖啡渍重复H", "RECV"),
    ("v24h_12", "binder_zero", "paid_total", 0.0,
     ["OPEN ONLY V24H", "X 39.00 open", "Y 42.00 open", "paid_total TARGET 0.00"],
     "活页未付H", "HOLD"),
    ("v24h_13", "skew_ledger", "paid_total", 38.25,
     ["LEDGER SKEW MILD V24H", "rA paid 18.50", "rB paid 19.75", "rC open 5.00", "TOTAL PAID TARGET 38.25"],
     "轻斜台账H", "RECV"),
    ("v24h_14", "ghost_ui", "paid_total", 40.5,
     ["UI GHOST DOUBLE V24H", "alpha paid 19.50", "beta paid 21.00", "gamma open 8.00", "TOTAL PAID TARGET 40.50"],
     "重影窗口H", "RECV"),
    ("v24h_15", "crumple_stack", "paid_total", 64.0,
     ["HEAVY CRUMPLE STACK V24H", "x paid 32.00 usd", "y paid 32.00 usd", "z open 12.00 usd", "TOTAL PAID TARGET 64.00"],
     "皱折堆单H", "RECV"),
    ("v24h_16", "carbon_mix", "paid_total", 38.75,
     ["CN-EN CARBON MIX V24H", "tea paid 19.00", "rice paid 19.75", "soup open 6.00", "TOTAL PAID TARGET 38.75"],
     "中英复写H", "RECV"),
    ("v24h_17", "fax_win", "paid_total", 49.0,
     ["FAX WIN V24H", "w1 paid 24.00", "w2 paid 25.00", "w3 open 11.00", "TOTAL PAID TARGET 49.00"],
     "传真双窗H", "RECV"),
    ("v24h_18", "grease_foot", "paid_total", 27.5,
     ["GREASE FOOT V24H", "p1 paid 13.00", "p2 paid 14.50", "p3 open 4.50", "TOTAL PAID TARGET 27.50"],
     "油渍脚注H", "RECV"),
]


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


PROTOCOL = """# Ant VL Gate V24 Heldout Protocol

Updated: {ts} (Asia/Shanghai)

## Purpose
Disjoint heldout for V24 train (C249). Different ids/amounts.
Same coffee/binder/tape/pen/crumple/carbon/sticky/fax/grease/contrast family.
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
    rng = random.Random(hash(fid + "_v24hc250") & 0xFFFFFFFF)
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
    d.text((8, 1), "SCAN DESK V24H bait 222.00 PAGE 01", fill=(70, 70, 70), font=f_fax)

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
        f"V24H C250 clarity floor jpeg_q{JPEG_Q} photo/{PHOTOCOPY_DIV} heldout",
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
            "coffee_ring", "binder_teeth", "yellow_tape", "pen_scribble",
            "crumple_x", "carbon_ghost", "sticky_stack", "fax_streak",
            "grease_blot", "gray_fade", "skew_mild", "ghost_double",
            f"jpeg_q{JPEG_Q}", f"photocopy_div{PHOTOCOPY_DIV}", f"blur_{BLUR_R}",
            "text_band_protect", "c250_heldout_clarity_floor",
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
        "version": "v24h",
        "n": len(items),
        "gate": GATE,
        "theme": "coffee_binder_tape_pen_crumple_carbon_sticky_fax_grease_gray_skew_ghost_heldout",
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
            "cycle": "C250", "theme": "vision_v24_heldout", "gate": GATE,
            "timestamp": ts(), "attempted": False, "reason": f"gpu_free={free}",
            "n": len(items), "id_disjoint": disjoint, "amt_overlap": amt_overlap,
            "vl_gate_v24_heldout_claim": False, "pass": False, "claim": False,
            "gate2_3_untouched": True, "gen11": "HOLD",
        }
        J(DOC / "C250_VISION_V24_HELDOUT_SMOKE.json", out)
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
    scope = "r50plus_v24_heldout_coffee_binder_n>=16_qwen35_2b_clarity_floor" if claim else None
    out = {
        "cycle": "C250",
        "theme": "vision_v24_heldout",
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
        "vl_gate_v24_heldout_claim": claim,
        "claim_scope": scope,
        "clarity_floor": man["clarity_floor"],
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "pass": gate_pass,
        "claim": claim,
    }
    J(DOC / "C250_VISION_V24_HELDOUT_SMOKE.json", out)
    J(RUN / "judge.json", out)
    if claim:
        J(DOC / "C250b_VISION_GATE_V24_HELDOUT_CLAIM.json", {
            "kind": "vision_gate_v24_heldout_claim",
            "timestamp": ts(),
            "vl_gate_v24_heldout_claim": True,
            "rate": rate, "n": n, "n_ok": n_ok, "gate": GATE,
            "claim_scope": scope,
            "id_disjoint": disjoint,
            "gate2_3_untouched": True,
            "gen11": "HOLD",
            "cycle": "C250",
        })
    print(json.dumps({
        "cycle": "C250", "rate": rate, "n_ok": n_ok, "n": n,
        "fail_ids": out["fail_ids"], "disjoint": disjoint,
        "claim": claim, "pass": gate_pass,
    }, ensure_ascii=False))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
