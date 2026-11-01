"""One task stream, six arms, the same experience and the same step budget.

agent and oracle never write weights. shift writes in batches. The continual arms
write inside the stream, on a shadow adapter, and the exam items never enter the buffer.
"""

from __future__ import annotations

import random

from evo.live.compare import judge_stream
from evo.live.episodic import Episode, EpisodicBuffer
from evo.live.identity import Identity
from evo.live.promote import Ledger
from evo.live.rails import denied
from evo.live.triggers import decide
from evo.live.verifier import CheckerTrust, literal_claim
from evo.model import blend_adapters, release
from evo.runlog import Run
from evo.util import repo_path, set_seed
from evo.world.census import Census


ARMS = ("agent", "oracle", "shift", "continual", "continual_nofast", "continual_sft")
ARM_SALT = {name: index + 1 for index, name in enumerate(ARMS)}


def tick_plan(ticks: int, tool_every: int, drift_tick, day_ticks: int) -> list[dict]:
    """What the world does at each tick. The arm does not change this plan."""
    rows = []
    for tick in range(int(ticks)):
        rows.append(
            {
                "tick": tick,
                "new_tool": tick > 0 and tool_every > 0 and tick % tool_every == 0,
                "drift": drift_tick is not None and tick == int(drift_tick),
                "exam": day_ticks > 0 and tick % day_ticks == 0,
                "shift_flush": day_ticks > 0 and tick % day_ticks == day_ticks - 1,
            }
        )
    return rows


def _uses_fast(arm: str) -> bool:
    return arm not in ("agent", "oracle", "continual_nofast")


def _learns(arm: str) -> bool:
    return arm not in ("agent", "oracle")


def reset_body(evo, policy_snap, memory_snap) -> None:
    from evo.model import ensure_input_grads

    for module in evo.model.modules():
        hooks = getattr(module, "_forward_hooks", None)
        if hooks:
            hooks.clear()
    ensure_input_grads(evo.model)
    evo.restore("policy", policy_snap)
    evo.restore("memory", memory_snap)
    for name in list(getattr(evo.model, "peft_config", {})):
        if name not in ("policy", "memory", "scratch"):
            evo.model.delete_adapter(name)
    paired = getattr(evo.model, "_paired", None)
    if isinstance(paired, dict):
        paired.clear()


def run_stream(cfg: dict) -> dict:
    from evo.model import build_model

    seeds = [int(seed) for seed in (cfg.get("seeds") or [cfg.get("seed", 0)])]
    arms = list(cfg.get("arms") or ARMS)
    reports = []
    for seed in seeds:
        one = dict(cfg)
        one["seed"] = seed
        one["run_name"] = f"{cfg.get('run_name', 'stream')}_s{seed}"
        set_seed(seed)
        evo = build_model(one)
        run = Run(one.get("runs_root", "runs"), one["run_name"], one)
        policy = evo.snapshot("policy")
        memory = evo.snapshot("memory")
        arm_rows = []
        try:
            for arm in arms:
                reset_body(evo, policy, memory)
                print(f"[stream] seed={seed} arm={arm}", flush=True)
                arm_rows.append(run_arm(evo, run, arm, one))
                run.log({"event": "arm", "arm": arm, "opt_steps": arm_rows[-1]["opt_steps"], "alive": arm_rows[-1]["alive"]})
        finally:
            release(evo)
        reports.append({"seed": seed, "arms": arm_rows, "run": str(run.dir)})
    summary = {"run_name": cfg.get("run_name", "stream"), "seeds": seeds, "arms": arms, "reports": reports}
    summary["gate"] = judge_stream(reports)
    path = repo_path("runs") / f"{cfg.get('run_name', 'stream')}_report.json"
    import json

    path.write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    print(
        f"[stream] wrote {path} gate_pass={summary['gate'].get('pass')} branch={summary['gate'].get('branch')}",
        flush=True,
    )
    if cfg.get("write_gate"):
        from evo.live.compare import write_gate

        write_gate(repo_path("docs") / "ROADMAP.md", summary["gate"])
    return summary


