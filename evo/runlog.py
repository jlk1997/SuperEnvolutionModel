"""Run directory, metric log, and checkpoint lineage."""

from __future__ import annotations

import json
import time
from pathlib import Path

import yaml

from evo.util import repo_path


class Run:
    def __init__(self, runs_root: str, name: str, config: dict):
        stamp = time.strftime("%Y%m%d-%H%M%S")
        self.dir = repo_path(runs_root) / name / stamp
        self.dir.mkdir(parents=True, exist_ok=True)
        self.ckpt = self.dir / "checkpoints"
        self.ckpt.mkdir(exist_ok=True)
        (self.dir / "config.yaml").write_text(
            yaml.safe_dump(config, sort_keys=False), encoding="utf-8"
        )
        self.metrics_path = self.dir / "metrics.jsonl"
        self.lineage_path = self.dir / "lineage.json"
        self.lineage: list[dict] = []

    def log(self, row: dict) -> None:
        record = {"time": time.time(), **row}
        with self.metrics_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=True) + "\n")
        text = json.dumps(record, ensure_ascii=True)
        print(text[:800], flush=True)

    def save_json(self, name: str, payload) -> Path:
        path = self.dir / name
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=True), encoding="utf-8")
        return path

    def commit_adapter(self, model, adapter: str, meta: dict) -> dict:
        import torch

        from evo.model import adapter_state

        generation = len(self.lineage) + 1
        path = self.ckpt / f"gen_{generation:03d}_{adapter}.pt"
        torch.save(adapter_state(model, adapter), path)
        if "parent_generation" in meta:
            parent = meta["parent_generation"]
        else:
            parent = self.lineage[-1]["generation"] if self.lineage else None
        parents = list(meta.get("parents") or ([] if parent is None else [parent]))
        record = {
            "generation": generation,
            "parent": parent,
            "parents": parents,
            "adapter": adapter,
            "path": str(path),
            **{key: value for key, value in meta.items() if key != "parent_generation"},
        }
        self.lineage.append(record)
        self.lineage_path.write_text(
            json.dumps(self.lineage, indent=2, ensure_ascii=True), encoding="utf-8"
        )
        return record
