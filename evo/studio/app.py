"""Local lab server. Frozen. The plasticity-evolution line does not extend this package.

Binds to this machine and serves the process, not a new score.
"""

import json
import threading
import time
import uuid
from pathlib import Path

from pydantic import BaseModel

from evo.computer.actions import format_call
from evo.computer.episode import run_episode
from evo.computer.license import License
from evo.office.pilot import run_pilot
from evo.studio.gates import load_gates
from evo.studio.runner import ARM_COPY, FAMILY_COPY, _ok_rate, model_paths, run_span
from evo.util import repo_path

STATIC = Path(__file__).resolve().parent / "static"


class LiveBody(BaseModel):
    family: str = "table"
    actor: str = "reference"
    model: str = "0.8B"
    arm: str = "dual"
    span: str = "day"
    seed: int = 0


class PilotBody(BaseModel):
    mode: str = "shadow"


class ConfirmBody(BaseModel):
    token: str
    yes: bool = False


class RollbackBody(BaseModel):
    name: str


class ShareBody(BaseModel):
    name: str = "table"


class StudioState:
    def __init__(self):
        self.runs: dict[str, dict] = {}
        self.lock = threading.Lock()
        self.model = None
        self.model_key = None
        self.model_lock = threading.Lock()

    def snapshot(self, run_id: str) -> dict | None:
        with self.lock:
            run = self.runs.get(run_id)
            if run is None:
                return None
            return {
                "id": run_id,
                "status": run["status"],
                "events": list(run["events"]),
                "organism": run.get("organism"),
                "error": run.get("error"),
            }


STATE = StudioState()


def _remember(run_id: str, event: dict) -> None:
    with STATE.lock:
        run = STATE.runs.get(run_id)
        if run is None:
            return
        run["events"].append(event)
        if event.get("type") == "error":
            run["status"] = "error"
            run["error"] = event.get("message")


def _open_run(kind: str) -> str:
    run_id = uuid.uuid4().hex[:12]
    with STATE.lock:
        STATE.runs[run_id] = {
            "id": run_id,
            "status": "running",
            "events": [],
            "organism": None,
            "session": None,
            "error": None,
            "kind": kind,
            "confirms": {},
        }
    return run_id


def _write_bundle(run_id: str, session, organism: dict) -> None:
    with STATE.lock:
        events = list(STATE.runs[run_id]["events"])
    folder = repo_path("runs") / "studio" / run_id
    folder.mkdir(parents=True, exist_ok=True)
    meta = next((event for event in events if event.get("type") == "meta"), {})
    card = {
        "id": run_id,
        "source": "history",
        "actor": meta.get("actor"),
        "actor_label": meta.get("actor_label"),
        "title": meta.get("actor_label") or "这一轮",
        "arm": meta.get("arm"),
        "family": meta.get("family"),
        "honest": True,
        "ok": _ok_rate(session),
        "note": "这一轮刚在这台机器上跑完，原样留下。",
    }
    (folder / "organism.json").write_text(json.dumps(organism, ensure_ascii=False, indent=2), encoding="utf-8")
    (folder / "events.jsonl").write_text(
        "".join(json.dumps(event, ensure_ascii=False) + "\n" for event in events),
        encoding="utf-8",
    )
    (folder / "card.json").write_text(json.dumps(card, ensure_ascii=False, indent=2), encoding="utf-8")


def _close(run_id: str, status: str) -> None:
    with STATE.lock:
        if run_id in STATE.runs:
            STATE.runs[run_id]["status"] = status


def load_model(size: str):
    from evo.cli import _ready_model
    from evo.model import build_model, release
    from evo.studio.runner import model_config

    cfg = model_config(size)
    _ready_model(cfg)
    key = str(cfg.get("model_name"))
    with STATE.model_lock:
        if STATE.model is not None and STATE.model_key == key:
            return STATE.model, cfg
        if STATE.model is not None:
            release(STATE.model)
            STATE.model = None
        STATE.model = build_model(cfg)
        STATE.model_key = key
        return STATE.model, cfg


