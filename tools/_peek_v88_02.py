import re
from pathlib import Path
t = Path(r"scripts/c635_vision_v88_design_and_batch.py").read_text(encoding="utf-8")
m = re.search(r'\("v88_02".*?"RECV"\)', t, re.S)
print(m.group(0) if m else "MISSING")
ht = Path(r"scripts/c637_vision_v88_heldout.py").read_text(encoding="utf-8")
m2 = re.search(r'\("v88h_02".*?"RECV"\)', ht, re.S)
print("--- heldout ---")
print(m2.group(0) if m2 else "MISSING")
