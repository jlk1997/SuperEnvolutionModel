"""One body, one world, day and night.

Actors share the base model and the tasks. The agent keeps notes in the prompt.
The evolved actor keeps them in its adapters, and a failed night rolls back.
"""

from __future__ import annotations

import json
import random
import traceback
from pathlib import Path

from evo.data import load_probe
from evo.fastmem import FastSidecar
from evo.generate import generate
from evo.model import build_model, joint_adapters, release
from evo.outer_loop import sft_policy
from evo.runlog import Run
from evo.scale_decision import write_decision
from evo.selfplay.executor import outputs_match
from evo.util import mean, repo_path, set_seed
from evo.world.agent_baseline import agent_notes, oracle_notes, remember_solution
from evo.world.body import attempt, extract_code, grade_task, task_prompt
from evo.world.census import Census, pick_tasks
from evo.world.drift import drift_oldest, refresh_expects
from evo.world.invent import concept_pairs, depth_tasks, half_solved, pose_pairs, propose_concepts
from evo.world.pixels import pixel_bundle, vision_status
from evo.world.population import apply_gene, base_gene, fitness, inherit_genes, initial_genes
from evo.world.skills import SkillLibrary
from evo.world.sleep import (
    consolidate,
    gate_keeps,
    retention_keeps,
    score_probe,
    select_traces,
    should_sleep,
)
from evo.world.tasks import (
    PREFERENCE_DOC,
    choose_difficulty,
    day_bundle,
    make_task,
    preference_task,
    project_tasks,
)
from evo.world.toolbox import build_tools, tool_docs


def run_phase4(cfg: dict) -> dict:
    station = cfg.get("station", "live")
    if station == "self":
        return _compare_self(cfg)
    return run_live(cfg)


def run_live(cfg: dict) -> dict:
    set_seed(int(cfg["seed"]))
    run = Run(cfg["runs_root"], cfg.get("run_name", "phase4_live"), cfg)
    evo = None
    try:
        evo = build_model(cfg)
        if cfg.get("skill_slots"):
            evo.joint = joint_adapters(evo.model, "policy", "memory")
            run.log({"event": "joint_adapters", "ok": bool(evo.joint)})
            print(f"[model] joint_adapters={bool(evo.joint)}", flush=True)
        if cfg.get("station") == "fast":
            summary = _run_fast(evo, cfg, run)
        else:
            summary = _run_days(evo, cfg, run)
        summary["vram_mb"] = evo.vram_mb()
        run.save_json("summary.json", summary)
        card = scorecard_line(summary)
        (run.dir / "scorecard.txt").write_text(card + "\n", encoding="utf-8")
        run.log({"event": "done", "run": str(run.dir)})
        print(card, flush=True)
        print(f"[live] wrote {run.dir}", flush=True)
        if cfg.get("write_decision"):
            smoke = _latest_summary("phase4_smoke")
            payload = write_decision(repo_path("runs") / "phase6_decision.json", smoke, summary)
            run.log({"event": "scale_decision", **payload})
        return summary
    except Exception:
        (run.dir / "error.txt").write_text(traceback.format_exc(), encoding="utf-8")
        raise
    finally:
        release(evo)


