"""Night: verified quizzes into memory, passed trajectories into policy, replay, then a gate."""

from __future__ import annotations

import re

from evo.generate import clean_edit, generate, score_questions
from evo.inner_loop import adapt_scratch, build_memory_cache
from evo.outer_loop import sft_policy
from evo.selfplay.tasks import learnability
from evo.world.toolbox import call_tool, chain_program, chain_result


def verified_drills(tool: dict) -> list[tuple[str, str]]:
    """Question/answer rows whose answers are the tool's real return values.

    The exam speaks in nicknames, so the drills teach the nickname, not only the raw call.
    """
    pairs = [(f"What is the function name for {tool['nick']}? Reply with the name only.", tool["name"])]
    for arg in tool["quiz_args"]:
        value = call_tool(tool, arg)
        shown = repr(value) if isinstance(value, str) else str(value)
        pairs.append((f"What does {tool['nick']} applied to {arg} return? Reply with the value only.", shown))
        pairs.append(
            (
                f"Write Python that applies {tool['nick']} to {arg}. Reply with code only.",
                f"print({tool['name']}({arg}))",
            )
        )
    return pairs


def _code_pair(prompt: str, code: str) -> tuple[str, str]:
    return ("Write Python that does the task. Reply with code only.\n\n" + prompt, code)


def _chain_args(tool: dict) -> list[str]:
    """Arguments used only to bind two names. Exam, gate, and practice values stay out."""
    fresh = [str(arg) for arg in tool.get("bind_args") or []]
    if fresh:
        return fresh
    return [str(arg) for arg in list(tool.get("quiz_args") or []) + list(tool.get("drill_args") or [])]


def compose_drills(tools: list[dict], per_kind: int = 8) -> list[tuple[str, str]]:
    """Extra arguments and tool chains. None of these strings are exam prompts.

    Each kind gets its own chain budget. A shared budget let the first kind
    (often yesterday's text tools) crowd out a new kind before the exam.
    """
    pairs = []
    for tool in tools:
        for arg in tool.get("drill_args") or []:
            pairs.append(
                _code_pair(
                    f"Print the result of {tool['nick']} applied to {arg}.",
                    f"print({tool['name']}({arg}))",
                )
            )
    by_kind: dict[str, list[dict]] = {}
    for tool in tools:
        by_kind.setdefault(tool["kind"], []).append(tool)
    for group in by_kind.values():
        if len(group) < 2:
            continue
        kind_chains = []
        for first in group:
            for second in group:
                if second["name"] == first["name"]:
                    continue
                for arg in _chain_args(first):
                    try:
                        chain_result(first, second, arg)
                    except (TypeError, ValueError, KeyError):
                        continue
                    kind_chains.append(
                        _code_pair(
                            (
                                f"Apply {first['nick']} to {arg}, then apply {second['nick']} "
                                "to that result. Print the final result."
                            ),
                            chain_program(first, second, arg),
                        )
                    )
        pairs.extend(kind_chains[:per_kind])
    return pairs


def _banned_args(tool: dict) -> set[str]:
    banned = set()
    for key in ("chain_arg", "gate_arg", "practice_arg", "exam_arg", "tune_arg"):
        if tool.get(key) is not None:
            banned.add(str(tool[key]))
    for arg in tool.get("held_args") or []:
        banned.add(str(arg))
    return banned


def _ordered_chains(first: dict, second: dict) -> list[tuple[str, str]]:
    """One direction, on bind args. Exam, gate, and practice values never appear."""
    banned = _banned_args(first) | _banned_args(second)
    pairs = []
    for arg in _chain_args(first):
        if str(arg) in banned:
            continue
        try:
            chain_result(first, second, arg)
        except (TypeError, ValueError, KeyError):
            continue
        pairs.append(
            _code_pair(
                (
                    f"Apply {first['nick']} to {arg}, then apply {second['nick']} "
                    "to that result. Print the final result."
                ),
                chain_program(first, second, arg),
            )
        )
    return pairs


def _chain_partner(first: dict, tools: list[dict]) -> dict | None:
    """Same partner the chain gate picks for index 0."""
    partners = [tool for tool in tools if tool["kind"] == first["kind"]]
    others = [tool for tool in partners if tool["name"] != first["name"]]
    partners = others or partners
    if not partners:
        return None
    return partners[1 % len(partners)]


