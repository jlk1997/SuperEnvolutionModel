"""One office stream shared by every arm. Reference actors test the loop; the model is optional."""

from __future__ import annotations

import random

from evo.computer.actions import OFFICE_TOOLS, format_call
from evo.computer.episode import scripted_reply
from evo.computer.license import License
from evo.office.families import FAMILIES, make_task
from evo.office.judge import REQUIRED_ARMS, judge_office
from evo.office.packs import DEV_PACKS


ARMS = ("agent", "oracle", "shift", "continual", "dual", "dual_agent", "continual_sft")


def zipf_plan(n: int, families: list[str], seed: int, drift_at: int | None, revisit_every: int) -> list[dict]:
    rng = random.Random(seed)
    weights = [1.0 / ((index + 1) ** 1.1) for index in range(len(families))]
    rows = []
    for index in range(int(n)):
        if rows and revisit_every and index % int(revisit_every) == 0:
            family = rows[0]["family"]
            kind = "revisit"
        else:
            family = _pick(families, weights, rng)
            kind = "draw"
        rows.append(
            {
                "index": index,
                "family": family,
                "kind": kind,
                "variant": index % 3,
                "drift": drift_at is not None and index == int(drift_at),
                "exam": index % 2 == 1,
            }
        )
    return rows


def run_office(cfg: dict, evo=None) -> dict:
    """Run every arm on the same plan. `evo` is only used when actor is model."""
    from evo.runlog import Run
    from evo.util import set_seed

    seeds = [int(seed) for seed in (cfg.get("seeds") or [cfg.get("seed", 0)])]
    reports = []
    for seed in seeds:
        set_seed(seed)
        report = _one_seed(dict(cfg), seed, evo)
        if cfg.get("required_arms"):
            report["required_arms"] = list(cfg.get("required_arms"))
        run = Run(cfg.get("runs_root", "runs"), f"{cfg.get('run_name', 'office')}_s{seed}", cfg)
        run.save_json("summary.json", report)
        reports.append(report)
    judged = judge_office(reports, required_arms=cfg.get("required_arms"))
    # Full Gate2 slate only: never mint gate2_claim when arms were narrowed.
    if cfg.get("required_arms") and list(cfg.get("required_arms")) != list(REQUIRED_ARMS):
        judged["gate2_claim"] = False
        if judged.get("pass"):
            judged["pass"] = False
            judged["branch"] = (
                "Narrowed required_arms smoke: checks can go green for CI/forget, "
                "but NOT Gate2 until full REQUIRED_ARMS slate."
            )
    elif (
        judged.get("pass")
        and str(cfg.get("reference_gate") or "") != "notes_open_book"
        and not judged.get("proxy")
    ):
        # Full REQUIRED_ARMS + judge.pass + not open-book proxy → legitimate Gate2 claim.
        judged["gate2_claim"] = True
    judged["power"] = _power_note(judged)
    # Reference open-book is a dissolution *proxy*; never mint a Gate2 LM claim from it.
    if str(cfg.get("reference_gate") or "") == "notes_open_book":
        judged["proxy"] = "notes_open_book"
        judged["proxy_beat_agent"] = bool((judged.get("checks") or {}).get("beat_agent"))
        judged["gate2_claim"] = False
        if judged.get("pass"):
            judged["pass"] = False
            judged["branch"] = (
                "Open-book reference proxy: dual beat retrieval-agent. "
                "NOT Gate2. Next: actor=model signal smoke / mid-n."
            )
    if cfg.get("write_gate"):
        _write_gate(judged, reports)
    return {"reports": reports, "judge": judged}


def _power_note(judged: dict) -> dict:
    from evo.stats import power_paired

    n = int((judged.get("ci") or {}).get("n") or 0)
    if n <= 0:
        return {"n": 0, "power": None, "required_n": 800}
    row = power_paired(0.55, 0.45, n, alpha_boots=40, sims=40, seed=n)
    return {"n": n, "power": row["power"], "required_n": 800}


