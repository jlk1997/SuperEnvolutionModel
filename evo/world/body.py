"""Thin body: write code, run it, see the error, try again. No plan and no retrieval."""

from __future__ import annotations

from pathlib import Path

from evo.generate import generate
from evo.selfplay.executor import outputs_match, run_code
from evo.world.toolbox import prelude


def extract_code(text: str) -> str:
    if "```" in text:
        chunk = text.split("```", 2)[1]
        if chunk.lstrip().startswith("python"):
            chunk = chunk.lstrip()[len("python") :]
        return chunk.strip()
    lines = []
    started = False
    for line in text.splitlines():
        stripped = line.strip()
        if not started and stripped.startswith(("print", "open", "def ", "for ", "while ", "import ", "with ", "result", "value")):
            started = True
        if started:
            lines.append(line)
    return "\n".join(lines).strip() or text.strip()


def task_prompt(task: dict, error: str, notes: str) -> str:
    parts = [
        "Write Python that does the task. Reply with code only.",
        task["prompt"],
    ]
    if notes.strip():
        parts.append(notes.strip())
    if error.strip():
        parts.append("The previous program failed:\n" + error.strip()[:500])
        parts.append("Write a corrected program.")
    return "\n\n".join(parts)


def grade_task(code: str, task: dict, tools: list[dict], workspace: Path | None, timeout: float) -> tuple[bool, object]:
    result = run_code(
        code,
        timeout,
        prelude=prelude(tools) if tools else "",
        world=True,
        workspace=workspace,
    )
    if task.get("kind") == "write":
        path = (workspace / task["file"]) if workspace is not None else None
        wrote = path is not None and path.exists() and path.read_text(encoding="utf-8") == task.get("file_text")
        ok = bool(result.ok and wrote and outputs_match(result.value, task["expect"]))
        return ok, result
    if task.get("kind") == "read":
        if workspace is None:
            return False, result
        path = workspace / task["file"]
        expected = path.read_text(encoding="utf-8").strip() if path.exists() else ""
        ok = bool(result.ok and expected and outputs_match(result.value, expected))
        return ok, result
    ok = bool(result.ok and outputs_match(result.value, task["expect"]))
    return ok, result


def attempt(
    evo,
    task: dict,
    tools: list[dict],
    cfg: dict,
    adapter: str | None,
    notes: str = "",
    workspace: Path | None = None,
    max_turns: int | None = None,
    sidecar=None,
    show_error: bool = True,
    initial_error: str = "",
    block_ids: list[int] | None = None,
    admit=None,
) -> dict:
    turns = int(max_turns if max_turns is not None else cfg.get("max_turns", 2))
    timeout = float(cfg.get("exec_timeout", 2.0))
    error = initial_error
    trace = []
    prompt_tokens = 0
    passed = False
    for turn in range(turns):
        extra = notes(error) if callable(notes) else notes
        prompt = task_prompt(task, error if show_error else "", extra)
        prompt_tokens += len(evo.tok(prompt, add_special_tokens=False)["input_ids"])
        if sidecar is not None:
            sidecar.on()
        try:
            reply = generate(evo, prompt, int(cfg.get("max_new_code", 160)), 0.0, adapter, block_ids=block_ids)
        finally:
            if sidecar is not None:
                sidecar.off()
        code = extract_code(reply)
        refused = list(admit(code) or []) if admit is not None else []
        if refused:
            trace.append(
                {
                    "turn": turn,
                    "code": code,
                    "ok": False,
                    "error": "refused:" + ",".join(refused),
                    "prompt": prompt,
                    "value": "",
                }
            )
            error = "refused:" + ",".join(refused)
            continue
        ok, result = grade_task(code or "raise SystemExit('empty')", task, tools, workspace, timeout)
        err = ""
        if not ok:
            err = (result.error or result.stderr or "wrong output")[:500]
            if result.stdout.strip():
                err = (err + "\nstdout: " + result.stdout.strip()[:200]).strip()
        trace.append(
            {
                "turn": turn,
                "code": code,
                "ok": ok,
                "error": err,
                "prompt": prompt,
                "value": result.value,
            }
        )
        passed = ok
        if ok:
            break
        error = err or "wrong output"
    return {
        "id": task["id"],
        "ok": passed,
        "turns": len(trace),
        "prompt_tokens": prompt_tokens,
        "trace": trace,
        "task": task,
    }
