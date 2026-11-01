"""Inner-loop adaptation on the scratch adapter, plus KL to a frozen teacher."""

from __future__ import annotations

import torch
import torch.nn.functional as F

from evo.generate import generate, qa_prompt, teacher_prompt
from evo.model import activate


def _device_batch(evo, input_ids, labels=None):
    ids = torch.tensor([input_ids], device=evo.device)
    attn = torch.ones_like(ids)
    batch = {"input_ids": ids, "attention_mask": attn}
    label_tensor = None if labels is None else torch.tensor([labels], device=evo.device)
    return batch, label_tensor


def _encode_pair(evo, prompt: str, completion: str, max_len: int):
    from evo.generate import render_user

    prompt_text, add_special = render_user(evo.tok, prompt)
    prompt_ids = evo.tok(prompt_text, add_special_tokens=add_special)["input_ids"]
    completion_ids = evo.tok(
        completion + (evo.tok.eos_token or ""), add_special_tokens=False
    )["input_ids"]
    input_ids = prompt_ids + completion_ids
    labels = [-100] * len(prompt_ids) + completion_ids
    if len(input_ids) > max_len:
        overflow = len(input_ids) - max_len
        input_ids = input_ids[overflow:]
        labels = labels[overflow:]
    return input_ids, labels


def _loss_or_none(evo, text: str, max_len: int):
    """A one-token note cannot train. Callers keep going with the other terms."""
    try:
        return causal_loss(evo, text, max_len)
    except ValueError:
        return None


def causal_loss(evo, text: str, max_len: int):
    ids = evo.tok(text, add_special_tokens=False, truncation=True, max_length=max_len)["input_ids"]
    if len(ids) < 2:
        raise ValueError("training text is too short")
    batch, labels = _device_batch(evo, ids, ids)
    evo.model.config.use_cache = False
    return evo.model(**batch, labels=labels).loss


def _answer_logits(evo, prompt: str, answer_ids: list[int], adapter: str | None):
    from evo.generate import render_user

    prompt_text, add_special = render_user(evo.tok, prompt)
    prompt_ids = evo.tok(prompt_text, add_special_tokens=add_special)["input_ids"]
    ids = prompt_ids + list(answer_ids)
    batch, _ = _device_batch(evo, ids)
    with activate(evo.model, adapter):
        logits = evo.model(**batch).logits
    start = len(prompt_ids) - 1
    return logits[:, start : start + len(answer_ids), :]


@torch.no_grad()
def build_distill_cache(evo, passage: str, questions: list[dict], answer_tokens: int, limit: int):
    """Frozen base reads the passage and produces the soft answer target."""
    cache = []
    evo.model.eval()
    for item in questions[:limit]:
        answer = generate(
            evo,
            teacher_prompt(passage, item["question"]),
            answer_tokens,
            0.0,
            adapter=None,
        ).split("\n", 1)[0].strip()
        if not answer:
            continue
        answer_ids = evo.tok(answer, add_special_tokens=False)["input_ids"][:answer_tokens]
        if not answer_ids:
            continue
        teacher = _answer_logits(evo, teacher_prompt(passage, item["question"]), answer_ids, None)
        cache.append(
            {
                "question": item["question"],
                "answer": answer,
                "answer_ids": answer_ids,
                "teacher_logits": teacher.detach(),
            }
        )
    return cache


@torch.no_grad()
def build_memory_cache(evo, questions: list[dict], answer_tokens: int, limit: int, adapter: str = "memory"):
    """Current memory answers old questions. The student must stay close to those answers."""
    cache = []
    evo.model.eval()
    for item in questions[:limit]:
        prompt = qa_prompt(item["question"])
        answer = generate(evo, prompt, answer_tokens, 0.0, adapter=adapter).split("\n", 1)[0].strip()
        if not answer:
            continue
        answer_ids = evo.tok(answer, add_special_tokens=False)["input_ids"][:answer_tokens]
        if not answer_ids:
            continue
        teacher = _answer_logits(evo, prompt, answer_ids, adapter)
        cache.append(
            {
                "question": item["question"],
                "answer": answer,
                "answer_ids": answer_ids,
                "teacher_logits": teacher.detach(),
            }
        )
    return cache


