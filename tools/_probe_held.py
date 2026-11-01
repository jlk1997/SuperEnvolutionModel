from pathlib import Path
import re
d=Path("scripts/c304_vision_v33_heldout.py").read_text(encoding="utf-8")
i=d.find("SPECS")
print(d[i:i+300] if i>=0 else "no SPECS")
m=re.search(r"SPECS = \[.*?\]\n", d, re.S)
print("match", bool(m), "len", len(m.group(0)) if m else 0)
# also check c308 current state
c=Path("scripts/c308_vision_v34_design_and_batch.py").read_text(encoding="utf-8")
print("c308 has v34_01", "v34_01" in c, "v33_01" in c, "bamboo" in c, "parchment" in c)
print("c308 SPECS head", c[c.find("SPECS"):c.find("SPECS")+200])
