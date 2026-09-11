<p align="center">
  <img src="assets/icons/eunoia.svg" alt="Eunoia" width="180">
</p>

<h1 align="center">Eunoia (에우노이아, εὔνοια)</h1>

<p align="center"><em>아름다운 사고</em> — 코드가 시로 읽히는 프로그래밍 언어.</p>

<p align="center">
  <a href="README.md">English</a> · <a href="README.ko.md">한국어</a>
</p>

<p align="center">
  <img alt="MIT" src="https://img.shields.io/badge/license-MIT-2B2D42?style=flat-square">
  <img alt="Python" src="https://img.shields.io/badge/python-3.9%2B-2B2D42?style=flat-square">
  <img alt="version" src="https://img.shields.io/badge/version-0.1.0-E8A33D?style=flat-square">
  <img alt="punctuation" src="https://img.shields.io/badge/punctuation-no%20parentheses-E8A33D?style=flat-square">
  <img alt="words" src="https://img.shields.io/badge/words-yes-F7F3E8?style=flat-square">
</p>

---

## Eunoia란 무엇인가?

**Eunoia**는 그리스어 *εὔνοια*("아름다운 생각, 조화로운 마음")에서 온 프로그래밍
언어로, 소스 파일을 여는 순간 마치 시집을 펼치는 듯한 느낌을 주는 것을 목표로 합니다.
Eunoia로 작성된 코드를 처음 보는 순간 떠오르는 생각은 바로 이것이기를 바랍니다:

> *"잠깐... 이거 시 아니야?"*

Eunoia는 시를 *흉내 내는* 장난감이 아닙니다. 의존성 없는 순수 파이썬으로 만든
**진짜 인터프리터**이며, 시를 실행되는 코드로 바꿔줍니다. 이 README의 모든 예시는
실제로 실행됩니다.

---

## 30초 만에 실행하기

```bash
git clone https://github.com/spidychoipro/eunoia.git
cd eunoia
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS / Linux
# source .venv/bin/activate

pip install -e .
eunoia recite poems/hello.euo
```

```text
$ eunoia recite poems/hello.euo
wow
```

끝입니다. 의존성도, 빌드 과정도 없어요 — 파이썬과 당신의 시만 있으면 됩니다.

> **파이썬 버전:** Eunoia는 **3.9 이상**에서 실행되며, 가능한 한 **최신 버전**(3.12+
> 권장)을 쓰시길 권합니다 — 프로젝트는 그것으로 개발되고 테스트됩니다.

---

## 오리지널 생각: 시 한 편, 그리고 시집

모든 언어는 "내가 쓰는 것"과 "기계가 하는 일" 사이에 다리를 숨깁니다.
Eunoia는 그 다리를 어둡게 만들지 않고, **아름답게** 만듭니다.

파이썬은 소스 파일을 `.py`, 컴파일된 파일을 `.pyc`라고 부릅니다.
Eunoia는 그것을 하나의 비유로 만듭니다:

| 산출물 | Python | Eunoia | 의미 |
|--------|--------|--------|------|
| 소스 파일   | `.py`  | `.euo`  | **시 한 편** |
| 컴파일 결과 | `.pyc` | `.euoc` | **시집 한 권** |

그래서 파일을 *실행*하지 않고, **낭송(recite)**합니다. 시들이 모여
`bind`로 엮이면(로드맵에 있습니다) **시집**이 탄생합니다.

---

## 첫 번째 시

`poems/hello.euo`:

```
let wow be "wow"
let hello be wow
whisper hello
```

모든 줄이 파이썬에 그대로 대응됩니다:

```python
wow = "wow"
hello = wow
print(hello)
```

좀 더 많은 예시:

```
let autumn be "the sky's hue"

let garden be five times six
let share be a dozen over four

whisper autumn
whisper garden
whisper share
speak "I am the poem"
```

```text
$ eunoia recite poems/autumn.euo
the sky's hue
30
3
I am the poem
```

---

## 문법 총정리

Eunoia 고유 문법에는 **괄호도, 기호도 없습니다.** 오직 단어와 공백, 그리고 모든
연(verse) 끝의 줄바꿈뿐입니다.

### 핵심 문법

| 키워드    | Eunoia 줄                  | 의미                            | Python                       |
|-----------|----------------------------|---------------------------------|------------------------------|
| `let`     | `let hello be wow`         | 이름에 뜻을 부여                | `hello = wow`                |
| `whisper` | `whisper hello`            | 값을 조용히 출력                | `print(hello)`               |
| `speak`   | `speak "I am the poem"`    | 문자열을 또렷이 출력            | `print("I am the poem")`     |
| `summon`  | `summon requests`          | 먼 곳에서 패키지를 불러 설치    | `pip install requests`       |
| `embrace` | `embrace requests`         | 패키지를 품에 안아 사용         | `import requests`            |

