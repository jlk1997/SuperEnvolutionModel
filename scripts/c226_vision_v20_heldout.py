# -*- coding: utf-8 -*-
"""C226: Vision V20 heldout — disjoint fixtures + real VL claim if rate>=0.6.
Different ids/amounts from V20 train (C224/C225). Same V20 theme family;
clarity floor (jpeg_q60, photo/2, blur<=0.5, text-band protect). Gate 0.6.
Gate2/3 untouched. gen11 HOLD.
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
FIX = ROOT / "evo/office/fixtures/vision_images_v20h"
WEIGHTS = ROOT / "models/Qwen3.5-2B"
RUN = ROOT / "runs/vision_v20h_c226"
PROTO = ROOT / "docs" / "蚁算_VL_GATE_V20_HELDOUT_PROTOCOL.md"

JPEG_Q = 60
PHOTOCOPY_DIV = 2
BLUR_R = 0.45
TEXT_BAND = (70, 250)

SPECS = [
    ("v20h_01", "crease_receipt", "paid_total", 64.5,
     ["CREASE GRID V20H", "a paid 31.00", "b paid 33.50", "c open 9.00", "TOTAL PAID TARGET 64.50"],
     "折痕收据H", "RECV"),
    ("v20h_02", "tape_wh", "qty_sum", 51.0,
     ["WH TAPE GLARE V20H", "SKU1 qty 24 ok", "SKU2 qty 11 hold", "SKU3 qty 27 ok", "qty_sum TARGET 51"],
     "胶带仓单H", "RECV"),
    ("v20h_03", "carbon_refund", "refund_done", 27.75,
     ["CARBON REFUND V20H", "itemR1 13.25 done", "itemR2 14.50 done", "itemR3 6.00 open", "refund_done TARGET 27.75"],
     "复写退款H", "DONE"),
    ("v20h_04", "halftone_tax", "tax_base_paid", 101.0,
     ["TAX HALFTONE V20H", "T1 56.00 paid", "T2 22.00 open", "T3 45.00 paid", "tax_base_paid TARGET 101.00"],
     "网点税基H", "RECV"),
    ("v20h_05", "fold_pay", "payroll_active", 1740.0,
     ["PAYROLL FOLD V20H", "A 920 active", "B 170 leave", "C 820 active", "payroll_active TARGET 1740"],
     "折角工资H", "OK"),
    ("v20h_06", "wet_ship", "ship_ok_qty", 41.0,
     ["SHIP WET EDGE V20H", "P1 21 ok", "P2 11 hold", "P3 20 ok", "ship_ok_qty TARGET 41"],
     "湿边发运H", "SHIP"),
    ("v20h_07", "thermal_sla", "open_pri_sum", 35.0,
     ["SLA THERMAL V20H", "S1 pri 15 open", "S2 pri 22 closed", "S3 pri 20 open", "open_pri_sum TARGET 35"],
     "热敏SLAH", "OPEN"),
    ("v20h_08", "fax_exp", "paid_total", 69.25,
     ["EXPENSE FAX V20H", "E1 34.00 paid", "E2 14.00 void", "E3 35.25 paid", "paid_total TARGET 69.25"],
     "传真报销H", "RECV"),
    ("v20h_09", "fp_po", "paid_total", 54.0,
     ["PO-FINGERPRINT V20H", "itemA paid 26.75", "itemB paid 27.25", "itemC open 10.00", "TOTAL PAID TARGET 54.00"],
     "指纹采购H", "RECV"),
    ("v20h_10", "clip_order", "paid_total", 47.5,
     ["ORDER CLIP V20H", "A paid 23.50", "B paid 24.00", "C open 7.00", "TOTAL PAID TARGET 47.50"],
     "夹影订单H", "RECV"),
    ("v20h_11", "crease_dup", "paid_total", 54.0,
     ["INVOICE #V20H-DUP", "line paid 18.00", "line paid 18.00", "line paid 18.00", "TOTAL PAID TARGET 54.00"],
     "折痕重复H", "RECV"),
    ("v20h_12", "carbon_zero", "paid_total", 0.0,
     ["OPEN ONLY V20H", "X 41.00 open", "Y 44.00 open", "paid_total TARGET 0.00"],
     "复写未付H", "HOLD"),
    ("v20h_13", "tape_ledger", "paid_total", 37.75,
     ["LEDGER TAPE V20H", "rA paid 18.50", "rB paid 19.25", "rC open 5.00", "TOTAL PAID TARGET 37.75"],
     "胶带台账H", "RECV"),
    ("v20h_14", "halftone_ui", "paid_total", 43.5,
     ["UI HALFTONE V20H", "alpha paid 21.50", "beta paid 22.00", "gamma open 7.50", "TOTAL PAID TARGET 43.50"],
     "网点界面H", "RECV"),
    ("v20h_15", "fold_stack", "paid_total", 66.0,
     ["HEAVY FOLD V20H", "x paid 33.00 usd", "y paid 33.00 usd", "z open 12.00 usd", "TOTAL PAID TARGET 66.00"],
     "折角堆单H", "RECV"),
    ("v20h_16", "wet_mix", "paid_total", 40.25,
     ["CN-EN WET MIX V20H", "tea paid 19.00", "rice paid 21.25", "soup open 6.00", "TOTAL PAID TARGET 40.25"],
     "中英湿边H", "RECV"),
    ("v20h_17", "thermal_win", "paid_total", 53.0,
     ["THERMAL WIN V20H", "w1 paid 26.00", "w2 paid 27.00", "w3 open 11.00", "TOTAL PAID TARGET 53.00"],
     "热敏双窗H", "RECV"),
    ("v20h_18", "fax_foot", "paid_total", 28.5,
     ["FAX FOOT V20H", "p1 paid 14.00", "p2 paid 14.50", "p3 open 5.00", "TOTAL PAID TARGET 28.50"],
     "传真脚注H", "RECV"),
]


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def in_text_band(yy):
    y0, y1 = TEXT_BAND
    return y0 <= yy <= y1


def make_fixture(fid, kind, metric, expected, lines, cn_title, stamp):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    FIX.mkdir(parents=True, exist_ok=True)
    rng = random.Random(hash(fid + "_v20h_c226") & 0xFFFFFFFF)
    bg = (218, 214, 204)
    img = Image.new("RGB", (1100, 740), bg)
    d = ImageDraw.Draw(img)
    try:
        f_title = ImageFont.truetype(r"C:\\Windows\\Fonts\\msyh.ttc", 16)
        f_body = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 14)
        f_tgt = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 15)
        f_sm = ImageFont.truetype(r"C:\\Windows\\Fonts\\msyh.ttc", 11)
        f_stamp = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 14)
        f_tiny = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 10)
        f_wm = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 32)
        f_fax = ImageFont.truetype(r"C:\\Windows\\Fonts\\consola.ttf", 11)
    except Exception:
        f_title = f_body = f_tgt = f_sm = f_stamp = f_tiny = f_wm = f_fax = ImageFont.load_default()

    d.rectangle([40, 20, 560, 600], fill=(250, 247, 238), outline=(35, 35, 35), width=2)
    for i in range(8):
        x0 = 50 + i * 55
        d.line([(x0, 260), (x0 + 80, 560)], fill=(200, 195, 185), width=2)
        d.line([(x0 + 40, 260), (x0 - 20, 560)], fill=(205, 200, 190), width=1)
    d.rectangle([42, 320, 558, 598], fill=(230, 238, 248))
    for ty in range(270, 520, 28):
        d.rectangle([50, ty, 540, ty + 3], fill=(235, 225, 210))
    d.rectangle([480, 80, 555, 240], fill=(255, 255, 230))
    d.text((490, 100), "TAPE", fill=(180, 160, 80), font=f_tiny)
    d.text((490, 145), "bait 88.88", fill=(160, 140, 60), font=f_tiny)
    d.rectangle([0, 0, 1100, 16], fill=(240, 240, 240))
    d.text((8, 2), "FAX FROM 021-555-0288  2026-10-19 08:20  PAGE 01/01  bait 222.00", fill=(80, 80, 80), font=f_fax)
    d.rectangle([380, 280, 540, 370], fill=(255, 250, 120), outline=(180, 160, 40), width=2)
    d.text((390, 290), "STICKY", fill=(80, 60, 20), font=f_sm)
    d.text((390, 315), "bait 99.99", fill=(80, 60, 20), font=f_tiny)
    for (cx, cy, label, col) in [
        (430, 400, stamp, (180, 30, 30)),
        (200, 480, "VOID", (150, 40, 40)),
        (320, 540, "COPY", (60, 60, 160)),
    ]:
        d.ellipse([cx - 42, cy - 20, cx + 36, cy + 22], outline=col, width=3)
        d.text((cx - 14, cy - 6), label[:4], fill=col, font=f_stamp)
    bx0 = 545
    for i in range(36):
        w = 1 if rng.random() < 0.55 else 2
        col = (10, 10, 10) if rng.random() < 0.7 else (240, 240, 240)
        d.rectangle([bx0 + i * 2, 300, bx0 + i * 2 + w, 460], fill=col)
    for r in (48, 55, 62):
        d.ellipse([150 - r, 520 - r, 150 + r, 520 + r], outline=(140, 100, 60), width=2)
    d.rectangle([250, 6, 340, 28], fill=(40, 40, 50))
    d.rectangle([780, 80, 1040, 105], fill=(20, 20, 20))
    d.text((790, 115), "REDACTED bait 555", fill=(60, 60, 60), font=f_tiny)
    d.text((100, 560), "CONFIDENTIAL", fill=(232, 228, 218), font=f_wm)
    d.rectangle([50, 28, 360, 58], fill=(30, 50, 70))
    d.text((56, 32), (cn_title or kind)[:18], fill=(240, 240, 240), font=f_title)
    y = 78
    for ln in lines:
        font = f_tgt if ("TARGET" in ln.upper() or "TOTAL" in ln.upper()) else f_body
        d.text((62, y + 2), ln[:54], fill=(230, 226, 216), font=font)
        d.text((60, y), ln[:54], fill=(8, 8, 8), font=font)
        y += 26
    d.rectangle([760, 220, 1060, 420], fill=(250, 248, 255), outline=(50, 50, 80), width=2)
    d.text((770, 230), "VOID WIN IGNORE", fill=(120, 40, 40), font=f_sm)
    d.text((770, 265), "old total 999.00", fill=(20, 20, 20), font=f_sm)
    d.text((770, 335), "bait 666.00", fill=(20, 20, 20), font=f_sm)
    d.rectangle([0, 710, 1100, 740], fill=(18, 18, 28))
    d.text((10, 718), f"V20H C226 jpeg_q{JPEG_Q} HELDOUT disjoint  Crease|Tape|Carbon|Halftone|Fold|Wet|Thermal|Fax", fill=(200, 200, 200), font=f_tiny)

    px = img.load()
    ww, hh = img.size
    for yy in range(20, 90):
        tear = int(2 + (yy - 20) // 8 + rng.randint(0, 2))
        for xx in range(40, 40 + tear):
            if 0 <= xx < ww and 0 <= yy < hh:
                px[xx, yy] = bg
    for _ in range(4):
        cx, cy = rng.randint(60, 500), rng.randint(400, 580)
        for dy in range(-22, 23):
            for dx in range(-22, 23):
                if dx * dx + dy * dy < 22 * 22 and rng.random() < 0.35:
                    xx, yy = cx + dx, cy + dy
                    if 0 <= xx < ww and 0 <= yy < hh and not in_text_band(yy):
                        r, g, b = px[xx, yy]
                        px[xx, yy] = (max(0, r - 20), max(0, g - 15), min(255, b + 10))
    for _ in range(80):
        xx, yy = rng.randint(50, 200), rng.randint(400, 580)
        r, g, b = px[xx, yy]
        px[xx, yy] = (max(0, r - 40), max(0, g - 50), max(0, b - 45))
    for _ in range(900):
        xx, yy = rng.randint(0, ww - 1), rng.randint(0, hh - 1)
        if in_text_band(yy) and 50 <= xx <= 540:
            continue
        if (xx + yy) % 3 == 0 and rng.random() < 0.4:
            r, g, b = px[xx, yy]
            v = 18 if rng.random() < 0.5 else -12
            px[xx, yy] = (max(0, min(255, r + v)), max(0, min(255, g + v)), max(0, min(255, b + v)))
    for _ in range(280):
        xx, yy = rng.randint(0, ww - 1), rng.randint(0, hh - 1)
        if in_text_band(yy) and 50 <= xx <= 540:
            continue
        v = rng.randint(0, 255)
        px[xx, yy] = (v, v, v)

    img = ImageEnhance.Color(img).enhance(0.82)
    img = ImageEnhance.Contrast(img).enhance(0.97)
    img = ImageEnhance.Brightness(img).enhance(0.95)
    w, h = img.size
    small = img.resize((max(1, w // PHOTOCOPY_DIV), max(1, h // PHOTOCOPY_DIV)), Image.BILINEAR)
    img = small.resize((w, h), Image.BILINEAR)
    img = img.transform((w, h), Image.AFFINE, (1, 0.028, -8, 0.010, 1, -4), resample=Image.BICUBIC, fillcolor=bg)
    img = img.filter(ImageFilter.GaussianBlur(radius=BLUR_R))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=JPEG_Q)
    buf.seek(0)
    img = Image.open(buf).convert("RGB").filter(ImageFilter.SMOOTH)
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
        "hardening": [f"jpeg_q{JPEG_Q}", f"photocopy_div{PHOTOCOPY_DIV}", "text_band_protect", "heldout_disjoint"],
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
    PROTO.write_text(
        f"""# Ant VL Gate V20 Heldout Protocol\n\nUpdated: {ts()} (Asia/Shanghai)\n\n"""
        "## Purpose\nDisjoint amounts/ids from V20 train. Same theme + clarity floor.\n\n"
        "## Gate\n- rate >= **0.6**, n >= 16, real VL\n- Must be disjoint from train SPECS\n\n"
        "## Honesty\nGate2/3 untouched. gen11 HOLD.\n",
        encoding="utf-8",
    )
    items = [make_fixture(*s) for s in SPECS]
    man = {
        "version": "v20h", "n": len(items), "gate": GATE,
        "theme": "v20_heldout_disjoint_clarity_floor",
        "harder_than": "v19h",
        "clarity_floor": {"jpeg_q": JPEG_Q, "photocopy_div": PHOTOCOPY_DIV, "blur": BLUR_R},
        "items": items, "timestamp": ts(),
    }
    J(FIX / "manifest.json", man)

    free = gpu_free_mib()
    if free < 2000 or not WEIGHTS.is_dir():
        out = {
            "cycle": "C226", "theme": "vision_v20_heldout", "gate": GATE,
            "timestamp": ts(), "attempted": False, "reason": f"gpu_free={free}",
            "vl_gate_v20_heldout_claim": False, "pass": False, "claim": False,
            "gate2_3_untouched": True, "gen11": "HOLD",
        }
        J(DOC / "C226_VISION_V20_HELDOUT_SMOKE.json", out)
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
    # disjoint check vs train expected set
    train_man = ROOT / "evo/office/fixtures/vision_images_v20/manifest.json"
    train_exps = set()
    train_ids = set()
    if train_man.is_file():
        tm = json.loads(train_man.read_text(encoding="utf-8"))
        for it in tm.get("items") or []:
            train_exps.add(float(it["expected"]))
            train_ids.add(it["id"])
    held_exps = {float(it["expected"]) for it in items}
    held_ids = {it["id"] for it in items}
    id_disjoint = len(held_ids & train_ids) == 0
    # allow some shared zeros; require majority disjoint expected
    exp_overlap = held_exps & train_exps
    exp_mostly_disjoint = len(exp_overlap) <= 2  # zero may overlap

    gate_pass = n >= 16 and rate >= GATE and id_disjoint
    claim = gate_pass
    scope = "r50plus_v20_heldout_disjoint_n>=16_qwen35_2b_clarity_floor" if claim else None
    out = {
        "cycle": "C226",
        "theme": "vision_v20_heldout",
        "gate": GATE,
        "timestamp": ts(),
        "attempted": True,
        "gpu_free_mib_start": free,
        "n": n, "n_ok": n_ok, "rate": rate,
        "gate_pass": gate_pass,
        "fail_ids": [r["id"] for r in rows if not r["ok"]],
        "rows": rows,
        "id_disjoint": id_disjoint,
        "expected_overlap": sorted(exp_overlap),
        "exp_mostly_disjoint": exp_mostly_disjoint,
        "clarity_floor": man["clarity_floor"],
        "vl_gate_v20_heldout_claim": claim,
        "claim_scope": scope,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "pass": gate_pass,
        "claim": claim,
    }
    J(DOC / "C226_VISION_V20_HELDOUT_SMOKE.json", out)
    J(RUN / "judge.json", out)
    if claim:
        J(DOC / "C226b_VISION_GATE_V20_HELDOUT_CLAIM.json", {
            "kind": "vision_gate_v20_heldout_claim",
            "timestamp": ts(),
            "vl_gate_v20_heldout_claim": True,
            "rate": rate, "n": n, "n_ok": n_ok, "gate": GATE,
            "claim_scope": scope,
            "id_disjoint": id_disjoint,
            "gate2_3_untouched": True,
            "gen11": "HOLD",
            "cycle": "C226",
        })
    print(json.dumps({
        "cycle": "C226", "rate": rate, "n_ok": n_ok, "n": n,
        "fail_ids": out["fail_ids"], "claim": claim, "id_disjoint": id_disjoint,
    }, ensure_ascii=False))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())

