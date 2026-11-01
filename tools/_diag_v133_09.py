import json, re
from pathlib import Path
d=json.load(open(r"docs/r50/C906_VISION_V133_SMOKE.json",encoding="utf-8"))
print("keys", list(d.keys())[:20])
rows=d.get("rows") or d.get("results") or d.get("items") or []
print("nrows", len(rows))
for r in rows:
    if r.get("id")=="v133_09" or r.get("ok") is False:
        print(json.dumps(r, ensure_ascii=False, indent=2)[:2500])
src=Path("scripts/c905_vision_v133_design_and_batch.py").read_text(encoding="utf-8")
# find po_open expected in SPECS
for ln in src.splitlines():
    if "v133_09" in ln or ("po_open" in ln and "1527" in ln) or ("JADEHAVEN" in ln):
        print("LN", ln[:160])
# also check train ABC for po index 8
t=json.load(open("tools/_v133_themes.json",encoding="utf-8"))
print("train_po", t["train"][8], "heldout_po", t["heldout"][8])
