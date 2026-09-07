# Eunoia (에우노이아)

> *아름다운 사고* — a programming language whose code reads like poetry.

**Eunoia** (from Greek *εὔνοια*, "beautiful thinking / well mind") is a programming
language inspired by the idea that source code can feel like a poem.
When you first open a file written in Eunoia, the hope is that your first thought is:

> *"Is this... a poem?"*

Eunoia aims for **beauty through simplicity** — code that reads naturally, like a
line of verse, while still being real, runnable software.

> **Note:** Eunoia is currently in the **design phase**. Syntax below is a
> proposal for discussion, not yet implemented.

---

## Why "Eunoia"?

- **Eunoia** is the shortest English word containing all five vowels.
- It means *beautiful thinking* / *harmonious mind*.
- It sets the tone: this is a language about feeling, not just function.

---

## The Idea

Unlike Shakespeare (which is dramatic and theatrical — characters, scenes, acts),
Eunoia leans into the **lyric poem**: quiet, simple, immediate.

Compare:

```
# Shakespeare (drama)
Romeo: "Let us proceed upon the road"

# Eunoia (lyric)
let hello be wow
whisper hello
```

---

## Proposed Syntax (design draft)

### Variables & Assignment

```
let hello be wow          # -> hello = wow
let autumn be the sky's hue  # -> autumn = "the sky's hue"
```

### Output

```
whisper hello             # print a value, softly
speak "I am the poem"     # print a string, aloud
```

> **Open question:** should `whisper` and `speak` be merged into a single
> output keyword? (leaning: yes — simpler is more poetic)

---

### Packages & Imports (proposal — not decided)

Python uses `pip install` and `import`. Eunoia wants to make that poetic too.
Several candidates are under consideration — **nothing is chosen yet**:

| Keyword | Meaning | Example |
|---------|---------|---------|
| `summon` | bring something in from outside | `summon from pip import requests` |
| `invoke` | call upon a power | `invoke the pip -i requests` |
| `borrow` | borrow temporarily | `borrow from the pip the requests` |

Two concepts are currently mixed and need separating:
- **installing** a package (`pip install`)
- **importing/using** a package (`import`)

Possible split: **install** → `summon`, **import/use** → `embrace` (끌어안는다).
Your thoughts welcome.

---

## Status

- [x] Repository created (`spidychoipro/eunoia`)
- [ ] Language name decided: **Eunoia**
- [ ] Syntax design in progress
- [ ] Interpreter implementation (Python)

---

## License

MIT
