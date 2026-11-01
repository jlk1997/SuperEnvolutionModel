"""Sealed industry packs.

Import this module only after the seal is opened on purpose. Opening a pack
burns it: the next milestone needs a new pack, not this one again.
"""

from __future__ import annotations

from evo.office.packs import _pack


HELD_PACKS = [
    _pack("grades", "paper", "points", "result", "passed", "sat_on", "student_id"),
    _pack("roster", "clinic", "minutes", "duty", "oncall", "clinic_day", "slot_id"),
]
for _pack_row in HELD_PACKS:
    _pack_row["heldout"] = True
