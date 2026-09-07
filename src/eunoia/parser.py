from __future__ import annotations

from dataclasses import dataclass

from .lexer import EOF, KEYWORD, NAME, NEWLINE, NUMBER, OP, STRING, Token


class ParseError(Exception):
    pass


@dataclass
class Num:
    value: int | float


@dataclass
class Str:
    value: str


@dataclass
class Var:
    name: str


@dataclass
class BinOp:
    op: str
    left: object
    right: object


@dataclass
class Assign:
    name: str
    value: object


@dataclass
class Whisper:
    expr: object


@dataclass
class Speak:
    text: str


@dataclass
class Summon:
    packages: list[str]


@dataclass
class Embrace:
    name: str


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0

    def _peek(self, n: int = 0) -> Token:
        return self.tokens[min(self.pos + n, len(self.tokens) - 1)]

    def _advance(self) -> Token:
        tok = self.tokens[self.pos]
        if tok.type != EOF:
            self.pos += 1
        return tok

    def _skip_newlines(self) -> None:
        while self._peek().type == NEWLINE:
            self._advance()

    def parse(self) -> list[object]:
        statements: list[object] = []
        self._skip_newlines()
        while self._peek().type != EOF:
            statements.append(self._statement())
            self._skip_newlines()
        return statements

    def _statement(self) -> object:
        tok = self._advance()
        if tok.type == KEYWORD:
            if tok.value == "let":
                return self._assign(tok)
            if tok.value == "whisper":
                return self._whisper(tok)
            if tok.value == "speak":
                return self._speak(tok)
            if tok.value == "summon":
                return self._summon(tok)
            if tok.value == "embrace":
                return self._embrace(tok)
        raise ParseError(f"line {tok.line}: {tok.value or tok.type} cannot open a verse")

    def _assign(self, tok: Token) -> Assign:
        name = self._advance()
        if name.type != NAME:
            raise ParseError(f"line {name.line}: expect a name after 'let'")
        be = self._advance()
        if not (be.type == KEYWORD and be.value == "be"):
            raise ParseError(f"line {be.line}: expect 'be' after the name")
        value = self._expr()
        self._expect_eol(tok.line)
        return Assign(name.value, value)

    def _whisper(self, tok: Token) -> Whisper:
        expr = self._expr()
        self._expect_eol(tok.line)
        return Whisper(expr)

    def _speak(self, tok: Token) -> Speak:
        s = self._advance()
        if s.type != STRING:
            raise ParseError(f"line {s.line}: speak wants a quoted line")
        self._expect_eol(tok.line)
        return Speak(s.value)

    def _summon(self, tok: Token) -> Summon:
        packages: list[str] = []
        while self._peek().type == NAME:
            packages.append(self._advance().value)
        if not packages:
            raise ParseError(f"line {tok.line}: summon wants at least one name")
        self._expect_eol(tok.line)
        return Summon(packages)

    def _embrace(self, tok: Token) -> Embrace:
        name = self._advance()
        if name.type != NAME:
            raise ParseError(f"line {name.line}: embrace wants a name")
        self._expect_eol(tok.line)
        return Embrace(name.value)

    def _expect_eol(self, line: int) -> None:
        t = self._peek()
        if t.type not in (NEWLINE, EOF):
            raise ParseError(f"line {line}: stray words before the line ends")

    def _expr(self) -> object:
        return self._additive()

    def _additive(self) -> object:
        node = self._multiplicative()
        while self._peek().type == OP and self._peek().value in "+-":
            op = self._advance().value
            right = self._multiplicative()
            node = BinOp(op, node, right)
        return node

    def _multiplicative(self) -> object:
        node = self._unary()
        while self._peek().type == OP and self._peek().value in "*/%":
            op = self._advance().value
            right = self._unary()
            node = BinOp(op, node, right)
        return node

    def _unary(self) -> object:
        t = self._advance()
        if t.type == NUMBER:
            return Num(t.value)
        if t.type == STRING:
            return Str(t.value)
        if t.type == NAME:
            return Var(t.value)
        raise ParseError(f"line {t.line}: expected a value here")