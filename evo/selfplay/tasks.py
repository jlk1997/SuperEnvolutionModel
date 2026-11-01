"""Task formats for deduction, abduction, and induction."""

from __future__ import annotations

import ast
import re

from evo.selfplay.executor import execute_solve, outputs_match


TASK_TYPES = ("deduction", "abduction", "induction")


def mutate_program(program: str, direction: str, depth: bool = False) -> list[str]:
    """Executor-side edits. `harder` wraps the return; `easier` peels one operation, then a short ladder.

    With depth, harder variants continue to modulo, a square, and digit reversal.
    Those are tried only after the shallow wraps, which a 0.5B model was still solving.
    """
    variants: list[str] = []
    if direction == "harder":
        for op, constant in ((ast.Add(), 2), (ast.Add(), 3), (ast.Mult(), 2), (ast.Mult(), 3)):
            wrapped = _wrap_returns(program, op, constant)
            if wrapped and not is_example_copy(wrapped):
                variants.append(wrapped)
        if depth:
            variants.extend(_deep_rewrites(program))
        return _unique(variants)
    peeled = _unwrap_return(program)
    if peeled and not is_example_copy(peeled):
        variants.append(peeled)
    for body in (
        "def solve(x):\n    return x - 1",
        "def solve(x):\n    return x * 2",
        "def solve(x):\n    return x + x",
    ):
        if not is_example_copy(body):
            variants.append(body)
    return _unique(variants)


def render_proposal(task: dict) -> str:
    program = str(task["program"]).strip()
    if task["type"] == "induction":
        lines = "\n".join(str(item) for item in task["inputs"])
        return f"PROGRAM:\n{program}\nINPUTS:\n{lines}\n"
    return f"PROGRAM:\n{program}\nINPUT:\n{task['input']}\n"


def _unique(programs: list[str]) -> list[str]:
    seen = set()
    ordered = []
    for program in programs:
        key = "".join(program.split())
        if key in seen:
            continue
        seen.add(key)
        ordered.append(program)
    return ordered


def _wrap_returns(program: str, op: ast.operator, constant: int) -> str | None:
    try:
        tree = ast.parse(program)
    except SyntaxError:
        return None
    found = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Return) and node.value is not None:
            node.value = ast.BinOp(left=node.value, op=op, right=ast.Constant(constant))
            found = True
    if not found:
        return None
    ast.fix_missing_locations(tree)
    return ast.unparse(tree)


def _deep_rewrites(program: str) -> list[str]:
    rewritten = [
        _replace_return(program, lambda expr: ast.BinOp(left=expr, op=ast.Mod(), right=ast.Constant(7))),
        _replace_return(program, _square_plus_one),
        _replace_return(program, _reverse_digits),
    ]
    return [item for item in rewritten if item and not is_example_copy(item)]


def _square_plus_one(expr: ast.AST) -> ast.AST:
    copy = ast.parse(ast.unparse(expr), mode="eval").body
    return ast.BinOp(
        left=ast.BinOp(left=expr, op=ast.Mult(), right=copy),
        op=ast.Add(),
        right=ast.Constant(1),
    )


def _reverse_digits(expr: ast.AST) -> ast.AST:
    text = ast.Call(func=ast.Name(id="str", ctx=ast.Load()), args=[expr], keywords=[])
    flipped = ast.Subscript(
        value=text,
        slice=ast.Slice(step=ast.UnaryOp(op=ast.USub(), operand=ast.Constant(1))),
        ctx=ast.Load(),
    )
    return ast.Call(func=ast.Name(id="int", ctx=ast.Load()), args=[flipped], keywords=[])


def _replace_return(program: str, builder) -> str | None:
    try:
        tree = ast.parse(program)
    except SyntaxError:
        return None
    for node in ast.walk(tree):
        if isinstance(node, ast.Return) and node.value is not None:
            expr = ast.parse(ast.unparse(node.value), mode="eval").body
            node.value = builder(expr)
            ast.fix_missing_locations(tree)
            try:
                return ast.unparse(tree)
            except ValueError:
                return None
    return None


def worked_example(task: dict, timeout: float) -> str | None:
    """One executor trace on a different input. Induction already shows its examples."""
    if task.get("type") == "induction":
        return None
    gold_in = str(task.get("input", "")).strip()
    target = str(task.get("output", "")).strip()
    for literal in ("0", "1", "2", "5"):
        if literal == gold_in:
            continue
        result = execute_solve(task["program"], literal, timeout)
        if not result.ok or outputs_match(result.value, target):
            continue
        return f"Example: solve({literal}) = {result.value}\n"
    return None


def _unwrap_return(program: str) -> str | None:
    try:
        tree = ast.parse(program)
    except SyntaxError:
        return None
    for node in ast.walk(tree):
        if isinstance(node, ast.Return) and isinstance(node.value, ast.BinOp):
            node.value = node.value.left
            ast.fix_missing_locations(tree)
            return ast.unparse(tree)
    return None


def is_example_copy(program: str) -> bool:
    """The prompt's demonstration is `return x + 1`. Copying it is not a new task."""
    compact = "".join(program.split())
    return compact == "defsolve(x):returnx+1"


