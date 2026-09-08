# Contributing to Eunoia

감사합니다 — 한 편의 시가 커뮤니티로부터 자라는 프로젝트입니다.
English follows anywhere you need it; 한국어도 자유롭게 써 주세요.

> **Side note:** because this file lives at the repository root, GitHub
> automatically links it in the **right sidebar** ("Contributing guidelines")
> whenever someone opens a new issue or pull request. Same goes for
> `CODE_OF_CONDUCT.md`. Just keep the files here and the sidebar grows itself.

---

## Ways to contribute

- **Propose a word** — a keyword, an operator, a number word, or a whole new verse form.
- **Report a stumble** — a poem that fell over, with the smallest `.euo` that shows it.
- **Write examples** — poems in `poems/` that run and feel like poetry.
- **Name things** — naming debates are the soul of this project.
- **Code** — lexer, parser, interpreter, CLI, and later the Neovim plugin.

---

## Quick start (dev)

```bash
git clone https://github.com/spidychoipro/eunoia.git
cd eunoia
python -m venv .venv
.venv\Scripts\activate        # macOS/Linux: source .venv/bin/activate
pip install -e .
python -m unittest discover -s tests
eunoia recite poems/hello.euo
```

Use the **latest Python** you can (3.12 or newer). That's where Eunoia is
actually tested — the code still runs on 3.9+, but why whisper in an old
tongue?

---

## Where things live

```
src/eunoia/lexicon.py        the closed word-list: numbers, keywords, operators
src/eunoia/lexer.py          turns verse into tokens
src/eunoia/parser.py         turns tokens into statements
src/eunoia/interpreter.py    makes the poem run
src/eunoia/soul.py           the inner creed (whisper the soul)
src/eunoia/cli.py            recite & chant
tests/test_eunoia.py         unit tests
poems/                       example poems
```

---

## How to add a word

1. Add the word to the right table in `src/eunoia/lexicon.py`
   (`UNITS`, `TEENS`, `TENS`, `SCALES`, `KEYWORDS`, or `OPERATORS`).
2. If it's a new statement, teach the parser (`parser.py`) and the interpreter
   (`interpreter.py`) about it.
3. Add a test in `tests/test_eunoia.py` and add an example poem.
4. Update the grammar table in `README.md` and `README.ko.md`.
5. Run the tests and recite an example poem.

---

## The house rules

- **No parentheses, no symbols.** Eunoia's own grammar is words and space and
  one line per verse. A change that smuggles in a `(` is a change that lost.
- **One word, one job.** Simpler is more poetic.
- **It must actually run.** A venerable idea with no interpreter is just a
  dream dressed up; show the `.euo` that works.
- **Errors stay gentle.** A stumble, not a slammed door.
- **Commits read like sentences.** Meaningful, human, done.
- When in doubt, `whisper the soul`.

---

## Communication

- **Bugs** → [open a bug report](https://github.com/spidychoipro/eunoia/issues/new/choose)
- **Ideas / words** → [propose a new word](https://github.com/spidychoipro/eunoia/issues/new/choose)
- **Open talk** → [repo discussions](https://github.com/spidychoipro/eunoia/discussions)
- **Code of conduct** → [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

This is a small, kind project. Whisper, don't shout.