from __future__ import annotations

import contextlib
import io
import unittest

from eunoia.anthology import (
    AnthologyError,
    bind_sources,
    compiled_statements,
    load_anthology,
    poem_sources,
)
from eunoia.interpreter import Interpreter
from eunoia.lexer import LexError


def _recite_statements(statements: list[object]) -> str:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        Interpreter().run(statements)
    return buf.getvalue()


class AnthologyTest(unittest.TestCase):
    def test_roundtrip_keeps_every_output(self) -> None:
        sources = [
            ("hello", 'let hello be "wow"\nwhisper hello\n'),
            ("arithmetic", "let garden be five times six\nwhisper garden\n"),
        ]
        data = bind_sources(sources)
        doc = load_anthology(data)

        expected = "wow\n" + "30\n"
        self.assertEqual(_recite_statements(compiled_statements(doc)), expected)

    def test_sources_come_back_word_for_word(self) -> None:
        source = 'let hello be "wow"\nwhisper hello\n'
        doc = load_anthology(bind_sources([("hello", source)]))
        self.assertEqual(poem_sources(doc), [("hello", source)])

    def test_soul_roundtrip(self) -> None:
        doc = load_anthology(bind_sources([("soul", "whisper the soul\n")]))
        out = _recite_statements(compiled_statements(doc))
        self.assertIn("The Soul of Eunoia", out)

    def test_keeps_poem_order_in_the_anthology(self) -> None:
        sources = [("a", 'speak "first"\n'), ("c", 'speak "last"\n')]
        doc = load_anthology(bind_sources(sources))
        self.assertEqual(_recite_statements(compiled_statements(doc)), "first\nlast\n")

    def test_rejects_foreign_bytes(self) -> None:
        with self.assertRaises(AnthologyError):
            load_anthology(b"not a poem, just noise")
        with self.assertRaises(AnthologyError):
            load_anthology(b'{"format":"other","version":1,"poems":[]}')

    def test_rejects_a_stumbling_poem(self) -> None:
        with self.assertRaises(AnthologyError):
            bind_sources([("broken", "let hello be\n")])


if __name__ == "__main__":
    unittest.main()