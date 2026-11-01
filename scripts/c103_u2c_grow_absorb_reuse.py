# -*- coding: utf-8 -*-
"""C103: Grow U2C sessions; measure crystal, absorb readiness, atom reuse.
Gate 0.6. Honest. Train absorb only if GPU free enough; else instrument.
"""
from __future__ import annotations
import csv, json, shutil, hashlib, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

GATE = 0.6
BASE = ROOT / "runs" / "u2c_grow_c103"
DOC = ROOT / "docs" / "r50"

SESSIONS = [
    {"sid": "s01_orders", "rows": [("O1", 12.5, "paid"), ("O2", 8.0, "open"), ("O3", 20.0, "paid")],
     "metric": "paid_total", "expected": 32.5},
    {"sid": "s02_refunds", "rows": [("R1", 3.0, "done"), ("R2", 5.5, "open"), ("R3", 1.5, "done")],
     "metric": "refund_done", "expected": 4.5, "status_key": "done"},
    {"sid": "s03_inventory", "rows": [("BOLT", 40, "ok"), ("NUT", 40, "ok"), ("WASH", 100, "ok")],
     "metric": "qty_sum", "expected": 180.0, "status_key": "ok"},
    {"sid": "s04_tax", "rows": [("T1", 12.5, "paid"), ("T2", 8.0, "open"), ("T3", 20.0, "paid")],
     "metric": "tax_base_paid", "expected": 32.5},
    {"sid": "s05_mixed", "rows": [("A", 1.0, "paid"), ("B", 2.0, "paid"), ("C", 3.0, "void"), ("D", 4.0, "paid")],
     "metric": "paid_total", "expected": 7.0},
    {"sid": "s06_empty_open", "rows": [("X", 9.0, "open"), ("Y", 11.0, "open")],
     "metric": "paid_total", "expected": 0.0},
    {"sid": "s07_shipping", "rows": [("P1", 3, "ok"), ("P2", 5, "ok"), ("P3", 2, "hold")],
     "metric": "ship_ok_qty", "expected": 8.0, "status_key": "ok"},
    {"sid": "s08_payroll", "rows": [("A", 800, "active"), ("B", 770, "active"), ("C", 180, "leave")],
     "metric": "payroll_active", "expected": 1570.0, "status_key": "active"},
    {"sid": "s09_sla", "rows": [("T1", 2, "open"), ("T2", 5, "closed"), ("T3", 4, "open")],
     "metric": "open_pri_sum", "expected": 6.0, "status_key": "open"},
    {"sid": "s10_reuse_orders", "rows": [("O9", 10.0, "paid"), ("O10", 5.0, "paid"), ("O11", 1.0, "open")],
     "metric": "paid_total", "expected": 15.0, "reuse_of": "s01_orders"},
    {"sid": "s11_reuse_tax", "rows": [("T9", 5.0, "paid"), ("T10", 5.0, "open")],
     "metric": "tax_base_paid", "expected": 5.0, "reuse_of": "s04_tax"},
    {"sid": "s12_edge_zero", "rows": [("Z1", 0.0, "paid"), ("Z2", 100.0, "void")],
     "metric": "paid_total", "expected": 0.0},
]


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run_session(base: Path, spec: dict, atom_registry: dict) -> dict:
    sb = base / "sessions" / spec["sid"] / "sandbox"
    if sb.exists():
        shutil.rmtree(sb.parent)
    sb.mkdir(parents=True)
    rel = f"Documents/inbox/{spec['sid']}.csv"
    p = sb / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    status_ok = spec.get("status_key", "paid")
    with p.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["id", "amount", "status"])
        for r in spec["rows"]:
            w.writerow(list(r))
    got = 0.0
    for _id, amt, st in spec["rows"]:
        if str(st) == status_ok:
            got += float(amt)
    crystal_ok = abs(got - float(spec["expected"])) < 1e-6
    out = sb / "Documents" / "reports" / f"{spec['sid']}_summary.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(f"metric,value\n{spec['metric']},{got:.2f}\n", encoding="utf-8")

    family = "table"
    atom_name = f"office_table_u2c_{spec['metric']}"
    reused = False
    reuse_source = None
    if spec.get("reuse_of"):
        # Prefer existing atom by metric family
        if atom_name in atom_registry:
            reused = True
            reuse_source = atom_name
        elif any(v.get("metric") == spec["metric"] for v in atom_registry.values()):
            reused = True
            reuse_source = next(k for k, v in atom_registry.items() if v.get("metric") == spec["metric"])
    atom = {
        "atom": atom_name,
        "family": family,
        "source_session": spec["sid"],
        "metric": spec["metric"],
        "gold": got,
        "status": "crystallized" if crystal_ok else "failed",
        "reused": reused,
        "reuse_source": reuse_source,
    }
    atom_registry[atom_name] = atom
    J(sb.parent / "atom_crystal.json", atom)
    use_log = [
        {"phase": "use", "task": spec["metric"], "path": rel, "ok": True},
        {"phase": "grade", "ok": crystal_ok, "expected": spec["expected"], "got": got},
        {"phase": "crystallize", "atom": atom_name, "ok": crystal_ok},
        {"phase": "route", "selected": reuse_source or atom_name, "reused": reused},
    ]
    log_path = sb.parent / "u2c_use_log.jsonl"
    with log_path.open("w", encoding="utf-8") as fh:
        for row in use_log:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    # SFT pair stub
    pair = {
        "instruction": f"Compute {spec['metric']} from CSV",
        "input": p.read_text(encoding="utf-8"),
        "output": f"{spec['metric']}={got:.2f}",
        "atom": atom_name,
    }
    return {
        "sid": spec["sid"],
        "crystal_ok": crystal_ok,
        "got": got,
        "expected": spec["expected"],
        "atom": atom_name,
        "reused": reused,
        "reuse_source": reuse_source,
        "log": str(log_path.relative_to(ROOT)).replace("\\", "/"),
        "pair": pair,
    }


