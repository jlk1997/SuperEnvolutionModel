# -*- coding: utf-8 -*-
"""C94: Real desktop screenshot capture path (PIL ImageGrab), not solid-draw.
Cheap probe: capture → save → optional VL OCR smoke (1 crop). Honest.
"""
from __future__ import annotations
import json, sys, traceback
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

GATE = 0.6
RUN = ROOT / "runs" / "desktop_capture_c94"
DOC = ROOT / "docs" / "r50"
WEIGHTS = ROOT / "models" / "Qwen3.5-2B"


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    if RUN.exists():
        import shutil
        shutil.rmtree(RUN)
    RUN.mkdir(parents=True)
    out = {
        "cycle": "C94",
        "theme": "desktop_screenshot_capture",
        "gate": GATE,
        "timestamp": ts(),
        "claim": False,
    }
    try:
        from PIL import ImageGrab, Image, ImageDraw, ImageFont
        # Capture primary screen (may be large)
        shot = ImageGrab.grab(all_screens=False)
        full = RUN / "desktop_full.png"
        # Downscale for storage
        w, h = shot.size
        max_w = 1280
        if w > max_w:
            nh = int(h * max_w / w)
            shot_s = shot.resize((max_w, nh))
        else:
            shot_s = shot
        shot_s.save(full)
        out["capture_ok"] = True
        out["size"] = [w, h]
        out["saved"] = str(full.relative_to(ROOT)).replace("\\", "/")
        # Also create a labeled office window mock overlay for VL readability check
        # Crop top-left 800x500 region as "active window" proxy
        crop = shot.crop((0, 0, min(800, w), min(500, h)))
        crop_path = RUN / "desktop_crop.png"
        crop.save(crop_path)
        out["crop"] = str(crop_path.relative_to(ROOT)).replace("\\", "/")
        # Draw a high-contrast notepad-like overlay image as second artifact (still real capture + label)
        overlay = crop.copy()
        d = ImageDraw.Draw(overlay)
        try:
            f = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 20)
        except Exception:
            f = ImageFont.load_default()
        d.rectangle([10, 10, 780, 80], fill=(255, 255, 200), outline=(0, 0, 0))
        d.text((20, 30), "ANT_CAPTURE_PROBE C94", fill=(0, 0, 0), font=f)
        ov_path = RUN / "desktop_crop_labeled.png"
        overlay.save(ov_path)
        out["labeled"] = str(ov_path.relative_to(ROOT)).replace("\\", "/")

        # Optional VL OCR on labeled crop — cheap 1-shot
        vl = {"attempted": False}
        if WEIGHTS.is_dir():
            try:
                from evo.office.vision_backend import RealVlBackend, VisionObs
                from evo.office.vision_ocr import ocr_image
                backend = RealVlBackend(WEIGHTS, max_new_tokens=64)
                ocr = ocr_image(ov_path, prefer="vl", vl_backend=backend)
                text = (ocr.get("text") or "")[:300]
                hit = "ANT_CAPTURE" in text.upper() or "C94" in text.upper() or "CAPTURE" in text.upper()
                vl = {
                    "attempted": True,
                    "text": text,
                    "hit_probe_label": hit,
                    "backend": "real_vl",
                    "synthetic_not_vl": False,
                }
            except Exception as e:
                vl = {"attempted": True, "error": f"{type(e).__name__}:{e}", "trace": traceback.format_exc()[-500:]}
        out["vl_ocr"] = vl
        out["pass"] = bool(out.get("capture_ok"))
        out["note"] = (
            "Real ImageGrab path works. Overlay label aids OCR probe; full desktop is real pixels not solid-draw fixtures."
        )
    except Exception as e:
        out["capture_ok"] = False
        out["pass"] = False
        out["error"] = f"{type(e).__name__}:{e}"
        out["trace"] = traceback.format_exc()[-800:]

    J(DOC / "C94_DESKTOP_CAPTURE.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps({k: out.get(k) for k in ('cycle', 'capture_ok', 'pass')}, ensure_ascii=True)); print('vl_hit', (out.get('vl_ocr') or {}).get('hit_probe_label'), 'attempted', (out.get('vl_ocr') or {}).get('attempted'))
    return 0 if out.get("pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())

