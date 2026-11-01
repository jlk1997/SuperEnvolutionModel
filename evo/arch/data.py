"""Synthetic domains for sequential learning and test-time absorption."""

from __future__ import annotations

import random


OBJECTS = [
    ("sky", "blue", "air"),
    ("grass", "green", "fiber"),
    ("coal", "black", "carbon"),
    ("chalk", "white", "lime"),
    ("lemon", "yellow", "pulp"),
    ("brick", "red", "clay"),
    ("ocean", "blue", "water"),
    ("sand", "tan", "silica"),
    ("leaf", "green", "cellulose"),
    ("snow", "white", "ice"),
    ("copper", "orange", "metal"),
    ("ink", "black", "pigment"),
    ("wheat", "gold", "grain"),
    ("clay", "brown", "soil"),
    ("lilac", "purple", "petal"),
    ("moss", "green", "plant"),
    ("salt", "white", "crystal"),
    ("rust", "brown", "iron"),
    ("grape", "purple", "fruit"),
    ("ash", "gray", "cinder"),
]


def _attribute_sentences(items: list[tuple[str, str, str]]) -> list[str]:
    sentences = []
    for name, color, material in items:
        sentences.append(f"the {name} is {color} .")
        sentences.append(f"color of the {name} is {color} .")
        sentences.append(f"the {name} is made of {material} .")
    return sentences


def domain_attributes() -> tuple[list[str], list[str]]:
    items = list(OBJECTS)
    random.Random(0).shuffle(items)
    cut = max(1, len(items) // 5)
    return _attribute_sentences(items[cut:]), _attribute_sentences(items[:cut])


def domain_arithmetic() -> tuple[list[str], list[str]]:
    train, test = [], []
    for left in range(12):
        for right in range(12):
            sentence = f"{left} plus {right} equals {left + right} ."
            if (left + right) % 5 == 0:
                test.append(sentence)
            else:
                train.append(sentence)
    return train, test


def domain_novel() -> list[str]:
    facts = [
        ("flute", "blowing"),
        ("drum", "striking"),
        ("harp", "plucking"),
        ("horn", "buzzing"),
        ("bell", "ringing"),
        ("violin", "bowing"),
        ("lyre", "strumming"),
        ("gong", "hitting"),
    ]
    sentences = []
    for name, action in facts:
        sentences.append(f"the {name} is played by {action} .")
        sentences.append(f"playing the {name} means {action} .")
    return sentences


class WordTokenizer:
    def __init__(self, texts: list[str]):
        table = {"<pad>": 0, "<unk>": 1}
        for text in texts:
            for word in text.split():
                if word not in table:
                    table[word] = len(table)
        self.stoi = table

    def encode(self, text: str) -> list[int]:
        return [self.stoi.get(word, 1) for word in text.split()]

    @property
    def vocab_size(self) -> int:
        return len(self.stoi)


def build_corpus() -> dict:
    a_train, a_test = domain_attributes()
    b_train, b_test = domain_arithmetic()
    novel = domain_novel()
    tok = WordTokenizer(a_train + a_test + b_train + b_test + novel)
    return {
        "tokenizer": tok,
        "a_train": a_train,
        "a_test": a_test,
        "b_train": b_train,
        "b_test": b_test,
        "novel": novel,
    }


def stream(sentences: list[str], tok: WordTokenizer) -> list[int]:
    ids: list[int] = []
    for sentence in sentences:
        ids.extend(tok.encode(sentence))
    if len(ids) < 8:
        raise RuntimeError("domain stream is too short")
    while len(ids) < 4096:
        ids = ids + ids
    return ids


def sample_batch(ids: list[int], batch: int, seq_len: int, rng: random.Random) -> list[list[int]]:
    if len(ids) <= seq_len:
        raise RuntimeError("cannot sample a batch from a short stream")
    rows = []
    for _ in range(batch):
        start = rng.randrange(0, len(ids) - seq_len)
        rows.append(ids[start : start + seq_len])
    return rows
