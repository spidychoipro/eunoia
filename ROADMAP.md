# Eunoia — the road to 1.0

A language is a promise. 1.0 is the day the promise is stuck in its frame:
the grammar freezes, the spec is published, and every verse still runs.

---

## Already bound (v0.1.x)

- Grammar: `let <name> be <value>`, `whisper`, `speak`, `summon`, `embrace`
- Number words (`two`, `a dozen`, `one hundred and five`) and arithmetic
  words (`and`/`with`, `without`, `times`, `over`/`shared among`, `keeps`)
- `whisper the soul` and the creed behind it
- `recite`, the interactive chant (`eunoia` alone, like `py`), the muse
  (a tiny IDLE in tkinter) and the single-file `eunoia.exe`
- `translate` — poems into plain Python, whose output matches the
  interpreter word for word
- `bind` / `unbind` — `.euoc` anthologies, compiled but never locked
- 40 tests, GitHub release mechanics, contributing guide and code of conduct

---

## v0.2 — the poem can think (Turing complete)

Today Eunoia can only walk forward: line after line. To be a real language
it must be able to look left and right, and to go round.

- **Branching** — `whenever <verse>` with `otherwise` (candidate words,
  free for debate)
- **Loops** — `until <verse>` (repeat while true) and `breathe` (repeat
  for a count)
- **Comparisons** — `same as`, `smaller than`, `larger than`; logic with
  words that do not collide with arithmetic (`also`, `neither`)
- **Verse definitions** — a reusable stanza: give it a name, give it
  arguments, recite it anywhere
- **Re-assignment** — `let x become ...` (change, without breaking the line)
- Tests for every feature; the translate output must still match the
  interpreter exactly (the `_say` promise holds)

## v0.3 — the poem can touch the world

- **Input** — `listen` (the reader answers)
- **Margin notes** — comments that a poet can write, that read like sketches
- **"Quote the foreign poet"** — the escape hatch to call plain Python with
  respect, their words set apart
- **File I/O** — to be worded by debate, as open as the page itself
- **SPEC.md** — the first full draft: grammar, semantics, error catalogue.
  This document is the spine of 1.0.

## v0.4 — the poem can be published

- **CI** — GitHub Actions runs the whole suite on Python 3.9–3.14 every push
- **Quality gates** — ruff and mypy, quiet and steady
- **Editor love** — the Neovim plugin, and syntax tinting inside the muse
- **Errors, all of them** — every stumble reads like a gentle line, not a
  slammed door
- **Grammar freeze review** — a deliberate meeting with the creed before the
  freeze

## 1.0 — the book is bound

- Grammar frozen: no word changes without a major version
- **SPEC.md v1.0** published and linked from the README
- CI green, releases automated (per-tag build of `eunoia.exe` plus the
  language/app source archives)
- Every mapped grammar rule covered by an explicit test
- Tag `v1.0.0` — and a poem in the release notes

---

## Deliberately not before 1.0

- **No symbols** — ever. The grammar stays words and space and a line.
- **No classes or OOP** — the poem is a sequence, not an object zoo.
- **No silent surprises** — errors stay gentle and named.
- **stdlib only** — no runtime outside Python; `summon` is already how you
  extend, and there is nothing to hide.