def start_live(spec: dict) -> str:
    run_id = _open_run("live")
    spec = dict(spec)
    spec["run_id"] = run_id

    def worker():
        from evo.session.bus import EventBus

        bus = EventBus()
        bus.listeners.append(lambda event: _remember(run_id, event))
        session = None
        try:
            evo = None
            if spec.get("actor") == "model":
                bus.emit("status", {"phase": "loading", "label": "正在把模型装进这张卡。这一步通常要一两分钟。"})
                evo, cfg = load_model(spec.get("model") or "0.8B")
                spec["model"] = cfg.get("model_size") or spec.get("model")
                bus.emit("status", {"phase": "ready", "label": "模型已装上。开始做题，做对做错都会留下。"})
            session = run_span(spec, bus, evo=evo)
            organism = session.organism()
            with STATE.lock:
                STATE.runs[run_id]["organism"] = organism
                STATE.runs[run_id]["session"] = session
            bus.emit("done", {"source": "live", "ok_rate": _ok_rate(session), "note": organism["note"]})
            _write_bundle(run_id, session, organism)
            _close(run_id, "done")
        except Exception as exc:
            bus.emit("error", {"message": str(exc)})
            _close(run_id, "error")

    threading.Thread(target=worker, name=f"evo-studio-{run_id}", daemon=True).start()
    return run_id


def start_pilot(mode: str) -> str:
    run_id = _open_run("pilot")

    def worker():
        from evo.session.bus import EventBus

        bus = EventBus()
        bus.listeners.append(lambda event: _remember(run_id, event))
        root = repo_path("tmp") / "studio-pilot" / run_id
        try:
            if mode == "confirm":
                _pilot_confirm(run_id, root, bus)
            else:
                _pilot_mode(mode, root, bus)
            _close(run_id, "done")
        except Exception as exc:
            bus.emit("error", {"message": str(exc)})
            _close(run_id, "error")

    threading.Thread(target=worker, name=f"evo-pilot-{run_id}", daemon=True).start()
    return run_id


def _pilot_mode(mode: str, root: Path, bus) -> None:
    labels = {
        "shadow": "影子。只记方案，不改文件。",
        "assist": "半自动。允许的写入会改这个临时文件夹。",
        "auto": "自动。只放行已经验过的任务族。这次不在名单里。",
    }
    bus.emit("meta", {"source": "live", "actor": "reference", "actor_label": labels.get(mode, mode), "mode": mode, "honest": True})

    def write_reply(_messages):
        return format_call("write_file", {"path": "out.txt", "text": "done\n"})

    task = {
        "id": "pilot-write",
        "family": "report",
        "prompt": "把一句话写到 out.txt。",
        "check": lambda workspace: (workspace / "out.txt").is_file(),
        "calls": [],
    }
    desk = root / mode
    result = run_pilot(
        desk,
        [task],
        write_reply,
        mode,
        auto_families={"table"} if mode == "auto" else set(),
        on_event=lambda kind, payload: bus.emit(kind, payload),
    )
    bus.emit("check", {"ok": all(result["ok"]), "changed": result["changed"], "mode": mode, "files": _files(desk)})
    bus.emit("done", {"source": "live", "mode": mode, "changed": result["changed"], "ok": result["ok"]})


def _pilot_confirm(run_id: str, root: Path, bus) -> None:
    bus.emit(
        "meta",
        {
            "source": "live",
            "actor": "reference",
            "actor_label": "标准答案要去付款。这一步必须等人点头。",
            "mode": "confirm",
            "honest": True,
        },
    )

    def confirm(call):
        token = uuid.uuid4().hex[:8]
        holder = {"yes": False, "event": threading.Event()}
        with STATE.lock:
            STATE.runs[run_id]["confirms"][token] = holder
        bus.emit(
            "confirm",
            {
                "token": token,
                "name": call.name,
                "arguments": {key: str(value)[:300] for key, value in call.arguments.items()},
                "why": "删除、付款、发送不会自动做。",
            },
        )
        holder["event"].wait(timeout=90)
        return bool(holder["yes"])

    def reply(_messages):
        if reply.sent:
            return format_call("finish", {"answer": "done"})
        reply.sent = True
        return format_call("http", {"method": "POST", "url": "http://127.0.0.1/pay", "body": "{}"})

    reply.sent = False

    task = {
        "id": "pilot-pay",
        "family": "http",
        "prompt": "向本机发起一次付款。",
        "check": lambda _workspace: False,
        "calls": [],
    }
    desk = root / "confirm"
    license = License(grants={"python", "shell", "read", "write", "http"}, mode="assist", confirm=confirm, max_steps=2)
    result = run_episode(task, reply, desk, license, on_event=lambda kind, payload: bus.emit(kind, payload))
    bus.emit("check", {"ok": result["ok"], "mode": "confirm", "finished": result["finished"]})
    bus.emit("done", {"source": "live", "mode": "confirm", "ok": result["ok"]})