def _one_seed(cfg: dict, seed: int, evo) -> dict:
    families = list(cfg.get("families") or FAMILIES)
    plan = zipf_plan(
        int(cfg.get("steps", 6)),
        families,
        seed,
        cfg.get("drift_at"),
        int(cfg.get("revisit_every", 4)),
    )
    arms = list(cfg.get("arms") or ARMS)
    pack = _pack(cfg, seed)
    rows = []
    for arm in arms:
        rows.append(_arm(arm, plan, pack, cfg, seed, evo))
    return {"seed": seed, "arms": rows, "plan": [{key: row[key] for key in ("index", "family", "kind", "drift", "exam")} for row in plan]}


def _arm(arm: str, plan: list[dict], pack: dict, cfg: dict, seed: int, evo) -> dict:
    """Same seven schedules. Dual writes go through the session's three gates, and every step is an event."""
    from evo.session.organism import OrganismSession

    session = OrganismSession(arm, cfg, evo, license=_license(cfg), bus=_bus(cfg, arm, seed))
    for step in plan:
        drift = "paginate" if step["drift"] else None
        family = step["family"] if step["family"] in FAMILIES else "table"
        variant = 0 if family in ("shell", "http", "mixed") else int(step["variant"])
        task = make_task(pack, family, seed + step["index"], variant=variant, difficulty=int(cfg.get("difficulty", 1)), drift=drift)
        task["split"] = "exam" if step["exam"] else "practice"
        task["_arm"] = arm
        notes = _notes(arm, task, session.bank, cfg)
        task["_notes_len"] = len(notes)
        if notes:
            task["prompt"] = task["prompt"] + "\n\n" + notes
        reply = _reply(arm, task, cfg, evo)
        if cfg.get("actor") == "model" and bool(cfg.get("practice_bootstrap", False)):
            reply = _bootstrap_reply(reply, arm, task, cfg, evo)
        # F3f: before exam items, reinforce day_pairs once more (dual/continual only)
        if (
            cfg.get("actor") == "model"
            and bool(cfg.get("exam_prep_sft", True))
            and task.get("split") == "exam"
            and arm in ("dual", "continual", "continual_sft")
            and getattr(session, "day_pairs", None)
            and not task.get("_exam_prepped")
        ):
            try:
                from evo.session.learn import commit_pairs
                epochs = int(cfg.get("exam_prep_sft_epochs", 2))
                commit_pairs(evo, list(session.day_pairs), cfg, "slot", phase="day", epochs=epochs)
                task["_exam_prepped"] = True
            except Exception as exc:
                task["_exam_prep_error"] = str(exc)[:160]
        workspace = _workspace(cfg, arm, step["index"])
        try:
            result = session.step(task, step, reply, workspace)
        finally:
            if not cfg.get("_workspace_root"):
                import shutil

                shutil.rmtree(workspace, ignore_errors=True)
        if cfg.get("actor") == "model":
            route_bit = ""
            if task.get("_route_generate"):
                route_bit = f" route={task['_route_generate'].get('atom')}"
            elif task.get("_route"):
                route_bit = f" notes_route={task['_route'].get('mode')}:{task['_route'].get('atom')}"
            elif task.get("_route_generate_error"):
                route_bit = f" route_err={task['_route_generate_error'][:60]}"
            print(
                f"[office] seed={seed} arm={arm} step={step['index']} ok={result['ok']}{route_bit}",
                flush=True,
            )
    session.finish(plan)
    organism_path = cfg.get("organism_path")
    if organism_path:
        from pathlib import Path

        session.save(Path(organism_path))
    exam_items = session.exam_items
    ok_flags = [item["ok"] for item in exam_items]
    use_log_path = None
    try:
        from evo.office.use_log import dump_arm_use_log

        use_log_path = dump_arm_use_log(session, cfg, arm=arm, seed=seed)
        if use_log_path is not None:
            print(f"[office] use_log arm={arm} path={use_log_path}", flush=True)
    except Exception as exc:
        print(f"[office] use_log skip arm={arm}: {exc}", flush=True)
    return {
        "arm": arm,
        "exam_items": exam_items,
        "practice_ok": session.practice_flags,
        "writes": len(session.writes),
        "safety_fails": session.safety,
        "exam_leak": any(row.split == "exam" for row in session.buffer.rows),
        "retain_drop": _retain_drop(exam_items),
        "tokens_per_ok": _tokens(exam_items, cfg),
        "train_tokens": len(session.day_pairs) * int(cfg.get("train_tokens_each", 0)),
        "morning": session.card["text"] if session.card else "",
        "morning_card": session.card,
        "ok_rate": (sum(ok_flags) / len(ok_flags)) if ok_flags else None,
        "use_log": str(use_log_path) if use_log_path else None,
    }


