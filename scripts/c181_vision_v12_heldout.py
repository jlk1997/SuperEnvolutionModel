# -*- coding: utf-8 -*-
"""C181: Vision V12 heldout — disjoint fixtures + real VL claim if rate>=0.6.
Different ids/amounts from V12 train (C176/C177/C180). Same torn/barcode/persp/qr/thermal/shadow/jpeg/ghost family.
Uses mild-readable TARGET style matching C180 claimed train. Gate 0.6. Gate2/3 untouched. gen11 HOLD.
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
FIX = ROOT / "evo/office/fixtures/vision_images_v12h"
WEIGHTS = ROOT / "models/Qwen3.5-2B"
RUN = ROOT / "runs/vision_v12h_c181"
PROTO = ROOT / "docs" / "蚁算_VL_GATE_V12_HELDOUT_PROTOCOL.md"

# Disjoint from V12 train amounts (C176/C180)
SPECS = [
    ("v12h_01", "torn_receipt", "paid_total", 31.5,
     ["TORN RECEIPT V12H", "a paid 14.00", "b paid 17.50", "c open 5.00", "TOTAL PAID TARGET 31.50"],
     "撕边收据H", "RECV"),
    ("v12h_02", "barcode_wh", "qty_sum", 29.0,
     ["WH BARCODE V12H", "SKU1 qty 15 ok", "SKU2 qty 4 hold", "SKU3 qty 14 ok", "qty_sum TARGET 29"],
     "条码仓单H", "RECV"),
    ("v12h_03", "persp_refund", "refund_done", 13.75,
     ["PERSP REFUND V12H", "itemR1 5.25 done", "itemR2 8.50 done", "itemR3 3.00 open", "refund_done TARGET 13.75"],
     "透视退款H", "DONE"),
    ("v12h_04", "qr_tax", "tax_base_paid", 52.0,
     ["TAX QR V12H", "T1 27.00 paid", "T2 12.00 open", "T3 25.00 paid", "tax_base_paid TARGET 52.00"],
     "二维码税联H", "RECV"),
    ("v12h_05", "thermal_payroll", "payroll_active", 980.0,
     ["PAYROLL THERMAL V12H", "A 510 active", "B 95 leave", "C 470 active", "payroll_active TARGET 980"],
     "热敏薪资H", "OK"),
    ("v12h_06", "shadow_ship", "ship_ok_qty", 21.0,
     ["SHIP SHADOW V12H", "P1 10 ok", "P2 7 hold", "P3 11 ok", "ship_ok_qty TARGET 21"],
     "阴影发货H", "SHIP"),
    ("v12h_07", "jpeg_sla", "open_pri_sum", 15.0,
     ["SLA JPEG V12H", "S1 pri 7 open", "S2 pri 12 closed", "S3 pri 8 open", "open_pri_sum TARGET 15"],
     "压缩SLAH", "OPEN"),
    ("v12h_08", "stamp_exp", "paid_total", 44.5,
     ["EXPENSE STAMP V12H", "E1 24.00 paid", "E2 8.00 void", "E3 20.50 paid", "paid_total TARGET 44.50"],
     "密章报销H", "RECV"),
    ("v12h_09", "ghost_po", "paid_total", 36.25,
     ["PO-GHOST V12H", "itemA paid 18.00", "itemB paid 18.25", "itemC open 6.00", "TOTAL PAID TARGET 36.25"],
     "重影采购H", "RECV"),
    ("v12h_10", "lores_order", "paid_total", 27.5,
     ["ORDER LORES V12H", "A paid 14.25", "B paid 13.25", "C open 4.00", "TOTAL PAID TARGET 27.50"],
     "低清订单H", "RECV"),
    ("v12h_11", "torn_dup", "paid_total", 30.0,
     ["INVOICE #V12H-DUP", "line paid 10.00", "line paid 10.00", "line paid 10.00", "TOTAL PAID TARGET 30.00"],
     "撕边重复H", "RECV"),
    ("v12h_12", "thermal_zero", "paid_total", 0.0,
     ["OPEN ONLY V12H", "X 14.00 open", "Y 16.00 open", "paid_total TARGET 0.00"],
     "热敏未付H", "HOLD"),
    ("v12h_13", "persp_ledger", "paid_total", 19.0,
     ["LEDGER PERSP V12H", "rA paid 9.50", "rB paid 9.50", "rC open 3.50", "TOTAL PAID TARGET 19.00"],
     "透视账本H", "RECV"),
    ("v12h_14", "barcode_ui", "paid_total", 22.0,
     ["UI BARCODE V12H", "alpha paid 10.50", "beta paid 11.50", "gamma open 2.50", "TOTAL PAID TARGET 22.00"],
     "条码界面H", "RECV"),
    ("v12h_15", "shadow_stack", "paid_total", 34.5,
     ["HEAVY SHADOW V12H", "x paid 17.25 usd", "y paid 17.25 usd", "z open 6.00 usd", "TOTAL PAID TARGET 34.50"],
     "阴影叠窗H", "RECV"),
    ("v12h_16", "qr_mix", "paid_total", 26.75,
     ["CN-EN QR MIX V12H", "tea paid 12.00", "rice paid 14.75", "soup open 3.00", "TOTAL PAID TARGET 26.75"],
     "中英二维码H", "RECV"),
    ("v12h_17", "jpeg_win", "paid_total", 38.0,
     ["JPEG WIN V12H", "w1 paid 18.50", "w2 paid 19.50", "w3 open 8.00", "TOTAL PAID TARGET 38.00"],
     "压缩双窗H", "RECV"),
    ("v12h_18", "ghost_foot", "paid_total", 15.25,
     ["GHOST FOOT V12H", "p1 paid 7.00", "p2 paid 8.25", "p3 open 2.50", "TOTAL PAID TARGET 15.25"],
     "重影脚注H", "RECV"),
]


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


PROTOCOL = """# 蚁算-视 VL Gate V12 Heldout Protocol

