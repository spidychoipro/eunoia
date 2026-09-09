from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .interpreter import EunoiaError, Interpreter
from .lexer import LexError, lex
from .parser import ParseError, Parser


def run_source(source: str) -> None:
    statements = Parser(lex(source)).parse()
    Interpreter().run(statements)


def run_file(path: str) -> None:
    run_source(Path(path).read_text(encoding="utf-8"))


def chant() -> None:
    print("Eunoia: let us begin. (press the empty line to rest)")
    interp = Interpreter()
    while True:
        try:
            line = input("  ")
        except EOFError:
            break
        if not line.strip():
            break
        try:
            for stmt in Parser(lex(line)).parse():
                interp._exec(stmt)
        except (LexError, ParseError, EunoiaError) as exc:
            print(f"  (the poem stumbles: {exc})")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="eunoia",
        description="recite a .euo poem, open the muse (a tiny IDLE), or chant (a live REPL)",
    )
    ap.add_argument(
        "command",
        nargs="?",
        choices=["recite", "write", "chant"],
        help="recite a .euo file, write in the muse (a tiny IDLE), or chant (a live REPL)",
    )
    ap.add_argument("file", nargs="?", help="path to a .euo poem")
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
    if args.command == "recite" or args.file:
        path = args.file
        if not path:
            ap.error("recite needs a poem file")
        try:
            run_file(path)
        except FileNotFoundError:
            print(f"no poem lies at {path}")
            return 1
        except (LexError, ParseError, EunoiaError) as exc:
            print(f"the poem stumbles: {exc}")
            return 1
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())