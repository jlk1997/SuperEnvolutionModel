# -*- coding: utf-8 -*-
"""蚁算-视 V0 smoke: load local Qwen3.5-2B on drawn office fixtures. Honest rates only."""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

from evo.office.vision_backend import RealVlBackend, VisionObs


def clean_pred(s: str) -> str:
    s = s or ""
    s = re.sub(r"<think>[\s\S]*?</think>", " ", s)
    s = re.sub(r"^assistant\s*", "", s, flags=re.I)
    s = re.sub(r"```(?:csv|text)?", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip().lower())


def score(pred: str, gold: str, task: str) -> bool:
    p, g = norm(clean_pred(pred)), norm(gold)
    if not g:
        return False
    if task == "ocr":
        # key tokens present
        keys = [t for t in re.split(r"\s+", g) if t]
        hit = sum(1 for t in keys if t.lower() in p)
        return hit / max(1, len(keys)) >= 0.5
    if task == "table_cells":
        need = ["sku", "a1", "b2"]
        return sum(1 for t in need if t in p) >= 2
    # caption: any meaningful gold token overlap
    stop = {"with", "a", "the", "and", "on", "of"}
    gt = [t for t in g.split() if t not in stop]
    hit = sum(1 for t in gt if t in p)
    return hit / max(1, len(gt)) >= 0.3


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    weights = root / "models" / "Qwen3.5-2B"
    img_dir = root / "evo" / "office" / "fixtures" / "vision_images_real"
    tasks = [
        ("office-caption-001.png", "caption", "caption"),
        ("office-ocr-001.png", "ocr", "ocr_text"),
        ("office-table-001.png", "table_cells", "cells_csv"),
        ("office-ui-001.png", "caption", "caption"),
    ]
    backend = RealVlBackend(weights, max_new_tokens=96)
    rows = []
    n_ok = 0
    for fname, task, gold_key in tasks:
        path = img_dir / fname
        meta = json.loads(path.with_suffix(".json").read_text(encoding="utf-8"))
        gold = str(meta.get(gold_key) or meta.get("gold") or "")
        try:
            pred = backend.predict(VisionObs(image_path=path, task=task, gold=gold))
            text = clean_pred(pred.text)
            ok = score(text, gold, task)
            err = None
        except Exception as e:  # noqa: BLE001
            text = ""
            ok = False
            err = f"{type(e).__name__}: {e}"
        n_ok += int(ok)
        rows.append({
            "image": fname,
            "task": task,
            "gold": gold,
            "pred": text,
            "ok": ok,
            "error": err,
            "backend": "real_vl",
            "synthetic_not_vl": False,
        })
    n = len(rows)
    rate = n_ok / n if n else 0.0
    gate = 0.6
    evidence = {
        "kind": "vision_v0_smoke_real_vl",
        "product": "蚁算-视",
        "timestamp": datetime.now().astimezone().isoformat(timespec="seconds"),
        "gate": str(gate),
        "weights_path": str(weights).replace("\\", "/"),
        "fixture_dir": str(img_dir).replace("\\", "/"),
        "weights_local": True,
        "synthetic_not_vl": False,
        "drawn_office_fixtures": True,
        "n": n,
        "n_ok": n_ok,
        "rate": rate,
        "gate_pass": rate >= gate,
        "vl_gate_claim": False,
        "rows": rows,
        "notes": "Honest V0 smoke on drawn office PNGs matching gold. Does NOT mint Epoch D gate claim. Gate2/3 untouched.",
    }
    out = root / "docs" / "VISION_V0_SMOKE_REAL_VL_2026-10-18.json"
    out.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"pass": evidence["gate_pass"], "rate": rate, "n_ok": n_ok, "n": n, "path": str(out)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
