"""Office jobs arrive one at a time. The sandbox grades every attempt.

Three arms see the same jobs in the same order:

- frozen: the base model, greedy, nothing kept.
- notes: the base model with the last verified success of the same kind of job in the prompt.
- evolve: the policy adapter, trained on its own verified successes.

The online score is the first greedy attempt at each job, before any practice on it.
After a miss, the notes and evolve arms practise: a few samples on the missed job and
on new instances of the same kind (new seed and industry pack, made by the job
generator), each graded by the sandbox. Successes become notes or training pairs.
The evolve arm trains every `learn_every` jobs and keeps the update only if a fixed
gate set of jobs does not get worse. At the end every arm takes the same fresh exam:
new instances of every kind, greedy, no practice.

Sealed held-out packs are not imported here.
"""

from __future__ import annotations

import random
import shutil
import time
from pathlib import Path

import torch


KINDS = (("table", 0), ("table", 1), ("file", 0), ("file", 1), ("report", 0), ("report", 1), ("shell", 0))
ASK = "Work in the current folder. Reply with one ```python``` block that does the job. No explanation."


def job(kind: tuple[str, int], seed: int, difficulty: int = 1) -> dict:
    from evo.office.families import make_task
    from evo.office.packs import DEV_PACKS

    family, variant = kind
    pack = DEV_PACKS[seed % len(DEV_PACKS)]
    task = make_task(pack, family, seed, variant=variant, difficulty=difficulty)
    task["kind"] = f"{family}{variant}"
    return task


def ask_text(task: dict, note: str = "") -> str:
    text = task["prompt"] + "\n" + ASK
    if note:
        text += "\n\nA previous success on this kind of job:\n" + note
    return text


def plan_stream(n: int, seed: int) -> list[dict]:
    """Every kind once per block, in a shuffled order. Seeds never repeat."""
    rng = random.Random(seed)
    rows = []
    while len(rows) < n:
        block = list(KINDS)
        rng.shuffle(block)
        for kind in block:
            if len(rows) >= n:
                break
            rows.append({"index": len(rows), "kind": kind, "seed": 100 + seed * 1000 + len(rows)})
    return rows


def grade(task: dict, reply: str, root: Path, tag: str) -> bool:
    from evo.computer.episode import run_episode
    from evo.computer.license import License

    workspace = root / tag
    if workspace.exists():
        shutil.rmtree(workspace, ignore_errors=True)
    license = License(grants={"python", "shell", "read", "write"}, max_steps=1, timeout=8.0)
    sent = {"done": False}

    def reply_fn(_messages):
        if sent["done"]:
            return ""
        sent["done"] = True
        return reply

    try:
        result = run_episode(task, reply_fn, workspace, license)
        return bool(result["ok"])
    except Exception:
        return False
    finally:
        shutil.rmtree(workspace, ignore_errors=True)


def sample(evo, prompt: str, count: int, max_new: int, temperature: float, adapter) -> list[str]:
    from evo.generate import render_user
    from evo.model import activate

    model, tok = evo.model, evo.tok
    model.eval()
    text, add_special = render_user(tok, prompt)
    encoded = tok(text, return_tensors="pt", add_special_tokens=add_special)
    encoded = {key: value.to(evo.device) for key, value in encoded.items()}
    previous = model.config.use_cache
    model.config.use_cache = True
    try:
        with activate(model, adapter), torch.no_grad():
            output = model.generate(
                **encoded,
                max_new_tokens=int(max_new),
                do_sample=True,
                temperature=float(temperature),
                top_p=0.95,
                num_return_sequences=int(count),
                pad_token_id=tok.pad_token_id,
                eos_token_id=tok.eos_token_id,
            )
    finally:
        model.config.use_cache = previous
    width = encoded["input_ids"].shape[1]
    return [tok.decode(row[width:], skip_special_tokens=True).strip() for row in output]


