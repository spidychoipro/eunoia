"""The muse — a tiny IDLE for composing and reciting Eunoia poems.

Run it from the console with `eunoia write`, or launch the single
executable. Built on tkinter, the same toolkit that powers IDLE itself.
"""

from __future__ import annotations

import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from . import __version__
from .interpreter import EunoiaError, Interpreter
from .lexer import LexError, lex
from .parser import ParseError, Parser
from .soul import SOUL

FONT = ("Consolas", 12)
FONT_SMALL = ("Consolas", 10)

PALETTE = {
    "ink": "#2B2D42",
    "ink_soft": "#3A3E5A",
    "cream": "#FAF6EC",
    "cream_line": "#E7DFC9",
    "amber": "#E8A33D",
    "amber_deep": "#C07F1F",
    "mute": "#8A8FA3",
    "paper": "#FFFFFF",
}

DEFAULT_POEM = (
    'let hello be "wow"\n'
    "whisper hello\n"
    'speak "I am the poem"\n'
)


class EunoiaEditor(tk.Tk):
    """One window: a verse on the left, its echo on the right."""

    def __init__(self) -> None:
        super().__init__()
        self.title(f"Eunoia {__version__} — write, and recite")
        self.geometry("980x660")
        self.minsize(700, 460)
        self.configure(bg=PALETTE["paper"])

        self._last_lines = 0
        self._current_path: Path | None = None

        self._menu()
        self._toolbar()
        self._panes()
        self._statusbar()
        self.bind("<Control-Return>", lambda _e: self._recite())
        self.bind("<Control-s>", lambda _e: self._save())
        self.bind("<Control-o>", lambda _e: self._open())
        self.bind("<Control-n>", lambda _e: self._new())
        for w in (self._editor, self._gutter):
            w.bind("<MouseWheel>", self._on_wheel)
            w.bind("<KeyRelease>", self._sync_gutter)
            w.bind("<ButtonRelease-1>", self._sync_gutter)
        self._editor.bind("<<Modified>>", self._on_modified)

        self._last_lines = 0
        self._set_poem(DEFAULT_POEM)
        self._echo("Eunoia is waiting for a verse. Ctrl+Enter to recite.\n")

    # -- chrome ---------------------------------------------------------

    def _menu(self) -> None:
        bar = tk.Menu(self)
        m_file = tk.Menu(bar, tearoff=0)
        m_file.add_command(label="New verse   Ctrl+N", command=self._new)
        m_file.add_command(label="Open poem... Ctrl+O", command=self._open)
        m_file.add_command(label="Save        Ctrl+S", command=self._save)
        m_file.add_command(label="Save as...", command=self._save_as)
        m_file.add_separator()
        m_file.add_command(label="Quit", command=self.destroy)
        bar.add_cascade(label="File", menu=m_file)

        m_run = tk.Menu(bar, tearoff=0)
        m_run.add_command(label="Recite      Ctrl+Enter", command=self._recite)
        m_run.add_command(label="whisper the soul", command=self._whisper_soul)
        m_run.add_command(label="Clear the echo", command=self._clear_echo)
        bar.add_cascade(label="Run", menu=m_run)

        m_help = tk.Menu(bar, tearoff=0)
        m_help.add_command(label="Grammar, in one breath", command=self._grammar)
        m_help.add_command(label="The soul of this project", command=self._whisper_soul)
        m_help.add_command(label="About Eunoia", command=self._about)
        bar.add_cascade(label="Help", menu=m_help)
        self.config(menu=bar)

    def _toolbar(self) -> None:
        tb = tk.Frame(self, bg=PALETTE["paper"])
        tb.pack(side="top", fill="x", padx=10, pady=(10, 4))
        for label, cmd in (
            ("New", self._new),
            ("Open", self._open),
            ("Save", self._save),
            ("Recite", self._recite),
        ):
            btn = tk.Button(
                tb,
                text=label,
                command=cmd,
                font=FONT_SMALL,
                bg=PALETTE["amber"],
                fg=PALETTE["ink"],
                activebackground=PALETTE["amber_deep"],
                activeforeground=PALETTE["cream"],
                relief="flat",
                padx=14,
                pady=3,
                cursor="hand2",
            )
            btn.pack(side="left", padx=(0, 6))
        tk.Label(
            tb,
            text="  Eunoia · with",  # kept for future habits
            font=FONT_SMALL,
            bg=PALETTE["paper"],
            fg=PALETTE["mute"],
        ).pack(side="right")

    def _panes(self) -> None:
        outer = tk.PanedWindow(self, orient="horizontal", sashwidth=6,
                               bg=PALETTE["paper"], sashrelief="flat")
        outer.pack(fill="both", expand=True, padx=10, pady=4)

        left = tk.Frame(outer, bg=PALETTE["cream"])
        right = tk.Frame(outer, bg=PALETTE["ink"])

        self._make_editor(left)
        self._make_echo(right)
        outer.add(left, minsize=380, width=560)
        outer.add(right, minsize=260, width=400)

    def _make_editor(self, parent: tk.Frame) -> None:
        head = tk.Label(
            parent,
            text="the verse",
            font=FONT_SMALL,
            bg=PALETTE["cream"],
            fg=PALETTE["mute"],
            anchor="w",
        )
        head.pack(fill="x")

        wrap = tk.Frame(parent, bg=PALETTE["cream"])
        wrap.pack(fill="both", expand=True)

        self._gutter = tk.Text(
            wrap, width=4,
            bg=PALETTE["ink_soft"], fg=PALETTE["amber"],
            font=FONT, padx=4, pady=6,
            relief="flat", highlightthickness=0,
        )
        self._gutter.pack(side="left", fill="y")

        self._editor = tk.Text(
            wrap,
            font=FONT, wrap="none",
            bg=PALETTE["cream"], fg=PALETTE["ink"],
            insertbackground=PALETTE["ink"],
            selectbackground=PALETTE["amber"],
            relief="flat", highlightthickness=0,
            padx=10, pady=6, undo=True,
        )
        scroll = ttk.Scrollbar(wrap, orient="vertical", command=self._on_scroll)
        self._editor.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        self._editor.config(yscrollcommand=self._scroll_echo_editor)
        self._gutter.config(yscrollcommand=self._scroll_echo_gutter)
        self._scroll = scroll

    def _make_echo(self, parent: tk.Frame) -> None:
        head = tk.Label(
            parent,
            text="the echo",
            font=FONT_SMALL,
            bg=PALETTE["ink"],
            fg=PALETTE["amber"],
            anchor="w",
        )
        head.pack(fill="x")
        self._echo_text = tk.Text(
            parent,
            font=FONT,
            bg=PALETTE["ink"], fg=PALETTE["cream"],
            insertbackground=PALETTE["amber"],
            relief="flat",
            state="disabled", wrap="word",
            padx=10, pady=6,
        )
        self._echo_text.pack(fill="both", expand=True)
        self._echo_text.tag_configure("prompt", foreground=PALETTE["amber"])
        self._echo_text.tag_configure("soul", foreground=PALETTE["amber"],
                                      font=("Georgia", 13, "italic"))

    def _statusbar(self) -> None:
        line = tk.StringVar()
        self._status_line = line
        bar = tk.Frame(self, bg=PALETTE["paper"])
        bar.pack(side="bottom", fill="x", padx=10, pady=(2, 6))
        tk.Label(
            bar, textvariable=line,
            font=FONT_SMALL, bg=PALETTE["paper"], fg=PALETTE["mute"],
            anchor="w",
        ).pack(side="left")
        tk.Label(
            bar,
            text=f"eunoia {__version__} · python {sys.version_info.major}.{sys.version_info.minor}",
            font=FONT_SMALL, bg=PALETTE["paper"], fg=PALETTE["mute"],
        ).pack(side="right")
        self._update_status()

    # -- actions -----------------------------------------------------------

    def _set_poem(self, text: str, path: Path | None = None) -> None:
        self._editor.delete("1.0", "end")
        self._editor.insert("1.0", text)
        self._editor.edit_reset()
        self._current_path = path
        self._sync_gutter()
        self._update_status()

    def _new(self) -> None:
        if messagebox.askyesno(
            "New verse",
            "Begin a blank page? The current verse will be lost.",
            parent=self,
        ):
            self._set_poem("", None)

    def _open(self) -> None:
        path = filedialog.askopenfilename(
            parent=self,
            title="Open a poem",
            filetypes=[("Eunoia poems", "*.euo"), ("All files", "*.*")],
        )
        if not path:
            return
        try:
            source = Path(path).read_text(encoding="utf-8")
        except OSError:
            messagebox.showerror("Open", f"the page will not turn: {path}", parent=self)
            return
        self._set_poem(source, Path(path))
        self._echo(f"(opened {Path(path).name} — a verse lost, a verse found.)\n")

    def _save(self) -> None:
        if self._current_path is None:
            self._save_as()
            return
        try:
            self._current_path.write_text(
                self._editor.get("1.0", "end-1c") + "\n", encoding="utf-8"
            )
            self._echo(f"(saved {self._current_path.name})\n")
        except OSError:
            messagebox.showerror("Save", f"the ink would not dry: {self._current_path}", parent=self)

    def _save_as(self) -> None:
        path = filedialog.asksaveasfilename(
            parent=self,
            title="Save the poem",
            defaultextension=".euo",
            filetypes=[("Eunoia poems", "*.euo"), ("All files", "*.*")],
        )
        if not path:
            return
        self._current_path = Path(path)
        self._save()

    def _recite(self) -> None:
        source = self._editor.get("1.0", "end-1c").strip()
        if not source:
            self._echo("(even the blank page waits for a word)\n", tag="prompt")
            return
        poem = self._echo_text.yview()[-1] == 1.0
        self._echo("\n>> \n", tag="prompt")
        old = sys.stdout
        sys.stdout = _EchoWriter(self._echo_text)
        try:
            statements = Parser(lex(source)).parse()
            Interpreter().run(statements)
        except (LexError, ParseError, EunoiaError) as exc:
            self._echo(f"(the poem stumbles: {exc})\n", tag="prompt")
        except Exception as exc:  # keep the editor alive, whatever the verse does
            self._echo(f"(the dream coughed up something strange: {exc!r})\n", tag="prompt")
        finally:
            sys.stdout = old
            if poem:
                self._echo_text.see("end")

    def _whisper_soul(self) -> None:
        self._echo("\n" + SOUL + "\n", tag="soul")

    def _clear_echo(self) -> None:
        self._echo_text.configure(state="normal")
        self._echo_text.delete("1.0", "end")
        self._echo_text.configure(state="disabled")

    def _grammar(self) -> None:
        self._echo(
            "the words:\n"
            "  let <name> be <value>         a line of the poem\n"
            "  whisper <value>               say a value without quotes\n"
            "  speak \"...\"                   a line spoken plainly\n"
            "  summon <package>              pip install\n"
            "  embrace <package>             import\n"
            "numbers: two, five, a dozen, one hundred and five...\n"
            "operators: and/with (+), without (-), times (*),\n"
            "  over/shared among (/), keeps (%)\n"
            "no parentheses, no symbols - words and space and a line.\n",
            tag="prompt",
        )

    def _about(self) -> None:
        messagebox.showinfo(
            "About Eunoia",
            f"Eunoia {__version__}\n\n"
            "a programming language whose code reads like poetry.\n"
            "write on the left, recite on the right.\n\n"
            "whisper the soul, and it will whisper back.",
            parent=self,
        )

    # -- plumbing -----------------------------------------------------------

    def _echo(self, text: str, tag: str | None = None) -> None:
        self._echo_text.configure(state="normal")
        self._echo_text.insert("end", text, tag)
        self._echo_text.configure(state="disabled")
        self._echo_text.see("end")

    def _sync_gutter(self, _event=None) -> None:
        count = int(self._editor.index("end-1c").split(".")[0])
        if count != self._last_lines:
            self._gutter.configure(state="normal")
            self._gutter.delete("1.0", "end")
            self._gutter.insert("1.0", "\n".join(str(i) for i in range(1, count + 1)))
            self._gutter.configure(state="disabled")
            self._last_lines = count
        self._gutter.yview_moveto(self._editor.yview()[0])
        self._update_status()

    def _update_status(self) -> None:
        line, col = self._editor.index("insert").split(".")
        self._status_line.set(
            f"{self._current_path.name if self._current_path else 'untitled.euo'}"
            f"   line {line}, column {int(col) + 1}"
        )

    def _on_modified(self, _event=None) -> None:
        if self._editor.edit_modified():
            self._editor.edit_modified(False)
            self._sync_gutter()

    def _on_scroll(self, *args) -> None:
        self._editor.yview(*args)
        self._gutter.yview(*args)

    def _scroll_echo_editor(self, first, last) -> None:
        self._scroll.set(first, last)

    def _scroll_echo_gutter(self, first, last) -> None:
        self._scroll.set(first, last)

    def _on_wheel(self, event) -> None:
        delta = -1 * (event.delta // 120)
        for w in (self._editor, self._gutter):
            w.yview_scroll(delta, "units")
        self._scroll.set(*self._editor.yview())
        return "break"


class _EchoWriter:
    """A paper that catches what the poem prints."""

    def __init__(self, widget: tk.Text) -> None:
        self._widget = widget

    def write(self, text: str) -> int:
        self._widget.configure(state="normal")
        self._widget.insert("end", text)
        self._widget.configure(state="disabled")
        self._widget.see("end")
        return len(text)

    def flush(self) -> None:
        pass


def main() -> int:
    app = EunoiaEditor()
    app.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())