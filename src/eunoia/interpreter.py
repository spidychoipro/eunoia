from __future__ import annotations

import importlib
import operator
import subprocess
import sys

from .parser import Assign, BinOp, Embrace, Num, Soul, Speak, Str, Summon, Var, Whisper
from .soul import SOUL

_OPS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "%": operator.mod,
}


class EunoiaError(Exception):
    pass


class Interpreter:
    def __init__(self):
        self.env = {}

    def run(self, statements: list[object]) -> None:
        for statement in statements:
            self._exec(statement)

    def _exec(self, statement: object) -> None:
        if isinstance(statement, Assign):
            self.env[statement.name] = self._eval(statement.value)
        elif isinstance(statement, Whisper):
            print(self._render(self._eval(statement.expr)))
        elif isinstance(statement, Speak):
            print(statement.text)
        elif isinstance(statement, Summon):
            self._summon(statement.packages)
        elif isinstance(statement, Embrace):
            self.env[statement.name] = self._embrace(statement.name)
        elif isinstance(statement, Soul):
            print(SOUL)
        else:
            raise EunoiaError(f"this verse is foreign to me: {statement!r}")

    def _eval(self, node: object) -> object:
        if isinstance(node, Num):
            return node.value
        if isinstance(node, Str):
            return node.value
        if isinstance(node, Var):
            try:
                return self.env[node.name]
            except KeyError:
                raise EunoiaError(
                    f"no one has yet given meaning to the name '{node.name}'"
                ) from None
        if isinstance(node, BinOp):
            return _OPS[node.op](self._eval(node.left), self._eval(node.right))
        raise EunoiaError(f"cannot read: {node!r}")

    @staticmethod
    def _render(value: object) -> str:
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        if isinstance(value, (int, float, str)):
            return str(value)
        return repr(value)

    @staticmethod
    def _summon(packages: list[str]) -> None:
        for package in packages:
            print(f"... summoning {package}")
            subprocess.run([sys.executable, "-m", "pip", "install", package])

    @staticmethod
    def _embrace(name: str) -> object:
        try:
            return importlib.import_module(name)
        except ImportError:
            raise EunoiaError(
                f"the muse '{name}' has not been heard of, so summon it first"
            ) from None