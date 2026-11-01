from pathlib import Path
o=Path("scripts/c302_vision_v33_design_and_batch.py").read_text(encoding="utf-8")
i=o.find("# --- V33 overlays")
# spiral was end of V33_OVERLAY in boot
k=o.find("spiral bind", i)
print("spiral", k)
print(o[k:k+400] if k>0 else "none")
# what comes after spiral arcs block
import re
m=re.search(r"# --- V33 overlays.*?spiral bind.*?\n(?:    for sy in range.*?\n(?:        .*\n)+)?", o, re.S)
