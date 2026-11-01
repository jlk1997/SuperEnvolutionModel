"""Practice, gate, and exam tasks. The three splits do not share arguments."""

from __future__ import annotations

from evo.selfplay.executor import outputs_match, run_code
from evo.world.toolbox import call_tool, chain_program, prelude


def choose_difficulty(agent_rate: float) -> str:
    """Day-0 knob. Aim the agent at a mid band before the scored days."""
    if agent_rate > 0.6:
        return "chain"
    if agent_rate < 0.3:
        return "single"
    return "mixed"


def _expect(tools: list[dict], gold: str, timeout: float, workspace=None) -> str:
    result = run_code(gold, timeout, prelude=prelude(tools), world=True, workspace=workspace)
    if not result.ok:
        raise RuntimeError(f"gold program failed: {result.error}")
    return result.value


def _call_task(split: str, day: int, index: int, tool: dict, arg_key: str, tools: list[dict], timeout: float) -> dict:
    arg = tool[arg_key]
    gold = f"print({tool['name']}({arg}))"
    return {
        "id": f"d{day}-{split}-call-{index}",
        "split": split,
        "day": day,
        "kind": "call",
        "prompt": f"Print the result of {tool['nick']} applied to {arg}.",
        "gold": gold,
        "expect": _expect(tools, gold, timeout),
        "tools": [tool["name"]],
        "arg": arg,
        "file": None,
    }


def _chain_task(split: str, day: int, index: int, first: dict, second: dict, arg: str, tools: list[dict], timeout: float) -> dict:
    gold = chain_program(first, second, arg)
    return {
        "id": f"d{day}-{split}-chain-{index}",
        "split": split,
        "day": day,
        "kind": "call",
        "prompt": (
            f"Apply {first['nick']} to {arg}, then apply {second['nick']} to that result. "
            "Print the final result."
        ),
        "gold": gold,
        "expect": _expect(tools, gold, timeout),
        "tools": [first["name"], second["name"]],
        "arg": arg,
        "file": None,
    }


def _same_kind(tools: list[dict], kind: str) -> list[dict]:
    return [tool for tool in tools if tool["kind"] == kind]


def make_task(
    split: str,
    day: int,
    index: int,
    tools: list[dict],
    focus: list[dict],
    difficulty: str,
    timeout: float,
    rng,
    arg_override: str | None = None,
) -> dict:
    """One task. `focus` is the tools this split is allowed to feature."""
    pool = focus or tools
    use_chain = difficulty == "chain" or (difficulty == "mixed" and index % 2 == 1)
    if use_chain and len(pool) >= 1:
        first = pool[index % len(pool)]
        partners = _same_kind(tools, first["kind"])
        partners = [tool for tool in partners if tool["name"] != first["name"]] or partners
        if partners:
            second = partners[(index + 1) % len(partners)]
            arg_key = {"practice": "practice_arg", "gate": "gate_arg", "exam": "exam_arg", "tune": "tune_arg"}[split]
            arg = arg_override if arg_override is not None else (
                first["chain_arg"] if split == "exam" and first.get("chain_arg") else first[arg_key]
            )
            if second["kind"] == "number" and first["kind"] == "number":
                return _chain_task(split, day, index, first, second, arg, tools, timeout)
            if second["kind"] == "text" and first["kind"] == "text":
                return _chain_task(split, day, index, first, second, arg, tools, timeout)
    tool = pool[index % len(pool)]
    arg_key = {"practice": "practice_arg", "gate": "gate_arg", "exam": "exam_arg", "tune": "tune_arg"}[split]
    if arg_override is not None:
        arg = arg_override
        gold = f"print({tool['name']}({arg}))"
        task = _call_task(split, day, index, tool, arg_key, tools, timeout)
        task["prompt"] = f"Print the result of {tool['nick']} applied to {arg}."
        task["gold"] = gold
        task["arg"] = arg
        task["expect"] = _expect(tools, gold, timeout)
        return task
    return _call_task(split, day, index, tool, arg_key, tools, timeout)


def day_bundle(day: int, tools: list[dict], new_tools: list[dict], difficulty: str, cfg: dict, rng) -> dict:
    timeout = float(cfg.get("exec_timeout", 2.0))
    counts = {
        "practice": int(cfg.get("practice_tasks", 2)),
        "gate": int(cfg.get("gate_tasks", 1)),
        "exam": int(cfg.get("exam_tasks", 2)),
    }
    bundle = {}
    focus = list(new_tools) or list(tools)
    # One exam item reuses the oldest tool so later days measure retention.
    for split, count in counts.items():
        rows = []
        for index in range(count):
            chosen = focus
            task_difficulty = difficulty
            retention = False
            override = None
            if split == "exam" and cfg.get("exam_mix"):
                task, retention = _mix_exam(day, index, tools, focus, timeout, rng)
                task["retention"] = retention
                rows.append(task)
                continue
            if cfg.get("chain_exam") and split in ("exam", "practice") and index == 0:
                task_difficulty = "chain"
            if split == "exam" and index == count - 1 and day > 0:
                oldest = [tool for tool in tools if tool["day"] == 0] or tools
                chosen = oldest
                task_difficulty = "single"
                retention = True
            task = make_task(split, day, index, tools, chosen, task_difficulty, timeout, rng, override)
            task["retention"] = retention
            rows.append(task)
        bundle[split] = rows
    pool = int(cfg.get("exam_pool") or 0)
    if pool:
        bundle["exam"] = expand_exam_pool(bundle["exam"], tools, day, pool, timeout, rng)
    return bundle


