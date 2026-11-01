import json, pprint
d=json.load(open("docs/r50/C267_VISION_V27_SMOKE.json",encoding="utf-8"))
print("keys", list(d.keys()))
for k in ("rate","claim","fail","failures","failed_ids","n_pass","n_total","gate"):
    if k in d: print(k, d[k])
# find results list
for key in ("results","cases","items","details","per_case","rows"):
    if key in d:
        print("list_key", key, "len", len(d[key]))
        for r in d[key]:
            rid = str(r.get("id", r.get("case_id", r.get("name",""))))
            if "v27_11" in rid or r.get("ok") is False or r.get("pass") is False or r.get("passed") is False:
                pprint.pp(r)
                print("---")
