"""Chat-template generation and no-context answer scoring."""

from __future__ import annotations

import torch

from evo.eval.scoring import score_prediction
from evo.model import activate
from evo.util import mean


def render_user(tok, content: str) -> tuple[str, bool]:
    """Return text and whether the tokenizer should add special tokens."""
    return render_messages(tok, [{"role": "user", "content": content}], enable_thinking=False)


def render_messages(tok, messages: list[dict], tools: list | None = None, enable_thinking: bool = False) -> tuple[str, bool]:
    """Chat text for a multi-turn tool conversation. Thinking stays off unless asked."""
    if not getattr(tok, "chat_template", None):
        text = "\n".join(f"{message.get('role', 'user')}: {message.get('content', '')}" for message in messages)
        return text, True
    kwargs = {"tokenize": False, "add_generation_prompt": True}
    if tools:
        kwargs["tools"] = tools
    try:
        text = tok.apply_chat_template(messages, enable_thinking=enable_thinking, **kwargs)
    except TypeError:
        text = tok.apply_chat_template(messages, **kwargs)
    return text, False


def parse_tool_calls(text: str):
    from evo.computer.actions import parse_calls

    return parse_calls(text)


def format_tool_call(name: str, arguments: dict | None = None) -> str:
    from evo.computer.actions import format_call

    return format_call(name, arguments)


def generate(
    evo,
    prompt: str,
    max_new: int,
    temperature: float,
    adapter: str | None,
    max_len: int | None = None,
    block_ids: list[int] | None = None,
) -> str:
    model, tok = evo.model, evo.tok
    model.eval()
    text, add_special = render_user(tok, prompt)
    limit = max_len or evo.cfg.get("max_seq_len", 384)
    encoded = tok(
        text,
        return_tensors="pt",
        add_special_tokens=add_special,
        truncation=True,
        max_length=limit,
    )
    encoded = {key: value.to(evo.device) for key, value in encoded.items()}
    previous_cache = model.config.use_cache
    model.config.use_cache = True
    kwargs = dict(
        max_new_tokens=max_new,
        pad_token_id=tok.pad_token_id,
        eos_token_id=tok.eos_token_id,
    )
    if temperature and temperature > 0:
        kwargs.update(do_sample=True, temperature=temperature, top_p=0.9)
    else:
        kwargs.update(do_sample=False)
    if block_ids:
        from transformers import LogitsProcessorList

        from evo.world.lexicon import NameGate

        kwargs["logits_processor"] = LogitsProcessorList([NameGate(block_ids)])
    with activate(model, adapter), torch.no_grad():
        output = model.generate(**encoded, **kwargs)
    model.config.use_cache = previous_cache
    new_tokens = output[0, encoded["input_ids"].shape[1] :]
    return tok.decode(new_tokens, skip_special_tokens=True).strip()


def generate_messages(
    evo,
    messages: list[dict],
    max_new: int,
    temperature: float,
    adapter: str | None,
    tools: list | None = None,
    enable_thinking: bool = False,
    max_len: int | None = None,
) -> str:
    """One assistant turn given the message list. Tool results belong in the list already."""
    model, tok = evo.model, evo.tok
    model.eval()
    text, add_special = render_messages(tok, messages, tools=tools, enable_thinking=enable_thinking)
    limit = max_len or evo.cfg.get("max_seq_len", 384)
    encoded = tok(
        text,
        return_tensors="pt",
        add_special_tokens=add_special,
        truncation=True,
        max_length=limit,
    )
    encoded = {key: value.to(evo.device) for key, value in encoded.items()}
    previous_cache = model.config.use_cache
    model.config.use_cache = True
    kwargs = dict(max_new_tokens=max_new, pad_token_id=tok.pad_token_id, eos_token_id=tok.eos_token_id)
    if temperature and temperature > 0:
        kwargs.update(do_sample=True, temperature=temperature, top_p=0.9)
    else:
        kwargs.update(do_sample=False)
    with activate(model, adapter), torch.no_grad():
        output = model.generate(**encoded, **kwargs)
    model.config.use_cache = previous_cache
    new_tokens = output[0, encoded["input_ids"].shape[1] :]
    return tok.decode(new_tokens, skip_special_tokens=True).strip()


def qa_prompt(question: str) -> str:
    return (
        "Answer the question with only the short factual answer. Do not explain.\n"
        f"Question: {question}\n"
        "Answer:"
    )


def blind_edit_prompt(passage: dict) -> str:
    """Write notes from the passage alone. The exam questions stay hidden."""
    context = passage["context"][: passage.get("_char_limit", 10**9)]
    return (
        "Read the passage and write factual statements a student could memorize. "
        "One self-contained fact per line. Do not ask questions and do not add commentary.\n\n"
        f"Passage:\n{context}\n\n"
        "Facts:"
    )


def edit_prompt(passage: dict, questions: list[dict]) -> str:
    context = passage["context"][: passage.get("_char_limit", 10**9)]
    lines = "\n".join(f"- {item['question']}" for item in questions)
    return (
        "Read the passage and write factual statements that would help answer the questions. "
        "One self-contained fact per line. Do not write the questions back and do not add commentary.\n\n"
        f"Passage:\n{context}\n\n"
        f"Questions:\n{lines}\n\n"
        "Facts:"
    )


def teacher_prompt(passage: str, question: str) -> str:
    return (
        "Copy the shortest span from the passage that answers the question.\n\n"
        f"Passage:\n{passage}\n\n"
        f"Question: {question}\n"
        "Answer:"
    )


def clean_edit(text: str) -> str:
    kept = []
    for raw in text.splitlines():
        line = raw.strip(" -\t*")
        if not line:
            continue
        low = line.lower()
        if low.startswith(("sure", "here are", "here is", "facts:", "the following", "i ")):
            continue
        kept.append(line)
    return "\n".join(kept[:12]).strip()


def first_line(text: str) -> str:
    return text.split("\n", 1)[0].strip()


def score_questions(evo, questions: list[dict], adapter: str | None, answer_tokens: int) -> dict:
    rows = []
    for item in questions:
        prediction = first_line(
            generate(evo, qa_prompt(item["question"]), answer_tokens, 0.0, adapter)
        )
        scores = score_prediction(prediction, item["answers"])
        rows.append(
            {
                "question": item["question"],
                "prediction": prediction,
                "answers": item["answers"],
                **scores,
            }
        )
    return {
        "em": mean([row["em"] for row in rows]) or 0.0,
        "f1": mean([row["f1"] for row in rows]) or 0.0,
        "n": len(rows),
        "rows": rows,
    }


def score_passages(evo, passages: list[dict], adapter: str | None, question_limit: int, answer_tokens: int) -> dict:
    per = []
    for passage in passages:
        questions = passage["qas"][:question_limit]
        scored = score_questions(evo, questions, adapter, answer_tokens)
        per.append({"id": passage["id"], "em": scored["em"], "f1": scored["f1"], "rows": scored["rows"]})
    return {
        "em": mean([item["em"] for item in per]) or 0.0,
        "f1": mean([item["f1"] for item in per]) or 0.0,
        "per_passage": per,
    }
