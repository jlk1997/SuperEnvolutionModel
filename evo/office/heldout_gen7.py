"""Seventh sealed pair. Do not import from development streams.

Burned: grades/roster, library/warehouse, ferry/bakery, museum/pharmacy,
cinema/nursery, harbor/orchard. Closed until load_gen7_heldout.
"""

from __future__ import annotations

from evo.office.packs import _pack


GEN7_PACKS = [
    _pack("atelier", "piece", "hours", "bench", "finished", "cast_on", "piece_id"),
    _pack("foundry", "pour", "kg", "mold", "poured", "poured_on", "pour_id"),
]
for _row in GEN7_PACKS:
    _row["heldout"] = True
