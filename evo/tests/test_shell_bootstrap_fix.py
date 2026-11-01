"""Shell license aliases + practice bootstrap-on-refuse (CPU, no GPU)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from evo.computer.actions import format_call, parse_calls
from evo.computer.episode import run_episode
from evo.computer.license import License
from evo.office.families import make_task
from evo.office.stream import DEV_PACKS, _bootstrap_reply


class ShellBootstrapFixTest(unittest.TestCase):
    def test_cp_alias_and_path_refuse(self):
        lic = License(grants={"python", "shell", "read", "write", "http"})
        self.assertEqual(
            lic.decide(parse_calls(format_call("shell", {"cmd": "cp inbox\\note.txt out\\note.txt"}))[0]),
            [],
        )
        self.assertEqual(lic.decide(parse_calls(format_call("shell", {"cmd": "mkdir -p out"}))[0]), [])
        self.assertIn(
            "shell-command",
            lic.decide(parse_calls(format_call("shell", {"cmd": "cp /path/to/a /path/to/b"}))[0]),
        )

    def test_bootstrap_on_refused_shell_yields_ok(self):
        pack = DEV_PACKS[0]
        task = make_task(pack, "shell", seed=42, variant=0, difficulty=1)
        task["split"] = "practice"
        bad = format_call(
            "shell",
            {"cmd": "mkdir -p /path/to/out && cp /path/to/inbox/notes.txt /path/to/out/notes.txt"},
        )
        cfg = {
            "grants": ["python", "shell", "read", "write", "http"],
            "practice_bootstrap": True,
            "bootstrap_sft_immediate": False,
        }
        boot = _bootstrap_reply(lambda _m: bad, "dual", task, cfg, evo=None)
        with tempfile.TemporaryDirectory() as folder:
            result = run_episode(task, boot, Path(folder), License(grants=set(cfg["grants"]), max_steps=6))
        self.assertTrue(result["ok"])
        self.assertTrue(task.get("_bootstrapped"))


if __name__ == "__main__":
    unittest.main()
