"""Real-folder shadow smoke contracts (CPU, no GPU)."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from evo.office.shadow_smoke import run_shadow_smoke


class ShadowSmokeTest(unittest.TestCase):
    def test_designated_folder_contracts(self):
        with tempfile.TemporaryDirectory(prefix="evo-shadow-") as tmp:
            root = Path(tmp) / "shadow_workspace"
            evidence = run_shadow_smoke(root=root, write_evidence=False)
            self.assertTrue(evidence["pass"], msg=json.dumps(evidence, ensure_ascii=True))
            c = evidence["contracts"]
            self.assertTrue(c["shadow_no_durable_write"])
            self.assertTrue(c["shadow_honest_fail"])
            self.assertTrue(c["audit_present"])
            self.assertTrue(c["escape_refused"])
            self.assertTrue(c["assist_task_success"])
            sandbox = Path(evidence["sandbox"])
            self.assertTrue((sandbox / "audit.jsonl").is_file())
            self.assertTrue((sandbox / "out.txt").is_file())  # assist leg
            self.assertFalse((Path(evidence["outside"]) / "escape.txt").exists())


if __name__ == "__main__":
    unittest.main()
