# -*- coding: utf-8 -*-
"""Vision adapter routing policy for Ant-Vision.

Evidence-backed (C66/C72/C86): dense tables regress under style LoRA → force bare.
LoRA only when domain is weak and adapter present. Never invent scores.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


# Domains where LoRA historically hurts (C66 flip stock; C72 flips defect+stock)
DENSE_TABLE_DOMAINS = frozenset({"dense_table", "table_cells", "table"})
# Domains where LoRA may help weak / train-style captions/OCR (not heldout ceiling)
WEAK_LORA_OK = frozenset({"ocr_weak", "caption_weak", "train_style", "style_train"})


@dataclass
class VisionRouteDecision:
    mode: str  # "bare" | "lora"
    use_adapter: bool
    adapter_path: str | None
    domain: str
    task: str
    reason: str
    policy: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "mode": self.mode,
            "use_adapter": self.use_adapter,
            "adapter_path": self.adapter_path,
            "domain": self.domain,
            "task": self.task,
            "reason": self.reason,
            "policy": self.policy,
        }


def infer_domain(task: str, meta: dict | None = None) -> str:
    meta = meta or {}
    d = str(meta.get("domain") or "").strip().lower()
    if d:
        return d
    t = (task or "").strip().lower()
    if t in ("table_cells", "table"):
        # heldout / dense tables default to dense_table (force bare)
        if meta.get("v3_heldout") or meta.get("v3_dense") or meta.get("harder_than_v2_heldout"):
            return "dense_table"
        cols = str(meta.get("gold") or "").count(",")
        # heuristic: many commas → dense
        if cols >= 12:
            return "dense_table"
        return "table_cells"
    if t == "ocr":
        return "ocr"
    if t == "caption":
        return "caption"
    return t or "unknown"


def route_vision(
    task: str,
    *,
    meta: dict | None = None,
    adapter_path: Path | str | None = None,
    force_bare: bool = False,
    allow_lora_domains: set[str] | frozenset[str] | None = None,
) -> VisionRouteDecision:
    """Route dense-table → bare; LoRA only on explicitly weak domains when adapter exists."""
    domain = infer_domain(task, meta)
    adapter = Path(adapter_path) if adapter_path else None
    adapter_ok = bool(adapter and adapter.is_dir() and (adapter / "adapter_config.json").is_file())
    allow = allow_lora_domains if allow_lora_domains is not None else WEAK_LORA_OK
    policy = "dense_table_bare__lora_only_weak_domains"

    if force_bare:
        return VisionRouteDecision(
            mode="bare",
            use_adapter=False,
            adapter_path=None,
            domain=domain,
            task=task,
            reason="force_bare=True",
            policy=policy,
        )

    if domain in DENSE_TABLE_DOMAINS or task in ("table_cells", "table"):
        return VisionRouteDecision(
            mode="bare",
            use_adapter=False,
            adapter_path=None,
            domain=domain,
            task=task,
            reason="dense/table domain: LoRA historically regresses (C66/C72); use bare",
            policy=policy,
        )

    if domain in allow and adapter_ok:
        return VisionRouteDecision(
            mode="lora",
            use_adapter=True,
            adapter_path=str(adapter),
            domain=domain,
            task=task,
            reason=f"weak/ok domain={domain}; adapter present → LoRA",
            policy=policy,
        )

    return VisionRouteDecision(
        mode="bare",
        use_adapter=False,
        adapter_path=None,
        domain=domain,
        task=task,
        reason=(
            f"default bare (domain={domain} not in weak-lora allowlist or adapter missing)"
        ),
        policy=policy,
    )

