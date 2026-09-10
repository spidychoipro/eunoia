from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .anthology import (
    AnthologyError,
    bind_sources,
    compiled_statements,
    load_anthology,
    poem_sources,
)
from .interpreter import EunoiaError, Interpreter
from .lexer import LexError, lex
from .parser import ParseError, Parser
from .transpile import poem_to_python


def run_source(source: str) -> None:
    statements = Parser(lex(source)).parse()
    Interpreter().run(statements)


def run_file(path: str) -> None:
    poem = Path(path)
    if poem.suffix == ".euoc":
        doc = load_anthology(poem.read_bytes())
        Interpreter().run(compiled_statements(doc))
        return
    run_source(poem.read_text(encoding="utf-8"))


def chant() -> None:
    print(f"Eunoia {__version__} - a language that reads like poetry.")
    print("Type a verse, line by line; an empty line rests the poem.")
    print('Try: let hello be "wow", then whisper hello')
    interp = Interpreter()
    while True:
        try:
            line = input(">>> ")
        except EOFError:
            break
        if not line.strip():
            break
        try:
            for stmt in Parser(lex(line)).parse():
                interp._exec(stmt)
        except (LexError, ParseError, EunoiaError) as exc:
            print(f"  (the poem stumbles: {exc})")


def _first(poems: list[str], ap: argparse.ArgumentParser, verb: str) -> str:
    if not poems:
        ap.error(f"{verb} needs a poem file")
    return poems[0]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="eunoia",
        description="recite, translate, bind, and unfold the language of poems",
    )
    ap.add_argument(
        "command",
        nargs="?",
        choices=["recite", "translate", "bind", "unbind", "write", "chant"],
        help=(
            "recite (.euo or .euoc), translate to Python, bind poems into an "
            ".euoc anthology, unbind it, write in the muse, or chant (a live REPL)"
        ),
    )
    ap.add_argument("poem", nargs="*", help="one or more poems (.euo / .euoc)")
    ap.add_argument("-o", "--out", metavar="FILE", help="translate: write Python here; bind: write the .euoc here")
    args = ap.parse_args(argv)

    if args.command == "write":
        try:
            from .ui import main as ui_main
        except ImportError:
            ap.error(
                "the muse is a separate package - grab eunoia-app, or pip install "
                "it alongside the language"
            )
            return 1
        return ui_main()
    if args.command == "chant":
        chant()
        return 0
    if args.command is None and not args.poem:
        chant()
        return 0

    if args.command == "recite" or (args.command is None and len(args.poem) == 1):
        path = _first(args.poem, ap, "recite")
        try:
            run_file(path)
        except FileNotFoundError:
            print(f"no poem lies at {path}")
            return 1
        except (LexError, ParseError, EunoiaError, AnthologyError) as exc:
            print(f"the poem stumbles: {exc}")
            return 1
        return 0

    if args.command == "translate":
        path = _first(args.poem, ap, "translate")
        try:
            python = poem_to_python(Path(path).read_text(encoding="utf-8"))
        except FileNotFoundError:
            print(f"no poem lies at {path}")
            return 1
        except (LexError, ParseError) as exc:
            print(f"the poem stumbles: {exc}")
            return 1
        if args.out:
            Path(args.out).write_text(python, encoding="utf-8")
        else:
            print(python, end="")
        return 0

    if args.command == "bind":
        if not args.poem:
            ap.error("bind needs at least one poem to gather")
        out = args.out or "anthology.euoc"
        try:
            sources = [
                (Path(p).stem, Path(p).read_text(encoding="utf-8")) for p in args.poem
            ]
        except FileNotFoundError:
            print("a poem in that gathering could not be read")
            return 1
        try:
            bound = bind_sources(sources)
        except (LexError, ParseError, AnthologyError) as exc:
            print(f"the poem stumbles: {exc}")
            return 1
        try:
            Path(out).write_bytes(bound)
        except OSError:
            print(f"the ink would not dry on {out}")
            return 1
        print(f"(bound {len(sources)} poem{'s' if len(sources) != 1 else ''} into {out})")
        return 0

    if args.command == "unbind":
        path = _first(args.poem, ap, "unbind")
        try:
            doc = load_anthology(Path(path).read_bytes())
        except FileNotFoundError:
            print(f"no anthology lies at {path}")
            return 1
        except AnthologyError as exc:
            print(f"the anthology stumbles: {exc}")
            return 1
        for name, source in poem_sources(doc):
            print(f"=== {name} ===")
            print(source, end="")
            print()
        return 0

    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())