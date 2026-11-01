"""Third sealed pair. Development streams must not import this module.

grades/roster (first) and library/warehouse (next) are burned.
This pair stays closed until load_gen3_heldout opens it with a written reason.
"""

from __future__ import annotations

from evo.office.packs import _pack


GEN3_PACKS = [
    _pack("ferry", "crossing", "tolls", "berth", "sailed", "sailed_on", "crossing_id"),
    _pack("bakery", "batch", "grams", "bake", "cooled", "mixed_on", "batch_id"),
]
for _row in GEN3_PACKS:
    _row["heldout"] = True
