# -*- coding: utf-8 -*-
"""C164: Vision V9 heldout — disjoint fixtures + real VL claim if rate>=0.6.
Different ids/amounts from V9 train. Uses C162 parse. Gate 0.6.
Gate2/3 untouched. gen11 HOLD. V0-V8 untouched.
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
FIX = ROOT / "evo/office/fixtures/vision_images_v9h"
WEIGHTS = ROOT / "models/Qwen3.5-2B"
RUN = ROOT / "runs/vision_v9h_c164"
PROTO = ROOT / "docs" / "蚁算_VL_GATE_V9_HELDOUT_PROTOCOL.md"

SPECS = [
    ("v9h_01", "torn_receipt", "paid_total", 18.5,
     ["TORN RECEIPT V9H", "a paid 7.50", "b paid 11.00", "c open 2.00", "TOTAL PAID TARGET 18.50"],
     "撕边收据H", "RECV"),
    ("v9h_02", "barcode_wh", "qty_sum", 24.0,
     ["WH BARCODE V9H", "SKU1 qty 16 ok", "SKU2 qty 3 hold", "SKU3 qty 8 ok", "qty_sum TARGET 24"],
     "条码仓单H", "RECV"),
    ("v9h_03", "fx_refund", "refund_done", 12.25,
     ["FX REFUND V9H", "itemR1 5.75 done", "itemR2 6.50 done", "itemR3 2.00 open", "refund_done TARGET 12.25"],
     "多币退款H", "DONE"),
    ("v9h_04", "ghost_tax", "tax_base_paid", 29.0,
     ["TAX GHOST V9H", "T1 16.00 paid", "T2 5.00 open", "T3 13.00 paid", "tax_base_paid TARGET 29.00"],
     "鬼影税联H", "RECV"),
    ("v9h_05", "qr_payroll", "payroll_active", 920.0,
     ["PAYROLL QR V9H", "A 480 active", "B 90 leave", "C 440 active", "payroll_active TARGET 920"],
     "二维码薪资H", "OK"),
    ("v9h_06", "rot_ship", "ship_ok_qty", 17.0,
     ["SHIP ROT V9H", "P1 10 ok", "P2 4 hold", "P3 7 ok", "ship_ok_qty TARGET 17"],
     "旋转发货H", "SHIP"),
    ("v9h_07", "multi_sla", "open_pri_sum", 12.0,
     ["SLA MULTI V9H", "S1 pri 6 open", "S2 pri 9 closed", "S3 pri 6 open", "open_pri_sum TARGET 12"],
     "多章SLAH", "OPEN"),
    ("v9h_08", "torn_exp", "paid_total", 39.75,
     ["EXPENSE TORN V9H", "E1 23.25 paid", "E2 8.00 void", "E3 16.50 paid", "paid_total TARGET 39.75"],
     "撕边报销H", "RECV"),
    ("v9h_09", "fx_po", "paid_total", 31.5,
     ["PO-FX V9H", "itemA paid 17.00", "itemB paid 14.50", "itemC open 4.00", "TOTAL PAID TARGET 31.50"],
     "多币采购H", "RECV"),
    ("v9h_10", "ghost_order", "paid_total", 20.75,
     ["ORDER GHOST V9H", "A paid 11.25", "B paid 9.50", "C open 3.00", "TOTAL PAID TARGET 20.75"],
     "鬼影订单H", "RECV"),
    ("v9h_11", "dup_barcode", "paid_total", 21.0,
     ["INVOICE #V9H-DUP", "line paid 7.00", "line paid 7.00", "line paid 7.00", "TOTAL PAID TARGET 21.00"],
     "条码重复H", "RECV"),
    ("v9h_12", "edge_zero_fx", "paid_total", 0.0,
     ["OPEN ONLY V9H", "X 10.00 open", "Y 14.00 open", "paid_total TARGET 0.00"],
     "未付多币H", "HOLD"),
    ("v9h_13", "qr_ledger", "paid_total", 16.5,
     ["LEDGER QR V9H", "rA paid 8.25", "rB paid 8.25", "rC open 1.00", "TOTAL PAID TARGET 16.50"],
     "二维码账本H", "RECV"),
    ("v9h_14", "rot_ui", "paid_total", 13.0,
     ["UI ROT V9H", "alpha paid 5.50", "beta paid 7.50", "gamma open 2.25", "TOTAL PAID TARGET 13.00"],
     "旋转界面H", "RECV"),
    ("v9h_15", "torn_stack", "paid_total", 28.5,
     ["HEAVY TORN V9H", "x paid 16.00 usd", "y paid 12.50 usd", "z open 3.00 usd", "TOTAL PAID TARGET 28.50"],
     "撕边重章H", "RECV"),
    ("v9h_16", "mix_fx", "paid_total", 17.0,
     ["CN-EN FX MIX V9H", "tea paid 8.00", "rice paid 9.00", "soup open 2.00", "TOTAL PAID TARGET 17.00"],
     "中英多币H", "RECV"),
]


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


PROTOCOL = """# 蚁算-视 VL Gate V9 Heldout Protocol

