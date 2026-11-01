from pathlib import Path
import json
ROOT = Path(r"E:/envolution")
# TR fax hold 755 -> 748 (avoid 755->756 OCR)
p = ROOT / "tools/_v169_themes.json"
d = json.loads(p.read_text(encoding="utf-8"))
assert d["train"][15][2] == 755, d["train"][15]
d["train"][15] = [780, 764, 748]
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
for rel in ["scripts/c1121_vision_v169_design_and_batch.py", "tools/_build_v169.py"]:
    fp = ROOT / rel
    t = fp.read_text(encoding="utf-8")
    t2 = t.replace("pgC 755 drop", "pgC 748 drop").replace("[780, 764, 755]", "[780, 764, 748]")
    if t2 != t:
        fp.write_text(t2, encoding="utf-8")
        print("patched", rel)
    else:
        print("nochange", rel)
# rebuild train fixture for fax only via design re-run is heavier; patch SPECS expected already same (a+b)
# re-run design to refresh png for v169_16
print("themes fax", d["train"][15])
