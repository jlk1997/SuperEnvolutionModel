"""One arm, one plan, one morning. The seven schedules stay; dual writes go through WritePolicy."""

from __future__ import annotations

import json
from pathlib import Path

from evo.computer.episode import run_episode
from evo.computer.license import License
from evo.live.absorb import AbsorbBook
from evo.live.episodic import Episode, EpisodicBuffer
from evo.live.identity import Identity
from evo.live.promote import Ledger
from evo.live.relabel import relabel
from evo.live.rhythm import apply_rollback, day_ready, interleave, morning_card, sleep_pressure
from evo.live.sorter import resolve_sort
from evo.session.bus import EventBus
from evo.session.learn import commit_pairs, commit_shadow
from evo.session.policy import write_policy
from evo.session.procedure import LINE, binding_card, hide_procedure, leaks, probe_train_plan, procedure_pairs, rewrite, said_line
from evo.session.trace import trace_text, workspace_files


DUAL = ("dual", "dual_agent")
MARKS = ["csv", "json", "open(", "mkdir", "http"]


def _trained(info: dict) -> dict:
    if not info.get("sites"):
        return {}
    return {"sites": list(info["sites"]), "phase": info.get("phase"), "adapter": info.get("adapter")}


def _site_card() -> dict:
    from evo.session.sites import sites_for

    return {
        "day": sites_for("day", "slot"),
        "night": sites_for("night", "slot"),
        "core": sites_for("day", "core"),
    }


def _pack_fields(name: str) -> list[str]:
    if not name:
        return []
    from evo.office.packs import pack_by_name

    try:
        pack = pack_by_name(name)
    except KeyError:
        return []
    return [str(pack[key]) for key in ("id_field", "amount", "status", "date") if pack.get(key)]


