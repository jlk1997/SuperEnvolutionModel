from pathlib import Path
import re
S = Path("scripts")
for n in [
    "c425_vision_v53_design_and_batch.py",
    "c426_vision_v53_smoke.py",
    "c427_vision_v53_heldout.py",
    "c428_confidence_gate_stretch.py",
    "c429_capture_office_regression.py",
    "c430_scorecard_and_stage.py",
]:
    t = (S / n).read_text(encoding="utf-8")
    compile(t, n, "exec")
    specs = len(re.findall(r'\("v53', t))
    left = sorted(set(re.findall(r"\b(?:v52|V52|C419|C420|C421|C422|C423|C424)\b", t)))
    print(n, "OK specs", specs, "left", left, "kelp", "kelp" in t)
print("all compile ok")
