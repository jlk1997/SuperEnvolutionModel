"""A tool changes its behavior. Old exam answers are recomputed from the new source."""

from __future__ import annotations

from evo.world.tasks import _expect


def shift_number_tool(tool: dict) -> bool:
    """Add one to a number tool's step. The lesson text changes with the source."""
    if tool.get("kind") != "number" or "step" not in tool:
        return False
    step = int(tool["step"])
    new_step = step + 1
    old = f"return int(number) + {step}"
    new = f"return int(number) + {new_step}"
    if old not in tool["source"]:
        return False
    tool["source"] = tool["source"].replace(old, new, 1)
    tool["doc"] = tool["doc"].replace(f"plus {step}", f"plus {new_step}")
    tool["step"] = new_step
    tool["drifted"] = True
    tool["drift_from"] = step
    return True


def drift_oldest(tools: list[dict]) -> dict | None:
    numbers = [tool for tool in tools if tool.get("kind") == "number" and not tool.get("drifted")]
    if not numbers:
        return None
    target = sorted(numbers, key=lambda tool: tool.get("day", 0))[0]
    if not shift_number_tool(target):
        return None
    return target


def refresh_expects(tasks: list[dict], tools: list[dict], timeout: float) -> int:
    changed = 0
    for task in tasks:
        gold = task.get("gold")
        if not gold or task.get("kind") != "call":
            continue
        try:
            updated = _expect(tools, gold, timeout)
        except RuntimeError:
            continue
        if updated != task.get("expect"):
            task["expect"] = updated
            changed += 1
    return changed
