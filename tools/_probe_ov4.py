from pathlib import Path
o=Path("scripts/c302_vision_v33_design_and_batch.py").read_text(encoding="utf-8")
i=o.find("# --- V33 overlays")
chunk=o[i:i+2500]
print(chunk)
print("====MID====")
print(o[i+2500:i+5000])