### 사칙연산 — 타자기 대신 우리말

| 연산 | 시적 단어            | 예시                                | 의미          |
|------|----------------------|-------------------------------------|---------------|
| `+`  | `and`, `with`        | `let sum be two and three`          | `sum = 2 + 3` |
| `-`  | `without`            | `let rest be ten without four`      | `rest = 10-4` |
| `×`  | `times`              | `let garden be five times six`      | `garden = 5*6` |
| `÷`  | `over`, `shared among` | `let share be a dozen over four`    | `share = 12/4` |
| `%`  | `keeps`              | `let what be twelve keeps five`     | `12 % 5`      |

### 숫자는 말로 씁니다

`one`…`twelve`, `thirteen`…`nineteen`, 십 단위 `twenty`…`ninety`.
그리고 `a`, `an`, `dozen`, `score`, `hundred`, `thousand`, `million`, `billion`.

```
one hundred and five     → 100 + 5 = 105
two dozen over four      → (2 × 12) / 4 = 6
a score and one          → 20 + 1 = 21
```

곱셈과 나눗셈이 덧셈·뺄셈보다 먼저 묶입니다. 익숙한 그 규칙 그대로요.

### 주석

`#`로 시작하는 줄은 조용합니다 — 기계가 아닌 독자에게만 말합니다.

```
let hello be "wow"  # 아무도 실행하지 않는 메모
whisper hello
```

---

## 영혼을 속삭이다

파이썬의 `import this`처럼, 딱 한 줄이 언어의 신조를 불러냅니다:

```
whisper the soul
```

```text
$ echo "whisper the soul" > the-soul.euo     # 아무 .euo 파일이나
$ eunoia recite the-soul.euo
The Soul of Eunoia

Let each poem be honest,
and each line worth reading twice.

Let the surface be the whole sky;
let the gears turn far below.

Let a name be chosen with care,
for it will be spoken softly many times.

Let simplicity win over cleverness,
let beauty win over noise.

Let the machine kneel quietly,
that the reader may stay in wonder.

Let foreign poets be quoted with respect,
their words set apart by marks.

Let a whisper comfort more than a shout.

Let the poem that runs
still be a poem.

Let errors be a gentle stumble,
not a slammed door.

Let the soul speak in one tongue
while the body serves the whole world.

Let the last line matter.
```

---

## 설계 원칙

1. **표면은 전부 시다.** 사용자가 보는 것은 오직 시뿐입니다. 기계의 지루한
   일(설치, import, 번역)은 시 아래에서 조용히 일어납니다.
2. **단순함이 곧 아름다움.** 한 가지를 잘하는 키워드가 다섯 가지를 하는
   키워드보다 더 시적입니다.
3. **시의 한 줄처럼, 왼쪽에서 오른쪽으로 읽힌다.**
4. **속은 진짜다.** Eunoia는 기계가 이해하는 무언가로 컴파일됩니다.
   장난감이 아니라, **실행되는 시**입니다.
5. **한국어의 영혼, 보편의 몸.** 느낌은 한국어로 전달하되, 기계는 어디서나
   작동하도록 만듭니다.

---

## 패키지는 보이지 않게

당신은 절대 `pip install`을 입력하지 않습니다. 시가 직접 불러옵니다:

```
summon requests
embrace requests
```

`summon`은 부끄러운 `pip`의 일을 시 아래에서 조용히 처리하고, `embrace`는 모듈을
품에 안아 시의 세계로 데려옵니다. 깊이 파이썬적인 API를 가진 라이브러리에게는,
그 정확한 문법을 "남의 시 인용"처럼 따로 떼어 쓰는 비상구를 계획 중입니다
(로드맵에 있습니다).

---

## Eunoia vs. 셰익스피어 언어

|                | 셰익스피어                      | Eunoia                     |
|----------------|---------------------------------|----------------------------|
| 영감            | 연극 / 드라마                    | 서정시                     |
| 구조            | 막·장·등장인물·`goto`           | 연(verse)·줄, 부드러운 흐름 |
| 분위기          | 웅장하고 연극적인                | 조용하고 내밀한             |
| 느낌            | 연극을 연기하는 듯한             | 시를 속삭이는 듯한          |

---

## 프로젝트 구조

