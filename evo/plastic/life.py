"""One loaded model learns rules one after another, and keeps the ones it learned.

A check after every few batches scores the new rule and every old rule that
lives in the same adapter, all on the selection inputs. The state kept is the
earliest one with the best new-rule score whose old rules all stay above the
`keep` floor. Samples-to-competence is the number of new-rule examples seen
when that state reached the target. The report inputs are scored only after a
state is chosen.

The model stays loaded across lives. `Body.reset` puts the birth weights back.
"""

from __future__ import annotations

import math
import random
import time

import torch

from evo.plastic.curriculum import Skill, split_inputs
from evo.plastic.fastscore import agreement, exact_rate, graded_rate
from evo.plastic.real_genome import LifeGenes


class Body:
    def __init__(self, evo, cfg: dict):
        from evo.model import adapter_state, ensure_input_grads
        from evo.plastic.grow import Router

        self.evo = evo
        self.cfg = cfg
        ensure_input_grads(evo.model)
        self.birth = adapter_state(evo.model, "policy")
        self.slots: list[str] = []
        self.home: dict[str, str] = {}
        self.router = Router()
        self.serial = 0

    def reset(self, state: dict | None = None) -> None:
        from evo.model import load_adapter_state
        from evo.plastic.grow import Router

        self.evo.model.set_adapter("policy")
        for name in self.slots:
            if name in self.evo.model.peft_config:
                self.evo.model.delete_adapter(name)
        self.slots = []
        self.home = {}
        self.router = Router()
        load_adapter_state(self.evo.model, "policy", state if state is not None else self.birth)

    def adapter_for(self, prompt: str) -> str:
        if not self.slots:
            return "policy"
        skill_id = self.router.route(self.evo, prompt)
        return self.home.get(skill_id or "", "policy")


class Writer:
    """AdamW on one adapter. One parameter group per site, each with its own rate."""

    def __init__(self, evo, adapter: str, site_lrs: dict[str, float], grad_clip: float = 1.0, max_len: int = 256):
        from evo.model import LORA_SITES, adapter_in_name

        self.evo = evo
        self.adapter = adapter
        self.grad_clip = float(grad_clip)
        self.max_len = int(max_len)
        named = list(evo.model.named_parameters())
        groups = []
        self.params = []
        for site, lr in site_lrs.items():
            if lr <= 0:
                continue
            params = [
                param
                for name, param in named
                if adapter_in_name(name, adapter) and any(f".{module}." in name for module in LORA_SITES[site])
            ]
            if params:
                groups.append({"params": params, "lr": float(lr)})
                self.params.extend(params)
        self.ids = {id(param) for param in self.params}
        self.opt = torch.optim.AdamW(groups) if groups else None
        self.sites = [site for site, lr in site_lrs.items() if lr > 0]

    def step(self, pairs: list[tuple[str, str]]) -> float | None:
        from evo.inner_loop import _encode_pair
        from evo.outer_loop import pad_right

        if self.opt is None or not pairs:
            return None
        evo = self.evo
        evo.set_adapter(self.adapter, inference=False)
        for param in evo.model.parameters():
            param.requires_grad = id(param) in self.ids
        evo.model.train()
        evo.model.config.use_cache = False
        rows = [_encode_pair(evo, prompt, completion, self.max_len) for prompt, completion in pairs]
        pad = evo.tok.pad_token_id if evo.tok.pad_token_id is not None else 0
        ids, labels, attn = pad_right(rows, pad, evo.device)
        self.opt.zero_grad(set_to_none=True)
        loss = evo.model(input_ids=ids, attention_mask=attn, labels=labels).loss
        if not torch.isfinite(loss):
            return None
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.params, self.grad_clip)
        self.opt.step()
        self.opt.zero_grad(set_to_none=True)
        return float(loss.detach().item())


