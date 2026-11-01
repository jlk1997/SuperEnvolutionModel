"""Eleventh sealed pair. Closed until load_gen11_heldout."""
from __future__ import annotations
from evo.office.packs import _pack
GEN11_PACKS = [
    _pack("archives", "box", "pages", "shelf", "filed", "filed_on", "box_id"),
    _pack("kiln", "batch", "celsius", "rack", "fired", "fired_on", "batch_id"),
]
for _row in GEN11_PACKS:
    _row["heldout"] = True
