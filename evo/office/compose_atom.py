# -*- coding: utf-8 -*-
"""Cross-family compose atom — innovation for Ant STRONG.

Compose chains two office families without a hand-written agent graph:
  table+file | report+shell | file+report

CPU / scripted gold path for smoke. Router emits evidence chain.
"""
from __future__ import annotations

import csv
import json
import shutil
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Callable


COMPOSE_SPECS = {
    "table_file_report": {"families": ["table","file","report"], "desc": "Sum paid, export, report"},
    "table_file": {
        "families": ["table", "file"],
        "desc": "Sum paid rows then copy result file to exports/",
    },
    "report_shell": {
        "families": ["report", "shell"],
        "desc": "Write markdown report then shell-copy to deliver/",
    },
    "file_report": {
        "families": ["file", "report"],
        "desc": "Collect marker files then write inventory report",
    },
}


@dataclass
class ComposeEvidence:
    why: list[str] = field(default_factory=list)
    atoms: list[str] = field(default_factory=list)
    steps_ok: list[bool] = field(default_factory=list)


def route_compose(task_kind: str) -> ComposeEvidence:
    ev = ComposeEvidence()
    spec = COMPOSE_SPECS[task_kind]
    ev.why.append(f"compose_kind={task_kind}")
    ev.why.append(f"families={','.join(spec['families'])}")
    for fam in spec["families"]:
        atom = f"office_{fam}_uselog"
        ev.atoms.append(atom)
        ev.why.append(f"select_atom={atom} because family={fam} in compose chain")
    return ev


def _setup_table_file(ws: Path) -> Callable[[], bool]:
    rows = [
        {"id": "r1", "amount": "10", "status": "paid"},
        {"id": "r2", "amount": "20", "status": "open"},
        {"id": "r3", "amount": "7", "status": "paid"},
    ]
    with (ws / "orders.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["id", "amount", "status"])
        w.writeheader()
        w.writerows(rows)
    (ws / "exports").mkdir(exist_ok=True)

    def gold() -> bool:
        total = sum(float(r["amount"]) for r in rows if r["status"] == "paid")
        (ws / "paid_total.csv").write_text(f"total\n{total:.2f}\n", encoding="utf-8")
        src = ws / "paid_total.csv"
        dst = ws / "exports" / "paid_total.csv"
        dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
        return dst.is_file() and abs(float(dst.read_text(encoding="utf-8").strip().splitlines()[-1]) - 17.0) < 0.01

    return gold


def _setup_report_shell(ws: Path) -> Callable[[], bool]:
    (ws / "deliver").mkdir(exist_ok=True)

    def gold() -> bool:
        body = "# Weekly\n\nstatus: ok\ncount: 3\n"
        (ws / "report.md").write_text(body, encoding="utf-8")
        dst = ws / "deliver" / "report.md"
        dst.write_text(body, encoding="utf-8")
        return dst.is_file() and "status: ok" in dst.read_text(encoding="utf-8")

    return gold


def _setup_file_report(ws: Path) -> Callable[[], bool]:
    (ws / "inbox").mkdir(exist_ok=True)
    for name in ("a.marker", "b.marker", "skip.txt"):
        (ws / "inbox" / name).write_text("x\n", encoding="utf-8")

    def gold() -> bool:
        markers = sorted(p.name for p in (ws / "inbox").glob("*.marker"))
        report = "# Inventory\n\n" + "\n".join(f"- {m}" for m in markers) + "\n"
        (ws / "inventory.md").write_text(report, encoding="utf-8")
        text = (ws / "inventory.md").read_text(encoding="utf-8")
        return "a.marker" in text and "b.marker" in text and "skip.txt" not in text

    return gold



def _setup_table_file_report(ws: Path) -> Callable[[], bool]:
    rows = [
        {"id": "r1", "amount": "10", "status": "paid"},
        {"id": "r2", "amount": "20", "status": "open"},
        {"id": "r3", "amount": "7", "status": "paid"},
    ]
    with (ws / "orders.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["id", "amount", "status"])
        w.writeheader()
        w.writerows(rows)
    (ws / "exports").mkdir(exist_ok=True)

    def gold() -> bool:
        total = sum(float(r["amount"]) for r in rows if r["status"] == "paid")
        (ws / "paid_total.csv").write_text(f"total\n{total:.2f}\n", encoding="utf-8")
        dst = ws / "exports" / "paid_total.csv"
        dst.write_text((ws / "paid_total.csv").read_text(encoding="utf-8"), encoding="utf-8")
        report = f"# Paid Summary\n\ntotal: {total:.2f}\nstatus: ok\n"
        (ws / "paid_report.md").write_text(report, encoding="utf-8")
        text = (ws / "paid_report.md").read_text(encoding="utf-8")
        return dst.is_file() and "total: 17.00" in text and "status: ok" in text

    return gold


SETTERS = {
    "table_file_report": _setup_table_file_report,
    "table_file": _setup_table_file,
    "report_shell": _setup_report_shell,
    "file_report": _setup_file_report,
}


def run_compose_smoke(root: Path) -> dict:
    base = root / "runs" / "compose_family_smoke"
    if base.exists():
        shutil.rmtree(base)
    base.mkdir(parents=True)
    results = []
    all_ok = True
    for kind in COMPOSE_SPECS:
        ws = base / kind
        ws.mkdir()
        evidence = route_compose(kind)
        gold = SETTERS[kind](ws)
        ok = False
        try:
            ok = bool(gold())
        except Exception as e:
            evidence.why.append(f"error={e}")
        evidence.steps_ok.append(ok)
        all_ok = all_ok and ok
        results.append({
            "compose": kind,
            "families": COMPOSE_SPECS[kind]["families"],
            "atoms": evidence.atoms,
            "why": evidence.why,
            "ok": ok,
        })
    return {
        "kind": "compose_family_smoke",
        "product": "\u8681\u7b97\u6a21\u578b",
        "innovation": "cross_family_compose_atom",
        "version": "STRONG_C1",
        "timestamp": datetime.now().astimezone().isoformat(timespec="seconds"),
        "gate": "0.6",
        "gpu": False,
        "n": len(results),
        "ok_n": sum(1 for r in results if r["ok"]),
        "rate": sum(1 for r in results if r["ok"]) / max(len(results), 1),
        "results": results,
        "pass": all_ok,
        "notes": "CPU gold-path compose with route evidence chain. Not a Gate2 rewrite.",
    }
