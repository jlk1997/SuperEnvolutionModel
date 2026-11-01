"""Morning census of every held-out exam. It records. It does not train or select."""

from __future__ import annotations

import random


def census_full(day: int, every: int, last: bool) -> bool:
    if last or every <= 1:
        return True
    return day % every == 0


def pick_tasks(tasks: list[dict], day: int, every: int, sample: int, rng: random.Random, last: bool = False) -> list[dict]:
    """Full paper every `every` days. Other mornings take an even sample."""
    if not tasks:
        return []
    if census_full(day, every, last) or sample <= 0 or len(tasks) <= sample:
        return list(tasks)
    step = len(tasks) / sample
    chosen = []
    seen = set()
    for index in range(sample):
        item = tasks[min(len(tasks) - 1, int(index * step))]
        if item["id"] in seen:
            continue
        seen.add(item["id"])
        chosen.append(item)
    return chosen


def mastery_lags(events: list[dict], actor: str, births: dict[str, int]) -> list[dict]:
    """Nights from a tool's arrival until an exam that uses it passes and keeps passing."""
    by_tool: dict[str, list[dict]] = {}
    for event in events:
        if event["actor"] != actor:
            continue
        for name in event["tools"]:
            by_tool.setdefault(name, []).append(event)
    rows = []
    for name, birth in births.items():
        seq = by_tool.get(name) or []
        mastered = None
        for event in seq:
            if not event["ok"]:
                continue
            later = [item for item in seq if item["day"] >= event["day"]]
            if later and all(item["ok"] for item in later):
                mastered = event["day"]
                break
        if mastered is not None:
            rows.append({"tool": name, "birth": int(birth), "lag": mastered - int(birth)})
    return rows


def mastery_lag(events: list[dict], actor: str, births: dict[str, int]) -> float | None:
    lags = [row["lag"] for row in mastery_lags(events, actor, births)]
    if not lags:
        return None
    return sum(lags) / len(lags)


def rollback_rates(flags: list[bool]) -> list[float]:
    """Share of nights returned so far. The morning row is not a night."""
    rates = []
    rolled = 0
    for index, flag in enumerate(flags, start=1):
        rolled += int(bool(flag))
        rates.append(rolled / index)
    return rates


def later_faster(lags: list[dict]) -> dict | None:
    """Compare tools that arrived in the second half of births with the first half.

    A smaller lag means the tool was mastered sooner. None when one side is empty.
    """
    if len(lags) < 2:
        return None
    births = sorted({int(item["birth"]) for item in lags})
    mid = births[len(births) // 2]
    early = [int(item["lag"]) for item in lags if int(item["birth"]) < mid]
    late = [int(item["lag"]) for item in lags if int(item["birth"]) >= mid]
    if not early or not late:
        return None
    early_mean = sum(early) / len(early)
    late_mean = sum(late) / len(late)
    return {"early_lag": early_mean, "late_lag": late_mean, "later_faster": late_mean < early_mean}


class Census:
    def __init__(self):
        self.events: list[dict] = []
        self.seen: dict[str, dict[str, dict]] = {}

    def add(self, day: int, actor: str, rows: list[dict]) -> None:
        book = self.seen.setdefault(actor, {})
        for row in rows:
            task = row["task"]
            record = book.setdefault(task["id"], {"ever": False, "tools": list(task.get("tools") or [])})
            ok = bool(row.get("ok"))
            if ok:
                record["ever"] = True
            record["last"] = ok
            record["tools"] = list(task.get("tools") or [])
            self.events.append(
                {
                    "day": day,
                    "actor": actor,
                    "id": task["id"],
                    "ok": ok,
                    "tokens": int(row.get("prompt_tokens") or 0),
                    "tools": list(task.get("tools") or []),
                }
            )

    def report(self, actor: str, day: int, births: dict[str, int]) -> dict:
        book = self.seen.get(actor, {})
        alive = sum(1 for record in book.values() if record.get("last"))
        forgotten = sum(1 for record in book.values() if record.get("ever") and not record.get("last"))
        todays = [event for event in self.events if event["actor"] == actor and event["day"] == day and event["ok"]]
        tokens = None
        if todays:
            tokens = sum(event["tokens"] for event in todays) / len(todays)
        return {
            "alive": alive,
            "forgotten": forgotten,
            "tracked": len(book),
            "mastery": mastery_lag(self.events, actor, births),
            "lags": mastery_lags(self.events, actor, births),
            "tokens_per_ok": tokens,
        }
