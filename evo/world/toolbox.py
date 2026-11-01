"""Fictional tools the base model cannot have memorized.

The source installed in the sandbox has no docstring. Lessons are a separate string.
"""

from __future__ import annotations

import ast
import random


SYLLABLES = [
    "zor", "nub", "vek", "pim", "qal", "rix", "fom", "jad",
    "wex", "luk", "bri", "tav", "mux", "kel", "dox", "yim",
]
NICKNAMES = [
    "red-stamp", "blue-fold", "gold-notch", "mint-latch", "iron-clip", "jade-pin",
    "opal-wrap", "ruby-mark", "sand-cut", "lime-tap", "pearl-shift", "onyx-bind",
    "coral-knot", "amber-skip", "ivory-trim", "copper-flip",
]


def _fresh_name(rng: random.Random, used: set[str]) -> str:
    for _ in range(1000):
        name = rng.choice(SYLLABLES) + rng.choice(SYLLABLES)
        if name not in used and not name.isidentifier():
            continue
        if name not in used:
            used.add(name)
            return name
    raise RuntimeError("ran out of tool names")


def _nick(rng: random.Random, used: set[str]) -> str:
    for nick in NICKNAMES:
        if nick not in used:
            used.add(nick)
            return nick
    nick = f"tool-{rng.randrange(10000)}"
    used.add(nick)
    return nick


def _make(rng: random.Random, name: str, nick: str, day: int, kind: str | None = None) -> dict:
    if kind == "number":
        kind_roll = 2
    elif kind == "text":
        kind_roll = rng.randrange(2)
    else:
        kind_roll = rng.randrange(3)
    if kind_roll == 0:
        mark = rng.choice(["Q", "X", "Z"])
        source = f"def {name}(text):\n    return {mark!r} + str(text)[::-1]\n"
        rule = f"returns {mark!r} followed by the characters of text in reverse"
        return {
            "name": name,
            "nick": nick,
            "kind": "text",
            "day": day,
            "source": source,
            "doc": f"The tool {nick} is the function {name}. {name}(text) {rule}. Example: {name}('ab').",
            "quiz_args": ["'ab'", "'cd'"],
            "drill_args": ["'wx'", "'yz'"],
            "practice_arg": "'gh'",
            "gate_arg": "'ij'",
            "exam_arg": "'ef'",
            "tune_arg": "'kl'",
            "chain_arg": "'qr'",
            "bind_args": ["'pl'", "'ok'", "'vw'", "'hi'"],
            "held_args": ["'qa'", "'ws'", "'ed'", "'rf'"],
        }
    if kind_roll == 1:
        keep = rng.choice([3, 4, 5])
        source = f"def {name}(text):\n    return (str(text) * 2)[:{keep}]\n"
        rule = f"repeats text once and keeps the first {keep} characters"
        return {
            "name": name,
            "nick": nick,
            "kind": "text",
            "day": day,
            "source": source,
            "doc": f"The tool {nick} is the function {name}. {name}(text) {rule}. Example: {name}('xy').",
            "quiz_args": ["'xy'", "'pq'"],
            "drill_args": ["'aa'", "'zz'"],
            "practice_arg": "'mn'",
            "gate_arg": "'uv'",
            "exam_arg": "'st'",
            "tune_arg": "'bc'",
            "chain_arg": "'jk'",
            "bind_args": ["'rb'", "'nc'", "'wd'", "'qs'"],
            "held_args": ["'lm'", "'no'", "'pq'", "'tu'"],
        }
    step = rng.choice([2, 3, 4, 7])
    source = f"def {name}(number):\n    return int(number) + {step}\n"
    return {
        "name": name,
        "nick": nick,
        "kind": "number",
        "day": day,
        "step": step,
        "source": source,
        "doc": f"The tool {nick} is the function {name}. {name}(number) returns that number plus {step}. Example: {name}(5).",
        "quiz_args": ["5", "8"],
        "drill_args": ["21", "34"],
        "practice_arg": "2",
        "gate_arg": "4",
        "exam_arg": "11",
        "tune_arg": "15",
        "chain_arg": "19",
        "bind_args": ["3", "6", "9", "13"],
        "held_args": ["17", "23", "29", "31"],
    }


def build_tools(
    seed: int,
    count: int,
    day: int,
    used: set[str] | None = None,
    pair: bool = False,
    kind: str | None = None,
) -> list[dict]:
    rng = random.Random(seed + day * 10007)
    taken = used if used is not None else set()
    tools = []
    for _ in range(count):
        this_kind = kind or (tools[0]["kind"] if pair and tools else None)
        tools.append(_make(rng, _fresh_name(rng, taken), _nick(rng, taken), day, this_kind))
    return tools


def prelude(tools: list[dict]) -> str:
    return "\n".join(tool["source"].rstrip() for tool in tools) + ("\n" if tools else "")


def call_tool(tool: dict, arg_literal: str):
    namespace: dict = {}
    exec(tool["source"], namespace)
    value = ast.literal_eval(arg_literal)
    return namespace[tool["name"]](value)


def chain_program(first: dict, second: dict, arg_literal: str) -> str:
    """Nested call checked by the sandbox. A two-statement form failed the chain gate on 0.5B."""
    return f"print({second['name']}({first['name']}({arg_literal})))"


def chain_result(first: dict, second: dict, arg_literal: str):
    """Run one tool and feed its return value into the next. Raises if the types do not fit."""
    namespace: dict = {}
    exec(first["source"] + "\n" + second["source"], namespace)
    value = ast.literal_eval(arg_literal)
    return namespace[second["name"]](namespace[first["name"]](value))


def tool_docs(tools: list[dict]) -> list[dict]:
    return [{"id": tool["name"], "text": tool["doc"], "tool": tool["name"]} for tool in tools]
