"""Small BM25 ranker. No extra packages."""

from __future__ import annotations

import math
import re


_TOKEN = re.compile(r"[a-z0-9_']+")


def _tokens(text: str) -> list[str]:
    return _TOKEN.findall(text.lower())


def bm25_rank(query: str, documents: list[dict], k: int = 3, k1: float = 1.5, b: float = 0.75) -> list[dict]:
    """Return the top `k` documents. Each document needs `id` and `text`."""
    if not documents or k <= 0:
        return []
    docs = [(doc, _tokens(doc.get("text") or "")) for doc in documents]
    lengths = [len(tokens) for _doc, tokens in docs]
    avg = (sum(lengths) / len(lengths)) if lengths else 1.0
    df: dict[str, int] = {}
    for _doc, tokens in docs:
        for token in set(tokens):
            df[token] = df.get(token, 0) + 1
    n_docs = len(docs)
    query_tokens = _tokens(query)
    scored = []
    for doc, tokens in docs:
        if not tokens:
            scored.append((0.0, doc))
            continue
        counts: dict[str, int] = {}
        for token in tokens:
            counts[token] = counts.get(token, 0) + 1
        score = 0.0
        for token in query_tokens:
            freq = counts.get(token, 0)
            if not freq:
                continue
            idf = math.log(1.0 + (n_docs - df.get(token, 0) + 0.5) / (df.get(token, 0) + 0.5))
            denom = freq + k1 * (1.0 - b + b * len(tokens) / avg)
            score += idf * (freq * (k1 + 1.0) / denom)
        scored.append((score, doc))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [doc for score, doc in scored[:k] if score > 0] or [doc for _score, doc in scored[:k]]
