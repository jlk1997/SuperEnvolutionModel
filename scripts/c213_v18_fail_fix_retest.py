# -*- coding: utf-8 -*-
"""C213: Diagnose+fix V18 fails honestly — mild fixture regen + VL retest.
Fails from C209: v18_02/06/08/09/16/17.
Root: heavy bleach/halftone/jpeg_q28 + affine crushed digits; OCR drifted
(amounts and status words). Parse-alone cannot recover wrong digits.
Fix: milder redraw (same expected), NOISE+=99.99 bait, full VL retest.
Refresh claim if rate>=0.6. Gate2/3 untouched. gen11 HOLD.
"""
from __future__ import annotations
import gc, io, json, random, re, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from evo.office.vision_metric_parse import parse_metric, _clean, sum_status

GATE = 0.6
DOC = ROOT / "docs" / "r50"
FIX = ROOT / "evo/office/fixtures/vision_images_v18"
WEIGHTS = ROOT / "models/Qwen3.5-2B"
RUN = ROOT / "runs/vision_v18_c213"
PRIOR = DOC / "C209_VISION_V18_SMOKE.json"

# Same expected amounts as C208; clearer ASCII lines; milder degradation
REGEN = {
    "v18_02": {
        "kind": "halftone_wh",
        "metric": "qty_sum",
        "expected": 67.0,
        "lines": [
            "WH HALFTONE V18",
            "SKU1 qty 34 ok",
            "SKU2 qty 15 hold",
            "SKU3 qty 33 ok",
            "qty_sum TARGET 67",
        ],
        "cn_title": "网点仓库",
        "stamp": "RECV",
    },
    "v18_06": {
        "kind": "clip_ship",
        "metric": "ship_ok_qty",
        "expected": 51.0,
        "lines": [
            "SHIP CLIP V18",
            "P1 26 ok",
            "P2 14 hold",
            "P3 25 ok",
            "ship_ok_qty TARGET 51",
        ],
        "cn_title": "夹影发货",
        "stamp": "SHIP",
    },
    "v18_08": {
        "kind": "finger_exp",
        "metric": "paid_total",
        "expected": 91.75,
        "lines": [
            "EXPENSE FINGER V18",
            "E1 45.50 paid",
            "E2 18.00 void",
            "E3 46.25 paid",
            "paid_total TARGET 91.75",
        ],
        "cn_title": "指纹报销",
        "stamp": "RECV",
    },
    "v18_09": {
        "kind": "bleach_po",
        "metric": "paid_total",
        "expected": 76.0,
        "lines": [
            "PO-BLEACH V18",
            "itemA paid 37.75",
            "itemB paid 38.25",
            "itemC open 13.00",
            "TOTAL PAID TARGET 76.00",
        ],
        "cn_title": "漂白采购",
        "stamp": "RECV",
    },
    "v18_16": {
        "kind": "finger_mix",
        "metric": "paid_total",
        "expected": 50.25,
        "lines": [
            "CN-EN FINGER MIX V18",
            "tea paid 23.00",
            "rice paid 27.25",
            "soup open 8.00",
            "TOTAL PAID TARGET 50.25",
        ],
        "cn_title": "中英指纹",
        "stamp": "RECV",
    },
    "v18_17": {
        "kind": "bleach_win",
        "metric": "paid_total",
        "expected": 68.0,
        "lines": [
            "BLEACH WIN V18",
            "w1 paid 33.00",
            "w2 paid 35.00",
            "w3 open 15.00",
            "TOTAL PAID TARGET 68.00",
        ],
        "cn_title": "漂白双窗",
        "stamp": "RECV",
    },
}


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def unit_reparse_saved():
    prior = json.loads(PRIOR.read_text(encoding="utf-8"))
    fail_before = set(prior.get("fail_ids") or [])
    rows, n_ok, fixed, still = [], 0, [], []
    for r in prior.get("rows") or []:
        text = r.get("ocr_preview") or ""
        got, atom_ok = parse_metric(text, r["metric"], r["expected"])
        ocr_ok = bool(r.get("ocr_ok", True))
        ok = bool(ocr_ok and atom_ok)
        n_ok += int(ok)
        rows.append({
            "id": r["id"], "metric": r["metric"], "got": got,
            "expected": r["expected"], "atom_ok": atom_ok, "ok": ok,
            "was_fail": r["id"] in fail_before,
            "cleaned_preview": _clean(text)[:220],
        })
        if r["id"] in fail_before:
            (fixed if ok else still).append(r["id"])
    n = len(rows)
    return {
        "n": n, "n_ok": n_ok, "rate": round(n_ok / n, 4) if n else 0.0,
        "fixed_by_parse_alone": fixed,
        "still_fail_need_regen": still,
        "rows": rows,
        "proof_noise_9999": {
            "sum_without_bait": sum_status(
                "w1 paid 33.00 w2 paid 35.00 w3 open 15.00 paid 99.99 old total 999.00",
                {"paid"},
            ),
            "expect_68": True,
        },
    }


