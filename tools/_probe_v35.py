from pathlib import Path
t=Path("scripts/c314_vision_v35_design_and_batch.py").read_text(encoding="utf-8")
keys=["v35h","HELDOUT","heldout","FIX","def main","HELD","TRAIN","SPECS","manifest"]
for i,l in enumerate(t.splitlines(),1):
    if any(k in l for k in keys) and "hardening" not in l and "coffee" not in l:
        print(f"{i}:{l[:150]}")
print("---C308---")
t2=Path("scripts/c308_vision_v34_design_and_batch.py").read_text(encoding="utf-8")
for i,l in enumerate(t2.splitlines(),1):
    if any(k in l for k in ["v34h","HELDOUT","heldout","FIX =","def main","HELD","TRAIN"]):
        print(f"{i}:{l[:150]}")
print("v34h", Path("evo/office/fixtures/vision_images_v34h").exists())
print([p.name for p in Path("evo/office/fixtures").glob("vision_images_v3*")])
# also dump C314 main tail
lines=t.splitlines()
print("---C314 main---")
for i,l in enumerate(lines):
    if l.startswith("def main"):
        print("\n".join(f"{j+1}:{lines[j][:160]}" for j in range(i, min(i+80, len(lines)))))
        break
