from __future__ import annotations

import contextlib
import io
import unittest

from eunoia.interpreter import Interpreter
from eunoia.lexer import lex
from eunoia.parser import Parser
from eunoia.soul import SOUL
from eunoia.transpile import poem_to_python


def _recite(source: str) -> str:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        Interpreter().run(Parser(lex(source)).parse())
    return buf.getvalue()


def _run_python(python: str) -> str:
    buf = io.StringIO()
    ns: dict = {}
    with contextlib.redirect_stdout(buf):
        exec(compile(python, "<eunoia>", "exec"), ns)
    return buf.getvalue()


class TranspileTest(unittest.TestCase):
    def test_assign_and_whisper(self) -> None:
        python = poem_to_python('let hello be "wow"\nwhisper hello\n')
        self.assertEqual(
            python,
            "def _say(v):\n"
            "    return int(v) if isinstance(v, float) and v.is_integer() else v\n"
            "\n"
            "hello = 'wow'\n"
            "print(_say(hello))\n",
        )

    def test_arithmetic_precedence_is_preserved(self) -> None:
        python = poem_to_python("let x be two and three times four\n")
        self.assertIn("x = (2 + (3 * 4))", python)

    def test_speak_prints_quotes_plainly(self) -> None:
        python = poem_to_python('speak "she said hi"\n')
        self.assertEqual(python, "print('she said hi')\n")

    def test_summon_emits_pip(self) -> None:
        python = poem_to_python("summon flask\n")
        self.assertIn("import subprocess, sys", python)
        self.assertIn("subprocess.run([sys.executable, '-m', 'pip', 'install', 'flask'])", python)

    def test_embrace_emits_import(self) -> None:
        python = poem_to_python("embrace os\n")
        self.assertEqual(python, "import os\n")

    def test_soul_is_embedded(self) -> None:
        python = poem_to_python("whisper the soul\n")
        self.assertIn("_SOUL = ", python)
        self.assertIn("print(_SOUL)", python)

    def test_hello_poem_roundtrip(self) -> None:
        source = 'let hello be "wow"\nwhisper hello\n'
        self.assertEqual(_run_python(poem_to_python(source)), _recite(source))

    def test_arithmetic_roundtrip(self) -> None:
        source = (
            "let garden be five times six\n"
            "let share be a dozen over four\n"
            "let left be a dozen keeps five\n"
            "whisper garden\n"
            "whisper share\n"
            "whisper left\n"
        )
        self.assertEqual(_run_python(poem_to_python(source)), _recite(source))

    def test_soul_roundtrip(self) -> None:
        source = "whisper the soul\n"
        self.assertEqual(_run_python(poem_to_python(source)), _recite(source))
        self.assertIn("The Soul of Eunoia", _recite(source))

    def test_poem_files_translate_like_the_interpreter(self) -> None:
        from pathlib import Path

        repo = Path(__file__).resolve().parents[1]
        for poem in sorted((repo / "poems").glob("*.euo")):
            source = poem.read_text(encoding="utf-8")
            if "summon" in source or "embrace" in source:
                continue
            self.assertEqual(
                _run_python(poem_to_python(source)),
                _recite(source),
                poem.name,
            )

    def test_soul_travels_word_for_word(self) -> None:
        python = poem_to_python("whisper the soul\n")
        self.assertIn(SOUL.splitlines()[0], python)
        self.assertIn("Let the last line matter.", python)


if __name__ == "__main__":
    unittest.main()