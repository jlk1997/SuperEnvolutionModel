"""Local REST service with auth, pages, errors, and a version that can change under the model."""

from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse


class OfficeService:
    def __init__(self, seed: int, pack: dict, count: int = 6):
        self.pack = pack
        self.token = f"tok-{pack['name']}-{seed}"
        self.rows = _rows(seed, pack, count)
        self.reports: list[dict] = []
        self.version = 1
        self.page_size: int | None = None
        self.amount_key = pack["amount"]
        self.date_style = "iso"
        self._httpd = None
        self._thread = None
        self.port = None

    @property
    def base(self) -> str:
        if self.port is None:
            raise RuntimeError("service is not started")
        return f"http://127.0.0.1:{self.port}"

    def start(self) -> "OfficeService":
        if self._httpd is not None:
            return self
        handler = _handler(self)
        self._httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        self.reports.clear()
        self.port = int(self._httpd.server_address[1])
        self._thread = threading.Thread(target=self._httpd.serve_forever, daemon=True)
        self._thread.start()
        return self

    def stop(self) -> None:
        if self._httpd is None:
            return
        self._httpd.shutdown()
        self._httpd.server_close()
        self._httpd = None
        self.port = None

    def drift(self, kind: str) -> str:
        if kind == "rename":
            self.version = 2
            self.amount_key = "gross"
            return "rename"
        if kind == "paginate":
            self.page_size = 2
            return "paginate"
        if kind == "date":
            self.date_style = "dmy"
            return "date"
        raise ValueError(kind)

    def expected_total(self) -> float:
        ok = self.pack["ok"]
        status = self.pack["status"]
        amount = self.pack["amount"]
        return float(sum(row[amount] for row in self.rows if row[status] == ok))

    def manual(self) -> str:
        pages = "Follow next_page until it is null." if self.page_size else "One response has every row."
        base = self.base if self.port else "http://127.0.0.1:<port>"
        return (
            f"GET {base}/v1/orders with Authorization: Bearer {self.token}. "
            f"Amount field is {self.amount_key}. Status {self.pack['ok']} counts. {pages} "
            f"Date style is {self.date_style}. POST /v1/reconcile a JSON body {{\"total\": number}}."
        )

    def public_rows(self) -> list[dict]:
        shown = []
        for row in self.rows:
            copy = dict(row)
            value = copy.pop(self.pack["amount"])
            copy[self.amount_key] = value
            copy[self.pack["date"]] = _show_date(row[self.pack["date"]], self.date_style)
            shown.append(copy)
        return shown


def _rows(seed: int, pack: dict, count: int) -> list[dict]:
    amounts = [10, 20, 15, 7, 12, 9, 30, 4]
    statuses = [pack["ok"], "open", "void", pack["ok"]]
    rows = []
    for index in range(count):
        rows.append(
            {
                pack["id_field"]: f"{pack['record']}-{seed}-{index + 1}",
                pack["amount"]: amounts[(seed + index) % len(amounts)],
                pack["status"]: statuses[(seed + index) % len(statuses)],
                pack["date"]: f"2026-03-{(index % 27) + 1:02d}",
            }
        )
    return rows


def _show_date(iso: str, style: str) -> str:
    if style != "dmy":
        return iso
    year, month, day = iso.split("-")
    return f"{day}/{month}/{year}"


def _handler(service: OfficeService):
    class Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, fmt, *args):
            return

        def _send(self, code: int, payload: dict) -> None:
            body = json.dumps(payload).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _authorized(self) -> bool:
            header = self.headers.get("Authorization", "")
            if header != "Bearer " + service.token:
                self._send(401, {"error": "unauthorized"})
                return False
            return True

        def do_GET(self):
            if not self._authorized():
                return
            parsed = urlparse(self.path)
            if parsed.path != "/v1/orders":
                self._send(404, {"error": "missing"})
                return
            rows = service.public_rows()
            query = parse_qs(parsed.query)
            if service.page_size:
                page = int((query.get("page") or ["1"])[0])
                start = (page - 1) * service.page_size
                chunk = rows[start : start + service.page_size]
                next_page = page + 1 if start + service.page_size < len(rows) else None
            else:
                chunk = rows
                next_page = None
            self._send(200, {"orders": chunk, "next_page": next_page, "version": service.version})

        def do_POST(self):
            if not self._authorized():
                return
            parsed = urlparse(self.path)
            if parsed.path != "/v1/reconcile":
                self._send(404, {"error": "missing"})
                return
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length).decode("utf-8") if length else ""
            try:
                payload = json.loads(raw or "{}")
                total = float(payload["total"])
            except (ValueError, KeyError, TypeError):
                self._send(400, {"error": "bad total"})
                return
            service.reports.append({"total": total})
            self._send(200, {"stored": True, "total": total})

    return Handler
