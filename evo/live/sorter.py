"""Night sort: a skill is general, local, or dropped. Cross-pack scores decide.

Frozen. The plasticity-evolution line does not extend this module.
"""

from __future__ import annotations


def classify(own_before: float, own_after: float, others_before: list[float], others_after: list[float], tol: float = 0.0) -> str:
    """core if the home pack rose and no other pack fell. local if only home rose. else drop."""
    own_up = float(own_after) > float(own_before) + tol
    if others_before and any(float(after) < float(before) - tol for before, after in zip(others_before, others_after)):
        return "drop"
    if not own_up:
        return "drop"
    if not others_before:
        return "local"
    if all(float(after) + tol >= float(before) for before, after in zip(others_before, others_after)):
        return "core"
    return "local"


def structural_class(text: str, secret: str, generic_marks: list[str]) -> str:
    """A cheap sort when there is no second pack to retest yet.

    A private canary string in the skill is local. A generic operation with no canary is core.
    """
    body = text or ""
    if secret and secret in body:
        return "local"
    if any(mark in body for mark in generic_marks):
        return "core"
    return "drop"


def resolve_sort(text: str, secret: str, marks: list[str], fields: list[str], cross_met: bool) -> str:
    """Column names from this pack stay local. Core waits until another pack has held."""
    structural = structural_class(text, secret, marks)
    bound = any(field and str(field) in (text or "") for field in fields)
    if bound or structural == "local":
        return "local"
    if structural == "drop":
        return "drop"
    if not cross_met:
        return "local"
    return "core"
