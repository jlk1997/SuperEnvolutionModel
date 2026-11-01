# -*- coding: utf-8 -*-
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
