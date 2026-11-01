# -*- coding: utf-8 -*-
from pathlib import Path
import sys
ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else r"E:\envolution")
SCR = ROOT / "scripts"

# C264 from c258
s = (SCR / "c258_capture_office_regression.py").read_text(encoding="utf-8")
s = s.replace("C258", "C264").replace("c258", "c264")
# Point regression at V26 as latest + keep prior
s = s.replace("vision_images_v25", "vision_images_v26")
s = s.replace("V25", "V26").replace("v25", "v26")
# Also ensure V4-V26 pointers if hardcoded list exists
(SCR / "c264_capture_office_regression.py").write_text(s, encoding="utf-8")
print("wrote c264")

# C265 from c259
t = (SCR / "c259_scorecard_and_stage.py").read_text(encoding="utf-8")
t = t.replace("C259", "C265").replace("c259", "c265")
t = t.replace("C254-C258", "C260-C264").replace("C254", "C260").replace("C255", "C261")
t = t.replace("C256", "C262").replace("C257", "C263").replace("C258", "C264")
t = t.replace("V25", "V26").replace("v25", "v26").replace("V24", "V25").replace("v24", "v25")
# Fix: after V24->V25 and V25->V26, old V24 became V25 and old V25 became V26.
# We want scorecard to show both V25 and V26. Need to carefully rebuild vision section.
# Re-read original and write a clean C265 instead.
src = (SCR / "c259_scorecard_and_stage.py").read_text(encoding="utf-8")
# Keep fresh rewrite below
