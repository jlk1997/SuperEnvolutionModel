# -*- coding: utf-8 -*-
"""C1212b: redesign V184 SLA after smoke fail v184_07 (550+590→1140 got 1249).
Use proven OCR-safe SLA TR 480+520 HO 360+400. Ban scrub. Re-emit fixtures.
"""
from __future__ import annotations
import json, re, subprocess, sys
from pathlib import Path
ROOT = Path(r"E:\envolution")
BAN = {755, 756, 770, 750, 830, 1830, 1560}
themes = json.loads((ROOT/"tools/_v184_themes.json").read_text(encoding="utf-8"))
themes["train"][6] = [480.0, 520.0, 640.0]
themes["heldout"][6] = [360.0, 400.0, 580.0]
for label, rows in (("TR", themes["train"]), ("HO", themes["heldout"])):
    for i, row in enumerate(rows):
        for v in row:
            if isinstance(v, (int, float)) and int(v) in BAN:
                raise SystemExit(f"banned {v} in {label}[{i}]")
(ROOT/"tools/_v184_themes.json").write_text(json.dumps(themes, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
# patch builder TR/HO sla rows then rebuild design script specs via _build_v184 re-run would overwrite; patch design SPECS directly
design = (ROOT/"scripts/c1211_vision_v184_design_and_batch.py").read_text(encoding="utf-8")
# replace hazebrook sla block numbers
old = """    ("v184_07", "hazebrook_sla", "sla_ok_hours", 1140.0,
     ['HAZEBROOK SLA CARD V184',
     'job1 550.00 hours ok',
     'job2 590.00 hours ok',
     'job3 630.00 hours late',
     'sla_ok_hours TARGET 1140.00'],
     'hazebrook', "SLA"),"""
new = """    ("v184_07", "hazebrook_sla", "sla_ok_hours", 1000.0,
     ['HAZEBROOK SLA CARD V184',
     'job1 480.00 hours ok',
     'job2 520.00 hours ok',
     'job3 640.00 hours late',
     'sla_ok_hours TARGET 1000.00'],
     'hazebrook', "SLA"),"""
if old not in design:
    # try float repr without .0 on expected
    raise SystemExit("design sla block not found:\n"+design[design.find("hazebrook_sla")-80:design.find("hazebrook_sla")+400])
design = design.replace(old, new, 1)
(ROOT/"scripts/c1211_vision_v184_design_and_batch.py").write_text(design, encoding="utf-8")
# heldout script
ho = (ROOT/"scripts/c1213_vision_v184_heldout.py").read_text(encoding="utf-8")
oldh = """    ("v184h_07", "hazebrook_sla", "sla_ok_hours", 900.0,
     ['HAZEBROOK SLA CARD V184H',
     'job1 430.00 hours ok',
     'job2 470.00 hours ok',
     'job3 610.00 hours late',
     'sla_ok_hours TARGET 900.00'],
     'hazebrook', "SLA"),"""
# compute what was generated: 430+470=900
newh = """    ("v184h_07", "hazebrook_sla", "sla_ok_hours", 760.0,
     ['HAZEBROOK SLA CARD V184H',
     'job1 360.00 hours ok',
     'job2 400.00 hours ok',
     'job3 580.00 hours late',
     'sla_ok_hours TARGET 760.00'],
     'hazebrook', "SLA"),"""
if oldh not in ho:
    # find actual
    i = ho.find("v184h_07")
    raise SystemExit("heldout sla block not found:\n"+ho[i:i+450])
ho = ho.replace(oldh, newh, 1)
(ROOT/"scripts/c1213_vision_v184_heldout.py").write_text(ho, encoding="utf-8")
print("patched themes+scripts")
print("sla TR", themes["train"][6], "HO", themes["heldout"][6])