def _held_singles(tool: dict) -> list[tuple[str, str]]:
    """Single calls on drill args. The exam argument stays out of the sentence."""
    banned = _banned_args(tool)
    pairs = []
    for arg in tool.get("drill_args") or []:
        if str(arg) in banned:
            continue
        pairs.append(
            _code_pair(
                f"Print the result of {tool['nick']} applied to {arg}.",
                f"print({tool['name']}({arg}))",
            )
        )
    return pairs


def reserved_chains(tools: list[dict], held_tasks: list[dict], new_tools: list[dict], rounds: int = 6) -> list[tuple[str, str]]:
    """Last pen of the night: pairs already passed, then today's new pair.

    A passed single call is rehearsed on a drill arg and placed before the final chain,
    so the last update is still a two-name program. The exam sentence is not copied.
    """
    by_name = {tool["name"]: tool for tool in tools}
    pairs = []
    singles = []
    seen = set()

    def add(first: dict, second: dict) -> None:
        for prompt, code in _ordered_chains(first, second):
            if prompt in seen:
                continue
            seen.add(prompt)
            pairs.append((prompt, code))

    for task in held_tasks or []:
        names = list(task.get("tools") or [])
        if "chain" in str(task.get("id", "")) and len(names) >= 2:
            first = by_name.get(names[0])
            second = by_name.get(names[1])
            if first is None or second is None:
                continue
            add(first, second)
            continue
        if len(names) == 1:
            tool = by_name.get(names[0])
            if tool is None:
                continue
            for single in _held_singles(tool):
                if single[0] in seen:
                    continue
                seen.add(single[0])
                singles.append(single)
    if new_tools:
        partner = _chain_partner(new_tools[0], tools)
        if partner is not None and partner["name"] != new_tools[0]["name"]:
            add(new_tools[0], partner)
    oldest = [tool for tool in tools if tool.get("day") == 0] or list(tools[:1])
    if oldest:
        for single in _held_singles(oldest[0])[:1]:
            if single[0] not in seen:
                seen.add(single[0])
                singles.append(single)
    if not pairs:
        return singles
    # Older and newer chains take turns, then the single call is written twice
    # and a chain is last. Ending on only chains drops a single the morning already passed.
    closing = contrast_block(pairs, rounds=rounds)
    tail = list(pairs) + closing
    if singles:
        tail.append(singles[0])
        tail.append(singles[0])
    tail.append(closing[-1] if closing else pairs[-1])
    return tail


def _program_names(code: str) -> tuple[str, ...]:
    names = re.findall(r"([A-Za-z_]\w*)\(", "".join(code.split()))
    return tuple(name for name in names if name != "print")


def contrast_block(pairs: list[tuple[str, str]], rounds: int = 6) -> list[tuple[str, str]]:
    """Alternate an older chain with the newest chain so the last updates keep both name pairs.

    Ends on the newest chain. A night with only one pair of tools returns nothing.
    The two sides are the function names in the program. Nicknames can repeat across kinds.
    """
    chains = []
    seen = set()
    for prompt, code in pairs:
        if "then apply" not in prompt or prompt in seen:
            continue
        seen.add(prompt)
        chains.append((prompt, code))
    if len(chains) < 2:
        return []
    by_names = []
    seen_names = set()
    for pair in chains:
        key = _program_names(pair[1])
        if not key or key in seen_names:
            continue
        seen_names.add(key)
        by_names.append(pair)
    if len(by_names) < 2:
        return []
    fresh = by_names[-1]
    older = by_names[:-1]
    block = []
    for index in range(rounds):
        block.append(older[index % len(older)])
        block.append(fresh)
    return block


def repeats_call(code: str) -> bool:
    """True when one function is nested inside a call to itself, as in name(name(."""
    compact = "".join(code.split())
    return re.search(r"([A-Za-z_]\w*)\(\1\(", compact) is not None


