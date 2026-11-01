"""Split a passage's questions into practice, gate, and exam sets."""

from __future__ import annotations


def question_splits(passage: dict, cfg: dict) -> tuple[list[dict], list[dict], list[dict]]:
    """Return (practice, gate, exam).

    The default keeps the historical behavior: all three are the same prefix.
    `split_questions` makes them disjoint so notes and the gate never see the exam.
    """
    qas = list(passage.get("qas") or [])
    limit = int(cfg.get("questions_per_passage") or len(qas) or 1)
    if not cfg.get("split_questions") or len(qas) < 3:
        used = qas[:limit]
        return used, used, used
    practice = qas[:1]
    gate = qas[1:2]
    exam = qas[2:limit]
    if not exam:
        exam = qas[2:3]
    return practice, gate, exam


def with_qas(passage: dict, qas: list[dict]) -> dict:
    graded = dict(passage)
    graded["qas"] = qas
    return graded
