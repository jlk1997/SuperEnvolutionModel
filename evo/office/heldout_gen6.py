"""Sixth sealed pair. Do not import from development streams.

Burned: grades/roster, library/warehouse, ferry/bakery, museum/pharmacy, cinema/nursery.
Closed until load_gen6_heldout opens with a written reason.
"""

from __future__ import annotations

from evo.office.packs import _pack


GEN6_PACKS = [
    _pack("harbor", "berth", "tonnage", "quay", "docked", "tied_on", "berth_id"),
    _pack("orchard", "row", "bushels", "grove", "picked", "picked_on", "row_id"),
]
for _row in GEN6_PACKS:
    _row["heldout"] = True
