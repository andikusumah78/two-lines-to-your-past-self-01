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


def validate(text: str) -> None:
    """Gate: UTF-8 text, 1-280 chars, exactly two lines, neither blank."""
    if not text or text.isspace():
        raise ValueError("entry is empty or only whitespace")
    if len(text) > 280:
        raise ValueError(f"entry is {len(text)} chars, over the 280 limit")
    lines = text.split("\n")
    # trailing newline leaves a final empty element; strip it for the count
    if lines and lines[-1] == "":
        lines = lines[:-1]
    if len(lines) != 2:
        raise ValueError(f"entry has {len(lines)} lines, expected exactly 2")
    for i, line in enumerate(lines, 1):
        if not line.strip():
            raise ValueError(f"line {i} is blank")


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    validate(TEXT)

    data = TEXT.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)

    # Read back and verify the bytes on disk match what we wrote.
    with open(path, "rb") as f:
        on_disk = f.read()
    if on_disk != data:
        raise ValueError("bytes on disk do not match the entry text")
    if on_disk.decode("utf-8") != TEXT:
        raise ValueError("round-trip UTF-8 decode mismatch")

    print(f"wrote {path} ({len(TEXT)} chars, {len(data)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
