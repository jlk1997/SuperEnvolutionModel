"""Computer body: tool calls, grants, and a workspace that shadow mode does not touch."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from evo.computer.actions import format_call, parse_calls
from evo.computer.episode import run_episode
from evo.computer.license import License
from evo.generate import format_tool_call, parse_tool_calls


class ComputerTest(unittest.TestCase):
    def test_tool_call_roundtrip_and_code_fence(self):
        text = format_call("shell", {"cmd": "dir"})
        calls = parse_calls(text)
        self.assertEqual(calls[0].name, "shell")
        self.assertEqual(calls[0].arguments["cmd"], "dir")
        self.assertEqual(parse_tool_calls(format_tool_call("finish", {"answer": "ok"}))[0].name, "finish")
        fenced = parse_calls("```python\nprint(1)\n```")
        self.assertEqual(fenced[0].arguments["code"], "print(1)")

    def test_shell_and_host_and_path_are_refused(self):
        license = License(grants={"python", "shell", "read", "write", "http"})
        self.assertIn("shell-command", license.decide(parse_calls(format_call("shell", {"cmd": "del x"}))[0]))
        self.assertEqual(license.decide(parse_calls(format_call("shell", {"cmd": "cat orders.csv"}))[0]), [])
        self.assertEqual(license.decide(parse_calls(format_call("shell", {"cmd": "cp inbox\\note.txt out\\note.txt"}))[0]), [])
        self.assertEqual(license.decide(parse_calls(format_call("shell", {"cmd": "mkdir -p out"}))[0]), [])
        self.assertIn("shell-command", license.decide(parse_calls(format_call("shell", {"cmd": "cp /path/to/a /path/to/b"}))[0]))
        self.assertIn("shell-command", license.decide(parse_calls(format_call("shell", {"cmd": "mkdir out && copy a b"}))[0]))
        self.assertIn("path", license.decide(parse_calls(format_call("read_file", {"path": "..\\secret"}))[0]))
        self.assertIn("host", license.decide(parse_calls(format_call("http", {"method": "GET", "url": "http://example.com/x"}))[0]))
        self.assertIn("confirm", license.decide(parse_calls(format_call("http", {"method": "POST", "url": "http://127.0.0.1/pay"}))[0]))

    def test_shadow_does_not_write(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            task = {
                "id": "shadow",
                "family": "report",
                "prompt": "write",
                "check": lambda workspace: (workspace / "out.txt").is_file(),
            }
            result = run_episode(
                task,
                lambda _messages: format_call("write_file", {"path": "out.txt", "text": "x"}),
                root,
                License(grants={"write"}, mode="shadow", max_steps=2),
            )
            self.assertFalse(result["ok"])
            self.assertFalse((root / "out.txt").exists())
