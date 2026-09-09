"""The anthology — a compiled collection of poems (.euoc).

`bind` gathers poems into one .euoc, keeping their words word for word and
storing the gears openly underneath as JSON. Everything is decodable:
`recite` unfolds an anthology to read it, and `unbind` returns the poems.
Nothing is ever locked — the machine kneels quietly.
"""

from __future__ import annotations

import json

from .lexer import LexError, lex
from .parser import (
    Assign,
    BinOp,
    Embrace,
    Num,
    ParseError,
    Parser,
    Soul,
    Speak,
    Str,
    Summon,
    Var,
    Whisper,
)

FORMAT = "euoc-anthology"
VERSION = 1


class AnthologyError(Exception):
    pass


def _encode(node: object) -> dict:
    if isinstance(node, Num):
        return {"k": "num", "v": node.value}
    if isinstance(node, Str):
        return {"k": "str", "v": node.value}
    if isinstance(node, Var):
        return {"k": "var", "n": node.name}
    if isinstance(node, BinOp):
        return {"k": "bin", "op": node.op, "l": _encode(node.left), "r": _encode(node.right)}
    if isinstance(node, Assign):
        return {"k": "assign", "n": node.name, "v": _encode(node.value)}
    if isinstance(node, Whisper):
        return {"k": "whisper", "e": _encode(node.expr)}
    if isinstance(node, Speak):
        return {"k": "speak", "t": node.text}
    if isinstance(node, Summon):
        return {"k": "summon", "p": list(node.packages)}
    if isinstance(node, Embrace):
        return {"k": "embrace", "n": node.name}
    if isinstance(node, Soul):
        return {"k": "soul"}
    raise AnthologyError(f"this verse is foreign to me: {node!r}")


def _decode(node: dict) -> object:
    kind = node.get("k")
    if kind == "num":
        return Num(node["v"])
    if kind == "str":
        return Str(node["v"])
    if kind == "var":
        return Var(node["n"])
    if kind == "bin":
        return BinOp(node["op"], _decode(node["l"]), _decode(node["r"]))
    if kind == "assign":
        return Assign(node["n"], _decode(node["v"]))
    if kind == "whisper":
        return Whisper(_decode(node["e"]))
    if kind == "speak":
        return Speak(node["t"])
    if kind == "summon":
        return Summon(list(node["p"]))
    if kind == "embrace":
        return Embrace(node["n"])
    if kind == "soul":
        return Soul()
    raise AnthologyError(f"the anthology speaks in a tongue I do not know: {kind!r}")


def bind_sources(sources: list[tuple[str, str]]) -> bytes:
    """Turn [(name, source), ...] into the bytes of a .euoc anthology."""
    poems = []
    for name, source in sources:
        try:
            statements = Parser(lex(source)).parse()
        except (LexError, ParseError) as exc:
            raise AnthologyError(f"the poem {name} stumbles: {exc}") from None
        poems.append(
            {
                "name": name,
                "source": source,
                "statements": [_encode(s) for s in statements],
            }
        )
    doc = {"format": FORMAT, "version": VERSION, "poems": poems}
    return json.dumps(doc, ensure_ascii=False, indent=2).encode("utf-8")


def load_anthology(data: bytes) -> dict:
    try:
        doc = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AnthologyError("this is no anthology I can read") from None
    if doc.get("format") != FORMAT:
        raise AnthologyError("this page belongs to another book")
    if doc.get("version") != VERSION:
        raise AnthologyError(f"this anthology speaks version {doc.get('version')}, I know only {VERSION}")
    return doc


def poem_sources(doc: dict) -> list[tuple[str, str]]:
    return [(p["name"], p["source"]) for p in doc["poems"]]


def compiled_statements(doc: dict) -> list[object]:
    statements: list[object] = []
    for poem in doc["poems"]:
        statements.extend(_decode(s) for s in poem["statements"])
    return statements