def gold_answer(task: dict) -> str:
    """The executor's answer, used as a hindsight target when the solver misses."""
    if task["type"] == "deduction":
        return str(task["output"])
    if task["type"] == "abduction":
        return str(task["input"])
    return str(task["program"]).strip()


def learnability(success_rate: float) -> float:
    """Peaks at 0.5. Always-solved and never-solved tasks teach nothing."""
    rate = min(1.0, max(0.0, success_rate))
    return 1.0 - abs(2.0 * rate - 1.0)


def extract_function(text: str) -> str | None:
    start = text.find("def solve")
    if start < 0:
        return None
    body = text[start:]
    stop = re.search(r"\n(?:INPUTS?|OUTPUT):", body)
    if stop:
        body = body[: stop.start()]
    return body.strip()


def _section(text: str, name: str) -> str | None:
    pattern = rf"{name}:\s*(.*?)(?=\n(?:PROGRAM|INPUTS|INPUT|OUTPUT):|\Z)"
    match = re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL)
    if not match:
        return None
    return match.group(1).strip()


def parse_proposal(text: str, task_type: str) -> dict | None:
    program = extract_function(text) or _section(text, "PROGRAM")
    if program and "def solve" not in program:
        program = None
    if not program:
        return None
    if task_type == "induction":
        raw = _section(text, "INPUTS")
        if not raw:
            return None
        literals = []
        for line in raw.splitlines():
            line = line.strip().lstrip("-").strip()
            if not line:
                continue
            try:
                ast.literal_eval(line)
            except (SyntaxError, ValueError):
                continue
            literals.append(line)
        if len(literals) < 2:
            return None
        return {"type": task_type, "program": program, "inputs": literals}
    raw_input = _section(text, "INPUT")
    if raw_input is None:
        return None
    first = raw_input.splitlines()[0].strip()
    try:
        ast.literal_eval(first)
    except (SyntaxError, ValueError):
        return None
    return {"type": task_type, "program": program, "input": first}


def materialize(task: dict, timeout: float) -> dict | None:
    """Fill gold outputs by execution. Returns None when the program is invalid."""
    if task["type"] == "induction":
        pairs = []
        for literal in task["inputs"]:
            result = execute_solve(task["program"], literal, timeout)
            if not result.ok:
                return None
            pairs.append({"input": literal, "output": result.value})
        if len(pairs) < 2:
            return None
        return {**task, "pairs": pairs, "heldout": pairs[-1], "shown": pairs[:-1]}
    result = execute_solve(task["program"], task["input"], timeout)
    if not result.ok:
        return None
    return {**task, "output": result.value}


def check_solver(task: dict, answer: str, timeout: float) -> bool:
    answer = answer.strip()
    if task["type"] == "deduction":
        line = answer.splitlines()[0].strip() if answer else ""
        return outputs_match(line, task["output"])
    if task["type"] == "abduction":
        line = answer.splitlines()[0].strip() if answer else ""
        result = execute_solve(task["program"], line, timeout)
        return result.ok and outputs_match(result.value, task["output"])
    program = extract_function(answer)
    if not program:
        return False
    heldout = task["heldout"]
    result = execute_solve(program, heldout["input"], timeout)
    return result.ok and outputs_match(result.value, heldout["output"])


def proposer_prompt(task_type: str) -> str:
    example = (
        "PROGRAM:\n"
        "def solve(x):\n"
        "    return x + 1\n"
        "INPUT:\n"
        "2\n"
    )
    if task_type == "deduction":
        return (
            "Invent a NEW tiny pure-Python function solve(x) and one input. "
            "No imports, no files, no network. Use only arithmetic, lists, or strings.\n"
            "Reply in exactly this format:\n"
            f"{example}"
        )
    if task_type == "abduction":
        return (
            "Invent a NEW tiny pure-Python function solve(x) and one input. "
            "No imports. The function should be deterministic.\n"
            "Reply in exactly this format:\n"
            f"{example}"
        )
    return (
        "Invent a NEW tiny pure-Python function solve(x) and three inputs. "
        "No imports.\n"
        "Reply in exactly this format:\n"
        "PROGRAM:\n"
        "def solve(x):\n"
        "    return x + 1\n"
        "INPUTS:\n"
        "1\n"
        "2\n"
        "3\n"
    )


def solver_prompt(task: dict) -> str:
    prefix = task.get("prompt_prefix") or ""
    if task["type"] == "deduction":
        return prefix + (
            f"PROGRAM:\n{task['program']}\n"
            f"INPUT:\n{task['input']}\n"
            "What does solve(INPUT) return? Reply with only the Python value."
        )
    if task["type"] == "abduction":
        return prefix + (
            f"PROGRAM:\n{task['program']}\n"
            f"OUTPUT:\n{task['output']}\n"
            "Give one Python literal INPUT such that solve(INPUT) equals OUTPUT. "
            "Reply with only the literal."
        )
    shown = "\n".join(f"solve({pair['input']}) = {pair['output']}" for pair in task["shown"])
    return prefix + (
        "Write the function solve(x) that fits these examples. No imports.\n"
        f"{shown}\n"
        "Reply in this format:\n"
        "PROGRAM:\n"
        "def solve(x):\n"
        "    ..."
    )