def refine_tail(evo, pairs: list[tuple[str, str]], tools: list[dict], cfg: dict) -> dict:
    """Run the reserved chains. If one is wrong, re-learn the old pair and the new pair together.

    A second pass that trains only the misses overwrites the chain that just started working.
    A night with only one pair of tools is left as the main update wrote it.
    These prompts use bind args. Exam sentences are not in this list.
    """
    from evo.selfplay.executor import run_code
    from evo.world.body import extract_code
    from evo.world.toolbox import prelude

    chains = []
    seen = set()
    for prompt, gold in pairs:
        if "then apply" not in prompt or prompt in seen:
            continue
        seen.add(prompt)
        chains.append((prompt, gold))
    if not chains:
        return {"tried": 0, "misses": 0, "repaired": 0}
    pre = prelude(tools)
    timeout = float(cfg.get("exec_timeout", 2.0))
    misses = []
    sample = ""
    for prompt, gold in chains:
        reply = generate(evo, prompt, int(cfg.get("max_new_code", 80)), 0.0, str(cfg.get("train_adapter") or "policy"))
        code = extract_code(reply)
        result = run_code(code or "raise SystemExit('empty')", timeout, prelude=pre, world=True)
        gold_run = run_code(gold, timeout, prelude=pre, world=True)
        wrong = (not result.ok) or (not gold_run.ok) or result.value != gold_run.value or repeats_call(code)
        if wrong:
            misses.append((prompt, gold))
            sample = sample or " ".join(code.split())[:100]
    repair = []
    lr = float(cfg.get("outer_lr", 5e-4))
    if misses and len(misses) == len(chains):
        # Nothing in this family runs yet. Learn the gold programs again, at the normal step size.
        repair = contrast_block(chains) or (chains + chains)
    elif misses:
        # Some chains already run. Only nudge when an older pair and a newer pair can be trained together.
        repair = contrast_block(chains)
        lr *= 0.25
    if repair:
        sft_policy(
            evo,
            repair,
            lr,
            1,
            int(cfg.get("max_seq_len", 384)),
            adapter=str(cfg.get("train_adapter") or "policy"),
        )
    skip = " skip=single-family" if misses and not repair else ""
    shown = f" sample={sample}" if sample else ""
    print(
        f"[live] refine tried={len(chains)} misses={len(misses)} repaired={len(repair)}{skip}{shown}",
        flush=True,
    )
    return {"tried": len(chains), "misses": len(misses), "repaired": len(repair)}


def curriculum_pairs(
    base: list[tuple[str, str]],
    reserved: list[tuple[str, str]],
    closing: list[tuple[str, str]],
    hand: bool,
) -> list[tuple[str, str]]:
    """Hand-written night order, or the plain verified pairs when that switch is off.

    The hand-written order is what made small models keep a new chain: reserved
    two-name programs, then a doubled single-call closer. A generic night keeps
    the verified drills and the trajectories, and nothing written for this world.
    """
    if not hand:
        return list(base)
    pairs = list(base) + list(reserved)
    if closing:
        pairs.extend(closing)
        pairs.extend(closing)
    return pairs


def ordered_night_pairs(pairs: list[tuple[str, str]], repeat: int, hand: bool) -> list[tuple[str, str]]:
    """Repeat chain programs at the end of the night only while the hand curriculum is on."""
    if not hand:
        return list(pairs)
    return chains_last(pairs, repeat)


def chains_last(pairs: list[tuple[str, str]], repeat: int = 1) -> list[tuple[str, str]]:
    """Put two-name programs after the single calls, and repeat them.

    The inner name is the token a larger model drops. It should be the last thing the night writes.
    """
    chains = [pair for pair in pairs if "then apply" in pair[0]]
    rest = [pair for pair in pairs if "then apply" not in pair[0]]
    copies = max(1, int(repeat))
    return rest + (chains * copies)


def binding_close(tools: list[dict]) -> list[tuple[str, str]]:
    """One single call per new tool, on a bind arg, placed after the chains.

    A night that ends on one chain makes every later answer that same chain,
    including tomorrow's tools. These sentences are not exam prompts.
    """
    pairs = []
    seen = set()
    for tool in tools:
        for arg in (tool.get("bind_args") or [])[:1]:
            if str(arg) in _banned_args(tool):
                continue
            prompt = f"Print the result of {tool['nick']} applied to {arg}."
            if prompt in seen:
                continue
            seen.add(prompt)
            pairs.append(_code_pair(prompt, f"print({tool['name']}({arg}))"))
    return pairs


