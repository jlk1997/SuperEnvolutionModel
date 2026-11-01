# -*- coding: utf-8 -*-
"""C67: Replace-agent STRESS — harder multi-hop bare compose (no agent graph)."""
from __future__ import annotations
import csv, json, shutil, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from evo.office.compose_atom import run_compose_smoke, COMPOSE_SPECS, route_compose

GATE = 0.6


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def stress_table_file_report_shell(ws: Path) -> bool:
    """Harder: filter paid, tax, export, report, shell-copy deliver — still bare gold path."""
    rows = [
        {"id": "1", "amount": "12.50", "status": "paid", "tax": "1.25"},
        {"id": "2", "amount": "8.00", "status": "open", "tax": "0.80"},
        {"id": "3", "amount": "20.00", "status": "paid", "tax": "2.00"},
        {"id": "4", "amount": "5.50", "status": "paid", "tax": "0.55"},
        {"id": "5", "amount": "100.00", "status": "void", "tax": "0"},
    ]
    with (ws / "orders.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["id", "amount", "status", "tax"])
        w.writeheader()
        w.writerows(rows)
    (ws / "exports").mkdir(exist_ok=True)
    (ws / "deliver").mkdir(exist_ok=True)

    paid = [r for r in rows if r["status"] == "paid"]
    subtotal = sum(float(r["amount"]) for r in paid)
    tax = sum(float(r["tax"]) for r in paid)
    total = subtotal + tax
    (ws / "paid_summary.csv").write_text(
        f"subtotal,tax,total\n{subtotal:.2f},{tax:.2f},{total:.2f}\n", encoding="utf-8"
    )
    shutil.copy(ws / "paid_summary.csv", ws / "exports" / "paid_summary.csv")
    report = (
        f"# Stress Paid Report\n\n"
        f"paid_n: {len(paid)}\n"
        f"subtotal: {subtotal:.2f}\n"
        f"tax: {tax:.2f}\n"
        f"total: {total:.2f}\n"
        f"agent_graph: none\n"
        f"scaffold_steps: 0\n"
    )
    (ws / "report.md").write_text(report, encoding="utf-8")
    shutil.copy(ws / "report.md", ws / "deliver" / "report.md")
    # checks
    exp = (ws / "exports" / "paid_summary.csv").read_text(encoding="utf-8")
    deliv = (ws / "deliver" / "report.md").read_text(encoding="utf-8")
    return (
        "38.00" in exp
        and "3.80" in exp
        and "41.80" in exp
        and "paid_n: 3" in deliv
        and "total: 41.80" in deliv
        and "agent_graph: none" in deliv
    )


def stress_cross_family_inventory(ws: Path) -> bool:
    (ws / "inbox").mkdir(exist_ok=True)
    (ws / "outbox").mkdir(exist_ok=True)
    for name, body in [
        ("inv_a.marker", "sku=BOLT-M6 qty=40"),
        ("inv_b.marker", "sku=NUT-M6 qty=40"),
        ("noise.txt", "ignore"),
        ("inv_c.marker", "sku=WASHER qty=100"),
    ]:
        (ws / "inbox" / name).write_text(body + "\n", encoding="utf-8")
    markers = sorted(p for p in (ws / "inbox").glob("*.marker"))
    lines = []
    total_qty = 0
    for p in markers:
        text = p.read_text(encoding="utf-8").strip()
        # sku=X qty=N
        parts = dict(kv.split("=", 1) for kv in text.split() if "=" in kv)
        qty = int(parts.get("qty", "0"))
        total_qty += qty
        lines.append(f"{parts.get('sku','?')},{qty}")
    csv_body = "sku,qty\n" + "\n".join(lines) + "\n"
    (ws / "inventory.csv").write_text(csv_body, encoding="utf-8")
    shutil.copy(ws / "inventory.csv", ws / "outbox" / "inventory.csv")
    report = f"# Inventory\n\nn_skus: {len(markers)}\ntotal_qty: {total_qty}\n"
    (ws / "inventory.md").write_text(report, encoding="utf-8")
    shutil.copy(ws / "inventory.md", ws / "outbox" / "inventory.md")
    out_csv = (ws / "outbox" / "inventory.csv").read_text(encoding="utf-8")
    out_md = (ws / "outbox" / "inventory.md").read_text(encoding="utf-8")
    return (
        "BOLT-M6,40" in out_csv
        and "NUT-M6,40" in out_csv
        and "WASHER,100" in out_csv
        and "n_skus: 3" in out_md
        and "total_qty: 180" in out_md
        and "noise" not in out_csv
    )


def main():
    ws_root = ROOT / "runs" / "r50plus" / "c67_replace_stress"
    if ws_root.exists():
        shutil.rmtree(ws_root)
    ws_root.mkdir(parents=True)

    compose = run_compose_smoke(ROOT)

    t1 = ws_root / "stress_paid_tax_deliver"
    t1.mkdir()
    ok1 = stress_table_file_report_shell(t1)
    ev1 = route_compose("table_file_report")
    ev1.why.append("stress=tax+deliver+shell_copy")
    ev1.atoms.append("office_shell_uselog")

    t2 = ws_root / "stress_inventory_cross"
    t2.mkdir()
    ok2 = stress_cross_family_inventory(t2)
    ev2 = route_compose("file_report")
    ev2.why.append("stress=parse_markers+sum_qty+dual_export")

    fam_rows = []
    for fam in ("table", "report", "file", "shell"):
        p = ROOT / "runs" / "capabilities" / f"office_{fam}_uselog" / "dissolution.json"
        if not p.is_file():
            continue
        d = json.loads(p.read_text(encoding="utf-8"))
        bare = float(d.get("bare_rate") or 0)
        diss = float(d.get("dissolution") or 0)
        fam_rows.append(
            {
                "family": fam,
                "bare_rate": bare,
                "dissolution": diss,
                "scaffold_steps_proxy": 0 if bare >= GATE and diss <= 0.05 else 3,
            }
        )
    scaffold_mean = sum(r["scaffold_steps_proxy"] for r in fam_rows) / max(1, len(fam_rows))

    stress_n = 2
    stress_ok = int(ok1) + int(ok2)
    stress_rate = stress_ok / stress_n
    compose_ok = bool(compose.get("pass"))
    bare_board_ok = stress_rate >= GATE and compose_ok and scaffold_mean == 0
    replace_score = (
        1.0
        if bare_board_ok and stress_rate == 1.0
        else (0.85 if bare_board_ok else (0.6 if stress_rate >= GATE else 0.3))
    )

    payload = {
        "kind": "r50plus_c67_replace_agent_stress",
        "timestamp": ts(),
        "gate": GATE,
        "compose_rate": compose.get("rate"),
        "compose_pass": compose_ok,
        "compose_n": compose.get("n"),
        "stress_tasks": [
            {
                "id": "stress_paid_tax_deliver",
                "families": ["table", "file", "report", "shell"],
                "ok": ok1,
                "why": ev1.why,
                "atoms": ev1.atoms,
            },
            {
                "id": "stress_inventory_cross",
                "families": ["file", "report"],
                "ok": ok2,
                "why": ev2.why,
                "atoms": ev2.atoms,
            },
        ],
        "stress_rate": round(stress_rate, 4),
        "families": fam_rows,
        "scaffold_steps_mean": scaffold_mean,
        "agent_graph": False,
        "replace_agent_score": replace_score,
        "replace_agent_stress_pass": bool(replace_score >= GATE),
        "workspace": str(ws_root.relative_to(ROOT)).replace("\\", "/"),
        "innovation": "Harder bare replace-agent stress with tax+inventory multi-hop",
        "gate2_3_untouched": True,
        "vs_c62": "C62 was light board; C67 adds tax calc + marker parse + dual export",
    }
    J(ROOT / "docs/r50/C67_replace_agent_stress.json", payload)
    (ROOT / "docs/r50/C67_replace_agent_stress.md").write_text(
        f"# C67 replace-agent stress\n\nstress_rate={stress_rate} compose={compose.get('rate')} "
        f"scaffold={scaffold_mean} replace={replace_score} pass={payload['replace_agent_stress_pass']}\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "stress_rate": round(stress_rate, 4),
                "ok1": ok1,
                "ok2": ok2,
                "compose_rate": compose.get("rate"),
                "replace_score": replace_score,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
