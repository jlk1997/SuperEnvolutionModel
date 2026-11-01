from pathlib import Path
# dump SPECS fully and PROTOCOL from c413
t = Path("scripts/c413_vision_v51_design_and_batch.py").read_text(encoding="utf-8")
# extract SPECS block
start = t.find("SPECS = [")
end = t.find("\n]\n", start)
print(t[start:end+3])
print("====PROTOCOL====")
ps = t.find("PROTOCOL")
print(t[ps:ps+1200])
