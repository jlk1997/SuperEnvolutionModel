"""Text the night sorter and the absorption book can see. The hidden answer stays out."""

from __future__ import annotations

from pathlib import Path


def trace_text(result: dict) -> str:
    parts = []
    for row in result.get("trace") or []:
        arguments = row.get("arguments") or {}
        parts.append(str(arguments.get("code") or arguments.get("cmd") or row.get("name") or ""))
    return "\n".join(part for part in parts if part and part != "finish")


def workspace_files(workspace: Path, limit: int = 30) -> list[dict]:
    if not workspace.is_dir():
        return []
    rows = []
    for path in sorted(workspace.rglob("*")):
        if not path.is_file() or path.name == "audit.jsonl":
            continue
        rel = str(path.relative_to(workspace))
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = "(binary)"
        except OSError as exc:
            text = f"(unreadable: {exc})"
        rows.append({"path": rel, "text": text[:800]})
        if len(rows) >= limit:
            break
    return rows
