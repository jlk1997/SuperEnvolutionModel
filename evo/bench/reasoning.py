"""Reasoning-gym style tasks. Use the library when it is installed, else a builtin set.

The builtin set is graded by the same integer check as the DSL families, so a
missing dependency does not stop the harness.
"""

from __future__ import annotations

import random

from evo.bench.families import Task, check_task


def builtin_reasoning(n: int, seed: int) -> list[Task]:
    rng = random.Random(seed)
    kinds = (_equation, _modulo, _count)
    tasks = []
    for index in range(n):
        tasks.append(kinds[index % len(kinds)](rng, index))
    return tasks


def load_reasoning(n: int, seed: int, name: str = "chain_sum") -> dict:
    """Prefer reasoning_gym. Fall back without changing the task fields."""
    try:
        import reasoning_gym
    except ImportError:
        return {"source": "builtin", "tasks": builtin_reasoning(n, seed)}
    try:
        data = reasoning_gym.create_dataset(name, size=n, seed=seed)
    except Exception as exc:
        return {"source": "builtin", "reason": type(exc).__name__, "tasks": builtin_reasoning(n, seed)}
    tasks = []
    for index, item in enumerate(data):
        question = str(item.get("question") or item.get("prompt") or "")
        answer = str(item.get("answer") or "")
        tasks.append(
            Task(
                family=f"rg-{name}",
                cluster="arith",
                prompt=question + "\nReply with the final answer only.",
                answer=answer,
                heldout=True,
                domain="reasoning",
            )
        )
        if index + 1 >= n:
            break
    if not tasks:
        return {"source": "builtin", "tasks": builtin_reasoning(n, seed)}
    return {"source": "reasoning_gym", "tasks": tasks}


def grade(task: Task, reply: str) -> bool:
    if task.domain == "reasoning" and not _looks_int(task.answer):
        return task.answer.strip() in (reply or "")
    return check_task(task, reply)


def _looks_int(text: str) -> bool:
    try:
        int(str(text).strip())
    except ValueError:
        return False
    return True


def _equation(rng: random.Random, index: int) -> Task:
    slope = rng.randint(2, 9)
    solution = rng.randint(-8, 8)
    bias = rng.randint(-6, 6)
    total = slope * solution + bias
    return Task(
        family="rg-equation",
        cluster="arith",
        prompt=f"Solve {slope}*x + {bias} = {total} for x. Reply with the integer only.",
        answer=str(solution),
        heldout=True,
        domain="reasoning",
    )


def _modulo(rng: random.Random, index: int) -> Task:
    del index
    base = rng.randint(10, 40)
    mod = rng.randint(3, 9)
    return Task(
        family="rg-modulo",
        cluster="arith",
        prompt=f"What is {base} mod {mod}? Reply with the integer only.",
        answer=str(base % mod),
        heldout=True,
        domain="reasoning",
    )


def _count(rng: random.Random, index: int) -> Task:
    del index
    lo = rng.randint(1, 5)
    hi = lo + rng.randint(3, 8)
    evens = len([value for value in range(lo, hi + 1) if value % 2 == 0])
    return Task(
        family="rg-count",
        cluster="list",
        prompt=f"How many even integers are there from {lo} through {hi}? Reply with the integer only.",
        answer=str(evens),
        heldout=True,
        domain="reasoning",
    )
