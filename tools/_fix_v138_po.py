import json, re
from pathlib import Path
ROOT = Path(r"E:\envolution")
t = json.loads((ROOT/"tools/_v138_themes.json").read_text(encoding="utf-8"))
t["train"][8] = [840.0, 760.0, 640.0]  # 840+760=1600; avoid 830->1830 / 740->720
(ROOT/"tools/_v138_themes.json").write_text(json.dumps(t, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
p = ROOT/"scripts/c935_vision_v138_design_and_batch.py"
src = p.read_text(encoding="utf-8")
old = '''    ("v138_09", "jadecrest_po", "po_open", 1570.0,
     ['JADECREST PO SHEET V138',
     'line1 830.00 open',
     'line2 740.00 open',
     'line3 640.00 closed',
     'po_open TARGET 1570.00'],
     'jadecrest', "PO"),'''
new = '''    ("v138_09", "jadecrest_po", "po_open", 1600.0,
     ['JADECREST PO SHEET V138',
     'line1 840.00 open',
     'line2 760.00 open',
     'line3 640.00 closed',
     'po_open TARGET 1600.00'],
     'jadecrest', "PO"),'''
if old not in src:
    src2, n = re.subn(
        r'\("v138_09", "jadecrest_po", "po_open", 1570\.0,\n     \[.*?\]\,\n     \'jadecrest\', "PO"\),',
        new.strip(), src, count=1, flags=re.S)
    print("re.sub", n); src = src2
else:
    src = src.replace(old, new); print("exact ok")
p.write_text(src, encoding="utf-8")
bp = ROOT/"tools/_build_v138.py"
bs = bp.read_text(encoding="utf-8")
bs = bs.replace("[830.0, 740.0, 640.0]", "[840.0, 760.0, 640.0]", 1)
bp.write_text(bs, encoding="utf-8")
print("patched")
