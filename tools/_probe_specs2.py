from pathlib import Path
t=Path("tools/_boot_v33_c302.py").read_text(encoding="utf-8")
i=t.find("def specs_to_py")
print(t[i:i+600])
print("---REPLACE---")
j=t.find("def replace_specs")
print(t[j:j+500])
# also show end of SPECS in design
d=Path("scripts/c302_vision_v33_design_and_batch.py").read_text(encoding="utf-8")
k=d.find("SPECS = [")
print("---SPECS HEAD---")
print(d[k:k+400])
# find end of SPECS
import re
m=re.search(r"SPECS = \[.*?\]\n\n", d, re.S)
print("SPECS len", len(m.group(0)) if m else None)
print("tail", m.group(0)[-200:] if m else None)
