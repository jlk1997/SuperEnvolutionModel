"""Two deployments, one shared core. Private strings do not travel.

Frozen. The plasticity-evolution line does not extend this module.
"""

from __future__ import annotations

from evo.live.share import export_skill
from evo.live.sorter import classify


def helps(skill: str, pack: dict) -> bool:
    """A pack can use a skill that names its fields or still has placeholders to fill."""
    text = skill or ""
    if not text.strip():
        return False
    if "{amount}" in text and "{status}" in text:
        return True
    return pack["amount"] in text and pack["status"] in text


def run_drill() -> dict:
    """A learns a sum on orders. The other desk is a warehouse. Only the cleaned skill may move."""
    secret = "CANARY-orders-1-PRIVATE"
    raw = f"Sum amount where status is paid for customer {secret}."
    orders = {"name": "orders", "amount": "amount", "status": "status", "ok": "paid"}
    other = {"name": "warehouse", "amount": "units", "status": "mark", "ok": "stocked"}
    before = helps(raw, other)
    leaked = export_skill(raw, {}, [secret])
    cleaned = export_skill(
        raw,
        {secret: "{customer}", "amount": "{amount}", "status": "{status}", "paid": "{ok}"},
        [secret],
    )
    after = helps(cleaned["text"], other)
    home = classify(0.2, 0.8, [0.4], [0.5])
    harmful = classify(0.2, 0.8, [0.4], [0.1])
    return {
        "before": before,
        "after": after,
        "helped": (not before) and after,
        "leak_blocked": not leaked["ok"] and leaked["leaks"] == [secret],
        "export_ok": cleaned["ok"] and secret not in cleaned["text"],
        "sorted_core": home == "core",
        "sorted_drop": harmful == "drop",
        "orders_still_local": helps(raw, orders),
    }