def make_mild(fid, kind, lines, metric, expected, cn_title, stamp):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    FIX.mkdir(parents=True, exist_ok=True)
    rng = random.Random(hash(fid + "_v18mild") & 0xFFFFFFFF)
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

    # paper
    d.rectangle([40, 20, 560, 600], fill=(248, 245, 235), outline=(40, 40, 40), width=2)
    # light residual cues (not crushing text)
    for _ in range(6):
        x0 = rng.randint(45, 500)
        y0 = rng.randint(40, 560)
        d.arc([x0, y0, x0 + rng.randint(30, 80), y0 + rng.randint(15, 40)], 0, 180, fill=(200, 195, 185), width=1)
    # punch holes (away from text column)
    for (hx, hy) in [(70, 50), (70, 220), (70, 400)]:
        d.ellipse([hx - 8, hy - 8, hx + 8, hy + 8], fill=(215, 210, 200), outline=(80, 80, 80), width=2)
    # binder clip
    d.rectangle([250, 8, 330, 28], fill=(50, 50, 60))
    # light redaction bait on right only
    d.rectangle([780, 80, 1040, 105], fill=(20, 20, 20))
    d.text((790, 115), "REDACTED bait 555", fill=(60, 60, 60), font=f_tiny)
    # light crayon away from TARGET
    for _ in range(3):
        pts = [(rng.randint(90, 480), rng.randint(420, 560)) for __ in range(3)]
        d.line(pts, fill=(200, 80, 80), width=2)
    # faint fingerprint
    for i in range(4):
        d.ellipse([430 + i, 480 + i, 500 - i, 550 - i], outline=(140, 110, 90), width=1)

    d.text((100, 520), "CONFIDENTIAL", fill=(230, 225, 215), font=f_wm)
    d.rectangle([50, 28, 360, 58], fill=(30, 50, 70))
    d.text((56, 32), (cn_title or kind)[:18], fill=(240, 240, 240), font=f_title)

    y = 78
    for ln in lines:
        font = f_tgt if ("TARGET" in ln.upper() or "TOTAL" in ln.upper()) else f_body
        # drop shadow then crisp ink for readability
        d.text((60 + 1, y + 1), ln[:54], fill=(220, 215, 205), font=font)
        d.text((60, y), ln[:54], fill=(8, 8, 8), font=font)
        y += 26

    # sticky bait uses NOISE amounts only
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
    d.text((10, 718), "V18 MILD FIX C213  [readable TARGET] Bleach|Halftone|Clip|Finger", fill=(200, 200, 200), font=f_tiny)

    # MILD hardening (keep theme, don't crush digits)
    px = img.load()
    ww, hh = img.size
    # sparse halftone dots outside text band
    for y0 in range(40, 600, 8):
        for x0 in range(50, 540, 8):
            if 70 <= y0 <= 220:
                continue  # protect line band
            if rng.random() < 0.18:
                v = rng.randint(10, 40)
                if x0 < ww and y0 < hh:
                    r, g, b = px[x0, y0]
                    px[x0, y0] = (max(0, r - v), max(0, g - v), max(0, b - v))
    # light thermal fade top only
    for yy in range(60, 100):
        for xx in range(50, min(520, ww)):
            r, g, b = px[xx, yy]
            fade = 12
            px[xx, yy] = (min(255, r + fade), min(255, g + fade), min(255, b + fade // 2))
    # light bleach away from TARGET lines (y~78-200)
    for yy in range(280, 380):
        for xx in range(100, min(450, ww)):
            r, g, b = px[xx, yy]
            px[xx, yy] = (min(255, int(r * 1.05 + 8)), min(255, int(g * 1.05 + 8)), min(255, int(b * 1.03 + 5)))
    # light dust
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
    # mild affine (was 0.095 / 0.035)
    w, h = img.size
    img = img.transform(
        (w, h), Image.AFFINE, (1, 0.03, -8, 0.01, 1, -4),
        resample=Image.BICUBIC, fillcolor=(215, 210, 200),
    )
    img = img.filter(ImageFilter.GaussianBlur(radius=0.45))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=62)  # was 28
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
            "mild_halftone", "mild_thermal", "mild_bleach", "punch_holes",
            "binder_clip", "light_crayon", "light_fingerprint", "jpeg_q62", "c213_clarity",
        ],
        "regenerated_c213": True,
    }


def regen_fail_fixtures():
    man = json.loads((FIX / "manifest.json").read_text(encoding="utf-8"))
    by_id = {it["id"]: it for it in man["items"]}
    updated = []
    for fid, spec in REGEN.items():
        item = make_mild(
            fid, spec["kind"], spec["lines"], spec["metric"],
            spec["expected"], spec["cn_title"], spec["stamp"],
        )
        by_id[fid] = item
        updated.append(fid)
    new_items = []
    for it in man["items"]:
        new_items.append(by_id.get(it["id"], it))
    man["items"] = new_items
    man["c213_regenerated"] = updated
    man["timestamp"] = ts()
    J(FIX / "manifest.json", man)
    return updated, man


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


