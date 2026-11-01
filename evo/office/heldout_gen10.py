"""Tenth sealed pair. gen9 lighthouse/tannery crashed mid-run after seal open — burned without judge.

Closed until load_gen10_heldout.
"""

from __future__ import annotations

from evo.office.packs import _pack


GEN10_PACKS = [
    _pack("observatory", "dome", "arcsec", "mount", "logged", "logged_on", "dome_id"),
    _pack("apiary", "hive", "grams", "comb", "harvested", "robbed_on", "hive_id"),
]
for _row in GEN10_PACKS:
    _row["heldout"] = True
