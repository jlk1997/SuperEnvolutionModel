# -*- coding: utf-8 -*-
"""Run C100→C106 blast in order. Prints per-cycle exit codes."""
from __future__ import annotations
import subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable
STEPS = [
    "scripts/c100_v4_protocol_register.py",
    "scripts/c101_vision_v4_multihop_claim.py",
    "scripts/c102_desktop_screenshot_office_e2e.py",
    "scripts/c103_u2c_grow_absorb_reuse.py",
    "scripts/c104_replace_agent_harder_mix.py",
    "scripts/c105_gen11_hold.py",
    "scripts/c106_docs_stage_checkpoint.py",
]


def main():
    results = []
    for rel in STEPS:
        print("=" * 60, flush=True)
        print("RUN", rel, flush=True)
        rc = subprocess.call([PY, str(ROOT / rel)], cwd=str(ROOT))
        results.append({"script": rel, "rc": rc})
        print("RC", rc, flush=True)
        # Continue even on soft fail for docs; hard-stop only if protocol missing
        if rel.endswith("c100_v4_protocol_register.py") and rc != 0:
            break
    print("=" * 60, flush=True)
    print("SUMMARY", results, flush=True)
    # final docs always attempted if not last
    bad = [r for r in results if r["rc"] not in (0,) and "c106" not in r["script"]]
    return 0 if not bad else 1


if __name__ == "__main__":
    raise SystemExit(main())
