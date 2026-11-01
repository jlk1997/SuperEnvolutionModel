# -*- coding: utf-8 -*-
from pathlib import Path
import re

v33 = Path("scripts/c302_vision_v33_design_and_batch.py").read_text(encoding="utf-8")
v34 = Path("scripts/c308_vision_v34_design_and_batch.py").read_text(encoding="utf-8")

# Extract V33 body from after torn margin to before first overlay block
# Start: after "torn margin" polygon loop
start_marker = "    # torn margin serrations (left)\n    for ty in range(30, 590, 14):\n        d.polygon([(40, ty), (28, ty + 7), (40, ty + 14)], fill=bg)\n"
# Find first overlay in v33
ov = re.search(r"\n    # --- V\d+ overlays", v33)
if not ov:
    raise SystemExit("no overlay in v33")
# Get content between torn margin end and first overlay
tm = v33.find(start_marker)
if tm < 0:
    raise SystemExit("no torn margin")
body_start = tm + len(start_marker)
body_mid = v33[body_start: ov.start()]
# Also get from after ALL overlay blocks to ImageEnhance - the fingerprint etc.
# In V33, after last overlays there is fingerprint then noise then enhance
enhance = v33.find("    img = ImageEnhance.Color(img).enhance(0.84)")
# Find fingerprint section
fp = v33.find("    # fingerprint ovals", ov.start())
if fp < 0:
    raise SystemExit("no fingerprint")
post_overlay = v33[fp:enhance]

print("body_mid len", len(body_mid), "post", len(post_overlay))
print("body has lines draw", "enumerate(lines)" in body_mid or "for i, line" in body_mid)
# show keys in body_mid
for key in ["enumerate(lines)", "TOTAL PAID", "cn_title", "stamp", "watermark", "in_text_band"]:
    print(key, key in body_mid)

# Now rebuild v34 make_fixture:
# fonts + card + torn + body_mid + V34_OVERLAY + post_overlay + enhance..return

boot = Path("tools/_boot_v34_c308.py").read_text(encoding="utf-8")
overlay = re.search(r"V34_OVERLAY = r'''(.*?)'''", boot, re.S).group(1)

# Get v34 header of make_fixture through torn margin
mf_s = v34.find("def make_fixture")
mf_e = v34.find("\ndef main")
# Take from start of make_fixture through torn margin inclusive
head_end = v34.find(start_marker, mf_s) + len(start_marker)
head = v34[mf_s:head_end]

# Get enhance..end from current v34 (already correct)
enh = v34.find("    img = ImageEnhance.Color(img).enhance(0.84)", mf_s)
tail = v34[enh:mf_e]

# Retarget body_mid version tags lightly
body_mid = body_mid.replace("_v33", "_v34").replace("V33", "V34")

new_mf = head + body_mid + overlay + "\n\n" + post_overlay + tail
# Ensure in_text_band exists - used by overlay
if "def in_text_band" not in v34[:mf_s] and "def in_text_band" not in new_mf:
    # check module level
    if "def in_text_band" not in v34:
        raise SystemExit("missing in_text_band")

new_script = v34[:mf_s] + new_mf + v34[mf_e:]
# version in main
new_script = new_script.replace('"version": "v33"', '"version": "v34"')
assert "enumerate(lines)" in new_script or "for i, line" in new_script
assert "bamboo grain" in new_script
assert "buf = io.BytesIO()" in new_script
assert new_script.count("def make_fixture") == 1
compile(new_script, "c308", "exec")
Path("scripts/c308_vision_v34_design_and_batch.py").write_text(new_script, encoding="utf-8")
print("rebuilt make_fixture ok", len(new_script))
