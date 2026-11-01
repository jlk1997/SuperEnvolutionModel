# -*- coding: utf-8 -*-
from pathlib import Path
import json, shutil
ROOT = Path(r"E:\envolution")
SCR = ROOT / "scripts"
DOC = ROOT / "docs" / "r50"
REPLACEMENTS = [
    ('DOC / "C308_VISION_V33_DESIGN.json"', 'DOC / "C308_VISION_V34_DESIGN.json"'),
    ('DOC / "C309_VISION_V33_SMOKE.json"', 'DOC / "C309_VISION_V34_SMOKE.json"'),
    ('DOC / "C309b_VISION_GATE_V33_CLAIM.json"', 'DOC / "C309b_VISION_GATE_V34_CLAIM.json"'),
    ('"kind": "vision_gate_v33_claim"', '"kind": "vision_gate_v34_claim"'),
    ('DOC / "C310_VISION_V33_HELDOUT_SMOKE.json"', 'DOC / "C310_VISION_V34_HELDOUT_SMOKE.json"'),
    ('DOC / "C310b_VISION_GATE_V33_HELDOUT_CLAIM.json"', 'DOC / "C310b_VISION_GATE_V34_HELDOUT_CLAIM.json"'),
    ('"kind": "vision_gate_v33_heldout_claim"', '"kind": "vision_gate_v34_heldout_claim"'),
    ('runs/vision_v33h_c310', 'runs/vision_v34h_c310'),
    ('vision_images_v33h', 'vision_images_v34h'),
    ('vision_v33h_c310', 'vision_v34h_c310'),
]
FILES = [
    "c308_vision_v34_design_and_batch.py",
    "c309_vision_v34_smoke.py",
    "c310_vision_v34_heldout.py",
    "c311_dissolve_cost_shadow.py",
    "c312_capture_office_regression.py",
    "c313_scorecard_and_stage.py",
]
for name in FILES:
    p = SCR / name
    t = p.read_text(encoding="utf-8"); orig = t
    for a,b in REPLACEMENTS: t = t.replace(a,b)
    if name.startswith("c313"):
        for a,b in [
            ("C308_VISION_V33_DESIGN","C308_VISION_V34_DESIGN"),
            ("C309_VISION_V33_SMOKE","C309_VISION_V34_SMOKE"),
            ("C309b_VISION_GATE_V33_CLAIM","C309b_VISION_GATE_V34_CLAIM"),
            ("C310_VISION_V33_HELDOUT_SMOKE","C310_VISION_V34_HELDOUT_SMOKE"),
            ("C310b_VISION_GATE_V33_HELDOUT_CLAIM","C310b_VISION_GATE_V34_HELDOUT_CLAIM"),
        ]: t = t.replace(a,b)
    if t != orig:
        p.write_text(t, encoding="utf-8"); print("patched", name)
    else:
        print("ok-nochange", name)
    leaks=[ln.strip() for ln in t.splitlines() if ("VISION_V33" in ln or "GATE_V33" in ln or "vision_v33" in ln or "v33h" in ln) and "V33 overlays" not in ln and "vs V33" not in ln and "new vs V33" not in ln]
    if leaks:
        print(" remaining", len(leaks))
        for ln in leaks[:8]: print(" ", ln[:120])
pairs=[
 ("C308_VISION_V33_DESIGN.json","C308_VISION_V34_DESIGN.json"),
 ("C309_VISION_V33_SMOKE.json","C309_VISION_V34_SMOKE.json"),
 ("C309b_VISION_GATE_V33_CLAIM.json","C309b_VISION_GATE_V34_CLAIM.json"),
 ("C310_VISION_V33_HELDOUT_SMOKE.json","C310_VISION_V34_HELDOUT_SMOKE.json"),
 ("C310b_VISION_GATE_V33_HELDOUT_CLAIM.json","C310b_VISION_GATE_V34_HELDOUT_CLAIM.json"),
]
for src_name,dst_name in pairs:
    src,dst=DOC/src_name,DOC/dst_name
    if not src.exists(): continue
    sd=json.loads(src.read_text(encoding="utf-8")); rate=sd.get("rate")
    should=False
    if not dst.exists(): should=True
    else:
        dd=json.loads(dst.read_text(encoding="utf-8"))
        if (dd.get("rate") or 0) < (rate or 0): should=True
        elif (dd.get("rate")==0) and (rate and rate>=0.6): should=True
    if should:
        shutil.copy2(src,dst); print("synced", src_name, "->", dst_name, "rate", rate)
    else:
        print("keep", dst_name)
print("done")
