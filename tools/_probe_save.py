from pathlib import Path
t=Path("scripts/c308_vision_v34_design_and_batch.py").read_text(encoding="utf-8")
# show around img.save
i=t.find("img.save")
print("count", t.count("img.save"))
print(t[i-400:i+200])
print("---ORIG---")
o=Path("scripts/c302_vision_v33_design_and_batch.py").read_text(encoding="utf-8")
j=o.find("img.save")
print(o[j-200:j+150])
