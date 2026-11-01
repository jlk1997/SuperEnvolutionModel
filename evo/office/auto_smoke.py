"""Real-folder auto (semi-automatic) smoke — CPU, no GPU.

After assist successes promote a family, mode=auto applies inside the sandbox
only for that family. Escape still refused. Everything audited.
Builds on shadow_smoke designated root (sandbox/ + outside/).
"""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from evo.computer.actions import format_call
from evo.computer.episode import run_episode
from evo.computer.license import License
from evo.office.auto_ledger import LEDGER_NAME, eligible_families, record_success
from evo.office.shadow_smoke import (
    AUDIT_NAME,
    DEFAULT_ROOT,
    OUT_NAME,
    OUT_TEXT,
    OUTSIDE_NAME,
    SANDBOX_NAME,
    SEED_NAME,
    SEED_TEXT,
    designated_root,
)
from evo.util import repo_path


def _scripted_write(path: str, text: str):
    state = {"done": False}

    def reply(_messages):
        if state["done"]:
            return format_call("finish", {"answer": "done"})
        state["done"] = True
        return format_call("write_file", {"path": path, "text": text})

    return reply


def _license(mode: str, auto_families: set[str] | None = None) -> License:
    return License(
        grants={"python", "shell", "read", "write", "http"},
        mode=mode,
        auto_families=auto_families or set(),
        max_steps=3,
    )


def _run(workspace: Path, mode: str, family: str, path: str, text: str, task_id: str, auto_families: set[str] | None = None) -> dict:
    audit = workspace / AUDIT_NAME
    task = {
        "id": task_id,
        "family": family,
        "prompt": f"Write {path}",
        "check": lambda ws, p=path: (ws / p).is_file() if ".." not in p.replace("\\", "/") else False,
    }
    return run_episode(
        task,
        _scripted_write(path, text),
        workspace,
        _license(mode, auto_families),
        audit_path=audit,
    )


def _audit_rows(workspace: Path) -> list[dict]:
    path = workspace / AUDIT_NAME
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def prepare(root: Path) -> tuple[Path, Path]:
    root.mkdir(parents=True, exist_ok=True)
    sandbox = root / SANDBOX_NAME
    outside = root / OUTSIDE_NAME
    if sandbox.exists():
        shutil.rmtree(sandbox)
    sandbox.mkdir(parents=True, exist_ok=True)
    outside.mkdir(parents=True, exist_ok=True)
    escape = outside / "escape.txt"
    if escape.exists():
        escape.unlink()
    (sandbox / SEED_NAME).write_text(SEED_TEXT, encoding="utf-8")
    ledger = root / LEDGER_NAME
    if ledger.exists():
        ledger.unlink()
    return sandbox, outside


def run_auto_smoke(root: Path | None = None, write_evidence: bool = True, min_n: int = 1) -> dict[str, Any]:
    base = designated_root(root if root is not None else repo_path(DEFAULT_ROOT))
    sandbox, outside = prepare(base)
    ledger_path = base / LEDGER_NAME

    # 1) Auto without promotion: family refused, no durable write
    cold = _run(sandbox, "auto", "report", OUT_NAME, OUT_TEXT, "auto-cold", auto_families=set())
    cold_rows = [r for r in _audit_rows(sandbox) if r.get("task") == "auto-cold"]
    write_cold = [r for r in cold_rows if r.get("name") == "write_file"]
    cold_ok = (
        cold["ok"] is False
        and not (sandbox / OUT_NAME).exists()
        and bool(write_cold)
        and any("family" in (r.get("refused") or []) for r in write_cold)
        and all(not r.get("applied") for r in write_cold)
    )

    # 2) Assist success then promote via ledger (semi-auto accept pattern)
    assist = _run(sandbox, "assist", "report", OUT_NAME, OUT_TEXT, "assist-promote", auto_families=None)
    assist_ok = assist["ok"] is True and (sandbox / OUT_NAME).is_file()
    if assist_ok:
        record_success(ledger_path, "report", n=1)
    promoted = eligible_families(ledger_path=ledger_path, audit_path=sandbox / AUDIT_NAME, min_n=min_n)
    promote_ok = "report" in promoted

    # Reset out.txt so auto leg must re-apply
    out_path = sandbox / OUT_NAME
    if out_path.exists():
        out_path.unlink()

    # 3) Auto with promoted family: apply inside sandbox, audit applied=true
    hot = _run(sandbox, "auto", "report", OUT_NAME, OUT_TEXT, "auto-hot", auto_families=promoted)
    hot_rows = [r for r in _audit_rows(sandbox) if r.get("task") == "auto-hot"]
    hot_ok = (
        hot["ok"] is True
        and out_path.is_file()
        and any(r.get("applied") and r.get("name") == "write_file" for r in hot_rows)
    )

    # 4) Auto still refuses unpromoted family (table) even after report promote
    other = _run(sandbox, "auto", "table", "table_out.txt", "nope", "auto-other", auto_families=promoted)
    other_rows = [r for r in _audit_rows(sandbox) if r.get("task") == "auto-other"]
    other_ok = (
        other["ok"] is False
        and not (sandbox / "table_out.txt").exists()
        and any("family" in (r.get("refused") or []) for r in other_rows if r.get("name") == "write_file")
    )

    # 5) Escape blocked in auto (even for promoted family)
    escape_rel = f"../{OUTSIDE_NAME}/escape.txt"
    esc = _run(sandbox, "auto", "report", escape_rel, "pwned", "auto-escape", auto_families=promoted)
    esc_rows = [r for r in _audit_rows(sandbox) if r.get("task") == "auto-escape"]
    escape_ok = (
        not (outside / "escape.txt").exists()
        and any("path" in (r.get("refused") or []) for r in esc_rows if r.get("name") == "write_file")
        and all(not r.get("applied") for r in esc_rows if r.get("name") == "write_file")
    )

    passed = bool(cold_ok and assist_ok and promote_ok and hot_ok and other_ok and escape_ok)

    evidence: dict[str, Any] = {
        "kind": "auto_smoke",
        "gate": "0.6",
        "actor": "scripted",
        "gpu": False,
        "vl": False,
        "root": str(base),
        "sandbox": str(sandbox),
        "outside": str(outside),
        "timestamp": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "min_n": min_n,
        "promoted_families": sorted(promoted),
        "contracts": {
            "auto_cold_refused": cold_ok,
            "assist_promote": assist_ok and promote_ok,
            "auto_hot_applies": hot_ok,
            "auto_other_family_refused": other_ok,
            "auto_escape_blocked": escape_ok,
            "audit_present": (sandbox / AUDIT_NAME).is_file(),
        },
        "pass": passed,
        "notes": (
            "Assist→auto: promote after audited assist success; "
            "auto applies only promoted families inside sandbox; "
            "D still deferred (no VL). Never reopen burned seals."
        ),
    }

    if write_evidence:
        out = base / "auto_evidence.json"
        out.write_text(json.dumps(evidence, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
        docs = repo_path("docs") / "AUTO_SMOKE_2026-10-18.json"
        docs.write_text(json.dumps(evidence, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
        evidence["evidence_path"] = str(out)
        evidence["docs_path"] = str(docs)

    return evidence


def main() -> None:
    evidence = run_auto_smoke()
    print(json.dumps(evidence, ensure_ascii=True), flush=True)
    if not evidence.get("pass"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
