from __future__ import annotations

import re
from dataclasses import dataclass

from . import lexicon

KEYWORD = "KEYWORD"
OP = "OP"
NUMBER = "NUMBER"
STRING = "STRING"
NAME = "NAME"
NEWLINE = "NEWLINE"
EOF = "EOF"


class LexError(Exception):
    pass


@dataclass(frozen=True)
class Token:
    type: str
    value: object = None
    line: int = 0


_WORD = re.compile(r"[A-Za-z_]+")


def _is_number_word(word: str) -> bool:
    return (
        word in lexicon.UNITS
        or word in lexicon.TEENS
        or word in lexicon.TENS
        or word in lexicon.SCALES
    )


def number_from_words(words: list[str]) -> int:
    total = 0
    current = 0
    for word in words:
        if word in lexicon.SCALES:
            current = (current or 1) * lexicon.SCALES[word]
        else:
            current += (
                lexicon.UNITS.get(word)
                or lexicon.TEENS.get(word)
                or lexicon.TENS.get(word)
            )
    return total + current


def lex(text: str) -> list[Token]:
    raw: list[Token] = []
    line = 1
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if ch in " \t":
            i += 1
        elif ch == '"':
            end = text.find('"', i + 1)
            if end == -1:
                raise LexError(f"line {line}: a string is left open, its words unanswered")
            raw.append(Token(STRING, text[i + 1:end], line))
            i = end + 1
        elif ch == "#":
            while i < n and text[i] != "\n":
                i += 1
        elif ch == "\n":
            raw.append(Token(NEWLINE, "\n", line))
            line += 1
            i += 1
        else:
            m = _WORD.match(text, i)
            if not m:
                raise LexError(f"line {line}: a strange mark {ch!r} that no poem knows")
            raw.append(Token(NAME, m.group(0), line))
            i = m.end()
    return _fold(raw)


def _fold(raw: list[Token]) -> list[Token]:
    tokens: list[Token] = []
    i = 0
    while i < len(raw):
        tok = raw[i]
        if tok.type == NAME:
            word = tok.value
            if word == "shared" and i + 1 < len(raw) and raw[i + 1].value == "among":
                tokens.append(Token(OP, "/", tok.line))
                i += 2
                continue
            if word in lexicon.OPERATORS:
                tokens.append(Token(OP, lexicon.OPERATORS[word], tok.line))
                i += 1
                continue
            if word in lexicon.KEYWORDS:
                tokens.append(Token(KEYWORD, word, tok.line))
                i += 1
                continue
            run, j = _number_run(raw, i)
            if run:
                tokens.append(Token(NUMBER, number_from_words(run), tok.line))
                i = j
                continue
        tokens.append(tok)
        i += 1
    tokens.append(Token(EOF, None, raw[-1].line if raw else 1))
    return tokens


def _number_run(raw: list[Token], start: int) -> tuple[list[str], int]:
    run: list[str] = []
    j = start
    while j < len(raw) and _is_number_word(raw[j].value):
        run.append(raw[j].value)
        j += 1
    return run, j