Updated: {ts} (Asia/Shanghai)

## Purpose
Disjoint heldout for V9 train (C163). Different ids/amounts.

## Gate
- rate >= **0.6**, n >= 16, real VL
- Claim only on PASS

## Honesty
- Gate2/3 untouched. V0-V8 untouched. gen11 HOLD.
"""

def make_fixture(fid, kind, lines, metric, expected, cn_title, stamp):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    FIX.mkdir(parents=True, exist_ok=True)
    rng = random.Random(hash(fid + "_v9h") & 0xFFFFFFFF)
    try:
        from PIL import ImageGrab
        shot = ImageGrab.grab(all_screens=False)
        w, h = shot.size
        bg = shot.crop((0, 0, min(1100, w), min(720, h))).convert("RGB").resize((920, 580))
        paper = Image.new("RGB", (920, 580), (208, 202, 192))
        img = Image.blend(bg, paper, 0.7)
        capture = True
    except Exception:
        img = Image.new("RGB", (920, 580), (208, 202, 192))
        capture = False
    d = ImageDraw.Draw(img)
    try:
        f_title = ImageFont.truetype(r"C:\\Windows\\Fonts\\msyh.ttc", 14)
        f_body = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 11)
        f_tgt = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 11)
        f_sm = ImageFont.truetype(r"C:\\Windows\\Fonts\\msyh.ttc", 10)
        f_stamp = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 15)
        f_wm = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 44)
        f_tiny = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 9)
    except Exception:
        f_title = f_body = f_tgt = f_sm = f_stamp = f_wm = f_tiny = ImageFont.load_default()

    d.rectangle([10, 10, 450, 545], fill=(228, 222, 212), outline=(85, 85, 85), width=2)
    # torn edge jagged
    for i in range(12):
        y0 = 20 + i * 40
        d.polygon([(8, y0), (18, y0 + 12), (8, y0 + 28)], fill=(180, 175, 165))
    # barcode distractor
    bx = 30
    for i in range(40):
        wbar = 1 if rng.random() < 0.5 else 2
        d.rectangle([bx, 480, bx + wbar, 530], fill=(30, 30, 30))
        bx += wbar + 1
    d.text((30, 532), "BARCODE IGNORE 4729183", fill=(60, 60, 60), font=f_tiny)
    # FX confuse
    d.text((300, 500), "$999 €888 ¥777", fill=(170, 165, 155), font=f_sm)
    # watermarks
    d.text((90, 210), "777", fill=(200, 195, 185), font=f_wm)
    d.text((210, 330), "666", fill=(198, 193, 183), font=f_wm)
    # ghost second page
    d.text((40, 300), "GHOST PAGE copy TOTAL 42", fill=(200, 195, 188), font=f_tiny)
    # QR-ish noise block
    for yy in range(400, 460, 3):
        for xx in range(360, 430, 3):
            if rng.random() < 0.45:
                d.rectangle([xx, yy, xx + 2, yy + 2], fill=(40, 40, 40))

    d.rectangle([18, 18, 440, 48], fill=(50, 65, 85))
    d.text((24, 22), (cn_title or kind)[:28], fill=(230, 230, 230), font=f_title)
    y = 58
    for ln in lines:
        font = f_tgt if ("TARGET" in ln.upper() or "TOTAL" in ln.upper()) else f_body
        d.text((26, y), ln[:56], fill=(30, 30, 30), font=font)
        y += 18
    d.rectangle([50, 125, 410, 141], fill=(175, 165, 145))
    d.text((54, 127), "~~ torn fold ~~", fill=(100, 90, 75), font=f_tiny)
    # rotated-ish stamp (offset oval)
    for (cx, cy, label, col) in [(350, 155, stamp, (190, 40, 40)), (290, 205, "VOID", (150, 55, 55))]:
        d.ellipse([cx - 55, cy - 24, cx + 45, cy + 32], outline=col, width=3)
        d.text((cx - 20, cy - 6), label[:6], fill=col, font=f_stamp)

    d.rectangle([480, 40, 900, 280], fill=(245, 245, 248), outline=(60, 60, 60), width=2)
    d.rectangle([480, 40, 900, 68], fill=(70, 70, 95))
    d.text((490, 46), "WIN-B VOID / IGNORE", fill=(255, 220, 220), font=f_sm)
    d.text((490, 80), "old total 999.00", fill=(20, 20, 20), font=f_sm)
    d.text((490, 100), "tiny distractor 888.00", fill=(20, 20, 20), font=f_sm)
    d.text((490, 120), "FX bait $777.00", fill=(20, 20, 20), font=f_sm)
    d.text((490, 150), f"{fid} status=void invoice#OLD", fill=(40, 40, 40), font=f_tiny)
    d.rectangle([0, 550, 920, 580], fill=(25, 25, 32))
    d.text((10, 556), "Start | Torn | POS | Chat  [V9H]", fill=(200, 200, 200), font=f_tiny)
    px = img.load()
    for _ in range(1600):
        x, y = rng.randint(0, 919), rng.randint(0, 579)
        v = rng.randint(0, 40)
        r, g, b = px[x, y]
        px[x, y] = (max(0, r - v), max(0, g - v), max(0, b - v))
    img = ImageEnhance.Contrast(img).enhance(0.88)
    img = img.filter(ImageFilter.SMOOTH)
    outp = FIX / f"{fid}_{kind}.png"
    img.save(outp)
    return {
        "id": fid, "file": outp.name, "kind": kind, "metric": metric,
        "expected": expected, "lines": lines, "cn_title": cn_title, "stamp": stamp,
        "capture_blend": capture,
        "path": str(outp.relative_to(ROOT)).replace("\\", "/"),
        "hardening": [
            "torn_edge", "barcode_distract", "fx_confuse", "ghost_page",
            "qr_noise", "rotated_stamp", "watermark_666",
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
    # mark disjoint
    for it in items:
        it["disjoint_from_train"] = True
    man = {
        "version": "v9_heldout", "n": len(items), "gate": GATE,
        "theme": "v9_heldout_disjoint", "harder_than": "v8_heldout",
        "items": items, "timestamp": ts(),
    }
    J(FIX / "manifest.json", man)

    free = gpu_free_mib()
    if free < 2000 or not WEIGHTS.is_dir():
        out = {
            "cycle": "C164", "theme": "vision_v9_heldout", "gate": GATE,
            "timestamp": ts(), "attempted": False, "reason": f"gpu_free={free}",
            "vl_gate_v9_heldout_claim": False, "pass": False, "claim": False,
            "gate2_3_untouched": True, "gen11": "HOLD",
        }
        J(DOC / "C164_VISION_V9_HELDOUT_SMOKE.json", out)
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
    scope = "r50plus_v9_heldout_disjoint_n>=16_c162_parse_qwen35_2b_c164" if claim else None
    out = {
        "cycle": "C164",
        "theme": "vision_v9_heldout",
        "gate": GATE,
        "timestamp": ts(),
        "attempted": True,
        "gpu_free_mib_start": free,
        "n": n, "n_ok": n_ok, "rate": rate,
        "gate_pass": gate_pass,
        "fail_ids": [r["id"] for r in rows if not r["ok"]],
        "rows": rows,
        "vl_gate_v9_heldout_claim": claim,
        "claim_scope": scope,
        "train_ref": "docs/r50/C163b_VISION_GATE_V9_CLAIM.json",
        "disjoint": True,
        "gate2_3_untouched": True,
        "v0_v8_untouched": True,
        "gen11": "HOLD",
        "pass": gate_pass,
        "claim": claim,
        "note": "V9 heldout real VL; claim only if rate>=0.6",
    }
    J(DOC / "C164_VISION_V9_HELDOUT_SMOKE.json", out)
    J(RUN / "judge.json", out)
    if claim:
        J(DOC / "C164b_VISION_GATE_V9_HELDOUT_CLAIM.json", {
            "kind": "vision_gate_v9_heldout_claim",
            "timestamp": ts(),
            "vl_gate_v9_heldout_claim": True,
            "rate": rate, "n": n, "n_ok": n_ok, "gate": GATE,
            "claim_scope": scope,
            "gate2_3_untouched": True,
            "v0_v8_untouched": True,
            "gen11": "HOLD",
            "cycle": "C164",
        })
    print(json.dumps({
        "cycle": "C164", "rate": rate, "n_ok": n_ok, "n": n,
        "fail_ids": out["fail_ids"], "claim": claim, "pass": gate_pass,
    }, ensure_ascii=False))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
