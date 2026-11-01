"""Within-life loop on a real LoRA model, plus a model-free loop the tests drive.

The gate is the same one the reference organism uses: competence starts under
0.2 and clears 0.6 inside the episode budget. A miss tells the run to move up
a base size or to recalibrate difficulty. It does not lower the gate.
"""

from __future__ import annotations

from evo.bench.families import Task, check_task
from evo.plastic.signal import learning_signal, with_verifier


def run_verified_loop(tasks: list[Task], act, teach, cfg: dict | None = None) -> dict:
    """`act(task) -> reply`. `teach(pairs) -> steps`. Competence is the running hit rate."""
    cfg = cfg or {}
    signal = learning_signal(cfg)
    hits = []
    sources = []
    steps = 0
    for task in tasks:
        samples = [act(task) for _ in range(signal["grpo_k"])]
        chosen = with_verifier(task.prompt, samples, lambda reply, task=task: check_task(task, reply), task.answer)
        # Grade the first draw. Teaching happens after the attempt, as in a real episode.
        hits.append(check_task(task, samples[0] if samples else ""))
        if chosen["pairs"]:
            steps += int(teach(chosen["pairs"]) or 0)
        sources.append(chosen["source"])
    head = hits[: max(1, len(hits) // 5)]
    tail = hits[-max(1, len(hits) // 5) :]
    return {
        "hits": hits,
        "start": sum(head) / len(head),
        "end": sum(tail) / len(tail),
        "steps": steps,
        "sources": sources,
        "grpo_k": signal["grpo_k"],
        "temperature": signal["temperature"],
    }


def run_model_m0(cfg: dict) -> dict:
    """Fit a real base on one family. The batch and the sites are the optimized path."""
    from evo.plastic.fit import run_model_fit

    return run_model_fit(cfg)
