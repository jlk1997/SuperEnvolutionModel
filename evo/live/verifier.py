"""The executor is the only reward until a second checker has earned trust.

A proposed test is ignored until it has matched the executor often enough.
That is the difference between a new rung and a model grading itself.
"""

from __future__ import annotations

import ast
import re


class CheckerTrust:
    def __init__(self, minimum: float = 0.8, needed: int = 4):
        self.minimum = float(minimum)
        self.needed = int(needed)
        self.agree = 0
        self.checks = 0

    def observe(self, executor_ok: bool, proposed_ok: bool) -> None:
        self.checks += 1
        self.agree += int(bool(executor_ok) == bool(proposed_ok))

    def trusted(self) -> bool:
        if self.checks < self.needed:
            return False
        return (self.agree / self.checks) >= self.minimum

    def reward(self, executor_ok: bool, proposed_ok: bool | None = None) -> float:
        if proposed_ok is None or not self.trusted():
            return 1.0 if executor_ok else 0.0
        return 1.0 if proposed_ok else 0.0


def literal_claim(code: str) -> str | None:
    """The value a program asserts, when it is written as a literal print or assert.

    A call such as print(tool(x)) makes no claim. There is nothing to calibrate.
    """
    text = code or ""
    matched = re.search(r"print\(\s*([0-9]+|'[^']*'|\"[^\"]*\")\s*\)", text)
    if matched:
        return _unwrap(matched.group(1))
    for node in _asserts(text):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, str)):
            return str(node.value)
    return None


def _unwrap(token: str) -> str:
    if len(token) >= 2 and token[0] == token[-1] and token[0] in ("'", '"'):
        return token[1:-1]
    return token


def _asserts(text: str):
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return []
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assert):
            test = node.test
            if isinstance(test, ast.Compare) and test.comparators:
                found.append(test.comparators[-1])
    return found
