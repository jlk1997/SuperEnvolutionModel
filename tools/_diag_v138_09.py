import json
d=json.load(open(r"docs/r50/C936_VISION_V138_SMOKE.json",encoding="utf-8"))
for r in d["rows"]:
    if r.get("id")=="v138_09":
        print(json.dumps(r, ensure_ascii=False, indent=2)[:2200])
