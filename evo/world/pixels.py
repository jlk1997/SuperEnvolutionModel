"""Draw and read a grid with code. The checker is the program output, not a vision model."""

from __future__ import annotations

import random


def vision_status() -> dict:
    return {
        "loaded": False,
        "reason": "Vision weights stay unloaded until the text line has shown faster learning and surviving inventions.",
    }


def _mirror_program(grid: list[list[int]]) -> str:
    literal = repr(grid)
    return (
        f"rows = {literal}\n"
        "print('/'.join(''.join(str(cell) for cell in reversed(row)) for row in rows))"
    )


def _grid_text(grid: list[list[int]]) -> str:
    return "/".join("".join(str(cell) for cell in row) for row in grid)


def mirror_task(split: str, day: int, index: int, rng: random.Random) -> dict:
    grid = [[rng.randrange(2) for _ in range(3)] for _ in range(3)]
    flipped = [list(reversed(row)) for row in grid]
    shown = "\n".join("".join(str(cell) for cell in row) for row in grid)
    gold = _mirror_program(grid)
    return {
        "id": f"d{day}-{split}-pixel-{index}",
        "split": split,
        "day": day,
        "kind": "call",
        "prompt": (
            "Mirror each row of this 3 by 3 grid of digits left to right. "
            "Print one line of three rows separated by slashes.\n"
            f"{shown}"
        ),
        "gold": gold,
        "expect": _grid_text(flipped),
        "tools": [],
        "arg": None,
        "file": None,
        "retention": False,
        "pixel": True,
    }


def draw_task(split: str, day: int, index: int, pattern: str) -> dict:
    patterns = {
        "center": "000010000",
        "corners": "101000101",
        "top": "111000000",
        "bottom": "000000111",
    }
    expect = patterns[pattern]
    return {
        "id": f"d{day}-{split}-draw-{pattern}",
        "split": split,
        "day": day,
        "kind": "call",
        "prompt": f"Print nine digits for a 3 by 3 grid, row by row, pattern {pattern}.",
        "gold": f"print({expect!r})",
        "expect": expect,
        "tools": [],
        "arg": None,
        "file": None,
        "retention": False,
        "pixel": True,
    }


def pixel_bundle(day: int, rng: random.Random) -> dict:
    """Practice mirrors two grids. The exam grid and the bottom-row drawing are held out."""
    practice_rng = random.Random(rng.randrange(1_000_000))
    exam_rng = random.Random(rng.randrange(1_000_000) + 17)
    practice = [mirror_task("practice", day, index, practice_rng) for index in range(2)]
    practice.append(draw_task("practice", day, 0, "center"))
    exam = [mirror_task("exam", day, 0, exam_rng), draw_task("exam", day, 1, "bottom")]
    gate = [mirror_task("gate", day, 0, random.Random(rng.randrange(1_000_000) + 29))]
    return {"practice": practice, "gate": gate, "exam": exam}
