"""A failed attempt that matches a different legal task becomes a demonstration of that task."""

from __future__ import annotations


def relabel(produced: float, asked: str, alternatives: list[tuple[str, float]], tol: float = 0.01) -> str | None:
    """Return the other task name when the number is that task's answer, not the one that was asked."""
    for name, value in alternatives:
        if name == asked:
            continue
        if abs(float(produced) - float(value)) <= tol:
            return name
    return None
