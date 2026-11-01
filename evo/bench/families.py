"""Fictional tool families that share a grammar and hide the base model's memory.

Train families and held-out families use different primitives. Some held-out
families also use a composition template the training families never show.
Answers are integers, so a program can grade them.
"""

from __future__ import annotations

import random
import re
from dataclasses import dataclass


CLUSTERS = ("arith", "text", "list", "logic")

_OPS = {
    "arith": (
        ("shift", lambda x, k: (x + k) % 50),
        ("spin", lambda x, k: (x * k + 1) % 50),
        ("fold", lambda x, k: (k * 3 - x) % 50),
        ("jump", lambda x, k: (x * 2 + k) % 50),
        ("wrap", lambda x, k: (x + k * k) % 50),
        ("tilt", lambda x, k: (k * x - 2) % 50),
    ),
    "text": (
        ("flip", lambda x, k: (k * 4 - x) % 40),
        ("echo", lambda x, k: (x + x + k) % 40),
        ("trim", lambda x, k: (x // 2 + k) % 40),
        ("mark", lambda x, k: (x * k) % 40),
        ("notch", lambda x, k: (x + 3 * k) % 40),
        ("stamp", lambda x, k: ((x + 1) * k) % 40),
    ),
    "list": (
        ("pick", lambda x, k: (x + k) % 30),
        ("drop", lambda x, k: (x - k) % 30),
        ("pair", lambda x, k: (2 * x + k) % 30),
        ("swap", lambda x, k: (k - 2 * x) % 30),
        ("heap", lambda x, k: (x * x + k) % 30),
        ("sift", lambda x, k: (x + k + 5) % 30),
    ),
    "logic": (
        ("gate", lambda x, k: (x + k) % 2 + (x % 5)),
        ("both", lambda x, k: ((x * k) % 7)),
        ("either", lambda x, k: (x + 2 * k) % 11),
        ("none", lambda x, k: (3 * k - x) % 9),
        ("iff", lambda x, k: (x * 3 + k) % 13),
        ("xor", lambda x, k: (x + k * k) % 8),
    ),
}

# Python form of each primitive. The prompt shows `mod` so a small model can read it.
# `sample` and the fitter both go through `render_prompt`, so the trained string is the scored string.
_EXPR = {
    ("arith", "shift"): "(n + {k}) % 50",
    ("arith", "spin"): "(n * {k} + 1) % 50",
    ("arith", "fold"): "({k} * 3 - n) % 50",
    ("arith", "jump"): "(n * 2 + {k}) % 50",
    ("arith", "wrap"): "(n + {k} * {k}) % 50",
    ("arith", "tilt"): "({k} * n - 2) % 50",
    ("text", "flip"): "({k} * 4 - n) % 40",
    ("text", "echo"): "(n + n + {k}) % 40",
    ("text", "trim"): "(n // 2 + {k}) % 40",
    ("text", "mark"): "(n * {k}) % 40",
    ("text", "notch"): "(n + 3 * {k}) % 40",
    ("text", "stamp"): "((n + 1) * {k}) % 40",
    ("list", "pick"): "(n + {k}) % 30",
    ("list", "drop"): "(n - {k}) % 30",
    ("list", "pair"): "(2 * n + {k}) % 30",
    ("list", "swap"): "({k} - 2 * n) % 30",
    ("list", "heap"): "(n * n + {k}) % 30",
    ("list", "sift"): "(n + {k} + 5) % 30",
    ("logic", "gate"): "((n + {k}) % 2) + (n % 5)",
    ("logic", "both"): "(n * {k}) % 7",
    ("logic", "either"): "(n + 2 * {k}) % 11",
    ("logic", "none"): "(3 * {k} - n) % 9",
    ("logic", "iff"): "(n * 3 + {k}) % 13",
    ("logic", "xor"): "(n + {k} * {k}) % 8",
}

_SYLLABLES = ("zor", "nub", "vek", "pim", "qal", "rix", "fom", "jad", "wex", "luk", "bri", "tav")
_TEMPLATES = ("then", "before", "branch")


@dataclass(frozen=True)
class Family:
    id: str
    cluster: str
    heldout: bool
    template: str
    left_name: str
    right_name: str
    left_op: str
    right_op: str
    left_k: int
    right_k: int
    domain: str = "dsl"

    def sample(self, rng: random.Random, x: int | None = None, reveal: bool = True) -> "Task":
        value = rng.randint(0, 36) if x is None else int(x)
        return task_at(self, value, reveal=reveal)


@dataclass(frozen=True)
class Task:
    family: str
    cluster: str
    prompt: str
    answer: str
    heldout: bool
    domain: str


def apply_family(family: Family, value: int) -> int:
    left = _call(family.cluster, family.left_op, value, family.left_k)
    right = _call(family.cluster, family.right_op, value, family.right_k)
    if family.template == "then":
        return _call(family.cluster, family.right_op, left, family.right_k)
    if family.template == "before":
        return _call(family.cluster, family.left_op, right, family.left_k)
    if value % 2 == 0:
        return left
    return right


def _call(cluster: str, op: str, value: int, k: int) -> int:
    for name, fn in _OPS[cluster]:
        if name == op:
            return int(fn(int(value), int(k)))
    raise KeyError(op)


def formula(cluster: str, op: str, k: int) -> str:
    """Readable rule. `mod` is the prompt spelling of Python `%`."""
    return _EXPR[(cluster, op)].format(k=int(k)).replace("%", "mod")


def eval_formula(cluster: str, op: str, n: int, k: int) -> int:
    expr = _EXPR[(cluster, op)].format(k=int(k))
    return int(eval(expr, {"__builtins__": {}}, {"n": int(n)}))


def render_prompt(family: Family, value: int, reveal: bool = True) -> str:
    """`reveal` puts the two rules in the prompt. Hidden prompts keep only the names and the input."""
    question = _template_text(family, value)
    if reveal:
        head = (
            f"{family.left_name}(n) = {formula(family.cluster, family.left_op, family.left_k)}.\n"
            f"{family.right_name}(n) = {formula(family.cluster, family.right_op, family.right_k)}."
        )
    else:
        head = f"Apply {family.left_name} and {family.right_name} as you were taught."
    return (
        f"{head}\n{question}\n"
        f"n = {value}\n"
        "Write the steps, then the last line exactly as answer: <integer>."
    )


def worked_trace(family: Family, value: int) -> str:
    """The steps a correct solution writes. The last integer is the graded answer."""
    x = int(value)
    left = _call(family.cluster, family.left_op, x, family.left_k)
    right = _call(family.cluster, family.right_op, x, family.right_k)
    if family.template == "then":
        final = _call(family.cluster, family.right_op, left, family.right_k)
        body = f"{family.left_name}({x}) = {left}\n{family.right_name}({left}) = {final}"
    elif family.template == "before":
        final = _call(family.cluster, family.left_op, right, family.left_k)
        body = f"{family.right_name}({x}) = {right}\n{family.left_name}({right}) = {final}"
    else:
        final = left if x % 2 == 0 else right
        taken = family.left_name if x % 2 == 0 else family.right_name
        body = f"{taken}({x}) = {final}"
    return f"{body}\nanswer: {final}"


def task_at(family: Family, value: int, reveal: bool = True) -> Task:
    return Task(
        family=family.id,
        cluster=family.cluster,
        prompt=render_prompt(family, value, reveal=reveal),
        answer=str(apply_family(family, value)),
        heldout=family.heldout,
        domain=family.domain,
    )


def _template_text(family: Family, value: int) -> str:
    if family.template == "then":
        return f"Compute {family.right_name}({family.left_name}({value}))."
    if family.template == "before":
        return f"Compute {family.left_name}({family.right_name}({value}))."
    return (
        f"If {value} is even compute {family.left_name}({value}), "
        f"otherwise compute {family.right_name}({value})."
    )


def substituted(cluster: str, op: str, n: int, k: int) -> str:
    """Plug n into the rule and show the result. This is the single-step training target."""
    shown = _EXPR[(cluster, op)].format(k=int(k)).replace("n", str(int(n))).replace("%", "mod")
    return f"{shown} = {eval_formula(cluster, op, n, k)}"


def grade_reply(text: str) -> int | None:
    """An answer line counts. A reply that is only an integer counts. A restated rule does not."""
    for line in reversed((text or "").splitlines()):
        stripped = line.strip()
        if stripped.lower().startswith("answer"):
            return parse_int(stripped)
        if "=" in stripped:
            return parse_int(stripped.split("=", 1)[1])
    stripped = (text or "").strip()
    if re.fullmatch(r"-?\d+", stripped):
        return int(stripped)
    return None


def parse_int(text: str) -> int | None:
    found = re.findall(r"-?\d+", text or "")
    if not found:
        return None
    return int(found[-1])


def check_task(task: Task, reply: str) -> bool:
    got = parse_int(reply)
    if got is None:
        return False
    try:
        return got == int(task.answer)
    except ValueError:
        return False


def build_catalog(n_train: int = 12, n_heldout: int = 32, seed: int = 0) -> list[Family]:
    """`n_train` and `n_heldout` are split evenly across the four clusters."""
    if n_train < 4 or n_heldout < 4:
        raise ValueError("need at least one family per cluster on each split")
    rng = random.Random(seed)
    used: set[str] = set()
    families = []
    per_train = n_train // len(CLUSTERS)
    per_held = n_heldout // len(CLUSTERS)
    for cluster in CLUSTERS:
        for index in range(per_train):
            families.append(_family(rng, used, cluster, index, heldout=False))
        for index in range(per_held):
            families.append(_family(rng, used, cluster, per_train + index, heldout=True))
    return families


def split_catalog(families: list[Family]) -> tuple[list[Family], list[Family]]:
    train = [family for family in families if not family.heldout]
    held = [family for family in families if family.heldout]
    return train, held


def families_in(families: list[Family], cluster: str, heldout: bool) -> list[Family]:
    return [family for family in families if family.cluster == cluster and family.heldout is heldout]


def sample_stream(families: list[Family], n: int, seed: int) -> list[Task]:
    """Same seed, same tasks. This is the common-random-number stream."""
    rng = random.Random(seed)
    if not families:
        return []
    picked = [families[rng.randrange(len(families))] for _ in range(n)]
    return [family.sample(rng) for family in picked]


def _family(rng: random.Random, used: set[str], cluster: str, index: int, heldout: bool) -> Family:
    ops = _OPS[cluster]
    # Training stays on the first half of the primitive list. Held-out takes the rest.
    pool = ops[len(ops) // 2 :] if heldout else ops[: len(ops) // 2]
    left = pool[index % len(pool)]
    right = pool[(index + 1) % len(pool)]
    template = "branch" if heldout and index % 4 == 0 else ("then" if index % 2 == 0 else "before")
    return Family(
        id=f"{'h' if heldout else 't'}-{cluster}-{index}",
        cluster=cluster,
        heldout=heldout,
        template=template,
        left_name=_fresh(rng, used),
        right_name=_fresh(rng, used),
        left_op=left[0],
        right_op=right[0],
        left_k=rng.randint(2, 8),
        right_k=rng.randint(2, 8),
    )


def _fresh(rng: random.Random, used: set[str]) -> str:
    for _ in range(1000):
        name = rng.choice(_SYLLABLES) + rng.choice(_SYLLABLES)
        if name not in used:
            used.add(name)
            return name
    raise RuntimeError("ran out of tool names")
