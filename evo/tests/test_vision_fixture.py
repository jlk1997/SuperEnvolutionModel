# -*- coding: utf-8 -*-
"""CPU tests: vision use_log fixture + atom stub (no VL weights)."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class VisionFixtureTest(unittest.TestCase):
    def test_fixture_jsonl_schema_shape(self):
        path = ROOT / "evo" / "office" / "fixtures" / "vision_use_log_fixture.jsonl"
        self.assertTrue(path.is_file(), msg=str(path))
        rows = []
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                rows.append(json.loads(line))
        self.assertGreaterEqual(len(rows), 2)
        for row in rows:
            self.assertIn(row.get("modality"), ("text", "image", "image+text"))
            self.assertIn("task_id", row)
            self.assertFalse(row.get("vl_gate_claim"))
            self.assertFalse(row.get("weights_local"))
            if row["modality"] in ("image", "image+text"):
                ref = row.get("image_ref") or {}
                self.assertEqual(len(ref.get("sha256") or ""), 64)
                self.assertTrue(ref.get("uri"))
                self.assertTrue(ref.get("mime"))

    def test_atom_stub_pending(self):
        path = ROOT / "evo" / "office" / "fixtures" / "vision_atom_stub.json"
        alt = ROOT / "runs" / "capabilities" / "vision_table_uselog" / "atom_stub.json"
        self.assertTrue(path.is_file() or alt.is_file(), msg=f"{path} or {alt}")
        data = json.loads((path if path.is_file() else alt).read_text(encoding="utf-8"))
        self.assertEqual(data.get("status"), "stub_pending_weights")
        self.assertFalse(data.get("weights_local"))
        self.assertFalse(data.get("vl_gate_claim"))
        self.assertIsNone(data.get("bare_rate"))


class ShadowReadonlyPilotTest(unittest.TestCase):
    def test_pilot_contracts(self):
        from evo.office.shadow_readonly_pilot import run_shadow_readonly_pilot

        with tempfile.TemporaryDirectory(prefix="evo-shadow-ro-") as tmp:
            root = Path(tmp) / "shadow_readonly_pilot"
            ev = run_shadow_readonly_pilot(root=root, write_evidence=False)
            self.assertTrue(ev["pass"], msg=json.dumps(ev, ensure_ascii=False)[:2000])
            c = ev["contracts"]
            self.assertTrue(c["multi_file_inventory_read"])
            self.assertTrue(c["seed_digests_intact"])
            self.assertTrue(c["shadow_no_durable_write"])
            self.assertTrue(c["escape_refused"])
            self.assertTrue(c["beyond_smoke"])


if __name__ == "__main__":
    unittest.main()
