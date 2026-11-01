from pathlib import Path
o=Path("scripts/c302_vision_v33_design_and_batch.py").read_text(encoding="utf-8")
i=o.find("# --- V33 overlays")
# find next section after overlay - look for blank line then non-indent draw that isn't overlay, or buf=
j=o.find("\n    buf = io.BytesIO()", i)
print("i", i, "j", j)
print("---OVERLAY TAIL---")
print(o[j-300:j+80])
print("---OVERLAY HEAD---")
print(o[i:i+200])
