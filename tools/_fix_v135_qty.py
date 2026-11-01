import json, re
from pathlib import Path
ROOT = Path(r"E:\envolution")
t = json.loads((ROOT/"tools/_v135_themes.json").read_text(encoding="utf-8"))
t["train"][1] = [740, 780, 590]  # 740+780=1520; avoid 750/770 7<->5 OCR
(ROOT/"tools/_v135_themes.json").write_text(json.dumps(t, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
p = ROOT/"scripts/c917_vision_v135_design_and_batch.py"
src = p.read_text(encoding="utf-8")
old = '''    ("v135_02", "cedarholt_wh", "qty_sum", 1520.0,
     ['WH CEDARHOLT BIN V135',
     'SKU1 qty 750 ok',
     'SKU2 qty 590 hold',
     'SKU3 qty 770 ok',
     'qty_sum TARGET 1520'],
     'cedarholt', "RECV"),'''
new = '''    ("v135_02", "cedarholt_wh", "qty_sum", 1520.0,
     ['WH CEDARHOLT BIN V135',
     'SKU1 qty 740 ok',
     'SKU2 qty 590 hold',
     'SKU3 qty 780 ok',
     'qty_sum TARGET 1520'],
     'cedarholt', "RECV"),'''
if old not in src:
    src2, n = re.subn(
        r'\("v135_02", "cedarholt_wh", "qty_sum", 1520\.0,\n     \[.*?\]\,\n     \'cedarholt\', "RECV"\),',
        new.strip(), src, count=1, flags=re.S)
    print("re.sub", n); src = src2
else:
    src = src.replace(old, new); print("exact ok")
p.write_text(src, encoding="utf-8")
bp = ROOT/"tools/_build_v135.py"
bs = bp.read_text(encoding="utf-8")
bs = bs.replace("[750, 770, 590]", "[740, 780, 590]", 1)
bp.write_text(bs, encoding="utf-8")
print("patched")
