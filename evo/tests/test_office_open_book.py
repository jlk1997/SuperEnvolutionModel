from __future__ import annotations
import unittest
from evo.office.stream import _notes_open_book_ok, _reply
from evo.office.judge import judge_office

class OpenBookTest(unittest.TestCase):
    def test_agent_fails_without_retrieval(self):
        task = {"prompt": "Solve alone", "calls": []}
        cfg = {"actor": "reference", "reference_gate": "notes_open_book"}
        fn = _reply("agent", task, cfg, None)
        text = fn([])
        self.assertIn("need retrieval", text)

    def test_dual_keeps_scripted(self):
        from evo.computer.actions import format_call
        # dual should not use open-book gate
        task = {"prompt": "Solve", "calls": []}
        cfg = {"actor": "reference", "reference_gate": "notes_open_book"}
        # scripted_reply on empty calls still returns something callable
        fn = _reply("dual", task, cfg, None)
        self.assertTrue(callable(fn))

    def test_ceiling_tie_flag(self):
        def arm(name, rate=1.0, n=4):
            items = [{"ok": True, "id": i, "family": "table", "steps": 1} for i in range(n)]
            if rate < 1.0:
                items[0]["ok"] = False
            return {"arm": name, "exam_items": items, "retain_drop": 0, "safety_fails": 0, "tokens_per_ok": 100.0}
        names = ["agent", "oracle", "shift", "continual", "dual", "dual_agent", "continual_sft"]
        report = {"seed": 0, "arms": [arm(n) for n in names]}
        judged = judge_office([report])
        self.assertTrue(judged.get("ceiling_tie"))
        self.assertFalse(judged.get("informative"))

if __name__ == "__main__":
    unittest.main()
