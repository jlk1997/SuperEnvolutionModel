"""Grants live outside the weights. The model cannot widen its own license."""

from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse

from evo.computer.actions import ACTIONS, Call
from evo.live.canary import safety_violations


SHELL_ALLOW = frozenset({"mkdir", "dir", "type", "copy"})
SHELL_ALIAS = {"cat": "type", "ls": "dir", "cp": "copy"}
IRREVERSIBLE = frozenset({"delete", "send", "pay"})


class License:
    def __init__(
        self,
        grants: set[str] | None = None,
        hosts: set[str] | None = None,
        shell_allow: set[str] | None = None,
        max_steps: int = 6,
        timeout: float = 8.0,
        mode: str = "lab",
        auto_families: set[str] | None = None,
        confirm=None,
        write_allowlist: set[str] | frozenset[str] | list[str] | None = None,
    ):
        self.grants = set(grants if grants is not None else {"python", "read", "write"})
        self.hosts = set(hosts if hosts is not None else {"127.0.0.1", "localhost"})
        self.shell_allow = set(shell_allow if shell_allow is not None else SHELL_ALLOW)
        self.max_steps = int(max_steps)
        self.timeout = float(timeout)
        self.mode = mode
        self.auto_families = set(auto_families or set())
        self.confirm = confirm
        # Relative workspace paths allowed for durable write_file when set.
        # None = no extra restriction (legacy assist/lab). Empty frozenset = refuse all writes.
        self.write_allowlist = (
            None if write_allowlist is None else {str(p).replace("\\", "/") for p in write_allowlist}
        )

    def decide(self, call: Call, family: str | None = None) -> list[str]:
        reasons = []
        if call.name not in ACTIONS:
            return ["unknown"]
        needed = _grant_for(call.name)
        if needed and needed not in self.grants:
            reasons.append(needed)
        if call.name == "python":
            reasons.extend(_python_reasons(call.arguments.get("code", "")))
        if call.name == "shell":
            reasons.extend(_shell_reasons(call.arguments.get("cmd", ""), self.shell_allow))
        if call.name == "http":
            reasons.extend(_http_reasons(call.arguments.get("url", ""), call.arguments.get("method", "GET"), self.hosts))
        if call.name in ("read_file", "write_file", "list_dir"):
            reasons.extend(_path_reasons(call.arguments.get("path", ".")))
        if call.name == "write_file" and self.write_allowlist is not None and not reasons:
            rel = str(call.arguments.get("path") or "").replace("\\", "/")
            if rel not in self.write_allowlist:
                reasons.append("write-allowlist")
        if _needs_confirm(call) and not (self.confirm and self.confirm(call)):
            reasons.append("confirm")
        # Auto only opens families already promoted (verified). Missing family = refuse.
        if self.mode == "auto" and call.name != "finish":
            if not family or family not in self.auto_families:
                reasons.append("family")
        return reasons


def _grant_for(name: str) -> str | None:
    if name == "python":
        return "python"
    if name == "shell":
        return "shell"
    if name in ("read_file", "list_dir"):
        return "read"
    if name == "write_file":
        return "write"
    if name == "http":
        return "http"
    return None


def _python_reasons(code: str) -> list[str]:
    reasons = []
    if safety_violations(code):
        reasons.append("unsafe")
    return reasons


def _shell_reasons(cmd: str, allow: set[str]) -> list[str]:
    text = normalize_shell(cmd)
    if not text:
        return ["shell-command"]
    if any(token in text for token in ("&", "|", ">", "<", "%", "\n", "..")):
        return ["shell-command"]
    head = text.split()[0].lower()
    if head not in {name.lower() for name in allow}:
        return ["shell-command"]
    # Workspace-relative only: refuse Unix abs paths and /path/to placeholders.
    for token in text.split()[1:]:
        if token.startswith("-"):
            continue
        raw = token.strip().strip('"').strip("\'")
        if not raw:
            continue
        if raw.startswith("/") or raw.startswith("\\") or (len(raw) >= 2 and raw[1] == ":"):
            return ["shell-command"]
        if "path/to" in raw.replace("\\", "/").lower():
            return ["shell-command"]
    return []


def normalize_shell(cmd: str) -> str:
    """Unix names the model already knows, mapped onto the Windows allowlist."""
    text = (cmd or "").strip()
    if not text:
        return ""
    parts = text.split()
    parts[0] = SHELL_ALIAS.get(parts[0].lower(), parts[0])
    head = parts[0].lower()
    # Drop Unix flags Windows cmd does not take (mkdir -p / cp -r).
    if head == "mkdir":
        parts = [parts[0]] + [p for p in parts[1:] if p not in ("-p", "--parents")]
    elif head == "copy":
        parts = [parts[0]] + [p for p in parts[1:] if p not in ("-r", "-R", "-a", "-f", "--recursive")]
    return " ".join(parts)


def _http_reasons(url: str, method: str, hosts: set[str]) -> list[str]:
    parsed = urlparse(url or "")
    host = (parsed.hostname or "").lower()
    if host not in {item.lower() for item in hosts}:
        return ["host"]
    if parsed.scheme not in ("http", "https"):
        return ["host"]
    return []


def _path_reasons(path: str) -> list[str]:
    raw = path or "."
    if ".." in raw.replace("\\", "/").split("/"):
        return ["path"]
    try:
        candidate = Path(raw)
    except (TypeError, ValueError):
        return ["path"]
    if candidate.is_absolute() or candidate.drive:
        return ["path"]
    return []


def _needs_confirm(call: Call) -> bool:
    if call.name == "http":
        url = (call.arguments.get("url") or "").lower()
        if any(token in url for token in ("/send", "/pay", "/delete")):
            return True
    if call.name == "shell" and (call.arguments.get("cmd") or "").split()[:1] == ["del"]:
        return True
    return False


def fence(workspace: Path, relative: str) -> Path | None:
    """Resolve a relative path and refuse anything outside the workspace."""
    root = workspace.resolve()
    try:
        target = (root / relative).resolve()
    except (OSError, ValueError):
        return None
    if target != root and root not in target.parents:
        return None
    return target
