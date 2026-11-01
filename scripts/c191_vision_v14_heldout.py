# -*- coding: utf-8 -*-
"""C191: Vision V14 heldout — disjoint fixtures + real VL claim if rate>=0.6.
Different ids/amounts from V14 train (C187/C188). Same salt/moire/ghost/tape/
redact/wet/mesh/oil/thermal family. Mild-readable TARGET.
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
FIX = ROOT / "evo/office/fixtures/vision_images_v14h"
WEIGHTS = ROOT / "models/Qwen3.5-2B"
RUN = ROOT / "runs/vision_v14h_c191"
PROTO = ROOT / "docs" / "蚁算_VL_GATE_V14_HELDOUT_PROTOCOL.md"

# Disjoint from V14 train amounts (C187/C188)
SPECS = [
    ("v14h_01", "salt_receipt", "paid_total", 42.25,
     ["SALT RECEIPT V14H", "a paid 20.00", "b paid 22.25", "c open 6.00", "TOTAL PAID TARGET 42.25"],
     "椒盐收据H", "RECV"),
    ("v14h_02", "moire_wh", "qty_sum", 41.0,
     ["WH MOIRE V14H", "SKU1 qty 21 ok", "SKU2 qty 9 hold", "SKU3 qty 20 ok", "qty_sum TARGET 41"],
     "莫尔仓单H", "RECV"),
    ("v14h_03", "ghost_refund", "refund_done", 22.5,
     ["GHOST REFUND V14H", "itemR1 10.25 done", "itemR2 12.25 done", "itemR3 4.00 open", "refund_done TARGET 22.50"],
     "重影退款H", "DONE"),
    ("v14h_04", "tape_tax", "tax_base_paid", 72.0,
     ["TAX TAPE V14H", "T1 40.00 paid", "T2 15.00 open", "T3 32.00 paid", "tax_base_paid TARGET 72.00"],
     "胶带税联H", "RECV"),
    ("v14h_05", "redact_payroll", "payroll_active", 1180.0,
     ["PAYROLL REDACT V14H", "A 640 active", "B 110 leave", "C 540 active", "payroll_active TARGET 1180"],
     "涂黑薪资H", "OK"),
    ("v14h_06", "wet_ship", "ship_ok_qty", 31.0,
     ["SHIP WET V14H", "P1 16 ok", "P2 9 hold", "P3 15 ok", "ship_ok_qty TARGET 31"],
     "水渍发货H", "SHIP"),
    ("v14h_07", "fade_sla", "open_pri_sum", 27.0,
     ["SLA FADE V14H", "S1 pri 12 open", "S2 pri 18 closed", "S3 pri 15 open", "open_pri_sum TARGET 27"],
     "淡墨SLAH", "OPEN"),
    ("v14h_08", "mesh_exp", "paid_total", 44.75,
     ["EXPENSE MESH V14H", "E1 23.50 paid", "E2 9.00 void", "E3 21.25 paid", "paid_total TARGET 44.75"],
     "网纹报销H", "RECV"),
    ("v14h_09", "oil_po", "paid_total", 38.25,
     ["PO-OIL V14H", "itemA paid 19.00", "itemB paid 19.25", "itemC open 7.00", "TOTAL PAID TARGET 38.25"],
     "指油采购H", "RECV"),
    ("v14h_10", "thermal_order", "paid_total", 27.5,
     ["ORDER THERMAL V14H", "A paid 14.00", "B paid 13.50", "C open 5.00", "TOTAL PAID TARGET 27.50"],
     "热敏订单H", "RECV"),
    ("v14h_11", "skew_dup", "paid_total", 42.0,
     ["INVOICE #V14H-DUP", "line paid 14.00", "line paid 14.00", "line paid 14.00", "TOTAL PAID TARGET 42.00"],
     "强斜重复H", "RECV"),
    ("v14h_12", "hail_zero", "paid_total", 0.0,
     ["OPEN ONLY V14H", "X 28.00 open", "Y 31.00 open", "paid_total TARGET 0.00"],
     "冰雹未付H", "HOLD"),
    ("v14h_13", "salt_ledger", "paid_total", 21.75,
     ["LEDGER SALT V14H", "rA paid 10.50", "rB paid 11.25", "rC open 3.50", "TOTAL PAID TARGET 21.75"],
     "椒盐账本H", "RECV"),
    ("v14h_14", "tape_ui", "paid_total", 35.5,
     ["UI TAPE V14H", "alpha paid 17.25", "beta paid 18.25", "gamma open 6.00", "TOTAL PAID TARGET 35.50"],
     "胶带界面H", "RECV"),
    ("v14h_15", "mesh_stack", "paid_total", 52.0,
     ["HEAVY MESH V14H", "x paid 26.00 usd", "y paid 26.00 usd", "z open 10.00 usd", "TOTAL PAID TARGET 52.00"],
     "网纹叠窗H", "RECV"),
    ("v14h_16", "ghost_mix", "paid_total", 25.25,
     ["CN-EN GHOST MIX V14H", "tea paid 11.00", "rice paid 14.25", "soup open 3.50", "TOTAL PAID TARGET 25.25"],
     "中英重影H", "RECV"),
    ("v14h_17", "wet_win", "paid_total", 43.0,
     ["WET WIN V14H", "w1 paid 21.00", "w2 paid 22.00", "w3 open 10.00", "TOTAL PAID TARGET 43.00"],
     "水渍双窗H", "RECV"),
    ("v14h_18", "oil_foot", "paid_total", 15.75,
     ["OIL FOOT V14H", "p1 paid 7.50", "p2 paid 8.25", "p3 open 2.50", "TOTAL PAID TARGET 15.75"],
     "指油脚注H", "RECV"),
]


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


PROTOCOL = """# 蚁算-视 VL Gate V14 Heldout Protocol

