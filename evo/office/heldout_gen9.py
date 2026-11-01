"""Ninth sealed pair. Do not import from development streams.

Burned through gen8 (… marina/greenhouse). Closed until load_gen9_heldout.
"""

from __future__ import annotations

from evo.office.packs import _pack


GEN9_PACKS = [
    _pack("lighthouse", "watch", "candles", "beacon", "lit", "lit_on", "watch_id"),
    _pack("tannery", "hide", "liters", "vat", "cured", "soaked_on", "hide_id"),
]
for _row in GEN9_PACKS:
    _row["heldout"] = True
