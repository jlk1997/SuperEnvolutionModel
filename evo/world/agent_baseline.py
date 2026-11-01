"""Agent control: a plan prompt, BM25 over tool notes, error retry, and a solution file.

The weights stay frozen. Everything it remembers sits in the prompt.
"""

from __future__ import annotations

from evo.retrieval import bm25_rank


def agent_notes(task: dict, documents: list[dict], solutions: list[dict], error: str, k_docs: int = 3) -> str:
    query = task["prompt"] + ("\n" + error if error else "")
    docs = bm25_rank(query, documents, k=k_docs)
    past = bm25_rank(query, solutions, k=1)
    prompt = task.get("prompt") or ""
    if "workspace" in prompt or "prefers" in prompt:
        lines = [
            "Follow the task. If it asks for a file, write that file under workspace. If it mentions a preference, use the preference note.",
            "Reply with code only.",
        ]
    else:
        lines = [
            "Plan: find the tool nickname in the notes, then write one print call using that function name and the value in the task.",
            "Reply with code only.",
        ]
    if docs:
        lines.append("Tool notes:")
        lines.extend(f"- {doc['text']}" for doc in docs)
    if past:
        lines.append("A past solution:")
        lines.append(past[0]["text"])
    return "\n".join(lines)


def oracle_notes(task: dict, documents: list[dict], solutions: list[dict], error: str) -> str:
    """Context ceiling: every tool note and every past solution, not a retrieved slice.

    The task argument is unused. The signature matches `agent_notes` so the same caller can switch.
    """
    del task
    lines = ["Every tool note and every past solution is below. Reply with code only."]
    if documents:
        lines.append("Tool notes:")
        lines.extend(f"- {doc['text']}" for doc in documents)
    if solutions:
        lines.append("Past solutions:")
        lines.extend(item["text"] for item in solutions)
    if error and error.strip():
        lines.append("The previous program failed:\n" + error.strip()[:500])
    return "\n".join(lines)


def remember_solution(solutions: list[dict], task: dict, code: str) -> None:
    solutions.append(
        {
            "id": task["id"],
            "text": task["prompt"] + "\n" + code,
            "task": task["id"],
        }
    )