def run_arm(evo, run, arm: str, cfg: dict) -> dict:
    from evo.fastmem import FastSidecar
    from evo.live.canary import anchors_hold, pick_canaries
    from evo.live.consolidator import drift_pairs, run_shadow
    from evo.live.onpolicy import onpolicy_update, sft_update
    from evo.world.agent_baseline import agent_notes, oracle_notes, remember_solution
    from evo.world.body import attempt
    from evo.world.drift import drift_oldest, refresh_expects
    from evo.world.tasks import day_bundle, make_task
    from evo.world.toolbox import build_tools, tool_docs

    world = random.Random(int(cfg["seed"]))
    canary_rng = random.Random(int(cfg["seed"]) + ARM_SALT.get(arm, 1) * 1009)
    ticks = int(cfg.get("ticks", 6))
    plan = tick_plan(ticks, int(cfg.get("tool_every", 3)), cfg.get("drift_tick"), int(cfg.get("day_ticks", 3)))
    used: set[str] = set()
    tools = build_tools(
        int(cfg["seed"]),
        int(cfg.get("new_tools_per_day", 2)),
        day=0,
        used=used,
        pair=True,
        kind="number",
    )
    buffer = EpisodicBuffer(int(cfg.get("buffer_limit", 64)))
    solutions: list[dict] = []
    exams: list[dict] = []
    book = Census()
    births: dict[str, int] = {tool["name"]: int(tool.get("day", 0)) for tool in tools}
    opt_steps = 0
    budget = int(cfg.get("max_opt_steps", 8))
    consecutive_failures = 0
    recent_successes = 0
    last_commit = -10**9
    safety_checks = 0
    safety_fails = 0
    infer_tokens = 0
    drifted_name = None
    drift_at = None
    recovery = None
    ledger = Ledger()
    ident = Identity(cfg.get("gene"))
    grants = set(cfg.get("grants") or ["python"])
    checker = CheckerTrust()
    writes = {"fast": 0, "slot": 0, "core": 0}
    sidecar = FastSidecar(evo, scale=float(cfg.get("fast_scale", 0.02))) if _uses_fast(arm) else None
    serve = {"name": None if arm in ("agent", "oracle") else "policy"}

    def refresh_serve() -> None:
        if arm in ("agent", "oracle"):
            serve["name"] = None
            return
        try:
            serve["name"] = blend_adapters(evo, "policy", "memory", dest="serve")
        except (RuntimeError, KeyError, ValueError, TypeError):
            serve["name"] = "policy"
    mode = "sft" if arm == "continual_sft" else "onpolicy"
    timeout = float(cfg.get("exec_timeout", 2.0))
    (run.dir / "workspace" / arm).mkdir(parents=True, exist_ok=True)

    def notes_for(task, error):
        docs = tool_docs(tools)
        if arm == "agent":
            return agent_notes(task, docs, solutions, error)
        if arm == "oracle":
            return oracle_notes(task, docs, solutions, error)
        return ""

    def play(tasks, record: bool):
        nonlocal infer_tokens, safety_checks, safety_fails, consecutive_failures, recent_successes
        rows = []
        if sidecar is not None:
            sidecar.off()
        for task in tasks:
            if sidecar is not None and task.get("split") != "exam":
                sidecar.on()
            else:
                if sidecar is not None:
                    sidecar.off()
            row = attempt(
                evo,
                task,
                tools,
                cfg,
                adapter=serve["name"],
                notes=lambda error, task=task: notes_for(task, error),
                workspace=run.dir / "workspace" / arm,
                max_turns=int(cfg.get("max_turns", 1)),
                sidecar=sidecar if task.get("split") != "exam" else None,
                admit=lambda code, grants=grants: denied(code, grants),
            )
            rows.append(row)
            infer_tokens += int(row.get("prompt_tokens") or 0)
            code = (row["trace"][-1].get("code") if row.get("trace") else "") or ""
            safety_checks += 1
            if not anchors_hold([code]):
                safety_fails += 1
            if task.get("split") != "exam":
                claim = literal_claim(code)
                proposed = None
                if claim is not None and row.get("trace"):
                    proposed = str(row["trace"][-1].get("value")) == claim
                    checker.observe(bool(row["ok"]), proposed)
                counted = checker.reward(bool(row["ok"]), proposed) >= 1.0
                if row["ok"]:
                    consecutive_failures = 0
                    if counted:
                        recent_successes += 1
                        ledger.note_practice(list(task.get("tools") or []), True)
                        ident.remember(task["prompt"], code, list(task.get("tools") or []), task.get("split") or "practice")
                    if arm in ("agent", "oracle") and record:
                        remember_solution(solutions, task, code)
                else:
                    consecutive_failures += 1
                    recent_successes = 0
                buffer.add(
                    Episode(
                        task["prompt"],
                        code,
                        row["ok"],
                        list(task.get("tools") or []),
                        plan_tick,
                        task.get("split") or "practice",
                        expect=task.get("expect"),
                        kind=task.get("kind") or "call",
                    )
                )
        return rows

    def canary_rate(adapter: str) -> float:
        picked = pick_canaries(exams, int(cfg.get("canary_size", 1)), canary_rng)
        if not picked:
            return 1.0
        if sidecar is not None:
            sidecar.off()
        rows = []
        for task in picked:
            rows.append(
                attempt(
                    evo,
                    task,
                    tools,
                    cfg,
                    adapter=adapter,
                    notes="",
                    workspace=run.dir / "workspace" / arm,
                    max_turns=1,
                    sidecar=None,
                )
            )
        return sum(1.0 for row in rows if row["ok"]) / len(rows)

    def spend(train, live: str = "policy") -> dict:
        nonlocal opt_steps, last_commit
        if opt_steps >= budget:
            return {"kept": False, "steps": 0}
        result = run_shadow(
            evo,
            run,
            live,
            train,
            canary_rate,
            cfg,
            {"arm": arm, "opt_steps": opt_steps, "live": live},
        )
        opt_steps += int(result["steps"])
        if result["kept"]:
            last_commit = plan_tick
            refresh_serve()
        return result

    refresh_serve()
    plan_tick = 0
    for event in plan:
        plan_tick = int(event["tick"])
        if event["new_tool"]:
            fresh = build_tools(int(cfg["seed"]) + 17, 1, day=plan_tick, used=used, kind="number")
            tools.extend(fresh)
            for tool in fresh:
                births[tool["name"]] = plan_tick
        if event["drift"]:
            changed = drift_oldest(tools)
            if changed is not None:
                drifted_name = changed["name"]
                drift_at = plan_tick
                refresh_expects(exams, tools, timeout)
                ledger.forget(changed["name"])
                if _learns(arm) and opt_steps < budget:
                    pairs = drift_pairs(changed)

                    def _train_drift(adapter, pairs=pairs):
                        if sidecar is not None:
                            sidecar.off()
                        return sft_update(evo, pairs, cfg, adapter)

                    spend(_train_drift)
        if event["exam"]:
            focus = tools[-int(cfg.get("new_tools_per_day", 2)) :]
            bundle = day_bundle(plan_tick, tools, focus, "single", cfg, world)
            exams.extend(bundle["exam"])
            rows = play(bundle["exam"], record=False)
            for row in rows:
                ledger.note_exam(list(row["task"].get("tools") or []), bool(row["ok"]))
            book.add(plan_tick, arm, rows)
            if drifted_name is not None and recovery is None:
                hit = [row for row in rows if drifted_name in (row["task"].get("tools") or []) and row["ok"]]
                if hit and drift_at is not None:
                    recovery = plan_tick - drift_at
        focus = [tools[plan_tick % len(tools)]]
        practice = make_task("practice", plan_tick, plan_tick, tools, focus, "single", timeout, world)
        play([practice], record=True)
        if not _learns(arm) or opt_steps >= budget:
            continue
        if arm == "shift":
            if event["shift_flush"]:
                ready = buffer.successes()[-int(cfg.get("flush_limit", 4)) :]

                def _train_shift(adapter, ready=ready):
                    if sidecar is not None:
                        sidecar.off()
                    steps = 0
                    codes = []
                    for row in ready:
                        if opt_steps + steps >= budget:
                            break
                        task = {
                            "prompt": row.prompt,
                            "expect": row.expect,
                            "kind": row.kind,
                            "tools": row.tools,
                            "split": "practice",
                        }
                        if mode == "sft":
                            stats = sft_update(evo, [(row.prompt, row.code)], cfg, adapter)
                        else:
                            stats = onpolicy_update(evo, task, tools, cfg, adapter, "")
                        steps += int(stats["steps"])
                        codes.extend(stats.get("codes") or [])
                    return {"steps": steps, "codes": codes}

                spend(_train_shift)
            continue
        choice = decide(
            {
                "tick": plan_tick,
                "opt_steps": opt_steps,
                "max_opt_steps": budget,
                "last_commit_tick": last_commit,
                "consecutive_failures": consecutive_failures,
                "buffer_size": len(buffer),
                "recent_successes": recent_successes,
            },
            cfg.get("gene"),
        )
        if choice is None:
            continue
        target = practice
        names = list(target.get("tools") or [])
        if choice == "teacher":
            level = "slot"
        else:
            level = ledger.destination(names, cfg.get("ladder"))
            if level == "fast":
                writes["fast"] += 1
                recent_successes = 0
                continue

        def _train_online(adapter, target=target, choice=choice):
            if sidecar is not None:
                sidecar.off()
            docs = tool_docs(tools)
            teacher = ""
            if choice == "teacher":
                teacher = oracle_notes(target, docs, solutions, "")
            if mode == "sft":
                pairs = [(row.prompt, row.code) for row in buffer.successes()[-2:]]
                if choice == "teacher" and not pairs:
                    from evo.generate import generate
                    from evo.world.body import extract_code, task_prompt

                    reply = generate(evo, task_prompt(target, "", teacher), int(cfg.get("max_new_code", 80)), 0.0, adapter)
                    code = extract_code(reply)
                    pairs = [(target["prompt"], code)] if code else []
                return sft_update(evo, pairs, cfg, adapter)
            return onpolicy_update(evo, target, tools, cfg, adapter, teacher)

        # A scaffold lesson stays in the skill adapter. Only a skill that later
        # exams still pass is allowed to move the slow core.
        live = "memory" if level == "core" else "policy"
        result = spend(_train_online, live)
        if result.get("kept"):
            writes[level] += 1
            if level == "slot":
                ledger.mark_slot(names)
        recent_successes = 0

    report = book.report(arm, ticks, births)
    ok_tokens = [
        event["tokens"]
        for event in book.events
        if event["actor"] == arm and event["ok"]
    ]
    items = [{"id": event["id"], "ok": bool(event["ok"])} for event in book.events if event["actor"] == arm]
    leaked = buffer.exam_leak({task["prompt"] for task in exams})
    if _learns(arm):
        ident.take(ledger)
        ident.save(run.dir / f"identity_{arm}.json")
    if sidecar is not None:
        sidecar.close()
    return {
        "arm": arm,
        "opt_steps": opt_steps,
        "alive": report["alive"],
        "forgotten": report["forgotten"],
        "mastery": report["mastery"],
        "tokens_per_ok": (sum(ok_tokens) / len(ok_tokens)) if ok_tokens else None,
        "infer_tokens": infer_tokens,
        "train_tokens": opt_steps * int(cfg.get("max_seq_len", 384)),
        "exam_items": items,
        "safety_checks": safety_checks,
        "safety_fails": safety_fails,
        "drift_recovery": recovery,
        "exam_leak": leaked,
        "writes": writes,
        "verifier": "executor" if not checker.trusted() else "calibrated",
    }
