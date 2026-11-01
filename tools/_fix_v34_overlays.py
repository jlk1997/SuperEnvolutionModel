# -*- coding: utf-8 -*-
"""Clean overlays in c308 design + fix boot strip for future."""
from pathlib import Path
import re

boot = Path("tools/_boot_v34_c308.py").read_text(encoding="utf-8")
# extract V34_OVERLAY
m = re.search(r"V34_OVERLAY = r'''(.*?)'''", boot, re.S)
if not m:
    raise SystemExit("no V34_OVERLAY")
overlay = m.group(1)
if "bamboo grain" not in overlay:
    raise SystemExit("overlay missing bamboo")

design = Path("scripts/c308_vision_v34_design_and_batch.py")
t = design.read_text(encoding="utf-8")
# strip all overlay blocks between first '# --- V' overlays and soft_affine/img.save
t2, n = re.subn(
    r"\n    # --- V\d+ overlays \(new vs V\d+\) ---.*?(?=\n    # soft_affine|\n    img\.save\(buf)",
    "\n",
    t,
    count=0,
    flags=re.S,
)
print("stripped overlay blocks:", n)
if "V34 overlays" in t2:
    # still present somehow
    t2, n2 = re.subn(
        r"\n    # --- V34 overlays.*? (?=\n    # soft_affine|\n    img\.save\(buf))",
        "\n",
        t2,
        count=1,
        flags=re.S,
    )
    print("extra strip", n2)

soft = "    # soft_affine"
if soft in t2:
    t2 = t2.replace(soft, overlay + "\n" + soft, 1)
elif "    img.save(buf" in t2:
    t2 = t2.replace("    img.save(buf", overlay + "\n    img.save(buf", 1)
else:
    raise SystemExit("no inject point")

assert "bamboo grain" in t2
assert "parchment fiber" not in t2
assert t2.count("# --- V34 overlays") == 1
design.write_text(t2, encoding="utf-8")
print("design fixed", design.stat().st_size)

# Also fix boot strip to remove ALL prior overlay blocks
bt = Path("tools/_boot_v34_c308.py").read_text(encoding="utf-8")
old_strip = '''    # strip V33 overlay from source BEFORE version rename
    text = re.sub(
        r"\\n    # --- V33 overlays \\(new vs V32\\) ---.*?(?=\\n    # soft_affine|\\n    img\\.save\\(buf)",
        "\\n",
        text,
        count=1,
        flags=re.S,
    )'''
# may not exist due to failed earlier patch; find any strip
if "strip V33 overlay" not in bt and "# strip old" in bt:
    bt = re.sub(
        r"    # strip old.*?flags=re\.S,\n    \)\n",
        '''    # strip ALL prior overlay blocks before rename
    text = re.sub(
        r"\\n    # --- V\\d+ overlays \\(new vs V\\d+\\) ---.*?(?=\\n    # soft_affine|\\n    img\\.save\\(buf)",
        "\\n",
        text,
        count=0,
        flags=re.S,
    )
''',
        bt,
        count=1,
        flags=re.S,
    )
    Path("tools/_boot_v34_c308.py").write_text(bt, encoding="utf-8")
    print("boot strip generalized")
elif "strip V33 overlay" in bt:
    bt = bt.replace(
        r'r"\n    # --- V33 overlays \(new vs V32\) ---.*?(?=\n    # soft_affine|\n    img\.save\(buf)"',
        r'r"\n    # --- V\d+ overlays \(new vs V\d+\) ---.*?(?=\n    # soft_affine|\n    img\.save\(buf)"',
    )
    bt = bt.replace("count=1,\n        flags=re.S,\n    )\n    for a, b in reps:", "count=0,\n        flags=re.S,\n    )\n    for a, b in reps:")
    Path("tools/_boot_v34_c308.py").write_text(bt, encoding="utf-8")
    print("boot strip via marker")
else:
    # insert strip before for a,b in reps inside xform_train
    needle = "    for a, b in reps:\n        text = text.replace(a, b)\n    text = replace_specs(text, train_specs)"
    insert = '''    text = re.sub(
        r"\\n    # --- V\\d+ overlays \\(new vs V\\d+\\) ---.*?(?=\\n    # soft_affine|\\n    img\\.save\\(buf)",
        "\\n",
        text,
        count=0,
        flags=re.S,
    )
''' + needle
    if needle in bt:
        # also remove old broken strip if present
        bt2 = re.sub(
            r"    # strip old V32 overlay block if present, then inject V33\n    text = re\.sub\(\n        r\"\\n    # --- V33 overlays.*?flags=re\.S,\n    \)\n",
            "",
            bt,
            count=1,
            flags=re.S,
        )
        bt2 = bt2.replace(needle, insert, 1)
        Path("tools/_boot_v34_c308.py").write_text(bt2, encoding="utf-8")
        print("boot strip inserted")
    else:
        print("WARN could not update boot strip")
