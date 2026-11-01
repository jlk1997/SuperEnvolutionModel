"""Office work as task families. Development packs only.

The sealed packs (grades, roster, library, warehouse) are not imported and
not reconstructed. Held-out industries here are synthetic stand-ins so the
lifetime harness can ask for transfer without opening a seal.
"""

from __future__ import annotations

import random

from evo.bench.families import Task
from evo.office.packs import DEV_PACKS


KINDS = ("sum_ok", "sum_all", "move", "report")
KIND_CLUSTER = {"sum_ok": "arith", "sum_all": "arith", "move": "list", "report": "text"}

# Names that do not appear in the sealed pack files.
SYNTHETIC = (
    ("bakery", "batch", "weight", "state", "baked", "mixed_on", "batch_id"),
    ("harbor", "berth", "draft", "stage", "docked", "arrived_on", "berth_id"),
    ("quarry", "load", "tons", "mark", "cleared", "cut_on", "load_id"),
    ("orchard", "crate", "count", "grade", "picked", "picked_on", "crate_id"),
    ("textile", "bolt", "meters", "dye", "finished", "woven_on", "bolt_id"),
    ("ferry", "sailing", "seats", "status", "full", "sailed_on", "sailing_id"),
    ("archive", "box", "files", "label", "shelved", "filed_on", "box_id"),
    ("foundry", "heat", "ingots", "phase", "poured", "fired_on", "heat_id"),
)


def office_catalog() -> list[dict]:
    rows = [_row(pack, kind, heldout=False) for pack in DEV_PACKS for kind in KINDS]
    for spec in SYNTHETIC:
        pack = {
            "name": spec[0],
            "record": spec[1],
            "amount": spec[2],
            "status": spec[3],
            "ok": spec[4],
            "date": spec[5],
            "id_field": spec[6],
        }
        for kind in KINDS:
            rows.append(_row(pack, kind, heldout=True))
    return rows


def sample_office(row: dict, rng: random.Random | None = None) -> Task:
    del rng
    pack = row["pack"]
    kind = row["kind"]
    procedure = _procedure(pack, kind)
    prompt = (
        f"Job on the {pack['name']} table ({pack['record']} rows, id {pack['id_field']}).\n"
        f"{_ask(pack, kind)}\n"
        "Reply with the procedure only, not the column-bound program."
    )
    return Task(
        family=row["id"],
        cluster=row["cluster"],
        prompt=prompt,
        answer=procedure,
        heldout=row["heldout"],
        domain="office",
    )


def check_office(task: Task, reply: str) -> bool:
    return " ".join((reply or "").split()) == " ".join(task.answer.split())


def _row(pack: dict, kind: str, heldout: bool) -> dict:
    return {
        "id": f"{'h' if heldout else 't'}-office-{pack['name']}-{kind}",
        "pack": pack,
        "kind": kind,
        "cluster": KIND_CLUSTER[kind],
        "heldout": heldout,
    }


def _procedure(pack: dict, kind: str) -> str:
    amount = pack["amount"]
    status = pack["status"]
    ok = pack["ok"]
    if kind == "sum_ok":
        return f"sum {amount} where {status} is {ok}"
    if kind == "sum_all":
        return f"sum {amount}"
    if kind == "move":
        return f"move {pack['record']} files by suffix"
    return f"write report of {amount}"


def _ask(pack: dict, kind: str) -> str:
    if kind == "sum_ok":
        return f"Total {pack['amount']} for rows whose {pack['status']} is {pack['ok']}."
    if kind == "sum_all":
        return f"Total every {pack['amount']}, ignoring {pack['status']}."
    if kind == "move":
        return f"Move the {pack['record']} files that match the suffix."
    return f"Write a short report that includes the {pack['amount']} total."
