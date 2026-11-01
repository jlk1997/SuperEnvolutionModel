"""GPU eval: bare crystallized LoRA vs scaffold-notes agent on held-out add prompts.

Writes runs/capabilities/<atom>/dissolution.json. Criterion stays 0.6.
"""

from __future__ import annotations

import json
from pathlib import Path

from evo.crystal.ablate import attach_ablation, dissolution_score, run_ablation
from evo.crystal.atom import CapabilityAtom
from evo.plastic.fit import _op_example, grade_reply, lesson
from evo.registry import require_ready
from evo.util import repo_path


def _heldout_add_items(exam: int = 4) -> list[dict]:
    plan = lesson(seed=0, teach=8, exam=exam)
    family = plan["family"]
    items = []
    for value in [1, 3, 5, 7]:
        prompt, _completion, answer = _op_example(family, "left", value)
        items.append({"prompt": prompt, "answer": answer, "n": value})
    return items


def _scaffold_note(family, value: int) -> str:
    demo_n = 0 if value != 0 else 2
    prompt, completion, _a = _op_example(family, "left", demo_n)
    return f"Previously verified:\n{prompt}\n{completion}\n\nNow solve:\n"


def _load_policy_adapter(evo, atom_dir: Path) -> str:
    """Load policy/*.safetensors into the live `policy` adapter. Returns load mode."""
    from peft import set_peft_model_state_dict
    from safetensors.torch import load_file

    policy_dir = atom_dir / "policy"
    weight = policy_dir / "adapter_model.safetensors"
    if not weight.is_file():
        weight = atom_dir / "adapter_model.safetensors"
        policy_dir = atom_dir
    if not weight.is_file():
        raise FileNotFoundError(f"no adapter_model.safetensors under {atom_dir}")
    state = load_file(str(weight))
    # Peft 0.21 accepts adapter_name; keys are base_model...lora_*.weight
    set_peft_model_state_dict(evo.model, state, adapter_name="policy")
    evo.set_adapter("policy", inference=True)
    return f"safetensors:{weight}"


def run_add_dissolution(
    atom_dir: str | Path | None = None,
    *,
    cfg: dict | None = None,
    write: bool = True,
) -> dict:
    import torch

    from evo.generate import generate
    from evo.model import build_model, release

    atom_path = Path(atom_dir) if atom_dir else repo_path("runs") / "capabilities" / "add6_mlp"
    atom = CapabilityAtom.load(atom_path)
    cfg = dict(cfg or {})
    cfg.setdefault("model_name", atom.base_model)
    cfg.setdefault("lora_rank", 8)
    cfg.setdefault("lora_alpha", 16)
    cfg.setdefault("lora_dropout", 0.0)
    # Match crystallized sites (add6 is mlp-only weights)
    sites = list(atom.sites or ["mlp"])
    cfg["fit_sites"] = sites
    cfg["lora_preset"] = "mlp" if sites == ["mlp"] else "attn_mlp"
    cfg.setdefault("max_seq_len", 256)
    cfg.setdefault("max_new_code", 32)
    require_ready(cfg)
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA required for real dissolution eval")

    items = _heldout_add_items()
    plan = lesson(seed=0, teach=8, exam=4)
    family = plan["family"]
    notes = {item["prompt"]: _scaffold_note(family, item["n"]) + item["prompt"] for item in items}

    evo = None
    try:
        evo = build_model(cfg)
        loaded = _load_policy_adapter(evo, Path(atom.adapter_dir))

        def act(prompt: str, mode: str) -> str:
            text = notes[prompt] if mode == "scaffold" else prompt
            return generate(
                evo,
                text,
                int(cfg.get("max_new_code", 32)),
                0.0,
                "policy",
                max_len=int(cfg.get("max_seq_len", 256)),
            )

        def grade(answer: str, reply: str) -> bool:
            got = grade_reply(reply)
            try:
                return got is not None and int(got) == int(answer)
            except (TypeError, ValueError):
                return False

        prompts = [item["prompt"] for item in items]
        answers = [item["answer"] for item in items]
        # Also score frozen-base style: temporarily zero? Skip — scaffold uses same LoRA+notes.
        # For true agent scaffold we'd use base; here scaffold = crystallized + notes (retrieval agent
        # that already has the skill partially). Also run notes-on-zero by comparing rates.
        report = run_ablation(prompts, answers, act, grade, criterion=float(atom.criterion or 0.6))
        report["atom"] = atom.name
        report["adapter_dir"] = atom.adapter_dir
        report["loaded"] = loaded
        report["items"] = [{"n": it["n"], "answer": it["answer"]} for it in items]
        report["dissolution"] = dissolution_score(report["scaffold_rate"], report["bare_rate"])
        # Capture one sample reply for debugging
        sample_prompt = prompts[0]
        report["sample"] = {
            "prompt_tail": sample_prompt[-80:],
            "bare": act(sample_prompt, "bare")[:120],
            "scaffold": act(sample_prompt, "scaffold")[:160],
        }
        attach_ablation(atom, report)
        if write:
            dest = Path(atom.adapter_dir) / "dissolution.json"
            dest.write_text(json.dumps(report, indent=2, ensure_ascii=True), encoding="utf-8")
            report["wrote"] = str(dest)
        return report
    finally:
        if evo is not None:
            release(evo)


def main(argv: list[str] | None = None) -> None:
    import sys
    args = list(sys.argv[1:] if argv is None else argv)
    atom = args[0] if args else None
    report = run_add_dissolution(atom)
    print(json.dumps(report, indent=2, ensure_ascii=True), flush=True)


if __name__ == "__main__":
    main()
