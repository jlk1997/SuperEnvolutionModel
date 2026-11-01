"""Where a write is allowed to land inside the network.

A day micro-update touches only the DeltaNet projections. The night
replay that consolidates a skill also trains the MLP, which is what
actually moves the loss. The slow core is the only place that may
touch attention, DeltaNet, and the MLP together.
"""

from __future__ import annotations

from evo.model import LORA_SITES


def sites_for(phase: str, dest: str) -> list[str]:
    if dest in {"retrieval", "fast", "drop"}:
        return []
    if dest == "core":
        return list(LORA_SITES["attn"]) + list(LORA_SITES["delta"]) + list(LORA_SITES["mlp"])
    if phase == "night":
        return list(LORA_SITES["delta"]) + list(LORA_SITES["mlp"])
    return list(LORA_SITES["delta"])
