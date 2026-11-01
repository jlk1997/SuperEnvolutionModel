# -*- coding: utf-8 -*-
"""Shared vision softmatch — stem/alias so reasonable VL captions are not false-fail."""
from __future__ import annotations

import re

ALIASES = {
    "totals": "total",
    "confirmation": "confirm",
    "confirming": "confirm",
    "deleting": "delete",
    "deleted": "delete",
    "files": "file",
    "dialogs": "dialog",
    "dialog": "modal",
    "dialogue": "modal",
    "three": "3",
    "two": "2",
    "one": "1",
    "four": "4",
    "five": "5",
    "buttons": "button",
    "printed": "print",
    "invoices": "invoice",
    "settings": "setting",
    "toggles": "toggle",
}


def norm_tok(t: str) -> str:
    t = (t or "").lower().strip()
    t = re.sub(r"[^a-z0-9.\-]+", "", t)
    if not t:
        return ""
    if t in ALIASES:
        return ALIASES[t]
    if len(t) > 3 and t.endswith("ing"):
        stem = t[:-3]
        return ALIASES.get(stem, stem) if len(stem) >= 2 else t
    if len(t) > 3 and t.endswith("s") and not t.endswith("ss"):
        stem = t[:-1]
        return ALIASES.get(stem, stem)
    return t


def tokenize(s: str) -> list[str]:
    parts = re.split(r"[\s,/:#\[\]\?\!\|;]+", (s or "").strip().lower())
    out = []
    stop = {"a", "the", "and", "on", "of", "to", "in", "with", "for", "is", "are", "this", "image", "shows", "display", "displays"}
    for p in parts:
        n = norm_tok(p)
        if not n or n in stop:
            continue
        if len(n) >= 2 or n.isdigit():
            out.append(n)
    return out


def softmatch(pred: str, gold: str, task: str) -> bool:
    p_raw = (pred or "").lower()
    p_toks = set(tokenize(p_raw))
    g_toks = tokenize(gold)
    if not g_toks:
        return len(p_raw.strip()) > 0
    p_join = " ".join(sorted(p_toks))
    hits = 0
    for t in g_toks:
        if t in p_toks or t in p_raw:
            hits += 1
            continue
        if any(t == pt or (len(t) >= 3 and (pt.startswith(t) or t.startswith(pt))) for pt in p_toks):
            hits += 1
    ratio = hits / len(g_toks)
    if task == "ocr":
        return ratio >= 0.5
    if task == "table_cells":
        return ratio >= 0.45
    return ratio >= 0.35