class Arm:
    def __init__(self, name: str, body, cfg: dict, root: Path):
        self.name = name
        self.body = body
        self.cfg = cfg
        self.root = root
        self.notes: dict[str, str] = {}
        self.pool: list[tuple[str, str]] = []
        self.fresh_pairs = 0
        self.updates: list[dict] = []
        self.online: list[dict] = []

    @property
    def adapter(self):
        return "policy" if self.name == "evolve" else None

    def prompt(self, task: dict) -> str:
        note = self.notes.get(task["kind"], "") if self.name == "notes" else ""
        return ask_text(task, note)

    def greedy(self, tasks: list[dict]) -> list[str]:
        from evo.plastic.fastscore import generate_batch

        prompts = [self.prompt(task) for task in tasks]
        return generate_batch(self.body.evo, prompts, int(self.cfg.get("stream_new", 256)), self.adapter, batch_size=8, max_len=1024)

    def keep(self, task: dict, reply: str) -> None:
        if self.name == "notes":
            self.notes[task["kind"]] = reply[:900]
        elif self.name == "evolve":
            self.pool.append((ask_text(task), reply))
            self.fresh_pairs += 1

    def practise(self, kind: tuple[str, int], task: dict, index: int) -> int:
        """Samples on the missed job and on new instances of its kind. Returns verified successes."""
        found = 0
        tries = [task] + [job(kind, 50_000 + index * 10 + extra) for extra in range(int(self.cfg.get("variants", 1)))]
        for number, target in enumerate(tries):
            replies = sample(
                self.body.evo,
                self.prompt(target),
                int(self.cfg.get("samples", 4)),
                int(self.cfg.get("stream_new", 256)),
                float(self.cfg.get("temperature", 0.8)),
                self.adapter,
            )
            for slot, reply in enumerate(replies):
                if grade(target, reply, self.root, f"{self.name}-p{index}-{number}-{slot}"):
                    self.keep(target, reply)
                    found += 1
                    break
        return found


def _gate_tasks(kinds: list[tuple[str, int]]) -> list[dict]:
    return [job(kind, 70_000 + KINDS.index(kind)) for kind in kinds]


def _gate_score(arm: Arm, tasks: list[dict]) -> int:
    replies = arm.greedy(tasks)
    return sum(grade(task, reply, arm.root, f"gate-{i}") for i, (task, reply) in enumerate(zip(tasks, replies)))


def learn_from_pool(arm: Arm, seen_kinds: list[tuple[str, int]]) -> dict:
    """Train policy on every verified success so far. Keep it only if the gate set does not get worse."""
    from evo.model import adapter_state, load_adapter_state
    from evo.plastic.life import Writer

    evo = arm.body.evo
    gate = _gate_tasks(seen_kinds)
    before = _gate_score(arm, gate)
    saved = adapter_state(evo.model, "policy")
    writer = Writer(evo, "policy", {"mlp": float(arm.cfg.get("stream_lr", 1e-4))}, max_len=1024)
    rng = random.Random(len(arm.pool))
    pairs = list(arm.pool)
    batch = int(arm.cfg.get("stream_batch", 4))
    for _ in range(int(arm.cfg.get("stream_passes", 2))):
        rng.shuffle(pairs)
        for start in range(0, len(pairs), batch):
            writer.step(pairs[start : start + batch])
    after = _gate_score(arm, gate)
    kept = after >= before
    if not kept:
        load_adapter_state(evo.model, "policy", saved)
    row = {"pool": len(arm.pool), "gate": len(gate), "before": before, "after": after, "kept": kept}
    arm.updates.append(row)
    arm.fresh_pairs = 0
    print(f"[stream] learn pool={len(arm.pool)} gate {before}->{after} kept={kept}", flush=True)
    return row


