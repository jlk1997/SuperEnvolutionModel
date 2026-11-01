from pathlib import Path
o=Path("scripts/c302_vision_v33_design_and_batch.py").read_text(encoding="utf-8")
print("V33 overlays" in o, "parchment fiber" in o, "DENIM" in o)
i=o.find("overlays")
print("overlays idx", i)
if i>0: print(o[i-100:i+200])
# find where overlay content is
i=o.find("parchment fiber")
print("parchment idx", i)
if i>0: print(o[i-80:i+100])
# c308 structure around blend
c=Path("scripts/c308_vision_v34_design_and_batch.py").read_text(encoding="utf-8")
i=c.find("Image.blend")
print("blend c308", i)
if i>0: print(c[i:i+400])
i=c.find("DENIM bait")
print("denim context:\n", c[i-100:i+50])