def _bus(cfg: dict, arm: str, seed: int):
    from pathlib import Path

    from evo.session.bus import EventBus

    raw = cfg.get("events_path")
    if not raw:
        return EventBus()
    path = Path(raw)
    if path.suffix != ".jsonl":
        path.mkdir(parents=True, exist_ok=True)
        path = path / f"{arm}-s{seed}.jsonl"
    return EventBus(path)


def _learn(evo, arm: str, pairs: list[tuple[str, str]], cfg: dict, dest: str) -> None:
    """Reference runs pass evo=None and only record the decision."""
    from evo.session.learn import commit_pairs

    del arm
    commit_pairs(evo, pairs, cfg, dest)


def _skill_candidates(task: dict, cfg: dict | None) -> list[str]:
    """Family name, optional family_skill_map, never global add/offset (would strip all office notes)."""
    cfg = cfg or {}
    family = str(task.get("family") or "")
    out: list[str] = []
    mapping = cfg.get("family_skill_map") or {}
    if family and family in mapping:
        mapped = mapping[family]
        if isinstance(mapped, (list, tuple)):
            out.extend(str(x) for x in mapped)
        else:
            out.append(str(mapped))
    if task.get("skill"):
        out.append(str(task["skill"]))
    if family:
        out.append(family)
    # de-dupe preserve order
    seen = set()
    uniq = []
    for s in out:
        if s and s not in seen:
            seen.add(s)
            uniq.append(s)
    return uniq




def _agent_demo_notes(family: str) -> str:
    """Weak open-book format demos for agent (no task secrets, no atom weights)."""
    demos = {
        "table": (
            "Format demo (adapt to this job):\n"
            "<tool_call>\n<function=python>\n<parameter=code>\n"
            "import csv\n"
            "# read a csv, filter rows, write an output csv\n"
            "</parameter>\n</function>\n</tool_call>"
        ),
        "report": (
            "Format demo (adapt to this job):\n"
            "<tool_call>\n<function=python>\n<parameter=code>\n"
            "import json\n"
            "# load json, write a markdown report starting with '# Summary'\n"
            "</parameter>\n</function>\n</tool_call>"
        ),
        "file": (
            "Format demo (adapt to this job):\n"
            "<tool_call>\n<function=python>\n<parameter=code>\n"
            "from pathlib import Path\n"
            "# move matching files between folders with Path.replace\n"
            "</parameter>\n</function>\n</tool_call>"
        ),
        "shell": (
            "Format demo (adapt to this job):\n"
            "<tool_call>\n<function=shell>\n<parameter=cmd>\nmkdir out\n</parameter>\n"
            "</function>\n</tool_call>"
        ),
    }
    return demos.get(str(family or ""), demos["table"])


def _prefer_atoms_for(cfg: dict | None, arm: str | None = None) -> bool:
    """Global prefer_atoms, overridable per arm (B-X6 contrast: dual on, agent off)."""
    cfg = cfg or {}
    by = cfg.get("prefer_atoms_by_arm") or {}
    if arm and arm in by:
        return bool(by[arm])
    return bool(cfg.get("prefer_atoms", True))


