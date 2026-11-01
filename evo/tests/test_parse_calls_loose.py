from __future__ import annotations
import unittest
from evo.computer.actions import parse_calls

class LooseParseTest(unittest.TestCase):
    def test_loose_function_shell(self):
        text = """<function>shell>
<parameter>command>
type notes.txt
</parameter>
</function>"""
        calls = parse_calls(text)
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].name, "shell")
        self.assertEqual(calls[0].arguments.get("cmd"), "type notes.txt")

    def test_anonymous_parameter(self):
        text = """<function>shell</function><parameter>type notes.txt</parameter>"""
        calls = parse_calls(text)
        self.assertEqual(calls[0].name, "shell")
        self.assertEqual(calls[0].arguments.get("cmd"), "type notes.txt")

    def test_strict_still_works(self):
        text = """<tool_call>
<function=finish>
<parameter=answer>
done
</parameter>
</function>
</tool_call>"""
        calls = parse_calls(text)
        self.assertEqual(calls[0].name, "finish")
        self.assertEqual(calls[0].arguments.get("answer"), "done")

if __name__ == "__main__":
    unittest.main()
