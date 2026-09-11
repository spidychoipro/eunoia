# Eunoia — the road to 1.0

A language is a promise. The promise here is strange:

> “I made some code.”
> “Where is the code? Isn't this a poem?”
> “This IS the code.”

1.0 is the day the promise holds: the grammar freezes, the spec is
published, and opening a source file still makes a reader hesitate —
*“Wait… is this a poem?”* — while the machine, underneath, runs. This is
not a normal language wearing poetic keywords. It is a real interpreter
whose surface is meant to be mistaken for verse.

The roadmap below is organized around that single challenge. Implementation
phases exist, but every phase is judged by one question: does this bring
executable code **closer to** poetry, without breaking the trust that the
poem runs?

---

## Already bound (v0.1.x) — identity, not phase steps

- Grammar: `let <name> be <value>`, `whisper`, `speak`, `summon`, `embrace`
- Number words (`two`, `a dozen`, `one hundred and five`) and arithmetic
  words (`and`/`with`, `without`, `times`, `over`/`shared among`, `keeps`)
- Reference vs text, word for word: **`wow` is a name, `"wow"` is literal
  text.** They are distinct tokens and must remain so
- `whisper the soul`, and the creed behind it
- `recite`, the interactive chant (`eunoia` alone, like `py`), and **Ink**,
  where thought becomes words — a tiny IDLE in tkinter, plus `ink.exe`
- `translate` — poems into plain Python, output matching the interpreter
  exactly; `bind`/`unbind` — `.euoc` anthologies, compiled but never locked
- 40 tests, issue templates, contributing guide, modifier code of conduct

Eunoia keeps these and grows. Nothing here is renounced to make the
language *different*; `whisper`, `speak`, `.euo`, `.euoc`, and the recite
metaphor are load-bearing.

---

## The north star: the poem-at-a-glance test

Before any new word lands, write the smallest real program that uses it —
an answer, a sum, a refrain. Show **only the source** to a non-programmer
and ask:

- “Is this a poem, or a program?”
- “What does it say?” *(not: “what does it compute?”)*

Then hand the same line to the parser and ask the machine half:

- Does every word have exactly one meaning here?
- Could a reader mistake a reference for literal text, or vice versa?
- Does the poem still translate to the same Python as before the change?

A feature passes only when both readers — the reader of poems and the
reader of tokens — give the same answer. Everything below is built around
this test.

---

## v0.2 — poetic language design (a dedicated phase)

The design work comes **before** any Turing-complete expansion. Today Eunoia
is honest but loud: much of it still reads as *Python translated into poetic
English*. This phase makes the surface earn the name — and it decides which
words v0.3 will be allowed to use.

### 1) The multi-word name investigation

Question: can a **phrase** hold a meaning? `let the morning be quiet` — an
open experiment, not a feature.

Today each line binds exactly one name. Phrase-names would let Eunoia
breathe like real verse, but they load the grammar with ambiguity, and the
lexer already has a crowd of residents:

- `a`, `an`, `two`, `a dozen`… are numbers before they are anything else.
- `and`, `with`, `without`, `times`, `over`, `keeps` are operators.
- `let`, `be`, `whisper`, `speak`, `summon`, `embrace` are keywords.

So `let a garden be quiet` begins with a number word, and
`let the morning and evening rest` passes through an operator. Both are
tempting poems; both are currently ambiguous — that is exactly the shape of
the problem to study. A phrase-name may not be allowed to swallow any of
those residents, and when it cannot, the failure must be a gentle stumble,
not a mystery.

Experiments, not commitments:

- **E1 — the side-by-side:** write five small programs twice — once in
  today's one-word syntax, once in each of three candidate phrase-name
  styles — and record which versions a non-programmer mistakes for verse.
- **E2 — the reserved-word census:** list what a phrase-name may not contain,
  and measure how many natural phrases still parse under each candidate
  style. Keep only styles where the reserved set stays small and the failure
  stays loud.
- **E3 — the smallest parser edit:** sketch the minimal lexer/parser change
  the winning style needs, plus a guard test proving a quoted string can
  never become a name and a name can never become text.

Accept into the language only what survives all three, and even then behind
the back-compat guardrails below. **No exact syntax is promised here** — the
phrase is invitation, not law.

### 2) The code-smell audit

Walk every construct and ask where the interpreter's shape still shows:

