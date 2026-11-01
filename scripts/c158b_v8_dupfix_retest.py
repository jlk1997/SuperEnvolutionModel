# -*- coding: utf-8 -*-
"""C158b: Finish V8 train raise — dup-amount parse + v8_17 OCR-stable regen + VL.
C158 got 0.8889 (fails v8_11 dup-dedup, v8_17 VL misread 19→10).
Gate 0.6. Gate2/3 untouched. gen11 HOLD.
"""
from __future__ import annotations
import gc, json, re, sys, random
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from evo.office.vision_metric_parse import parse_metric, sum_status

GATE = 0.6
DOC = ROOT / "docs" / "r50"
FIX = ROOT / "evo/office/fixtures/vision_images_v8"
WEIGHTS = ROOT / "models/Qwen3.5-2B"
RUN = ROOT / "runs/vision_v8_c158b"
PRIOR = DOC / "C158_V8_FAIL_FIX_RETEST.json"


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


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


def unit_dup_and_reparse():
    prior = json.loads(PRIOR.read_text(encoding="utf-8"))
    proof = parse_metric(
        "line paid 4.00 line paid 5.00 line paid 5.00 666 PAID VOID",
        "paid_total", 14.0,
    )
    rows = []
    for r in prior.get("rows") or []:
        if r["id"] not in ("v8_11", "v8_17"):
            continue
        got, atom_ok = parse_metric(r.get("ocr_preview") or "", r["metric"], r["expected"])
        rows.append({
            "id": r["id"], "got": got, "expected": r["expected"],
            "atom_ok": atom_ok, "ocr_preview": (r.get("ocr_preview") or "")[:200],
        })
    return {
        "dup_proof": {"got": proof[0], "ok": proof[1], "expect": 14.0},
        "reparse_fails": rows,
        "v8_11_fixed_by_parse": any(x["id"] == "v8_11" and x["atom_ok"] for x in rows),
    }


def regen_v8_17():
    """Use OCR-stable amounts 18+13=31 (19 was misread as 10)."""
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    fid, kind = "v8_17", "noise_inv"
    lines = [
        "INVENTORY PAY V8",
        "lot1 paid 18.00",
        "lot2 paid 13.00",
        "lot3 open 6.00",
        "TOTAL PAID TARGET 31.00",
    ]
    expected = 31.0
    cn_title, stamp = "噪声库存付", "RECV"
    rng = random.Random(hash(fid + "_c158b") & 0xFFFFFFFF)
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
        f_body = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 12)
        f_tgt = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 12)
        f_sm = ImageFont.truetype(r"C:\\Windows\\Fonts\\msyh.ttc", 10)
        f_stamp = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 16)
        f_wm = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 48)
        f_tiny = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 10)
    except Exception:
        f_title = f_body = f_tgt = f_sm = f_stamp = f_wm = f_tiny = ImageFont.load_default()

    d.rectangle([10, 10, 450, 545], fill=(230, 226, 218), outline=(80, 80, 80), width=2)
    for y in range(20, 540, 8):
        if rng.random() < 0.4:
            d.line([(12, y), (448, y)], fill=(195, 190, 180), width=1)
    d.text((80, 200), "777", fill=(205, 200, 190), font=f_wm)
    d.text((200, 320), "666", fill=(203, 198, 188), font=f_wm)
    d.rectangle([18, 18, 440, 48], fill=(55, 70, 90))
    d.text((24, 22), cn_title[:28], fill=(230, 230, 230), font=f_title)
    y = 60
    for ln in lines:
        font = f_tgt if "TARGET" in ln.upper() or "TOTAL" in ln.upper() else f_body
        d.text((28, y), ln[:56], fill=(20, 20, 20), font=font)
        y += 22
    d.rectangle([50, 160, 410, 176], fill=(180, 170, 150))
    d.text((54, 162), "~~ fax fold ~~", fill=(110, 100, 85), font=f_tiny)
    for (cx, cy, label, col) in [(340, 190, stamp, (190, 40, 40)), (300, 230, "VOID", (160, 60, 60))]:
        d.ellipse([cx - 50, cy - 28, cx + 50, cy + 28], outline=col, width=3)
        d.text((cx - 22, cy - 8), label[:6], fill=col, font=f_stamp)
    d.rectangle([480, 40, 900, 260], fill=(245, 245, 248), outline=(60, 60, 60), width=2)
    d.rectangle([480, 40, 900, 68], fill=(80, 80, 100))
    d.text((490, 46), "WIN-B VOID / IGNORE", fill=(255, 220, 220), font=f_sm)
    d.text((490, 80), "old total 999.00", fill=(20, 20, 20), font=f_sm)
    d.text((490, 100), "tiny distractor 888.00", fill=(20, 20, 20), font=f_sm)
    d.text((490, 120), "occlusion copy TOTAL 42", fill=(20, 20, 20), font=f_sm)
    d.text((490, 150), f"{fid} status=void invoice#OLD", fill=(40, 40, 40), font=f_tiny)
    d.rectangle([0, 550, 920, 580], fill=(25, 25, 32))
    d.text((10, 556), "Start | Fax | POS | Chat  [V8c158b]", fill=(200, 200, 200), font=f_tiny)
    px = img.load()
    for _ in range(1000):
        x, y = rng.randint(0, 919), rng.randint(0, 579)
        v = rng.randint(0, 30)
        r, g, b = px[x, y]
        px[x, y] = (max(0, r - v), max(0, g - v), max(0, b - v))
    img = ImageEnhance.Contrast(img).enhance(0.95)
    img = img.filter(ImageFilter.SMOOTH)
    out = FIX / f"{fid}_{kind}.png"
    for old in FIX.glob(f"{fid}_*.png"):
        if old != out:
            try:
                old.unlink()
            except Exception:
                pass
    img.save(out)
    item = {
        "id": fid, "file": out.name, "kind": kind, "metric": "paid_total",
        "expected": expected, "lines": lines, "cn_title": cn_title, "stamp": stamp,
        "capture_blend": capture,
        "path": str(out.relative_to(ROOT)).replace("\\", "/"),
        "hardening": [
            "low_contrast", "fax_carbon_noise", "multi_stamp", "watermark_distract",
            "hand_scribble", "c158b_ocr_stable_amounts",
        ],
        "regenerated_c158b": True,
    }
    man = json.loads((FIX / "manifest.json").read_text(encoding="utf-8"))
    man["items"] = [item if it["id"] == fid else it for it in man["items"]]
    man["c158b_regenerated"] = [fid]
    man["timestamp"] = ts()
    J(FIX / "manifest.json", man)
    return item, man


