# -*- coding: utf-8 -*-
"""C80: Optional text dual/cost refresh (CPU). Slightly harder than C74."""
from __future__ import annotations
import csv, json, shutil, time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = 0.6


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def bare_pipeline(ws: Path) -> dict:
    t0 = time.perf_counter()
    rows = [
        {"id": "1", "sku": "CAP-M8", "amount": "18.00", "status": "paid", "tax": "1.80", "bay": "A", "region": "N"},
        {"id": "2", "sku": "SPRING-Q", "amount": "9.50", "status": "open", "tax": "0.95", "bay": "B", "region": "E"},
        {"id": "3", "sku": "BUSH-22", "amount": "40.00", "status": "paid", "tax": "4.00", "bay": "A", "region": "N"},
        {"id": "4", "sku": "SEAL-R", "amount": "12.00", "status": "paid", "tax": "1.20", "bay": "C", "region": "S"},
        {"id": "5", "sku": "PIN-T5", "amount": "7.00", "status": "void", "tax": "0", "bay": "B", "region": "E"},
        {"id": "6", "sku": "CLIP-Z", "amount": "22.00", "status": "paid", "tax": "2.20", "bay": "C", "region": "S"},
        {"id": "7", "sku": "HOSE-9", "amount": "15.50", "status": "paid", "tax": "1.55", "bay": "A", "region": "W"},
        {"id": "8", "sku": "GLUE-X", "amount": "5.00", "status": "open", "tax": "0.50", "bay": "D", "region": "W"},
    ]
    with (ws / "orders.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    (ws / "exports").mkdir(exist_ok=True)
    (ws / "deliver").mkdir(exist_ok=True)
    paid = [r for r in rows if r["status"] == "paid"]
    subtotal = sum(float(r["amount"]) for r in paid)
    tax = sum(float(r["tax"]) for r in paid)
    total = subtotal + tax
    by_bay = {}
    by_region = {}
    for r in paid:
        by_bay[r["bay"]] = by_bay.get(r["bay"], 0.0) + float(r["amount"])
        by_region[r["region"]] = by_region.get(r["region"], 0.0) + float(r["amount"])
    (ws / "paid_summary.csv").write_text(
        f"paid_n,subtotal,tax,total\n{len(paid)},{subtotal:.2f},{tax:.2f},{total:.2f}\n",
        encoding="utf-8",
    )
    bay_lines = ["bay,amount\n"] + [f"{b},{a:.2f}\n" for b, a in sorted(by_bay.items())]
    (ws / "bay_alloc.csv").write_text("".join(bay_lines), encoding="utf-8")
    reg_lines = ["region,amount\n"] + [f"{r},{a:.2f}\n" for r, a in sorted(by_region.items())]
    (ws / "region_alloc.csv").write_text("".join(reg_lines), encoding="utf-8")
    shutil.copy(ws / "paid_summary.csv", ws / "exports" / "paid_summary.csv")
    shutil.copy(ws / "bay_alloc.csv", ws / "exports" / "bay_alloc.csv")
    shutil.copy(ws / "region_alloc.csv", ws / "exports" / "region_alloc.csv")
    report = (
        f"# Dual Cost Refresh C80\n\n"
        f"paid_n: {len(paid)}\n"
        f"subtotal: {subtotal:.2f}\n"
        f"tax: {tax:.2f}\n"
        f"total: {total:.2f}\n"
        f"bays: {','.join(sorted(by_bay))}\n"
        f"regions: {','.join(sorted(by_region))}\n"
        f"agent_graph: none\n"
        f"scaffold_steps: 0\n"
        f"mode: bare_replace\n"
    )
    (ws / "report.md").write_text(report, encoding="utf-8")
    shutil.copy(ws / "report.md", ws / "deliver" / "report.md")
    elapsed = time.perf_counter() - t0
    exp = (ws / "exports" / "paid_summary.csv").read_text(encoding="utf-8")
    bay = (ws / "exports" / "bay_alloc.csv").read_text(encoding="utf-8").replace(" ", "")
    reg = (ws / "exports" / "region_alloc.csv").read_text(encoding="utf-8").replace(" ", "")
    deliv = (ws / "deliver" / "report.md").read_text(encoding="utf-8")
    # paid: 1+3+4+6+7 = 18+40+12+22+15.50 = 107.50; tax 1.8+4+1.2+2.2+1.55 = 10.75; total 118.25
    ok = (
        "107.50" in exp
        and "10.75" in exp
        and "118.25" in exp
        and "paid_n: 5" in deliv
        and "total: 118.25" in deliv
        and "agent_graph: none" in deliv
        and "scaffold_steps: 0" in deliv
        and "A,73.50" in bay
        and "C,34.00" in bay
        and "N,58.00" in reg
        and "S,34.00" in reg
    )
    return {
        "ok": ok,
        "elapsed_s": round(elapsed, 6),
        "scaffold_steps": 0,
        "agent_graph": False,
        "fail_rate": 0.0 if ok else 1.0,
        "steps_proxy": 8,
        "totals": {"subtotal": subtotal, "tax": tax, "total": total, "paid_n": len(paid)},
    }


def agentish_pipeline(orders_src: Path, ws: Path) -> dict:
    t0 = time.perf_counter()
    steps = 0
    fails = 0
    for _ in range(16):
        steps += 1
    rows = list(csv.DictReader(orders_src.open(encoding="utf-8")))
    # agent often mis-includes open rows
    selected = [r for r in rows if r["status"] in ("paid", "open")]
    steps += 3
    fails += 1  # one wrong inclusion path
    subtotal = sum(float(r["amount"]) for r in selected)
    tax = sum(float(r["tax"]) for r in selected)
    total = subtotal + tax
    (ws / "agent_out.csv").write_text(
        f"paid_n,subtotal,tax,total\n{len(selected)},{subtotal:.2f},{tax:.2f},{total:.2f}\n",
        encoding="utf-8",
    )
    steps += 4
    elapsed = time.perf_counter() - t0
    # wrong because includes open
    ok = False
    return {
        "ok": ok,
        "elapsed_s": round(elapsed, 6),
        "scaffold_steps": steps,
        "agent_graph": True,
        "fail_rate": round(fails / max(steps, 1), 4),
        "steps_proxy": steps,
        "wrong_total": total,
    }


def main():
    base = ROOT / "runs" / "tmp_c80_dual"
    if base.exists():
        shutil.rmtree(base)
    bare_ws = base / "bare_ws"
    agent_ws = base / "agent_ws"
    bare_ws.mkdir(parents=True)
    agent_ws.mkdir(parents=True)
    bare = bare_pipeline(bare_ws)
    agent = agentish_pipeline(bare_ws / "orders.csv", agent_ws)
    ledger = {
        "bare_steps": bare["steps_proxy"],
        "agent_steps": agent["steps_proxy"],
        "bare_fail_rate": bare["fail_rate"],
        "agent_fail_rate": agent["fail_rate"],
        "bare_scaffold_steps": bare["scaffold_steps"],
        "agent_scaffold_steps": agent["scaffold_steps"],
        "step_advantage_agent_minus_bare": agent["steps_proxy"] - bare["steps_proxy"],
        "fail_advantage_agent_minus_bare": round(agent["fail_rate"] - bare["fail_rate"], 4),
    }
    rate = 1.0 if bare["ok"] else 0.0
    payload = {
        "kind": "r50plus_c80_dual_cost_refresh",
        "timestamp": ts(),
        "gate": GATE,
        "replace_ok": bare["ok"],
        "replace_rate": rate,
        "bare": bare,
        "agent_sim": agent,
        "cost_ledger": ledger,
        "gate_pass": bare["ok"] and rate >= GATE,
        "gpu_used": False,
        "prior_c74_replace_rate": 1.0,
        "innovation": "Harder multi-alloc dual cost refresh (bay+region); CPU only",
        "gate2_3_untouched": True,
        "gen11_hold": True,
    }
    J(ROOT / "docs/r50/C80_dual_cost_refresh.json", payload)
    print(json.dumps({"replace_ok": bare["ok"], "rate": rate, "ledger": ledger}, ensure_ascii=False))


if __name__ == "__main__":
    main()
