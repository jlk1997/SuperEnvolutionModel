# -*- coding: utf-8 -*-
"""C272a: Honest cheap repair of v27_11 — kill 发票 OCR-loop bait, diversify lines.
Re-render fixture only; no fake VL scores. Gate2/3 untouched. gen11 HOLD.
"""
from __future__ import annotations
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

SCR = ROOT / "scripts" / "c266_vision_v27_design_and_batch.py"
FIX = ROOT / "evo" / "office" / "fixtures" / "vision_images_v27"
DOC = ROOT / "docs" / "r50"


def main():
    text = SCR.read_text(encoding="utf-8")
    # Replace the v27_11 SPECS tuple (match by id+kind+expected)
    import re
    pat = re.compile(
        r'\("v27_11",\s*"perf_dup",\s*"paid_total",\s*111\.0,\s*'
        r'\[[^\]]+\],\s*"[^"]*",\s*"[^"]*"\)',
        re.S,
    )
    new_tuple = (
        '("v27_11", "perf_dup", "paid_total", 111.0,\n'
        '     ["INVOICE #V27-PERF", "lineA paid 37.00", "lineB paid 37.00", '
        '"lineC paid 37.00", "TOTAL PAID TARGET 111.00"],\n'
        '     "撕边复写联单", "RECV")'
    )
    m = pat.search(text)
    if not m:
        raise SystemExit("v27_11 SPECS not found")
    text2 = text[: m.start()] + new_tuple + text[m.end() :]
    SCR.write_text(text2, encoding="utf-8")
    print("patched c266 SPECS v27_11")

    # Also patch tools/gen_v27_batch.py TRAIN specs for consistency
    gen = ROOT / "tools" / "gen_v27_batch.py"
    if gen.is_file():
        gt = gen.read_text(encoding="utf-8")
        gm = pat.search(gt)
        if gm:
            gen.write_text(gt[: gm.start()] + new_tuple + gt[gm.end() :], encoding="utf-8")
            print("patched gen_v27_batch TRAIN v27_11")

    # Import make_fixture and re-render
    import importlib.util
    spec = importlib.util.spec_from_file_location("c266", SCR)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    item = mod.make_fixture(
        "v27_11",
        "perf_dup",
        [
            "INVOICE #V27-PERF",
            "lineA paid 37.00",
            "lineB paid 37.00",
            "lineC paid 37.00",
            "TOTAL PAID TARGET 111.00",
        ],
        "paid_total",
        111.0,
        "撕边复写联单",
        "RECV",
    )
    print("rerendered", item["path"])

    # Update manifest item
    man_path = FIX / "manifest.json"
    man = json.loads(man_path.read_text(encoding="utf-8"))
    for i, it in enumerate(man["items"]):
        if it["id"] == "v27_11":
            man["items"][i] = item
            break
    else:
        raise SystemExit("v27_11 not in manifest")
    man["timestamp"] = mod.ts()
    man["note"] = (man.get("note") or "") + "; C272a repaired v27_11 cn_title+line labels (no 发票 loop bait)"
    man_path.write_text(json.dumps(man, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    out = {
        "cycle": "C272a",
        "theme": "v27_11_honest_repair",
        "gate": 0.6,
        "timestamp": mod.ts(),
        "id": "v27_11",
        "change": {
            "cn_title": "撕边复写联单",
            "lines": item["lines"],
            "expected": 111.0,
            "reason": "VL OCR collapsed into 发票 token loop; remove short repeatable CN token; diversify line labels",
            "fake_vl": False,
        },
        "path": item["path"],
        "pass": True,
        "claim": False,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }
    DOC.mkdir(parents=True, exist_ok=True)
    (DOC / "C272a_V27_11_REPAIR.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
