from __future__ import annotations

import os
import sys
import threading
import time
from contextlib import AbstractContextManager
from dataclasses import dataclass
from typing import IO, Callable, Optional


def _isatty(stream: IO[str]) -> bool:
    try:
        return stream.isatty()
    except Exception:
        return False


def _ansi_enabled(stream: IO[str]) -> bool:
    if os.getenv("NO_COLOR") is not None:
        return False
    return _isatty(stream)


@dataclass(frozen=True)
class Ansi:
    enabled: bool

    def wrap(self, s: str, code: str) -> str:
        if not self.enabled:
            return s
        return f"\x1b[{code}m{s}\x1b[0m"

    def dim(self, s: str) -> str:
        return self.wrap(s, "2")

    def red(self, s: str) -> str:
        return self.wrap(s, "31")

    def green(self, s: str) -> str:
        return self.wrap(s, "32")

    def yellow(self, s: str) -> str:
        return self.wrap(s, "33")

    def blue(self, s: str) -> str:
        return self.wrap(s, "34")


class Spinner(AbstractContextManager["Spinner"]):
    _frames = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"

    def __init__(
        self,
        *,
        label: str,
        stream: IO[str] = sys.stderr,
        ansi: Ansi | None = None,
        interval_s: float = 0.08,
    ):
        self._label = label
        self._stream = stream
        self._ansi = ansi or Ansi(enabled=_ansi_enabled(stream))
        self._interval_s = interval_s

        self._stop = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._start = 0.0

    @property
    def ansi(self) -> Ansi:
        return self._ansi

    def __enter__(self) -> "Spinner":
        self._start = time.perf_counter()
        if _isatty(self._stream):
            self._thread = threading.Thread(target=self._run, daemon=True)
            self._thread.start()
        else:
            # Non-tty: just print a single line.
            self._stream.write(f"{self._label}\n")
            self._stream.flush()
        return self

    def _run(self) -> None:
        i = 0
        while not self._stop.is_set():
            frame = self._frames[i % len(self._frames)]
            line = f"{frame} {self._label}"
            if self._ansi.enabled:
                line = self._ansi.dim(line)
            self._stream.write("\r" + line)
            self._stream.flush()
            time.sleep(self._interval_s)
            i += 1

    def succeed(self, message: str | None = None) -> None:
        self._finish(ok=True, message=message)

    def fail(self, message: str | None = None) -> None:
        self._finish(ok=False, message=message)

    def _finish(self, *, ok: bool, message: str | None) -> None:
        elapsed = time.perf_counter() - self._start
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=0.5)

        if _isatty(self._stream):
            # Clear spinner line
            self._stream.write("\r\x1b[2K")

        icon = "✔" if ok else "✖"
        icon = self._ansi.green(icon) if ok else self._ansi.red(icon)

        final = message or self._label
        duration = self._ansi.dim(f"({elapsed:.1f}s)")
        self._stream.write(f"{icon} {final} {duration}\n")
        self._stream.flush()

    def __exit__(self, exc_type, exc, tb) -> bool:
        if exc is None:
            self.succeed()
            return False
        self.fail(f"{self._label} failed")
        return False


class Step(Spinner):
    """Alias kept for readability at call sites."""


def header(title: str, *, stream: IO[str] = sys.stderr) -> None:
    ansi = Ansi(enabled=_ansi_enabled(stream))
    stream.write(ansi.blue(title) + "\n")
    stream.flush()


def info(msg: str, *, stream: IO[str] = sys.stderr) -> None:
    ansi = Ansi(enabled=_ansi_enabled(stream))
    stream.write(ansi.dim(msg) + "\n")
    stream.flush()