def _notes(arm: str, task: dict, bank: dict | None = None, cfg: dict | None = None) -> str:
    """A short hint. Prefer crystallized atoms over bank/scaffold notes when internalized."""
    if arm == "oracle":
        shown = "\n".join(format_call(call.name, call.arguments) for call in task.get("calls") or [])
        raw = "Do this:\n" + shown[:700]
    elif arm in ("agent", "dual_agent"):
        lines = ["Reply with one <tool_call> block. Prefer python for CSV/JSON/files; shell only if asked."]
        if bool((cfg or {}).get("agent_demo_notes", True)):
            lines.append(_agent_demo_notes(str(task.get("family") or "")))
        prior = ((bank or {}).get(task.get("family") or "") or "").strip()
        if prior:
            lines.append("A previous success on this kind of job:\n" + prior[:400])
        raw = "\n".join(lines)
    else:
        raw = ""

    prefer = _prefer_atoms_for(cfg, arm)
    if prefer:
        from evo.crystal.router import route
        for skill in _skill_candidates(task, cfg):
            decision = route(skill, notes=raw or None, prefer_atom=True)
            if decision.get("mode") == "atom" and not decision.get("use_notes"):
                task["_route"] = {
                    "mode": decision["mode"],
                    "skill": skill,
                    "atom": decision.get("atom"),
                    "use_notes": False,
                    "reason": decision.get("reason"),
                }
                # Dual/continual already have empty notes; agent notes get stripped.
                return ""
    if raw:
        task["_route"] = {"mode": "scaffold", "use_notes": True}
    return raw


def _notes_open_book_ok(task: dict) -> bool:
    """True when retrieval notes carry a *prior success trace*, not the generic tool hint.

    Agent instructions mention <tool_call> as a format reminder; that must not count.
    """
    blob = str(task.get("prompt") or "")
    # Bank prior block written by dual/agent absorption.
    if "A previous success on this kind of job:" in blob:
        prior = blob.split("A previous success on this kind of job:", 1)[-1]
        if len(prior.strip()) >= 40:
            return True
    # Explicit prior tool execution (function=...) beyond the boilerplate hint line.
    if "A previous success" not in blob and "<function=" in blob:
        # Count function tags; boilerplate finish hints are rare without prior.
        if blob.count("<function=") >= 1 and "need retrieval" not in blob:
            # Still too easy to spoof 鈥?require parameter payload
            if "<parameter=" in blob:
                return True
    return False



def _bootstrap_reply(inner, arm: str, task: dict, cfg: dict, evo=None):
    """F3c/F3f: practice gold scripted calls + optional immediate SFT on XML tool traces.

    Exam stays pure model (no bootstrap) so Gate2 stays honest.

    Also fires when the model emits parseable shell cmds that license would refuse
    (e.g. cp/&&//path/to) — otherwise shell practice never yields ok use_log pairs.
    """
    from evo.computer.actions import parse_calls, format_call
    from evo.computer.episode import scripted_reply
    from evo.computer.license import License
    from pathlib import Path

    log_path = Path(cfg.get("model_turn_log") or "runs/logs/office_model_turns.log")
    probe = License(grants=set(cfg.get("grants") or ["python", "shell", "read", "write", "http"]))
    scripted = {"fn": None}
    sft_done = {"ok": False}

    def _all_refused(parsed) -> bool:
        if not parsed:
            return False
        return all(bool(probe.decide(call, task.get("family"))) for call in parsed)

    def _should_bootstrap(parsed) -> bool:
        if task.get("split") != "practice" or not task.get("calls"):
            return False
        allowed = cfg.get("bootstrap_arms") or ("dual", "continual", "continual_sft", "shift")
        if arm not in set(allowed):
            return False
        if not parsed:
            return True
        return _all_refused(parsed)

    def reply(messages):
        text = inner(messages) or ""
        parsed = parse_calls(text)
        if not parsed:
            try:
                log_path.parent.mkdir(parents=True, exist_ok=True)
                with log_path.open("a", encoding="utf-8") as fh:
                    fh.write(f"arm={arm} split={task.get('split')} family={task.get('family')}\n{text[:1500]}\n---\n")
            except Exception:
                pass
        if _should_bootstrap(parsed):
            if scripted["fn"] is None:
                scripted["fn"] = scripted_reply(task.get("calls") or [])
            gold = scripted["fn"](messages)
            task["_bootstrapped"] = True
            if (
                evo is not None
                and bool(cfg.get("bootstrap_sft_immediate", True))
                and not sft_done["ok"]
            ):
                try:
                    from evo.session.learn import commit_pairs
                    calls = task.get("calls") or []
                    parts = []
                    for call in calls:
                        if hasattr(call, "name"):
                            parts.append(format_call(call.name, dict(getattr(call, "arguments", {}) or {})))
                        elif isinstance(call, dict):
                            parts.append(format_call(str(call.get("name") or "finish"), dict(call.get("arguments") or {})))
                    gold_xml = "\n".join(parts) if parts else gold
                    prompt = ""
                    for msg in reversed(messages):
                        if msg.get("role") == "user":
                            prompt = str(msg.get("content") or "")
                            break
                    if prompt and gold_xml.strip():
                        epochs = int(cfg.get("bootstrap_sft_epochs", 2))
                        commit_pairs(evo, [(prompt, gold_xml)], cfg, "slot", phase="day", epochs=epochs)
                        task["_bootstrap_sft"] = True
                        sft_done["ok"] = True
                except Exception as exc:
                    task["_bootstrap_sft_error"] = str(exc)[:160]
            return gold
        return text

    return reply


