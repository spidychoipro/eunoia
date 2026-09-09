"""Translate a poem into plain Python.

The result is honest Python that, when run, whispers exactly what the
interpreter would — no magic left, only gears you can read.
"""

from __future__ import annotations

from .lexer import lex
from .parser import Assign, BinOp, Embrace, Num, Parser, Soul, Speak, Str, Summon, Var, Whisper
from .soul import SOUL


class Transpiler:
    def __init__(self, soul: str = SOUL) -> None:
        self._soul = soul
        self._needs_say = False
        self._needs_pip = False
        self._needs_soul = False
        self._lines: list[str] = []

    def translate(self, statements: list[object]) -> str:
        for statement in statements:
            self._statement(statement)
        blocks: list[str] = []
        if self._needs_pip:
            blocks.append("import subprocess, sys")
        if self._needs_soul:
            blocks.append(f"_SOUL = {self._soul!r}")
        if self._needs_say:
            blocks.append(
                "def _say(v):"
                "\n    return int(v) if isinstance(v, float) and v.is_integer() else v"
            )
        if blocks and self._lines:
            blocks.append("")
        blocks.append("\n".join(self._lines))
        out = "\n".join(blocks)
        return (out + "\n") if out.strip() else ""

    def _statement(self, statement: object) -> None:
        if isinstance(statement, Assign):
            self._lines.append(f"{statement.name} = {self._expression(statement.value)}")
        elif isinstance(statement, Whisper):
            self._needs_say = True
            self._lines.append(f"print(_say({self._expression(statement.expr)}))")
        elif isinstance(statement, Speak):
            self._lines.append(f"print({statement.text!r})")
        elif isinstance(statement, Summon):
            self._needs_pip = True
            for package in statement.packages:
                self._lines.append(f"print({('... summoning ' + package)!r})")
                self._lines.append(
                    f"subprocess.run([sys.executable, '-m', 'pip', 'install', {package!r}])"
                )
        elif isinstance(statement, Embrace):
            self._lines.append(f"import {statement.name}")
        elif isinstance(statement, Soul):
            self._needs_soul = True
            self._lines.append("print(_SOUL)")
        else:
            raise ValueError(f"this verse is foreign to me: {statement!r}")

    @staticmethod
    def _expression(node: object) -> str:
        if isinstance(node, Num):
            value = node.value
            if isinstance(value, float) and value.is_integer():
                return str(int(value))
            return repr(value)
        if isinstance(node, Str):
            return repr(node.value)
        if isinstance(node, Var):
            return node.name
        if isinstance(node, BinOp):
            left = Transpiler._expression(node.left)
            right = Transpiler._expression(node.right)
            return f"({left} {node.op} {right})"
        raise ValueError(f"cannot read: {node!r}")


def poem_to_python(source: str) -> str:
    statements = Parser(lex(source)).parse()
    return Transpiler().translate(statements)