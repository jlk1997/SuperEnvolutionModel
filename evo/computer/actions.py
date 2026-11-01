"""Qwen3.5 tool-call text, plus a code-fence fallback for smaller models."""

from __future__ import annotations

import re
from dataclasses import dataclass


ACTIONS = ("python", "shell", "read_file", "write_file", "list_dir", "http", "finish")

OFFICE_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": name,
            "description": text,
            "parameters": {"type": "object", "properties": props, "required": required},
        },
    }
    for name, text, props, required in (
        ("python", "Run Python inside the workspace.", {"code": {"type": "string"}}, ["code"]),
        ("shell", "Run ONE allowlisted cmd in the workspace (mkdir, dir, type, copy; cp→copy). Relative paths only. No &&, pipes, or /path/to placeholders.", {"cmd": {"type": "string"}}, ["cmd"]),
        ("read_file", "Read a workspace file.", {"path": {"type": "string"}}, ["path"]),
        ("write_file", "Write a workspace file.", {"path": {"type": "string"}, "text": {"type": "string"}}, ["path", "text"]),
        ("list_dir", "List a workspace directory.", {"path": {"type": "string"}}, ["path"]),
        ("http", "Call an authorized HTTP API.", {"method": {"type": "string"}, "url": {"type": "string"}, "body": {"type": "string"}}, ["method", "url"]),
        ("finish", "Stop. The workspace is graded as it stands.", {"answer": {"type": "string"}}, []),
    )
]


_CALL = re.compile(r"<tool_call>\s*<function=([A-Za-z0-9_]+)>(.*?)</function>\s*</tool_call>", re.DOTALL)
_PARAM = re.compile(r"<parameter=([A-Za-z0-9_]+)>\s*(.*?)\s*</parameter>", re.DOTALL)
_FENCE = re.compile(r"```(?:python)?\s*(.*?)```", re.DOTALL)


@dataclass
class Call:
    name: str
    arguments: dict[str, str]
    raw: str = ""


def format_call(name: str, arguments: dict | None = None) -> str:
    lines = ["<tool_call>", f"<function={name}>"]
    for key, value in (arguments or {}).items():
        lines.append(f"<parameter={key}>")
        lines.append(str(value))
        lines.append("</parameter>")
    lines.append("</function>")
    lines.append("</tool_call>")
    return "\n".join(lines)


def format_response(text: str) -> str:
    return "<tool_response>\n" + str(text) + "\n</tool_response>"


_CALL_LOOSE = re.compile(
    r"(?:<tool_call>\s*)?<function(?:=|\s*>)\s*([A-Za-z0-9_]+)\s*>(.*?)</function>(?:\s*</tool_call>)?",
    re.DOTALL,
)
_PARAM_LOOSE = re.compile(r"<parameter(?:=|\s*>)\s*([A-Za-z0-9_]+)\s*>\s*(.*?)\s*</parameter>", re.DOTALL)
_ARG_ALIASES = {"command": "cmd", "cmd": "cmd", "code": "code", "path": "path", "text": "text",
                "url": "url", "method": "method", "body": "body", "answer": "answer"}


def parse_calls(text: str) -> list[Call]:
    """Native tool calls + loose <function>name> forms. Fence → python fallback."""
    found = []
    blob = text or ""
    for match in _CALL.finditer(blob):
        name = match.group(1)
        arguments = {key: value for key, value in _PARAM.findall(match.group(2))}
        if name not in ACTIONS:
            found.append(Call(name, arguments, match.group(0)))
        else:
            found.append(Call(name, arguments, match.group(0)))
    if not found:
        for match in _CALL_LOOSE.finditer(blob):
            name = match.group(1)
            raw_args = {key: value for key, value in _PARAM_LOOSE.findall(match.group(2))}
            arguments = {}
            for key, value in raw_args.items():
                dest = _ARG_ALIASES.get(key, key)
                arguments[dest] = value
            found.append(Call(name, arguments, match.group(0)))
    if found:
        return found
    # <function>shell</function><parameter>cmd text</parameter> (anonymous parameter)
    bare = re.compile(
        r"<function>\s*([A-Za-z0-9_]+)\s*</function>\s*<parameter>\s*(.*?)\s*</parameter>",
        re.DOTALL,
    )
    for match in bare.finditer(blob):
        name = match.group(1)
        raw = match.group(2).strip()
        if name == "shell":
            arguments = {"cmd": raw}
        elif name == "python":
            arguments = {"code": raw}
        elif name in ("read_file", "list_dir"):
            arguments = {"path": raw}
        elif name == "finish":
            arguments = {"answer": raw}
        else:
            arguments = {"text": raw}
        found.append(Call(name, arguments, match.group(0)))
    if found:
        return found
    fence = _FENCE.search(blob)
    if fence and fence.group(1).strip():
        return [Call("python", {"code": fence.group(1).strip()}, fence.group(0))]
    return []