def _reply(arm: str, task: dict, cfg: dict, evo):
    actor = cfg.get("actor", "reference")
    if actor == "noop":
        return lambda _messages: format_call("finish", {"answer": "skip"})
    if actor == "model" and evo is not None:
        return _model_reply(evo, cfg, task)
    # reference_gate=notes_open_book: agent-like arms must retrieve calls; dual/continual
    # keep full scripted skill as a stand-in for internalized weights (dissolution proxy).
    if (
        str(cfg.get("reference_gate") or "") == "notes_open_book"
        and arm in ("agent", "dual_agent")
        and not _notes_open_book_ok(task)
    ):
        return lambda _messages: format_call("finish", {"answer": "need retrieval notes"})
    return scripted_reply(task.get("calls") or [])


TOOL_CALL_PRIMER = """You are an office agent. Output ONLY one XML tool call per turn. No prose before or after.

COPY THIS SHAPE EXACTLY (names use = not >). Prefer python for CSV/JSON/file jobs:

<tool_call>
<function=python>
<parameter=code>
print("ok")
</parameter>
</function>
</tool_call>

Shell only when asked (allowlist: mkdir, dir, type, copy; cp→copy). Relative paths only. No && or /path/to.

When finished:
<tool_call>
<function=finish>
<parameter=answer>
done
</parameter>
</function>
</tool_call>

Allowed: python, shell, read_file, write_file, list_dir, http, finish.
Never invent <function>shell</function> — always <function=shell>.
"""


def _model_reply(evo, cfg: dict, task: dict | None = None):
    """Generate with policy, or an internalized capability atom adapter when routed."""
    from evo.generate import generate_messages

    adapter = "policy"
    route_info = None
    arm = (task or {}).get("_arm") if task is not None else None
    if task is not None and _prefer_atoms_for(cfg, arm):
        try:
            from evo.crystal.router import route
            from evo.model import add_named_adapter
            from peft import set_peft_model_state_dict
            from safetensors.torch import load_file
            from pathlib import Path

            for skill in _skill_candidates(task, cfg):
                decision = route(skill, notes=None, prefer_atom=True)
                if decision.get("mode") != "atom":
                    continue
                atom_dir = Path(str(decision.get("adapter_dir") or ""))
                # Prefer skill2 for offset-like atoms; else policy/
                weight = atom_dir / "skill2" / "adapter_model.safetensors"
                name = "atom_skill2"
                if not weight.is_file():
                    weight = atom_dir / "policy" / "adapter_model.safetensors"
                    name = "atom_policy"
                if not weight.is_file():
                    continue
                try:
                    add_named_adapter(evo, name)
                except Exception:
                    pass
                # Atoms are saved under training adapter name (policy/skill2). Loading those
                # tensors into atom_policy without retarget is a silent no-op — exam then
                # runs the base/policy LoRA and stays at 0 (C6 "atom" logs were cosmetic).
                raw = load_file(str(weight))
                src = "skill2" if name == "atom_skill2" else "policy"
                loaded = {k.replace(f".{src}.", f".{name}."): v for k, v in raw.items()}
                set_peft_model_state_dict(evo.model, loaded, adapter_name=name)
                adapter = name
                route_info = {"atom": decision.get("atom"), "adapter": name, "skill": skill}
                if task is not None:
                    task["_route_generate"] = route_info
                print(
                    f"[office] _route_generate atom={route_info.get('atom')} adapter={name} skill={skill}",
                    flush=True,
                )
                try:
                    log_path = Path(cfg.get("model_turn_log") or "runs/logs/office_model_turns.log")
                    log_path.parent.mkdir(parents=True, exist_ok=True)
                    with log_path.open("a", encoding="utf-8") as fh:
                        fh.write(f"_route_generate {route_info}\n")
                except Exception:
                    pass
                break
        except Exception as exc:
            if task is not None:
                task["_route_generate_error"] = str(exc)[:200]
            print(f"[office] _route_generate_error {exc}", flush=True)

    def reply(messages, _adapter=adapter):
        primed = list(messages)
        if bool(cfg.get("tool_call_primer", True)):
            if not primed or primed[0].get("role") != "system":
                primed = [{"role": "system", "content": TOOL_CALL_PRIMER}, *primed]
        # F3d: chat_template tools= makes Qwen emit schema/JSON we do not parse.
        # With XML primer, omit tools so the model copies <tool_call> format.
        use_tools = None if bool(cfg.get("tool_call_primer", True)) else OFFICE_TOOLS
        if cfg.get("force_native_tools"):
            use_tools = OFFICE_TOOLS
        return generate_messages(
            evo,
            primed,
            int(cfg.get("max_new_code", 160)),
            float(cfg.get("temperature", 0.0) or 0.0),
            _adapter,
            tools=use_tools,
            enable_thinking=False,
        )

    return reply


