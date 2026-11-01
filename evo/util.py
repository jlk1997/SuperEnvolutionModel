"""Shared helpers that do not import the training stack."""

from __future__ import annotations

import random
from pathlib import Path

import numpy as np
import torch
import yaml


ROOT = Path(__file__).resolve().parents[1]

DEFAULTS = {
    "seed": 0,
    "model_name": str(ROOT / "models" / "Qwen2.5-1.5B-Instruct"),
    "lora_rank": 8,
    "lora_alpha": 16,
    "lora_dropout": 0.0,
    "target_modules": ["q_proj", "k_proj", "v_proj", "o_proj"],
    "max_seq_len": 384,
    "max_passage_chars": 1600,
    "inner_steps": 8,
    "inner_lr": 1e-4,
    "outer_lr": 5e-5,
    "outer_epochs": 2,
    "outer_iters": 1,
    "n_edits": 2,
    "edit_tokens": 96,
    "answer_tokens": 16,
    "temperature": 0.7,
    "questions_per_passage": 3,
    "n_train": 2,
    "n_test": 2,
    "n_passages": 5,
    "candidate_pool": 16,
    "reward_metric": "f1",
    "reward_threshold": 0.0,
    "lam": 1.0,
    "max_f1_drop": 0.34,
    "max_kl": 5.0,
    "kl_coef": 0.5,
    "distill_questions": 2,
    "methods": ["none", "gate", "kl", "reward"],
    "method": "none",
    "runs_root": "runs",
    "data_cache": "data/squad_cache.json",
    "fallback_path": "data/fallback_passages.json",
    "probe_path": "data/probe_questions.json",
    "rounds": 2,
    "proposals_per_type": 1,
    "solver_samples": 3,
    "exec_timeout": 2.0,
    "min_learnability": 0.34,
    "heldout_code": "data/heldout_code.json",
    "heldout_math": "data/heldout_math.json",
    "heldout_limit": 4,
    "max_new_code": 160,
    "d_model": 768,
    "n_layers": 6,
    "n_heads": 12,
    "d_mem": 128,
    "seq_len": 64,
    "batch_size": 4,
    "steps_per_domain": 80,
    "arch_lr": 3e-4,
    "log_every": 20,
    "grad_clip": 1.0,
    "freqs": [1, 4, 16],
    "etas": [0.30, 0.10, 0.02],
    "decays": [0.60, 0.90, 0.99],
    "bptt": 64,
}


def repo_path(path: str | Path) -> Path:
    p = Path(path)
    if p.is_absolute():
        return p
    return ROOT / p


def load_config(path: str | Path | None) -> dict:
    cfg = dict(DEFAULTS)
    if path:
        config_path = Path(path)
        if not config_path.is_file():
            config_path = ROOT / path
        with open(config_path, encoding="utf-8") as handle:
            user = yaml.safe_load(handle) or {}
        cfg.update(user)
    return cfg


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def mean(values) -> float | None:
    values = [v for v in values if v is not None]
    if not values:
        return None
    return float(sum(values) / len(values))
