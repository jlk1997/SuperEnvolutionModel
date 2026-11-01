# -*- coding: utf-8 -*-
from __future__ import annotations
import subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable
STEPS = [
    "scripts/c114_u2c_absorb_push_gate.py",
    "scripts/c115_harden_ant_capture.py",
    "scripts/c116_v5_design_and_batch.py",
    "scripts/c117_dissolve_cost_refresh.py",
    "scripts/c118_gen11_hold.py",
    "scripts/c119_docs_stage.py",
]
def main():
    results = []
    for rel in STEPS:
        print("=" * 60, flush=True)
        print("RUN", rel, flush=True)
        rc = subprocess.call([PY, str(ROOT / rel)], cwd=str(ROOT))
        results.append({"script": rel, "rc": rc})
        print("RC", rc, flush=True)
    print("SUMMARY", results, flush=True)
    soft = ("c118", "c119")
    bad = [r for r in results if r["rc"] != 0 and not any(s in r["script"] for s in soft)]
    return 0 if not bad else 1
if __name__ == "__main__":
    raise SystemExit(main())
