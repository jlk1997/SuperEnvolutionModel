"""Fourth sealed pair. Do not import from development streams.

Burned: grades/roster, library/warehouse, ferry/bakery.
This pair stays closed until load_gen4_heldout opens it with a written reason.
"""

from __future__ import annotations

from evo.office.packs import _pack


GEN4_PACKS = [
    _pack("museum", "exhibit", "visitors", "gallery", "shown", "hung_on", "exhibit_id"),
    _pack("pharmacy", "rx", "doses", "dispense", "filled", "filled_on", "rx_id"),
]
for _row in GEN4_PACKS:
    _row["heldout"] = True