class Keeper:
    """`choose_epoch`, one check at a time. Only the pre-skill state and the best state are held."""

    def __init__(self, floor: float):
        self.floor = float(floor)
        self.index = -1
        self.count = 0
        self.rate = -1.0
        self.seen = 0
        self.state = None
        self.first = None
        self.eligible = False

    def offer(self, rate: float, kept: float, seen: int, state_fn) -> bool:
        index = self.count
        self.count += 1
        if index == 0:
            self.first = state_fn()
            self.index, self.rate, self.seen, self.state = 0, rate, seen, self.first
            self.eligible = kept >= self.floor
            return True
        if kept < self.floor:
            return False
        if not self.eligible or rate > self.rate:
            self.index, self.rate, self.seen, self.state = index, rate, seen, state_fn()
            self.eligible = True
            return True
        return False

    def done(self, target: float) -> bool:
        return self.eligible and self.rate >= target


def lesson_inputs(skill: Skill, size: int, seed: int) -> list[int]:
    pool = split_inputs()["train"]
    rng = random.Random(f"{skill.id}:{seed}")
    return sorted(rng.sample(pool, min(int(size), len(pool))))


def replay_pairs(old: list[dict], ratio: float, fresh: int, rng: random.Random) -> list[tuple[str, str]]:
    """Old lessons only. Replay never shows an old rule an input its lesson did not have."""
    if not old or ratio <= 0:
        return []
    count = int(round(ratio * fresh))
    pairs = []
    for index in range(count):
        row = old[index % len(old)]
        value = rng.choice(row["lesson"])
        pairs.append((row["skill"].prompt(value), row["skill"].completion(value)))
    return pairs


def learn(body: Body, skill: Skill, index: int, learned: list[dict], genes: LifeGenes, cfg: dict, adapter: str = "policy", lesson: list[int] | None = None, seen_before: int = 0) -> dict:
    """Train `skill` into `adapter` until the selection set reaches the target, or the example cap."""
    from evo.model import adapter_state, load_adapter_state

    evo = body.evo
    split = split_inputs()
    seed = int(cfg.get("seed", 0))
    rng = random.Random(seed * 7919 + index * 31 + len(adapter))
    lesson = lesson if lesson is not None else lesson_inputs(skill, genes.lesson, seed)
    fresh = [(prompt, completion, True) for prompt, completion in skill.pairs(lesson)]
    watch = [row for row in learned if body.home.get(row["skill"].id) == adapter]
    replay = [(prompt, completion, False) for prompt, completion in replay_pairs(watch, genes.replay, len(fresh), rng)]
    writer = Writer(
        evo,
        adapter,
        {"mlp": genes.lr_at("mlp", index), "attn": genes.lr_at("attn", index)},
        max_len=int(cfg.get("max_seq_len", 256)),
    )
    # Each old rule has its own floor: `keep`, or one question under where it stood before this
    # rule, whichever is lower. A rule that never reached `keep` must not block every later one.
    keeper = Keeper(0.0)
    target = float(cfg.get("life_target", 0.9))
    cap = int(cfg.get("life_cap", 144))
    every = max(1, int(cfg.get("check_every", 1)))
    trace = []
    select_pairs = skill.pairs(split["select"])
    old_pairs = [(row["skill"].id, row["skill"].pairs(split["select"])) for row in watch]
    floors: dict[str, float] = {}
    slack_step = 1.0 / max(1, len(split["select"]))

    def check(seen: int, steps: int, loss) -> None:
        new = exact_rate(evo, select_pairs, adapter)
        olds = {skill_id: exact_rate(evo, pairs, adapter)["rate"] for skill_id, pairs in old_pairs}
        if not floors:
            floors.update({skill_id: min(genes.keep, rate - slack_step) for skill_id, rate in olds.items()})
        slack = min((olds[skill_id] - floors[skill_id] for skill_id in olds), default=1.0)
        kept = min(olds.values()) if olds else 1.0
        took = keeper.offer(new["rate"], slack, seen, lambda: adapter_state(evo.model, adapter))
        trace.append(
            {
                "seen": seen,
                "steps": steps,
                "new": new["rate"],
                "margin": round(new["margin"], 3),
                "kept": kept,
                "olds": olds,
                "took": took,
                "loss": loss,
            }
        )
        worst = min(olds, key=olds.get) if olds else "-"
        print(
            f"[life] {skill.id}@{adapter} seen={seen} new={new['rate']:.2f} kept={kept:.2f}({worst}) "
            f"loss={'-' if loss is None else f'{loss:.3f}'}{' *' if took else ''}",
            flush=True,
        )

    check(0, 0, None)
    seen = 0
    steps = 0
    last_loss = None
    while seen < cap and not keeper.done(target):
        order = fresh + replay
        rng.shuffle(order)
        for start in range(0, len(order), genes.batch):
            batch = order[start : start + genes.batch]
            last_loss = writer.step([(prompt, completion) for prompt, completion, _new in batch])
            steps += 1
            seen += sum(1 for _prompt, _completion, new in batch if new)
            if steps % every == 0:
                check(seen, steps, last_loss)
            if keeper.done(target) or seen >= cap:
                break
        if writer.opt is None:
            break
    if steps % every:
        check(seen, steps, last_loss)
    load_adapter_state(evo.model, adapter, keeper.state)
    reached = keeper.done(target)
    return {
        "skill": skill.id,
        "adapter": adapter,
        "lesson": lesson,
        "reached": reached,
        "samples": (seen_before + keeper.seen) if reached else None,
        "seen": seen_before + seen,
        "steps": steps,
        "replay": len(replay),
        "birth_select": trace[0]["new"],
        "best_select": keeper.rate,
        "kept_check": keeper.index,
        "sites": writer.sites,
        "trace": trace,
        "_pre": keeper.first,
    }