def _run_days(evo, cfg: dict, run: Run) -> dict:
    rng = random.Random(int(cfg["seed"]))
    timeout = float(cfg.get("exec_timeout", 2.0))
    difficulty, day0 = _tune(evo, cfg, run, rng, timeout)
    used: set[str] = set()
    tools: list[dict] = []
    solutions: list[dict] = []
    oracle_solutions: list[dict] = []
    past_pairs: list[tuple[str, str]] = []
    held_exams: list[dict] = []
    archive: list[dict] = []
    census = Census()
    library = SkillLibrary(int(cfg.get("slot_cap", 8))) if cfg.get("skill_slots") else None
    pending_depth: list[dict] = []
    stale_docs: list[dict] | None = None
    stale_solutions: list[dict] = []
    gene_rng = random.Random(int(cfg["seed"]) + 3)
    genes = (
        initial_genes(cfg, int(cfg.get("population", 1)), gene_rng)
        if int(cfg.get("population", 1)) > 1
        else [base_gene(cfg)]
    )
    probe = load_probe(cfg)["qas"]
    days = []
    last_exam: list[dict] = []
    last_exam_solutions: list[dict] = []
    last_oracle_solutions: list[dict] = []
    schedule = cfg.get("new_tools_schedule")
    for day in range(int(cfg["days"])):
        count = int(schedule[day]) if schedule else int(cfg.get("new_tools_per_day", 2))
        new_tools = (
            build_tools(int(cfg["seed"]) + 17, count, day, used, pair=bool(cfg.get("chain_exam"))) if count else []
        )
        tools.extend(new_tools)
        if cfg.get("pixels"):
            bundle = pixel_bundle(day, rng)
        else:
            bundle = day_bundle(day, tools, new_tools, difficulty, cfg, rng) if tools else {"practice": [], "gate": [], "exam": []}
        if pending_depth:
            bundle["exam"] = list(bundle["exam"]) + pending_depth
            pending_depth = []
        if cfg.get("drift_day") is not None and day == int(cfg["drift_day"]) and tools:
            stale_docs = tool_docs(tools)
            stale_solutions = list(solutions)
            drifted = drift_oldest(tools)
            if drifted is not None:
                refresh_expects(archive + held_exams, tools, timeout)
                print(f"[live] drift tool={drifted['name']} step={drifted.get('drift_from')}->{drifted.get('step')}", flush=True)
        if cfg.get("wider") and tools:
            bundle["exam"] = list(bundle["exam"]) + [preference_task(day)]
            project = project_tasks(day, tools[0], tools, timeout)
            if project is not None:
                bundle["exam"].append(project)
        if bundle["exam"]:
            last_exam = bundle["exam"]
            last_exam_solutions = list(solutions)
            last_oracle_solutions = list(oracle_solutions)
        docs = tool_docs(tools)
        if cfg.get("wider"):
            docs = docs + [PREFERENCE_DOC]
        actors = _day_actors(cfg, stale_docs is not None)
        print(f"[live] day={day + 1}/{cfg['days']} tools={len(tools)} new={len(new_tools)} difficulty={difficulty}", flush=True)
        exam = {}
        for actor in actors:
            actor_docs = stale_docs if actor == "agent_stale" and stale_docs is not None else docs
            actor_solutions = _solution_bank(actor, solutions, stale_solutions, oracle_solutions)
            exam[actor] = _summarize(
                _run_actor(
                    evo, actor, bundle["exam"], tools, actor_docs, actor_solutions, cfg, run, record=False, library=library
                )
            )
        evolved_rows = exam["evolved"]["rows"]
        if cfg.get("retention_gate", True):
            known = {task["id"] for task in held_exams}
            for row in evolved_rows:
                task = row["task"]
                if row["ok"] and task.get("kind") == "call" and task["id"] not in known:
                    held_exams.append(task)
                    known.add(task["id"])
            cap = int(cfg.get("held_exam_cap", 8))
            if cap > 0:
                del held_exams[:-cap]
        consistency = _consistency(evo, evolved_rows, tools, cfg, run) if cfg.get("measure_consistency", True) else None
        practice_rows = _practice(evo, bundle["practice"], tools, cfg, run, library)
        agent_practice = _run_actor(
            evo, "agent", bundle["practice"], tools, docs, solutions, cfg, run, record=True, library=library
        )
        if cfg.get("oracle"):
            _run_actor(
                evo, "oracle", bundle["practice"], tools, docs, oracle_solutions, cfg, run, record=True, library=library
            )
        fail_rate = 1.0 - (_rate(practice_rows) if practice_rows else 0.0)
        sleep = should_sleep(
            fail_rate,
            len(new_tools),
            len(tools),
            bool(cfg.get("self_directed")),
            float(cfg.get("sleep_fail", 0.4)),
            float(cfg.get("sleep_novelty", 0.25)),
        )
        kept = select_traces(practice_rows, bool(cfg.get("self_directed")), float(cfg.get("min_learnability", 0.34)))
        night = {"slept": False, "rolled_back": False, "probe_f1": None, "reject": None}
        night_traces = practice_rows if cfg.get("hindsight") else kept
        concept_tools = []
        cfg["posed_pairs"] = []
        if cfg.get("invent"):
            if half_solved(1.0 - fail_rate):
                concept_tools = propose_concepts(practice_rows, tools, used, limit=1)
            cfg["posed_pairs"] = pose_pairs(evo, cfg)
            if cfg["posed_pairs"]:
                print(f"[live] posed={len(cfg['posed_pairs'])}", flush=True)
        if sleep and (new_tools or night_traces or past_pairs or concept_tools or cfg.get("posed_pairs")):
            night = _night(
                evo,
                cfg,
                run,
                new_tools,
                night_traces,
                past_pairs,
                bundle["gate"],
                tools,
                probe,
                day,
                held_exams,
                library=library,
                genes=genes,
                gene_rng=gene_rng,
                concepts=concept_tools,
            )
            if cfg.get("evolve_recipe") and night.get("gene"):
                genes = inherit_genes(night["gene"], int(cfg.get("population", 1)), gene_rng)
            if night.get("concepts"):
                tools.extend(night["concepts"])
                for concept in night["concepts"]:
                    pending_depth.extend(depth_tasks(concept, tools, day + 1, timeout))
        else:
            print(f"[live] day={day + 1} skip_sleep fail_rate={fail_rate:.2f}", flush=True)
        old_tool = _old_tool_flag(exam, day)
        row = {
            "day": day,
            "new_tools": [tool["name"] for tool in new_tools],
            "difficulty": difficulty,
            "exam": {actor: _exam_public(exam[actor]) for actor in exam},
            "old_tool": old_tool,
            "practice_fail_rate": fail_rate,
            "slept": night["slept"],
            "rolled_back": night["rolled_back"],
            "probe_f1": night["probe_f1"],
            "consistency": consistency,
            "agent_practice_rate": _rate(agent_practice),
            "chain": _chain_flags(exam),
            "reject": night.get("reject"),
            "route": None if library is None else library.accuracy(),
            "inventions": sum(1 for tool in tools if tool.get("concept")),
        }
        if bundle["exam"]:
            archive.extend(bundle["exam"])
        if cfg.get("census") and archive:
            last = day == int(cfg["days"]) - 1
            row["census"] = _take_census(
                evo, cfg, run, census, archive, tools, docs, solutions, stale_docs, stale_solutions, library, day, last, oracle_solutions
            )
        days.append(row)
        run.log({"event": "day", **{key: value for key, value in row.items() if key != "exam"}, "exam": row["exam"]})
        (run.dir / "scorecard.txt").write_text(scorecard_line({"days": days}) + "\n", encoding="utf-8")
    if last_exam and tools:
        # The day's exam ran before the night. Score it once more so the last night is visible.
        print("[live] morning after the last night", flush=True)
        docs = tool_docs(tools)
        if cfg.get("wider"):
            docs = docs + [PREFERENCE_DOC]
        morning = {}
        for actor in _day_actors(cfg, False):
            bank = _solution_bank(actor, last_exam_solutions, last_exam_solutions, last_oracle_solutions)
            morning[actor] = _summarize(
                _run_actor(evo, actor, last_exam, tools, docs, bank, cfg, run, record=False, library=library)
            )
        morning_row = {
            "day": int(cfg["days"]),
            "new_tools": [],
            "difficulty": difficulty,
            "exam": {actor: _exam_public(morning[actor]) for actor in morning},
            "old_tool": _old_tool_flag(morning, 1),
            "practice_fail_rate": None,
            "slept": False,
            "rolled_back": False,
            "probe_f1": days[-1]["probe_f1"] if days else None,
            "consistency": None,
            "agent_practice_rate": None,
            "after_last_night": True,
            "chain": _chain_flags(morning),
            "reject": days[-1].get("reject") if days else None,
        }
        days.append(morning_row)
        run.log({"event": "morning", "exam": morning_row["exam"], "chain": morning_row["chain"]})
    summary = {
        "station": cfg.get("station", "live"),
        "model": cfg["model_name"],
        "difficulty": difficulty,
        "day0": day0,
        "days": days,
        "self_directed": bool(cfg.get("self_directed")),
        "wider": bool(cfg.get("wider")),
        "census_curve": [row.get("census") for row in days if row.get("census")],
        "vision": vision_status() if cfg.get("pixels") else None,
        "genes": genes,
        "joint_adapters": bool(getattr(evo, "joint", False)) if library is not None else None,
    }
    return summary


