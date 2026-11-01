from pathlib import Path
import json, re
p = Path("scripts/c310_vision_v34_heldout.py")
t = p.read_text(encoding="utf-8")
t2 = t.replace("_v33hc274", "_v34hc310")
t2 = t2.replace('"version": "v33h"', '"version": "v34h"')
t2 = t2.replace("vision_images_v33h", "vision_images_v34h")
if t2 != t:
    p.write_text(t2, encoding="utf-8")
    print("patched c310 leftovers")
else:
    print("c310 already clean")
for m in re.finditer(r"^(FIX|IMG|OUT|DOC|RUN|PROTO|JPEG|FIXTURE|ROOT).*=.*", t2, re.M):
    print(m.group(0)[:160])
c = json.load(open("docs/r50/C309b_VISION_GATE_V34_CLAIM.json", encoding="utf-8"))
print("claim", {k: c.get(k) for k in ["kind","rate","n_ok","vl_gate_v34_claim","cycle"]})
if c.get("kind") != "vision_gate_v34_claim":
    c["kind"] = "vision_gate_v34_claim"
    json.dump(c, open("docs/r50/C309b_VISION_GATE_V34_CLAIM.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("normalized claim kind")
sm = json.load(open("docs/r50/C309_VISION_V34_SMOKE.json", encoding="utf-8"))
print("smoke", sm.get("rate"), sm.get("n_ok"), sm.get("gate_pass"))
# check heldout script SPECS ids
ids = re.findall(r'"id"\s*:\s*"(v34h_\d+)"', t2)
print("heldout ids", ids[:5], "... n=", len(ids))
print("fixture v34h count", len(list(Path("evo/office/fixtures/vision_images_v34h").glob("*"))))