def scored(body: Body, rows: list[dict], which: str = "report") -> dict:
    """One-pass exact rate per learned rule, each prompt sent to the adapter the router picks."""
    split = split_inputs()
    out = {}
    hits_routed = 0
    asked = 0
    for row in rows:
        skill = row["skill"]
        pairs = skill.pairs(split[which])
        groups: dict[str, list[tuple[str, str]]] = {}
        for prompt, completion in pairs:
            adapter = body.adapter_for(prompt)
            groups.setdefault(adapter, []).append((prompt, completion))
            asked += 1
            hits_routed += int(adapter == body.home.get(skill.id, "policy"))
        hits = []
        for adapter, chunk in groups.items():
            hits.extend(exact_rate(body.evo, chunk, adapter)["hits"])
        out[skill.id] = sum(hits) / len(hits) if hits else 0.0
    return {"rates": out, "routing": (hits_routed / asked) if asked else 1.0}


def real_report(body: Body, rows: list[dict], max_new: int = 40) -> dict:
    """Real greedy decoding on the report inputs, graded by `grade_reply`, plus the one-pass agreement."""
    split = split_inputs()
    out = {}
    for row in rows:
        skill = row["skill"]
        prompts = skill.prompts(split["report"])
        answers = skill.answers(split["report"])
        adapters = [body.adapter_for(prompt) for prompt in prompts]
        real_hits = [False] * len(prompts)
        fast_hits = [False] * len(prompts)
        replies = [""] * len(prompts)
        for adapter in sorted(set(adapters)):
            picked = [index for index, name in enumerate(adapters) if name == adapter]
            graded = graded_rate(body.evo, [prompts[i] for i in picked], [answers[i] for i in picked], max_new, adapter)
            fast = exact_rate(body.evo, [skill.pairs([split["report"][i]])[0] for i in picked], adapter)
            for slot, index in enumerate(picked):
                real_hits[index] = graded["hits"][slot]
                fast_hits[index] = fast["hits"][slot]
                replies[index] = graded["replies"][slot]
        lengths = [len(body.evo.tok(reply, add_special_tokens=False)["input_ids"]) for reply in replies]
        out[skill.id] = {
            "real": sum(real_hits) / len(real_hits),
            "fast": sum(fast_hits) / len(fast_hits),
            "agree": agreement(fast_hits, real_hits),
            "tokens": sum(lengths) / len(lengths),
            "sample": replies[0],
        }
    return out


