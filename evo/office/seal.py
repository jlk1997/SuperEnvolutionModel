"""The held-out seal. Development streams call this and get refused."""

from __future__ import annotations

import json
import time
from pathlib import Path


def load_heldout(opened: bool, reason: str = "", record: Path | None = None) -> list[dict]:
    if not opened:
        raise PermissionError("held-out packs are sealed; pass open_heldout with a reason")
    if not reason.strip():
        raise PermissionError("opening the seal requires a written reason")
    if record is not None and record.is_file():
        previous = json.loads(record.read_text(encoding="utf-8"))
        if previous.get("packs"):
            raise PermissionError("this seal was already opened; the next round needs a new pack")
    from evo.office.heldout import HELD_PACKS

    if record is not None:
        record.parent.mkdir(parents=True, exist_ok=True)
        record.write_text(
            json.dumps({"opened": time.time(), "reason": reason, "packs": [pack["name"] for pack in HELD_PACKS]}, indent=2),
            encoding="utf-8",
        )
    return list(HELD_PACKS)


def load_next_heldout(opened: bool, reason: str = "", record: Path | None = None) -> list[dict]:
    """The pair that replaces grades and roster. Still sealed. Opening it burns it."""
    if not opened:
        raise PermissionError("the next held-out packs are sealed")
    if not reason.strip():
        raise PermissionError("opening the seal requires a written reason")
    from evo.office.heldout_next import NEXT_PACKS

    if record is not None and record.is_file():
        previous = json.loads(record.read_text(encoding="utf-8"))
        if previous.get("packs"):
            raise PermissionError("this seal was already opened; the next round needs a new pack")
    if record is not None:
        record.parent.mkdir(parents=True, exist_ok=True)
        record.write_text(
            json.dumps(
                {"opened": time.time(), "reason": reason, "packs": [pack["name"] for pack in NEXT_PACKS], "generation": "next"},
                indent=2,
            ),
            encoding="utf-8",
        )
    return list(NEXT_PACKS)


def load_gen3_heldout(opened: bool, reason: str = "", record: Path | None = None) -> list[dict]:
    """Third sealed pair (ferry, bakery). Opening burns it."""
    if not opened:
        raise PermissionError("the gen3 held-out packs are sealed")
    if not reason.strip():
        raise PermissionError("opening the seal requires a written reason")
    from evo.office.heldout_gen3 import GEN3_PACKS

    if record is not None and record.is_file():
        previous = json.loads(record.read_text(encoding="utf-8"))
        if previous.get("packs"):
            raise PermissionError("this seal was already opened; the next round needs a new pack")
    if record is not None:
        record.parent.mkdir(parents=True, exist_ok=True)
        record.write_text(
            json.dumps(
                {
                    "opened": time.time(),
                    "reason": reason,
                    "packs": [pack["name"] for pack in GEN3_PACKS],
                    "generation": "gen3",
                },
                indent=2,
            ),
            encoding="utf-8",
        )
    return list(GEN3_PACKS)


def load_gen4_heldout(opened: bool, reason: str = "", record: Path | None = None) -> list[dict]:
    """Fourth sealed pair (museum, pharmacy). Opening burns it."""
    if not opened:
        raise PermissionError("the gen4 held-out packs are sealed")
    if not reason.strip():
        raise PermissionError("opening the seal requires a written reason")
    from evo.office.heldout_gen4 import GEN4_PACKS

    if record is not None and record.is_file():
        previous = json.loads(record.read_text(encoding="utf-8"))
        if previous.get("packs"):
            raise PermissionError("this seal was already opened; the next round needs a new pack")
    if record is not None:
        record.parent.mkdir(parents=True, exist_ok=True)
        record.write_text(
            json.dumps(
                {
                    "opened": time.time(),
                    "reason": reason,
                    "packs": [pack["name"] for pack in GEN4_PACKS],
                    "generation": "gen4",
                },
                indent=2,
            ),
            encoding="utf-8",
        )
    return list(GEN4_PACKS)


def load_gen5_heldout(opened: bool, reason: str = "", record: Path | None = None) -> list[dict]:
    """Fifth sealed pair (cinema, nursery). Opening burns it."""
    if not opened:
        raise PermissionError("the gen5 held-out packs are sealed")
    if not reason.strip():
        raise PermissionError("opening the seal requires a written reason")
    from evo.office.heldout_gen5 import GEN5_PACKS

    if record is not None and record.is_file():
        previous = json.loads(record.read_text(encoding="utf-8"))
        if previous.get("packs"):
            raise PermissionError("this seal was already opened; the next round needs a new pack")
    if record is not None:
        record.parent.mkdir(parents=True, exist_ok=True)
        record.write_text(
            json.dumps(
                {
                    "opened": time.time(),
                    "reason": reason,
                    "packs": [pack["name"] for pack in GEN5_PACKS],
                    "generation": "gen5",
                },
                indent=2,
            ),
            encoding="utf-8",
        )
    return list(GEN5_PACKS)


