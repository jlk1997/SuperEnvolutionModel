"""Capability crystallizer: verified success -> named LoRA atom -> bare vs scaffold ablation."""

from evo.crystal.atom import CapabilityAtom
from evo.crystal.crystallize import crystallize_from_adapter, crystallize_from_pairs
from evo.crystal.ablate import dissolution_score, run_ablation
from evo.crystal.router import is_internalized, load_atom, prompt_for, route
from evo.crystal.batch import batch_crystallize, discover_success_adapters

__all__ = [
    "CapabilityAtom",
    "crystallize_from_adapter",
    "crystallize_from_pairs",
    "dissolution_score",
    "run_ablation",
    "is_internalized",
    "prompt_for",
    "route",
    "load_atom",
    "batch_crystallize",
    "discover_success_adapters",
]
