"""Development industry packs. Held-out packs are not imported from here."""

from __future__ import annotations


def _pack(name: str, record: str, amount: str, status: str, ok: str, date: str, id_field: str) -> dict:
    return {
        "name": name,
        "record": record,
        "amount": amount,
        "status": status,
        "ok": ok,
        "date": date,
        "id_field": id_field,
        "heldout": False,
    }


DEV_PACKS = [
    _pack("orders", "order", "amount", "status", "paid", "ordered_on", "order_id"),
    _pack("expenses", "claim", "cost", "state", "approved", "spent_on", "claim_id"),
    _pack("attendance", "shift", "hours", "mark", "present", "work_day", "shift_id"),
    _pack("parcels", "parcel", "weight", "stage", "delivered", "sent_on", "parcel_id"),
]


def pack_by_name(name: str) -> dict:
    for pack in DEV_PACKS:
        if pack["name"] == name:
            return pack
    raise KeyError(name)