def icl_report(body: Body, rows: list[dict], shots: int = 8, max_new: int = 256) -> dict:
    """The frozen base with the rule's own lesson examples as earlier chat turns. Adapters are off."""
    split = split_inputs()
    out = {}
    for row in rows:
        skill = row["skill"]
        shot_x = list(row["lesson"])[: int(shots)]
        prompts = [skill.shot_messages(n, shot_x) for n in split["report"]]
        graded = graded_rate(body.evo, prompts, skill.answers(split["report"]), max_new, None)
        out[skill.id] = graded["rate"]
        out[f"{skill.id}_sample"] = graded["replies"][0][:300] if graded["replies"] else ""
    return out


def think_report(body: Body, rows: list[dict], max_new: int = 256) -> dict:
    """The frozen base on the plain prompt, with room to derive. Accuracy and reply length."""
    split = split_inputs()
    out = {}
    for row in rows:
        skill = row["skill"]
        graded = graded_rate(body.evo, skill.prompts(split["report"]), skill.answers(split["report"]), max_new, None)
        out[skill.id] = {"real": graded["rate"], "tokens": graded["tokens"]}
    return out


def acceleration(samples: list[int | None]) -> dict:
    """N_first / N_k for every reached rule, and the slope of log N_k over k (negative is faster)."""
    reached = [(index, max(1, int(value))) for index, value in enumerate(samples) if value is not None]
    if not reached:
        return {"ratios": [], "slope": None, "first": None}
    first = reached[0][1]
    ratios = [None if value is None else round(first / max(1, int(value)), 3) for value in samples]
    slope = None
    if len(reached) >= 2:
        xs = [index for index, _value in reached]
        ys = [math.log(value) for _index, value in reached]
        mx = sum(xs) / len(xs)
        my = sum(ys) / len(ys)
        den = sum((x - mx) ** 2 for x in xs)
        slope = None if den == 0 else round(sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / den, 4)
    return {"ratios": ratios, "slope": slope, "first": first}


def live(body: Body, skills: list[Skill], genes: LifeGenes, cfg: dict, primer: Skill | None = None, start: dict | None = None, final: bool = True) -> dict:
    """A whole life. The primer teaches the answer format and is left out of the acceleration numbers."""
    from evo.plastic.grow import grow_first, maybe_grow, maybe_sleep

    started = time.time()
    body.reset(start)
    learned: list[dict] = []
    per_skill = []
    retention = []
    sleeps = []
    order = ([primer] if primer is not None else []) + list(skills)
    for index, skill in enumerate(order):
        is_primer = primer is not None and index == 0
        result = grow_first(body, skill, index, genes, cfg) if genes.grow == "always" and not is_primer else None
        if result is None:
            result = learn(body, skill, index, learned, genes, cfg)
            body.home[skill.id] = "policy"
            if not result["reached"]:
                grown = maybe_grow(body, skill, index, result, genes, cfg)
                if grown is not None:
                    result = grown
        result.pop("_pre", None)
        result["primer"] = is_primer
        body.router.add(body.evo, skill.id, skill.prompts(result["lesson"]))
        learned.append({"skill": skill, "lesson": result["lesson"]})
        per_skill.append(result)
        if genes.sleep_every and (index + 1) % genes.sleep_every == 0:
            slept = maybe_sleep(body, learned, genes, cfg)
            if slept is not None:
                sleeps.append({"after": skill.id, **slept})
        row = scored(body, learned)
        retention.append({"after": skill.id, **row})
        print(f"[life] after {skill.id}: {row['rates']} routing={row['routing']:.2f} slots={len(body.slots)}", flush=True)
    counted = [row["samples"] for row in per_skill if not row["primer"]]
    report = {
        "skills": [skill.id for skill in order],
        "primer": primer.id if primer is not None else None,
        "genes": genes.as_dict(),
        "per_skill": per_skill,
        "retention": retention,
        "sleeps": sleeps,
        "slots": list(body.slots),
        "home": dict(body.home),
        "acceleration": acceleration(counted),
        "learned": sum(1 for row in per_skill if row["reached"]),
    }
    last = retention[-1]["rates"] if retention else {}
    report["final_select"] = scored(body, learned, which="select")["rates"]
    report["final_report_fast"] = last
    if final:
        report["final_real"] = real_report(body, learned, max_new=int(cfg.get("max_new_code", 40)))
    report["seconds"] = round(time.time() - started, 1)
    report["_learned"] = learned
    return report


