"""Prefer crystallized atoms over scaffold notes when internalized."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from evo.crystal.atom import CapabilityAtom
from evo.util import repo_path


def list_atoms(index_path: Path | None = None) -> list[dict]:
    path = index_path or (repo_path("runs") / "capabilities" / "index.json")
    if not path.is_file():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def load_atom(name: str, index_path: Path | None = None) -> CapabilityAtom | None:
    for row in list_atoms(index_path):
        if row.get("name") == name:
            folder = Path(row["path"])
            if (folder / "capability.json").is_file():
                return CapabilityAtom.load(folder)
    folder = repo_path("runs") / "capabilities" / name
    if (folder / "capability.json").is_file():
        return CapabilityAtom.load(folder)
    return None


def is_internalized(atom: CapabilityAtom, *, max_d: float = 0.05) -> bool:
    if atom.bare_rate is None:
        return False
    if atom.bare_rate < float(atom.criterion or 0.6):
        return False
    d = atom.dissolution
    if d is None and atom.scaffold_rate is not None:
        d = max(0.0, float(atom.scaffold_rate) - float(atom.bare_rate))
    if d is None:
        return True
    return float(d) <= max_d


def route(
    skill: str,
    *,
    notes: str | None = None,
    prefer_atom: bool = True,
    index_path: Path | None = None,
) -> dict[str, Any]:
    """Decide atom vs scaffold notes for `skill`.

    When several atoms share a skill, the internalized one with highest bare_rate wins.
    Cross-skill atoms never match (table cannot steal shell).
    """
    matches = []
    for row in list_atoms(index_path):
        atom = load_atom(str(row.get("name")), index_path=index_path)
        if atom is None:
            continue
        if atom.skill != skill and atom.name != skill:
            continue
        matches.append(atom)
    matches.sort(key=lambda a: (is_internalized(a), a.bare_rate or 0.0), reverse=True)
    if prefer_atom and matches and is_internalized(matches[0]):
        atom = matches[0]
        return {
            "mode": "atom",
            "skill": skill,
            "atom": atom.name,
            "adapter_dir": atom.adapter_dir,
            "bare_rate": atom.bare_rate,
            "dissolution": atom.dissolution,
            "use_notes": False,
            "notes": None,
            "reason": "internalized capability clears gate without scaffold",
            "n_matches": len(matches),
        }
    if notes:
        return {
            "mode": "scaffold",
            "skill": skill,
            "atom": matches[0].name if matches else None,
            "use_notes": True,
            "notes": notes,
            "reason": (
                "prefer_atom=False; keep retrieval notes"
                if not prefer_atom
                else "no internalized atom; fall back to retrieval notes"
            ),
            "n_matches": len(matches),
        }
    # prefer_atom=False with internalized match still reports atom identity but uses notes=None path
    if matches and not prefer_atom:
        return {
            "mode": "scaffold" if notes else "none",
            "skill": skill,
            "atom": matches[0].name,
            "use_notes": bool(notes),
            "notes": notes,
            "reason": "prefer_atom=False; atom available but notes path kept",
            "n_matches": len(matches),
        }
    return {
        "mode": "none",
        "skill": skill,
        "atom": None,
        "use_notes": False,
        "notes": None,
        "reason": "no atom and no notes",
        "n_matches": len(matches),
    }


def prompt_for(
    skill: str,
    user_prompt: str,
    notes: str | None = None,
    *,
    index_path: Path | None = None,
) -> dict[str, Any]:
    """Build the prompt to send; strip notes when an internalized atom wins."""
    decision = route(skill, notes=notes, prefer_atom=True, index_path=index_path)
    if decision["mode"] == "atom":
        decision["prompt"] = user_prompt
    elif decision["mode"] == "scaffold" and notes:
        decision["prompt"] = notes.rstrip() + "\n\n" + user_prompt
    else:
        decision["prompt"] = user_prompt
    return decision