def _license(cfg: dict) -> License:
    return License(
        grants=set(cfg.get("grants") or ["python", "shell", "read", "write", "http"]),
        max_steps=int(cfg.get("max_steps", 6)),
        timeout=float(cfg.get("exec_timeout", 8)),
    )


def _pack(cfg: dict, seed: int) -> dict:
    packs = DEV_PACKS
    names = cfg.get("packs")
    if names:
        packs = [pack for pack in DEV_PACKS if pack["name"] in names]
    return packs[seed % len(packs)]


def _workspace(cfg: dict, arm: str, index: int):
    from pathlib import Path

    from evo.util import repo_path

    root = Path(cfg["_workspace_root"]) if cfg.get("_workspace_root") else repo_path("tmp") / "office"
    path = root / f"{arm}-{index}"
    if path.exists():
        import shutil

        shutil.rmtree(path, ignore_errors=True)
    path.mkdir(parents=True)
    return path


def _retain_drop(items: list[dict], *, min_family_n: int = 4) -> float:
    """First-half vs second-half exam ok drop within a family.

    With n<min_family_n per family (common on short smokes), a single hard
    variant in the second half looks like catastrophic forget (drop=1.0).
    Require enough items before scoring forget; else 0.0 (insufficient evidence).
    """
    by_family: dict[str, list[bool]] = {}
    for item in items:
        by_family.setdefault(item["family"], []).append(bool(item["ok"]))
    drops = []
    for flags in by_family.values():
        if len(flags) < int(min_family_n):
            continue
        mid = len(flags) // 2
        if mid == 0 or mid >= len(flags):
            continue
        first = sum(flags[:mid]) / mid
        second = sum(flags[mid:]) / (len(flags) - mid)
        drops.append(first - second)
    return max(drops) if drops else 0.0


def _tokens(items: list[dict], cfg: dict) -> float | None:
    oks = [item for item in items if item.get("ok")]
    if not oks:
        return None
    per = cfg.get("tokens_per_step")
    if per is None:
        per = float(cfg.get("token_per_step_guess", 80))
    return sum(int(item.get("steps") or 1) for item in oks) / len(oks) * float(per)


def _pick(families: list[str], weights: list[float], rng: random.Random) -> str:
    total = sum(weights)
    draw = rng.random() * total
    cursor = 0.0
    for family, weight in zip(families, weights):
        cursor += weight
        if draw <= cursor:
            return family
    return families[-1]


def _write_gate(judged: dict, reports: list[dict]) -> None:
    from evo.office.judge import write_gate

    write_gate(judged, reports)
