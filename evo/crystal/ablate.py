"""Retrieval-agent (scaffold notes) vs crystallized bare competence.

Toy-friendly: pass callables so unit tests need no GPU. Real runs wire generate().
"""

from __future__ import annotations

from typing import Callable

from evo.crystal.atom import CapabilityAtom


GradeFn = Callable[[str, str], bool]  # prompt, reply -> ok
ActFn = Callable[[str, str], str]  # prompt, mode -> reply; mode in {"bare", "scaffold"}


def dissolution_score(scaffold_rate: float, bare_rate: float) -> float:
    """How much the notes still help. Target -> 0 as skill internalizes.

    D = max(0, scaffold_rate - bare_rate). Gate competence stays separate (0.6).
    """
    return max(0.0, float(scaffold_rate) - float(bare_rate))


def run_ablation(
    prompts: list[str],
    answers: list[str],
    act: ActFn,
    grade: GradeFn,
    *,
    criterion: float = 0.6,
) -> dict:
    """Score bare vs scaffold on the same prompts.

    `act(prompt, "scaffold")` may prepend retrieval notes; `act(prompt, "bare")` must not.
    """
    if len(prompts) != len(answers):
        raise ValueError("prompts/answers length mismatch")
    bare_hits = []
    scaf_hits = []
    for prompt, answer in zip(prompts, answers):
        bare = act(prompt, "bare")
        scaf = act(prompt, "scaffold")
        # grade against gold answer string contained / exact via caller
        bare_hits.append(grade(answer, bare))
        scaf_hits.append(grade(answer, scaf))
    bare_rate = sum(bare_hits) / len(bare_hits) if bare_hits else 0.0
    scaf_rate = sum(scaf_hits) / len(scaf_hits) if scaf_hits else 0.0
    d = dissolution_score(scaf_rate, bare_rate)
    return {
        "n": len(prompts),
        "bare_rate": bare_rate,
        "scaffold_rate": scaf_rate,
        "dissolution": d,
        "bare_clears_gate": bare_rate >= criterion,
        "scaffold_clears_gate": scaf_rate >= criterion,
        "criterion": criterion,
        "internalized": bare_rate >= criterion and d <= 0.05,
    }


def attach_ablation(atom: CapabilityAtom, report: dict) -> CapabilityAtom:
    atom.bare_rate = float(report["bare_rate"])
    atom.scaffold_rate = float(report["scaffold_rate"])
    atom.dissolution = float(report["dissolution"])
    atom.evidence["ablation"] = report
    atom.write()
    return atom
