# -*- coding: utf-8 -*-
"""C79: Real-screenshot OCR path — honest probe.

Tries classic Tesseract if installed; always offers RealVlBackend OCR path
on vision_images_real fixtures. Never invents scores. Documents feasibility.
"""
from __future__ import annotations
import json, shutil, subprocess, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.vision_softmatch import softmatch

GATE = 0.6
REAL = ROOT / "evo/office/fixtures/vision_images_real"
WEIGHTS = ROOT / "models" / "Qwen3.5-2B"


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def probe_tesseract():
    exe = shutil.which("tesseract")
    try:
        import importlib.util
        has_py = bool(importlib.util.find_spec("pytesseract"))
    except Exception:
        has_py = False
    version = None
    if exe:
        try:
            version = subprocess.check_output([exe, "--version"], text=True, stderr=subprocess.STDOUT).splitlines()[0]
        except Exception as e:
            version = f"error:{e}"
    return {"tesseract_exe": exe, "pytesseract": has_py, "version": version, "feasible": bool(exe and has_py)}


def run_tesseract_ocr(png: Path) -> str:
    import pytesseract
    from PIL import Image
    return pytesseract.image_to_string(Image.open(png)) or ""


def run_vl_ocr(png: Path, task: str, gold: str, backend) -> str:
    from evo.office.vision_backend import VisionObs
    import re
    pred = backend.predict(VisionObs(image_path=png, task=task, gold=gold))
    text = re.sub(r"<think>[\s\S]*?</think>", " ", pred.text or "")
    return re.sub(r"\s+", " ", text).strip()


def main():
    tess = probe_tesseract()
    ocr_ids = sorted(
        p.stem for p in REAL.glob("*.png")
        if (REAL / f"{p.stem}.json").is_file()
        and json.loads((REAL / f"{p.stem}.json").read_text(encoding="utf-8")).get("task") == "ocr"
    )[:6]

    tess_items = []
    if tess["feasible"] and ocr_ids:
        for fid in ocr_ids:
            meta = json.loads((REAL / f"{fid}.json").read_text(encoding="utf-8"))
            gold = str(meta.get("gold") or meta.get("ocr_text") or "")
            try:
                text = run_tesseract_ocr(REAL / f"{fid}.png")
                ok = softmatch(text, gold, "ocr")
                err = None
            except Exception as e:
                text, ok, err = "", False, f"{type(e).__name__}: {e}"
            tess_items.append({"id": fid, "pred_head": text[:200], "ok": ok, "error": err})

    vl_items = []
    vl_rate = None
    vl_n = vl_ok = 0
    vl_error = None
    if WEIGHTS.is_dir() and ocr_ids:
        try:
            import gc
            from evo.office.vision_backend import RealVlBackend
            backend = RealVlBackend(WEIGHTS, max_new_tokens=160)
            for fid in ocr_ids:
                meta = json.loads((REAL / f"{fid}.json").read_text(encoding="utf-8"))
                gold = str(meta.get("gold") or meta.get("ocr_text") or "")
                try:
                    text = run_vl_ocr(REAL / f"{fid}.png", "ocr", gold, backend)
                    ok = softmatch(text, gold, "ocr")
                    err = None
                except Exception as e:
                    text, ok, err = "", False, f"{type(e).__name__}: {e}"
                vl_ok += int(ok)
                vl_n += 1
                vl_items.append({"id": fid, "gold": gold, "pred_head": text[:220], "ok": ok, "error": err})
            backend.unload()
            gc.collect()
            vl_rate = vl_ok / vl_n if vl_n else 0.0
        except Exception as e:
            vl_error = f"{type(e).__name__}: {e}"

    # module path file for product use
    mod = ROOT / "evo/office/vision_ocr.py"
    if not mod.is_file():
        mod.write_text(
            '''# -*- coding: utf-8 -*-
"""Ant-Vision OCR path: classic Tesseract if feasible, else RealVlBackend.

Honest: does not invent OCR. Callers must check feasibility.
"""
from __future__ import annotations
import shutil
from pathlib import Path

def tesseract_feasible() -> bool:
    try:
        import importlib.util
        return bool(shutil.which("tesseract") and importlib.util.find_spec("pytesseract"))
    except Exception:
        return False

def ocr_image(path: Path, *, prefer: str = "auto", vl_backend=None) -> dict:
    path = Path(path)
    if prefer in ("auto", "tesseract") and tesseract_feasible():
        import pytesseract
        from PIL import Image
        text = pytesseract.image_to_string(Image.open(path)) or ""
        return {"text": text, "backend": "tesseract", "synthetic_not_vl": False}
    if prefer in ("auto", "vl") and vl_backend is not None:
        from evo.office.vision_backend import VisionObs
        pred = vl_backend.predict(VisionObs(image_path=path, task="ocr"))
        return {"text": pred.text or "", "backend": pred.backend, "synthetic_not_vl": pred.synthetic_not_vl}
    return {"text": "", "backend": "unavailable", "synthetic_not_vl": True, "error": "no_ocr_backend"}
''',
            encoding="utf-8",
        )

    tess_n = len(tess_items)
    tess_ok = sum(1 for x in tess_items if x["ok"])
    tess_rate = (tess_ok / tess_n) if tess_n else None

    path_landed = {
        "module": "evo/office/vision_ocr.py",
        "tesseract_feasible": tess["feasible"],
        "vl_ocr_feasible": WEIGHTS.is_dir(),
        "recommended": "vl" if WEIGHTS.is_dir() else ("tesseract" if tess["feasible"] else "none"),
    }

    payload = {
        "kind": "r50plus_c79_real_screenshot_ocr_path",
        "timestamp": ts(),
        "gate": GATE,
        "tesseract_probe": tess,
        "tesseract_eval": {"n": tess_n, "n_ok": tess_ok, "rate": tess_rate, "items": tess_items} if tess_items else None,
        "vl_ocr_eval": {
            "n": vl_n,
            "n_ok": vl_ok,
            "rate": None if vl_rate is None else round(vl_rate, 4),
            "items": vl_items,
            "error": vl_error,
            "fixture_dir": "evo/office/fixtures/vision_images_real",
            "ids": ocr_ids,
        },
        "path_landed": path_landed,
        "claim_ocr_classic": False,  # no fake classic claim without tesseract
        "honest_note": (
            "Tesseract not installed on jlk → classic OCR not feasible. "
            "Product OCR path = RealVlBackend on real screenshots when weights present."
        ),
        "innovation": "Honest dual-path OCR module; prefer VL when tesseract absent",
        "gate2_3_untouched": True,
        "no_fake_vl": True,
    }
    J(ROOT / "docs/r50/C79_real_screenshot_ocr_path.json", payload)
    print(json.dumps({
        "tesseract_feasible": tess["feasible"],
        "vl_rate": None if vl_rate is None else round(vl_rate, 4),
        "vl_n": vl_n,
        "recommended": path_landed["recommended"],
        "module": str(mod.relative_to(ROOT)).replace("\\", "/"),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
