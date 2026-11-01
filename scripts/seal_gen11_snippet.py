
def load_gen11_heldout(opened: bool, reason: str = "", record: Path | None = None) -> list[dict]:
    """Eleventh sealed pair (archives, kiln). Opening burns it."""
    if not opened:
        raise PermissionError("the gen11 held-out packs are sealed")
    if not reason.strip():
        raise PermissionError("opening the seal requires a written reason")
    from evo.office.heldout_gen11 import GEN11_PACKS
    if record is not None and record.is_file():
        previous = json.loads(record.read_text(encoding="utf-8"))
        if previous.get("packs"):
            raise PermissionError("this seal was already opened; the next round needs a new pack")
    if record is not None:
        record.parent.mkdir(parents=True, exist_ok=True)
        record.write_text(json.dumps({"opened": time.time(), "reason": reason, "packs": [pack["name"] for pack in GEN11_PACKS], "generation": "gen11"}, indent=2), encoding="utf-8")
    return list(GEN11_PACKS)
