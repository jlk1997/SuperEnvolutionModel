import json
from pathlib import Path
ROOT = Path(r"E:/envolution")
p = ROOT / "tools/_v168_themes.json"
d = json.loads(p.read_text(encoding="utf-8"))
if d["heldout"][1][2] == 830:
    d["heldout"][1] = [840, 760, 810]
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("themes fixed")
else:
    print("themes already", d["heldout"][1])
hp = ROOT / "scripts/c1117_vision_v168_heldout.py"
t = hp.read_text(encoding="utf-8")
if "SKU2 qty 830 hold" in t:
    hp.write_text(t.replace("SKU2 qty 830 hold", "SKU2 qty 810 hold"), encoding="utf-8")
    print("heldout script fixed")
else:
    print("heldout script ok", "830" in t)
# also fix builder for future
bp = ROOT / "tools/_build_v168.py"
bt = bp.read_text(encoding="utf-8")
if "[840, 760, 830]" in bt:
    bp.write_text(bt.replace("[840, 760, 830]", "[840, 760, 810]"), encoding="utf-8")
    print("builder fixed")
print("done", d["heldout"][1])
