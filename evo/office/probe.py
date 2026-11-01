"""Development check: orders teach a procedure, expenses only swaps the card.

This is not gate 3. The burned packs and the next sealed pair stay closed.
A reference script that still passes does not count as the model.
"""

from __future__ import annotations

from evo.computer.actions import format_call
from evo.computer.episode import run_episode
from evo.computer.license import License
from evo.office.families import make_task
from evo.office.packs import pack_by_name
from evo.session.procedure import LINE, binding_card, expand, leaks, procedure_pairs, said_line


STOP = "这个尺寸记不住这段做法"
NOT_RUN = "没跑成"
NOT_SAID = "这个尺寸记不住这一句"
SAID = "这一题是模型自己过的"


def probe_outcome(ran: bool, said: bool = False, checked: bool = False, steps: int = 0) -> dict:
    """Separate a missing model from a model that ran and did not say the line."""
    if not ran:
        return {"ran": False, "why": NOT_RUN, "stop": "", "model": False, "orders_ok": False, "steps": 0}
    if said and checked:
        return {"ran": True, "why": SAID, "stop": "", "model": True, "orders_ok": True, "steps": int(steps)}
    return {"ran": True, "why": NOT_SAID, "stop": NOT_SAID, "model": False, "orders_ok": False, "steps": int(steps)}


def exercise_swap(seed: int = 0) -> dict:
    """Rewrite an orders trace, then run it on expenses with only the card changed.

    `model` stays false. The script can pass and still not be a model result.
    """
    orders = pack_by_name("orders")
    expenses = pack_by_name("expenses")
    source = make_task(orders, "table", seed, variant=0, difficulty=1)
    code = str(source["calls"][0].arguments.get("code") or "")
    pairs, card = procedure_pairs([(source["prompt"], code)], orders, str(source.get("secret") or ""))
    line = pairs[0][1]
    question = pairs[0][0]
    target = make_task(expenses, "table", seed, variant=0, difficulty=1)
    target_code = str(target["calls"][0].arguments.get("code") or "")
    swapped = expand(line, binding_card(expenses, target_code))

    def reply(_messages):
        return format_call("python", {"code": swapped})

    from tempfile import TemporaryDirectory
    from pathlib import Path

    with TemporaryDirectory() as folder:
        result = run_episode(target, reply, Path(folder), License(grants={"python", "read", "write"}))
    return {
        "script_ok": bool(result["ok"]),
        "model": False,
        "procedure": line,
        "question": question,
        "swapped": swapped,
        "leaks": leaks(pairs[0][0] + "\n" + line, card, str(source.get("secret") or "")),
    }


def contrast_pairs(procedures: list[tuple[str, str]]) -> list[tuple[str, str]]:
    """Push down only the other job's distinctive words. The shared write-out clause stays."""
    head = LINE.split(";")[0].strip()
    rows = []
    for prompt, completion in procedures:
        if completion == LINE:
            rows.append((prompt, file_line()))
        elif completion == file_line():
            rows.append((prompt, head))
    return rows


def choose_line(scores: dict, margin: float = 0.15):
    """Pick a procedure only when its loss is clearly below the other one. Lower loss is better."""
    if len(scores) < 2:
        return None
    ordered = sorted(scores.items(), key=lambda item: float(item[1]))
    best, best_loss = ordered[0]
    second_loss = float(ordered[1][1])
    if float(best_loss) + float(margin) < second_loss:
        return best
    return None


def unlike_once(evo, pairs: list[tuple[str, str]], lr: float, max_len: int, sites: list[str]) -> dict:
    """One pass that makes the wrong procedure line less likely. The right line is not in these pairs."""
    import torch

    from evo.model import ensure_input_grads, set_trainable_sites

    if not pairs:
        return {"steps": 0}
    ensure_input_grads(evo.model)
    evo.set_adapter("policy", inference=False)
    set_trainable_sites(evo.model, "policy", sites)
    params = [param for param in evo.model.parameters() if param.requires_grad]
    if not params:
        return {"steps": 0}
    opt = torch.optim.AdamW(params, lr=lr)
    evo.model.train()
    evo.model.config.use_cache = False
    steps = 0
    for prompt, completion in pairs:
        from evo.inner_loop import _encode_pair

        input_ids, labels = _encode_pair(evo, prompt, completion, max_len)
        if not any(label != -100 for label in labels):
            continue
        batch_ids = torch.tensor([input_ids], device=evo.device)
        batch_labels = torch.tensor([labels], device=evo.device)
        attn = torch.ones_like(batch_ids)
        opt.zero_grad(set_to_none=True)
        nll = evo.model(input_ids=batch_ids, attention_mask=attn, labels=batch_labels).loss
        if not torch.isfinite(nll):
            continue
        (-nll).backward()
        torch.nn.utils.clip_grad_norm_(params, 1.0)
        opt.step()
        steps += 1
    return {"steps": steps}