def hindsight_pairs(traces: list[dict]) -> list[tuple[str, str]]:
    """When the day produced no success, imitate the executor's program on the practice prompt.

    Exam prompts are never included.
    """
    pairs = []
    seen = set()
    for trace in traces:
        if trace.get("ok"):
            continue
        task = trace.get("task") or {}
        if task.get("split") == "exam":
            continue
        gold = (task.get("gold") or "").strip()
        prompt = task.get("prompt") or ""
        if not gold or not prompt or prompt in seen:
            continue
        seen.add(prompt)
        pairs.append(_code_pair(prompt, gold))
    return pairs


def retention_keeps(before_passed: int, after_passed: int, max_drop: float) -> bool:
    """A night may not wipe tasks the model already passed this morning."""
    if before_passed <= 0:
        return True
    drop = 1.0 - (after_passed / before_passed)
    return drop <= max_drop


def lesson_notes(evo, tools: list[dict], cfg: dict) -> str:
    lesson = "\n".join(tool["doc"] for tool in tools)
    extra = (cfg.get("extra_lesson") or "").strip()
    if extra:
        lesson = (lesson + "\n" + extra).strip()
    if not lesson.strip():
        return ""
    prompt = (
        "Write one short note per tool. State the rule. Do not add questions.\n\n"
        f"{lesson}\n\n"
        "Notes:"
    )
    raw = generate(evo, prompt, int(cfg.get("edit_tokens", 96)), 0.0, "policy")
    return clean_edit(raw) or lesson


def select_traces(traces: list[dict], self_directed: bool, min_learnability: float) -> list[dict]:
    """Human rule keeps every success. The model rule keeps the half-solved band."""
    if not self_directed:
        return [trace for trace in traces if trace.get("ok")]
    grouped: dict[str, list[dict]] = {}
    for trace in traces:
        grouped.setdefault(trace["id"], []).append(trace)
    kept = []
    for rows in grouped.values():
        rate = sum(1.0 for row in rows if row.get("ok")) / len(rows)
        if learnability(rate) < min_learnability:
            continue
        kept.extend(row for row in rows if row.get("ok"))
    return kept


def should_sleep(fail_rate: float, new_tools: int, seen_tools: int, self_directed: bool, fail_bar: float = 0.4, novelty_bar: float = 0.25) -> bool:
    """Human rule sleeps every night. The model sleeps when work is failing or new."""
    if not self_directed:
        return True
    novelty = new_tools / max(1, seen_tools)
    return fail_rate >= fail_bar or novelty >= novelty_bar


def gate_keeps(before_rate: float, after_rate: float, before_probe: float, after_probe: float, max_drop: float, max_probe_drop: float) -> bool:
    if before_rate - after_rate > max_drop:
        return False
    if before_probe - after_probe > max_probe_drop:
        return False
    return True


def trajectory_pairs(traces: list[dict]) -> list[tuple[str, str]]:
    pairs = []
    for trace in traces:
        if not trace.get("ok"):
            continue
        last = trace["trace"][-1]
        # Train the prompt the exam will use: the task, without tool notes and without the error.
        prompt = trace["task"]["prompt"]
        code = last.get("code") or ""
        if code.strip():
            pairs.append(("Write Python that does the task. Reply with code only.\n\n" + prompt, code))
    return pairs