```
src/eunoia/        인터프리터
  lexer.py         시를 토큰으로 (단어·숫자·연산자)
  parser.py        토큰을 문장으로
  interpreter.py   시를 실행시키는 영혼
  soul.py          속삭이면 들려주는 신조
  transpile.py     시를 평범한 Python으로 옮기는 도구
  anthology.py     .euoc 시집을 묶고(bind) 푸는(unbind) 도구
  cli.py           recite, translate, bind, unbind, write & chant
  ui.py            Ink — 생각이 글이 되는 곳 (작은 IDLE, tkinter)
poems/             실제로 실행되는 예제 시 (.euo)
tests/             단위 테스트 (python -m unittest)
assets/prompts/    로고와 파일 아이콘 이미지 프롬프트
assets/icons/      로고와 .euo 파일 아이콘 (SVG로 직접 그림)
```

---

## CLI

| 명령                                         | 의미                                        |
|----------------------------------------------|---------------------------------------------|
| `eunoia`                                     | 대화형 낭독을 연다 (`py`처럼)               |
| `eunoia recite <file.euo>`                   | 시를 낭송한다 (= 실행)                      |
| `eunoia recite <file.euoc>`                  | 시집을 펼쳐 낭송한다                        |
| `eunoia translate <file.euo> [-o out.py]`    | 시를 평범한 Python으로 옮긴다               |
| `eunoia bind a.euo b.euo -o c.euoc`          | 시들을 한 시집으로 묶는다                    |
| `eunoia unbind c.euoc`                       | 시집을 열고 원문을 다시 읽는다               |
| `eunoia write`                               | Ink를 연다 (작은 IDLE, tkinter)          |
| `eunoia chant`                               | 대화형 낭독회 — 다른 이름일 뿐               |

시집(`.euoc`)은 컴파일되었지만 절대 잠기지 않습니다 — 모든 시를 원문 그대로
열어서 보관하기에, `unbind`는 언제든 시를 돌려줍니다.

---

## Ink — 시인처럼 써 보기

시인은 원고지에 시를 쓰고, 그 시를 눈에 보이게 만드는 것은 결국 잉크입니다.
그래서 그 작문 앱의 이름을 **Ink**로 지었습니다 — 생각이 글이 되는 바로 그
곳. `eunoia write`가 그것을 엽니다 (또는 `ink.exe` 실행). 왼쪽에서
시를 쓰고, 오른쪽에서 그 울림(echo)을 봅니다. 인터프리터를 그대로
재현하므로 종이가 거짓말하지 않아요 — 도움말 메뉴, `whisper the soul`,
`.euo` 열기/저장, 줄 번호, Ctrl+Enter 낭송까지 갖췄습니다.

**단일 실행 파일.** PyInstaller로 Windows 단일 exe를 만듭니다:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --clean --name ink --paths src app.py
# → dist/ink.exe
```

`app.py`는 Ink를 여는 아주 작은 진입점입니다. `dist/ink.exe`를 어디에든
갖다 놓고, 두 번 클릭하고, 쓰면 됩니다. 잉크는 거짓말하지 않아요.

---

## 로드맵

1.0까지의 전체 길은 [ROADMAP.md](ROADMAP.md)에 있습니다.

- [x] 저장소 생성
- [x] 이름 결정: **Eunoia**
- [x] 핵심 문법 확정 및 구현
- [x] `recite`와 `chant`
- [x] `whisper the soul`
- [x] Ink — 작문 앱 IDLE + 단일 파일 `ink.exe`
- [x] `translate` — 시를 평범한 Python으로
- [x] `bind` & `unbind` — `.euoc` 시집, 언제나 해독 가능
- [ ] "남의 시 인용" 비상구
- [ ] 흐름을 리듬으로 (breathe / until / whenever)
- [ ] 네오빔 플러그인
- [x] 실제 로고·파일 아이콘 (손으로 그린 SVG)

---

## 기여

설계 단계 프로젝트입니다. 코드보다 **아이디어**가 더 환영받습니다 — 시적인 단어,
한국어 감성의 비유, 이름 논쟁 모두요.

- **시가 넘어졌다?** → [버그 리포트 열기](https://github.com/spidychoipro/eunoia/issues/new/choose)
- **새 단어를 제안하고 싶다?** → [단어 요청 열기](https://github.com/spidychoipro/eunoia/issues/new/choose)
- **어떻게 돌아가는지** → [CONTRIBUTING.md](CONTRIBUTING.md)
- **친절함이 먼저** → [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

두 가이드는 저장소 루트에 있어서, 이슈/PR을 새로 열 때 GitHub가 **오른쪽
사이드바**(Contributing guidelines)에 자동으로 띄워줍니다. 무엇보다 먼저:
`whisper the soul`.

---

## 라이선스

MIT