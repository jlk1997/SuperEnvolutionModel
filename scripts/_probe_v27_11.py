# -*- coding: utf-8 -*-
"""Quick single-case VL probe for repaired v27_11."""
from __future__ import annotations
import gc, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from evo.office.vision_metric_parse import parse_metric

FIX = ROOT / "evo/office/fixtures/vision_images_v27"
WEIGHTS = ROOT / "models/Qwen3.5-2B"


def soft_ocr_ok(text, lines):
    t = (text or "").lower().replace(" ", "")
    keys = re.findall(r"\d+\.?\d*", " ".join(lines))
    if not t:
        return False
    hit = sum(1 for k in keys[:5] if k.replace(".00", "") in t or k in t)
    return hit >= max(2, min(3, len(keys[:5]) // 2))


def main():
    man = json.loads((FIX / "manifest.json").read_text(encoding="utf-8"))
    it = next(x for x in man["items"] if x["id"] == "v27_11")
    from evo.office.vision_backend import RealVlBackend
    from evo.office.vision_ocr import ocr_image
    backend = RealVlBackend(WEIGHTS, max_new_tokens=200)
    try:
        ocr = ocr_image(ROOT / it["path"], prefer="vl", vl_backend=backend)
        text = re.sub(r"<think>[\s\S]*?</think>", " ", ocr.get("text") or "")
        text = re.sub(r"\s+", " ", text).strip()
        ocr_ok = soft_ocr_ok(text, it["lines"])
        got, atom_ok = parse_metric(text, it["metric"], it["expected"])
        ok = bool(ocr_ok and atom_ok)
        out = {
            "id": it["id"], "ok": ok, "ocr_ok": ocr_ok, "atom_ok": atom_ok,
            "got": got, "expected": it["expected"], "ocr_preview": text[:400],
            "lines": it["lines"], "cn_title": it.get("cn_title"),
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
        (ROOT / "docs/r50/C272a_V27_11_PROBE.json").write_text(
            json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        return 0 if ok else 1
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


if __name__ == "__main__":
    raise SystemExit(main())
