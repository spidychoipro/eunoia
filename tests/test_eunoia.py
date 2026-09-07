import contextlib
import io
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from eunoia.interpreter import EunoiaError, Interpreter
from eunoia.lexer import LexError, lex
from eunoia.parser import ParseError, Parser


def run(source: str) -> str:
    statements = Parser(lex(source)).parse()
    interp = Interpreter()
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        interp.run(statements)
    return buf.getvalue().rstrip("\n")


class AssignmentTest(unittest.TestCase):
    def test_let_be_string(self):
        self.assertEqual(run('let hello be "wow"\nwhisper hello\n'), "wow")

    def test_let_be_reference(self):
        self.assertEqual(run('let wow be "wow"\nlet hello be wow\nwhisper hello\n'), "wow")


class ArithmeticTest(unittest.TestCase):
    def assert_whisper(self, expr: str, expected: str):
        self.assertEqual(run(f"whisper {expr}\n"), expected)

    def test_add(self):
        self.assert_whisper("two and three", "5")
        self.assert_whisper("two with three", "5")

    def test_subtract(self):
        self.assert_whisper("ten without four", "6")

    def test_multiply(self):
        self.assert_whisper("five times six", "30")

    def test_divide(self):
        self.assert_whisper("a dozen over four", "3")
        self.assert_whisper("one over two", "0.5")

    def test_divide_shared_among(self):
        self.assert_whisper("a dozen shared among four", "3")

    def test_modulo(self):
        self.assert_whisper("twelve keeps five", "2")

    def test_precedence(self):
        self.assert_whisper("two and three times four", "14")

    def test_assignment_flows(self):
        self.assertEqual(
            run("let share be a dozen over four\nwhisper share\n"), "3"
        )


class NumberWordsTest(unittest.TestCase):
    def assert_whisper(self, expr: str, expected: str):
        self.assertEqual(run(f"whisper {expr}\n"), expected)

    def test_hundreds(self):
        self.assert_whisper("one hundred and five", "105")

    def test_dozen(self):
        self.assert_whisper("two dozen over four", "6")

    def test_score(self):
        self.assert_whisper("a score and one", "21")

    def test_million(self):
        self.assert_whisper("two million over a thousand", "2000")


class SpeakTest(unittest.TestCase):
    def test_speak_string(self):
        self.assertEqual(run('speak "I am the poem"\n'), "I am the poem")


class EmbraceTest(unittest.TestCase):
    def test_embrace_math(self):
        statements = Parser(lex("embrace math\n")).parse()
        interp = Interpreter()
        interp.run(statements)
        self.assertEqual(interp.env["math"].__name__, "math")

    def test_embrace_unknown(self):
        with self.assertRaises(EunoiaError):
            run("embrace no_such_muse_xyz\n")


class CommentTest(unittest.TestCase):
    def test_comment(self):
        self.assertEqual(run('let hello be "wow"  # a note\nwhisper hello\n'), "wow")


class ErrorTest(unittest.TestCase):
    def test_undefined_name(self):
        with self.assertRaises(EunoiaError):
            run("whisper ghost\n")

    def test_unclosed_string(self):
        with self.assertRaises(LexError):
            run('speak "unclosed\n')

    def test_missing_value(self):
        with self.assertRaises(ParseError):
            run("let x be\n")


if __name__ == "__main__":
    unittest.main()