def run_arm(name: str, body, plan: list[dict], cfg: dict, root: Path) -> dict:
    started = time.time()
    body.reset()
    arm = Arm(name, body, cfg, root)
    seen: list[tuple[str, int]] = []
    learn_every = int(cfg.get("learn_every", 4))
    for step in plan:
        kind = step["kind"]
        if kind not in seen:
            seen.append(kind)
        task = job(kind, step["seed"])
        reply = arm.greedy([task])[0]
        ok = grade(task, reply, root, f"{name}-{step['index']}")
        found = 0
        if name != "frozen":
            if ok:
                arm.keep(task, reply)
            else:
                found = arm.practise(kind, task, step["index"])
        arm.online.append({"index": step["index"], "kind": task["kind"], "ok": ok, "practice_found": found})
        print(f"[stream] {name} job {step['index']} {task['kind']} ok={ok} found={found}", flush=True)
        if name == "evolve" and arm.fresh_pairs and (step["index"] + 1) % learn_every == 0:
            learn_from_pool(arm, seen)
    if name == "evolve" and arm.fresh_pairs:
        learn_from_pool(arm, seen)
    exam = [job(kind, 90_000 + KINDS.index(kind) * 10 + copy) for kind in KINDS for copy in range(int(cfg.get("exam_copies", 2)))]
    replies = arm.greedy(exam)
    exam_ok = [grade(task, reply, root, f"{name}-exam-{i}") for i, (task, reply) in enumerate(zip(exam, replies))]
    lengths = [len(body.evo.tok(reply, add_special_tokens=False)["input_ids"]) for reply in replies]
    thirds = _thirds([row["ok"] for row in arm.online])
    return {
        "arm": name,
        "online": arm.online,
        "online_rate": sum(row["ok"] for row in arm.online) / len(arm.online),
        "thirds": thirds,
        "exam_rate": sum(exam_ok) / len(exam_ok),
        "exam_by_kind": _by_kind(exam, exam_ok),
        "exam_tokens": sum(lengths) / len(lengths),
        "updates": arm.updates,
        "pool": len(arm.pool),
        "notes": len(arm.notes),
        "seconds": round(time.time() - started, 1),
    }


def _thirds(flags: list[bool]) -> list[float | None]:
    size = max(1, len(flags) // 3)
    parts = [flags[:size], flags[size : 2 * size], flags[2 * size :]]
    return [round(sum(part) / len(part), 3) if part else None for part in parts]


def _by_kind(tasks: list[dict], flags: list[bool]) -> dict:
    out: dict[str, list[bool]] = {}
    for task, ok in zip(tasks, flags):
        out.setdefault(task["kind"], []).append(ok)
    return {kind: sum(values) / len(values) for kind, values in out.items()}


def run_stream(cfg: dict) -> dict:
    from evo.model import release
    from evo.plastic.life import build_body
    from evo.util import repo_path

    if not torch.cuda.is_available():
        return {"status": "no_cuda", "passed": False}
    root = repo_path("tmp") / "use_stream"
    root.mkdir(parents=True, exist_ok=True)
    plan = plan_stream(int(cfg.get("stream_steps", 21)), int(cfg.get("seed", 0)))
    body = build_body(cfg)
    try:
        arms = {}
        for name in cfg.get("stream_arms") or ("frozen", "notes", "evolve"):
            arms[name] = run_arm(name, body, plan, cfg, root)
            print(f"[stream] {name} online={arms[name]['online_rate']:.2f} thirds={arms[name]['thirds']} exam={arms[name]['exam_rate']:.2f}", flush=True)
        evolve = arms.get("evolve", {})
        others = [arms[name]["exam_rate"] for name in arms if name != "evolve"]
        passed = bool(evolve) and all(evolve["exam_rate"] > rate for rate in others)
        return {"status": "passed" if passed else "failed", "passed": passed, "plan": [{"index": r["index"], "kind": f"{r['kind'][0]}{r['kind'][1]}"} for r in plan], "arms": arms}
    finally:
        release(body.evo)
        shutil.rmtree(root, ignore_errors=True)
