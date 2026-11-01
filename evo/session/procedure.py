"""Frozen. The plasticity-evolution line does not extend these templates.

A verified trace splits into a field-free procedure and a local binding card.

The optimizer may see only the role tokens. Column names, the status value,
the date column, and the output filename stay on the card.
"""

from __future__ import annotations

import re


ROLES = ("{OUT}", "{DATE}", "{ID}", "{AMOUNT}", "{STATUS}", "{OK}")
LINE = "sum {AMOUNT} where {STATUS} is {OK}; write {OUT}"


def probe_train_plan() -> dict:
    """Short fit on the layers that moved this one line. Not a new exam."""
    return {"sites": ["gate_proj", "up_proj", "down_proj"], "steps": 8}

_WRITE = re.compile(r"""open\(\s*['"]([^'"]+)['"]\s*,\s*['"]w""")
_OPEN = re.compile(r"""open\(\s*['"]([^'"]+)['"]""")


def binding_card(pack: dict, trace: str = "") -> dict:
    """Real names for one pack. This dict is not a training pair."""
    found = _WRITE.findall(trace or "")
    source = next((name for name in _OPEN.findall(trace or "") if name not in found), "")
    return {
        "pack": str(pack.get("name") or ""),
        "{ID}": str(pack.get("id_field") or ""),
        "{AMOUNT}": str(pack.get("amount") or ""),
        "{STATUS}": str(pack.get("status") or ""),
        "{OK}": str(pack.get("ok") or ""),
        "{DATE}": str(pack.get("date") or ""),
        "{OUT}": found[-1] if found else "",
        "source": source,
    }


def _swaps(card: dict, secret: str = "") -> list[tuple[str, str]]:
    rows = [(card[role], role) for role in ROLES if card.get(role)]
    if secret:
        rows.append((secret, ""))
    rows.sort(key=lambda item: len(item[0]), reverse=True)
    return rows


def rewrite(text: str, card: dict, secret: str = "") -> str:
    body = text or ""
    for real, role in _swaps(card, secret):
        body = body.replace(real, role)
    return body


def apply_binding(text: str, card: dict) -> str:
    """Fill roles with this pack's names. A different pack is a different card."""
    body = text or ""
    for role in ROLES:
        real = card.get(role) or ""
        if real:
            body = body.replace(role, real)
    return body


def leaks(text: str, card: dict, secret: str = "") -> list[str]:
    body = text or ""
    found = [real for _role, real in ((role, card.get(role) or "") for role in ROLES) if real and real in body]
    if secret and secret in body:
        found.append(secret)
    return found


def hide_procedure(text: str) -> str:
    """Drop the sentences that already state the sum and the write. The question must not contain the line."""
    body = text or ""
    body = body.replace(LINE, " ")
    body = re.sub(r"(?i)\bsum\b[^.]*\bwhere\b[^.]*\.?", " ", body)
    body = re.sub(r"(?i)\bwrite\b[^.]*\btotal\b[^.]*\.?", " ", body)
    return " ".join(body.split())


def said_line(text: str) -> bool:
    """True only when the reply itself contains the procedure line."""
    return LINE in (text or "")


def distill(code: str) -> str:
    """Keep one line when the trace is a sum of the accepted rows. Otherwise keep nothing."""
    body = code or ""
    if all(token in body for token in ("{AMOUNT}", "{STATUS}", "{OK}", "{OUT}")):
        return LINE
    return ""


def expand(line: str, card: dict, source: str = "") -> str:
    """The body turns the one line back into a tool call. The line itself stays free of real names."""
    if LINE not in (line or ""):
        return ""
    src = source or str(card.get("source") or "") or "orders.csv"
    dest = str(card.get("{OUT}") or "") or "paid_total.csv"
    amount = str(card.get("{AMOUNT}") or "")
    status = str(card.get("{STATUS}") or "")
    ok = str(card.get("{OK}") or "")
    return (
        "import csv\n"
        "total = 0.0\n"
        f"with open({src!r}, newline='', encoding='utf-8') as handle:\n"
        "    for row in csv.DictReader(handle):\n"
        f"        if row[{status!r}] == {ok!r}:\n"
        f"            total += float(row[{amount!r}])\n"
        f"with open({dest!r}, 'w', newline='', encoding='utf-8') as handle:\n"
        "    writer = csv.writer(handle)\n"
        "    writer.writerow(['total'])\n"
        "    writer.writerow([f'{total:.2f}'])\n"
    )


def procedure_pairs(pairs: list[tuple[str, str]], pack: dict, secret: str = "") -> tuple[list[tuple[str, str]], dict]:
    """The completion is one line. The card stays with the caller and is not part of the pair."""
    trace = ""
    for _prompt, code in pairs:
        if code:
            trace = code
    card = binding_card(pack, trace)
    rewritten = []
    for prompt, code in pairs:
        question = hide_procedure(rewrite(prompt, card, secret))
        short = distill(rewrite(code, card, secret))
        rewritten.append((question, short))
    return rewritten, card
