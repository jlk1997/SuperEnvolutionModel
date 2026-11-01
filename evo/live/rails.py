"""Permissions the learner cannot grant itself.

A correct-looking program that opens a file, a shell, or the network is refused
before it runs, unless that grant was set on the body from outside the model.
"""

from __future__ import annotations

from evo.live.canary import safety_violations


DEFAULT_GRANTS = frozenset({"python"})


def denied(code: str, grants: set[str] | frozenset[str] | None = None) -> list[str]:
    """Reasons to refuse. Empty means the program may be executed."""
    allowed = set(DEFAULT_GRANTS if grants is None else grants)
    reasons = []
    if safety_violations(code):
        reasons.append("unsafe")
    text = code or ""
    if _touches_file(text) and not ({"read", "write"} & allowed):
        reasons.append("file")
    if _touches_shell(text) and "shell" not in allowed:
        reasons.append("shell")
    if _touches_network(text) and "http" not in allowed:
        reasons.append("http")
    return reasons


def _touches_file(text: str) -> bool:
    return "open(" in text or "os.remove" in text or "shutil." in text


def _touches_shell(text: str) -> bool:
    return "os.system" in text or "subprocess" in text


def _touches_network(text: str) -> bool:
    return any(token in text for token in ("urllib", "requests.", "socket"))
