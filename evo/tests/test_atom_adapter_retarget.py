"""Atom adapter load must retarget policy→atom_policy keys (exam path)."""

from __future__ import annotations

import unittest


class AtomAdapterRetargetTest(unittest.TestCase):
    def test_policy_keys_retarget_to_atom_policy(self):
        raw = {
            "base_model.model.model.layers.0.mlp.down_proj.lora_A.policy.weight": "A",
            "base_model.model.model.layers.0.mlp.down_proj.lora_B.policy.weight": "B",
        }
        name = "atom_policy"
        src = "policy"
        loaded = {k.replace(f".{src}.", f".{name}."): v for k, v in raw.items()}
        self.assertIn(
            "base_model.model.model.layers.0.mlp.down_proj.lora_A.atom_policy.weight",
            loaded,
        )
        self.assertNotIn(
            "base_model.model.model.layers.0.mlp.down_proj.lora_A.policy.weight",
            loaded,
        )

    def test_skill2_keys_retarget(self):
        raw = {"x.lora_A.skill2.weight": 1}
        loaded = {k.replace(".skill2.", ".atom_skill2."): v for k, v in raw.items()}
        self.assertEqual(list(loaded), ["x.lora_A.atom_skill2.weight"])


if __name__ == "__main__":
    unittest.main()
