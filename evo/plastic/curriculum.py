"""Rules the model has to learn, and the birth test that drops rules it already knows.

Every rule maps n in 0..49 to an integer. The 50 inputs are split once into a
training pool, a selection set, and a report set. A rule counts as new only if
the base model misses it even with worked examples in the prompt. `n * 5` was
answered at birth, so a zero-shot miss alone is not enough.

`shown` prompts write the rule. `named` prompts give only the name, so the rule
has to live in the weights.
"""

from __future__ import annotations

import ast
import random
from dataclasses import dataclass


_PREC = {ast.Add: 1, ast.Sub: 1, ast.Mult: 2, ast.FloorDiv: 2, ast.Mod: 2}
_SYMBOL = {ast.Add: "+", ast.Sub: "-", ast.Mult: "*", ast.FloorDiv: "//", ast.Mod: "mod"}
_APPLY = {
    ast.Add: lambda left, right: left + right,
    ast.Sub: lambda left, right: left - right,
    ast.Mult: lambda left, right: left * right,
    ast.FloorDiv: lambda left, right: left // right,
    ast.Mod: lambda left, right: left % right,
}


def reduce_steps(expr: str) -> list[str]:
    """`(37 * 7 + 4) % 50` -> ["(37 * 7 + 4) mod 50", "(259 + 4) mod 50", "263 mod 50", "13"]."""
    tree = ast.parse(expr, mode="eval").body
    steps = [_render(tree)]
    while not isinstance(tree, ast.Constant):
        tree = _reduce_one(tree)
        steps.append(_render(tree))
    return steps


def _reduce_one(node):
    if isinstance(node, ast.BinOp):
        if isinstance(node.left, ast.Constant) and isinstance(node.right, ast.Constant):
            left, right = int(node.left.value), int(node.right.value)
            if isinstance(node.op, ast.Mult) and abs(left) >= 10 and abs(right) >= 10 and right % 10:
                # 37 * 37 -> 37 * 30 + 37 * 7. The 1.5B misses a two-digit product written in one step.
                tens, ones = right - right % 10, right % 10
                return ast.BinOp(
                    ast.BinOp(ast.Constant(left), ast.Mult(), ast.Constant(tens)),
                    ast.Add(),
                    ast.BinOp(ast.Constant(left), ast.Mult(), ast.Constant(ones)),
                )
            return ast.Constant(_APPLY[type(node.op)](left, right))
        if not isinstance(node.left, ast.Constant):
            return ast.BinOp(_reduce_one(node.left), node.op, node.right)
        return ast.BinOp(node.left, node.op, _reduce_one(node.right))
    if isinstance(node, ast.UnaryOp) and isinstance(node.operand, ast.Constant):
        return ast.Constant(int(-node.operand.value))
    raise ValueError(f"cannot reduce {ast.dump(node)}")


def _render(node, parent: int = 0, right: bool = False, under_mod: bool = False) -> str:
    """Parentheses only where precedence needs them, and always around the operand of `mod`."""
    if isinstance(node, ast.Constant):
        return str(int(node.value))
    if isinstance(node, ast.UnaryOp):
        return f"-{_render(node.operand, 3)}"
    prec = _PREC[type(node.op)]
    is_mod = isinstance(node.op, ast.Mod)
    text = (
        f"{_render(node.left, prec, under_mod=is_mod)} {_SYMBOL[type(node.op)]} "
        f"{_render(node.right, prec, right=True, under_mod=is_mod)}"
    )
    if under_mod or prec < parent or (right and prec == parent):
        return f"({text})"
    return text


SPLIT_SEED = 1234
REPORT_SIZE = 16
SELECT_SIZE = 16
MASTERED_AT = 0.9
TRAIN_EXTRA = 50


