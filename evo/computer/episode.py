"""Multi-turn episode. Each observation comes back as a tool response."""

from __future__ import annotations

from pathlib import Path

from evo.computer.actions import Call, format_response, parse_calls
from evo.computer.license import License
from evo.computer.sandbox import append_audit, execute


def run_episode(
    task: dict,
    reply,
    workspace: Path,
    license: License,
    audit_path: Path | None = None,
    apply: bool | None = None,
    on_event=None,
) -> dict:
    """`reply(messages) -> str`. `apply` False is shadow mode: proposals are logged, files stay put.

    `on_event(kind, payload)` fires for each model turn and each tool row, before the episode returns.
    """
    workspace.mkdir(parents=True, exist_ok=True)
    setup = task.get("setup")
    if setup is not None:
        setup(workspace)
    do_apply = license.mode != "shadow" if apply is None else apply
    try:
        return _loop(task, reply, workspace, license, audit_path, do_apply, on_event)
    finally:
        close = task.get("close")
        if close is not None:
            close()


def _emit(on_event, kind: str, payload: dict) -> None:
    if on_event is not None:
        on_event(kind, payload)


def _loop(task, reply, workspace, license, audit_path, do_apply, on_event) -> dict:
    messages = [{"role": "user", "content": task["prompt"]}]
    trace = []
    finished = False
    for step in range(license.max_steps):
        text = reply(messages) or ""
        calls = parse_calls(text)
        _emit(on_event, "model_turn", {"step": step, "text": text[:4000], "parsed": bool(calls)})
        if not calls:
            observation = "no tool call. Reply with a <tool_call> block."
            messages.append({"role": "assistant", "content": text})
            messages.append({"role": "user", "content": format_response(observation)})
            row = {"step": step, "ok": False, "error": observation, "name": "", "arguments": {}, "applied": False, "observation": observation[:500], "refused": ["no-tool-call"]}
            trace.append(row)
            _emit(on_event, "tool", row)
            continue
        messages.append({"role": "assistant", "content": text})
        observations = []
        for call in calls:
            reasons = license.decide(call, task.get("family"))
            if reasons:
                observation = "refused:" + ",".join(reasons)
                applied = False
            else:
                observation = execute(call, workspace, license, apply=do_apply)
                applied = do_apply
            row = {
                "step": step,
                "name": call.name,
                "arguments": dict(call.arguments),
                "applied": applied,
                "observation": observation[:500],
                "refused": reasons,
            }
            trace.append(row)
            _emit(on_event, "tool", row)
            if audit_path is not None:
                append_audit(audit_path, {"task": task.get("id"), "family": task.get("family"), **row})
            observations.append(observation)
            if call.name == "finish" and not reasons:
                finished = True
        messages.append({"role": "user", "content": format_response("\n".join(observations))})
        if finished:
            break
    checker = task.get("check")
    try:
        ok = bool(checker(workspace)) if checker is not None else False
    except Exception:
        ok = False
    return {
        "id": task.get("id"),
        "family": task.get("family"),
        "pack": task.get("pack"),
        "ok": ok,
        "steps": len(trace),
        "trace": trace,
        "finished": finished,
    }


def scripted_reply(calls: list[Call]):
    """Emit the reference calls one turn at a time, then finish."""
    cursor = {"index": 0}

    def reply(_messages):
        from evo.computer.actions import format_call

        if cursor["index"] >= len(calls):
            return format_call("finish", {"answer": "done"})
        call = calls[cursor["index"]]
        cursor["index"] += 1
        return format_call(call.name, call.arguments)

    return reply
