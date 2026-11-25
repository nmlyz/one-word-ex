#!/usr/bin/env python3
"""one-word-ex: write one word describing an ex to a text file.

The entry is a single word, "Subscription". It is the word for the ex
who keeps charging you long after you thought you cancelled: the
cancel button hidden three menus deep, the renewal you never agreed
to, the monthly charge that arrives anyway. The word carries the
whole scene: the trap, the bill, the fight with a form that will not
let go. It needs no caption, and anyone who has ever wrestled a
subscription cancel flow feels the truth in it at once.

The program writes the word, and nothing else, to ``entry.txt``
inside the output directory. By default that directory is ``/output``;
setting ``MAKEFUN_OUTPUT_DIR`` overrides it. The output is exactly
twelve bytes, ``Subscription`` with no trailing newline, and running
the program twice produces byte-identical files.

Standard library only. No network, no arguments, no configuration files.
"""

import os
import sys
from pathlib import Path

# The entry: the one word describing the ex.
WORD = "Subscription"

# The brief allows a single word of one to one hundred and eleven characters.
MIN_WORD_LENGTH = 1
MAX_WORD_LENGTH = 111

# Where the entry goes unless MAKEFUN_OUTPUT_DIR says otherwise.
DEFAULT_OUTPUT_DIR = "/output"
ENTRY_FILENAME = "entry.txt"

# File mode for the written entry, so the grader can read it.
ENTRY_MODE = 0o644


def check_length(text: str) -> str | None:
    """Return an error message if *text* breaks the length rule."""
    if len(text) < MIN_WORD_LENGTH:
        return f"entry is empty, must be at least {MIN_WORD_LENGTH} character"
    if len(text) > MAX_WORD_LENGTH:
        return (
            f"entry is {len(text)} characters, "
            f"must be at most {MAX_WORD_LENGTH}"
        )
    return None


def check_one_word(text: str) -> str | None:
    """Return an error message if *text* is not exactly one word."""
    if "\n" in text or "\r" in text:
        return "entry must be a single line, no line breaks"
    if not text.strip():
        return "entry must not be only white space"
    if text != text.strip():
        return "entry must not start or end with white space"
    if len(text.split()) != 1:
        return "entry must be exactly one word, no spaces"
    return None


def check_letters(text: str) -> str | None:
    """Return an error message if *text* is not plain letters.

    An ex described in one word is a word, not a code or a number:
    digits and punctuation would read as a label, not a description.
    """
    if not text.isalpha():
        return "entry must be letters only, no digits or punctuation"
    return None


# Every check, in the order it is reported.
CHECKS = (check_length, check_one_word, check_letters)


def validate(text: str) -> list[str]:
    """Collect every brief violation for *text* (empty list means valid)."""
    problems = []
    for check in CHECKS:
        problem = check(text)
        if problem is not None:
            problems.append(problem)
    return problems


def resolve_output_dir() -> Path:
    """Return the directory the entry is written into.

    ``MAKEFUN_OUTPUT_DIR`` wins when it is set to a non-empty value;
    an empty value falls back to the default, so an accidental empty
    export can never point the entry at the current directory.
    """
    override = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if override:
        return Path(override)
    return Path(DEFAULT_OUTPUT_DIR)


def write_entry(text: str, path: Path) -> None:
    """Write *text* to *path* exactly as given, no added newline."""
    path.write_text(text, encoding="utf-8")
    # Best effort only: a failed chmod must never fail the run.
    try:
        os.chmod(path, ENTRY_MODE)
    except OSError:
        pass


def run() -> int:
    """Validate the word, write it, and verify what was written."""
    problems = validate(WORD)
    if problems:
        for problem in problems:
            print(problem, file=sys.stderr)
        return 1

    output_dir = resolve_output_dir()
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / ENTRY_FILENAME
    write_entry(WORD, path)

    expected = WORD.encode("utf-8")
    if path.read_bytes() != expected:
        print("wrote back bytes do not match entry", file=sys.stderr)
        return 1

    print(f"wrote {len(WORD)} characters to {path}")
    return 0


def main() -> int:
    """Entry point: exit 0 on success, 1 when the entry is invalid."""
    os.umask(0o022)
    return run()


if __name__ == "__main__":
    sys.exit(main())
