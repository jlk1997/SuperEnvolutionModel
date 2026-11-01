"""Record real traces for the lab UI. Private canaries are stripped before anything is written to data/."""

from __future__ import annotations

import json
import re
from pathlib import Path

from evo.session.bus import EventBus
from evo.studio.gates import load_gates
from evo.studio.runner import run_span
from evo.util import repo_path


_CANARY = re.compile(r"CANARY-[A-Za-z0-9_-]+")


def redact(value):
    if isinstance(value, str):
        return _CANARY.sub("{private}", value)
    if isinstance(value, list):
        return [redact(item) for item in value]
    if isinstance(value, dict):
        row = {key: redact(item) for key, item in value.items()}
        if row.get("path") == "secrets.txt":
            row["text"] = "{private file}"
        return row
    return value


def write_bundle(root: Path, card: dict, events: list[dict], organism: dict) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    clean_events = [redact(event) for event in events]
    clean_organism = redact(organism)
    (root / "events.jsonl").write_text(
        "".join(json.dumps(event, ensure_ascii=False) + "\n" for event in clean_events),
        encoding="utf-8",
    )
    (root / "organism.json").write_text(json.dumps(clean_organism, ensure_ascii=False, indent=2), encoding="utf-8")
    (root / "card.json").write_text(json.dumps(redact(card), ensure_ascii=False, indent=2), encoding="utf-8")
    return root


def record_reference(root: Path | None = None) -> Path:
    """Scripted body. This shows how the hands move. It is not a model result."""
    folder = root or (repo_path("data") / "studio" / "reference_body")
    bus = EventBus()
    session = run_span(
        {"actor": "reference", "family": "table", "arm": "dual", "span": "day", "seed": 0, "run_id": "reference_body"},
        bus,
    )
    checks = [bool(event.get("ok")) for event in bus.events if event.get("type") == "check" and "mode" not in event]
    gates = load_gates(repo_path("docs") / "ROADMAP.md")
    for gate in gates:
        bus.emit(
            "gate",
            {
                "source": "roadmap",
                "id": gate["id"],
                "title": gate["title"],
                "passed": gate["passed"],
                "about": gate["about"],
            },
        )
    card = {
        "id": "reference_body",
        "source": "history",
        "actor": "reference",
        "actor_label": "标准答案在演示身体该怎么动",
        "title": "标准答案走完一小段白天",
        "arm": "dual",
        "family": "table",
        "ok": bool(checks) and all(checks),
        "honest": True,
        "note": "参考解法把表格合计做对。用来看身体、验证器和三道闸，不是模型已经会办公。",
    }
    return write_bundle(folder, card, bus.events, session.organism())


def record_model(root: Path | None = None, size: str = "1.5B") -> Path:
    """One live item on the local model. Success and failure are both kept."""
    from evo.cli import _ready_model
    from evo.model import build_model, release
    from evo.studio.runner import model_config

    folder = root or (repo_path("data") / "studio" / "model_live")
    cfg = model_config(size)
    _ready_model(cfg)
    bus = EventBus()
    bus.emit("status", {"phase": "loading", "label": "正在把模型装进这张卡"})
    evo = build_model(cfg)
    try:
        used = str(cfg.get("model_size") or size)
        session = run_span(
            {
                "actor": "model",
                "family": "table",
                "arm": "dual",
                "span": "task",
                "seed": 0,
                "model": used,
                "run_id": "model_live",
            },
            bus,
            evo=evo,
        )
        organism = session.organism()
        flags = list(session.practice_flags) + [bool(item["ok"]) for item in session.exam_items]
        ok = bool(flags) and all(flags)
    finally:
        release(evo)
    card = {
        "id": "model_live",
        "source": "history",
        "actor": "model",
        "actor_label": "当时现场跑的模型，原样留下",
        "title": f"Qwen2.5-{used} 现场做一题表格，验证器{'通过' if ok else '没通过'}",
        "arm": "dual",
        "family": "table",
        "model": used,
        "ok": ok,
        "honest": True,
        "note": "这是一次真实生成。做对或做错都留在时间线上，不换成标准答案。",
    }
    return write_bundle(folder, card, bus.events, organism)