def split_inputs(seed: int = SPLIT_SEED) -> dict[str, list[int]]:
    """Exams come from 0..49. Training gets the other 18 of those plus 50..99.

    With 18 training inputs the named rules reached zero loss and stalled near 0.7
    on new inputs. Inputs past 50 also make the modulus do work.
    """
    values = list(range(50))
    random.Random(seed).shuffle(values)
    report = sorted(values[:REPORT_SIZE])
    select = sorted(values[REPORT_SIZE : REPORT_SIZE + SELECT_SIZE])
    train = sorted(values[REPORT_SIZE + SELECT_SIZE :] + list(range(50, 50 + TRAIN_EXTRA)))
    if set(train) & set(select) or set(train) & set(report) or set(select) & set(report):
        raise RuntimeError("exam inputs leaked into training")
    return {"train": train, "select": select, "report": report}


@dataclass(frozen=True)
class Skill:
    id: str
    name: str
    expr: str
    mode: str = "shown"

    def answer(self, n: int) -> int:
        return int(eval(self.expr, {"__builtins__": {}}, {"n": int(n)}))

    def rule(self) -> str:
        return self.expr.replace("%", "mod")

    def prompt(self, n: int) -> str:
        if self.mode == "named":
            return f"Use the rule you learned for {self.name}.\nn = {int(n)}\nEnd with `{self.name}({int(n)}) = <integer>`."
        return f"{self.name}(n) = {self.rule()}.\nn = {int(n)}\nFill in the rule. End with `= <integer>`."

    def completion(self, n: int) -> str:
        """The substituted rule, reduced one operation per step.

        Writing `263` straight after `(37 * 7 + 4) mod 50 =` was memorised for the
        twelve lesson inputs and missed on new ones. One operation per step is a
        procedure the base can already do. A named prompt writes the rule back
        from memory first.
        """
        trace = " = ".join(reduce_steps(self.expr.replace("n", str(int(n)))))
        if self.mode == "named":
            return f"{self.name}({int(n)}) = {trace}"
        return trace

    def pairs(self, values: list[int]) -> list[tuple[str, str]]:
        return [(self.prompt(n), self.completion(n)) for n in values]

    def answers(self, values: list[int]) -> list[int]:
        return [self.answer(n) for n in values]

    def prompts(self, values: list[int]) -> list[str]:
        return [self.prompt(n) for n in values]

    def shot_prompt(self, n: int, shots: list[int]) -> str:
        """The prompt with worked examples in front. This is the in-context baseline."""
        lines = [f"{self.completion(x)}" for x in shots if x != n]
        if self.mode == "named":
            head = f"Examples of {self.name}:\n" + "\n".join(lines)
            return f"{head}\n\nn = {int(n)}\nEnd with `{self.name}({int(n)}) = <integer>`."
        head = f"{self.name}(n) = {self.rule()}.\nWorked examples:\n" + "\n".join(lines)
        return f"{head}\n\nn = {int(n)}\nFill in the rule. End with `= <integer>`."

    def shot_messages(self, n: int, shots: list[int]) -> list[dict]:
        """Chat few-shot: each example is its own user turn and assistant turn.

        With eight examples inside one user message, the 1.5B kept writing the list
        (`zorpim(23) = ...`) instead of answering, so that baseline scored near zero.
        """
        messages = []
        for x in shots:
            if x == n:
                continue
            messages.append({"role": "user", "content": self.prompt(x)})
            messages.append({"role": "assistant", "content": self.completion(x)})
        messages.append({"role": "user", "content": self.prompt(n)})
        return messages

    def named(self) -> "Skill":
        return Skill(self.id, self.name, self.expr, "named")


# The +6 rule is the one the 1.5B already learned. It stays first so later rules are compared to it.
CATALOG = (
    Skill("add6", "fform", "(n + 6) % 50"),
    Skill("add13", "gvek", "(n + 13) % 50"),
    Skill("lin7", "zorpim", "(n * 7 + 4) % 50"),
    Skill("square", "nubqal", "(n * n) % 50"),
    Skill("fold40", "rixfom", "(40 - n) % 50"),
    Skill("lin3", "jadwex", "(n * 3 + 11) % 50"),
    Skill("add27", "lukbri", "(n + 27) % 50"),
    Skill("dbl9", "tavzor", "(n * 2 + 9) % 50"),
    Skill("tri", "pimnub", "(n * n + n) % 50"),
    Skill("lin9", "qalrix", "(n * 9 + 2) % 50"),
    Skill("mod17", "fomjad", "(n * 4) % 17"),
    Skill("lin11", "wexluk", "(n * 11 + 3) % 50"),
    Skill("sq7", "britav", "(n * n + 7) % 50"),
    Skill("back3", "vekzor", "(60 - 3 * n) % 50"),
)

