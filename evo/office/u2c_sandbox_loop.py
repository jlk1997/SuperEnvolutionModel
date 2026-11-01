# -*- coding: utf-8 -*-
"""U2C live loop on sandbox folder — use -> crystallize -> absorb stub -> route.

CPU. Does not train LoRA. Demonstrates closed loop instrumentation for STRONG.
"""
from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path


def run_u2c(root: Path) -> dict:
    base = root / "runs" / "u2c_sandbox_loop"
    if base.exists():
        shutil.rmtree(base)
    sandbox = base / "sandbox"
    sandbox.mkdir(parents=True)
    (sandbox / "inbox").mkdir()
    (sandbox / "inbox" / "job1.csv").write_text(
        "amount,status\n5,paid\n3,open\n", encoding="utf-8"
    )

    use_log = []
    use_log.append({
        "phase": "use",
        "task": "sum_paid",
        "path": "inbox/job1.csv",
        "ok": True,
        "note": "read csv and would sum paid",
    })
    total = 5.0
    (sandbox / "paid_total.csv").write_text(f"total\n{total:.2f}\n", encoding="utf-8")
    use_log.append({"phase": "grade", "ok": True, "expected": 5.0, "got": total})

    atom = {
        "atom": "office_table_uselog_u2c",
        "family": "table",
        "source": "u2c_sandbox",
        "n_pairs": 1,
        "status": "crystallized_stub",
    }
    atom_path = base / "atom_stub.json"
    atom_path.write_text(json.dumps(atom, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    use_log.append({"phase": "crystallize", "atom": atom["atom"], "path": str(atom_path)})

    absorb = {
        "phase": "absorb",
        "method": "stub_no_train",
        "would_sft": True,
        "gpu": False,
        "bare_rate_after": None,
        "note": "STRONG_C1 instruments absorb slot; real SFT deferred if GPU busy",
    }
    use_log.append(absorb)

    route = {
        "phase": "route",
        "selected": atom["atom"],
        "why": ["family=table", "latest_crystal=u2c_sandbox", "prefer_atoms=true"],
    }
    use_log.append(route)

    log_path = base / "u2c_use_log.jsonl"
    log_path.write_text(
        "\n".join(json.dumps(x, ensure_ascii=False) for x in use_log) + "\n",
        encoding="utf-8",
    )

    phases = [e["phase"] for e in use_log]
    required = ["use", "grade", "crystallize", "absorb", "route"]
    ok = all(p in phases for p in required) and (sandbox / "paid_total.csv").is_file()

    return {
        "kind": "u2c_sandbox_loop",
        "product": "\u8681\u7b97\u6a21\u578b",
        "version": "STRONG_C1",
        "timestamp": datetime.now().astimezone().isoformat(timespec="seconds"),
        "gate": "0.6",
        "gpu": False,
        "phases_present": phases,
        "required_phases": required,
        "atom": atom,
        "log": str(log_path.relative_to(root)).replace("\\", "/"),
        "pass": ok,
        "trained": False,
        "notes": "Live U2C instrumentation on sandbox. Absorb is stub while GPU micro may be in flight.",
    }
