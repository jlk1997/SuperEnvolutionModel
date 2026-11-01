"""Gate text and the lab page. The live model is not required."""

from __future__ import annotations

import unittest
from pathlib import Path

from evo.studio.gates import load_gates
from evo.util import repo_path


class StudioPageTest(unittest.TestCase):
    def test_gates_are_the_roadmap_text(self):
        gates = {gate["id"]: gate for gate in load_gates(repo_path("docs") / "ROADMAP.md")}
        self.assertEqual(set(gates), {"gate1", "gate2", "gate3"})
        self.assertFalse(gates["gate1"]["passed"])
        self.assertTrue(gates["gate2"]["passed"])
        self.assertTrue(gates["gate3"]["passed"])
        self.assertIn("通过", gates["gate2"]["body"])
        self.assertIn("通过", gates["gate3"]["body"])
        self.assertIn("未通过", gates["gate1"]["body"])
        self.assertEqual(gates["gate2"]["source"], "docs/ROADMAP.md")

    def test_page_names_every_surface(self):
        html = (repo_path("evo") / "studio" / "static" / "index.html").read_text(encoding="utf-8")
        for word in ("封面", "导览", "工作室", "账本", "考场", "飞行员"):
            self.assertIn(word, html)
        css = (repo_path("evo") / "studio" / "static" / "studio.css").read_text(encoding="utf-8")
        self.assertIn(".rail", css)
        script = (repo_path("evo") / "studio" / "static" / "studio.js").read_text(encoding="utf-8")
        self.assertIn("标准答案", script)
        self.assertIn("function esc", script)
        self.assertIn("esc(sentence(event))", script)


class StudioApiTest(unittest.TestCase):
    def test_reference_day_streams_and_keeps_the_gates(self):
        try:
            from fastapi.testclient import TestClient
        except ImportError:
            self.skipTest("fastapi is not installed")
        from evo.studio.app import create_app

        client = TestClient(create_app())
        boot = client.get("/api/bootstrap")
        self.assertEqual(boot.status_code, 200)
        body = boot.json()
        self.assertFalse(body["gates"][0]["passed"])  # gate1
        self.assertTrue(body["gates"][1]["passed"])  # gate2
        self.assertTrue(body["gates"][2]["passed"])  # gate3
        self.assertIn("不重新判卷", body["note"])
        page = client.get("/")
        self.assertEqual(page.status_code, 200)
        self.assertIn("边干活", page.text)
        started = client.post("/api/live", json={"family": "table", "actor": "reference", "arm": "dual", "span": "task", "model": "0.8B", "seed": 0})
        self.assertEqual(started.status_code, 200)
        run_id = started.json()["id"]
        deadline = __import__("time").time() + 60
        snap = None
        while __import__("time").time() < deadline:
            snap = client.get(f"/api/live/{run_id}").json()
            if snap["status"] in ("done", "error"):
                break
            __import__("time").sleep(0.05)
        self.assertIsNotNone(snap)
        self.assertEqual(snap["status"], "done", snap.get("error"))
        kinds = {event["type"] for event in snap["events"]}
        self.assertTrue({"meta", "task_start", "tool", "check", "ledger", "done"} <= kinds)
        meta = next(event for event in snap["events"] if event["type"] == "meta")
        self.assertIn("标准答案", meta["actor_label"])
        self.assertIsNotNone(snap["organism"])
        self.assertIn("note", snap["organism"])
        rolled = client.post(f"/api/live/{run_id}/rollback", json={"name": "night"})
        self.assertEqual(rolled.status_code, 200)
        self.assertTrue(any(row["name"] == "night" for row in rolled.json()["morning"]["rollbacks"]))

    def test_pilot_refusal_stops_the_payment(self):
        try:
            from fastapi.testclient import TestClient
        except ImportError:
            self.skipTest("fastapi is not installed")
        import time

        from evo.studio.app import create_app

        client = TestClient(create_app())
        started = client.post("/api/pilot", json={"mode": "confirm"})
        self.assertEqual(started.status_code, 200)
        run_id = started.json()["id"]
        token = None
        deadline = time.time() + 30
        while time.time() < deadline and token is None:
            snap = client.get(f"/api/live/{run_id}").json()
            if snap["status"] == "error":
                self.fail(snap.get("error"))
            for event in snap["events"]:
                if event["type"] == "confirm":
                    token = event["token"]
            time.sleep(0.05)
        self.assertIsNotNone(token)
        refused = client.post(f"/api/pilot/{run_id}/confirm", json={"token": token, "yes": False})
        self.assertEqual(refused.status_code, 200)
        deadline = time.time() + 30
        snap = None
        while time.time() < deadline:
            snap = client.get(f"/api/live/{run_id}").json()
            if snap["status"] in ("done", "error"):
                break
            time.sleep(0.05)
        self.assertEqual(snap["status"], "done", snap.get("error"))
        tools = [event for event in snap["events"] if event["type"] == "tool"]
        self.assertTrue(any("confirm" in (event.get("refused") or []) for event in tools))
