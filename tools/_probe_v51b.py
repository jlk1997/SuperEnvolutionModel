from pathlib import Path
# dump key functions from c413 for overlay/render understanding
t = Path("scripts/c413_vision_v51_design_and_batch.py").read_text(encoding="utf-8")
# find function names
import re
funcs = re.findall(r"^def (\w+)", t, re.M)
print("funcs", funcs)
# print middle section with make_fixture and overlays
idx = t.find("def make_fixture")
print(t[idx:idx+4500])
