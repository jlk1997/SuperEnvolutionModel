"""Eighth sealed pair. Do not import from development streams.

Burned through gen7 (grades/roster … atelier/foundry). Closed until load_gen8_heldout.
"""

from __future__ import annotations

from evo.office.packs import _pack


GEN8_PACKS = [
    _pack("marina", "slip", "fees", "dock", "paid_up", "tied_on", "slip_id"),
    _pack("greenhouse", "tray", "ml", "aisle", "watered", "sown_on", "tray_id"),
]
for _row in GEN8_PACKS:
    _row["heldout"] = True