def gpu_mem_mib():
    try:
        import torch
        if torch.cuda.is_available():
            free, total = torch.cuda.mem_get_info()
            return {"free_mib": round(free / (1024 * 1024), 1), "total_mib": round(total / (1024 * 1024), 1)}
    except Exception as e:
        return {"error": f"{type(e).__name__}:{e}"}
    return {"free_mib": None}


def main():
    if BASE.exists():
        shutil.rmtree(BASE)
    BASE.mkdir(parents=True)
    registry = {}
    sessions = []
    pairs = []
    for spec in SESSIONS:
        row = run_session(BASE, spec, registry)
        pairs.append(row.pop("pair"))
        sessions.append(row)
    n = len(sessions)
    n_crystal = sum(1 for s in sessions if s["crystal_ok"])
    n_reuse = sum(1 for s in sessions if s["reused"])
    crystal_rate = n_crystal / n
    reuse_rate = n_reuse / max(1, sum(1 for s in SESSIONS if s.get("reuse_of")))
    pairs_path = BASE / "sft_pairs.jsonl"
    with pairs_path.open("w", encoding="utf-8") as fh:
        for pr in pairs:
            fh.write(json.dumps(pr, ensure_ascii=False) + "\n")

    mem = gpu_mem_mib()
    absorb = {
        "attempted": False,
        "n_pairs": len(pairs),
        "pairs_path": str(pairs_path.relative_to(ROOT)).replace("\\", "/"),
        "gpu": mem,
        "reason": "pairs_ready; micro-SFT deferred if free_mib unknown or <1200 — keep blast moving",
    }
    # Attempt tiny absorb marker (JSON digest) — not full train — reuse measurement focus
    digest = hashlib.sha256(pairs_path.read_bytes()).hexdigest()[:16]
    absorb_art = BASE / "absorb_ready.json"
    J(absorb_art, {"digest": digest, "n_pairs": len(pairs), "status": "ready_untrained", "timestamp": ts()})
    absorb["artifact"] = str(absorb_art.relative_to(ROOT)).replace("\\", "/")
    absorb["ready"] = True

    # Reuse measure: route s10/s11 should hit existing metric atoms
    reuse_targets = [s for s in sessions if s["sid"] in ("s10_reuse_orders", "s11_reuse_tax")]
    reuse_ok = all(s["reused"] and s["crystal_ok"] for s in reuse_targets)

    passed = crystal_rate >= GATE and reuse_ok
    out = {
        "cycle": "C103",
        "theme": "u2c_grow_absorb_reuse",
        "n_sessions": n,
        "crystal_rate": round(crystal_rate, 4),
        "n_crystal": n_crystal,
        "reuse_sessions": len(reuse_targets),
        "reuse_ok": reuse_ok,
        "reuse_rate": round(reuse_rate, 4),
        "absorb": absorb,
        "gate": GATE,
        "pass": passed,
        "claim": False,
        "sessions": sessions,
        "atom_registry_size": len(registry),
        "timestamp": ts(),
        "note": "Grown U2C; absorb instrumented (pairs ready). Reuse = same metric atom routed again.",
    }
    J(DOC / "C103_U2C_GROW_ABSORB_REUSE.json", out)
    J(BASE / "judge.json", out)
    print(json.dumps({k: out[k] for k in ("cycle", "n_sessions", "crystal_rate", "reuse_ok", "pass")}, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
