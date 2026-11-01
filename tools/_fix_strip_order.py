# -*- coding: utf-8 -*-
from pathlib import Path
P = Path("tools/_boot_v34_c308.py")
t = P.read_text(encoding="utf-8")
old = '''    for a, b in reps:
        text = text.replace(a, b)
    text = replace_specs(text, train_specs)
    # strip old V32 overlay block if present, then inject V33
    text = re.sub(
        r"\n    # --- V33 overlays \(new vs V32\) ---.*?(?=\n    # soft_affine|\n    img\.save\(buf)",
        "\n",
        text,
        count=1,
        flags=re.S,
    )
    if "V34 overlays" not in text:'''
new = '''    # strip V33 overlay from source BEFORE version rename
    text = re.sub(
        r"\n    # --- V33 overlays \(new vs V32\) ---.*?(?=\n    # soft_affine|\n    img\.save\(buf)",
        "\n",
        text,
        count=1,
        flags=re.S,
    )
    for a, b in reps:
        text = text.replace(a, b)
    text = replace_specs(text, train_specs)
    if "V34 overlays" not in text:'''
if old not in t:
    raise SystemExit("block not found")
P.write_text(t.replace(old, new), encoding="utf-8")
print("fixed")
