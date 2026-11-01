# -*- coding: utf-8 -*-
from __future__ import annotations
import subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable
STEPS = [
    "scripts/c107_vision_v4_heldout_multihop.py",
    "scripts/c108_u2c_absorb_lora_honest.py",
    "scripts/c109_ant_capture_office_cli.py",
    "scripts/c110_replace_agent_harder_cost.py",
    "scripts/c111_gen11_hold.py",
    "scripts/c112_docs_stage_checkpoint.py",
]
def main():
    results = []
    for rel in STEPS:
        print("=" * 60, flush=True); print("RUN", rel, flush=True)
        rc = subprocess.call([PY, str(ROOT / rel)], cwd=str(ROOT))
        results.append({"script": rel, "rc": rc}); print("RC", rc, flush=True)
    print("SUMMARY", results, flush=True)
    bad = [r for r in results if r["rc"] not in (0,) and "c112" not in r["script"] and "c111" not in r["script"]]
    return 0 if not bad else 1
if __name__ == "__main__":
    raise SystemExit(main())
