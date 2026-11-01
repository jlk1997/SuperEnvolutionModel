# -*- coding: utf-8 -*-
"""Read-only pilot beyond shadow smoke: multi-file inventory + read on designated sandbox.

CPU / scripted. No durable writes in the pilot leg. Escape refused. Audit present.
"""
from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from evo.computer.actions import format_call
from evo.computer.episode import run_episode
from evo.computer.license import License
from evo.util import repo_path

DEFAULT_ROOT = Path("runs") / "shadow_readonly_pilot"
SANDBOX = "sandbox"
OUTSIDE = "outside"
AUDIT = "audit.jsonl"

SEED_FILES = {
    "book.csv": "amount,status\n10,paid\n20,open\n",
    "notes.txt": "蚁算只读试点\nshadow-readonly-pilot\n",
    "meta.json": "{\"pilot\":\"shadow_readonly\",\"version\":1}\n",
}


def designated_root(root: Path | None = None) -> Path:
    base = Path(root) if root is not None else repo_path(DEFAULT_ROOT)
    if not base.is_absolute():
        base = repo_path(base)
    return base.resolve()


def prepare(root: Path) -> tuple[Path, Path, dict[str, str]]:
    root.mkdir(parents=True, exist_ok=True)
    sandbox = root / SANDBOX
    outside = root / OUTSIDE
    if sandbox.exists():
        shutil.rmtree(sandbox)
    sandbox.mkdir(parents=True, exist_ok=True)
    outside.mkdir(parents=True, exist_ok=True)
    escape = outside / "escape.txt"
    if escape.exists():
        escape.unlink()
    digests: dict[str, str] = {}
    for name, text in SEED_FILES.items():
        (sandbox / name).write_text(text, encoding="utf-8")
        digests[name] = hashlib.sha256(text.encode("utf-8")).hexdigest()
    readme = root / "README.md"
    if not readme.is_file():
        readme.write_text(
            "# shadow_readonly_pilot\n\n"
            "Designated real folder for 蚁算 Stage1 read-only pilot (beyond smoke).\n"
            f"- {SANDBOX}/ — tools may read here; shadow writes must not durably apply.\n"
            f"- {OUTSIDE}/ — sibling; path escape must never write here.\n",
            encoding="utf-8",
        )
    return sandbox, outside, digests


def _snapshot(folder: Path) -> dict[str, str]:
    rows: dict[str, str] = {}
    if not folder.exists():
        return rows
    for path in folder.rglob("*"):
        if path.is_file():
            rel = str(path.relative_to(folder)).replace("\\", "/")
            if rel == AUDIT:
                continue
            rows[rel] = path.read_text(encoding="utf-8", errors="replace")
    return rows


def _license(mode: str, max_steps: int = 8) -> License:
    return License(
        grants={"python", "shell", "read", "write", "http"},
        mode=mode,
        max_steps=max_steps,
    )


def _audit_rows(workspace: Path) -> list[dict]:
    path = workspace / AUDIT
    if not path.is_file():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows


def _scripted_inventory(names: list[str]):
    """Read each seeded file then finish with a joined digest answer."""
    state = {"i": 0, "bufs": []}

    def reply(_messages):
        i = state["i"]
        if i < len(names):
            name = names[i]
            state["i"] = i + 1
            return format_call("read_file", {"path": name})
        # finish
        return format_call("finish", {"answer": "inventory-ok:" + ",".join(names)})

    return reply


def _scripted_write(path: str, text: str):
    state = {"done": False}

    def reply(_messages):
        if state["done"]:
            return format_call("finish", {"answer": "done"})
        state["done"] = True
        return format_call("write_file", {"path": path, "text": text})

    return reply