- `let x be y` is, to the eye, `x = y`.
- `whisper hello` is, to the eye, `print(hello)`.
- arithmetic words are operator symbols wearing jackets: `five times six`
  parses as tokens, not as a spoken thought.

None of these *must* change. Each deserves the audit question: does a reader
think “poetry that computes,” or “code that rhymes”? Fix the second kind.
Where a construct is already natural — the number runs, the line break
ending every verse — keep it and say so. Simplicity is beauty, and the
current grammar is the well that must not be poisoned.

### 3) The quiet parts

- **The line stays a verse.** One line, one verse — the README promises
  words, space, and a line break. Any future multi-line construct must read
  as a stanza, not as indentation wearing a hat.
- **Whispers stay quiet, spoken stays aloud.** `whisper` and `speak` are
  identity, never renamed for difference's sake.
- **The reference-vs-text guardrail.** Bare words are references; quoted
  words are text. Every construct that lands ships with a test asserting
  both sides.
- **Comments exist (`#`) and stay.** A poetic margin-annotation is an
  *investigation* for this phase — how a note might read as a sketch — not a
  replacement for what already works.

---

## v0.3 — the poem can think

Turing completeness, pursued as rhythm — and only after v0.2 has set the
words it will use. Until then these are candidate metaphors, deliberately
unfrozen:

- **Branching as the weather** — *when / unless* (candidate words, free for
  debate), phrased so truth reads as condition, not `if`.
- **Repetition as refrain** — `until`, `breathe`: a refrain returns to the
  same line and means “again,” the way a chorus does.
- **Comparisons in plain song** — `same as`, `smaller than`, `larger than`;
  logic words that do not collide with the arithmetic already claimed
  (`and`/`with` are taken).
- **A stanza as a verse** — a named group of lines, recited anywhere, with
  arguments passed as words: the function dress-rehearsed as verse.
- **Change without breaking the line** — `let x become …` (re-assignment
  inside the existing line rhythm).

Rule for the whole phase: every new word passes the poem-at-a-glance test,
ships a reference-vs-text guard test, and keeps `translate` output and the
interpreter agreeing word for word. Nothing here is promised by name — the
words are placeholders until v0.2 hands them down.

---

## v0.4 — the poem can touch the world

- **Input** — `listen` (the reader answers the poem)
- **“Quote the foreign poet”** — the escape hatch, set apart like quotation
  marks, deliberately narrow. Reading it should feel like scansion notes in
  the margin, not a door into another language.
- **File I/O** — to be worded by debate, as open as the page itself
- **SPEC.md** — the first full draft: grammar, semantics, and the error
  catalogue, written in prose that is itself poetry-adjacent.

---

## v0.5 — the poem can be published

- **CI** — GitHub Actions runs the suite on Python 3.9–3.14 on every push
- **Quality gates** — ruff and mypy, quiet and steady
- **Editor love** — the Neovim plugin, and verse-tinting inside Ink
- **Errors, all of them** — every stumble reads like a gentle line, not a
  slammed door (a 1.0 gate, listed early because it is)
- **Grammar freeze review** — a deliberate meeting with the creed; every
  word still receives exactly one reading, and the poem-at-a-glance test is
  run over the whole corpus before the freeze

---

## 1.0 — the book is bound

- Grammar frozen: no word changes without a major version
- **SPEC.md v1.0** published and linked from the README
- The non-programmer's first question — “is this a poem?” — is asked of your
  oldest example, not of a lab experiment
- Every mapped grammar rule covered by an explicit test, including the
  reference-vs-text guardrail on every construct
- CI green, releases automated (per-tag `ink.exe` plus language/app archives)
- Tag `v1.0.0` — and a poem in the release notes

---

## Deliberately not before 1.0

- **No symbols** — ever. The grammar stays words and space and a line.
- **No classes or OOP** — the poem is a sequence, not an object zoo.
- **No silent surprises** — errors stay gentle and named.
- **No lock-in** — anthologies stay decodable; a poem is always readable as
  itself.
- **stdlib only** — no runtime outside Python; `summon` is already how you
  extend, and there is nothing to hide.

---

## Back-compat guardrails, held at every step

- **Old poems still recite.** If a phrase-name or new construct must change
  an old line's meaning, it waits, or the old line wins.
- **`wow` ≠ `"wow"` always.** The guard test lives in the suite and travels
  with every feature.
- **`translate` never drifts.** Transpiled output and interpreter behavior
  stay identical for the same poem.