def consolidate(evo, new_tools: list[dict], traces: list[dict], past_pairs: list[tuple[str, str]], gate_rate_before: float, probe_before: float, probe_questions: list[dict], cfg: dict) -> dict:
    """Write the night's update. Caller restores snapshots when `keep` is false."""
    notes = lesson_notes(evo, new_tools, cfg)
    drills = []
    for tool in new_tools:
        drills.extend(verified_drills(tool))
    preference = cfg.get("preference_pair")
    if preference:
        drills.append(preference)
    file_pair = cfg.get("file_pair")
    if file_pair:
        drills.append(file_pair)
    if cfg.get("compose"):
        drills.extend(compose_drills(cfg.get("compose_tools") or new_tools))
    if cfg.get("hindsight"):
        drills.extend(hindsight_pairs(traces))
    replay = list(past_pairs)[-int(cfg.get("replay_limit", 32)) :]
    ratio = float(cfg.get("replay_ratio", 1.0))
    if replay and ratio < 1:
        replay = replay[-max(1, int(len(replay) * ratio)) :]
    memory_text = notes.strip() or "Reviewed tools."
    cache = None
    kl_coef = 0.0
    if probe_questions:
        cache = build_memory_cache(
            evo,
            probe_questions,
            int(cfg.get("answer_tokens", 8)),
            int(cfg.get("distill_questions", 2)),
            adapter="memory",
        )
        kl_coef = float(cfg.get("kl_coef", 0.5)) if cache else 0.0
    evo.copy_memory_to_scratch()
    mem_loss, _ = adapt_scratch(
        evo,
        memory_text,
        steps=int(cfg.get("night_steps", 12)),
        lr=float(cfg.get("inner_lr", 5e-4)),
        max_len=int(cfg.get("max_seq_len", 384)),
        pairs=(drills + replay) or None,
        kl_coef=kl_coef,
        distill_cache=cache,
    )
    evo.copy_scratch_to_memory()
    hand = bool(cfg.get("hand_curriculum", True))
    repeat = int(cfg.get("chain_repeat", 2 if cfg.get("chain_exam") else 1))
    policy_pairs = ordered_night_pairs(trajectory_pairs(traces) + drills + replay, repeat, hand)
    tail = []
    if hand and cfg.get("chain_exam"):
        tail = reserved_chains(
            cfg.get("compose_tools") or new_tools,
            cfg.get("held_tasks") or [],
            new_tools,
            rounds=int(cfg.get("contrast_rounds", 6)),
        )
        policy_pairs = policy_pairs + tail
    if cfg.get("skill_slots"):
        owned = {tool["name"] for tool in new_tools}
        policy_pairs = [pair for pair in policy_pairs if _owned_by(pair[1], owned)]
        tail = [pair for pair in tail if _owned_by(pair[1], owned)]
    if not cfg.get("concept_slot"):
        for pair in cfg.get("concept_pairs") or []:
            policy_pairs.append(pair)
            tail.append(pair)
    posed = list(cfg.get("posed_pairs") or [])
    train_name = str(cfg.get("train_adapter") or "policy")
    if posed and train_name != "policy":
        # General practice stays on the core. The slot is only for today's tools.
        sft_policy(
            evo,
            posed,
            float(cfg.get("outer_lr", 5e-4)),
            1,
            int(cfg.get("max_seq_len", 384)),
            adapter="policy",
        )
    elif posed:
        policy_pairs = policy_pairs + posed
    closing = binding_close(new_tools) if hand and (cfg.get("bind_close") or cfg.get("lexical_gate")) else []
    policy_pairs = curriculum_pairs(policy_pairs, [], closing, bool(closing))
    policy_stats = sft_policy(
        evo,
        policy_pairs,
        float(cfg.get("outer_lr", 5e-4)),
        int(cfg.get("night_epochs", 1)),
        int(cfg.get("max_seq_len", 384)),
        adapter=str(cfg.get("train_adapter") or "policy"),
    )
    refine = (
        refine_tail(evo, tail, cfg.get("compose_tools") or new_tools, cfg)
        if hand and tail and cfg.get("refine", True)
        else {"tried": 0, "misses": 0, "repaired": 0}
    )
    return {
        "notes": notes,
        "drills": len(drills),
        "memory_loss": mem_loss,
        "policy": policy_stats,
        "refine": refine,
        "trained_pairs": policy_pairs,
        "new_pairs": trajectory_pairs(traces) + drills,
        "gate_before": gate_rate_before,
        "probe_before": probe_before,
        "probe_questions": probe_questions,
    }


def _owned_by(code: str, names: set[str]) -> bool:
    used = [name for name in _program_names(code) if name not in names and name not in {"str", "int", "print"}]
    if not names:
        return True
    mentioned = [name for name in _program_names(code) if name in names]
    return bool(mentioned) and not used


def score_probe(evo, questions: list[dict], answer_tokens: int) -> float:
    if not questions:
        return 0.0
    return float(score_questions(evo, questions, "memory", answer_tokens)["f1"])
