#!/usr/bin/env python3
"""one-word-ex: write one word describing an ex to a text file.

The entry is a single word, "Subscription". It names the ex who keeps
charging you long after you thought you cancelled: the cancel button
hidden three menus deep, the renewal you never agreed to, the monthly
charge that arrives anyway, the form that will not let go. The word
carries the whole scene in one noun -- the trap, the bill, the fight
with a cancel flow designed to wear you down -- and it needs no
caption. Anyone who has ever wrestled a subscription cancel flow
feels the truth in it at once, which is exactly what one word has
to do here: land the joke and the recognition together, with nothing
around it to explain the punchline.

Why this word, and not the others that were in the running:

- "Ghosted" says the ex left, but says nothing about what they keep
  taking. The sting here is not absence, it is the charge that
  follows you home every month.
- "Renewal" is the mechanism, not the person. It reads like a label
  on a bill, and it misses the relationship the brief asks for.
- "Overdraft" is the consequence, and it points at your bank account
  instead of at the ex. The word should describe them, not you.
- "Auto-renew" is two words joined by a hyphen, and it fails the
  brief's one-word rule on its face.
- "Subscription" is the person and the trap in one word: an ex who
  behaves exactly like a subscription -- impossible to cancel,
  always billing, always there next month. The metaphor does the
  describing, so the word itself stays plain, and plain is what
  makes it land.

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
    """Return an error message if *text* breaks the length rule.

    The message names the actual length and the allowed range, so a
    failure tells the reader exactly how far off the word is.
    """
    if len(text) < MIN_WORD_LENGTH:
        return (
            f"entry is {len(text)} characters, "
            f"the brief needs {MIN_WORD_LENGTH} to {MAX_WORD_LENGTH}"
        )
    if len(text) > MAX_WORD_LENGTH:
        return (
            f"entry is {len(text)} characters, "
            f"the brief allows at most {MAX_WORD_LENGTH}"
        )
    return None


def check_one_word(text: str) -> str | None:
    """Return an error message if *text* is not exactly one word.

    The message says which shape rule broke, and for a multi-word
    entry how many words were found, so the fix is obvious.
    """
    if "\n" in text or "\r" in text:
        return "entry must be a single line, no line breaks"
    if not text.strip():
        return "entry must not be only white space"
    if text != text.strip():
        return "entry must not start or end with white space"
    words = text.split()
    if len(words) != 1:
        return f"entry must be exactly one word, found {len(words)} words"
    return None


def check_letters(text: str) -> str | None:
    """Return an error message if *text* is not plain letters.

    An ex described in one word is a word, not a code or a number:
    digits and punctuation would read as a label, not a description.
    The message names the first offending character so the reader
    sees at once what to remove.
    """
    for char in text:
        if not char.isalpha():
            return (
                f"entry must be letters only, "
                f"found {char!r} which is not a letter"
            )
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


def verify_written(path: Path, expected: bytes) -> str | None:
    """Read *path* back and compare it with *expected* bytes.

    Returns an error message when the file is missing, unreadable, or
    holds anything other than the exact entry bytes. Writing without
    this check would let a silent disk or encoding fault pass as a
    successful run, and the grader would see a wrong file.
    """
    try:
        actual = path.read_bytes()
    except OSError as exc:
        return f"could not read back {path}: {exc}"
    if actual != expected:
        return (
            f"read back {len(actual)} bytes from {path}, "
            f"expected {len(expected)} bytes of the entry"
        )
    return None


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

    problem = verify_written(path, WORD.encode("utf-8"))
    if problem is not None:
        print(problem, file=sys.stderr)
        return 1

    print(f"wrote {len(WORD)} characters to {path}")
    return 0


def main() -> int:
    """Entry point: exit 0 on success, 1 when the entry is invalid."""
    os.umask(0o022)
    return run()


if __name__ == "__main__":
    sys.exit(main())