def fitness(report: dict, cfg: dict) -> float:
    """Faster learning, kept rules, and few slots. Scored on selection inputs only."""
    cap = int(cfg.get("life_cap", 144))
    parts = []
    for row in report["per_skill"]:
        if row.get("primer"):
            continue
        if row["samples"] is not None:
            parts.append(1.0 - math.log(1 + row["samples"]) / math.log(1 + 2 * cap))
        else:
            parts.append(0.0)
    speed = sum(parts) / len(parts) if parts else 0.0
    kept = report["final_select"]
    retain = sum(kept.values()) / len(kept) if kept else 0.0
    return round(speed + retain - 0.05 * len(report["slots"]), 6)


def build_body(cfg: dict) -> Body:
    from evo.model import build_model

    evo = build_model(cfg)
    return Body(evo, cfg)


def run_life(cfg: dict) -> dict:
    """Load once, run the birth test, then one life over the new rules."""
    from evo.model import release
    from evo.plastic.curriculum import by_id, catalog, new_skills, split_skills
    from evo.plastic.real_genome import decode_life, default_vector, with_units

    if not torch.cuda.is_available():
        return {"status": "no_cuda", "passed": False}
    body = build_body(cfg)
    try:
        mode = str(cfg.get("skill_mode", "shown"))
        births = cached_births(body, cfg, mode)
        train, _held = split_skills(catalog(mode))
        fresh = new_skills(train, births, str(cfg.get("birth_rule", "new")))
        wanted = cfg.get("life_skills")
        skills = [by_id(skill_id, mode) for skill_id in wanted] if wanted else fresh[: int(cfg.get("life_n", 4))]
        primer_id = cfg.get("life_primer", "add6")
        primer = by_id(primer_id, mode) if primer_id else None
        skills = [skill for skill in skills if primer is None or skill.id != primer.id]
        genes = decode_life(with_units(default_vector(), **(cfg.get("life_units") or {})))
        print(f"[life] skills={[s.id for s in skills]} primer={primer_id} genes={genes.as_dict()}", flush=True)
        report = live(body, skills, genes, cfg, primer=primer)
        learned = report.pop("_learned")
        report["icl"] = icl_report(body, learned, max_new=int(cfg.get("icl_new", 256)))
        report["think"] = think_report(body, learned, max_new=int(cfg.get("icl_new", 256)))
        report["births"] = births
        report["passed"] = _life_passed(report)
        return report
    finally:
        release(body.evo)


def _life_passed(report: dict) -> bool:
    """Every counted rule reached the target, the last report row keeps all rules at 0.8, and learning beats the prompt."""
    rows = [row for row in report["per_skill"] if not row.get("primer")]
    if not rows or not all(row["reached"] for row in rows):
        return False
    real = report.get("final_real") or {}
    if any(value["real"] < 0.8 for value in real.values()):
        return False
    icl = report.get("icl") or {}
    think = report.get("think") or {}
    beats_prompt = all(real[key]["real"] > icl.get(key, 0.0) for key in real)
    beats_thinking = all(real[key]["real"] >= (think.get(key) or {}).get("real", 0.0) for key in real)
    return beats_prompt and beats_thinking


def cached_births(body: Body, cfg: dict, mode: str) -> list[dict]:
    import json
    from pathlib import Path

    from evo.plastic.curriculum import birth_test, catalog
    from evo.util import repo_path

    model = Path(str(cfg.get("model_name") or "model")).name
    budget = int(cfg.get("birth_new", 256))
    dest = repo_path("runs") / f"evoplast_births_{mode}_{model}_{budget}.json"
    if dest.is_file() and not cfg.get("fresh_births"):
        return json.loads(dest.read_text(encoding="utf-8"))
    rows = birth_test(body.evo, catalog(mode), adapter=None, max_new=budget)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    return rows
