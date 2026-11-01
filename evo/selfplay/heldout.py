"""Held-out code and math checks, plus the self-score gap."""

from __future__ import annotations

import json
import re

from evo.generate import first_line, generate
from evo.selfplay.executor import execute_solve, outputs_match
from evo.selfplay.tasks import extract_function
from evo.util import mean, repo_path


def load_json(path: str):
    with open(repo_path(path), encoding="utf-8") as handle:
        return json.load(handle)


def last_number(text: str) -> str:
    nums = re.findall(r"-?\d+(?:\.\d+)?", text.replace(",", ""))
    return nums[-1] if nums else ""


def parse_yes(text: str) -> float:
    token = text.strip().lower()
    if token.startswith("yes"):
        return 1.0
    if token.startswith("no"):
        return 0.0
    has_yes = "yes" in token
    has_no = "no" in token
    if has_yes and not has_no:
        return 1.0
    if has_no and not has_yes:
        return 0.0
    return 0.5


def confidence_prompt(claim: str) -> str:
    return f"You answered:\n{claim}\nIs that answer correct? Reply with only yes or no."


def _confidence(evo, claim: str, cfg: dict) -> float:
    reply = generate(evo, confidence_prompt(claim), 8, 0.0, "policy")
    return parse_yes(first_line(reply))


def eval_code(evo, cfg: dict) -> dict:
    items = load_json(cfg["heldout_code"])[: cfg["heldout_limit"]]
    correct, self_scores, agrees = [], [], []
    for item in items:
        raw = generate(evo, item["prompt"], cfg["max_new_code"], 0.0, "policy")
        program = extract_function(raw) or raw
        ok = True
        for test in item["tests"]:
            result = execute_solve(program, test["input"], cfg["exec_timeout"])
            if not (result.ok and outputs_match(result.value, test["output"])):
                ok = False
                break
        correct.append(1.0 if ok else 0.0)
        self_scores.append(_confidence(evo, first_line(raw), cfg))
        if cfg.get("measure_consistency") and item["tests"]:
            other = generate(evo, item["prompt"], cfg["max_new_code"], 0.7, "policy")
            other_program = extract_function(other) or other
            test = item["tests"][0]
            left = execute_solve(program, test["input"], cfg["exec_timeout"])
            right = execute_solve(other_program, test["input"], cfg["exec_timeout"])
            agreed = left.ok and right.ok and outputs_match(left.value, right.value)
            agrees.append(1.0 if agreed else 0.0)
    payload = {
        "n": len(correct),
        "accuracy": mean(correct) or 0.0,
        "self_score": mean(self_scores) or 0.0,
    }
    if agrees:
        payload["consistency"] = mean(agrees) or 0.0
    return payload


def eval_math(evo, cfg: dict) -> dict:
    items = load_json(cfg["heldout_math"])[: cfg["heldout_limit"]]
    correct, self_scores, agrees = [], [], []
    for item in items:
        prompt = f"Solve the problem. Reply with only the final number.\n{item['question']}"
        raw = generate(evo, prompt, cfg["answer_tokens"], 0.0, "policy")
        ok = last_number(raw) == str(item["answer"])
        correct.append(1.0 if ok else 0.0)
        self_scores.append(_confidence(evo, first_line(raw), cfg))
        if cfg.get("measure_consistency"):
            other = generate(evo, prompt, cfg["answer_tokens"], 0.7, "policy")
            left = last_number(raw)
            agrees.append(1.0 if left and left == last_number(other) else 0.0)
    payload = {
        "n": len(correct),
        "accuracy": mean(correct) or 0.0,
        "self_score": mean(self_scores) or 0.0,
    }
    if agrees:
        payload["consistency"] = mean(agrees) or 0.0
    return payload


def verification_gap(evo, cfg: dict) -> dict:
    code = eval_code(evo, cfg)
    math = eval_math(evo, cfg)
    weight = max(code["n"] + math["n"], 1)
    true_acc = ((code["accuracy"] * code["n"]) + (math["accuracy"] * math["n"])) / weight
    self_score = ((code["self_score"] * code["n"]) + (math["self_score"] * math["n"])) / weight
    report = {
        "code": code,
        "math": math,
        "true_accuracy": true_acc,
        "self_score": self_score,
        "verification_gap": self_score - true_acc,
    }
    if "consistency" in code and "consistency" in math:
        consistency = ((code["consistency"] * code["n"]) + (math["consistency"] * math["n"])) / weight
        report["consistency"] = consistency
        report["consistency_gap"] = consistency - true_acc
    return report