def pair_loss(evo, prompt: str, completion: str) -> float:
    import torch

    from evo.inner_loop import _device_batch, _encode_pair
    from evo.model import activate

    ids, labels = _encode_pair(evo, prompt, completion, 256)
    batch, label_tensor = _device_batch(evo, ids, labels)
    evo.model.eval()
    evo.model.config.use_cache = False
    with torch.no_grad():
        with activate(evo.model, "policy"):
            loss = evo.model(**batch, labels=label_tensor).loss
    return float(loss.detach().item())


def replay_budget() -> dict:
    """Known jobs are repeated. Refusal is one pass, so it does not erase a new wording."""
    return {"procedure": 8, "refusal": 1}


def probe_train_plan() -> dict:
    from evo.session.procedure import probe_train_plan as plan

    return plan()


def grade_reply(reply: str, task: dict, card: dict) -> bool:
    """Only the model's own line counts. The body then binds this card and the checker decides."""
    if not said_line(reply):
        return False
    program = expand(reply, card)
    if not program:
        return False

    def answer(_messages):
        return format_call("python", {"code": program})

    from tempfile import TemporaryDirectory
    from pathlib import Path

    with TemporaryDirectory() as folder:
        result = run_episode(task, answer, Path(folder), License(grants={"python", "read", "write"}))
    return bool(result["ok"])


def blind_pair(pack: dict, seed: int, difficulty: int) -> tuple[dict, str, str, dict]:
    task = make_task(pack, "table", seed, variant=0, difficulty=difficulty)
    code = str(task["calls"][0].arguments.get("code") or "")
    pairs, card = procedure_pairs([(task["prompt"], code)], pack, str(task.get("secret") or ""))
    return task, pairs[0][0], pairs[0][1], card


def wording_split(pack: dict, seed: int = 0) -> tuple[list[tuple[str, str]], tuple]:
    """Two blinded wordings are trained. The third wording is held out."""
    rows = [blind_pair(pack, seed, difficulty) for difficulty in (1, 3, 5)]
    train = [(question, line) for _task, question, line, _card in rows[:2]]
    held = rows[2]
    return train, held


FILE_LINE = "move {KIND} from {SRC} to {DST}"


def file_line() -> str:
    return FILE_LINE


def other_job() -> str:
    """One trained wording of a different job."""
    return file_jobs()[0][0]


def file_jobs() -> tuple[list[str], str]:
    """Two wordings of moving a file train one line. A third wording is held out."""
    trained = [
        "Move every .txt file from inbox into reports. Leave other files in inbox.",
        "Using the shell, make a directory out and copy inbox\\note.txt to out\\note.txt.",
    ]
    held = "Copy the note into out."
    return trained, held


def other_jobs() -> tuple[list[str], str]:
    """Kept for the split check. The held wording is the file job, not the sum."""
    return file_jobs()


def report_job() -> str:
    """A third job that is neither a trained sum wording nor a trained file wording."""
    return "Write the summary report."


NONE_LINE = "no procedure"


def none_line() -> str:
    return NONE_LINE


def none_jobs() -> tuple[list[str], str]:
    """Two jobs with no procedure train a refusal. The report wording is left out."""
    trained = [
        "Publish the html summary.",
        "Keep the marked drops.",
    ]
    left_out = report_job()
    return trained, left_out


def with_notes(question: str) -> str:
    """The scaffold: the same question, with the procedure line written in."""
    return (question or "") + "\n" + LINE


def smallest_qwen() -> str:
    """Primary local checkpoint via the model registry (Qwen2.5-1.5B-Instruct)."""
    from evo.registry import PRIMARY, is_ready, resolve

    path = resolve(PRIMARY)
    if is_ready(path):
        return str(path)
    return ""


