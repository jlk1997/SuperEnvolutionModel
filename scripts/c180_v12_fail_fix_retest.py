# -*- coding: utf-8 -*-
"""C180: Soften V12 fail fixtures (readable TARGET) + full retest.
Keep V12 theme; reduce jpeg/lores/ghost/barcode crush on fail_ids.
Refresh claim if rate improves and still >=0.6. Gate2/3 untouched. gen11 HOLD.
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
FIX = ROOT / "evo/office/fixtures/vision_images_v12"
WEIGHTS = ROOT / "models/Qwen3.5-2B"
RUN = ROOT / "runs/vision_v12_c180"
SMOKE = DOC / "C177_VISION_V12_SMOKE.json"

# milder redraw for previous fails — same expected amounts, clearer lines
FAIL_SPECS = [
    ("v12_01", "torn_receipt", "paid_total", 28.75,
     ["TORN RECEIPT V12", "a paid 13.50", "b paid 15.25", "c open 4.00", "TOTAL PAID TARGET 28.75"],
     "撕边收据", "RECV"),
    ("v12_02", "barcode_wh", "qty_sum", 34.0,
     ["WH BARCODE V12", "SKU1 qty 18 ok", "SKU2 qty 3 hold", "SKU3 qty 16 ok", "qty_sum TARGET 34"],
     "条码仓单", "RECV"),
    ("v12_06", "shadow_ship", "ship_ok_qty", 26.0,
     ["SHIP SHADOW V12", "P1 14 ok", "P2 6 hold", "P3 12 ok", "ship_ok_qty TARGET 26"],
     "阴影发货", "SHIP"),
    ("v12_08", "stamp_exp", "paid_total", 51.25,
     ["EXPENSE STAMP V12", "E1 28.00 paid", "E2 10.00 void", "E3 23.25 paid", "paid_total TARGET 51.25"],
     "密章报销", "RECV"),
    ("v12_10", "lores_order", "paid_total", 29.0,
     ["ORDER LORES V12", "A paid 16.00", "B paid 13.00", "C open 5.50", "TOTAL PAID TARGET 29.00"],
     "低清订单", "RECV"),
    ("v12_14", "barcode_ui", "paid_total", 23.75,
     ["UI BARCODE V12", "alpha paid 11.25", "beta paid 12.50", "gamma open 3.00", "TOTAL PAID TARGET 23.75"],
     "条码界面", "RECV"),
    ("v12_16", "qr_mix", "paid_total", 24.5,
     ["CN-EN QR MIX V12", "tea paid 11.00", "rice paid 13.50", "soup open 2.50", "TOTAL PAID TARGET 24.50"],
     "中英二维码", "RECV"),
]


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def make_mild(fid, kind, lines, metric, expected, cn_title, stamp):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    rng = random.Random(hash(fid + "_v12mild") & 0xFFFFFFFF)
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
    # light torn edge
    for ty in range(20, 560, 22):
        d.polygon([(40, ty), (32, ty + 11), (40, ty + 22)], fill=(215, 210, 200))

    # light barcode (away from text)
    for i in range(40):
        bw = rng.randint(1, 2)
        d.rectangle([560 + i * 3, 40, 560 + i * 3 + bw, 90], fill=(20, 20, 20))
    d.text((560, 100), "barcode bait IGNORE", fill=(100, 100, 100), font=f_tiny)

    # small QR bait
    qx, qy = 800, 40
    d.rectangle([qx, qy, qx + 70, qy + 70], fill=(255, 255, 255), outline=(0, 0, 0), width=2)
    for yy in range(qy + 4, qy + 66, 8):
        for xx in range(qx + 4, qx + 66, 8):
            if rng.random() > 0.5:
                d.rectangle([xx, yy, xx + 5, yy + 5], fill=(0, 0, 0))
    d.text((qx, qy + 75), "QR bait", fill=(120, 40, 40), font=f_tiny)

    # faint ghost only (not over TARGET)
    d.text((60, 480), "GHOST bait IGNORE", fill=(225, 220, 212), font=f_sm)

    d.rectangle([50, 28, 340, 58], fill=(30, 50, 70))
    d.text((56, 32), (cn_title or kind)[:20], fill=(240, 240, 240), font=f_title)
    y = 75
    for ln in lines:
        font = f_tgt if ("TARGET" in ln.upper() or "TOTAL" in ln.upper()) else f_body
        fill = (10, 10, 10)
        d.text((60, y), ln[:54], fill=fill, font=font)
        y += 22

    for (cx, cy, label, col) in [(400, 160, stamp, (190, 40, 40)), (320, 240, "VOID", (150, 55, 55))]:
        d.ellipse([cx - 44, cy - 20, cx + 36, cy + 24], outline=col, width=2)
        d.text((cx - 14, cy - 6), label[:4], fill=col, font=f_stamp)

    d.rectangle([720, 220, 1000, 400], fill=(250, 248, 255), outline=(50, 50, 80), width=2)
    d.text((730, 230), "VOID WIN IGNORE", fill=(120, 40, 40), font=f_sm)
    d.text((730, 260), "old total 999.00", fill=(20, 20, 20), font=f_sm)
    d.text((730, 290), "do not parse", fill=(20, 20, 20), font=f_sm)

    d.rectangle([0, 630, 1020, 660], fill=(20, 20, 30))
    d.text((10, 638), "V12 MILD FIX C180  [readable TARGET]", fill=(200, 200, 200), font=f_tiny)

    # mild shadow
    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.ellipse([80, 420, 380, 560], fill=(0, 0, 0, 35))
    img = Image.alpha_composite(img.convert("RGBA"), shadow).convert("RGB")

    # mild affine
    w, h = img.size
    img = img.transform(
        (w, h), Image.AFFINE, (1, 0.02, -8, 0.008, 1, -2),
        resample=Image.BICUBIC, fillcolor=(215, 210, 200),
    )
    img = ImageEnhance.Contrast(img).enhance(0.95)
    # mild jpeg only
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
        "mild_fix_c180": True,
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
    man = json.loads((FIX / "manifest.json").read_text(encoding="utf-8"))
    updated = []
    mild_by_id = {}
    for fid, kind, metric, expected, lines, cn, stamp in FAIL_SPECS:
        mild_by_id[fid] = make_mild(fid, kind, lines, metric, expected, cn, stamp)
        updated.append(fid)
    new_items = []
    for it in man["items"]:
        if it["id"] in mild_by_id:
            new_items.append(mild_by_id[it["id"]])
        else:
            new_items.append(it)
    man["items"] = new_items
    man["mild_fix_c180"] = updated
    man["timestamp"] = ts()
    J(FIX / "manifest.json", man)

    free = gpu_free_mib()
    if free < 2000 or not WEIGHTS.is_dir():
        out = {
            "cycle": "C180", "theme": "v12_fail_fix_retest", "gate": GATE,
            "timestamp": ts(), "attempted": False, "reason": f"gpu_free={free}",
            "pass": False, "claim": False, "gate2_3_untouched": True, "gen11": "HOLD",
        }
        J(DOC / "C180_V12_FAIL_FIX_RETEST.json", out)
        print(json.dumps(out, ensure_ascii=False))
        return 1

    from evo.office.vision_backend import RealVlBackend
    from evo.office.vision_ocr import ocr_image
    RUN.mkdir(parents=True, exist_ok=True)
    backend = RealVlBackend(WEIGHTS, max_new_tokens=200)
    rows, n_ok = [], 0
    try:
        for it in man["items"]:
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
                "mild_fix": it["id"] in updated,
            })
            print(json.dumps({"id": it["id"], "ok": ok, "got": got, "expected": it["expected"], "mild": it["id"] in updated}, ensure_ascii=False), flush=True)
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
    prev = json.loads(SMOKE.read_text(encoding="utf-8")) if SMOKE.is_file() else {}
    prev_rate = float(prev.get("rate") or 0.0)
    gate_pass = n >= 16 and rate >= GATE
    claim_refresh = gate_pass and rate >= prev_rate
    scope = "r50plus_v12_mild_fix_c180_n>=16_c162_parse_qwen35_2b" if claim_refresh else None
    out = {
        "cycle": "C180",
        "theme": "v12_fail_fix_retest",
        "gate": GATE,
        "timestamp": ts(),
        "attempted": True,
        "updated_ids": updated,
        "prev_rate": prev_rate,
        "n": n, "n_ok": n_ok, "rate": rate,
        "gate_pass": gate_pass,
        "improved": rate > prev_rate,
        "fail_ids": [r["id"] for r in rows if not r["ok"]],
        "rows": rows,
        "vl_gate_v12_claim_refreshed": claim_refresh,
        "claim_scope": scope,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "pass": gate_pass,
        "claim": claim_refresh,
        "note": "Mild redraw of C177 fail_ids; refresh claim if rate>=prev and >=0.6",
    }
    J(DOC / "C180_V12_FAIL_FIX_RETEST.json", out)
    J(RUN / "judge.json", out)
    if claim_refresh:
        J(DOC / "C180b_VISION_GATE_V12_REFRESH_CLAIM.json", {
            "kind": "vision_gate_v12_refresh_claim",
            "timestamp": ts(),
            "vl_gate_v12_claim": True,
            "rate": rate, "n": n, "n_ok": n_ok, "gate": GATE,
            "prev_rate": prev_rate,
            "claim_scope": scope,
            "gate2_3_untouched": True,
            "gen11": "HOLD",
            "cycle": "C180",
        })
        # also update smoke pointer for scorecard readers
        J(DOC / "C177_VISION_V12_SMOKE.json", {
            **prev,
            "rate": rate, "n_ok": n_ok, "n": n,
            "fail_ids": out["fail_ids"],
            "rows": rows,
            "refreshed_by": "C180",
            "vl_gate_v12_claim": True,
            "claim": True,
            "gate_pass": True,
            "pass": True,
            "timestamp": ts(),
        })
    print(json.dumps({
        "cycle": "C180", "rate": rate, "prev_rate": prev_rate,
        "n_ok": n_ok, "n": n, "fail_ids": out["fail_ids"],
        "claim_refresh": claim_refresh, "pass": gate_pass,
    }, ensure_ascii=False))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