def _day_actors(cfg: dict, stale: bool) -> list[str]:
    actors = ["base", "agent"]
    if stale:
        actors.append("agent_stale")
    if cfg.get("oracle"):
        actors.append("oracle")
    actors.append("evolved")
    return actors


def _solution_bank(actor: str, solutions, stale_solutions, oracle_solutions):
    if actor == "agent_stale":
        return stale_solutions
    if actor == "oracle":
        return oracle_solutions
    return solutions


def _exam_public(cell: dict) -> dict:
    """Rates plus the per-item record a paired interval needs. The full trace stays out of the log."""
    return {
        "rate": cell["rate"],
        "turns": cell["turns"],
        "tokens": cell["tokens"],
        "items": [{"id": row["id"], "ok": bool(row["ok"])} for row in cell["rows"]],
    }


def _tune(evo, cfg, run, rng, timeout: float) -> tuple[str, dict]:
    n = int(cfg.get("tune_tasks", 4))
    if n <= 0:
        return str(cfg.get("difficulty", "mixed")), {}
    used: set[str] = set()
    tools = build_tools(int(cfg["seed"]) + 99, max(2, n // 2), day=0, used=used)
    tasks = [make_task("tune", 0, index, tools, tools, "mixed", timeout, rng) for index in range(n)]
    docs = tool_docs(tools)
    scores = {}
    for actor in ("base", "agent", "evolved"):
        rows = _run_actor(evo, actor, tasks, tools, docs, [], cfg, run, record=False)
        scores[actor] = _summarize(rows)
        print(f"[live] day0 actor={actor} rate={scores[actor]['rate']:.2f}", flush=True)
    agent_rate = scores["agent"]["rate"]
    difficulty = choose_difficulty(agent_rate)
    payload = {
        "agent_rate": agent_rate,
        "base_rate": scores["base"]["rate"],
        "evolved_rate": scores["evolved"]["rate"],
        "difficulty": difficulty,
        "turns": {actor: scores[actor]["turns"] for actor in scores},
        "tokens": {actor: scores[actor]["tokens"] for actor in scores},
    }
    run.log({"event": "day0", **payload})
    return difficulty, payload


def _run_actor(evo, actor, tasks, tools, docs, solutions, cfg, run, record: bool, max_turns=None, library=None):
    workspace = _workspace(run, actor)
    rows = []
    for task in tasks:
        notes = ""
        if actor in ("agent", "agent_stale"):
            notes = lambda error, task=task: agent_notes(task, docs, solutions, error)
        elif actor == "oracle":
            notes = lambda error, task=task: oracle_notes(task, docs, solutions, error)
        adapter, slot = _evolved_adapter(evo, task, library, cfg) if actor == "evolved" else (None, None)
        row = attempt(
            evo,
            task,
            tools,
            cfg,
            adapter=adapter,
            notes=notes,
            workspace=workspace,
            max_turns=max_turns,
            block_ids=_lexical_block(evo, task, slot, library, cfg),
        )
        rows.append(row)
        if record and actor in ("agent", "oracle") and row["ok"]:
            remember_solution(solutions, task, row["trace"][-1]["code"])
        extra = ""
        if row["trace"] and ("chain" in task["id"] or not row["ok"]):
            code = " ".join((row["trace"][-1].get("code") or "").split())
            extra = f" code={code[:160]}"
        print(
            f"[live] actor={actor} task={task['id']} ok={row['ok']} turns={row['turns']}{extra}",
            flush=True,
        )
    return rows


def _practice(evo, tasks, tools, cfg, run, library=None) -> list[dict]:
    """Evolved practice. No tool notes. Self-directed mode takes two single tries."""
    rows = []
    samples = 2 if cfg.get("self_directed") else 1
    turns = 1 if cfg.get("self_directed") else None
    for task in tasks:
        for _ in range(samples):
            adapter, slot = _evolved_adapter(evo, task, library, cfg)
            row = attempt(
                evo,
                task,
                tools,
                cfg,
                adapter=adapter,
                notes="",
                workspace=_workspace(run, "evolved"),
                max_turns=turns,
                block_ids=_lexical_block(evo, task, slot, library, cfg),
            )
            rows.append(row)
    return rows


def _night(
    evo,
    cfg,
    run,
    new_tools,
    traces,
    past_pairs,
    gate_tasks,
    tools,
    probe,
    day,
    held_exams=None,
    library=None,
    genes=None,
    gene_rng=None,
    concepts=None,
    persist=True,
) -> dict:
    if persist and int(cfg.get("population", 1)) > 1:
        return _population_night(
            evo, cfg, run, new_tools, traces, past_pairs, gate_tasks, tools, probe, day, held_exams, library, genes, gene_rng, concepts
        )
    return _night_body(
        evo, cfg, run, new_tools, traces, past_pairs, gate_tasks, tools, probe, day, held_exams, library, concepts, persist
    )


def _night_body(
    evo, cfg, run, new_tools, traces, past_pairs, gate_tasks, tools, probe, day, held_exams, library, concepts, persist
) -> dict:
    lib_snap = library.snapshot(evo) if library is not None else None
    snap_policy = evo.snapshot("policy")
    snap_memory = evo.snapshot("memory")
    slot = None
    evict = None
    train_name = str(cfg.get("body_adapter") or "policy")
    cfg["train_adapter"] = train_name
    core = str(cfg.get("body_adapter") or "policy")
    if library is not None and new_tools:
        slot, evict = library.open_slot(evo, new_tools, day, core)
        train_name = slot.name
        cfg["train_adapter"] = train_name
        if evict is not None and evict.pairs:
            sft_policy(
                evo,
                evict.pairs,
                float(cfg.get("outer_lr", 5e-4)) * 0.25,
                1,
                int(cfg.get("max_seq_len", 384)),
                adapter="policy",
            )
    concept_slots = []
    if library is not None and concepts:
        for concept in concepts:
            concept_slot, _extra = library.open_slot(evo, [concept], day, core)
            concept_slots.append((concept_slot, concept))
    cfg["concept_pairs"] = []
    cfg["concept_slot"] = None
    if concepts:
        cfg["concept_pairs"] = [pair for concept in concepts for pair in concept_pairs(concept)]
        if concept_slots:
            cfg["concept_slot"] = concept_slots[-1][0].name
    before_rows = _run_actor(evo, "evolved", gate_tasks, tools, [], [], cfg, run, record=False, max_turns=1, library=library)
    before_rate = _rate(before_rows)
    before_probe = score_probe(evo, probe, int(cfg.get("answer_tokens", 16)))
    night_cfg = dict(cfg)
    if cfg.get("wider") and day == 0:
        night_cfg["extra_lesson"] = PREFERENCE_DOC["text"]
        night_cfg["preference_pair"] = ("How must every printed line start? Reply with the tag only.", "ACK")
        if new_tools:
            tool = new_tools[0]
            arg = tool["quiz_args"][0]
            night_cfg["file_pair"] = (
                f"Write the result of {tool['nick']} applied to {arg} into workspace/keep.txt and print saved.",
                "open('workspace/keep.txt', 'w', encoding='utf-8').write("
                f"str({tool['name']}({arg})))\nprint('saved')",
            )
    else:
        night_cfg["preference_pair"] = None
        night_cfg["extra_lesson"] = ""
    night_cfg["compose_tools"] = tools
    night_cfg["held_tasks"] = list(held_exams or [])
    trained = consolidate(evo, new_tools, traces, past_pairs, before_rate, before_probe, probe, night_cfg)
    if night_cfg.get("concept_slot") and night_cfg.get("concept_pairs"):
        sft_policy(
            evo,
            night_cfg["concept_pairs"],
            float(cfg.get("outer_lr", 5e-4)),
            1,
            int(cfg.get("max_seq_len", 384)),
            adapter=night_cfg["concept_slot"],
        )
    after_rows = _run_actor(evo, "evolved", gate_tasks, tools, [], [], cfg, run, record=False, max_turns=1, library=library)
    after_rate = _rate(after_rows)
    after_probe = score_probe(evo, probe, int(cfg.get("answer_tokens", 16)))
    # The skill lives on policy. The probe lives on memory. A probe drop must not
    # erase a policy that just learned the new tools.
    skill_ok = gate_keeps(before_rate, after_rate, before_probe, after_probe, float(cfg.get("gate_drop", 0.34)), 1.0)
    probe_ok = (before_probe - after_probe) <= float(cfg.get("max_f1_drop", 0.15))
    held = list(held_exams or [])
    retention_after = None
    retention_ok = True
    if cfg.get("retention_gate", True) and held:
        retained = _run_actor(
            evo, "evolved", held, tools, [], [], cfg, run, record=False, max_turns=int(cfg.get("max_turns", 2)), library=library
        )
        retention_after = sum(1 for row in retained if row["ok"])
        for row in retained:
            if row["ok"] or not row.get("trace"):
                continue
            code = " ".join((row["trace"][-1].get("code") or "").split())
            print(f"[live] retention fail id={row['id']} code={code[:160]}", flush=True)
        retention_ok = retention_keeps(len(held), retention_after, float(cfg.get("gate_drop", 0.34)))
    chain_gate_ok = None
    if cfg.get("chain_exam"):
        focus = list(new_tools) or list(tools)
        gate_chain = make_task(
            "gate",
            day,
            0,
            tools,
            focus,
            "chain",
            float(cfg.get("exec_timeout", 2.0)),
            random.Random(int(cfg["seed"])),
        )
        if "chain" in gate_chain["id"]:
            chain_rows = _run_actor(
                evo, "evolved", [gate_chain], tools, [], [], cfg, run, record=False, max_turns=1, library=library
            )
            chain_gate_ok = bool(chain_rows and chain_rows[0]["ok"])
    reject = []
    if not skill_ok:
        reject.append("skill")
    if not retention_ok:
        reject.append("retention")
    if chain_gate_ok is False:
        reject.append("chain_gate")
    keep = not reject
    retest = _bind_retest(evo, tools, cfg, run, library) if int(cfg.get("population", 1)) > 1 else None
    if keep:
        if slot is not None and library is not None:
            library.remember(evo, slot, new_tools)
        for concept_slot, concept in concept_slots:
            library.remember(evo, concept_slot, [concept])
        if persist:
            seen_prompts = {prompt for prompt, _completion in past_pairs}
            for pair in trained["new_pairs"]:
                if pair[0] not in seen_prompts:
                    past_pairs.append(pair)
                    seen_prompts.add(pair[0])
            parent_generation = run.lineage[-1]["generation"] if run.lineage else None
            run.commit_adapter(
                evo.model,
                train_name,
                {
                    "kind": "night",
                    "day": day,
                    "kept": True,
                    "parent_generation": parent_generation,
                    "gene": cfg.get("_gene"),
                    "fitness": cfg.get("_fitness"),
                },
            )
    else:
        evo.restore("policy", snap_policy)
        if library is not None and lib_snap is not None:
            library.restore(evo, lib_snap)
        cfg["train_adapter"] = "policy"
    if probe_ok and persist:
        run.commit_adapter(evo.model, "memory", {"kind": "night", "day": day, "kept": True})
    elif not probe_ok:
        evo.restore("memory", snap_memory)
    print(
        f"[live] night day={day + 1} keep={keep} gate {before_rate:.2f}->{after_rate:.2f} "
        f"probe {before_probe:.2f}->{after_probe:.2f} memory_kept={probe_ok} retained={retention_after} "
        f"chain_gate={chain_gate_ok} skill={skill_ok} retention={retention_ok} reject={','.join(reject) or 'none'}",
        flush=True,
    )
    run.log(
        {
            "event": "night",
            "day": day,
            "keep": keep,
            "persist": persist,
            "gate_before": before_rate,
            "gate_after": after_rate,
            "probe_before": before_probe,
            "probe_after": after_probe,
            "drills": trained["drills"],
            "policy_steps": trained["policy"]["steps"],
            "chain_gate": chain_gate_ok,
            "skill": skill_ok,
            "retention": retention_ok,
            "reject": reject,
            "refine": trained.get("refine"),
            "gene": cfg.get("_gene"),
            "retest": retest,
        }
    )
    reported_probe = after_probe if probe_ok else before_probe
    return {
        "slept": True,
        "rolled_back": not keep,
        "probe_f1": reported_probe,
        "memory_kept": probe_ok,
        "reject": reject,
        "skill": skill_ok,
        "chain_gate": chain_gate_ok,
        "retention": retention_ok,
        "gate_before": before_rate,
        "gate_after": after_rate,
        "retest": retest,
        "concepts": list(concepts or []) if keep else [],
        "gene": cfg.get("_gene"),
        "new_pairs": trained["new_pairs"] if keep else [],
    }


def _population_night(
    evo, cfg, run, new_tools, traces, past_pairs, gate_tasks, tools, probe, day, held_exams, library, genes, gene_rng, concepts
) -> dict:
    """Train each recipe from the same parent. Keep the best night that still passes the gates."""
    from evo.model import add_named_adapter, load_adapter_state

    body = str(cfg.get("body_adapter") or "policy")
    parent_body = evo.snapshot(body)
    parent_memory = evo.snapshot("memory")
    parent_lib = library.snapshot(evo) if library is not None else None
    head = run.lineage[-1]["generation"] if run.lineage else None
    scored = []
    for gene in genes or [base_gene(cfg)]:
        evo.restore(body, parent_body)
        evo.restore("memory", parent_memory)
        if library is not None and parent_lib is not None:
            library.restore(evo, parent_lib)
        night_cfg = apply_gene(cfg, gene)
        night_cfg["_gene"] = gene
        night_cfg["body_adapter"] = body
        result = _night_body(
            evo, night_cfg, run, new_tools, traces, past_pairs, gate_tasks, tools, probe, day, held_exams, library, concepts, False
        )
        fit = fitness(result.get("gate_after") or 0.0, result.get("chain_gate"), result.get("retest") or 0.0)
        print(f"[live] candidate fit={fit:.2f} keep={not result['rolled_back']} gene_lr={gene['outer_lr']:.5f}", flush=True)
        if result["rolled_back"]:
            continue
        scored.append(
            {
                "fitness": fit,
                "gene": gene,
                "body": evo.snapshot(body),
                "memory": evo.snapshot("memory"),
                "library": library.snapshot(evo) if library is not None else None,
                "result": result,
            }
        )
        run.commit_adapter(
            evo.model,
            body,
            {"kind": "candidate", "day": day, "kept": False, "parent_generation": head, "parents": [head] if head is not None else [], "gene": gene, "fitness": fit},
        )
    scored.sort(key=lambda item: item["fitness"], reverse=True)
    if len(scored) >= 2 and library is None:
        crossed = _cross_candidate(evo, scored[0], scored[1], cfg, run, tools, gate_tasks, day, held_exams, library, head, body)
        if crossed is not None and crossed["fitness"] >= scored[0]["fitness"]:
            scored.insert(0, crossed)
    if not scored:
        evo.restore(body, parent_body)
        evo.restore("memory", parent_memory)
        if library is not None and parent_lib is not None:
            library.restore(evo, parent_lib)
        print(f"[live] night day={day + 1} keep=False reject=population", flush=True)
        return {"slept": True, "rolled_back": True, "probe_f1": None, "reject": ["population"], "concepts": [], "gene": None}
    winner = scored[0]
    if winner.get("infer"):
        cfg["infer_adapter"] = winner["infer"]
        cfg["body_adapter"] = winner["infer"]
    else:
        cfg["infer_adapter"] = None
        evo.restore(body, winner["body"])
    evo.restore("memory", winner["memory"])
    if library is not None and winner["library"] is not None:
        library.restore(evo, winner["library"])
    seen = {prompt for prompt, _completion in past_pairs}
    for pair in winner["result"].get("new_pairs") or []:
        if pair[0] not in seen:
            past_pairs.append(pair)
            seen.add(pair[0])
    run.commit_adapter(
        evo.model,
        str(cfg.get("body_adapter") or body),
        {
            "kind": "winner",
            "day": day,
            "kept": True,
            "parent_generation": head,
            "parents": [head] if head is not None else [],
            "gene": winner["gene"],
            "fitness": winner["fitness"],
            "combination": winner.get("combination"),
        },
    )
    if library is not None and library.slots:
        run.commit_adapter(
            evo.model,
            library.slots[-1].name,
            {
                "kind": "slot",
                "day": day,
                "kept": True,
                "parent_generation": head,
                "parents": [head] if head is not None else [],
                "gene": winner["gene"],
                "fitness": winner["fitness"],
                "tools": list(library.slots[-1].tool_names),
            },
        )
    print(f"[live] winner fit={winner['fitness']:.2f} combination={winner.get('combination') or 'none'}", flush=True)
    return {**winner["result"], "gene": winner["gene"], "rolled_back": False}


def _adapter_rank(evo, name: str) -> int:
    spec = evo.model.peft_config.get(name)
    if spec is None:
        return int(evo.cfg["lora_rank"])
    return int(spec.r)


def _cross_candidate(evo, first, second, cfg, run, tools, gate_tasks, day, held, library, head, body):
    """Rank-concat the top two. Weights are one half each, so the merge is their average update."""
    from evo.model import _move_lora_to_cuda, add_named_adapter, load_adapter_state

    left = body or "policy"
    if _adapter_rank(evo, left) >= 4 * int(cfg.get("lora_rank", 8)):
        print("[live] crossover skipped rank", flush=True)
        return None
    dest = "cross_b" if str(left).startswith("cross") else "cross"
    try:
        evo.restore(left, first["body"])
        if "mate" in evo.model.peft_config:
            evo.model.delete_adapter("mate")
        add_named_adapter(evo, "mate", rank=_adapter_rank(evo, left))
        load_adapter_state(evo.model, "mate", second["body"])
        if dest in evo.model.peft_config:
            evo.model.delete_adapter(dest)
        evo.model.add_weighted_adapter([left, "mate"], [0.5, 0.5], dest, combination_type="cat")
        _move_lora_to_cuda(evo.model)
    except Exception as exc:
        print(f"[live] crossover skipped {type(exc).__name__}: {exc}", flush=True)
        return None
    cfg["infer_adapter"] = dest
    try:
        gate_rows = _run_actor(evo, "evolved", gate_tasks, tools, [], [], cfg, run, record=False, max_turns=1, library=library)
        chain_ok = None
        if cfg.get("chain_exam"):
            focus = list(tools[-2:]) or list(tools)
            gate_chain = make_task("gate", day, 0, tools, focus, "chain", float(cfg.get("exec_timeout", 2.0)), random.Random(int(cfg["seed"])))
            if "chain" in gate_chain["id"]:
                chain_rows = _run_actor(evo, "evolved", [gate_chain], tools, [], [], cfg, run, record=False, max_turns=1, library=library)
                chain_ok = bool(chain_rows and chain_rows[0]["ok"])
        retest = _bind_retest(evo, tools, cfg, run, library)
        retention_ok = True
        if held:
            retained = _run_actor(
                evo, "evolved", held, tools, [], [], cfg, run, record=False, max_turns=int(cfg.get("max_turns", 2)), library=library
            )
            retention_ok = retention_keeps(len(held), sum(1 for row in retained if row["ok"]), float(cfg.get("gate_drop", 0.34)))
    finally:
        cfg["infer_adapter"] = None
    if chain_ok is False or not retention_ok:
        print(f"[live] crossover rejected chain={chain_ok} retention={retention_ok}", flush=True)
        return None
    fit = fitness(_rate(gate_rows), chain_ok, retest)
    print(f"[live] crossover fit={fit:.2f}", flush=True)
    return {
        "fitness": fit,
        "gene": dict(first["gene"]),
        "body": first["body"],
        "memory": evo.snapshot("memory"),
        "library": first["library"],
        "result": dict(first["result"]),
        "infer": dest,
        "combination": "cat",
    }


def _bind_retest(evo, tools, cfg, run, library) -> float:
    """Old skills on bind args. Exam arguments stay out of the score that picks a winner."""
    tasks = []
    timeout = float(cfg.get("exec_timeout", 2.0))
    rng = random.Random(int(cfg["seed"]) + 11)
    for tool in tools:
        args = tool.get("bind_args") or []
        if not args:
            continue
        tasks.append(make_task("practice", int(tool.get("day", 0)), len(tasks), tools, [tool], "single", timeout, rng, args[0]))
        if len(tasks) >= 6:
            break
    if not tasks:
        return 0.0
    return _rate(_run_actor(evo, "evolved", tasks, tools, [], [], cfg, run, record=False, max_turns=1, library=library))


def _take_census(
    evo, cfg, run, census, archive, tools, docs, solutions, stale_docs, stale_solutions, library, day, last, oracle_solutions=None
) -> dict:
    rng = random.Random(int(cfg["seed"]) + 1000 + day)
    chosen = pick_tasks(
        archive,
        day,
        int(cfg.get("census_every", 5)),
        int(cfg.get("census_sample", 4)),
        rng,
        last=last,
    )
    actors = ["evolved", "agent"]
    if day == 0 or last:
        actors.insert(0, "base")
    if stale_docs is not None:
        actors.append("agent_stale")
    if cfg.get("oracle"):
        actors.append("oracle")
    births = {tool["name"]: int(tool.get("day", 0)) for tool in tools}
    turns = int(cfg.get("census_turns", 1))
    for actor in actors:
        actor_docs = stale_docs if actor == "agent_stale" and stale_docs is not None else docs
        actor_solutions = _solution_bank(actor, solutions, stale_solutions, oracle_solutions or [])
        rows = _run_actor(
            evo, actor, chosen, tools, actor_docs, actor_solutions, cfg, run, record=False, max_turns=turns, library=library
        )
        census.add(day, actor, rows)
    report = {actor: census.report(actor, day, births) for actor in actors}
    text = " ".join(
        f"{actor} alive={report[actor]['alive']} forgotten={report[actor]['forgotten']} mastery={report[actor]['mastery']}"
        for actor in ("evolved", "agent")
        if actor in report
    )
    print(f"[census] day={day} n={len(chosen)} {text}", flush=True)
    run.log({"event": "census", "day": day, "n": len(chosen), "report": report})
    return {"day": day, "n": len(chosen), "actors": report}


def _evolved_adapter(evo, task, library, cfg):
    forced = cfg.get("infer_adapter")
    if forced:
        return forced, None
    core = cfg.get("body_adapter") or "policy"
    if library is None or not library.slots:
        return core, None
    slot = library.choose(evo, task)
    if slot is None:
        return core, None
    return library.activate(evo, slot, core), slot


def _lexical_block(evo, task, slot, library, cfg):
    if not cfg.get("lexical_gate") or library is None or slot is None:
        return None
    from evo.world.lexicon import gate_for_task

    others = []
    for other in library.slots:
        if other.name == slot.name:
            continue
        others.extend(other.tool_names)
    block = gate_for_task(evo.tok, list(slot.tool_names), others, list(task.get("tools") or []))
    return block or None


def _consistency(evo, rows, tools, cfg, run) -> dict | None:
    if not rows:
        return None
    agrees = []
    correct = []
    for row in rows:
        reply = generate(evo, task_prompt(row["task"], "", ""), int(cfg.get("max_new_code", 64)), 0.7, "policy")
        _ok, result = grade_task(extract_code(reply), row["task"], tools, _workspace(run, "evolved"), float(cfg.get("exec_timeout", 2.0)))
        first = row["trace"][0]["value"] if row["trace"] else ""
        agrees.append(1.0 if outputs_match(first, result.value) and (first or result.value) else 0.0)
        correct.append(1.0 if row["ok"] else 0.0)
    return {"agreement": mean(agrees) or 0.0, "accuracy": mean(correct) or 0.0}


def _run_fast(evo, cfg, run: Run) -> dict:
    """Second attempt versus first, with the fast state and without an optimizer."""
    sidecar = FastSidecar(evo, scale=float(cfg.get("fast_scale", 0.02)))
    try:
        used: set[str] = set()
        tools = build_tools(int(cfg["seed"]), int(cfg.get("new_tools_per_day", 2)), day=0, used=used)
        timeout = float(cfg.get("exec_timeout", 2.0))
        rng = random.Random(int(cfg["seed"]))
        tasks = [
            make_task("exam", 0, index, tools, tools, "single", timeout, rng)
            for index in range(int(cfg.get("exam_tasks", 4)))
        ]
        conditions = {"error_only": [], "state_only": [], "state_and_error": []}
        for task in tasks:
            sidecar.off()
            sidecar.reset()
            first = attempt(evo, task, tools, cfg, "policy", max_turns=1, sidecar=None)
            second = attempt(
                evo, task, tools, cfg, "policy", max_turns=1, sidecar=None, initial_error=first["trace"][-1]["error"]
            )
            conditions["error_only"].append({"first": first["ok"], "second": second["ok"]})

            sidecar.reset()
            state_first = attempt(evo, task, tools, cfg, "policy", max_turns=1, sidecar=sidecar)
            sidecar.absorb(state_first["trace"][-1]["error"] or state_first["trace"][-1]["code"], "policy")
            state_second = attempt(evo, task, tools, cfg, "policy", max_turns=1, sidecar=sidecar, show_error=False)
            conditions["state_only"].append({"first": state_first["ok"], "second": state_second["ok"]})

            sidecar.reset()
            both_first = attempt(evo, task, tools, cfg, "policy", max_turns=1, sidecar=sidecar)
            both_second = attempt(
                evo,
                task,
                tools,
                cfg,
                "policy",
                max_turns=1,
                sidecar=sidecar,
                initial_error=both_first["trace"][-1]["error"],
            )
            conditions["state_and_error"].append({"first": both_first["ok"], "second": both_second["ok"]})
            print(
                f"[fast] task={task['id']} error {first['ok']}->{second['ok']} "
                f"state {state_first['ok']}->{state_second['ok']}",
                flush=True,
            )
        distill_pairs = []
        for task, row in zip(tasks, conditions["state_and_error"]):
            if row["second"] and not row["first"]:
                distill_pairs.append(
                    (
                        "Write Python that does the task. Reply with code only.\n\n" + task["prompt"],
                        f"print({task['tools'][0]}({_arg_of(task)}))",
                    )
                )
        sidecar.off()
        stats = sft_policy(
            evo,
            distill_pairs,
            float(cfg.get("outer_lr", 5e-4)),
            int(cfg.get("night_epochs", 1)),
            int(cfg.get("max_seq_len", 256)),
        )
        fresh = [
            make_task("gate", 0, index, tools, tools, "single", timeout, rng)
            for index in range(len(tasks))
        ]
        after = _run_actor(evo, "evolved", fresh, tools, [], [], cfg, run, record=False, max_turns=1)
        summary = {
            "station": "fast",
            "model": cfg["model_name"],
            "conditions": {name: _turn_rates(rows) for name, rows in conditions.items()},
            "distill_pairs": len(distill_pairs),
            "distill": stats,
            "fresh_after_distill": _rate(after),
        }
        run.log({"event": "fast", "conditions": summary["conditions"], "fresh": summary["fresh_after_distill"]})
        return summary
    finally:
        sidecar.close()


def _compare_self(cfg: dict) -> dict:
    fixed_cfg = dict(cfg)
    fixed_cfg["self_directed"] = False
    fixed_cfg["run_name"] = str(cfg.get("run_name", "phase4_self")) + "_fixed"
    fixed_cfg["station"] = "live"
    fixed = run_live(fixed_cfg)
    free_cfg = dict(cfg)
    free_cfg["self_directed"] = True
    free_cfg["run_name"] = str(cfg.get("run_name", "phase4_self")) + "_self"
    free_cfg["station"] = "live"
    free = run_live(free_cfg)
    fixed_rates = [row["exam"]["evolved"]["rate"] for row in fixed["days"]]
    free_rates = [row["exam"]["evolved"]["rate"] for row in free["days"]]
    summary = {
        "fixed_final": fixed_rates[-1] if fixed_rates else None,
        "self_final": free_rates[-1] if free_rates else None,
        "fixed_rates": fixed_rates,
        "self_rates": free_rates,
        "self_not_slower": (free_rates[-1] if free_rates else 0) >= (fixed_rates[-1] if fixed_rates else 0),
    }
    out = repo_path("runs") / "phase4_self_compare.json"
    out.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"[live] self_compare {summary}", flush=True)
    return summary


def _turn_rates(rows: list[dict]) -> dict:
    return {
        "first": _rate_flags([row["first"] for row in rows]),
        "second": _rate_flags([row["second"] for row in rows]),
        "n": len(rows),
    }


def _rate_flags(flags) -> float:
    if not flags:
        return 0.0
    return sum(1.0 for flag in flags if flag) / len(flags)


def _rate(rows: list[dict]) -> float:
    if not rows:
        return 0.0
    return sum(1.0 for row in rows if row.get("ok")) / len(rows)


def _summarize(rows: list[dict]) -> dict:
    return {
        "rate": _rate(rows),
        "turns": mean([row["turns"] for row in rows]) or 0.0,
        "tokens": sum(row["prompt_tokens"] for row in rows),
        "rows": rows,
    }


def _actor_bits(exam: dict, chain: dict) -> str:
    bits = []
    names = [name for name in ("base", "agent", "agent_stale", "oracle", "evolved") if name in exam]
    for actor in names:
        cell = exam.get(actor) or {}
        bits.append(f"{actor}={cell.get('rate')} chain={chain.get(actor)} tokens={cell.get('tokens')}")
    return " ".join(bits)


def scorecard_line(summary: dict) -> str:
    """Each afternoon, then the morning, with the reason a night was returned."""
    days = summary.get("days") or []
    if not days:
        return "[exam] no scored day"
    lines = []
    for row in days:
        exam = row.get("exam") or {}
        chain = row.get("chain") or {}
        if row.get("after_last_night"):
            lines.append("[exam] morning " + _actor_bits(exam, chain) + f" reject={row.get('reject')}")
        else:
            lines.append(
                f"[exam] day={row.get('day')} "
                + _actor_bits(exam, chain)
                + f" reject={row.get('reject')} rolled_back={row.get('rolled_back')}"
            )
        census = row.get("census")
        if census:
            evolved = (census.get("actors") or {}).get("evolved") or {}
            lines.append(
                f"[census] day={row.get('day')} alive={evolved.get('alive')} forgotten={evolved.get('forgotten')} "
                f"mastery={evolved.get('mastery')} tokens_per_ok={evolved.get('tokens_per_ok')} "
                f"route={row.get('route')} inventions={row.get('inventions')}"
            )
    return "\n".join(lines)


def _chain_flags(exam: dict) -> dict:
    flags = {}
    for actor, cell in exam.items():
        chains = [row for row in cell["rows"] if "chain" in row["id"]]
        flags[actor] = None if not chains else all(row["ok"] for row in chains)
    return flags


def _old_tool_flag(exam: dict, day: int) -> dict | None:
    if day == 0:
        return None
    flags = {}
    for actor, cell in exam.items():
        held = [row for row in cell["rows"] if row["task"].get("retention")]
        flags[actor] = bool(held[-1]["ok"]) if held else None
    return flags


def _workspace(run: Run, actor: str) -> Path:
    path = run.dir / "workspace" / actor
    path.mkdir(parents=True, exist_ok=True)
    return path


def _latest_summary(name: str) -> dict | None:
    root = repo_path("runs") / name
    if not root.exists():
        return None
    found = sorted(path for path in root.iterdir() if (path / "summary.json").exists())
    if not found:
        return None
    return json.loads((found[-1] / "summary.json").read_text(encoding="utf-8"))


def _arg_of(task: dict) -> str:
    if task.get("arg"):
        return str(task["arg"])
    prompt = task["prompt"]
    start = prompt.find("(")
    stop = prompt.rfind(")")
    if start >= 0 and stop > start:
        return prompt[start + 1 : stop]
    return ""
