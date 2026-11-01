from pathlib import Path
import re
# parse_metric metrics
t=Path("evo/office/vision_metric_parse.py").read_text(encoding="utf-8")
print("=== parse_metric metrics ===")
for i,l in enumerate(t.splitlines(),1):
    if "metric" in l.lower() or l.strip().startswith("if ") or l.strip().startswith("elif ") or "def parse" in l:
        print(f"{i}:{l[:140]}")
print("=== C317 head ===")
c317=Path("scripts/c317_product_u2c_cost.py").read_text(encoding="utf-8")
print(c317[:800])
print("=== C318 head ===")
c318=Path("scripts/c318_capture_office_regression.py").read_text(encoding="utf-8")
print(c318[:500])
print("=== C315 SPECS metrics vs parse ===")
man=Path("evo/office/fixtures/vision_images_v35/manifest.json")
import json
m=json.loads(man.read_text(encoding="utf-8"))
metrics=sorted({it["metric"] for it in m["items"]})
print("train metrics", metrics)
# quick dry parse on expected via synthetic text
from evo.office.vision_metric_parse import parse_metric
for it in m["items"]:
    lines="\n".join(it["lines"])
    got, ok = parse_metric(lines, it["metric"], it["expected"])
    if not ok:
        print("FAIL parse", it["id"], it["metric"], it["expected"], "got", got)
print("dry parse done")
