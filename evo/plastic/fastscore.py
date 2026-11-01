"""Exam scoring in one forward pass, and batched greedy generation.

`exact_hits` teacher-forces prompt + target. If the argmax at every target
position is the target token, greedy decoding writes exactly the target and
stops. A reply that is right in a different format counts as a miss, so this
is for picking epochs after the format is trained. Birth and the final report
use `generate_batch` and `grade_reply`.
"""

from __future__ import annotations

import torch

from evo.model import activate


def exact_hits(evo, pairs: list[tuple[str, str]], adapter, batch_size: int = 8, max_len: int = 256) -> list[dict]:
    """One row per pair: `hit` and `margin` (smallest target-minus-runner-up logit).

    The end-of-turn token is not checked. `grade_reply` reads the last `=` line, so
    a reply that writes the whole trace and then stops differently still counts.
    """
    from evo.inner_loop import _encode_pair
    from evo.outer_loop import pad_right

    if not pairs:
        return []
    model = evo.model
    model.eval()
    pad = evo.tok.pad_token_id if evo.tok.pad_token_id is not None else 0
    eos = evo.tok.eos_token_id
    encoded = []
    for prompt, completion in pairs:
        ids, labels = _encode_pair(evo, prompt, completion, max_len)
        if eos is not None and labels and labels[-1] == eos:
            labels = labels[:-1] + [-100]
        encoded.append((ids, labels))
    rows: list[dict] = []
    previous = model.config.use_cache
    model.config.use_cache = False
    with activate(model, adapter), torch.no_grad():
        for start in range(0, len(encoded), max(1, int(batch_size))):
            chunk = encoded[start : start + int(batch_size)]
            ids, labels, attn = pad_right(chunk, pad, evo.device)
            logits = model(input_ids=ids, attention_mask=attn).logits
            rows.extend(_rows(logits[:, :-1, :], labels[:, 1:]))
            del logits
    model.config.use_cache = previous
    return rows


def _rows(logits: torch.Tensor, labels: torch.Tensor) -> list[dict]:
    out = []
    for row in range(labels.shape[0]):
        mask = labels[row] != -100
        if not bool(mask.any()):
            out.append({"hit": False, "margin": -1e9})
            continue
        picked = logits[row][mask].float()
        target = labels[row][mask]
        gold = picked.gather(1, target.unsqueeze(1)).squeeze(1)
        rival = picked.clone()
        rival.scatter_(1, target.unsqueeze(1), float("-inf"))
        margin = gold - rival.max(dim=1).values
        out.append({"hit": bool((picked.argmax(dim=1) == target).all()), "margin": float(margin.min())})
    return out


def exact_rate(evo, pairs: list[tuple[str, str]], adapter, batch_size: int = 8, max_len: int = 256) -> dict:
    rows = exact_hits(evo, pairs, adapter, batch_size=batch_size, max_len=max_len)
    hits = [row["hit"] for row in rows]
    margins = [max(-20.0, min(20.0, row["margin"])) for row in rows]
    return {
        "rate": sum(hits) / len(hits) if hits else 0.0,
        "margin": sum(margins) / len(margins) if margins else 0.0,
        "hits": hits,
    }


def generate_batch(evo, prompts: list[str], max_new: int, adapter, batch_size: int = 16, max_len: int = 1024) -> list[str]:
    """Greedy, left-padded. Same decoding as `evo.generate.generate`, many prompts per call.

    A prompt may be a chat message list instead of one user string.
    Long prompts or long replies shrink the batch. On the 8 GB laptop card a 16-wide
    batch of 8-shot prompts with 256 new tokens spilled into shared memory and stalled.
    """
    from evo.generate import render_messages, render_user

    if not prompts:
        return []
    longest = max(len(str(prompt)) for prompt in prompts) // 3 + int(max_new)
    batch_size = max(1, min(int(batch_size), int(4096 // max(1, longest)) or 1))
    model, tok = evo.model, evo.tok
    model.eval()
    side = tok.padding_side
    tok.padding_side = "left"
    previous = model.config.use_cache
    model.config.use_cache = True
    replies: list[str] = []
    try:
        with activate(model, adapter), torch.no_grad():
            for start in range(0, len(prompts), max(1, int(batch_size))):
                texts = []
                add_special = False
                for prompt in prompts[start : start + int(batch_size)]:
                    if isinstance(prompt, list):
                        text, add_special = render_messages(tok, prompt)
                    else:
                        text, add_special = render_user(tok, prompt)
                    texts.append(text)
                encoded = tok(
                    texts,
                    return_tensors="pt",
                    padding=True,
                    add_special_tokens=add_special,
                    truncation=True,
                    max_length=max_len,
                )
                encoded = {key: value.to(evo.device) for key, value in encoded.items()}
                output = model.generate(
                    **encoded,
                    max_new_tokens=int(max_new),
                    do_sample=False,
                    pad_token_id=tok.pad_token_id,
                    eos_token_id=tok.eos_token_id,
                )
                width = encoded["input_ids"].shape[1]
                for row in output:
                    replies.append(tok.decode(row[width:], skip_special_tokens=True).strip())
    finally:
        tok.padding_side = side
        model.config.use_cache = previous
        torch.cuda.empty_cache()
    return replies


def graded_rate(evo, prompts: list[str], answers: list[int], max_new: int, adapter, batch_size: int = 16) -> dict:
    from evo.bench.families import grade_reply

    replies = generate_batch(evo, prompts, max_new, adapter, batch_size=batch_size)
    hits = []
    lengths = []
    for reply, answer in zip(replies, answers):
        got = grade_reply(reply)
        hits.append(got is not None and got == int(answer))
        lengths.append(len(evo.tok(reply, add_special_tokens=False)["input_ids"]))
    return {
        "rate": sum(hits) / len(hits) if hits else 0.0,
        "hits": hits,
        "replies": replies,
        "tokens": sum(lengths) / len(lengths) if lengths else 0.0,
    }


def agreement(fast_hits: list[bool], real_hits: list[bool]) -> float:
    """Share of questions where the one-pass check and real decoding agree."""
    if len(fast_hits) != len(real_hits) or not fast_hits:
        return 0.0
    return sum(1 for left, right in zip(fast_hits, real_hits) if left == right) / len(fast_hits)