def run_feasibility() -> dict:
    """The check this machine can finish.

    Before training, the held-out wording must fail. After eight MLP steps on two
    other wordings, that wording must say the line and pass the checker.
    This is not gate 2.
    """
    path = smallest_qwen()
    if not path:
        return {"feasible": False, "why": "没跑成"}
    try:
        from evo.generate import generate
        from evo.model import build_model
        from evo.outer_loop import sft_policy

        orders = pack_by_name("orders")
        train, held = wording_split(orders, 0)
        held_task, held_question, held_line, held_card = held
        if held_line != LINE or LINE in held_question or "where" in held_question:
            return {"feasible": False, "why": "题目没盲干净"}
        plan = probe_train_plan()
        cfg = {
            "model_name": path,
            "lora_rank": 8,
            "lora_alpha": 16,
            "lora_dropout": 0.0,
            "target_modules": list(plan["sites"]),
            "max_seq_len": 256,
            "outer_lr": 5e-4,
            "seed": 0,
        }
        evo = build_model(cfg)
        before = generate(evo, held_question, 64, 0.0, "policy")
        print("FEAS_BEFORE " + before.replace("\n", " ")[:180], flush=True)
        before_ok = grade_reply(before, held_task, held_card)
        trained = sft_policy(
            evo,
            train,
            float(cfg["outer_lr"]),
            int(plan["steps"]),
            int(cfg["max_seq_len"]),
            adapter="policy",
            sites=list(plan["sites"]),
        )
        steps = int(trained.get("steps") or 0)
        after = generate(evo, held_question, 64, 0.0, "policy")
        print("FEAS_AFTER " + after.replace("\n", " ")[:180], flush=True)
        after_ok = grade_reply(after, held_task, held_card)
        feasible = (not before_ok) and after_ok and steps > 0
        return {"feasible": feasible, "before_ok": before_ok, "after_ok": after_ok, "steps": steps, "why": "通过" if feasible else "没通过"}
    except Exception as exc:
        print(f"FEAS_FAILED {type(exc).__name__}: {exc}", flush=True)
        return {"feasible": False, "why": "没跑成"}
    """One orders question, one optimizer step, one reply. A missing model is not a failed memory."""
    path = smallest_qwen()
    if not path:
        return probe_outcome(False)
    try:
        from evo.generate import generate
        from evo.model import build_model
        from evo.outer_loop import sft_policy

        orders = pack_by_name("orders")
        train, held = wording_split(orders, 0)
        task, _q, line, card = blind_pair(orders, 0, 1)
        question = train[0][0]
        if any(item != LINE or not prompt or LINE in prompt or "where" in prompt for prompt, item in train):
            return probe_outcome(False)
        held_task, held_question, held_line, held_card = held
        if held_question in {prompt for prompt, _item in train} or "where" in held_question or LINE in held_question:
            return probe_outcome(False)
        neg_train, neg_held = file_jobs()
        none_train, none_left = none_jobs()
        procedures = list(train) + [(text, file_line()) for text in neg_train]
        plan = probe_train_plan()
        cfg = {
            "model_name": path,
            "lora_rank": 8,
            "lora_alpha": 16,
            "lora_dropout": 0.0,
            "target_modules": list(plan["sites"]),
            "max_seq_len": 256,
            "outer_lr": 5e-4,
            "seed": 0,
        }
        evo = build_model(cfg)
        before = generate(evo, held_question, 64, 0.0, "policy")
        before_other = generate(evo, other_job(), 64, 0.0, "policy")
        noted = generate(evo, with_notes(held_question), 64, 0.0, "policy")
        print("PROBE_BEFORE " + before.replace("\n", " ")[:180], flush=True)
        print("PROBE_OTHER_BEFORE " + before_other.replace("\n", " ")[:180], flush=True)
        print("PROBE_NOTES " + noted.replace("\n", " ")[:180], flush=True)
        scaffold_ok = grade_reply(noted, held_task, held_card)
        trained = sft_policy(
            evo,
            procedures,
            float(cfg["outer_lr"]),
            int(plan["steps"]),
            int(cfg["max_seq_len"]),
            adapter="policy",
            sites=list(plan["sites"]),
        )
        steps = int(trained.get("steps") or 0)
        contrasted = unlike_once(
            evo,
            contrast_pairs(procedures),
            float(cfg["outer_lr"]),
            int(cfg["max_seq_len"]),
            list(plan["sites"]),
        )
        steps += int(contrasted.get("steps") or 0)
        if steps <= 0:
            return probe_outcome(True, said=False, checked=False, steps=0)
        reply = generate(evo, question, 64, 0.0, "policy")
        print("PROBE_REPLY " + reply.replace("\n", " ")[:240], flush=True)
        said = said_line(reply)
        checked = grade_reply(reply, task, card) if said else False
        expenses_ok = False
        other_said = False
        if checked:
            expenses = pack_by_name("expenses")
            other_task, other_question, other_line, other_card = blind_pair(expenses, 0, 1)
            other_reply = generate(evo, other_question, 64, 0.0, "policy")
            print("PROBE_EXPENSES " + other_reply.replace("\n", " ")[:240], flush=True)
            other_said = said_line(other_reply)
            expenses_ok = other_line == LINE and grade_reply(other_reply, other_task, other_card)
            hard_reply = generate(evo, held_question, 64, 0.0, "policy")
            print("PROBE_HARD " + hard_reply.replace("\n", " ")[:240], flush=True)
            hard_ok = held_line == LINE and grade_reply(hard_reply, held_task, held_card)
            after_other = generate(evo, neg_held, 64, 0.0, "policy")
            print("PROBE_FILE " + after_other.replace("\n", " ")[:180], flush=True)
            other_job_said = said_line(after_other)
            file_ok = file_line() in after_other and not other_job_said
            report_reply = generate(evo, none_left, 64, 0.0, "policy")
            print("PROBE_REPORT " + report_reply.replace("\n", " ")[:180], flush=True)
            report_said = said_line(report_reply)
            none_ok = none_line() in report_reply and not report_said and file_line() not in report_reply
            _train, claim_held = wording_split(expenses, 0)
            claim_task, claim_question, claim_line, claim_card = claim_held
            claim_reply = generate(evo, claim_question, 64, 0.0, "policy")
            print("PROBE_CLAIM " + claim_reply.replace("\n", " ")[:240], flush=True)
            claim_ok = (
                claim_line == LINE
                and claim_question not in {prompt for prompt, _item in train}
                and "cost" not in claim_reply
                and "approved" not in claim_reply
                and grade_reply(claim_reply, claim_task, claim_card)
            )
            fresh = {}
            seen_prompts = {prompt for prompt, _item in train}
            for name, banned in (("attendance", ("hours", "present")), ("parcels", ("weight", "delivered"))):
                fresh_pack = pack_by_name(name)
                _fresh_train, fresh_held = wording_split(fresh_pack, 0)
                fresh_task, fresh_question, fresh_line, fresh_card = fresh_held
                fresh_reply = generate(evo, fresh_question, 64, 0.0, "policy")
                print("PROBE_" + name.upper() + " " + fresh_reply.replace("\n", " ")[:240], flush=True)
                fresh[name] = (
                    fresh_line == LINE
                    and fresh_question not in seen_prompts
                    and not any(word in fresh_reply for word in banned)
                    and grade_reply(fresh_reply, fresh_task, fresh_card)
                )
        else:
            hard_ok = False
            other_job_said = False
            file_ok = False
            report_said = False
            none_ok = False
            claim_ok = False
            fresh = {"attendance": False, "parcels": False}
        picked = {
            "sum": choose_line({"sum": pair_loss(evo, held_question, LINE), "file": pair_loss(evo, held_question, file_line())}),
            "file": choose_line({"sum": pair_loss(evo, neg_held, LINE), "file": pair_loss(evo, neg_held, file_line())}),
            "report": choose_line({"sum": pair_loss(evo, none_left, LINE), "file": pair_loss(evo, none_left, file_line())}),
        }
        print("PROBE_PICK " + str(picked), flush=True)
        outcome = probe_outcome(True, said=said, checked=checked, steps=steps)
        outcome["expenses_ok"] = expenses_ok
        outcome["expenses_said"] = other_said
        outcome["hard_ok"] = hard_ok
        outcome["before_held"] = said_line(before)
        outcome["other_job_said"] = other_job_said
        outcome["file_ok"] = file_ok
        outcome["report_said"] = report_said
        outcome["none_ok"] = none_ok
        outcome["picked"] = picked
        outcome["scaffold_ok"] = scaffold_ok
        outcome["claim_ok"] = claim_ok
        outcome["attendance_ok"] = bool(fresh.get("attendance"))
        outcome["parcels_ok"] = bool(fresh.get("parcels"))
        return outcome
    except Exception as exc:
        print(f"PROBE_LOAD_FAILED {type(exc).__name__}: {exc}", flush=True)
        return probe_outcome(False)