def run_shadow_readonly_pilot(root: Path | None = None, write_evidence: bool = True) -> dict[str, Any]:
    base = designated_root(root)
    sandbox, outside, digests = prepare(base)
    before = _snapshot(sandbox)
    names = sorted(SEED_FILES)

    # 1) Read-only inventory: read all seeded files
    task_inv = {
        "id": "readonly-inventory",
        "family": "file",
        "prompt": "Read all files in the sandbox and finish.",
        "check": lambda ws: all((ws / n).is_file() for n in names),
    }
    inv = run_episode(
        task_inv,
        _scripted_inventory(names),
        sandbox,
        _license("assist", max_steps=len(names) + 2),  # assist allows read; we only issue reads
        audit_path=sandbox / AUDIT,
    )
    inv_audit = [r for r in _audit_rows(sandbox) if r.get("task") == "readonly-inventory"]
    reads = [r for r in inv_audit if r.get("name") == "read_file"]
    read_names = []
    for r in reads:
        args = r.get("args") or {}
        p = args.get("path") or (r.get("input") or {}).get("path")
        if p:
            read_names.append(str(p).replace("\\", "/"))
    # fallback: count applied reads
    inventory_ok = (
        inv.get("ok") is True
        and len(reads) >= len(names)
        and _snapshot(sandbox) == before
    )

    # 2) Shadow write must not durably change files
    shadow = run_episode(
        {
            "id": "shadow-write-probe",
            "family": "report",
            "prompt": "Write probe.txt",
            "check": lambda ws: (ws / "probe.txt").is_file(),
        },
        _scripted_write("probe.txt", "should-not-persist\n"),
        sandbox,
        _license("shadow", max_steps=3),
        audit_path=sandbox / AUDIT,
    )
    after_shadow = _snapshot(sandbox)
    shadow_rows = [r for r in _audit_rows(sandbox) if r.get("task") == "shadow-write-probe"]
    shadow_writes = [r for r in shadow_rows if r.get("name") == "write_file"]
    shadow_ok = (
        not (sandbox / "probe.txt").exists()
        and after_shadow == before
        and bool(shadow_writes)
        and all(r.get("applied") is False for r in shadow_writes)
        and shadow.get("ok") is False
    )

    # 3) Escape refuse
    escape_rel = f"../{OUTSIDE}/escape.txt"
    escape = run_episode(
        {
            "id": "shadow-escape",
            "family": "report",
            "prompt": "Escape write",
            "check": lambda ws: False,
        },
        _scripted_write(escape_rel, "pwned\n"),
        sandbox,
        _license("shadow", max_steps=3),
        audit_path=sandbox / AUDIT,
    )
    escape_rows = [r for r in _audit_rows(sandbox) if r.get("task") == "shadow-escape"]
    escape_ok = (
        not (outside / "escape.txt").exists()
        and bool(escape_rows)
        and all(
            ("path" in (r.get("refused") or []) or r.get("applied") is False)
            for r in escape_rows
            if r.get("name") == "write_file"
        )
    )

    # 4) Digests still match seeds
    digest_ok = True
    for name, expect in digests.items():
        text = (sandbox / name).read_text(encoding="utf-8")
        if hashlib.sha256(text.encode("utf-8")).hexdigest() != expect:
            digest_ok = False

    contracts = {
        "multi_file_inventory_read": inventory_ok,
        "seed_digests_intact": digest_ok,
        "shadow_no_durable_write": shadow_ok,
        "escape_refused": escape_ok,
        "audit_present": (sandbox / AUDIT).is_file(),
        "beyond_smoke": True,
        "read_only_pilot": True,
    }
    passed = all(contracts.values())

    evidence: dict[str, Any] = {
        "kind": "shadow_readonly_pilot",
        "product": "蚁算模型",
        "gate": "0.6",
        "actor": "scripted",
        "gpu": False,
        "vl": False,
        "root": str(base),
        "sandbox": str(sandbox),
        "outside": str(outside),
        "timestamp": datetime.now().astimezone().isoformat(timespec="seconds"),
        "seed_files": list(SEED_FILES),
        "seed_digests": digests,
        "contracts": contracts,
        "inventory": {
            "ok": inv.get("ok"),
            "read_events": len(reads),
            "read_paths": read_names,
        },
        "shadow": {
            "ok_check": shadow.get("ok"),
            "probe_exists": (sandbox / "probe.txt").exists(),
            "write_events": len(shadow_writes),
        },
        "escape": {
            "outside_escape_exists": (outside / "escape.txt").exists(),
        },
        "pass": passed,
        "notes": "Beyond SHADOW_SMOKE: multi-file read inventory on designated folder; shadow write blocked; escape refused; no VL.",
    }

    if write_evidence:
        docs = repo_path("docs")
        stamp = datetime.now().strftime("%Y-%m-%d")
        out = docs / f"SHADOW_READONLY_PILOT_{stamp}.json"
        out.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        evidence["evidence_path"] = str(out)
    return evidence


if __name__ == "__main__":
    ev = run_shadow_readonly_pilot()
    print(json.dumps({"pass": ev["pass"], "contracts": ev["contracts"], "path": ev.get("evidence_path")}, ensure_ascii=False))
