import json, re
from pathlib import Path
ROOT = Path(r"E:\envolution")
# patch themes
t = json.loads((ROOT/"tools/_v133_themes.json").read_text(encoding="utf-8"))
t["train"][8] = [780.0, 740.0, 590.0]  # 780+740=1520 OCR-friendly; avoid 755->756
(ROOT/"tools/_v133_themes.json").write_text(json.dumps(t, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
# patch SPECS in design script
p = ROOT/"scripts/c905_vision_v133_design_and_batch.py"
src = p.read_text(encoding="utf-8")
old = '''    ("v133_09", "jadehaven_po", "po_open", 1527.0,
     ['JADEHAVEN PO SHEET V133',
     'line1 772.00 open',
     'line2 755.00 open',
     'line3 595.00 closed',
     'po_open TARGET 1527.00'],
     'jadehaven', "PO"),'''
new = '''    ("v133_09", "jadehaven_po", "po_open", 1520.0,
     ['JADEHAVEN PO SHEET V133',
     'line1 780.00 open',
     'line2 740.00 open',
     'line3 590.00 closed',
     'po_open TARGET 1520.00'],
     'jadehaven', "PO"),'''
if old not in src:
    # try flexible match
    src2, n = re.subn(
        r'\("v133_09", "jadehaven_po", "po_open", 1527\.0,\n     \[.*?\]\,\n     \'jadehaven\', "PO"\),',
        new.strip(),
        src, count=1, flags=re.S)
    print("re.sub n", n)
    src = src2
else:
    src = src.replace(old, new)
    print("exact replace ok")
p.write_text(src, encoding="utf-8")
# also patch builder TR133 po
bp = ROOT/"tools/_build_v133.py"
bs = bp.read_text(encoding="utf-8")
bs = bs.replace("[772.0, 755.0, 595.0]", "[780.0, 740.0, 590.0]", 1)
bp.write_text(bs, encoding="utf-8")
print("patched")
