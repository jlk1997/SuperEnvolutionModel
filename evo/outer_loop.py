"""ReST-EM outer loop: supervised update on self-edits that earned positive reward."""

from __future__ import annotations

import torch

from evo.inner_loop import _encode_pair


def sft_policy(
    evo,
    pairs: list[tuple[str, str]],
    lr: float,
    epochs: int,
    max_len: int,
    grad_clip: float = 1.0,
    adapter: str = "policy",
    sites: list[str] | None = None,
    batch_size: int = 1,
    opt=None,
) -> dict:
    """`batch_size` > 1 right-pads each batch. Labels on padding are -100.

    Pass `opt` to keep AdamW moments across calls. It must hold the same parameters.
    """
    if not pairs:
        return {"steps": 0, "loss": None, "pairs": 0}
    from evo.model import ensure_input_grads, set_trainable_sites

    ensure_input_grads(evo.model)
    # Pairing a slot with policy marks both trainable. Freeze policy again afterwards.
    evo.set_adapter(adapter, inference=False)
    if sites:
        set_trainable_sites(evo.model, adapter, sites)
    else:
        evo.trainable(adapter)
    params = [param for param in evo.model.parameters() if param.requires_grad]
    if not params:
        return {"steps": 0, "loss": None, "pairs": len(pairs), "sites": list(sites or [])}
    owned = opt is None
    if owned:
        opt = torch.optim.AdamW(params, lr=lr)
    else:
        for group in opt.param_groups:
            group["lr"] = lr
    evo.model.train()
    evo.model.config.use_cache = False
    losses = []
    steps = 0
    encoded = [_encode_pair(evo, prompt, completion, max_len) for prompt, completion in pairs]
    encoded = [row for row in encoded if any(label != -100 for label in row[1])]
    width = max(1, int(batch_size))
    pad = evo.tok.pad_token_id if evo.tok.pad_token_id is not None else 0
    for _ in range(epochs):
        for start in range(0, len(encoded), width):
            chunk = encoded[start : start + width]
            batch_ids, batch_labels, attn = pad_right(chunk, pad, evo.device)
            opt.zero_grad(set_to_none=True)
            loss = evo.model(input_ids=batch_ids, attention_mask=attn, labels=batch_labels).loss
            if not torch.isfinite(loss):
                continue
            loss.backward()
            torch.nn.utils.clip_grad_norm_(params, grad_clip)
            opt.step()
            losses.append(float(loss.detach().item()))
            steps += 1
    if owned:
        del opt
    return {
        "steps": steps,
        "loss": (sum(losses) / len(losses)) if losses else None,
        "pairs": len(pairs),
        "sites": list(sites or []),
    }


def pad_right(rows: list[tuple[list[int], list[int]]], pad: int, device):
    """Right padding keeps every prompt at position 0. Padded labels are ignored."""
    width = max(len(ids) for ids, _labels in rows)
    ids = torch.full((len(rows), width), int(pad), dtype=torch.long)
    labels = torch.full((len(rows), width), -100, dtype=torch.long)
    attn = torch.zeros((len(rows), width), dtype=torch.long)
    for row, (row_ids, row_labels) in enumerate(rows):
        ids[row, : len(row_ids)] = torch.tensor(row_ids, dtype=torch.long)
        labels[row, : len(row_labels)] = torch.tensor(row_labels, dtype=torch.long)
        attn[row, : len(row_ids)] = 1
    return ids.to(device), labels.to(device), attn.to(device)
