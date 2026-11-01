"""Passage loading. SQuAD when the hub is reachable, fictional fallback otherwise."""

from __future__ import annotations

import json
import os
import random

from evo.util import repo_path


def _read_json(path) -> list:
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def load_probe(cfg: dict) -> dict:
    rows = _read_json(repo_path(cfg["probe_path"]))
    return {"id": "probe", "title": "probe", "context": "", "qas": rows}


def _from_squad_rows(rows, limit: int, seed: int) -> list[dict]:
    grouped: dict[str, dict] = {}
    for row in rows:
        answers = [text for text in row["answers"]["text"] if text]
        if not answers:
            continue
        bucket = grouped.setdefault(
            row["context"],
            {
                "id": row.get("id", ""),
                "title": row.get("title", ""),
                "context": row["context"],
                "qas": [],
            },
        )
        if len(bucket["qas"]) < 5:
            bucket["qas"].append({"question": row["question"], "answers": answers})
    passages = [item for item in grouped.values() if len(item["qas"]) >= 2]
    random.Random(seed).shuffle(passages)
    for index, passage in enumerate(passages):
        passage["id"] = f"squad-{index:04d}"
    return passages[:limit]


def _try_download_squad(limit: int, seed: int) -> list[dict]:
    from datasets import load_dataset

    dataset = load_dataset("rajpurkar/squad", split="validation")
    return _from_squad_rows(dataset, limit, seed)


def load_passages(cfg: dict, n: int) -> tuple[list[dict], str]:
    """Return (passages, source). Source is 'squad-cache', 'squad', or 'fallback'."""
    cache = repo_path(cfg["data_cache"])
    if cache.exists():
        cached = _read_json(cache)
        if len(cached) >= n:
            return cached[:n], "squad-cache"
    try:
        downloaded = _try_download_squad(max(n, cfg.get("candidate_pool", n)), cfg["seed"])
    except Exception as first_error:
        if not os.environ.get("HF_ENDPOINT"):
            os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
            try:
                downloaded = _try_download_squad(max(n, cfg.get("candidate_pool", n)), cfg["seed"])
            except Exception:
                downloaded = None
        else:
            downloaded = None
        if downloaded is None:
            print(f"[data] SQuAD unavailable ({type(first_error).__name__}); using fallback passages", flush=True)
    if downloaded:
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_text(json.dumps(downloaded, ensure_ascii=True, indent=2), encoding="utf-8")
        return downloaded[:n], "squad"
    fallback = _read_json(repo_path(cfg["fallback_path"]))
    if len(fallback) < n:
        raise RuntimeError(f"Need {n} passages but fallback has {len(fallback)}")
    return fallback[:n], "fallback"


def clip_passage(passage: dict, max_chars: int) -> dict:
    text = passage["context"]
    if len(text) <= max_chars:
        return passage
    clipped = dict(passage)
    clipped["context"] = text[:max_chars]
    return clipped