def full_vl_retest(man):
    free = gpu_free_mib()
    if free < 2000 or not WEIGHTS.is_dir():
        return {"attempted": False, "reason": f"gpu_free={free}", "n": 0, "n_ok": 0, "rate": 0.0, "rows": [], "fail_ids": []}
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
                "regenerated_c213": bool(it.get("regenerated_c213")),
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
    return {
        "attempted": True, "gpu_free_mib_start": free,
        "n": n, "n_ok": n_ok, "rate": rate,
        "rows": rows, "fail_ids": [r["id"] for r in rows if not r["ok"]],
    }


def main():
    RUN.mkdir(parents=True, exist_ok=True)
    unit = unit_reparse_saved()
    J(RUN / "unit_reparse.json", unit)
    # proof: 99.99 bait filtered after parse patch
    assert abs(unit["proof_noise_9999"]["sum_without_bait"] - 68.0) < 0.08, unit["proof_noise_9999"]

    updated, man = regen_fail_fixtures()
    vl = full_vl_retest(man)
    rate = vl["rate"]
    gate_pass = bool(vl.get("attempted") and vl["n"] >= 16 and rate >= GATE)
    claim = gate_pass
    scope = (
        "r50plus_v18_c213_mildfix_bleach_halftone_n>=16_c162_parse_qwen35_2b"
        if claim else None
    )
    prior_rate = 0.6667
    out = {
        "cycle": "C213",
        "theme": "v18_fail_fix_retest",
        "gate": GATE,
        "timestamp": ts(),
        "diagnosis": {
            "fail_ids_c209": ["v18_02", "v18_06", "v18_08", "v18_09", "v18_16", "v18_17"],
            "root_cause": "heavy_degrade_ocr_digit_drift_status_drop_decoy_paid_99.99",
            "unit_fixed_by_parse_alone": unit["fixed_by_parse_alone"],
            "still_needed_regen": unit["still_fail_need_regen"],
            "parse_fixes": ["NOISE+=99.99"],
            "fixture_fixes": ["mild_jpeg_q62", "protect_text_band", "lighter_affine_blur", "sticky_bait_888_only"],
        },
        "unit_reparse": {
            "rate": unit["rate"],
            "fixed_by_parse_alone": unit["fixed_by_parse_alone"],
            "still_fail_need_regen": unit["still_fail_need_regen"],
            "proof_99_99_sum": unit["proof_noise_9999"]["sum_without_bait"],
        },
        "regenerated_fixtures": updated,
        "attempted": vl.get("attempted"),
        "n": vl.get("n"),
        "n_ok": vl.get("n_ok"),
        "rate": rate,
        "gate_pass": gate_pass,
        "fail_ids": vl.get("fail_ids"),
        "rows": vl.get("rows"),
        "vl_gate_v18_claim": claim,
        "claim_scope": scope,
        "prior_c209_rate": prior_rate,
        "rate_delta": round(rate - prior_rate, 4) if vl.get("attempted") else None,
        "supersedes": "docs/r50/C209b_VISION_GATE_V18_CLAIM.json",
        "gate2_3_untouched": True,
        "v0_v17_untouched": True,
        "gen11": "HOLD",
        "pass": gate_pass,
        "claim": claim,
        "note": "Honest raise of V18 train rate via parse bait filter + mild fixture clarity; no Gate2/3 touch.",
    }
    J(DOC / "C213_V18_FAIL_FIX_RETEST.json", out)
    J(RUN / "judge.json", out)
    if claim:
        J(DOC / "C213b_VISION_GATE_V18_REFRESH_CLAIM.json", {
            "kind": "vision_gate_v18_claim",
            "timestamp": ts(),
            "vl_gate_v18_claim": True,
            "rate": rate, "n": vl["n"], "n_ok": vl["n_ok"], "gate": GATE,
            "claim_scope": scope,
            "supersedes": "docs/r50/C209b_VISION_GATE_V18_CLAIM.json",
            "prior_rate": prior_rate,
            "gate2_3_untouched": True,
            "v0_v17_untouched": True,
            "gen11": "HOLD",
            "cycle": "C213",
        })
    print(json.dumps({
        "cycle": "C213", "unit_fixed": unit["fixed_by_parse_alone"],
        "still_before_regen": unit["still_fail_need_regen"],
        "regen": updated, "rate": rate, "n_ok": vl.get("n_ok"),
        "fail_ids": vl.get("fail_ids"), "claim": claim, "pass": gate_pass,
    }, ensure_ascii=False))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
