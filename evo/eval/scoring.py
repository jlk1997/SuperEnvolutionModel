"""SQuAD-style local scoring. No external judge model."""

from __future__ import annotations

import re
import string
from collections import Counter


def normalize_answer(text: str) -> str:
    text = text.lower()
    text = "".join(ch for ch in text if ch not in set(string.punctuation))
    text = re.sub(r"\b(a|an|the)\b", " ", text)
    return " ".join(text.split())


def exact_match(prediction: str, golds: list[str]) -> float:
    pred = normalize_answer(prediction)
    return float(any(pred == normalize_answer(gold) and pred != "" for gold in golds))


def f1_score(prediction: str, gold: str) -> float:
    pred_tokens = normalize_answer(prediction).split()
    gold_tokens = normalize_answer(gold).split()
    if not pred_tokens and not gold_tokens:
        return 1.0
    if not pred_tokens or not gold_tokens:
        return 0.0
    common = Counter(pred_tokens) & Counter(gold_tokens)
    same = sum(common.values())
    if same == 0:
        return 0.0
    precision = same / len(pred_tokens)
    recall = same / len(gold_tokens)
    return 2 * precision * recall / (precision + recall)


def max_f1(prediction: str, golds: list[str]) -> float:
    if not golds:
        return 0.0
    return max(f1_score(prediction, gold) for gold in golds)


def score_prediction(prediction: str, golds: list[str]) -> dict:
    return {
        "em": exact_match(prediction, golds),
        "f1": max_f1(prediction, golds),
    }