def exam_sheet() -> dict:
    """The fixed paper. Training wordings and exam wordings do not overlap."""
    orders = pack_by_name("orders")
    train, orders_left = wording_split(orders, 0)
    file_train, file_left = file_jobs()
    sums = [("orders",) + orders_left]
    for name in ("expenses", "attendance", "parcels"):
        _trained, left = wording_split(pack_by_name(name), 0)
        sums.append((name,) + left)
    pairs = list(train) + [(text, file_line()) for text in file_train]
    return {"pairs": pairs, "sums": sums, "file": file_left, "report": report_job()}


def exam_verdict(card: dict) -> dict:
    """Four bars, fixed before the run. A report that says the sum line fails the exam."""
    sums = card["sums"]
    failed = []
    if not all(not row["before"] and row["after"] for row in sums):
        failed.append("留出的加总")
    if not (sum(row["after"] for row in sums) > sum(row["notes"] for row in sums)):
        failed.append("没有好过题目里的做法")
    if not (card["file_said"] and not card["file_sum"]):
        failed.append("搬文件")
    if card["report_sum"]:
        failed.append("写报告")
    return {"passed": not failed, "failed": failed}


def run_exam(epochs: int = 8, sum_epochs: int | None = None, file_epochs: int | None = None) -> dict:
    """One training run, then the fixed exam. No refusal target and no push-down of the other line."""
    path = smallest_qwen()
    sum_n = int(epochs if sum_epochs is None else sum_epochs)
    file_n = int(epochs if file_epochs is None else file_epochs)
    sheet = exam_sheet()
    if not path:
        return {"passed": False, "why": "没跑成", "failed": ["没跑成"], "epochs": epochs, "sum_epochs": sum_n, "file_epochs": file_n}
    try:
        from evo.generate import generate
        from evo.model import build_model
        from evo.outer_loop import sft_policy

        plan = probe_train_plan()
        cfg = {
            "model_name": path,
            "lora_rank": 8,
            "lora_alpha": 16,
            "lora_dropout": 0.0,
            "target_modules": list(plan["sites"]),
            "max_seq_len": 256,
            "outer_lr": 5e-4,
            "seed": 0,
        }
        evo = build_model(cfg)

        def ask(prompt: str) -> str:
            text = generate(evo, prompt, 64, 0.0, "policy")
            print("EXAM " + prompt[:40].replace("\n", " ") + " => " + text.replace("\n", " ")[:120], flush=True)
            return text

        sums = []
        for name, task, question, line, card in sheet["sums"]:
            before = ask(question)
            noted = ask(with_notes(question))
            sums.append({"name": name, "task": task, "question": question, "line": line, "card": card, "before": grade_reply(before, task, card), "notes": grade_reply(noted, task, card)})
        file_before = ask(sheet["file"])
        report_before = ask(sheet["report"])
        sum_pairs = [pair for pair in sheet["pairs"] if pair[1] == LINE]
        file_pairs = [pair for pair in sheet["pairs"] if pair[1] == file_line()]
        mixed = []
        for index in range(max(sum_n, file_n)):
            if index < sum_n:
                mixed.extend(sum_pairs)
            if index < file_n:
                mixed.extend(file_pairs)
        trained = sft_policy(evo, mixed, float(cfg["outer_lr"]), 1, int(cfg["max_seq_len"]), adapter="policy", sites=list(plan["sites"]))
        steps = int(trained.get("steps") or 0)
        for row in sums:
            reply = ask(row["question"])
            row["after_text"] = reply
            row["after"] = row["line"] == LINE and grade_reply(reply, row["task"], row["card"])
        file_after = ask(sheet["file"])
        report_after = ask(sheet["report"])
        card = {
            "sums": sums,
            "file_said": file_line() in file_after,
            "file_sum": said_line(file_after),
            "report_sum": ("sum {AMOUNT}" in report_after) or said_line(report_after),
        }
        verdict = exam_verdict(card)
        verdict.update({
            "epochs": epochs,
            "sum_epochs": sum_n,
            "file_epochs": file_n,
            "steps": steps,
            "sums": [{key: row[key] for key in ("name", "before", "notes", "after")} for row in sums],
            "file_before": file_before.replace("\n", " ")[:80],
            "file_after": file_after.replace("\n", " ")[:80],
            "report_before": report_before.replace("\n", " ")[:80],
            "report_after": report_after.replace("\n", " ")[:80],
        })
        return verdict
    except Exception as exc:
        print(f"EXAM_FAILED {type(exc).__name__}: {exc}", flush=True)
        return {"passed": False, "why": "没跑成", "failed": ["没跑成"], "epochs": epochs}


def conclude(model_ok: bool) -> dict:
    """The stop sentence is the result until a model passes with the notes removed."""
    if not model_ok:
        return {"stop": STOP, "model": False, "orders_ok": False, "expenses_ok": False}
    return {"stop": "", "model": True, "orders_ok": True, "expenses_ok": True}
