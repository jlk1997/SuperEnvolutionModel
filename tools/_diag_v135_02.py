import json
from pathlib import Path
d=json.load(open(r"docs/r50/C918_VISION_V135_SMOKE.json",encoding="utf-8"))
for r in d["rows"]:
    if r.get("id")=="v135_02":
        print(json.dumps(r, ensure_ascii=False, indent=2)[:2000])