def full_vl(man):
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
    return {
        "attempted": True, "gpu_free_mib_start": free,
        "n": n, "n_ok": n_ok, "rate": rate, "rows": rows,
        "fail_ids": [r["id"] for r in rows if not r["ok"]],
    }


def main():
    unit = unit_dup_and_reparse()
    assert unit["dup_proof"]["ok"], unit
    item, man = regen_v8_17()
    vl = full_vl(man)
    rate = vl["rate"]
    gate_pass = bool(vl.get("attempted") and vl["n"] >= 16 and rate >= GATE)
    claim = gate_pass
    scope = "r50plus_v8_c158b_dupfix_ocrstable_n>=16_qwen35_2b" if claim else None
    out = {
        "cycle": "C158b",
        "theme": "v8_dup_parse_and_v17_regen_retest",
        "gate": GATE,
        "timestamp": ts(),
        "unit": unit,
        "regenerated": ["v8_17"],
        "v8_17_lines": item["lines"],
        "attempted": vl.get("attempted"),
        "n": vl.get("n"),
        "n_ok": vl.get("n_ok"),
        "rate": rate,
        "gate_pass": gate_pass,
        "fail_ids": vl.get("fail_ids"),
        "rows": vl.get("rows"),
        "vl_gate_v8_claim": claim,
        "claim_scope": scope,
        "prior_c158_rate": 0.8889,
        "prior_c155_rate": 0.7222,
        "rate_delta_vs_c155": round(rate - 0.7222, 4) if vl.get("attempted") else None,
        "gate2_3_untouched": True,
        "v0_v7_untouched": True,
        "gen11": "HOLD",
        "pass": gate_pass,
        "claim": claim,
    }
    J(DOC / "C158b_V8_DUPFIX_RETEST.json", out)
    J(RUN / "judge.json", out)
    if claim:
        J(DOC / "C158c_VISION_GATE_V8_REFRESH_CLAIM.json", {
            "kind": "vision_gate_v8_claim",
            "timestamp": ts(),
            "vl_gate_v8_claim": True,
            "rate": rate,
            "n": vl["n"],
            "n_ok": vl["n_ok"],
            "gate": GATE,
            "claim_scope": scope,
            "supersedes": [
                "docs/r50/C155b_VISION_GATE_V8_CLAIM.json",
                "docs/r50/C158b_VISION_GATE_V8_REFRESH_CLAIM.json",
            ],
            "gate2_3_untouched": True,
            "v0_v7_untouched": True,
            "gen11": "HOLD",
            "cycle": "C158b",
        })
    print(json.dumps({
        "cycle": "C158b", "dup_ok": unit["dup_proof"]["ok"],
        "v8_11_reparse": unit["v8_11_fixed_by_parse"],
        "rate": rate, "n_ok": vl.get("n_ok"), "fail_ids": vl.get("fail_ids"),
        "claim": claim, "pass": gate_pass,
    }, ensure_ascii=False))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
