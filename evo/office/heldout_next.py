"""The next sealed pair. Development streams must not import this module.

grades and roster were opened and burned. This pair stays closed until a
milestone calls load_next_heldout with a written reason.
"""

from __future__ import annotations

from evo.office.packs import _pack


NEXT_PACKS = [
    _pack("library", "loan", "pages", "state", "returned", "borrowed_on", "loan_id"),
    _pack("warehouse", "bin", "units", "mark", "stocked", "counted_on", "bin_id"),
]
for _row in NEXT_PACKS:
    _row["heldout"] = True
