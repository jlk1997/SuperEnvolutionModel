"""A named capability atom: metadata + adapter path."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class CapabilityAtom:
    """One internalized skill. The weight delta lives at `adapter_dir`."""

    name: str
    skill: str
    adapter_dir: str
    base_model: str
    criterion: float = 0.6
    birth: float | None = None
    bare_rate: float | None = None
    scaffold_rate: float | None = None
    dissolution: float | None = None
    sites: list[str] = field(default_factory=list)
    evidence: dict[str, Any] = field(default_factory=dict)
    version: int = 1

    def to_dict(self) -> dict:
        return asdict(self)

    def write(self, dest: Path | None = None) -> Path:
        folder = Path(dest) if dest else Path(self.adapter_dir)
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / "capability.json"
        path.write_text(json.dumps(self.to_dict(), indent=2, ensure_ascii=True), encoding="utf-8")
        return path

    @classmethod
    def load(cls, folder: str | Path) -> "CapabilityAtom":
        path = Path(folder) / "capability.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        return cls(**data)
