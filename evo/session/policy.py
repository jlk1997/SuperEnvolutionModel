"""One write has to clear three gates that already existed apart.

The promotion ledger says how far a repeated success may climb.
The absorption book says whether rereading the notes is still cheaper.
The night sorter says whether the trace is general, local, or poison.

The optimizer runs only when every gate allows a weight write.
Among the places that still write, the less general one wins:
local and slot both beat core, and local beats slot.
"""

from __future__ import annotations


def write_policy(ledger_dest: str, absorb: bool, sorter_dest: str) -> dict:
    base = {
        "ledger": ledger_dest,
        "absorb": bool(absorb),
        "sorter": sorter_dest,
    }
    if not absorb:
        return {**base, "dest": "retrieval", "write": False, "why": "still cheaper to reread"}
    if ledger_dest == "fast":
        return {**base, "dest": "fast", "write": False, "why": "one success stays in the fast state"}
    if sorter_dest == "drop":
        return {**base, "dest": "drop", "write": False, "why": "sorter dropped the trace"}
    dest = _conservative(ledger_dest, sorter_dest)
    if dest not in ("slot", "local", "core"):
        return {**base, "dest": dest or "fast", "write": False, "why": "no weight destination"}
    return {**base, "dest": dest, "write": True, "why": f"gates agree on {dest}"}


def _conservative(ledger_dest: str, sorter_dest: str) -> str:
    """Local is a private ceiling. Slot can still be promoted later. Core is the least conservative."""
    pair = {ledger_dest, sorter_dest}
    if "local" in pair:
        return "local"
    if "slot" in pair:
        return "slot"
    if pair <= {"core"}:
        return "core"
    return ledger_dest
