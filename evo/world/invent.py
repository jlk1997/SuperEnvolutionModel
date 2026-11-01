"""Concepts the model names for itself. A concept is a verified shortcut, not an exam sentence."""

from __future__ import annotations

from evo.selfplay.tasks import learnability
from evo.world.sleep import _code_pair, _program_names
from evo.world.toolbox import NICKNAMES, chain_program, chain_result


def half_solved(rate: float, floor: float = 0.34) -> bool:
    return learnability(rate) >= floor


def pose_kept(rate: float, floor: float = 0.34) -> bool:
    """A self-proposed task is kept only inside the learnability band."""
    return learnability(rate) >= floor


def pose_pairs(evo, cfg: dict, adapter: str = "policy", limit: int = 1) -> list[tuple[str, str]]:
    """One executor-checked solve(x) task at the edge of what the model can do.

    The proposal is not an exam item. Always-solved and never-solved tasks are dropped.
    """
    from evo.generate import generate
    from evo.selfplay.tasks import (
        check_solver,
        gold_answer,
        is_example_copy,
        materialize,
        parse_proposal,
        proposer_prompt,
        solver_prompt,
    )

    timeout = float(cfg.get("exec_timeout", 2.0))
    samples = max(2, int(cfg.get("solver_samples", 3)))
    floor = float(cfg.get("min_learnability", 0.34))
    kept: list[tuple[str, str]] = []
    for _ in range(max(1, limit)):
        raw = generate(
            evo,
            proposer_prompt("deduction"),
            int(cfg.get("max_new_code", 80)),
            float(cfg.get("temperature", 0.7)),
            adapter,
        )
        parsed = parse_proposal(raw, "deduction")
        if parsed is None or is_example_copy(parsed.get("program", "")):
            continue
        task = materialize(parsed, timeout)
        if task is None:
            continue
        prompt = solver_prompt(task)
        hits = 0
        for _sample in range(samples):
            answer = generate(evo, prompt, int(cfg.get("answer_tokens", 16)), 0.0, adapter)
            if check_solver(task, answer, timeout):
                hits += 1
        rate = hits / samples
        if not pose_kept(rate, floor):
            continue
        kept.append((prompt, gold_answer(task)))
    return kept


def propose_concepts(traces: list[dict], tools: list[dict], used: set[str], limit: int = 1) -> list[dict]:
    """Name a pair of tools that keep showing up together, when the shorter program still runs."""
    counts: dict[tuple[str, str], int] = {}
    for trace in traces:
        if not trace.get("ok"):
            continue
        code = ((trace.get("trace") or [{}])[-1].get("code") or "")
        names = [name for name in _program_names(code) if name != "print"]
        for outer, inner in zip(names, names[1:]):
            if outer == inner:
                continue
            counts[(inner, outer)] = counts.get((inner, outer), 0) + 1
    by_name = {tool["name"]: tool for tool in tools}
    ranked = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    concepts = []
    for (first_name, second_name), _count in ranked:
        first = by_name.get(first_name)
        second = by_name.get(second_name)
        if first is None or second is None or first["kind"] != second["kind"]:
            continue
        concept = _concept(first, second, used)
        if concept is None:
            continue
        concepts.append(concept)
        if len(concepts) >= limit:
            break
    return concepts


def concept_pairs(concept: dict) -> list[tuple[str, str]]:
    """Bind-arg drills. Exam and held arguments are not in here."""
    pairs = []
    for arg in concept.get("bind_args") or []:
        pairs.append(
            _code_pair(
                f"Print the result of {concept['nick']} applied to {arg}.",
                f"print({concept['name']}({arg}))",
            )
        )
    return pairs


def depth_tasks(concept: dict, tools: list[dict], day: int, timeout: float) -> list[dict]:
    """Depth 3 and 4 on held-out arguments. These prompts are for the next exam only."""
    from evo.world.tasks import _expect

    held = (concept.get("held_args") or [None])[0]
    if held is None:
        return []
    rows = []
    gold3 = f"print({concept['second']}({concept['name']}({held})))"
    rows.append(_depth_row(concept, day, 3, held, gold3, tools, timeout, _expect))
    gold4 = f"print({concept['name']}({concept['name']}({held})))"
    rows.append(_depth_row(concept, day, 4, held, gold4, tools, timeout, _expect))
    return [row for row in rows if row is not None]


def _depth_row(concept, day, depth, arg, gold, tools, timeout, expect) -> dict | None:
    try:
        value = expect(tools + [concept], gold, timeout)
    except (RuntimeError, TypeError, ValueError):
        return None
    return {
        "id": f"d{day}-exam-depth-{depth}-{concept['name']}",
        "split": "exam",
        "day": day,
        "kind": "call",
        "prompt": (
            f"Apply {concept['nick']} to {arg}"
            + (f", then apply {concept['outer_nick']} to that result." if depth == 3 else " twice.")
            + " Print the final result."
        ),
        "gold": gold,
        "expect": value,
        "tools": [concept["name"], concept["second"]] if depth == 3 else [concept["name"]],
        "arg": arg,
        "file": None,
        "retention": False,
        "depth": depth,
    }


def _concept(first: dict, second: dict, used: set[str]) -> dict | None:
    nick = next((item for item in NICKNAMES if item not in used), None)
    if nick is None:
        return None
    name = (first["name"][:3] + second["name"][:3])
    if name in used or not name.isidentifier():
        return None
    bind = []
    for arg in first.get("bind_args") or []:
        try:
            chain_result(first, second, arg)
        except (TypeError, ValueError, KeyError):
            continue
        bind.append(arg)
    if len(bind) < 2:
        return None
    direct = chain_program(first, second, bind[0])
    short = f"print({name}({bind[0]}))"
    if len(short) >= len(direct):
        return None
    used.add(nick)
    used.add(name)
    source = f"def {name}(value):\n    return {second['name']}({first['name']}(value))\n"
    return {
        "name": name,
        "nick": nick,
        "kind": first["kind"],
        "day": first.get("day", 0),
        "source": source,
        "doc": (
            f"The tool {nick} is the function {name}. "
            f"{name}(value) means {second['name']}({first['name']}(value))."
        ),
        "quiz_args": list(first.get("quiz_args") or []),
        "drill_args": list(first.get("drill_args") or []),
        "practice_arg": first.get("practice_arg"),
        "gate_arg": first.get("gate_arg"),
        "exam_arg": first.get("exam_arg"),
        "tune_arg": first.get("tune_arg"),
        "chain_arg": first.get("chain_arg"),
        "bind_args": bind,
        "held_args": list(first.get("held_args") or []),
        "first": first["name"],
        "second": second["name"],
        "outer_nick": second["nick"],
        "concept": True,
    }
