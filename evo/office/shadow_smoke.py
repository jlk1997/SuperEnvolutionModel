"""Real-folder shadow smoke (CPU). Tools act only inside a designated sandbox.

Judge branch after Gate3 transfer: try a real folder in shadow mode before assist/auto.
Shadow = proposals logged to audit.jsonl, durable writes suppressed (apply=false).
Fence = relative paths only; `..` and absolute paths refused so a sibling outside/ stays untouched.
Assist leg proves measurable task success on the same folder. No GPU / no model actor.
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
from evo.util import repo_path


DEFAULT_ROOT = Path("runs") / "shadow_workspace"
SANDBOX_NAME = "sandbox"
OUTSIDE_NAME = "outside"
SEED_NAME = "book.csv"
SEED_TEXT = "amount,status\n10,paid\n"
OUT_NAME = "out.txt"
OUT_TEXT = "shadow-smoke-ok"
AUDIT_NAME = "audit.jsonl"


def designated_root(root: Path | None = None) -> Path:
    """Repo-relative real folder (not tempfile)."""
    base = Path(root) if root is not None else repo_path(DEFAULT_ROOT)
    if not base.is_absolute():
        base = repo_path(base)
    return base.resolve()


def prepare(root: Path) -> tuple[Path, Path]:
    """Create sandbox + outside sibling; reset sandbox contents; seed book.csv."""
    root.mkdir(parents=True, exist_ok=True)
    sandbox = root / SANDBOX_NAME
    outside = root / OUTSIDE_NAME
    if sandbox.exists():
        shutil.rmtree(sandbox)
    sandbox.mkdir(parents=True, exist_ok=True)
    outside.mkdir(parents=True, exist_ok=True)
    # clear prior escape attempts
    escape = outside / "escape.txt"
    if escape.exists():
        escape.unlink()
    (sandbox / SEED_NAME).write_text(SEED_TEXT, encoding="utf-8")
    readme = root / "README.md"
    if not readme.is_file():
        readme.write_text(
            "# shadow_workspace\\n\\n"
            "Designated real folder for Gate3 judge-branch shadow smoke.\\n"
            f"- {SANDBOX_NAME}/ — tools may act here (shadow: log only; assist: durable).\\n"
            f"- {OUTSIDE_NAME}/ — sibling; path escape must never write here.\\n"
            "CPU scripted smoke only until a model actor is explicitly scheduled.\\n",
            encoding="utf-8",
        )
    return sandbox, outside


def _snapshot_files(folder: Path) -> dict[str, str]:
    rows: dict[str, str] = {}
    if not folder.exists():
        return rows
    for path in folder.rglob("*"):
        if path.is_file():
            rel = str(path.relative_to(folder)).replace("\\", "/")
            if rel == AUDIT_NAME:
                continue
            rows[rel] = path.read_text(encoding="utf-8", errors="replace")
    return rows


def _scripted_write(path: str, text: str):
    state = {"done": False}

    def reply(_messages):
        if state["done"]:
            return format_call("finish", {"answer": "done"})
        state["done"] = True
        return format_call("write_file", {"path": path, "text": text})

    return reply


def _license(mode: str) -> License:
    return License(
        grants={"python", "shell", "read", "write", "http"},
        mode=mode,
        max_steps=3,
    )


def _run_write(workspace: Path, mode: str, path: str, text: str, task_id: str) -> dict:
    audit = workspace / AUDIT_NAME
    task = {
        "id": task_id,
        "family": "report",
        "prompt": f"Write {path}",
        "check": lambda ws, p=path: (ws / p).is_file() if ".." not in p.replace("\\", "/") else False,
    }
    return run_episode(task, _scripted_write(path, text), workspace, _license(mode), audit_path=audit)


def _audit_rows(workspace: Path) -> list[dict]:
    path = workspace / AUDIT_NAME
    if not path.is_file():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows


def run_shadow_smoke(root: Path | None = None, write_evidence: bool = True) -> dict[str, Any]:
    """Four contracts on one designated real folder. CPU / scripted. Returns evidence dict."""
    base = designated_root(root)
    sandbox, outside = prepare(base)
    before = _snapshot_files(sandbox)

    # 1) Shadow: propose out.txt — durable file must not appear; audit must log applied=false
    shadow = _run_write(sandbox, "shadow", OUT_NAME, OUT_TEXT, "shadow-write")
    after_shadow = _snapshot_files(sandbox)
    shadow_audit = _audit_rows(sandbox)
    shadow_proposals = [
        r for r in shadow_audit if r.get("name") == "write_file" and r.get("task") == "shadow-write"
    ]
    shadow_ok = (
        not (sandbox / OUT_NAME).exists()
        and after_shadow == before
        and bool(shadow_proposals)
        and all(r.get("applied") is False for r in shadow_proposals)
        and shadow["ok"] is False  # honest fail: check wants out.txt
    )

    # 2) Escape: ../outside/escape.txt refused; sibling untouched
    escape_rel = f"../{OUTSIDE_NAME}/escape.txt"
    escape = _run_write(sandbox, "shadow", escape_rel, "pwned\\n", "shadow-escape")
    escape_audit = [
        r for r in _audit_rows(sandbox) if r.get("task") == "shadow-escape"
    ]
    escape_ok = (
        not (outside / "escape.txt").exists()
        and bool(escape_audit)
        and all("path" in (r.get("refused") or []) for r in escape_audit if r.get("name") == "write_file")
        and all(r.get("applied") is False for r in escape_audit)
    )

    # 3) Assist: durable write + check pass on same sandbox
    assist = _run_write(sandbox, "assist", OUT_NAME, OUT_TEXT, "assist-write")
    assist_ok = (
        assist["ok"] is True
        and (sandbox / OUT_NAME).is_file()
        and (sandbox / OUT_NAME).read_text(encoding="utf-8") == OUT_TEXT
    )
    assist_rows = [r for r in _audit_rows(sandbox) if r.get("task") == "assist-write"]
    assist_applied = any(r.get("applied") is True and r.get("name") == "write_file" for r in assist_rows)

    passed = bool(shadow_ok and escape_ok and assist_ok and assist_applied and (sandbox / AUDIT_NAME).is_file())

    evidence: dict[str, Any] = {
        "kind": "shadow_smoke",
        "gate": "0.6",
        "actor": "scripted",
        "gpu": False,
        "vl": False,
        "root": str(base),
        "sandbox": str(sandbox),
        "outside": str(outside),
        "timestamp": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "contracts": {
            "shadow_no_durable_write": shadow_ok,
            "shadow_honest_fail": shadow["ok"] is False,
            "audit_present": (sandbox / AUDIT_NAME).is_file(),
            "escape_refused": escape_ok,
            "assist_task_success": assist_ok and assist_applied,
        },
        "shadow": {
            "ok_check": shadow["ok"],
            "changed": sorted(set(after_shadow) ^ set(before)),
            "proposals": len(shadow_proposals),
            "applied_any": any(r.get("applied") for r in shadow_proposals),
        },
        "escape": {
            "outside_escape_exists": (outside / "escape.txt").exists(),
            "refused_path": escape_ok,
            "audit_rows": len(escape_audit),
        },
        "assist": {
            "ok_check": assist["ok"],
            "out_exists": (sandbox / OUT_NAME).is_file(),
            "applied": assist_applied,
        },
        "pass": passed,
        "notes": (
            "Shadow mode on designated real folder; assist proves success; "
            "D still deferred (no VL weights). Never reopen burned seals."
        ),
    }

    if write_evidence:
        out = base / "evidence.json"
        out.write_text(json.dumps(evidence, ensure_ascii=True, indent=2) + "\\n", encoding="utf-8")
        docs = repo_path("docs") / "SHADOW_SMOKE_2026-10-18.json"
        docs.write_text(json.dumps(evidence, ensure_ascii=True, indent=2) + "\\n", encoding="utf-8")
        evidence["evidence_path"] = str(out)
        evidence["docs_path"] = str(docs)

    return evidence


def main() -> None:
    evidence = run_shadow_smoke()
    print(json.dumps(evidence, ensure_ascii=True), flush=True)
    if not evidence.get("pass"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
