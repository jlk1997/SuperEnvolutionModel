# -*- coding: utf-8 -*-
"""Write-guarded shadow pilot contracts (CPU)."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from evo.office.shadow_write_guarded_pilot import run_shadow_write_guarded_pilot


class ShadowWriteGuardedTest(unittest.TestCase):
    def test_allowlist_contracts(self):
        with tempfile.TemporaryDirectory(prefix="evo-wg-") as tmp:
            root = Path(tmp) / "shadow_write_guarded"
            evidence = run_shadow_write_guarded_pilot(root=root, write_evidence=False)
            self.assertTrue(evidence["pass"], msg=json.dumps(evidence["contracts"], ensure_ascii=True))
            c = evidence["contracts"]
            self.assertTrue(c["allowlisted_write_persists"])
            self.assertTrue(c["non_allowlisted_write_refused"])
            self.assertTrue(c["shadow_still_blocks"])
            self.assertTrue(c["escape_refused"])
            sandbox = Path(evidence["sandbox"])
            self.assertTrue((sandbox / "out.txt").is_file())
            self.assertFalse((sandbox / "secret.txt").exists())
            self.assertFalse((Path(evidence["outside"]) / "escape.txt").exists())


if __name__ == "__main__":
    unittest.main()
