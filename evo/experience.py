"""A short local demo: one self-edit, then one executor-checked program."""

from __future__ import annotations

from pathlib import Path

from evo.eval.scoring import score_prediction
from evo.generate import blind_edit_prompt, clean_edit, first_line, generate, qa_prompt
from evo.inner_loop import adapt_scratch
from evo.model import build_model, release
from evo.selfplay.executor import execute_solve
from evo.selfplay.tasks import check_solver, materialize, solver_prompt
from evo.util import repo_path, set_seed


DEMO_FACT = "The fictitious alloy brinium melts at 451 degrees and was first refined in 1888."
DEMO_QUESTIONS = [
    {
        "question": "At what temperature does brinium melt?",
        "answers": ["451 degrees", "451"],
    },
    {
        "question": "When was brinium first refined?",
        "answers": ["1888"],
    },
]
DEMO_PROGRAM = "def solve(x):\n    return x * 3\n"
DEMO_INPUT = "4"


def run_experience(cfg: dict, fact: str, questions: list[dict], steps: int, lr: float) -> dict:
    set_seed(cfg["seed"])
    evo = None
    try:
        evo = build_model(cfg)
        before = [_ask(evo, item) for item in questions]
        passage = {"context": fact, "qas": questions}
        raw_edit = generate(
            evo,
            blind_edit_prompt(passage),
            cfg.get("edit_tokens", 96),
            0.0,
            "memory",
        )
        edit = clean_edit(raw_edit) or fact
        notes = edit
        bound = _train_text(edit, questions)
        memory_at_start = evo.snapshot("memory")
        scratch_at_start = evo.snapshot("scratch")
        notes_only = _fit(evo, notes, steps, lr, cfg, questions)
        evo.restore("memory", memory_at_start)
        evo.restore("scratch", scratch_at_start)
        notes_answers = _fit(evo, bound, steps, lr, cfg, questions)
        code = _code_check(evo, cfg)
        report = {
            "model": cfg["model_name"],
            "fact": fact,
            "edit": edit,
            "trained": bound,
            "raw_edit": raw_edit,
            "steps": steps,
            "lr": lr,
            "loss": notes_answers["loss"],
            "trainable": notes_answers["trainable"],
            "before": before,
            "after": notes_answers["after"],
            "notes_only": notes_only,
            "notes_answers": notes_answers,
            "code": code,
            "vram_mb": evo.vram_mb(),
        }
        path = _write(report)
        _print(report, path)
        return report
    finally:
        release(evo)


def _fit(evo, text: str, steps: int, lr: float, cfg: dict, questions: list[dict]) -> dict:
    evo.reset_scratch()
    loss, trainable = adapt_scratch(
        evo,
        text,
        steps=steps,
        lr=lr,
        max_len=cfg["max_seq_len"],
    )
    evo.copy_scratch_to_memory()
    after = [_ask(evo, item) for item in questions]
    return {"loss": loss, "trainable": trainable, "after": after, "text": text}


def _train_text(edit: str, questions: list[dict]) -> str:
    lines = [edit, ""]
    for item in questions:
        answers = item.get("answers") or []
        if not answers:
            continue
        lines.append(f"Question: {item['question']}")
        lines.append(f"Answer: {answers[0]}")
        lines.append("")
    return "\n".join(lines).strip()


def _ask(evo, item: dict) -> dict:
    prediction = first_line(generate(evo, qa_prompt(item["question"]), 16, 0.0, "memory"))
    scores = score_prediction(prediction, item["answers"]) if item.get("answers") else {"em": None, "f1": None}
    return {"question": item["question"], "prediction": prediction, **scores}


def _code_check(evo, cfg: dict) -> dict:
    task = materialize(
        {"type": "deduction", "program": DEMO_PROGRAM, "input": DEMO_INPUT},
        cfg.get("exec_timeout", 2.0),
    )
    gold = execute_solve(DEMO_PROGRAM, DEMO_INPUT, cfg.get("exec_timeout", 2.0))
    reply = generate(evo, solver_prompt(task), cfg.get("max_new_code", 64), 0.0, "policy")
    return {
        "program": DEMO_PROGRAM.strip(),
        "input": DEMO_INPUT,
        "executor": gold.value if gold.ok else gold.error,
        "model": first_line(reply),
        "match": check_solver(task, reply, cfg.get("exec_timeout", 2.0)),
    }


def _write(report: dict) -> Path:
    path = repo_path("runs") / "try" / "latest.txt"
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"model: {report['model']}",
        f"fact: {report['fact']}",
        f"edit: {report['edit']}",
        f"trained:\n{report['trained']}",
        f"steps: {report['steps']}  lr: {report['lr']}  loss: {report['loss']:.4f}",
        "",
        "notes_only (the edit text, no gold answers)",
    ]
    for row in report["notes_only"]["after"]:
        lines.append(f"  Q: {row['question']}\n  A: {row['prediction']}\n  f1: {row['f1']}")
    lines.append("")
    lines.append("notes_plus_answers")
    for label, rows in (("before", report["before"]), ("after", report["after"])):
        lines.append(label)
        for row in rows:
            lines.append(
                f"  Q: {row['question']}\n  A: {row['prediction']}\n  f1: {row['f1']}"
            )
        lines.append("")
    code = report["code"]
    lines.append(
        f"code policy (not updated by the fact)\n"
        f"  program: {code['program']} input: {code['input']}\n"
        f"  executor: {code['executor']}\n"
        f"  model: {code['model']}\n"
        f"  match: {code['match']}"
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def _print(report: dict, path: Path) -> None:
    def f1(rows):
        values = [row["f1"] for row in rows if isinstance(row["f1"], float)]
        if not values:
            return None
        return sum(values) / len(values)

    before = f1(report["before"])
    notes_f1 = f1(report["notes_only"]["after"])
    answers_f1 = f1(report["notes_answers"]["after"])
    print(f"[try] model={report['model']} vram_mb={report['vram_mb']:.0f}", flush=True)
    print(f"[try] trained steps={report['steps']} notes_loss={report['notes_only']['loss']:.4f} answers_loss={report['notes_answers']['loss']:.4f}", flush=True)
    for row in report["before"]:
        print(f"[try] before q={row['question']!r} a={row['prediction']!r} f1={row['f1']}", flush=True)
    for row in report["notes_only"]["after"]:
        print(f"[try] notes_only q={row['question']!r} a={row['prediction']!r} f1={row['f1']}", flush=True)
    for row in report["notes_answers"]["after"]:
        print(f"[try] notes_plus_answers q={row['question']!r} a={row['prediction']!r} f1={row['f1']}", flush=True)
    if before is not None and notes_f1 is not None and answers_f1 is not None:
        print(f"[try] notes_only mean_f1 {before:.3f} -> {notes_f1:.3f}", flush=True)
        print(f"[try] notes_plus_answers mean_f1 {before:.3f} -> {answers_f1:.3f}", flush=True)
    code = report["code"]
    print(
        f"[try] code executor={code['executor']!r} model={code['model']!r} match={code['match']}",
        flush=True,
    )
    print(f"[try] wrote {path}", flush=True)
