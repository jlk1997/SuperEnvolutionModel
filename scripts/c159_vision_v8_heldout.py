# -*- coding: utf-8 -*-
"""C159: Vision V8 heldout — disjoint fixtures + real VL claim if rate>=0.6.
Different ids/amounts from V8 train. Uses C158b parse (666 noise, colon, dup-safe).
Gate 0.6. Gate2/3 untouched. gen11 HOLD. V0–V7 untouched.
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
FIX = ROOT / "evo/office/fixtures/vision_images_v8h"
WEIGHTS = ROOT / "models/Qwen3.5-2B"
RUN = ROOT / "runs/vision_v8h_c159"
PROTO = ROOT / "docs" / "蚁算_VL_GATE_V8_HELDOUT_PROTOCOL.md"

# Disjoint from train: different ids, amounts, kinds mix
SPECS = [
    ("v8h_01", "fax_receipt", "paid_total", 17.5,
     ["RECEIPT #V8H-01", "coffee paid 9.50", "bagel paid 8.00", "juice open 3.00", "TOTAL PAID TARGET 17.50"],
     "传真收据H", "RECV"),
    ("v8h_02", "carbon_wh", "qty_sum", 23.0,
     ["WH TICKET V8H", "BOLT qty 14 ok", "NUT qty 5 hold", "CLIP qty 9 ok", "qty_sum TARGET 23"],
     "复写仓单H", "RECV"),
    ("v8h_03", "lowcon_refund", "refund_done", 11.5,
     ["REFUND STUB V8H", "itemR1 3.50 done", "itemR2 8.00 done", "itemR3 2.00 open", "refund_done TARGET 11.50"],
     "低对比退款H", "DONE"),
    ("v8h_04", "watermark_tax", "tax_base_paid", 28.0,
     ["TAX SLIP V8H", "T1 15.00 paid", "T2 6.00 open", "T3 13.00 paid", "tax_base_paid TARGET 28.00"],
     "水印税联H", "RECV"),
    ("v8h_05", "scribble_pay", "payroll_active", 780.0,
     ["PAYROLL V8H", "A 400 active", "B 70 leave", "C 380 active", "payroll_active TARGET 780"],
     "涂鸦薪资H", "OK"),
    ("v8h_06", "fax_ship", "ship_ok_qty", 15.0,
     ["SHIP RECEIPT V8H", "P1 9 ok", "P2 3 hold", "P3 6 ok", "ship_ok_qty TARGET 15"],
     "传真发货H", "SHIP"),
    ("v8h_07", "stampstack_sla", "open_pri_sum", 11.0,
     ["SLA TICKET V8H", "S1 pri 4 open", "S2 pri 8 closed", "S3 pri 7 open", "open_pri_sum TARGET 11"],
     "叠章SLAH", "OPEN"),
    ("v8h_08", "carbon_exp", "paid_total", 41.25,
     ["EXPENSE V8H", "E1 22.75 paid", "E2 9.00 void", "E3 18.50 paid", "paid_total TARGET 41.25"],
     "复写报销H", "RECV"),
    ("v8h_09", "po_watermark", "paid_total", 33.0,
     ["PO-91 V8H", "itemA paid 14.00", "itemB paid 19.00", "itemC open 4.50", "TOTAL PAID TARGET 33.00"],
     "水印采购H", "RECV"),
    ("v8h_10", "skew_order", "paid_total", 21.75,
     ["ORDER V8H", "A paid 10.25", "B paid 11.50", "C open 1.75", "TOTAL PAID TARGET 21.75"],
     "倾斜订单H", "RECV"),
    ("v8h_11", "dup_fax", "paid_total", 18.0,
     ["INVOICE #V8H-DUP", "line paid 6.00", "line paid 6.00", "line paid 6.00", "TOTAL PAID TARGET 18.00"],
     "传真重复H", "RECV"),
    ("v8h_12", "edge_zero_lc", "paid_total", 0.0,
     ["OPEN ONLY V8H", "X 11.00 open", "Y 17.00 open", "paid_total TARGET 0.00"],
     "低对比未付H", "HOLD"),
    ("v8h_13", "ledger_scribble", "paid_total", 15.25,
     ["LEDGER V8H", "rA paid 6.75", "rB paid 8.50", "rC open 2.00", "TOTAL PAID TARGET 15.25"],
     "涂鸦账本H", "RECV"),
    ("v8h_14", "ui_fax", "paid_total", 12.5,
     ["UI RECEIPT V8H", "alpha paid 5.00", "beta paid 7.50", "gamma open 2.25", "TOTAL PAID TARGET 12.50"],
     "界面传真H", "RECV"),
    ("v8h_15", "heavy_stack", "paid_total", 29.0,
     ["HEAVY STACK V8H", "x paid 17.00 usd", "y paid 12.00 usd", "z open 5.00 usd", "TOTAL PAID TARGET 29.00"],
     "重章叠印H", "RECV"),
    ("v8h_16", "mix_cn_fax", "paid_total", 16.0,
     ["CN-EN FAX MIX H", "tea paid 7.00", "rice paid 9.00", "soup open 2.00", "TOTAL PAID TARGET 16.00"],
     "中英传真H", "RECV"),
]


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


PROTOCOL = """# 蚁算-视 VL Gate V8 Heldout Protocol

