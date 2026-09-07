from __future__ import annotations

import importlib
import operator
import subprocess
import sys

from .parser import Assign, BinOp, Embrace, Num, Speak, Str, Summon, Var, Whisper

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
        else:
            raise EunoiaError(f"unknown verse: {statement!r}")

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
                    f"the name '{node.name}' has not been given a meaning"
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
                f"cannot find the muse '{name}' — try summoning it first"
            ) from None