# -*- coding: utf-8 -*-
"""Write-guarded shadow pilot (蚁算 v0.2.5): beyond readonly — allowlisted durable writes only.

CPU / scripted. Sandbox designated folder. Explicit write allowlist.
Allowed writes persist; non-allowlisted and path-escape refused. Audit present.
"""
from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

from evo.computer.actions import format_call
from evo.computer.episode import run_episode
from evo.computer.license import License
from evo.util import repo_path

DEFAULT_ROOT = Path("runs") / "shadow_write_guarded_pilot"
SANDBOX = "sandbox"
OUTSIDE = "outside"
AUDIT = "audit.jsonl"

SEED_FILES = {
    "book.csv": "amount,status\n10,paid\n20,open\n",
    "notes.txt": "蚁算写护栏试点\nshadow-write-guarded\n",
    "meta.json": '{"pilot":"shadow_write_guarded","version":"0.2.5"}\n',
}

# Explicit allowlist: only these relative paths may receive durable writes.
WRITE_ALLOWLIST = frozenset({"out.txt", "exports/summary.txt"})


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
    readme.write_text(
        "# shadow_write_guarded_pilot\n\n"
        "蚁算 v0.2.5 Stage1 write-guarded pilot (beyond readonly).\n"
        f"- {SANDBOX}/ — durable writes ONLY for allowlist: {sorted(WRITE_ALLOWLIST)}\n"
        f"- {OUTSIDE}/ — sibling; path escape must never write here.\n"
        "- Non-allowlisted write_file must be refused (write-allowlist).\n",
        encoding="utf-8",
    )
    (root / "ALLOWLIST.json").write_text(
        json.dumps({"write_allowlist": sorted(WRITE_ALLOWLIST), "version": "0.2.5"}, ensure_ascii=False, indent=2)
        + "\n",
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


def _license(mode: str, allowlist: frozenset[str] | None, max_steps: int = 6) -> License:
    return License(
        grants={"python", "shell", "read", "write", "http"},
        mode=mode,
        max_steps=max_steps,
        write_allowlist=set(allowlist) if allowlist is not None else None,
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


def _scripted_write(path: str, text: str):
    state = {"done": False}

    def reply(_messages):
        if state["done"]:
            return format_call("finish", {"answer": "done"})
        state["done"] = True
        return format_call("write_file", {"path": path, "text": text})

    return reply


def _scripted_two_writes(first: tuple[str, str], second: tuple[str, str]):
    state = {"i": 0}

    def reply(_messages):
        i = state["i"]
        if i == 0:
            state["i"] = 1
            return format_call("write_file", {"path": first[0], "text": first[1]})
        if i == 1:
            state["i"] = 2
            return format_call("write_file", {"path": second[0], "text": second[1]})
        return format_call("finish", {"answer": "done"})

    return reply


def run_shadow_write_guarded_pilot(root: Path | None = None, write_evidence: bool = True) -> dict[str, Any]:
    base = designated_root(root)
    sandbox, outside, digests = prepare(base)
    before = _snapshot(sandbox)

    # 1) Allowlisted durable write in assist mode
    allowed_text = "write-guarded-ok\n"
    allow = run_episode(
        {
            "id": "wg-allow-write",
            "family": "file",
            "prompt": "Write out.txt",
            "check": lambda ws: (ws / "out.txt").is_file()
            and (ws / "out.txt").read_text(encoding="utf-8").strip() == allowed_text.strip(),
        },
        _scripted_write("out.txt", allowed_text),
        sandbox,
        _license("assist", WRITE_ALLOWLIST, max_steps=3),
        audit_path=sandbox / AUDIT,
    )
    allow_rows = [r for r in _audit_rows(sandbox) if r.get("task") == "wg-allow-write"]
    allow_writes = [r for r in allow_rows if r.get("name") == "write_file"]
    allow_ok = (
        allow.get("ok") is True
        and (sandbox / "out.txt").is_file()
        and bool(allow_writes)
        and all(r.get("applied") is True for r in allow_writes)
        and all(not r.get("refused") for r in allow_writes)
    )

    # 2) Nested allowlisted write (exports/summary.txt)
    nested_text = "summary-ok\n"
    nested = run_episode(
        {
            "id": "wg-allow-nested",
            "family": "file",
            "prompt": "Write exports/summary.txt",
            "check": lambda ws: (ws / "exports" / "summary.txt").is_file()
            and (ws / "exports" / "summary.txt").read_text(encoding="utf-8").strip() == nested_text.strip(),
        },
        _scripted_write("exports/summary.txt", nested_text),
        sandbox,
        _license("assist", WRITE_ALLOWLIST, max_steps=3),
        audit_path=sandbox / AUDIT,
    )
    nested_ok = nested.get("ok") is True and (sandbox / "exports" / "summary.txt").is_file()

    # 3) Non-allowlisted write must be refused (durably absent)
    deny = run_episode(
        {
            "id": "wg-deny-write",
            "family": "file",
            "prompt": "Write secret.txt",
            "check": lambda ws: (ws / "secret.txt").is_file(),
        },
        _scripted_write("secret.txt", "should-not-exist\n"),
        sandbox,
        _license("assist", WRITE_ALLOWLIST, max_steps=3),
        audit_path=sandbox / AUDIT,
    )
    deny_rows = [r for r in _audit_rows(sandbox) if r.get("task") == "wg-deny-write"]
    deny_writes = [r for r in deny_rows if r.get("name") == "write_file"]
    deny_ok = (
        deny.get("ok") is False
        and not (sandbox / "secret.txt").exists()
        and bool(deny_writes)
        and all(r.get("applied") is False for r in deny_writes)
        and all("write-allowlist" in (r.get("refused") or []) for r in deny_writes)
    )

    # 4) Shadow mode still blocks even allowlisted path
    # Use allowlisted path: shadow must still not durably apply even when allowlisted
    before_shadow_out = (sandbox / "out.txt").read_text(encoding="utf-8") if (sandbox / "out.txt").is_file() else None
    shadow = run_episode(
        {
            "id": "wg-shadow-block",
            "family": "report",
            "prompt": "Shadow overwrite out.txt",
            "check": lambda ws: False,
        },
        _scripted_write("out.txt", "shadow-should-not-persist\n"),
        sandbox,
        _license("shadow", WRITE_ALLOWLIST, max_steps=3),
        audit_path=sandbox / AUDIT,
    )
    after_shadow_out = (sandbox / "out.txt").read_text(encoding="utf-8") if (sandbox / "out.txt").is_file() else None
    shadow_rows = [r for r in _audit_rows(sandbox) if r.get("task") == "wg-shadow-block"]
    shadow_writes = [r for r in shadow_rows if r.get("name") == "write_file"]
    shadow_ok = (
        after_shadow_out == before_shadow_out
        and shadow.get("ok") is False
        and bool(shadow_writes)
        and all(r.get("applied") is False for r in shadow_writes)
    )

    # 5) Escape refuse
    escape_rel = f"../{OUTSIDE}/escape.txt"
    escape = run_episode(
        {
            "id": "wg-escape",
            "family": "report",
            "prompt": "Escape write",
            "check": lambda ws: False,
        },
        _scripted_write(escape_rel, "pwned\n"),
        sandbox,
        _license("assist", WRITE_ALLOWLIST, max_steps=3),
        audit_path=sandbox / AUDIT,
    )
    escape_rows = [r for r in _audit_rows(sandbox) if r.get("task") == "wg-escape"]
    escape_writes = [r for r in escape_rows if r.get("name") == "write_file"]
    escape_ok = (
        not (outside / "escape.txt").exists()
        and bool(escape_writes)
        and all(
            ("path" in (r.get("refused") or []) or r.get("applied") is False)
            for r in escape_writes
        )
    )

    # 6) Seeds intact (except intentional allowlisted new files)
    digest_ok = True
    for name, expect in digests.items():
        text = (sandbox / name).read_text(encoding="utf-8")
        if hashlib.sha256(text.encode("utf-8")).hexdigest() != expect:
            digest_ok = False

    contracts = {
        "allowlisted_write_persists": allow_ok,
        "nested_allowlisted_write_persists": nested_ok,
        "non_allowlisted_write_refused": deny_ok,
        "shadow_still_blocks": shadow_ok,
        "escape_refused": escape_ok,
        "seed_digests_intact": digest_ok,
        "audit_present": (sandbox / AUDIT).is_file(),
        "allowlist_file_present": (base / "ALLOWLIST.json").is_file(),
        "beyond_readonly": True,
        "write_guarded_pilot": True,
    }
    passed = all(contracts.values())

    evidence: dict[str, Any] = {
        "kind": "shadow_write_guarded_pilot",
        "product": "蚁算模型",
        "version": "0.2.5",
        "gate": "0.6",
        "actor": "scripted",
        "gpu": False,
        "vl": False,
        "root": str(base),
        "sandbox": str(sandbox),
        "outside": str(outside),
        "write_allowlist": sorted(WRITE_ALLOWLIST),
        "timestamp": datetime.now().astimezone().isoformat(timespec="seconds"),
        "seed_files": list(SEED_FILES),
        "seed_digests": digests,
        "contracts": contracts,
        "legs": {
            "allow": {"ok": allow.get("ok"), "out_exists": (sandbox / "out.txt").exists()},
            "nested": {"ok": nested.get("ok"), "summary_exists": (sandbox / "exports" / "summary.txt").exists()},
            "deny": {"ok_check": deny.get("ok"), "secret_exists": (sandbox / "secret.txt").exists()},
            "shadow": {"ok_check": shadow.get("ok"), "probe2_exists": (sandbox / "probe2.txt").exists()},
            "escape": {"outside_escape_exists": (outside / "escape.txt").exists()},
        },
        "pass": passed,
        "notes": (
            "Beyond SHADOW_READONLY_PILOT: assist writes persist only on explicit allowlist; "
            "non-allowlisted refused with write-allowlist; shadow still non-durable; escape refused; no VL."
        ),
    }

    if write_evidence:
        docs = repo_path("docs")
        stamp = datetime.now().strftime("%Y-%m-%d")
        out = docs / f"SHADOW_WRITE_GUARDED_PILOT_{stamp}.json"
        out.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        evidence["evidence_path"] = str(out)
    return evidence


if __name__ == "__main__":
    ev = run_shadow_write_guarded_pilot()
    print(json.dumps({"pass": ev["pass"], "contracts": ev["contracts"], "path": ev.get("evidence_path")}, ensure_ascii=False))