def load_gen6_heldout(opened: bool, reason: str = "", record: Path | None = None) -> list[dict]:
    """Sixth sealed pair (harbor, orchard). Opening burns it."""
    if not opened:
        raise PermissionError("the gen6 held-out packs are sealed")
    if not reason.strip():
        raise PermissionError("opening the seal requires a written reason")
    from evo.office.heldout_gen6 import GEN6_PACKS

    if record is not None and record.is_file():
        previous = json.loads(record.read_text(encoding="utf-8"))
        if previous.get("packs"):
            raise PermissionError("this seal was already opened; the next round needs a new pack")
    if record is not None:
        record.parent.mkdir(parents=True, exist_ok=True)
        record.write_text(
            json.dumps(
                {
                    "opened": time.time(),
                    "reason": reason,
                    "packs": [pack["name"] for pack in GEN6_PACKS],
                    "generation": "gen6",
                },
                indent=2,
            ),
            encoding="utf-8",
        )
    return list(GEN6_PACKS)


def load_gen7_heldout(opened: bool, reason: str = "", record: Path | None = None) -> list[dict]:
    """Seventh sealed pair (atelier, foundry). Opening burns it."""
    if not opened:
        raise PermissionError("the gen7 held-out packs are sealed")
    if not reason.strip():
        raise PermissionError("opening the seal requires a written reason")
    from evo.office.heldout_gen7 import GEN7_PACKS

    if record is not None and record.is_file():
        previous = json.loads(record.read_text(encoding="utf-8"))
        if previous.get("packs"):
            raise PermissionError("this seal was already opened; the next round needs a new pack")
    if record is not None:
        record.parent.mkdir(parents=True, exist_ok=True)
        record.write_text(
            json.dumps(
                {
                    "opened": time.time(),
                    "reason": reason,
                    "packs": [pack["name"] for pack in GEN7_PACKS],
                    "generation": "gen7",
                },
                indent=2,
            ),
            encoding="utf-8",
        )
    return list(GEN7_PACKS)


def load_gen8_heldout(opened: bool, reason: str = "", record: Path | None = None) -> list[dict]:
    """Eighth sealed pair (marina, greenhouse). Opening burns it."""
    if not opened:
        raise PermissionError("the gen8 held-out packs are sealed")
    if not reason.strip():
        raise PermissionError("opening the seal requires a written reason")
    from evo.office.heldout_gen8 import GEN8_PACKS

    if record is not None and record.is_file():
        previous = json.loads(record.read_text(encoding="utf-8"))
        if previous.get("packs"):
            raise PermissionError("this seal was already opened; the next round needs a new pack")
    if record is not None:
        record.parent.mkdir(parents=True, exist_ok=True)
        record.write_text(
            json.dumps(
                {
                    "opened": time.time(),
                    "reason": reason,
                    "packs": [pack["name"] for pack in GEN8_PACKS],
                    "generation": "gen8",
                },
                indent=2,
            ),
            encoding="utf-8",
        )
    return list(GEN8_PACKS)


def load_gen9_heldout(opened: bool, reason: str = "", record: Path | None = None) -> list[dict]:
    """Ninth sealed pair (lighthouse, tannery). Opening burns it."""
    if not opened:
        raise PermissionError("the gen9 held-out packs are sealed")
    if not reason.strip():
        raise PermissionError("opening the seal requires a written reason")
    from evo.office.heldout_gen9 import GEN9_PACKS

    if record is not None and record.is_file():
        previous = json.loads(record.read_text(encoding="utf-8"))
        if previous.get("packs"):
            raise PermissionError("this seal was already opened; the next round needs a new pack")
    if record is not None:
        record.parent.mkdir(parents=True, exist_ok=True)
        record.write_text(
            json.dumps(
                {
                    "opened": time.time(),
                    "reason": reason,
                    "packs": [pack["name"] for pack in GEN9_PACKS],
                    "generation": "gen9",
                },
                indent=2,
            ),
            encoding="utf-8",
        )
    return list(GEN9_PACKS)


def load_gen10_heldout(opened: bool, reason: str = "", record: Path | None = None) -> list[dict]:
    """Tenth sealed pair (observatory, apiary). Opening burns it."""
    if not opened:
        raise PermissionError("the gen10 held-out packs are sealed")
    if not reason.strip():
        raise PermissionError("opening the seal requires a written reason")
    from evo.office.heldout_gen10 import GEN10_PACKS

    if record is not None and record.is_file():
        previous = json.loads(record.read_text(encoding="utf-8"))
        if previous.get("packs"):
            raise PermissionError("this seal was already opened; the next round needs a new pack")
    if record is not None:
        record.parent.mkdir(parents=True, exist_ok=True)
        record.write_text(
            json.dumps(
                {
                    "opened": time.time(),
                    "reason": reason,
                    "packs": [pack["name"] for pack in GEN10_PACKS],
                    "generation": "gen10",
                },
                indent=2,
            ),
            encoding="utf-8",
        )
    return list(GEN10_PACKS)

def load_gen11_heldout(opened: bool, reason: str = '', record: Path | None = None) -> list[dict]:
    """Eleventh sealed pair (archives, kiln). Opening burns it."""
    if not opened:
        raise PermissionError('the gen11 held-out packs are sealed')
    if not reason.strip():
        raise PermissionError('opening the seal requires a written reason')
    from evo.office.heldout_gen11 import GEN11_PACKS
    if record is not None and record.is_file():
        previous = json.loads(record.read_text(encoding='utf-8'))
        if previous.get('packs'):
            raise PermissionError('this seal was already opened; the next round needs a new pack')
    if record is not None:
        record.parent.mkdir(parents=True, exist_ok=True)
        record.write_text(json.dumps({'opened': time.time(), 'reason': reason, 'packs': [pack['name'] for pack in GEN11_PACKS], 'generation': 'gen11'}, indent=2), encoding='utf-8')
    return list(GEN11_PACKS)