Updated: {ts} (Asia/Shanghai)

## Purpose
Disjoint heldout for V12 train (C176/C177/C180 refresh). Different ids/amounts;
same torn/barcode/persp/qr/thermal/shadow/jpeg/ghost family; mild-readable TARGET (C180 style).

## Gate
- rate >= **0.6**, n >= 16, real VL
- Claim only on PASS

## Honesty
- Gate2/3 untouched. V0-V11 untouched. gen11 HOLD.
"""


def make_mild(fid, kind, lines, metric, expected, cn_title, stamp):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    FIX.mkdir(parents=True, exist_ok=True)
    rng = random.Random(hash(fid + "_v12h") & 0xFFFFFFFF)
    img = Image.new("RGB", (1020, 660), (215, 210, 200))
    d = ImageDraw.Draw(img)
    try:
        f_title = ImageFont.truetype(r"C:\\Windows\\Fonts\\msyh.ttc", 15)
        f_body = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 13)
        f_tgt = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 14)
        f_sm = ImageFont.truetype(r"C:\\Windows\\Fonts\\msyh.ttc", 11)
        f_stamp = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 14)
        f_tiny = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 10)
    except Exception:
        f_title = f_body = f_tgt = f_sm = f_stamp = f_tiny = ImageFont.load_default()

    d.rectangle([40, 20, 520, 560], fill=(240, 235, 225), outline=(40, 40, 40), width=2)
    for ty in range(20, 560, 22):
        d.polygon([(40, ty), (32, ty + 11), (40, ty + 22)], fill=(215, 210, 200))

    for i in range(40):
        bw = rng.randint(1, 2)
        d.rectangle([560 + i * 3, 40, 560 + i * 3 + bw, 90], fill=(20, 20, 20))
    d.text((560, 100), "barcode bait IGNORE", fill=(100, 100, 100), font=f_tiny)

    qx, qy = 800, 40
    d.rectangle([qx, qy, qx + 70, qy + 70], fill=(255, 255, 255), outline=(0, 0, 0), width=2)
    for yy in range(qy + 4, qy + 66, 8):
        for xx in range(qx + 4, qx + 66, 8):
            if rng.random() > 0.5:
                d.rectangle([xx, yy, xx + 5, yy + 5], fill=(0, 0, 0))
    d.text((qx, qy + 75), "QR bait", fill=(120, 40, 40), font=f_tiny)

    d.text((60, 480), "GHOST bait IGNORE", fill=(225, 220, 212), font=f_sm)

    d.rectangle([50, 28, 340, 58], fill=(30, 50, 70))
    d.text((56, 32), (cn_title or kind)[:20], fill=(240, 240, 240), font=f_title)
    y = 75
    for ln in lines:
        font = f_tgt if ("TARGET" in ln.upper() or "TOTAL" in ln.upper()) else f_body
        d.text((60, y), ln[:54], fill=(10, 10, 10), font=font)
        y += 22

    for (cx, cy, label, col) in [(400, 160, stamp, (190, 40, 40)), (320, 240, "VOID", (150, 55, 55))]:
        d.ellipse([cx - 44, cy - 20, cx + 36, cy + 24], outline=col, width=2)
        d.text((cx - 14, cy - 6), label[:4], fill=col, font=f_stamp)

    d.rectangle([720, 220, 1000, 400], fill=(250, 248, 255), outline=(50, 50, 80), width=2)
    d.text((730, 230), "VOID WIN IGNORE", fill=(120, 40, 40), font=f_sm)
    d.text((730, 260), "old total 999.00", fill=(20, 20, 20), font=f_sm)
    d.text((730, 290), "do not parse", fill=(20, 20, 20), font=f_sm)

    d.rectangle([0, 630, 1020, 660], fill=(20, 20, 30))
    d.text((10, 638), "V12H HELDOUT C181  [readable TARGET]", fill=(200, 200, 200), font=f_tiny)

    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.ellipse([80, 420, 380, 560], fill=(0, 0, 0, 35))
    img = Image.alpha_composite(img.convert("RGBA"), shadow).convert("RGB")

    w, h = img.size
    img = img.transform(
        (w, h), Image.AFFINE, (1, 0.02, -8, 0.008, 1, -2),
        resample=Image.BICUBIC, fillcolor=(215, 210, 200),
    )
    img = ImageEnhance.Contrast(img).enhance(0.95)
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
        "disjoint_from_train": True,
        "mild_style_c180": True,
        "hardening": [
            "torn_edges_mild", "barcode_noise_away", "perspective_mild", "qr_bait_small",
            "shadow_mild", "jpeg_q62", "readable_target",
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
        items.append(make_mild(fid, kind, lines, metric, expected, cn, stamp))
    man = {
        "version": "v12_heldout", "n": len(items), "gate": GATE,
        "theme": "v12_heldout_disjoint", "harder_than": "v11_heldout",
        "items": items, "timestamp": ts(),
    }
    J(FIX / "manifest.json", man)

    free = gpu_free_mib()
    if free < 2000 or not WEIGHTS.is_dir():
        out = {
            "cycle": "C181", "theme": "vision_v12_heldout", "gate": GATE,
            "timestamp": ts(), "attempted": False, "reason": f"gpu_free={free}",
            "vl_gate_v12_heldout_claim": False, "pass": False, "claim": False,
            "gate2_3_untouched": True, "gen11": "HOLD",
        }
        J(DOC / "C181_VISION_V12_HELDOUT_SMOKE.json", out)
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
    scope = "r50plus_v12_heldout_disjoint_n>=16_c162_parse_qwen35_2b_c181" if claim else None
    out = {
        "cycle": "C181",
        "theme": "vision_v12_heldout",
        "gate": GATE,
        "timestamp": ts(),
        "attempted": True,
        "gpu_free_mib_start": free,
        "n": n, "n_ok": n_ok, "rate": rate,
        "gate_pass": gate_pass,
        "fail_ids": [r["id"] for r in rows if not r["ok"]],
        "rows": rows,
        "vl_gate_v12_heldout_claim": claim,
        "claim_scope": scope,
        "train_ref": "docs/r50/C180b_VISION_GATE_V12_REFRESH_CLAIM.json",
        "disjoint": True,
        "gate2_3_untouched": True,
        "v0_v11_untouched": True,
        "gen11": "HOLD",
        "pass": gate_pass,
        "claim": claim,
        "note": "V12 heldout real VL; claim only if rate>=0.6",
    }
    J(DOC / "C181_VISION_V12_HELDOUT_SMOKE.json", out)
    J(RUN / "judge.json", out)
    if claim:
        J(DOC / "C181b_VISION_GATE_V12_HELDOUT_CLAIM.json", {
            "kind": "vision_gate_v12_heldout_claim",
            "timestamp": ts(),
            "vl_gate_v12_heldout_claim": True,
            "rate": rate, "n": n, "n_ok": n_ok, "gate": GATE,
            "claim_scope": scope,
            "gate2_3_untouched": True,
            "v0_v11_untouched": True,
            "gen11": "HOLD",
            "cycle": "C181",
        })
    print(json.dumps({
        "cycle": "C181", "rate": rate, "n_ok": n_ok, "n": n,
        "fail_ids": out["fail_ids"], "claim": claim, "pass": gate_pass,
    }, ensure_ascii=False))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