# Evolution never trains or scores these. They test whether an evolved learning rule carries over.
HELDOUT_IDS = ("lin11", "sq7", "back3", "lin9")


def catalog(mode: str = "shown") -> list[Skill]:
    rows = list(CATALOG)
    return [skill.named() for skill in rows] if mode == "named" else rows


def by_id(skill_id: str, mode: str = "shown") -> Skill:
    for skill in catalog(mode):
        if skill.id == skill_id:
            return skill
    raise KeyError(skill_id)


def split_skills(skills: list[Skill]) -> tuple[list[Skill], list[Skill]]:
    train = [skill for skill in skills if skill.id not in HELDOUT_IDS]
    held = [skill for skill in skills if skill.id in HELDOUT_IDS]
    return train, held


def birth_test(evo, skills: list[Skill], adapter="policy", shots: int = 3, max_new: int = 256, innate_at: float = 0.5) -> list[dict]:
    """Birth scores on the selection set, with room for the base model's own long derivation.

    At 48 tokens the 1.5B was cut off mid-LaTeX on every rule, so a short budget
    measures the answer format, not the arithmetic. A shown rule is innate when
    the base solves it zero-shot or with `shots` worked examples. A named rule
    cannot be solved zero-shot; its few-shot score is the in-context baseline.
    """
    from evo.plastic.fastscore import graded_rate

    split = split_inputs()
    shot_x = split["train"][:shots]
    rows = []
    for skill in skills:
        # A named rule cannot be derived from its name, so a long zero-shot budget buys nothing.
        zero_new = min(int(max_new), 64) if skill.mode == "named" else int(max_new)
        zero = graded_rate(evo, skill.prompts(split["select"]), skill.answers(split["select"]), zero_new, adapter)
        few_prompts = [skill.shot_prompt(n, shot_x) for n in split["select"]]
        few = graded_rate(evo, few_prompts, skill.answers(split["select"]), max_new, adapter)
        innate = zero["rate"] >= innate_at
        best = zero["rate"]
        if skill.mode == "shown":
            innate = innate or few["rate"] >= innate_at
            best = max(best, few["rate"])
        rows.append(
            {
                "skill": skill.id,
                "mode": skill.mode,
                "budget": int(max_new),
                "zero_shot": zero["rate"],
                "few_shot": few["rate"],
                "zero_tokens": zero["tokens"],
                "innate": innate,
                "mastered": best >= MASTERED_AT,
                "zero_reply": zero["replies"][0] if zero["replies"] else "",
                "few_reply": few["replies"][0] if few["replies"] else "",
            }
        )
        print(f"[curriculum] {skill.id} zero={zero['rate']:.2f} few={few['rate']:.2f}", flush=True)
    return rows


def new_skills(skills: list[Skill], births: list[dict], rule: str = "new") -> list[Skill]:
    """`new` drops rules the base can already do. `unmastered` drops only rules it already gets right 90% of the time.

    With room to derive, the 1.5B solved every shown rule at least half the time.
    For shown rules the gain on offer is accuracy and length, so `unmastered` is the filter there.
    """
    if rule == "unmastered":
        dropped = {row["skill"] for row in births if _base_best(row) >= MASTERED_AT}
    else:
        dropped = {row["skill"] for row in births if row["innate"]}
    return [skill for skill in skills if skill.id not in dropped]


def _base_best(row: dict) -> float:
    if row.get("mode", "shown") == "shown":
        return max(float(row["zero_shot"]), float(row["few_shot"]))
    return float(row["zero_shot"])
