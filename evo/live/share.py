"""Export a skill without the private strings it was practiced on.

Frozen. The plasticity-evolution line does not extend this module.
"""

from __future__ import annotations


def rewrite(text: str, replacements: dict[str, str]) -> str:
    cleaned = text or ""
    for secret, placeholder in replacements.items():
        if secret:
            cleaned = cleaned.replace(secret, placeholder)
    return cleaned


def leak_scan(text: str, canaries: list[str]) -> list[str]:
    body = text or ""
    return [canary for canary in canaries if canary and canary in body]


def export_skill(text: str, replacements: dict[str, str], canaries: list[str]) -> dict:
    """Refuse the export when a canary survives the rewrite."""
    cleaned = rewrite(text, replacements)
    leaks = leak_scan(cleaned, canaries)
    return {"text": "" if leaks else cleaned, "leaks": leaks, "ok": not leaks}


def offer_skill(text: str, dest: str, replacements: dict[str, str] | None = None, canaries: list[str] | None = None) -> dict:
    """Only a core skill leaves this desk, and only after the private strings are gone."""
    if dest != "core":
        return {"ok": False, "text": "", "leaks": [], "why": "stays here", "dest": dest or "local"}
    exported = export_skill(text or "", replacements or {}, list(canaries or []))
    return {
        "ok": exported["ok"],
        "text": exported["text"],
        "leaks": exported["leaks"],
        "why": "shared" if exported["ok"] else "leak",
        "dest": "core",
    }
