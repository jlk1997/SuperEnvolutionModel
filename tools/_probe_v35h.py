from pathlib import Path
# How was v34h generated?
for name in ["c310_vision_v34_heldout.py","c308_vision_v34_design_and_batch.py","c316_vision_v35_heldout.py"]:
    p=Path("scripts")/name
    t=p.read_text(encoding="utf-8")
    print("====", name, "len", len(t))
    for i,l in enumerate(t.splitlines(),1):
        if any(k in l for k in ["v34h","v35h","make_fixture","FIX =","HELD","held","SPECS","def main","Image.new","generate"]):
            if "hardening" in l: continue
            print(f"{i}:{l[:150]}")
print("==== v34h manifest head ====")
man=Path("evo/office/fixtures/vision_images_v34h/manifest.json")
if man.exists():
    import json
    m=json.loads(man.read_text(encoding="utf-8"))
    print("n", m.get("n"), "version", m.get("version"), "theme", str(m.get("theme"))[:80])
    print("first ids", [it["id"] for it in m.get("items",[])[:3]])
    print("files", len(list(man.parent.glob("*.png"))))
# check boot for heldout
boot=Path("tools/_boot_v35_c314.py").read_text(encoding="utf-8")
print("==== boot held refs ====")
for i,l in enumerate(boot.splitlines(),1):
    if "held" in l.lower() or "v35h" in l or "HELD" in l or "c316" in l:
        print(f"{i}:{l[:160]}")
