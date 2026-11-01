from pathlib import Path
o=Path("scripts/c302_vision_v33_design_and_batch.py").read_text(encoding="utf-8")
j=o.find("GaussianBlur")
print(o[j:j+800])
print("====C308====")
c=Path("scripts/c308_vision_v34_design_and_batch.py").read_text(encoding="utf-8")
j=c.find("GaussianBlur")
print(c[j:j+500] if j>=0 else "no blur")
# find buf =
print("buf count c302", o.count("buf = io.BytesIO()"))
print("buf count c308", c.count("buf = io.BytesIO()"))
