"""Turn a verified adapter or graded pairs into a CapabilityAtom."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Callable

from evo.crystal.atom import CapabilityAtom
from evo.registry import PRIMARY, resolve
from evo.util import repo_path


def crystallize_from_adapter(
    name: str,
    skill: str,
    adapter_dir: str | Path,
    *,
    dest: str | Path | None = None,
    base_model: str | None = None,
    birth: float | None = None,
    bare_rate: float | None = None,
    sites: list[str] | None = None,
    evidence: dict | None = None,
    criterion: float = 0.6,
) -> CapabilityAtom:
    """Copy/link an existing LoRA folder into `runs/capabilities/<name>` and write capability.json.

    Does not lower `criterion`. Callers should only crystallize when bare_rate >= criterion
    (or when promoting a previously gated adapter such as evoplast_fit_add).
    """
    src = Path(adapter_dir)
    if not src.is_dir():
        raise FileNotFoundError(f"adapter not found: {src}")
    out = Path(dest) if dest else repo_path("runs") / "capabilities" / name
    out.mkdir(parents=True, exist_ok=True)
    # Copy adapter files (skip huge duplicates if same path)
    if src.resolve() != out.resolve():
        for item in src.iterdir():
            target = out / item.name
            if item.is_file():
                shutil.copy2(item, target)
            elif item.is_dir() and (item.name in {"policy", "memory", "scratch"} or item.name.startswith("skill")):
                if target.exists():
                    shutil.rmtree(target)
                shutil.copytree(item, target)
    base = base_model or str(resolve(PRIMARY))
    atom = CapabilityAtom(
        name=name,
        skill=skill,
        adapter_dir=str(out),
        base_model=base,
        criterion=float(criterion),
        birth=birth,
        bare_rate=bare_rate,
        sites=list(sites or []),
        evidence=dict(evidence or {}),
    )
    if bare_rate is not None and bare_rate < criterion:
        atom.evidence["warning"] = (
            f"bare_rate {bare_rate} < criterion {criterion}; atom recorded but not gate-cleared"
        )
    atom.write(out)
    manifest = repo_path("runs") / "capabilities" / "index.json"
    _index_add(manifest, atom)
    return atom


def crystallize_from_pairs(
    name: str,
    skill: str,
    pairs: list[tuple[str, str]],
    grade: Callable[[str, str], bool],
    *,
    adapter_dir: str | Path | None = None,
    criterion: float = 0.6,
    dest: str | Path | None = None,
    sites: list[str] | None = None,
) -> CapabilityAtom:
    """Toy path: grade completions offline; require hit-rate >= criterion before crystallizing.

    `pairs` are (prompt, completion). `grade(prompt, completion) -> bool`.
    When `adapter_dir` is set, copies weights; otherwise writes a notes-only atom (scaffold).
    """
    if not pairs:
        raise ValueError("no pairs to crystallize")
    hits = [bool(grade(prompt, completion)) for prompt, completion in pairs]
    rate = sum(hits) / len(hits)
    if rate < criterion:
        raise RuntimeError(
            f"crystallize refused: hit-rate {rate:.3f} < criterion {criterion}. Gate not lowered."
        )
    evidence = {"n": len(pairs), "hits": sum(hits), "rate": rate, "mode": "pairs"}
    if adapter_dir is None:
        out = Path(dest) if dest else repo_path("runs") / "capabilities" / name
        out.mkdir(parents=True, exist_ok=True)
        (out / "scaffold_notes.json").write_text(
            json.dumps([{"prompt": p, "completion": c} for p, c in pairs], indent=2),
            encoding="utf-8",
        )
        atom = CapabilityAtom(
            name=name,
            skill=skill,
            adapter_dir=str(out),
            base_model=str(resolve(PRIMARY)),
            criterion=criterion,
            bare_rate=None,
            scaffold_rate=rate,
            sites=list(sites or []),
            evidence=evidence,
        )
        atom.evidence["kind"] = "notes_only"
        atom.write(out)
        _index_add(repo_path("runs") / "capabilities" / "index.json", atom)
        return atom
    return crystallize_from_adapter(
        name,
        skill,
        adapter_dir,
        dest=dest,
        bare_rate=rate,
        sites=sites,
        evidence=evidence,
        criterion=criterion,
    )


def _index_add(manifest: Path, atom: CapabilityAtom) -> None:
    manifest.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    if manifest.is_file():
        rows = json.loads(manifest.read_text(encoding="utf-8"))
    rows = [row for row in rows if row.get("name") != atom.name]
    rows.append({"name": atom.name, "path": atom.adapter_dir, "skill": atom.skill, "bare_rate": atom.bare_rate})
    manifest.write_text(json.dumps(rows, indent=2), encoding="utf-8")