def distill_kl(evo, cache) -> torch.Tensor:
    total = None
    count = 0
    for item in cache:
        student = _answer_logits(evo, qa_prompt(item["question"]), item["answer_ids"], "scratch")
        teacher = item["teacher_logits"].to(device=student.device, dtype=student.dtype)
        steps = min(student.size(1), teacher.size(1))
        if steps <= 0:
            continue
        log_student = F.log_softmax(student[:, :steps, :].float(), dim=-1)
        teacher_prob = F.softmax(teacher[:, :steps, :].float(), dim=-1)
        kl = F.kl_div(log_student, teacher_prob, reduction="none").sum(dim=-1).mean()
        total = kl if total is None else total + kl
        count += 1
    if total is None:
        return torch.zeros((), device=evo.device)
    return total / count


@torch.no_grad()
def kl_between(evo, text: str, adapter_ref: str, adapter_new: str, max_len: int) -> float:
    """KL(ref || new) on `text`. How far the candidate moved from the reference."""
    ids = evo.tok(text, add_special_tokens=False, truncation=True, max_length=max_len)["input_ids"]
    if len(ids) < 2:
        return 0.0
    batch, _ = _device_batch(evo, ids)
    evo.model.eval()
    with activate(evo.model, adapter_ref):
        ref_logits = evo.model(**batch).logits
    with activate(evo.model, adapter_new):
        new_logits = evo.model(**batch).logits
    log_new = F.log_softmax(new_logits.float(), dim=-1)
    ref_prob = F.softmax(ref_logits.float(), dim=-1)
    kl = F.kl_div(log_new, ref_prob, reduction="none").sum(dim=-1)
    return float(kl.mean().item())


def _pair_loss(evo, prompt: str, completion: str, max_len: int):
    input_ids, labels = _encode_pair(evo, prompt, completion, max_len)
    if not any(label != -100 for label in labels):
        return None
    batch, label_tensor = _device_batch(evo, input_ids, labels)
    evo.model.config.use_cache = False
    return evo.model(**batch, labels=label_tensor).loss


def adapt_scratch(
    evo,
    text: str,
    steps: int,
    lr: float,
    max_len: int,
    kl_coef: float = 0.0,
    distill_cache=None,
    grad_clip: float = 1.0,
    replay_text: str | None = None,
    replay_coef: float = 0.5,
    pairs: list[tuple[str, str]] | None = None,
    pair_coef: float = 1.0,
) -> tuple[float, int]:
    """Train scratch only. Caller chooses whether scratch starts from memory or identity.

    `pairs` are prompt/completion rows (a quiz or a trajectory). Prompt tokens are masked.
    """
    params_n = evo.trainable("scratch")
    params = [param for param in evo.model.parameters() if param.requires_grad]
    if not params:
        raise RuntimeError("scratch adapter has no trainable parameters")
    opt = torch.optim.AdamW(params, lr=lr)
    evo.model.train()
    evo.model.config.use_cache = False
    losses = []
    for step in range(steps):
        evo.set_adapter("scratch")
        opt.zero_grad(set_to_none=True)
        loss = _loss_or_none(evo, text, max_len)
        if replay_text and replay_text.strip():
            replay_loss = _loss_or_none(evo, replay_text, max_len)
            if replay_loss is not None:
                loss = replay_loss * replay_coef if loss is None else loss + replay_coef * replay_loss
        if pairs:
            prompt, completion = pairs[step % len(pairs)]
            extra = _pair_loss(evo, prompt, completion, max_len)
            if extra is not None:
                loss = extra * pair_coef if loss is None else loss + pair_coef * extra
        if kl_coef and distill_cache and loss is not None:
            loss = loss + kl_coef * distill_kl(evo, distill_cache)
        if loss is None or not torch.isfinite(loss):
            break
        loss.backward()
        torch.nn.utils.clip_grad_norm_(params, grad_clip)
        opt.step()
        losses.append(float(loss.detach().item()))
        if step == 0 or step + 1 == steps or (step + 1) % 10 == 0:
            print(f"[inner] step={step + 1}/{steps} loss={losses[-1]:.3f}", flush=True)
    del opt
    return sum(losses) / len(losses) if losses else float("inf"), params_n
