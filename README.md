# Eunoia (εὔνοια)

> *beautiful thinking* — a programming language whose code reads like poetry.

- **[한국어 (Korean)](README.ko.md)**
- **[English](README.md)**

**Eunoia** (from Greek *εὔνοια*, "beautiful thinking / well mind") is a
programming language designed so that opening a source file feels like opening
a book of verse. When you first look at Eunoia code, the hope is that your
first thought is:

> *"Wait... is this a poem?"*

This project is in the **design phase**, with a working prototype that already
implements the confirmed grammar below. The rest of the language is still open
to discussion. The interpreter is written in **Python**.

---

## Why "Eunoia"?

- It is the **shortest English word containing all five vowels** — *a e i o u*.
- It means **beautiful thinking**, *a harmonious mind*.
- It sets the tone: this is a language about **feeling** as much as **function**.

---

## The Original Idea

Every language hides a bridge between what you write and what the machine does.
Eunoia leans into that bridge — not to be obscure, but to be **beautiful**.

Python calls a source file `.py` and a compiled file `.pyc`. Eunoia turns that
into a metaphor:

| Artifact | Python | Eunoia | Meaning |
|----------|--------|--------|---------|
| Source file    | `.py`  | `.euo` | a **poem** *(시)* |
| Compiled file  | `.pyc` | `.euoc` | a **poetry collection** *(시집)* |

So — you don't "run" or "compile." You **recite** the poem, and when poems are
**bound** together, a **poetry collection** is born.

---

## Design Principles

1. **The surface is poetry.** The user only ever sees verse. The machine's dull
   work (installing, importing, translating) happens invisibly below the poem.
2. **Simplicity is beauty.** A keyword that does one thing well is more poetic
   than one that does five.
3. **Reads left to right, like a line of verse.**
4. **Under the hood, it is real.** Eunoia compiles to something the machine
   understands — it is not a toy, it is a poem that runs.
5. **Korean soul, universal body.** The ideas are felt in Korean; the machine
   works everywhere.

---

## A First Taste

```
let wow be "wow"
let hello be wow
whisper hello
```

The Python equivalent:

```python
wow = "wow"
hello = wow
print(hello)
```

Now imagine a whole file:

```
let autumn be "the sky's hue"

let garden be five times six
let share be a dozen over four

whisper autumn
whisper garden
speak "I am the poem"
```

### Try it

```bash
pip install -e .
eunoia recite poems/hello.euo
eunoia chant        # a live REPL
```

---

## Grammar Reference

### Core (confirmed)

| Keyword        | Eunoia line                          | Means                              | Python                              |
|----------------|--------------------------------------|------------------------------------|-------------------------------------|
| `let`          | `let hello be wow`                   | assign a value to a name           | `hello = wow`                       |
| `whisper`      | `whisper hello`                      | print a value, softly              | `print(hello)`                      |
| `speak`        | `speak "I am the poem"`              | print a string, aloud              | `print("I am the poem")`            |
| `summon`       | `summon requests`                    | install a package from afar        | `pip install requests`              |
| `embrace`      | `embrace requests`                   | bring a package into use           | `import requests`                   |

### Arithmetic (confirmed)

| Operator | Poetic word         | Example                                | Means          |
|----------|---------------------|----------------------------------------|----------------|
| `+`      | `and`, `with`       | `let sum be two and three`             | `sum = 2 + 3`  |
| `-`      | `without`           | `let rest be ten without four`         | `rest = 10-4`  |
| `×`      | `times`             | `let garden be five times six`         | `garden =5*6`  |
| `÷`      | `over`, `shared among` | `let share be a dozen over four`     | `share = 12/4` |
| `%`      | `keeps`             | `let what be twelve keeps five`        | `12 % 5`       |

Numbers are written as words: `one`, `two`, `three`, ..., `a dozen`.
It's a closed word-list, so the parser knows them without ambiguity.

### Open Questions

| Question                                             | Options                          | Lean              |
|------------------------------------------------------|----------------------------------|-------------------|
| Should `whisper` and `speak` be merged?              | separate / one keyword           | one keyword       |
| Source extension?                                    | `.euo`, `.eunoia`, ...           | `.euo`            |

---

## The Package Problem (confirmed)

Python uses `pip install` and `import`. Eunoia wants the *whole* experience to
be poetic — **the user never types `pip install`.** Instead, the poem itself
summons:

```
summon requests
embrace requests
write a letter to the server at dawn
```

The language quietly does the undignified work of `pip` underneath.
`borrow` and `invoke` were considered but set aside — `summon` + `embrace` won.

---

## Eunoia vs. Shakespeare

|                       | Shakespeare                      | Eunoia                        |
|-----------------------|----------------------------------|-------------------------------|
| Inspired by           | theatre / drama                  | lyric poetry                  |
| Structure             | acts, scenes, characters, `goto` | verses, lines, gentle flow    |
| Mood                  | grand, theatrical                | quiet, intimate               |
| Feels like            | a play being acted               | a poem being whispered        |

---

## The CLI, as visioned

| Command                    | Meaning                                       |
|----------------------------|-----------------------------------------------|
| `eunoia recite poem.euo`   | run a poem                                    |
| `eunoia bind poem.euo`     | compile a poem into a poetry collection       |
| `eunoia chant`             | interactive REPL — a live recitation          |

---

## The Poem Book

`.euo` files are **poems**. A poem can:

- declare verses (`let ... be ...`)
- whisper and speak
- summon and embrace packages
- (future) breathe, pause, return — control flow as rhythm

---

## Roadmap

- [x] Repository created
- [x] Name decided: **Eunoia**
- [x] Core grammar confirmed (see Grammar Reference)
- [x] Lexer, parser, interpreter (recite works)
- [x] `chant` REPL
- [ ] Remaining design questions (whisper/speak, extension)
- [ ] `bind` (compiling a poem into an anthology)
- [ ] Package summoning demo (pip bridge works, not yet polished)
- [ ] More example poems, escape hatch for foreign libraries
- [ ] Neovim plugin

---

## Contributing

This is a design-phase project. Ideas are as welcome as code — especially
poetic keywords, Korean-flavored metaphors, and naming debate. Open an issue
or a pull request.

---

## License

MIT