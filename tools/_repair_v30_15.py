# -*- coding: utf-8 -*-
"""Repair v30_15: clearer cn_title + redundant English body; re-render; single-item VL retest."""
from __future__ import annotations
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
SCR = ROOT / "scripts" / "c284_vision_v30_design_and_batch.py"
FIX = ROOT / "evo" / "office" / "fixtures" / "vision_images_v30"
DOC = ROOT / "docs" / "r50"
WEIGHTS = ROOT / "models/Qwen3.5-2B"

NEW_LINES = [
    "INKJET FADE STACK V30",
    "x paid 58.00 usd",
    "y paid 61.00 usd",
    "z open 20.00 usd",
    "TOTAL PAID TARGET 119.00",
]
NEW_CN = "喷墨叠页单"  # shorter, less OCR bait


def main():
    text = SCR.read_text(encoding="utf-8")
    pat = re.compile(
        r'\("v30_15",\s*"inkjet_stack",\s*"paid_total",\s*119\.0,\s*'
        r'\[[^\]]+\],\s*"[^"]*",\s*"[^"]*"\)',
        re.S,
    )
    new_tuple = (
        '("v30_15", "inkjet_stack", "paid_total", 119.0,\n'
        '     ["INKJET FADE STACK V30", "x paid 58.00 usd", "y paid 61.00 usd", '
        '"z open 20.00 usd", "TOTAL PAID TARGET 119.00"],\n'
        '     "喷墨叠页单", "RECV")'
    )
    m = pat.search(text)
    if not m:
        raise SystemExit("v30_15 SPECS not found")
    SCR.write_text(text[: m.start()] + new_tuple + text[m.end() :], encoding="utf-8")
    print("patched SPECS")

    import importlib.util
    spec = importlib.util.spec_from_file_location("c284", SCR)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    item = mod.make_fixture(
        "v30_15", "inkjet_stack", NEW_LINES, "paid_total", 119.0, NEW_CN, "RECV",
    )
    print("rerendered", item["path"])

    man_path = FIX / "manifest.json"
    man = json.loads(man_path.read_text(encoding="utf-8"))
    for i, it in enumerate(man["items"]):
        if it["id"] == "v30_15":
            man["items"][i] = item
            break
    else:
        raise SystemExit("v30_15 missing")
    man["note"] = (man.get("note") or "") + "; repaired v30_15 cn_title shorter"
    man_path.write_text(json.dumps(man, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    from evo.office.vision_backend import RealVlBackend
    from evo.office.vision_ocr import ocr_image
    from evo.office.vision_metric_parse import parse_metric
    backend = RealVlBackend(WEIGHTS, max_new_tokens=200)
    ocr = ocr_image(ROOT / item["path"], prefer="vl", vl_backend=backend)
    text_ocr = re.sub(r"<think>[\s\S]*?</think>", " ", ocr.get("text") or "")
    text_ocr = re.sub(r"\s+", " ", text_ocr).strip()
    got, atom_ok = parse_metric(text_ocr, "paid_total", 119.0)
    keys = re.findall(r"\d+\.?\d*", " ".join(NEW_LINES))
    t = text_ocr.lower().replace(" ", "")
    hit = sum(1 for k in keys[:5] if k.replace(".00", "") in t or k in t)
    ocr_ok = hit >= max(2, min(3, len(keys[:5]) // 2))
    ok = bool(ocr_ok and atom_ok)
    print(json.dumps({"ocr_ok": ocr_ok, "atom_ok": bool(atom_ok), "got": got, "ok": ok, "preview": text_ocr[:240]}, ensure_ascii=False))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