def expand_exam_pool(rows: list[dict], tools: list[dict], day: int, pool: int, timeout: float, rng) -> list[dict]:
    """Score more held-arg exams than the night is allowed to train on.

    `held_args` are already banned from drills. Extra items only widen the measurement.
    """
    wider = list(rows)
    if pool <= len(wider) or not tools:
        return wider
    index = len(wider)
    guard = 0
    while len(wider) < pool and guard < pool * 4:
        tool = tools[index % len(tools)]
        held = [str(arg) for arg in (tool.get("held_args") or [])]
        if not held:
            break
        arg = held[index % len(held)]
        task = make_task("exam", day, index, tools, [tool], "single", timeout, rng, arg)
        task["retention"] = False
        task["pool"] = True
        wider.append(task)
        index += 1
        guard += 1
    return wider


def _mix_exam(day: int, index: int, tools: list[dict], new_tools: list[dict], timeout: float, rng) -> tuple[dict, bool]:
    """Six-item paper: new chains, new singles, an older tool, and one day-0 single.

    Extra items use held_args. Those values stay out of the night's drills.
    """
    fresh = list(new_tools) or list(tools)
    older = [tool for tool in tools if tool["name"] not in {item["name"] for item in fresh}]
    day0 = [tool for tool in tools if tool.get("day") == 0] or list(tools)
    slot = index % 6
    if slot == 0:
        return make_task("exam", day, index, tools, fresh, "chain", timeout, rng), False
    if slot == 1:
        return make_task("exam", day, index, tools, fresh, "single", timeout, rng), False
    if slot == 2:
        arg = (fresh[0].get("held_args") or [fresh[0]["exam_arg"]])[0]
        return make_task("exam", day, index, tools, fresh, "chain", timeout, rng, arg), False
    if slot == 3:
        chosen = older or fresh
        if older:
            return make_task("exam", day, index, tools, chosen, "single", timeout, rng), False
        arg = (chosen[0].get("held_args") or [chosen[0]["exam_arg"]])[1 % len(chosen[0].get("held_args") or [1])]
        return make_task("exam", day, index, tools, chosen, "single", timeout, rng, arg), False
    if slot == 4:
        chosen = older or fresh
        if older:
            return make_task("exam", day, index, tools, chosen, "chain", timeout, rng), False
        arg = (chosen[0].get("held_args") or [chosen[0]["exam_arg"]])[-1]
        return make_task("exam", day, index, tools, chosen, "chain", timeout, rng, arg), False
    held = (day0[index % len(day0)].get("held_args") or [None])[-1]
    task = make_task("exam", day, index, tools, day0, "single", timeout, rng, held)
    return task, day > 0


def preference_task(day: int) -> dict:
    return {
        "id": f"d{day}-exam-pref",
        "split": "exam",
        "day": day,
        "kind": "call",
        "prompt": "Print the word ready in the form the user prefers.",
        "gold": "print('ACK ready')",
        "expect": "ACK ready",
        "tools": [],
        "file": None,
    }


def project_tasks(day: int, tool: dict, tools: list[dict], timeout: float) -> dict | None:
    """A file that is written on day 0 and read on later days."""
    if tool is None:
        return None
    if day == 0:
        text = str(call_tool(tool, tool["exam_arg"]))
        gold = (
            "open('workspace/keep.txt', 'w', encoding='utf-8').write("
            f"str({tool['name']}({tool['exam_arg']})))\n"
            "print('saved')"
        )
        return {
            "id": f"d{day}-exam-file",
            "split": "exam",
            "day": day,
            "kind": "write",
            "prompt": (
                f"Write the result of {tool['nick']} applied to {tool['exam_arg']} into workspace/keep.txt "
                "and print saved."
            ),
            "gold": gold,
            "expect": "saved",
            "file_text": text,
            "file": "keep.txt",
            "tools": [tool["name"]],
        }
    return {
        "id": f"d{day}-exam-file",
        "split": "exam",
        "day": day,
        "kind": "read",
        "prompt": "Read workspace/keep.txt and print its contents.",
        "gold": "print(open('workspace/keep.txt', encoding='utf-8').read())",
        "expect": "",
        "file": "keep.txt",
        "tools": [],
    }


PREFERENCE_DOC = {
    "id": "preference",
    "text": "User preference: every printed line starts with ACK. Example: ACK ready.",
    "tool": "preference",
}
