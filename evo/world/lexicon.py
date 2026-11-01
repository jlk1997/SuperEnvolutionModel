"""A routed slot may say its own function names. Other slots' names stay shut.

The weights still have to remember order and arguments. This only stops yesterday's
name from being the easiest token when today's slot is the one in use.
"""

from __future__ import annotations

import torch
from transformers import LogitsProcessor


def name_token_ids(tokenizer, name: str) -> list[int]:
    """Token ids of a function name as it appears after an opening parenthesis."""
    wrapped = tokenizer.encode("(" + name, add_special_tokens=False)
    paren = tokenizer.encode("(", add_special_tokens=False)
    if paren and wrapped[: len(paren)] == paren and len(wrapped) > len(paren):
        return list(wrapped[len(paren) :])
    return list(tokenizer.encode(name, add_special_tokens=False))


def blocked_token_ids(allowed: list[list[int]], banned: list[list[int]]) -> list[int]:
    """Tokens that belong to a banned name and to no allowed name.

    Shared pieces, such as a syllable used by both names, stay available.
    """
    keep = {token for seq in allowed for token in seq}
    block = {token for seq in banned for token in seq if token not in keep}
    return sorted(block)


def apply_block(scores: torch.Tensor, block_ids: list[int]) -> torch.Tensor:
    if not block_ids:
        return scores
    out = scores.clone()
    out[:, list(block_ids)] = torch.finfo(out.dtype).min
    return out


class NameGate(LogitsProcessor):
    def __init__(self, block_ids: list[int]):
        self.block = [int(token) for token in block_ids]

    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor) -> torch.FloatTensor:
        return apply_block(scores, self.block)


def gate_for_task(tokenizer, slot_names: list[str], other_names: list[str], task_names: list[str]) -> list[int]:
    """Block other slots' names unless this task itself asks for them."""
    allowed_names = set(slot_names) | set(task_names)
    banned = [name for name in other_names if name not in allowed_names]
    if not banned:
        return []
    allowed = [name_token_ids(tokenizer, name) for name in allowed_names]
    blocked = [name_token_ids(tokenizer, name) for name in banned]
    return blocked_token_ids(allowed, blocked)
