# -*- coding: utf-8 -*-
"""Fix V145 qty TR 780+740 (OCR 740->780 ->1560) to 840+760; rebuild train fixture 02 only."""
from __future__ import annotations
import json, re, sys
from pathlib import Path
ROOT = Path(r"E:\envolution")
sys.path.insert(0, str(ROOT))

# update themes
tj = ROOT / "tools/_v145_themes.json"
d = json.loads(tj.read_text(encoding="utf-8"))
# train idx1 qty was [780,740,690] -> [840,760,610]
old = d["train"][1]
d["train"][1] = [840, 760, 610]
tj.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("themes train qty", old, "->", d["train"][1])

# patch design script SPECS for v145_02
p = ROOT / "scripts/c977_vision_v145_design_and_batch.py"
t = p.read_text(encoding="utf-8")
# Find v145_02 block and replace qty lines
# expected was 1520.0 -> 1600.0
pat = re.compile(
    r'\("v145_02", "cedarmere_wh", "qty_sum", 1520\.0,\n'
    r'     \[.*?qty_sum TARGET 1520\],\n'
    r'     \'cedarmere\', "RECV"\),',
    re.S,
)
repl = (
    '("v145_02", "cedarmere_wh", "qty_sum", 1600.0,\n'
    '     [\'WH CEDARMERE BIN V145\', \'SKU1 qty 840 ok\', \'SKU2 qty 610 hold\', \'SKU3 qty 760 ok\', \'qty_sum TARGET 1600\'],\n'
    '     \'cedarmere\', "RECV"),'
)
m = pat.search(t)
if not m:
    # try double-quote style from build_specs
    pat2 = re.compile(
        r'\("v145_02", "cedarmere_wh", "qty_sum", 1520\.0,\n'
        r'     \[.*?\],\n'
        r'     \'cedarmere\', "RECV"\),',
        re.S,
    )
    m = pat2.search(t)
    if m:
        t = pat2.sub(repl, t, count=1)
        print("patched design SPECS via pat2")
    else:
        # dump nearby
        i = t.find("v145_02")
        print("NO MATCH near:", repr(t[i:i+350]) if i>=0 else "missing")
        raise SystemExit(1)
else:
    t = pat.sub(repl, t, count=1)
    print("patched design SPECS via pat")
p.write_text(t, encoding="utf-8")

# also patch smoke if it embeds expected from manifest only — smoke reads fixtures/manifest
# Rebuild fixtures by invoking design's render path: easiest re-run design (train only)
print("re-run design to refresh fixtures")
