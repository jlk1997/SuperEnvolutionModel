"""Fifth sealed pair. Do not import from development streams.

Burned: grades/roster, library/warehouse, ferry/bakery, museum/pharmacy.
Closed until load_gen5_heldout opens with a written reason.
"""

from __future__ import annotations

from evo.office.packs import _pack


GEN5_PACKS = [
    _pack("cinema", "screening", "seats", "reel", "shown", "played_on", "screening_id"),
    _pack("nursery", "plot", "saplings", "bed", "planted", "sown_on", "plot_id"),
]
for _row in GEN5_PACKS:
    _row["heldout"] = True
