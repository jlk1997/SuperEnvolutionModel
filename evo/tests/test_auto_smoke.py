"""Auto (assist→promote→apply) smoke contracts + license gate."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from evo.computer.actions import format_call, parse_calls
from evo.computer.license import License
from evo.office.auto_ledger import eligible_families, record_success
from evo.office.auto_smoke import run_auto_smoke


class AutoLicenseTest(unittest.TestCase):
    def test_auto_requires_promoted_family(self):
        call = parse_calls(format_call("write_file", {"path": "out.txt", "text": "x"}))[0]
        cold = License(grants={"write"}, mode="auto", auto_families=set(), max_steps=2)
        self.assertIn("family", cold.decide(call, "report"))
        self.assertIn("family", cold.decide(call, None))
        hot = License(grants={"write"}, mode="auto", auto_families={"report"}, max_steps=2)
        self.assertEqual(hot.decide(call, "report"), [])
        self.assertIn("family", hot.decide(call, "table"))


class AutoLedgerTest(unittest.TestCase):
    def test_record_and_eligible(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "promote.json"
            record_success(path, "report", n=1)
            self.assertEqual(eligible_families(ledger_path=path, min_n=1), {"report"})
            self.assertEqual(eligible_families(ledger_path=path, min_n=2), set())


class AutoSmokeTest(unittest.TestCase):
    def test_designated_folder_auto_contracts(self):
        with tempfile.TemporaryDirectory(prefix="evo-auto-") as tmp:
            root = Path(tmp) / "shadow_workspace"
            evidence = run_auto_smoke(root=root, write_evidence=False, min_n=1)
            self.assertTrue(evidence["pass"], msg=json.dumps(evidence, ensure_ascii=True))
            c = evidence["contracts"]
            self.assertTrue(c["auto_cold_refused"])
            self.assertTrue(c["assist_promote"])
            self.assertTrue(c["auto_hot_applies"])
            self.assertTrue(c["auto_other_family_refused"])
            self.assertTrue(c["auto_escape_blocked"])
            self.assertIn("report", evidence["promoted_families"])
            self.assertFalse((Path(evidence["outside"]) / "escape.txt").exists())


if __name__ == "__main__":
    unittest.main()
