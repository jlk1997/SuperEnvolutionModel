"""Execute one licensed call. Python and shell stay inside the workspace."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

from evo.computer.actions import Call
from evo.computer.license import License, fence


def execute(call: Call, workspace: Path, license: License, apply: bool = True) -> str:
    workspace.mkdir(parents=True, exist_ok=True)
    if not apply:
        return "shadow: not applied"
    if call.name == "python":
        return _python(call.arguments.get("code", ""), workspace, license.timeout)
    if call.name == "shell":
        return _shell(call.arguments.get("cmd", ""), workspace, license.timeout)
    if call.name == "read_file":
        return _read(workspace, call.arguments.get("path", ""))
    if call.name == "write_file":
        return _write(workspace, call.arguments.get("path", ""), call.arguments.get("text", ""))
    if call.name == "list_dir":
        return _list(workspace, call.arguments.get("path", "."))
    if call.name == "http":
        return _http(
            call.arguments.get("method", "GET"),
            call.arguments.get("url", ""),
            call.arguments.get("body", ""),
            call.arguments.get("token", ""),
            license.timeout,
        )
    if call.name == "finish":
        return call.arguments.get("answer", "")
    return "unknown action"


def _python(code: str, workspace: Path, timeout: float) -> str:
    from evo.util import repo_path

    scratch = repo_path("tmp") / "sandbox"
    scratch.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="evo-computer-", dir=scratch))
    try:
        header = _guard(workspace)
        script = work / "main.py"
        script.write_text(header + "\n" + (code or "raise SystemExit('empty')"), encoding="utf-8")
        env = dict(os.environ)
        env["PYTHONIOENCODING"] = "utf-8"
        env["PYTHONSAFEPATH"] = "1"
        env["PYTHONUTF8"] = "1"
        env["TEMP"] = str(workspace)
        env["TMP"] = str(workspace)
        try:
            completed = subprocess.run(
                [sys.executable, "-I", str(script)],
                capture_output=True,
                timeout=timeout,
                cwd=str(workspace),
                env=env,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
        except subprocess.TimeoutExpired:
            return "timeout"
        out = (completed.stdout or "")[:4000]
        err = (completed.stderr or "")[:1500]
        if completed.returncode != 0:
            tail = err.strip().splitlines()[-1] if err.strip() else "error"
            return (tail + "\n" + out).strip()[:4000]
        return out.strip() or "ok"
    finally:
        shutil.rmtree(work, ignore_errors=True)


def _guard(workspace: Path) -> str:
    root = str(workspace.resolve())
    return f"""
import builtins, io, os, sys
_ROOT = os.path.abspath({root!r})
_OPEN = builtins.open
def _guard_open(file, *args, **kwargs):
    raw = os.path.abspath(os.fspath(file))
    if raw != _ROOT and not raw.startswith(_ROOT + os.sep):
        raise PermissionError("blocked open")
    return _OPEN(file, *args, **kwargs)
builtins.open = _guard_open
io.open = _guard_open
_BLOCKED = {{"socket", "requests", "ftplib", "smtplib", "subprocess", "ctypes", "ssl", "pickle", "marshal"}}
class _Block:
    def find_spec(self, name, path, target=None):
        root = name.split(".")[0]
        if name in _BLOCKED or root in _BLOCKED:
            raise ImportError("blocked import: %s" % name)
        return None
sys.meta_path.insert(0, _Block())
"""


def _shell(cmd: str, workspace: Path, timeout: float) -> str:
    from evo.computer.license import normalize_shell

    cmd = normalize_shell(cmd)
    try:
        completed = subprocess.run(
            ["cmd", "/c", cmd],
            capture_output=True,
            timeout=timeout,
            cwd=str(workspace),
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except subprocess.TimeoutExpired:
        return "timeout"
    out = ((completed.stdout or "") + (completed.stderr or ""))[:2000]
    if completed.returncode != 0:
        return (out or "shell error").strip()
    return out.strip() or "ok"


def _read(workspace: Path, relative: str) -> str:
    path = fence(workspace, relative or "")
    if path is None or not path.is_file():
        return "missing"
    return path.read_text(encoding="utf-8", errors="replace")[:4000]


def _write(workspace: Path, relative: str, text: str) -> str:
    path = fence(workspace, relative or "")
    if path is None:
        return "refused:path"
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists() and path.is_dir():
            return "refused: path is a directory"
        path.write_text(text, encoding="utf-8")
    except OSError as exc:
        return f"write failed: {exc}"
    return "wrote " + relative


def _list(workspace: Path, relative: str) -> str:
    path = fence(workspace, relative or ".")
    if path is None or not path.is_dir():
        return "missing"
    names = sorted(item.name for item in path.iterdir())
    return "\n".join(names)


def _http(method: str, url: str, body: str, token: str, timeout: float) -> str:
    data = None if not body else body.encode("utf-8")
    request = urllib.request.Request(url, data=data, method=(method or "GET").upper())
    if token:
        request.add_header("Authorization", "Bearer " + token)
    if body:
        request.add_header("Content-Type", "application/json")
    try:
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        with opener.open(request, timeout=timeout) as response:
            payload = response.read().decode("utf-8", errors="replace")
            return payload[:4000]
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:500]
        return f"http {exc.code} {detail}"
    except urllib.error.URLError as exc:
        return "http error " + str(exc.reason)


def append_audit(path: Path, row: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=True) + "\n")
