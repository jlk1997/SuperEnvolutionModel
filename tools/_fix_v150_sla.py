# -*- coding: utf-8 -*-
"""Fix V150 SLA TR 550+590 OCR trap (got 1249) -> 480+520."""
from __future__ import annotations
import json, re
from pathlib import Path
ROOT = Path(r"E:\envolution")

tj = ROOT / "tools/_v150_themes.json"
d = json.loads(tj.read_text(encoding="utf-8"))
old = d["train"][6]
d["train"][6] = [480.0, 520.0, 300.0]
tj.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("sla", old, "->", d["train"][6])

p = ROOT / "scripts/c1007_vision_v150_design_and_batch.py"
t = p.read_text(encoding="utf-8")
pat = re.compile(
    r'\("v150_07", "hazefen_sla", "sla_ok_hours", 1140\.0,\n'
    r'     \[.*?\],\n'
    r'     \'hazefen\', "SLA"\),',
    re.S,
)
repl = (
    '("v150_07", "hazefen_sla", "sla_ok_hours", 1000.0,\n'
    "     ['HAZEFEN SLA CARD V150', 'job1 480.00 hours ok', 'job2 520.00 hours ok', 'job3 300.00 hours late', 'sla_ok_hours TARGET 1000.00'],\n"
    "     'hazefen', \"SLA\"),"
)
m = pat.search(t)
if not m:
    i = t.find("v150_07")
    print("NO MATCH", repr(t[i:i+400]) if i>=0 else "missing")
    raise SystemExit(1)
t = pat.sub(repl, t, count=1)
p.write_text(t, encoding="utf-8")
print("SPECS patched")