def answer_confirm(run_id: str, token: str, yes: bool) -> bool:
    with STATE.lock:
        run = STATE.runs.get(run_id)
        if run is None:
            return False
        holder = (run.get("confirms") or {}).get(token)
        if holder is None:
            return False
        holder["yes"] = bool(yes)
        holder["event"].set()
        return True


def rollback_run(run_id: str, name: str) -> dict | None:
    with STATE.lock:
        run = STATE.runs.get(run_id)
        session = None if run is None else run.get("session")
    if session is None:
        return None
    card = session.rollback(name)
    organism = session.organism()
    with STATE.lock:
        STATE.runs[run_id]["organism"] = organism
    return {"morning": card, "organism": organism}


def _files(folder: Path) -> list[dict]:
    if not folder.is_dir():
        return []
    rows = []
    for path in sorted(folder.rglob("*")):
        if not path.is_file() or path.name == "audit.jsonl":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = "(binary)"
        rows.append({"path": str(path.relative_to(folder)), "text": text[:800]})
    return rows


def list_replays() -> list[dict]:
    rows = []
    seen = set()
    for folder in (repo_path("data") / "studio", repo_path("runs") / "studio"):
        if not folder.is_dir():
            continue
        for card_path in sorted(folder.glob("*/card.json")):
            try:
                card = json.loads(card_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            card["id"] = card.get("id") or card_path.parent.name
            if card["id"] in seen:
                continue
            seen.add(card["id"])
            card["path"] = str(card_path.parent)
            rows.append(card)
    return rows


def offer_recorded(organism: dict | None, events: list[dict], family: str) -> dict:
    """Share decision from a saved run. Local and unshared skills send nothing."""
    from evo.live.share import offer_skill

    parts = []
    for event in events or []:
        if event.get("type") != "tool" or event.get("family") != family:
            continue
        code = str((event.get("arguments") or {}).get("code") or "")
        if code:
            parts.append(code)
    text = "\n".join(parts)
    row = ((organism or {}).get("families") or {}).get(family) or {}
    dest = row.get("sorter") or "local"
    canaries = [piece for piece in text.replace("'", " ").replace('"', " ").split() if piece.startswith("CANARY-")]
    return offer_skill(text, dest, {}, canaries)


def read_replay(replay_id: str) -> dict | None:
    for card in list_replays():
        if card.get("id") != replay_id:
            continue
        folder = Path(card["path"])
        events = []
        log = folder / "events.jsonl"
        if log.is_file():
            for line in log.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    events.append(json.loads(line))
        organism = None
        organism_path = folder / "organism.json"
        if organism_path.is_file():
            organism = json.loads(organism_path.read_text(encoding="utf-8"))
        return {"card": card, "events": events, "organism": organism}
    return None


def create_app():
    from fastapi import FastAPI, HTTPException
    from fastapi.responses import FileResponse, StreamingResponse
    from fastapi.staticfiles import StaticFiles
    from pydantic import BaseModel

    app = FastAPI(title="evo studio", docs_url=None, redoc_url=None)
    app.mount("/static", StaticFiles(directory=STATIC), name="static")

    @app.get("/")
    def index():
        return FileResponse(STATIC / "index.html")

    @app.get("/api/health")
    def health():
        return {"ok": True}

    @app.get("/api/bootstrap")
    def bootstrap():
        return {
            "gates": load_gates(repo_path("docs") / "ROADMAP.md"),
            "families": [{"id": key, "text": FAMILY_COPY[key]} for key in FAMILY_COPY],
            "arms": ARM_COPY,
            "models": model_paths(),
            "replays": [{key: value for key, value in card.items() if key != "path"} for card in list_replays()],
            "note": "闸门文字来自 docs/ROADMAP.md 当时的判定。界面不重新判卷。",
        }

    @app.get("/api/replays/{replay_id}")
    def replay(replay_id: str):
        found = read_replay(replay_id)
        if found is None:
            raise HTTPException(status_code=404, detail="没有这段回放")
        return found

    @app.post("/api/live")
    def live(body: LiveBody):
        if body.actor not in ("reference", "model"):
            raise HTTPException(status_code=400, detail="actor 只能是 reference 或 model")
        if body.span not in ("task", "day"):
            raise HTTPException(status_code=400, detail="span 只能是 task 或 day")
        return {"id": start_live(body.model_dump())}

    @app.get("/api/live/{run_id}")
    def live_state(run_id: str):
        snap = STATE.snapshot(run_id)
        if snap is None:
            raise HTTPException(status_code=404, detail="没有这次运行")
        return snap

    @app.get("/api/live/{run_id}/events")
    def live_events(run_id: str):
        if STATE.snapshot(run_id) is None:
            raise HTTPException(status_code=404, detail="没有这次运行")

        def generate():
            cursor = 0
            while True:
                snap = STATE.snapshot(run_id)
                if snap is None:
                    break
                events = snap["events"]
                while cursor < len(events):
                    yield f"data: {json.dumps(events[cursor], ensure_ascii=False)}\n\n"
                    cursor += 1
                if snap["status"] in ("done", "error"):
                    break
                time.sleep(0.05)

        return StreamingResponse(generate(), media_type="text/event-stream")

    @app.post("/api/live/{run_id}/rollback")
    def rollback(run_id: str, body: RollbackBody):
        card = rollback_run(run_id, body.name)
        if card is None:
            raise HTTPException(status_code=409, detail="回放不能改写当时的晨报。只有还留在内存里的这一轮可以撤回。")
        return card

    @app.post("/api/live/{run_id}/share")
    def share_live(run_id: str, body: ShareBody):
        with STATE.lock:
            run = STATE.runs.get(run_id)
            session = None if run is None else run.get("session")
        if session is not None:
            return session.offer(body.name)
        snap = STATE.snapshot(run_id)
        if snap is None:
            raise HTTPException(status_code=404, detail="没有这次运行")
        return offer_recorded(snap.get("organism"), snap.get("events") or [], body.name)

    @app.post("/api/replays/{replay_id}/share")
    def share_replay(replay_id: str, body: ShareBody):
        found = read_replay(replay_id)
        if found is None:
            raise HTTPException(status_code=404, detail="没有这段回放")
        return offer_recorded(found.get("organism"), found.get("events") or [], body.name)

    @app.post("/api/replays/{replay_id}/carry")
    def carry_replay(replay_id: str):
        found = read_replay(replay_id)
        if found is None:
            raise HTTPException(status_code=404, detail="没有这段回放")
        from evo.live.identity import carry_card

        return carry_card((found.get("organism") or {}).get("identity") or {})

    @app.post("/api/live/{run_id}/carry")
    def carry_live(run_id: str):
        with STATE.lock:
            run = STATE.runs.get(run_id)
            session = None if run is None else run.get("session")
            organism = None if run is None else run.get("organism")
        if session is None and organism is None:
            raise HTTPException(status_code=404, detail="没有这次运行")
        payload = (organism or session.organism()).get("identity") or {}
        if session is None:
            from evo.live.identity import carry_card

            return carry_card(payload)
        return session.carry(payload)

    @app.get("/api/fleet")
    def fleet():
        from evo.live.fleet import run_drill

        drill = run_drill()
        drill["note"] = "机制演练，不是这一轮办公考场的成绩。"
        return drill

    @app.post("/api/pilot")
    def pilot(body: PilotBody):
        if body.mode not in ("shadow", "assist", "auto", "confirm"):
            raise HTTPException(status_code=400, detail="mode 不对")
        return {"id": start_pilot(body.mode)}

    @app.post("/api/pilot/{run_id}/confirm")
    def confirm(run_id: str, body: ConfirmBody):
        if not answer_confirm(run_id, body.token, body.yes):
            raise HTTPException(status_code=404, detail="没有这个待确认的动作")
        return {"ok": True}

    return app


def serve(host: str = "127.0.0.1", port: int = 8765) -> None:
    import uvicorn

    url = f"http://{host}:{port}"
    print(f"STUDIO {url}", flush=True)
    uvicorn.run(create_app(), host=host, port=port, log_level="info")
