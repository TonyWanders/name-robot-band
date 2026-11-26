#!/usr/bin/env python3
"""Write one funny robot band name and its hit song to /output/entry.txt.

Deterministic: no network, no clock, no randomness. The entry is a fixed
string. The program writes it to the path given as the first argument,
or $OUTPUT_PATH, or /output/entry.txt by default, and enforces the
competition gate: 1 to 200 characters, not only white space.
"""

import os
import sys
from pathlib import Path

ENTRY = (
    "The Roombas, whose hit 'Bump Into You' is a love song about "
    "crashing into the same wall every night."
)

MIN_CHARS = 1
MAX_CHARS = 200
DEFAULT_PATH = "/output/entry.txt"


def resolve_output_path(argv, env) -> Path:
    """Pick the output path: argv[1], then $OUTPUT_PATH, then the default."""
    if len(argv) > 1:
        return Path(argv[1])
    env_path = env.get("OUTPUT_PATH")
    if env_path:
        return Path(env_path)
    return Path(DEFAULT_PATH)


def write_entry(text: str, path: Path) -> None:
    """Write the entry exactly as given, creating parent dirs if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def validate(text: str) -> int:
    """Enforce the competition gate: 1 to 200 chars, not only white space.

    Returns the character count. Raises ValueError when the gate fails.
    """
    chars = len(text)
    if not (MIN_CHARS <= chars <= MAX_CHARS):
        raise ValueError(f"entry is {chars} characters, outside 1-200")
    if not text.strip():
        raise ValueError("entry is only white space")
    return chars


def main() -> int:
    try:
        chars = validate(ENTRY)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1

    path = resolve_output_path(sys.argv, os.environ)
    write_entry(ENTRY, path)
    print(f"wrote {chars} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
