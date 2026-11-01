import json, pprint
d=json.load(open("docs/r50/C268_VISION_V27_HELDOUT_SMOKE.json",encoding="utf-8"))
print("rate", d.get("rate"), "claim", d.get("claim"))
for r in d.get("rows",[]):
    if "11" in str(r.get("id","")) or r.get("ok") is False:
        pprint.pp({k:r[k] for k in r if k!="ocr_preview"})
        print("preview", repr(r.get("ocr_preview","")[:200]))
design=json.load(open("docs/r50/C266_VISION_V27_DESIGN.json",encoding="utf-8"))
print("design keys", list(design.keys()))
# find case 11
for key in design:
    v=design[key]
    if isinstance(v,list):
        for item in v:
            if isinstance(item,dict) and ("v27_11" in str(item) or item.get("id")=="v27_11" or item.get("kind")=="perf_dup"):
                pprint.pp(item)
    elif isinstance(v,dict) and ("v27_11" in str(v) or "perf_dup" in str(v)):
        # maybe cases dict
        if "v27_11" in v: pprint.pp(v["v27_11"])
        elif "cases" in v:
            pass