Updated: {ts} (Asia/Shanghai)

## Purpose
Disjoint heldout for V14 train (C187/C188). Different ids/amounts;
same salt/moire/ghost/tape/redact/wet/mesh/oil/thermal family; mild-readable TARGET.

## Gate
- rate >= **0.6**, n >= 16, real VL
- Claim only on PASS

## Honesty
- Gate2/3 untouched. V0-V13 untouched. gen11 HOLD.
"""


def make_fixture(fid, kind, lines, metric, expected, cn_title, stamp):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    FIX.mkdir(parents=True, exist_ok=True)
    rng = random.Random(hash(fid + "_v14h") & 0xFFFFFFFF)
    img = Image.new("RGB", (1060, 700), (205, 200, 190))
    d = ImageDraw.Draw(img)
    try:
        f_title = ImageFont.truetype(r"C:\\Windows\\Fonts\\msyh.ttc", 15)
        f_body = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 13)
        f_tgt = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 14)
        f_sm = ImageFont.truetype(r"C:\\Windows\\Fonts\\msyh.ttc", 11)
        f_stamp = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 14)
        f_tiny = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 10)
        f_wm = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 34)
    except Exception:
        f_title = f_body = f_tgt = f_sm = f_stamp = f_tiny = f_wm = ImageFont.load_default()

    d.rectangle([34, 16, 550, 590], fill=(244, 238, 228), outline=(30, 30, 30), width=2)
    for _ in range(12):
        x0 = rng.randint(40, 500)
        y0 = rng.randint(40, 540)
        d.arc([x0, y0, x0 + rng.randint(40, 120), y0 + rng.randint(20, 60)], 0, 180, fill=(195, 190, 180), width=1)
    d.rectangle([48, 100, 510, 122], fill=(255, 255, 110))
    d.rectangle([370, 210, 530, 295], fill=(255, 248, 110), outline=(170, 150, 30), width=2)
    d.text((380, 220), "STICKY", fill=(80, 60, 20), font=f_sm)
    d.text((380, 245), "bait 888.00", fill=(80, 60, 20), font=f_tiny)
    d.text((380, 268), "IGNORE", fill=(80, 60, 20), font=f_tiny)
    d.rectangle([60, 300, 200, 322], fill=(240, 220, 140))
    d.rectangle([420, 420, 540, 445], fill=(235, 210, 130))
    d.rectangle([560, 80, 720, 110], fill=(10, 10, 10))
    d.rectangle([560, 130, 700, 155], fill=(10, 10, 10))
    d.text((560, 165), "REDACT bait", fill=(80, 80, 80), font=f_tiny)

    wet = Image.new("RGBA", img.size, (0, 0, 0, 0))
    wd = ImageDraw.Draw(wet)
    wd.ellipse([70, 430, 240, 580], outline=(100, 60, 30, 100), width=12)
    wd.ellipse([95, 455, 215, 555], fill=(130, 75, 40, 45))
    wd.ellipse([300, 500, 420, 620], fill=(90, 110, 140, 35))
    img = Image.alpha_composite(img.convert("RGBA"), wet).convert("RGB")
    d = ImageDraw.Draw(img)

    for hy in (50, 180, 320, 460):
        d.ellipse([16, hy, 32, hy + 14], fill=(205, 200, 190), outline=(40, 40, 40), width=1)
    for fy in range(28, 580, 6):
        if rng.random() > 0.4:
            d.line([(36, fy), (548, fy)], fill=(190, 185, 180), width=1)
    for mx in range(40, 540, 5):
        d.line([(mx, 20), (mx + 8, 580)], fill=(200, 198, 192), width=1)
    for ty in range(40, 560, 18):
        d.rectangle([36, ty, 548, ty + 2], fill=(230, 225, 215))

    d.text((90, 340), "GHOST bait 666.00", fill=(228, 222, 214), font=f_sm)
    d.text((92, 342), "GHOST bait 666.00", fill=(215, 208, 200), font=f_sm)
    d.text((70, 380), "CONFIDENTIAL", fill=(218, 210, 200), font=f_wm)

    d.rectangle([44, 24, 340, 54], fill=(20, 40, 60))
    d.text((50, 28), (cn_title or kind)[:20], fill=(240, 240, 240), font=f_title)
    y = 68
    for ln in lines:
        font = f_tgt if ("TARGET" in ln.upper() or "TOTAL" in ln.upper()) else f_body
        d.text((52, y), ln[:54], fill=(6, 6, 6), font=font)
        y += 22

    for (cx, cy, label, col) in [(400, 130, stamp, (175, 25, 25)), (270, 260, "作废", (135, 45, 45)), (450, 330, "VOID", (145, 35, 35))]:
        d.ellipse([cx - 46, cy - 22, cx + 40, cy + 26], outline=col, width=3)
        d.text((cx - 14, cy - 6), label[:4], fill=col, font=f_stamp)

    d.rectangle([760, 210, 1040, 430], fill=(250, 248, 255), outline=(50, 50, 80), width=2)
    d.text((770, 220), "VOID WIN IGNORE", fill=(120, 40, 40), font=f_sm)
    d.text((770, 255), "old total 999.00", fill=(20, 20, 20), font=f_sm)
    d.text((770, 290), "do not parse", fill=(20, 20, 20), font=f_sm)

    d.rectangle([0, 670, 1060, 700], fill=(16, 16, 26))
    d.text((10, 678), "V14H HELDOUT C191  [readable TARGET]", fill=(200, 200, 200), font=f_tiny)

    px = img.load()
    ww, hh = img.size
    for _ in range(1800):
        xx = rng.randint(0, ww - 1)
        yy = rng.randint(0, hh - 1)
        v = 0 if rng.random() < 0.5 else 255
        px[xx, yy] = (v, v, v)
    for yy in range(130, 200):
        for xx in range(48, min(520, ww - 3)):
            r, g, b = px[xx, yy]
            px[xx, yy] = (r, g, min(255, b + 20))

    oil = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(oil)
    od.ellipse([480, 480, 580, 580], fill=(90, 70, 40, 50))
    for i in range(5):
        od.arc([485 + i, 485 + i, 575 - i, 575 - i], 0, 270, fill=(60, 40, 20, 40), width=1)
    img = Image.alpha_composite(img.convert("RGBA"), oil).convert("RGB")

    glare = Image.new("RGBA", img.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glare)
    gd.ellipse([150, 20, 380, 150], fill=(255, 255, 230, 50))
    img = Image.alpha_composite(img.convert("RGBA"), glare).convert("RGB")

    w, h = img.size
    img = img.transform(
        (w, h), Image.AFFINE, (1, 0.04, -14, 0.015, 1, -4),
        resample=Image.BICUBIC, fillcolor=(205, 200, 190),
    )
    img = ImageEnhance.Contrast(img).enhance(0.88)
    img = ImageEnhance.Brightness(img).enhance(0.92)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=48)
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
            "salt_pepper", "moire_scanlines", "double_ghost", "tape_strips",
            "redaction_bars", "wet_smear", "low_contrast_fade", "mesh_screen",
            "fingerprint_oil", "thermal_stripes", "stronger_skew", "hail_noise",
            "cyan_misreg", "jpeg_q48",
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
        "version": "v14_heldout", "n": len(items), "gate": GATE,
        "theme": "v14_heldout_disjoint", "harder_than": "v13_heldout",
        "items": items, "timestamp": ts(),
    }
    J(FIX / "manifest.json", man)

    free = gpu_free_mib()
    if free < 2000 or not WEIGHTS.is_dir():
        out = {
            "cycle": "C191", "theme": "vision_v14_heldout", "gate": GATE,
            "timestamp": ts(), "attempted": False, "reason": f"gpu_free={free}",
            "vl_gate_v14_heldout_claim": False, "pass": False, "claim": False,
            "gate2_3_untouched": True, "gen11": "HOLD",
        }
        J(DOC / "C191_VISION_V14_HELDOUT_SMOKE.json", out)
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
    scope = "r50plus_v14_heldout_disjoint_n>=16_c162_parse_qwen35_2b_c191" if claim else None
    out = {
        "cycle": "C191",
        "theme": "vision_v14_heldout",
        "gate": GATE,
        "timestamp": ts(),
        "attempted": True,
        "gpu_free_mib_start": free,
        "n": n, "n_ok": n_ok, "rate": rate,
        "gate_pass": gate_pass,
        "fail_ids": [r["id"] for r in rows if not r["ok"]],
        "rows": rows,
        "vl_gate_v14_heldout_claim": claim,
        "claim_scope": scope,
        "train_ref": "docs/r50/C188b_VISION_GATE_V14_CLAIM.json",
        "disjoint": True,
        "gate2_3_untouched": True,
        "v0_v13_untouched": True,
        "gen11": "HOLD",
        "pass": gate_pass,
        "claim": claim,
        "note": "V14 heldout real VL; claim only if rate>=0.6",
    }
    J(DOC / "C191_VISION_V14_HELDOUT_SMOKE.json", out)
    J(RUN / "judge.json", out)
    if claim:
        J(DOC / "C191b_VISION_GATE_V14_HELDOUT_CLAIM.json", {
            "kind": "vision_gate_v14_heldout_claim",
            "timestamp": ts(),
            "vl_gate_v14_heldout_claim": True,
            "rate": rate, "n": n, "n_ok": n_ok, "gate": GATE,
            "claim_scope": scope,
            "gate2_3_untouched": True,
            "v0_v13_untouched": True,
            "gen11": "HOLD",
            "cycle": "C191",
        })
    print(json.dumps({
        "cycle": "C191", "rate": rate, "n_ok": n_ok, "n": n,
        "fail_ids": out["fail_ids"], "claim": claim, "pass": gate_pass,
    }, ensure_ascii=False))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
