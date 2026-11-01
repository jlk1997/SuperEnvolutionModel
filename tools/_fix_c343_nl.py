# -*- coding: utf-8 -*-
from pathlib import Path
p = Path("scripts/c343_capture_office_regression.py")
t = p.read_text(encoding="utf-8")
bad = '("V38_heldout", DOC / "C334_VISION_V38_HELDOUT_SMOKE.json"),`n    ("V39", DOC / "C340_VISION_V39_SMOKE.json"),`n    ("V39_heldout", DOC / "C341_VISION_V39_HELDOUT_SMOKE.json"),`n    ("C342_confidence_gate_stretch", DOC / "C342_CONFIDENCE_GATE_STRETCH.json"),'
good = '''("V38_heldout", DOC / "C334_VISION_V38_HELDOUT_SMOKE.json"),
    ("V39", DOC / "C340_VISION_V39_SMOKE.json"),
    ("V39_heldout", DOC / "C341_VISION_V39_HELDOUT_SMOKE.json"),
    ("C342_confidence_gate_stretch", DOC / "C342_CONFIDENCE_GATE_STRETCH.json"),'''
if bad not in t:
    raise SystemExit("bad marker not found")
p.write_text(t.replace(bad, good), encoding="utf-8")
print("fixed")
