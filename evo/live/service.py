"""A small service whose answers change. The model speaks an action, not a hidden function.

The manual is what a scaffold would read. The evolved model is not given it.
After drift, yesterday's correct action returns a different body.
"""

from __future__ import annotations

import random
import re


_ACTION = re.compile(r"HTTP\s+GET\s+/([A-Za-z_]\w*)/(-?\d+)\b", re.IGNORECASE)


def parse_action(text: str) -> dict | None:
    matched = _ACTION.search(text or "")
    if matched is None:
        return None
    return {"name": matched.group(1), "arg": int(matched.group(2))}


class DriftAPI:
    def __init__(self, seed: int, count: int = 2):
        rng = random.Random(seed)
        self.endpoints: dict[str, dict] = {}
        for index in range(count):
            name = rng.choice(("zor", "nub", "vek", "pim")) + rng.choice(("qal", "rix", "fom", "jad"))
            while name in self.endpoints:
                name += str(rng.randrange(10))
            self.endpoints[name] = {"step": rng.choice((2, 3, 4)), "birth": 0, "drifted": False}
        self._order = list(self.endpoints)

    def call(self, name: str, arg: int) -> int:
        return int(arg) + int(self.endpoints[name]["step"])

    def act(self, text: str) -> tuple[bool, str]:
        action = parse_action(text)
        if action is None or action["name"] not in self.endpoints:
            return False, ""
        return True, str(self.call(action["name"], action["arg"]))

    def drift(self) -> str | None:
        pending = [name for name in self._order if not self.endpoints[name]["drifted"]]
        if not pending:
            return None
        name = pending[0]
        self.endpoints[name]["step"] = int(self.endpoints[name]["step"]) + 1
        self.endpoints[name]["drifted"] = True
        return name

    def manual(self) -> str:
        lines = ["Service routes. The body is the argument plus the step."]
        for name in self._order:
            step = self.endpoints[name]["step"]
            lines.append(f"GET /{name}/<n> returns <n> plus {step}.")
        return "\n".join(lines)

    def task(self, name: str, arg: int, split: str) -> dict:
        return {
            "id": f"{split}-{name}-{arg}",
            "split": split,
            "kind": "http",
            "prompt": f"Call the service with HTTP GET /{name}/{arg}. Reply with that action line only.",
            "expect": str(self.call(name, arg)),
            "tools": [name],
            "arg": str(arg),
        }


def grade_action(text: str, api: DriftAPI, expect: str) -> bool:
    """The reply must name the route and state the body. The route alone is not an answer."""
    ok, _body = api.act(text)
    if not ok:
        return False
    claimed = _claimed_body(text)
    return claimed is not None and claimed == str(expect)


def _claimed_body(text: str) -> str | None:
    lines = [line.strip() for line in (text or "").splitlines() if line.strip()]
    for line in reversed(lines):
        if line.upper().startswith("HTTP"):
            continue
        if re.fullmatch(r"-?\d+", line):
            return line
    return None


def _reply(name: str, arg: int, step: int | None) -> str:
    action = f"HTTP GET /{name}/{arg}"
    if step is None:
        return action
    return action + "\n" + str(int(arg) + int(step))


def _step_in_manual(manual: str, name: str) -> int | None:
    matched = re.search(rf"GET /{name}/<n> returns <n> plus (\d+)", manual)
    if matched is None:
        return None
    return int(matched.group(1))


def run_actors(actors: dict[str, tuple[str, object]], seed: int = 1, steps: int = 6, drift_at: int = 3) -> dict:
    """Each actor is `(role, reply)`.

    Role `fresh` is handed the manual as it is now. `frozen` is handed the manual from
    before the first drift. `bare` is handed nothing. `reply(task, manual)` returns text.
    A reply the body would refuse is a failure and is not executed.
    """
    from evo.live.rails import denied

    api = DriftAPI(seed, count=2)
    names = list(api.endpoints)
    frozen = api.manual()
    rows = {name: [] for name in actors}
    for tick in range(steps):
        if tick == drift_at:
            api.drift()
        name = names[tick % len(names)]
        arg = 3 + tick
        task = api.task(name, arg, "exam")
        task["expect"] = str(api.call(name, arg))
        for actor, (role, reply) in actors.items():
            manual = api.manual() if role == "fresh" else frozen if role == "frozen" else None
            text = reply(task, manual)
            if denied(text or "", {"python", "http"}):
                rows[actor].append(False)
            else:
                rows[actor].append(grade_action(text, api, task["expect"]))
    fresh = rows.get("fresh") or []
    return {
        "rows": rows,
        "absorption": {name: absorption(flags, fresh) for name, flags in rows.items() if name != "fresh"},
    }


def _scripted_pair():
    remembered: dict[str, int] = {}

    def fresh(task, manual):
        return _reply(task["tools"][0], int(task["arg"]), _step_in_manual(manual or "", task["tools"][0]))

    def frozen(task, manual):
        return fresh(task, manual)

    def bare(task, _manual):
        name = task["tools"][0]
        text = _reply(name, int(task["arg"]), remembered.get(name))
        return text

    def bare_after(task, manual):
        text = bare(task, manual)
        remembered[task["tools"][0]] = int(task["expect"]) - int(task["arg"])
        return text

    return {"fresh": ("fresh", fresh), "stale": ("frozen", frozen), "evolved": ("bare", bare_after)}


def run_pair(seed: int = 1, steps: int = 6, drift_at: int = 3) -> dict:
    """Fresh manual, a frozen manual, and a model that only remembers what it was told came back."""
    session = run_actors(_scripted_pair(), seed=seed, steps=steps, drift_at=drift_at)
    rows = session["rows"]
    return {
        "fresh": rows["fresh"],
        "stale": rows["stale"],
        "evolved": rows["evolved"],
        "absorption_fresh": session["absorption"].get("evolved"),
        "absorption_stale": absorption(rows["evolved"], rows["stale"]),
    }


def write_pair(path: str = "runs/service_pair.json") -> dict:
    import json
    from pathlib import Path

    from evo.util import repo_path

    payload = run_pair()
    dest = repo_path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(
        f"[service] fresh={sum(payload['fresh'])}/{len(payload['fresh'])} "
        f"stale={sum(payload['stale'])}/{len(payload['stale'])} "
        f"evolved={sum(payload['evolved'])}/{len(payload['evolved'])} "
        f"absorption_fresh={payload['absorption_fresh']}",
        flush=True,
    )
    return payload


def model_reply(evo, adapter: str | None, tokens: int = 48):
    """A reply function for `run_actors`. The manual is included only when the role passes one."""

    def reply(task: dict, manual: str | None) -> str:
        from evo.generate import generate

        prompt = task["prompt"]
        if manual:
            prompt = manual + "\n\n" + prompt
        return generate(evo, prompt, tokens, 0.0, adapter)

    return reply


def absorption(evolved: list[bool], scaffold: list[bool]) -> float | None:
    """Of the items the scaffold still solves, the share the bare model also solves.

    None when the scaffold solved nothing, because there is nothing to absorb.
    """
    both = [(left, right) for left, right in zip(evolved, scaffold) if right]
    if not both:
        return None
    return sum(1.0 for left, _right in both if left) / len(both)
