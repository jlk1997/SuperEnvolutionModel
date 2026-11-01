"""Learn from the model's own samples, and from a scaffolded teacher on those samples.

GRPO-lite keeps the completions the executor scored above the batch mean.
Reverse KL is computed on the student continuation, which is the on-policy half.
Both fit a 4-bit model because only one forward keeps a graph.
"""

from __future__ import annotations

import torch
import torch.nn.functional as F


def advantages(rewards: list[float]) -> list[float]:
    if not rewards:
        return []
    base = sum(rewards) / len(rewards)
    return [float(reward) - base for reward in rewards]


def positive_pairs(prompt: str, samples: list[dict], adv: list[float]) -> list[tuple[str, str]]:
    pairs = []
    for sample, score in zip(samples, adv):
        code = (sample.get("code") or "").strip()
        if score > 0 and code:
            pairs.append((prompt, code))
    return pairs


def reverse_kl(student_logits: torch.Tensor, teacher_logits: torch.Tensor) -> torch.Tensor:
    """KL(student || teacher) on matching continuation positions."""
    width = min(student_logits.size(1), teacher_logits.size(1))
    student = student_logits[:, :width, :].float()
    teacher = teacher_logits[:, :width, :].float()
    student_log = F.log_softmax(student, dim=-1)
    teacher_log = F.log_softmax(teacher, dim=-1)
    student_prob = student_log.exp()
    return (student_prob * (student_log - teacher_log)).sum(dim=-1).mean()


def _completion_logits(evo, prompt: str, completion: str, adapter: str, max_len: int):
    from evo.inner_loop import _device_batch, _encode_pair
    from evo.model import activate

    input_ids, labels = _encode_pair(evo, prompt, completion, max_len)
    positions = [index for index, label in enumerate(labels) if label != -100 and index > 0]
    if not positions:
        return None
    batch, _ = _device_batch(evo, input_ids)
    evo.model.config.use_cache = False
    with activate(evo.model, adapter):
        logits = evo.model(**batch).logits
    index = torch.tensor([pos - 1 for pos in positions], device=logits.device)
    return logits.index_select(1, index)


def reverse_kl_step(evo, student_prompt: str, teacher_prompt: str, completion: str, adapter: str, lr: float, max_len: int) -> dict:
    """One step that pulls the bare student toward the scaffolded teacher on this continuation."""
    if not completion.strip():
        return {"steps": 0, "loss": None}
    from evo.model import ensure_input_grads

    ensure_input_grads(evo.model)
    evo.trainable(adapter)
    params = [param for param in evo.model.parameters() if param.requires_grad]
    if not params:
        return {"steps": 0, "loss": None}
    opt = torch.optim.AdamW(params, lr=lr)
    evo.model.train()
    opt.zero_grad(set_to_none=True)
    student = _completion_logits(evo, student_prompt, completion, adapter, max_len)
    with torch.no_grad():
        teacher = _completion_logits(evo, teacher_prompt, completion, adapter, max_len)
    if student is None or teacher is None:
        del opt
        return {"steps": 0, "loss": None}
    loss = reverse_kl(student, teacher)
    if not torch.isfinite(loss):
        del opt
        return {"steps": 0, "loss": None}
    loss.backward()
    torch.nn.utils.clip_grad_norm_(params, 1.0)
    opt.step()
    value = float(loss.detach().item())
    del opt
    return {"steps": 1, "loss": value}


def onpolicy_update(evo, task: dict, tools: list[dict], cfg: dict, adapter: str, teacher_notes: str = "") -> dict:
    """Sample k programs from the bare model. Keep the ones above the mean. Then one KL step."""
    from evo.generate import generate
    from evo.outer_loop import sft_policy
    from evo.world.body import extract_code, grade_task, task_prompt

    k = max(1, int(cfg.get("grpo_k", 2)))
    temperature = float(cfg.get("temperature", 0.7))
    max_new = int(cfg.get("max_new_code", 80))
    timeout = float(cfg.get("exec_timeout", 2.0))
    bare = task_prompt(task, "", "")
    samples = []
    for _ in range(k):
        reply = generate(evo, bare, max_new, temperature, adapter)
        code = extract_code(reply)
        ok, _result = grade_task(code or "raise SystemExit('empty')", task, tools, None, timeout)
        samples.append({"code": code, "reward": 1.0 if ok else 0.0})
    scores = advantages([sample["reward"] for sample in samples])
    pairs = positive_pairs(bare, samples, scores)
    steps = 0
    loss = None
    if pairs:
        stats = sft_policy(
            evo,
            pairs,
            float(cfg.get("outer_lr", 5e-4)),
            1,
            int(cfg.get("max_seq_len", 384)),
            adapter=adapter,
        )
        steps += int(stats["steps"])
        loss = stats["loss"]
    codes = [sample["code"] for sample in samples if sample["code"]]
    kl = {"steps": 0, "loss": None}
    if teacher_notes:
        taught = task_prompt(task, "", teacher_notes)
        target = ""
        if pairs:
            target = pairs[0][1]
        else:
            reply = generate(evo, taught, max_new, 0.0, adapter)
            target = extract_code(reply)
            if target:
                codes.append(target)
        if target:
            kl = reverse_kl_step(
                evo,
                bare,
                taught,
                target,
                adapter,
                float(cfg.get("outer_lr", 5e-4)),
                int(cfg.get("max_seq_len", 384)),
            )
            steps += int(kl["steps"])
    return {"steps": steps, "loss": loss, "codes": codes, "rewards": [sample["reward"] for sample in samples], "kl": kl["loss"]}


def multiturn_update(evo, prompt: str, traces: list[dict], cfg: dict, adapter: str, teacher_prompt: str = "", sites: list[str] | None = None) -> dict:
    """GRPO-lite on whole tool-call traces, then one reverse-KL step toward the scaffolded teacher."""
    rewards = [float(trace.get("reward", 0.0)) for trace in traces]
    scores = advantages(rewards)
    pairs = []
    for trace, score in zip(traces, scores):
        text = (trace.get("text") or "").strip()
        if score > 0 and text:
            pairs.append((prompt, text))
    steps = 0
    loss = None
    if pairs:
        stats = sft_update(evo, pairs, cfg, adapter, sites)
        steps += int(stats["steps"])
        loss = stats["loss"]
    kl = {"steps": 0, "loss": None}
    target = pairs[0][1] if pairs else ""
    if teacher_prompt and target:
        kl = reverse_kl_step(
            evo,
            prompt,
            teacher_prompt,
            target,
            adapter,
            float(cfg.get("outer_lr", 5e-4)),
            int(cfg.get("max_seq_len", 384)),
        )
        steps += int(kl["steps"])
    return {"steps": steps, "loss": loss, "pairs": len(pairs), "kl": kl["loss"]}


def sft_update(evo, pairs: list[tuple[str, str]], cfg: dict, adapter: str, sites: list[str] | None = None) -> dict:
    from evo.outer_loop import sft_policy

    stats = sft_policy(
        evo,
        pairs,
        float(cfg.get("outer_lr", 5e-4)),
        1,
        int(cfg.get("max_seq_len", 384)),
        adapter=adapter,
        sites=sites,
    )
    return {"steps": int(stats["steps"]), "loss": stats["loss"], "codes": [code for _prompt, code in pairs]}
