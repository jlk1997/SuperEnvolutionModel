"""Append-only process log. One JSON object per line, plus in-memory listeners."""

from __future__ import annotations

import json
import threading
import time
from pathlib import Path


class EventBus:
    def __init__(self, path: Path | str | None = None):
        self.path = Path(path) if path else None
        self.events: list[dict] = []
        self.listeners: list = []
        self._seq = 0
        self._lock = threading.Lock()

    def emit(self, kind: str, payload: dict | None = None) -> dict:
        event = dict(payload or {})
        event["type"] = kind
        event["time"] = time.time()
        with self._lock:
            self._seq += 1
            event["seq"] = self._seq
            self.events.append(event)
            path = self.path
            listeners = list(self.listeners)
        if path is not None:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(event, ensure_ascii=False) + "\n")
        for listener in listeners:
            listener(event)
        return event
