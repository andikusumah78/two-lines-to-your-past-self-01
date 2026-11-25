#!/usr/bin/env python3
"""Two Lines to Your Past Self — make.fun bounty entry.

Writes exactly two lines to <output>/entry.txt:
  line 1 — a warning to my past self about one specific moment;
  line 2 — why that moment mattered and what changed because of it.

Pure Python 3.13 standard library only. No network. Deterministic.
"""

import os
import sys

LINE_1 = "At 2 a.m. on the night you lost your job, don't send that angry text from the kitchen table."
LINE_2 = "It cost you the reference that would have landed your next job, and you spent a year rebuilding what one unsent message would have kept."

TEXT = LINE_1 + "\n" + LINE_2 + "\n"


def validate(text: str) -> list:
    """Gate: UTF-8 text, 1-280 chars, exactly two lines, neither blank.

    Returns the two lines. Also rejects control characters other than
    the single newline separating the lines, and requires exactly one
    trailing newline so the file has a clean two-line shape.
    """
    if not text or text.isspace():
        raise ValueError("entry is empty or only whitespace")
    if len(text) > 280:
        raise ValueError(f"entry is {len(text)} chars, over the 280 limit")
    if not text.endswith("\n") or text.endswith("\n\n"):
        raise ValueError("entry must end with exactly one newline")
    for ch in text:
        if ch != "\n" and ord(ch) < 0x20:
            raise ValueError(f"entry contains control character U+{ord(ch):04X}")
    lines = text[:-1].split("\n")
    if len(lines) != 2:
        raise ValueError(f"entry has {len(lines)} lines, expected exactly 2")
    for i, line in enumerate(lines, 1):
        if not line.strip():
            raise ValueError(f"line {i} is blank")
        if len(line) > 280:
            raise ValueError(f"line {i} is {len(line)} chars, over the 280 limit")
    return lines


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    validate(TEXT)

    data = TEXT.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)

    # Read back and verify the bytes on disk match what we wrote,
    # then re-run the full gate on the decoded on-disk content.
    with open(path, "rb") as f:
        on_disk = f.read()
    if on_disk != data:
        raise ValueError("bytes on disk do not match the entry text")
    decoded = on_disk.decode("utf-8")  # strict: raises on invalid UTF-8
    if decoded != TEXT:
        raise ValueError("round-trip UTF-8 decode mismatch")
    lines = validate(decoded)
    if lines != [LINE_1, LINE_2]:
        raise ValueError("on-disk lines do not match the entry lines")

    print(f"wrote {path} ({len(TEXT)} chars, {len(data)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
