# -*- coding: utf-8 -*-
from pathlib import Path
import re
docs = Path("docs")
good = docs / "蚁算_VL_GATE_V30_HELDOUT_PROTOCOL.md"
for p in docs.glob("*V30_HELDOUT*"):
    print("found", repr(p.name))
    if p.resolve() != good.resolve():
        good.write_text(p.read_text(encoding="utf-8"), encoding="utf-8")
        p.unlink()
        print("renamed ->", good.name)

for scr_name, pat, repl in [
    ("scripts/c286_vision_v30_heldout.py", r'PROTO = ROOT / "docs" / "[^"]+V30_HELDOUT[^"]+"',
     'PROTO = ROOT / "docs" / "蚁算_VL_GATE_V30_HELDOUT_PROTOCOL.md"'),
    ("scripts/c284_vision_v30_design_and_batch.py", r'PROTO = ROOT / "docs" / "[^"]+V30_PROTOCOL[^"]+"',
     'PROTO = ROOT / "docs" / "蚁算_VL_GATE_V30_PROTOCOL.md"'),
]:
    scr = Path(scr_name)
    t = scr.read_text(encoding="utf-8")
    t2, n = re.subn(pat, repl, t, count=1)
    scr.write_text(t2, encoding="utf-8")
    print(scr_name, "subs", n)

# ensure good protocol exists (heldout may already have written under wrong name)
if not good.is_file():
    # regenerate minimal from smoke protocol sibling
    smoke = docs / "蚁算_VL_GATE_V30_PROTOCOL.md"
    if smoke.is_file():
        txt = smoke.read_text(encoding="utf-8").replace("V30 Protocol", "V30 Heldout Protocol").replace("C284", "C286").replace("smoke", "heldout")
        good.write_text(txt, encoding="utf-8")
        print("wrote heldout protocol from smoke twin")

for p in sorted(docs.glob("*V30*")):
    print("keep", p.name)
