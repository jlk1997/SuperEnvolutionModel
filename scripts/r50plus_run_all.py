# -*- coding: utf-8 -*-
"""Run R50+ cycles C58-C64 in order."""
from __future__ import annotations
import runpy, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
SCRIPTS=[
 "c58_softmatch_harden.py",
 "c59_vision_v2_fixtures.py",
 "c60_vision_u2c_lora.py",
 "c61_gen11_prep.py",
 "c62_replace_agent_board.py",
 "c63_vision_v2_smoke.py",
 "c64_docs_checkpoint.py",
]
for name in SCRIPTS:
    path=ROOT/"scripts"/name
    print(f"\n===== RUN {name} =====", flush=True)
    runpy.run_path(str(path), run_name="__main__")
print("\n===== ALL DONE =====", flush=True)