class OrganismSession:
    def __init__(self, arm: str, cfg: dict, evo=None, license: License | None = None, bus: EventBus | None = None):
        self.arm = arm
        self.cfg = cfg
        self.evo = evo
        self.license = license or License()
        self.bus = bus or EventBus()
        self.ledger = Ledger()
        self.book = AbsorbBook()
        self.buffer = EpisodicBuffer()
        self.identity = Identity({"arm": arm})
        self.counts: dict[str, int] = {}
        self.writes: list[dict] = []
        self.rollbacks: list[dict] = []
        self.day_pairs: list[tuple[str, str]] = []
        self.old_pairs: list[tuple[str, str]] = []
        self.absorbed: list[tuple[str, str]] = []
        self.bank: dict[str, str] = {}
        self.safety = 0
        self.exam_items: list[dict] = []
        self.practice_flags: list[bool] = []
        self.needed = int(cfg.get("day_after", 2))
        self.train_cost = int(cfg.get("absorb_train_tokens", 800))
        self.ladder = dict(cfg.get("ladder") or {})
        self.ladder.setdefault("cross_holds", 1)
        self.marks = list(cfg.get("generic_marks") or MARKS)
        self.last_sort: dict[str, str] = {}
        self.night_local = False
        self.home_pack: dict[str, str] = {}
        self.bindings: dict[str, dict] = {}
        self.demonstrations: list[dict] = []
        self.card: dict | None = None
        self.pressure: str | None = None
        self._family = ""
        self._task = ""

    def step(self, task: dict, plan_step: dict, reply, workspace: Path) -> dict:
        family = str(task.get("family") or plan_step.get("family") or "")
        self._family = family
        self._task = str(task.get("id") or "")
        self.bus.emit(
            "task_start",
            {
                "arm": self.arm,
                "task": self._task,
                "family": family,
                "split": task.get("split"),
                "index": plan_step.get("index"),
                "kind": plan_step.get("kind"),
                "drift": bool(plan_step.get("drift")),
                "prompt": (task.get("prompt") or "")[:2000],
            },
        )
        result = run_episode(task, reply, workspace, self.license, on_event=self._on_body)
        self.bus.emit(
            "check",
            {
                "arm": self.arm,
                "task": self._task,
                "family": family,
                "split": task.get("split"),
                "ok": bool(result["ok"]),
                "finished": bool(result["finished"]),
                "steps": result["steps"],
            "files": workspace_files(workspace),
        },
        )
        self._maybe_relabel(task, workspace, bool(result["ok"]))
        traced = trace_text(result)
        index = int(plan_step.get("index") or 0)
        self.buffer.add(Episode(task.get("prompt") or "", traced, result["ok"], [family], index, task.get("split") or "practice"))
        if task.get("split") == "exam":
            self.exam_items.append({"id": task.get("id"), "ok": result["ok"], "family": family, "steps": result["steps"]})
            self.ledger.note_exam([family], bool(result["ok"]))
        else:
            self.practice_flags.append(bool(result["ok"]))
            self.ledger.note_practice([family], bool(result["ok"]))
        self.safety += sum(1 for row in result["trace"] if "unsafe" in (row.get("refused") or []))
        practice_ok = bool(result["ok"]) and task.get("split") != "exam"
        if practice_ok:
            self.counts[family] = self.counts.get(family, 0) + 1
            self.day_pairs.append((task.get("prompt") or "", traced))
            self.bank[family] = traced
            notes_len = int(task.get("_notes_len") or 0)
            self.book.note(family, max(40, notes_len), self.train_cost)
            self.identity.remember(task.get("prompt") or "", traced, [family], "practice")
            self._note_cross_pack(family, str(task.get("pack") or ""))
        ready = practice_ok and day_ready(self.counts, family, self.needed)
        self.bus.emit("ledger", self._ledger_event(family))
        if practice_ok:
            decision = self.book.decision(family)
            self.bus.emit(
                "absorb",
                {
                    "arm": self.arm,
                    "triggered": ready and self.arm in DUAL,
                    **decision,
                },
            )
        if self.arm in DUAL and ready:
            self._dual_write(task, family, traced)
        elif self.evo is not None and self.arm in ("continual", "continual_sft") and practice_ok:
            role_batch, _card = self._roles([(task.get("prompt") or "", traced)], task)
            trained = commit_pairs(self.evo, role_batch, self.cfg, "slot", phase="day")
            self.bus.emit(
                "write",
                {
                    "arm": self.arm,
                    "name": family,
                    "dest": "slot",
                    "write": True,
                    "why": "practice",
                    "policy": "schedule",
                    "counted": False,
                    **_trained(trained),
                },
            )
        ticks = int(self.cfg.get("day_ticks", 4))
        if self.arm == "shift" and ticks > 0 and index % ticks == ticks - 1:
            role_batch, _card = self._roles(list(self.day_pairs), task)
            trained = commit_pairs(self.evo, role_batch, self.cfg, "slot", phase="night")
            row = {"name": "shift", "dest": "slot", "why": "night batch", **_trained(trained)}
            self.writes.append(row)
            self.bus.emit(
                "write",
                {
                    "arm": self.arm,
                    "name": "shift",
                    "dest": "slot",
                    "write": True,
                    "why": "night batch",
                    "policy": "schedule",
                    "counted": True,
                    **_trained(trained),
                },
            )
            self.old_pairs = interleave(self.day_pairs, self.old_pairs)
            self.day_pairs = []
        return result

    def finish(self, plan: list[dict]) -> dict:
        self.pressure = sleep_pressure(
            {
                "day_steps": len(self.day_pairs),
                "day_budget": int(self.cfg.get("day_budget", 8)),
                "drift": any(step.get("drift") for step in plan),
                "shift_end": True,
            }
        )
        self.bus.emit(
            "sleep",
            {"arm": self.arm, "pressure": self.pressure, "day_steps": len(self.day_pairs)},
        )
        if self.arm in DUAL and self.pressure:
            if self.absorbed:
                trained = commit_pairs(self.evo, interleave(self.absorbed, self.old_pairs), self.cfg, "local" if self.night_local else "slot", phase="night")
                dest = "local" if self.night_local else "slot"
                row = {"name": "night", "dest": dest, "why": self.pressure, "pairs": len(self.absorbed), **_trained(trained)}
            else:
                row = {"name": "night", "dest": "retrieval", "why": self.pressure}
            self.writes.append(row)
            self.bus.emit("write", {"arm": self.arm, "policy": "night", "write": row["dest"] == "slot", "counted": True, **row})
        self.card = morning_card(self.writes, self.rollbacks)
        self.bus.emit("morning", {"arm": self.arm, **self.card})
        return self.card

    def rollback(self, name: str) -> dict:
        found = any(row.get("name") == name for row in self.writes)
        self.writes = apply_rollback(self.writes, name)
        self.rollbacks.append({"name": name, "why": "human"})
        self.card = morning_card(self.writes, self.rollbacks)
        self.bus.emit("morning", {"arm": self.arm, "rollback": name, "found": found, **self.card})
        return self.card

    def organism(self) -> dict:
        names = set(self.book.seen) | set(self.ledger.verified) | set(self.counts) | set(self.last_sort)
        families = {}
        for name in sorted(names):
            decision = self.book.decision(name) if name in self.book.seen else None
            families[name] = {
                "verified": int(self.ledger.verified.get(name, 0)),
                "holds": int(self.ledger.holds.get(name, 0)),
                "in_slot": name in self.ledger.in_slot,
                "ledger": self.ledger.destination([name], self.ladder or None),
                "absorb": decision,
                "sorter": self.last_sort.get(name),
                "day_count": int(self.counts.get(name, 0)),
            }
        self.identity.take(self.ledger)
        return {
            "arm": self.arm,
            "license": {
                "grants": sorted(self.license.grants),
                "mode": self.license.mode,
                "max_steps": self.license.max_steps,
                "hosts": sorted(self.license.hosts),
            },
            "families": families,
            "writes": [dict(row) for row in self.writes],
            "rollbacks": [dict(row) for row in self.rollbacks],
            "morning": self.card,
            "pressure": self.pressure,
            "identity": self.identity.pack(),
            "demonstrations": list(self.demonstrations),
            "bindings": {name: dict(card) for name, card in self.bindings.items()},
            "safety_fails": self.safety,
            "sites": _site_card(),
            "note": "闸门 2 以 docs/ROADMAP.md 当时的判定为准。这里是封装之后的过程记录，不是重新判卷。",
        }

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.organism(), ensure_ascii=False, indent=2), encoding="utf-8")

    def _dual_write(self, task: dict, family: str, traced: str) -> None:
        del traced
        raw_batch = list(self.day_pairs[-self.needed :])
        role_batch, card = self._roles(raw_batch, task)
        pack_name = str(card.get("pack") or task.get("pack") or "")
        if pack_name:
            self.bindings[pack_name] = card
        secret = str(task.get("secret") or "")
        program = "\n".join(code for _prompt, code in role_batch)
        blob = "\n".join(part for pair in role_batch for part in pair)
        need = int(self.ladder.get("cross_holds") or 0)
        cross_met = need <= 0 or int(self.ledger.cross.get(family, 0)) >= need
        marks = list(self.marks)
        if role_batch and all(code.strip() == LINE for _prompt, code in role_batch):
            marks = marks + ["sum "]
        sorter = resolve_sort(program, "", marks, [], cross_met)
        self.last_sort[family] = sorter
        ledger_dest = self.ledger.destination([family], self.ladder or None)
        decision = self.book.decision(family)
        choice = write_policy(ledger_dest, bool(decision["absorb"]), sorter)
        if not decision["measured"] and not choice["write"] and choice["why"] == "still cheaper to reread":
            trial = write_policy(ledger_dest, True, sorter)
            choice = {**trial, "why": "shadow trial", "trial": True} if trial["write"] else trial
        policy_dest = choice["dest"]
        policy_why = choice["why"]
        trained = {"sites": [], "phase": "day", "adapter": "policy", "kept": False}
        kept = False
        distilled = bool(role_batch) and all(code.strip() for _prompt, code in role_batch)
        leaked = leaks(blob, card, secret)
        if choice["write"] and not distilled:
            choice = {**choice, "dest": "drop", "write": False, "why": "procedure is still a long script"}
        elif leaked:
            choice = {**choice, "dest": "drop", "write": False, "why": "procedure still has a column name"}
        elif choice["write"]:
            plan = probe_train_plan() if program.strip() == LINE else None
            trained = commit_shadow(
                self.evo,
                role_batch,
                self.cfg,
                choice["dest"],
                "day",
                "memory" if choice["dest"] == "core" else "policy",
                lambda adapter: self._bare(task, card, adapter),
                train=self._shadow_train(role_batch),
                sites=None if plan is None else list(plan["sites"]),
                epochs=1 if plan is None else int(plan["steps"]),
            )
            kept = bool(trained.get("kept"))
            if kept:
                self.absorbed.extend(role_batch)
                if choice["dest"] in ("slot", "local", "core"):
                    self.ledger.mark_slot([family])
                if choice["dest"] == "local":
                    self.night_local = True
                self.book.measure(family, float(len(role_batch[-1][1]) if role_batch else 0))
            else:
                choice = {**choice, "dest": "retrieval", "write": False, "why": trained.get("why") or "ablation missed"}
        row = {
            "name": family,
            "dest": choice["dest"],
            "why": choice["why"],
            "kept": kept,
            "procedure": program,
            "policy_dest": policy_dest,
            "policy_why": policy_why,
            **_trained(trained),
        }
        self.writes.append(row)
        self.bus.emit(
            "write",
            {
                "arm": self.arm,
                "name": family,
                "policy": "write_policy",
                "counted": True,
                "kept": kept,
                "procedure": program,
                "policy_dest": policy_dest,
                "policy_why": policy_why,
                **choice,
                **_trained(trained),
            },
        )
        self.counts[family] = 0

    def _roles(self, pairs: list[tuple[str, str]], task: dict) -> tuple[list[tuple[str, str]], dict]:
        pack = self._pack_dict(task)
        return procedure_pairs(pairs, pack, str(task.get("secret") or ""))

    def _pack_dict(self, task: dict) -> dict:
        name = str(task.get("pack") or "")
        if not name:
            return {}
        from evo.office.packs import pack_by_name

        try:
            return pack_by_name(name)
        except KeyError:
            return {"name": name}

    def _shadow_train(self, pairs: list[tuple[str, str]]):
        hook = self.cfg.get("shadow_train")
        if not callable(hook):
            return None

        def train(adapter: str) -> dict:
            return hook(adapter, pairs) or {}

        return train

    def _bare(self, task: dict, card: dict, adapter: str) -> bool:
        """One practice item, notes removed. A scripted reference reply does not count."""
        hook = self.cfg.get("ablation")
        if callable(hook):
            return bool(hook(adapter, card))
        if self.evo is None or self.cfg.get("actor") != "model":
            return False
        from evo.office.families import make_task

        pack = self._pack_dict(task)
        if not pack.get("name"):
            return False
        fresh = make_task(
            pack,
            str(task.get("family") or "table"),
            int(self.cfg.get("seed", 0)) + 10007,
            variant=int(task.get("variant") or 0),
            difficulty=int(self.cfg.get("difficulty", 1)),
        )
        fresh["split"] = "practice"
        calls = fresh.get("calls") or []
        sample = "\n".join(str((call.arguments or {}).get("code") or "") for call in calls)
        fresh_card = binding_card(pack, sample)
        fresh["prompt"] = hide_procedure(rewrite(fresh.get("prompt") or "", fresh_card, str(fresh.get("secret") or "")))
        from evo.office.stream import _model_reply
        from evo.session.procedure import expand
        from evo.computer.actions import format_call

        raw_reply = _model_reply(self.evo, self.cfg, adapter)
        source = str(fresh_card.get("source") or "")

        def reply(messages):
            text = raw_reply(messages)
            if said_line(text):
                code = expand(text, fresh_card, source)
                if code:
                    return format_call("python", {"code": code})
            return format_call("finish", {"answer": "missing procedure"})

        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as folder:
            result = run_episode(fresh, reply, Path(folder), self.license)
        return bool(result["ok"])

    def _maybe_relabel(self, task: dict, workspace: Path, ok: bool) -> None:
        """A miss that landed on the other legal total is kept as that total, not as a success."""
        if ok or task.get("split") == "exam":
            return
        if task.get("expected") is None or task.get("expected_all") is None:
            return
        from evo.office.families import produced_total

        produced = produced_total(workspace)
        if produced is None:
            return
        other = relabel(produced, "paid", [("paid", float(task["expected"])), ("all", float(task["expected_all"]))])
        if not other:
            return
        self.demonstrations.append(
            {
                "asked": "paid",
                "other": other,
                "produced": produced,
                "family": task.get("family"),
                "kept": False,
            }
        )
        self.bus.emit(
            "relabel",
            {
                "arm": self.arm,
                "task": task.get("id"),
                "family": task.get("family"),
                "asked": "paid",
                "other": other,
                "produced": produced,
                "kept": False,
            },
        )

    def offer(self, family: str) -> dict:
        from evo.live.share import offer_skill

        text = self.bank.get(family) or ""
        dest = self.last_sort.get(family) or "local"
        fields = _pack_fields(self.home_pack.get(family, ""))
        replacements = {field: "{field}" for field in fields}
        canaries = [piece for piece in text.split() if piece.startswith("CANARY-")]
        result = offer_skill(text, dest, replacements, canaries)
        self.bus.emit("share", {"arm": self.arm, "family": family, "ok": result["ok"], "why": result["why"], "dest": result["dest"]})
        return result

    def carry(self, payload: dict) -> dict:
        from evo.live.identity import carry_card, load_identity

        card = carry_card(payload)
        ident = load_identity(payload)
        self.identity = ident
        self.ledger.verified = dict(ident.verified)
        self.ledger.holds = dict(ident.holds)
        self.ledger.in_slot = set(ident.in_slot)
        self.bus.emit("carry", {"arm": self.arm, **card})
        return card

    def _note_cross_pack(self, family: str, pack: str) -> None:
        if not pack:
            return
        home = self.home_pack.get(family)
        if home is None:
            self.home_pack[family] = pack
            return
        if home != pack:
            self.ledger.note_cross([family], True)

    def _ledger_event(self, family: str) -> dict:
        return {
            "arm": self.arm,
            "family": family,
            "destination": self.ledger.destination([family], self.ladder or None) if family else "fast",
            "verified": int(self.ledger.verified.get(family, 0)),
            "holds": int(self.ledger.holds.get(family, 0)),
            "in_slot": family in self.ledger.in_slot,
            "day_count": int(self.counts.get(family, 0)),
        }

    def _on_body(self, kind: str, payload: dict) -> None:
        self.bus.emit(kind, {"arm": self.arm, "task": self._task, "family": self._family, **payload})
