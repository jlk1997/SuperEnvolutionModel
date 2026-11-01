# -*- coding: utf-8 -*-
"""C168: Real desktop multi-window office pressure (ImageGrab batches).
Capture real desktop N times, overlay 3 office windows per batch, VL OCR+parse.
Gate 0.6. Honest. Gate2/3 untouched. gen11 HOLD.
"""
from __future__ import annotations
import gc, json, re, shutil, sys, traceback
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from evo.office.vision_metric_parse import parse_metric

GATE = 0.6
DOC = ROOT / "docs" / "r50"
RUN = ROOT / "runs" / "desktop_multiwin_c168"
WEIGHTS = ROOT / "models" / "Qwen3.5-2B"

BATCHES = [
    ("b01", "paid_total", 27.5, ["MW OFFICE B01", "a paid 12.00", "b paid 15.50", "c open 4.00", "TOTAL PAID TARGET 27.50"]),
    ("b02", "paid_total", 19.25, ["MW OFFICE B02", "x paid 9.00", "y paid 10.25", "z open 2.50", "TOTAL PAID TARGET 19.25"]),
    ("b03", "qty_sum", 22.0, ["MW WH B03", "SKU1 qty 14 ok", "SKU2 qty 5 hold", "SKU3 qty 8 ok", "qty_sum TARGET 22"]),
    ("b04", "paid_total", 0.0, ["MW OPEN B04", "p 11.00 open", "q 13.00 open", "paid_total TARGET 0.00"]),
    ("b05", "refund_done", 11.5, ["MW REFUND B05", "r1 5.00 done", "r2 6.50 done", "r3 3.00 open", "refund_done TARGET 11.50"]),
    ("b06", "paid_total", 33.0, ["MW PO B06", "itemA paid 18.00", "itemB paid 15.00", "itemC open 6.00", "TOTAL PAID TARGET 33.00"]),
]


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


def build_panel(shot, bid, lines):
    from PIL import Image, ImageDraw, ImageFont
    w, h = shot.size
    crop = shot.crop((0, 0, min(1100, w), min(700, h))).convert("RGB").resize((960, 580))
    washed = Image.blend(crop, Image.new("RGB", (960, 580), (255, 255, 255)), 0.55)
    d = ImageDraw.Draw(washed)
    try:
        f = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 14)
        f2 = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 13)
        fsm = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 11)
        ft = ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 12)
    except Exception:
        f = f2 = fsm = ft = ImageFont.load_default()
    d.rectangle([20, 20, 480, 360], fill=(235, 230, 220), outline=(30, 30, 30), width=2)
    d.rectangle([20, 20, 480, 50], fill=(40, 55, 75))
    d.text((28, 26), f"WIN-A {bid}", fill=(240, 240, 240), font=ft)
    y = 60
    for ln in lines:
        font = f2 if "TARGET" in ln.upper() or "TOTAL" in ln.upper() else f
        d.text((30, y), ln[:48], fill=(20, 20, 20), font=font)
        y += 20
    d.rectangle([520, 40, 920, 280], fill=(250, 250, 255), outline=(50, 50, 80), width=2)
    d.rectangle([520, 40, 920, 68], fill=(70, 80, 120))
    d.text((530, 46), "WIN-B CHAT bait", fill=(255, 220, 220), font=fsm)
    d.text((530, 80), "ignore total 888.00", fill=(20, 20, 20), font=fsm)
    d.text((530, 105), "ignore fee 777.00", fill=(20, 20, 20), font=fsm)
    d.text((530, 130), "not the office panel", fill=(20, 20, 20), font=fsm)
    d.rectangle([500, 300, 920, 540], fill=(245, 255, 245), outline=(40, 90, 40), width=2)
    d.rectangle([500, 300, 920, 328], fill=(40, 100, 50))
    d.text((510, 306), "WIN-C CAL bait", fill=(230, 255, 230), font=fsm)
    d.text((510, 340), "event cost 666.00", fill=(20, 20, 20), font=fsm)
    d.text((510, 365), "travel 555.00 open", fill=(20, 20, 20), font=fsm)
    d.rectangle([0, 550, 960, 580], fill=(20, 20, 28))
    d.text((10, 556), "MultiWin Desktop Pressure [C168]", fill=(200, 200, 200), font=fsm)
    return washed


def main():
    if RUN.exists():
        shutil.rmtree(RUN)
    RUN.mkdir(parents=True)
    free = gpu_free_mib()
    out = {
        "cycle": "C168",
        "theme": "desktop_multiwindow_office_pressure",
        "gate": GATE,
        "timestamp": ts(),
        "gpu_free_mib_start": free,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "claim": False,
    }
    try:
        from PIL import ImageGrab
        shots = []
        for i in range(len(BATCHES)):
            shot = ImageGrab.grab(all_screens=False)
            shots.append(shot)
        out["capture_ok"] = True
        out["n_grabs"] = len(shots)
        out["size"] = list(shots[0].size)

        vl_ready = free >= 2000 and WEIGHTS.is_dir()
        backend = None
        rows, n_ok = [], 0
        if vl_ready:
            from evo.office.vision_backend import RealVlBackend
            from evo.office.vision_ocr import ocr_image
            backend = RealVlBackend(WEIGHTS, max_new_tokens=180)
        try:
            for idx, (bid, metric, expected, lines) in enumerate(BATCHES):
                shot = shots[idx % len(shots)]
                panel = build_panel(shot, bid, lines)
                png = RUN / f"{bid}_multiwin.png"
                panel.save(png)
                row = {
                    "id": bid, "metric": metric, "expected": expected,
                    "path": str(png.relative_to(ROOT)).replace("\\", "/"),
                }
                if backend is not None:
                    ocr = ocr_image(png, prefer="vl", vl_backend=backend)
                    text = re.sub(r"<think>[\s\S]*?</think>", " ", ocr.get("text") or "")
                    text = re.sub(r"\s+", " ", text).strip()
                    ocr_ok = soft_ocr_ok(text, lines)
                    got, atom_ok = parse_metric(text, metric, expected)
                    ok = bool(ocr_ok and atom_ok)
                    n_ok += int(ok)
                    row.update({
                        "ocr_ok": ocr_ok, "atom_ok": atom_ok, "ok": ok,
                        "got": got, "ocr_preview": text[:300],
                    })
                else:
                    row.update({"ocr_ok": False, "atom_ok": False, "ok": False, "reason": "no_vl"})
                rows.append(row)
        finally:
            if backend is not None:
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
        rate = round(n_ok / n, 4) if n and vl_ready else 0.0
        gate_pass = bool(out.get("capture_ok")) and vl_ready and rate >= GATE and n >= 6
        out.update({
            "vl_attempted": vl_ready,
            "n": n, "n_ok": n_ok, "rate": rate,
            "rows": rows,
            "gate_pass": gate_pass,
            "pass": gate_pass,
            "note": "Real ImageGrab multi-window batches with WIN-A office + WIN-B/C bait. Claim=False (pressure board, not VL gate).",
        })
    except Exception as e:
        out["pass"] = False
        out["error"] = f"{type(e).__name__}:{e}"
        out["trace"] = traceback.format_exc()[-800:]
    J(DOC / "C168_DESKTOP_MULTIWIN_PRESSURE.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps({
        "cycle": "C168", "capture": out.get("capture_ok"), "rate": out.get("rate"),
        "n_ok": out.get("n_ok"), "n": out.get("n"), "pass": out.get("pass"),
    }, ensure_ascii=False))
    return 0 if out.get("pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
