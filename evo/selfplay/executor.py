"""Subprocess Python sandbox with a timeout and blocked network imports."""

from __future__ import annotations

import ast
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


NETWORK_BLOCKED = {
    "socket", "urllib", "http", "requests", "ftplib", "smtplib",
    "subprocess", "asyncio", "ctypes", "ssl",
}
SOURCE_BLOCKED = {"inspect", "dis", "pickle", "marshal"}


def _import_hook(blocked: set[str]) -> str:
    names = ", ".join(repr(name) for name in sorted(blocked))
    return f"""
import sys
_BLOCKED = {{{names}}}
class _BlockNetwork:
    def find_spec(self, name, path, target=None):
        root = name.split(".")[0]
        if name in _BLOCKED or root in _BLOCKED:
            raise ImportError("blocked import: %s" % name)
        return None
sys.meta_path.insert(0, _BlockNetwork())
"""


def _world_guard(allow_workspace: bool) -> str:
    flag = "True" if allow_workspace else "False"
    return f"""
import builtins, io, os
_ALLOW_WORKSPACE = {flag}
_OPEN = builtins.open
def _guard_open(file, *args, **kwargs):
    raw = os.path.abspath(os.fspath(file))
    root = os.path.abspath("workspace")
    allowed = _ALLOW_WORKSPACE and (raw == root or raw.startswith(root + os.sep))
    if not allowed:
        raise PermissionError("blocked open")
    return _OPEN(file, *args, **kwargs)
builtins.open = _guard_open
io.open = _guard_open
_OS_OPEN = os.open
def _guard_os_open(path, flags, *args, **kwargs):
    raw = os.path.abspath(os.fspath(path))
    root = os.path.abspath("workspace")
    allowed = _ALLOW_WORKSPACE and (raw == root or raw.startswith(root + os.sep))
    if not allowed:
        raise PermissionError("blocked open")
    return _OS_OPEN(path, flags, *args, **kwargs)
os.open = _guard_os_open
"""


@dataclass
class ExecResult:
    ok: bool
    stdout: str
    stderr: str
    error: str | None

    @property
    def value(self) -> str:
        lines = [line for line in self.stdout.splitlines() if line.strip()]
        return lines[-1].strip() if lines else ""


def _child_env() -> dict[str, str]:
    # Keep the parent environment so the Windows interpreter can find its DLLs.
    # Network access is blocked by the import hook inside the child, not by the env.
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONSAFEPATH"] = "1"
    env["PYTHONNOUSERSITE"] = "1"
    env["PYTHONUTF8"] = "1"
    return env


def _sync_tree(src: Path, dest: Path) -> None:
    if not src.exists():
        return
    for path in src.rglob("*"):
        if not path.is_file():
            continue
        target = dest / path.relative_to(src)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)


def run_code(
    code: str,
    timeout: float = 2.0,
    *,
    prelude: str = "",
    world: bool = False,
    workspace: str | Path | None = None,
) -> ExecResult:
    """Run `code` in a fresh interpreter. Network and subprocess imports are blocked.

    `world` also blocks modules that can read function source, and blocks open()
    outside an optional workspace directory. Tool definitions live in `prelude`.
    """
    work = Path(tempfile.mkdtemp(prefix="evo-sandbox-"))
    real_workspace = Path(workspace) if workspace else None
    try:
        sandbox_ws = work / "workspace"
        sandbox_ws.mkdir()
        if real_workspace is not None:
            real_workspace.mkdir(parents=True, exist_ok=True)
            _sync_tree(real_workspace, sandbox_ws)
        blocked = set(NETWORK_BLOCKED)
        header = _import_hook(blocked | (SOURCE_BLOCKED if world else set()))
        if world:
            header += "\n" + _world_guard(real_workspace is not None)
        if prelude.strip():
            header += "\n" + prelude.rstrip() + "\n"
        script = work / "main.py"
        script.write_text(header + "\n" + code, encoding="utf-8")
        try:
            completed = subprocess.run(
                [sys.executable, "-I", str(script)],
                capture_output=True,
                timeout=timeout,
                cwd=work,
                env=_child_env(),
                text=True,
                encoding="utf-8",
                errors="replace",
            )
        except subprocess.TimeoutExpired:
            return ExecResult(False, "", "", "timeout")
        if real_workspace is not None:
            _sync_tree(sandbox_ws, real_workspace)
        stdout = (completed.stdout or "")[:10000]
        stderr = (completed.stderr or "")[:4000]
        if completed.returncode != 0:
            return ExecResult(False, stdout, stderr, stderr.strip().splitlines()[-1] if stderr.strip() else "error")
        return ExecResult(True, stdout, stderr, None)
    finally:
        shutil.rmtree(work, ignore_errors=True)


def execute_solve(program: str, input_literal: str, timeout: float = 2.0) -> ExecResult:
    try:
        value = ast.literal_eval(input_literal)
    except (SyntaxError, ValueError) as exc:
        return ExecResult(False, "", "", f"bad input literal: {exc}")
    code = program.rstrip() + f"\n_INPUT = {value!r}\nprint(repr(solve(_INPUT)))\n"
    return run_code(code, timeout=timeout)


def outputs_match(got: str, expected: str) -> bool:
    left = got.strip()
    right = expected.strip()
    if not left and not right:
        return True
    if left == right:
        return True
    try:
        return ast.literal_eval(left) == ast.literal_eval(right)
    except (SyntaxError, ValueError):
        return left.lower() == right.lower()
