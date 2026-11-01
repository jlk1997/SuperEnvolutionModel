# -*- coding: utf-8 -*-
"""Run C83-C90 in order. GPU steps sequential."""
from __future__ import annotations
import subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable
STEPS = [
    "scripts/c83_vision_ocr_weak_fixtures.py",
    "scripts/c84_vision_ocr_weak_bare_smoke.py",
    "scripts/c85_vision_ocr_weak_lora_absorb.py",
    "scripts/c86_vision_ocr_weak_lora_vs_bare.py",
    "scripts/c87_e2e_vision_office_loop.py",
    "scripts/c88_user_sandbox_shadow_u2c.py",
    "scripts/c89_gen11_hold.py",
    "scripts/c90_docs_checkpoint.py",
]

def main():
    for rel in STEPS:
        print("=" * 60, flush=True)
        print("RUN", rel, flush=True)
        r = subprocess.run([PY, str(ROOT / rel)], cwd=str(ROOT))
        if r.returncode != 0:
            print("FAIL", rel, "code", r.returncode, flush=True)
            sys.exit(r.returncode)
        print("OK", rel, flush=True)
    print("BATCH_C83_C90_DONE", flush=True)

if __name__ == "__main__":
    main()
