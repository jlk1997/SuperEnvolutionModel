# -*- coding: utf-8 -*-
from pathlib import Path
import re

v33 = Path("scripts/c302_vision_v33_design_and_batch.py").read_text(encoding="utf-8")
v34 = Path("scripts/c308_vision_v34_design_and_batch.py").read_text(encoding="utf-8")
boot = Path("tools/_boot_v34_c308.py").read_text(encoding="utf-8")
om = re.search(r"V34_OVERLAY = r'''(.*?)'''", boot, re.S)
overlay = om.group(1)
assert "bamboo grain" in overlay

# Extract from V33 the pipeline after overlays: from "img = ImageEnhance.Color" through end of make_fixture return
# Find last overlay end - use Color enhance as anchor
anchor = "    img = ImageEnhance.Color(img).enhance(0.84)"
idx = v33.find(anchor)
if idx < 0:
    raise SystemExit("no enhance anchor")
# find end of make_fixture (next \n\ndef )
end = v33.find("\n\ndef main():", idx)
tail = v33[idx:end]
# retarget V33 -> V34 in lesson strings inside tail if any
tail = tail.replace("V33 keeps floor", "V34 keeps floor")
tail = tail.replace('"version": "v33"', '"version": "v34"')  # not in tail

# In v34, replace from first V34 overlays through end of make_fixture with overlay + tail
m = re.search(
    r"\n    # --- V34 overlays \(new vs V33\) ---.*?(?=\n\ndef main\(\):)",
    v34,
    re.S,
)
if not m:
    # maybe broken already — find from overlays to def main
    m = re.search(r"\n    # --- V34 overlays.*? (?=\n\ndef main\(\):)", v34, re.S)
if not m:
    raise SystemExit("cannot find overlay..main span")

replacement = overlay + "\n\n" + tail
v34n = v34[: m.start()] + replacement + v34[m.end():]
# ensure SPECS/version still v34
assert "bamboo_recv" in v34n
assert "buf = io.BytesIO()" in v34n
assert "JPEG_Q = 60" in v34n
assert v34n.count("def make_fixture") == 1
assert v34n.count("def main") == 1
compile(v34n, "c308", "exec")
Path("scripts/c308_vision_v34_design_and_batch.py").write_text(v34n, encoding="utf-8")
print("restored pipeline", len(v34n))
