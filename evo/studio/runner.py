"""Run one office span and stream the session events. No new gate is scored here."""

from __future__ import annotations

from pathlib import Path

from evo.office.families import FAMILIES, make_task
from evo.office.stream import _license, _notes, _pack, _reply, zipf_plan
from evo.session.organism import OrganismSession
from evo.util import repo_path


FAMILY_COPY = {
    "table": "表格。读进来，按条件合计，把结果写出去。",
    "file": "文件。按规则搬动或改名。",
    "report": "报告。把算出来的数字写进说明。",
    "shell": "命令行。只放行 mkdir、dir、type、copy。",
    "http": "本机接口。带令牌、分页，也会改名。",
    "mixed": "几步连着做完。",
}

ARM_COPY = [
    {"id": "agent", "title": "agent", "text": "权重不动。提示里只有一句工具格式，外加同一类工作上次做对的短动作。"},
    {"id": "oracle", "title": "oracle", "text": "权重不动。参考解法直接放进提示，用来看上限，不是模型自己会了。"},
    {"id": "shift", "title": "shift", "text": "倒班。做完一段再批量写进技能槽。"},
    {"id": "continual", "title": "continual", "text": "做对就写。不看回本，也不等夜里。"},
    {"id": "dual", "title": "dual", "text": "双节律。白天攒够同类成功，再过三道闸：账本、回本、分拣。夜里交错重放。"},
    {"id": "dual_agent", "title": "dual_agent", "text": "和 dual 同一套写入，提示里仍留着检索到的短动作。"},
    {"id": "continual_sft", "title": "continual_sft", "text": "只学做对的样本，当场写进技能槽。"},
]


def model_paths() -> list[dict]:
    from evo.registry import list_models

    return list_models()


def span_plan(family: str, span: str, seed: int) -> list[dict]:
    if family not in FAMILIES:
        family = "table"
    if span == "day":
        return zipf_plan(4, [family], seed, None, 0)
    return [{"index": 0, "family": family, "kind": "draw", "variant": 0, "drift": False, "exam": False}]


def run_span(spec: dict, bus, evo=None, workspace: Path | None = None) -> OrganismSession:
    """One arm. `span` is `task` (one item) or `day` (four items on one family)."""
    actor = spec.get("actor") or "reference"
    family = spec.get("family") or "table"
    arm = spec.get("arm") or "dual"
    seed = int(spec.get("seed") or 0)
    span = spec.get("span") or "task"
    label = "标准答案在演示身体该怎么动" if actor == "reference" else "现场模型，做对做错都留下"
    bus.emit(
        "meta",
        {
            "source": "live",
            "actor": actor,
            "actor_label": label,
            "arm": arm,
            "family": family,
            "span": span,
            "honest": True,
            "model": spec.get("model"),
        },
    )
    cfg = {
        "actor": actor,
        "day_after": 2,
        "day_ticks": 4,
        "day_budget": 8,
        "absorb_train_tokens": 800,
        "max_steps": 4 if actor == "model" else 6,
        "exec_timeout": 12 if actor == "model" else 8,
        "max_new_code": 120,
        "max_seq_len": 1024,
        "difficulty": 1,
        "grants": ["python", "shell", "read", "write", "http"],
        "packs": ["orders"],
        "seed": seed,
        "train_tokens_each": 0,
    }
    plan = span_plan(family, span, seed)
    pack = _pack(cfg, seed)
    root = workspace or (repo_path("tmp") / "studio" / str(spec.get("run_id") or "live"))
    session = OrganismSession(arm, cfg, evo, license=_license(cfg), bus=bus)
    for step in plan:
        drift = "paginate" if step["drift"] else None
        chosen = step["family"] if step["family"] in FAMILIES else "table"
        variant = 0 if chosen in ("shell", "http", "mixed") else int(step["variant"])
        task = make_task(pack, chosen, seed + step["index"], variant=variant, difficulty=1, drift=drift)
        task["split"] = "exam" if step["exam"] else "practice"
        notes = _notes(arm, task, session.bank)
        task["_notes_len"] = len(notes)
        if notes:
            task["prompt"] = task["prompt"] + "\n\n" + notes
        reply = _reply(arm, task, cfg, evo)
        desk = root / f"{arm}-{step['index']}"
        if desk.exists():
            import shutil

            shutil.rmtree(desk, ignore_errors=True)
        desk.mkdir(parents=True, exist_ok=True)
        session.step(task, step, reply, desk)
    session.finish(plan)
    return session


def _ok_rate(session: OrganismSession):
    flags = [bool(item["ok"]) for item in session.exam_items]
    if not flags:
        flags = list(session.practice_flags)
    if not flags:
        return None
    return sum(1 for flag in flags if flag) / len(flags)


def model_config(size: str) -> dict:
    from evo.registry import PRIMARY, is_ready, resolve

    # Default / legacy 0.8B alias -> primary 1.5B. Optional 2B only when ready.
    alias = {"0.8B": "1.5B", "1.5B": "1.5B", "2B": "2B"}.get(size, "1.5B")
    primary = resolve(PRIMARY)
    optional = resolve("Qwen3.5-2B")
    if alias == "2B" and is_ready(optional):
        name, chosen = str(optional), "2B"
    else:
        name, chosen = str(primary), "1.5B"
    return {
        "model_name": name,
        "model_size": chosen,
        "seed": 0,
        "lora_rank": 8,
        "lora_alpha": 16,
        "lora_dropout": 0.0,
        "lora_preset": "full",
        "max_seq_len": 1024,
        "max_new_code": 120,
        "inner_lr": 5e-4,
        "outer_lr": 5e-4,
        "exec_timeout": 12,
        "temperature": 0.0,
    }
