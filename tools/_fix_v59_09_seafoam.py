# -*- coding: utf-8 -*-
"""C462b: rename foam->seafoam to stop VL collapse; regenerate train fixture; retest smoke."""
from __future__ import annotations
import json, re, sys
from pathlib import Path

ROOT = Path(r"E:\envolution")
sys.path.insert(0, str(ROOT))

# patch design SPECS theme foam -> seafoam
p = ROOT / "scripts/c461_vision_v59_design_and_batch.py"
t = p.read_text(encoding="utf-8")
t2 = t.replace('"foam_po"', '"seafoam_po"')
t2 = t2.replace("'FOAM PO SHEET V59'", "'SEAFOAM PO SHEET V59'")
t2 = t2.replace("     'foam', \"PO\"),", "     'seafoam', \"PO\"),")
t2 = t2.replace(",foam,", ",seafoam,")
t2 = t2.replace("eddy_foam_gasket", "eddy_seafoam_gasket")
if t2 == t:
    print("WARN: design patch no-op?")
p.write_text(t2, encoding="utf-8")

# patch heldout similarly
hp = ROOT / "scripts/c463_vision_v59_heldout.py"
ht = hp.read_text(encoding="utf-8")
ht2 = ht.replace('"foam_po"', '"seafoam_po"')
ht2 = ht2.replace("'FOAM PO SHEET V59H'", "'SEAFOAM PO SHEET V59H'")
ht2 = ht2.replace("     'foam', \"PO\"),", "     'seafoam', \"PO\"),")
ht2 = ht2.replace("eddy_foam_gasket", "eddy_seafoam_gasket")
hp.write_text(ht2, encoding="utf-8")

# regenerate only v59_09 via importing make from design
import importlib.util
spec = importlib.util.spec_from_file_location("c461", p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
row = [s for s in mod.SPECS if s[0] == "v59_09"][0]
fid, kind, metric, expected, lines, cn_title, stamp = row
print("regen", fid, kind, expected, lines[0])
item = mod.make_fixture(fid, kind, lines, metric, expected, cn_title, stamp)
# update manifest item
man_path = mod.FIX / "manifest.json"
man = json.loads(man_path.read_text(encoding="utf-8"))
for it in man["items"]:
    if it["id"] == "v59_09":
        it.update({
            "kind": kind,
            "metric": metric,
            "expected": expected,
            "lines": lines,
            "cn_title": cn_title,
            "stamp": stamp,
            "path": str(Path(item["path"]).relative_to(ROOT)).replace("\\", "/") if "path" in item else it.get("path"),
        })
        # make_fixture return shape
        if isinstance(item, dict):
            for k in ("path", "kind", "lines", "expected", "metric"):
                if k in item:
                    it[k] = item[k]
        break
# ensure path relative
for it in man["items"]:
    if it["id"] == "v59_09":
        print("manifest09", it.get("kind"), it.get("path"), it.get("expected"))
man_path.write_text(json.dumps(man, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("ok regen")
