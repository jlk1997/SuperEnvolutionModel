from pathlib import Path
import re
p = Path("scripts/c413_vision_v51_design_and_batch.py")
t = p.read_text(encoding="utf-8")
print("len", len(t))
themes = re.findall(r'"(v51_\d+)",\s*"(\w+)"', t)
print("themes", themes)
print("---TAIL---")
print(t[-2000:])