Updated: {ts} (Asia/Shanghai)

## Purpose
Disjoint heldout for V8 train (C158b rate=1.0). Different ids/amounts.
Hardening vocabulary retained: low-contrast, fax, watermark 666/777, multi-stamp.
Parse: C158b (NOISE+=666, colon-decimal, dup-amount safe).

## Gate
- rate = n_ok/n >= **0.6**, n >= 16
- Real VL only (Qwen3.5-2B)
- Claim: `vl_gate_v8_heldout_claim=true` only on PASS

## Honesty
- No overlap with train expected totals / ids
- Gate2/3 untouched. V0–V7 untouched. gen11 HOLD.
"""


def make_fixture(fid, kind, lines, metric, expected, cn_title, stamp):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    FIX.mkdir(parents=True, exist_ok=True)
    rng = random.Random(hash(fid + "_v8h") & 0xFFFFFFFF)
    try:
        from PIL import ImageGrab
        shot = ImageGrab.grab(all_screens=False)
        w, h = shot.size
        bg = shot.crop((0, 0, min(1100, w), min(720, h))).convert("RGB").resize((920, 580))
        paper = Image.new("RGB", (920, 580), (210, 205, 195))
        img = Image.blend(bg, paper, 0.72)
        capture = True
    except Exception:
        img = Image.new("RGB", (920, 580), (210, 205, 195))
        capture = False
    d = ImageDraw.Draw(img)
    try:
        f_title = ImageFont.truetype(r"C:\\Windows\\Fonts\\msyh.ttc", 14)
        f_body = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 11)
        f_tgt = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 11)
        f_sm = ImageFont.truetype(r"C:\\Windows\\Fonts\\msyh.ttc", 10)
        f_stamp = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 16)
        f_wm = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 48)
        f_tiny = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 10)
    except Exception:
        f_title = f_body = f_tgt = f_sm = f_stamp = f_wm = f_tiny = ImageFont.load_default()

    d.rectangle([10, 10, 450, 545], fill=(225, 220, 210), outline=(90, 90, 90), width=2)
    for y in range(20, 540, 7):
        if rng.random() < 0.5:
            d.line([(12, y), (448, y)], fill=(190, 185, 175), width=1)
    d.text((80, 200), "777", fill=(200, 195, 185), font=f_wm)
    d.text((200, 320), "666", fill=(198, 193, 183), font=f_wm)
    d.rectangle([18, 18, 440, 48], fill=(55, 70, 90))
    d.text((24, 22), (cn_title or kind)[:28], fill=(230, 230, 230), font=f_title)
    y = 58
    for ln in lines:
        font = f_tgt if ("TARGET" in ln.upper() or "TOTAL" in ln.upper()) else f_body
        d.text((26, y), ln[:56], fill=(35, 35, 35), font=font)
        y += 18
    d.rectangle([50, 130, 410, 146], fill=(180, 170, 150))
    d.text((54, 132), "~~ fax fold ~~", fill=(110, 100, 85), font=f_tiny)
    for (cx, cy, label, col) in [(340, 160, stamp, (190, 40, 40)), (300, 200, "VOID", (160, 60, 60))]:
        d.ellipse([cx - 50, cy - 28, cx + 50, cy + 28], outline=col, width=3)
        d.text((cx - 22, cy - 8), label[:6], fill=col, font=f_stamp)
    for _ in range(5):
        x0, y0 = rng.randint(30, 400), rng.randint(60, 480)
        d.line([(x0, y0), (x0 + rng.randint(-40, 80), y0 + rng.randint(-20, 40))], fill=(40, 40, 120), width=1)
    d.rectangle([480, 40, 900, 260], fill=(245, 245, 248), outline=(60, 60, 60), width=2)
    d.rectangle([480, 40, 900, 68], fill=(80, 80, 100))
    d.text((490, 46), "WIN-B VOID / IGNORE", fill=(255, 220, 220), font=f_sm)
    d.text((490, 80), "old total 999.00", fill=(20, 20, 20), font=f_sm)
    d.text((490, 100), "tiny distractor 888.00", fill=(20, 20, 20), font=f_sm)
    d.text((490, 120), "occlusion copy TOTAL 42", fill=(20, 20, 20), font=f_sm)
    d.text((490, 150), f"{fid} status=void invoice#OLD", fill=(40, 40, 40), font=f_tiny)
    d.rectangle([0, 550, 920, 580], fill=(25, 25, 32))
    d.text((10, 556), "Start | Fax | POS | Chat  [V8H]", fill=(200, 200, 200), font=f_tiny)
    px = img.load()
    for _ in range(1400):
        x, y = rng.randint(0, 919), rng.randint(0, 579)
        v = rng.randint(0, 35)
        r, g, b = px[x, y]
        px[x, y] = (max(0, r - v), max(0, g - v), max(0, b - v))
    img = ImageEnhance.Contrast(img).enhance(0.9)
    img = img.filter(ImageFilter.SMOOTH)
    outp = FIX / f"{fid}_{kind}.png"
    img.save(outp)
    return {
        "id": fid, "file": outp.name, "kind": kind, "metric": metric,
        "expected": expected, "lines": lines, "cn_title": cn_title, "stamp": stamp,
        "capture_blend": capture,
        "path": str(outp.relative_to(ROOT)).replace("\\", "/"),
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
        items.append(make_fixture(fid, kind, lines, metric, expected, cn, stamp))
    man = {
        "version": "v8_heldout", "n": len(items), "gate": GATE,
        "theme": "v8_heldout_disjoint", "harder_than": "v7_heldout",
        "items": items, "timestamp": ts(),
    }
    J(FIX / "manifest.json", man)

    free = gpu_free_mib()
    if free < 2000 or not WEIGHTS.is_dir():
        out = {
            "cycle": "C159", "theme": "vision_v8_heldout", "gate": GATE,
            "timestamp": ts(), "attempted": False, "reason": f"gpu_free={free}",
            "vl_gate_v8_heldout_claim": False, "pass": False, "claim": False,
            "gate2_3_untouched": True, "gen11": "HOLD",
        }
        J(DOC / "C159_VISION_V8_HELDOUT_SMOKE.json", out)
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
    scope = "r50plus_v8_heldout_disjoint_n>=16_c158b_parse_qwen35_2b_c159" if claim else None
    out = {
        "cycle": "C159",
        "theme": "vision_v8_heldout",
        "gate": GATE,
        "timestamp": ts(),
        "attempted": True,
        "gpu_free_mib_start": free,
        "n": n, "n_ok": n_ok, "rate": rate,
        "gate_pass": gate_pass,
        "fail_ids": [r["id"] for r in rows if not r["ok"]],
        "rows": rows,
        "vl_gate_v8_heldout_claim": claim,
        "claim_scope": scope,
        "train_ref": "docs/r50/C158c_VISION_GATE_V8_REFRESH_CLAIM.json",
        "disjoint": True,
        "gate2_3_untouched": True,
        "v0_v7_untouched": True,
        "gen11": "HOLD",
        "pass": gate_pass,
        "claim": claim,
        "note": "V8 heldout real VL; claim only if rate>=0.6",
    }
    J(DOC / "C159_VISION_V8_HELDOUT_SMOKE.json", out)
    J(RUN / "judge.json", out)
    if claim:
        J(DOC / "C159b_VISION_GATE_V8_HELDOUT_CLAIM.json", {
            "kind": "vision_gate_v8_heldout_claim",
            "timestamp": ts(),
            "vl_gate_v8_heldout_claim": True,
            "rate": rate, "n": n, "n_ok": n_ok, "gate": GATE,
            "claim_scope": scope,
            "gate2_3_untouched": True,
            "v0_v7_untouched": True,
            "gen11": "HOLD",
            "cycle": "C159",
        })
    print(json.dumps({
        "cycle": "C159", "rate": rate, "n_ok": n_ok, "n": n,
        "fail_ids": out["fail_ids"], "claim": claim, "pass": gate_pass,
    }, ensure_ascii=False))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
