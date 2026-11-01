"""Gate text copied from the roadmap, not a new judgment."""

from __future__ import annotations

from pathlib import Path


_MARKERS = (
    ("GATE1", "闸门 1", "连续学习和倒班"),
    ("GATE2", "闸门 2", "办公世界里的双节律"),
    ("GATE3", "闸门 3", "封存行业包"),
)


def load_gates(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    gates = []
    for key, title, about in _MARKERS:
        start = text.find(f"<!-- {key}_START -->")
        end = text.find(f"<!-- {key}_END -->")
        if start < 0 or end < 0 or end <= start:
            gates.append(
                {
                    "id": key.lower(),
                    "title": title,
                    "about": about,
                    "passed": None,
                    "body": "",
                    "source": str(path),
                }
            )
            continue
        body = text[start + len(f"<!-- {key}_START -->") : end].strip()
        if "判定：未通过" in body:
            passed = False
        elif "判定：通过" in body:
            passed = True
        else:
            passed = None
        gates.append(
            {
                "id": key.lower(),
                "title": title,
                "about": about,
                "passed": passed,
                "body": body,
                "source": "docs/ROADMAP.md",
            }
        )
    return gates
