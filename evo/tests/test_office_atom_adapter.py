from __future__ import annotations
import unittest
from unittest import mock

class AtomAdapterRouteTest(unittest.TestCase):
    def test_model_reply_selects_atom_adapter(self):
        from evo.office import stream
        task = {"family": "table", "skill": "add", "prompt": "x"}
        cfg = {"prefer_atoms": True, "family_skill_map": {"table": "add"}, "max_new_code": 32}
        evo = mock.Mock()
        evo.model = mock.Mock()
        decision = {
            "mode": "atom",
            "atom": "add6_mlp",
            "adapter_dir": "runs/capabilities/add6_mlp",
            "use_notes": False,
        }
        with mock.patch.object(stream, "_skill_candidates", return_value=["add"]):
            with mock.patch("evo.crystal.router.route", return_value=decision):
                with mock.patch("evo.model.add_named_adapter"):
                    with mock.patch("peft.set_peft_model_state_dict"):
                        with mock.patch("safetensors.torch.load_file", return_value={}):
                            with mock.patch("pathlib.Path.is_file", return_value=True):
                                with mock.patch("evo.generate.generate_messages", return_value="ok") as gen:
                                    fn = stream._model_reply(evo, cfg, task)
                                    out = fn([{"role": "user", "content": "hi"}])
        self.assertEqual(out, "ok")
        self.assertEqual(task.get("_route_generate", {}).get("atom"), "add6_mlp")
        # generate called with atom adapter name
        args, kwargs = gen.call_args
        self.assertIn(args[4], ("atom_policy", "atom_skill2"))

if __name__ == "__main__":
    unittest.main()
