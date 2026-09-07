# Eunoia (εὔνοια)

> *beautiful thinking* — a programming language whose code reads like poetry.

- **[한국어 (Korean)](README.ko.md)**
- **[English](README.md)**

**Eunoia** (from Greek *εὔνοια*, "beautiful thinking / well mind") is a
programming language designed so that opening a source file feels like opening
a book of verse. When you first look at Eunoia code, the hope is that your
first thought is:

> *"Wait... is this a poem?"*

This project is currently in the **design phase**. The grammar below is a
living proposal, open to discussion, not yet implemented. The interpreter is
planned to be written in **Python**.

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
let hello be wow
whisper hello
```

The Python equivalent:

```python
hello = "wow"
print(hello)
```

Now imagine a whole file:

```
let autumn be the sky's hue

let the rain whisper through the tired streets
let the streetlights bow their silver heads

whisper autumn
speak "I am the poem"
```

---

## Grammar Reference

> `*` = proposal on the table — nothing is final yet.

| Keyword        | Eunoia line                          | Means                              | Python                              |
|----------------|--------------------------------------|------------------------------------|-------------------------------------|
| `let`          | `let hello be wow`                   | assign a value to a name           | `hello = wow`                       |
| `whisper`      | `whisper hello`                      | print a value, softly              | `print(hello)`                      |
| `speak`        | `speak "I am the poem"`              | print a string, aloud              | `print("I am the poem")`            |
| `summon` `*`   | `summon requests`                    | install a package from afar        | `pip install requests`              |
| `embrace` `*`  | `embrace requests`                   | bring a package into use           | `import requests`                   |

### Open Questions

| Question                                             | Options                          | Lean              |
|------------------------------------------------------|----------------------------------|-------------------|
| Should `whisper` and `speak` be merged?              | separate / one keyword           | one keyword       |
| Install vs. import — which words?                    | `summon`+`embrace`, `summon`+`borrow`, ... | `summon` + `embrace` |
| Source extension?                                    | `.euo`, `.eunoia`, ...           | `.euo`            |

---

## The Package Problem (proposal)

Python uses `pip install` and `import`. Eunoia wants the *whole* experience to
be poetic — **the user never types `pip install`.** Instead, the poem itself
summons:

```
summon requests
embrace requests
write a letter to the server at dawn
```

The language quietly does the undignified work of `pip` underneath.

Candidates for the words:

| Keyword   | Feeling                                        |
|-----------|------------------------------------------------|
| `summon`  | call something in from outside (install)       |
| `embrace` | take it into your arms (import/use)            |
| `borrow`  | take it for a while, return it later (both?)   |
| `invoke`  | call upon a power (vague — left as an option)  |

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
- [ ] Grammar proposal finalized (open questions above)
- [ ] Lexer in Python
- [ ] Parser
- [ ] Interpreter
- [ ] Package summoning (pip bridge)
- [ ] CLI (`recite` / `bind` / `chant`)
- [ ] Example poems that actually run

---

## Contributing

This is a design-phase project. Ideas are as welcome as code — especially
poetic keywords, Korean-flavored metaphors, and naming debate. Open an issue
or a pull request.

---

## License

MIT